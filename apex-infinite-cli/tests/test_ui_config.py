"""Tests for UI configuration resolution."""

from types import SimpleNamespace

import pytest
from rich.console import Console

from apex_infinite.ui import (
    UiCliOverrides,
    UiConfigError,
    build_theme_registry,
    resolve_ui_settings,
)


def make_config(ui_config=None):
    """Return a minimal config mapping for UI resolution tests."""
    config = {}
    if ui_config is not None:
        config["ui"] = ui_config
    return config


def terminal(is_terminal=True):
    """Return an object with the Console terminal capability contract."""
    return SimpleNamespace(is_terminal=is_terminal)


def test_defaults_resolve_auto_to_crt_green_on_terminal():
    settings = resolve_ui_settings(make_config(), env={}, console=terminal(True))

    assert settings.requested_theme == "auto"
    assert settings.theme_name == "crt-green"
    assert settings.effect_level == "low"
    assert settings.color_enabled is True
    assert settings.plain is False
    assert settings.ascii_only is False
    assert settings.compact is False
    assert settings.tokens.name == "crt-green"


def test_config_values_are_validated_and_applied():
    settings = resolve_ui_settings(
        make_config(
            {
                "theme": "ibm-dos",
                "effect_level": "medium",
                "ascii": True,
                "compact": True,
                "show_elapsed": False,
                "show_provider": False,
                "themes": {},
            }
        ),
        env={},
        console=terminal(True),
    )

    assert settings.theme_name == "ibm-dos"
    assert settings.effect_level == "medium"
    assert settings.ascii_only is True
    assert settings.compact is True
    assert settings.show_elapsed is False
    assert settings.show_provider is False
    assert settings.glyphs.name == "ascii"


def test_cli_overrides_win_over_config_values():
    settings = resolve_ui_settings(
        make_config({"theme": "crt-green", "ascii": False, "compact": False}),
        UiCliOverrides(theme="crt-amber", ascii_only=True, compact=True),
        env={},
        console=terminal(True),
    )

    assert settings.requested_theme == "crt-amber"
    assert settings.theme_name == "crt-amber"
    assert settings.ascii_only is True
    assert settings.compact is True
    assert settings.color_enabled is True
    assert settings.plain is False
    assert settings.glyphs.name == "ascii"


def test_plain_override_forces_plain_output_and_disables_effects():
    settings = resolve_ui_settings(
        make_config({"theme": "crt-green", "effect_level": "medium"}),
        UiCliOverrides(theme="crt-amber", plain=True),
        env={},
        console=terminal(True),
    )

    assert settings.requested_theme == "crt-amber"
    assert settings.theme_name == "plain"
    assert settings.effect_level == "off"
    assert settings.color_enabled is False
    assert settings.plain is True
    assert settings.glyphs.name == "ascii"


def test_no_color_constrains_auto_to_plain_output():
    settings = resolve_ui_settings(
        make_config({"theme": "auto"}),
        env={"NO_COLOR": "1"},
        console=terminal(True),
    )

    assert settings.theme_name == "plain"
    assert settings.effect_level == "off"
    assert settings.color_enabled is False
    assert settings.constraint_reason == "NO_COLOR"


def test_explicit_theme_can_override_no_color_constraint():
    settings = resolve_ui_settings(
        make_config({"theme": "auto"}),
        UiCliOverrides(theme="crt-amber"),
        env={"NO_COLOR": "1"},
        console=terminal(True),
    )

    assert settings.requested_theme == "crt-amber"
    assert settings.theme_name == "crt-amber"
    assert settings.color_enabled is True
    assert settings.constraint_reason is None


def test_term_dumb_constrains_config_theme_without_explicit_theme():
    settings = resolve_ui_settings(
        make_config({"theme": "crt-amber"}),
        env={"TERM": "dumb"},
        console=terminal(True),
    )

    assert settings.theme_name == "plain"
    assert settings.constraint_reason == "TERM=dumb"


def test_non_terminal_console_constrains_auto_to_plain_output():
    settings = resolve_ui_settings(
        make_config({"theme": "auto"}),
        env={},
        console=Console(record=True),
    )

    assert settings.theme_name == "plain"
    assert settings.constraint_reason == "non-terminal output"


def test_custom_theme_registry_and_resolution():
    config = make_config(
        {
            "theme": "night-shift",
            "themes": {
                "night-shift": {
                    "base": "crt-amber",
                    "foreground": "bright_white",
                    "accent": "cyan",
                }
            },
        }
    )

    registry = build_theme_registry(config["ui"]["themes"])
    settings = resolve_ui_settings(config, env={}, console=terminal(True))

    assert registry["night-shift"].name == "night-shift"
    assert registry["night-shift"].foreground == "bright_white"
    assert registry["night-shift"].accent == "cyan"
    assert registry["night-shift"].warning == "bright_yellow"
    assert settings.theme_name == "night-shift"
    assert settings.tokens.accent == "cyan"


def test_builtin_theme_tokens_include_operator_console_states():
    registry = build_theme_registry({})

    for theme_name in ("crt-green", "crt-amber", "ibm-dos", "plain"):
        tokens = registry[theme_name]
        assert tokens.info
        assert tokens.dry_run
        assert tokens.complete
        assert tokens.separator


@pytest.mark.parametrize(
    ("ui_config", "message"),
    [
        ({"theme": "missing"}, "ui.theme"),
        ({"effect_level": "high"}, "ui.effect_level"),
        ({"ascii": "yes"}, "ui.ascii"),
        ({"unknown": True}, "unknown keys"),
        ({"themes": {"BadName": {"accent": "red"}}}, "theme name"),
        ({"themes": {"custom": {"base": "missing", "accent": "red"}}}, "base"),
        ({"themes": {"custom": {"base": "crt-green"}}}, "token override"),
    ],
)
def test_invalid_ui_config_fails_fast(ui_config, message):
    with pytest.raises(UiConfigError, match=message):
        resolve_ui_settings(make_config(ui_config), env={}, console=terminal(True))


def test_empty_explicit_theme_fails_fast():
    with pytest.raises(UiConfigError, match="--theme"):
        resolve_ui_settings(
            make_config({"theme": "crt-green"}),
            UiCliOverrides(theme=""),
            env={},
            console=terminal(True),
        )
