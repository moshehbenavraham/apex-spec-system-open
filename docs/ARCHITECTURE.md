# Architecture

## System Overview

The Apex Spec System is a 24-command skill surface for AI-assisted development:
14 staged workflow commands for specification-driven delivery, plus 10 utility
commands for out-of-band support tasks. It is packaged as an Agent Skill
following the Agent Skills standard (agentskills.io). It uses a "Skill Family
with Shared References" pattern: a root orchestrator (SKILL.md) dispatches to
command-specific reference documents based on user intent.

## Skill Structure

```
apex-spec-system-open/
|-- SKILL.md                  # Root orchestrator (entry point)
|-- AGENTS.md                 # Custom instructions for AI agents
|-- CLAUDE.md                 # Claude Code custom instructions
|-- agents/
|   \-- openai.yaml           # Codex CLI UI metadata
|-- docs/
|   \-- CHANGELOG.md          # Version history
|   \-- CONTRIBUTING.md       # Branch, commit, and PR process
|-- references/               # Command and supporting reference files
|   |-- initspec.md           # Initialize spec system
|   |-- createprd.md          # Generate PRD
|   |-- plansession.md        # Plan session
|   |-- implement.md          # Execute implementation
|   |-- creview.md            # Review and repair uncommitted changes
|   |-- validate.md           # Verify session completeness
|   |-- updateprd.md          # Mark session complete
|   |-- (17 more commands)    # 24 total: 14 workflow, 10 utility
|   |-- guidance.md           # Usage guidance
|   |-- utilities.md          # Utility commands reference
|   \-- walkthrough.md        # Real-world walkthrough
|-- scripts/                  # Bash utilities
|   |-- analyze-project.sh    # Deterministic project state analysis
|   |-- check-prereqs.sh      # Environment verification
|   \-- common.sh             # Shared functions
|-- apex-infinite-cli/        # Autonomous session manager
|   |-- pyproject.toml        # Package, dependency, and tool config
|   |-- src/apex_infinite/    # CLI entry point, events, UI, config
|   |-- src/apex_infinite_visual/ # Optional Linux visual wrapper source mode
|   |-- tests/                # pytest suite for CLI, renderer, events, wrapper
|   \-- n8n-workflow/         # Original n8n workflow (reference archive)
\-- docs/                     # Project documentation
```

## Dispatch Flow

```
User Request
    |
    v
SKILL.md (Orchestrator)
    |-- Matches keywords against dispatch table (24 entries: 14 workflow, 10 utility)
    |
    v
references/<command>.md
    |-- Contains full instructions for that workflow step or utility command
    |-- Uses platform-neutral language
    |-- References .spec_system/scripts/ for analysis
    |
    v
Project .spec_system/
    |-- state.json, specs/, PRD/, scripts/
```

### Why This Pattern

Three options were evaluated (see ADR 0001):

1. **Single Compound Skill** -- Everything in one SKILL.md. Too large.
2. **Individual Skills per Command** -- 24 separate skills. Pollutes namespace.
3. **Skill Family with Shared References (Chosen)** -- Clean namespace,
   modular files, progressive disclosure works naturally.

## Script Architecture

Scripts provide deterministic project state analysis. They are bundled in the
skill's `scripts/` directory and copied to `.spec_system/scripts/` during
project initialization (initspec). Commands use a local-first resolution
pattern:

```bash
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

### Script Dependencies

| Script | Depends On | Purpose |
|--------|-----------|---------|
| analyze-project.sh | common.sh, jq | Project state as JSON |
| check-prereqs.sh | common.sh, jq | Environment verification |
| common.sh | bash, jq | Shared functions |

## Tech Stack

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| Markdown (SKILL.md, references/) | Skill definitions | Agent Skills standard |
| YAML (agents/openai.yaml) | Codex UI metadata | Codex convention |
| Bash (scripts/) | Project analysis | Portable, no extra deps |
| JSON (state.json) | State tracking | Simple, jq-parseable |
| jq | JSON processing | Standard CLI tool |

## Content Transformation Rules

When converting from Claude Code plugin format to Agent Skill format, these
rules are applied to every command file:

1. Strip YAML frontmatter
2. Add `# Command Name` heading as first line
3. Replace tool directives with generic verbs ("Read" not "Use the Read tool")
4. Replace /commandname with workflow step names
5. Replace ${CLAUDE_PLUGIN_ROOT} with local-first script resolution
6. Remove co-author/attribution references
7. Preserve all core workflow logic

## Dual-Platform Strategy

Currently maintained as separate repos:

- **apex-spec-system** (private) -- Claude Code plugin, canonical source
- **apex-spec-system-open** (this repo) -- Codex CLI skill, ported

Long-term goal: cross-compatible single format that works on both platforms.

## Apex Infinite CLI

The `apex-infinite-cli/` directory contains an autonomous session manager -- a
standalone Python package that runs the full Apex Spec System workflow in a loop
without human intervention.

### Components

| Component | Purpose |
|-----------|---------|
| `pyproject.toml` | Package metadata, dependencies, console scripts, and Python tool config |
| `src/apex_infinite/cli.py` | Click entry point, config loading, manager loop, Codex subprocess execution, SQLite history, notifications |
| `src/apex_infinite/ui.py` | Rich/plain renderer boundary, display settings, themes, width-aware output helpers |
| `src/apex_infinite/events.py` | Importable event emitter and line-buffered JSONL lifecycle event writer |
| `src/apex_infinite/config.yaml` | Packaged default provider, Codex, and UI config |
| `src/apex_infinite_visual/` | Optional PySide6/Qt Quick Linux visual wrapper over the event stream |
| `requirements*.txt` | Compatibility shims that install `pyproject.toml` dependencies and extras |
| `tests/` | pytest coverage for prompt routing, CLI flags, renderer, history, subprocess, events, and wrapper behavior |
| `n8n-workflow/` | Original n8n workflow JSON (reference archive) |

### How It Works

1. Manager LLM decides the next workflow command
2. CLI executes `codex exec` with the chosen command
3. Response is logged to SQLite (`~/.apex-infinite/history.db`)
4. Optional JSONL lifecycle events are emitted to a file or machine-output
   stdout
5. Loop repeats until `alldonebaby`, an operator stop, or max iterations

### Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.10+ | CLI runtime |
| SQLite (WAL mode) | Interaction history |
| OpenAI-compatible API | Manager and summarizer LLM calls |
| Codex CLI (`codex exec`) | Agent execution subprocess |
| Rich | Human terminal rendering with plain and ASCII fallbacks |
| pytest + pytest-mock | Test suite |
| black, pylint, mypy | Python formatting, linting, and type checks |
| pip-audit | Local Python dependency vulnerability audit |
| PySide6 / Qt Quick / QML | Optional Linux visual wrapper source mode |

See [apex-infinite-cli/README.md](../apex-infinite-cli/README.md) for usage details.

Deep-dive docs:

- [Operator runbook](../apex-infinite-cli/docs/operator-runbook.md)
- [Event stream contract](../apex-infinite-cli/docs/event-stream.md)
- [History DB reference](../apex-infinite-cli/docs/history-db.md)
- [Prompt contract](../apex-infinite-cli/docs/prompt-contract.md)
- [Troubleshooting guide](../apex-infinite-cli/docs/troubleshooting.md)
- [Visual wrapper boundary](../apex-infinite-cli/docs/visual-wrapper-boundary.md)

## Key Decisions

See [Architecture Decision Records](adr/) for detailed decision history.

- ADR 0001: Skill Family with Shared References pattern
