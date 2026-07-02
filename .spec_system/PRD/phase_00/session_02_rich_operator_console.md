# Session 02: Rich Operator Console

**Session ID**: `phase00-session02-rich-operator-console`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Implement the first cohesive Rich-based retro operator console experience using
the renderer and configuration boundary from Session 01.

---

## Scope

### In Scope (MVP)

- Implement independently chosen `crt-green`, `crt-amber`, `ibm-dos`, and
  `plain` theme presets using the Phase 00 token model.
- Redesign startup as a compact boot/status panel.
- Replace iteration separators with stable iteration frames.
- Add status strips for provider, model, project, iteration, elapsed time,
  dry-run state, and current operation.
- Distinguish manager decisions, Codex prompts, agent output, errors, LLM
  retries, interrupts, timeouts, `help`, `alldonebaby`, and DB writes.
- Add low-fidelity scanline-like separators using independently chosen repeated
  ASCII-compatible characters, with automatic disablement in `plain` and
  compact modes.
- Validate styled, plain, ASCII, and compact output at 80, 100, and 120
  columns.

### Out of Scope

- Rewriting manager prompt routing or prompt text for display-only behavior.
- Changing SQLite schema or stored history semantics.
- Public event-stream API or graphical wrapper implementation.

---

## Prerequisites

- [ ] Session 01 validated.
- [ ] Renderer helpers and UI config resolver exist.
- [ ] Clean-room visual boundary from the phase PRD is reviewed.

---

## Deliverables

1. Rich operator-console views for normal interactive runs and fallbacks.
2. Themed render states for core lifecycle outcomes and failure paths.
3. Renderer tests that assert semantic labels, sections, and fallback behavior.

---

## Success Criteria

- [ ] Normal interactive output presents a coherent operator-console look.
- [ ] Plain, ASCII, compact, `NO_COLOR`, non-TTY, and `TERM=dumb` paths remain
  readable.
- [ ] Narrow output does not hide errors, decisions, prompts, or completion
  state.
- [ ] Visual direction references the local `cool-retro-term` study material
  only through independent mood, hierarchy, labels, and layout choices.

---

## Folded Source Plan Details

<!-- FOLDED_SESSION_SOURCE_START -->

This section carries forward the actionable session material formerly stored in
`docs/ongoing-projects/apex-infinite-cli-upgrade-plan.md`. The Phase 00 PRD
contains the verbatim archive; this stub keeps the session-specific details and
full-path `EXAMPLE/` references close to the session executor.

### EXAMPLE Reference Links

- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/README.md](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/README.md)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/utils.js](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/utils.js)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png)

### Detailed Session Split Source

`````markdown
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
`````

### Mapped Rough Implementation Source

`````markdown
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
`````

<!-- FOLDED_SESSION_SOURCE_END -->
