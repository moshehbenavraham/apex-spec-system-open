# Agent Skills Prompt Improvement Guide

## Session Split Plan

### Session 01: Planning Assumption Checks

**Objective**: Add Apex-native assumption and conflict handling to the
remaining planning references without changing workflow handoffs.

**Status**: Complete (2026-06-21)

**Scope**:
- Patch `references/createuxprd.md` with material working-assumption handling,
  especially for autonomous Mode C design decisions.
- Patch `references/phasebuild.md` with structured reconciliation of PRD phase
  definitions and `state.json` before phase artifact creation.
- Keep assumptions and conflict resolutions evidence-backed, material, and
  resolved inside the command flow rather than routed to user arbitration.
- Verify successful artifact templates do not contain hard-blocker placeholders
  or generic autonomy boilerplate.

**Outputs**:
- Updated `references/createuxprd.md` and `references/phasebuild.md`.
- Updated rollout checklist entries for the planning-reference work.
- Generated plugin skill payload refreshed if canonical reference changes make
  the packaged copy stale.

**Dependencies / Notes**:
- `references/createprd.md` and `references/plansession.md` are already marked
  done and should be used as local examples.
- Assumption: `docs/CONVENTIONS.md`, `SKILL.md`, and
  `references/workflow-overview.md` remain the authoritative constraints.

**Acceptance Checks**:
- Both target references remain under the 500-line budget or are kept
  line-neutral if already near the budget.
- Handoffs match `SKILL.md` and `references/workflow-overview.md`.
- Material assumptions and conflict resolutions are visible in generated
  artifacts without creating clarification loops.

**Session Result (2026-06-21)**:
- Completed `references/createuxprd.md` with a No Deferral Policy, material
  assumption/conflict resolution step, Mode C traceability rules, and UX PRD
  output fields for working assumptions and conflict resolutions.
- Completed `references/phasebuild.md` with a No Deferral Policy, structured
  PRD/state reconciliation step, materiality threshold, and phase PRD output
  fields for planning assumptions and conflict resolutions.
- Refreshed generated plugin skill payload with
  `bash scripts/sync-plugin-payload.sh`.
- Downstream audit found no parser updates required: `analyze-project.sh`
  parses session stubs, and `updateprd` updates the phase progress tracker.
- Verification run: line counts, ASCII checks, LF checks, downstream `rg`
  audit, sync command, and diff review.
- State after this session: Session 01 was complete; Session 02 was the next
  scoped qimpl target.

### Session 02: Implement Evidence

**Status**: Complete (2026-06-21)

**Objective**: Upgrade `implement` so completed work records task-level
verification evidence and rejects common shortcut behavior.

**Scope**:
- Extend `references/implement.md` so `implementation-notes.md` task entries
  include a `Verification` subsection with exact checks run for each task.
- Add compact anti-rationalization and red-flag guidance using the existing
  `plansession` and `validate` style as the model.
- Audit downstream consumers if the implementation-notes template changes.

**Outputs**:
- Updated `references/implement.md`.
- Any required downstream reconciliations for changed implementation artifact
  shape.
- Updated rollout or backlog checklist status for `implement`.

**Dependencies / Notes**:
- Depends on the evidence-contract pattern in this guide and the strict tone of
  `validate.md` Step 3.D.

**Acceptance Checks**:
- Each implemented task must require concrete verification evidence, not only a
  completion statement.
- Rationalizations and red flags are short, command-specific, and tied to real
  shortcut risks.
- Existing implementation success criteria and task-progress discipline are not
  weakened.

**Session Result (2026-06-21)**:
- Completed `references/implement.md` with a durable per-task evidence rule,
  compact rationalization and red-flag guidance, and task-log gating before a
  task can be checked off.
- Extended the `implementation-notes.md` task entry template with a
  `Verification` subsection that records exact command/check, result, and
  evidence for each completed task.
- Updated the successful `implement` output to state that task evidence was
  recorded with files changed and verification results.
- Refreshed generated plugin skill payload with
  `bash scripts/sync-plugin-payload.sh`.
- Downstream audit found no direct parser updates required: `validate` reads
  `implementation-notes.md` as a progress log, while `documents` and
  `carryforward` collect implementation notes without depending on the old
  task-entry shape. Session 03 remains responsible for validation evidence
  output changes.
