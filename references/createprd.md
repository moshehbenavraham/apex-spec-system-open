# createprd

Convert a user-provided document (notes, PRD, spec, RFC, meeting notes) into the Apex Spec System master PRD at `.spec_system/PRD/PRD.md`.

Downstream workflow steps (`phasebuild`, `plansession`, `documents`) depend on this PRD as the source of truth.

This is a Stage 1 initialization command. Run it after `initspec`, or let this command run `initspec` if the spec system is missing. `createprd` requires at least one source requirements input. After `createprd`, the usual next step is `createuxprd` when UX or design inputs still need conversion; otherwise continue to `phasebuild`.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--skip-conventions` | false | Skip CONVENTIONS.md fine-tuning |

## Rules

1. **Never overwrite a real PRD** without explicit user confirmation (template placeholders can be overwritten silently)
2. **Do not invent requirements** - derive them from the source document, repo evidence, and prior artifacts only
3. **Resolve normal ambiguity with evidence-backed working assumptions** - do not turn routine gaps into a clarification loop
4. **Surface and resolve material conflicts** between inputs before writing
5. **Distinguish working assumptions from true hard blockers**
6. **ASCII-only characters** and Unix LF line endings in all output
7. **Do not create phase directories or session stubs** - that is the `phasebuild` workflow step's job
8. **CONVENTIONS.md must stay under 300 lines** - trim ruthlessly if exceeded
9. Only add conventions with clear evidence from the tech stack - no speculative additions
10. Open questions are allowed only for non-blocking decisions that genuinely need later human confirmation

### No Deferral Policy

- Read the source document, deterministic project state, and existing PRD artifacts before considering user escalation
- Ambiguity alone is not a blocker; resolve it with evidence-backed working assumptions when the PRD can still be written safely
- If inputs disagree, choose the best-supported interpretation and record the resolution when it materially shapes the PRD
- Ask the user only when the source requirements are missing entirely, overwrite confirmation is required, or a critical requirement gap would make the PRD misleading
- Successful output must not contain unresolved template placeholders, hard-blocker text, or "ask user" notes outside the `Open Questions` section

## Steps

### 1. Confirm Spec System Is Initialized

Check for `.spec_system/state.json` and `.spec_system/PRD/`. If missing, run `initspec` yourself to set up the spec system. Only ask the user if `initspec` requires user input you do not have.

### 2. Get Deterministic Project State (REQUIRED FIRST STEP)

Run the analysis script to get reliable state facts. Local scripts take precedence over bundled scripts:

```bash
if [ -d ".spec_system/scripts" ]; then
  bash .spec_system/scripts/analyze-project.sh --json
else
  bash scripts/analyze-project.sh --json
