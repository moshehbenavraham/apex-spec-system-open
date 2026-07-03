"""JSONL event parsing and wrapper state adaptation."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field

from apex_infinite.events import (
    EVENT_NAMES,
    EVENT_VERSION,
    EventStreamError,
    JsonValue,
    validate_payload,
)

FAILURE_STATE_TEXT: dict[str, tuple[str, str, str]] = {
    "missing_cli": (
        "CLI missing",
        "Launch validation",
        "Base CLI script was not found.",
    ),
    "invalid_cli": (
        "CLI invalid",
        "Launch validation",
        "Base CLI script is not valid.",
    ),
    "invalid_project": (
        "Project unavailable",
        "Launch validation",
        "Project path could not be opened.",
    ),
    "invalid_settings": (
        "Settings issue",
        "Settings validation",
        "Wrapper settings are invalid.",
    ),
    "missing_pyside6": (
        "Wrapper unavailable",
        "Dependency check",
        "PySide6 is not installed.",
    ),
    "display_backend": (
        "Display unavailable",
        "Display backend",
        "Qt could not open the display backend.",
    ),
    "malformed_event": (
        "Malformed event",
        "Event recovery",
        "An event line could not be parsed.",
    ),
    "timeout": (
        "Timed out",
        "Subprocess timeout",
        "The base CLI process exceeded the wrapper timeout.",
    ),
    "stderr": (
        "Subprocess stderr",
        "Subprocess stderr",
        "The base CLI process wrote stderr.",
    ),
    "non_zero_exit": (
        "Process failed",
        "Subprocess exit",
        "The base CLI process exited non-zero.",
    ),
    "operator_stop": ("Stopped", "Stopped", "Operator stopped the run."),
    "wrapper": (
        "Wrapper issue",
        "Wrapper runtime",
        "The wrapper caught a runtime failure.",
    ),
}


class EventLineError(ValueError):
    """Raised when one JSONL event line cannot be consumed by the wrapper."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


@dataclass(frozen=True)
class EventRecord:
    """Validated wrapper-facing lifecycle event."""

    version: int
    event: str
    timestamp: str
    payload: dict[str, JsonValue]
    sequence: int = 0


@dataclass(frozen=True)
class LogEntry:
    """One product-facing log row derived from a lifecycle event."""

    sequence: int
    level: str
    title: str
    detail: str
    timestamp: str
    event: str


@dataclass(frozen=True)
class WrapperSnapshot:  # pylint: disable=too-many-instance-attributes
    """Immutable status snapshot for the visual bridge and tests."""

    status: str
    stage: str
    running: bool
    has_error: bool
    error_text: str
    iteration: int | None
    project_path: str
    provider_name: str
    model_name: str
    manager_output: str
    last_event: str
    log: tuple[LogEntry, ...] = field(default_factory=tuple)


