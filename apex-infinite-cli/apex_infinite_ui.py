"""UI configuration and rendering helpers for Apex Infinite CLI."""

# pylint: disable=too-many-instance-attributes

from __future__ import annotations

import os
import re
from dataclasses import dataclass, fields, replace
from typing import Mapping, Sequence

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

BUILT_IN_THEME_NAMES = ("auto", "crt-green", "crt-amber", "ibm-dos", "plain")
EFFECT_LEVELS = ("off", "low", "medium")
CONCRETE_THEME_NAMES = ("crt-green", "crt-amber", "ibm-dos", "plain")
THEME_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
DEFAULT_UI_CONFIG = {
    "theme": "auto",
    "effect_level": "low",
    "ascii": False,
    "compact": False,
    "show_elapsed": True,
    "show_provider": True,
    "themes": {},
}
UI_CONFIG_KEYS = set(DEFAULT_UI_CONFIG)


@dataclass(frozen=True)
class ThemeTokens:
    """Semantic style tokens used by operator-facing renderers."""

    name: str
    foreground: str
    accent: str
    muted: str
    success: str
    warning: str
    error: str
    panel: str
    border: str
    emphasis: str
    dim: str


@dataclass(frozen=True)
class GlyphSet:
    """Semantic glyph choices for styled and ASCII-safe output."""

    name: str
    bullet: str
    arrow: str
    ok: str
    warn: str
    error: str
    horizontal: str


@dataclass(frozen=True)
class UiCliOverrides:
    """CLI-level UI overrides collected before config resolution."""

    theme: str | None = None
    plain: bool = False
    ascii_only: bool = False
    compact: bool = False


@dataclass(frozen=True)
class UiSettings:
    """Resolved UI settings and display tokens."""

    requested_theme: str
    theme_name: str
    effect_level: str
    ascii_only: bool
    compact: bool
    show_elapsed: bool
    show_provider: bool
    color_enabled: bool
    plain: bool
    constraint_reason: str | None
    tokens: ThemeTokens
    glyphs: GlyphSet


@dataclass(frozen=True)
class StartupSnapshot:
    """Operator-facing startup context."""

    project_path: str
    provider_name: str
    model_name: str
    config_path: str
    max_iterations: int
    theme_name: str
    requested_theme: str
    dry_run: bool
    start_command: str | None = None
    ceo_present: bool = False


@dataclass(frozen=True)
class CodexCommandSnapshot:
    """Display facts for a Codex subprocess command."""

    binary: str
    exec_flags: str
    prompt: str
    project_path: str
    timeout: int | None = None
    return_code: int | None = None


class UiConfigError(ValueError):
    """Raised when UI configuration is malformed."""


THEME_TOKEN_FIELDS = tuple(
    field.name for field in fields(ThemeTokens) if field.name != "name"
)


BUILT_IN_THEMES: Mapping[str, ThemeTokens] = {
    "auto": ThemeTokens(
        name="auto",
        foreground="bright_green",
        accent="cyan",
        muted="green4",
        success="bright_green",
        warning="yellow",
        error="bright_red",
        panel="green",
        border="bright_green",
        emphasis="bold bright_green",
        dim="dim green",
    ),
    "crt-green": ThemeTokens(
        name="crt-green",
        foreground="bright_green",
        accent="spring_green2",
        muted="green4",
        success="bright_green",
        warning="khaki1",
        error="orange_red1",
        panel="green",
        border="spring_green2",
        emphasis="bold spring_green2",
        dim="dim green",
    ),
    "crt-amber": ThemeTokens(
        name="crt-amber",
        foreground="bright_yellow",
        accent="orange1",
        muted="dark_orange3",
        success="green3",
        warning="bright_yellow",
        error="red1",
        panel="dark_orange3",
        border="orange1",
        emphasis="bold orange1",
        dim="dim yellow",
    ),
    "ibm-dos": ThemeTokens(
        name="ibm-dos",
        foreground="bright_white",
        accent="bright_cyan",
        muted="blue",
        success="bright_green",
        warning="bright_yellow",
        error="bright_red",
        panel="blue",
        border="bright_blue",
        emphasis="bold bright_white",
        dim="dim white",
    ),
    "plain": ThemeTokens(
        name="plain",
        foreground="white",
        accent="white",
        muted="white",
        success="white",
        warning="white",
        error="white",
        panel="white",
        border="white",
        emphasis="white",
        dim="white",
    ),
}

