"""Renderer and history safety tests."""

import re
from types import SimpleNamespace

import pytest
from rich.console import Console

import apex_infinite.cli as apex_infinite
from apex_infinite.ui import (
    ApexRenderer,
    CodexCommandSnapshot,
    DbLogSnapshot,
    StartupSnapshot,
    NoHumanOutputRenderer,
    UiCliOverrides,
    resolve_ui_settings,
)

ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")
FORBIDDEN_HISTORY_MARKERS = [
    "Agent Response",
    "Manager Decision",
    "Codex Execution",
    "History Write",
    "LOGGED",
    "BOOT",
    "ITERATION",
    "DRY RUN",
    "ACCENT",
    "SUCCESS",
    "[bold]",
    "[/bold]",
]
FRAME_GLYPHS = [
    chr(0x2500),
    chr(0x2502),
    chr(0x256D),
    chr(0x256E),
    chr(0x2570),
    chr(0x2572),
]


def make_renderer(width=100, plain=False, ascii_only=False, compact=False):
    """Create an ApexRenderer backed by a recorded Rich console."""
    settings = resolve_ui_settings(
        {"ui": {"theme": "crt-green"}},
        UiCliOverrides(plain=plain, ascii_only=ascii_only, compact=compact),
        env={},
        console=SimpleNamespace(is_terminal=True),
    )
    output_console = Console(
        record=True,
        width=width,
        force_terminal=True,
        color_system=None,
        no_color=not settings.color_enabled,
    )
    return ApexRenderer(settings, output_console), output_console


@pytest.mark.parametrize("width", [80, 100, 120])
def test_renderer_outputs_semantic_sections_at_supported_widths(width):
    renderer, output_console = make_renderer(width=width)

    renderer.print_startup(
        StartupSnapshot(
            project_path="/tmp/project/",
            provider_name="ollama",
            model_name="qwen2.5:7b",
            config_path="config.yaml",
            max_iterations=5,
            theme_name="crt-green",
            requested_theme="auto",
            dry_run=True,
            start_command="implement",
            ceo_present=True,
        )
    )
    renderer.print_iteration(2, "history summary")
    renderer.print_manager_decision("implement", "ready for implementation", True)
    renderer.print_prompt_preview("Run the apex-spec skill command /implement " * 8)
    renderer.print_codex_command(
        "dry-run",
        CodexCommandSnapshot(
            binary="codex",
            exec_flags="--dangerously-auto-approve",
            prompt="Run the apex-spec skill command /implement",
            project_path="/tmp/project/",
            timeout=1800,
        ),
    )
    renderer.print_agent_response("agent output " * 40)

    text = output_console.export_text()

    for expected in [
        "BOOT Apex Infinite Operator Console",
        "ITERATION Iteration Frame",
        "DECISION Manager Decision",
        "PROMPT Prompt Preview",
        "DRY RUN Codex Execution",
        "RESPONSE Agent Response",
    ]:
        assert expected in text
    assert "ready for implementation" in text
    assert "Run the apex-spec skill command" in text


@pytest.mark.parametrize("width", [80, 100, 120])
def test_history_renderer_outputs_semantic_rows_at_supported_widths(width):
    renderer, output_console = make_renderer(width=width)
    row = {
        "id": 1,
        "created_at": "2026-07-03 00:00:00",
        "path": "/p/",
        "ai_decision_output": "go",
        "ai_decision_reason": "continue",
        "cc_response": "done",
        "help_or_done_msg": "",
    }

    renderer.print_history([row], verbose=width == 120)
    text = output_console.export_text()

    assert "Apex Infinite - History" in text
    assert "go" in text
    assert "/p/" in text
    assert "continue" in text


def test_plain_ascii_compact_renderer_uses_ascii_and_keeps_critical_states():
    renderer, output_console = make_renderer(plain=True, ascii_only=True, compact=True)

    renderer.print_interrupt("pause", "CEO interrupt - input requested.")
    renderer.print_help("external credential missing")
    renderer.print_completion("done", 3)
    renderer.print_max_iterations(5)

    text = output_console.export_text()

    assert "INTERRUPT Operator Interrupt" in text
    assert "HELP Manager Needs Help" in text
    assert "COMPLETE Project Complete" in text
    assert "STOP Safety Stop" in text
    assert all(ord(character) < 128 for character in text)


