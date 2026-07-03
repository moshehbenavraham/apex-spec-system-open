"""PySide6/Qt Quick prototype entrypoint for the optional visual wrapper."""

from __future__ import annotations

import argparse
import json
import os
import queue
import sys
import threading
from dataclasses import dataclass
from pathlib import Path

from apex_infinite_visual.events import EventStateAdapter
from apex_infinite_visual.launcher import (
    ApexCliLaunchError,
    ApexCliLaunchOptions,
    ApexCliProcess,
    ApexCliTimeoutError,
)
from apex_infinite_visual.settings import (
    FONT_FAMILIES,
    THEME_CRT_GREEN,
    THEME_PLAIN,
    WRAPPER_THEME_NAMES,
    WrapperSettings,
    WrapperSettingsError,
    build_settings,
)


class VisualWrapperUnavailable(RuntimeError):
    """Raised when the optional graphical wrapper cannot start."""


@dataclass(frozen=True)
class VisualWrapperOptions:  # pylint: disable=too-many-instance-attributes
    """Runtime options for the prototype wrapper surface."""

    project_path: str
    start_command: str
    config_path: str | None
    provider: str | None
    model: str | None
    max_iterations: int
    dry_run: bool
    launch_cli: bool
    theme: str
    reduced_effects: bool
    auto_close_ms: int | None
    qml_path: Path
    effect_intensity: int | None = None
    font_family: str = "monospace"
    font_scale: float = 1.0
    plain_fallback: bool = False
    process_timeout_seconds: int | None = None


def import_qt_modules():  # pylint: disable=import-outside-toplevel
    """Import PySide6 lazily so normal package imports stay headless-safe."""
    try:
        from PySide6.QtCore import (  # pylint: disable=import-outside-toplevel
            Property,
            QObject,
            QTimer,
            QUrl,
            Signal,
            Slot,
        )
        from PySide6.QtQml import (  # pylint: disable=import-outside-toplevel
            QQmlApplicationEngine,
        )
        from PySide6.QtWidgets import (  # pylint: disable=import-outside-toplevel
            QApplication,
        )
    except ImportError as exc:
        raise VisualWrapperUnavailable(
            "PySide6 is not installed. Install the visual extra to run the "
            "optional visual wrapper."
        ) from exc
    return {
        "Property": Property,
        "QObject": QObject,
        "QTimer": QTimer,
        "QUrl": QUrl,
        "Signal": Signal,
        "Slot": Slot,
        "QQmlApplicationEngine": QQmlApplicationEngine,
        "QApplication": QApplication,
    }


