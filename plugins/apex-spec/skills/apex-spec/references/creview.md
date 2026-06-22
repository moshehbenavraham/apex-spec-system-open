# creview

Review every uncommitted change in the working tree, then repair every issue
you find.

This is the third command in the Session Workflow stage. Run it after
`implement` has marked all tasks complete. When `creview` finishes, the next
workflow command is `validate`.

`creview` reviews ALL uncommitted changes in the repository -- not only the
current session's deliverables. This is deliberate: it is the safety net that
catches anything that slipped past `implement`, manual edits made outside the
workflow, drift, and cross-file side effects. Work autonomously through every
step; never stop for human input.

## Rules

1. **Autonomous execution** - do not ask questions, request approval, or wait
   for human feedback. There is no human in the loop.
2. **Review ALL uncommitted changes** - the complete uncommitted working tree is
   your review surface, not just session files.
3. **ASCII-only characters** and Unix LF line endings in all output.
4. **Follow `CONVENTIONS.md`** - findings and fixes must match local
   conventions, not generic preferences.
5. **Minimal, surgical fixes** - address the root cause, not the symptom; do not
   refactor unrelated code.
6. **Stay within the uncommitted scope** - do not search for unrelated defects
   in code that is already committed and unchanged. Read committed code for
   context, and modify it only when required to fix a defect introduced by the
   uncommitted work; record that rationale in `code-review.md`.
7. **Test every fix** - add or update a test for every bug you fix; ensure it
   passes.
8. **Preserve intended behavior** - per `spec.md`; record any fix that changes
   observable behavior in `code-review.md`.
9. **Resolve ambiguity with evidence** - when a finding is genuinely ambiguous,
   choose the safest evidence-backed option, record the assumption and rationale
   in `code-review.md`, and continue. Never leave a finding unresolved pending a
   human decision.

### No Deferral Policy

- Fix every finding you can resolve from the repository or environment. "The
  environment isn't set up" is not a blocker -- setting it up is part of the
  task.
- The only valid blocker is an external requirement you cannot satisfy
  (credentials, API keys, billing, sudo access). Preserve all work, record the
  exact blocker in `code-review.md`, and set `Next command: creview` so the same
  command resumes.
- Leaving a repo-fixable finding unfixed is a critical failure.

### Rationalizations To Reject

- "This change is unrelated to the session, so I can skip it" -> No. ALL
  uncommitted changes are in scope, including manual edits.
- "This finding is ambiguous, so I'll leave it for a human" -> No. There is no
  human in the loop. Record an evidence-backed assumption and fix it, or
  deliberately leave behavior unchanged with a logged rationale.
- "Tests can wait for validate" -> No. Add a test for every bug fixed now.
- "It looks fine, so I don't need to read the surrounding code" -> No. Read
  context before judging or editing.

### Red Flags

- A finding recorded in `code-review.md` with no corresponding fix or logged
  rationale.
- A fix without an added or updated test.
- Edits to already-committed, unchanged code beyond what a finding required.
- A "QUESTION" or "needs decision" item left for a human (this command has no
  such outcome).

## Steps

### 1. Get Deterministic Project State (REQUIRED FIRST STEP)

Run the analysis script for context. Local scripts take precedence over plugin
scripts if they exist:

```bash
# Check for local scripts first, fall back to skill directory
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

Use the `current_session` value to locate session context (`spec.md`,
`tasks.md`, `implementation-notes.md`). If `monorepo` is `true`, note the active
package for convention context, but remember the review surface is still the
entire uncommitted tree.

### 2. Establish Scope (ALL uncommitted changes)

Build a complete inventory of everything that differs from the last commit:

```bash
git status                                  # staged, unstaged, untracked
git diff HEAD                               # all modifications to tracked files
git diff --cached                           # staged changes
git ls-files --others --exclude-standard    # untracked files
```

Inventory every untracked file. Read untracked text files fully. For binary or
generated files, record metadata, provenance, and why byte-level inspection is
or is not needed. This inventory is your entire review surface. Do not search
already committed and unchanged code for unrelated defects; modify unchanged
files only when required to fix an issue introduced by the uncommitted work, and
record the rationale.

Read the source-of-truth context first: `.spec_system/CONVENTIONS.md`,
`.spec_system/CONSIDERATIONS.md`, and the session `spec.md`, `tasks.md`, and
`implementation-notes.md`. Map each changed area back to the task it implements,
and explicitly check for tasks that appear started-but-incomplete or missing
entirely.

### 3. Learn Local Conventions

Before judging anything, learn how this codebase does things: naming,
error-handling patterns, logging, test style, and any linter/formatter/
type-checker config (for example .eslintrc, ruff.toml, tsconfig,
pyproject.toml, .editorconfig). Findings must match local conventions.

### 4. Review Every Changed Hunk

For each issue, record file:line, severity (Critical / High / Medium / Low), and
reasoning. Review across these categories:

- **Correctness** - logic errors, off-by-one, wrong conditionals, bad API usage,
  race conditions
- **Spec adherence** - missing, misinterpreted, or incomplete requirements
- **Security** - injection, unsanitized input, secrets in code, auth/authz gaps,
  path traversal, missing validation at trust boundaries
- **Error handling** - swallowed exceptions, missing error paths, resource or
  connection leaks, missing cleanup
- **Edge cases** - empty/null/undefined, boundaries, concurrency, large or
  unexpected inputs
- **Data integrity** - transactions, partial writes, idempotency, migration
  safety
- **Tests** - is the new behavior actually tested with meaningful assertions?
  missing cases?
- **Dead code and leftovers** - debug prints, commented-out blocks, unused
  imports, stray scaffolding
- **Product surface discipline** - user-facing UI polluted with debug panels,
  runtime telemetry, readiness badges, route ownership notes, seed/frame/input
  readouts, resize readouts, package/version labels, or scaffolding copy that
  belongs in logs, tests, devtools, hidden dev overlays, or separate debug/admin
  routes
- **Consistency and readability** - naming, duplication, unclear logic,
  convention violations
- **Performance** - N+1s, needless work in loops, blocking calls on hot paths
  (only where it matters)

Use `references/behavioral-quality-checklist.md` for the behavioral categories
and `references/security-compliance-checklist.md` for the security category as
the reusable checklists.

### 5. Write the Findings Report

Create `code-review.md` in the session directory
(`.spec_system/specs/[current-session]/code-review.md`):

```markdown
# Code Review and Repair Report

