# Session Specification

**Session ID**: `phase00-session01-config-and-renderer-boundary`
**Phase**: 00 - Apex Infinite CLI Upgrade
**Status**: Not Started
**Created**: 2026-07-02

---

## 1. Session Overview

This session creates the UI configuration and rendering boundary for
`apex-infinite-cli/` without changing the autonomous workflow contract. It adds
validated UI settings, independent theme tokens, CLI overrides, and renderer
helpers that can be tested with injected Rich consoles.

It is next because Phase 00 has no completed sessions and every later console,
subprocess visibility, history, and event-stream session depends on a stable
display boundary. The work preserves manager prompt routing, SQLite schema
compatibility, Codex subprocess return semantics, and raw durable history data.

The session delivers the smallest testable split: one focused UI helper module,
minimal wiring in `apex_infinite.py`, tracked config defaults, focused tests,
and README updates for the new operator-facing controls.

---

## 2. Objectives

1. Add validated UI settings resolution for config, environment constraints,
   CLI flags, and built-in defaults.
2. Create renderer helpers with injected `Console` support and semantic display
   methods for current CLI output paths.
3. Wire `--theme`, `--plain`, `--ascii`, and `--compact` without changing
   prompt, manager routing, DB schema, or subprocess output semantics.
4. Prove through tests that plain fallback, invalid config, renderer output,
   and SQLite history isolation behave correctly.

---

## 3. Prerequisites

### Required Sessions

- None - this is the first executable Phase 00 session.

### Required Tools Or Knowledge

- Python 3.10+ CLI development with Click, Rich, PyYAML, SQLite, and pytest.
- Current prompt/routing compatibility tests in
  `apex-infinite-cli/tests/test_prompts.py`.
- Current CLI boundaries in `apex-infinite-cli/apex_infinite.py`.

### Environment Requirements

- Development dependencies from `apex-infinite-cli/requirements.txt` and
  `apex-infinite-cli/requirements-dev.txt`.
- No graphical runtime dependencies for the base CLI.
- Root-authored and CLI-authored files remain ASCII-only with Unix LF endings.

---

## 4. Scope

### In Scope (MVP)

- Operator can configure `ui.theme`, `ui.effect_level`, `ui.ascii`,
  `ui.compact`, `ui.show_elapsed`, `ui.show_provider`, and validated
  `ui.themes` overrides in `apex-infinite-cli/config.yaml`.
- Operator can pass `--theme`, `--plain`, `--ascii`, and `--compact` through
  the Click CLI.
- Developer can test renderer output using injected Rich
  `Console(record=True, width=...)` objects.
- CLI renders startup, iteration, manager decision, prompt preview, Codex
  execution result, DB/history, interrupt, help, completion, timeout, and error
  states through renderer helpers.
- CLI keeps ANSI escapes, Rich markup, box glyphs, theme tokens, and styled
  display strings out of SQLite history rows.
- README documents the new UI config keys and CLI flags at the same time the
  behavior lands.

### Out Of Scope (Deferred)

- Full retro operator-console redesign - Reason: Session 02 owns the rich
  visual console once this boundary exists.
- Live Codex subprocess display changes - Reason: Session 03 owns live
  subprocess visibility and must preserve captured output semantics.
- Public JSONL event stream or wrapper event API - Reason: Session 04 owns the
  machine-readable event boundary.
- Linux graphical wrapper code or dependencies - Reason: Sessions 06 and 07 own
  optional wrapper spike and productization.
- Prompt contract changes - Reason: UI work must not change manager routing
  unless prompt tests and docs are updated in the same explicit session.
- SQLite schema migrations - Reason: this session only verifies raw history
  isolation and preserves the legacy `cc_response` column.

---

## 5. Technical Approach

### Architecture

Create `apex-infinite-cli/apex_infinite_ui.py` as the focused boundary for UI
settings, theme tokens, glyph sets, validation, and renderer helpers. Keep
workflow, LLM, DB, and subprocess behavior in `apex_infinite.py`, but replace
direct `console.print` display paths with renderer calls where the current code
already emits operator-facing output.

Use standard-library data structures and Rich primitives already available in
the runtime dependency set. The resolver reads the existing loaded config dict,
the new CLI option values, environment constraints such as `NO_COLOR` and
`TERM=dumb`, and the injected console's terminal capability. Invalid explicit
theme or custom theme configuration fails fast through Click/config errors;
environment constraints select plain output only when the operator did not
explicitly force a theme.

