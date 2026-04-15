# Agent Skills Prompt Improvement Guide

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
- [ ] `references/createuxprd.md` - add Assumption And Conflict Check
- [x] `references/plansession.md` - add Assumption And Conflict Check plus
  Anti-Rationalization And Red Flags
- [ ] `references/phasebuild.md` - add Assumption And Conflict Check
- [ ] `references/implement.md` - add Evidence Contracts plus
  Anti-Rationalization And Red Flags
- [ ] `references/validate.md` - add Evidence Contracts plus
  Anti-Rationalization And Red Flags
- [ ] `references/audit.md` - add Evidence Contracts plus
  Anti-Rationalization And Red Flags
- [ ] `references/documents.md` - add Evidence Contracts
- [ ] `references/qimpl.md` - add Evidence Contracts
- [ ] `references/qbackenddev.md` - add Evidence Contracts
- [ ] `references/qfrontdev.md` - add Evidence Contracts

Backlog:

- [ ] `references/implement.md` - add optional `Observations (out of scope)`
  field if still useful after the main prompt revisions land
- [ ] `references/qimpl.md` - add short "When Not To Use" guidance
- [ ] `references/qbackenddev.md` - add short "When Not To Use" guidance
- [ ] `references/qfrontdev.md` - add short "When Not To Use" guidance
- [ ] `references/copush.md` - add short "When Not To Use" guidance
- [ ] `references/pullndoc.md` - add short "When Not To Use" guidance

Conditional follow-through:

- [ ] Reconcile any downstream consumers touched by artifact-template or state
  shape changes before marking the related command patch complete

## Non-Negotiables

- Preserve Apex staged workflow and command handoffs from `SKILL.md` and
  `references/workflow-overview.md`
- Preserve autonomy inside command steps; ambiguity is not a reason to ask
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
- Keep reference files under 500 lines and follow `docs/CONVENTIONS.md`
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

- Optional out-of-scope observation field in `implement`
- Short "when not to use this command" guidance in selected utility references

Reject:

- Mandatory human review gates as the default resolution path
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
4. Keep the file under the 500-line budget. Tighten surrounding prose or move
   reusable detail into supporting references if needed.
5. Treat artifact template edits as schema changes. Audit downstream
   references, scripts, and tests when sections, fields, or state semantics
   change.
6. Do not silently weaken an existing success criterion. If the contract says
   `Manual testing completed`, do not downgrade it to planning-only language.
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
  session plan; resolve package scope from repo evidence before asking; keep
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

- 3-5 rationalizations per file
- 3-5 red flags per file
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

Use `validate.md` Step 3.D as the model for tone and strictness. Extend that
pattern to other high-risk commands instead of inventing a new style.

Done when:

- Known shortcut behavior is addressed before it causes bad output
- Failure modes are easier to spot while drafting or reviewing prompt changes

## Backlog

### Optional Observation Field In `implement`

Target:

- `references/implement.md`

Add an optional `Observations (out of scope)` field to the task log so agents
can record useful findings without scope creep.

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
inputs into a default human-approval checkpoint. Apex supports autonomous
progression within steps and between workflow stages.

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
- New wording preserves or strengthens existing success criteria
- Any artifact shape change is reconciled across downstream consumers
- Claimed specificity improvements produce concrete repo-derived output
- Package and cross-cutting scope semantics remain consistent
- Successful artifacts do not contain hard-blocker placeholders
- Added examples, quotas, tables, and checklist handoffs do not contradict the
  command's hard limits or canonical next actions