def build_bridge_class(qt):  # pylint: disable=too-many-statements
    """Build the QObject bridge class after Qt modules are available."""
    property_factory = qt["Property"]
    qobject = qt["QObject"]
    signal = qt["Signal"]
    slot = qt["Slot"]
    timer = qt["QTimer"]

    class WrapperBridge(
        # pylint: disable=too-many-instance-attributes,invalid-name
        qobject  # type: ignore[misc, valid-type]
    ):
        """Expose event-driven wrapper state and controls to QML."""

        statusChanged = signal()
        logChanged = signal()
        controlsChanged = signal()
        effectsChanged = signal()

        def __init__(self, options: VisualWrapperOptions):
            super().__init__()
            self._options = options
            self._adapter = EventStateAdapter(max_entries=200)
            self._snapshot = self._adapter.snapshot()
            self._log_lines: list[str] = []
            self._project_path = options.project_path
            self._start_command = options.start_command
            self._max_iterations = options.max_iterations
            self._dry_run = options.dry_run
            self._settings = _settings_from_options(options)
            self._theme_names = list(WRAPPER_THEME_NAMES)
            self._font_families = list(FONT_FAMILIES)
            self._glow_enabled = False
            self._scanlines_enabled = False
            self._flicker_enabled = False
            self._curvature_enabled = False
            self._sync_effects_from_settings()
            self._running = False
            self._queue: queue.Queue[tuple[str, str]] = queue.Queue()
            self._worker: threading.Thread | None = None
            self._process: ApexCliProcess | None = None
            self._stop_requested = False
            self._fixture_rows: list[str] = []
            self._fixture_index = 0
            self._fixture_timer = timer(self)
            self._fixture_timer.setInterval(80)
            self._fixture_timer.timeout.connect(self._emit_next_fixture)
            self._pump_timer = timer(self)
            self._pump_timer.setInterval(50)
            self._pump_timer.timeout.connect(self._drain_queue)
            self._pump_timer.start()

        def _get_status(self) -> str:
            return self._snapshot.status

        def _get_stage(self) -> str:
            return self._snapshot.stage

        def _get_running(self) -> bool:
            return self._running or self._snapshot.running

        def _get_has_error(self) -> bool:
            return self._snapshot.has_error

        def _get_error_text(self) -> str:
            return self._snapshot.error_text

        def _get_project_path(self) -> str:
            return self._project_path

        def _get_start_command(self) -> str:
            return self._start_command

        def _get_max_iterations(self) -> int:
            return self._max_iterations

        def _get_dry_run(self) -> bool:
            return self._dry_run

        def _get_provider(self) -> str:
            return self._snapshot.provider_name or "Provider pending"

        def _get_model(self) -> str:
            return self._snapshot.model_name or "Model pending"

        def _get_iteration(self) -> str:
            if self._snapshot.iteration is None:
                return "Not started"
            return str(self._snapshot.iteration)

        def _get_manager_output(self) -> str:
            return self._snapshot.manager_output or "No decision yet"

        def _get_log_lines(self) -> list[str]:
            return list(self._log_lines)

        def _get_theme(self) -> str:
            return self._settings.theme_name

        def _get_effective_theme(self) -> str:
            return self._settings.effective_theme_name

        def _get_theme_names(self) -> list[str]:
            return list(self._theme_names)

        def _get_theme_label(self) -> str:
            return self._settings.preset.label

        def _get_reduced_effects(self) -> bool:
            return self._settings.reduced_effects

        def _get_plain_fallback(self) -> bool:
            return (
                self._settings.plain_fallback
                or self._settings.theme_name == THEME_PLAIN
            )

        def _get_effect_intensity(self) -> int:
            return self._settings.effect_intensity

        def _get_effect_opacity(self) -> float:
            return self._settings.effect_opacity

        def _get_font_family(self) -> str:
            return self._settings.font_family

        def _get_font_scale(self) -> float:
            return self._settings.font_scale

        def _get_font_families(self) -> list[str]:
            return list(self._font_families)

        def _color(self, key: str) -> str:
            return self._settings.color_map()[key]

        def _get_background_color(self) -> str:
            return self._color("background")

        def _get_panel_color(self) -> str:
            return self._color("panel")

        def _get_panel_alt_color(self) -> str:
            return self._color("panel_alt")

        def _get_cell_color(self) -> str:
            return self._color("cell")

        def _get_border_color(self) -> str:
            return self._color("border")

        def _get_accent_color(self) -> str:
            return self._color("accent")

        def _get_text_color(self) -> str:
            return self._color("text")

        def _get_muted_color(self) -> str:
            return self._color("muted")

        def _get_warning_color(self) -> str:
            return self._color("warning")

        def _get_error_color(self) -> str:
            return self._color("error")

        def _get_glow_enabled(self) -> bool:
            return self._glow_enabled

        def _get_scanlines_enabled(self) -> bool:
            return self._scanlines_enabled

        def _get_flicker_enabled(self) -> bool:
            return self._flicker_enabled

        def _get_curvature_enabled(self) -> bool:
            return self._curvature_enabled

        statusText = property_factory(str, _get_status, notify=statusChanged)
        stageText = property_factory(str, _get_stage, notify=statusChanged)
        running = property_factory(bool, _get_running, notify=statusChanged)
        hasError = property_factory(bool, _get_has_error, notify=statusChanged)
        errorText = property_factory(str, _get_error_text, notify=statusChanged)
        projectPath = property_factory(str, _get_project_path, notify=controlsChanged)
        startCommand = property_factory(str, _get_start_command, notify=controlsChanged)
        maxIterations = property_factory(
            int, _get_max_iterations, notify=controlsChanged
        )
        dryRun = property_factory(bool, _get_dry_run, notify=controlsChanged)
        providerName = property_factory(str, _get_provider, notify=statusChanged)
        modelName = property_factory(str, _get_model, notify=statusChanged)
        iterationText = property_factory(str, _get_iteration, notify=statusChanged)
        managerOutput = property_factory(str, _get_manager_output, notify=statusChanged)
        logLines = property_factory("QStringList", _get_log_lines, notify=logChanged)
        themeName = property_factory(str, _get_theme, notify=effectsChanged)
        effectiveThemeName = property_factory(
            str, _get_effective_theme, notify=effectsChanged
        )
        themeNames = property_factory(
            "QStringList", _get_theme_names, notify=effectsChanged
        )
        themeLabel = property_factory(str, _get_theme_label, notify=effectsChanged)
        reducedEffects = property_factory(
            bool, _get_reduced_effects, notify=effectsChanged
        )
        plainFallback = property_factory(
            bool, _get_plain_fallback, notify=effectsChanged
        )
        effectIntensity = property_factory(
            int, _get_effect_intensity, notify=effectsChanged
        )
        effectOpacity = property_factory(
            float, _get_effect_opacity, notify=effectsChanged
        )
        fontFamily = property_factory(str, _get_font_family, notify=effectsChanged)
        fontScale = property_factory(float, _get_font_scale, notify=effectsChanged)
        fontFamilies = property_factory(
            "QStringList", _get_font_families, notify=effectsChanged
        )
        backgroundColor = property_factory(
            str, _get_background_color, notify=effectsChanged
        )
        panelColor = property_factory(str, _get_panel_color, notify=effectsChanged)
        panelAltColor = property_factory(
            str, _get_panel_alt_color, notify=effectsChanged
        )
        cellColor = property_factory(str, _get_cell_color, notify=effectsChanged)
        borderColor = property_factory(str, _get_border_color, notify=effectsChanged)
        accentColor = property_factory(str, _get_accent_color, notify=effectsChanged)
        textColor = property_factory(str, _get_text_color, notify=effectsChanged)
        mutedColor = property_factory(str, _get_muted_color, notify=effectsChanged)
        warningColor = property_factory(str, _get_warning_color, notify=effectsChanged)
        errorColor = property_factory(str, _get_error_color, notify=effectsChanged)
        glowEnabled = property_factory(bool, _get_glow_enabled, notify=effectsChanged)
        scanlinesEnabled = property_factory(
            bool, _get_scanlines_enabled, notify=effectsChanged
        )
        flickerEnabled = property_factory(
            bool, _get_flicker_enabled, notify=effectsChanged
        )
        curvatureEnabled = property_factory(
            bool, _get_curvature_enabled, notify=effectsChanged
        )

        @slot()
        def startRun(self) -> None:
            """Start fixture playback or the real guarded CLI subprocess."""
            if self._running:
                return
            self._running = True
            self._stop_requested = False
            self.statusChanged.emit()
            if self._options.launch_cli:
                self._start_process_worker()
                return
            self._start_fixture_flow()

        @slot()
        def stopRun(self) -> None:
            """Stop the current fixture or subprocess lifecycle."""
            if not self._running and not self._snapshot.running:
                return
            self._stop_requested = True
            if self._fixture_timer.isActive():
                self._fixture_timer.stop()
            if self._process:
                self._process.terminate()
            self._running = False
            self._ingest_synthetic_event(
                "run_stopped", {"reason": "operator_stop", "iteration": 0}
            )
            self.statusChanged.emit()

        @slot()
        def shutdown(self) -> None:
            """Release timers and subprocess resources before wrapper exit."""
            if self._fixture_timer.isActive():
                self._fixture_timer.stop()
            if self._pump_timer.isActive():
                self._pump_timer.stop()
            if self._process:
                self._process.terminate()
            self._running = False

        @slot(str)
        def setProjectPath(self, value: str) -> None:
            """Update the project path control."""
            if self._running:
                return
            self._project_path = value.strip() or os.getcwd()
            self.controlsChanged.emit()

        @slot(str)
        def setStartCommand(self, value: str) -> None:
            """Update the optional start command control."""
            if self._running:
                return
            self._start_command = value.strip()
            self.controlsChanged.emit()

        @slot(int)
        def setMaxIterations(self, value: int) -> None:
            """Update the max-iteration control."""
            if self._running:
                return
            self._max_iterations = max(1, int(value))
            self.controlsChanged.emit()

        @slot(bool)
        def setDryRun(self, value: bool) -> None:
            """Update dry-run mode."""
            if self._running:
                return
            self._dry_run = bool(value)
            self.controlsChanged.emit()

        @slot(str)
        def setTheme(self, value: str) -> None:
            """Update the QML theme selector."""
            plain_fallback = value == THEME_PLAIN
            self._update_settings(theme_name=value, plain_fallback=plain_fallback)

        @slot(bool)
        def setReducedEffects(self, value: bool) -> None:
            """Apply the reduced-effects fallback."""
            self._update_settings(reduced_effects=bool(value))

        @slot(int)
        def setEffectIntensity(self, value: int) -> None:
            """Update the bounded effect intensity."""
            self._update_settings(effect_intensity=max(0, min(100, int(value))))

        @slot(str)
        def setFontFamily(self, value: str) -> None:
            """Update the wrapper font family."""
            self._update_settings(font_family=value.strip() or "monospace")

        @slot(float)
        def setFontScale(self, value: float) -> None:
            """Update the wrapper font scale."""
            self._update_settings(font_scale=round(float(value), 2))

        @slot(bool)
        def setPlainFallback(self, value: bool) -> None:
            """Apply or clear the plain fallback surface."""
            if self._settings.theme_name == THEME_PLAIN and not value:
                self._update_settings(theme_name=THEME_CRT_GREEN, plain_fallback=False)
                return
            self._update_settings(plain_fallback=bool(value))

        @slot(str, bool)
        def setEffectEnabled(self, name: str, value: bool) -> None:
            """Update one independent visual effect control."""
            enabled = bool(value) and self._settings.effects_available
            if name == "glow":
                self._glow_enabled = enabled
            elif name == "scanlines":
                self._scanlines_enabled = enabled
            elif name == "flicker":
                self._flicker_enabled = enabled
            elif name == "curvature":
                self._curvature_enabled = enabled
            self.effectsChanged.emit()

        def _start_fixture_flow(self) -> None:
            self._reset_adapter()
            self._fixture_rows = build_fixture_event_lines(
                self._project_path,
                self._start_command or "implement",
                self._max_iterations,
            )
            self._fixture_index = 0
            self._fixture_timer.start()

        def _emit_next_fixture(self) -> None:
            if self._fixture_index >= len(self._fixture_rows):
                self._fixture_timer.stop()
                self._running = False
                self.statusChanged.emit()
                return
            self._adapter.ingest_line(self._fixture_rows[self._fixture_index])
            self._fixture_index += 1
            self._refresh_snapshot()

        def _start_process_worker(self) -> None:
            self._reset_adapter()
            self._worker = threading.Thread(target=self._run_process, daemon=True)
            self._worker.start()

        def _run_process(self) -> None:
            launch_options = ApexCliLaunchOptions(
                project_path=self._project_path,
                start_command=self._start_command or None,
                config_path=self._options.config_path,
                provider=self._options.provider,
                model=self._options.model,
                max_iterations=self._max_iterations,
                dry_run=self._dry_run,
                process_timeout_seconds=self._options.process_timeout_seconds,
            )
            try:
                with ApexCliProcess(launch_options) as process:
                    self._process = process
                    stderr_chunks: list[str] = []
                    stdout_reader = threading.Thread(
                        target=self._read_stdout,
                        args=(process,),
                        daemon=True,
                    )
                    stderr_reader = threading.Thread(
                        target=self._read_stderr,
                        args=(process, stderr_chunks),
                        daemon=True,
                    )
                    stdout_reader.start()
                    stderr_reader.start()
                    try:
                        if hasattr(process, "wait"):
                            return_code = process.wait()
                        elif process.process:
                            return_code = process.process.wait()
                        else:
                            return_code = 0
                    finally:
                        stdout_reader.join()
                        stderr_reader.join()
                    stderr = "".join(stderr_chunks)
                    if self._stop_requested:
                        return
                    if stderr.strip():
                        self._queue.put(("stderr", stderr.strip()))
                    if return_code:
                        self._queue.put(("return_code", str(int(return_code))))
            except ApexCliTimeoutError as exc:
                self._queue.put(("timeout", str(exc.timeout_seconds)))
            except ApexCliLaunchError as exc:
                self._queue.put(
                    (
                        "launch_error",
                        json.dumps(
                            {
                                "error_type": exc.code,
                                "message": exc.message,
                            },
                            ensure_ascii=True,
                            sort_keys=True,
                        ),
                    )
                )
            except Exception as exc:  # pylint: disable=broad-exception-caught
                self._queue.put(("error", exc.__class__.__name__))
            finally:
                self._process = None
                self._queue.put(("done", ""))

        def _read_stdout(self, process: ApexCliProcess) -> None:
            for line in process.iter_stdout_lines():
                self._queue.put(("line", line))

        def _read_stderr(
            self, process: ApexCliProcess, stderr_chunks: list[str]
        ) -> None:
            stderr_chunks.append(process.read_stderr())

        def _drain_queue(self) -> None:
            changed = False
            while True:
                try:
                    kind, value = self._queue.get_nowait()
                except queue.Empty:
                    break
                changed = True
                if kind == "line":
                    self._adapter.ingest_line(value)
                elif kind == "stderr":
                    self._ingest_synthetic_event(
                        "error",
                        {
                            "stage": "stderr",
                            "error_type": "stderr",
                            "message": _stderr_summary(value),
                        },
                    )
                elif kind == "return_code":
                    self._ingest_synthetic_event(
                        "error",
                        {
                            "stage": "subprocess",
                            "error_type": "non_zero_exit",
                            "return_code": int(value),
                        },
                    )
                elif kind == "timeout":
                    self._ingest_synthetic_event(
                        "error",
                        {
                            "stage": "subprocess",
                            "error_type": "timeout",
                            "timeout_seconds": int(value),
                        },
                    )
                elif kind == "launch_error":
                    payload = json.loads(value)
                    self._ingest_synthetic_event(
                        "error",
                        {"stage": "launch_validation", **payload},
                    )
                elif kind == "error":
                    self._ingest_synthetic_event(
                        "error",
                        {"stage": "wrapper", "error_type": value},
                    )
                elif kind == "done":
                    self._running = False
            if changed:
                self._refresh_snapshot()

        def _ingest_synthetic_event(
            self, event: str, payload: dict[str, object]
        ) -> None:
            row = {
                "version": 1,
                "event": event,
                "timestamp": "2026-07-03T00:00:00Z",
                "payload": payload,
            }
            self._adapter.ingest_line(json.dumps(row, ensure_ascii=True))
            self._refresh_snapshot()

        def _reset_adapter(self) -> None:
            self._adapter = EventStateAdapter(max_entries=200)
            self._snapshot = self._adapter.snapshot()
            self._log_lines = []
            self.statusChanged.emit()
            self.logChanged.emit()

        def _refresh_snapshot(self) -> None:
            self._snapshot = self._adapter.snapshot()
            self._log_lines = [_format_log_line(entry) for entry in self._snapshot.log]
            self.statusChanged.emit()
            self.logChanged.emit()

        def _update_settings(self, **changes: object) -> None:
            try:
                self._settings = self._settings.updated(**changes)
            except WrapperSettingsError as exc:
                self._ingest_synthetic_event(
                    "error",
                    {
                        "stage": "settings",
                        "error_type": "invalid_settings",
                        "message": str(exc),
                    },
                )
                return
            self._sync_effects_from_settings()
            self.effectsChanged.emit()

        def _sync_effects_from_settings(self) -> None:
            self._glow_enabled = self._settings.effect_enabled("glow")
            self._scanlines_enabled = self._settings.effect_enabled("scanlines")
            self._flicker_enabled = self._settings.effect_enabled("flicker")
            self._curvature_enabled = self._settings.effect_enabled("curvature")

    return WrapperBridge


