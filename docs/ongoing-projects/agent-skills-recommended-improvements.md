# Agent Skills Recommended Improvements

## Audit Metadata

- Date: 2026-04-09
- Session: Sessions 6-9 - Recommendation Package and Final Handoff
- External repo: `agent-skills/`
- Internal repo: `apex-spec-system-open`
- Purpose: Finalize the recommendation package by preserving the
  implementation-ready adopt-now items from Session 7 and turning backlog and
  reject items into durable decision records, then verify final package
  consistency in Session 9.

## Filtering Rules

Only keep a candidate if all of the following are true:

- It is backed by file-level evidence from the audit notes and comparison matrix.
- It improves reliability, clarity, reuse, or maintainability in this repo.
- It preserves apex non-negotiables: staged handoffs, session sizing,
  orchestrator-plus-reference architecture, local-first scripts, and ASCII/LF
  conventions.
- It remains platform-neutral unless there is a clear repo-level reason to
  accept tool-specific behavior.

Reject or defer a candidate if it is primarily stylistic, depends on
Claude-only wiring, increases context cost without clear benefit, or introduces
operational complexity that this repo does not currently need.

## Candidate Decision Matrix

| Candidate | Decision | Impact | Effort | Risk | Rationale |
|-----------|----------|--------|--------|------|-----------|
| Add stronger fallback routing and discovery guidance outside the main orchestrator | Adopt now | Medium | Low | Low | `agent-skills` is stronger in `AGENTS.md` and its discovery layer, while apex currently relies mostly on `SKILL.md`. A lightweight routing fallback in `AGENTS.md`, `README.md`, and metadata would improve non-orchestrator behavior without changing the core architecture. |
| Add an explicit writing contract for command references | Adopt now | High | Low | Low | The clearest anatomy gap is structural guidance for contributors. `agent-skills/docs/skill-anatomy.md` provides reusable section-level rules, while apex currently has file conventions but not an equally explicit reference anatomy contract. |
| Extract a small reusable checklist layer for repeated quality gates | Adopt now | High | Medium | Low | This is the strongest reusable-content gap in the matrix. Apex repeats cross-cutting quality expectations inline in `references/implement.md`, `references/validate.md`, and `references/audit.md`, so a small shared checklist layer should reduce duplication without weakening local completeness. |
| Expand public onboarding and multi-agent packaging guidance | Backlog | Medium | Medium | Medium | `agent-skills` has a stronger public distribution surface, but apex intentionally favors platform-neutral content over tool-specific packaging. A broader onboarding pass is worthwhile, but it is not as immediate as routing, anatomy, and quality-reference fixes. |
| Add portable reviewer persona files under `agents/` | Backlog | Low | Medium | Medium | The external repo's personas are portable, but they also add another instruction layer. This could help some workflows later, but it should follow clearer governance to avoid splitting authority between workflow references and role prompts. |
| Adopt Claude-specific hook wiring or plugin packaging | Reject | Low | High | High | `hooks/hooks.json`, `session-start.sh`, and `.claude-plugin/` are useful external packaging assets, but they do not transfer directly to this repo's platform-neutral skill model. Direct adoption would increase maintenance while narrowing portability. |
| Add stateful file-mutation automation like `simplify-ignore` | Reject | Low | High | High | The external hook solves a narrow workflow problem by mutating files and relying on restore logic. There is no evidence that apex has the same failure mode, so the operational complexity is not justified. |
| Replace apex's shared-reference architecture with longer self-contained entry files | Reject | Low | High | Medium | Apex already scores better on progressive disclosure and context economy. Moving more workflow detail back into large entry files would work against a current internal advantage. |
| Adopt an aggressive "use a skill if there is even a 1 percent chance" routing rule | Reject | Low | Low | Medium | The external rule reinforces discovery, but apex has a larger and more specialized command surface. Directly copying the threshold would likely increase false-positive routing. The underlying problem is better solved by clearer fallback guidance, not by importing the exact rule. |

## Adopt-Now Recommendations

### 1. Stronger fallback routing and discovery guidance

**Problem**

Apex routing is strongest inside `SKILL.md`, but weaker in secondary entry
surfaces such as `AGENTS.md` and `README.md`. That leaves more ambiguity when
an environment or user does not start from the main orchestrator.

**Evidence**

- External strength: `agent-skills/AGENTS.md`,
  `agent-skills/skills/using-agent-skills/SKILL.md`
- Internal gap: `AGENTS.md`, `README.md`
- Matrix criterion: Activation and routing guidance

**Recommendation**

Add a small fallback routing layer outside `SKILL.md` so the repo remains easy
to route even when the orchestrator is not the first file an agent or
maintainer reads.

