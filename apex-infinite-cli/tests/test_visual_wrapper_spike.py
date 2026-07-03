"""Visual wrapper spike tests."""

import builtins
import io
import json
import subprocess
import sys
import threading
from pathlib import Path

import pytest

import apex_infinite_visual.main as visual_main
from apex_infinite_visual.events import (
    EventLineError,
    EventStateAdapter,
    parse_event_line,
)
from apex_infinite_visual.launcher import (
    ApexCliLaunchOptions,
    ApexCliProcess,
    assert_machine_output_command,
    build_apex_cli_command,
)
from apex_infinite_visual.main import (
    VisualWrapperUnavailable,
    VisualWrapperOptions,
    build_bridge_class,
    build_fixture_event_lines,
    import_qt_modules,
    parse_args,
)


def event_line(event="startup_begin", payload=None, version=1):
    """Build one valid JSONL event line."""
    return json.dumps(
        {
            "version": version,
            "event": event,
            "timestamp": "2026-07-03T00:00:00Z",
            "payload": payload or {},
        },
        sort_keys=True,
    )


def test_parse_event_line_accepts_current_event_shape():
    record = parse_event_line(
        event_line(
            "manager_decision_finished",
            {"iteration": 1, "output": "implement", "reason": "continue"},
        ),
        sequence=7,
    )

    assert record.version == 1
    assert record.event == "manager_decision_finished"
    assert record.sequence == 7
    assert record.payload["output"] == "implement"


def test_parse_event_line_rejects_malformed_json():
    with pytest.raises(EventLineError, match="invalid_json"):
        parse_event_line("{bad")


def test_parse_event_line_rejects_unsupported_version():
    with pytest.raises(EventLineError, match="unsupported_version"):
        parse_event_line(event_line(version=99))


def test_parse_event_line_rejects_unsafe_payload_values():
    with pytest.raises(EventLineError, match="secret-like"):
        parse_event_line(event_line(payload={"value": "Bearer abcdef1234567890"}))


def test_event_state_adapter_bounds_log_and_maps_malformed_lines():
    adapter = EventStateAdapter(max_entries=2)

    adapter.ingest_line(event_line("startup_begin", {"dry_run": True}))
    adapter.ingest_line(event_line("project_resolved", {"project_path": "/tmp/app"}))
    adapter.ingest_line("{bad")
    snapshot = adapter.snapshot()

    assert snapshot.status == "Malformed event"
    assert snapshot.has_error is True
    assert [entry.sequence for entry in snapshot.log] == [2, 3]
    assert snapshot.log[-1].event == "invalid_json"


def test_fixture_event_flow_maps_to_stopped_state():
    adapter = EventStateAdapter()
    lines = build_fixture_event_lines("/tmp/project", "implement", 1)

    for line in lines:
        adapter.ingest_line(line)

    snapshot = adapter.snapshot()
    assert snapshot.status == "fixture_complete"
    assert snapshot.running is False
    assert snapshot.manager_output == "implement"
    assert [json.loads(line)["event"] for line in lines] == [
        "startup_begin",
        "config_loaded",
        "project_resolved",
        "startup",
        "iteration_started",
        "manager_decision_started",
        "manager_decision_finished",
        "prompt_dispatched",
        "codex_dry_run",
        "db_log_finished",
        "run_stopped",
    ]


def test_build_apex_cli_command_uses_stdout_jsonl_guard(tmp_path):
    cli_script = tmp_path / "apex_infinite.py"
    cli_script.write_text("print('stub')\n", encoding="ascii")

    command = build_apex_cli_command(
        ApexCliLaunchOptions(
            project_path=tmp_path,
            cli_script=cli_script,
            python_executable=sys.executable,
            start_command="implement",
            max_iterations=1,
            dry_run=True,
        )
    )

    assert command[:4] == [sys.executable, str(cli_script), "--path", str(tmp_path)]
    assert command[command.index("--event-stream") + 1] == "-"
    assert "--machine-output" in command
    assert command[-1] == "--dry-run"