class EventStateAdapter:  # pylint: disable=too-many-instance-attributes
    """Convert event lines into bounded wrapper state without crashing."""

    def __init__(self, max_entries: int = 200):
        if max_entries < 1:
            raise ValueError("max_entries must be positive")
        self.max_entries = max_entries
        self._sequence = 0
        self._log: list[LogEntry] = []
        self.status = "Offline"
        self.stage = "Waiting"
        self.running = False
        self.has_error = False
        self.error_text = ""
        self.iteration: int | None = None
        self.project_path = ""
        self.provider_name = ""
        self.model_name = ""
        self.manager_output = ""
        self.last_event = ""

    def ingest_line(self, line: str) -> EventRecord | None:
        """Consume one JSONL line, mapping malformed input to error state."""
        sequence = self._sequence + 1
        try:
            record = parse_event_line(line, sequence=sequence)
        except EventLineError as exc:
            self._sequence = sequence
            self._record_error(sequence, exc)
            return None
        self._sequence = sequence
        self.ingest_event(record)
        return record

    def ingest_event(self, record: EventRecord) -> None:
        """Apply one validated event record to wrapper state."""
        self.last_event = record.event
        self._apply_event_state(record)
        title, detail, level = _event_log_text(record)
        self._append_log(
            LogEntry(
                sequence=record.sequence or self._sequence,
                level=level,
                title=title,
                detail=detail,
                timestamp=record.timestamp,
                event=record.event,
            )
        )

    def snapshot(self) -> WrapperSnapshot:
        """Return an immutable copy of current wrapper state."""
        return WrapperSnapshot(
            status=self.status,
            stage=self.stage,
            running=self.running,
            has_error=self.has_error,
            error_text=self.error_text,
            iteration=self.iteration,
            project_path=self.project_path,
            provider_name=self.provider_name,
            model_name=self.model_name,
            manager_output=self.manager_output,
            last_event=self.last_event,
            log=tuple(self._log),
        )

    def _record_error(self, sequence: int, error: EventLineError) -> None:
        self.has_error = True
        self.error_text = error.message
        self.status = "Malformed event"
        self.stage = "Event recovery"
        self._append_log(
            LogEntry(
                sequence=sequence,
                level="error",
                title="Event line rejected",
                detail=error.message,
                timestamp="",
                event=error.code,
            )
        )

    def _append_log(self, entry: LogEntry) -> None:
        self._log.append(entry)
        if len(self._log) > self.max_entries:
            self._log = self._log[-self.max_entries :]

    def _apply_event_state(  # pylint: disable=too-many-branches,too-many-statements
        self, record: EventRecord
    ) -> None:
        payload = record.payload
        event = record.event

        if event == "startup_begin":
            self.status = "Starting"
            self.stage = "Startup"
            self.running = True
            self.has_error = False
            self.error_text = ""
        elif event == "config_loaded":
            self.provider_name = _payload_string(payload, "provider_name")
            self.model_name = _payload_string(payload, "model_name")
            self.stage = "Configuration"
        elif event == "ui_resolved":
            self.stage = "Display ready"
        elif event == "project_resolved":
            self.project_path = _payload_string(payload, "project_path")
            self.stage = "Project"
        elif event == "startup":
            self.project_path = _payload_string(payload, "project_path")
            self.provider_name = _payload_string(payload, "provider_name")
            self.model_name = _payload_string(payload, "model_name")
            self.status = "Ready"
            self.stage = "Startup complete"
        elif event == "iteration_started":
            self.iteration = _payload_int(payload, "iteration")
            operation = _payload_string(payload, "operation")
            self.status = f"Iteration {self.iteration or ''}".strip()
            self.stage = operation or "Iteration"
            self.running = True
        elif event in {"history_summarize_started", "history_summary_started"}:
            self.stage = "History summary"
            self.status = "Summarizing"
        elif event in {"history_summarize_finished", "history_summary_completed"}:
            self.stage = "History ready"
            self.status = "Context ready"
        elif event == "manager_decision_started":
            self.stage = "Manager"
            self.status = "Manager deciding"
        elif event in {"manager_decision_finished", "manager_decision_completed"}:
            self.stage = "Manager decision"
            self.manager_output = _payload_string(payload, "output")
            self.status = self.manager_output or "Decision received"
        elif event in {"prompt_built", "prompt_dispatched"}:
            self.stage = "Prompt"
            self.status = "Prompt dispatched"
        elif event == "codex_dry_run":
            self.stage = "Codex"
            self.status = "Dry run"
        elif event == "codex_started":
            self.stage = "Codex"
            self.status = "Codex running"
        elif event in {"codex_finished", "codex_completed"}:
            self.stage = "Codex"
            self.status = "Codex complete"
        elif event in {"codex_error", "codex_failed", "codex_timeout"}:
            self._apply_failure(record)
        elif event in {"db_log_started", "db_log_finished", "db_logged"}:
            self.stage = "History log"
            self.status = "History updated"
        elif event in {"workflow_completed", "completion"}:
            self.stage = "Complete"
            self.status = "Workflow complete"
            self.running = False
        elif event == "max_iterations_reached":
            self.stage = "Safety stop"
            self.status = "Max iterations reached"
            self.running = False
        elif event == "run_stopped":
            self.stage = "Stopped"
            self.running = False
            if _payload_string(payload, "reason") == "operator_stop":
                self.status = "Stopped"
                self.has_error = False
                self.error_text = ""
            else:
                self.status = _payload_string(payload, "reason") or "Stopped"
        elif event in {"error", "event_stream_error"}:
            self._apply_failure(record)

    def _apply_failure(self, record: EventRecord) -> None:
        status, stage, detail = _failure_text(record)
        self.status = status
        self.stage = stage
        self.running = False
        self.has_error = True
        self.error_text = detail
        if _failure_code(record.payload, record.event) == "operator_stop":
            self.running = False
            self.has_error = False


