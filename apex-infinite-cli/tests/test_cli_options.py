"""Click option wiring tests for display settings."""

from click.testing import CliRunner

import apex_infinite

CONFIG_TEXT = """provider: ollama
codex:
  binary: "codex"
  exec_flags: "--dangerously-auto-approve"
  model_reasoning_effort: "high"
ui:
  theme: "auto"
  effect_level: "low"
  ascii: false
  compact: false
  show_elapsed: true
  show_provider: true
  themes: {}
providers:
  ollama:
    base_url: "http://localhost:11434/v1"
    api_key: "ollama"
    model: "qwen2.5:7b"
"""


def write_config(tmp_path, text=CONFIG_TEXT):
    """Write a config file for CLI tests."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(text, encoding="ascii")
    return config_path


def prepare_cli(monkeypatch, tmp_path):
    """Patch stateful CLI boundaries and return test paths plus captured loop data."""
    config_path = write_config(tmp_path)
    project_path = tmp_path / "project"
    project_path.mkdir()
    captured = {}

    def fake_loop(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(apex_infinite, "DB_DIR", tmp_path / "db")
    monkeypatch.setattr(apex_infinite, "DB_PATH", tmp_path / "db" / "history.db")
    monkeypatch.setattr(apex_infinite, "infinite_loop", fake_loop)
    return config_path, project_path, captured


def invoke_cli(monkeypatch, tmp_path, args):
    """Invoke the CLI with an isolated config, project, DB, and loop."""
    config_path, project_path, captured = prepare_cli(monkeypatch, tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--path",
            str(project_path),
            *args,
        ],
    )
    return result, captured, project_path


def test_theme_flag_reaches_resolved_renderer(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--theme", "crt-amber", "--max-iterations", "0"],
    )

    assert result.exit_code == 0
    assert captured["renderer"].settings.requested_theme == "crt-amber"
    assert captured["renderer"].settings.theme_name == "crt-amber"


def test_plain_ascii_and_compact_flags_reach_loop(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--plain", "--ascii", "--compact", "--max-iterations", "0"],
    )

    assert result.exit_code == 0
    settings = captured["renderer"].settings
    assert settings.plain is True
    assert settings.theme_name == "plain"
    assert settings.ascii_only is True
    assert settings.compact is True


def test_invalid_theme_fails_before_loop(monkeypatch, tmp_path):
    result, captured, _project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--theme", "missing", "--max-iterations", "0"],
    )

    assert result.exit_code == 1
    assert captured == {}


def test_dry_run_startup_wiring_reaches_loop(monkeypatch, tmp_path):
    result, captured, project_path = invoke_cli(
        monkeypatch,
        tmp_path,
        ["--start", "implement", "--dry-run", "--theme", "crt-green"],
    )

    assert result.exit_code == 0
    assert captured["path"] == f"{project_path}/"
    assert captured["start_command"] == "implement"
    assert captured["dry_run"] is True
    assert captured["renderer"].settings.theme_name == "crt-green"


def test_history_mode_uses_renderer_and_does_not_start_loop(monkeypatch, tmp_path):
    config_path, project_path, captured = prepare_cli(monkeypatch, tmp_path)
    history_call = {}

    def fake_history(path=None, renderer=None, verbose=False):
        history_call["path"] = path
        history_call["renderer"] = renderer
        history_call["verbose"] = verbose

    monkeypatch.setattr(apex_infinite, "db_show_history", fake_history)

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--path",
            str(project_path),
            "--history",
            "--verbose",
            "--plain",
        ],
    )

    assert result.exit_code == 0
    assert captured == {}
    assert history_call["path"] == str(project_path)
    assert history_call["verbose"] is True
    assert history_call["renderer"].settings.plain is True


def test_history_verbose_does_not_register_duplicate_flag(monkeypatch, tmp_path):
    config_path, project_path, captured = prepare_cli(monkeypatch, tmp_path)

    result = CliRunner().invoke(
        apex_infinite.main,
        [
            "--config",
            str(config_path),
            "--path",
            str(project_path),
            "--history-verbose",
        ],
    )

    assert result.exit_code == 2
    assert "No such option '--history-verbose'" in result.output
    assert captured == {}


def test_infinite_loop_passes_operator_context_to_renderer(monkeypatch):
    captured = {"iterations": [], "logs": [], "db": []}
    config = {
        "provider": "ollama",
        "codex": {"binary": "codex", "exec_flags": "--test"},
        "providers": {
            "ollama": {
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama",
                "model": "qwen2.5:7b",
            }
        },
    }

    class CapturingRenderer:
        """Capture renderer snapshots without printing terminal output."""

        def print_iteration(self, snapshot):
            captured["iterations"].append(snapshot)

        def print_status(self, *_args, **_kwargs):
            return None

        def print_manager_decision(self, *_args, **_kwargs):
            return None

        def print_completion(self, *_args, **_kwargs):
            return None

        def print_db_log(self, snapshot):
            captured["logs"].append(snapshot)

    monkeypatch.setattr(
        apex_infinite, "get_llm_client", lambda _config: ("client", "model")
    )
    monkeypatch.setattr(apex_infinite, "db_fetch_history", lambda _path, limit=15: [])
    monkeypatch.setattr(
        apex_infinite,
        "llm_summarize",
        lambda _client, _model, _records, renderer=None: "summary",
    )
    monkeypatch.setattr(
        apex_infinite,
        "llm_manager_decide",
        lambda _client, _model, _agent_response, _ceo_msg, _summary, renderer=None: {
            "output": "alldonebaby",
            "reason": "complete",
        },
    )
    monkeypatch.setattr(
        apex_infinite,
        "db_log",
        lambda *args, **kwargs: captured["db"].append((args, kwargs)),
    )
    monkeypatch.setattr(apex_infinite, "notify", lambda *_args, **_kwargs: None)

    apex_infinite.infinite_loop(
        path="/tmp/project/",
        config=config,
        max_iterations=1,
        dry_run=True,
        renderer=CapturingRenderer(),
    )

    iteration = captured["iterations"][0]
    assert iteration.project_path == "/tmp/project/"
    assert iteration.provider_name == "ollama"
    assert iteration.model_name == "qwen2.5:7b"
    assert iteration.iteration == 1
    assert iteration.operation == "history summary"
    assert iteration.dry_run is True
    assert iteration.elapsed_seconds >= 0
    assert captured["logs"][0].manager_output == "alldonebaby"
    assert captured["logs"][0].stored_state == "completion"
    assert captured["db"][0][0][2] == "alldonebaby"


def test_operator_console_wiring_keeps_known_prompt_routing():
    assert (
        apex_infinite.build_codex_prompt("implement", "implement")
        == "Run the apex-spec skill command /implement"
    )
    assert (
        apex_infinite.build_codex_prompt("/validate", "/validate")
        == "Run the apex-spec skill command /validate"
    )
    assert (
        apex_infinite.build_codex_prompt("fix the tests", "fix the tests")
        == "fix the tests"
    )
