"""Validated settings for the optional visual wrapper."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Any

THEME_CRT_GREEN = "crt-green"
THEME_CRT_AMBER = "crt-amber"
THEME_IBM_DOS = "ibm-dos"
THEME_PLAIN = "plain"

WRAPPER_THEME_NAMES = (
    THEME_CRT_GREEN,
    THEME_CRT_AMBER,
    THEME_IBM_DOS,
    THEME_PLAIN,
)

FONT_FAMILIES = (
    "monospace",
    "DejaVu Sans Mono",
    "Liberation Mono",
    "Noto Sans Mono",
)

EFFECT_INTENSITY_MIN = 0
EFFECT_INTENSITY_MAX = 100
FONT_SCALE_MIN = 0.8
FONT_SCALE_MAX = 1.4
DEFAULT_EFFECT_INTENSITY = 45
DEFAULT_FONT_FAMILY = "monospace"
DEFAULT_FONT_SCALE = 1.0


class WrapperSettingsError(ValueError):
    """Raised when visual wrapper settings are invalid."""


@dataclass(frozen=True)
class ThemePreset:  # pylint: disable=too-many-instance-attributes
    """Clean-room visual preset consumed by Python and QML."""

    name: str
    label: str
    background: str
    panel: str
    panel_alt: str
    cell: str
    border: str
    accent: str
    text: str
    muted: str
    warning: str
    error: str
    default_intensity: int


THEME_PRESETS: dict[str, ThemePreset] = {
    THEME_CRT_GREEN: ThemePreset(
        name=THEME_CRT_GREEN,
        label="Green CRT",
        background="#07100d",
        panel="#0b1b17",
        panel_alt="#10231d",
        cell="#111c19",
        border="#263c34",
        accent="#6ee7a8",
        text="#d8ffe7",
        muted="#8dbca2",
        warning="#f2c166",
        error="#ff6f6f",
        default_intensity=45,
    ),
    THEME_CRT_AMBER: ThemePreset(
        name=THEME_CRT_AMBER,
        label="Amber CRT",
        background="#120e08",
        panel="#1b160d",
        panel_alt="#241b0f",
        cell="#1d180e",
        border="#4a3720",
        accent="#f0a53a",
        text="#ffe2a8",
        muted="#c59a63",
        warning="#f2c166",
        error="#ff746d",
        default_intensity=40,
    ),
    THEME_IBM_DOS: ThemePreset(
        name=THEME_IBM_DOS,
        label="IBM DOS",
        background="#050914",
        panel="#07152a",
        panel_alt="#0c1f3a",
        cell="#0a172b",
        border="#27496f",
        accent="#62a8ff",
        text="#d9ecff",
        muted="#89a7c5",
        warning="#f2c166",
        error="#ff6f6f",
        default_intensity=30,
    ),
    THEME_PLAIN: ThemePreset(
        name=THEME_PLAIN,
        label="Plain",
        background="#101419",
        panel="#182029",
        panel_alt="#1e2732",
        cell="#151b22",
        border="#303943",
        accent="#e6edf3",
        text="#e6edf3",
        muted="#8b949e",
        warning="#d8b45f",
        error="#ff6f6f",
        default_intensity=0,
    ),
}


@dataclass(frozen=True)
class WrapperSettings:
    """Validated visual settings for the wrapper surface."""

    theme_name: str = THEME_CRT_GREEN
    effect_intensity: int = DEFAULT_EFFECT_INTENSITY
    font_family: str = DEFAULT_FONT_FAMILY
    font_scale: float = DEFAULT_FONT_SCALE
    reduced_effects: bool = False
    plain_fallback: bool = False

    def __post_init__(self) -> None:
        _validate_theme_name(self.theme_name)
        _validate_intensity(self.effect_intensity)
        _validate_font_family(self.font_family)
        _validate_font_scale(self.font_scale)

    @property
    def effective_theme_name(self) -> str:
        """Return the preset after applying the plain fallback."""
        if self.plain_fallback or self.theme_name == THEME_PLAIN:
            return THEME_PLAIN
        return self.theme_name

    @property
    def preset(self) -> ThemePreset:
        """Return the effective visual preset."""
        return THEME_PRESETS[self.effective_theme_name]

    @property
    def effective_intensity(self) -> int:
        """Return the bounded effect intensity after fallbacks."""
        if self.reduced_effects or self.effective_theme_name == THEME_PLAIN:
            return 0
        return self.effect_intensity

    @property
    def effects_available(self) -> bool:
        """Return whether optional visual effects may run."""
        return self.effective_intensity > 0

    @property
    def effect_opacity(self) -> float:
        """Return a normalized opacity multiplier for QML effects."""
        return round(self.effective_intensity / EFFECT_INTENSITY_MAX, 2)

    def effect_enabled(self, name: str) -> bool:
        """Return the default enabled state for an optional effect."""
        if not self.effects_available:
            return False
        if name in {"glow", "scanlines", "curvature"}:
            return True
        if name == "flicker":
            return self.effective_intensity >= 65
        return False

    def updated(self, **changes: Any) -> "WrapperSettings":
        """Return a validated copy with selected fields changed."""
        return replace(self, **changes)

    def color_map(self) -> dict[str, str]:
        """Return QML-facing colors for the effective preset."""
        preset = self.preset
        return {
            "background": preset.background,
            "panel": preset.panel,
            "panel_alt": preset.panel_alt,
            "cell": preset.cell,
            "border": preset.border,
            "accent": preset.accent,
            "text": preset.text,
            "muted": preset.muted,
            "warning": preset.warning,
            "error": preset.error,
        }


def default_settings(theme_name: str = THEME_CRT_GREEN) -> WrapperSettings:
    """Build settings with the selected theme preset defaults."""
    _validate_theme_name(theme_name)
    preset = THEME_PRESETS[theme_name]
    return WrapperSettings(
        theme_name=theme_name,
        effect_intensity=preset.default_intensity,
        plain_fallback=theme_name == THEME_PLAIN,
    )


def build_settings(
    *,
    theme_name: str = THEME_CRT_GREEN,
    effect_intensity: int | None = None,
    font_family: str = DEFAULT_FONT_FAMILY,
    font_scale: float = DEFAULT_FONT_SCALE,
    reduced_effects: bool = False,
    plain_fallback: bool = False,
) -> WrapperSettings:
    """Build validated settings from CLI or bridge inputs."""
    _validate_theme_name(theme_name)
    preset = THEME_PRESETS[theme_name]
    return WrapperSettings(
        theme_name=theme_name,
        effect_intensity=(
            preset.default_intensity
            if effect_intensity is None
            else int(effect_intensity)
        ),
        font_family=font_family,
        font_scale=float(font_scale),
        reduced_effects=bool(reduced_effects),
        plain_fallback=bool(plain_fallback or theme_name == THEME_PLAIN),
    )


def _validate_theme_name(value: str) -> None:
    if value not in THEME_PRESETS:
        accepted = ", ".join(WRAPPER_THEME_NAMES)
        raise WrapperSettingsError(f"theme must be one of: {accepted}")


def _validate_intensity(value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise WrapperSettingsError("effect intensity must be an integer")
    if value < EFFECT_INTENSITY_MIN or value > EFFECT_INTENSITY_MAX:
        raise WrapperSettingsError("effect intensity must be between 0 and 100")


def _validate_font_family(value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise WrapperSettingsError("font family must be non-empty text")
    try:
        value.encode("ascii")
    except UnicodeEncodeError as exc:
        raise WrapperSettingsError("font family must be ASCII text") from exc


def _validate_font_scale(value: float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise WrapperSettingsError("font scale must be a number")
    if not math.isfinite(float(value)):
        raise WrapperSettingsError("font scale must be finite")
    if value < FONT_SCALE_MIN or value > FONT_SCALE_MAX:
        raise WrapperSettingsError("font scale must be between 0.8 and 1.4")
