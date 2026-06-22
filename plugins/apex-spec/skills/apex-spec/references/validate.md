# validate

Verify that all session requirements are met before marking the session complete.

This is the fourth command in the Session Workflow stage. Run it after
`creview`. If `validate` passes, the next workflow command is `updateprd`. If
it fails, fix the issues and rerun the correct workflow command.

## Rules

1. **Autonomous execution** - do not ask questions, request approval, or wait for human feedback
2. **PASS requires ALL of**: `code-review.md` exists with `Result: RESOLVED`, 100% tasks complete, all deliverables exist, all files ASCII-encoded with LF endings, all tests passing, all success criteria met, database/schema alignment verified when the session touches the DB layer, no security or GDPR violations, no critical behavioral quality violations (when BQC applies)
3. **Any single failure = overall FAIL** - no partial passes
4. **Script first** - run `analyze-project.sh --json` before any analysis
5. **Evidence required** - every PASS/FAIL/N/A claim in `validation.md` must name the exact command, check, or inspected artifact that produced it
6. Conventions compliance is a spot-check, not exhaustive - flag obvious violations only

### No Deferral Policy

- If a validation check fails and YOU can fix it (encoding issues, missing directories, failing tests with obvious fixes, missing schema artifacts, unapplied migrations), FIX IT and re-validate
- The ONLY valid reason to leave a FAIL unresolved is an external requirement you cannot satisfy from the repository or environment, such as missing credentials, API keys, billing, or sudo access
- "The environment isn't set up" is NOT a valid FAIL -- setting it up IS the task
- If you report a FAIL for something you could have fixed, that is a **critical failure**

### Rationalizations To Reject

- "Tests passed, so validation is done" -> No. Tests are one check; tasks, deliverables, encoding, success criteria, schema, security, GDPR, BQC, and conventions still need evidence.
- "This failure was probably pre-existing" -> No. Prove it with a current comparison against the pre-session commit or fix it.
- "Security review is unnecessary for simple changes" -> No. Apply the scoped checklist to touched session files and record PASS or N/A evidence.
- "The result is obvious, so I can summarize without the command" -> No. Report the exact command or targeted inspection that produced each claim.

### Red Flags

- `validation.md` says PASS but omits command/check evidence for one or more checks.
- Tests or security review are marked PASS based only on `implementation-notes.md`.
- "Pre-existing", "environment issue", or "not relevant" appears without current evidence and scope justification.
- `validation.md` says FAIL while leaving a repo-fixable issue unresolved.

## Steps

### 1. Get Deterministic Project State (REQUIRED FIRST STEP)

Run the analysis script to get reliable state facts. Local scripts (`.spec_system/scripts/`) take precedence over plugin scripts if they exist:

```bash
# Check for local scripts first, fall back to plugin
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

This returns structured JSON including the current session, whether its specs
directory exists, existing session files, monorepo state, packages, and active
package context.

**IMPORTANT**: Use the `current_session` value from this output. If `current_session` is `null`, run plansession yourself to set one up.

### 1a. Determine Package Context (Monorepo Only)

**Skip this step if** `monorepo` is not `true` in the JSON output.

Resolve the active package for this session:

1. **spec.md header**: Read the `Package:` field from the session's spec.md (set during plansession)
2. **active_package from script**: If spec.md has no Package field, use `active_package` from the JSON output

Store the resolved package path for use in Steps 3-5. A `null` package means this is a cross-cutting session.

### 2. Read Session Files

Using the `current_session` value from the script output, read all session documents:
- `.spec_system/specs/[current-session]/spec.md` - Requirements
- `.spec_system/specs/[current-session]/tasks.md` - Task checklist
- `.spec_system/specs/[current-session]/implementation-notes.md` - Progress log
- `.spec_system/specs/[current-session]/code-review.md` - Code review and repair report from `creview`
- `.spec_system/specs/[current-session]/security-compliance.md` - Prior security report (if exists from previous validation run)
- `.spec_system/CONVENTIONS.md` - Project coding conventions (if exists)

**CONVENTIONS.md** is used in the Quality Gates check (section 3.H) to verify code follows project conventions for naming, structure, error handling, testing, etc.

### 3. Run Validation Checks

For every check below, capture evidence before writing `validation.md`:
- Check name
- Exact command run, or exact targeted inspection when no command applies
- Result, output summary, and any fix applied during validation
- Remaining blocker, if any, and why it cannot be resolved autonomously

#### A. Code Review Gate

Verify `code-review.md` exists and has `Result: RESOLVED`:
- Confirm the file is present in the current session directory
- Confirm the result is exactly `RESOLVED`
- Confirm the review scope says all uncommitted changes were reviewed
- If `code-review.md` is missing, `BLOCKED`, or not `RESOLVED`, validation must
  FAIL and the correct handoff is `Next command: creview`

This is a workflow-order gate. It does not change ordinary validation failure
routing: code, task, deliverable, test, schema, security, or behavioral fixes
still hand off to `implement`.

#### B. Task Completion
Verify all tasks in tasks.md are marked `[x]`:
- Count total tasks
- Count completed tasks
- List any incomplete tasks

#### C. Deliverables Check
From spec.md deliverables section:
- Verify each file exists
- Check file is non-empty
- Note any missing files
- **Monorepo**: File paths should be repo-root-relative (e.g., `apps/web/src/auth.ts`). Verify files are within the declared package scope (from Step 1a). Flag any deliverables outside the package boundary.

#### D. ASCII Encoding Check
For each deliverable file:
```bash
# Check encoding
file [filename]  # Should show: ASCII text

