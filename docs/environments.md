# Environments

The Apex Spec System is a plain-files skill and Codex plugin wrapper. The
runtime environments below describe where the files are validated and consumed;
there is no hosted application environment.

| Environment | Location | Purpose | Verification |
|-------------|----------|---------|--------------|
| Local development | Repository checkout | Edit skill files, scripts, docs, and the Apex Infinite CLI | `bats tests/`, `bash scripts/sync-plugin-payload.sh --check`, CLI pytest |
| GitHub Actions | `.github/workflows/` | Validate shell scripts, reference integrity, plugin payload sync, release inventory, and secrets patterns | Push, pull request, scheduled security, and tag workflows |
| Installed skill | Agent skills directory or Codex plugin install | Consume `SKILL.md`, `references/`, `scripts/`, and `agents/openai.yaml` | `ls ~/.agents/skills/apex-spec/SKILL.md` or plugin install verification |
| Apex Infinite CLI | `apex-infinite-cli/` | Run autonomous Codex workflow loops against initialized projects | `apex-infinite --help`, `pytest tests/ -v`, `scripts/check-ollama.sh` |
| Optional visual wrapper | `apex-infinite-cli/src/apex_infinite_visual/` | Source-mode Linux companion UI over the JSONL event boundary | `QT_QPA_PLATFORM=offscreen apex-infinite-visual --dry-run --max-iterations 1 --auto-close-ms 900` |

## Environment Variables

| Variable | Used By | Purpose | Required |
|----------|---------|---------|----------|
| `OLLAMA_HOST` | Apex Infinite CLI Ollama provider | Host used in the local Ollama OpenAI-compatible base URL | Optional, defaults to `localhost` |
| `OLLAMA_PORT` | Apex Infinite CLI Ollama provider | Port used in the local Ollama OpenAI-compatible base URL | Optional, defaults to `11434` |
| `OLLAMA_API_KEY` | Apex Infinite CLI Ollama provider | API key placeholder for the OpenAI-compatible client | Optional, defaults to `ollama` |
| `OLLAMA_MODEL` | Apex Infinite CLI Ollama provider | Model name used for local Ollama manager calls | Optional, defaults to `qwen2.5:7b` |
| `APEX_INFINITE_PROVIDER_CHECK_TIMEOUT` | Apex Infinite CLI provider preflight | Timeout in seconds for provider model-list and chat checks | Optional, defaults to `10` |
| `APEX_INFINITE_LIVE_OLLAMA` | Apex Infinite CLI pytest | Enables the opt-in live Ollama integration test when set to `1` | Optional, defaults to disabled |
| `XAI_API_KEY` | Apex Infinite CLI Grok provider | API key expanded from `config.yaml` | Only when `provider: grok` |
| `OPENAI_API_KEY` | Apex Infinite CLI OpenAI provider | API key expanded from `config.yaml` | Only when `provider: openai` |
| `NO_COLOR` | Apex Infinite CLI renderer | Forces plain fallback unless an explicit theme is selected | Optional |
| `TERM=dumb` | Apex Infinite CLI renderer | Forces constrained-output fallback | Optional |
| `QT_QPA_PLATFORM=offscreen` | Optional visual wrapper | Enables headless wrapper smoke checks | Optional |

Copy `apex-infinite-cli/.env.example` to `apex-infinite-cli/.env` only for
local CLI provider settings. Do not commit `.env` files or provider keys.

## Local Data

The CLI stores interaction history in `~/.apex-infinite/history.db` with SQLite
WAL mode. The database can contain project paths, operator instructions,
manager decisions, and agent output. See
[History DB reference](../apex-infinite-cli/docs/history-db.md) and
[Security & Compliance](../.spec_system/SECURITY-COMPLIANCE.md).

## Deployment Notes

The base skill has no server, database, or cloud runtime. Release distribution
is described in [Deployment](deployment.md). The optional Linux visual wrapper
is source-shippable only; binary/AppImage publishing remains gated by the
license, notice, checksum, source/relink, and generated-bundle review described
in [Visual wrapper productization](../apex-infinite-cli/docs/visual-wrapper-productization.md).
