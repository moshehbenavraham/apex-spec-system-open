# PRD Phase 00: Apex Infinite CLI Upgrade

**Status**: Complete
**Sessions**: 8
**Estimated Duration**: 8-16 days
**Progress**: 8/8 sessions (100%)
**Source plan status**: proposed

This archived file (`.spec_system/archive/phases/phase_00/PRD_phase_00.md`)
consolidates the former folded source plan from
`docs/ongoing-projects/apex-infinite-cli-upgrade-plan.md`. The standalone plan
can be removed without losing detail; this file and the archived session stubs
record the completed Phase 00 execution interface.

---

## Overview

Upgrade `apex-infinite-cli/` from a functional autonomous workflow runner into
a polished, testable operator console with an optional Linux visual wrapper
path. Preserve manager routing, prompt contracts, SQLite compatibility,
normalized project path keys, Codex subprocess semantics, and raw durable data.

The priority is the interactive operator experience: intentional Rich terminal
output, robust plain fallbacks, better long-running subprocess visibility,
machine-readable lifecycle events, documentation, and clean-room wrapper
validation.

---

## Progress Tracker

| Session | Name | Status | Est. Tasks | Duration | Validated |
|---------|------|--------|------------|----------|-----------|
| 01 | Config And Renderer Boundary | Complete | ~18 | 2-4h | 2026-07-03 |
| 02 | Rich Operator Console | Complete | ~18 | 2-4h | 2026-07-03 |
| 03 | Subprocess And History Visibility | Complete | ~18 | 2-4h | 2026-07-03 |
| 04 | Event Stream Boundary | Complete | ~18 | 2-4h | 2026-07-03 |
| 05 | Docs Samples And Runbooks | Complete | ~16 | 2-4h | 2026-07-03 |
| 06 | Linux Wrapper Spike | Complete | ~18 | 2-4h | 2026-07-03 |
| 07 | Linux Visual Wrapper Productization | Complete | ~18 | 2-4h | 2026-07-03 |
| 08 | Release Verification | Complete | ~16 | 2-4h | 2026-07-03 |

Completed sessions:

- 2026-07-03: Session 01, Config And Renderer Boundary.
- 2026-07-03: Session 02, Rich Operator Console.
- 2026-07-03: Session 03, Subprocess And History Visibility.
- 2026-07-03: Session 04, Event Stream Boundary.
- 2026-07-03: Session 05, Docs Samples And Runbooks.
- 2026-07-03: Session 06, Linux Wrapper Spike.
- 2026-07-03: Session 07, Linux Visual Wrapper Productization.
- 2026-07-03: Session 08, Release Verification.

---

## Objectives

1. Centralize UI configuration and rendering without changing workflow behavior.
2. Deliver a cohesive Rich terminal console with plain, ASCII, compact, and
   constrained-terminal fallbacks.
3. Improve long-running Codex execution and history visibility while preserving
   raw captured output and SQLite compatibility.
4. Expose lifecycle facts through an opt-in JSONL event stream for future
   renderers and wrappers.
5. Document controls, fallback behavior, event contracts, clean-room visual
   rules, and wrapper interfaces.
6. Spike and productize the optional Linux visual wrapper without adding
   graphical dependencies to the base CLI.
7. Verify compatibility, tests, docs, release readiness, and clean-room
   completion criteria.

---

## Preconditions And Planning Resolutions

### Preconditions

- Spec system is initialized for the Apex Infinite CLI scope.
- Master PRD defines Phase 00 as the next not-started phase.
- `.spec_system/state.json` (`state.json`) has `current_phase` set to 0,
  records no completed sessions, and has `monorepo: false`.
- `apex-infinite-cli/` baseline behavior and prompt-routing tests are the
  compatibility reference.
- The source plan defines the full 8-session upgrade scope.
- `EXAMPLE/cool-retro-term` remains ignored by Git and reference-only.
- Phase 00 sessions target `apex-infinite-cli/`; session stubs omit package
  metadata because no formal workspace manager is configured.

### Resolved Conflicts

- The old Phase 00 placeholder described `Foundation` with 0 sessions. Replace
  that placeholder with this 8-session upgrade.
- `.spec_system/PRD/PRD.md` and `.spec_system/state.json` previously split the
  work across Phase 00 and Phase 01. The user clarified that all 8 sessions
  belong in Phase 00; stale Phase 01 tracking is invalid.
- Documentation originally preceded the event stream. The active order places
  `Event Stream Boundary` before `Docs Samples And Runbooks` so docs describe
  shipped event behavior.

---

## Current State Findings

- `apex-infinite-cli/apex_infinite.py` is a single-file Click app with global
  `Console()` output, SQLite history, LLM calls, manager routing, signal
  handling, desktop notification, and `codex exec` subprocess execution.
- `execute_codex()` uses `subprocess.run(..., capture_output=True)`. Live
  display must preserve stdout, stderr, exit code, timeout, stderr fallback,
  verbose output, `FileNotFoundError`, and generic exception behavior.
