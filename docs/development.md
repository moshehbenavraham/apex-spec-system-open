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
git clone https://github.com/aiwithapex/apex-spec-system-open.git
cd apex-spec-system-open
pre-commit install
```

No build step -- the skill is plain files.

## Project Layout

| Directory | Contents |
|-----------|----------|
| `SKILL.md` | Root orchestrator (dispatch table, workflow overview) |
| `references/` | Platform-neutral reference files (26 total: 22 commands + 4 docs) |
| `scripts/` | Bash utilities for project analysis |
| `agents/` | Codex CLI metadata (openai.yaml) |
| `apex-infinite-cli/` | Autonomous session manager (Python CLI) |
| `commands/` | Original Claude Code command files (source for conversion) |
| `docs/` | Project documentation |
| `tests/` | Root-level tests (bats) |
| `skills/` | Legacy skill directory (pre-port, archived) |
| `.spec_system/` | Spec system state for this project's own development |

## Dev Scripts

| Command | Purpose |
|---------|---------|
| `bash scripts/analyze-project.sh --json` | Show project state as JSON |
| `bash scripts/check-prereqs.sh --json --env` | Verify environment |
| `shellcheck scripts/*.sh` | Lint all scripts |
| `shfmt -d scripts/*.sh` | Check script formatting |
| `pre-commit run --all-files` | Run all pre-commit hooks |

## Converting a Command File

To convert a command from `commands/` to `references/`:

1. Copy `commands/<name>.md` to `references/<name>.md`
2. Strip the YAML frontmatter (`---name:...---` block)
3. Change heading from `# /<name> Command` to `# <name>`
4. Replace `${CLAUDE_PLUGIN_ROOT}/scripts/` with local-first pattern
5. Replace `/commandname` slash syntax with workflow step names
6. Replace tool directives with generic verbs
7. Remove co-author references
8. Verify ASCII encoding: `LC_ALL=C grep -n '[^[:print:][:space:]]' references/<name>.md`
9. Verify line count is under 500: `wc -l references/<name>.md`
10. Verify the dispatch table in SKILL.md routes to the new file

See `.spec_system/CONVENTIONS.md` for the full style guide.

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
pip install -r requirements.txt -r requirements-dev.txt
pytest tests/ -v
```

The test suite covers prompt generation, system prompt content, JSON parsing,
and build_codex_prompt parametrized across all 13 known commands.

### CI Release Verification

The `release.yml` workflow runs 4 verification steps before publishing a release:

1. **ASCII encoding** -- Validates all skill files contain only ASCII (0-127). Excludes `commands/` and `apex-infinite-cli/` (archived/separate).
2. **Version sync** -- Confirms the version in `SKILL.md` frontmatter matches `README.md`.
3. **File inventory** -- Checks that at least 26 reference files and 3 scripts are present.
4. **Script executability** -- Verifies all `.sh` files in `scripts/` have the execute bit set.

All 4 checks must pass before a GitHub Release is created.

### Encoding Testing

```bash
# Check for non-ASCII characters
LC_ALL=C grep -rn '[^[:print:][:space:]]' references/ scripts/ SKILL.md

# Check for CRLF line endings
grep -rn "$(printf '\r')" references/ scripts/ SKILL.md
```