def _settings_from_options(options: VisualWrapperOptions) -> WrapperSettings:
    return build_settings(
        theme_name=options.theme,
        effect_intensity=options.effect_intensity,
        font_family=options.font_family,
        font_scale=options.font_scale,
        reduced_effects=options.reduced_effects,
        plain_fallback=options.plain_fallback,
    )


def build_fixture_event_lines(
    project_path: str,
    start_command: str,
    max_iterations: int,
) -> list[str]:
    """Build deterministic fixture events for smoke tests and dry-run previews."""
    rows = [
        (
            "startup_begin",
            {"event_stream": True, "machine_output": True, "dry_run": True},
        ),
        (
            "config_loaded",
            {
                "config_path": "config.yaml",
                "provider_name": "ollama",
                "model_name": "qwen2.5:7b",
            },
        ),
        ("project_resolved", {"project_path": str(Path(project_path).expanduser())}),
        (
            "startup",
            {
                "project_path": str(Path(project_path).expanduser()),
                "provider_name": "ollama",
                "model_name": "qwen2.5:7b",
                "max_iterations": max_iterations,
                "dry_run": True,
                "start_command": start_command,
                "machine_output": True,
            },
        ),
        (
            "iteration_started",
            {
                "project_path": str(Path(project_path).expanduser()),
                "provider_name": "ollama",
                "model_name": "qwen2.5:7b",
                "iteration": 1,
                "operation": "dry-run preview",
                "dry_run": True,
            },
        ),
        ("manager_decision_started", {"iteration": 1, "source": "fixture"}),
        (
            "manager_decision_finished",
            {
                "iteration": 1,
                "output": start_command,
                "reason": "Wrapper smoke fixture",
                "known_command": True,
            },
        ),
        ("prompt_dispatched", {"iteration": 1, "prompt_length": 43}),
        (
            "codex_dry_run",
            {
                "binary": "codex",
                "project_path": str(Path(project_path).expanduser()),
                "prompt_length": 43,
                "timeout_seconds": 1800,
            },
        ),
        ("db_log_finished", {"project_path": project_path, "stored_state": "fixture"}),
        ("run_stopped", {"reason": "fixture_complete", "iteration": 1}),
    ]
    return [
        json.dumps(
            {
                "version": 1,
                "event": event,
                "timestamp": "2026-07-03T00:00:00Z",
                "payload": payload,
            },
            ensure_ascii=True,
            sort_keys=True,
        )
        for event, payload in rows
    ]


