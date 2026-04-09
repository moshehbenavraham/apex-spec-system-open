# Agent Skills Comparison Matrix

## Audit Metadata

- Date: 2026-04-09
- Session: Session 5 - Criterion-by-Criterion Comparison Matrix
- External repo: `agent-skills/`
- Internal repo: `apex-spec-system-open`
- Purpose: Compare both repos against the audit rubric using file-backed
  evidence before filtering recommendations.

## Scoring Model

Scores are evidence-based and relative to the audit objective, not a generic
quality score.

- `5` = strong and explicit
- `4` = solid with minor tradeoffs
- `3` = adequate but uneven
- `2` = weak or inconsistent
- `1` = missing or materially deficient

## Non-Negotiable Apex Constraints

Any later recommendation must preserve these internal constraints established in
Session 4:

- `1 session = 1 spec = 2-4 hours (12-25 tasks)`
- Explicit staged handoffs across the core workflow
- Single-orchestrator plus shared-reference architecture
- Local-first script resolution and script-backed state facts
- ASCII-only, LF-only, and platform-neutral file rules

## Matrix

| Criterion | Why It Matters | `agent-skills` | `apex-spec-system-open` | Evidence | Comparative Assessment |
|-----------|----------------|----------------|-------------------------|----------|------------------------|
| Workflow model and lifecycle clarity | Agents need a legible operating sequence with low ambiguity. | 4 | 5 | External: `README.md`, `.claude/commands/spec.md`, `.claude/commands/build.md`, `AGENTS.md`. Internal: `SKILL.md`, `README.md`, `references/workflow-overview.md`. | `agent-skills` has a very legible six-stage lifecycle and thin command-entry stubs. Apex is stronger on mandatory handoffs and prohibited jumps, which makes stage discipline more explicit and auditable. |
| Activation and routing guidance | Better routing lowers false starts and raises workflow compliance. | 5 | 3 | External: `AGENTS.md`, `README.md`, `skills/using-agent-skills/SKILL.md`, `hooks/session-start.sh`. Internal: `SKILL.md`, `AGENTS.md`, `agents/openai.yaml`. | `agent-skills` gives a stronger fallback routing model outside slash-command environments and reinforces it with a discovery meta-skill. Apex routes well through `SKILL.md`, but its lighter `AGENTS.md` and minimal metadata give weaker non-orchestrator guidance. |
| Anatomy contract and contributor consistency | A normalized structure reduces drift when new skills or references are added. | 5 | 3 | External: `docs/skill-anatomy.md`, `skills/spec-driven-development/SKILL.md`, `skills/code-review-and-quality/SKILL.md`. Internal: `docs/CONVENTIONS.md`, `SKILL.md`, `references/`. | `agent-skills` has an explicit anatomy guide with stable sections, verification, and anti-rationalization patterns. Apex enforces file conventions and naming well, but it does not define an equally explicit section-level writing contract for command references. |
| Progressive disclosure and context economy | Lower entry-file cost matters for routing accuracy and long sessions. | 3 | 5 | External: `docs/skill-anatomy.md`, `skills/spec-driven-development/SKILL.md`, `skills/test-driven-development/SKILL.md`, `skills/idea-refine/`. Internal: `SKILL.md`, `references/`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`. | The external repo documents progressive disclosure well, but its flagship lifecycle skills stay long and self-contained. Apex applies the pattern more consistently through one orchestrator plus per-command reference files with explicit size discipline. |
| Verification rigor and quality gates | The audit values evidence, repeatability, and resistance to agent shortcut behavior. | 4 | 5 | External: `docs/skill-anatomy.md`, `skills/test-driven-development/SKILL.md`, `skills/code-review-and-quality/SKILL.md`, `skills/shipping-and-launch/SKILL.md`. Internal: `references/implement.md`, `references/validate.md`, `references/audit.md`, `scripts/analyze-project.sh`, `scripts/check-prereqs.sh`. | `agent-skills` models strong verification sections and reusable review practices. Apex is stricter overall because validation rules are explicit, pass/fail thresholds are hard, and key checks are backed by deterministic scripts instead of prose alone. |
| Reusable quality references | Shared checklists reduce duplication and make cross-cutting quality rules easier to keep aligned. | 5 | 3 | External: `references/testing-patterns.md`, `references/security-checklist.md`, `references/performance-checklist.md`, `references/accessibility-checklist.md`; also reused from `skills/test-driven-development/SKILL.md`, `skills/code-review-and-quality/SKILL.md`, `skills/shipping-and-launch/SKILL.md`. Internal: `references/validate.md`, `references/implement.md`, `references/audit.md`, `references/guidance.md`. | This is the clearest external advantage. `agent-skills` separates domain checklists into reusable root references that multiple skills consume. Apex keeps comparable expectations inline inside command docs, which is stronger for local completeness but weaker for reuse and consistent updates. |
| Automation and tooling support | Tooling can enforce behavior that prose alone cannot reliably protect. | 4 | 4 | External: `hooks/hooks.json`, `hooks/session-start.sh`, `hooks/simplify-ignore.sh`, `.claude-plugin/plugin.json`. Internal: `scripts/analyze-project.sh`, `scripts/check-prereqs.sh`, `references/qimpl.md`, `references/validate.md`. | The repos are strong in different ways. `agent-skills` uses hooks and plugin wiring to steer behavior inside Claude. Apex uses portable scripts and local-first execution to generate deterministic project facts. External automation is more opinionated; internal tooling is more portable. |
| Onboarding, packaging, and cross-agent portability | Good packaging lowers adoption cost and improves behavior across tools. | 5 | 3 | External: `README.md`, `docs/getting-started.md`, `docs/cursor-setup.md`, `docs/gemini-cli-setup.md`, `docs/opencode-setup.md`, `agents/`. Internal: `README.md`, `agents/openai.yaml`, `docs/ARCHITECTURE.md`. | `agent-skills` has the stronger public distribution surface: tool-specific install docs, plugin packaging, and portable personas. Apex intentionally favors content portability over rich packaging, but today that leaves a thinner cross-agent onboarding and metadata story. |
| Audience separation and repo ergonomics | Clear audience boundaries help maintainers change the right layer safely. | 4 | 4 | External: `README.md`, `AGENTS.md`, `docs/skill-anatomy.md`, `agents/`. Internal: `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`. | Both repos separate audiences reasonably well. `agent-skills` distinguishes commands, skills, references, and review personas. Apex distinguishes public README, agent rules, architecture, and command references. The main difference is that the external repo adds a stronger contributor-writing contract, while apex adds a stronger architecture contract. |

## Score Summary

| Criterion | `agent-skills` | `apex-spec-system-open` | Net |
|-----------|----------------|-------------------------|-----|
| Workflow model and lifecycle clarity | 4 | 5 | Apex advantage |
| Activation and routing guidance | 5 | 3 | External advantage |
| Anatomy contract and contributor consistency | 5 | 3 | External advantage |
| Progressive disclosure and context economy | 3 | 5 | Apex advantage |
| Verification rigor and quality gates | 4 | 5 | Apex advantage |
| Reusable quality references | 5 | 3 | External advantage |
| Automation and tooling support | 4 | 4 | Rough parity, different strengths |
| Onboarding, packaging, and cross-agent portability | 5 | 3 | External advantage |
| Audience separation and repo ergonomics | 4 | 4 | Rough parity, different emphasis |

## Highest-Confidence Differences

### External advantages worth carrying into Session 6

- Stronger fallback routing guidance outside the main entry surface through
  `AGENTS.md` and the `using-agent-skills` discovery layer
- A clearer anatomy contract for contributors in `docs/skill-anatomy.md`,
  especially around verification and anti-rationalization
- Better reuse of root quality references across multiple skills
- A more complete packaging and onboarding surface for multiple agent tools

### Internal advantages that should be preserved

- Stronger explicit stage boundaries and handoff enforcement
- Lower context cost through orchestrator-plus-reference-file progressive
  disclosure
- Harder validation gates backed by deterministic scripts and no-deferral rules
- Platform-neutral content conventions and local-first script execution

## Session 6 Input

Session 6 should filter differences from this matrix into three buckets:

- Adopt now: clear ROI, low ambiguity, compatible with apex constraints
- Backlog: plausible but higher effort or unresolved portability questions
- Reject: stylistic, tool-specific, or in conflict with the apex operating model

The highest-confidence candidate areas to test first are:

- richer routing/discovery guidance for non-orchestrator contexts
- a stronger writing contract for command/reference anatomy
- a small reusable root checklist layer for repeated quality gates
- better public onboarding and packaging guidance that remains platform-neutral