fi
```

Use the JSON output as ground truth for:
- Project name (if available)
- Current phase number
- Existing phases list (if present)

Do not parse `state.json` directly.

### 3. Collect the Source Requirements Document

This command requires at least one source requirements input in one of these forms:
- Paste the text directly into the chat
- Provide a file path in the repo to read
- Provide multiple snippets or documents when the content is split across sources

If the user provides a file path, read it. If pasted text, treat it as the source of truth.

If multiple source documents are provided, treat them as an ordered source set and carry any material contradictions into Step 5.

If no source requirements input is available, stop and ask for it. Do not attempt a no-source autonomous PRD generation pass for this command.

### 4. Decide Whether to Create or Update

Check whether `.spec_system/PRD/PRD.md` already exists.

- If it does not exist: create it
- If it exists: check if it is a template placeholder or real content

**Detecting Template Placeholder PRD**:

The `initspec` workflow step creates a placeholder PRD with bracket markers like `[Goal 1]`, `[PROJECT_DESCRIPTION]`, `[Objective 1]`, and similar placeholders. If **2 or more** such markers are present, it is a template - overwrite without confirmation.

If the PRD has real content (fewer than 2 template markers), ask for explicit user confirmation before overwriting.

**If overwriting real content (confirmation given)**:
1. Create a timestamped backup in `.spec_system/archive/PRD/` before writing
2. Then replace `.spec_system/PRD/PRD.md`

Backup naming (ASCII only):
- `.spec_system/archive/PRD/PRD-backup-YYYYMMDD-HHMMSS.md`

If overwrite is not confirmed:
- Offer to create a new file next to it for review and stop

### 5. Resolve Assumptions And Conflicts

Before normalizing requirements, explicitly resolve ambiguity that will shape the PRD.

**Materiality threshold**:
- Treat an assumption or conflict as material if it would change goals or non-goals, primary users, MVP versus deferred scope, measurable NFR targets, compliance/privacy/security posture, hosting/deployment constraints, required integrations, phase boundaries, or monorepo/package structure
- Do **not** record cosmetic wording choices, placeholder defaults, section ordering, or routine deduplication as material decisions

For each material working assumption, state:
- The assumption itself
- The source or repo evidence supporting it
- Why the PRD can proceed without user arbitration

For each material conflict between inputs, state:
- The conflicting sources
- The viable interpretations
- The chosen interpretation
- Why that interpretation is the best-supported one

Rules for this step:
- Do not invent filler assumptions just to satisfy format
- A working assumption is not a hard blocker
- Hard blockers stop the command only when source requirements are inaccessible or too incomplete to support a defensible PRD
- If an assumption or conflict resolution materially shapes the PRD, record it in the generated artifact
- Keep blocking questions out of successful artifact sections; use `Open Questions` only for non-blocking follow-up decisions

### 6. Extract and Normalize Requirements

From the source document plus resolved assumptions and conflict decisions, extract and normalize:
- **Product overview**: 1-3 paragraphs
- **Goals**: 3-7 bullets that are outcome-focused
- **Non-goals**: 3-10 bullets (explicitly out of scope)
- **Users and use cases**: primary personas and key workflows
- **Functional requirements**: grouped by area (MVP first). Write each requirement as "[Actor] can [capability] [context]" (for example, "User can reset password via email link"). Focus on WHAT, not HOW. Keep requirements implementation-agnostic.
- **Non-functional requirements**: performance, security, privacy, reliability, accessibility. Each NFR must include a specific, measurable target (for example, "API response < 200ms at p95", not "should be fast")
- **Constraints**: tech constraints, compliance, hosting, budgets, deadlines
- **Assumptions**: only evidence-backed working assumptions that materially shape the PRD
- **Risks**: major risks and mitigations
- **Success criteria**: checkboxes that can be validated
- **Open questions**: unresolved items that genuinely need later human confirmation but do not block phase planning

Important:
- Do not invent details
- If critical information is missing and cannot be inferred from the provided materials or repo evidence, ask only the minimum targeted questions needed to avoid a misleading PRD
- Keep content high-level and stable. Session-level details belong in the `plansession` workflow step
- Keep phases as planning scaffolding, not implementation plans
- Apply chosen assumptions and conflict resolutions consistently across all sections

### 7. Generate Master PRD

Create `.spec_system/PRD/PRD.md` using this template. Use straight quotes only. Use hyphens, not em-dashes. ASCII-only.

```markdown
# [PROJECT_NAME] - Product Requirements Document

## Overview

[1-3 paragraphs describing what this product is and who it is for.]

## Goals

1. [Goal]
2. [Goal]
3. [Goal]

## Non-Goals

- [Non-goal]
- [Non-goal]

## Users and Use Cases

### Primary Users

- **[Persona]**: [short description]

### Key Use Cases

1. [Use case]
2. [Use case]

## Requirements

### MVP Requirements

- [Actor] can [capability] [context]
- [Actor] can [capability] [context]

### Deferred Requirements

- [Actor] can [capability] [context]

## Non-Functional Requirements

- **Performance**: [specific measurable target, for example, "API response < 200ms at p95"]
- **Security**: [specific measurable target, for example, "OWASP Top 10 compliance"]
- **Reliability**: [specific measurable target, for example, "99.9% uptime SLA"]
- **Accessibility**: [specific measurable target, for example, "WCAG 2.1 AA"]

## Constraints and Dependencies

- [Constraint or dependency]

## Phases

This system delivers the product via phases. Each phase is implemented via multiple 2-4 hour sessions (12-25 tasks each).

| Phase | Name | Sessions | Status |
|-------|------|----------|--------|
| 00 | [PHASE_NAME] | TBD | Not Started |

## Phase 00: [PHASE_NAME]

### Objectives

1. [Objective]
2. [Objective]

### Sessions (To Be Defined)

Sessions are defined via `phasebuild` as `session_NN_name.md` stubs under `.spec_system/PRD/phase_00/`.

**Note**: This command does NOT create phase directories or session stubs. Run `phasebuild` after creating the PRD.

## Technical Stack

- [Technology] - [why]

## Success Criteria

- [ ] [Criterion]
- [ ] [Criterion]

## Risks

- **[Risk]**: [mitigation]

## Assumptions

<!-- Omit bullets if no material working assumptions remain -->
- [Working assumption]: [Supporting evidence and why it is safe to proceed]

### Conflict Resolutions

<!-- Omit subsection if no material conflicts were resolved -->
- [Conflict]: [Chosen interpretation and supporting evidence]

## Open Questions

<!-- Include only non-blocking questions that still need human confirmation -->
1. [Question]
2. [Question]
```

Notes:
- If the project already has phases beyond Phase 00 (from state analysis), update the phases table accordingly
- Do not create phase directories here - that is the `phasebuild` workflow step's job
- Use `[PHASE_NAME]` placeholder - default to "Foundation" if not specified
- If no material working assumptions remain, omit the bullet list under `## Assumptions`
- If no material conflicts were resolved, omit the `### Conflict Resolutions` subsection rather than inventing one