- Verification run: downstream `rg` audit, diff review, generated payload
  `cmp`, line counts, ASCII checks, LF checks, and
  `bats tests/reference-autonomy.bats`.
- Current state: Session 02 is complete; Session 03 is the next scoped qimpl
  target.

### Session 03: Validate Evidence

**Status**: Complete (2026-06-21)

**Objective**: Upgrade `validate` so verification claims are backed by exact
commands, results, and disciplined failure handling.

**Scope**:
- Patch `references/validate.md` to require exact commands for each reported
  check instead of only PASS or FAIL status.
- Add compact anti-rationalization and red-flag guidance covering tests as only
  part of the bar, proven pre-existing failures, and mandatory security review.
- Keep validation stop conditions and successful artifacts logically
  consistent.
- Reconcile downstream validation templates or references if output shape
  changes.

**Outputs**:
- Updated `references/validate.md`.
- Updated rollout checklist entry for validation prompt work.
- Notes or edits for any downstream consumer affected by validation artifact
  changes.

**Dependencies / Notes**:
- Should follow the `implement` evidence update so validation can consume the
  stronger implementation notes without contradiction.

**Acceptance Checks**:
- Validation output distinguishes commands run, check results, remaining
  blockers, and unresolved failures.
- Pre-existing failure claims require current evidence.
- Security and compliance review requirements remain explicit and cannot be
  skipped by passing tests alone.

**Session Result (2026-06-21)**:
- Completed `references/validate.md` with an explicit evidence rule requiring
  every PASS, FAIL, or N/A claim in `validation.md` to name the exact command,
  check, or inspected artifact behind it.
- Added compact `validate` rationalization and red-flag guidance covering tests
  as only one validation gate, current proof for pre-existing failure claims,
  mandatory scoped security review, and report-shape red flags.
- Added an Evidence Ledger to the `validation.md` template so commands,
  targeted inspections, check results, evidence, and unresolved blockers are
  visible in one place.
- Tightened the security and validation report templates so the reference is
  under the 500-line budget while preserving the pass/fail bar and workflow
  handoffs.
- Refreshed generated plugin skill payload with
  `bash scripts/sync-plugin-payload.sh`.
- Downstream audit found no parser changes required: `updateprd` checks the
  overall `validation.md` PASS/FAIL result and does not depend on the removed
  verbose template rows.
- Verification run: generated payload `cmp`, line counts, ASCII checks, LF
  checks, diff review, and `bats tests/reference-autonomy.bats`.
- Current state: Session 03 is complete; Session 04 is the next scoped qimpl
  target.

### Session 04: Audit And Documents Evidence

**Status**: Complete (2026-06-21)

**Objective**: Strengthen phase-transition audit and documentation commands
with concrete evidence while preserving phase handoffs.

**Scope**:
- Patch `references/audit.md` to record the selected bundle, commands run,
  fixes applied, and remaining failures by package.
- Add compact audit anti-rationalization and red-flag guidance focused on
  configured tools being run and re-validated.
- Patch `references/documents.md` to record what was verified against the
  codebase, not only documentation coverage conclusions.
- Reconcile `carryforward`, `documents`, and `phasebuild` handoff language if
  related text is touched.

**Outputs**:
- Updated `references/audit.md` and `references/documents.md`.
- Updated rollout checklist entries for audit and documents.
- Any required downstream reconciliation notes or edits for changed artifact
  expectations.

**Dependencies / Notes**:
- Can run after the main planning and validation evidence patterns are stable.
- Assumption: audit and documents belong together because both operate in the
  phase-transition quality and evidence path.

**Acceptance Checks**:
- Audit evidence names actual commands, fixes, failures, and package scope.
- Documentation evidence names what was checked against the current codebase.
- Phase-transition next actions still match the canonical workflow.

**Session Result (2026-06-21)**:
- Completed `references/audit.md` with an explicit evidence rule, compact
  rationalization and red-flag guidance, validation evidence capture, an audit
  Evidence Ledger, and output evidence for commands/checks run by bundle and
  package.
- Completed `references/documents.md` with an explicit documentation evidence
  rule, finding-level codebase/spec evidence requirements, a docs-audit
  Evidence Ledger, and output evidence for commands or targeted inspections.