# Find non-ASCII characters
LC_ALL=C grep '[^[:print:][:space:]]' [filename]

# Check for CRLF line endings
grep -l $'\r' [filename]
```
- Report any non-ASCII characters found
- Report any CRLF line endings

#### E. Test Verification
Run the project's test suite:
- Record exact command(s) and exit status
- Record total tests
- Record passed/failed
- Calculate coverage if available
- Note any failures
- **Monorepo**: When a package is resolved (Step 1a), run tests scoped to that package first (e.g., `cd apps/web && npm test`, or using workspace commands like `pnpm --filter web test`). Also run repo-root tests if they exist, since cross-package regressions matter.

**CRITICAL -- NO "PRE-EXISTING" EXCUSE**: If ANY test fails, you MUST:
1. Investigate the root cause -- determine whether the session's changes caused or contributed to the failure
2. NEVER dismiss a failure as "pre-existing" or "environment issue" -- if tests passed before this session and fail now, THIS SESSION BROKE THEM
3. FIX the failure before continuing validation. If you changed a Docker image, a dependency, a config file, or any shared code, failures in existing tests are YOUR responsibility
4. Only after all tests pass (0 failures) may you mark Test Verification as PASS
5. If a failure is genuinely unrelated (e.g., flaky network test), you must PROVE it by showing the exact command also fails on the pre-session commit -- do not assume

#### F. Database/Schema Alignment (if relevant)
If the session changes persisted data shape, constraints, indexes, migrations, seeds, or other DB-layer behavior that project conventions track in versioned artifacts:
- Verify the matching schema artifact exists in the session changes (migration, schema file, SQL patch, DDL, ORM metadata update, seed/test fixture update, etc.)
- Verify application code and schema artifacts describe the same tables, columns, constraints, indexes, and generated types
- Run the relevant migration status, schema diff, or apply/validate command to confirm there is no drift and the artifact works locally
- If conventions require reversible migrations, rollback support, or seed updates, verify those are present
- FAIL if implementation expects DB changes that are not represented in project-tracked schema artifacts, or if the artifacts exist but were not verified

If the session includes no DB-layer changes, mark this check N/A with a brief justification.

#### G. Success Criteria
From spec.md success criteria:
- Check each functional requirement
- Verify testing requirements met
- Confirm quality gates passed

#### H. Conventions Compliance (if CONVENTIONS.md exists)
Spot-check deliverables against project conventions:
- **Naming**: Functions, variables, files follow naming conventions
- **Structure**: Files are organized according to file structure conventions
- **Error Handling**: Follows the project's error handling approach
- **Comments**: Explain "why" not "what", no commented-out code
- **Testing**: Tests follow project testing philosophy
- **Database** (if Database Layer conventions exist): Migration naming follows convention, model/table naming matches convention, required columns present on new tables, indexes on foreign keys, and schema artifacts live in the expected location

Note: This is a spot-check, not exhaustive. Flag obvious violations only.

#### I. Security & GDPR Compliance

Use `references/security-compliance-checklist.md` as the reusable checklist for
this section.

Review **only files created or modified in this session** (use deliverables from spec.md and git diff against the pre-session commit). Skip files not touched by this session.

Apply the checklist's:

- Security spot-check categories
- GDPR review categories
- Scope rules and automatic FAIL conditions

This review is mandatory for touched session files. It remains targeted to
session deliverables, not a full codebase audit.

#### J. Behavioral Quality Spot-Check

Determine whether a BQC applies: does this session produce application code?

**If no application code**: Mark as N/A and skip to Step 4.

**If application code**: Read
`references/behavioral-quality-checklist.md`, then select up to 5 deliverable
files most likely to contain behavioral issues (files with side effects,
mutations, external calls, user interaction, or data fetching). Use the shared
priority spot-check categories from that checklist.

**Scoring**:
- 0 violations: PASS
- 1-2 low-severity (e.g., missing retry backoff on non-critical read path): WARN -- log but do not block
- Any high-severity in top priorities: FAIL -- fix before passing

### 4. Generate Security & Compliance Report

Create `security-compliance.md` in the session directory (`.spec_system/specs/[current-session]/security-compliance.md`):

```markdown
# Security & Compliance Report

