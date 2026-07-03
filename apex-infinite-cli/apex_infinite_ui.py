"""UI configuration and rendering helpers for Apex Infinite CLI."""

# pylint: disable=too-many-instance-attributes,too-many-lines

from __future__ import annotations

import os
import re
from dataclasses import dataclass, fields, replace
from pathlib import Path
from typing import Mapping, Sequence

from rich import box
from rich.console import Console
from rich.panel import Panel
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
    info: str
    dry_run: str
    complete: str
    separator: str
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
    process_state: str | None = None
    elapsed_seconds: float | None = None


@dataclass(frozen=True)
class IterationSnapshot:
    """Display facts for an autonomous loop iteration."""

    project_path: str
    provider_name: str
    model_name: str
    iteration: int
    operation: str
    dry_run: bool
    elapsed_seconds: float | None = None


@dataclass(frozen=True)
class DbLogSnapshot:
    """Display facts for a successful durable history write."""

    project_path: str
    manager_output: str
    stored_state: str
    created_at: str | None = None


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
        info="bright_cyan",
        dry_run="magenta",
        complete="bright_green",
        separator="green4",
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
        info="spring_green2",
        dry_run="magenta",
        complete="bright_green",
        separator="green4",
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
        info="orange1",
        dry_run="dark_orange",
        complete="green3",
        separator="dark_orange3",
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
        info="bright_cyan",
        dry_run="bright_magenta",
        complete="bright_green",
        separator="blue",
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
        info="white",
        dry_run="white",
        complete="white",
        separator="white",
        panel="white",
        border="white",
        emphasis="white",
        dim="white",
    ),
}

SEMANTIC_LABELS: Mapping[str, str] = {
    "boot": "BOOT",
    "iteration": "ITERATION",
    "history": "HISTORY",
    "decision": "DECISION",
    "prompt": "PROMPT",
    "executing": "EXECUTING",
    "dry_run": "DRY RUN",
    "response": "RESPONSE",
    "logged": "LOGGED",
    "help": "HELP",
    "interrupt": "INTERRUPT",
    "timeout": "TIMEOUT",
    "error": "ERROR",
    "complete": "COMPLETE",
    "stop": "STOP",
}

CODEX_STATE_LABELS: Mapping[str, str] = {
    "dry-run": SEMANTIC_LABELS["dry_run"],
    "start": SEMANTIC_LABELS["executing"],
    "complete": SEMANTIC_LABELS["complete"],
    "non-zero": SEMANTIC_LABELS["error"],
    "timeout": SEMANTIC_LABELS["timeout"],
    "missing": SEMANTIC_LABELS["error"],
    "error": SEMANTIC_LABELS["error"],
}

CODEX_STATE_TEXT: Mapping[str, str] = {
    "dry-run": "No Codex subprocess launched",
    "start": "Codex subprocess starting",
    "complete": "Codex subprocess completed",
    "non-zero": "Codex exited with a non-zero status",
    "timeout": "Codex command timed out",
    "missing": "Codex binary was not found",
    "error": "Codex execution failed",
}