- Trimmed `references/documents.md` from 532 to 460 lines while adding the
  evidence contract, bringing the reference back under the 500-line budget.
- Reconciled phase-transition handoffs against `SKILL.md`,
  `references/workflow-overview.md`, `references/carryforward.md`, and
  `references/phasebuild.md`; no downstream handoff edits were required.
- Refreshed generated plugin skill payload with
  `bash scripts/sync-plugin-payload.sh`.
- Verification run: generated payload `cmp`, line counts, ASCII checks, LF
  checks, handoff/evidence `rg` audit, diff review, and
  `bats tests/reference-autonomy.bats`.
- Current state: Session 04 is complete; Session 05 is the next scoped qimpl
  target.

### Session 05: Quick Command Evidence

**Status**: Complete (2026-06-21)

**Objective**: Add consistent, lightweight evidence contracts to the autonomous
quick implementation commands.

**Scope**:
- Patch `references/qimpl.md`, `references/qbackenddev.md`, and
  `references/qfrontdev.md` so outputs distinguish files changed, commands run,
  checks attempted, check results, and unresolved blockers.
- Keep the evidence contract aligned with utility-command behavior rather than
  importing staged-workflow artifact requirements wholesale.
- Preserve each command's existing routing, scope, and standalone
  `Next command: none` behavior when complete.
- Update rollout checklist entries for the `q*` command evidence work.

**Outputs**:
- Updated `references/qimpl.md`, `references/qbackenddev.md`, and
  `references/qfrontdev.md`.
- Updated rollout checklist status for quick-command evidence.
- Any required follow-through notes for shared wording or templates touched
  across the quick commands.

**Dependencies / Notes**:
- Should reuse the evidence shape from execution-heavy commands while avoiding
  quota-driven ceremony.

**Acceptance Checks**:
- Each quick command requires proof of what was actually verified.
- Evidence wording does not relax testing requirements or overpromise checks
  that were not run.
- Utility-command handoffs remain concise and command-shaped.

**Session Result (2026-06-21)**:
- Completed `references/qimpl.md`, `references/qbackenddev.md`, and
  `references/qfrontdev.md` with lightweight evidence rules for work-file
  updates and final outputs.
- Each quick command now distinguishes files changed, commands run, checks
  attempted, check results, unresolved blockers, and work-file continuity.
- Updated the final output shapes so utility responses include `Summary:`,
  `Next command:`, and `Reason:` while preserving `none` when complete and the
  same quick command when work remains.
- Added frontend-specific quality-gate evidence guidance for `qfrontdev`,
  including `N/A` handling for documentation, planning, or non-UI-only work.
- Refreshed generated plugin skill payload with
  `bash scripts/sync-plugin-payload.sh`.
- Downstream audit found no parser, state, or staged-workflow updates required;
  the quick-command output contract is consumed by agents, not scripts.
- Verification run: line counts, ASCII checks, LF checks, generated payload
  `cmp`, evidence-output `rg` audit, diff review, and
  `bats tests/reference-autonomy.bats`.
- Current state: Session 05 is complete; Session 06 is the next scoped qimpl
  target.

### Session 06: Utility Routing Guardrails

**Objective**: Add focused "When Not To Use" guidance for selected utility
commands without expanding generic policy text.

**Status**: Complete (2026-06-21)

**Scope**:
- Add short routing-mistake guidance to `references/qimpl.md`,
  `references/qbackenddev.md`, `references/qfrontdev.md`,
  `references/copush.md`, and `references/pullndoc.md`.
- Keep each section focused on realistic misuse cases, such as choosing a quick
  command when normal staged workflow artifacts already exist.
- Avoid long anatomy sections, generic autonomy boilerplate, and repeated
  command-dispatch prose.
- Update backlog checklist entries for the utility guidance work.

**Outputs**:
- Updated utility reference files with concise "When Not To Use" guidance.
- Updated backlog checklist status.
- Notes on any routing wording reconciled with `SKILL.md` dispatch behavior.

**Dependencies / Notes**:
- Should follow or coordinate with Session 05 so `q*` files are not edited in
  conflicting ways.

**Acceptance Checks**:
- Guidance prevents routing mistakes without weakening utility-command
  autonomy.
- No new text contradicts staged workflow routing or command dispatch.
- Added sections stay short and command-specific.