def parse_args(argv: list[str] | None = None) -> VisualWrapperOptions:
    """Parse wrapper command-line arguments."""
    parser = argparse.ArgumentParser(description="Apex Infinite visual wrapper")
    parser.add_argument("--path", default=os.getcwd(), help="Project path to display")
    parser.add_argument(
        "--start-command", default="implement", help="Optional start command"
    )
    parser.add_argument("--config", dest="config_path", default=None)
    parser.add_argument("--provider", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--max-iterations", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--launch-cli",
        action="store_true",
        help="Launch the real CLI instead of fixture playback",
    )
    parser.add_argument(
        "--theme",
        choices=list(WRAPPER_THEME_NAMES),
        default=THEME_CRT_GREEN,
    )
    parser.add_argument("--effect-intensity", type=int, default=None)
    parser.add_argument("--font-family", default="monospace")
    parser.add_argument("--font-scale", type=float, default=1.0)
    parser.add_argument(
        "--plain-fallback",
        action="store_true",
        help="Start with the plain low-effects fallback active",
    )
    parser.add_argument("--process-timeout-seconds", type=int, default=None)
    parser.add_argument("--reduced-effects", action="store_true")
    parser.add_argument("--auto-close-ms", type=int, default=None)
    args = parser.parse_args(argv)
    if args.max_iterations < 1:
        parser.error("--max-iterations must be positive")
    if args.auto_close_ms is not None and args.auto_close_ms < 1:
        parser.error("--auto-close-ms must be positive")
    if args.process_timeout_seconds is not None and args.process_timeout_seconds < 1:
        parser.error("--process-timeout-seconds must be positive")
    try:
        build_settings(
            theme_name=args.theme,
            effect_intensity=args.effect_intensity,
            font_family=args.font_family,
            font_scale=args.font_scale,
            reduced_effects=args.reduced_effects,
            plain_fallback=args.plain_fallback,
        )
    except WrapperSettingsError as exc:
        parser.error(str(exc))
    return VisualWrapperOptions(
        project_path=args.path,
        start_command=args.start_command,
        config_path=args.config_path,
        provider=args.provider,
        model=args.model,
        max_iterations=args.max_iterations,
        dry_run=args.dry_run,
        launch_cli=args.launch_cli,
        theme=args.theme,
        reduced_effects=args.reduced_effects,
        auto_close_ms=args.auto_close_ms,
        qml_path=Path(__file__).resolve().parent / "qml" / "Main.qml",
        effect_intensity=args.effect_intensity,
        font_family=args.font_family,
        font_scale=args.font_scale,
        plain_fallback=args.plain_fallback,
        process_timeout_seconds=args.process_timeout_seconds,
    )


