# Agent Skills Audit Notes

## Audit Metadata

- Date: 2026-04-09
- External repo: `agent-skills/`
- Internal repo: `apex-spec-system-open`
- Purpose: Capture evidence-backed audit notes before drafting the comparison matrix and final recommendations.

## Session 1: Root Model and Lifecycle Mapping

### Scope

This session covered the external repo's root operating model, lifecycle
framing, command surface, and agent-routing behavior.

### Sources Reviewed

- `agent-skills/README.md`
- `agent-skills/AGENTS.md`
- `agent-skills/.claude/commands/spec.md`
- `agent-skills/.claude/commands/plan.md`
- `agent-skills/.claude/commands/build.md`
- `agent-skills/.claude/commands/test.md`
- `agent-skills/.claude/commands/review.md`
- `agent-skills/.claude/commands/code-simplify.md`
- `agent-skills/.claude/commands/ship.md`

### Evidence Summary

#### Root operating model

- The repo presents a six-stage lifecycle: Define, Plan, Build, Verify,
  Review, Ship. `agent-skills/README.md` places each stage in a single linear
  diagram and maps it to a slash command surface.
- The public command surface is intentionally compact: `/spec`, `/plan`,
  `/build`, `/test`, `/review`, `/code-simplify`, and `/ship` in
  `agent-skills/README.md`.
- The command files in `agent-skills/.claude/commands/` are thin dispatch
  stubs. Each command invokes one or more deeper skills and then states the
  expected workflow in a short numbered sequence.

#### Skill and routing model

- `agent-skills/README.md` treats slash commands as entry points and the
  underlying skills as the real implementation mechanism.
- `agent-skills/AGENTS.md` extends that model for environments without slash
  commands. It defines intent-to-skill mapping and a lifecycle mapping that an
  agent should follow internally.
- `agent-skills/AGENTS.md` is explicitly skill-first. It says the agent must
  invoke a matching skill, must not implement directly when a skill applies,
  and should treat even a small chance of skill relevance as sufficient to
  activate one.

#### Packaging and portability

- `agent-skills/README.md` is written as a multi-agent distribution surface,
  not only a repo README. It contains installation paths for Claude Code,
  Cursor, Gemini CLI, Windsurf, OpenCode, GitHub Copilot, and generic agents.
- The root layout in `agent-skills/README.md` emphasizes portability:
  `skills/`, `agents/`, `references/`, `hooks/`, `.claude-plugin/`, and
  `.claude/commands/` are all part of the stated package.

### Lifecycle Map

| Lifecycle stage | User-facing entry point | Underlying behavior | Evidence |
|-----------------|-------------------------|---------------------|----------|
| Define | `/spec` | Invoke `spec-driven-development` and save a structured spec | `agent-skills/README.md`, `agent-skills/.claude/commands/spec.md` |
| Plan | `/plan` | Invoke `planning-and-task-breakdown` and produce plan artifacts | `agent-skills/README.md`, `agent-skills/.claude/commands/plan.md` |
| Build | `/build` | Invoke `incremental-implementation` plus `test-driven-development` | `agent-skills/README.md`, `agent-skills/.claude/commands/build.md` |
| Verify | `/test` | Run TDD or Prove-It workflow, with browser validation when relevant | `agent-skills/README.md`, `agent-skills/.claude/commands/test.md` |
| Review | `/review` | Run five-axis review and pull in security/performance checks as needed | `agent-skills/README.md`, `agent-skills/.claude/commands/review.md` |
| Review extension | `/code-simplify` | Run simplification workflow on recent or specified code | `agent-skills/README.md`, `agent-skills/.claude/commands/code-simplify.md` |
| Ship | `/ship` | Run pre-launch checklist across quality, security, performance, accessibility, infra, and docs | `agent-skills/README.md`, `agent-skills/.claude/commands/ship.md` |

### Objective Strengths

- The lifecycle mental model is immediately legible. A new reader can infer the
  repo's operating sequence from the top of `agent-skills/README.md` without
  reading individual skills.
- The command surface is small enough to memorize, but still maps to distinct
  engineering stages. That reduces top-level routing complexity.
- The command stubs are intentionally thin. This keeps the command layer easy to
  inspect while pushing detailed workflow logic into specialized skills.