- `apex-infinite-cli/config.yaml` contains provider and Codex settings only; it
  has no `ui` section.
- `apex-infinite-cli/requirements.txt` already includes `rich`, `click`,
  `openai`, `python-dotenv`, and `pyyaml`; the Rich milestone needs no new
  runtime dependency.
- Existing tests are prompt- and routing-focused in
  `apex-infinite-cli/tests/test_prompts.py`.
- Missing test coverage: Click option parsing, UI config defaults, renderer
  helpers, history rendering, environment color behavior, subprocess display.
- Existing docs live in `apex-infinite-cli/README_apex-infinite-cli.md`,
  `apex-infinite-cli/docs/operator-runbook.md`,
  `apex-infinite-cli/docs/history-db.md`,
  `apex-infinite-cli/docs/prompt-contract.md`, and
  `apex-infinite-cli/docs/troubleshooting.md`.
- History DB compatibility requires preserving `~/.apex-infinite/history.db`
  and the legacy `cc_response` column without migration or rename.

Upgrade path: isolate rendering/config first, improve operator display second,
then add a structured event channel before productizing any graphical wrapper.

---

## Technical Baseline

### Technologies

- Python 3.10+
- Click
- Rich
- PyYAML and python-dotenv
- SQLite
- OpenAI-compatible Python client
- Codex CLI
- pytest, pytest-mock, pytest-cov, black, and pylint
- Optional PySide6 with Qt Quick/QML for Linux visual wrapper work

### Architecture Rules

- Create small renderer and configuration boundaries around the current CLI.
- Use those boundaries for display changes; do not change prompt routing,
  history storage, or subprocess semantics for visual reasons.
- Event streams publish raw lifecycle facts so future wrappers do not scrape
  Rich or plain human output.
- Extract helpers only when the split lowers risk and improves testability.
- Normal CLI execution must remain fast, readable, scriptable, headless-safe,
  and safe to run unattended.

---

## Visual Direction

Use `https://github.com/Swordfish90/cool-retro-term` as visual inspiration for
a retro CRT operator console: amber and green phosphor presets, IBM DOS style
contrast, compact status readouts, strong terminal framing, and subtle
scanline-like separation.

Do not require users to run `apex-infinite-cli` inside `cool-retro-term`. The
upgraded experience must remain standalone.

### Visual Milestones

1. Rich terminal milestone: standalone operator-console layout, colors,
   framing, and status language.
2. Bridge milestone: structured lifecycle facts for future renderers without
   graphical dependencies in the base CLI.
3. Linux visual milestone: standalone Linux-only Qt/QML wrapper, or equivalent
   renderer, for glow, screen curvature, flicker, shader-like scanlines, burn
   trails, RGB shift, bloom, and frame shine.

### Translation Boundaries

Allowed:

- Convert concepts into independently chosen CLI UI tokens: profile names,
  role labels, status severity, panel hierarchy, and output grouping.
- Use settings groups as a checklist: profile, screen, terminal, effects,
  advanced/performance, import/export, and persistence.
- Use the render pipeline as wrapper architecture inspiration: terminal source,
  optional bloom source, dynamic pass, static pass, frame, frame buffer.
- Use effect lists as feasibility checklists: bloom, burn-in, static noise,
  jitter, glow line, curvature, ambient light, flicker, horizontal sync, RGB
  shift, frame size, frame color, and frame shininess.

Forbidden:

- Do not copy profile JSON, shader code, shader constants, generated `.qsb`
  blobs, QML code, image assets, font assets, resource manifests, icons, build
  scripts, or literal profile data.
- Do not vendor `cool-retro-term`, qmltermwidget, QTermWidget, copied terminal
  emulators, GPL code, or reference assets.
- Do not make the base CLI require `cool-retro-term`, qmltermwidget, Qt,
  PySide, PyQt, a terminal emulator, or a graphical display.
- Do not let style wrappers alter manager prompts, command normalization, DB
  persistence, path normalization, timeout behavior, or autonomous handoffs.

### Rich Translation Targets

- Translate color mood, contrast, and profile naming from
  `ApplicationSettings.qml`.
- Translate operator settings grouping from `SettingsWindow.qml`.
- Translate frame, margin, status, and size-overlay concepts from
  `TerminalFrame.qml`, `SettingsGeneralTab.qml`, and `SizeOverlay.qml`.
- Translate low-fidelity scanline/noise ideas from `SettingsEffectsTab.qml`
  and `terminal_dynamic.frag`.
- Leave glow, bloom, curvature, burn-in trails, flicker, shader scanlines, RGB
  shift, and frame shine to the Linux wrapper milestone.

---

## Resolved Direction

As of 2026-07-02:

- Invalid theme names fail fast with clear Click/config errors; only terminal
  environment constraints fall back to `plain`.
- Core presets are built-in Python token definitions. Validated
  `ui.themes.<name>` YAML entries can extend or override them.
