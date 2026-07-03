"""JSONL event stream support for Apex Infinite CLI."""

from __future__ import annotations

import json
import math
import re
import sys
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Literal, TextIO

EVENT_VERSION = 1

EVENT_NAMES = frozenset(
    {
        "startup_begin",
        "config_loaded",
        "config_resolved",
        "ui_resolved",
        "project_resolved",
        "startup",
        "iteration_started",
        "history_fetched",
        "history_summary_started",
        "history_summary_completed",
        "history_summarize_started",
        "history_summarize_finished",
        "manager_decision_started",
        "manager_decision_completed",
        "manager_decision_finished",
        "prompt_built",
        "prompt_dispatched",
        "codex_dry_run",
        "codex_started",
        "codex_completed",
        "codex_finished",
        "codex_failed",
        "codex_timeout",
        "codex_error",
        "output_summary",
        "response_summarized",
        "db_log_started",
        "db_log_finished",
        "db_logged",
        "help_requested",
        "operator_interrupt_requested",
        "operator_interrupt_quit",
        "operator_input_received",
        "completion",
        "workflow_completed",
        "max_iterations_reached",
        "run_stopped",
        "event_stream_error",
        "error",
    }
)

ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
RICH_MARKUP_PATTERN = re.compile(r"\[(?:/?[a-z][a-z0-9_ -]*|#[0-9A-Fa-f]{3,6})\]")
VISUAL_TOKEN_PATTERN = re.compile(
    r"\b(?:accent|foreground|border|panel|separator|glyph|theme token|"
    r"bright_green)\b",
    re.IGNORECASE,
)
SECRET_VALUE_PATTERN = re.compile(
    r"(?:"
    r"sk-[A-Za-z0-9_-]{20,}|"
    r"AKIA[0-9A-Z]{16}|"
    r"AIza[0-9A-Za-z_-]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{10,}|"
    r"Bearer\s+[A-Za-z0-9._-]{10,}"
    r")"
)
SECRET_KEY_PATTERN = re.compile(
    r"(?:api[_-]?key|secret|token|password|passwd|authorization|credential)",
    re.IGNORECASE,
)
FRAME_GLYPHS = frozenset(
    {
        chr(0x2500),
        chr(0x2502),
        chr(0x250C),
        chr(0x2510),
        chr(0x2514),
        chr(0x2518),
        chr(0x256D),
        chr(0x256E),
        chr(0x2570),
        chr(0x256F),
        chr(0x2572),
        chr(0x2571),
    }
)

JsonScalar = str | int | float | bool | None
JsonValue = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


class EventStreamError(RuntimeError):
    """Raised when event stream creation, validation, or writing fails."""


class NoOpEventEmitter:
    """Disabled event emitter with the same caller contract."""

    enabled = False

    def emit(self, _name: str, _payload: Mapping[str, object] | None = None) -> None:
        """Discard event facts."""

    def close(self) -> None:
        """No-op cleanup."""

    def __enter__(self) -> "NoOpEventEmitter":
        return self

    def __exit__(self, _exc_type, _exc, _traceback) -> Literal[False]:
        self.close()
        return False


class EventEmitter:
    """Write validated lifecycle events as line-buffered JSONL."""

    enabled = True

    def __init__(self, stream: TextIO, close_stream: bool = False):
        self._stream = stream
        self._close_stream = close_stream
        self._closed = False

    def emit(self, name: str, payload: Mapping[str, object] | None = None) -> None:
        """Validate and write one event object."""
        if self._closed:
            raise EventStreamError("event stream is closed")
        validate_event_name(name)
        validated_payload = validate_payload(payload or {})
        event = {
            "version": EVENT_VERSION,
            "event": name,
            "timestamp": _timestamp(),
            "payload": validated_payload,
        }
        try:
            line = json.dumps(event, ensure_ascii=True, sort_keys=True)
            self._stream.write(f"{line}\n")
            self._stream.flush()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise EventStreamError(f"failed to write event stream: {exc}") from exc

    def close(self) -> None:
        """Flush and close the stream if this emitter owns it."""
        if self._closed:
            return
        try:
            self._stream.flush()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            raise EventStreamError(f"failed to flush event stream: {exc}") from exc
        finally:
            if self._close_stream:
                try:
                    self._stream.close()
                finally:
                    self._closed = True
            else:
                self._closed = True

    def __enter__(self) -> "EventEmitter":
        return self

    def __exit__(self, _exc_type, _exc, _traceback) -> Literal[False]:
        self.close()
        return False


