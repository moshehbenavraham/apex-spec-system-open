# Plan: Add `creview` (Code Review and Repair) Step to the Staged Workflow

## Goal

Insert a new staged workflow command, `creview` (short for "code review and
repair"), between `implement` and `validate` in Stage 2 (Session Workflow).

After this change:

- Stage 2 becomes: `plansession -> implement -> creview -> validate -> updateprd`
- Command counts change from **13 staged / 23 total** to **14 staged / 24 total**
  (utility command count stays at 10).

The command behavior originated as a rough draft (formerly
`docs/ongoing-projects/prompt.md`). That draft has been corrected to house style
and folded into this plan -- see **Appendix A** for the complete literal content
to create as `references/creview.md`. The standalone draft is no longer needed.

---

## What `creview` Does (Scope and Role)

`creview` performs a thorough review of **ALL uncommitted changes in the working
tree** and then repairs every issue it finds. It runs after `implement` has
marked all tasks complete and before `validate` acts as the pass/fail gate.

Reviewing the entire uncommitted surface (not just the session's deliverables)
is the whole point of the command: it is the safety net that catches anything
that slipped past `implement`, manual edits made outside the workflow, drift, and
cross-file side effects. This scope is **non-negotiable** and matches the
original `prompt.md` draft ("ALL uncommitted work in this repository").

- **Input / review surface:** every uncommitted change in the repo --
  - `git status` (staged, unstaged, and untracked files)
  - `git diff HEAD` (all modifications to tracked files)
  - `git diff --cached` (staged changes)
  - `git ls-files --others --exclude-standard` (untracked files; inventory all,
    read text files fully, and record binary/generated files by metadata)

  Context is also read for intent: `spec.md`, `tasks.md`,
  `implementation-notes.md`, `CONVENTIONS.md`, `CONSIDERATIONS.md`. Already
  committed, unchanged code is read for context; modify it only when required to
  fix a defect introduced by the uncommitted work, and record the rationale.
- **Output artifact:** `code-review.md` in the session directory
  (`.spec_system/specs/[current-session]/code-review.md`) -- a findings report
  grouped by severity, plus a record of what was fixed.
- **Side effect:** surgical fixes applied to the uncommitted code, with tests
  added or updated for every bug fixed.

### Why it is distinct from `validate`

`validate` is a **read-mostly gate** that produces `validation.md` and a PASS/FAIL
verdict, scoped to the session's deliverables. `creview` is an **active
remediation pass** that finds and fixes correctness, security, spec-adherence,
and quality defects across the **entire uncommitted working tree** before
validation runs. Keeping them separate preserves `validate` as the objective gate
and prevents `creview` from masking failures it could not fix.

`creview` is also distinct from the existing utility-adjacent tools:

- It reviews **all uncommitted changes in the repo** (a broader net than
  `validate`'s session-scoped check), so it catches manual edits and out-of-band
  changes the staged loop would otherwise miss.
- It is part of the **required staged loop**, not an out-of-band utility.

---

## Design Decisions (resolved)

These shape the content of the new reference file and a few handoff edits.
No open decision points remain.

1. **Autonomy reconciliation (RESOLVED -- no human in the loop).** The draft
   prompt tells the reviewer to flag ambiguous findings as `QUESTION` and "leave
   them unfixed" for a human to decide. This **contradicts** the Autonomous
   Command Contract in `SKILL.md` ("Commands must not ask questions ... choose
   the safest evidence-backed default, record the assumption, and continue") and
   the system-wide assumption that there is no human in the loop.
   - **Decision:** Remove the human-decision gate entirely. There is no
     `QUESTION` outcome and no "needs my decision" / "open questions" reporting.
     Any draft language implying human review, approval, or sign-off is a defect
     to delete -- not an option to preserve.
   - For genuinely ambiguous findings, `creview` records an evidence-backed
     assumption in `code-review.md`, applies the safest fix (or deliberately
     leaves the behavior unchanged with a logged rationale), and proceeds. It
     never stops for input.
   - This correction is already applied in the Appendix A draft: the original
     draft's "EXCEPT for any finding that is genuinely ambiguous ... Flag those
     as QUESTION and leave them unfixed" and "Open QUESTIONS needing my decision"
     are gone, replaced with an "Assumptions and deliberate non-fixes"
     subsection that records the assumption and rationale, then
     continues.

2. **Handoff on completion.** `creview` ends with `Next command: validate`.

3. **Handoff when blocked.** If an external requirement (credentials, sudo,
   billing) prevents a fix, preserve work, log the blocker, and set
   `Next command: creview` so the same command resumes (mirrors `implement`).

4. **`validate` FAIL routing -- keep implementation failures pointed at
   `implement`, add a workflow-order exception for `creview`.** Today
   `validate` FAIL routes to `implement`. Keep that for code, task,
   deliverable, test, schema, security, or behavioral fixes. Add one explicit
   exception: if `validate` finds that `code-review.md` is missing, BLOCKED, or
   not RESOLVED, it must set `Next command: creview`. This prevents accidental
   bypass of the new required step without routing ordinary validation failures
   into an implement/creview/validate ping-pong loop.

5. **Reuse existing checklists.** `references/creview.md` should reference
   `references/behavioral-quality-checklist.md` and
   `references/security-compliance-checklist.md` rather than restating their
   contents, matching how `implement.md` and `validate.md` reuse them.

6. **Version bump scheme.** Adding a workflow command is a feature.
   **Decision:** `2.0.29-codex -> 2.1.0-codex` (minor bump).

---

## File-by-File Change Checklist

Edit canonical/root files first, then run the payload sync (Section G last).

### A. New file: `references/creview.md`

Author a new reference following the house pattern (no YAML frontmatter; first
line is a level-1 `# creview` heading; ASCII-only; LF endings; platform-neutral
language; autonomous; ends with `Summary:` / `Next command:` / `Reason:`).

The complete literal file content to create is in **Appendix A** at the end of
this plan (the corrected, folded-in version of the former `prompt.md` draft). It
is structured as:

- **Intro line:** position it as the third Session Workflow command, run after
  `implement`, handing off to `validate`.
- **Rules:** autonomous execution; ASCII/LF; **review ALL uncommitted changes in
  the working tree** (the full review surface -- not just session deliverables);
  minimal surgical fixes addressing root cause; add/update a test for every bug
  fixed; **no human in the loop** -- no `QUESTION` gate, no approval/review stop,
  no "needs my decision" output (per Decision 1). Ambiguity is resolved with
  evidence-backed assumptions recorded in `code-review.md`. Do not search for
  unrelated defects in already committed, unchanged code; modify unchanged files
  only when required to fix an issue introduced by the uncommitted work, and log
  the rationale.
- **Steps:**
  1. Get deterministic project state (`analyze-project.sh --json`, local-first),
     resolve `current_session` and monorepo package context (mirror the
     `implement.md` / `validate.md` Step 1 / 1a blocks).
  2. Build the complete review surface from ALL uncommitted changes:
     `git status`, `git diff HEAD`, `git diff --cached`, and
     `git ls-files --others --exclude-standard`. Inventory every untracked file;
     read untracked text files fully and record binary/generated files by
     metadata. This entire set is the review surface, not just session files.
  3. Learn local conventions (`CONVENTIONS.md`, linter/formatter/type config).
  4. Review every changed hunk across the draft's categories (correctness,
     spec adherence, security, error handling, edge cases, data integrity,
     tests, dead code, consistency, performance).
  5. Write `code-review.md` (findings grouped by severity with file:line), plus
     an "Assumptions and deliberate non-fixes" subsection for anything ambiguous
     (record the assumption and rationale -- never a human-facing question).
  6. Fix all findings; add/update tests.
  7. Verify (run applicable tests, linter, formatter, type checker; record
     evidence-backed N/A for unavailable checks; re-read own diff).
  8. Final summary -- no "open questions" / "needs decision" section.
- **No Deferral Policy / Rationalizations / Red Flags:** mirror the style in
  `implement.md` and `validate.md`.
- **Output block:** `code-review.md` template + the `Next command: validate`
  success handoff and the `Next command: creview` blocked handoff.

### B. Canonical skill files

- [ ] `SKILL.md`
  - Line ~52: "23 commands total: 13 staged workflow commands" -> "24 commands
    total: 14 staged workflow commands".
  - Line ~80 heading "## The 13-Command Workflow" -> "## The 14-Command
    Workflow".
  - Stage 2 ASCII diagram (~101-115): insert `creview` between `implement` and
    `validate`.
  - Line ~117 note ("the next workflow command is always `implement`") is about
    `plansession`; no change. Add/adjust note that after `implement` the next
    command is `creview`, and after `creview` it is `validate`.
  - Stage 2 dispatch table (~186-193): add a `creview` row
    (keywords: "code review", "creview", "review and repair";
    file: `references/creview.md`).
  - Line ~220: "Total: 23 command references: 13 staged ..." -> "24 ... 14
    staged ...".
  - Directory Structure session listing (~239-244): add `code-review.md`
    alongside `validation.md`.
  - Staged Workflow Quick Reference table (~320-334): add `creview` row
    (Input: all uncommitted changes; Output: code-review.md).
  - Frontmatter `description` keywords (~3-13): optionally add "code review",
    "creview" for discoverability.

- [ ] `references/workflow-overview.md`
  - Line ~3: "13-command staged workflow" -> "14-command staged workflow".
  - Stage 2 table (~50-57): add `creview` step row; renumber steps.
  - "after a successful `plansession`" note stays; add note that `implement`
    hands to `creview`, `creview` hands to `validate`.
  - Workflow Diagram (~88-110): add `creview` under `implement` in the Stage 2
    column.
  - Staged Workflow Command Quick Reference table (~140-156): add `creview`
    row; change `implement` "Normal next command" from `validate` to `creview`;
    `creview` next command = `validate`.

- [ ] `references/implement.md`
  - Line ~6-7: "the next workflow command is `validate`" -> "`creview`".
  - Output success block (~330-331): `Next command: validate` ->
    `Next command: creview`; update the Reason text.
  - "Next Action" section (~348-351): "After `implement` completes, run
    `validate`" -> "run `creview`"; update the "Do not jump directly" sentence.

- [ ] `references/plansession.md`
  - Completion Checklist template (~412-417): replace "Ready for the `validate`
    workflow step" with wording that points to the staged flow, e.g. "Ready for
    `implement` to start the implement -> creview -> validate sequence."

- [ ] `references/validate.md`
  - Line ~5: "This is the third command ... Run it after `implement`." ->
    "This is the fourth command ... Run it after `creview`."
  - Step 2 "Read Session Files": include `code-review.md` as a required prior
    artifact, not optional context.
  - Add a validation check that `code-review.md` exists and has `Result:
    RESOLVED`; if it is missing, BLOCKED, or not RESOLVED, the correct handoff is
    `Next command: creview`.
  - Keep all implementation, task, deliverable, test, schema, security, or
    behavioral FAIL routing pointed at `implement` (Decision 4).

- [ ] `references/guidance.md`
  - Line ~80 diagram: `plansession -> implement -> creview -> validate ->
    updateprd`.
  - Line ~83 note: add that `implement` hands to `creview`, then `validate`.
  - Artifacts list (~89-94): add `code-review.md` (code review and repair log).
  - Command Cheat Sheet (~294): add a `creview` row between "Implement tasks"
    and "Verify completion".

- [ ] `references/utilities.md`
  - Line ~8: replace "plan-implement-validate cycle" with "staged session
    workflow" or the full `plansession -> implement -> creview -> validate ->
    updateprd` loop.

- [ ] `references/walkthrough.md`
  - Insert a new "Step: creview" between current Step 5 (implement) and Step 6
    (validate); renumber subsequent steps.
  - Diagrams at ~287 and ~477: add `creview`.
  - Monorepo section (~455-457): note `creview` uses the declared package for
    context, but still reviews and repairs the full uncommitted working tree
    before `validate`.
  - Session tree comment (~123): add `code-review.md` to the
    "created by creview" note.

### C. Root and project instruction files

- [ ] `README.md`
  - Quick Start block (~46-50): add `$apex-spec creview` between `implement` and
    `validate`.
  - Choosing a Starting Command (~64-65): add a bullet for creview
    ("Implementation is done and the new code needs review/repair: use
    `creview`") and adjust the `validate` bullet ("review is done ...").
  - Line ~132: "23 commands total: 13 staged" -> "24 ... 14 staged".
  - Heading ~145 "## The 13-Command Workflow" -> "## The 14-Command Workflow".
  - Stage 2 block (~162-167): add `creview` line.
  - Line ~252 Features bullet: "23 Commands Total: 13 staged ..." -> "24 ... 14
    staged ...".
  - Line ~271: "13-command staged workflow overview" -> "14-command ...".

- [ ] `AGENTS.md`
  - Lines ~26-27: "23-command surface: a 13-command staged workflow ... plus 10
    utility commands" -> "24-command surface: a 14-command staged workflow ...".
  - Routing Fallback Stage 2 bullets (~89-92): add a creview bullet between the
    `implement` and `validate` lines.
  - Version line (~10) -> new version (Section F).

- [ ] `CLAUDE.md`
  - Project Context paragraph: "23-command surface: a 13-command staged
    workflow ... plus 10 utility commands" -> "24-command ... 14-command ...".
  - Routing Fallback Stage 2: add a creview bullet after the `implement` line.
  - Version line ("Current version: 2.0.29-codex") -> new version.

### D. Developer docs

- [ ] `docs/ARCHITECTURE.md`
  - Lines ~5-6: "23-command skill surface ... 13 staged workflow commands" ->
    "24-command ... 14 staged ...".
  - Line ~29 tree comment: "(17 more commands) # 23 total: 13 workflow, 10
    utility" -> "(18 more commands) # 24 total: 14 workflow, 10 utility"
    (or add an explicit `creview.md` line and keep the arithmetic consistent).
  - Line ~52: "dispatch table (23 entries: 13 workflow, 10 utility)" ->
    "(24 entries: 14 workflow, 10 utility)".
  - Options/Rationale text that says "23 separate skills" should become
    "24 separate skills".
  - Apex Infinite CLI test suite comments/tables that say "54 tests" should be
    updated after the CLI tests are changed (expected: 56 tests if only
    `creview` is added to the parametrized command lists).

- [ ] `docs/adr/0001-skill-family-with-shared-references.md`
  - Update every current command-count reference in the ADR: "23 commands
    total", "all 23 command", "23 separate skill directories", and "23 entries"
    -> the corresponding 24-command wording, with staged count 14 and utility
    count 10 where applicable.
  - Add a short new ADR (e.g. `docs/adr/0002-creview-step.md`) recording why a
    dedicated review/repair step was inserted between `implement` and
    `validate`.

- [ ] `docs/onboarding.md`
  - Line ~37 flow: `... plansession -> implement -> creview -> validate ->
    updateprd`.

- [ ] `docs/CONVENTIONS.md`
  - Line ~125 end-to-end test flow: `initspec -> plansession -> implement ->
    creview -> validate`.

- [ ] `docs/development.md`
  - Apex Infinite CLI Testing section (~137): "all 13 known commands" ->
    "all 14 known commands".
  - CI Release Verification section (~152): align the file-inventory sentence
    with `.github/workflows/release.yml` ("at least 23 reference files") unless
    the workflow threshold itself is intentionally changed.

- [ ] `docs/apex-infinite-cli/prompt-contract.md`
  - Known Command Set section (~17): "13 Apex Spec workflow commands" ->
    "14 Apex Spec workflow commands"; add `creview` between `implement` and
    `validate`.
  - Allowed Output Classes examples can keep `validate`, but add `creview` if
    you want the review/repair handoff to be explicit.

- [ ] `apex-infinite-cli/README-apex-infinite-cli.md`
  - "Decide" example (~32): include `creview` in the command examples or make
    the list less exhaustive.
  - Supported Commands table (~48): add `creview` to the Session workflow row.
  - Testing section (~162-170): update total/test-class counts after running
    pytest (expected: 56 total, `TestBuildCodexPrompt` 33).

- [ ] `CHANGELOG.md`
  - Add a new version entry (date 2026-06-22 or release date) under the new
    version number with an `### Added` note: "creview (code review and repair)
    staged workflow command between implement and validate" and `### Changed`
    notes for the count updates and CLI command list.

### E. apex-infinite-cli (Python CLI + tests)

- [ ] `apex-infinite-cli/apex_infinite.py`
  - `KNOWN_COMMANDS` set (~34-48): add `"creview"`.
  - `MANAGER_SYSTEM_PROMPT`: in the implement block (~159-177) change
    `Next: validate` -> `Next: creview`; insert a new `creview` command-reference
    block (purpose, steps, `Next: validate`) before the `validate` block
    (~180).
  - Quick Reference table (~361-372): add a `creview` row.

- [ ] `apex-infinite-cli/tests/test_prompts.py`
  - `WORKFLOW_COMMANDS` list (~196-208): add `"creview"`. (The
    `test_known_commands_coverage` test at ~254-256 asserts the test lists equal
    `KNOWN_COMMANDS`, so this keeps it green.)
  - `slash_cmds` regex (~69): add `creview` to the alternation.
  - Run `pytest` in `apex-infinite-cli/` to confirm all parametrized tests pass.

  Note: the CLI has its own version (separate from the skill version); no CLI
  version bump is required for this change.

- [ ] `tests/reference-autonomy.bats`
  - Add `references/creview.md` to the `COMMAND_REFERENCES` array so the Bats
    handoff regression covers the new staged command.
  - Run `bats tests/` to confirm root-level tests pass.

### F. Version bump (canonical locations + CLAUDE.md + plugin longDescription)

Per `CLAUDE.md` / `AGENTS.md`, update the version in all of:

- [ ] `README.md`
- [ ] `SKILL.md` (frontmatter `version:` field)
- [ ] `AGENTS.md`
- [ ] `plugins/apex-spec/.codex-plugin/plugin.json` (`version` field)
- [ ] `plugins/apex-spec/skills/apex-spec/SKILL.md` (generated -- updated by the
      sync script, not by hand)
- [ ] `CLAUDE.md` ("Current version" line -- also a version location in
      practice even though the canonical list omits it)

Also update `plugins/apex-spec/.codex-plugin/plugin.json` line ~23
`longDescription`: "packages a 23-command specification-driven workflow" ->
"24-command". (plugin.json is **not** part of the payload sync, so this must be
hand-edited.)

### G. Regenerate the plugin payload (run last)

After all canonical edits (`SKILL.md`, `references/`, `scripts/`,
`agents/openai.yaml`) are done:

```bash
bash scripts/sync-plugin-payload.sh
```

This copies the new `references/creview.md` and the updated `SKILL.md` into
`plugins/apex-spec/skills/apex-spec/`. Do **not** hand-edit the nested payload.
Verify with:

```bash
bash scripts/sync-plugin-payload.sh --check
```

Reminder: the sync script does **not** touch `plugin.json` or
`.agents/plugins/marketplace.json`. Hand-edit `plugin.json` for the version and
longDescription per Section F; `.agents/plugins/marketplace.json` has no command
count and should remain unchanged unless its metadata changes for another
reason.

---

## No Change Needed (verified)

- `scripts/analyze-project.sh` -- `current_session_files` is computed from the
  actual directory contents, so `code-review.md` appears automatically once
  present. No hardcoded artifact allow-list to update. (The example JSON at
  ~348 is illustrative only; optional to mention `code-review.md` there.)
- `scripts/common.sh`, `scripts/check-prereqs.sh` -- no command list.
- `agents/openai.yaml`, `.agents/plugins/marketplace.json` -- no per-command
  content; no change (marketplace.json carries no command count).
- `.github/workflows/test.yml` -- reference resolution is driven by SKILL.md, so
  adding the dispatch row is enough. The plugin wrapper check already compares
  the synced payload.
- `.github/workflows/release.yml` -- no exact command count. The file inventory
  threshold is only a minimum reference-file guard and does not need a creview
  edit unless you intentionally tighten the threshold.

---

## Suggested Execution Order

1. (Decisions resolved -- see Resolved section.)
2. Author `references/creview.md` (Section A).
3. Edit canonical skill files (Section B).
4. Edit root/instruction files (Section C) and developer docs (Section D).
5. Edit the CLI and tests (Section E); run `pytest` and `bats tests/`.
6. Apply the version bump + plugin.json longDescription (Section F).
7. Run `bash scripts/sync-plugin-payload.sh` then `--check` (Section G).
8. Run the verification sweep below.

---

## Verification Sweep

- [ ] No stale counts remain:
      `grep -rn -E "13[- ](command|staged|workflow)|23[- ]?(command|commands|entries|total)|23 separate" --include="*.md" --include="*.json" .`
      (expect only intended historical CHANGELOG/docs/CONSIDERATIONS entries,
      if any).
- [ ] No stale active CLI test counts remain:
      `grep -rn -E "54 tests|13 known commands" docs/ARCHITECTURE.md docs/development.md apex-infinite-cli/README-apex-infinite-cli.md`
      (historical CHANGELOG entries can remain unchanged).
- [ ] `creview` appears in: `SKILL.md` dispatch table, `workflow-overview.md`,
      `implement.md` handoff, `validate.md` intro, `guidance.md`,
      `walkthrough.md`, `utilities.md`, `README.md`, `AGENTS.md`, `CLAUDE.md`,
      `docs/development.md`, `docs/apex-infinite-cli/prompt-contract.md`,
      `apex-infinite-cli/README-apex-infinite-cli.md`, `KNOWN_COMMANDS`, and
      `tests/reference-autonomy.bats`.
- [ ] `implement.md` and the CLI implement block both hand off to `creview`.
- [ ] `creview.md` and the CLI creview block both hand off to `validate`.
- [ ] `validate.md` requires `code-review.md` with `Result: RESOLVED`; missing
      or blocked code review routes to `Next command: creview`, while ordinary
      validation failures still route to `implement`.
- [ ] `bash scripts/sync-plugin-payload.sh --check` reports current.
- [ ] `pytest` passes in `apex-infinite-cli/`.
- [ ] `bats tests/` passes from the repo root.
- [ ] ASCII/LF check on `references/creview.md`:
      `file references/creview.md` shows ASCII text; no CRLF.
- [ ] Version string is identical across all locations in Section F.

---

## Resolved (all decisions settled -- ready to implement)

- **Autonomy / no human in the loop** (Decision 1) -- SETTLED. No `QUESTION`
  gate, no approval or review stop, no "needs my decision" output. Any draft
  language implying human review is a defect to delete.
- **Review scope** -- SETTLED. `creview` reviews **ALL uncommitted changes in
  the working tree**, not just session deliverables. This is critical and
  non-negotiable: it catches manual edits, drift, and anything that slipped
  past `implement`.
- **Version number** (Decision 6) -- SETTLED: `2.0.29-codex -> 2.1.0-codex`
  (minor bump) across all version locations + plugin.json longDescription.
- **`validate` FAIL routing** (Decision 4) -- SETTLED: implementation-related
  FAILs stay pointed at `implement`; missing, BLOCKED, or not-RESOLVED
  `code-review.md` points to `creview`.
- **New ADR** -- SETTLED: add `docs/adr/0002-creview-step.md` documenting why
  the review/repair step was inserted between `implement` and `validate`.
- **Artifact name** -- SETTLED: `code-review.md` in the session directory.

No open decision points remain.

---

## Appendix A: Full draft of `references/creview.md`

This is the complete, corrected, house-style content for the new reference file
(the folded-in replacement for the former `prompt.md`). Create
`references/creview.md` with exactly this content (the outer four-backtick fence
below is a wrapper for this plan only -- the file itself starts at the
`# creview` line and uses normal three-backtick code blocks). ASCII-only, LF
endings.

````markdown
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

### 1. Get Deterministic Project State

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
````
