# Agent Skills Prompt Improvements

## Audit Metadata

- Date: 2026-04-10
- Tightened: 2026-04-15 after comparing a sample `plansession` rewrite against
  `references/plansession.md`, `SKILL.md`, and `references/workflow-overview.md`
- Scope: Prompt-level improvements for `references/`
- External repo studied: `agent-skills/`
- Internal repo studied: `apex-spec-system-open`
- Focus: Transfer prompt-writing patterns that improve reliability and clarity
  without importing tool-specific behavior, weakening Apex workflow rules, or
  degrading step-level autonomy

## Scope Boundary

This document is narrower than
`docs/ongoing-projects/agent-skills-recommended-improvements.md`.

That earlier audit already covered the biggest architecture and documentation
wins and those changes have landed. This pass looks only at prompt behavior
inside `references/`:

- how commands surface assumptions
- how commands require evidence
- how commands defend against predictable agent shortcuts
- how commands define applicability and exit criteria

This pass also uses a stricter autonomy standard than the earlier audit:

- preserve autonomy within each command step, not only between workflow steps
- treat assumption handling as resolve-and-proceed behavior, not a clarification
  loop
- allow step interruption only for missing inaccessible inputs, missing
  credentials or secrets, or explicit safety policies such as overwrite
  confirmation

## Method

Compared these external prompt sources:

- `agent-skills/docs/skill-anatomy.md`
- `agent-skills/skills/spec-driven-development/SKILL.md`
- `agent-skills/skills/planning-and-task-breakdown/SKILL.md`
- `agent-skills/skills/incremental-implementation/SKILL.md`
- `agent-skills/skills/code-review-and-quality/SKILL.md`
- `agent-skills/skills/context-engineering/SKILL.md`
- `agent-skills/skills/debugging-and-error-recovery/SKILL.md`

Against these internal workflow references and contracts:

- `docs/CONVENTIONS.md`
- `references/createprd.md`
- `references/createuxprd.md`
- `references/plansession.md`
- `references/phasebuild.md`
- `references/implement.md`
- `references/validate.md`
- `references/audit.md`
- `references/documents.md`
- `references/qimpl.md`
- `references/qbackenddev.md`
- `references/qfrontdev.md`
- `references/copush.md`
- `docs/apex-infinite-cli/prompt-contract.md`

## Current Strengths In Apex

Apex already does several things better than the external repo for this use
case:

- Stronger staged workflow and handoff discipline
- Better local-first script resolution rules
- Better deterministic first-step state checks in core commands
- Better command-specific no-deferral policies
- Better separation between orchestrator and shared checklist references
- `validate.md` Step 3.D already uses targeted anti-rationalization language
  ("NO PRE-EXISTING EXCUSE") for test failures -- this proves the pattern
  works in Apex and can be extended to other commands

This means the remaining opportunity is not "copy agent-skills." The useful
transfer is prompt technique, not architecture. Any imported pattern must be
adapted to Apex's stronger autonomy model.

## Candidate Decision Matrix

