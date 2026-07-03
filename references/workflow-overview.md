# Workflow Overview

Quick-reference for the Apex Spec System's 14-command staged workflow. Apex
Spec also exposes 10 utility commands, listed separately below, for out-of-band
support tasks.

## Core Philosophy

**1 session = 1 spec = 2-4 hours (12-25 tasks)**

A collection of sessions is a phase. A collection of phases is a mature
technical PRD.

## Session Scope Rules

| Limit | Value |
|-------|-------|
| Maximum tasks | 25 |
| Maximum duration | 4 hours |
| Ideal task count | 12-25 (sweet spot: 20) |
| Objectives | Single clear objective |

## Autonomy and Handoff Rules

- Commands must not ask questions, request approval, wait for feedback, or add
  interactive review stops.
- Commands resolve ambiguity from repository evidence and record working
  assumptions when needed.
- If an external requirement prevents progress, commands report it as a
  blocker and still provide a deterministic next command.
- Every command response ends with `Summary:`, `Next command:`, and `Reason:`.

## The 3 Stages

### Stage 1: Initialization (One-Time Setup)

| Step | Command | Purpose |
|------|---------|---------|
| 1 | initspec | Set up .spec_system/ in your project |
| 2 | createprd | Generate PRD from requirements doc (optional) |
| 3 | createuxprd | Generate UX PRD from design docs (optional) |
| 4 | phasebuild | Create first phase structure with session stubs |

### Stage 2: Session Workflow (Repeat Until Phase Complete)

| Step | Command | Purpose |
|------|---------|---------|
| 1 | plansession | Analyze project state, create spec + task checklist |
| 2 | implement | AI-led task-by-task implementation |
| 3 | creview | Review and repair all uncommitted changes |
| 4 | validate | Verify session completeness and quality gates |
| 5 | updateprd | Mark session complete, sync PRD and state |

Repeat this cycle for each session in the phase.

Important: after a successful `plansession` run that creates `spec.md` and `tasks.md`, the next workflow command is always `implement`.
Important: after a successful `implement` run, the next workflow command is always `creview`; after `creview`, the next workflow command is `validate`.
Important: after a successful `updateprd` run, return to `plansession` if the phase still has unfinished sessions; otherwise begin Phase Transition at `audit`.

### Stage 3: Phase Transition (After All Phase Sessions Complete)

| Step | Command | Purpose |
|------|---------|---------|
| 1 | audit | Set up local dev tooling (formatter, linter, types, tests) |
| 2 | pipeline | Configure CI/CD workflows (quality, build, security) |
| 3 | infra | Set up production infrastructure (health, security, deploy) |
| 4 | carryforward | Capture lessons learned |
| 5 | documents | Audit and update project documentation |
| 6 | phasebuild | Create next phase structure if another phase remains |

Important: `carryforward` does not lead directly to `plansession`. Finish
`documents`, then run `phasebuild` only if `PRD.md` still defines another
unfinished phase. Only after `phasebuild` do you return to Stage 2 with
`plansession`. If `PRD.md` has no remaining phase, the workflow ends and the
project is complete.

## Workflow Diagram

```
STAGE 1: INIT           STAGE 2: SESSIONS        STAGE 3: TRANSITION

initspec                plansession ----+         audit
    |                       |           |             |
    v                       v           |             v
createprd (opt)         implement       |         pipeline
    |                       |           |             |
    v                       v           |             v
createuxprd (opt)       creview         |         infra
    |                       |           |             |
    v                       v           |             v
phasebuild              validate        |         carryforward
                            |           |             |
                            v           |             v
                        updateprd ------+         documents
                                                      |
                                                      v
                                                  phasebuild --> Stage 2
```

## Utility Commands (Safe at Any Time)

These 10 commands are not part of the required staged workflow. They run outside
the session workflow and can be used for support tasks at any time:

| Command | Purpose |
|---------|---------|
| copush | Pull, version-bump, commit all changes, push to origin |
| sculpt-ui | Guide AI-led creation of distinctive frontend interfaces |
| seshsplit | Insert or refresh a session split plan inside a text or Markdown plan file |
| dockbuild | Quick Docker Compose build and start |
| dockcleanbuild | Clean Docker environment and rebuild from scratch |
| up2imp | Audit upstream changes and curate implementation list |
| qimpl | Context-aware autonomous implementation session |
| qfrontdev | Autonomous frontend implementation session |
| qbackenddev | Autonomous backend/infrastructure development session |
| pullndoc | Git pull upstream repo and document imported changes |

## Staged Workflow Command Quick Reference

| Command | Input | Output | Normal next command |
|---------|-------|--------|---------------------|
| initspec | Project info | .spec_system/ structure | createprd |
| createprd | Requirements doc | PRD/PRD.md | createuxprd or phasebuild |
| createuxprd | Design docs | PRD/PRD_UX.md | phasebuild |
| phasebuild | PRD | PRD/phase_NN/ | plansession or none |
| plansession | state.json, PRD | spec.md + tasks.md | implement or audit |
| implement | spec.md, tasks.md | implementation-notes.md | creview |
| creview | All uncommitted changes | code-review.md | validate |
| validate | All session files | validation.md | updateprd or implement |
| updateprd | validation.md | Updated state.json | plansession or audit |
| audit | CONVENTIONS.md | Updated dev tools | pipeline or audit |
| pipeline | CONVENTIONS.md | Workflow files | infra or pipeline |
| infra | CONVENTIONS.md | Config files | carryforward or infra |
| carryforward | Phase artifacts | CONSIDERATIONS.md | documents |
| documents | state.json, PRD | Updated docs | phasebuild or none |

## Task Format

```
- [ ] TNNN [SNNMM] [P] Action verb + what + where (`path/to/file`)
```

- `TNNN`: Sequential task ID (T001, T002, ...)
- `[SNNMM]`: Session reference (S0103 = Phase 01, Session 03)
- `[P]`: Optional parallelization marker
