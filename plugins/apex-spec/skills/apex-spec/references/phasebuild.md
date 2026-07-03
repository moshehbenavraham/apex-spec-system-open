# phasebuild

Create the directory structure, phase PRD, and session stubs for a new phase. Ensures alignment with completed work and lessons learned.

Use this command only when there is clear evidence that another phase should be created. After a successful `phasebuild`, the next workflow command is always `plansession`.

## Rules

1. **Autonomous execution** - do not ask questions, request approval, or wait for human feedback
2. **ASCII-only characters** and Unix LF line endings in all output
3. **Resolve misalignment before building** - as projects progress, later phases may drift from reality. Reconcile with actual progress before creating artifacts.
4. **If interrupted mid-process**, delete partial artifacts before retrying
5. Each session must have a single clear objective, 12-25 tasks, 2-4 hours scope
6. **Resolve normal ambiguity with evidence-backed working assumptions** - incomplete phase detail is not a reason to ask or stop when PRD and state evidence can support a defensible phase
7. **Surface and resolve material conflicts** between PRD phase definitions, state tracking, completed work, and institutional memory before creating artifacts
8. **Record material resolutions** in the phase PRD when they shape the generated phase or session stubs
9. **Keep hard blockers out of successful artifacts** - successful phase files must not contain blocker placeholders or interactive follow-up notes

### No Deferral Policy

- Read PRD.md, state.json, existing phase artifacts, CONSIDERATIONS.md, and SECURITY-COMPLIANCE.md when present before declaring a blocker
- Ambiguity alone is not a blocker; resolve it with evidence-backed working assumptions when phase artifacts can still be created safely
- If PRD.md and state.json disagree, choose the best-supported interpretation, update stale tracking where required, and record the resolution when material
- Stop only when neither PRD.md nor state.json provides clear evidence that another phase should be created
- Successful output must not contain unresolved template placeholders, hard-blocker text, or requests for user arbitration

## Steps

### 1. Assess Current State

Read `.spec_system/state.json` and `.spec_system/PRD/PRD.md` to understand:
- What has been accomplished
- Next sequential phase number
- High-level objectives remaining

Determine whether an upcoming phase is clearly indicated:

- From `.spec_system/PRD/PRD.md`: Look for a phases table, roadmap, or other explicit phase definitions that show at least one unfinished phase beyond the current one
- From `.spec_system/state.json`: Look for phase tracking that makes it clear another phase should exist next (for example, completed/current phases with remaining planned work or an incomplete phase sequence that `PRD.md` supports)

Resolve the next phase from these two sources before creating any artifacts.

**Fail early if both sources are unclear:**

- If `.spec_system/PRD/PRD.md` does not clearly indicate any remaining upcoming phase
- And `.spec_system/state.json` also does not clearly indicate any remaining upcoming phase
- Then STOP immediately, create nothing, and report that the project is complete

**Proceed if at least one source is clear:**

- If `PRD.md` clearly defines the next phase, use it as the primary source of truth and reconcile `state.json` as needed
- If `state.json` clearly indicates the next phase but `PRD.md` is vague or stale, update `PRD.md` during this run so both sources align with the phase being created
- If the two sources conflict, reconcile the mismatch before creating phase artifacts. Do not create a phase from contradictory inputs.

If `.spec_system/CONSIDERATIONS.md` exists, review it for:
- **Active Concerns** that should influence session ordering or scope
- **Lessons Learned** (patterns to follow or avoid)
- **Tool/Library Notes** relevant to this phase

If `.spec_system/SECURITY-COMPLIANCE.md` exists, review it for:
- **Open Findings** that should be addressed in this phase's sessions
- **GDPR Status** that may affect data-handling session scope

**Monorepo Checkpoint** (skip if `monorepo` is already `true` or `false`):
- If the PRD references multiple packages/services but `state.json` has no `packages` array, include this warning in the output summary:
  ```
  Warning: PRD references multiple packages but monorepo is not configured.
  Consider running createprd to detect and configure monorepo settings,
  ```
- This is advisory only -- do not block phase creation

### 2. Resolve Assumptions And Phase Conflicts

Before creating any phase directory or session stub, reconcile PRD phase
definitions and state tracking into one source decision.

**Materiality threshold**:
- Treat an assumption or conflict as material if it changes the next phase
  number, phase name, phase objective, session count, session ordering,
  prerequisites, completed-phase status, package ownership, security scope, or
  whether phasebuild should create anything at all
- Do not record cosmetic wording cleanup, routine status normalization, or
  obvious markdown-table repair as material decisions

For each material working assumption, state:
- The assumption itself
- The PRD, state, existing artifact, consideration, or security evidence
  supporting it
- Why phasebuild can proceed without user arbitration

For each material conflict, state:
- The conflicting sources
- The viable interpretations
- The chosen interpretation
- Why that interpretation is the best-supported one
- Which artifact will be updated to reconcile stale information, if any

Rules for this step:
- Prefer PRD.md for intended phase scope when it clearly defines the next phase
- Prefer state.json for completed-session and completed-phase facts when those
  facts conflict with stale prose
- If state.json indicates a phase that PRD.md does not describe, update PRD.md
  only when surrounding PRD evidence supports that phase; otherwise stop with
  `Next command: none`
- If PRD.md indicates the next phase but state.json is stale, update state.json
  during this run so both sources align
- Record material assumptions and conflict resolutions in the generated phase
  PRD
- Do not create artifacts from contradictory unreconciled inputs

### 3. Create Phase Directory and PRD Markdown

Create directory `.spec_system/PRD/phase_NN/` and markdown `.spec_system/PRD/phase_NN/PRD_phase_NN.md`:

```markdown
# PRD Phase NN: Phase Name

**Status**: Not Started
**Sessions**: N (initial estimate)
**Estimated Duration**: X-Y days

**Progress**: 0/N sessions (0%)

---

## Overview

[Phase description]

---

## Progress Tracker

| Session | Name | Status | Est. Tasks | Validated |
|---------|------|--------|------------|-----------|
| 01 | [Name] | Not Started | ~12-25 | - |
| 02 | [Name] | Not Started | ~12-25 | - |
| 03 | [Name] | Not Started | ~12-25 | - |
| ... | ... | ... | ... | ... |

---

## Completed Sessions

[None yet]

---

## Upcoming Sessions

- Session 01: [Name]

---

## Objectives

1. [Primary objective]
2. [Secondary objective]
3. [Tertiary objective]

---

## Prerequisites

- Phase NN-1 completed (omit for Phase 01)
- [Other prerequisites]

---

## Planning Assumptions And Resolutions

<!-- Omit this section if no material assumptions or conflicts shaped the phase -->

### Working Assumptions

- [Working assumption]: [Supporting evidence and why it is safe to proceed]

### Conflict Resolutions

- [Conflict]: [Chosen interpretation, supporting evidence, and any artifact reconciled]

---

## Technical Considerations

### Architecture
[Architecture notes for this phase]

### Technologies
- [Technology 1]
- [Technology 2]

### Risks
- [Risk 1]: [Mitigation]

### Relevant Considerations
<!-- From CONSIDERATIONS.md - remove section if none apply -->
- [P##] **[Item from Active Concerns]**: How it affects this phase
- [P##] **[Lesson Learned]**: How we're applying it

---

## Success Criteria

Phase complete when:
- [ ] All N sessions completed
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## Dependencies

### Depends On
- Phase NN-1: [Name]

### Enables
- Phase NN+1: [Name]
```

Notes:
- If no material working assumptions or conflicts shaped the phase, omit `Planning Assumptions And Resolutions`
- If only assumptions or only conflicts exist, include only the relevant subsection
- Do not include hard-blocker text in a successful phase PRD

### 4. Create All Session Stubs

For each session, create `session_NN_name.md` (use `snake_case` for name):

.spec_system/PRD/phase_NN/
|-- PRD_phase_NN.md
|-- session_01_name.md
|-- session_02_name.md
\-- ...

```markdown
# Session NN: Session Name

**Session ID**: `phaseNN-sessionNN-name`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

[Clear single objective for this session]

---

## Scope

### In Scope (MVP)
- [Feature 1]
- [Feature 2]

### Out of Scope
- [Deferred item 1]

---

## Prerequisites

- [ ] [Prerequisite 1]

---

## Deliverables

1. [Deliverable 1]
2. [Deliverable 2]

---

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

**Monorepo package annotation** (only when `monorepo: true` in state.json):

Add a `Package:` or `Packages:` line to the stub header, after the Session ID line:
- Single-package session: `**Package**: apps/web`
- Multi-package session: `**Packages**: apps/web, apps/api`
- Cross-cutting or single-repo: omit the line entirely

This annotation is parsed by `analyze-project.sh` to enable `--package` filtering and package-scoped workflows.

**Cross-package guidance**: When a session touches multiple packages, note which package owns the primary deliverables and which are secondary dependencies. Keep cross-package sessions to 2-3 packages maximum -- split if more are needed.

### 5. Update State

Merge into `.spec_system/state.json` (add to existing `phases` object):

```json
{
  "phases": {
    "NN": {
      "name": "Phase Name",
      "description": "Phase description",
      "status": "not_started",
      "session_count": N
    }
  }
}
```

### 6. Update Master PRD

Add the new phase to the Phases table in `.spec_system/PRD/PRD.md`. Also update any stale info (completed phases marked as such, session counts reflecting reality):

```markdown
## Phases

| Phase | Name | Sessions | Status |
|-------|------|----------|--------|
| ... | ... | ... | ... |
| NN | Phase Name | N | Not Started |
```

## Phase Planning Guidelines

### Session Count
- Typical phase: 4-8 sessions
- Small phase: 2-3 sessions
- Large phase: Consider splitting

### Session Sizing
- Each session: 12-25 tasks
- Each session: 2-4 hours
- Single clear objective per session

### Dependency Management
- Sessions within phase can depend on each other
- Early sessions provide foundation
- Later sessions build complexity

## Output

Report:

```
Phase NN Created: Phase Name

Summary:
- Created phase NN with N session stubs
- Phase source: [PRD.md | state.json reconciled with PRD.md]
- Working Assumptions: N recorded
- Conflict Resolutions: N recorded
- Scope: [brief phase objective]

Structure:
- .spec_system/PRD/phase_NN/
  - PRD_phase_NN.md
  - session_01_name.md
  - session_02_name.md
  - session_03_name.md

State Updated:
- Phase added to .spec_system/state.json
- Master PRD updated

Sessions Defined: N

Next command: `plansession`
Reason: phase stubs now exist; plansession must select the next executable session and create spec.md plus tasks.md.
```

If Step 1 determined that neither `PRD.md` nor `state.json` clearly indicates another upcoming phase, report instead:

```
No upcoming phase found in PRD.md or state.json.

Project status: complete

phasebuild did not create any new artifacts.

Summary:
- No upcoming phase exists in PRD.md or state.json
- The staged workflow has no remaining phase to create

Next command: `none`
Reason: the project has no remaining planned phase.
```

Do not recommend `plansession` in that case, because there is no new phase to plan.