| Candidate | Decision | Impact | Effort | Risk | Rationale |
|-----------|----------|--------|--------|------|-----------|
| Add explicit assumption-surfacing and deterministic conflict-resolution steps to ambiguous planning commands | Adopt now | High | Low | Low | `agent-skills` is better at forcing assumptions into the open before planning proceeds. Apex says "do not invent requirements" but usually jumps straight from reading inputs to generating artifacts. The transferred pattern must be adapted so the agent records and resolves ambiguity autonomously rather than asking for arbitration. |
| Add stronger evidence contracts to execution and validation outputs | Adopt now | High | Medium | Low | External skills consistently tie verification to proof. Apex has validation checks, but several references still allow a result summary without requiring exact supporting evidence. |
| Add compact anti-rationalization and red-flag sections to high-risk commands | Adopt now | Medium | Low | Low | This is the strongest prompt-quality technique missing from Apex. None of the current `references/*.md` files use it. |
| Add structured conflict surfacing to planning and execution commands | Adopt now | High | Low | Low | `context-engineering/SKILL.md` provides a "Confusion Management" pattern for when inputs contradict each other (spec vs codebase, PRD vs stub). Apex commands that read multiple inputs before generating artifacts have no structured way to surface contradictions. This is distinct from assumption-surfacing: assumptions address what you don't know, conflicts address what you've been told inconsistent things about. |
| Add scope observation template to `implement` | Backlog | Medium | Low | Low | `incremental-implementation/SKILL.md` Rule 0.5 provides a structured "NOTICED BUT NOT TOUCHING" template for when agents spot issues outside their current task scope. Apex `implement.md` Rule 4 says "no refactoring unrelated code" but gives agents no structured way to record observations without acting on them. |
| Add short "when not to use this command" guidance to selected utility references | Backlog | Medium | Low | Low | Useful for reducing misrouting, but less important than assumption and evidence handling because `SKILL.md` already handles most routing. |
| Import mandatory human review gates from `agent-skills` spec workflows | Reject | Low | Medium | Medium | Apex intentionally supports autonomous end-to-end workflow progress. Mandatory human approval gates would conflict with that operating model. |
| Copy long SKILL-style anatomy sections into every command reference | Reject | Low | High | Medium | That would increase context cost and duplicate the anatomy contract already defined in `docs/CONVENTIONS.md`. |

## Translation Checklist For Future Revisions

This document is a pattern source, not a patch file. When converting any
recommendation here into concrete edits for a command reference, apply this
checklist before drafting the patch:

1. Start from the target command's current contract, not from sample prompt
   text or external wording.
2. Reconcile the draft against `docs/CONVENTIONS.md` reference anatomy:
   summary, workflow position, `## Rules`, `### No Deferral Policy` when
   applicable, `## Steps`, `## Output`, and `## Next Action`.
3. Reconcile every workflow handoff against both `SKILL.md` and
   `references/workflow-overview.md` before editing nearby prose. Do not
   preserve stale transitions just because they were present in the target
   file.
4. Keep the edited reference under the 500-line limit. If a change would push
   it over budget, tighten surrounding prose or move reusable detail into a
   supporting reference instead of appending everything inline.
5. Treat artifact template edits as schema changes. When a recommendation adds,
   removes, or renames generated sections or state fields, audit downstream
   references, scripts, and tests before considering the patch complete.
6. Keep stop conditions and generated artifacts logically consistent. Do not
   add template placeholders such as `Hard blocker: None` to artifacts that
   should only exist after a successful run.
7. Prefer wording that fits Apex's existing vocabulary. For assumption handling,
   use labels like `Working assumption` or `Evidence-backed working assumption`
   rather than language that reads like casual guessing.
8. Translate imported patterns into Apex form. Do not copy external repo
   anatomy, tool-specific wording, or workflow logic verbatim.

## Adopt-Now Recommendation 1

### Explicit assumption-surfacing and deterministic conflict handling for ambiguous commands

**Problem**

Several Apex planning references correctly forbid invention but do not force a
short assumptions pass before artifact generation. That leaves more room for
silent interpretation drift.

**External evidence**

- `agent-skills/skills/spec-driven-development/SKILL.md` explicitly requires
  assumptions to be surfaced before writing spec content, using a structured
  "ASSUMPTIONS I'M MAKING" block with a numbered list
- `agent-skills/skills/planning-and-task-breakdown/SKILL.md` starts in read-only
  planning mode and maps unknowns before decomposition
- `agent-skills/skills/context-engineering/SKILL.md` adds a complementary
  pattern: structured conflict surfacing ("CONFUSION" blocks) for when inputs
  contradict each other, with explicit options

The useful transfer is the explicitness, not the invitation to ask for human
resolution.

**Internal gap**

- `references/createprd.md` Step 5 lists "Assumptions" as one of ~12 extraction
  targets during normalization. But it treats assumptions as data to extract, not
  as a gate to pass through before writing begins. There is no named pre-write
  step where the agent states its working assumptions and checks them.
