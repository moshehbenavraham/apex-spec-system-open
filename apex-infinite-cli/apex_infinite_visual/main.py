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
from apex_infinite_visual.launcher import ApexCliLaunchOptions, ApexCliProcess


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
            "PySide6 is not installed. Install requirements-wrapper.txt to run "
            "the optional visual wrapper."
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

    class WrapperBridge(  # pylint: disable=too-many-instance-attributes,invalid-name
        qobject
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
            self._theme = options.theme
            self._reduced_effects = options.reduced_effects
            self._glow_enabled = not options.reduced_effects
            self._scanlines_enabled = not options.reduced_effects
            self._flicker_enabled = False
            self._curvature_enabled = not options.reduced_effects
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
            return self._theme

        def _get_reduced_effects(self) -> bool:
            return self._reduced_effects

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
        reducedEffects = property_factory(
            bool, _get_reduced_effects, notify=effectsChanged
        )
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
            if value in {"crt-green", "crt-amber", "ibm-dos", "plain"}:
                self._theme = value
                self.effectsChanged.emit()

        @slot(bool)
        def setReducedEffects(self, value: bool) -> None:
            """Apply the reduced-effects fallback."""
            self._reduced_effects = bool(value)
            if self._reduced_effects:
                self._glow_enabled = False
                self._scanlines_enabled = False
                self._flicker_enabled = False
                self._curvature_enabled = False
            self.effectsChanged.emit()

        @slot(str, bool)
        def setEffectEnabled(self, name: str, value: bool) -> None:
            """Update one independent visual effect control."""
            enabled = bool(value) and not self._reduced_effects
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
            )
            try:
                with ApexCliProcess(launch_options) as process:
                    self._process = process
                    stderr_chunks: list[str] = []
                    stderr_reader = threading.Thread(
                        target=self._read_stderr,
                        args=(process, stderr_chunks),
                        daemon=True,
                    )
                    stderr_reader.start()
                    for line in process.iter_stdout_lines():
                        self._queue.put(("line", line))
                    return_code = process.process.wait() if process.process else 0
                    stderr_reader.join()
                    stderr = "".join(stderr_chunks)
                    if self._stop_requested:
                        return
                    if stderr.strip():
                        self._queue.put(("stderr", stderr.strip()))
                    if return_code:
                        self._queue.put(("return_code", str(return_code)))
            except Exception as exc:  # pylint: disable=broad-exception-caught
                self._queue.put(("error", exc.__class__.__name__))
            finally:
                self._process = None
                self._queue.put(("done", ""))

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
                        {"stage": "stderr", "message": value[:240]},
                    )
                elif kind == "return_code":
                    self._ingest_synthetic_event(
                        "error",
                        {"stage": "subprocess", "error_type": f"return_{value}"},
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

    return WrapperBridge


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
    parser = argparse.ArgumentParser(description="Apex Infinite visual wrapper spike")
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
        choices=["crt-green", "crt-amber", "ibm-dos", "plain"],
        default="crt-green",
    )
    parser.add_argument("--reduced-effects", action="store_true")
    parser.add_argument("--auto-close-ms", type=int, default=None)
    args = parser.parse_args(argv)
    if args.max_iterations < 1:
        parser.error("--max-iterations must be positive")
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


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for `python -m apex_infinite_visual.main`."""
    try:
        return run_app(parse_args(argv))
    except VisualWrapperUnavailable as exc:
        print(f"Visual wrapper unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
