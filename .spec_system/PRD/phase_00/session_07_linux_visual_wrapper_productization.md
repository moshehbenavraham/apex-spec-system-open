# Session 07: Linux Visual Wrapper Productization

**Session ID**: `phase00-session07-linux-visual-wrapper-productization`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Turn the accepted Linux wrapper prototype into an optional standalone visual
mode, or record a precise deferral if the spike blocks.

---

## Scope

### In Scope (MVP)

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
- Keep wrapper dependencies optional so base CLI installs remain lightweight
  and headless-safe.
- If Session 06 uncovers a blocker, replace productization with a deferral note
  that names the blocker, records evidence, and identifies the minimum evidence
  needed to reopen wrapper work.

### Out of Scope

- Making the base CLI require PySide6, Qt, a graphical display, or wrapper
  assets.
- Scraping Rich output or forking manager decisions, prompt routing, storage, or
  safety behavior.
- Shipping macOS or Windows wrapper support.

---

## Prerequisites

- [ ] Session 06 accepted or completed with a documented blocker.
- [ ] Session 04 event boundary remains stable.
- [ ] Optional dependency and license requirements are documented before release
  work lands.

---

## Deliverables

1. Optional standalone Linux visual mode, or a clear deferral record.
2. Packaging, setup, license, and troubleshooting documentation.
3. Wrapper smoke tests and fallback behavior when productized.

---

## Success Criteria

- [ ] Users can run the visual mode without installing or launching
  `cool-retro-term`.
- [ ] Visual mode preserves the same workflow decisions and safety behavior as
  the CLI.
- [ ] Base CLI installation remains usable without graphical dependencies.
- [ ] If deferred, the blocker and reopen criteria are explicit and testable.

---

## Folded Source Plan Details

<!-- FOLDED_SESSION_SOURCE_START -->

This section carries forward the actionable session material formerly stored in
`docs/ongoing-projects/apex-infinite-cli-upgrade-plan.md`. The Phase 00 PRD
contains the verbatim archive; this stub keeps the session-specific details and
full-path `EXAMPLE/` references close to the session executor.

### EXAMPLE Reference Links

- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/FullContextMenu.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/FullContextMenu.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/ShortContextMenu.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/ShortContextMenu.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/WindowMenu.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/WindowMenu.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.desktop](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.desktop)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/snap/snapcraft.yaml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/snap/snapcraft.yaml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/scripts/build-appimage.sh](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/scripts/build-appimage.sh)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/32x32/cool-retro-term.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/32x32/cool-retro-term.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/64x64/cool-retro-term.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/64x64/cool-retro-term.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/128x128/cool-retro-term.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/128x128/cool-retro-term.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/256x256/cool-retro-term.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/256x256/cool-retro-term.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/crt.icns](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/crt.icns)

### Detailed Session Split Source

`````markdown
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
`````

### Mapped Rough Implementation Source

`````markdown
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
`````

<!-- FOLDED_SESSION_SOURCE_END -->