- Built-in default is `ui.theme: auto`: `crt-green` on capable interactive TTYs
  and `plain` under `NO_COLOR`, `TERM=dumb`, non-TTY output, redirected output,
  or `Console().is_terminal == false`.
- Existing `--verbose` extends to history mode; do not add
  `--history-verbose`.
- Docs commit only deterministic ASCII transcripts or asciinema `.cast` files.
  Binary screenshots stay out of the repo and may attach to releases only if
  useful.
- UI and event-stream changes do not alter `MANAGER_SYSTEM_PROMPT`,
  `SUMMARIZER_SYSTEM_PROMPT`, or `build_codex_prompt()` unless those functions
  actually change with matching tests and docs.
- Wrapper boundary is `--event-stream PATH`, a line-buffered JSONL stream, plus
  an importable event emitter API.
- `--event-stream -` is valid only when human rendering is disabled. Source
  plan candidate names for that guard were `--no-human-output`,
  `--machine-output`, or an equivalent internal mode.
- Selected Linux wrapper path is PySide6 with Qt Quick/QML as an optional extra.
  It launches the CLI as a subprocess and consumes JSONL events.
- Wrapper UI uses a read-only terminal-like log viewport and operational event
  panels, not qmltermwidget, QTermWidget, PyQt, copied QML, copied shaders,
  copied assets, copied fonts, or copied terminal-emulator code.
- pywebview plus xterm.js is a documented backup if a full terminal-emulator
  viewport becomes mandatory.

Research basis:

- Repo license is MIT; `.gitignore` excludes `EXAMPLE/`.
- Local reference package metadata and file headers identify
  `EXAMPLE/cool-retro-term` as GPL-3.0-or-later style material.
- `EXAMPLE/cool-retro-term/.gitmodules` lists qmltermwidget and
  KDSingleApplication, but both directories are empty locally.
- Qt for Python: `https://doc.qt.io/qtforpython-6/index.html`
- Qt licensing: `https://doc.qt.io/qt-6/licensing.html`
- Riverbank PyQt licensing: `https://riverbankcomputing.com/commercial/pyqt`
- qmltermwidget licensing: `https://github.com/Swordfish90/qmltermwidget`
- pywebview backup: `https://pywebview.flowrl.com/`
- xterm.js backup: `https://github.com/xtermjs/xterm.js/`

---

## Operator Experience

Target feel: mission-control terminal for autonomous development sessions.

- Startup shows project, provider, model, config, max iterations, dry-run state,
  and selected theme in a compact boot/status panel.
- Each iteration has stable sections: history, manager decision, prompt, Codex
  execution, result, log write, and next wait.
- Active work shows elapsed time and subprocess state.
- Manager decisions are visually distinct from Codex output.
- Errors, `Ctrl+C`, operator interrupts, `help`, `alldonebaby`, timeouts, and
  non-zero exits are impossible to miss in every theme and in plain mode.
- History mode is a compact operations ledger, not a wide table.

---

## Configuration Contract

Add `ui` to `apex-infinite-cli/config.yaml`:

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

Add CLI overrides:

```bash
python apex_infinite.py --theme crt-amber
python apex_infinite.py --plain
python apex_infinite.py --ascii
python apex_infinite.py --compact
python apex_infinite.py --event-stream /tmp/apex-infinite-events.jsonl
```

Precedence:

1. CLI flags
2. Environment constraints
3. `config.yaml`
4. Built-in defaults

Rules:

- `--plain` forces `theme: plain`, `effect_level: off`, and color disabled.
- `NO_COLOR` behaves like `--plain` unless an explicit `--theme` opts back into
  color; document that override.
- Non-TTY output, redirected output, `TERM=dumb`, or
  `Console().is_terminal == false` defaults to plain unless an operator forces
  a theme.
- `--ascii` changes glyph selection only and does not disable color.
- `--compact` reduces vertical space without hiding errors, manager reasons,
  command prompts, or completion state.
- Invalid `--theme`, `ui.theme`, and malformed `ui.themes` fail fast. Do not
  silently fall back for invalid user configuration.
- `--event-stream PATH` writes line-buffered JSONL events to a file without
  changing human output.
- `--event-stream -` requires disabled human rendering so JSONL never mixes
  with Rich or plain human output.

---

## Scope

### In Scope

Rich milestone:

- Theme tokens for colors, emphasis, borders, status states, severity labels,
  warning labels, muted text, glyph sets, and plain/ASCII fallbacks.