def parse_event_line(line: str, sequence: int = 0) -> EventRecord:
    """Parse and validate one Apex Infinite CLI event JSONL line."""
    if not isinstance(line, str):
        raise EventLineError("invalid_type", "event line must be text")
    stripped = line.strip()
    if not stripped:
        raise EventLineError("empty_line", "event line is empty")
    try:
        raw = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise EventLineError(
            "invalid_json", f"invalid JSON at column {exc.colno}"
        ) from exc
    if not isinstance(raw, Mapping):
        raise EventLineError("invalid_object", "event line must contain a JSON object")

    version = raw.get("version")
    if not isinstance(version, int) or isinstance(version, bool):
        raise EventLineError("missing_version", "event version must be an integer")
    if version != EVENT_VERSION:
        raise EventLineError(
            "unsupported_version",
            f"event version {version} is not supported by this wrapper",
        )

    event = raw.get("event")
    if not isinstance(event, str) or not event:
        raise EventLineError("missing_event", "event name must be a non-empty string")
    if event not in EVENT_NAMES:
        raise EventLineError("unsupported_event", f"event {event!r} is not supported")

    timestamp = raw.get("timestamp")
    if not isinstance(timestamp, str) or not timestamp:
        raise EventLineError(
            "missing_timestamp", "event timestamp must be a non-empty string"
        )

    payload = raw.get("payload")
    if not isinstance(payload, Mapping):
        raise EventLineError("invalid_payload", "event payload must be an object")
    try:
        validated_payload = validate_payload(payload)
    except EventStreamError as exc:
        raise EventLineError("invalid_payload", str(exc)) from exc

    return EventRecord(
        version=version,
        event=event,
        timestamp=timestamp,
        payload=validated_payload,
        sequence=sequence,
    )


def _payload_string(payload: Mapping[str, JsonValue], key: str) -> str:
    value = payload.get(key)
    return value if isinstance(value, str) else ""