def run_app(options: VisualWrapperOptions) -> int:
    """Run the Qt Quick wrapper application."""
    if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
        os.environ.setdefault("QT_QUICK_BACKEND", "software")
    qt = import_qt_modules()
    app = qt["QApplication"](sys.argv[:1])
    bridge_class = build_bridge_class(qt)
    bridge = bridge_class(options)
    engine = qt["QQmlApplicationEngine"]()
    engine.rootContext().setContextProperty("bridge", bridge)
    engine.load(qt["QUrl"].fromLocalFile(str(options.qml_path)))
    if not engine.rootObjects():
        raise VisualWrapperUnavailable("QML surface could not be loaded")
    app.aboutToQuit.connect(bridge.shutdown)
    if options.dry_run:
        qt["QTimer"].singleShot(0, bridge.startRun)
    auto_close_ms = options.auto_close_ms
    if auto_close_ms is None and os.environ.get("QT_QPA_PLATFORM") == "offscreen":
        auto_close_ms = 900
    if auto_close_ms:
        qt["QTimer"].singleShot(auto_close_ms, app.quit)
    return app.exec()


def _format_log_line(entry) -> str:
    detail = f" - {entry.detail}" if entry.detail else ""
    return f"{entry.sequence:03d} [{entry.level.upper()}] {entry.title}{detail}"


def _stderr_summary(stderr: str) -> str:
    stripped = stderr.strip()
    if not stripped:
        return "Base CLI wrote stderr."
    line_count = len(stripped.splitlines())
    return (
        f"Base CLI wrote {len(stripped)} stderr characters across {line_count} line(s)."
    )


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for `apex-infinite-visual`."""
    try:
        return run_app(parse_args(argv))
    except VisualWrapperUnavailable as exc:
        print(f"Visual wrapper unavailable: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # pylint: disable=broad-exception-caught
        print(
            "Visual wrapper unavailable: display backend or Qt runtime failed "
            f"({exc.__class__.__name__})",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
