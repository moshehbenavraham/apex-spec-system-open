# PRD Phase 00: Apex Infinite CLI Upgrade

**Status**: Not Started
**Sessions**: 8 (initial estimate)
**Estimated Duration**: 8-16 days

**Progress**: 0/8 sessions (0%)

---

## Overview

Phase 00 upgrades `apex-infinite-cli/` from a functional autonomous workflow
runner into a polished, testable operator console and optional Linux visual
wrapper path. The phase preserves manager routing, prompt contracts, SQLite
compatibility, and Codex subprocess semantics while adding a renderer/config
boundary, Rich-based operator views, better subprocess and history visibility,
a raw lifecycle event stream, documentation, wrapper spike/productization, and
release verification.

---

## Progress Tracker

| Session | Name | Status | Est. Tasks | Validated |
|---------|------|--------|------------|-----------|
| 01 | Config And Renderer Boundary | Not Started | ~18 | - |
| 02 | Rich Operator Console | Not Started | ~18 | - |
| 03 | Subprocess And History Visibility | Not Started | ~18 | - |
| 04 | Event Stream Boundary | Not Started | ~18 | - |
| 05 | Docs Samples And Runbooks | Not Started | ~16 | - |
| 06 | Linux Wrapper Spike | Not Started | ~18 | - |
| 07 | Linux Visual Wrapper Productization | Not Started | ~18 | - |
| 08 | Release Verification | Not Started | ~16 | - |

---

## Completed Sessions

None yet.

---

## Upcoming Sessions

- Session 01: Config And Renderer Boundary
- Session 02: Rich Operator Console
- Session 03: Subprocess And History Visibility
- Session 04: Event Stream Boundary
- Session 05: Docs Samples And Runbooks
- Session 06: Linux Wrapper Spike
- Session 07: Linux Visual Wrapper Productization
- Session 08: Release Verification

---

## Objectives

1. Centralize UI configuration and operator-facing rendering without changing
   workflow behavior.
2. Deliver the first cohesive Rich-based terminal console with robust plain,
   ASCII, compact, and constrained-terminal fallbacks.
3. Improve long-running Codex execution and history visibility while preserving
   raw captured output semantics and SQLite compatibility.
4. Expose lifecycle facts through an opt-in JSONL event stream for future
   renderers and wrappers.
5. Document the implemented controls, fallback behavior, clean-room visual
   boundary, and wrapper interface.
6. Spike and productize the optional Linux visual wrapper without adding
   graphical dependencies to the base CLI.
7. Verify the complete upgrade against compatibility, testing, documentation,
   release, and clean-room criteria.

---

## Prerequisites

- Spec system initialized for the Apex Infinite CLI scope.
- Master PRD defines Phase 00 as the next not-started phase.
- The folded source plan archive in this Phase 00 PRD and the session
  stubs define the full 8-session upgrade scope.
- `apex-infinite-cli/` baseline behavior and prompt-routing tests are the
  compatibility reference for this phase.
- `EXAMPLE/cool-retro-term` remains reference-only and ignored by Git.

---

## Planning Assumptions And Resolutions

### Working Assumptions

- Phase 00 is the next buildable phase: `.spec_system/state.json` has
  `current_phase` set to 0, no completed sessions are recorded, and the source
  upgrade plan defines 8 ordered sessions. Proceeding is safe because the user
  clarified that all 8 sessions belong in Phase 00.
- Phase 00 sessions are scoped to `apex-infinite-cli/` inside a single
  repository: the master PRD says no formal workspace manager is configured and
  `state.json` has `monorepo: false`. Session stubs therefore omit package
  metadata and name the target path in scope.
- Wrapper spike, wrapper productization, and release verification are part of
  Phase 00: the source plan defines them as Sessions 06, 07, and 08, and the
  user explicitly confirmed that Phase 00 must contain all 8 sessions.
  Proceeding is safe because the event stream boundary is ordered before the
  wrapper sessions and release verification is ordered last.

### Conflict Resolutions

- Existing `.spec_system/PRD/phase_00/PRD_phase_00.md` originally described a
  placeholder `Foundation` phase with 0 sessions, while the source upgrade plan
  defines 8 sessions. The full 8-session upgrade interpretation is chosen, and
  the placeholder phase file is replaced.
- `.spec_system/PRD/PRD.md` and `.spec_system/state.json` previously split the
  upgrade across Phase 00 and Phase 01. The user clarified that this split is
  invalid and that Phase 00 must contain all 8 sessions. The chosen
  interpretation is a single 8-session Phase 00, with stale Phase 01 tracking
  removed from PRD and state.
- The master PRD candidate list put documentation before the event stream, but
  the current session split plan puts `Event Stream Boundary` before `Docs
  Samples And Runbooks` and states that docs should describe implemented event
  behavior. The current split plan ordering is chosen so the documentation
  session can cover the shipped event stream rather than placeholders.

---

## Technical Considerations

### Architecture

Start by creating small renderer and configuration boundaries around the
current single-file CLI. Subsequent sessions should use those boundaries rather
than changing prompt routing, history storage, or subprocess semantics for
display-only reasons. The event stream should publish raw lifecycle facts that
future wrappers can consume without scraping Rich or plain human output.

### Technologies

- Python 3.10+
- Click
- Rich
- PyYAML and python-dotenv
- SQLite
- OpenAI-compatible Python client
- Codex CLI
- pytest, pytest-mock, pytest-cov, black, and pylint
- PySide6 with Qt Quick/QML as an optional Linux wrapper dependency

### Risks

- Styled output can pollute durable records: keep SQLite rows and JSONL events
  raw and cover that with tests.
- Terminal compatibility can vary: plain, ASCII, compact, `NO_COLOR`,
  `TERM=dumb`, non-TTY, redirected output, and common widths need coverage.
- Live subprocess display can change semantics: preserve stdout, stderr,
  return code, timeout, dry-run, missing-binary, generic-exception, and verbose
  behavior with focused tests.
- Clean-room visual work can drift into copied material: use the reference as a
  concept checklist only and do not copy code, shaders, assets, fonts, profile
  data, resource manifests, or build scripts.
- Single-file pressure can grow: extract helpers only when the split lowers
  risk and improves testability.
- Optional wrapper dependencies can burden base CLI users: keep PySide6 and
  graphical runtime requirements optional and isolated from base install paths.
- Release verification can uncover late compatibility regressions: keep Session
  08 focused on final checks plus small compatibility fixes only.

### Relevant Considerations

- [P00] **Renderer boundary first**: Route startup, iteration frames, manager
  decisions, prompt previews, execution results, DB notices, history,
  interrupts, and completion through renderer helpers with injected `Console`
  support.
- [P00] **Prompt contract coupling**: Keep manager and summarizer prompts stable
  unless tests and docs move with an explicit prompt-contract change.
- [P00] **History compatibility**: Preserve the legacy `cc_response` column,
  normalized project path keys, and raw stored workflow data.
- [P00] **Subprocess behavior lock**: Preserve current Codex execution result
  semantics while adding live visibility.
- [P00] **Raw durable facts only**: SQLite rows and JSONL events must not
  contain ANSI escapes, Rich markup, frame glyphs, visual tokens, secrets, or
  renderer snapshots.
- [P00] **Clean-room visual translation**: Implement independent tokens,
  labels, settings, and layouts; do not copy reference implementation material.
- [P00] **Optional wrapper obligations**: PySide6/Qt Quick/QML belongs only in
  an optional Linux visual wrapper path with license and packaging notes.
- [P00] **Wrapper as companion surface**: The wrapper must launch or reuse the
  CLI workflow engine through the event boundary.

---

## Success Criteria

Phase complete when:

- [ ] All 8 sessions completed
- [ ] Existing prompt and routing behavior remains compatible and covered by
  tests.
- [ ] Operator UI config supports built-in themes, plain mode, ASCII mode,
  compact mode, and deterministic environment fallback rules.
- [ ] Rich operator views cover startup, iteration, manager decision, prompt,
  Codex execution, results, DB writes, help, completion, interrupts, timeouts,
  and errors.
- [ ] History display is readable and backward compatible with existing SQLite
  databases.
- [ ] JSONL event stream emits raw lifecycle facts without Rich markup, ANSI
  escapes, frame glyphs, copied visual tokens, or secrets.
- [ ] README and deep-dive docs describe UI flags, config, fallback behavior,
  event stream, prompt-contract impact, clean-room boundary, and wrapper path.
- [ ] Optional Linux wrapper path is either productized with isolated
  dependencies and smoke tests or explicitly deferred by Session 07 evidence.
