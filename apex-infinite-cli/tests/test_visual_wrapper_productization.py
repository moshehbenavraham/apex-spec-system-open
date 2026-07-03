"""Visual wrapper productization tests."""

import builtins
import io
import json
import subprocess
import sys
import threading

import pytest

import apex_infinite_visual.main as visual_main
from apex_infinite_visual.events import EventStateAdapter
from apex_infinite_visual.launcher import (
    ApexCliLaunchError,
    ApexCliLaunchOptions,
    ApexCliProcess,
    ApexCliTimeoutError,
    build_apex_cli_command,
)
from apex_infinite_visual.main import (
    VisualWrapperOptions,
    VisualWrapperUnavailable,
    build_bridge_class,
    import_qt_modules,
    parse_args,
)
from apex_infinite_visual.settings import (
    FONT_SCALE_MAX,
    FONT_SCALE_MIN,
    THEME_PLAIN,
    WRAPPER_THEME_NAMES,
    WrapperSettings,
    WrapperSettingsError,
    build_settings,
)


def event_line(event, payload):
    """Build one productization event line."""
    return json.dumps(
        {
            "version": 1,
            "event": event,
            "timestamp": "2026-07-03T00:00:00Z",
            "payload": payload,
        },
        ensure_ascii=True,
        sort_keys=True,
    )


def test_settings_presets_validate_and_export_colors():
    for theme_name in WRAPPER_THEME_NAMES:
        settings = build_settings(theme_name=theme_name)
        colors = settings.color_map()

        assert settings.effective_theme_name == theme_name
        assert colors["background"].startswith("#")
        assert colors["accent"].startswith("#")


def test_settings_plain_fallback_disables_effects():
    settings = build_settings(
        theme_name="crt-amber",
        effect_intensity=75,
        plain_fallback=True,
    )

    assert settings.effective_theme_name == THEME_PLAIN
    assert settings.effective_intensity == 0
    assert settings.effect_enabled("glow") is False
    assert settings.color_map()["background"] == "#101419"


def test_settings_reduced_effects_and_intensity_thresholds():
    settings = build_settings(theme_name="crt-green", effect_intensity=70)
    reduced = settings.updated(reduced_effects=True)

    assert settings.effect_enabled("flicker") is True
    assert reduced.effective_intensity == 0
    assert reduced.effect_enabled("scanlines") is False


@pytest.mark.parametrize(
    "changes",
    [
        {"theme_name": "unknown"},
        {"effect_intensity": -1},
        {"effect_intensity": 101},
        {"font_family": ""},
        {"font_family": "mono-\u2603"},
        {"font_scale": float("nan")},
        {"font_scale": float("inf")},
        {"font_scale": FONT_SCALE_MIN - 0.1},
        {"font_scale": FONT_SCALE_MAX + 0.1},
    ],
)
def test_settings_reject_invalid_values(changes):
    with pytest.raises(WrapperSettingsError):
        build_settings(**changes)


def test_parse_args_validates_productized_settings():
    options = parse_args(
        [
            "--theme",
            "ibm-dos",
            "--effect-intensity",
            "35",
            "--font-family",
            "monospace",
            "--font-scale",
            "1.2",
            "--plain-fallback",
            "--process-timeout-seconds",
            "2",
        ]
    )

    assert options.theme == "ibm-dos"
    assert options.effect_intensity == 35
    assert options.font_scale == 1.2
    assert options.plain_fallback is True
    assert options.process_timeout_seconds == 2


def test_parse_args_rejects_invalid_font_scale():
    with pytest.raises(SystemExit):
        parse_args(["--font-scale", "2.0"])


def test_package_import_remains_pyside_free(monkeypatch):
    before = {name for name in sys.modules if name.startswith("PySide6")}
    monkeypatch.delitem(sys.modules, "apex_infinite_visual", raising=False)

    __import__("apex_infinite_visual")

    after = {name for name in sys.modules if name.startswith("PySide6")}
    assert after == before