**Files likely to change**

- `AGENTS.md`
- `README.md`

**Minimum viable implementation**

- Add a short `Routing Fallback` section to `AGENTS.md` that:
  - tells the reader to prefer `SKILL.md` when they need the full workflow
  - explains how to choose between Stage 1, Stage 2, Stage 3, and utility
    commands
  - gives a small number of intent-to-command examples such as
    `new project -> initspec`, `need the next scoped session -> plansession`,
    `have a work file and want an autonomous burst -> qimpl`, and
    `phase sessions are done -> audit`
  - explicitly avoids importing the external `1 percent` activation rule
- Add a compact `Choosing a Starting Command` section to `README.md` that:
  - mirrors the same command-family split at a higher level
  - points readers to `references/workflow-overview.md` for the complete map
  - keeps the command-selection content short enough that it does not compete
    with `SKILL.md`
- Leave `agents/openai.yaml` unchanged unless there is a Codex-only routing gap
  that cannot be solved in platform-neutral docs. The current evidence does not
  justify expanding tool-specific metadata yet.

**Validation**

- A cold reader can correctly route these four scenarios from `AGENTS.md` or
  `README.md` alone:
  - first-time setup in a repo with no `.spec_system/`
  - continuation of the normal session loop in a repo with `.spec_system/`
  - autonomous work against an existing work file
  - post-session phase transition after all sessions in a phase are complete
- The fallback guidance does not add new workflow rules or conflict with
  `SKILL.md`
- `references/workflow-overview.md` remains the detailed quick-reference rather
  than being duplicated inline

**Sequencing**

- Land this first. It is the smallest, lowest-risk adopt-now item and improves
  repo usability immediately.
- Keep it documentation-only. Do not mix this recommendation with deeper
  workflow refactors.

### 2. Explicit reference anatomy contract

**Problem**

The repo has strong file-level conventions, but contributors do not have a
clear section-level writing contract for command references.

**Evidence**

- External strength: `agent-skills/docs/skill-anatomy.md`
- Internal gap: `docs/CONVENTIONS.md`, `references/`
- Matrix criterion: Anatomy contract and contributor consistency

**Recommendation**

Define a documented section contract for command references so contributors know
what belongs in each file and where recurring instruction types should live.

**Files likely to change**

- `docs/CONVENTIONS.md`
- `references/implement.md`
- `references/validate.md`
- `references/audit.md`
- `references/documents.md`

**Minimum viable implementation**

- Extend `docs/CONVENTIONS.md` with a `Reference Anatomy` section that defines:
  - required sections for command references such as opening summary, rules,
    required first step, main workflow steps, and expected output or handoff
  - where local-first script resolution belongs when a command depends on
    scripts
  - where no-deferral policy language should appear when a command can resolve
    its own blockers
  - where validation, recovery, and next-command guidance should appear
- Normalize the highest-leverage command references to match the contract first:
  `references/implement.md`, `references/validate.md`, `references/audit.md`,
  and `references/documents.md`
- Keep the current orchestrator-plus-reference architecture. The goal is not to
  make references longer; it is to make their internal shape more predictable.

**Validation**

- A contributor can draft a new reference file by following
  `docs/CONVENTIONS.md` without reverse-engineering multiple existing files
- The normalized reference files use the same section order and naming for
  equivalent concepts such as rules, first-step state checks, and handoff
  guidance
- No reference file grows materially in size just to satisfy the contract

**Sequencing**

- Land this before extracting shared checklist documents so the later checklist
  links fit a stable reference structure.
- Limit the first pass to the most central workflow files. Apply the contract
  to the rest of `references/` incrementally rather than creating a large
  normalization-only sweep.

### 3. Reusable quality checklist layer

**Problem**

Cross-cutting testing, security, performance, and documentation checks are
repeated across command references, which makes them harder to update
consistently.

**Evidence**

- External strength: `agent-skills/references/testing-patterns.md`,
  `agent-skills/references/security-checklist.md`,
  `agent-skills/references/performance-checklist.md`,
  `agent-skills/references/accessibility-checklist.md`
- Internal gap: repeated inline expectations in `references/implement.md`,
  `references/validate.md`, `references/audit.md`, `references/documents.md`
- Matrix criterion: Reusable quality references

**Recommendation**

Extract a small shared checklist layer for repeated quality domains while
keeping command-specific pass or fail criteria inside the command references.

**Files likely to change**

- New supporting references under `references/`, likely:
  - `references/behavioral-quality-checklist.md`
  - `references/security-compliance-checklist.md`
  - `references/documentation-readiness-checklist.md`
