"""Opt-in live Ollama integration test."""

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

import apex_infinite.cli as apex_infinite

CLI_DIR = Path(__file__).resolve().parents[1]
load_dotenv(CLI_DIR / ".env")

pytestmark = pytest.mark.skipif(
    os.environ.get("APEX_INFINITE_LIVE_OLLAMA") != "1",
    reason="set APEX_INFINITE_LIVE_OLLAMA=1 to run live Ollama checks",
)


def test_live_ollama_provider_lists_model_and_completes_chat():
    config_path = CLI_DIR / "config.yaml"
    config = apex_infinite.load_config(config_path, provider_override="ollama")

    result = apex_infinite.run_provider_preflight(config, check_completion=True)

    assert result.provider_name == "ollama"
    assert result.model_name == config["providers"]["ollama"]["model"]
    assert result.model_count >= 1
    assert result.completion_checked is True