UNICODE_GLYPHS = GlyphSet(
    name="unicode",
    bullet=chr(0x2022),
    arrow=chr(0x2192),
    ok=chr(0x2713),
    warn="!",
    error="x",
    horizontal="-",
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


class NoHumanOutputRenderer:  # pylint: disable=too-many-public-methods
    """Renderer adapter that suppresses all human-facing output."""

    def __init__(self, settings: UiSettings | None = None):
        self.settings = settings

    def input_prompt(self, _label: str) -> str:
        """Return an empty prompt so stdout stays machine-readable."""
        return ""

    def print_block(self, *_args, **_kwargs) -> None:
        """Suppress generic blocks."""

    def print_startup(self, *_args, **_kwargs) -> None:
        """Suppress startup output."""

    def print_intro(self, *_args, **_kwargs) -> None:
        """Suppress intro output."""

    def print_project_list(self, *_args, **_kwargs) -> None:
        """Suppress project list output."""

    def print_error(self, *_args, **_kwargs) -> None:
        """Suppress human errors."""

    def print_warning(self, *_args, **_kwargs) -> None:
        """Suppress warnings."""

    def print_status(self, *_args, **_kwargs) -> None:
        """Suppress status output."""

    def print_history(self, *_args, **_kwargs) -> None:
        """Suppress history output."""

    def print_iteration(self, *_args, **_kwargs) -> None:
        """Suppress iteration output."""

    def print_manager_decision(self, *_args, **_kwargs) -> None:
        """Suppress manager decisions."""

    def print_prompt_preview(self, *_args, **_kwargs) -> None:
        """Suppress prompt previews."""

    def print_codex_command(self, *_args, **_kwargs) -> None:
        """Suppress subprocess status output."""

    def print_agent_response(self, *_args, **_kwargs) -> None:
        """Suppress agent response output."""

    def print_db_log(self, *_args, **_kwargs) -> None:
        """Suppress DB log output."""

    def print_interrupt(self, *_args, **_kwargs) -> None:
        """Suppress interrupt output."""

    def print_help(self, *_args, **_kwargs) -> None:
        """Suppress help output."""

    def print_completion(self, *_args, **_kwargs) -> None:
        """Suppress completion output."""

    def print_max_iterations(self, *_args, **_kwargs) -> None:
        """Suppress safety-stop output."""

    def print_llm_retry(self, *_args, **_kwargs) -> None:
        """Suppress retry output."""

    def print_json_fallback(self, *_args, **_kwargs) -> None:
        """Suppress manager parse fallback output."""

    def print_status_strip(self, *_args, **_kwargs) -> None:
        """Suppress status strip output."""


class ApexRenderer:  # pylint: disable=too-many-public-methods
    """Semantic renderer for operator-facing CLI output."""

    def __init__(self, settings: UiSettings, output_console: Console | None = None):
        self.settings = settings
        self.console = output_console or Console(no_color=not settings.color_enabled)

    def print_block(
        self,
        title: str,
        rows: Sequence[tuple[str, object] | str],
        severity: str = "accent",
        label: str | None = None,
    ) -> None:
        """Print a semantic block using the active renderer mode."""
        block_label = label or self._label_for_title(title, severity)
        if self.settings.plain:
            self._print_plain_block(title, rows, severity, block_label)
            return

        self._print_effect_separator()
        panel_title = f"{block_label} {title}" if block_label else title
        body = Text()
        for index, row in enumerate(rows):
            if isinstance(row, tuple):
                row_label, value = row
                body.append(f"{row_label}: ", style=self.settings.tokens.emphasis)
                body.append(str(value), style=self.settings.tokens.foreground)
            else:
                body.append(str(row), style=self.settings.tokens.foreground)
            if index < len(rows) - 1:
                body.append("\n")
        self.console.print(
            Panel(
                body,
                title=panel_title,
                border_style=self._style(severity),
                box=box.ASCII if self.settings.ascii_only else box.ROUNDED,
                expand=False,
            )
        )

    def print_startup(self, snapshot: StartupSnapshot) -> None:
        """Render startup context before the loop begins."""
        rows: list[tuple[str, object] | str] = [
            ("Project", snapshot.project_path),
            ("Provider", snapshot.provider_name),
            ("Model", snapshot.model_name),
            ("Config", snapshot.config_path),
            ("Max iterations", snapshot.max_iterations),
            (
                "Theme",
                f"{snapshot.theme_name} requested={snapshot.requested_theme}",
            ),
            ("Effects", self.settings.effect_level),
            ("Glyphs", self.settings.glyphs.name),
            ("Dry run", "enabled" if snapshot.dry_run else "disabled"),
        ]
        if self.settings.constraint_reason:
            rows.append(("Output fallback", self.settings.constraint_reason))
        if snapshot.start_command:
            rows.append(("Start command", snapshot.start_command))
        if snapshot.ceo_present:
            rows.append(("CEO instructions", "provided"))
        self.print_block(
            "Apex Infinite Operator Console",
            rows,
            label=SEMANTIC_LABELS["boot"],
        )

    def print_intro(self) -> None:
        """Render the interactive startup intro."""
        self.print_block(
            "Apex Infinite CLI",
            ["Autonomous Codex session manager"],
            label=SEMANTIC_LABELS["boot"],
        )

    def print_project_list(self, project_dirs: Sequence[Path]) -> None:
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

    def print_status(
        self, message: str, title: str = "Status", label: str | None = None
    ) -> None:
        """Render an operator status block."""
        self.print_block(title, [message], label=label)

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

        self.print_block(
            "Apex Infinite - History",
            self._history_display_rows(rows, verbose),
            label=SEMANTIC_LABELS["history"],
        )

    def print_iteration(
        self, iteration: int | IterationSnapshot, operation: str | None = None
    ) -> None:
        """Render the current loop iteration."""
        if isinstance(iteration, IterationSnapshot):
            snapshot = iteration
        else:
            snapshot = IterationSnapshot(
                project_path="",
                provider_name="",
                model_name="",
                iteration=iteration,
                operation=operation or "working",
                dry_run=False,
            )
        self.print_status_strip(snapshot)

    def print_manager_decision(
        self, output_value: str, reason: str, known_command: bool
    ) -> None:
        """Render the manager decision and reason."""
        decision_type = "workflow command" if known_command else "custom instruction"
        preview_width = self._preview_width()
        self.print_block(
            "Manager Decision",
            [
                ("Output", self._truncate(output_value, preview_width)),
                ("Type", decision_type),
                (
                    "Reason",
                    self._truncate(reason or "No reason supplied", preview_width),
                ),
            ],
            label=SEMANTIC_LABELS["decision"],
        )

    def print_prompt_preview(self, prompt: str) -> None:
        """Render a width-aware prompt preview."""
        self.print_block(
            "Prompt Preview",
            [
                ("Length", f"{len(prompt)} chars"),
                ("Preview", self._truncate(prompt, self._preview_width())),
            ],
            label=SEMANTIC_LABELS["prompt"],
        )

    def print_codex_command(self, state: str, snapshot: CodexCommandSnapshot) -> None:
        """Render Codex execution state, dry-run, or failure details."""
        state_label = CODEX_STATE_LABELS.get(state, SEMANTIC_LABELS["executing"])
        rows: list[tuple[str, object] | str] = [
            ("State", CODEX_STATE_TEXT.get(state, state)),
            ("Binary", snapshot.binary),
            ("Project", snapshot.project_path),
        ]
        if snapshot.process_state:
            rows.append(("Process state", snapshot.process_state))
        if snapshot.elapsed_seconds is not None:
            rows.append(("Elapsed", self._format_elapsed(snapshot.elapsed_seconds)))
        if snapshot.exec_flags:
            rows.append(("Flags", snapshot.exec_flags))
        if snapshot.timeout is not None:
            rows.append(("Timeout", f"{snapshot.timeout}s"))
        if snapshot.return_code is not None:
            rows.append(("Return code", snapshot.return_code))
        rows.append(("Prompt", self._truncate(snapshot.prompt, self._preview_width())))
        self.print_block(
            "Codex Execution",
            rows,
            severity=self._codex_severity(state),
            label=state_label,
        )

    def print_agent_response(self, output: str, verbose: bool = False) -> None:
        """Render captured Codex output without altering the returned raw value."""
        limit = 2000 if verbose else 500
        rendered = output if verbose else self._truncate(output, limit)
        self.print_block(
            "Agent Response",
            [
                ("Mode", "verbose" if verbose else "summary"),
                ("Output", rendered or "(empty response)"),
            ],
            label=SEMANTIC_LABELS["response"],
        )

    def print_db_log(self, snapshot: DbLogSnapshot) -> None:
        """Render a successful SQLite history write without mutating row data."""
        rows: list[tuple[str, object] | str] = [
            ("Project", snapshot.project_path),
            ("Manager output", snapshot.manager_output or "(empty)"),
            ("Stored state", snapshot.stored_state or "history row"),
        ]
        if snapshot.created_at:
            rows.append(("Recorded at", snapshot.created_at))
        self.print_block(
            "History Write",
            rows,
            severity="success",
            label=SEMANTIC_LABELS["logged"],
        )

    def print_interrupt(self, state: str, message: str) -> None:
        """Render interrupt and operator pause states."""
        severity = "error" if state == "force-quit" else "warning"
        self.print_block(
            "Operator Interrupt",
            [("State", state), ("Message", message)],
            severity,
            label=SEMANTIC_LABELS["interrupt"],
        )

    def print_help(self, reason: str) -> None:
        """Render emergency help pause state."""
        self.print_block(
            "Manager Needs Help",
            [("Reason", reason)],
            severity="warning",
            label=SEMANTIC_LABELS["help"],
        )

    def print_completion(self, reason: str, iteration: int) -> None:
        """Render workflow completion state."""
        self.print_block(
            "Project Complete",
            [("Reason", reason), ("Total iterations", iteration)],
            severity="success",
            label=SEMANTIC_LABELS["complete"],
        )

    def print_max_iterations(self, max_iterations: int) -> None:
        """Render safety stop at max iterations."""
        self.print_block(
            "Safety Stop",
            [f"Reached max iterations ({max_iterations}). Stopping."],
            severity="warning",
            label=SEMANTIC_LABELS["stop"],
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
            label=SEMANTIC_LABELS["error"],
        )

    def print_json_fallback(self) -> None:
        """Render manager JSON parsing fallback state."""
        self.print_status(
            "Could not parse LLM response as JSON; using raw output.",
            "Manager Parse Fallback",
            label=SEMANTIC_LABELS["decision"],
        )

    def print_status_strip(self, snapshot: IterationSnapshot) -> None:
        """Render a stable iteration frame and status strip."""
        self.print_block(
            "Iteration Frame",
            self._status_rows(snapshot),
            severity="dry-run" if snapshot.dry_run else "accent",
            label=SEMANTIC_LABELS["iteration"],
        )

    def _print_plain_block(
        self,
        title: str,
        rows: Sequence[tuple[str, object] | str],
        severity: str,
        label: str | None,
    ) -> None:
        block_label = label or severity.upper()
        self.console.print(f"{block_label} {title}")
        for row in rows:
            if isinstance(row, tuple):
                row_label, value = row
                self.console.print(f"{row_label}: {value}")
            else:
                self.console.print(str(row))

    def _print_plain_history(
        self, rows: Sequence[Mapping[str, object]], verbose: bool
    ) -> None:
        self._print_plain_block(
            "History",
            self._history_display_rows(rows, verbose),
            "accent",
            SEMANTIC_LABELS["history"],
        )

    def _history_display_rows(
        self, rows: Sequence[Mapping[str, object]], verbose: bool
    ) -> list[tuple[str, object] | str]:
        display_rows: list[tuple[str, object] | str] = [("Rows", len(rows))]
        for index, row in enumerate(rows, 1):
            display_rows.append((f"Row {index}", self._history_summary_line(row)))
            display_rows.extend(self._history_detail_rows(row, verbose))
        return display_rows

    def _history_summary_line(self, row: Mapping[str, object]) -> str:
        row_id = self._history_text(row, "id", "?")
        timestamp = self._history_text(row, "created_at", "unknown-time")
        status = self._history_status(row)
        project = self._history_project_key(row.get("path"))
        command = self._truncate(
            self._history_text(row, "ai_decision_output", "(blank)"),
            28,
        )
        return (
            f"#{row_id} {timestamp} "
            f"status={status} project={project} command={command}"
        )

    def _history_detail_rows(
        self, row: Mapping[str, object], verbose: bool
    ) -> list[tuple[str, object]]:
        reason_limit = 160 if verbose else 72
        response_limit = 220 if verbose else 88
        detail_rows: list[tuple[str, object]] = [
            (
                "Path",
                self._truncate(
                    self._history_text(row, "path", "(blank)"),
                    160 if verbose else 48,
                ),
            ),
            (
                "Reason",
                self._truncate(
                    self._history_text(row, "ai_decision_reason", "(blank)"),
                    reason_limit,
                ),
            ),
            (
                "Response",
                self._truncate(
                    self._history_text(row, "cc_response", "(blank)"),
                    response_limit,
                ),
            ),
        ]
        if verbose:
            detail_rows.append(
                (
                    "Stored state",
                    self._truncate(
                        self._history_text(row, "help_or_done_msg", "(blank)"),
                        80,
                    ),
                )
            )
        return detail_rows

    def _history_status(self, row: Mapping[str, object]) -> str:
        stored_state = self._history_text(row, "help_or_done_msg", "")
        if stored_state:
            return self._truncate(stored_state, 24)
        command = self._history_text(row, "ai_decision_output", "").lower()
        if command == "alldonebaby":
            return "complete"
        if command == "help":
            return "help"
        if command:
            return "iteration"
        return "legacy"

    def _history_project_key(self, path: object) -> str:
        normalized = " ".join(str(path or "").split()).rstrip("/")
        if not normalized:
            return "(unknown)"
        return self._truncate(normalized.rsplit("/", maxsplit=1)[-1] or normalized, 24)

    def _history_text(
        self,
        row: Mapping[str, object],
        key: str,
        fallback: str,
    ) -> str:
        value = row.get(key)
        text = " ".join(str(value).split()) if value is not None else ""
        return text or fallback

    def _separator(self) -> str:
        width = max(24, min(self._console_width(), 80))
        return self.settings.glyphs.horizontal * width

    def _print_effect_separator(self) -> None:
        if not self._effects_enabled():
            return
        self.console.print(
            Text(self._separator(), style=self.settings.tokens.separator)
        )

    def _effects_enabled(self) -> bool:
        return (
            not self.settings.plain
            and not self.settings.compact
            and self.settings.effect_level != "off"
        )

    def _status_rows(
        self, snapshot: IterationSnapshot
    ) -> list[tuple[str, object] | str]:
        rows: list[tuple[str, object] | str] = [
            ("Iteration", snapshot.iteration),
            ("Operation", snapshot.operation),
        ]
        if self.settings.show_provider and snapshot.provider_name:
            rows.append(("Provider", snapshot.provider_name))
        if self.settings.show_provider and snapshot.model_name:
            rows.append(("Model", snapshot.model_name))
        if snapshot.project_path:
            rows.append(("Project", self._truncate(snapshot.project_path, 80)))
        if self.settings.show_elapsed and snapshot.elapsed_seconds is not None:
            rows.append(("Elapsed", self._format_elapsed(snapshot.elapsed_seconds)))
        rows.append(("Dry run", "enabled" if snapshot.dry_run else "disabled"))
        return rows

    def _format_elapsed(self, elapsed_seconds: float) -> str:
        whole_seconds = max(0, int(elapsed_seconds))
        minutes, seconds = divmod(whole_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours}h {minutes}m {seconds}s"
        if minutes:
            return f"{minutes}m {seconds}s"
        return f"{seconds}s"

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

    def _label_for_title(self, title: str, severity: str) -> str | None:
        normalized = title.lower()
        label = None
        if "history" in normalized:
            label = SEMANTIC_LABELS["history"]
        elif "decision" in normalized or "manager" in normalized:
            label = SEMANTIC_LABELS["decision"]
        elif "prompt" in normalized:
            label = SEMANTIC_LABELS["prompt"]
        elif severity == "error":
            label = SEMANTIC_LABELS["error"]
        elif severity == "success":
            label = SEMANTIC_LABELS["complete"]
        elif severity == "warning":
            label = SEMANTIC_LABELS["stop"]
        return label

    def _codex_severity(self, state: str) -> str:
        if state in {"timeout", "missing", "error", "non-zero"}:
            return "error"
        if state == "complete":
            return "success"
        if state == "dry-run":
            return "dry-run"
        return "accent"

    def _style(self, severity: str) -> str:
        token = self.settings.tokens
        styles = {
            "accent": token.border,
            "success": token.success,
            "warning": token.warning,
            "error": token.error,
            "dry-run": token.dry_run,
        }
        return styles.get(severity, token.border)