**Session ID**: `phaseNN-sessionNN-name`
[MONOREPO ONLY - include when monorepo: true]
**Package**: [package-path]
[END MONOREPO ONLY]
**Reviewed**: [YYYY-MM-DD]
**Scope**: All uncommitted changes in the working tree
**Result**: RESOLVED / BLOCKED

## Review Surface

**Files reviewed** (all uncommitted changes):
- `path/file1` - [tracked-modified / staged / untracked]
- `path/file2` - [...]

**Inventory commands**: `git status`, `git diff HEAD`, `git diff --cached`,
`git ls-files --others --exclude-standard`

## Findings by Severity

### Critical
- `path/file:line` - [description] | Fix: [what was done] | Status: FIXED

### High
- [...]

### Medium
- [...]

### Low
- [...]

[Or "No findings."]

## Assumptions and Deliberate Non-Fixes

[For ambiguous findings: the assumption made, the supporting evidence, and the
fix applied -- or the rationale for leaving behavior unchanged. Or "None."]

## Behavior Changes

[Any fix that changes observable behavior, with rationale, or "None."]

## Verification

- Tests: `[command]` - PASS/FAIL/N/A - [counts or evidence]
- Linter: `[command]` - PASS/FAIL/N/A
- Formatter: `[command]` - PASS/FAIL/N/A
- Type checker: `[command]` - PASS/FAIL/N/A
- Final diff re-read: [no remaining issues / notes]

## Summary

1. What was reviewed (file count, rough scope)
2. Findings by severity and how each was resolved
3. Anything deliberately not fixed, and why (evidence-backed)
4. Verification results (tests / lint / types)
```

### 6. Fix Every Finding

- Fix ALL findings within the uncommitted scope.
- Make minimal, surgical edits that address the root cause, not the symptom.
- Preserve intended behavior per the spec; note any fix that changes observable
  behavior in `code-review.md`.
- Add or update a test for every bug you fix.
- For ambiguous findings, apply the safest evidence-backed fix (or deliberately
  leave behavior unchanged) and record the assumption in `code-review.md`. Never
  defer to a human.

### 7. Verify

- Run the full relevant test suite available in the repo -- all applicable tests
  must pass. If no test command exists, record the evidence for N/A.
- Run the linter, formatter, and type checker when configured -- resolve all
  applicable errors, or record evidence for N/A when a check is not configured.
- Re-read the full uncommitted diff one final time: no new issues, no debug
  artifacts left behind.
- Find the right commands in package.json scripts, Makefile, CI config,
  pyproject.toml, or equivalent.

### 8. Update the Report and Hand Off

Update `code-review.md` with the resolution status for every finding and the
verification results, then produce the handoff.

## Output

When all findings are resolved:

```text
Code review and repair complete.

Summary:
- Reviewed all uncommitted changes ([N] files)
- Findings: [C critical, H high, M medium, L low]; all resolved
- Tests/checks run: [brief list]
- Remaining blockers: none

Next command: `validate`
Reason: all uncommitted changes have been reviewed and repaired; the session is
ready for the validation gate.
```

If an external blocker remains:

```text
Code review blocked.

Summary:
- Reviewed: [N] files; fixed [X] findings
- Blocker: [exact missing external requirement]
- Preserved work in: code-review.md and the working tree

Next command: `creview`
Reason: review and repair must resume after the external requirement exists;
validate is not valid until findings are resolved.
```

## Next Action

After `creview` completes, run `validate`. Do not jump directly from
`implement` to `validate`; `creview` runs in between.