- `references/createuxprd.md` Mode C explicitly instructs the agent to "make
  confident, opinionated decisions" autonomously but does not require listing
  those decisions as explicit working assumptions first. Modes A and B still carry a
  clarifying-question posture that this recommendation should not preserve.
- `references/plansession.md` goes directly from Step 2 (read PRD content) to
  Step 3 (analyze and recommend) with no intermediate assumption or conflict
  check. When PRD content and session stubs disagree, nothing forces the
  disagreement to be surfaced.
- `references/phasebuild.md` Step 1 has a "Fail early" clause for missing phase
  signals and a reconciliation clause for conflicting PRD vs state.json, but no
  assumption listing before creating phase artifacts.

There is also a document-level risk in this recommendation itself: if phrased
loosely, contributors may implement assumption or conflict checks as "surface
ambiguity, then ask the user." That would weaken Apex autonomy and should be
explicitly prohibited.

**Recommendation**

Add a compact `Assumption and Conflict Check` sub-step to commands that
transform ambiguous or multi-source inputs into planning artifacts. This
combines two related but distinct checks and must be framed as
resolve-and-proceed behavior:

1. **Assumption check** -- list the 3-7 evidence-backed working assumptions
   currently driving the output; distinguish between working assumptions and
   hard blockers caused by inaccessible inputs, missing secrets, or explicit
   safety policies
2. **Conflict check** -- when two or more inputs disagree (PRD vs codebase,
   stub vs completed sessions, PRD_UX vs PRD), surface the contradiction with
   explicit options and select the best-supported interpretation rather than
   silently drifting

The sub-step should:

- list the 3-7 evidence-backed working assumptions currently driving the output
- distinguish between working assumptions and true hard blockers
- surface any input conflicts with explicit options (A/B/C format)
- resolve assumptions and conflicts deterministically inside the step whenever
  the needed evidence is available in the repo, specs, or prior artifacts
- record the chosen assumption set and conflict resolutions in the generated
  artifact when they matter and the run succeeds
- use evidence-backed wording for assumptions so the label reads as a traceable
  working decision, not as permission to guess
- keep hard blockers out of successful artifact templates; a true hard blocker
  should terminate the command before artifact generation
- never turn ambiguity by itself into a prompt for user arbitration

**Autonomy guardrail**

Inside a command step, ambiguity is not a reason to ask. Contradiction is not a
reason to ask. The agent should resolve, record, and proceed.

Only three categories justify stopping the step:

- the required external input artifact does not exist anywhere accessible to the
  agent
- execution requires credentials, secrets, or permissions the agent does not
  have
- an explicit safety policy requires confirmation before a destructive action
  such as overwriting non-template content

**Likely edit targets**

- `references/createprd.md` (assumption check before Step 5)
- `references/createuxprd.md` (assumption check before Step 5, especially
  Mode C)
- `references/plansession.md` (assumption and conflict check between Steps 2
  and 3)
- `references/phasebuild.md` (assumption check before Step 2)

**Concrete examples**

- `createprd`: add a pre-write assumptions pass after source collection and
  before requirement normalization. Example assumptions: target deployment
  model, authentication strategy, whether MVP scope matches the source doc's
  full scope. If the source leaves one of these unclear, choose the most
  conservative interpretation that preserves PRD stability and record it.
- `createuxprd`: add assumptions for target audience, platform, device mix, and
  existing design system constraints. In Mode C, list every autonomous decision
  as an explicit working assumption and proceed without asking.
- `plansession`: add assumptions for package ownership, dependency readiness,
  deliverable boundaries, and required testing level. Add a conflict check
  when PRD scope and session stub scope disagree, then choose the
  best-supported interpretation and record why. Resolve package scope from repo
  evidence before asking. Keep the phase-complete handoff aligned with the real
  workflow (`audit`, not `phasebuild`). Do not add a hard-blocker placeholder
  to `spec.md`; if a hard blocker exists, stop before writing session artifacts.
- `phasebuild`: add assumptions for why a new phase is warranted and what must
  stay out of the phase. Surface conflicts between PRD.md phase definitions and
  state.json phase tracking as structured options, then reconcile them during
  the run rather than deferring to the user