- `agent-skills/AGENTS.md` gives a concrete fallback model for agents that do
  not support slash commands. That improves cross-tool portability.
- The repo clearly distinguishes workflows, personas, and reusable references in
  the root documentation, which should help contributors find the right layer to
  edit.

### Objective Ambiguities Or Risks

- The lifecycle diagram shows six stages, but the public command surface has
  seven commands because `/code-simplify` behaves like a review-adjacent
  utility. This is not necessarily wrong, but it creates a minor mismatch
  between the headline lifecycle and the actual command inventory.
- `agent-skills/AGENTS.md` says to invoke a skill if there is even a "1% chance"
  it applies. That is strong enforcement, but it may increase false-positive
  skill activation if the surrounding agent does not have good intent routing.
- The README mixes command-first and skill-first mental models. It is still
  understandable, but the repo relies on the reader noticing that commands are
  only entry points and that the real behavior lives in skills.
- The repository overview in `agent-skills/AGENTS.md` still describes the repo
  as a collection of skills for Claude.ai and Claude Code, while the README
  presents a broader multi-agent portability story. This is a wording drift risk
  rather than a structural flaw.

### Early Comparison Hypotheses To Test Later

- Apex may benefit from a clearer lifecycle summary near the top of its root
  docs if the current 22-command surface feels harder to route quickly.
- Apex should only adopt stronger routing enforcement if it can do so without
  causing over-triggering across its broader command set.
- Thin command-entry documents plus deeper reusable workflow documents may be a
  transferable pattern, but only if it does not weaken apex's current
  local-first and reference-driven behavior.

### Next Session Input

Session 2 should inspect structural anatomy and reuse patterns in the external
repo, starting with:

- `agent-skills/docs/skill-anatomy.md`
- Representative lifecycle skills under `agent-skills/skills/`
- Any repeated section structure or progressive-disclosure patterns that appear
  intentional and consistent

## Session 2: Skill Anatomy and Reuse Patterns

### Scope

This session covered the external repo's documented skill anatomy model,
representative lifecycle skills, and the concrete reuse patterns that show up
in shipped skill directories.

### Sources Reviewed

- `agent-skills/docs/skill-anatomy.md`
- `agent-skills/skills/spec-driven-development/SKILL.md`
- `agent-skills/skills/planning-and-task-breakdown/SKILL.md`
- `agent-skills/skills/incremental-implementation/SKILL.md`
- `agent-skills/skills/test-driven-development/SKILL.md`
- `agent-skills/skills/code-review-and-quality/SKILL.md`
- `agent-skills/skills/idea-refine/SKILL.md`
- `agent-skills/references/testing-patterns.md`
- `agent-skills/references/security-checklist.md`
- `agent-skills/references/performance-checklist.md`

### Evidence Summary

#### Documented anatomy model

- `agent-skills/docs/skill-anatomy.md` defines a normalized skill contract:
  required frontmatter, an activation-oriented description, a stable set of
  sections, optional supporting files, and root-level references for reusable
  shared material.
- The anatomy guide is explicit that descriptions are part of skill discovery.
  It tells contributors to describe both what the skill does and when it should
  be activated, while avoiding process summaries in the description itself.
- The documented standard sections are not generic prose headings. They are
  behavior-shaping structures: `Overview`, `When to Use`, a workflow section,
  `Common Rationalizations`, `Red Flags`, and `Verification`.
- The anatomy guide treats anti-rationalization as a first-class design tool,
  not an optional flourish. It explicitly calls `Common Rationalizations` a
  distinctive part of a well-crafted skill.

#### What the shipped lifecycle skills actually do

- All five sampled lifecycle skills follow the frontmatter pattern and use
  short, trigger-focused descriptions that separate activation logic from the
  deeper workflow.
- The representative skills also converge on the same broad section pattern:
  `Overview`, `When to Use`, a named process section, `Common Rationalizations`,
  `Red Flags`, and `Verification`. The process section title changes by skill,
  but the overall shape is stable.
- The shipped lifecycle skills are not thin entry files. The sampled files are
  all long, self-contained playbooks:

| Skill | Approx. lines |
|-------|---------------|
| `spec-driven-development` | 200 |
| `planning-and-task-breakdown` | 223 |
| `incremental-implementation` | 241 |
| `test-driven-development` | 379 |
| `code-review-and-quality` | 347 |