- Built-in themes: `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and `plain`,
  plus validated `ui.themes` overrides.
- Central rendering helpers around `rich.console.Console`, with injectable
  `Console(record=True, width=...)` support.
- Startup banner, iteration frame, decision panel, prompt preview, response
  panel, DB log notice, interrupt, completion, and history view rendering.
- UI config for theme, effect level, ASCII, compact, elapsed time, provider
  display, and custom themes.
- CLI flags for theme, plain, ASCII, and compact modes.
- Documentation and ASCII-only transcripts or asciinema recordings.
- Tests for rendering paths, config parsing, Click flags, subprocess display,
  history rendering, plain output, terminal widths, and environment fallbacks.

Bridge milestone:

- Internal lifecycle event/snapshot model for startup, iteration start, history
  summary, manager decision, prompt build, Codex start, Codex finish, DB log,
  help pause, completion, timeout, and error.
- Public wrapper-facing JSONL stream through `--event-stream PATH`.
- Importable event emitter API.
- Tests proving event payloads are raw and independent from Rich markup.

Linux visual milestone:

- Linux-only PySide6/Qt Quick/QML wrapper as an optional extra.
- CLI remains workflow engine, subprocess target, event producer, and API
  provider.
- CRT effects Rich cannot render faithfully.
- Linux development, packaging, release, troubleshooting, dependency, license,
  and operator-use notes.

### Out Of Scope

- Replacing Codex CLI.
- Requiring `cool-retro-term` or any external terminal emulator at runtime.
- Copying reference implementation details or assets.
- Rewriting the manager or summarizer prompt contract unless UI changes require
  clearer display metadata with matching tests and docs.
- macOS or Windows visual-wrapper support.

---

## Behavioral Guardrails

- Keep `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, and
  `build_codex_prompt()` stable unless the change explicitly concerns display
  metadata and updates all prompt-contract tests and docs.
- Store raw workflow data only. Do not write ANSI escapes, box characters,
  Rich markup, frame glyphs, visual tokens, secrets, or renderer snapshots to
  SQLite rows or JSONL events.
- Plain mode must be deterministic for logs and tests: no live-only displays,
  carriage-return animations, or terminal-specific glyphs.
- `--verbose` remains an output-depth control and must expose more captured
  Codex response detail than default mode.
- Renderer tests assert semantic sections and labels, not brittle full-frame
  snapshots.
- Base CLI installs remain lightweight and headless-safe.
- Source files stay ASCII-only and LF-only.
- Every visual element carries operational information; avoid decoration that
  hides manager decisions, prompts, errors, or completion state.
- Linux visual wrapper is a companion execution surface for the same autonomous
  engine, not a workflow fork.

---

## Session Plan

### Session 01: Config And Renderer Boundary

**Objective**: Create a tested UI configuration and rendering boundary around
the current single-file CLI without changing workflow behavior.

**Scope**:

- Add a bounded renderer module or internal renderer section with injected
  `Console` support.
- Resolve `ui.theme`, `ui.effect_level`, `ui.ascii`, `ui.compact`,
  `ui.show_elapsed`, `ui.show_provider`, and validated `ui.themes`.
- Add `--theme`, `--plain`, `--ascii`, and `--compact`.
- Define independent tokens, status labels, severity labels, warning labels,
  muted text, glyph sets, plain/ASCII fallbacks, and lifecycle snapshots.
- Route startup, iteration banners, manager decisions, prompt previews,
  response panels, DB notices, interrupts, completion, and history display
  through renderer helpers.
- Start with the smallest testable boundary; extract a module only when lower
  risk than extending `apex_infinite.py`.

**Tests**:

- Config defaults, CLI overrides, custom theme validation, invalid theme
  values, `NO_COLOR`, `TERM=dumb`, redirected output, non-TTY output,
  `Console().is_terminal == false`, SQLite history isolation.

**Outputs**:

- UI config resolver and renderer helpers.
- Built-in Python token definitions for `auto`, `crt-green`, `crt-amber`,
  `ibm-dos`, and `plain`.
- Validated custom YAML theme override schema.
- Focused config, Click, renderer, and history-isolation tests.

**Acceptance**:

- Existing prompt/routing tests pass unchanged.
- `--history`, `--dry-run`, and direct execution still function.
- Invalid themes fail fast with clear Click/config errors.
- `auto` chooses `crt-green` only for capable interactive TTYs and `plain` for
  constrained output unless `--theme` explicitly opts back in.
- SQLite history rows contain no ANSI escapes, Rich markup, frame glyphs, or
  styled output.
- Default output changes only through the renderer boundary.

### Session 02: Rich Operator Console

**Objective**: Implement the first cohesive Rich-based retro operator console.

**Scope**:

- Implement independently chosen `crt-green`, `crt-amber`, `ibm-dos`, and
  `plain` theme presets.
- Redesign startup as a compact boot/status panel.
- Replace iteration separators with stable iteration frames.
- Add status strips for provider, model, project, iteration, elapsed time,
  dry-run state, and current operation.
- Distinguish manager decisions, Codex prompts, agent output, errors, LLM
  retries, interrupts, timeouts, `help`, `alldonebaby`, and DB writes.
- Add low-fidelity scanline-like separators using repeated characters; disable
  them in `plain` and compact modes.
- Use only code points 0-127 in ASCII (`ascii`) mode.
- Validate width handling at 80, 100, and 120 columns.

**Outputs**:

- Rich operator-console views for normal interactive runs and fallbacks.
- Themed and fallback render states for important lifecycle outcomes.
- Renderer tests that assert semantic labels and section presence.

**Acceptance**:

- Interactive output has a coherent retro terminal look.
- Plain, ASCII, compact, `NO_COLOR`, non-TTY, redirected, and `TERM=dumb`
  paths remain readable.
- Narrow output does not hide errors, decisions, prompts, or completion state.
- Reference inspiration is visible in mood and structure without copied
  implementation material.

### Session 03: Subprocess And History Visibility

**Objective**: Improve long-running Codex subprocess awareness while preserving
captured-output semantics.

**Scope**:

- Add live elapsed subprocess display using `rich.status.Status`,
  `rich.progress`, `rich.live.Live`, or equivalent wrapper.
- If replacing `subprocess.run()` with `subprocess.Popen`, preserve stdout,
  stderr, return code, timeout text, stderr fallback, `FileNotFoundError`,
  generic exception reporting, dry-run, and verbose behavior.
- Show command timeout, elapsed time, and process state during `codex exec`.
- Redesign `--history` as a compact ledger with command, reason, timestamp,
  status, and truncated response summary.
- Extend existing `--verbose` to history mode with larger response/reason
  detail; do not add `--history-verbose`.
- Keep `~/.apex-infinite/history.db` readable without migration and preserve
  the `cc_response` column.

**Tests**:

- Subprocess success, stderr-only output, non-zero exit, timeout, dry-run,
  missing binary, and generic exception via fake runner or monkeypatch.
- History formatting for empty, short, and long records.

**Outputs**:

- Live subprocess display that does not leak styled output into history.
- Backward-compatible history rendering.
- Subprocess display and history formatting tests.

**Acceptance**:

- Operators can tell whether Codex is running and for how long.
- Captured stdout, stderr, exit code, timeout, and verbose behavior remain
  compatible.
- History mode is usable without horizontal scrolling.
- Styled output never enters stored history rows.

### Session 04: Event Stream Boundary

**Objective**: Create the minimum stable machine-readable lifecycle boundary
for future renderers and wrappers.

**Scope**:

- Separate config loading, DB access, LLM calls, manager decisions, prompt
  building, Codex execution, notification, and rendering as much as practical.
- Promote the internal lifecycle snapshot into a documented wrapper event
  design.
- Implement `--event-stream PATH` as a line-buffered JSONL file while keeping
  normal human stdout unchanged.
- Define the human-rendering disable mechanism needed for `--event-stream -`.
  Candidate names from the source plan were `--no-human-output`,
  `--machine-output`, or an equivalent internal mode; use an existing flag only
  if it already guarantees silent human rendering.
- Expose the same event emitter as an importable Python API.
- Add event names for iteration lifecycle, manager decisions, prompt dispatch,
  subprocess lifecycle, output summary, DB logging, help, completion, timeout,
  interrupts, and errors.
- Keep payloads raw: no Rich markup, ANSI escapes, frame glyphs, secrets, or
  reference-derived visual tokens.

**Tests**:

- Dry-run event order, event names, payload stability, file flushing, stdout
  collision prevention, and no real LLM/Codex calls.

**Outputs**:

- Documented lifecycle event interface and importable emitter API.
- `--event-stream PATH` JSONL support and guarded stdout JSONL behavior.
- Event tests for ordering, names, raw payloads, and stdout isolation.

**Acceptance**:

- Rich output and future wrappers can consume the same lifecycle facts.
- Wrappers can observe state without scraping terminal frames.
- Prompt routing, autonomous handoffs, and SQLite compatibility remain
  unchanged.
- `--event-stream -` cannot mix JSONL with Rich or plain human output.

### Session 05: Docs Samples And Runbooks

**Objective**: Document the operator experience, fallback behavior, event
contract, and clean-room visual boundary after behavior exists.

**Scope**:

- Update `apex-infinite-cli/README_apex-infinite-cli.md` with UI flags, config
  examples, theme descriptions, event-stream usage, and examples.
- Update the operator runbook with theme guidance and plain-output guidance for
  CI, logs, remote shells, constrained terminals, `NO_COLOR`, redirected
  output, and `TERM=dumb`.
- Update `apex-infinite-cli/docs/history-db.md` for status labels, truncation
  rules, or verbose history behavior.