**Validation**

- A reader can point to the assumptions that shaped the generated artifact
- Two different agents are less likely to produce materially different output
  from the same ambiguous source notes
- Generated artifacts show not just what assumptions existed, but which ones
  were actually chosen and acted on
- The assumption/conflict pass reduces silent drift without reintroducing a
  clarification loop

## Adopt-Now Recommendation 2

### Stronger evidence contracts for outputs and task logs

**Problem**

Apex core commands often say to verify or validate, but several of them do not
require the output or working notes to preserve exact proof of what was checked.
That weakens auditability and makes resumption harder.

**External evidence**

- `agent-skills/docs/skill-anatomy.md` emphasizes evidence-backed verification
  and treats the Verification section as a checklist of exit criteria where
  "every checkbox should be verifiable with evidence (test output, build
  result, screenshot, etc.)"
- `agent-skills/skills/incremental-implementation/SKILL.md` requires each
  increment to be tested and verified before moving on, with an explicit
  7-item checklist after each increment
- `agent-skills/skills/code-review-and-quality/SKILL.md` Step 5 ("Verify the
  Verification") asks reviewers to check the author's verification story:
  what tests were run, did the build pass, was there manual verification

**Internal gap**

The gap is not that verification is missing -- Apex requires it. The gap is
that output contracts do not consistently mandate structured proof.

- `references/implement.md` Step 5D task log template records Files Changed but
  has no Verification subsection (what commands were run, what each produced).
  The evidence that a task was verified lives only in the agent's memory, not
  in the persistent artifact.
- `references/validate.md` generates a validation report with PASS/FAIL tables,
  but the report template does not require recording exact commands run for each
  check. A future reader sees "Tests Passing: PASS" but not what test command
  was executed or how many tests ran.
- `references/audit.md` Step 8 REPORT shows a summary ("Fixed: 47 format
  issues, 12 lint errors") but does not require the exact commands that
  produced those numbers.
- `references/documents.md` Step 9 generates a coverage report but not an
  evidence report of what was actually verified against the codebase.
- `references/qimpl.md` Step 5 says to update the work file with "What was
  completed / What remains / Current state / Any concise notes / Clear next
  steps" -- purely prose, no structured evidence block.
- `references/qbackenddev.md` Step 6 and `references/qfrontdev.md` Step 5
  have identical structures -- prose update with no mandated evidence shape.
  A future session inherits narrative, not proof.

**Recommendation**

For execution-heavy commands, require an evidence block in either the command
output or the persistent work artifact.

Minimum evidence shape:

- commands run
- files created or modified
- tests or checks run
- result of each check
- unresolved blocker, if any, with why it could not be resolved autonomously

**Likely edit targets**

- `references/implement.md`
- `references/validate.md`
- `references/audit.md`
- `references/documents.md`
- `references/qimpl.md`
- `references/qbackenddev.md`
- `references/qfrontdev.md`

**Concrete examples**

- `implement`: extend `implementation-notes.md` task entries with a
  `Verification` subsection that records exact checks run for that task
- `validate`: require the final validation report to include exact commands run
  for test, schema, and security checks when applicable
- `audit`: require bundle reports to record the selected bundle, commands run,
  fixes applied, and remaining failures by package
- `q*` commands: require the work file update to include evidence of what was
  actually verified, not only a prose summary of what was attempted

**Validation**

- A fresh session can resume without re-deriving what was already proven
- A reviewer can tell the difference between "implemented" and "implemented and
  verified"
- Command outputs become easier to compare across sessions because the proof
  shape is consistent

## Adopt-Now Recommendation 3

### Add compact anti-rationalization and red-flag language

**Problem**

Apex has strong rules, but it rarely addresses the specific excuses agents use
to bypass those rules. `agent-skills` does this unusually well.

**External evidence**

- `agent-skills/docs/skill-anatomy.md` treats `Common Rationalizations` as a
  first-class section and calls it "the most distinctive feature of
  well-crafted skills"
- `agent-skills/skills/spec-driven-development/SKILL.md`,
  `planning-and-task-breakdown/SKILL.md`,
  `incremental-implementation/SKILL.md`, and
  `code-review-and-quality/SKILL.md` all use rationalization and red-flag
  language to target known failure modes directly
- `agent-skills/skills/debugging-and-error-recovery/SKILL.md` applies the
  same pattern to debugging shortcuts ("I know what the bug is, I'll just
  fix it" -> reproduce first)

**Internal gap**

No current file under `references/` contains a `Common Rationalizations`,
`Red Flags`, or equivalent section.

**Partial exception**: `validate.md` Step 3.D already uses targeted
anti-rationalization language for one specific failure mode: "NEVER dismiss a
failure as 'pre-existing' or 'environment issue'". This is effective and
proves the pattern works in Apex. The recommendation is to extend this
approach to other high-risk commands.

**Recommendation**

Do not add this everywhere. Add a short version only to the commands with the
highest failure cost or strongest tendency toward shortcutting.

Recommended initial targets:

- `references/plansession.md`
- `references/implement.md`
- `references/validate.md`
- `references/audit.md`

Suggested shape:

- 3-5 rationalizations per file
- each phrased as excuse -> factual counterpoint
- 3-5 red flags per file
- keep them short and command-specific
- if adding them would push the file past 500 lines, tighten existing prose or
  move reusable detail to a supporting reference instead of just appending more

**Concrete examples**

For `plansession`:

- "Implement can figure out the edge cases later" -> if BQC applies, edge cases
  belong in task descriptions now
- "This session can probably fit if I keep tasks vague" -> vague tasks hide
  overscope and break the 12-25 task contract
- "The phase PRD already scoped the sessions well enough" -> session stubs are
  high-level; plansession must derive deliverables, file paths, and task-level
  acceptance criteria from the PRD
- "25 tasks is enough budget, I don't need to worry about sizing" -> the
  contract is 12-25 tasks at ~20-25 minutes each; 25 vague tasks is worse
  than 15 precise ones

For `implement`:

- "I will update `tasks.md` after I finish a few tasks" -> delayed updates break
  resume safety and state accuracy
- "The test failure looks unrelated" -> prove it on the pre-session commit or
  fix it now
- "The spec doesn't say how to handle this edge case, so I won't" -> if BQC
  applies, the edge case belongs in the task; if it doesn't, log it in
  implementation-notes.md
- "I can infer what the user wants without reading the code" -> Rule 1 says
  "Make NO assumptions"; read the relevant code and comments first

For `validate`:

- "This is probably a pre-existing failure" -> prove it, do not assume it
  (this rationalization is already addressed in Step 3.D and should be
  preserved as a model for the other commands)
- "Security review can happen in a later pass" -> targeted security review is
  part of this command's pass criteria
- "Tests passed, so the session is valid" -> tests are one of 9 checks; task
  completion, deliverables, encoding, database alignment, conventions,
  security, and behavioral quality all apply

For `audit`:

- "The new tool config is enough; I do not need to run all checks" -> Step 5
  requires validating all configured tools in the current state, not just the
  new one
- "This tool is too noisy, I will skip its output" -> process the output;
  known issues belong in known-issues.md, not in your judgment
- "I already fixed the new tool; the old tools don't need re-validation" ->
  the new tool may have broken existing tools; validate all

**Validation**

- Shortcut behavior is addressed before it happens, not only after it causes a
  bad outcome
- Command failure modes become more legible to contributors writing new
  references
- Prompt guidance becomes more behavior-shaping and less purely procedural

## Backlog Recommendation 1

### Add scope observation template to `implement`

**Source**: `agent-skills/skills/incremental-implementation/SKILL.md` Rule 0.5

`implement.md` Rule 4 says "no extra features, no refactoring unrelated code"
but gives agents no structured way to record observations without acting on
them. The external repo solves this with a "NOTICED BUT NOT TOUCHING" template
that lets the agent note issues for future sessions without scope creep.

**Likely edit target**: `references/implement.md` Step 5D task log template

**Suggested addition to the task log**: an optional "Observations (out of
scope)" field where agents record things worth addressing later. This preserves
the information without violating scope discipline.

## Backlog Recommendation 2

### Add "when not to use" guidance to selected utility references

This is useful, but lower priority than the items above.

Best targets:

- `references/qimpl.md`
- `references/qbackenddev.md`
- `references/qfrontdev.md`
- `references/copush.md`
- `references/pullndoc.md`

The goal is to reduce misuse such as using `qimpl` when normal staged workflow
artifacts already exist, or using `copush` when the repo has unrelated dirty
state that should first be reviewed.

## Rejected Transfers

### Mandatory human review gates

Rejected because Apex intentionally supports autonomous progression both
between workflow steps and within each individual step. Human approval can
still exist for explicit safety boundaries, but it should not be hard-coded as
the default resolution path for ambiguity, contradiction, or incomplete
planning inputs.

### Long SKILL-style anatomy in every reference

Rejected because Apex already has a lighter-weight `Reference Anatomy` contract
in `docs/CONVENTIONS.md`. Duplicating anatomy prose into every command would
raise context cost without improving routing or execution.

## Proposed Rollout Order

0. For each target reference, apply the Translation Checklist above before
   drafting the patch: anatomy, workflow handoffs, line budget, and downstream
   schema impact all get checked first
1. Assumption and Conflict Check for `createprd`, `createuxprd`, `plansession`,
   `phasebuild` -- these are independent of each other and can be done in
   parallel
2. Anti-rationalization pilot in `plansession`, `implement`, `validate`,
   `audit` -- low effort, high signal, can also be done in parallel with item 1
3. Evidence contract upgrades for `implement`, `validate`, `audit`, `q*`
   commands -- these touch more files and benefit from having items 1-2 landed
   first so reviewers can see the full prompt shape
4. Optional backlog pass for scope observation template and utility references

Items 1 and 2 are independent and low-risk. They can ship together or in any
order. Item 3 should follow because its changes are larger and benefit from
the assumption/rationalization patterns being established first.

## Success Criteria For This Recommendation Package

### Process criteria (verifiable now)

- Recommendations are tied to named file evidence from both repos
- Adopt-now items preserve Apex non-negotiables: staged workflow, autonomy
  within steps, local-first scripts, shared-reference architecture, and
  ASCII/LF constraints
- Each applied revision is reconciled against `docs/CONVENTIONS.md`, `SKILL.md`,
  and `references/workflow-overview.md` before patching
- The changes improve prompt reliability without importing tool-specific wiring
  from `agent-skills`
- Each recommendation identifies specific steps or sections in specific files
  to edit, not just file-level targets
- No edited command reference exceeds the 500-line budget unless surrounding
  content is tightened or moved so the final file returns under the limit
- No successful artifact template contains a hard-blocker placeholder or other
  state that should have stopped the command instead of being recorded inside
  the artifact
- When artifact shapes or state mutation guidance change, downstream
  references, scripts, and tests are audited as part of the same patch

### Outcome criteria (verifiable after rollout)

- Planning commands (`createprd`, `plansession`, `phasebuild`) produce
  artifacts that contain a visible assumptions/conflicts section traceable to
  the input sources and the selected resolution
- Two different agents given the same ambiguous input produce fewer materially
  different outputs because the assumption gate forces alignment before writing
- The planning commands do not convert ambiguity into clarification prompts;
  they resolve the best-supported path and record it
- `plansession` no longer preserves stale workflow guidance when phase-complete;
  its recommendation path matches the orchestrator and workflow overview
- `implement` task log entries contain a Verification subsection with at least
  one command-and-result pair per task
- `validate` reports contain the exact commands executed for each check, not
  just PASS/FAIL status
- No `q*` work file update consists solely of prose summary -- each includes at
  least a structured evidence block (commands run, files changed, checks
  verified)
- Anti-rationalization sections in `plansession`, `implement`, `validate`,
  and `audit` are each under 15 lines and contain 3-5 command-specific
  excuse/counterpoint pairs
- Assumption labels in edited references read as evidence-backed working
  decisions, not as permission to guess