- These files embed detailed examples, checklists, templates, and workflow
  diagrams directly in the main `SKILL.md`, which means the external repo keeps
  a large amount of operational detail at the skill-entry layer.

#### Reuse and progressive-disclosure patterns

- Cross-skill composition is explicit and name-based. For example,
  `spec-driven-development` hands implementation off to
  `incremental-implementation`, `test-driven-development`, and
  `context-engineering` instead of restating their full workflows.
- Reusable deep-dive material also exists at the repo root. The inspected
  skills point to shared references such as `references/testing-patterns.md`,
  `references/security-checklist.md`, and
  `references/performance-checklist.md`.
- Supporting files inside a skill directory are used selectively rather than
  universally. In the current tree, `idea-refine/` is the clearest example of
  the documented progressive-disclosure pattern, with `frameworks.md`,
  `examples.md`, `refinement-criteria.md`, and `scripts/idea-refine.sh`
  alongside its main `SKILL.md`.
- The net pattern is layered reuse, but not minimal entry files. The external
  repo relies on cross-skill references and shared root references while still
  keeping the core lifecycle skills highly self-contained.

### Objective Strengths

- The anatomy guide gives contributors a concrete writing contract instead of
  leaving skill structure implicit. That should reduce drift across new skills.
- Activation guidance is strong because frontmatter descriptions are treated as
  routing surfaces, not as mini-documentation dumps.
- Anti-rationalization and verification sections are modeled consistently across
  the sampled lifecycle skills, which should help counter common agent shortcut
  behavior.
- Cross-skill references appear intentional rather than incidental. The repo
  does reuse deeper skills and root references where domain-specific detail
  would otherwise be duplicated.

### Objective Ambiguities Or Risks

- `agent-skills/docs/skill-anatomy.md` recommends supporting files when
  reference material exceeds roughly 100 lines, but the sampled lifecycle
  `SKILL.md` files are 200 to 379 lines and still keep most material inline.
  That creates a visible gap between the documented anatomy target and the
  structure of the flagship shipped skills.
- Because the lifecycle skills remain long and self-contained, the external
  repo's progressive-disclosure model is only partial in practice. A reader gets
  a strong single-file workflow, but not necessarily a low-token entry point.
- The section pattern is consistent at a high level, but the process-section
  names and local conventions vary enough that the repo still depends on human
  judgment rather than strict structural normalization.

### Early Comparison Hypotheses To Test Later

- Apex may benefit from stronger normalized section contracts for command
  references even if it keeps its shared-reference architecture.
- Apex should test whether anti-rationalization and verification sections should
  become more explicit and consistent across its command references.
- Apex should not assume that the external repo's longer entry files are an
  automatic improvement. The actual gain may come from the writing contract and
  reuse cues, not from moving more content into entry files.

### Next Session Input

Session 3 should inspect transferable shared references, hooks, and packaging
patterns in the external repo, starting with:

- `agent-skills/references/`
- `agent-skills/hooks/`
- `agent-skills/.claude-plugin/`
- Any agent metadata or packaging files that affect contributor ergonomics or
  enforcement

## Session 3: Shared References, Hooks, and Packaging

### Scope

This session covered the external repo's reusable root references, hook-based
automation surfaces, packaging metadata, and portable review personas.

### Sources Reviewed

- `agent-skills/references/accessibility-checklist.md`
- `agent-skills/references/performance-checklist.md`
- `agent-skills/references/security-checklist.md`
- `agent-skills/references/testing-patterns.md`
- `agent-skills/hooks/hooks.json`
- `agent-skills/hooks/session-start.sh`
- `agent-skills/hooks/SIMPLIFY-IGNORE.md`
- `agent-skills/hooks/simplify-ignore.sh`
- `agent-skills/.claude-plugin/plugin.json`
- `agent-skills/.claude-plugin/marketplace.json`
- `agent-skills/agents/code-reviewer.md`
- `agent-skills/agents/security-auditor.md`
- `agent-skills/agents/test-engineer.md`
- `agent-skills/skills/using-agent-skills/SKILL.md`
- `agent-skills/skills/test-driven-development/SKILL.md`
- `agent-skills/skills/code-review-and-quality/SKILL.md`
- `agent-skills/skills/security-and-hardening/SKILL.md`
- `agent-skills/skills/performance-optimization/SKILL.md`
- `agent-skills/skills/frontend-ui-engineering/SKILL.md`
- `agent-skills/skills/shipping-and-launch/SKILL.md`