- [ ] Release verification traces every completion criterion to a passing
  check, shipped artifact, or explicit deferral.
- [ ] No reference source, shader, image, icon, font, resource manifest, build
  script, or literal profile data is copied into the CLI.

---

## Dependencies

### Depends On

- Initialized Apex Spec System PRD and state files.
- Existing Apex Infinite CLI baseline in `apex-infinite-cli/`.

### Enables

- Session workflow planning for `phase00-session01-config-and-renderer-boundary`
- Full Apex Infinite CLI upgrade release readiness after Session 08

---

## Folded Source Plan Archive

<!-- FOLDED_SOURCE_PLAN_ARCHIVE_START -->

This section preserves the former ongoing-project upgrade plan verbatim so the
standalone plan file can be removed without losing detail. The progress tracker
and session stubs above remain the active execution interface.

`````markdown
# Apex Infinite CLI Upgrade Plan

## Session Split Plan

### Session 01: Config And Renderer Boundary

**Objective**: Create a tested UI configuration and rendering boundary around
the current single-file CLI without changing Apex Infinite workflow behavior.

**Scope**:
- Add a bounded renderer module or internal renderer section with injected
  `Console` support for `Console(record=True, width=...)` tests.
- Define UI settings resolution for `ui.theme`, `ui.effect_level`,
  `ui.ascii`, `ui.compact`, `ui.show_elapsed`, `ui.show_provider`, and
  validated `ui.themes` overrides.
- Add Click options for `--theme`, `--plain`, `--ascii`, and `--compact`.
- Define independent theme tokens, status labels, severity labels, glyph sets,
  plain/ascii fallbacks, and a minimal internal lifecycle snapshot shape.
- Route startup, iteration banners, manager decisions, prompt previews,
  response panels, DB log notices, interrupts, completion, and history display
  through renderer helpers.
- Add tests for config defaults, Click overrides, invalid theme values,
  `NO_COLOR`, `TERM=dumb`, redirected/non-TTY output, custom theme validation,
  and SQLite history isolation.

**Outputs**:
- UI config resolver and renderer helpers for the current CLI.
- Built-in Python token definitions for `auto`, `crt-green`, `crt-amber`,
  `ibm-dos`, and `plain`, plus validated custom YAML theme overrides.
- Focused config, Click, renderer, and history-isolation tests.

**Dependencies / Notes**:
- Current evidence: `apex_infinite.py` owns Click, global `Console()`,
  SQLite, LLM calls, signal handling, notifications, and `subprocess.run()`.
- Preserve `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`,
  `build_codex_prompt()`, path normalization, timeout behavior, and the
  `cc_response` SQLite column unless a later session explicitly changes its
  contract with matching tests and docs.
- Decision: invalid `--theme`, `ui.theme`, and malformed `ui.themes` values
  fail fast with clear Click/config errors.
- Decision: `auto` resolves to `crt-green` on capable interactive TTYs and to
  `plain` for `NO_COLOR`, `TERM=dumb`, non-TTY output, redirected output, or
  `Console().is_terminal == false`, unless an explicit `--theme` opts back in.
- Assumption: start with the smallest boundary that is testable; extract a
  separate module only when it lowers risk compared with extending
  `apex_infinite.py`.

**EXAMPLE Reference Paths**:
- Study settings shape, built-in profile organization, custom profile storage,
  and validation boundaries:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`
- Study settings grouping for general, terminal, effects, and advanced
  controls:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`
- Study profile management, import/export, frame settings, and persistence UI
  concepts:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`
- Study terminal-facing configuration controls for font, rasterization, color,
  scaling, width, line spacing, frame color, and chroma:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`
- Study effects control categories for later theme/effect names:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`
- Study performance and miscellaneous settings organization:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml`
- Study settings persistence concepts only:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml`
- Study the file I/O bridge for import/export concepts only:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp`
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h`
- Study small reusable control patterns, not implementation:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ColorButton.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SimpleSlider.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/CheckableSlider.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Components/SizedLabel.qml`

**Acceptance Checks**:
- Existing prompt and routing tests pass unchanged.
- `--history`, `--dry-run`, and direct execution still function.
- No ANSI escapes, Rich markup, frame glyphs, or styled output are written to history DB rows.
- Config precedence is deterministic and documented in tests.
- Default output changes only through the renderer boundary.

### Session 02: Rich Operator Console

**Objective**: Implement the first cohesive Rich-based retro operator console experience.

**Scope**:
- Implement independently chosen `crt-green`, `crt-amber`, `ibm-dos`, and
  `plain` theme presets using the token model from Session 01.
- Redesign startup as a compact boot/status panel and replace iteration
  separators with stable iteration frames.
- Add status strips for provider, model, project, iteration, elapsed time,
  dry-run state, and current operation.
- Distinguish manager decisions, Codex prompts, agent output, errors, LLM
  retries, interrupts, timeouts, `help`, `alldonebaby`, and DB writes.
- Add low-fidelity scanline-like separators using plain repeated characters,
  with automatic disablement in `plain` and compact modes.
- Validate width handling at 80, 100, and 120 columns.

**Outputs**:
- Rich operator-console views for normal interactive runs and fallbacks.
- Themed and fallback render states for all important lifecycle outcomes.
- Renderer tests that assert semantic labels and section presence instead of brittle full-frame snapshots.

**Dependencies / Notes**:
- Depends on Session 01 renderer/config boundaries.
- Rich can translate only color mood, status hierarchy, compact framing,
  settings grouping, and low-fidelity separators from the local
  `EXAMPLE/cool-retro-term` reference.
- Do not copy reference code, profile data, colors, shaders, images, icons,
  fonts, resource manifests, or build scripts.
- Keep every visual element operational; avoid decoration that hides manager
  decisions, prompts, errors, or completion state.

**EXAMPLE Reference Paths**:
- Study top-level visual moods and README screenshots/descriptions for
  inspiration only:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/README.md`
- Study profile names and visual families as a checklist, not literal values:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`
- Study application shell, window status, actions, fullscreen, settings,
  copy/paste, zoom, and size overlay concepts:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`
- Study terminal framing, viewport composition, bloom source placement, and
  source-to-frame hierarchy for Rich layout translation:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`
- Study static frame concepts only:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml`
- Study terminal-size display behavior for compact status readouts:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml`
- Study timing concepts for elapsed/live display naming:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml`
- Study low-fidelity effect categories for Rich separators only:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`
- Study shader effect categories only; do not copy shader source, constants, or
  formulas:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag`
- Study utility color/math categories only; do not copy implementation:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/utils.js`
- Treat texture/image assets as forbidden source material while using them to
  understand what must not be copied:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png`
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png`

**Acceptance Checks**:
- Normal interactive output presents a coherent operator-console look.
- Plain, ascii, compact, `NO_COLOR`, non-TTY, and `TERM=dumb` paths remain readable.
- Narrow output does not hide errors, decisions, prompts, or completion state.
- The reference inspiration is visible in mood and structure without copied
  implementation material.

### Session 03: Subprocess And History Visibility

**Objective**: Improve operator awareness during long Codex subprocess runs while preserving captured-output semantics.

**Scope**:
- Add live elapsed subprocess display using Rich status, progress, live rendering, or an equivalent wrapper.
- If moving from `subprocess.run()` to `subprocess.Popen`, preserve
  stdout/stderr capture, timeout text, return-code handling, stderr fallback,
  `FileNotFoundError`, and generic exception reporting.
- Show command timeout, elapsed time, and process state during `codex exec`.
- Redesign `--history` as a compact ledger with command, reason, timestamp, status, and truncated response summary.
- Extend the existing `--verbose` flag to history mode instead of adding
  `--history-verbose`; verbose history shows larger response/reason detail
  while default history stays compact.
- Add fake-runner or monkeypatch tests for success, stderr-only output,
  non-zero exit, timeout, dry-run, missing binary, and generic exceptions.

**Outputs**:
- Live subprocess status display that does not leak styled output into history.
- Backward-compatible history rendering for empty, short, and long records.
- Tests for subprocess display and history formatting.

**Dependencies / Notes**:
- Depends on Session 01 renderer boundaries and should use Session 02 labels where available.
- Existing `~/.apex-infinite/history.db` files must remain readable without migration.
- The legacy `cc_response` column must not be renamed.
- Preserve current `--verbose` behavior for normal execution while making it
  useful for history output.

**EXAMPLE Reference Paths**:
- Study command-line argument handling and process launch concepts for wrapper
  parity only:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp`
