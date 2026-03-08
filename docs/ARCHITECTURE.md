# Architecture

## System Overview

The Apex Spec System is a 22-command specification-driven workflow for
AI-assisted development, packaged as an Agent Skill following the Agent Skills
standard (agentskills.io). It uses a "Skill Family with Shared References"
pattern: a root orchestrator (SKILL.md) dispatches to command-specific
reference documents based on user intent.

## Skill Structure

```
apex-spec-system-open/
|-- SKILL.md                  # Root orchestrator (entry point)
|-- AGENTS.md                 # Custom instructions for AI agents
|-- CLAUDE.md                 # Claude Code custom instructions
|-- agents/
|   \-- openai.yaml           # Codex CLI UI metadata
|-- references/               # Command reference files (1 per command)
|   |-- initspec.md           # Initialize spec system
|   |-- createprd.md          # Generate PRD
|   |-- plansession.md        # Plan session
|   |-- implement.md          # Execute implementation
|   \-- (18 more planned)     # Remaining commands (Phase 01)
|-- scripts/                  # Bash utilities
|   |-- analyze-project.sh    # Deterministic project state analysis
|   |-- check-prereqs.sh      # Environment verification
|   \-- common.sh             # Shared functions
|-- commands/                 # Original Claude Code command files (source)
|-- docs/                     # Documentation
|   |-- GUIDANCE.md           # Usage guidance
|   |-- UTILITIES.md          # Utility commands reference
|   \-- WALKTHROUGH.md        # Real-world walkthrough
\-- skills/                   # Legacy skill directory (pre-port)
```

## Dispatch Flow

```
User Request
    |
    v
SKILL.md (Orchestrator)
    |-- Matches keywords against dispatch table (22 entries)
    |
    v
references/<command>.md
    |-- Contains full instructions for that workflow step
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
2. **Individual Skills per Command** -- 22 separate skills. Pollutes namespace.
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

## Key Decisions

See [Architecture Decision Records](adr/) for detailed decision history.

- ADR 0001: Skill Family with Shared References pattern