### Evidence Summary

#### Shared reference model

- The root `references/` directory is small and intentionally domain-focused:
  testing, security, performance, and accessibility. Each file is a reusable
  checklist or quick-reference document rather than a workflow entry point.
- These reference files are not isolated documentation. The lifecycle skills
  link out to them directly at the point where deeper domain checks matter. For
  example, `test-driven-development` points to
  `references/testing-patterns.md`, `code-review-and-quality` points to
  `references/security-checklist.md` and
  `references/performance-checklist.md`, `frontend-ui-engineering` points to
  `references/accessibility-checklist.md`, and `shipping-and-launch` points to
  all three launch-relevant checklists.
- The content style is operational rather than narrative. The inspected
  references emphasize explicit checks, commands, thresholds, anti-patterns,
  and concrete examples that can be reused across multiple skills without
  copying large blocks into each `SKILL.md`.

#### Hook and automation model

- `agent-skills/hooks/hooks.json` defines a `SessionStart` hook that runs
  `hooks/session-start.sh` on every new Claude session.
- `session-start.sh` reads `skills/using-agent-skills/SKILL.md` and injects its
  contents as a high-priority message, making the repo's discovery flowchart
  and operating rules available automatically at session start.
- The hook directory also contains a more specialized automation surface for
  `code-simplify`: `simplify-ignore.sh` filters annotated code blocks into
  placeholders before model reads, restores real content after edits, and
  documents crash recovery and known limitations in `SIMPLIFY-IGNORE.md`.
- The simplify-ignore implementation is not a toy example. It includes
  multi-event hook behavior, backup and restore logic, content hashing,
  malformed-input handling, and a dedicated test script.

#### Packaging and portability model

- `.claude-plugin/plugin.json` packages the repo as an installable Claude
  plugin with commands rooted at `.claude/commands`, while
  `.claude-plugin/marketplace.json` provides marketplace-facing metadata for
  GitHub distribution.
- The repo also ships standalone agent persona files in `agents/` for code
  review, security review, and test engineering. These are independent prompt
  assets rather than workflow skills, which makes them easier to copy into
  other tools and repositories.
- The session-start hook's injected meta-skill, `using-agent-skills`, acts as a
  central discovery and behavior layer for the whole pack. That is a packaging
  choice as much as a workflow choice because it standardizes how the pack gets
  introduced to the model.

### Objective Strengths

- The shared references are narrowly scoped, reusable, and actually consumed by
  multiple skills. That is a concrete maintenance win over repeating the same
  security, performance, testing, or accessibility guidance inline.
- The reference content is highly operational. Checklists, commands, metrics,
  and anti-patterns are easier for an agent or contributor to apply than
  abstract prose.
- The session-start hook materially reduces bootstrap ambiguity inside Claude by
  loading the discovery meta-skill automatically instead of relying on the user
  or model to remember it.
- The repo cleanly separates workflow skills from portable review personas in
  `agents/`, which strengthens reuse across environments that may not support
  the same skill or command surfaces.
- The simplify-ignore hook demonstrates a real case where automation enforces a
  workflow constraint that prose alone would not reliably protect.

### Objective Ambiguities Or Risks

- The strongest automation and packaging mechanisms in this session are
  Claude-specific. `hooks/hooks.json`, `session-start.sh`, and
  `.claude-plugin/` are useful in that ecosystem, but they do not transfer
  directly to a platform-neutral skill repo without replacement mechanisms.
- Injecting the full `using-agent-skills` meta-skill at every session start may
  improve routing consistency, but it also imposes a permanent context cost and
  assumes the receiving environment tolerates that pattern.
- The simplify-ignore system is sophisticated, but it achieves its result by
  mutating files during the session and relying on backup and restore logic.
  That adds operational complexity and recovery edge cases that may outweigh the
  value outside the narrow `/code-simplify` workflow.
- The agent persona files are portable, but they introduce another instruction
  layer alongside skills. If adopted carelessly, this pattern could fragment
  authority between workflow docs and role prompts.