- Existing command references:
  - `references/implement.md`
  - `references/validate.md`
  - `references/audit.md`
  - `references/documents.md`

**Minimum viable implementation**

- Extract the longest repeated cross-cutting guidance into a few root
  checklist-style supporting references rather than many micro-files
- Move reusable domain guidance into those supporting references, especially:
  - behavioral quality expectations reused across implementation and validation
  - security and compliance spot-check prompts reused during validation and
    later audit work
  - documentation freshness and handoff checks reused by documentation-focused
    workflows
- Keep command-local material in place when it is specific to a command's gate,
  such as `PASS requires ALL of`, bundle ordering, or phase-transition rules
- Link to the shared checklist documents from the command references instead of
  repeating the full prose in every file

**Validation**

- Each extracted checklist is referenced by at least two workflow documents or
  clearly reduces duplication in one very large workflow document
- Updating one checklist changes the shared guidance everywhere it is used
- Command references remain executable on their own and do not degrade into
  thin shells that require constant reference-hopping

**Sequencing**

- Land this after the reference anatomy contract so the extracted checklist
  links sit in a predictable section.
- Keep the first extraction intentionally small. If a quality domain appears in
  only one place, leave it inline.

## Recommended Implementation Order

1. Add stronger fallback routing and discovery guidance in `AGENTS.md` and
   `README.md`.
2. Define the reference anatomy contract in `docs/CONVENTIONS.md` and align the
   core workflow references.
3. Extract the smallest useful shared checklist layer under `references/` and
   update the affected workflow files to point to it.

This order keeps the lowest-risk documentation fix first, establishes the
structure contract before reuse extraction, and avoids mixing architectural
normalization with platform-facing routing changes in the same patch.

## Backlog

### 1. Public onboarding and multi-agent packaging expansion

**Problem**

The external repo has a stronger public adoption surface than apex. It ships
tool-specific getting-started paths and clearer packaging cues, while apex
currently relies more on a general README plus architecture and onboarding
docs.

**Evidence**

- External strength: `agent-skills/README.md`,
  `agent-skills/docs/getting-started.md`,
  `agent-skills/docs/cursor-setup.md`,
  `agent-skills/docs/gemini-cli-setup.md`,
  `agent-skills/docs/opencode-setup.md`, `agent-skills/agents/`
- Internal baseline: `README.md`, `docs/onboarding.md`,
  `docs/ARCHITECTURE.md`, `agents/openai.yaml`
- Matrix criterion: Onboarding, packaging, and cross-agent portability

**Why this is backlog instead of adopt now**

This is a real gap, but it is not the next best use of effort. Session 7
already identified three smaller changes with clearer ROI: routing fallback,
reference anatomy, and reusable checklist extraction. Those improvements raise
day-to-day workflow reliability inside the repo itself, while onboarding and
packaging expansion mainly improve external distribution and adoption.

There is also an unresolved strategy question. The repo deliberately uses
platform-neutral reference content and documents a dual-platform history rather
than a single shared packaging layer. A rushed packaging push could pull the
repo toward tool-specific install surfaces before maintainers decide how far
cross-agent support should actually go.

**Future implementation shape**

- Tighten `README.md` and `docs/onboarding.md` into a clearer installation and
  first-session path for new users
- Add cross-agent guidance only where the behavior is truly portable
- Keep command and reference files platform-neutral even if surrounding setup
  docs become more segmented by environment
- Reuse any future routing improvements from the adopt-now track so onboarding
  starts from the right workflow entry points

**Revisit trigger**

Move this into implementation planning only after the adopt-now items land and
the maintainers can answer two questions:

- Which agent environments are first-class support targets for this repo?
- Can the extra packaging surface be added without duplicating instructions or
  weakening the platform-neutral content contract?

### 2. Portable reviewer personas

**Problem**

The external repo gains some portability by shipping standalone reviewer
personas under `agents/`, but apex currently keeps almost all workflow
authority in the orchestrator and command references.

**Evidence**

- External strength: `agent-skills/agents/code-reviewer.md`,
  `agent-skills/agents/security-auditor.md`,
  `agent-skills/agents/test-engineer.md`
- Internal baseline: `agents/openai.yaml`, `AGENTS.md`, `SKILL.md`,
  `references/validate.md`, `references/audit.md`
- Notes risk callout: persona files are portable, but they can fragment
  authority if they overlap existing workflow instructions

**Why this is backlog instead of adopt now**

The concept is plausible, but the repo is not ready to add another instruction
layer yet. Apex is stronger when workflow rules stay centralized in `SKILL.md`
and the command references. Persona files would only help if maintainers first
define exactly what those personas may own and what must remain authoritative
in the workflow documents.

