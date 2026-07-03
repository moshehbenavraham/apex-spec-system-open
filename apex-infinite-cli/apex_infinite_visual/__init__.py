"""Optional Apex Infinite CLI visual wrapper prototype."""

from apex_infinite_visual.events import (
    EventLineError,
    EventRecord,
    EventStateAdapter,
    WrapperSnapshot,
    parse_event_line,
)
from apex_infinite_visual.launcher import (
    ApexCliLaunchOptions,
    ApexCliProcess,
    build_apex_cli_command,
)

__all__ = [
    "ApexCliLaunchOptions",
    "ApexCliProcess",
    "EventLineError",
    "EventRecord",
    "EventStateAdapter",
    "WrapperSnapshot",
    "build_apex_cli_command",
    "parse_event_line",
]

__version__ = "0.1.0-spike"