### Early Comparison Hypotheses To Test Later

- Apex may benefit from a small set of reusable root references for
  verification-heavy domains, especially where the same checks are currently
  repeated across command references or supporting docs.
- Apex should evaluate whether it needs a lighter-weight, cross-agent discovery
  aid in root documentation or metadata, but not assume that session-start hook
  injection is the right mechanism.
- Apex should treat Claude-only plugin packaging and hook wiring as evidence of
  portability strategy, not as automatic implementation candidates.
- Apex should be skeptical of stateful hook machinery unless it solves a
  concrete failure mode that exists in this repo today.

### Next Session Input

Session 4 should re-baseline the internal apex spec system before any
improvement claims are made, starting with:

- `SKILL.md`
- `README.md`
- `AGENTS.md`
- `references/`
- `scripts/`
- `agents/openai.yaml`

## Session 4: Apex Baseline and Internal Model Mapping

### Scope

This session re-baselined the internal apex spec system's orchestrator,
command model, reference structure, verification surfaces, and portability
constraints before any comparison scoring.

### Sources Reviewed

- `SKILL.md`
- `README.md`
- `AGENTS.md`
- `docs/ARCHITECTURE.md`
- `docs/CONVENTIONS.md`
- `references/workflow-overview.md`
- `references/plansession.md`
- `references/implement.md`
- `references/validate.md`
- `references/audit.md`
- `references/qimpl.md`
- `scripts/analyze-project.sh`
- `scripts/check-prereqs.sh`
- `agents/openai.yaml`

### Evidence Summary

#### Root orchestrator and command model

- `SKILL.md` is the single routing surface. It carries the activation
  description, the stage model, the dispatch table, the directory contract, and
  the local-first script resolution pattern.
- The repo-level workflow is intentionally split between a narrow lifecycle and
  a broader command inventory. `SKILL.md`, `README.md`, and
  `references/workflow-overview.md` all describe a 13-command core workflow
  across three stages, while the same root files also document 9 utility
  commands for a total of 22 routed commands.
- The stage boundaries are explicit and prescriptive. `SKILL.md` and
  `references/workflow-overview.md` define required handoffs such as
  `plansession -> implement`, `updateprd -> plansession or audit`, and
  `audit -> pipeline`, with direct warnings not to skip across stages.
- `AGENTS.md` is deliberately lighter than `SKILL.md`. It gives project
  context, conventions, and layout, but not a second full routing system.
  That keeps the root orchestrator authoritative instead of splitting workflow
  logic across multiple top-level files.

#### Reference layout and documentation structure

- The repo uses a "Skill Family with Shared References" pattern as documented
  in `AGENTS.md` and `docs/ARCHITECTURE.md`: one root `SKILL.md`, one command
  definition per reference file, and a shallow directory layout.
- The `references/` directory currently contains 26 markdown files: 22 command
  references plus 4 supporting documents (`guidance.md`, `utilities.md`,
  `walkthrough.md`, `workflow-overview.md`).
- Reference normalization is real, not just aspirational. The first line of
  every file in `references/` is a level-1 heading, and `docs/CONVENTIONS.md`
  requires no YAML frontmatter, platform-neutral language, and a sub-500-line
  size target.
- `README.md` acts as the public distribution surface, while `AGENTS.md`
  focuses on agent-facing repo constraints and `docs/ARCHITECTURE.md` explains
  the design rationale. That is a clear separation of audience even though some
  workflow description is repeated.

#### Verification and enforcement model

- Apex relies on command-level rules more than shared domain checklists.
  `references/plansession.md`, `references/implement.md`,
  `references/validate.md`, and `references/audit.md` each embed strong
  behavioral rules, step-by-step procedures, and explicit no-deferral policies.
- The validation posture is especially strong in `references/validate.md`. PASS
  requires full task completion, deliverables, ASCII and LF checks, passing
  tests, success criteria, and targeted security, GDPR, and behavioral quality
  spot-checks.
- `references/implement.md` and `references/validate.md` both encode reusable
  behavioral-quality expectations, but they do so inline inside command docs
  rather than through a shared root checklist file.
- The verification model is partly automated through scripts rather than prose
  alone. `scripts/analyze-project.sh` produces deterministic JSON state facts,
  and `scripts/check-prereqs.sh` verifies environment, files, tools, and
  database signals with JSON output support.