Tests should assert semantic labels, plain/ascii fallbacks, width behavior, and
raw DB inputs instead of brittle full-frame snapshots. Prompt constants,
`build_codex_prompt()`, `aggregate_history()`, path normalization, timeout text,
return values from `execute_codex()`, and the SQLite schema are compatibility
boundaries.

### Design Patterns

- Focused helper module: lowers single-file pressure while avoiding a broad
  application rewrite.
- Injectable renderer: allows recorded-console tests and avoids coupling tests
  to the global `console`.
- Resolver plus immutable token maps: keeps user config validation separate
  from display rendering.
- Semantic renderer methods: lets later sessions improve layout without
  changing workflow logic.
- Raw-data boundary tests: prove display strings do not leak into durable
  SQLite history.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/apex_infinite_ui.py` | UI setting resolver, theme tokens, glyph sets, lifecycle snapshot helpers, and renderer methods | ~350 |
| `apex-infinite-cli/tests/test_ui_config.py` | Config, CLI override, environment fallback, and invalid theme tests | ~220 |
| `apex-infinite-cli/tests/test_cli_options.py` | Click option parsing and startup wiring tests for new UI flags | ~180 |
| `apex-infinite-cli/tests/test_renderer.py` | Renderer semantic, width, ascii/plain, and history safety tests | ~240 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/apex_infinite.py` | Import UI helpers, add Click flags, instantiate renderer, and route existing output through renderer helpers | ~220 |
| `apex-infinite-cli/config.yaml` | Add default `ui` section with documented built-in values | ~25 |
| `apex-infinite-cli/README_apex-infinite-cli.md` | Document new UI config keys, flags, precedence, and fallback behavior | ~80 |
| `apex-infinite-cli/tests/conftest.py` | Add shared fixtures only if needed for temp DB, config files, or recorded consoles | ~60 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] `--theme`, `--plain`, `--ascii`, and `--compact` are accepted by Click and
      affect resolved UI settings.
- [ ] Built-in themes `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and `plain`
      are represented as independent Python token definitions.
- [ ] `auto` resolves to styled output for capable interactive consoles and to
      plain output under `NO_COLOR`, `TERM=dumb`, non-TTY output, redirected
      output, or non-terminal Rich consoles.
- [ ] Invalid explicit theme names and malformed `ui.themes` values fail fast
      with clear Click/config errors.
- [ ] Current `--history`, `--dry-run`, direct execution, interrupt, help,
      completion, timeout, and non-zero exit display paths still function.

### Testing Requirements

- [ ] Existing prompt/routing tests pass unchanged.
- [ ] New resolver tests cover defaults, config values, CLI overrides,
      `NO_COLOR`, `TERM=dumb`, non-terminal consoles, custom themes, and
      invalid values.
- [ ] New Click tests cover all four new flags and relevant invalid option
      combinations.
- [ ] Renderer tests use injected `Console(record=True, width=...)` at 80, 100,
      and 120 columns.
- [ ] History tests prove SQLite rows receive raw agent/manager values only,
      without ANSI escapes, Rich markup, frame glyphs, or renderer labels.

### Non-Functional Requirements

- [ ] No new graphical runtime dependency is added to the base CLI.
- [ ] Existing SQLite databases remain readable without migration.
- [ ] Prompt constants and command-routing behavior remain unchanged unless a
      failing compatibility test proves an intentional update is required.
- [ ] Plain and ASCII modes emit only ASCII output for changed renderer paths.
- [ ] Critical states remain visible in styled, plain, ASCII, and compact modes.

### Quality Gates

- [ ] All files ASCII-encoded
- [ ] Unix LF line endings
- [ ] Code follows project conventions
- [ ] `pytest tests/ -v` passes from `apex-infinite-cli/`
- [ ] `black --check apex_infinite.py apex_infinite_ui.py tests/` passes from
      `apex-infinite-cli/`
- [ ] `pylint apex_infinite.py apex_infinite_ui.py` passes from
      `apex-infinite-cli/`

---

## 8. Implementation Notes

### Working Assumptions

- This session is path-scoped to `apex-infinite-cli/`: the analysis script
  reports `monorepo: false`, the master PRD says no formal workspace manager is
  configured, and Phase 00 stubs target the CLI subproject by path.
- A separate `apex_infinite_ui.py` module is the safest boundary: the current
  CLI already has direct `console.print` calls across config, history, LLM
  retry, subprocess, and loop code, while `CONVENTIONS.md` prefers helper
  extraction when it lowers risk and improves testability.
- README updates are included now even though a later docs session exists:
  `CONVENTIONS.md` requires docs to move with user-facing flags and config
  behavior, while Session 05 can still own broader samples, runbooks, and
  polish.

### Conflict Resolutions

- Stub wording allows a renderer module or an internal renderer section. The
  chosen interpretation is a small separate module because it directly supports
  injected-console tests and avoids adding more responsibilities to the
  single-file CLI.
- UI precedence states both that environment constraints select plain output
  and that an explicit `--theme` may opt back into color under constrained
  environments. The chosen interpretation is: `--plain` always forces plain;
  otherwise an explicit `--theme` can override environment-driven plain fallback
  when tests document the behavior.

### Key Considerations

- Keep `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, and
  `build_codex_prompt()` stable.
