# Apex Spec System

**Version: 2.0.9-codex**

A specification-driven workflow system for AI-assisted development, packaged as
an Agent Skill following the [Agent Skills standard](https://agentskills.io).

Break large projects into manageable, well-scoped implementation sessions that
fit within AI context windows and human attention spans.

**Philosophy**: `1 session = 1 spec = 2-4 hours (12-25 tasks)`

## Requirements

| Dependency | Required | Install |
|------------|----------|---------|
| bash | Yes | Pre-installed on macOS/Linux |
| git | Yes | Pre-installed or `apt install git` |
| jq | Yes | `apt install jq` or `brew install jq` |

Verify with: `bash scripts/check-prereqs.sh --env`

## Quick Start

```bash
# 1. Install the skill (see Installation below)
# 2. Initialize spec system in your project
$apex-spec initspec

# 3. Create a PRD from your requirements doc
$apex-spec createprd

# 4. Build the first phase structure
$apex-spec phasebuild

# 5. Plan and implement sessions
$apex-spec plansession
$apex-spec implement
$apex-spec validate
$apex-spec updateprd
```

The skill also activates implicitly when working in a project with a
`.spec_system/` directory.

## Installation

### Method 1: Git Clone (Recommended)

Clone directly into your agent skills directory:

```bash
git clone https://github.com/aiwithapex/apex-spec-system-open.git \
  ~/.agents/skills/apex-spec
```

### Method 2: Skill Installer

If your agent supports skill installation commands:

```bash
# Codex CLI
codex install-skill https://github.com/aiwithapex/apex-spec-system-open.git
```

### Method 3: Manual Download

Download and extract to your skills directory:

```bash
mkdir -p ~/.agents/skills/apex-spec
curl -L https://github.com/aiwithapex/apex-spec-system-open/archive/refs/heads/master.tar.gz \
  | tar xz --strip-components=1 -C ~/.agents/skills/apex-spec
```

After installation, verify: `ls ~/.agents/skills/apex-spec/SKILL.md`

## The 13-Command Workflow

The workflow has 3 distinct stages. See
[references/workflow-overview.md](references/workflow-overview.md) for the
complete quick-reference.

### Stage 1: Initialization (One-Time Setup)

```
initspec      ->  Set up spec system in project
createprd     ->  Generate PRD from requirements (optional)
createuxprd   ->  Generate UX PRD from design docs (optional)
phasebuild    ->  Create first phase structure
```

### Stage 2: Session Workflow (Repeat Until Phase Complete)

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

## Session Limits

| Limit | Value |
|-------|-------|
| Maximum tasks | 25 |
| Maximum duration | 4 hours |
| Ideal task count | 12-25 (sweet spot: 20) |
| Objectives | Single clear objective |

## Repository Structure

```
apex-spec-system-open/
|-- SKILL.md              # Root orchestrator (skill entry point)
|-- AGENTS.md             # Project instructions for AI agents
|-- CLAUDE.md             # Claude Code custom instructions
|-- agents/
|   \-- openai.yaml       # Codex CLI UI metadata
|-- references/           # Command reference files (26 total)
|-- scripts/              # Bash utilities for project analysis
|-- commands/             # Original Claude Code source files (archive)
\-- docs/                 # Development documentation
```

### Project Structure (After Initialization)

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

The system auto-detects monorepo structures. A single `.spec_system/` lives at
the repo root. Sessions reference their target package in metadata, not in
directory names.

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

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Skill structure and design decisions
- [Development Guide](docs/development.md) - Local setup, testing, contributing
- [Onboarding](docs/onboarding.md) - Zero-to-hero checklist
- [Deployment](docs/deployment.md) - Installation, CI/CD, release process
- [Usage Guidance](references/guidance.md) - When to use, workflow modes, team patterns
- [Production Walkthrough](references/walkthrough.md) - Real-world examples
- [Workflow Quick-Reference](references/workflow-overview.md) - 13-command overview
- [Contributing](CONTRIBUTING.md) - Branch conventions, commit style, PR process
- [ADRs](docs/adr/) - Architecture decision records

## Video Tutorial

[Watch on YouTube](https://youtu.be/iY6ySesmOCg) - Installation and workflow walkthrough

## Development Status

| Phase | Name | Status |
|-------|------|--------|
| 00 | Proof of Concept | Complete |
| 01 | Full Command Migration | Complete |
| 02 | Documentation and Polish | Complete |
| 03 | Distribution | Not Started |

See [PRD](.spec_system/PRD/PRD.md) for the full roadmap.

## License

[MIT](LICENSE)
