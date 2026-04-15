# plansession

Analyze current project state, choose the next executable session, create its specification, and generate the task checklist in one run.

This is the first command in the Session Workflow stage. Run it after `phasebuild`, or after a successful `updateprd` when the current phase still has unfinished sessions. If `plansession` succeeds and creates `spec.md` plus `tasks.md`, the next workflow command is always `implement`. If the current phase is already complete, do not create a new session plan; hand off to `audit`.

## Rules

1. **Script first** - Always run `analyze-project.sh --json` before analysis
2. **Trust the script** - Use JSON output as authoritative state; do not parse `state.json` directly
3. **One session at a time** - Only recommend one session
4. **Respect dependencies** - Do not skip prerequisites
5. **MVP focus** - Recommend core product progress before polish
6. **Scope discipline** - Sessions must be 12-25 tasks and 2-4 hours
7. **Hard limits** - Max 25 tasks, max 4 hours, single clear objective
8. **Do not invent scope** - Derive objectives, deliverables, paths, and tests from PRD, stubs, codebase, and state facts
9. **Incorporate `CONVENTIONS.md`** - Naming, file structure, and testing philosophy must shape the plan
10. **Incorporate `CONSIDERATIONS.md`** - Address active concerns and lessons learned when relevant
11. **ASCII-only characters** and Unix LF line endings in all output
12. **Task sizing** - Aim for about 20-25 minutes per task, with one clear atomic action
13. **Every task must have** - Task ID (`TNNN`), session ref (`[SPPSS]`), action verb, and target file path
14. **Mark `[P]`** only when tasks are truly independent
15. **Sequence by reality** - Dependencies first, then setup, foundation, implementation, and testing
16. **Behavioral quality by design** - When a Behavioral Quality Checklist applies, embed edge-case handling into task descriptions instead of leaving it for `implement` or `validate`
17. **Resolve ambiguity with evidence-backed working assumptions** - Normal ambiguity is not a reason to ask the user
18. **Surface and resolve conflicts** - When inputs disagree, choose the best-supported interpretation and record it when it materially shapes the plan

### No Deferral Policy

- Resolve ambiguity from repo evidence, prior artifacts, and script output before considering user escalation
- Use evidence-backed working assumptions for incomplete but non-blocking inputs
- Distinguish assumptions from true hard blockers; successful artifacts must not contain hard-blocker placeholders
- Stop only when required planning inputs cannot be read or when required plan artifacts cannot be updated because the repo is not yet at the `plansession` stage
- If `.spec_system/`, the active PRD, or the current phase stubs are missing, route to the earlier workflow step instead of inventing plan content
- If the current phase is complete, stop planning and hand off to `audit` instead of creating a new session spec

### Rationalizations To Reject

- "The stub is vague, so a thin placeholder session is fine" -> No. Convert vague intent into concrete repo-derived deliverables or choose a different ready session
- "This session is a little big, but implement can sort it out" -> No. Right-size it now to the 12-25 task contract
- "Package scope is unclear, so I should ask the user before planning" -> No. Resolve it from repo evidence or proceed with a recorded working assumption
- "The dependency is probably satisfied even if not proven" -> No. Missing prerequisite evidence means the prerequisite is not met

### Red Flags

- Multiple objectives or more than 25 tasks in a supposed single session
- Tasks without repo-derived file paths or tasks that are still generic placeholders
- Phase-complete state incorrectly handing off to `phasebuild` instead of `audit`
- Successful artifacts that still contain `TBD`, `ask user`, `blocked`, or equivalent unresolved placeholders

## Steps

### 1. Get Deterministic Project State (REQUIRED FIRST STEP)

Run the analysis script to get reliable state facts. Local scripts (`.spec_system/scripts/`) take precedence over bundled scripts if they exist:

```bash
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

This returns structured JSON with:
- `current_phase` - Current phase number
- `current_session` - Active session or `null`
- `current_session_dir_exists` - Whether the active session directory already exists
- `current_session_files` - Existing markdown files in the active session directory
- `completed_sessions` - Completed session IDs
- `candidate_sessions` - Current-phase session stubs and status; each candidate includes a `package` field parsed from the stub or `null`
- `phases` - All phases with status and session counts
- `monorepo` - `true`, `false`, or `null`
- `packages` - Registered package objects with `name`, `path`, and `stack_hint` when monorepo is enabled
- `active_package` - Package object resolved from `--package` or CWD inference, or `null`
- `monorepo_detection` - Auto-detection result when `monorepo` is `null`

Use this JSON output as ground truth for project state. Do not re-read `state.json` directly.

### 1a. Determine Package Context (Monorepo Only)

Skip this step if `monorepo` is not `true` in the JSON output.

When working in a monorepo, resolve the package context with this priority:

1. User statement naming a package
2. Selected candidate stub `package` field
3. `active_package.path` from the analysis script
4. Repo evidence from PRD language, referenced paths, package layout, and related prior sessions
5. Best-supported working assumption, recorded in `spec.md`, if planning can still proceed safely

Do not ask the user only because a stub omitted package metadata. If no single package is defensible, treat the session as cross-cutting and record `Package: null` in `spec.md`.

### 2. Read Planning Inputs

With state facts established, read these files for planning context:
- `.spec_system/PRD/PRD.md` - Master project requirements
- `.spec_system/PRD/PRD_UX.md` - UX requirements when present and relevant
- Candidate session files from the analysis JSON (`path` field)
- `.spec_system/CONSIDERATIONS.md` - Institutional memory, if present
- `.spec_system/SECURITY-COMPLIANCE.md` - Security posture, if present
- `.spec_system/CONVENTIONS.md` - Project conventions, if present

Focus on:
- Session objectives and boundaries
- Dependencies and ordering
- Active concerns and lessons learned that should shape planning
- Open security findings that affect scope or implementation approach
- Naming, file placement, testing expectations, and DB-layer requirements from `CONVENTIONS.md`

If `CONVENTIONS.md` includes a database-layer section and the planned session touches persisted data shape or migrations, the plan must include the matching schema artifact work and DB verification tasks.

### 3. Resolve Assumptions And Conflicts

Before choosing a session or writing artifacts, explicitly resolve ambiguity.

Surface only the evidence-backed working assumptions that materially shape the plan. For each working assumption, state:
- The assumption itself
- The repo evidence supporting it
- Why planning can proceed without user arbitration

For each material conflict between inputs:
- Name the conflicting sources
- State the viable interpretations
- Choose the best-supported interpretation
- Record why that interpretation wins

Rules for this step:
- Do not invent filler assumptions just to satisfy format
- A working assumption is not a hard blocker
- Hard blockers stop the command only when required planning inputs are inaccessible
- Ambiguity alone is not a blocker
- If a chosen assumption or conflict resolution materially shapes the plan, record it in `spec.md`
- Do not generate successful artifacts that still contain unresolved blocker text

### 4. Analyze Candidates And Select The Next Session

Using deterministic state plus semantic context:

1. If `current_session` is already set and `current_session_files` include both `spec.md` and `tasks.md`, do not select a different session; the active session is already planned and the correct handoff is `implement`
2. If `current_session` is already set but the planning artifacts are incomplete, repair or finish that same session plan instead of switching sessions
3. Identify which candidates have unmet prerequisites from `completed_sessions`
4. Identify which candidates are executable now
5. Evaluate ready candidates by dependency order, MVP value, technical coherence, package fit, and active considerations
6. Choose exactly one session

Selection rules:
- If multiple sessions are ready, choose the one with the clearest dependency pull and best MVP progression
- If a candidate is blocked, explain the missing prerequisite and prefer the earliest executable prerequisite session instead
- If the current phase has no unfinished sessions, do not create `spec.md` or `tasks.md`; the correct handoff is `audit`
- Do not route a phase-complete result to `phasebuild`; `phasebuild` belongs after the Phase Transition workflow

If an active session already has complete planning artifacts, skip Steps 5-8 and proceed to `## Output` and `## Next Action`. If this step results in a created or repaired session plan with `spec.md` and `tasks.md`, the workflow handoff is fixed: `plansession -> implement`.

### 5. Create Session Directory And Specification

Create the session directory:

```text
.spec_system/specs/phaseNN-sessionNN-name/
|-- spec.md
\-- tasks.md
```

Generate `spec.md` with all sections filled in and no unresolved placeholders:

```markdown
# Session Specification

**Session ID**: `phaseNN-sessionNN-name`
**Phase**: NN - Phase Name
**Status**: Not Started
**Created**: [YYYY-MM-DD]
[MONOREPO ONLY - include when monorepo: true]
**Package**: [package-path or null for cross-cutting]
**Package Stack**: [stack_hint or mixed]
[END MONOREPO ONLY]

---

## 1. Session Overview

[2-3 short paragraphs covering what this session delivers, why it is next, and how it advances the phase]

---

## 2. Objectives

1. [Specific, measurable objective]
2. [Specific, measurable objective]
3. [Specific, measurable objective]
4. [Specific, measurable objective]

---

## 3. Prerequisites

### Required Sessions
- [x] `phaseNN-sessionNN-name` - [what it provides]

### Required Tools Or Knowledge
- [tool or knowledge item]

### Environment Requirements
- [environment requirement]

---

## 4. Scope

### In Scope (MVP)
- [PRD requirement in actor/capability form] - [implementation note]
- [PRD requirement in actor/capability form] - [implementation note]

### Out Of Scope (Deferred)
- [PRD requirement] - Reason: [why deferred]

---

## 5. Technical Approach

### Architecture
[Technical approach rooted in existing codebase and conventions]

### Design Patterns
- [Pattern]: [Why it fits]

---

## 6. Deliverables

### Files To Create
| File | Purpose | Est. Lines |
|------|---------|------------|
| `path/to/file` | Description | ~100 |

### Files To Modify
| File | Changes | Est. Lines |
|------|---------|------------|
| `path/to/file` | Description | ~20 |

---

## 7. Success Criteria

### Functional Requirements
- [ ] [Testable requirement]

### Testing Requirements
- [ ] Unit tests written and passing
- [ ] Manual testing completed

### Non-Functional Requirements
- [ ] [Relevant NFR with measurable target]

### Quality Gates
- [ ] All files ASCII-encoded
- [ ] Unix LF line endings
- [ ] Code follows project conventions

---

## 8. Implementation Notes

### Working Assumptions
<!-- Omit subsection if no material working assumptions remain after planning -->
- [Assumption]: [Repo evidence and why it is safe to proceed]

### Conflict Resolutions
<!-- Omit subsection if no material conflicts were resolved -->
- [Conflict]: [Chosen interpretation and evidence]

### Key Considerations
- [Important consideration]

### Potential Challenges
- [Challenge]: [Mitigation]

### Relevant Considerations
<!-- From CONSIDERATIONS.md; omit subsection if none apply -->
- [P##] **[Active Concern]**: [How it changes planning or execution]
- [P##] **[Lesson Learned]**: [How it is applied here]

### Behavioral Quality Focus
<!-- Include when session produces application code; omit otherwise -->
Checklist active: Yes
Top behavioral risks for this session:
- [Risk 1 relevant to this session]
- [Risk 2 relevant to this session]
- [Risk 3 relevant to this session]

---

## 9. Testing Strategy

### Unit Tests
- [What to test]

### Integration Tests
- [What to test]

### Manual Testing
- [Scenario to verify]

### Edge Cases
- [Edge case to handle]

---

## 10. Dependencies

### Other Sessions
- Depends on: [sessions]
- Depended by: [sessions]

---

## Next Steps

Run the `implement` workflow step to begin implementation.
```

Spec-writing rules:
- All deliverables must be repo-derived and specific
- Do not use placeholder paths, generic module names, or non-committal language
- If a monorepo session is intentionally cross-cutting, write `Package: null` instead of omitting the decision
- Do not include hard-blocker placeholders in a successful spec

### 5a. Enrich Task Descriptions With Behavioral Quality

Skip this step if the session produces no application code.

When behavioral quality applies, enrich task descriptions in Step 6 with concrete failure-path and state-handling expectations:

| If task involves... | Append to description... |
|---------------------|--------------------------|
| Scoped lifecycle with async work or subscriptions | "with cleanup on scope exit for all acquired resources" |
| State-mutating action (submit, delete, send, write) | "with duplicate-trigger prevention while in-flight" |
| View or screen that fetches or displays remote data | "with explicit loading, empty, error, and offline states" |
| Handler for external input (endpoint, consumer, deep link, event) | "with schema-validated input and explicit error mapping" |
| Write path (create/update/delete, single or multi-step) | "with idempotency protection, transaction boundaries, and compensation on failure" |
| Call to external system (API, database, third-party service) | "with timeout, retry/backoff, and failure-path handling" |
| Access-controlled resource or action | "with authorization enforced at the boundary closest to the resource" |
| Query or list returning unbounded results | "with bounded pagination, validated filters, and deterministic ordering" |
| Reopenable or revisitable context (dialog, form, screen, connection) | "with state reset or revalidation on re-entry" |
| Permission-gated feature | "with denied/restricted/revoked handling and fallback behavior" |
| Interactive control or element | "with platform-appropriate accessibility labels, focus management, and input support" |
| Optimistic state update | "with scoped rollback on error" |
| Component consuming external contract (API response, event payload) | "with types matching declared contract; exhaustive enum handling" |

These additions are short, but they prevent high-cost bugs from being deferred into later sessions.

### 6. Generate Task Checklist

