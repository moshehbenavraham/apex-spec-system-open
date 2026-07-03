"""Optional Apex Infinite CLI visual wrapper productization surface."""

from apex_infinite_visual.events import (
    EventLineError,
    EventRecord,
    EventStateAdapter,
    WrapperSnapshot,
    parse_event_line,
)
from apex_infinite_visual.launcher import (
    ApexCliLaunchError,
    ApexCliLaunchOptions,
    ApexCliProcess,
    ApexCliTimeoutError,
    build_apex_cli_command,
)
from apex_infinite_visual.settings import (
    THEME_PRESETS,
    WRAPPER_THEME_NAMES,
    ThemePreset,
    WrapperSettings,
    WrapperSettingsError,
    build_settings,
    default_settings,
)

__all__ = [
    "ApexCliLaunchError",
    "ApexCliLaunchOptions",
    "ApexCliProcess",
    "ApexCliTimeoutError",
    "EventLineError",
    "EventRecord",
    "EventStateAdapter",
    "THEME_PRESETS",
    "ThemePreset",
    "WrapperSnapshot",
    "WrapperSettings",
    "WrapperSettingsError",
    "WRAPPER_THEME_NAMES",
    "build_apex_cli_command",
    "build_settings",
    "default_settings",
    "parse_event_line",
]

__version__ = "0.2.0-productized"