**Session Result (2026-06-21)**:
- Completed short `## When Not To Use` sections in `references/qimpl.md`,
  `references/qbackenddev.md`, `references/qfrontdev.md`,
  `references/copush.md`, and `references/pullndoc.md`.
- Kept the guidance focused on concrete routing mistakes: bypassing staged
  workflow artifacts, choosing the wrong quick command for UI/backend work,
  confusing origin publish workflows with upstream pulls, and using
  documentation commands for implementation curation.
- Preserved utility-command autonomy and existing `Next command:` behavior; no
  output templates, state semantics, or staged workflow handoffs were changed.
- Refreshed generated plugin skill payload with
  `bash scripts/sync-plugin-payload.sh`.
- Downstream audit found no parser, state, artifact-template, or workflow
  updates required because the patch only adds routing guidance.
- Verification run: line counts, ASCII checks, LF checks, generated payload
  `cmp`, targeted `rg` routing-text audit, diff review, and
  `bats tests/reference-autonomy.bats`.
- Current state: Session 06 is complete; Session 07 is the next scoped qimpl
  target.

### Session 07: Rollout Consistency

**Objective**: Close the rollout by verifying consistency, downstream impacts,
line budgets, and packaged skill output.

**Status**: Complete (2026-06-21)

**Scope**:
- Reconcile every touched reference against `SKILL.md`,
  `references/workflow-overview.md`, and `docs/CONVENTIONS.md`.
- Check ASCII-only content, LF line endings, and reference file line budgets.
- Reconcile downstream consumers for any artifact-template or state-shape
  changes before marking related command patches complete.
- Refresh generated plugin skill payload after canonical reference changes and
  confirm only intended files changed.
- Update this guide's rollout status so completed and remaining work are
  accurate.

**Outputs**:
- Final consistency patch for checklist status, downstream references, or
  generated plugin payload as needed.
- Verification notes naming the checks and commands run.
- Clean list of any remaining open questions or deferred backlog items.

**Dependencies / Notes**:
- Runs after the content-editing sessions.
- Assumption: repository packaging conventions require syncing generated
  plugin payload whenever canonical skill files change.

**Acceptance Checks**:
- All rollout checklist entries accurately reflect repository state.
- Generated plugin payload is not stale relative to canonical skill files.
- New examples, templates, checklist lines, and next actions are internally
  consistent with command hard limits and workflow handoffs.

**Session Result (2026-06-21)**:
- Completed the rollout consistency pass against `SKILL.md`,
  `references/workflow-overview.md`, and `docs/CONVENTIONS.md`.
- Trimmed the adjacent monorepo JSON field bullets in
  `references/plansession.md`, bringing the file from 502 to 500 lines without
  changing the command contract.
- Refreshed generated plugin skill payload with
  `bash scripts/sync-plugin-payload.sh`; generated files match canonical
  `SKILL.md`, `references/`, `scripts/`, and `agents/openai.yaml`.
- Downstream audit found no additional parser, script, test, state-shape, or
  artifact-consumer edits required. `implement`, `validate`, `documents`, and
  `carryforward` references remain aligned with the updated
  implementation-notes, validation, and docs-audit artifact expectations.
- Verification run: line counts for all `references/*.md`, ASCII checks for
  modified files, LF checks for modified files, generated payload `diff -qr`,
  targeted artifact and handoff `rg` audit, `git diff --check`, diff review,
  and `bats tests/reference-autonomy.bats`.
- Files changed this session: `references/plansession.md`,
  `plugins/apex-spec/skills/apex-spec/references/plansession.md`, and this
  guide.
- Unresolved blockers: none.
- Current state: all rollout sessions are complete; no further qimpl session is
  needed for this guide.

Use this guide when revising prompt text in `references/`. It is a working
operator guide, not an audit log.

## Goal

Improve command reliability and clarity without changing Apex architecture,
weakening workflow rules, importing tool-specific behavior, or turning
useful guidance into quota-driven ceremony.

## Rollout Checklist

Done:

- [x] `docs/ongoing-projects/agent-skills-prompt-improvements.md` - tighten
  the guide so future revisions avoid quota-driven ceremony, generic autonomy
  boilerplate, and template drift

Adopt now:

- [x] `references/createprd.md` - add Assumption And Conflict Check
- [x] `references/createuxprd.md` - add Assumption And Conflict Check
- [x] `references/plansession.md` - add Assumption And Conflict Check plus
  Anti-Rationalization And Red Flags
- [x] `references/phasebuild.md` - add Assumption And Conflict Check
- [x] `references/implement.md` - add Evidence Contracts plus
  Anti-Rationalization And Red Flags
- [x] `references/validate.md` - add Evidence Contracts plus
  Anti-Rationalization And Red Flags
- [x] `references/audit.md` - add Evidence Contracts plus
  Anti-Rationalization And Red Flags
- [x] `references/documents.md` - add Evidence Contracts
- [x] `references/qimpl.md` - add Evidence Contracts
- [x] `references/qbackenddev.md` - add Evidence Contracts
- [x] `references/qfrontdev.md` - add Evidence Contracts

Backlog:

- [x] `references/qimpl.md` - add short "When Not To Use" guidance
- [x] `references/qbackenddev.md` - add short "When Not To Use" guidance
- [x] `references/qfrontdev.md` - add short "When Not To Use" guidance
- [x] `references/copush.md` - add short "When Not To Use" guidance
- [x] `references/pullndoc.md` - add short "When Not To Use" guidance

Conditional follow-through:

- [x] Reconcile any downstream consumers touched by artifact-template or state
  shape changes before marking the related command patch complete

## Non-Negotiables

- Preserve Apex staged workflow and command handoffs from `SKILL.md` and
  `references/workflow-overview.md`
- Preserve autonomy inside command steps; ambiguity is not a reason to ask,
  pause, or route through approval
- Every command output must include concise `Summary:`, `Next command:`, and
  `Reason:` lines, using `none` only when the workflow or standalone utility
  is complete
- Treat assumption handling as resolve-and-proceed behavior, not a
  clarification loop
- Keep stop conditions command-shaped. Do not paste generic blocker categories
  into a reference unless they are realistic for that command's normal inputs
  and failure modes
- When a command genuinely depends on inaccessible required inputs, missing
  credentials or secrets, or explicit safety policies that require
  confirmation before destructive action, say so explicitly
- Keep local-first script resolution, shared-reference architecture, and
  repo-native state semantics intact
- Do not weaken existing pass/fail bars, testing requirements, or completion
  criteria while tightening prompt language
- Keep reference files under 500 lines and follow `docs/CONVENTIONS.md`; when a
  target is already over budget, trim first or keep the prompt patch
  line-neutral
- Translate useful prompt patterns into Apex form; do not copy external
  anatomy, wording, or workflow logic verbatim
- Any new table, quota, checklist, example, or template line must survive a
  self-consistency check against workflow rules, hard limits, and downstream
  artifact consumers

## Decision Summary

Adopt now:

- Explicit assumption and conflict handling in ambiguous planning commands
- Stronger evidence contracts in execution-heavy outputs and work artifacts
- Compact anti-rationalization and red-flag sections in high-risk commands

Backlog:

- Short "when not to use this command" guidance in selected utility references

Reject:

- Mandatory interactive review gates as the default resolution path
- Long repeated anatomy sections inside every command reference
- Quota-driven ceremony and generic autonomy boilerplate that do not solve a
  demonstrated Apex command failure mode

## Translation Checklist

Apply this checklist before patching any command reference.

1. Start from the target command's current contract, not from sample wording.
2. Reconcile the draft against `docs/CONVENTIONS.md` reference anatomy:
   summary, workflow position, `## Rules`, `### No Deferral Policy` when
   applicable, `## Steps`, `## Output`, and `## Next Action`.
3. Reconcile every workflow handoff against both `SKILL.md` and
   `references/workflow-overview.md`. Do not preserve stale transitions.
4. Keep the file under the 500-line budget. If the target is already over
   budget, trim first or keep the prompt patch line-neutral.
5. Treat artifact template edits as schema changes. Audit downstream
   references, scripts, and tests when sections, fields, or state semantics
   change.
6. Do not silently weaken an existing success criterion. If the contract says
   `Verification scenarios completed`, do not downgrade it to planning-only
   language.
7. Keep stop conditions and successful artifacts logically consistent. A true
   hard blocker should stop the command before artifact generation.
