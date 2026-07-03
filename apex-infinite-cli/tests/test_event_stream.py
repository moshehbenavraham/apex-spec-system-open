"""Event stream fixtures and tests."""

import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

import apex_infinite.cli as apex_infinite
from apex_infinite.events import (
    EventEmitter,
    EventStreamError,
    NoOpEventEmitter,
    open_event_stream,
)
from apex_infinite.ui import NoHumanOutputRenderer

CONFIG_TEXT = """provider: ollama
codex:
  binary: "codex"
  exec_flags: "--dangerously-auto-approve"
  model_reasoning_effort: "high"
ui:
  theme: "auto"
  effect_level: "low"
  ascii: false
  compact: false
  show_elapsed: true
  show_provider: true
  themes: {}
providers:
  ollama:
    base_url: "http://localhost:11434/v1"
    api_key: "ollama"
    model: "qwen2.5:7b"
"""


@dataclass
class FakeEmitter:
    """Small event emitter test double for CLI wiring tests."""

    events: list[tuple[str, dict[str, object]]] = field(default_factory=list)
    closed: bool = False

    def emit(self, name, payload=None):
        """Capture emitted event facts."""
        self.events.append((name, dict(payload or {})))

    def close(self):
        """Mark the fake emitter closed."""
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc, _traceback):
        self.close()
        return False