def test_ascii_only_renderer_keeps_styled_layout_with_ascii_glyphs():
    renderer, output_console = make_renderer(ascii_only=True)

    assert renderer.settings.plain is False
    assert renderer.settings.color_enabled is True

    renderer.print_startup(
        StartupSnapshot(
            project_path="/tmp/project/",
            provider_name="ollama",
            model_name="qwen2.5:7b",
            config_path="config.yaml",
            max_iterations=5,
            theme_name="crt-green",
            requested_theme="auto",
            dry_run=False,
        )
    )
    renderer.print_history(
        [
            {
                "id": 1,
                "created_at": "2026-07-03 00:00:00",
                "path": "/p/",
                "ai_decision_output": "go",
                "ai_decision_reason": "continue",
                "cc_response": "done",
                "help_or_done_msg": "",
            }
        ]
    )

    text = output_console.export_text()

    assert "BOOT Apex Infinite Operator Console" in text
    assert "Apex Infinite - History" in text
    assert "ACCENT Apex Infinite CLI" not in text
    assert all(ord(character) < 128 for character in text)


def test_no_human_output_renderer_suppresses_all_output(capsys):
    renderer = NoHumanOutputRenderer()

    renderer.print_startup(
        StartupSnapshot(
            project_path="/tmp/project/",
            provider_name="ollama",
            model_name="qwen2.5:7b",
            config_path="config.yaml",
            max_iterations=5,
            theme_name="plain",
            requested_theme="plain",
            dry_run=True,
        )
    )
    renderer.print_iteration(1, "history summary")
    renderer.print_manager_decision("implement", "reason", True)
    renderer.print_prompt_preview("prompt")
    renderer.print_codex_command(
        "dry-run",
        CodexCommandSnapshot(
            binary="codex",
            exec_flags="--dangerously-auto-approve",
            prompt="prompt",
            project_path="/tmp/project/",
            timeout=1800,
        ),
    )
    renderer.print_agent_response("agent output")
    renderer.print_db_log(
        DbLogSnapshot(
            project_path="/tmp/project/",
            manager_output="implement",
            stored_state="iteration result",
        )
    )
    renderer.print_help("reason")
    renderer.print_completion("done", 1)
    renderer.print_max_iterations(1)

    assert renderer.input_prompt("CEO") == ""
    assert capsys.readouterr().out == ""


def test_sqlite_history_stores_raw_values_without_renderer_labels(
    monkeypatch, tmp_path
):
    monkeypatch.setattr(apex_infinite, "DB_DIR", tmp_path / "db")
    monkeypatch.setattr(apex_infinite, "DB_PATH", tmp_path / "db" / "history.db")
    apex_infinite.db_init()

    renderer, output_console = make_renderer(width=100)
    renderer.print_manager_decision("implement", "use current session", True)
    renderer.print_agent_response("rendered agent output")
    renderer.print_db_log(
        DbLogSnapshot(
            project_path="/tmp/project/",
            manager_output="implement",
            stored_state="iteration result",
            created_at="2026-07-03 01:00:00",
        )
    )
    rendered_text = output_console.export_text()
    assert "Manager Decision" in rendered_text
    assert "Agent Response" in rendered_text
    assert "LOGGED History Write" in rendered_text

    project_path = f"{tmp_path}/project/"
    apex_infinite.db_log(
        project_path,
        "raw agent output",
        "implement",
        "plain manager reason",
        "done",
    )
    rows = apex_infinite.db_fetch_history(project_path, limit=5)

    assert len(rows) == 1
    stored_values = [
        rows[0]["cc_response"],
        rows[0]["ai_decision_output"],
        rows[0]["ai_decision_reason"],
        rows[0]["help_or_done_msg"],
    ]
    assert stored_values == [
        "raw agent output",
        "implement",
        "plain manager reason",
        "done",
    ]
    for value in stored_values:
        assert not ANSI_PATTERN.search(value)
        assert all(marker not in value for marker in FORBIDDEN_HISTORY_MARKERS)
        assert all(glyph not in value for glyph in FRAME_GLYPHS)
        assert all(ord(character) < 128 for character in value)