- Study session start/finish, terminal source updates, copy/paste, focus,
  resize, and mouse/wheel event handling as a checklist for subprocess status
  and failure visibility:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`
- Study tab lifecycle and session-finished handling:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml`
- Study operator actions and failure-visible window controls:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`
- Study terminal-size overlay concepts for narrow history/status displays:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml`
- Study menu placement for copy, paste, settings, profile, fullscreen, zoom,
  and new tab actions:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/FullContextMenu.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/ShortContextMenu.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/WindowMenu.qml`

**Acceptance Checks**:
- Operators can tell whether Codex is running and how long it has been running.
- Captured stdout, stderr, exit code, timeout, and verbose behavior remain compatible with the current CLI.
- History mode is usable without horizontal scrolling.
- Styled output never becomes part of stored history rows.

### Session 04: Event Stream Boundary

**Objective**: Create the minimum stable machine-readable lifecycle boundary
needed by future renderers and wrappers.

**Scope**:
- Separate config loading, DB access, LLM calls, manager decisions, prompt
  building, Codex execution, notification, and rendering as much as practical.
- Promote the internal lifecycle snapshot from Session 01 into a documented
  event design for wrappers.
- Implement `--event-stream PATH` as a line-buffered JSONL file while leaving
  normal human stdout unchanged.
- Define the exact human-rendering disable mechanism needed for
  `--event-stream -`; expected implementation is an explicit machine-output
  mode unless an existing flag already guarantees silent human rendering.
- Expose the same event emitter as an importable Python API for tests and
  future wrappers.
- Add event names for iteration lifecycle, manager decisions, prompt dispatch,
  subprocess lifecycle, output summary, DB logging, help, completion, timeout,
  interrupts, and errors.
- Ensure event payloads contain raw operational facts and no Rich markup,
  ANSI escapes, frame glyphs, or reference-derived visual tokens.
- Add dry-run tests for event order, event names, payload stability, file
  flushing, stdout collision prevention, and no real LLM/Codex calls.

**Outputs**:
- Documented lifecycle event interface and importable emitter API.
- `--event-stream PATH` JSONL support, plus guarded stdout JSONL behavior.
- Event tests that verify ordering, names, raw payloads, and stdout isolation.

**Dependencies / Notes**:
- Depends on Sessions 01 through 03 for renderer and subprocess lifecycle
  facts.
- Normal human CLI output remains the default behavior.
- The event stream is the contract future wrappers consume; wrappers must not
  scrape Rich frames or parse human terminal output.
- Open question captured for implementation: whether the silent human-output
  guard is named `--no-human-output`, `--machine-output`, or an equivalent
  internal mode.

**EXAMPLE Reference Paths**:
- Study root application and window creation flow for lifecycle event grouping:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml`
- Study root C++ to QML wiring, arguments, application metadata, and import
  paths:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp`
- Study application-wide settings as the event/context model checklist:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`
- Study lifecycle flow from window to tabs to terminal surface:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`
- Study render-stage separation for event names, not implementation:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml`
- Study persisted settings and file import/export boundaries for event payload
  stability:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h`
- Study submodule declarations only to confirm what not to depend on:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules`

**Acceptance Checks**:
- Rich output and future wrappers can consume the same lifecycle facts.
- A future wrapper can observe state without scraping terminal frames.
- Prompt routing, autonomous handoffs, and SQLite compatibility remain unchanged.
- `--event-stream -` cannot mix JSONL with Rich or plain human output.

### Session 05: Docs Samples And Runbooks

**Objective**: Document the operator experience, fallback behavior, event
contract, and clean-room visual boundary after the implemented behavior exists.

**Scope**:
- Update `apex-infinite-cli/README-apex-infinite-cli.md` with UI flags,
  config examples, theme descriptions, event-stream usage, and examples.
- Update the operator runbook with theme guidance and plain-output guidance for
  CI, logs, remote shells, constrained terminals, `NO_COLOR`, redirected
  output, and `TERM=dumb`.
- Update `docs/apex-infinite-cli/history-db.md` if display changes add status
  labels, truncation rules, or verbose history behavior.
- Update `docs/apex-infinite-cli/prompt-contract.md` with either matching
  prompt-contract changes or a clear note that UI/event-stream changes do not
  alter `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or
  `build_codex_prompt()`.
- Add deterministic ASCII-only terminal transcripts or asciinema `.cast` files
  from fixture/dry-run output; do not commit binary screenshots.
- Document the local `EXAMPLE/` tree as ignored, reference-only, GPL-licensed
  study material and document the no-copying rule.
- Document the selected PySide6/QML wrapper path, the qmltermwidget/QTermWidget
  and PyQt exclusions, and the pywebview plus xterm.js backup option.
- Add troubleshooting for unreadable colors, non-UTF terminals, terminal width,
  `NO_COLOR`, `TERM=dumb`, redirected output, remote shells, and event-stream
  misuse.

**Outputs**:
- Updated README and deep-dive docs for UI, history, prompt-contract impact,
  event stream, fallback behavior, and visual-wrapper direction.
- ASCII-only transcripts or `.cast` recordings.
- Troubleshooting guidance for fallback and compatibility modes.

**Dependencies / Notes**:
- Depends on Sessions 01 through 04 so documentation describes implemented
  behavior instead of placeholders.
- Binary screenshots stay out of the repo and may be attached to releases only
  if useful.
- Documentation must identify `EXAMPLE/` as ignored by Git and reference-only.

**EXAMPLE Reference Paths**:
- Cite the reference README and describe it as visual inspiration only:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/README.md`
- Cite local license evidence and GPL boundary:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-2.0.txt`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-3.0.txt`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/packaging/debian/copyright`
- Cite submodule evidence for qmltermwidget and KDSingleApplication:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules`
- Study build and packaging docs as examples of what the wrapper docs must
  cover without copying scripts:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.desktop`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/snap/snapcraft.yaml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`
