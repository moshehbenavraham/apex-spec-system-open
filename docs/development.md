# Development Guide

## Required Tools

| Tool | Version | Install |
|------|---------|---------|
| bash | 4.0+ | Pre-installed on macOS/Linux |
| git | any | Pre-installed or `apt install git` |
| jq | any | `apt install jq` or `brew install jq` |
| shellcheck | any | `apt install shellcheck` or `brew install shellcheck` |
| shfmt | any | `go install mvdan.cc/sh/v3/cmd/shfmt@latest` or `brew install shfmt` |
| pre-commit | any | `pip install pre-commit` or `brew install pre-commit` |

## Local Setup

```bash
git clone https://github.com/moshehbenavraham/apex-spec-system-open.git
cd apex-spec-system-open
pre-commit install
```

No build step -- the skill is plain files.

## Project Layout

| Directory | Contents |
|-----------|----------|
| `SKILL.md` | Root orchestrator (dispatch table, workflow overview) |
| `references/` | Platform-neutral command and supporting reference files |
| `scripts/` | Bash utilities for project analysis |
| `agents/` | Codex CLI metadata (openai.yaml) |
| `plugins/apex-spec/` | Codex plugin wrapper plus generated skill payload |
| `apex-infinite-cli/` | Autonomous session manager |
| `apex-infinite-cli/docs/` | CLI runbook, event stream, history, prompt, wrapper, and troubleshooting docs |
| `docs/` | Project documentation |
| `tests/` | Root-level tests (bats) |
| `skills/` | Legacy skill directory (pre-port, archived) |
| `.spec_system/` | Spec system state for this project's own development |

## Dev Scripts

| Command | Purpose |
|---------|---------|
| `bash scripts/analyze-project.sh --json` | Show project state as JSON |
| `bash scripts/check-prereqs.sh --json --env` | Verify environment |
| `bash scripts/sync-plugin-payload.sh` | Rebuild generated Codex plugin skill payload |
| `bash scripts/sync-plugin-payload.sh --check` | Verify generated plugin payload is current |
| `shellcheck scripts/*.sh` | Lint all scripts |
| `shfmt -d scripts/*.sh` | Check script formatting |
| `pre-commit run --all-files` | Run all pre-commit hooks |

## Skill Payload Sync

The repo-root skill files are canonical:

- `SKILL.md`
- `references/`
- `scripts/`
- `agents/openai.yaml`

The nested skill payload under `plugins/apex-spec/skills/apex-spec/` is
generated packaging output for the Codex plugin wrapper. Do not edit that nested
payload directly.

When changing skill files:

1. Edit the root canonical files.
2. Run `bash scripts/sync-plugin-payload.sh`.
3. Run the relevant checks.
4. Commit both canonical changes and generated plugin payload changes.

## Editing a Command Reference

All active workflow definitions live in `references/`.

When updating a workflow step:

1. Edit `references/<name>.md` directly
2. Keep the first line as `# <name>`
3. Use platform-neutral language and local-first script resolution
4. Verify ASCII encoding: `LC_ALL=C grep -n '[^[:print:][:space:]]' references/<name>.md`
5. Verify line count is under 500: `wc -l references/<name>.md`
6. Verify the dispatch table in SKILL.md routes to the file
7. Run `bash scripts/sync-plugin-payload.sh`

See `docs/CONVENTIONS.md` for the full style guide.

## Validation Checklist

Before submitting changes:

- [ ] All files are ASCII-only (no Unicode, emoji, smart quotes)
- [ ] All files use LF line endings (no CRLF)
- [ ] Reference files have no YAML frontmatter
- [ ] Reference files start with `# Command Name` heading
- [ ] Reference files are under 500 lines
- [ ] No `${CLAUDE_PLUGIN_ROOT}` references remain
- [ ] No `/commandname` slash syntax remains
- [ ] No Claude Code tool directives remain ("Use the Read tool", etc.)
- [ ] shellcheck passes on all scripts
- [ ] shfmt reports no formatting issues
- [ ] `bash scripts/sync-plugin-payload.sh --check` passes
- [ ] pre-commit hooks pass

## Testing

### Script Testing

```bash
# Test on current platform
bash scripts/analyze-project.sh --json | jq .
bash scripts/check-prereqs.sh --json --env | jq .
```

Scripts should produce identical JSON output on macOS, Ubuntu/Debian, and WSL2.

### Command Dispatch Testing

Verify the SKILL.md dispatch table matches existing reference files:

```bash
# Count dispatch entries
grep -c 'references/' SKILL.md

# List reference files
ls references/*.md
```

### Apex Infinite CLI Testing

```bash
cd apex-infinite-cli
python -m pip install -e ".[dev]"
pytest tests/ -v
python -m black --check src tests
python -m pylint src/apex_infinite src/apex_infinite_visual
python -m mypy
```

Install the `visual` extra only when working on the optional Linux
visual wrapper:

```bash
cd apex-infinite-cli
python -m pip install -e ".[visual]"
QT_QPA_PLATFORM=offscreen apex-infinite-visual --dry-run --max-iterations 1 --auto-close-ms 900
```

The test suite covers prompt routing, CLI flags, UI config, renderer behavior,
history rendering, subprocess handling, event streams, and optional wrapper
source-mode behavior. Phase 00 release verification recorded 216 local pytest
tests passing after wrapper productization.

Deep-dive docs for the CLI live in `apex-infinite-cli/docs/`:

- `operator-runbook.md` for day-to-day operation
- `event-stream.md` for JSONL lifecycle events and machine-output mode
- `history-db.md` for SQLite storage details
- `prompt-contract.md` for manager and summarizer behavior
- `visual-wrapper-boundary.md` and `visual-wrapper-productization.md` for
  optional wrapper source mode and binary release gates
- `troubleshooting.md` for common failures and recovery paths

### CI Release Verification

The `release.yml` workflow runs 5 verification steps before publishing a release:

1. **ASCII encoding** -- Validates all skill files contain only ASCII (0-127). Excludes `apex-infinite-cli/` (separate Python tool).
2. **Version sync** -- Confirms the version in `SKILL.md` frontmatter matches `README.md`.
3. **File inventory** -- Checks that at least 23 reference files and 3 scripts are present.
4. **Script executability** -- Verifies all `.sh` files in `scripts/` have the execute bit set.
5. **Apex Infinite CLI health** -- Installs the CLI package, runs
   `apex-infinite --version`, and checks help output for event-stream
   options.

All release checks must pass before a GitHub Release is created.

The `test.yml` workflow also validates the Codex plugin wrapper: the repo
marketplace entry must point to `plugins/apex-spec`, the plugin manifest version
must match the root skill version, and the packaged skill must mirror the root
skill files.

Python dependency vulnerability checks currently have local Phase 00 evidence
from `pip-audit` in the CLI development environment. Recurring CLI dependency
audit automation remains an open follow-up in `.spec_system/SECURITY-COMPLIANCE.md`.

### Encoding Testing

```bash
# Check for non-ASCII characters
LC_ALL=C grep -rn '[^[:print:][:space:]]' references/ scripts/ SKILL.md

# Check for CRLF line endings
grep -rn "$(printf '\r')" references/ scripts/ SKILL.md
```
