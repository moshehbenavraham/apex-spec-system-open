"""Dry-run tests for prompt content and generation.

Verifies that system prompts reference Codex CLI (not Claude Code),
and that build_codex_prompt() produces correct output for all known commands.
"""
import re
from unittest.mock import MagicMock, patch

import pytest

from apex_infinite import (
    KNOWN_COMMANDS,
    MANAGER_SYSTEM_PROMPT,
    SUMMARIZER_SYSTEM_PROMPT,
    build_codex_prompt,
    llm_manager_decide,
)

# -------------------------------------------------------------------
# Forbidden / required strings
# -------------------------------------------------------------------

FORBIDDEN_STRINGS = [
    "Claude Code",
    "claude code",
    "CLAUDE CODE",
]

# "CC" as a standalone abbreviation for Claude Code (not inside other words)
CC_PATTERN = re.compile(r"\bCC\b")


class TestManagerSystemPrompt:
    """T015: MANAGER_SYSTEM_PROMPT content assertions."""

    def test_contains_codex_cli(self):
        assert "Codex CLI" in MANAGER_SYSTEM_PROMPT

    def test_no_claude_code_references(self):
        for forbidden in FORBIDDEN_STRINGS:
            assert forbidden not in MANAGER_SYSTEM_PROMPT, (
                f"Found forbidden string '{forbidden}' in MANAGER_SYSTEM_PROMPT"
            )

    def test_no_cc_abbreviation(self):
        matches = CC_PATTERN.findall(MANAGER_SYSTEM_PROMPT)
        assert len(matches) == 0, (
            f"Found {len(matches)} standalone 'CC' abbreviation(s) in MANAGER_SYSTEM_PROMPT"
        )

    def test_role_section_references_codex(self):
        assert "'Codex CLI'" in MANAGER_SYSTEM_PROMPT

    def test_senior_developer_heading(self):
        assert "# Your Senior Developer Codex CLI" in MANAGER_SYSTEM_PROMPT

    def test_codex_cli_commands_heading(self):
        assert "## Codex CLI Commands" in MANAGER_SYSTEM_PROMPT

    def test_command_reference_heading(self):
        assert "Codex CLI Senior Developer - Command Reference" in MANAGER_SYSTEM_PROMPT

    def test_no_slash_commands_in_prose(self):
        """Slash-command syntax should not appear in prompt prose (outside code blocks)."""
        # Extract text outside of code blocks
        parts = re.split(r"```.*?```", MANAGER_SYSTEM_PROMPT, flags=re.DOTALL)
        prose = " ".join(parts)
        # Check for /commandname patterns that reference workflow commands
        slash_cmds = re.findall(r"/(?:plansession|implement|validate|updateprd|audit|pipeline|infra|carryforward|documents|phasebuild)\b", prose)
        assert len(slash_cmds) == 0, (
            f"Found slash-command references in prose: {slash_cmds}"
        )

    def test_output_section_references_codex(self):
        assert "Codex CLI" in MANAGER_SYSTEM_PROMPT
        # The output JSON example should reference Codex CLI not Claude Code
        assert "Codex CLI our Senior Developer" in MANAGER_SYSTEM_PROMPT

    def test_issues_section_references_codex(self):
        assert "If Codex CLI reports any issues" in MANAGER_SYSTEM_PROMPT
        assert "Codex CLI has shell access" in MANAGER_SYSTEM_PROMPT

    def test_ceo_section_references_codex(self):
        assert "relay the instructions to Codex CLI" in MANAGER_SYSTEM_PROMPT
        assert "Codex CLI TRULY cannot do" in MANAGER_SYSTEM_PROMPT

    def test_prompt_is_well_structured(self):
        """Verify key structural sections exist."""
        assert "# Role" in MANAGER_SYSTEM_PROMPT
        assert "# Input" in MANAGER_SYSTEM_PROMPT
        assert "# Output" in MANAGER_SYSTEM_PROMPT
        assert "# Senior Developer's Commands" in MANAGER_SYSTEM_PROMPT
        assert "Quick Reference" in MANAGER_SYSTEM_PROMPT


class TestSummarizerSystemPrompt:
    """T015: SUMMARIZER_SYSTEM_PROMPT content assertions."""

    def test_no_claude_code_references(self):
        for forbidden in FORBIDDEN_STRINGS:
            assert forbidden not in SUMMARIZER_SYSTEM_PROMPT, (
                f"Found forbidden string '{forbidden}' in SUMMARIZER_SYSTEM_PROMPT"
            )

    def test_no_cc_abbreviation(self):
        matches = CC_PATTERN.findall(SUMMARIZER_SYSTEM_PROMPT)
        assert len(matches) == 0, (
            f"Found standalone 'CC' abbreviation(s) in SUMMARIZER_SYSTEM_PROMPT"
        )

    def test_codex_aware_language(self):
        assert "Codex CLI" in SUMMARIZER_SYSTEM_PROMPT

    def test_role_description_updated(self):
        assert "AI coding agent" in SUMMARIZER_SYSTEM_PROMPT

    def test_prompt_structure(self):
        assert "# Role" in SUMMARIZER_SYSTEM_PROMPT
        assert "# Input" in SUMMARIZER_SYSTEM_PROMPT
        assert "# Output" in SUMMARIZER_SYSTEM_PROMPT