- Cite resource manifests and asset paths as material that must not be copied:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/32x32/cool-retro-term.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/64x64/cool-retro-term.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/128x128/cool-retro-term.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/256x256/cool-retro-term.png`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/crt.icns`
- Study settings documentation scope from the reference settings files:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml`

**Acceptance Checks**:
- Users can discover and configure the new look from documentation.
- Operators have clear fallback instructions for poor terminal rendering.
- Docs preserve the Apex Spec workflow contract and no-copying boundary.
- Event-stream usage is documented without implying that wrappers parse Rich output.

### Session 06: Linux Wrapper Spike

**Objective**: Prove whether a standalone Linux visual wrapper can provide CRT effects without changing the workflow engine.

**Scope**:
- Use PySide6 with Qt Quick/QML as the selected Linux wrapper path, packaged as
  an optional extra separate from the base CLI.
- Evaluate pywebview plus xterm.js only as a documented backup if a true
  terminal-emulator viewport becomes mandatory.
- Launch the CLI as a subprocess and consume the Session 04 JSONL event stream;
  do not embed a pseudo-terminal, scrape Rich output, or depend on
  `cool-retro-term` at runtime.
- Prototype an event-driven visual console with a read-only terminal-like log
  viewport, theme selector, status panels, and enough effects to validate glow,
  scanlines, flicker, curvature, frame treatment, and timing feasibility.
- Use the local reference render pipeline only as a feasibility checklist:
  source surface, optional bloom source, dynamic/effects pass, static/final
  pass, frame pass, frame buffer, and timing driver.
- Study but do not copy the reference settings groups: profile, screen,
  terminal, effects, advanced/performance, import/export, and persistence.
- Document build dependencies, packaging risks, license obligations, the
  CLI/wrapper interface contract, and the empty local qmltermwidget placeholder.
- Keep prototype code isolated from the Rich milestone until the approach is accepted.

**Outputs**:
- Standalone PySide6/QML Linux prototype or documented evidence that a specific
  technical or licensing blocker requires deferral.
- License, dependency, toolkit, and packaging assessment.
- Decision record for PySide6/QML as the selected path and pywebview/xterm.js
  as the backup option.

**Dependencies / Notes**:
- Depends on Session 04 unless the spike explicitly documents why a weaker
  temporary interface is sufficient.
- Do not vendor GPL reference code or depend on `cool-retro-term` at runtime.
- Decision: use PySide6/Qt Quick/QML with LGPLv3/commercial compliance notes;
  do not use PyQt, qmltermwidget, QTermWidget, copied QML, copied shaders,
  copied images, copied icons, copied fonts, resource manifests, or literal
  profile data.
- The local reference's qmltermwidget and KDSingleApplication submodule
  directories are empty in this checkout; treat them as unavailable.

**EXAMPLE Reference Paths**:
- Study Qt/QML app bootstrap and command argument wiring:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp`
- Study project/module layout and shader-baker/build requirements without
  copying qmake files:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro`
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro`
- Study root QML application and window creation:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml`
- Study window, tab, terminal source, and session lifecycle:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`
- Study effect pipeline stages and timing:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml`
- Study settings, controls, and persistence:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h`
- Study font handling concepts and then choose independent system-font behavior:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h`
- Study shader source categories only; do not copy source, constants, compiled
  `.qsb` blobs, or formulas:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.vert`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/passthrough.vert`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.vert`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.vert`
- Study resource and submodule declarations only to avoid accidental runtime
  dependencies:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc`
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules`

**Acceptance Checks**:
- Prototype can launch or display an Apex Infinite session through the event stream, or the plan documents the exact blocker that forces deferral.
- Prototype demonstrates visual effects Rich cannot faithfully render.
- The selected path has an explicit license and dependency story.
- Base CLI installation remains unaffected by graphical dependencies.

### Session 07: Wrapper Productization Or Deferral

**Objective**: Turn the accepted Linux wrapper prototype into an optional
standalone visual mode, or record a precise deferral if the spike blocks.

**Scope**:
- If Session 06 is accepted, implement the selected PySide6/Qt Quick/QML
  Linux-only wrapper in a maintainable optional-extra directory structure.
- Use the Session 04 subprocess plus JSONL event-stream boundary rather than
  scraping themed Rich output.
- Add independently designed amber CRT, green CRT, and IBM DOS inspired
  presets.
- Add controls for effect intensity, font, scaling, reduced effects, and plain
  fallback.
- Add Linux development, packaging, release, and troubleshooting instructions.
- Add smoke tests for wrapper launch, CLI subprocess/event-stream invocation,
  timeout display, non-zero exit display, missing CLI display, malformed event
  display, and failure display.
- Keep wrapper dependencies optional so base CLI installs remain lightweight and headless-safe.
- If Session 06 uncovers a blocker, replace productization with a deferral note
  that names the blocker, records evidence, and identifies the minimum evidence
  needed to reopen wrapper work.

**Outputs**:
- Optional standalone Linux visual mode, or a clear deferral record.
- Packaging, setup, license, and troubleshooting documentation.
- Wrapper smoke tests and fallback behavior when productized.

**Dependencies / Notes**:
- Depends on an accepted Session 06 prototype and the Session 04 event boundary.
- Do not make the base CLI require PySide6, Qt, a graphical display, or wrapper
  assets.
- Visual mode is a companion execution surface for the same autonomous engine,
  not a fork of workflow behavior.

**EXAMPLE Reference Paths**:
- Study maintainable wrapper surface and window actions:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`
- Study tab/session structure only if productizing multiple visual sessions:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml`
- Study menu, profile, copy/paste, settings, fullscreen, zoom, and action
  organization:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/FullContextMenu.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/ShortContextMenu.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/WindowMenu.qml`
- Study settings persistence and profile import/export concepts:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h`
- Study font/scaling controls and then implement independent optional controls:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h`
- Study effects and performance controls for productized user settings:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml`
- Study packaging and install surfaces without copying build scripts or
  manifests:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.desktop`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/snap/snapcraft.yaml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`
- Treat resource manifests, image assets, icons, and fonts as forbidden source
  material while auditing for accidental copying:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/32x32/cool-retro-term.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/64x64/cool-retro-term.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/128x128/cool-retro-term.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/256x256/cool-retro-term.png`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/crt.icns`

**Acceptance Checks**:
- Users can run the visual mode without installing or launching `cool-retro-term`.
- Visual mode preserves the same workflow decisions and safety behavior as the CLI.
- Base CLI installation remains usable without graphical dependencies.
- If deferred, the blocker and reopen criteria are explicit and testable.

### Session 08: Release Verification

**Objective**: Verify the full upgrade against compatibility, documentation, testing, and clean-room completion criteria.

**Scope**:
- Run the CLI test suite and all new focused rendering, config, Click, history,
  subprocess, plain-mode, event, docs, and wrapper tests that apply.
- Smoke test with a real initialized Apex Spec project and a small `--max-iterations` value.
- Verify `--dry-run`, `--history`, `--verbose`, `--plain`, `--ascii`,
  `--compact`, `--event-stream PATH`, guarded `--event-stream -`, every
  built-in theme, `NO_COLOR`, non-TTY output, redirected output, and
  `TERM=dumb`.
- Confirm source files remain ASCII-only and LF-only.
- Confirm history rows contain raw workflow data and no styled output.
- Confirm event rows contain raw operational facts and no Rich/reference tokens.
- Confirm no reference source, shader, image, icon, font, resource manifest,
  literal profile data, or GPL code was copied.
- Confirm docs describe UI controls, prompt-contract impact, fallback behavior,
  event-stream behavior, wrapper boundary, dependency plan, and license
  assessment.
- If the wrapper shipped, run launch and failure-mode smoke tests; if it was
  deferred, verify the deferral is explicit and base CLI improvements are complete.

**Outputs**:
- Final verification notes or checklist results.
- Any small compatibility fixes found during release testing.
- Clear status on whether the selected PySide6/QML wrapper path shipped, was
  deferred by a named blocker, or remains documented as near-future work.

**Dependencies / Notes**:
- Runs after the implemented scope of Sessions 01 through 07.
- If the wrapper is deferred, verification should check that deferral is explicit and that base CLI improvements are still complete.
- This session should trace every rough-plan completion criterion to either a
  passing check, a shipped artifact, or an explicit deferral.

**EXAMPLE Reference Paths**:
- Verify inspiration and clean-room documentation claims against:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/README.md`
- Verify license and no-copy boundary against:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-2.0.txt`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-3.0.txt`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/packaging/debian/copyright`
- Verify submodule and external dependency boundaries against:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules`
- Audit against source QML reference files to ensure no copied QML:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc`
- Audit against shader source and compiled shader paths to ensure no copied
  shader source or `.qsb` blobs:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.vert`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/passthrough.vert`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.vert`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.vert`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic_raster0_burn0_frame0_chroma0.frag.qsb`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static_rgb0_bloom0_curve0_shine0.frag.qsb`
- Audit against C++ bridge/build files to ensure no copied implementation:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro`
- Audit against assets and packaging files to ensure none were copied:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/32x32/cool-retro-term.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/64x64/cool-retro-term.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/128x128/cool-retro-term.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/256x256/cool-retro-term.png`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/crt.icns`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.desktop`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/snap/snapcraft.yaml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`

**Acceptance Checks**:
- Existing workflow behavior remains compatible.
- Prompt contract is either unchanged or updated with matching tests and documentation.
- Users can enable the new UI, disable it cleanly, and operate safely in constrained terminals.
- Completion criteria in the source plan are satisfied or explicitly deferred with rationale.

Status: proposed

## Goal

Upgrade `apex-infinite-cli` from a functional autonomous loop runner into a
polished operator console for long-running Apex Spec workflows.

The highest-priority improvement is the look and feel. The CLI should still be
fast, readable, scriptable, and safe to run unattended, but its default
interactive experience should feel intentional instead of like raw diagnostic
output.

Secondary objectives:

- Keep the autonomous manager, prompt routing, history schema, and Codex
  subprocess behavior stable unless a change is explicitly required for display.
- Give future visual surfaces a structured event boundary so they do not have
  to scrape Rich-rendered terminal output.
- Make every visual feature degrade cleanly to plain output for logs, CI,
  non-TTY shells, dumb terminals, and `NO_COLOR`.
- Keep the visual inspiration clean-room: study the reference, then implement
  independently selected names, colors, layouts, effects, and assets.

## Visual Direction