def test_missing_pyside6_message_is_product_facing(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name.startswith("PySide6"):
            raise ImportError("missing PySide6")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(VisualWrapperUnavailable, match="PySide6 is not installed"):
        import_qt_modules()


def test_launcher_validates_cli_script_and_project_path(tmp_path):
    cli_script = tmp_path / "apex_infinite.py"
    cli_script.write_text("print('stub')\n", encoding="ascii")

    command = build_apex_cli_command(
        ApexCliLaunchOptions(project_path=tmp_path, cli_script=cli_script)
    )

    assert command[command.index("--event-stream") + 1] == "-"
    assert "--machine-output" in command

    with pytest.raises(ApexCliLaunchError, match="base CLI script"):
        build_apex_cli_command(
            ApexCliLaunchOptions(project_path=tmp_path, cli_script=tmp_path / "no.py")
        )

    with pytest.raises(ApexCliLaunchError, match="project path"):
        build_apex_cli_command(
            ApexCliLaunchOptions(
                project_path=tmp_path / "missing",
                cli_script=cli_script,
            )
        )


class TimeoutProcess:
    """Process double that times out once and then exits during cleanup."""

    def __init__(self, *_args, **_kwargs):
        self.stdout = io.StringIO("")
        self.stderr = io.StringIO("")
        self.returncode = None
        self.terminated = False
        self.killed = False

    def poll(self):
        return None if self.returncode is None else self.returncode

    def terminate(self):
        self.terminated = True

    def kill(self):
        self.killed = True
        self.returncode = -9

    def wait(self, timeout=None):
        if timeout == 1:
            raise subprocess.TimeoutExpired(cmd=["fake"], timeout=timeout)
        self.returncode = 0
        return 0


def test_launcher_timeout_terminates_process(tmp_path):
    cli_script = tmp_path / "apex_infinite.py"
    cli_script.write_text("print('stub')\n", encoding="ascii")
    process = ApexCliProcess(
        ApexCliLaunchOptions(
            project_path=tmp_path,
            cli_script=cli_script,
            process_timeout_seconds=1,
        ),
        popen_factory=TimeoutProcess,
    ).start()

    with pytest.raises(ApexCliTimeoutError) as exc_info:
        process.wait()

    assert exc_info.value.code == "timeout"
    assert process.process.terminated is True


@pytest.mark.parametrize(
    ("event", "payload", "status"),
    [
        ("codex_timeout", {"timeout_seconds": 5}, "Timed out"),
        (
            "error",
            {"stage": "stderr", "error_type": "stderr", "message": "stderr text"},
            "Subprocess stderr",
        ),
        (
            "error",
            {
                "stage": "subprocess",
                "error_type": "non_zero_exit",
                "return_code": 7,
            },
            "Process failed",
        ),
        (
            "error",
            {"stage": "launch_validation", "error_type": "missing_cli"},
            "CLI missing",
        ),
    ],
)
def test_event_adapter_maps_productized_failure_states(event, payload, status):
    adapter = EventStateAdapter()

    adapter.ingest_line(event_line(event, payload))

    snapshot = adapter.snapshot()
    assert snapshot.status == status
    assert snapshot.has_error is True


def test_event_adapter_recovers_after_malformed_event():
    adapter = EventStateAdapter()

    adapter.ingest_line("{bad")
    assert adapter.snapshot().status == "Malformed event"
    adapter.ingest_line(event_line("startup_begin", {"dry_run": True}))

    snapshot = adapter.snapshot()
    assert snapshot.status == "Starting"
    assert snapshot.has_error is False


def test_event_adapter_failure_clears_running_state():
    adapter = EventStateAdapter()

    adapter.ingest_line(event_line("startup_begin", {"dry_run": True}))
    adapter.ingest_line(
        event_line(
            "error",
            {
                "stage": "subprocess",
                "error_type": "non_zero_exit",
                "return_code": 1,
            },
        )
    )

    snapshot = adapter.snapshot()
    assert snapshot.status == "Process failed"
    assert snapshot.running is False


class FakeSignal:
    """Signal double for bridge tests."""

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
    """Timer double for bridge tests."""

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
    """Return a Python property for fake bridge tests."""
    return property(getter)


def fake_slot(*_args, **_kwargs):
    """Return an identity decorator for fake bridge tests."""

    def decorator(func):
        return func

    return decorator


def fake_qt_modules():
    """Return fake Qt bindings for bridge tests."""
    return {
        "Property": fake_property,
        "QObject": FakeQObject,
        "QTimer": FakeTimer,
        "Signal": FakeSignal,
        "Slot": fake_slot,
    }


def bridge_options(tmp_path, launch_cli=False):
    """Build bridge options for productization tests."""
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
        effect_intensity=45,
        font_family="monospace",
        font_scale=1.0,
        plain_fallback=False,
        process_timeout_seconds=1,
    )


def test_bridge_settings_slots_update_state(tmp_path):
    bridge_class = build_bridge_class(fake_qt_modules())
    bridge = bridge_class(bridge_options(tmp_path))

    bridge.setTheme("crt-amber")
    bridge.setEffectIntensity(70)
    bridge.setFontFamily("Liberation Mono")
    bridge.setFontScale(1.2)

    assert bridge.themeName == "crt-amber"
    assert bridge.effectIntensity == 70
    assert bridge.fontFamily == "Liberation Mono"
    assert bridge.fontScale == 1.2
    assert bridge.flickerEnabled is True

    bridge.setPlainFallback(True)

    assert bridge.effectiveThemeName == "plain"
    assert bridge.glowEnabled is False