- Preserve `cc_response`, path normalization, and raw history values.
- Keep `execute_codex()` return values and stdout/stderr fallback semantics
  stable.
- Do not copy source, QML, shader code, assets, fonts, icons, resource
  manifests, profile data, or literal constants from `EXAMPLE/cool-retro-term`.
- Do not introduce PySide6, PyQt, qmltermwidget, QTermWidget, or any graphical
  dependency to the base CLI.

### Potential Challenges

- Broad output routing could become a rewrite: limit changes to display calls
  and keep workflow logic in place.
- Renderer tests can become brittle: assert semantic sections, labels, and
  absence of forbidden sequences instead of exact frames.
- Environment and console capability can be hard to simulate: use injected
  consoles, monkeypatched environment variables, and temporary streams.
- Raw history pollution can be subtle: test `db_log()` inputs and stored rows
  with styled renderer output nearby but not persisted.

### Relevant Considerations

- [P00] **Single-file CLI pressure**: Extract UI helpers because this session
  touches many output paths and needs independent tests.
- [P00] **UI config gap**: Add a single resolver before visual polish.
- [P00] **Prompt contract coupling**: Keep prompt text and routing tests stable.
- [P00] **History compatibility**: Preserve the legacy column and raw stored
  facts.
- [P00] **Plain-output safety**: Cover constrained output defaults in tests.
- [P00] **Critical-state visibility**: Keep help, completion, interrupts,
  timeouts, DB notices, and non-zero exits visible in every mode.
- [P00] **Clean-room visual translation**: Use independent tokens and labels
  only.

### Behavioral Quality Focus

Checklist active: Yes
Top behavioral risks for this session:
- Invalid or malformed UI config silently falling back and hiding operator
  mistakes.
- Styled output or renderer-only labels leaking into SQLite history rows.
- Compact, plain, or ASCII modes hiding critical workflow states or errors.

---

## 9. Testing Strategy

### Unit Tests

- Test UI setting defaults, built-in theme names, custom theme validation,
  invalid config errors, environment constraints, and CLI override precedence in
  `apex-infinite-cli/tests/test_ui_config.py`.
- Test renderer methods with injected recorded consoles at 80, 100, and 120
  columns in `apex-infinite-cli/tests/test_renderer.py`.
- Test `build_codex_prompt()` and existing prompt constants remain covered by
  `apex-infinite-cli/tests/test_prompts.py`.

### Integration Tests

- Use Click `CliRunner` in `apex-infinite-cli/tests/test_cli_options.py` for
  new flag parsing, dry-run startup, history mode, and invalid option handling.
- Use temporary DB paths or monkeypatched `DB_DIR` and `DB_PATH` to verify
  history display and raw storage without touching a real user database.

### Runtime Verification

- Run from `apex-infinite-cli/`:
  `pytest tests/ -v`
- Run from `apex-infinite-cli/`:
  `black --check apex_infinite.py apex_infinite_ui.py tests/`
- Run from `apex-infinite-cli/`:
  `pylint apex_infinite.py apex_infinite_ui.py`
- Run representative dry-run commands with `--plain`, `--ascii`, `--compact`,
  and `--theme plain` to confirm startup output and prompt routing remain
  readable.

### Edge Cases

- `NO_COLOR` set with no explicit theme.
- `NO_COLOR` set with explicit `--theme crt-green`.
- `TERM=dumb`.
- Non-terminal or redirected output.
- Empty history table.
- Long legacy `cc_response` history rows.
- Invalid `ui.theme`.
- Malformed `ui.themes` values.
- `--plain` combined with `--theme`.
- ASCII mode with status labels, borders, and fallback glyphs.

---

## 10. Dependencies

### Other Sessions

- Depends on: none.
- Depended by: `phase00-session02-rich-operator-console`,
  `phase00-session03-subprocess-and-history-visibility`, and
  `phase00-session04-event-stream-boundary`.

---

## Next Steps

Run the `implement` workflow step to begin implementation.
