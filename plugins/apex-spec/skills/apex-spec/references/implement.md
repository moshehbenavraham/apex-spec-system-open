# implement

Execute each task in the session's task list, updating progress as you go.

This is the second command in the Session Workflow stage. Run it after
`plansession` has created `spec.md` and `tasks.md`. When `implement` finishes,
the next workflow command is `creview`.

## Rules

1. **Autonomous execution** - do not ask questions, request approval, or wait for human feedback.
2. **Make NO assumptions.** Before editing, read the relevant code and comments; pattern-match precisely, validate systematically.
3. **Follow `CONVENTIONS.md`.** All code must follow project-specific coding standards.
4. **ASCII-only characters** and Unix LF line endings in all output.
5. **Never lie and implement exactly what's in the spec** -- no lying, no extra features, no refactoring unrelated code.
6. **Update `tasks.md` immediately** after completing each task -- never batch checkbox updates.
7. **Write tests as specified** -- ensure they pass before moving on.
8. **Ensure logging and error handling** -- no silent failures.
9. **Prefer cohesive, moderately sized modules** -- avoid multi-thousand-line god files; if a file grows beyond ~400-600 LOC or multiple responsibilities, schedule a refactor.
10. **Behavioral correctness over speed** - Code must handle edge cases, cleanup, and failure paths before a task is marked done. A checked task with a behavioral bug costs 10x more to find in a later audit.
11. **No schema drift on database work** -- If a task changes persisted data shape or database behavior, implement the matching schema artifact in the same session (migration, schema file, SQL patch, DDL, seed update, etc.) and verify it locally before marking the task complete.
12. **Evidence per task** -- every completed task log entry must name the files changed and include exact verification checks with results.
13. **Product surface discipline for UI work** -- User-facing routes, screens,
    dashboards, games, extensions, and visual components must present the product
    experience, not implementation telemetry. Do not expose debug labels,
    runtime boundaries, seed/frame/input panels, resize readouts, "shell ready",
    readiness badges, data-source status, route ownership notes, or scaffolding
    copy in the primary interface unless the spec explicitly requires a
    developer/admin/debug surface. Put diagnostics in logs, tests, devtools,
    hidden development overlays, or separate developer-only routes.
14. **UI craft floor** -- UI implementation is not just data plumbing. For UI
    work, follow PRD_UX and existing product/design evidence, preserve or improve
    visual hierarchy, responsive behavior, accessibility, and interaction polish,
    and reject generic filler layouts.

### No Deferral Policy

- NEVER mark a task as "pending", "requires X", or "blocked" if the blocker is something YOU can resolve
- If a service needs to be running, START IT (e.g., `docker compose up -d db`)
- If a dependency needs installing, INSTALL IT
- If a directory needs creating, CREATE IT
- "The environment isn't set up" is NOT a blocker -- setting it up IS the task
- The ONLY valid blocker is an external requirement you cannot satisfy from the repository or environment, such as missing credentials, API keys, billing, or sudo access
- If you skip a task that was executable, that is a **critical failure**

### Rationalizations To Reject

- "I can update all checkboxes at the end" -> No. Task status and notes must be updated immediately after each completed task.
- "The change is obvious, so verification can wait for validate" -> No. Record task-level evidence now; `validate` is a later gate, not a substitute for implementation checks.
- "This file looks unrelated, so I do not need to read it" -> No. Read the code, spec, and surrounding context before inferring intent or impact.
- "The test failure is probably pre-existing" -> No. Investigate the current failure and record evidence before deciding whether it blocks this session.

### Red Flags

- A checked task without a matching `implementation-notes.md` task entry.
- A task log entry that says "done" or "verified" without exact commands, checks, or inspected files.
- Files changed outside the task or package scope without a recorded justification.
- Tests, schema verification, or BQC fixes deferred even though the repository provides enough context to run or apply them now.

## Steps

### 1. Get Deterministic Project State (REQUIRED FIRST STEP)

Run the analysis script to get reliable state facts. Local scripts (`.spec_system/scripts/`) take precedence over plugin scripts if they exist:

```bash
# Check for local scripts first, fall back to skill directory
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

This returns structured JSON including:
- `current_session` - The session to implement
- `current_session_dir_exists` - Whether specs directory exists
- `current_session_files` - Files already in the session directory
- `monorepo` - true/false/null from state.json
- `packages` - Array of registered packages (empty if not monorepo)
- `active_package` - Resolved package context (null if not applicable)

**IMPORTANT**: Use the `current_session` value from this output. If `current_session` is `null`, run plansession yourself to set one up.

### 1a. Determine Package Context (Monorepo Only)

**Skip this step if** `monorepo` is not `true` in the JSON output.

Resolve the active package for this session:

1. **spec.md header**: Read the `Package:` field from the session's spec.md (set during plansession)
2. **active_package from script**: If spec.md has no Package field, use `active_package` from the JSON output
3. **Evidence-backed fallback**: If neither resolves a package, infer from task paths and repo layout. If no single package is defensible, treat the session as cross-cutting.

Store the resolved package path for use in Steps 2, 4, and 5. A `null` package means this is a cross-cutting session.

### 2. Verify Environment Prerequisites (REQUIRED)

Run the prerequisite checker to verify the environment is ready. Use the same local-first pattern:

```bash
# Check for local scripts first, fall back to skill directory
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/check-prereqs.sh --json --env
else
  bash scripts/check-prereqs.sh --json --env