def _payload_int(payload: Mapping[str, JsonValue], key: str) -> int | None:
    value = payload.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _event_log_text(  # pylint: disable=too-many-return-statements,too-many-branches
    record: EventRecord,
) -> tuple[str, str, str]:
    payload = record.payload
    event = record.event
    if event == "startup_begin":
        return "Starting Apex Infinite", "Opening the event channel.", "info"
    if event == "config_loaded":
        provider = _payload_string(payload, "provider_name")
        model = _payload_string(payload, "model_name")
        return "Configuration loaded", _join_detail(provider, model), "info"
    if event == "project_resolved":
        return "Project selected", _payload_string(payload, "project_path"), "info"
    if event == "startup":
        start = _payload_string(payload, "start_command") or "auto"
        return "Run ready", f"Start command: {start}", "success"
    if event == "iteration_started":
        iteration = _payload_int(payload, "iteration")
        operation = _payload_string(payload, "operation")
        return f"Iteration {iteration}", operation, "info"
    if event in {"history_summarize_started", "history_summary_started"}:
        return "History summary", "Preparing context from prior records.", "info"
    if event in {"history_summarize_finished", "history_summary_completed"}:
        return "Context ready", "History summary completed.", "success"
    if event == "manager_decision_started":
        return "Manager deciding", "Selecting the next workflow action.", "info"
    if event in {"manager_decision_finished", "manager_decision_completed"}:
        output = _payload_string(payload, "output")
        reason = _payload_string(payload, "reason")
        return "Manager decision", _join_detail(output, reason), "success"
    if event in {"prompt_built", "prompt_dispatched"}:
        length = _payload_int(payload, "prompt_length")
        return "Prompt dispatched", f"Prompt length: {length or 0}", "info"
    if event == "codex_dry_run":
        return "Dry run", "Codex subprocess was not launched.", "info"
    if event == "codex_started":
        return "Codex started", "Agent subprocess is running.", "info"
    if event in {"codex_finished", "codex_completed"}:
        return "Codex complete", "Agent subprocess completed.", "success"
    if event in {"codex_error", "codex_failed", "codex_timeout"}:
        status, _stage, detail = _failure_text(record)
        return status, detail, "error"
    if event in {"response_summarized", "output_summary"}:
        has_output = payload.get("has_output")
        return "Response summarized", f"Output present: {bool(has_output)}", "info"
    if event in {"db_log_started", "db_log_finished", "db_logged"}:
        state = _payload_string(payload, "stored_state") or "iteration result"
        return "History updated", state, "success"
    if event in {"workflow_completed", "completion"}:
        return "Workflow complete", _payload_string(payload, "reason"), "success"
    if event == "max_iterations_reached":
        count = _payload_int(payload, "max_iterations")
        return "Safety stop", f"Max iterations: {count or 0}", "warning"
    if event == "run_stopped":
        reason = _payload_string(payload, "reason")
        if reason == "operator_stop":
            return "Run stopped", "Operator stopped the run.", "warning"
        return "Run stopped", reason, "warning"
    if event in {"error", "event_stream_error"}:
        status, _stage, detail = _failure_text(record)
        return status, detail, "error"
    return event.replace("_", " ").title(), "Event received.", "info"


def _join_detail(*parts: str) -> str:
    return " | ".join(part for part in parts if part)


def _failure_text(record: EventRecord) -> tuple[str, str, str]:
    code = _failure_code(record.payload, record.event)
    status, stage, default_detail = FAILURE_STATE_TEXT.get(
        code, ("Attention needed", "Error", "The wrapper needs attention.")
    )
    detail = _failure_detail(record.payload, default_detail)
    return status, stage, detail


def _failure_code(  # pylint: disable=too-many-return-statements
    payload: Mapping[str, JsonValue], event: str
) -> str:
    if event == "codex_timeout":
        return "timeout"
    stage = _payload_string(payload, "stage")
    error_type = _payload_string(payload, "error_type")
    reason = _payload_string(payload, "reason")
    if reason == "operator_stop":
        return "operator_stop"
    if error_type in FAILURE_STATE_TEXT:
        return error_type
    if stage in {"stderr", "subprocess_stderr"}:
        return "stderr"
    if stage in {"launcher", "launch_validation"}:
        return error_type or "missing_cli"
    if stage in {"display", "display_backend"}:
        return "display_backend"
    if stage in {"wrapper", "dependency"} and error_type == "missing_pyside6":
        return "missing_pyside6"
    if error_type.startswith("return_"):
        return "non_zero_exit"
    if event == "event_stream_error":
        return "malformed_event"
    return error_type or stage or "wrapper"


def _failure_detail(payload: Mapping[str, JsonValue], fallback: str) -> str:
    message = _payload_string(payload, "message")
    if message:
        return message
    return_code = _payload_int(payload, "return_code")
    if return_code is not None:
        return f"Exit code {return_code}"
    timeout_seconds = _payload_int(payload, "timeout_seconds")
    if timeout_seconds is not None:
        return f"Timeout after {timeout_seconds} seconds"
    error_type = _payload_string(payload, "error_type")
    return error_type or fallback
