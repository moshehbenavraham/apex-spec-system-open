"""Operator-console renderer fixtures and coverage."""

from types import SimpleNamespace

import pytest
from rich.console import Console

from apex_infinite.ui import (
    ApexRenderer,
    CodexCommandSnapshot,
    DbLogSnapshot,
    IterationSnapshot,
    StartupSnapshot,
    UiCliOverrides,
    resolve_ui_settings,
)

SUPPORTED_WIDTHS = (80, 100, 120)

FALLBACK_CASES = (
    ("styled", UiCliOverrides(), {}, True),
    ("plain", UiCliOverrides(plain=True), {}, True),
    ("ascii", UiCliOverrides(ascii_only=True), {}, True),
    ("compact", UiCliOverrides(compact=True), {}, True),
    ("no-color", UiCliOverrides(), {"NO_COLOR": "1"}, True),
    ("term-dumb", UiCliOverrides(), {"TERM": "dumb"}, True),
    ("non-terminal", UiCliOverrides(), {}, False),
)


def make_operator_renderer(
    width=100,
    overrides=None,
    env=None,
    is_terminal=True,
    ui_config=None,
):
    """Create a recorded renderer for operator-console tests."""
    settings = resolve_ui_settings(
        {"ui": ui_config or {"theme": "crt-green"}},
        overrides or UiCliOverrides(),
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


@pytest.fixture(params=SUPPORTED_WIDTHS)
def supported_width(request):
    """Parametrize tests across supported terminal widths."""
    return request.param


@pytest.fixture(params=FALLBACK_CASES, ids=[case[0] for case in FALLBACK_CASES])
def fallback_case(request):
    """Parametrize tests across display fallback modes."""
    return request.param


def test_operator_console_fixture_can_record_output(supported_width):
    renderer, output_console = make_operator_renderer(width=supported_width)

    renderer.print_status("fixture ready", "Fixture")

    assert "fixture ready" in output_console.export_text()


def test_operator_console_sections_and_critical_states_at_supported_widths(
    supported_width,
):
    renderer, output_console = make_operator_renderer(width=supported_width)

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
    renderer.print_iteration(
        IterationSnapshot(
            project_path="/tmp/project/",
            provider_name="ollama",
            model_name="qwen2.5:7b",
            iteration=3,
            operation="codex execution",
            dry_run=True,
            elapsed_seconds=125,
        )
    )
    renderer.print_manager_decision("implement", "continue session work", True)
    renderer.print_prompt_preview("Run the apex-spec skill command /implement " * 8)
    renderer.print_db_log(
        DbLogSnapshot(
            project_path="/tmp/project/",
            manager_output="implement",
            stored_state="iteration result",
            created_at="2026-07-03 01:00:00",
        )
    )
    renderer.print_llm_retry(1, 3, "temporary provider error", wait_seconds=5)
    renderer.print_json_fallback()
    renderer.print_help("credential required")
    renderer.print_interrupt("pause", "CEO interrupt - input requested.")
    renderer.print_completion("done", 3)
    renderer.print_max_iterations(5)
    for state in ["dry-run", "start", "non-zero", "timeout", "missing", "error"]:
        renderer.print_codex_command(
            state,
            CodexCommandSnapshot(
                binary="codex",
                exec_flags="--dangerously-auto-approve",
                prompt="Run the apex-spec skill command /implement",
                project_path="/tmp/project/",
                timeout=1800,
                return_code=2 if state == "non-zero" else None,
            ),
        )

    text = output_console.export_text()

    for expected in [
        "BOOT Apex Infinite Operator Console",
        "ITERATION Iteration Frame",
        "Provider",
        "qwen2.5:7b",
        "Elapsed",
        "Dry run",
        "DECISION Manager Decision",
        "PROMPT Prompt Preview",
        "LOGGED History Write",
        "ERROR LLM Retry",
        "DECISION Manager Parse Fallback",
        "HELP Manager Needs Help",
        "INTERRUPT Operator Interrupt",
        "COMPLETE Project Complete",
        "STOP Safety Stop",
        "DRY RUN Codex Execution",
        "EXECUTING Codex Execution",
        "TIMEOUT Codex Execution",
        "ERROR Codex Execution",
    ]:
        assert expected in text


def test_operator_console_fallback_modes_keep_labels_and_separator_rules(
    fallback_case,
):
    _name, overrides, env, is_terminal = fallback_case
    renderer, output_console = make_operator_renderer(
        overrides=overrides,
        env=env,
        is_terminal=is_terminal,
    )

    renderer.print_iteration(
        IterationSnapshot(
            project_path="/tmp/project/",
            provider_name="ollama",
            model_name="qwen2.5:7b",
            iteration=1,
            operation="history summary",
            dry_run=False,
            elapsed_seconds=0,
        )
    )
    renderer.print_codex_command(
        "timeout",
        CodexCommandSnapshot(
            binary="codex",
            exec_flags="--dangerously-auto-approve",
            prompt="Run the apex-spec skill command /implement",
            project_path="/tmp/project/",
            timeout=1800,
        ),
    )
    text = output_console.export_text()

    assert "ITERATION" in text
    assert "TIMEOUT" in text
    if renderer.settings.plain or renderer.settings.compact:
        assert not any(
            set(line) == {"-"} and len(line) >= 24 for line in text.splitlines()
        )
    if renderer.settings.plain or renderer.settings.ascii_only:
        assert all(ord(character) < 128 for character in text)
    if env.get("NO_COLOR") or env.get("TERM") == "dumb" or not is_terminal:
        assert renderer.settings.plain is True
