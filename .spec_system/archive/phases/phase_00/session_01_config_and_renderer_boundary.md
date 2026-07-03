# Session 01: Config And Renderer Boundary

**Session ID**: `phase00-session01-config-and-renderer-boundary`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Create a tested UI configuration and rendering boundary around the current CLI
without changing Apex Infinite workflow behavior.

---

## Scope

### In Scope (MVP)

- Add a bounded renderer module or internal renderer section with injected
  `Console` support for tests.
- Resolve UI settings for `ui.theme`, `ui.effect_level`, `ui.ascii`,
  `ui.compact`, `ui.show_elapsed`, `ui.show_provider`, and validated
  `ui.themes` overrides.
- Add Click options for `--theme`, `--plain`, `--ascii`, and `--compact`.
- Define independent theme tokens, status labels, severity labels, glyph sets,
  plain and ASCII fallbacks, and a minimal lifecycle snapshot shape.
- Route startup, iteration banners, manager decisions, prompt previews,
  response panels, DB log notices, interrupts, completion, and history display
  through renderer helpers.
- Add tests for config defaults, Click overrides, invalid theme values,
  `NO_COLOR`, `TERM=dumb`, redirected or non-TTY output, custom theme
  validation, and SQLite history isolation.

### Out of Scope

- Full retro operator-console visual redesign.
- Live Codex subprocess display changes.
- Public JSONL event stream or wrapper-facing event API.
- Graphical wrapper dependencies or wrapper code.

---

## Prerequisites

- [ ] Phase 00 PRD and session stubs exist.
- [ ] Current prompt and routing tests are available as compatibility checks.
- [ ] Current `apex-infinite-cli/config.yaml` and `apex_infinite.py` behavior is
  reviewed before editing.

---

## Deliverables

1. UI config resolver and validated theme token definitions.
2. Renderer helpers with injectable `Console` support.
3. CLI flag wiring for theme, plain, ASCII, and compact modes.
4. Focused config, Click, renderer, and history-isolation tests.

---

## Success Criteria

- [ ] Existing prompt and routing tests pass unchanged.
- [ ] `--history`, `--dry-run`, and direct execution still function.
- [ ] Invalid theme names and malformed custom theme config fail fast.
- [ ] `auto` resolves to styled output only for capable interactive terminals
  and to `plain` under constrained output conditions.
- [ ] No ANSI escapes, Rich markup, frame glyphs, or styled output are written
  to SQLite history rows.

---

## Folded Source Plan Details

<!-- FOLDED_SESSION_SOURCE_START -->

This section carries forward the actionable session material formerly stored in
`docs/ongoing-projects/apex-infinite-cli-upgrade-plan.md`. The Phase 00 PRD
contains the verbatim archive; this stub keeps the session-specific details and
full-path `EXAMPLE/` references close to the session executor.

### EXAMPLE Reference Links

- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ColorButton.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ColorButton.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SimpleSlider.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SimpleSlider.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/CheckableSlider.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/CheckableSlider.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Components/SizedLabel.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Components/SizedLabel.qml)

### Detailed Session Split Source

`````markdown
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
`````

### Mapped Rough Implementation Source

`````markdown
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
`````

<!-- FOLDED_SESSION_SOURCE_END -->
