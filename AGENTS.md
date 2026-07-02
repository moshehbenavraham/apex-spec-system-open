# Apex Spec System - Agent Guide

A specification-driven workflow system for AI-assisted development, packaged
as an Agent Skill (agentskills.io) with a Codex plugin wrapper.

Philosophy: 1 session = 1 spec = 1 clear objective = 2-4 hours (12-25 tasks).

Current version: 2.1.5-codex

Note: CLAUDE.md and GEMINI.md are symlinks to this file. Edit AGENTS.md only.

## Critical Rules

1. **Never edit generated output.** Root `SKILL.md`, `references/`, `scripts/`,
   and `agents/openai.yaml` are the canonical authored files. Everything under
   `plugins/apex-spec/skills/apex-spec/` is generated packaging output. After
   changing canonical files, run `bash scripts/sync-plugin-payload.sh`.
2. **ASCII only** (code points 0-127) with Unix LF line endings, in every file.
3. **References are platform-neutral**: no tool-specific directives, no YAML
   frontmatter; the first line is always a level-1 heading.
4. **Scripts use bash + jq only**; no additional dependencies. Output must be
   identical on macOS, Ubuntu/Debian, and WSL2.

See docs/CONVENTIONS.md for the complete coding standards.

## Architecture

The skill uses a "Skill Family with Shared References" pattern: the root
orchestrator (SKILL.md) matches user intent against a dispatch table and
routes to one of 24 command references in references/ - a 14-command staged
workflow plus 10 utilities.

| Group | Commands |
|-------|----------|
| Stage 1: Initialization | initspec, createprd, createuxprd, phasebuild |
| Stage 2: Session loop | plansession > implement > creview > validate > updateprd |
| Stage 3: Phase transition | audit, pipeline, infra, carryforward, documents |
| Utilities | copush, sculpt-ui, seshsplit, dockbuild, dockcleanbuild, up2imp, qimpl, qfrontdev, qbackenddev, pullndoc |

Command behavior contracts (enforced across all references):

- Commands are autonomous: never ask questions, request approval, or wait for
  human feedback. Make evidence-backed assumptions, record them, continue.
- Every command response ends with a concise summary and an explicit
  `Next command:` handoff (`Next command: none` when the workflow is done).
- Local-first script resolution: check `.spec_system/scripts/` before falling
  back to `scripts/`.

## Routing

Prefer the full dispatch table in SKILL.md; references/workflow-overview.md is
the quick-reference summary. Fast routing by project state:

| Situation | Command |
|-----------|---------|
| No `.spec_system/` directory yet | initspec |
| Requirements or design docs need PRD artifacts | createprd / createuxprd |
| PRD ready, phase structure missing | phasebuild |
| Initialized, next scoped session needed | plansession |
| Current session has spec.md and tasks.md | implement |
| Implementation done, needs review/repair | creview |
| Review done, needs verification | validate |
| Validation passed, sync progress | updateprd |
| All sessions in the phase complete | audit |
| Out-of-band work (push, docker, quick bursts) | utilities above |

Do not adopt a blanket low-threshold routing rule; route via the staged
workflow rather than guessing.

## Layout

| Path | Purpose |
|------|---------|
| SKILL.md | Root orchestrator: dispatch table, scope rules, workflow stages |
| references/ | 24 command references plus checklists and workflow docs |
| scripts/ | Bash utilities (analyze-project.sh, check-prereqs.sh, common.sh, sync-plugin-payload.sh) |
| tests/ | bats tests for scripts and reference autonomy rules |
| agents/ | Codex CLI metadata (openai.yaml) |
| plugins/apex-spec/ | Codex plugin wrapper + generated skill payload (do not edit) |
| .agents/plugins/ | Codex plugin marketplace metadata |
| agent-skills/ | Companion engineering-skills collection (has its own AGENTS.md) |
| apex-infinite-cli/ | Autonomous session manager, Python CLI (has its own README) |
| docs/ | ARCHITECTURE.md, CONVENTIONS.md, development.md, adr/ |
| skills/ | Legacy pre-port skill directory (archived) |

## Version Bumps

Update the version string in README.md, SKILL.md (frontmatter), AGENTS.md, and
plugins/apex-spec/.codex-plugin/plugin.json, then run
`bash scripts/sync-plugin-payload.sh` to regenerate the packaged SKILL.md copy.

## Verification

```bash
bats tests/                                        # script + reference tests
bash scripts/sync-plugin-payload.sh --check        # generated payload in sync
bash scripts/analyze-project.sh --json | jq .      # script smoke tests
bash scripts/check-prereqs.sh --json --env | jq .
```

See docs/development.md for local setup and testing, and CONTRIBUTING.md for
branch conventions, commit style, and the PR process.