- Update `apex-infinite-cli/docs/prompt-contract.md` with matching
  prompt-contract changes, or state that UI/event-stream changes do not alter
  `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or
  `build_codex_prompt()`.
- Add deterministic ASCII-only terminal transcripts or asciinema `.cast`
  files from fixture/dry-run output.
- Do not commit binary screenshots.
- Document `EXAMPLE/` as ignored, reference-only, GPL-licensed study material
  with a no-copying rule.
- Document the selected PySide6/QML wrapper path, qmltermwidget/QTermWidget and
  PyQt exclusions, and pywebview plus xterm.js backup.
- Add troubleshooting for unreadable colors, non-UTF terminals, terminal
  width, `NO_COLOR`, `TERM=dumb`, redirected output, remote shells, and
  event-stream misuse.

**Outputs**:

- Updated README and deep-dive docs for UI, history, prompt-contract impact,
  event stream, fallback behavior, and visual-wrapper direction.
- ASCII-only transcripts or `.cast` recordings.
- Troubleshooting guidance for fallback and compatibility modes.

**Acceptance**:

- Users can discover and configure the new look.
- Operators have clear fallback instructions for poor terminal rendering.
- Docs preserve the Apex Spec workflow contract and no-copy boundary.
- Event-stream docs do not imply wrappers parse Rich output.

### Session 06: Linux Wrapper Spike

**Objective**: Prove whether a standalone Linux visual wrapper can provide CRT
effects without changing the workflow engine.

**Scope**:

- Use PySide6 with Qt Quick/QML as the selected Linux wrapper path, packaged as
  an optional extra separate from the base CLI.
- Evaluate pywebview plus xterm.js only as a documented backup if a true
  terminal-emulator viewport becomes mandatory.
- Launch the CLI as a subprocess and consume the Session 04 JSONL event stream.
- Do not embed a pseudo-terminal, scrape Rich output, or depend on
  `cool-retro-term` at runtime.
- Prototype an event-driven visual console with a read-only terminal-like log
  viewport, theme selector, status panels, and enough effects to validate glow,
  scanlines, flicker, curvature, frame treatment, and timing.
- Use the reference render pipeline only as a feasibility checklist: source
  surface, optional bloom source, dynamic/effects pass, static/final pass,
  frame pass, frame buffer, and timing driver.
- Study but do not copy profile, screen, terminal, effects,
  advanced/performance, import/export, and persistence settings groups.
- Document build dependencies, packaging risks, license obligations, the
  CLI/wrapper interface contract, and the empty local qmltermwidget placeholder.
- Keep prototype code isolated from the Rich milestone until accepted.
- Do not use PyQt, qmltermwidget, QTermWidget, copied QML, copied shaders,
  copied images, copied icons, copied fonts, resource manifests, or literal
  profile data.

**Outputs**:

- Standalone PySide6/QML Linux prototype, or documented evidence that a
  technical/licensing blocker requires deferral.
- License, dependency, toolkit, and packaging assessment.
- Decision record for PySide6/QML as selected path and pywebview/xterm.js as
  backup.

**Acceptance**:

- Prototype can launch or display an Apex Infinite session through the event
  stream, or documents the exact blocker forcing deferral.
- Prototype demonstrates visual effects Rich cannot render faithfully.
- Selected path has an explicit license and dependency story.
- Base CLI install remains unaffected by graphical dependencies.

### Session 07: Linux Visual Wrapper Productization

**Objective**: Turn the accepted Linux wrapper prototype into an optional
standalone visual mode, or record a precise deferral.

**Scope**:

- If Session 06 is accepted, implement the PySide6/Qt Quick/QML Linux-only
  wrapper in a maintainable optional-extra directory structure.
- Use the Session 04 subprocess plus JSONL event-stream boundary rather than
  scraping themed Rich output.
- Add independently designed amber CRT, green CRT, and IBM DOS inspired
  presets.
- Add controls for effect intensity, font, scaling, reduced effects, and plain
  fallback.
- Add Linux development, packaging, release, and troubleshooting instructions.
- Add smoke tests for wrapper launch, CLI subprocess/event-stream invocation,
  timeout display, non-zero exit display, missing CLI display, malformed event
  display, and generic failure display.
- Keep wrapper dependencies optional so base CLI installs remain lightweight
  and headless-safe.
- If blocked, replace productization with a deferral note naming the blocker,
  recording evidence, and identifying minimum evidence needed to reopen wrapper
  work.

**Outputs**:

- Optional standalone Linux visual mode, or clear deferral record.
- Packaging, setup, license, and troubleshooting docs.
- Wrapper smoke tests and fallback behavior if productized.

**Acceptance**:

- Users can run visual mode without installing or launching `cool-retro-term`.
- Visual mode preserves the same workflow decisions and safety behavior as the
  CLI.
- Base CLI remains usable without graphical dependencies.
- If deferred, blocker and reopen criteria are explicit and testable.

### Session 08: Release Verification

**Objective**: Verify the full upgrade against compatibility, documentation,
testing, release, and clean-room completion criteria.

**Scope**:

- Run the CLI test suite and all applicable rendering, config, Click, history,
  subprocess, plain-mode, event, docs, and wrapper tests.
- Smoke test with a real initialized Apex Spec project and a small
  `--max-iterations` value.
- Verify `--dry-run`, `--history`, `--verbose`, `--plain`, `--ascii`,
  `--compact`, `--event-stream PATH`, guarded `--event-stream -`, every
  built-in theme, `NO_COLOR`, non-TTY output, redirected output, and
  `TERM=dumb`.
- Confirm source files are ASCII-only and LF-only.
- Confirm history rows contain raw workflow data and no styled output.
- Confirm event rows contain raw operational facts and no Rich/reference
  tokens.
- Confirm no reference source, shader, image, icon, font, resource manifest,
  literal profile data, or GPL code was copied.
- Confirm docs describe UI controls, prompt-contract impact, fallback
  behavior, event-stream behavior, wrapper boundary, dependency plan, and
  license assessment.
- If wrapper shipped, run launch and failure-mode smoke tests.
- If wrapper deferred, verify deferral is explicit and base CLI improvements
  are complete.
- Trace every completion criterion to a passing check, shipped artifact, or
  explicit deferral.
- Limit fixes to small compatibility repairs discovered during release
  testing.

**Outputs**:

- Final verification notes or checklist results.
- Small compatibility fixes.
- Clear status on whether PySide6/QML shipped, was deferred by a named blocker,
  or remains documented as near-future work.

**Acceptance**:

- Existing workflow behavior remains compatible.
- Prompt contract is unchanged or updated with matching tests and docs.
- Users can enable the UI, disable it cleanly, and operate safely in
  constrained terminals.
- Source-plan completion criteria are satisfied or explicitly deferred with
  rationale.

---

## Testing Plan

- Run `pytest tests/ -v` from `apex-infinite-cli/`.
- Keep prompt/routing tests green unless a session explicitly updates prompt
  contract and docs.
- Use `Console(record=True, width=...)` for representative rendered output.
- Add Click `CliRunner` tests for new flags and invalid option combinations.
- Use temporary DB paths or monkeypatched `DB_DIR`/`DB_PATH` for history tests.
- Validate widths at 80, 100, and 120 columns.
- Exercise `--dry-run`, `--history`, `--verbose`, `--plain`, `--ascii`, and
  every built-in theme.
- Verify `NO_COLOR=1` disables color unless explicitly overridden.
- Verify `TERM=dumb`, redirected output, and non-TTY paths choose plain output
  by default.
- Verify history rows contain raw agent responses, not styled output.
- Verify subprocess display preserves success, stderr-only output, non-zero
  exit wrapping, timeout text, missing binary, dry-run, generic exception, and
  verbose behavior.
- Validate `--event-stream PATH`, `--event-stream -` with human rendering
  disabled, event order, event names, file flushing, stdout isolation, and raw
  payloads with dry-run fixtures.
- Confirm source files remain ASCII-only and LF-only.
- Smoke test with a real initialized Apex Spec project and a very small
  `--max-iterations` value.

---

## Risks And Mitigations

| Risk | Mitigation |
|------|------------|
| Retro styling reduces readability | Keep contrast high, effects low by default, and provide `--plain` |
| Terminal compatibility varies | Add `--ascii`, compact/plain modes, `NO_COLOR`, `TERM=dumb`, non-TTY, redirected-output, and width tests |
| Output becomes hard to parse in logs | Keep plain mode stable and avoid hiding important text behind live-only views |
| Styled output pollutes durable records | Store raw data only and test SQLite/JSONL for no ANSI, Rich markup, glyphs, visual tokens, or secrets |
| Live subprocess display changes behavior | Preserve stdout, stderr, return code, timeout, dry-run, missing-binary, generic-exception, and verbose semantics with tests |
| Clean-room visual work drifts into copied material | Use the reference as a concept checklist only; audit copied code, shaders, assets, fonts, profile data, manifests, and build scripts |
| Dependency creep | Finish the Rich milestone first and isolate wrapper dependencies |
| PySide6 LGPL compliance is missed | Keep PySide6 optional, document LGPLv3/commercial obligations, avoid GPL-only Qt modules, and keep base CLI independent |
| PyQt licensing conflicts with MIT repo | Avoid PyQt unless a future commercial/GPL-compatible decision explicitly approves it |
| Snapshot tests become brittle | Test semantic markers and config behavior more than exact frames |
| Wrapper diverges from CLI behavior | Use one workflow engine and make wrapper a display/runtime shell |
| Config precedence surprises operators | Document and test CLI flag, `NO_COLOR`, non-TTY, redirected, and config precedence |
| Single-file CLI becomes harder to maintain | Split renderer/config/event helpers only when lower risk than extending `apex_infinite.py` |
| qmltermwidget reference is unavailable locally | Treat empty submodule placeholders as unavailable; do not use qmltermwidget or QTermWidget in selected path |
| Graphical wrapper burdens headless installs | Keep wrapper dependencies optional and Linux-only setup documented separately |
| Release verification finds late regressions | Keep Session 08 focused on final checks and small compatibility fixes |

---

## Success Criteria

Phase complete when:

- [ ] All 8 sessions are completed or explicitly deferred where allowed.
- [ ] Existing prompt, routing, autonomous manager, and workflow behavior remain
  compatible and covered by tests.
- [ ] Operator UI config supports built-in themes, custom validated themes,
  plain mode, ASCII mode, compact mode, and deterministic environment fallback
  rules.
- [ ] Users can enable the new UI, disable it cleanly, and operate safely in
  constrained terminals.
- [ ] Rich views cover startup, iteration, manager decision, prompt, Codex
  execution, results, DB writes, help, completion, interrupts, timeouts, LLM
  retries, and errors.
- [ ] History display is readable and backward compatible with existing SQLite
  databases.
- [ ] Existing history databases remain readable without migration.
- [ ] JSONL events emit raw lifecycle facts without Rich markup, ANSI escapes,
  frame glyphs, copied visual tokens, or secrets.
- [ ] README and deep-dive docs describe UI flags, config, theme controls,
  fallback behavior, event stream, prompt-contract impact, clean-room boundary,
  wrapper path, dependency plan, and license assessment.
- [ ] Optional Linux wrapper path is productized with isolated dependencies and
  smoke tests, or explicitly deferred by Session 07 evidence.
- [ ] Release verification traces every criterion to a passing check, shipped
  artifact, or explicit deferral.
- [ ] No reference source, shader, image, icon, font, resource manifest, build
  script, GPL code, or literal profile data is copied into the CLI.
- [ ] The CLI has a coherent CRT-inspired default or opt-in look that directly
  references `cool-retro-term` as inspiration in docs.
- [ ] Tests cover config parsing, renderer behavior, Click options, history
  output, plain mode, `NO_COLOR`, non-TTY output, and subprocess display.
- [ ] The near-future Linux wrapper path is standalone and does not depend on
  running inside `cool-retro-term`.

---

## Dependencies And Handoff

Depends on:

- Initialized Apex Spec System PRD and state files.
- Existing Apex Infinite CLI baseline in `apex-infinite-cli/`.

Enables:

- Session workflow planning for
  `phase00-session01-config-and-renderer-boundary`.
- Full Apex Infinite CLI upgrade release readiness after Session 08.

Next command: `plansession`
Reason: Phase 00 is defined, not started, and ready for the first scoped
session plan.

---

## Reference Catalog

All paths are study references only. Do not copy source, assets, shaders,
compiled artifacts, fonts, manifests, icons, profile data, or build scripts.

### Local Reference Root And License Evidence

- Root: `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term`
- README and overview:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/README.md`
- GPL/license evidence:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-2.0.txt`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-3.0.txt`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/packaging/debian/copyright`
- Submodule evidence:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/qmltermwidget`