### 7a. Monorepo Detection from PRD Content

**Skip this step if** `monorepo` in `state.json` is already `true` or `false` (already determined by `initspec` or a previous run).

When `monorepo` is `null` (unknown), scan for multi-package signals:

1. **Check PRD content** for signals:
   - Multiple services or applications mentioned (for example, "web app", "API server", "worker service")
   - Explicit monorepo language ("monorepo", "workspace", "packages")
   - Multiple distinct tech stacks for different components
   - References to shared libraries or cross-service code

2. **Check `monorepo_detection`** from the `analyze-project.sh --json` output (Step 2):
   - If `monorepo_detection.detected` is `true`, use it as supporting evidence

3. **If signals are found**:
   - Derive the best-supported package map from source requirements, repo layout, and script output
   - If monorepo is the best-supported interpretation, set `monorepo: true` in `state.json`, add the `packages` array, and add a Package Map section to the PRD after Technical Stack:

     ```markdown
     ## Package Map

     | Package | Path | Stack | Purpose |
     |---------|------|-------|---------|
     | web | apps/web | TypeScript | Frontend application |
     | api | apps/api | TypeScript | Backend API server |
     ```

   - If signals are mixed but one interpretation is still defensible, proceed with a recorded working assumption in `## Assumptions`
   - If no defensible package map exists yet, leave package details out of the PRD, keep `monorepo: null`, and add a non-blocking item to `## Open Questions`
   - Do not ask for confirmation only because package metadata is incomplete
   - Do not add a Package Map section unless `monorepo` is set to `true`

4. **If no signals are found**: set `monorepo: false` in `state.json`

5. **If `monorepo` remains `null`**:
   - Revisit it on the next `createprd` run with stronger evidence, or before any workflow step needs package-scoped planning or workspace-specific tooling
   - Keep downstream artifact text honest: no Package Map in the PRD and no Workspace Structure section in `CONVENTIONS.md`

### 8. Customize CONVENTIONS.md for Tech Stack

Customize `.spec_system/CONVENTIONS.md` to reflect the project's actual tech stack and domain. This is **initial customization** (more freedom to reshape) versus the `audit` workflow step, which makes surgical edits later.

#### 8.1 Detect Tech Stack

From the PRD's Technical Stack section and source requirements, identify: primary language(s), framework(s), runtime, package manager, testing framework, and project domain.

#### 8.2 Transform Generic Template

Read `.spec_system/CONVENTIONS.md` (the generic template from `initspec`). Replace generic conventions with stack-specific equivalents, add new ones required by the stack, and remove ones that do not apply. Keep each convention to 1-2 lines. No speculative additions.

**Stack-specific transformations (examples):**

| Stack | Transformations |
|-------|-----------------|
| TypeScript | Replace generic naming with TS conventions; add type safety rules; add `interface` vs `type` guidance |
| React | Add component patterns; hooks conventions; state management approach; JSX style |
| Next.js | Add App Router conventions; server/client component rules; API route patterns; file-based routing |
| Python | Replace with PEP 8; add type hint requirements; docstring format; import ordering |
| Go | Replace with Effective Go idioms; add error handling patterns; package naming; interface conventions |
| Rust | Add Clippy compliance; Result/Option patterns; ownership conventions; module organization |
| CLI | Add exit code standards; stdout vs stderr rules; flag naming; help text conventions |
| API | Add REST conventions; status code usage; error response format; versioning approach |
| Library | Add semantic versioning rules; public API stability; backwards compatibility; documentation requirements |
| Monorepo | Add Workspace Structure section (package table + cross-package rules); shared dependency rules; cross-package imports; workspace alias conventions |
| Database | Add Database Layer section: connection source, migration tool + rules, model/table naming, query safety, seed script, test DB strategy, vector/embeddings conventions (if applicable) |

**Section-specific transformations:**

| Section | Generic -> Stack-Specific |
|---------|--------------------------|
| **Naming** | Universal advice -> language-specific casing (camelCase, snake_case, PascalCase, kebab-case) |
| **Files & Structure** | Generic -> framework directory conventions (src/, app/, lib/, components/, routes/) |
| **Functions & Modules** | Universal -> language idioms (async/await, error returns, generators, decorators) |
| **Error Handling** | Generic -> stack patterns (try/catch, Result types, error boundaries, panic vs error) |
| **Testing** | Universal -> framework patterns (describe/it, pytest fixtures, table-driven tests, mocking approach) |
| **Dependencies** | Generic -> package manager commands, lockfile rules, version pinning strategy |