class TestUserMessageTemplate:
    """T015: llm_manager_decide() user-message template assertions."""

    def test_user_message_references_codex(self):
        """Verify the user message template uses CODEX CLI, not CLAUDE CODE."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"output": "implement", "reason": "test"}'
        mock_client.chat.completions.create.return_value = mock_response

        llm_manager_decide(mock_client, "test-model", "agent response", "ceo msg", "summary")

        # Inspect the messages passed to the LLM call
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs.get("messages") or call_args[1].get("messages")
        user_msg = messages[1]["content"]

        assert "CODEX CLI SENIOR DEVELOPER" in user_msg
        assert "CLAUDE CODE" not in user_msg

    def test_user_message_contains_agent_response(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"output": "validate", "reason": "next"}'
        mock_client.chat.completions.create.return_value = mock_response

        llm_manager_decide(mock_client, "test-model", "test agent output", "", "")

        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs.get("messages") or call_args[1].get("messages")
        user_msg = messages[1]["content"]
        assert "test agent output" in user_msg

    def test_user_message_contains_ceo_instructions(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"output": "audit", "reason": "ceo said"}'
        mock_client.chat.completions.create.return_value = mock_response

        llm_manager_decide(mock_client, "test-model", "", "run audit now", "")

        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs.get("messages") or call_args[1].get("messages")
        user_msg = messages[1]["content"]
        assert "run audit now" in user_msg

    def test_system_message_is_manager_prompt(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"output": "implement", "reason": "test"}'
        mock_client.chat.completions.create.return_value = mock_response

        llm_manager_decide(mock_client, "test-model", "", "", "")

        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs.get("messages") or call_args[1].get("messages")
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == MANAGER_SYSTEM_PROMPT


class TestBuildCodexPrompt:
    """T016: build_codex_prompt() output for each known command."""

    # The 10 workflow commands from the command reference table
    WORKFLOW_COMMANDS = [
        "plansession",
        "implement",
        "validate",
        "updateprd",
        "audit",
        "pipeline",
        "infra",
        "carryforward",
        "documents",
        "phasebuild",
    ]

    # Additional known commands not in the workflow table
    EXTRA_COMMANDS = [
        "initspec",
        "createprd",
        "createuxprd",
    ]

    @pytest.mark.parametrize("cmd", WORKFLOW_COMMANDS)
    def test_workflow_command_produces_skill_invocation(self, cmd):
        result = build_codex_prompt(cmd, cmd)
        assert "apex-spec" in result
        assert cmd in result

    @pytest.mark.parametrize("cmd", EXTRA_COMMANDS)
    def test_extra_command_produces_skill_invocation(self, cmd):
        result = build_codex_prompt(cmd, cmd)
        assert "apex-spec" in result
        assert cmd in result

    @pytest.mark.parametrize("cmd", WORKFLOW_COMMANDS + EXTRA_COMMANDS)
    def test_command_output_format(self, cmd):
        result = build_codex_prompt(cmd, cmd)
        expected = f"Run the apex-spec skill command /{cmd}"
        assert result == expected

    def test_unknown_command_returns_raw_output(self):
        result = build_codex_prompt("unknown_cmd", "do something custom")
        assert result == "do something custom"

    def test_command_with_leading_slash(self):
        result = build_codex_prompt("/implement", "/implement")
        assert "apex-spec" in result
        assert "implement" in result

    def test_command_case_insensitive(self):
        result = build_codex_prompt("IMPLEMENT", "IMPLEMENT")
        assert "apex-spec" in result
        assert "implement" in result

    def test_command_with_whitespace(self):
        result = build_codex_prompt("  plansession  ", "plansession")
        assert "apex-spec" in result
        assert "plansession" in result

    def test_all_known_commands_covered(self):
        """Verify our test lists cover all KNOWN_COMMANDS."""
        tested = set(self.WORKFLOW_COMMANDS + self.EXTRA_COMMANDS)
        assert tested == KNOWN_COMMANDS


class TestJsonParsing:
    """Verify JSON output parsing still works with updated prompts."""

    def test_json_mode_response(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"output": "implement", "reason": "ready"}'
        mock_client.chat.completions.create.return_value = mock_response

        result = llm_manager_decide(mock_client, "test-model", "done", "", "summary")
        assert result["output"] == "implement"
        assert result["reason"] == "ready"

    def test_regex_fallback_parsing(self):
        """When json_mode fails, regex extraction should work."""
        mock_client = MagicMock()
        call_count = 0

        def side_effect(**kwargs):
            nonlocal call_count
            call_count += 1
            if kwargs.get("response_format"):
                raise ValueError("json_mode not supported")
            mock_resp = MagicMock()
            mock_resp.choices = [MagicMock()]
            mock_resp.choices[0].message.content = (
                'Here is my decision: {"output": "validate", "reason": "tests passed"}'
            )
            return mock_resp

        mock_client.chat.completions.create.side_effect = side_effect

        result = llm_manager_decide(mock_client, "test-model", "done", "", "summary")
        assert result["output"] == "validate"
        assert result["reason"] == "tests passed"