fi
```

This verifies:
- `.spec_system/` directory and `state.json` are valid
- `jq` is installed (required for scripts)
- `git` availability (optional)

**Monorepo**: If a package was resolved in Step 1a, add `--package <path>` to verify package-specific prerequisites and workspace tooling:

```bash
# Example: check-prereqs.sh --json --env --package apps/web
```

**If any environment check fails**: FIX the issues yourself. Install missing tools, create missing directories, start required services. Stop only for external requirements you cannot satisfy, such as credentials, API keys, billing, or sudo access; report the exact blocker and set `Next command: implement`.

**Optional - Tool Verification**: After reading spec.md (next step), if the Prerequisites section lists required tools, also run:

```bash
# Check for local scripts first, fall back to skill directory
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/check-prereqs.sh --json --tools "tool1,tool2,tool3"
else
  bash scripts/check-prereqs.sh --json --tools "tool1,tool2,tool3"
fi
```

This catches missing tools BEFORE implementation starts, preventing mid-session failures.

**Optional - Database Prerequisites**: If `.spec_system/CONVENTIONS.md` has a "Database Layer" section, verify:
1. Database service is running (`docker compose ps` or connection test)
2. Migrations are current (no pending migrations)
3. If the session includes DB-layer changes, identify the required schema artifact up front (migration, schema file, SQL patch, seed update, etc.) so it is part of implementation scope, not deferred follow-up work
If checks fail, resolve them (start services, run migrations) before proceeding.

### 3. Read Session Context

Using the `current_session` value from the script output, read:
- `.spec_system/specs/[current-session]/spec.md` - Full specification
- `.spec_system/specs/[current-session]/tasks.md` - Task checklist
- `.spec_system/specs/[current-session]/implementation-notes.md` - Progress log (if exists)
- `.spec_system/specs/[current-session]/security-compliance.md` - Prior security report (if exists from previous validation run)
- `.spec_system/PRD/PRD_UX.md` - UX requirements, design brief, product surface
  boundaries, and anti-patterns when the session changes UI (if present)
- `.spec_system/CONVENTIONS.md` - Project coding conventions (if exists)

**Resuming?** If `implementation-notes.md` and completed tasks already exist, read them to understand current state and resume from the next incomplete task.

### 3a. Load Behavioral Quality Checklist (BQC)

BQC applies when the session produces application code (not pure configuration, documentation, or infrastructure-as-code). If the session is entirely non-code work, skip to Step 4.

Read `references/behavioral-quality-checklist.md` and apply the relevant items
before marking each task complete.

How to apply:

- After each task, check only the items relevant to the code you touched
- Fix violations now rather than logging them for later cleanup
- Record any meaningful BQC-driven fixes in `implementation-notes.md`

### 4. Initialize Implementation Notes

If `implementation-notes.md` doesn't exist, create it:

```markdown
# Implementation Notes

**Session ID**: `phaseNN-sessionNN-name`
[MONOREPO ONLY - include when monorepo: true]
**Package**: [package-path]
[END MONOREPO ONLY]
**Started**: [YYYY-MM-DD HH:MM]
**Last Updated**: [YYYY-MM-DD HH:MM]

---

## Session Progress

| Metric | Value |
|--------|-------|
| Tasks Completed | 0 / N |
| Estimated Remaining | X hours |
| Blockers | 0 |

---

## Task Log

### [YYYY-MM-DD] - Session Start

**Environment verified**:
- [x] Prerequisites confirmed
- [x] Tools available
- [x] Directory structure ready
[IF DATABASE SESSION]
- [x] Database running
- [x] Migrations current
[END IF]