UNICODE_GLYPHS = GlyphSet(
    name="unicode",
    bullet=chr(0x2022),
    arrow=chr(0x2192),
    ok=chr(0x2713),
    warn="!",
    error="x",
    horizontal=chr(0x2500),
)

ASCII_GLYPHS = GlyphSet(
    name="ascii",
    bullet="*",
    arrow="->",
    ok="OK",
    warn="!",
    error="x",
    horizontal="-",
)


def _format_allowed(values: tuple[str, ...] | list[str]) -> str:
    return ", ".join(sorted(values))


def _validate_theme_name(name: object, field_name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise UiConfigError(f"{field_name} must be a non-empty string")
    normalized = name.strip()
    if not THEME_NAME_PATTERN.fullmatch(normalized):
        raise UiConfigError(
            f"{field_name} must use lowercase letters, numbers, and hyphens"
        )
    return normalized


def _require_mapping(value: object, field_name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise UiConfigError(f"{field_name} must be a mapping")
    return value


def _validate_token_overrides(
    theme_name: str, value: object
) -> tuple[str, dict[str, str]]:
    raw_theme = _require_mapping(value, f"ui.themes.{theme_name}")
    allowed_keys = set(THEME_TOKEN_FIELDS) | {"base"}
    unknown_keys = sorted(set(raw_theme) - allowed_keys)
    if unknown_keys:
        raise UiConfigError(
            f"ui.themes.{theme_name} has unknown keys: "
            f"{', '.join(unknown_keys)}. Allowed keys: "
            f"{_format_allowed(list(allowed_keys))}"
        )

    base_name = raw_theme.get("base")
    if base_name is None:
        base_name = theme_name if theme_name in CONCRETE_THEME_NAMES else "crt-green"
    if not isinstance(base_name, str):
        raise UiConfigError(f"ui.themes.{theme_name}.base must be a string")
    base_name = base_name.strip()
    if base_name not in CONCRETE_THEME_NAMES:
        raise UiConfigError(
            f"ui.themes.{theme_name}.base must be one of: "
            f"{_format_allowed(CONCRETE_THEME_NAMES)}"
        )

    token_values = {
        key: raw_theme[key]
        for key in THEME_TOKEN_FIELDS
        if key in raw_theme and raw_theme[key] is not None
    }
    if not token_values:
        raise UiConfigError(
            f"ui.themes.{theme_name} must define at least one token override"
        )

    validated: dict[str, str] = {}
    for key, token_value in token_values.items():
        if not isinstance(token_value, str) or not token_value.strip():
            raise UiConfigError(
                f"ui.themes.{theme_name}.{key} must be a non-empty string"
            )
        validated[key] = token_value.strip()
    return base_name, validated


def build_theme_registry(raw_themes: object | None) -> dict[str, ThemeTokens]:
    """Build the theme registry from built-ins plus validated custom overrides."""
    registry = dict(BUILT_IN_THEMES)
    if raw_themes in (None, {}):
        return registry

    themes = _require_mapping(raw_themes, "ui.themes")
    for raw_name, raw_theme in themes.items():
        theme_name = _validate_theme_name(raw_name, "ui.themes theme name")
        base_name, token_values = _validate_token_overrides(theme_name, raw_theme)
        registry[theme_name] = replace(
            registry[base_name],
            name=theme_name,
            **token_values,
        )
    return registry


def _read_ui_config(config: Mapping[str, object]) -> Mapping[str, object]:
    root = _require_mapping(config, "config")
    raw_ui = root.get("ui", {})
    if raw_ui is None:
        raw_ui = {}
    ui_config = _require_mapping(raw_ui, "ui")
    unknown_keys = sorted(set(ui_config) - UI_CONFIG_KEYS)
    if unknown_keys:
        raise UiConfigError(
            f"ui has unknown keys: {', '.join(unknown_keys)}. "
            f"Allowed keys: {_format_allowed(sorted(UI_CONFIG_KEYS))}"
        )
    return ui_config


def _read_bool(ui_config: Mapping[str, object], key: str, default: bool) -> bool:
    value = ui_config.get(key, default)
    if not isinstance(value, bool):
        raise UiConfigError(f"ui.{key} must be true or false")
    return value


def _read_str(ui_config: Mapping[str, object], key: str, default: str) -> str:
    value = ui_config.get(key, default)
    if not isinstance(value, str) or not value.strip():
        raise UiConfigError(f"ui.{key} must be a non-empty string")
    return value.strip()


def _read_theme_name(
    value: str | None, field_name: str, registry: Mapping[str, ThemeTokens]
) -> str:
    theme_name = _validate_theme_name(value, field_name)
    if theme_name not in registry:
        raise UiConfigError(
            f"{field_name} must be one of: {_format_allowed(list(registry))}"
        )
    return theme_name


def _read_effect_level(ui_config: Mapping[str, object]) -> str:
    effect_level = _read_str(
        ui_config, "effect_level", str(DEFAULT_UI_CONFIG["effect_level"])
    )
    if effect_level not in EFFECT_LEVELS:
        raise UiConfigError(
            f"ui.effect_level must be one of: {_format_allowed(EFFECT_LEVELS)}"
        )
    return effect_level


def _detect_output_constraint(
    env: Mapping[str, str], console: object | None
) -> str | None:
    if "NO_COLOR" in env:
        return "NO_COLOR"
    if env.get("TERM", "").lower() == "dumb":
        return "TERM=dumb"
    if console is not None and not bool(getattr(console, "is_terminal", True)):
        return "non-terminal output"
    return None


# pylint: disable-next=too-many-locals
def resolve_ui_settings(
    config: Mapping[str, object],
    cli_overrides: UiCliOverrides | None = None,
    env: Mapping[str, str] | None = None,
    console: object | None = None,
) -> UiSettings:
    """Resolve UI settings from config, environment, CLI flags, and defaults."""
    overrides = cli_overrides or UiCliOverrides()
    current_env = os.environ if env is None else env
    ui_config = _read_ui_config(config)
    registry = build_theme_registry(
        ui_config.get("themes", DEFAULT_UI_CONFIG["themes"])
    )

    config_theme = _read_theme_name(
        _read_str(ui_config, "theme", str(DEFAULT_UI_CONFIG["theme"])),
        "ui.theme",
        registry,
    )
    requested_theme = config_theme
    explicit_theme = False
    if overrides.theme is not None:
        requested_theme = _read_theme_name(overrides.theme, "--theme", registry)
        explicit_theme = True

    effect_level = _read_effect_level(ui_config)
    ascii_only = _read_bool(ui_config, "ascii", bool(DEFAULT_UI_CONFIG["ascii"]))
    compact = _read_bool(ui_config, "compact", bool(DEFAULT_UI_CONFIG["compact"]))
    show_elapsed = _read_bool(
        ui_config, "show_elapsed", bool(DEFAULT_UI_CONFIG["show_elapsed"])
    )
    show_provider = _read_bool(
        ui_config, "show_provider", bool(DEFAULT_UI_CONFIG["show_provider"])
    )

    if overrides.ascii_only:
        ascii_only = True
    if overrides.compact:
        compact = True

    constraint_reason = _detect_output_constraint(current_env, console)
    applied_constraint = None

    if overrides.plain:
        theme_name = "plain"
        resolved_effect = "off"
        color_enabled = False
        plain = True
    elif requested_theme == "auto":
        if constraint_reason:
            theme_name = "plain"
            resolved_effect = "off"
            color_enabled = False
            plain = True
            applied_constraint = constraint_reason
        else:
            theme_name = "crt-green"
            resolved_effect = effect_level
            color_enabled = True
            plain = False
    elif constraint_reason and not explicit_theme:
        theme_name = "plain"
        resolved_effect = "off"
        color_enabled = False
        plain = True
        applied_constraint = constraint_reason
    else:
        theme_name = requested_theme
        resolved_effect = "off" if theme_name == "plain" else effect_level
        color_enabled = theme_name != "plain"
        plain = theme_name == "plain"

    return UiSettings(
        requested_theme=requested_theme,
        theme_name=theme_name,
        effect_level=resolved_effect,
        ascii_only=ascii_only,
        compact=compact,
        show_elapsed=show_elapsed,
        show_provider=show_provider,
        color_enabled=color_enabled,
        plain=plain,
        constraint_reason=applied_constraint,
        tokens=registry[theme_name],
        glyphs=ASCII_GLYPHS if ascii_only or plain else UNICODE_GLYPHS,
    )


class ApexRenderer:
    """Semantic renderer for operator-facing CLI output."""

    def __init__(self, settings: UiSettings, output_console: Console | None = None):
        self.settings = settings
        self.console = output_console or Console(no_color=not settings.color_enabled)

    def print_block(
        self,
        title: str,
        rows: Sequence[tuple[str, object] | str],
        severity: str = "accent",
    ) -> None:
        """Print a semantic block using the active renderer mode."""
        if self.settings.plain:
            self._print_plain_block(title, rows, severity)
            return

        body = Text()
        for index, row in enumerate(rows):
            if isinstance(row, tuple):
                label, value = row
                body.append(f"{label}: ", style=self.settings.tokens.emphasis)
                body.append(str(value), style=self.settings.tokens.foreground)
            else:
                body.append(str(row), style=self.settings.tokens.foreground)
            if index < len(rows) - 1:
                body.append("\n")
        self.console.print(
            Panel(
                body,
                title=title,
                border_style=self._style(severity),
                box=box.ASCII if self.settings.ascii_only else box.ROUNDED,
                expand=False,
            )
        )

    def print_startup(self, snapshot: StartupSnapshot) -> None:
        """Render startup context before the loop begins."""
        rows: list[tuple[str, object] | str] = [
            ("Project", snapshot.project_path),
            ("Provider", f"{snapshot.provider_name} ({snapshot.model_name})"),
            ("Config", snapshot.config_path),
            ("Max iterations", snapshot.max_iterations),
            ("Theme", f"{snapshot.theme_name} (requested {snapshot.requested_theme})"),
            ("Dry run", "yes" if snapshot.dry_run else "no"),
        ]
        if self.settings.constraint_reason:
            rows.append(("Output fallback", self.settings.constraint_reason))
        if snapshot.start_command:
            rows.append(("Start command", snapshot.start_command))
        if snapshot.ceo_present:
            rows.append(("CEO instructions", "provided"))
        self.print_block("Apex Infinite CLI", rows)

    def print_intro(self) -> None:
        """Render the interactive startup intro."""
        self.print_block("Apex Infinite CLI", ["Autonomous Codex session manager"])

    def print_project_list(self, project_dirs: Sequence[object]) -> None:
        """Render available project choices."""
        rows = [
            (str(index), f"~/{directory.relative_to(directory.home())}/")
            for index, directory in enumerate(project_dirs, 1)
        ]
        self.print_block("Available projects", rows)

    def input_prompt(self, label: str) -> str:
        """Return a prompt string appropriate for the active output mode."""
        if self.settings.plain:
            return f"{label}: "
        return f"[bold]{label}: [/bold]"

    def print_error(self, message: str, title: str = "Error") -> None:
        """Render a visible error block."""
        self.print_block(title, [message], severity="error")

    def print_warning(self, message: str, title: str = "Warning") -> None:
        """Render a visible warning block."""
        self.print_block(title, [message], severity="warning")

    def print_status(self, message: str, title: str = "Status") -> None:
        """Render an operator status block."""
        self.print_block(title, [message])

    def print_history(
        self,
        rows: Sequence[Mapping[str, object]],
        verbose: bool = False,
    ) -> None:
        """Render SQLite history rows without mutating stored data."""
        if not rows:
            self.print_status("No history records found.", "History")
            return
        if self.settings.plain:
            self._print_plain_history(rows, verbose)
            return

        table = Table(
            title="Apex Infinite - History",
            show_lines=not self.settings.compact,
            box=box.ASCII if self.settings.ascii_only else box.SIMPLE,
        )
        overflow = "crop" if self.settings.ascii_only else None
        table.add_column(
            "ID", style=self.settings.tokens.dim, width=5, overflow=overflow
        )
        table.add_column(
            "Time", style=self.settings.tokens.dim, width=19, overflow=overflow
        )
        table.add_column(
            "Project",
            style=self.settings.tokens.accent,
            max_width=28,
            overflow=overflow,
        )
        table.add_column(
            "Manager",
            style=self.settings.tokens.success,
            max_width=20,
            overflow=overflow,
        )
        table.add_column("Reason", max_width=40, overflow=overflow)
        table.add_column("Response", max_width=50 if verbose else 34, overflow=overflow)
        table.add_column(
            "State", style=self.settings.tokens.warning, max_width=16, overflow=overflow
        )
        for row in rows:
            table.add_row(
                str(row.get("id", "")),
                str(row.get("created_at", "")),
                self._truncate(str(row.get("path", "") or ""), 48),
                self._truncate(str(row.get("ai_decision_output", "") or ""), 28),
                self._truncate(str(row.get("ai_decision_reason", "") or ""), 80),
                self._truncate(str(row.get("cc_response", "") or ""), 160),
                self._truncate(str(row.get("help_or_done_msg", "") or ""), 32),
            )
        self.console.print(table)

    def print_iteration(self, iteration: int, operation: str | None = None) -> None:
        """Render the current loop iteration."""
        rows: list[tuple[str, object] | str] = [("Iteration", iteration)]
        if operation:
            rows.append(("Operation", operation))
        self.print_block("Iteration", rows)

    def print_manager_decision(
        self, output_value: str, reason: str, known_command: bool
    ) -> None:
        """Render the manager decision and reason."""
        decision_type = "workflow command" if known_command else "custom instruction"
        self.print_block(
            "Manager Decision",
            [
                ("Output", output_value),
                ("Type", decision_type),
                ("Reason", reason or "No reason supplied"),
            ],
        )

    def print_prompt_preview(self, prompt: str) -> None:
        """Render a width-aware prompt preview."""
        self.print_block(
            "Prompt Preview", [self._truncate(prompt, self._preview_width())]
        )

    def print_codex_command(self, state: str, snapshot: CodexCommandSnapshot) -> None:
        """Render Codex execution state, dry-run, or failure details."""
        rows: list[tuple[str, object] | str] = [
            ("State", state),
            ("Binary", snapshot.binary),
            ("Project", snapshot.project_path),
        ]
        if snapshot.exec_flags:
            rows.append(("Flags", snapshot.exec_flags))
        if snapshot.timeout is not None:
            rows.append(("Timeout", f"{snapshot.timeout}s"))
        if snapshot.return_code is not None:
            rows.append(("Return code", snapshot.return_code))
        rows.append(("Prompt", self._truncate(snapshot.prompt, self._preview_width())))
        severity = (
            "error"
            if state in {"timeout", "missing", "error", "non-zero"}
            else "accent"
        )
        self.print_block("Codex Execution", rows, severity=severity)

    def print_agent_response(self, output: str, verbose: bool = False) -> None:
        """Render captured Codex output without altering the returned raw value."""
        limit = 2000 if verbose else 500
        rendered = output if verbose else self._truncate(output, limit)
        self.print_block("Agent Response", [rendered or "(empty response)"])

    def print_interrupt(self, state: str, message: str) -> None:
        """Render interrupt and operator pause states."""
        severity = "error" if state == "force-quit" else "warning"
        self.print_block(
            "Operator Interrupt", [("State", state), ("Message", message)], severity
        )

    def print_help(self, reason: str) -> None:
        """Render emergency help pause state."""
        self.print_block("Manager Needs Help", [("Reason", reason)], severity="warning")

    def print_completion(self, reason: str, iteration: int) -> None:
        """Render workflow completion state."""
        self.print_block(
            "Project Complete",
            [("Reason", reason), ("Total iterations", iteration)],
            severity="success",
        )

    def print_max_iterations(self, max_iterations: int) -> None:
        """Render safety stop at max iterations."""
        self.print_block(
            "Safety Stop",
            [f"Reached max iterations ({max_iterations}). Stopping."],
            severity="warning",
        )

    def print_llm_retry(
        self, attempt: int, total: int, error: object, wait_seconds: int = 5
    ) -> None:
        """Render LLM retry state."""
        self.print_block(
            "LLM Retry",
            [
                ("Attempt", f"{attempt}/{total}"),
                ("Error", error),
                ("Next wait", f"{wait_seconds}s"),
            ],
            severity="warning",
        )

    def print_json_fallback(self) -> None:
        """Render manager JSON parsing fallback state."""
        self.print_warning(
            "Could not parse LLM response as JSON; using raw output.",
            "Manager Parse Fallback",
        )

    def _print_plain_block(
        self,
        title: str,
        rows: Sequence[tuple[str, object] | str],
        severity: str,
    ) -> None:
        label = severity.upper()
        if not self.settings.compact:
            self.console.print(self._separator())
        self.console.print(f"{label} {title}")
        for row in rows:
            if isinstance(row, tuple):
                row_label, value = row
                self.console.print(f"{row_label}: {value}")
            else:
                self.console.print(str(row))
        if not self.settings.compact:
            self.console.print(self._separator())

    def _print_plain_history(
        self, rows: Sequence[Mapping[str, object]], verbose: bool
    ) -> None:
        self._print_plain_block("History", [f"Rows: {len(rows)}"], "accent")
        response_limit = 160 if verbose else 80
        for row in rows:
            parts = [
                f"ID {row.get('id', '')}",
                str(row.get("created_at", "") or ""),
                self._truncate(str(row.get("path", "") or ""), 48),
                f"manager={self._truncate(str(row.get('ai_decision_output', '') or ''), 28)}",
                f"state={self._truncate(str(row.get('help_or_done_msg', '') or ''), 24)}",
            ]
            self.console.print(" | ".join(parts))
            reason = str(row.get("ai_decision_reason", "") or "")
            response = str(row.get("cc_response", "") or "")
            if reason:
                self.console.print(f"Reason: {self._truncate(reason, 100)}")
            if response:
                self.console.print(
                    f"Response: {self._truncate(response, response_limit)}"
                )

    def _separator(self) -> str:
        width = max(24, min(self._console_width(), 80))
        return self.settings.glyphs.horizontal * width

    def _console_width(self) -> int:
        return int(getattr(self.console, "width", 100) or 100)

    def _preview_width(self) -> int:
        return max(60, min(self._console_width() - 12, 180))

    def _truncate(self, value: str, limit: int) -> str:
        clean = " ".join(str(value).split())
        if len(clean) <= limit:
            return clean
        suffix = f"... ({len(clean)} chars total)"
        return clean[: max(0, limit - len(suffix))].rstrip() + suffix

    def _style(self, severity: str) -> str:
        token = self.settings.tokens
        styles = {
            "accent": token.border,
            "success": token.success,
            "warning": token.warning,
            "error": token.error,
        }
        return styles.get(severity, token.border)