**Session ID**: `phaseNN-sessionNN-name`
[MONOREPO ONLY - include when monorepo: true]
**Package**: [package-path]
[END MONOREPO ONLY]
**Reviewed**: [YYYY-MM-DD]
**Result**: PASS / FAIL / N/A

## Scope

**Files reviewed** (session deliverables only):
- `path/file1` - [brief description]
- `path/file2` - [brief description]

**Review method**: Static analysis of session deliverables + dependency audit (if applicable)

**Review evidence**:
- Command/check: `[exact command or targeted inspection]`
  - Result: PASS/FAIL/N/A - [specific result]
  - Evidence: [output summary, files inspected, or why N/A applies]

## Security Assessment

### Overall: PASS / FAIL

| Category | Status | Severity | Details |
|----------|--------|----------|---------|
| Injection (SQLi, CMDi, LDAPi) | PASS/FAIL | -- / Critical / High | [details] |
| Hardcoded Secrets | PASS/FAIL | -- / Critical | [details] |
| Sensitive Data Exposure | PASS/FAIL | -- / High / Medium | [details] |
| Insecure Dependencies | PASS/FAIL | -- / High / Medium | [details] |
| Security Misconfiguration | PASS/FAIL | -- / Medium | [details] |

### Security Findings

[List each finding with severity, file:line, description, remediation, and
status; or "No security findings."]

## GDPR Compliance Assessment

### Overall: PASS / FAIL / N/A

*N/A if session introduced no personal data handling.*

**Categories reviewed**: Data Collection & Purpose, Consent Mechanism, Data
Minimization, Right to Erasure, PII in Logs, Third-Party Data Transfers.

### Personal Data Inventory

| Data Element | Source | Storage | Purpose | Retention | Deletion Path |
|-------------|--------|---------|---------|-----------|---------------|
| [e.g., email] | [user input] | [database table] | [authentication] | [until account deletion] | [DELETE /api/user] |

[Or "No personal data collected or processed in this session."]

### GDPR Findings

[List each finding with category, file:line, description, remediation, and
status; or "No GDPR findings."]

## Recommendations

[Actionable items for future sessions, or "None -- session is compliant."]

## Sign-Off

- **Result**: PASS / FAIL / N/A
- **Reviewed by**: AI validation (validate)
- **Date**: [YYYY-MM-DD]
```

### 5. Generate Validation Report

Create `validation.md` in the session directory:

```markdown
# Validation Report
**Session ID**: `phaseNN-sessionNN-name`
[MONOREPO ONLY - include when monorepo: true]
**Package**: [package-path]
[END MONOREPO ONLY]
**Validated**: [YYYY-MM-DD]
**Result**: PASS / FAIL

## Validation Summary

| Check | Status | Notes |
|-------|--------|-------|
| Code Review | PASS/FAIL | `code-review.md` Result: RESOLVED |
| Tasks Complete | PASS/FAIL | X/Y tasks |
| Files Exist | PASS/FAIL | X/Y files |
| ASCII Encoding | PASS/FAIL | [issues] |
| Tests Passing | PASS/FAIL | X/Y tests |
| Database/Schema Alignment | PASS/FAIL/N/A | [issues or "N/A -- no DB-layer changes"] |
| Quality Gates | PASS/FAIL | [issues] |
| Conventions | PASS/SKIP | [issues or "No CONVENTIONS.md"] |
| Security & GDPR | PASS/FAIL/N/A | [issues] |
| Behavioral Quality | PASS/WARN/FAIL/N/A | [issues or "N/A -- no application code"] |

**Overall**: PASS / FAIL

## Evidence Ledger

Every row must name the exact command or targeted inspection used.

| Check | Command or Inspection | Result | Evidence / Blocker |
|-------|-----------------------|--------|--------------------|
| Project state | `bash .../analyze-project.sh --json` | PASS/FAIL | [summary] |
| Code review | `code-review.md` inspection | PASS/FAIL | [Result: RESOLVED or handoff to creview] |
| Task completion | [task checklist inspection] | PASS/FAIL | [X/Y tasks] |
| Deliverables | [file existence/non-empty command or inspection] | PASS/FAIL | [X/Y files] |
| ASCII/LF | `file ...`; `LC_ALL=C grep ...`; `grep ...` | PASS/FAIL | [issues or none] |
| Tests | [exact test command] | PASS/FAIL | [counts, coverage, failures] |
| Database/schema | [exact schema command or inspection] | PASS/FAIL/N/A | [evidence or N/A reason] |
| Success criteria | [spec criteria inspection + commands] | PASS/FAIL | [summary] |
| Conventions | [conventions inspection] | PASS/SKIP | [issues or skip reason] |
| Security/GDPR | [checklist inspection and commands] | PASS/FAIL/N/A | [findings or N/A reason] |
| Behavioral quality | [BQC inspection] | PASS/WARN/FAIL/N/A | [files checked, violations] |