- The same local-first script resolution pattern is repeated across command
  references and architecture docs: prefer `.spec_system/scripts/` inside the
  target project, fall back to the bundled `scripts/` directory in the skill.

#### Packaging, routing, and portability surfaces

- `README.md` positions the repo as an Agent Skill distribution and lists
  multiple installation paths, but the internal metadata surface is minimal.
  `agents/openai.yaml` only defines display metadata plus implicit invocation.
- Portability is pursued mostly through neutral content rules rather than rich
  packaging metadata. `docs/CONVENTIONS.md` bans tool-specific directives in
  reference files and treats platform-neutral wording as a project standard.
- `docs/ARCHITECTURE.md` documents a dual-platform strategy: the open repo is a
  Codex-oriented port of a separate private Claude plugin repo. That means the
  current structure intentionally optimizes for portability of content, not
  single-repo multi-platform packaging.

### Objective Strengths

- The workflow boundaries are unusually explicit. Required next steps and
  prohibited jumps are spelled out in both the orchestrator and quick
  reference, which should reduce stage-skipping errors.
- The root architecture is coherent: one orchestrator, one reference per
  command, shallow layout, and script-backed state facts. That is easier to
  maintain than a large number of peer skills with duplicated routing logic.
- Verification expectations are concrete and auditable. The inline rules around
  ASCII, LF, testing, security, GDPR, database alignment, and behavioral
  quality go well beyond a generic "run tests" instruction.
- The local-first script model is a real operational strength. It lets the same
  workflow adapt to a target project's initialized `.spec_system/` state
  without forking the skill's source instructions.
- The repo has strong convention discipline. `docs/CONVENTIONS.md` defines file
  structure, naming, encoding, and testing expectations tightly enough that new
  reference files and scripts have a visible contract to follow.

### Objective Ambiguities Or Risks

- The "13-command workflow" headline is accurate only for the staged lifecycle.
  The actual routed command inventory is 22. A new reader has to reconcile the
  lifecycle model with the larger command surface by reading closely.
- Verification is strong, but much of it is embedded inline in large command
  references. That can make cross-command quality guidance harder to reuse or
  update consistently than a shared checklist model.
- `AGENTS.md` is intentionally concise, but it provides less explicit
  activation and routing help than the main `SKILL.md`. In environments that
  lean more heavily on agent-instruction files than on the skill entry file,
  that may reduce discoverability.
- The dual-platform story is documented, but packaging remains fragmented across
  separate repositories. Portability is achieved by manual content conversion
  rules rather than a single shared packaging mechanism.

### Internal Constraints That Must Not Be Weakened

- Preserve the core session-sizing model: `1 session = 1 spec = 2-4 hours
  (12-25 tasks)` from `SKILL.md`, `README.md`, and `AGENTS.md`.
- Preserve the staged workflow boundaries and mandatory handoffs documented in
  `SKILL.md` and `references/workflow-overview.md`.
- Preserve the single-orchestrator plus shared-reference architecture described
  in `AGENTS.md` and `docs/ARCHITECTURE.md`.
- Preserve local-first script resolution and script-backed state facts from
  `scripts/analyze-project.sh`, `scripts/check-prereqs.sh`, and the command
  references that depend on them.
- Preserve ASCII-only, LF-only, and platform-neutral reference-file rules from
  `docs/CONVENTIONS.md`.

### Early Comparison Hypotheses To Test Later

- The external repo may outperform apex more in reusable quality-reference
  packaging than in lifecycle rigor, because apex already has stronger stage
  boundaries and validation gates than many lightweight skill packs.
- Any recommendation to simplify the apex command surface must be tested
  against a real routing benefit, because the current specialization appears
  intentional and tightly coupled to the session workflow.
- The most plausible improvement area is likely discoverability and reuse
  consistency, not replacing apex's orchestrator-centered model.

### Next Session Input

Session 5 should build the criterion-by-criterion comparison matrix using the
evidence now captured for both repos, starting with:

- `docs/ongoing-projects/agent-skills-audit-notes.md`
- `docs/ongoing-projects/agent-skills-audit-plan.md`
- The audit rubric and workstreams in the project plan
