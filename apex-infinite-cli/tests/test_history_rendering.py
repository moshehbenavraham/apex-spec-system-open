"""History ledger rendering tests."""

from types import SimpleNamespace

import pytest
from rich.console import Console

import apex_infinite.cli as apex_infinite
from apex_infinite.ui import ApexRenderer, UiCliOverrides, resolve_ui_settings

SUPPORTED_WIDTHS = (80, 100, 120)


def make_history_renderer(
    width=100,
    plain=False,
    ascii_only=False,
    compact=False,
    is_terminal=True,
    env=None,
):
    """Create an ApexRenderer backed by a recorded console."""
    settings = resolve_ui_settings(
        {"ui": {"theme": "crt-green"}},
        UiCliOverrides(plain=plain, ascii_only=ascii_only, compact=compact),
        env={} if env is None else env,
        console=SimpleNamespace(is_terminal=is_terminal),
    )
    output_console = Console(
        record=True,
        width=width,
        force_terminal=is_terminal,
        color_system=None,
        no_color=not settings.color_enabled,
    )
    return ApexRenderer(settings, output_console), output_console


def sample_history_row(**overrides):
    """Build a representative SQLite history row."""
    row = {
        "id": 7,
        "path": "/tmp/apex/project/",
        "cc_response": "Codex completed the current implementation task.",
        "ai_decision_output": "implement",
        "ai_decision_reason": "Continue the active implementation session.",
        "help_or_done_msg": "",
        "created_at": "2026-07-03 01:30:00",
    }
    row.update(overrides)
    return row


def compact_text(text):
    """Normalize Rich wrapping for semantic assertions."""
    return "".join(text.split())


def test_history_renderer_handles_empty_rows():
    renderer, output_console = make_history_renderer(width=80)

    renderer.print_history([])

    text = output_console.export_text()
    assert "HISTORY History" in text
    assert "No history records found." in text


@pytest.mark.parametrize("width", SUPPORTED_WIDTHS)
def test_history_renderer_handles_short_long_and_sparse_rows(width):
    renderer, output_console = make_history_renderer(width=width)
    long_text = " ".join(["long-response"] * 30)
    rows = [
        sample_history_row(),
        sample_history_row(
            id=8,
            path="/tmp/apex/project-with-a-very-long-directory-name/",
            cc_response=long_text,
            ai_decision_reason=" ".join(["long-reason"] * 20),
        ),
        sample_history_row(
            id=9,
            path="",
            cc_response=None,
            ai_decision_output="help",
            ai_decision_reason="",
            help_or_done_msg="operator pause",
        ),
    ]

    renderer.print_history(rows, verbose=width == 120)

    text = output_console.export_text()
    compact = compact_text(text)
    assert "Apex Infinite - History" in text
    assert "implement" in compact
    assert "help" in compact
    assert "operatorpause" in compact
    assert "long-response" in compact


def test_styled_history_uses_compact_ledger_fields_at_80_columns():
    renderer, output_console = make_history_renderer(width=80)

    renderer.print_history([sample_history_row()])

    text = output_console.export_text()
    compact = compact_text(text)
    assert "Apex Infinite - History" in text
    assert "2026-07-0301:30:00" in compact
    assert "status=iteration" in compact
    assert "project=project" in compact
    assert "command=implement" in compact
    assert "Path:" in text
    assert "Reason:" in text
    assert "Response:" in text


def test_plain_ascii_compact_history_is_line_oriented_and_ascii():
    renderer, output_console = make_history_renderer(
        width=80,
        plain=True,
        ascii_only=True,
        compact=True,
    )

    renderer.print_history([sample_history_row()], verbose=True)

    text = output_console.export_text()
    assert "HISTORY History" in text
    assert "Rows: 1" in text
    assert "command=implement" in text
    assert "Reason:" in text
    assert "Response:" in text
    assert all(ord(character) < 128 for character in text)


@pytest.mark.parametrize(
    ("name", "renderer_kwargs", "requires_ascii"),
    [
        ("plain", {"plain": True}, True),
        ("ascii", {"ascii_only": True}, True),
        ("compact", {"compact": True}, False),
        ("non-terminal", {"is_terminal": False}, True),
    ],
)
def test_history_fallback_modes_keep_labels_and_truncation_counts(
    name,
    renderer_kwargs,
    requires_ascii,
):
    renderer, output_console = make_history_renderer(width=80, **renderer_kwargs)
    row = sample_history_row(
        cc_response=" ".join(["response-detail"] * 30),
        help_or_done_msg="operator pause",
    )

    renderer.print_history([row], verbose=name == "plain")

    text = output_console.export_text()
    assert "History" in text
    assert "Rows: 1" in text
    assert "status=operator pause" in text
    assert "command=implement" in text
    assert "Path:" in text
    assert "Reason:" in text
    assert "Response:" in text
    assert "chars total" in text
    if name == "plain":
        assert "Stored state: operator pause" in text
    if renderer.settings.plain:
        assert renderer.settings.theme_name == "plain"
    if requires_ascii:
        assert all(ord(character) < 128 for character in text)


def test_history_verbose_expands_detail_without_mutating_rows():
    renderer, output_console = make_history_renderer(width=120)
    row = sample_history_row(
        ai_decision_reason=" ".join(["verbose-reason"] * 8),
        cc_response=" ".join(["verbose-response"] * 12),
    )
    before = dict(row)

    renderer.print_history([row], verbose=True)

    text = output_console.export_text()
    compact = compact_text(text)
    assert "verbose" in compact
    assert "reason" in compact
    assert "response" in compact
    assert row == before


def test_history_display_does_not_persist_ledger_derivations(monkeypatch, tmp_path):
    monkeypatch.setattr(apex_infinite, "DB_DIR", tmp_path / "db")
    monkeypatch.setattr(apex_infinite, "DB_PATH", tmp_path / "db" / "history.db")
    apex_infinite.db_init()
    project_path = f"{tmp_path}/project/"
    raw_response = " ".join(["raw-response"] * 40)
    raw_reason = " ".join(["raw-reason"] * 20)

    apex_infinite.db_log(
        project_path,
        raw_response,
        "implement",
        raw_reason,
        help_or_done_msg="",
    )
    renderer, output_console = make_history_renderer(width=80)

    apex_infinite.db_show_history(project_path, renderer=renderer, verbose=False)

    rendered = output_console.export_text()
    rows = apex_infinite.db_fetch_history(project_path, limit=5)
    assert len(rows) == 1
    assert rows[0]["cc_response"] == raw_response
    assert rows[0]["ai_decision_reason"] == raw_reason
    assert rows[0]["ai_decision_output"] == "implement"
    assert rows[0]["help_or_done_msg"] == ""
    assert "chars total" in rendered
    for value in [
        rows[0]["cc_response"],
        rows[0]["ai_decision_reason"],
        rows[0]["ai_decision_output"],
    ]:
        assert "chars total" not in value
        assert "status=" not in value
        assert "command=" not in value
        assert "\x1b[" not in value
