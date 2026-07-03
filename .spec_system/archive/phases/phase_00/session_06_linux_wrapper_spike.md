# Session 06: Linux Wrapper Spike

**Session ID**: `phase00-session06-linux-wrapper-spike`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Prove whether a standalone Linux visual wrapper can provide CRT effects without
changing the Apex Infinite CLI workflow engine.

---

## Scope

### In Scope (MVP)

- Use PySide6 with Qt Quick/QML as the selected Linux wrapper path, packaged as
  an optional extra separate from the base CLI.
- Evaluate pywebview plus xterm.js only as a documented backup if a true
  terminal-emulator viewport becomes mandatory.
- Launch the CLI as a subprocess and consume the Session 04 JSONL event stream.
- Avoid embedding a pseudo-terminal, scraping Rich output, or depending on
  `cool-retro-term` at runtime.
- Prototype an event-driven visual console with a read-only terminal-like log
  viewport, theme selector, status panels, and enough effects to validate glow,
  scanlines, flicker, curvature, frame treatment, and timing feasibility.
- Use the local reference render pipeline only as a feasibility checklist.
- Document build dependencies, packaging risks, license obligations, CLI/wrapper
  interface contract, and the empty local qmltermwidget placeholder.
- Keep prototype code isolated from the Rich milestone until the approach is
  accepted.

### Out of Scope

- Productizing the wrapper for release.
- Copying QML, shaders, assets, fonts, icons, profile data, resource manifests,
  build scripts, or terminal-emulator code from reference material.
- Adding PySide6 or any graphical dependency to the base CLI install path.
- Using PyQt, qmltermwidget, QTermWidget, or a copied terminal emulator.

---

## Prerequisites

- [ ] Sessions 01 through 05 validated.
- [ ] `--event-stream PATH` and importable event emitter API exist.
- [ ] Clean-room visual and license boundaries are reviewed before writing
  prototype code.

---

## Deliverables

1. Standalone PySide6/QML Linux prototype or documented blocker evidence.
2. License, dependency, toolkit, and packaging assessment.
3. Decision record for PySide6/QML as the selected path and pywebview plus
   xterm.js as the backup option.

---

## Success Criteria

- [ ] Prototype can launch or display an Apex Infinite session through the event
  stream, or the plan documents the exact blocker that forces deferral.
- [ ] Prototype demonstrates visual effects Rich cannot faithfully render.
- [ ] The selected path has an explicit license and dependency story.
- [ ] Base CLI installation remains unaffected by graphical dependencies.

---

## Folded Source Plan Details

<!-- FOLDED_SESSION_SOURCE_START -->

This section carries forward the actionable session material formerly stored in
`docs/ongoing-projects/apex-infinite-cli-upgrade-plan.md`. The Phase 00 PRD
contains the verbatim archive; this stub keeps the session-specific details and
full-path `EXAMPLE/` references close to the session executor.

### EXAMPLE Reference Links

- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.vert](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.vert)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/passthrough.vert](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/passthrough.vert)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.vert](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.vert)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.vert](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.vert)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules)

### Detailed Session Split Source

`````markdown
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
`````

### Mapped Rough Implementation Source

`````markdown
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
`````

<!-- FOLDED_SESSION_SOURCE_END -->