def test_build_apex_cli_command_defaults_to_package_module(tmp_path):
    command = build_apex_cli_command(
        ApexCliLaunchOptions(
            project_path=tmp_path,
            python_executable=sys.executable,
            start_command="implement",
            max_iterations=1,
            dry_run=True,
        )
    )

    assert command[:5] == [
        sys.executable,
        "-m",
        "apex_infinite",
        "--path",
        str(tmp_path),
    ]
    assert command[command.index("--event-stream") + 1] == "-"
    assert "--machine-output" in command


@pytest.mark.parametrize(
    "command",
    [
        ["python", "apex_infinite.py", "--machine-output"],
        ["python", "apex_infinite.py", "--event-stream", "/tmp/events.jsonl"],
    ],
)
def test_assert_machine_output_command_rejects_unguarded_stdout(command):
    with pytest.raises(ValueError):
        assert_machine_output_command(command)


class FakeProcess:
    """Small process double for cleanup tests."""

    def __init__(self, *_args, **_kwargs):
        self.stdout = io.StringIO("")
        self.stderr = io.StringIO("stderr text")
        self.returncode = None
        self.terminated = False
        self.killed = False
        self.communicated = False

    def poll(self):
        return None if self.returncode is None else self.returncode

    def terminate(self):
        self.terminated = True

    def kill(self):
        self.killed = True
        self.returncode = -9

    def communicate(self, timeout=None):
        self.communicated = True
        if timeout == 0:
            raise subprocess.TimeoutExpired(cmd=["fake"], timeout=timeout)
        self.returncode = 0
        return "", "stderr text"

    def wait(self, timeout=None):
        if timeout == 0:
            raise subprocess.TimeoutExpired(cmd=["fake"], timeout=timeout)
        self.returncode = 0
        return 0


def test_apex_cli_process_terminates_without_consuming_streams(tmp_path):
    cli_script = tmp_path / "apex_infinite.py"
    cli_script.write_text("print('stub')\n", encoding="ascii")

    process = ApexCliProcess(
        ApexCliLaunchOptions(project_path=tmp_path, cli_script=cli_script),
        popen_factory=FakeProcess,
    ).start()

    fake = process.process
    process.terminate(cleanup_timeout=0)

    assert fake.terminated is True
    assert fake.killed is True
    assert fake.communicated is False