@pytest.fixture
def cli_config_path(tmp_path):
    """Write a minimal CLI config file."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(CONFIG_TEXT, encoding="ascii")
    return config_path


@pytest.fixture
def cli_project_path(tmp_path):
    """Create an isolated project directory for CliRunner tests."""
    project_path = tmp_path / "project"
    project_path.mkdir()
    return project_path


@pytest.fixture
def event_file_path(tmp_path):
    """Return a temporary JSONL event path."""
    return tmp_path / "events.jsonl"


@pytest.fixture
def fake_llm_decision():
    """Return a deterministic manager decision for dry-run loop tests."""
    return {"output": "alldonebaby", "reason": "complete"}


@pytest.fixture
def fake_codex_process():
    """Return a deterministic subprocess result factory."""

    def factory(stdout="agent output\n", stderr="", returncode=0):
        return apex_infinite.CodexProcessResult(
            stdout=stdout,
            stderr=stderr,
            returncode=returncode,
        )

    return factory


@pytest.fixture
def fake_emitter():
    """Return a fake emitter that records events and cleanup."""
    return FakeEmitter()


def read_jsonl(path: Path):
    """Read one JSON object per line from a JSONL file."""
    text = path.read_text(encoding="ascii")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


class FlushTrackingStream:
    """Text stream test double that records writes, flushes, and close calls."""

    def __init__(self):
        self.parts = []
        self.flush_count = 0
        self.closed = False

    def write(self, text):
        """Capture text writes."""
        if self.closed:
            raise ValueError("stream is closed")
        self.parts.append(text)
        return len(text)

    def flush(self):
        """Capture flush calls."""
        self.flush_count += 1

    def close(self):
        """Capture close calls."""
        self.closed = True

    @property
    def text(self):
        """Return all text written so far."""
        return "".join(self.parts)


class RecordingEmitter:
    """Capture real runtime event emissions."""

    enabled = True

    def __init__(self):
        self.events = []

    def emit(self, name, payload=None):
        self.events.append((name, dict(payload or {})))

    @property
    def names(self):
        return [name for name, _payload in self.events]


def make_loop_config():
    """Return a minimal runtime config for infinite_loop tests."""
    return {
        "provider": "ollama",
        "codex": {"binary": "codex", "exec_flags": "--test"},
        "providers": {
            "ollama": {
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama",
                "model": "qwen2.5:7b",
            }
        },
    }


def test_event_emitter_writes_one_json_object_per_line_and_flushes():
    stream = FlushTrackingStream()
    emitter = EventEmitter(stream, close_stream=False)

    emitter.emit(
        "startup_begin",
        {"project_path": "/tmp/project/", "dry_run": True, "iteration": 1},
    )
    emitter.emit("history_fetched", {"record_count": 0})

    lines = stream.text.splitlines()
    assert len(lines) == 2
    assert stream.flush_count == 2
    first = json.loads(lines[0])
    second = json.loads(lines[1])
    assert first["version"] == 1
    assert first["event"] == "startup_begin"
    assert first["payload"] == {
        "project_path": "/tmp/project/",
        "dry_run": True,
        "iteration": 1,
    }
    assert second["event"] == "history_fetched"


def test_event_emitter_closes_owned_stream_on_context_exit():
    stream = FlushTrackingStream()

    with EventEmitter(stream, close_stream=True) as emitter:
        emitter.emit("run_stopped", {"reason": "done"})

    assert stream.closed is True


def test_noop_event_emitter_accepts_events_without_writing():
    stream = FlushTrackingStream()
    emitter = NoOpEventEmitter()

    emitter.emit("startup_begin", {"project_path": "/tmp/project/"})
    emitter.close()

    assert stream.text == ""


def test_open_event_stream_writes_file_jsonl(event_file_path):
    with open_event_stream(str(event_file_path)) as emitter:
        emitter.emit("config_loaded", {"config_path": "config.yaml"})
        emitter.emit("ui_resolved", {"theme_name": "plain"})

    rows = read_jsonl(event_file_path)
    assert [row["event"] for row in rows] == ["config_loaded", "ui_resolved"]


def test_open_event_stream_stdout_uses_provided_stdout(capsys):
    with open_event_stream("-", stdout_allowed=True) as emitter:
        emitter.emit("run_stopped", {"reason": "dry-run"})

    rows = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert rows[0]["event"] == "run_stopped"
    assert rows[0]["payload"] == {"reason": "dry-run"}


@pytest.mark.parametrize("event_name", ["", "bad event", "unknown_event"])
def test_event_emitter_rejects_invalid_event_names(event_name):
    stream = FlushTrackingStream()
    emitter = EventEmitter(stream)

    with pytest.raises(EventStreamError, match="event name"):
        emitter.emit(event_name, {})


def test_event_emitter_rejects_non_json_payload_values():
    stream = FlushTrackingStream()
    emitter = EventEmitter(stream)

    with pytest.raises(EventStreamError, match="JSON"):
        emitter.emit("startup_begin", {"path": Path("/tmp/project")})


@pytest.mark.parametrize(
    "bad_value",
    [
        "\x1b[31mred\x1b[0m",
        "[bold]markup[/bold]",
        chr(0x2500),
        "token accent=green",
        "sk-1234567890abcdef1234567890abcdef12345678",
        "Bearer abcdef1234567890",
    ],
)
def test_event_emitter_rejects_unsafe_payload_strings(bad_value):
    stream = FlushTrackingStream()
    emitter = EventEmitter(stream)

    with pytest.raises(EventStreamError):
        emitter.emit("startup_begin", {"value": bad_value})


def test_emit_event_surfaces_human_write_failure_without_raising():
    class FailingEmitter:
        enabled = True

        def emit(self, _name, _payload=None):
            raise EventStreamError("disk full")

    class CapturingRenderer:
        def __init__(self):
            self.errors = []

        def print_error(self, message, title="Error"):
            self.errors.append((title, message))

    renderer = CapturingRenderer()

    apex_infinite._emit_event(  # pylint: disable=protected-access
        FailingEmitter(),
        "startup_begin",
        {"machine_output": False},
        renderer=renderer,
        machine_output=False,
    )

    assert renderer.errors == [("Event Stream", "Event stream error: disk full")]


def test_emit_event_reports_machine_write_failure_when_possible():
    class FailingOnceEmitter:
        enabled = True

        def __init__(self):
            self.events = []

        def emit(self, name, payload=None):
            if not self.events:
                self.events.append((name, dict(payload or {})))
                raise EventStreamError("pipe closed")
            self.events.append((name, dict(payload or {})))

    emitter = FailingOnceEmitter()

    apex_infinite._emit_event(  # pylint: disable=protected-access
        emitter,
        "startup_begin",
        {"machine_output": True},
        machine_output=True,
    )

    assert emitter.events[1][0] == "event_stream_error"
    assert emitter.events[1][1]["source_event"] == "startup_begin"


def test_infinite_loop_emits_completion_event_order(monkeypatch, tmp_path):
    events = RecordingEmitter()
    db_calls = []
    config = make_loop_config()

    monkeypatch.setattr(
        apex_infinite, "get_llm_client", lambda _config: ("client", "model")
    )
    monkeypatch.setattr(apex_infinite, "db_fetch_history", lambda _path, limit=15: [])
    monkeypatch.setattr(
        apex_infinite,
        "llm_summarize",
        lambda _client, _model, _records, renderer=None: "summary",
    )
    monkeypatch.setattr(
        apex_infinite,
        "llm_manager_decide",
        lambda _client, _model, _agent_response, _ceo_msg, _summary, renderer=None: {
            "output": "alldonebaby",
            "reason": "complete",
        },
    )
    monkeypatch.setattr(
        apex_infinite,
        "db_log",
        lambda *args, **kwargs: db_calls.append((args, kwargs)),
    )
    monkeypatch.setattr(
        apex_infinite,
        "notify",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("notifications disabled")
        ),
    )

    apex_infinite.infinite_loop(
        path=f"{tmp_path}/project/",
        config=config,
        max_iterations=1,
        dry_run=True,
        renderer=NoHumanOutputRenderer(),
        event_emitter=events,
        machine_output=True,
        notifications_enabled=False,
    )

    assert events.names == [
        "iteration_started",
        "history_fetched",
        "history_summarize_started",
        "history_summarize_finished",
        "manager_decision_started",
        "manager_decision_finished",
        "workflow_completed",
        "db_log_started",
        "db_log_finished",
        "run_stopped",
    ]
    assert db_calls[0][0][2] == "alldonebaby"


def test_infinite_loop_emits_prompt_db_and_max_iteration_events(monkeypatch, tmp_path):
    events = RecordingEmitter()
    db_calls = []
    config = make_loop_config()

    monkeypatch.setattr(
        apex_infinite, "get_llm_client", lambda _config: ("client", "model")
    )
    monkeypatch.setattr(apex_infinite, "db_fetch_history", lambda _path, limit=15: [])
    monkeypatch.setattr(
        apex_infinite,
        "llm_summarize",
        lambda _client, _model, _records, renderer=None: "summary",
    )
    monkeypatch.setattr(
        apex_infinite,
        "llm_manager_decide",
        lambda _client, _model, _agent_response, _ceo_msg, _summary, renderer=None: {
            "output": "implement",
            "reason": "continue",
        },
    )
    monkeypatch.setattr(
        apex_infinite,
        "db_log",
        lambda *args, **kwargs: db_calls.append((args, kwargs)),
    )
    monkeypatch.setattr(
        apex_infinite,
        "notify",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("notifications disabled")
        ),
    )

    apex_infinite.infinite_loop(
        path=f"{tmp_path}/project/",
        config=config,
        max_iterations=1,
        dry_run=True,
        renderer=NoHumanOutputRenderer(),
        event_emitter=events,
        machine_output=True,
        notifications_enabled=False,
    )

    for expected in [
        "prompt_built",
        "prompt_dispatched",
        "codex_dry_run",
        "response_summarized",
        "db_log_started",
        "db_log_finished",
        "max_iterations_reached",
        "run_stopped",
    ]:
        assert expected in events.names
    assert db_calls[0][0][2] == "implement"


def test_infinite_loop_emits_error_event_before_reraising_llm_failure(
    monkeypatch, tmp_path
):
    events = RecordingEmitter()
    config = make_loop_config()

    monkeypatch.setattr(
        apex_infinite, "get_llm_client", lambda _config: ("client", "model")
    )
    monkeypatch.setattr(
        apex_infinite,
        "db_fetch_history",
        lambda _path, limit=15: [{"id": 1, "cc_response": "prior"}],
    )

    def fail_summarize(*_args, **_kwargs):
        raise RuntimeError("provider down")

    monkeypatch.setattr(apex_infinite, "llm_summarize", fail_summarize)

    with pytest.raises(RuntimeError, match="provider down"):
        apex_infinite.infinite_loop(
            path=f"{tmp_path}/project/",
            config=config,
            max_iterations=1,
            dry_run=True,
            renderer=NoHumanOutputRenderer(),
            event_emitter=events,
            machine_output=True,
            notifications_enabled=False,
        )

    assert events.names[-1] == "error"
    assert events.events[-1][1] == {
        "stage": "history_summary",
        "iteration": 1,
        "error_type": "RuntimeError",
    }


def test_infinite_loop_emits_help_and_interrupt_events(monkeypatch, tmp_path):
    events = RecordingEmitter()
    db_calls = []
    config = make_loop_config()

    monkeypatch.setattr(
        apex_infinite, "get_llm_client", lambda _config: ("client", "model")
    )
    monkeypatch.setattr(apex_infinite, "db_fetch_history", lambda _path, limit=15: [])
    monkeypatch.setattr(
        apex_infinite,
        "llm_summarize",
        lambda _client, _model, _records, renderer=None: "summary",
    )
    monkeypatch.setattr(
        apex_infinite,
        "llm_manager_decide",
        lambda _client, _model, _agent_response, _ceo_msg, _summary, renderer=None: {
            "output": "help",
            "reason": "need operator",
        },
    )
    monkeypatch.setattr(
        apex_infinite,
        "db_log",
        lambda *args, **kwargs: db_calls.append((args, kwargs)),
    )
    monkeypatch.setattr(apex_infinite.console, "input", lambda _prompt: "quit")
    monkeypatch.setattr(
        apex_infinite,
        "notify",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("notifications disabled")
        ),
    )

    apex_infinite.infinite_loop(
        path=f"{tmp_path}/project/",
        config=config,
        max_iterations=1,
        dry_run=True,
        renderer=NoHumanOutputRenderer(),
        event_emitter=events,
        machine_output=True,
        notifications_enabled=False,
    )

    assert "help_requested" in events.names
    assert "operator_input_received" in events.names
    assert events.names[-1] == "run_stopped"
    assert db_calls[0][0][2] == "help"
