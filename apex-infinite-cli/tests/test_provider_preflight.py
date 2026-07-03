"""Provider preflight tests."""

from types import SimpleNamespace

import pytest

import apex_infinite.cli as apex_infinite


def make_config(model="qwen2.5:7b"):
    """Return a minimal runtime config for provider preflight tests."""
    return {
        "provider": "ollama",
        "providers": {
            "ollama": {
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama",
                "model": model,
            }
        },
    }


class FakeOpenAIClient:
    """Small OpenAI-compatible test double."""

    def __init__(self, model_ids):
        self.models = SimpleNamespace(
            list=lambda: SimpleNamespace(
                data=[SimpleNamespace(id=model_id) for model_id in model_ids]
            )
        )
        self.chat_calls = []
        self.chat = SimpleNamespace(
            completions=SimpleNamespace(create=self._create_chat_completion)
        )

    def _create_chat_completion(self, **kwargs):
        self.chat_calls.append(kwargs)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))]
        )


def test_run_provider_preflight_accepts_available_model(monkeypatch):
    fake_client = FakeOpenAIClient(["qwen2.5:7b", "llama3.1:8b"])

    monkeypatch.setattr(apex_infinite, "OpenAI", lambda **_kwargs: fake_client)

    result = apex_infinite.run_provider_preflight(make_config())

    assert result.provider_name == "ollama"
    assert result.model_name == "qwen2.5:7b"
    assert result.model_count == 2
    assert result.completion_checked is False
    assert fake_client.chat_calls == []


def test_run_provider_preflight_accepts_implicit_latest_tag(monkeypatch):
    fake_client = FakeOpenAIClient(["llama3.2:latest"])

    monkeypatch.setattr(apex_infinite, "OpenAI", lambda **_kwargs: fake_client)

    result = apex_infinite.run_provider_preflight(make_config(model="llama3.2"))

    assert result.model_name == "llama3.2"
    assert result.model_count == 1


def test_run_provider_preflight_rejects_missing_model(monkeypatch):
    fake_client = FakeOpenAIClient(["llama3.1:8b"])

    monkeypatch.setattr(apex_infinite, "OpenAI", lambda **_kwargs: fake_client)

    with pytest.raises(apex_infinite.CliStartupError, match="not available"):
        apex_infinite.run_provider_preflight(make_config())


def test_run_provider_preflight_checks_chat_when_requested(monkeypatch):
    fake_client = FakeOpenAIClient(["qwen2.5:7b"])

    monkeypatch.setattr(apex_infinite, "OpenAI", lambda **_kwargs: fake_client)

    result = apex_infinite.run_provider_preflight(
        make_config(),
        check_completion=True,
    )

    assert result.completion_checked is True
    assert fake_client.chat_calls == [
        {
            "model": "qwen2.5:7b",
            "messages": [{"role": "user", "content": "Reply with ok."}],
            "max_tokens": 8,
            "temperature": 0,
        }
    ]


def test_run_provider_preflight_rejects_unresolved_env_placeholder():
    config = make_config()
    config["providers"]["ollama"]["base_url"] = "http://${OLLAMA_HOST}:11434/v1"

    with pytest.raises(apex_infinite.CliStartupError, match="unresolved"):
        apex_infinite.run_provider_preflight(config)