**Add new sections if warranted:**
- **TypeScript**: Add "Types" section for type conventions
- **React**: Add "Components" section for component patterns
- **API**: Add "Endpoints" section for API design conventions
- **Database**: Add "Database Layer" section with subsections for connection, migrations, models, queries, seeding, testing. If the PRD references vector search, embeddings, or RAG, include a "Vector / Embeddings" subsection. Detection: PRD mentions database, schema, any DB technology, migrations, ORM, data modeling, vector/embeddings, or RAG.
- **Monorepo** (if confirmed in Step 7a): Add "Workspace Structure" section with package table and cross-package rules (import aliases, shared types location, test boundaries, cross-package session scope)

#### 8.3 Enforce 300-Line Limit (STRICT)

After transformation, verify `CONVENTIONS.md` stays under **300 lines maximum**.

```bash
wc -l .spec_system/CONVENTIONS.md
```

If over 300 lines:
1. **Merge** similar conventions into single entries
2. **Prioritize** stack-specific over generic (remove generic if redundant)
3. **Condense** verbose explanations to single lines
4. **Remove** lowest-impact conventions until compliant

**Budget guidance**: The generic template is about 85 lines. You have about 215 lines for stack-specific customization. A well-customized `CONVENTIONS.md` typically lands between 120-200 lines.

#### 8.4 Validate Changes

After edits:
1. Verify the file is valid markdown
2. Confirm line count <= 300
3. Ensure no duplicate sections were created
4. Confirm ASCII-only characters

```bash
wc -l .spec_system/CONVENTIONS.md
LC_ALL=C grep -n '[^[:print:][:space:]]' .spec_system/CONVENTIONS.md && echo "Non-ASCII found"
```

#### 8.5 Skip Conditions

Skip this step entirely if:
- `.spec_system/CONVENTIONS.md` does not exist
- No tech stack was identified from the requirements
- User explicitly requests `--skip-conventions`

### 9. Validate Output

Before reporting completion, run both encoding and content quality checks.

#### 9.1 Encoding Validation

- Confirm the file exists at `.spec_system/PRD/PRD.md`
- Confirm it is ASCII-only and uses LF line endings

```bash
file .spec_system/PRD/PRD.md
grep -n "$(printf '\r')" .spec_system/PRD/PRD.md && echo "CRLF found"
LC_ALL=C grep -n '[^[:print:][:space:]]' .spec_system/PRD/PRD.md && echo "Non-ASCII found"
```

If checks fail, fix the PRD content and re-check.

#### 9.2 Content Quality Validation

Scan the generated PRD for common quality issues. For each check, fix inline if possible or flag it to the user:

| Check | What to look for | Action |
|-------|------------------|--------|
| Template placeholders | Bracket markers like `[Goal 1]`, `[Requirement]`, `[Actor]` remaining in output | Replace with real content or remove |
| Vague NFRs | NFRs without specific numbers (for example, "should be fast", "highly available") | Rewrite with measurable targets |
| Empty sections | Sections with no content below the heading | Fill in or ask the minimum required follow-up |
| Weak requirements | Requirements that describe HOW (implementation) rather than WHAT (capability) | Rewrite in actor/capability form |
| Invented assumptions | Assumptions without source or repo evidence | Remove or convert to a non-blocking open question |
| Unresolved conflicts | Different sections imply incompatible interpretations | Normalize to one interpretation and record it under `Conflict Resolutions` |
| Missing sections | Any required section from the template entirely absent | Add the section |

Report any issues found and fixed in the output summary.

## Output

Report to the user:

```text
createprd complete!

Created:
- .spec_system/PRD/PRD.md (master PRD)
[If backup was made:]
- Backup: .spec_system/archive/PRD/PRD-backup-YYYYMMDD-HHMMSS.md

Summary:
- Goals: N defined
- MVP Requirements: N items
- Non-Goals: N items
- Working Assumptions: N recorded
- Conflict Resolutions: N recorded
- Open Questions: N items

[If conventions were customized:]
Conventions:
- .spec_system/CONVENTIONS.md customized for [stack] (N/300 lines)
- Key additions: [brief list, max 3]

[If monorepo was determined:]
Monorepo: [true - N packages detected | false - single-repo confirmed | null - evidence insufficient]
[If monorepo true:]
- Package Map added to PRD
- Workspace Structure added to CONVENTIONS.md

[If quality issues were found and fixed:]
Quality:
- N issues auto-fixed (template placeholders, vague NFRs, invented assumptions, etc.)

[If quality issues remain for the user:]
Quality:
- N issues need user input: [brief list]
```

## Next Action

If UX or design source material still needs to be converted into a PRD artifact, run `createuxprd`.

Otherwise run `phasebuild` to define the first phase's session stubs.