---
```

### 5. Work Through Tasks

For each incomplete task:

#### A. Identify Next Task
Find the first unchecked `- [ ]` task in tasks.md

#### B. Implement Task
- Read the task description carefully
- Read surrounding code to match existing patterns before writing new code
- Follow the spec's technical approach and CONVENTIONS.md standards
- If `docs/adr/` exists, review relevant Architecture Decision Records and follow their decisions
- Implement the required changes
- **Database completion rule**: If this task changes persisted data shape, constraints, indexes, queries that depend on schema, or other DB-layer behavior, add the matching schema artifact now (migration, patch, schema definition, ORM metadata, seed/test updates, etc.), apply or verify it locally, and do not mark the task complete until code and schema are aligned
- **Monorepo path validation**: If a package was resolved in Step 1a, verify that files being created or modified fall within the declared package directory (e.g., `apps/web/...`). Warn if a task references files outside the package scope -- this may indicate scope creep. Exception: cross-cutting sessions (package: null) may touch any file.
- **Behavioral quality verification** (if BQC loaded in Step 3a): Before marking this task complete, scan your code against the applicable checklist items. Fix violations now -- do not defer. Note any BQC fixes in the task log entry (Step 5D).
- **UI product-surface verification**: If the task changes a user-facing
  surface, inspect the rendered route or component at the target viewport before
  marking it complete. Confirm the first viewport is product-focused and does not
  contain implementation diagnostics or generic scaffolding. If diagnostics are
  needed for development, move them to a developer-only route, hidden dev-only
  overlay, logs, tests, or implementation notes.
- **UI craft verification**: For UI tasks, compare the result to PRD_UX,
  existing design patterns, and adjacent product surfaces. Fix generic spacing,
  weak hierarchy, broken responsive behavior, inaccessible controls, or rough
  interaction states before marking the task complete.

#### C. Update Task Status
Before marking the task complete, write the task log entry from Step 5D,
including the `Verification` subsection. Do not check the task off until that
evidence exists.

In `tasks.md`, change:
```markdown
- [ ] T001 [S0101] Task description
```
To:
```markdown
- [x] T001 [S0101] Task description
```

#### D. Log Progress
Add to `.spec_system/specs/[current-session]/implementation-notes.md`:
```markdown
### Task TNNN - [Description]

**Started**: [YYYY-MM-DD HH:MM]
**Completed**: [YYYY-MM-DD HH:MM]
**Duration**: [X] minutes

**Notes**:
- [Implementation details]
- [Decisions made]

**Files Changed**:
- `path/to/file` - [changes made]

**Verification**:
- Command/check: `[exact command or targeted inspection]`
  - Result: PASS/FAIL/N/A - [specific result]
  - Evidence: [test count, diff inspected, output summary, or why no automated check applies]
- UI product-surface check: [PASS/FAIL/N/A] - [route/component inspected,
  viewport, and confirmation that debug/runtime/scaffolding copy is absent from
  the normal product surface]
- UI craft check: [PASS/FAIL/N/A] - [UX PRD/design evidence used, viewports or
  components inspected, and polish issues fixed]

**BQC Fixes** (if any):
- [Category]: [What was caught and fixed] (`path/to/file`)

[MONOREPO ONLY - include if any files fall outside the declared package scope]
**Out-of-Scope Files** (files outside declared package):
- `other-package/path/file` - [justification]
[END MONOREPO ONLY]
```

### 6. Handle Blockers

If you encounter an obstacle, RESOLVE IT YOURSELF before documenting:

- **Service not running?** Start it (e.g., `docker compose up -d db`)
- **Dependency missing?** Install it
- **Directory missing?** Create it
- **Config file missing?** Generate it from the spec
- **Database not running?** Start it (`docker compose up -d [service]`)
- **Migrations pending?** Run migration tool to apply them
- **Schema artifact missing?** Generate or update the required migration, schema file, or SQL patch yourself, then apply or validate it locally
- **Connection refused?** Check `DATABASE_URL` in `.env`, verify port
- **"The environment isn't set up"** is NOT a blocker -- setting it up IS the task

If credentials, API keys, billing, sudo access, or another external requirement
prevents progress, do not ask for it. Preserve completed work, document the
blocker and exact missing requirement in implementation-notes.md, and set
`Next command: implement` so the same command resumes after the requirement
exists. If you skip a task that was executable, that is a **critical failure**.

After resolving, document in implementation-notes.md:
```markdown
## Blockers & Solutions

### Blocker N: [Title]

**Description**: [What was blocking]
**Impact**: [Which tasks affected]
**Resolution**: [How YOU resolved it]
**Time Lost**: [Duration]
```

### 7. Track Design Decisions

When making implementation choices:

```markdown
## Design Decisions

### Decision N: [Title]

**Context**: [Why decision needed]
**Options Considered**:
1. [Option A] - [pros/cons]
2. [Option B] - [pros/cons]

**Chosen**: [Option]
**Rationale**: [Why]
```

### 8. Track Progress and Checkpoint

After each task:
- Update Progress Summary table in tasks.md
- Update implementation-notes.md
- Report status: tasks done (X of Y), next task

**Checkpoint every 3-5 tasks minimum** and before any risky operations. If approaching context limits, document current state and next task in implementation-notes.md.

## Output

When all tasks complete:
```
Session implementation complete!
Tasks: N/N (100%)
BQC: [X] fixes applied across [Y] tasks [or "N/A - no application code in session"]

Summary:
- Completed all implementation tasks for [current-session]
- Task evidence recorded in implementation-notes.md with files changed and verification results
- Tests/checks run: [brief list]
- Remaining blockers: none

Next command: `creview`
Reason: implementation is complete and all uncommitted changes must be reviewed and repaired before validation.
```

If an external blocker remains:

```text
Implementation blocked.

Summary:
- Completed tasks: X/Y
- Blocker: [exact missing external requirement]
- Preserved work in: [files/artifacts]

Next command: `implement`
Reason: implementation must resume after the external requirement exists; validate is not valid until all tasks are complete.
```

## Next Action

After `implement` completes, run `creview`. Do not jump directly from
`implement` to `validate` or `updateprd`.
