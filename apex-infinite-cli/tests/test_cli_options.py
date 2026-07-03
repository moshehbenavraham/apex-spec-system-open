"""Click option wiring tests for display settings."""

import io
import json

import pytest
from click.testing import CliRunner

import apex_infinite.cli as apex_infinite

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

OLLAMA_ENV_CONFIG_TEXT = """provider: ollama
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
    base_url: "http://${OLLAMA_HOST}:${OLLAMA_PORT}/v1"
    api_key: "${OLLAMA_API_KEY}"
    model: "${OLLAMA_MODEL}"
"""


def write_config(tmp_path, text=CONFIG_TEXT):
    """Write a config file for CLI tests."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(text, encoding="ascii")
    return config_path


def clear_ollama_env(monkeypatch):
    """Clear Ollama env vars so config tests use explicit fixtures."""
    for name in ("OLLAMA_HOST", "OLLAMA_PORT", "OLLAMA_API_KEY", "OLLAMA_MODEL"):
        monkeypatch.delenv(name, raising=False)


def prepare_cli(monkeypatch, tmp_path):
    """Patch stateful CLI boundaries and return test paths plus captured loop data."""
    config_path = write_config(tmp_path)
    project_path = tmp_path / "project"
    project_path.mkdir()
    captured = {}

    def fake_loop(**kwargs):
        captured.update(kwargs)

    def fake_preflight(config, check_completion=False):
        provider_name = config["provider"]
        provider = config["providers"][provider_name]
        captured.setdefault("preflight_calls", []).append(check_completion)
        return apex_infinite.ProviderPreflightResult(
            provider_name=provider_name,
            base_url=provider["base_url"],
            model_name=provider["model"],
            model_count=1,
            completion_checked=check_completion,
        )

    monkeypatch.setattr(apex_infinite, "DB_DIR", tmp_path / "db")
    monkeypatch.setattr(apex_infinite, "DB_PATH", tmp_path / "db" / "history.db")
    monkeypatch.setattr(apex_infinite, "infinite_loop", fake_loop)
    monkeypatch.setattr(apex_infinite, "run_provider_preflight", fake_preflight)
    return config_path, project_path, captured


def invoke_cli(monkeypatch, tmp_path, args):
    """Invoke the CLI with an isolated config, project, DB, and loop."""
    config_path, project_path, captured = prepare_cli(monkeypatch, tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--path",
            str(project_path),
            *args,
        ],
    )
    return result, captured, project_path


def jsonl_rows(text):
    """Parse non-empty JSONL output lines."""
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def test_load_config_uses_ollama_env_defaults(monkeypatch, tmp_path):
    clear_ollama_env(monkeypatch)
    config_path = write_config(tmp_path, OLLAMA_ENV_CONFIG_TEXT)

    config = apex_infinite.load_config(config_path)
    provider = config["providers"]["ollama"]

    assert provider["base_url"] == "http://localhost:11434/v1"
    assert provider["api_key"] == "ollama"
    assert provider["model"] == "qwen2.5:7b"


def test_load_config_reads_ollama_env_file(monkeypatch, tmp_path):
    clear_ollama_env(monkeypatch)
    config_path = write_config(tmp_path, OLLAMA_ENV_CONFIG_TEXT)
    (tmp_path / ".env").write_text(
        "\n".join(
            [
                "OLLAMA_HOST=127.0.0.1",
                "OLLAMA_PORT=11500",
                "OLLAMA_API_KEY=local-test-key",
                "OLLAMA_MODEL=llama3.1:8b",
                "",
            ]
        ),
        encoding="ascii",
    )

    config = apex_infinite.load_config(config_path)
    provider = config["providers"]["ollama"]

    assert provider["base_url"] == "http://127.0.0.1:11500/v1"
    assert provider["api_key"] == "local-test-key"
    assert provider["model"] == "llama3.1:8b"


def test_theme_flag_reaches_resolved_renderer(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--theme", "crt-amber", "--max-iterations", "0"],
    )

    assert result.exit_code == 0
    assert captured["renderer"].settings.requested_theme == "crt-amber"
    assert captured["renderer"].settings.theme_name == "crt-amber"


def test_plain_ascii_and_compact_flags_reach_loop(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--plain", "--ascii", "--compact", "--max-iterations", "0"],
    )

    assert result.exit_code == 0
    settings = captured["renderer"].settings
    assert settings.plain is True
    assert settings.theme_name == "plain"
    assert settings.ascii_only is True
    assert settings.compact is True


def test_invalid_theme_fails_before_loop(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--theme", "missing", "--max-iterations", "0"],
    )

    assert result.exit_code == 1
    assert captured == {}


def test_dry_run_startup_wiring_reaches_loop(monkeypatch, tmp_path):
    result, captured, project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--start", "implement", "--dry-run", "--theme", "crt-green"],
    )

    assert result.exit_code == 0
    assert captured["path"] == f"{project_path}/"
    assert captured["start_command"] == "implement"
    assert captured["dry_run"] is True
    assert captured["renderer"].settings.theme_name == "crt-green"


def test_event_stream_path_writes_startup_events_and_reaches_loop(
    monkeypatch, tmp_path
):
    event_path = tmp_path / "events.jsonl"

    result, captured, project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        [
            "--start",
            "implement",
            "--dry-run",
            "--event-stream",
            str(event_path),
        ],
    )

    assert result.exit_code == 0
    assert captured["event_emitter"].enabled is True
    assert captured["machine_output"] is False
    assert captured["notifications_enabled"] is True
    assert captured["path"] == f"{project_path}/"
    rows = jsonl_rows(event_path.read_text(encoding="ascii"))
    assert [row["event"] for row in rows[:4]] == [
        "startup_begin",
        "config_loaded",
        "ui_resolved",
        "project_resolved",
    ]
    assert rows[-1]["event"] == "startup"


def test_event_stream_stdout_requires_machine_output(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--event-stream", "-"],
    )

    assert result.exit_code == 2
    assert "--event-stream - requires --machine-output" in result.output
    assert captured == {}


def test_machine_output_requires_event_stream(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--machine-output"],
    )

    assert result.exit_code == 2
    assert "--machine-output requires --event-stream" in result.output
    assert captured == {}


def test_machine_output_stdout_is_jsonl_only(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--event-stream", "-", "--machine-output", "--max-iterations", "0"],
    )

    assert result.exit_code == 0
    assert "BOOT" not in result.output
    assert "Apex Infinite Operator Console" not in result.output
    rows = jsonl_rows(result.output)
    assert rows
    assert all("event" in row and "payload" in row for row in rows)
    assert [row["event"] for row in rows[:3]] == [
        "startup_begin",
        "config_loaded",
        "ui_resolved",
    ]
    assert captured["machine_output"] is True
    assert captured["notifications_enabled"] is False


def test_machine_output_startup_error_is_jsonl_only(monkeypatch, tmp_path):
    project_path = tmp_path / "project"
    project_path.mkdir()
    missing_config = tmp_path / "missing.yaml"
    monkeypatch.setattr(apex_infinite, "DB_DIR", tmp_path / "db")
    monkeypatch.setattr(apex_infinite, "DB_PATH", tmp_path / "db" / "history.db")

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(missing_config),
            "--path",
            str(project_path),
            "--event-stream",
            "-",
            "--machine-output",
        ],
    )

    assert result.exit_code == 1
    rows = jsonl_rows(result.output)
    assert [row["event"] for row in rows] == ["startup_begin", "error"]
    assert rows[-1]["payload"]["stage"] == "config"
    assert rows[-1]["payload"]["message"] == f"Config file not found: {missing_config}"


def test_event_stream_open_error_is_click_error_without_traceback(
    monkeypatch, tmp_path
):
    event_path = tmp_path / "events-as-directory"
    event_path.mkdir()

    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--event-stream", str(event_path)],
    )

    assert result.exit_code == 1
    assert "failed to open event stream" in result.output
    assert "Traceback" not in result.output
    assert captured == {}


def test_check_provider_flag_runs_preflight_without_project_path(monkeypatch, tmp_path):
    config_path = write_config(tmp_path)
    captured = {}

    def fake_loop(**_kwargs):
        raise AssertionError("check-provider mode should not start the loop")

    def fake_preflight(config, check_completion=False):
        provider_name = config["provider"]
        provider = config["providers"][provider_name]
        captured["provider_name"] = provider_name
        captured["model_name"] = provider["model"]
        captured["completion_check"] = check_completion
        return apex_infinite.ProviderPreflightResult(
            provider_name=provider_name,
            base_url=provider["base_url"],
            model_name=provider["model"],
            model_count=1,
            completion_checked=check_completion,
        )

    monkeypatch.setattr(apex_infinite, "DB_DIR", tmp_path / "db")
    monkeypatch.setattr(apex_infinite, "DB_PATH", tmp_path / "db" / "history.db")
    monkeypatch.setattr(apex_infinite, "infinite_loop", fake_loop)
    monkeypatch.setattr(apex_infinite, "run_provider_preflight", fake_preflight)

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--check-provider",
            "--check-provider-chat",
            "--plain",
        ],
    )

    assert result.exit_code == 0
    assert captured == {
        "provider_name": "ollama",
        "model_name": "qwen2.5:7b",
        "completion_check": True,
    }
    assert "Provider Preflight" in result.output


def test_startup_provider_preflight_runs_before_loop(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--check-provider-chat", "--max-iterations", "0"],
    )

    assert result.exit_code == 0
    assert captured["preflight_calls"] == [True]
    assert "path" in captured


def test_skip_provider_check_reaches_loop_without_preflight(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--skip-provider-check", "--max-iterations", "0"],
    )

    assert result.exit_code == 0
    assert "preflight_calls" not in captured
    assert "path" in captured


def test_provider_preflight_failure_stops_before_loop(monkeypatch, tmp_path):
    config_path, project_path, captured = prepare_cli(monkeypatch, tmp_path)

    def fail_preflight(_config, check_completion=False):
        raise apex_infinite.CliStartupError("local provider is down")

    monkeypatch.setattr(apex_infinite, "run_provider_preflight", fail_preflight)

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--path",
            str(project_path),
            "--plain",
        ],
    )

    assert result.exit_code == 1
    assert "local provider is down" in result.output
    assert captured == {}


def test_check_provider_conflicts_with_skip_provider_check(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--check-provider", "--skip-provider-check"],
    )

    assert result.exit_code == 2
    assert "--check-provider cannot be combined" in result.output
    assert captured == {}


@pytest.mark.parametrize(
    ("extra_args", "env"),
    [
        ([], {}),
        (["--plain"], {}),
        (["--ascii"], {}),
        (["--compact"], {}),
        ([], {"NO_COLOR": "1"}),
        ([], {"TERM": "dumb"}),
    ],
)
def test_event_stream_file_coexists_with_human_output_modes(
    monkeypatch, tmp_path, extra_args, env
):
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    event_path = tmp_path / f"events-{len(extra_args)}-{len(env)}.jsonl"

    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        [
            "--event-stream",
            str(event_path),
            "--max-iterations",
            "0",
            *extra_args,
        ],
    )

    assert result.exit_code == 0
    assert "Apex Infinite Operator Console" in result.output
    assert captured["machine_output"] is False
    rows = jsonl_rows(event_path.read_text(encoding="ascii"))
    assert rows[0]["event"] == "startup_begin"
    assert rows[-1]["event"] == "startup"


def test_notify_does_not_emit_terminal_bell_to_redirected_stdout(monkeypatch):
    stream = io.StringIO()
    calls = []

    monkeypatch.setattr(apex_infinite.sys, "stdout", stream)
    monkeypatch.setattr(
        apex_infinite.subprocess,
        "run",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )

    apex_infinite.notify("Apex Infinite", "Reached max iterations")

    assert "\a" not in stream.getvalue()
    assert calls


def test_history_mode_uses_renderer_and_does_not_start_loop(monkeypatch, tmp_path):
    config_path, project_path, captured = prepare_cli(monkeypatch, tmp_path)
    history_call = {}

    def fake_history(path=None, renderer=None, verbose=False):
        history_call["path"] = path
        history_call["renderer"] = renderer
        history_call["verbose"] = verbose

    monkeypatch.setattr(apex_infinite, "db_show_history", fake_history)

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--path",
            str(project_path),
            "--history",
            "--verbose",
            "--plain",
        ],
    )

    assert result.exit_code == 0
    assert captured == {}
    assert history_call["path"] == str(project_path)
    assert history_call["verbose"] is True
    assert history_call["renderer"].settings.plain is True


def test_history_verbose_does_not_register_duplicate_flag(monkeypatch, tmp_path):
    config_path, project_path, captured = prepare_cli(monkeypatch, tmp_path)

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--path",
            str(project_path),
            "--history-verbose",
        ],
    )

    assert result.exit_code == 2
    assert "No such option '--history-verbose'" in result.output
    assert captured == {}


def test_infinite_loop_passes_operator_context_to_renderer(monkeypatch):
    captured = {"iterations": [], "logs": [], "db": []}
    config = {
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

    class CapturingRenderer:
        """Capture renderer snapshots without printing terminal output."""

        def print_iteration(self, snapshot):
            captured["iterations"].append(snapshot)

        def print_status(self, *_args, **_kwargs):
            return None

        def print_manager_decision(self, *_args, **_kwargs):
            return None

        def print_completion(self, *_args, **_kwargs):
            return None

        def print_db_log(self, snapshot):
            captured["logs"].append(snapshot)

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
        lambda *args, **kwargs: captured["db"].append((args, kwargs)),
    )
    monkeypatch.setattr(apex_infinite, "notify", lambda *_args, **_kwargs: None)

    apex_infinite.infinite_loop(
        path="/tmp/project/",
        config=config,
        max_iterations=1,
        dry_run=True,
        renderer=CapturingRenderer(),
    )

    iteration = captured["iterations"][0]
    assert iteration.project_path == "/tmp/project/"
    assert iteration.provider_name == "ollama"
    assert iteration.model_name == "qwen2.5:7b"
    assert iteration.iteration == 1
    assert iteration.operation == "history summary"
    assert iteration.dry_run is True
    assert iteration.elapsed_seconds >= 0
    assert captured["logs"][0].manager_output == "alldonebaby"
    assert captured["logs"][0].stored_state == "completion"
    assert captured["db"][0][0][2] == "alldonebaby"


def test_operator_console_wiring_keeps_known_prompt_routing():
    assert (
        apex_infinite.build_codex_prompt("implement", "implement")
        == "Run the apex-spec skill command /implement"
    )
    assert (
        apex_infinite.build_codex_prompt("/validate", "/validate")
        == "Run the apex-spec skill command /validate"
    )
    assert (
        apex_infinite.build_codex_prompt("fix the tests", "fix the tests")
        == "fix the tests"
    )