Create `tasks.md` from the selected spec's deliverables, success criteria, technical approach, and dependencies:

```markdown
# Task Checklist

**Session ID**: `phaseNN-sessionNN-name`
**Total Tasks**: [N]
**Estimated Duration**: [X-Y] hours
**Created**: [YYYY-MM-DD]

---

## Legend

- `[x]` = Completed
- `[ ]` = Pending
- `[P]` = Parallelizable
- `[SNNMM]` = Session reference
- `TNNN` = Task ID

---

## Setup (N tasks)

- [ ] T001 [SPPSS] Verify prerequisites and environment (`path/to/config-or-command`)
- [ ] T002 [SPPSS] Create required directories or baseline files (`path/to/file`)

---

## Foundation (N tasks)

- [ ] T003 [SPPSS] [P] Create core type or interface (`path/to/file`)
- [ ] T004 [SPPSS] [P] Create base module or component (`path/to/file`)
- [ ] T005 [SPPSS] Implement foundational behavior (`path/to/file`)

---

## Implementation (N tasks)

- [ ] T006 [SPPSS] Implement feature slice 1 (`path/to/file`)
- [ ] T007 [SPPSS] Implement feature slice 2 (`path/to/file`)
- [ ] T008 [SPPSS] [P] Add supporting component or module (`path/to/file`)
- [ ] T009 [SPPSS] Wire integration path (`path/to/file`)
- [ ] T010 [SPPSS] Add failure-path handling (`path/to/file`)

---

## Testing (N tasks)

- [ ] T011 [SPPSS] [P] Write unit tests for core behavior (`tests/path`)
- [ ] T012 [SPPSS] [P] Write integration or regression tests (`tests/path`)
- [ ] T013 [SPPSS] Run required automated checks (`path/to/script-or-command`)
- [ ] T014 [SPPSS] Validate ASCII and LF requirements (`path/to/files-or-command`)
- [ ] T015 [SPPSS] Complete manual verification scenarios (`manual-scenarios`)

---

## Completion Checklist

- [ ] All tasks marked `[x]`
- [ ] All tests and checks passing
- [ ] All files ASCII-encoded with LF line endings
- [ ] implementation-notes.md updated
- [ ] Ready for the `validate` workflow step

---

## Next Steps

Run the `implement` workflow step.
```

Task-writing rules:
- Keep the session within 12-25 tasks total
- Every task must reference concrete repo paths, commands, or deliverables
- Generic filler such as "continue implementation" or "do testing" is not acceptable
- Parallelize only when tasks do not depend on each other

### Path Scoping Rules (Monorepo Only)

When `monorepo: true`, all task paths must be repo-root-relative:
- Single-package sessions: every task path starts with the package prefix
- Cross-cutting sessions: group tasks by package using subheadings inside each category when helpful

### 7. Update State

Update `.spec_system/state.json`:

```json
{
  "current_session": "phaseNN-sessionNN-name",
  "next_session_history": [
    {
      "date": "YYYY-MM-DD",
      "session": "phaseNN-sessionNN-name",
      "status": "planned"
    }
  ]
}
```

Update rules:
- Set `current_session` to the selected session ID
- Add one `next_session_history` entry with status `planned`
- When monorepo package context resolves to a concrete package path, include `package`
- Omit `package` for single-repo projects or `Package: null` cross-cutting sessions
- If rerunning `plansession` for an already planned active session, do not add a duplicate history entry

### 8. Archive Stale Specs

Keep `.spec_system/specs/` lean. Retain only specs from the current phase and one phase back. Move anything older to `.spec_system/archive/sessions/`.

Example: if the current phase is 3, keep Phase 2 and Phase 3 specs and archive Phase 0 and Phase 1 specs.

## Output

If `spec.md` and `tasks.md` were created or repaired, summarize:
- Recommended session name and why it is next
- Key deliverables
- Working assumptions that materially shaped the plan
- Any conflict resolutions that materially changed interpretation
- Total task count and category breakdown
- Estimated duration
- Key parallelization opportunities

If no new session was created because the active session is already planned, summarize:
- The active session ID
- That `spec.md` and `tasks.md` already exist
- That the correct next workflow command is `implement`

If no new session was created because the phase is complete, summarize:
- That the current phase is complete
- Why no new session plan was created
- That the correct next workflow command is `audit`

## Next Action

- After a successful `plansession` run that creates or repairs `spec.md` and `tasks.md`, run `implement`
- If an active session is already planned, run `implement`
- If the phase is complete, run `audit`
- If a true hard blocker prevented planning, report the blocker clearly and stop