def test_bridge_prevents_duplicate_start(tmp_path):
    bridge_class = build_bridge_class(fake_qt_modules())
    bridge = bridge_class(bridge_options(tmp_path))
    calls = {"count": 0}

    def fake_start_fixture():
        calls["count"] += 1

    bridge._start_fixture_flow = fake_start_fixture  # pylint: disable=protected-access
    bridge.startRun()
    bridge.startRun()

    assert calls["count"] == 1


def test_bridge_resets_state_on_reentry(tmp_path):
    bridge_class = build_bridge_class(fake_qt_modules())
    bridge = bridge_class(bridge_options(tmp_path))
    bridge._adapter.ingest_line("{bad")  # pylint: disable=protected-access
    bridge._refresh_snapshot()  # pylint: disable=protected-access

    bridge._start_fixture_flow()  # pylint: disable=protected-access

    assert bridge.hasError is False
    assert bridge.logLines == []


def test_bridge_maps_launcher_validation_failure(monkeypatch, tmp_path):
    class RaisingProcess:
        """Process double that raises validation before launch."""

        def __init__(self, _options):
            raise ApexCliLaunchError("missing_cli", "base CLI script was not found")

    monkeypatch.setattr(visual_main, "ApexCliProcess", RaisingProcess)
    bridge_class = build_bridge_class(fake_qt_modules())
    bridge = bridge_class(bridge_options(tmp_path, launch_cli=True))

    bridge._run_process()  # pylint: disable=protected-access
    bridge._drain_queue()  # pylint: disable=protected-access

    assert bridge.statusText == "CLI missing"
    assert bridge.hasError is True


class GatedStdoutProcess:
    """Process double whose stdout reader only releases after wait begins."""

    instances = []

    def __init__(self, _options):
        self.wait_started = threading.Event()
        self.stdout_released = threading.Event()
        self.stdout_reader_timed_out = False
        self.process = None
        GatedStdoutProcess.instances.append(self)

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc, _traceback):
        return False

    def iter_stdout_lines(self):
        if not self.stdout_released.wait(timeout=0.2):
            self.stdout_reader_timed_out = True
        return iter([])

    def read_stderr(self):
        return ""

    def wait(self):
        self.wait_started.set()
        self.stdout_released.set()
        return 0

    def terminate(self):
        self.stdout_released.set()


def test_bridge_waits_while_stdout_reader_drains(monkeypatch, tmp_path):
    GatedStdoutProcess.instances = []
    monkeypatch.setattr(visual_main, "ApexCliProcess", GatedStdoutProcess)
    bridge_class = build_bridge_class(fake_qt_modules())
    bridge = bridge_class(bridge_options(tmp_path, launch_cli=True))

    bridge._run_process()  # pylint: disable=protected-access
    bridge._drain_queue()  # pylint: disable=protected-access

    process = GatedStdoutProcess.instances[0]
    assert process.wait_started.is_set()
    assert process.stdout_reader_timed_out is False
    assert bridge.hasError is False


def test_bridge_maps_unsafe_stderr_to_safe_stderr_state(tmp_path):
    bridge_class = build_bridge_class(fake_qt_modules())
    bridge = bridge_class(bridge_options(tmp_path, launch_cli=True))

    bridge._queue.put(  # pylint: disable=protected-access
        ("stderr", "Bearer abcdef1234567890\n\x1b[31maccent issue\x1b[0m")
    )
    bridge._drain_queue()  # pylint: disable=protected-access

    assert bridge.statusText == "Subprocess stderr"
    assert bridge.hasError is True
    assert bridge.errorText.startswith("Base CLI wrote ")
    assert bridge.errorText.endswith(" stderr characters across 2 line(s).")
    assert "Bearer" not in bridge.errorText


def test_bridge_stop_terminates_process(tmp_path):
    class TerminatedProcess:
        """Minimal process double for stop cleanup."""

        def __init__(self):
            self.terminated = False

        def terminate(self):
            self.terminated = True

    bridge_class = build_bridge_class(fake_qt_modules())
    bridge = bridge_class(bridge_options(tmp_path))
    fake_process = TerminatedProcess()
    bridge._running = True  # pylint: disable=protected-access
    bridge._process = fake_process  # pylint: disable=protected-access

    bridge.stopRun()

    assert fake_process.terminated is True
    assert bridge.statusText == "Stopped"


def test_wrapper_settings_export_type():
    settings = build_settings(theme_name="plain")

    assert isinstance(settings, WrapperSettings)
