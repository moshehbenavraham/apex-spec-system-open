# Apex Spec System

A specification-driven workflow system for AI-assisted development.

Philosophy: 1 session = 1 spec = 2-4 hours (12-25 tasks)

## Version

Current version: 2.0.13-codex

When updating version, update it in all the following files:

- README.md
- SKILL.md (frontmatter version field)

## Project Context

This project is an Agent Skill packaged for the Agent Skills standard. It
provides a 22-command workflow for breaking large projects into manageable
implementation sessions. The skill uses a "Skill Family with Shared References"
pattern: a root orchestrator (SKILL.md) dispatches to command-specific reference
documents in references/.

## Key Conventions

- All files must be ASCII-only (code points 0-127) with Unix LF line endings
- Reference files use platform-neutral language (no tool-specific directives)
- Reference files have no YAML frontmatter; first line is always a level-1 heading
- Scripts use bash + jq only; no additional dependencies
- Commands use local-first script resolution: check .spec_system/scripts/ before
  falling back to scripts/
- See .spec_system/CONVENTIONS.md for complete coding standards

## Directory Layout

| Directory | Purpose |
|-----------|---------|
| SKILL.md | Root orchestrator and entry point |
| references/ | 26 command reference files (1 per command + 4 docs) |
| scripts/ | Bash utilities (analyze-project.sh, check-prereqs.sh, common.sh) |
| agents/ | Codex CLI metadata (openai.yaml) |
| commands/ | Original Claude Code source files (archive, not active) |
| docs/ | Development documentation (ARCHITECTURE.md, development.md, adr/) |

## Workflow Reference

See SKILL.md for the complete command dispatch table and workflow stages.
See references/workflow-overview.md for a quick-reference summary.

## Development

See docs/development.md for local setup, testing, and contributing guidelines.
See CONTRIBUTING.md for branch conventions, commit style, and PR process.
