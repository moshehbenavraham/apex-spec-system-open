# Apex Spec System

**Version: 2.0.5-codex**

A specification-driven workflow system for AI-assisted development, packaged as
an Agent Skill following the [Agent Skills standard](https://agentskills.io).

Ported from the original Claude Code plugin to work with Codex CLI and any
agent tool that supports the Agent Skills standard.

## Overview

The Apex Spec System breaks large projects into manageable, well-scoped
implementation sessions that fit within AI context windows and human attention
spans.

**Philosophy**: `1 session = 1 spec = 2-4 hours (12-25 tasks)`

## Quick Start

```bash
# Install to your skills directory
git clone https://github.com/[org]/apex-spec-system-open.git ~/.agents/skills/apex-spec
```

Then invoke:

```
$apex-spec
```

Or let the skill activate implicitly when working in a project with a
`.spec_system/` directory.

## Requirements

| Dependency | Required | Install |
|------------|----------|---------|
| bash | Yes | Pre-installed on macOS/Linux |
| git | Yes | Pre-installed or `apt install git` |
| jq | Yes | `apt install jq` or `brew install jq` |

Verify with: `bash scripts/check-prereqs.sh --env`

## The Workflow

### Stage 1: Initialize (Once)

```
initspec      ->  Set up spec system in project
createprd     ->  Generate PRD from requirements (optional)
createuxprd   ->  Generate UX PRD from design docs (optional)
phasebuild    ->  Create first phase structure
```

### Stage 2: Session Workflow (Repeat)

```
plansession   ->  Analyze project, create spec + task checklist
implement     ->  AI-led task-by-task implementation
validate      ->  Verify session completeness
updateprd     ->  Mark session complete, sync state
```

### Stage 3: Phase Transition

```
audit         ->  Local dev tooling (formatter, linter, types, tests)
pipeline      ->  CI/CD workflows
infra         ->  Production infrastructure
carryforward  ->  Capture lessons learned
documents     ->  Audit and update documentation
phasebuild    ->  Create next phase structure
```

### Utility Commands (Safe at Any Time)

| Command | Purpose |
|---------|---------|
| copush | Pull, version-bump, commit, push |
| sculpt-ui | Guide AI-led frontend design |
| dockbuild | Docker Compose build and start |
| dockcleanbuild | Clean Docker rebuild |
| up2imp | Audit upstream changes |
| qimpl | Autonomous implementation session |
| qfrontdev | Autonomous frontend development |
| qbackenddev | Autonomous backend development |
| pullndoc | Pull and document upstream changes |

## Repository Structure

```
.
|-- SKILL.md              # Root orchestrator (entry point)
|-- AGENTS.md             # Agent custom instructions
|-- agents/
|   \-- openai.yaml       # Codex CLI metadata
|-- references/           # Command reference files (1 per command)
|-- scripts/              # Bash utilities for project analysis
|-- commands/             # Original Claude Code source files
\-- docs/                 # Documentation
```

## Project Structure (After Initialization)

Running the initspec workflow step creates this in your project:

```
your-project/
|-- .spec_system/               # All spec system files
|   |-- state.json              # Project state tracking
|   |-- CONSIDERATIONS.md       # Institutional memory
|   |-- SECURITY-COMPLIANCE.md  # Security posture
|   |-- CONVENTIONS.md          # Coding standards
|   |-- PRD/                    # Product requirements
|   |-- specs/                  # Implementation specs
|   |-- scripts/                # Copied analysis scripts
|   \-- archive/                # Completed work
\-- (your project source files)
```

## Monorepo Support

The system auto-detects monorepo structures. Single `.spec_system/` at the
repo root. Sessions reference their target package in metadata, not in
directory names. Sessions interleave across packages within a phase.

Supported workspace managers: pnpm, npm workspaces, Turborepo, Nx, Cargo
workspaces, Go modules, Lerna.

## Features

- **22-Command Workflow**: Structured process from initialization to completion
- **Session Scoping**: 12-25 tasks per session, 2-4 hours max
- **Progress Tracking**: State file and checklists track progress
- **Validation Gates**: Verify completeness and security before marking done
- **Coding Conventions**: Customizable standards enforced during sessions
- **Monorepo Support**: Auto-detects workspace structures, per-package scoping
- **ASCII Enforcement**: Avoid encoding issues that break code generation
- **Platform Neutral**: Works with any agent tool supporting Agent Skills

## Session Limits

| Limit | Value |
|-------|-------|
| Maximum tasks | 25 |
| Maximum duration | 4 hours |
| Ideal task count | 12-25 (sweet spot: 20) |
| Objectives | Single clear objective |

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Skill structure and design decisions
- [Development Guide](docs/development.md) - Local setup, testing, contributing
- [Usage Guidance](docs/GUIDANCE.md) - When to use, workflow modes, team patterns
- [Production Walkthrough](docs/WALKTHROUGH.md) - Real-world examples
- [Contributing](CONTRIBUTING.md) - Branch conventions, commit style, PR process
- [ADRs](docs/adr/) - Architecture decision records

## Video Tutorial

[Watch on YouTube](https://youtu.be/iY6ySesmOCg) - Installation and workflow walkthrough

## Development Status

| Phase | Name | Status |
|-------|------|--------|
| 00 | Proof of Concept | Complete |
| 01 | Full Command Migration | Complete |
| 02 | Documentation and Polish | Not Started |
| 03 | Distribution | Not Started |

Phase 00 established the orchestrator SKILL.md and converted 4 core commands
(initspec, createprd, plansession, implement) to platform-neutral reference
files. Phase 01 converted the remaining 18 commands and 3 doc files, with
full regression verification across all 25 reference files.

See [PRD](.spec_system/PRD/PRD.md) for the full roadmap.

## License

[MIT](LICENSE)