Take look inspiration directly from
[Swordfish90/cool-retro-term](https://github.com/Swordfish90/cool-retro-term).
The target is a retro CRT operator console mood: amber and green phosphor theme
presets, IBM DOS style contrast, compact status readouts, strong terminal
framing, and subtle scanline-like separation.

This is visual inspiration only. Do not copy `cool-retro-term` code, shaders,
images, fonts, themes, or bundled assets.

The work has two visual milestones and one bridge milestone:

1. First pass: implement a standalone Rich-based terminal experience that
   captures the operator-console layout, colors, framing, and status language.
2. Bridge: expose structured lifecycle facts for future renderers without
   forcing graphical dependencies into the base CLI.
3. Soon after: build a standalone Linux-only Qt/QML wrapper or equivalent
   renderer for the visual effects Rich cannot provide, such as glow, screen
   curvature, flicker, and shader-like scanlines.

Do not require users to run `apex-infinite-cli` inside `cool-retro-term`. The
upgraded experience must remain standalone.

## Current State Findings

Evidence reviewed:

- `apex-infinite-cli/apex_infinite.py` is a single-file Click application with
  global `Console()` output, SQLite history, LLM calls, manager routing, signal
  handling, desktop notification, and `codex exec` subprocess execution.
- `apex-infinite-cli/config.yaml` has provider and Codex settings only. It has
  no `ui` section today.
- `apex-infinite-cli/requirements.txt` already includes `rich`, `click`,
  `openai`, `python-dotenv`, and `pyyaml`; the first milestone should not need
  new runtime dependencies.
- Current tests are prompt- and routing-focused in
  `apex-infinite-cli/tests/test_prompts.py`. There are no tests yet for Click
  option parsing, UI config defaults, rendering helpers, history rendering,
  environment color behavior, or subprocess display behavior.
- Existing documentation is split across the CLI README and deep-dive docs:
  `docs/apex-infinite-cli/operator-runbook.md`,
  `docs/apex-infinite-cli/history-db.md`,
  `docs/apex-infinite-cli/prompt-contract.md`, and
  `docs/apex-infinite-cli/troubleshooting.md`.
- The history DB intentionally preserves the legacy `cc_response` column. UI
  work must not rename it or require a migration.
- `execute_codex()` currently uses `subprocess.run(..., capture_output=True)`.
  Live execution display will require either a careful `subprocess.Popen`
  rewrite or a wrapper that shows elapsed status while preserving captured
  stdout, stderr, exit code, timeout, and verbose output semantics.

Upgrade implication: first isolate rendering and configuration without changing
workflow behavior; then improve the operator experience; then add a structured
event channel before productizing any graphical wrapper.

## Local cool-retro-term Feature Reference Map

The local reference copy is ignored by Git and exists only for visual study:

- Local root:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term`
- README and visual overview:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/README.md`
- License boundary for the reference project:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-2.0.txt`
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-3.0.txt`

Use these paths for analysis only. Do not copy source code, shader code,
compiled shader blobs, image assets, font assets, profile JSON, or resource
manifests into `apex-infinite-cli`.

The local `EXAMPLE/` tree is ignored by Git. The
`EXAMPLE/cool-retro-term/qmltermwidget` directory exists in this checkout, but
it contains no local source files. Treat qmltermwidget as an external reference
mentioned by the `cool-retro-term` README and imported by
`PreprocessedTerminal.qml`, not as available local source material unless the
submodule is intentionally populated later.

### Visual Feature Sources

| Feature area | What to study | Local full path references |
|--------------|---------------|----------------------------|
| Application shell | QML application root, window creation, global settings, time driver | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml` |
| Built-in profiles | Amber, green, DOS-like, IBM, and other theme presets; study the grouped choices, not the literal values | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml` |
| Settings window | Profile, screen, terminal, effects, advanced, import, and export organization | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml` |
| Theme color controls | Font, background, frame color, chroma, saturation, brightness, contrast | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ColorButton.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/utils.js` |
| CRT effects controls | Bloom, burn-in, static noise, jitter, glow line, curvature, ambient light, flicker, horizontal sync, RGB shift, frame shininess | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml` |
| Performance controls | Effects FPS, texture quality, bloom quality, burn-in quality | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml` |
| Terminal viewport | PTY terminal, scroll bar, font handling, selection, paste, mouse, wheel, focus, corrected mouse coordinates under distortion. The local qmltermwidget directory is an empty submodule placeholder in this checkout. | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/qmltermwidget` |
| Render pipeline | Preprocessed terminal source, bloom source, dynamic shader pass, static shader pass, frame buffer | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml` |
| Burn-in trail | Burn-in source accumulation, update timing, quality scaling | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.vert` |
| Screen frame | Physical monitor frame color, ambient light, curvature, radius, frame size, shininess | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.vert` |
| Dynamic CRT shader | Rasterization, burn-in overlay, display frame influence, chroma, flicker, horizontal sync, glow line, jitter, static noise | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert` |
| Static CRT shader | RGB shift, bloom, screen curvature, frame shininess, brightness, final composition | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.vert` |
| Compiled shader variants | Qt Shader Baker output for raster, burn-in, frame, chroma, RGB shift, bloom, curvature, and shine combinations | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc` |
| Noise and texture assets | Static noise texture and CRT image reference | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png` |
| Font source and rendering modes | Bundled vs system fonts, default/scanline/pixel/subpixel/modern rasterization, scaling, width, line spacing | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml` |
| Menus and profile switching | Context menu, menu bar, profile menu, copy/paste/settings/fullscreen/zoom/new tab actions | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/FullContextMenu.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/ShortContextMenu.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/WindowMenu.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml` |
| Tabs and window controls | New tab, close tab, title normalization, fullscreen, size overlay, zoom shortcuts | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml` |
| Profile persistence | Settings storage, custom profile import/export, file IO bridge | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h` |
| Dialog and small controls | About dialog, profile naming dialog, sliders, checkable sliders, sized labels | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/AboutDialog.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/InsertNameDialog.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SimpleSlider.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/CheckableSlider.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Components/SizedLabel.qml` |
| Qt resource manifest | QML, images, fonts, icons, and compiled shader inclusion | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc` |
| Linux build and packaging | Qt modules, qmake build, shader baking, Linux icon install, desktop entry, Snap packaging reference | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.desktop`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/snap/snapcraft.yaml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/scripts/build-appimage.sh` |
| Icons | Linux desktop/app icon shape and sizes | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/32x32/cool-retro-term.png`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/64x64/cool-retro-term.png`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/128x128/cool-retro-term.png`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/256x256/cool-retro-term.png` |

### Built-In Profile Reference

The local copy defines these built-in profile names in
`/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`.
Use them as a checklist for visual moods, not as data to copy:

- Default Amber
- Monochrome Green
- Deep Blue
- Commodore 64
- Commodore PET
- Apple ][
- Atari 400
- IBM VGA 8x16
- IBM 3278 Reborn
- Neon Cyan
- Ghost Terminal
- Plasma
- Boring
- E-Ink

### Shader Source Reference

Study the shader source categories at these full paths:

- Burn-in fragment:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag`
- Burn-in vertex:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.vert`
- Pass-through vertex:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/passthrough.vert`
- Dynamic terminal fragment:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`
- Dynamic terminal vertex:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert`
- Terminal frame fragment:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag`
- Terminal frame vertex:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.vert`
- Static terminal fragment:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag`
- Static terminal vertex:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.vert`

Compiled `.qsb` shader blobs are reference artifacts only. They live in
`/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders`
and are enumerated in
`/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc`.

### Bundled Font Asset Reference

Do not copy these fonts or their licenses. Use them to understand the visual
range of CRT and old-computer typography:

- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/apple2/PRNumber3.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/apple2/PrintChar21.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/atari-400-800/AtariClassic-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/bigblue-terminal/BigBlueTerm437NerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/cozette/CozetteVector.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/departure-mono/DepartureMonoNerdFontMono-Regular.otf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/fira-code/FiraCodeNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/fixedsys-excelsior/FSEX301-L2.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/gohu/GohuFont11NerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/greybeard/Greybeard-12px.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/greybeard/Greybeard-16px.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/hack/HackNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/ibm-3278/3270NerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/iosevka/IosevkaTermNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/jetbrains-mono/JetBrainsMonoNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/oldschool-pc-fonts/PxPlus_IBM_EGA_8x8.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/oldschool-pc-fonts/PxPlus_IBM_VGA8.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/oldschool-pc-fonts/PxPlus_IBM_VGA_8x16.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/opendyslexic/OpenDyslexicMNerdFontMono-Regular.otf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/pet-me/PetMe.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/pet-me/PetMe64.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/source-code-pro/SauceCodeProNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/terminus/TerminessNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/unscii/unscii-16-full.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/unscii/unscii-8-thin.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/unscii/unscii-8.ttf`

### Rich Milestone Translation Targets

The first Rich milestone can translate only these local reference ideas:

- Color mood, contrast, and profile naming from
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`.
- Operator settings grouping from
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`.
- Frame, margin, status, and size-overlay concepts from
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml`.
- Low-fidelity scanline/noise suggestion from
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`.

The Linux wrapper milestone is responsible for features that require a real
rendering layer: glow, bloom, curvature, burn-in trails, flicker, shader
scanlines, RGB shift, and frame shine.

## Reference Translation Boundaries

Allowed translation:

- Convert the reference app's concepts into independently chosen CLI UI tokens:
  profile names, role labels, status severity, panel hierarchy, and output
  grouping.
- Use the reference settings groups as a checklist: profile, screen, terminal,
  effects, advanced/performance, import/export, and persistence.
- Use the render pipeline as architecture inspiration for the wrapper spike:
  terminal source, optional bloom source, dynamic pass, static pass, frame, and
  frame buffer.
- Use the effect list as a feasibility checklist: bloom, burn-in, static noise,
  jitter, glow line, curvature, ambient light, flicker, horizontal sync, RGB
  shift, frame size, frame color, and frame shininess.

Forbidden translation:

- Do not copy literal profile JSON, shader code, shader constants, generated
  `.qsb` blobs, QML code, image assets, font assets, resource manifests, icons,
  or build scripts.
- Do not vendor `cool-retro-term` or qmltermwidget into this repo as part of
  the Rich milestone.
- Do not make the CLI require `cool-retro-term`, qmltermwidget, Qt, PySide, a
  terminal emulator, or a graphical display for normal operation.
- Do not let style wrappers alter manager prompts, command normalization, DB
  persistence, path normalization, timeout behavior, or autonomous handoffs.

## Resolved Direction

As of 2026-07-02, repo and reference research resolve the open choices in this
plan:

- Invalid theme names fail fast with clear Click/config errors. Only terminal
  environment constraints fall back to `plain`.
- Core theme presets are built-in Python token definitions. Users can extend or
  override them through validated `ui.themes.<name>` YAML entries.
- The default theme is `auto`. On capable interactive TTYs, `auto` resolves to
  `crt-green`; under `NO_COLOR`, `TERM=dumb`, non-TTY output, or redirected
  output, it resolves to `plain`.
- History mode reuses the existing `--verbose` flag for expanded row detail. Do
  not add `--history-verbose`.
- Documentation commits only ASCII artifacts, such as deterministic asciinema
  `.cast` files or plain transcripts. Binary screenshots stay out of the repo
  and may be attached to releases if useful.
- UI changes do not change the manager or summarizer prompt contract. Add a
  short prompt-contract note only to state that the UI/event stream is outside
  prompt routing unless `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or
  `build_codex_prompt()` actually changes.
- The wrapper-facing boundary is an opt-in line-buffered JSONL event stream to
  a file path via `--event-stream PATH`, plus an importable event emitter API.
  `--event-stream -` is allowed only when human rendering is disabled.
- The selected Linux visual wrapper path is PySide6 with Qt Quick/QML as an
  optional extra. It launches the CLI as a subprocess and consumes the JSONL
  event stream.
- The wrapper uses a read-only terminal-like log viewport and operational event
  panels, not qmltermwidget, QTermWidget, PyQt, copied QML, copied shaders,
  copied assets, copied fonts, or a copied terminal emulator.
- pywebview plus xterm.js is a documented backup if a full terminal-emulator
  viewport becomes mandatory, not the primary path.

Research basis:

- Local repo license is MIT, and `.gitignore` excludes `EXAMPLE/`.
- Local `EXAMPLE/cool-retro-term` package metadata and file headers identify
  the reference project as GPL-3.0-or-later style material.
- `EXAMPLE/cool-retro-term/.gitmodules` shows qmltermwidget and
  KDSingleApplication as submodules, but both directories are empty locally.
- Qt for Python documentation: https://doc.qt.io/qtforpython-6/index.html
- Qt licensing documentation: https://doc.qt.io/qt-6/licensing.html
- Riverbank PyQt licensing: https://riverbankcomputing.com/commercial/pyqt
- qmltermwidget licensing: https://github.com/Swordfish90/qmltermwidget
- pywebview backup option: https://pywebview.flowrl.com/
- xterm.js backup option: https://github.com/xtermjs/xterm.js/

## Design Principles

- Prioritize legibility over novelty.
- Make the retro look configurable and easy to disable.
- Preserve unattended automation and plain terminal output behavior.
- Keep source files ASCII-only and LF-only.
- Prefer the existing `rich` dependency before adding new dependencies.
- Provide a low-effects fallback for CI, log files, dumb terminals, and
  `NO_COLOR` environments.
- Treat every visual element as operational information, not decoration.
- Treat the Linux visual wrapper as a companion execution surface for the same
  autonomous engine, not a fork of workflow behavior.

## Behavioral Guardrails

- The manager prompt contract remains stable. UI work should not edit
  `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or
  `build_codex_prompt()` unless the change is explicitly about display metadata
  and all prompt-contract tests and docs are updated in the same session.
- Stored history remains raw workflow data, not styled terminal output. Do not
  write ANSI escape codes, box characters, or Rich markup into
  `~/.apex-infinite/history.db`.
- Plain mode must be deterministic enough for logs and tests. It should not use
  live-only displays, carriage-return animations, or terminal-specific glyphs.
- `--verbose` remains an output-depth control. It can coexist with UI themes,
  but it must still expose more of the captured Codex response than default
  mode.
- `Ctrl+C`, `help`, `alldonebaby`, timeout, and non-zero subprocess exits must
  remain impossible to miss in every theme and in plain mode.
- Renderer tests should assert semantic sections and labels, not exact full
  frame snapshots.

## Target Experience

The upgraded CLI should feel like a mission-control terminal for autonomous
development sessions:

- Startup shows a compact boot screen with project, provider, model, config,
  max iterations, dry-run state, and selected theme.
- Each iteration renders as a framed cycle with stable sections: history,
  manager decision, prompt, Codex execution, result, log write, and next wait.
- Active work uses a live status line with elapsed time and subprocess state.
- Manager decisions are visually distinct from Codex output.
- Errors and operator interrupts are impossible to miss without overwhelming
  normal output.
- History mode becomes a readable operations ledger, not just a wide table.

## Scope

In scope:

First Rich milestone:

- Theme tokens for colors, emphasis, borders, and status states.
- Built-in themes: `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and `plain`,
  plus validated `ui.themes` overrides for custom operator themes.
- Centralized rendering helpers around `rich.console.Console`.
- Improved startup banner, iteration frame, decision panel, output panel, and
  history view.
- Config support for theme selection, effect level, ascii output, compact
  output, elapsed time, and provider display.
- CLI flags for theme, plain, ascii, and compact output.
- Documentation and ASCII-only terminal transcripts or asciinema recordings.
- Tests for rendering paths, config parsing, Click flags, subprocess display,
  history rendering, and plain output behavior.

Bridge milestone:

- A small internal lifecycle event model for rendering and future wrappers.
- An opt-in wrapper-facing line-buffered JSONL stream to a file path via
  `--event-stream PATH`, plus an importable event emitter API.
- Tests that prove event payloads stay raw and independent from Rich markup.

Soon-future Linux visual milestone:

- A standalone Linux-only PySide6/Qt Quick/QML wrapper packaged as an optional
  extra.
- Reuse of the existing Python CLI as the workflow engine, subprocess target,
  event stream producer, and importable event API provider.
- CRT effects that Rich cannot faithfully render: glow, curvature, flicker,
  phosphor trails, and full-viewport scanline overlays.
- Packaging notes for Linux distribution, local development, and operator use.

Out of scope:

- Replacing Codex CLI.
- Requiring `cool-retro-term` or any external terminal emulator at runtime.
- Copying `cool-retro-term` implementation details or assets.
- Rewriting the manager or summarizer prompt contract unless UI changes require
  clearer display metadata.
- Shipping macOS or Windows visual-wrapper support in this project.

## Proposed Configuration

Add a `ui` section to `apex-infinite-cli/config.yaml`:

```yaml
ui:
  theme: "auto"            # auto | crt-green | crt-amber | ibm-dos | plain | custom name
  effect_level: "low"      # off | low | medium
  ascii: false
  compact: false
  show_elapsed: true
  show_provider: true
  themes: {}               # optional validated custom theme overrides
```

Add command-line overrides:

```bash
python apex_infinite.py --theme crt-amber
python apex_infinite.py --plain
python apex_infinite.py --ascii
python apex_infinite.py --compact
python apex_infinite.py --event-stream /tmp/apex-infinite-events.jsonl
```

`--plain` should disable color and effects. `--ascii` should avoid box-drawing
glyphs where possible. `NO_COLOR` should behave like `--plain` unless the user
explicitly opts back into a theme.

### Configuration Precedence

Use a single resolver for UI settings:

1. CLI flags
2. environment constraints
3. `config.yaml`
4. built-in defaults

Rules:

- Built-in default is `ui.theme: auto`.
- `auto` resolves to `crt-green` only on capable interactive TTYs.
- `auto` resolves to `plain` for `NO_COLOR`, `TERM=dumb`, non-TTY output,
  redirected output, or `Console().is_terminal == false`.
- `--plain` forces `theme: plain`, `effect_level: off`, and color disabled.
- `NO_COLOR` behaves like `--plain` when no explicit `--theme` is passed.
- An explicit `--theme` can opt back into color even when `NO_COLOR` exists,
  but this behavior must be documented.
- Non-TTY output, `TERM=dumb`, or `Console().is_terminal == false` should
  default to plain unless the operator explicitly forces a theme.
- `--ascii` changes glyph selection only. It does not by itself disable color.
- `--compact` reduces vertical space but must not hide errors, manager reasons,
  command prompts, or completion state.
- Invalid `--theme`, `ui.theme`, and `ui.themes` values fail fast with clear
  Click/config errors. Do not silently fall back to `plain` for invalid user
  configuration.
- `--event-stream PATH` writes line-buffered JSONL events to a file without
  changing human output. `--event-stream -` is valid only with human rendering
  disabled so JSONL is not mixed with Rich output.

## Implementation Sessions

### Session 1: UI Architecture And Theme Tokens

Objective: create the rendering foundation without changing workflow behavior.

Tasks:

- Add a small renderer module or internal renderer section that owns all
  operator-facing `rich` output. Prefer a separate module if the change can be
  kept low-risk; otherwise create a clearly bounded section inside
  `apex_infinite.py` and split later.
- Allow the renderer to receive an injected `Console` so tests can use
  `Console(record=True, width=...)` and temporary streams without touching the
  global console.
- Define theme token data for color names, border styles, emphasis, status
  labels, warning labels, muted text, glyph sets, and plain/ascii fallbacks.
- Define built-in Python token data for `auto`, `crt-green`, `crt-amber`,
  `ibm-dos`, and `plain`, plus a validated `ui.themes` override schema for
  custom themes.
- Define a minimal internal display-event shape or snapshot dictionary for:
  startup, iteration start, history summary, manager decision, prompt build,
  codex start, codex finish, DB log, help pause, completion, timeout, and error.
  The first Rich renderer can consume these events directly without exposing a
  public machine interface yet.
- Move startup banner, history table, iteration banner, decision output, and
  agent response panels through renderer helpers.
- Add config parsing for `ui.theme`, `ui.effect_level`, `ui.ascii`,
  `ui.compact`, `ui.show_elapsed`, `ui.show_provider`, and `ui.themes`.
- Add CLI overrides for `--theme`, `--plain`, `--ascii`, and `--compact`.
- Implement and test the configuration precedence rules from this plan.
- Add tests for config defaults, CLI overrides, `NO_COLOR`, non-TTY/plain
  behavior, and invalid theme behavior.
- Fail fast on invalid `--theme`, `ui.theme`, and malformed `ui.themes`
  entries with clear Click/config errors.

Acceptance:

- Existing commands still work with the default config.
- `--history`, `--dry-run`, and direct execution still function.
- Prompt contract tests still pass unchanged.
- No ANSI escapes, Rich markup, or frame glyphs are written to SQLite history.
- The default output path is visually changed only through renderer helpers,
  with `auto` choosing `crt-green` for capable interactive TTYs and `plain`
  for constrained outputs.

### Session 2: CRT-Inspired Operator Console

Objective: implement the first complete visual pass inspired by
`cool-retro-term`.

Tasks:

- Add `crt-green`, `crt-amber`, and `ibm-dos` theme presets.
- Choose independent color tokens. Do not copy literal profile JSON or color
  constants from `cool-retro-term`.
- Make `auto` select `crt-green` on capable interactive TTYs and `plain` under
  constrained output conditions.
- Redesign the startup banner as a compact boot/status panel.
- Replace the plain iteration separator with a stable iteration frame.
- Add a small status strip for provider, model, project, iteration, elapsed
  time, dry-run state, and current operation.
- Distinguish manager decisions, Codex prompts, agent output, errors, and
  database writes with consistent labels.
- Add subtle scanline-like separators using plain repeated characters, with
  automatic disablement in `plain` and compact modes. In `ascii` mode use only
  code points 0-127.
- Add visibly distinct render states for `help`, `alldonebaby`, timeout,
  non-zero Codex exit, LLM retry, and operator interrupt.
- Ensure terminal width handling works at 80, 100, and 120 columns.

Acceptance:

- The normal interactive run presents a cohesive retro terminal look.
- The visual direction clearly references `cool-retro-term` without copying any
  external assets.
- Output remains readable in narrow terminals and under color-disabled modes.

### Session 3: Live Execution And Better History

Objective: improve operator awareness during long-running Codex subprocesses.

Tasks:

- Use `rich.status.Status`, `rich.progress`, or `rich.live.Live` for elapsed
  subprocess display while stdout is captured.
- If replacing `subprocess.run()` with `subprocess.Popen`, preserve current
  behavior for stdout/stderr capture, stderr fallback when stdout is empty,
  non-zero exit wrapping, timeout text, `FileNotFoundError`, and generic
  exception reporting.
- Show command timeout, elapsed time, and process state during `codex exec`.
- Redesign `--history` as a compact ledger with command, reason, timestamp,
  status, and truncated response summary.
- Make existing `--verbose` meaningful in history mode by expanding response
  and reason detail; do not add `--history-verbose`.
- Keep the SQLite schema backward compatible.
- Add tests for history formatting with empty, short, and long records.
- Add tests for subprocess success, stderr-only output, non-zero exit, timeout,
  dry-run, and missing binary with a fake command runner or monkeypatch.

Acceptance:

- Operators can tell whether Codex is still running and how long it has been
  running.
- History mode is useful on a normal terminal without horizontal scrolling.
- Existing `~/.apex-infinite/history.db` files remain readable.
- Existing `--verbose` behavior for normal execution remains at least as
  informative as today.

### Session 4: Documentation, Samples, And Polish

Objective: make the upgrade easy to understand and maintain.

Tasks:

- Update `apex-infinite-cli/README-apex-infinite-cli.md` with UI flags,
  config examples, and theme descriptions.
- Update the operator runbook with recommended theme settings and plain-output
  guidance for CI or remote shells.
- Update `docs/apex-infinite-cli/history-db.md` if history display changes
  expose new status labels or summary rules.
- Update `docs/apex-infinite-cli/prompt-contract.md` only if prompt routing or
  machine-event behavior changes the contract. Otherwise add a short note that
  UI and event-stream changes do not alter manager prompts, summarizer prompts,
  or `build_codex_prompt()`.
- Add deterministic ASCII-only terminal transcripts or asciinema `.cast`
  recordings from fixture/dry-run output. Do not commit binary screenshots.
- Document the visual inspiration from
  `https://github.com/Swordfish90/cool-retro-term` and the no-copying
  constraint.
- Document the selected PySide6/QML wrapper path, the qmltermwidget/PyQt
  exclusion, and the pywebview/xterm.js backup option.
- Add a troubleshooting entry for unreadable colors, non-UTF terminals, and
  `NO_COLOR`, plus remote shells, redirected output, and `TERM=dumb`.
- Run the existing test suite and add focused rendering/config tests.

Acceptance:

- Users can discover and configure the new look from the README.
- Operators have clear fallback instructions when a terminal renders poorly.
- The upgrade is documented without changing the Apex Spec workflow contract.
- The docs identify `EXAMPLE/` as reference-only and ignored by Git.

### Session 5: Engine Boundary And Event Stream

Objective: create the minimum stable boundary needed by future visual surfaces
without productizing a graphical wrapper yet.

Tasks:

- Separate, as much as practical, config loading, DB access, LLM calls, manager
  decisions, prompt building, Codex execution, notification, and rendering.
  This can be module-level functions first; do not force a large class rewrite
  unless it reduces risk.
- Turn the internal display-event shape from Session 1 into a documented
  wrapper-facing event stream design.
- Implement the machine interface as `--event-stream PATH`, writing
  line-buffered JSONL events to a file while leaving normal human stdout
  unchanged.
- Support `--event-stream -` only with human rendering disabled, so JSONL is
  never mixed with Rich output.
- Expose the same event emitter as an importable Python API for tests and
  future wrappers.
- Add event names for iteration lifecycle, manager decisions, prompt dispatch,
  subprocess lifecycle, output summary, DB logging, help, completion, timeout,
  and errors.
- Ensure event payloads contain raw operational facts, not Rich markup or
  reference-derived visual tokens.
- Add dry-run tests that verify event ordering and payload stability without
  making real LLM or Codex calls.

Acceptance:

- The Rich renderer can consume the same lifecycle facts that a future wrapper
  would need.
- Existing human CLI output remains the default.
- A future wrapper has a documented JSONL/API way to observe state without
  scraping terminal frames.
- Prompt routing and SQLite compatibility remain unchanged.

### Session 6: Linux Visual Wrapper Spike

Objective: prove the standalone Linux visual-wrapper approach without changing
the autonomous workflow engine.

Tasks:

- Use PySide6 with Qt Quick/QML as the selected Linux wrapper path and package
  it as an optional extra separate from the base CLI.
- Document pywebview plus xterm.js as the backup if a full terminal-emulator
  viewport becomes mandatory; do not treat it as the primary path.
- Launch the Python CLI as a subprocess and consume the opt-in JSONL event
  stream. Do not scrape Rich output or embed a pseudo-terminal in the selected
  path.
- Prototype a window with an event-driven, read-only terminal-like log
  viewport, theme selector, status panels, and enough CRT effects to validate
  glow, scanlines, flicker, and curvature feasibility.
- Use the reference render pipeline as a checklist for feasibility: source
  terminal, optional bloom source, dynamic pass, static pass, frame, frame
  buffer, and timing driver.
- Confirm the prototype does not depend on `cool-retro-term` at runtime.
- Document build dependencies, packaging risks, and the interface contract
  between the wrapper and `apex_infinite.py`.
- Document the empty local qmltermwidget submodule placeholder and whether any
  external terminal widget is needed. The expected answer is no qmltermwidget
  or QTermWidget for the selected path.
- Document PySide6 LGPLv3/commercial compliance requirements and avoid PyQt
  unless a future commercial/GPL-compatible decision explicitly allows it.
- Keep all prototype code isolated from the Rich milestone until the approach is
  accepted.

Acceptance:

- A standalone Linux prototype can launch or display an Apex Infinite session.
- The prototype demonstrates visual effects that cannot be done well in Rich.
- The prototype uses `cool-retro-term` only as visual reference material.
- The team has enough evidence to proceed with PySide6/QML or document the
  exact blocker that forces deferral.
- The selected path has an explicit license and dependency story.

### Session 7: Linux Visual Wrapper Productization

Objective: turn the accepted prototype into the near-future standalone visual
mode.

Tasks:

- Implement the selected PySide6/Qt Quick/QML Linux-only wrapper in a
  maintainable directory structure.
- Use the Session 5 subprocess plus JSONL event-stream boundary rather than
  scraping themed Rich output.
- Add theme presets inspired by amber CRT, green CRT, and IBM DOS visuals.
- Add user controls for effect intensity, font, scaling, and plain fallback.
- Add packaging instructions for Linux development and release artifacts.
- Add smoke tests for wrapper launch, CLI subprocess or event-stream
  invocation, timeout display, non-zero exit display, and failure display.
- Keep the wrapper optional. Installing the base CLI must not install graphical
  dependencies unless the packaging strategy explicitly uses extras.

Acceptance:

- Users can run the standalone visual mode without installing or launching
  `cool-retro-term`.
- The visual mode preserves the same workflow decisions and safety behavior as
  the CLI.
- Linux setup and troubleshooting docs are complete enough for operators.
- Base CLI installation remains lightweight and usable on headless systems.

## Testing Plan

- Run `pytest tests/ -v` from `apex-infinite-cli/`.
- Keep existing prompt/routing tests green unless a session explicitly updates
  the prompt contract and its docs.
- Use `Console(record=True, width=...)` tests for representative rendered
  output.
- Add Click `CliRunner` tests for new flags and invalid option combinations.
- Use temporary DB paths or monkeypatched `DB_DIR`/`DB_PATH` for history tests.
- Validate 80, 100, and 120 column widths.
- Exercise `--dry-run`, `--history`, `--verbose`, `--plain`, `--ascii`, and
  every built-in theme.
- Verify `NO_COLOR=1` disables color unless explicitly overridden.
- Verify `TERM=dumb`, redirected output, or non-TTY console paths choose plain
  output by default.
- Verify normal history rows contain raw agent responses, not styled output.
- Verify subprocess display changes preserve success, stderr-only output,
  non-zero exit wrapping, timeout text, and missing binary behavior.
- Validate `--event-stream PATH`, `--event-stream -` with human rendering
  disabled, event order, event names, and raw payloads with dry-run fixtures.
- Confirm source files remain ASCII-only and LF-only.
- Smoke test with a real initialized Apex Spec project and a very small
  `--max-iterations` value.

## Risks And Mitigations

| Risk | Mitigation |
|------|------------|
| Retro styling reduces readability | Keep contrast high, make effects low by default, and provide `--plain` |
| Terminal compatibility varies | Add `--ascii`, respect `NO_COLOR`, and test common widths |
| Output becomes hard to parse in logs | Keep plain mode stable and avoid hiding important text behind live-only views |
| Dependency creep | Finish the Rich milestone first; isolate Linux wrapper dependencies |
| GPL contamination concerns | Use `cool-retro-term` only as visual inspiration; do not copy code or assets |
| PySide6 LGPL compliance is missed | Keep PySide6 in an optional extra, document LGPLv3/commercial obligations, avoid GPL-only Qt modules, and keep base CLI independent |
| PyQt licensing conflicts with the MIT repo | Do not use PyQt unless a future commercial/GPL-compatible decision explicitly approves it |
| Snapshot tests become brittle | Test semantic output markers and config behavior more than exact full frames |
| Wrapper diverges from CLI behavior | Keep one workflow engine and make the wrapper a display/runtime shell |
| Renderer leaks style into stored history | Store raw agent responses and manager data only; test the DB rows |
| Live subprocess display changes behavior | Preserve current stdout/stderr, timeout, return-code, and verbose semantics with tests |
| Config precedence surprises operators | Document and test CLI flag, `NO_COLOR`, non-TTY, and config precedence |
| Single-file CLI becomes harder to maintain | Split renderer/config/event helpers when the local change is lower risk than extending `apex_infinite.py` |
| qmltermwidget reference is unavailable locally | Treat the empty submodule placeholder as unavailable; do not use qmltermwidget or QTermWidget in the selected path |
| Graphical wrapper creates headless install burden | Keep wrapper dependencies optional and document Linux-only setup separately |

## Resolved Decisions

- Session 1 uses fail-fast validation for invalid themes.
- Session 1 stores core presets as built-in Python token data and supports
  validated `ui.themes` YAML overrides.
- Session 2 uses `auto` as the first-release default: `crt-green` for capable
  interactive TTYs and `plain` for constrained outputs.
- Session 3 extends existing `--verbose` behavior to history mode.
- Session 4 commits only deterministic ASCII recordings or transcripts, not
  binary screenshots.
- Session 4 documents that UI and event-stream changes do not alter the prompt
  contract unless the prompt functions themselves change.
- Session 5 implements `--event-stream PATH` plus an importable event emitter
  API, with `--event-stream -` allowed only when human rendering is disabled.
- Session 6 uses PySide6 with Qt Quick/QML as the selected Linux wrapper path.
- Session 6 excludes PyQt, qmltermwidget, QTermWidget, copied QML, copied
  shaders, copied assets, copied fonts, and copied terminal-emulator code.
- Session 6 keeps pywebview plus xterm.js as a documented backup if a true
  terminal-emulator viewport becomes mandatory.

## Completion Criteria

This project is complete when:

- The CLI has a coherent CRT-inspired default or opt-in look.
- The look directly references `cool-retro-term` as inspiration in docs.
- Users can disable styling cleanly for automation and constrained terminals.
- All existing workflow behavior remains compatible.
- Tests cover config parsing, renderer behavior, Click options, history output,
  plain mode, `NO_COLOR`, non-TTY output, and subprocess display behavior.
- The CLI README and deep-dive docs describe the new UI controls.
- Existing history databases remain readable without migration.
- The prompt contract either remains unchanged or is updated with matching
  tests and documentation.
- No reference source, shader, image, icon, font, resource manifest, or literal
  profile data is copied into the CLI.
- The optional visual-wrapper path has a documented process/API/event boundary,
  dependency plan, and license assessment.
- The near-future Linux wrapper path is documented as standalone and not
  dependent on running inside `cool-retro-term`.
`````

<!-- FOLDED_SOURCE_PLAN_ARCHIVE_END -->