EventStream = NoOpEventEmitter | EventEmitter


def open_event_stream(path: str | None, stdout_allowed: bool = False) -> EventStream:
    """Open a file or stdout event stream path."""
    if not path:
        return NoOpEventEmitter()
    if path == "-":
        if not stdout_allowed:
            raise EventStreamError("--event-stream - requires machine output")
        return EventEmitter(sys.stdout, close_stream=False)
    event_path = Path(path)
    try:
        event_path.parent.mkdir(parents=True, exist_ok=True)
        stream = event_path.open(  # pylint: disable=consider-using-with
            "w", encoding="ascii", buffering=1
        )
    except OSError as exc:
        raise EventStreamError(f"failed to open event stream: {exc}") from exc
    return EventEmitter(stream, close_stream=True)


def validate_event_name(name: str) -> str:
    """Validate a stable event name."""
    if not isinstance(name, str) or name not in EVENT_NAMES:
        raise EventStreamError(f"invalid event name: {name!r}")
    return name


def validate_payload(payload: Mapping[str, object]) -> dict[str, JsonValue]:
    """Validate and return a JSON-serializable payload mapping."""
    if not isinstance(payload, Mapping):
        raise EventStreamError("event payload must be a mapping")
    return _validate_mapping(payload, "payload")


def summarize_text(text: str | None, limit: int = 240) -> dict[str, JsonValue]:
    """Return bounded output metadata without exposing full text."""
    raw_text = text or ""
    stripped = raw_text.strip()
    preview = " ".join(stripped.split())
    if len(preview) > limit:
        preview = f"{preview[:limit].rstrip()}..."
    return {
        "length": len(raw_text),
        "line_count": len(raw_text.splitlines()),
        "has_output": bool(stripped),
        "preview": preview,
    }


def _validate_mapping(payload: Mapping[str, object], path: str) -> dict[str, JsonValue]:
    result: dict[str, JsonValue] = {}
    for key, value in payload.items():
        if not isinstance(key, str):
            raise EventStreamError(f"event payload key at {path} must be a string")
        _validate_payload_key(key, f"{path}.{key}")
        result[key] = _validate_value(value, f"{path}.{key}")
    return result


def _validate_sequence(values: Sequence[object], path: str) -> list[JsonValue]:
    return [_validate_value(value, f"{path}[]") for value in values]


def _validate_value(value: object, path: str) -> JsonValue:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, str):
        _validate_payload_string(value, path)
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise EventStreamError(f"event payload value at {path} is not finite JSON")
        return value
    if isinstance(value, Mapping):
        return _validate_mapping(value, path)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return _validate_sequence(value, path)
    raise EventStreamError(f"event payload value at {path} is not JSON serializable")


def _validate_payload_key(key: str, path: str) -> None:
    if SECRET_KEY_PATTERN.search(key):
        raise EventStreamError(f"event payload key at {path} looks secret-like")


def _validate_payload_string(value: str, path: str) -> None:
    if ANSI_ESCAPE_PATTERN.search(value):
        raise EventStreamError(f"event payload string at {path} contains ANSI escapes")
    if RICH_MARKUP_PATTERN.search(value):
        raise EventStreamError(f"event payload string at {path} contains Rich markup")
    if any(glyph in value for glyph in FRAME_GLYPHS):
        raise EventStreamError(f"event payload string at {path} contains frame glyphs")
    if VISUAL_TOKEN_PATTERN.search(value):
        raise EventStreamError(f"event payload string at {path} contains visual tokens")
    if SECRET_VALUE_PATTERN.search(value):
        raise EventStreamError(f"event payload string at {path} looks secret-like")


def _timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