8. Prefer Apex-native wording such as `Working assumption` or
   `Evidence-backed working assumption` over casual guessing language.
9. Demand real specificity. Renaming placeholders is not enough unless the
   prompt now requires repo-derived deliverables, paths, commands, or checks.
10. Preserve repo-native monorepo semantics such as omitted or `null` package
    for cross-cutting scope and existing `Package:` or `Packages:` headers
    unless all dependent consumers change together.
11. When changing autonomy rules for shared flows, reconcile adjacent
    references and supporting guidance that describe the same behavior.
12. Keep rollout scope explicit. Do not smuggle execution-evidence changes into
    planning-command patches unless downstream work is included.
13. Run a self-consistency pass across rules, examples, tables, templates,
    completion checklists, and output text. Budgets, counts, and next-action
    lines must agree with the command's hard limits and workflow handoffs.
14. Treat examples as normative. If a sample `tasks.md` checklist points to the
    wrong next workflow step, the draft is wrong even if the prose above it is
    correct.
15. Use materiality, not quotas. Require assumptions, conflict notes, or other
    sections only when they are actively shaping the output; do not force a
    fixed count just to make the prompt sound rigorous.
16. Only add ceremony that changes behavior. Do not add progress tables,
    category budgets, or generic policy text unless they solve a concrete
    command-level failure mode and remain internally consistent.
17. Use this guide to sharpen behavior, not to expand files with redundant
    explanation.

## Adopt-Now Pattern 1

### Assumption And Conflict Check

Apply to commands that turn ambiguous or multi-source inputs into planning
artifacts.

Primary targets:

- `references/createprd.md`
- `references/createuxprd.md`
- `references/plansession.md`
- `references/phasebuild.md`

Add a compact sub-step before artifact generation that does both jobs:

- Assumption check: surface only the evidence-backed working assumptions that
  materially shape the output; do not impose a fixed quota
- Conflict check: when inputs disagree, surface the contradiction, state the
  viable interpretations, and choose the best-supported one

The sub-step must:

- Distinguish working assumptions from true hard blockers
- Resolve assumptions and conflicts inside the step whenever repo evidence,
  specs, or prior artifacts are sufficient
- Avoid filler assumptions. If ambiguity is fully resolved without any
  persistent working assumption, do not invent one just to satisfy format
- Record chosen assumptions and conflict resolutions in the generated artifact
  when they materially shape the output
- Keep hard blockers out of successful artifact templates
- Never convert ambiguity by itself into a request for user arbitration

Command notes:

- `createprd`: add a pre-write assumptions pass after source collection and
  before requirement normalization
- `createuxprd`: in Mode C, every material autonomous design decision should
  appear as a working assumption before writing proceeds
- `plansession`: add the check between reading inputs and generating the
  session plan; resolve package scope from repo evidence without stopping; keep
  phase-complete handoffs aligned with the real workflow so completion routes
  to `audit`, not `phasebuild`
- `phasebuild`: reconcile PRD phase definitions and `state.json` with a
  structured resolution step before creating phase artifacts

Done when:

- Assumptions that shaped the artifact are visible and traceable
- Contradictions are surfaced and resolved instead of ignored
- Two agents given the same ambiguous inputs are less likely to drift into
  materially different outputs

## Adopt-Now Pattern 2

### Evidence Contracts For Execution

Apply to execution-heavy commands that claim work was completed or verified.

Primary targets:

- `references/implement.md`
- `references/validate.md`
- `references/audit.md`
- `references/documents.md`
- `references/qimpl.md`
- `references/qbackenddev.md`
- `references/qfrontdev.md`

Require an evidence block in the command output or persistent work artifact.

Minimum evidence shape:

- Commands run
- Files created or modified
- Tests or checks run
- Result of each check
- Remaining blocker, if any, and why it could not be resolved autonomously

Command notes:

- `implement`: extend `implementation-notes.md` task entries with a
  `Verification` subsection that records exact checks run for that task
- `validate`: require exact commands for each reported check, not only
  PASS/FAIL status
- `audit`: record the selected bundle, commands run, fixes applied, and
  remaining failures by package
- `documents`: record what was verified against the codebase, not only coverage
  conclusions
- `q*` commands: require evidence of what was actually verified, not only a
  prose summary of what was attempted

Scope rule:

- Planning commands may name intended verification work, but that does not
  satisfy execution evidence and must not relax existing testing requirements

Done when:

- A fresh session can resume without re-deriving what was already proven
- A reviewer can distinguish "implemented" from "implemented and verified"
- Output comparison across sessions is easier because the proof shape is
  consistent

## Adopt-Now Pattern 3

### Anti-Rationalization And Red Flags

Add short behavior-shaping sections to commands with high shortcut risk.

Primary targets:

- `references/plansession.md`
- `references/implement.md`
- `references/validate.md`
- `references/audit.md`

Use a compact format:

- Aim for 3-5 rationalizations per file only when each maps to a real shortcut
  risk
- Aim for 3-5 red flags per file only when each maps to a real review signal
- Each rationalization is written as excuse -> counterpoint
- Keep the section short; tighten surrounding prose if line budget becomes
  tight

Recommended command-specific themes:

- `plansession`: vague tasks hide overscope; session stubs are not enough;
  sizing must reflect the 12-25 task contract and real deliverables
- `implement`: delayed task updates break resume safety; "looks unrelated" is
  not proof; read the code before inferring intent
- `validate`: passing tests are only part of the bar; pre-existing failure
  claims must be proven; security review is not optional
- `audit`: configuring a tool is not enough; all configured tools must be run
  and re-validated in the current state

Use `validate.md` Step 3.D (the no-pre-existing-excuse block) as the model for
strict tone, and the now-adopted `plansession.md` sections
(`### Rationalizations To Reject` plus `### Red Flags`) as the model for the
format. Extend that pattern to other high-risk commands instead of inventing a
new style.

Done when:

- Known shortcut behavior is addressed before it causes bad output
- Failure modes are easier to spot while drafting or reviewing prompt changes

## Backlog

### "When Not To Use" Guidance For Utilities

Best targets:

- `references/qimpl.md`
- `references/qbackenddev.md`
- `references/qfrontdev.md`
- `references/copush.md`
- `references/pullndoc.md`

Keep this short and focused on routing mistakes, such as using `qimpl` when the
normal staged workflow artifacts already exist.

## Rejected Patterns

### Mandatory Human Review Gates

Reject any change that turns ambiguity, contradiction, or incomplete planning
inputs into a default approval checkpoint. Apex supports autonomous progression
within steps and between workflow stages.

### Repeated Long Anatomy Sections

Reject changes that copy long anatomy guidance into every command reference.
`docs/CONVENTIONS.md` already defines the reference structure contract.

### Quota-Driven Ceremony

Reject changes that convert good ideas into fixed counts or mandatory tables
without a command-specific reason. Examples include forced assumption quotas,
category budgets that do not map cleanly to the command's hard limits, or
progress tables that add no decision value.

### Generic Autonomy Boilerplate

Reject pasted autonomous-agent policy language that is not tied to the
command's real dependencies or failure modes. Stop conditions and autonomy
rules should be command-shaped, not imported as generic doctrine.

### Template Drift And Self-Contradiction

Reject edits where examples, checklists, category budgets, or next-step lines
contradict the command's own rules, the canonical workflow, or downstream
artifact semantics.

## Rollout Order

1. Apply the Translation Checklist to each target reference before drafting the
   patch.
2. Add Assumption And Conflict Check to `createprd`, `createuxprd`,
   `plansession`, and `phasebuild`.
3. Add Anti-Rationalization And Red Flags to `plansession`, `implement`,
   `validate`, and `audit`.
4. Upgrade Evidence Contracts in `implement`, `validate`, `audit`,
   `documents`, and the `q*` commands.
5. If useful, add the backlog items after the higher-signal prompt changes are
   in place.

## Completion Standard For Any Patch

A prompt-improvement patch is not complete unless all of the following are
true:

- Workflow handoffs match the orchestrator and workflow overview
- Each command output has clear `Summary:`, `Next command:`, and `Reason:` lines
- New wording preserves or strengthens existing success criteria
- Any artifact shape change is reconciled across downstream consumers
- Claimed specificity improvements produce concrete repo-derived output
- Package and cross-cutting scope semantics remain consistent
- Successful artifacts do not contain hard-blocker placeholders
- Added examples, quotas, tables, and checklist handoffs do not contradict the
  command's hard limits or canonical next actions
