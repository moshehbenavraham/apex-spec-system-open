# Session Specification

**Session ID**: `phase00-session02-rich-operator-console`
**Phase**: 00 - Apex Infinite CLI Upgrade
**Status**: Implemented
**Created**: 2026-07-03

---

## 1. Session Overview

This session turns the renderer boundary from Session 01 into the first cohesive
Rich operator console for `apex-infinite-cli/`. It improves the visible startup
panel, iteration framing, status strips, themed lifecycle states, and fallback
rendering without changing manager routing, prompt text, SQLite schema, or
Codex subprocess return semantics.

It is next because the analysis script reports Phase 00 in progress with
Session 01 completed and no active session. Session 02 is the earliest
unfinished candidate, and Sessions 03 through 08 depend on richer semantic
labels or later event and wrapper boundaries.

The work stays path-scoped to the CLI subproject. It uses the existing
`apex_infinite_ui.py` renderer and settings module as the implementation
boundary, adds focused tests for supported terminal widths and fallback modes,
and preserves the clean-room visual rule from the phase PRD.

---

## 2. Objectives

1. Deliver a coherent Rich operator-console layout for startup, iteration, and
   core lifecycle states using the existing renderer boundary.
2. Add visible status strips for provider, model, project, iteration, elapsed
   time, dry-run state, and current operation without changing workflow logic.
3. Distinguish manager decisions, prompts, agent output, DB writes, retries,
   interrupts, timeouts, help, completion, and execution failures with semantic
   labels that survive styled, plain, ASCII, and compact modes.
4. Prove through tests that output remains readable at 80, 100, and 120
   columns and that styled display data never enters SQLite history rows.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase00-session01-config-and-renderer-boundary` - Provides validated UI
      config resolution, theme tokens, glyph sets, renderer helpers, Click
      flags, and raw-history safety tests.

### Required Tools Or Knowledge

- Python 3.10+ CLI development with Click, Rich, SQLite, and pytest.
- Existing renderer contracts in `apex-infinite-cli/apex_infinite_ui.py`.
- Existing CLI loop, DB, LLM, and subprocess contracts in
  `apex-infinite-cli/apex_infinite.py`.
- Clean-room visual translation rules from the Phase 00 PRD and PRD UX.

### Environment Requirements

- CLI dependencies from `apex-infinite-cli/requirements.txt` and
  `apex-infinite-cli/requirements-dev.txt`.
- No graphical runtime dependencies for the base CLI.
- Authored files remain ASCII-only with Unix LF line endings.

---

## 4. Scope

### In Scope (MVP)

- Operator can see a compact boot/status panel that presents project, provider,
  model, config, selected theme, dry-run state, and start context.
- Operator can see stable iteration frames and status strips for provider,
  model, project, iteration, elapsed time, dry-run state, and current
  operation.
- Operator can distinguish manager decisions, Codex prompts, captured agent
  output, errors, LLM retries, interrupts, timeouts, `help`, `alldonebaby`,
  execution failures, and DB writes through centralized renderer helpers.
- Operator can use `crt-green`, `crt-amber`, `ibm-dos`, and `plain` presets
  that are independently chosen Python token definitions.
- Plain, ASCII, compact, `NO_COLOR`, `TERM=dumb`, non-terminal console, and
  constrained-width output paths remain readable and keep critical states
  visible.
- Low-fidelity scanline-like separators use independently chosen repeated
  characters and are disabled in `plain` and compact modes.
- Tests assert semantic labels, status sections, fallback behavior, width
  handling, and raw SQLite history isolation.

### Out Of Scope (Deferred)

- Live Codex subprocess progress display - Reason: Session 03 owns live
  subprocess visibility and must preserve captured-output semantics.
- History ledger redesign or `--verbose` history expansion - Reason: Session 03
  owns compact and verbose history rendering changes.
- Public JSONL event stream or wrapper event API - Reason: Session 04 owns the
  machine-readable lifecycle boundary.
- Broad runbooks, event docs, transcripts, and wrapper documentation - Reason:
  Session 05 owns documentation samples and runbooks after event behavior
  exists.
- Linux graphical wrapper code or dependencies - Reason: Sessions 06 and 07 own
  optional wrapper spike and productization.
- Prompt contract changes - Reason: display-only work must not change
  `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or
  `build_codex_prompt()`.
- SQLite schema migrations or history key changes - Reason: this session only
  renders DB write visibility and preserves raw durable data.
- Debug/admin UI surfaces - Reason: no debug surface is required; diagnostics
  belong in tests and implementation notes.

---

## 5. Technical Approach

### Architecture

Extend `apex-infinite-cli/apex_infinite_ui.py` as the display boundary created
in Session 01. Keep workflow, LLM, DB, and subprocess execution in
`apex_infinite.py`, but pass richer display snapshots into renderer methods
where the loop already knows provider, model, path, iteration, dry-run, and
operation state.