def test_parse_args_defaults_to_fixture_dry_run_path(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    options = parse_args(["--dry-run", "--max-iterations", "2"])

    assert options.project_path == str(tmp_path)
    assert options.dry_run is True
    assert options.launch_cli is False
    assert options.max_iterations == 2


def test_import_qt_modules_reports_missing_pyside(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name.startswith("PySide6"):
            raise ImportError("missing PySide6")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(VisualWrapperUnavailable, match="PySide6 is not installed"):
        import_qt_modules()


def test_wrapper_package_import_does_not_import_pyside6(monkeypatch):
    before = {name for name in sys.modules if name.startswith("PySide6")}
    monkeypatch.delitem(sys.modules, "apex_infinite_visual", raising=False)

    __import__("apex_infinite_visual")

    after = {name for name in sys.modules if name.startswith("PySide6")}
    assert after == before


class FakeSignal:
    """Small signal double for bridge tests."""

    def __init__(self):
        self.callbacks = []

    def connect(self, callback):
        self.callbacks.append(callback)

    def emit(self):
        for callback in self.callbacks:
            callback()


class FakeQObject:
    """QObject double for bridge tests."""

    def __init__(self, *_args, **_kwargs):
        super().__init__()


class FakeTimer:
    """QTimer double for bridge tests."""

    def __init__(self, *_args, **_kwargs):
        self.timeout = FakeSignal()
        self.active = False

    def setInterval(self, _interval):
        pass

    def start(self):
        self.active = True

    def stop(self):
        self.active = False

    def isActive(self):
        return self.active


def fake_property(_kind, getter, notify=None):
    """Return a Python property for bridge tests."""
    return property(getter)


def fake_slot(*_args, **_kwargs):
    """Return an identity decorator for bridge tests."""

    def decorator(func):
        return func

    return decorator


def fake_qt_modules():
    """Build fake Qt module bindings for bridge tests."""
    return {
        "Property": fake_property,
        "QObject": FakeQObject,
        "QTimer": FakeTimer,
        "Signal": FakeSignal,
        "Slot": fake_slot,
    }


def bridge_options(tmp_path, launch_cli=False):
    """Build visual wrapper options for bridge tests."""
    return VisualWrapperOptions(
        project_path=str(tmp_path),
        start_command="implement",
        config_path=None,
        provider=None,
        model=None,
        max_iterations=1,
        dry_run=True,
        launch_cli=launch_cli,
        theme="crt-green",
        reduced_effects=False,
        auto_close_ms=None,
        qml_path=tmp_path / "Main.qml",
    )


def test_bridge_start_resets_previous_error_state(tmp_path):
    bridge_class = build_bridge_class(fake_qt_modules())
    bridge = bridge_class(bridge_options(tmp_path))
    bridge._adapter.ingest_line("{bad")  # pylint: disable=protected-access
    bridge._refresh_snapshot()  # pylint: disable=protected-access

    bridge._start_fixture_flow()  # pylint: disable=protected-access

    assert bridge.hasError is False
    assert bridge.statusText == "Offline"
    assert bridge.logLines == []


class WaitingProcessHandle:
    """Process handle that requires stderr to be drained before wait returns."""

    def __init__(self, wrapper):
        self.wrapper = wrapper

    def wait(self):
        if not self.wrapper.stderr_read_started.wait(timeout=1):
            raise RuntimeError("stderr was not drained before process wait")
        return self.wrapper.return_code


class FakeApexCliProcess:
    """ApexCliProcess double for bridge process worker tests."""

    instances = []

    def __init__(self, _options):
        self.stderr_read_started = threading.Event()
        self.return_code = 1
        self.process = WaitingProcessHandle(self)
        FakeApexCliProcess.instances.append(self)

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc, _traceback):
        return False

    def iter_stdout_lines(self):
        return iter([])

    def read_stderr(self):
        self.stderr_read_started.set()
        return "stderr text"

    def terminate(self):
        self.return_code = -15


def test_bridge_process_worker_drains_stderr_before_wait(monkeypatch, tmp_path):
    FakeApexCliProcess.instances = []
    monkeypatch.setattr(visual_main, "ApexCliProcess", FakeApexCliProcess)
    bridge_class = build_bridge_class(fake_qt_modules())
    bridge = bridge_class(bridge_options(tmp_path, launch_cli=True))

    bridge._run_process()  # pylint: disable=protected-access
    bridge._drain_queue()  # pylint: disable=protected-access

    assert FakeApexCliProcess.instances[0].stderr_read_started.is_set()
    assert bridge.hasError is True
    assert bridge.errorText == "Exit code 1"


def test_bridge_operator_stop_suppresses_terminated_process_error(
    monkeypatch, tmp_path
):
    FakeApexCliProcess.instances = []
    monkeypatch.setattr(visual_main, "ApexCliProcess", FakeApexCliProcess)
    bridge_class = build_bridge_class(fake_qt_modules())
    bridge = bridge_class(bridge_options(tmp_path, launch_cli=True))
    bridge._stop_requested = True  # pylint: disable=protected-access

    bridge._run_process()  # pylint: disable=protected-access
    bridge._drain_queue()  # pylint: disable=protected-access

    assert FakeApexCliProcess.instances[0].stderr_read_started.is_set()
    assert bridge.hasError is False
