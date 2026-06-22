# Apex Spec System

A specification-driven workflow system for AI-assisted development.

Philosophy: 1 session = 1 spec = 2-4 hours (12-25 tasks)

## Version

Current version: 2.1.1-codex

When updating version, update it in all the following files:

- README.md
- SKILL.md (frontmatter version field)
- AGENTS.md
- plugins/apex-spec/.codex-plugin/plugin.json
- plugins/apex-spec/skills/apex-spec/SKILL.md (generated from root SKILL.md)

Edit the root files first, then run `bash scripts/sync-plugin-payload.sh` to
refresh the generated plugin skill payload. Do not edit the generated plugin
skill copy directly.

## Project Context

This project is an Agent Skill packaged for the Agent Skills standard. It
provides a 24-command surface: a 14-command staged workflow for breaking large
projects into manageable implementation sessions, plus 10 utility commands for
out-of-band support tasks. The skill uses a "Skill Family with Shared
References" pattern: a root orchestrator (SKILL.md) dispatches to
command-specific reference documents in references/.

## Key Conventions

- All files must be ASCII-only (code points 0-127) with Unix LF line endings
- Reference files use platform-neutral language (no tool-specific directives)
- Reference files have no YAML frontmatter; first line is always a level-1 heading
- Scripts use bash + jq only; no additional dependencies
- Commands use local-first script resolution: check .spec_system/scripts/ before
  falling back to scripts/
- Commands are autonomous: do not ask questions, request approval, or wait for
  human feedback. Use evidence-backed assumptions, record them, and continue.
- Every command response must include a concise summary and an explicit
  `Next command:` handoff, or `Next command: none` when the workflow is complete.
- Root `SKILL.md`, `references/`, `scripts/`, and `agents/openai.yaml` are the
  canonical authored skill files. The nested plugin skill payload under
  `plugins/apex-spec/skills/apex-spec/` is generated packaging output. Do not
  edit the nested payload directly; run `bash scripts/sync-plugin-payload.sh`
  after changing canonical skill files.
- See docs/CONVENTIONS.md for complete coding standards

## Directory Layout

| Directory | Purpose |
|-----------|---------|
| SKILL.md | Root orchestrator and entry point |
| .agents/plugins/ | Codex plugin marketplace metadata |
| plugins/apex-spec/ | Codex plugin wrapper and generated packaged skill copy |
| references/ | Command references plus supporting checklists and workflow docs |
| scripts/ | Bash utilities (analyze-project.sh, check-prereqs.sh, common.sh) |
| agents/ | Codex CLI metadata (openai.yaml) |
| apex-infinite-cli/ | Autonomous session manager (Python CLI, see its own README) |
| docs/ | Development documentation (ARCHITECTURE.md, development.md, adr/) |

## Workflow Reference

See SKILL.md for the complete command dispatch table and workflow stages.
See references/workflow-overview.md for a quick-reference summary.

## Routing Fallback

Prefer `SKILL.md` when you need the full dispatch table. If you only need a
fast starting point, route by stage:

- Stage 1, no `.spec_system/` yet: `initspec`
- Stage 1, requirements or design docs need to become PRD artifacts:
  `createprd` or `createuxprd`
- Stage 1, PRD is ready and phase structure is missing: `phasebuild`
- Stage 2, initialized project and next scoped session needed: `plansession`
- Stage 2, current session already has `spec.md` and `tasks.md`: `implement`
- Stage 2, implementation is done and needs review/repair: `creview`
- Stage 2, review is done and implementation needs verification: `validate`
- Stage 2, validation passed and progress should be synced: `updateprd`
- Stage 3, all sessions in the current phase are done: `audit`
- Utility work outside the staged flow: `copush`, `qimpl`, `dockbuild`,
  `pullndoc`, and the other utility commands

Intent examples:

- New repo or existing repo with no spec system: `initspec`
- Need the next right-sized session in an initialized project: `plansession`
- Have a work file and want an autonomous implementation burst: `qimpl`
- Finished all sessions in a phase and need the next workflow step: `audit`

Do not import a blanket low-threshold routing rule. Use the staged workflow in
`SKILL.md` and `references/workflow-overview.md` rather than guessing.

## Development

See docs/development.md for local setup, testing, and contributing guidelines.
See CONTRIBUTING.md for branch conventions, commit style, and PR process.