Add small data structures only where they keep renderer calls explicit and
testable. The likely shape is a run or iteration snapshot for status-strip
facts and a renderer method for DB log confirmation. The implementation should
reuse the current `StartupSnapshot`, `CodexCommandSnapshot`, `UiSettings`,
theme tokens, glyph sets, and injected `Console(record=True, width=...)`
testing pattern unless a narrow extension lowers complexity.

Keep theme presets independent. Use the PRD UX as the durable visual source of
truth for mood, hierarchy, labels, and effect categories. Do not copy source,
QML, shader code, constants, images, icons, fonts, resource manifests, profile
data, or build scripts from the local reference tree.

### Design Patterns

- Semantic renderer methods: workflow code reports facts, renderer code decides
  presentation.
- Snapshot objects: status strips remain explicit and easy to test without
  parsing terminal frames.
- Independent theme token maps: visual direction can improve without using
  external profile data.
- Fallback-first rendering: plain, ASCII, compact, and constrained outputs are
  primary paths, not afterthoughts.
- Raw-data boundary tests: verify DB writes store workflow facts only.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/tests/test_operator_console.py` | Session 02 renderer tests for boot panel, iteration frame, status strips, critical states, fallback modes, and width behavior | ~260 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/apex_infinite_ui.py` | Add richer theme tokens, status-strip and iteration-frame helpers, DB write rendering, low-effect separators, and critical-state labels | ~280 |
| `apex-infinite-cli/apex_infinite.py` | Pass run context into renderer calls and render DB write confirmation after successful log calls without changing DB data | ~90 |
| `apex-infinite-cli/tests/test_renderer.py` | Extend existing renderer and raw-history safety coverage for new console states | ~120 |
| `apex-infinite-cli/tests/test_ui_config.py` | Add preset and fallback assertions for the operator-console token behavior | ~60 |
| `apex-infinite-cli/tests/test_cli_options.py` | Add CLI smoke coverage for dry-run startup and renderer context wiring | ~60 |
| `apex-infinite-cli/README_apex-infinite-cli.md` | Add a minimal note for the richer operator console and current fallback guarantees | ~40 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] Normal interactive output presents a coherent operator-console look using
      product-facing labels only.
- [ ] Startup output shows project, provider, model, config, selected theme,
      dry-run state, and start context when available.
- [ ] Iteration output shows provider, model, project, iteration, elapsed time,
      dry-run state, and current operation without changing manager decisions
      or prompts.
- [ ] Manager decisions, prompt previews, agent output, DB writes, LLM retries,
      interrupts, help, completion, max-iteration stops, timeouts, missing
      Codex, generic errors, and non-zero Codex exits have distinct semantic
      render states.
- [ ] `plain`, `ascii`, compact, `NO_COLOR`, `TERM=dumb`, and non-terminal
      output paths remain readable and keep critical states visible.
- [ ] Low-fidelity separators are ASCII-safe and are disabled in `plain` and
      compact modes.
- [ ] No SQLite schema, stored history semantics, prompt routing, or subprocess
      return semantics change.

### Testing Requirements

- [ ] Existing prompt/routing tests pass unchanged.
- [ ] Operator-console renderer tests cover 80, 100, and 120 column widths.
- [ ] Tests cover styled, plain, ASCII, compact, `NO_COLOR`, `TERM=dumb`, and
      non-terminal fallback behavior.
- [ ] Tests prove rendered DB labels, Rich markup, ANSI escapes, box/frame
      glyphs, scanline separators, and theme tokens do not enter stored history
      rows.
- [ ] Tests cover critical states: LLM retry, JSON fallback, help, interrupt,
      completion, max iterations, timeout, missing binary, generic error, and
      non-zero Codex exit.

### Non-Functional Requirements

- [ ] No new graphical runtime dependency is added to the base CLI.
- [ ] Output remains readable at 80 columns without hiding errors, decisions,
      prompts, completion state, or safety stops.
- [ ] Built-in theme tokens remain independently chosen and do not copy
      reference profile values.
- [ ] Plain and ASCII changed paths emit only ASCII output.
- [ ] The current `--verbose`, `--history`, `--dry-run`, and direct execution
      contracts remain compatible.

### Quality Gates

- [ ] All files ASCII-encoded
- [ ] Unix LF line endings
- [ ] Code follows project conventions
- [ ] `pytest tests/ -v` passes from `apex-infinite-cli/`
- [ ] `black --check apex_infinite.py apex_infinite_ui.py tests/` passes from
      `apex-infinite-cli/`
- [ ] `pylint apex_infinite.py apex_infinite_ui.py` passes from
      `apex-infinite-cli/`
- [ ] Primary user-facing surfaces contain product-facing copy only

---

## 8. Implementation Notes

### Working Assumptions

- This session is path-scoped to `apex-infinite-cli/`: the analysis script
  reports `monorepo: false`, the master PRD says there is no formal workspace
  manager config, and `CONVENTIONS.md` names `apex-infinite-cli/` as the
  primary development target.
- Session 02 should extend the existing renderer module rather than replacing
  it: Session 01 validated `apex_infinite_ui.py`, injected consoles, config
  resolution, and Click flag wiring, and the current session objective is a
  richer console on top of that boundary.