## 1. Code Review Gate

### Status: PASS/FAIL
**Report**: `code-review.md`
**Result**: RESOLVED / BLOCKED / missing / other
**Issues**: [list or "None"]

## 2. Task Completion

### Status: PASS/FAIL
**Tasks**: X/Y complete
**Incomplete tasks**: [list or "None"]

## 3. Deliverables Verification

### Status: PASS/FAIL

| File | Found | Status |
|------|-------|--------|
| `path/file1` | Yes | PASS |
| `path/file2` | Yes | PASS |

**Missing deliverables**: [list or "None"]

## 4. ASCII Encoding Check

### Status: PASS/FAIL

| File | Encoding | Line Endings | Status |
|------|----------|--------------|--------|
| `path/file1` | ASCII | LF | PASS |

**Encoding issues**: [list or "None"]

## 5. Test Results

### Status: PASS/FAIL

| Metric | Value |
|--------|-------|
| Total Tests | N |
| Passed | N |
| Failed | 0 |
| Coverage | X% |

**Failed tests**: [list or "None"]

## 6. Database/Schema Alignment

### Status: PASS/FAIL/N/A

*N/A if the session introduced no DB-layer changes.*

**Evidence**: [schema artifact, code/schema alignment, migration/status/diff
command, seed/rollback checks, or "N/A -- no DB-layer changes"]

**Issues found**: [list or "None"]

## 7. Success Criteria

From spec.md:

**Functional requirements**: [checked list from spec.md]

**Testing requirements**: [checked list from spec.md]

**Quality gates**: [checked list from spec.md]

## 8. Conventions Compliance

### Status: PASS/SKIP

*Skipped if no `.spec_system/CONVENTIONS.md` exists.*

**Categories spot-checked**: naming, file structure, error handling, comments,
testing, and database conventions when relevant.

**Convention violations**: [list or "None" or "Skipped - no CONVENTIONS.md"]

## 9. Security & GDPR Compliance

### Status: PASS/FAIL/N/A

**Full report**: See `security-compliance.md` in this session directory.

#### Summary
| Area | Status | Findings |
|------|--------|----------|
| Security | PASS/FAIL | [count] issues |
| GDPR | PASS/FAIL/N/A | [count] issues |

**Critical violations**: [list critical/high severity items or "None"]

## 10. Behavioral Quality Spot-Check

### Status: PASS/WARN/FAIL/N/A

*N/A if session produced no application code.*

**Checklist applied**: [Yes / N/A]
**Files spot-checked**: [list of up to 5 files]

**Categories spot-checked**: trust boundaries, resource cleanup, mutation
safety, failure paths, and contract alignment.

**Violations found**: [list with file:line, category, severity, or "None"]

**Fixes applied during validation**: [list fixes, or "None"]

## Validation Result

### PASS / FAIL

[Summary of validation outcome]

### Unresolved Failures And Blockers

[List unresolved failures, exact external blocker and why it cannot be resolved
autonomously, or "None"]

## Next Steps

[If PASS]: Next command: `updateprd`
[If FAIL because `code-review.md` is missing, BLOCKED, or not RESOLVED]: Next command: `creview`
[If FAIL otherwise]: Next command: `implement` for code, task, deliverable, test, schema, security, or behavioral fixes; `validate` only when validation was blocked by an external requirement and no implementation change is pending.
```

### 6. Update State

Update `.spec_system/state.json` based on validation result:

- If PASS: keep `current_session` set to the validated session and append a
  `next_session_history` entry with `status: "validated"`.
- If FAIL: append a `next_session_history` entry with
  `status: "validation_failed"`.
- **Monorepo only**: Include `package` in the history entry when Step 1a
  resolved a package. Omit it for single-repo projects or cross-cutting
  sessions.

## Output

Report PASS/FAIL with a summary of each check, including database/schema alignment when relevant.

The output must include:
- `Summary:` with check results and any fixes applied during validation
- `Next command: updateprd` when PASS
- `Next command: creview` when `code-review.md` is missing, BLOCKED, or not RESOLVED
- `Next command: implement` when FAIL requires implementation, task, test, schema, security, or behavioral fixes
- `Next command: validate` only when validation could not complete because of an external requirement and no implementation change is pending
- `Reason:` explaining the handoff

## Next Action

- If PASS: run `updateprd`
- If FAIL because `code-review.md` is missing, BLOCKED, or not RESOLVED: run `creview`
- If FAIL with implementation or artifact issues: run `implement`
- If FAIL because validation itself was externally blocked and no implementation change is pending: rerun `validate` after the external requirement exists
