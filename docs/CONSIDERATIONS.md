# Considerations

> Institutional memory for AI assistants. Updated between phases via /carryforward.
> **Line budget**: 600 max | **Last updated**: Phase 04 (2026-03-09)

---

## Active Concerns

Items requiring attention in upcoming phases. Review before each session.

### Technical Debt
<!-- Max 5 items -->

- [P04] **DB column cc_response preserved**: SQLite column name kept as `cc_response` for backward compatibility with existing databases; only Python variable names were renamed to `agent_response`. Future migration could unify naming.
- [P02] **Near-limit reference files**: Several reference files at 498-499 lines against a 500-line cap. Any future edits risk exceeding the limit; monitor line counts on changes.
- [P04] **n8n-workflow archive contains Claude Code references**: The `n8n-workflow/` directory still has Claude Code language. Out of scope (archived), but could confuse future contributors.

### External Dependencies
<!-- Max 5 items -->

- [P04] **Codex CLI skill system evolving**: Invocation patterns and Agent Skills standard may change. Monitor agentskills.io and openai/codex changelog for breaking changes.
- [P03] **Skills catalog PR #244 pending**: Submission to openai/skills `.experimental/` tier awaits maintainer review. Promotion to `.curated/` tier requires community adoption.

### Performance / Security
<!-- Max 5 items -->

- [P04] **Subprocess timeout hardcoded at 1800s**: `execute_codex()` enforces a 30-minute timeout. May need tuning for long-running sessions or reducing for faster failure detection.

### Architecture
<!-- Max 5 items -->

- [P04] **Natural language prompt invocation**: Codex exec uses `"Run the apex-spec skill command /{cmd}"` pattern. If Codex CLI adds structured skill invocation, prompts should migrate.
- [P04] **Cross-platform unification opportunity**: A single CLI that drives either Claude Code or Codex CLI based on config is a potential future direction. Current code is Codex-only.
- [P04] **config.yaml for agent settings, .env for API keys**: Agent binary/flags live in `config.yaml` codex section; API keys stay in `.env`. Mixing these causes confusion.

---

## Lessons Learned

Proven patterns and anti-patterns. Reference during implementation.

### What Worked
<!-- Max 15 items -->

- [P01] **Exemplar-driven batch transformation**: When one file is fully converted, the rest go fast using the same pattern. Establish the exemplar first, then batch.
- [P01] **Template condensation for trimming**: Condensing templates to skeleton form is more effective than removing sections when hitting line limits.
- [P01] **Systematic grep verification**: Run grep across all files after batch conversions to catch stray tool directives and stale references.
- [P02] **File-by-file cross-reference audit**: Systematic audits catch stale paths that ad-hoc checking misses.
- [P02] **Thin-reference CLAUDE.md**: Having CLAUDE.md point to AGENTS.md avoids duplication and keeps them aligned.
- [P03] **Fail-fast CI pattern**: Running tests before release creation prevents broken releases from being published.
- [P03] **Symlink simulation for catalog testing**: Simulating catalog installation via symlink catches packaging issues before submission.
- [P03] **Use current version, not spec's target**: Version drift between spec creation and implementation is normal; always use the actual current version.
- [P04] **Two-layer session approach**: Separating mechanical renaming (Session 01) from prompt rewriting (Session 02) keeps sessions focused and avoids complexity bleed.
- [P04] **Systematic cataloging before rewriting**: Cataloging all 18 occurrences across 6 prompt sections before editing prevents missed references.
- [P04] **Parametrized tests across all commands**: Testing `build_codex_prompt()` for all 13 KNOWN_COMMANDS with parametrize catches regressions efficiently with minimal code.
- [P04] **Grep audit as final validation**: Essential for catching stale references in test fixtures, archived files, and documentation.
- [P04] **Read full file before documentation edits**: Documentation-only sessions maintain narrative coherence when the entire file is read first.

### What to Avoid
<!-- Max 10 items -->

- [P01] **Context window language is deeply embedded**: Autonomous session commands embed context window references throughout; replacing them requires careful, section-by-section work.
- [P02] **Ad-hoc cross-reference checking**: Too easy to miss stale paths. Always do systematic file-by-file audits.
- [P04] **Inconsistent slash-command removal**: Must remove /commandname syntax from both prose AND embedded code blocks. Removing only from prose leaves confusing inconsistencies.

### Tool/Library Notes
<!-- Max 5 items -->

- [P01] **sed pipelines for batch transformation**: Effective for mechanical find-and-replace across multiple files when the pattern is well-defined.
- [P04] **Codex exec natural language prompts**: Skill invocation works by referencing the command name naturally, not via structured syntax.
- [P03] **openai/skills catalog**: `.experimental/` tier uses directory-based submission; mirror released files exactly, exclude dev artifacts.

---

## Resolved

Recently closed items (buffer - rotates out after 2 phases).

| Phase | Item | Resolution |
|-------|------|------------|
| P04 | Orchestrator SKILL.md dispatch pattern untested | Full regression across all 26 reference files + catalog submission validated the pattern |
| P04 | Script path resolution strategy needs validation | Validated through P01-P03 regression and release workflow; local-first fallback works |
| P04 | Progressive disclosure behavior unverified in Codex CLI | All 26 reference files tested during P02-P03 regression; progressive disclosure functional |
| P04 | MANAGER/SUMMARIZER prompts reference Claude Code | Rewrote all prompt constants in P04 Session 02; zero Claude Code refs in runtime code |
| P04 | README-apex-infinite-cli.md references Claude Code | Updated all documentation to Codex CLI in P04 Session 03 |

---

*Auto-generated by /carryforward. Manual edits allowed but may be overwritten.*