- Minimal README updates are allowed for behavior that changes visible operator
  output: `CONVENTIONS.md` says user-facing behavior and docs should move
  together, while Session 05 still owns broader runbooks, transcripts, and
  event/wrapper documentation.

### Conflict Resolutions

- The Phase 00 current-state findings say `config.yaml` has no `ui` section,
  but Session 01 implementation and validation show the UI section now exists.
  The chosen interpretation is to trust the validated current codebase for
  planning while treating the PRD finding as historical baseline.
- Session 02 asks to distinguish DB writes, while DB schema and history
  semantics are out of scope. The chosen interpretation is to render a
  post-`db_log()` confirmation using raw facts already known by the loop, not
  to change the schema or persisted row contents.
- The folded session source lists local reference paths, while the clean-room
  rules forbid copying implementation material. The chosen interpretation is to
  use `PRD_UX.md` and the phase PRD as the durable distilled source and treat
  reference files as conceptual study material only.

### Key Considerations

- Keep prompt constants and `build_codex_prompt()` stable.
- Preserve `cc_response`, path normalization, raw DB rows, and existing SQLite
  query behavior.
- Preserve `execute_codex()` returned strings for dry-run, success,
  stderr-fallback, non-zero exit, timeout, missing binary, and generic error
  paths.
- Do not add PySide6, PyQt, qmltermwidget, QTermWidget, copied terminal
  emulators, or graphical dependencies.
- Keep visual styling operational and readable; do not hide manager reasons,
  prompts, errors, completion, DB logging, or safety stops.

### Relevant Considerations

- [P00] **Single-file CLI pressure**: Keep display changes in the renderer
  boundary and avoid broad workflow rewrites.
- [P00] **Prompt contract coupling**: Do not change manager or summarizer
  prompt text during display work.
- [P00] **History compatibility**: Preserve the legacy `cc_response` column and
  raw stored workflow data.
- [P00] **Plain-output safety**: Verify constrained output resolves to plain
  unless explicitly overridden.
- [P00] **Critical-state visibility**: Ensure help, completion, interrupts,
  timeouts, provider failures, non-zero Codex exits, DB writes, and safety stops
  remain visible in all modes.
- [P00] **Clean-room visual translation**: Do not copy third-party code,
  shaders, constants, assets, fonts, icons, profiles, or build scripts.

### Behavioral Quality Focus

Checklist active: Yes
Top behavioral risks for this session:
- Styled renderer state could leak into SQLite history if DB log rendering is
  coupled to stored row data.
- Compact or plain output could hide critical state labels that operators need
  during autonomous runs.
- Width handling could crop manager reasons, prompts, errors, or completion
  state at 80 columns.

### Potential Challenges

- Rich layout can become brittle across widths: assert semantic labels and
  required content instead of full-frame snapshots.
- Adding status-strip facts can tempt workflow rewrites: pass explicit display
  snapshots and leave manager, prompt, DB, and subprocess logic intact.
- Low-fidelity separators can become decoration: render them only when they
  carry section separation, disable them in plain and compact modes, and keep
  them ASCII-safe.

---

## 9. Testing Strategy

### Unit Tests

- Test renderer theme labels, boot/status panels, iteration frames, status
  strips, low-effect separators, and critical states in
  `apex-infinite-cli/tests/test_operator_console.py`.
- Extend UI config tests for preset token behavior and constrained fallback
  decisions in `apex-infinite-cli/tests/test_ui_config.py`.

### Integration Tests

- Extend CLI option tests to verify dry-run startup and loop context reach the
  renderer without changing prompt routing in
  `apex-infinite-cli/tests/test_cli_options.py`.
- Extend renderer safety tests to verify DB log visibility does not affect
  stored history rows in `apex-infinite-cli/tests/test_renderer.py`.

### Runtime Verification

- Run the CLI in dry-run mode for styled, plain, ASCII, and compact variants.
- Inspect recorded Rich console output at 80, 100, and 120 columns.
- Run existing prompt/routing tests to confirm display changes did not alter
  workflow command generation.

### Edge Cases

- Empty agent output, long prompt previews, long manager reasons, long project
  paths, `NO_COLOR`, `TERM=dumb`, non-terminal consoles, compact output, plain
  output, ASCII output, non-zero Codex exit, timeout, missing Codex binary,
  generic subprocess exception, help pause, operator interrupt, completion, and
  max-iteration safety stop.

---

## 10. Dependencies

### Other Sessions

- Depends on: `phase00-session01-config-and-renderer-boundary`
- Depended by: `phase00-session03-subprocess-and-history-visibility`,
  `phase00-session04-event-stream-boundary`,
  `phase00-session05-docs-samples-and-runbooks`,
  `phase00-session06-linux-wrapper-spike`,
  `phase00-session07-linux-visual-wrapper-productization`,
  `phase00-session08-release-verification`

---

## Next Steps

Run the `creview` workflow step to review and repair the implementation changes.