`EXAMPLE/cool-retro-term/qmltermwidget` exists as an empty local submodule
placeholder. Treat qmltermwidget and KDSingleApplication as unavailable unless
intentionally populated later.

### QML And UI References

- Application shell, window creation, global settings, time driver:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml`
- Terminal/session lifecycle, viewport, scroll, selection, paste, mouse, wheel,
  focus, and corrected mouse coordinates under distortion, especially
  `PreprocessedTerminal.qml`:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`
- Settings groups, profile management, import/export, frame settings,
  persistence, general/terminal/effects/advanced controls:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml`
- Frame, size overlay, render-stage separation, burn-in, shader/effect stages:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml`
- Menus, profile switching, copy/paste, settings, fullscreen, zoom, new tab:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/FullContextMenu.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/ShortContextMenu.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/WindowMenu.qml`
- Dialog and reusable control concepts:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/AboutDialog.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/InsertNameDialog.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ColorButton.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SimpleSlider.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/CheckableSlider.qml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Components/SizedLabel.qml`
- Utility color/math categories only:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/utils.js`
- Resource manifest, image assets, and texture references:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png`

### C++ Bridge, Fonts, Build, Packaging, And Icons

- C++ app bootstrap, arguments, metadata, import paths, file I/O:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h`
- Font handling concepts, then choose independent system-font behavior:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h`
- Build and packaging surfaces:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.desktop`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/snap/snapcraft.yaml`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/scripts/build-appimage.sh`
- Icon assets:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/32x32/cool-retro-term.png`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/64x64/cool-retro-term.png`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/128x128/cool-retro-term.png`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/256x256/cool-retro-term.png`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/crt.icns`

### Shader References

Study shader categories only; do not copy source, constants, formulas, or
compiled `.qsb` blobs.

- Burn-in:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.vert`
- Pass-through vertex:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/passthrough.vert`
- Dynamic terminal, including rasterization, burn-in overlay, display-frame
  influence, chroma, flicker, horizontal sync, glow line, jitter, static noise:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert`
- Static terminal, including RGB shift, bloom, curvature, frame shininess,
  brightness, final composition:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.vert`
- Terminal frame:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.vert`
- Compiled shader examples and location:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic_raster0_burn0_frame0_chroma0.frag.qsb`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static_rgb0_bloom0_curve0_shine0.frag.qsb`
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders`

### Built-In Profile Names

Defined in `ApplicationSettings.qml`; use as visual mood checklist only, not
literal data:

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

### Bundled Font Asset References

Do not copy these fonts or licenses; use only to understand CRT and
old-computer typography range.

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