The current evidence also does not show a pressing internal failure mode that
personas would solve immediately. They may improve portability later, but they
are less urgent than the structural fixes already chosen for adopt-now.

**Future implementation shape**

- Define governance first: workflow references stay authoritative for staged
  execution and pass or fail criteria
- Limit personas to review lenses or specialist prompts rather than alternate
  workflow definitions
- Start with one narrowly scoped reviewer artifact only if there is a clear
  reuse case across tools

**Revisit trigger**

Reopen this only after maintainers define instruction-authority boundaries and
have a concrete cross-tool need that cannot be met cleanly by the existing
workflow references.

## Reject

### 1. Claude-only hooks and plugin packaging

**Why this is rejected**

The strongest external packaging mechanisms in Session 3 are explicitly tied to
Claude: `hooks/hooks.json`, `hooks/session-start.sh`, and
`.claude-plugin/plugin.json`. Apex intentionally treats platform-neutral
content as a non-negotiable and documents a separate dual-platform history in
`docs/ARCHITECTURE.md`. Directly adopting Claude-only hook registration or
plugin packaging into this repo would move the repo away from that portability
contract.

**Non-adoption boundary**

- Do not add Claude-only hook registration as a default repo requirement
- Do not treat `.claude-plugin/` packaging as the next baseline delivery model
- Only revisit tool-specific packaging if the repo explicitly changes strategy
  and decides to support a first-class tool-specific distribution layer

**What to do instead**

Carry forward the underlying lesson, not the mechanism: improve routing and
discoverability through portable documentation and lightweight metadata where
possible.

### 2. Stateful file-mutation hooks

**Why this is rejected**

The external `simplify-ignore` system is sophisticated, but it solves a narrow
problem through file mutation, backup and restore logic, and crash-recovery
paths. The audit found no comparable apex failure mode that requires this
complexity. Adopting stateful mutation machinery without a concrete local need
would add operational risk with no proven payoff.

**Non-adoption boundary**

- Do not introduce mutation-and-restore hooks as a general workflow pattern
- Do not add recovery-heavy automation unless a specific apex workflow cannot
  be protected through simpler documentation or validation changes
- Require a concrete, repeated failure mode before reconsidering this class of
  tooling

**What to do instead**

Prefer simpler enforcement layers first: tighter workflow instructions,
reusable checklists, and deterministic validation scripts.

### 3. Longer self-contained entry files

**Why this is rejected**

The audit does not support replacing apex's orchestrator-plus-reference
architecture with large self-contained entry documents. Session 2 showed that
the external repo's biggest anatomy win comes from its writing contract and
reuse cues, not from making lifecycle entry files longer. Apex already scores
better on progressive disclosure and context economy, so copying the external
repo's longer entry-file shape would trade away an existing internal strength.

**Non-adoption boundary**

- Do not move substantial workflow detail out of `references/` back into
  `SKILL.md`
- Do not equate contributor consistency with larger entry files
- Treat structural normalization and reusable references as the preferred
  improvement path instead

**What to do instead**

Strengthen the internal section contract for reference files and extract only
the smallest useful shared checklist layer.

### 4. Direct adoption of the external 1 percent routing threshold

**Why this is rejected**

The external threshold is a strong discovery heuristic for a smaller command
surface, but apex has a broader and more specialized routed inventory. Directly
copying the `1 percent` trigger would likely increase false-positive routing
and unnecessary workflow activation. The audit already identified a cleaner
solution: strengthen fallback guidance in `AGENTS.md` and `README.md` without
importing the exact threshold rule.

**Non-adoption boundary**

- Do not add a blanket low-threshold activation rule to apex routing docs
- Do not override the orchestrator's more specific intent-to-command mapping
- Only revisit this area if a later audit shows persistent under-activation
  that lighter routing guidance cannot fix

**What to do instead**

Use clearer examples and command-family selection help in the repo's secondary
entry surfaces.

## Final Handoff

Session 9 verified that this recommendations package is consistent with
`docs/ongoing-projects/agent-skills-audit-notes.md` and
`docs/ongoing-projects/agent-skills-comparison-matrix.md`.

Final consistency result:

- The evidence cited here matches the strengths, gaps, and constraints recorded
  in the notes and matrix
- Every candidate is classified exactly once as adopt now, backlog, or reject
- No concrete citation gap or contradiction required reopening discovery
- The package is implementation-ready as written, with a clear execution order
  for the three adopt-now items

Recommended maintainer handoff:

- Treat this file as the decision source of truth
- Use the implementation order already defined in this document
- Treat backlog and reject sections as durable boundaries unless new evidence
  materially changes the portability, maintenance, or workflow tradeoff
