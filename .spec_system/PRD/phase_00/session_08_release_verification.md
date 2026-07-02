# Session 08: Release Verification

**Session ID**: `phase00-session08-release-verification`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Verify the full Apex Infinite CLI upgrade against compatibility,
documentation, testing, release, and clean-room completion criteria.

---

## Scope

### In Scope (MVP)

- Run the CLI test suite and all focused rendering, config, Click, history,
  subprocess, plain-mode, event, docs, and wrapper tests that apply.
- Smoke test with a real initialized Apex Spec project and a small
  `--max-iterations` value.
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
  deferred, verify the deferral is explicit and base CLI improvements are
  complete.

### Out of Scope

- Starting new feature work that should have been scoped to Sessions 01 through
  07.
- Reopening wrapper architecture decisions without a failing verification
  result.
- Creating binary screenshots or copying reference assets.

---

## Prerequisites

- [ ] Sessions 01 through 07 completed or explicitly deferred where allowed.
- [ ] Documentation and tests from prior sessions are committed to local working
  tree.
- [ ] Clean-room verification checklist is available from the source upgrade
  plan.

---

## Deliverables

1. Final verification notes or checklist results.
2. Small compatibility fixes found during release testing.
3. Clear status on whether the selected PySide6/QML wrapper path shipped, was
   deferred by a named blocker, or remains documented as near-future work.

---

## Success Criteria

- [ ] Existing workflow behavior remains compatible.
- [ ] Prompt contract is unchanged or updated with matching tests and
  documentation.
- [ ] Users can enable the new UI, disable it cleanly, and operate safely in
  constrained terminals.
- [ ] Completion criteria in the source plan are satisfied or explicitly
  deferred with rationale.

---

## Folded Source Plan Details

<!-- FOLDED_SESSION_SOURCE_START -->

This section carries forward the actionable session material formerly stored in
`docs/ongoing-projects/apex-infinite-cli-upgrade-plan.md`. The Phase 00 PRD
contains the verbatim archive; this stub keeps the session-specific details and
full-path `EXAMPLE/` references close to the session executor.

### EXAMPLE Reference Links

- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/README.md](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/README.md)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-2.0.txt](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-2.0.txt)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-3.0.txt](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-3.0.txt)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/packaging/debian/copyright](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/packaging/debian/copyright)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.vert](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.vert)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/passthrough.vert](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/passthrough.vert)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.vert](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.vert)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.vert](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.vert)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic_raster0_burn0_frame0_chroma0.frag.qsb](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic_raster0_burn0_frame0_chroma0.frag.qsb)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static_rgb0_bloom0_curve0_shine0.frag.qsb](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static_rgb0_bloom0_curve0_shine0.frag.qsb)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/32x32/cool-retro-term.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/32x32/cool-retro-term.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/64x64/cool-retro-term.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/64x64/cool-retro-term.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/128x128/cool-retro-term.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/128x128/cool-retro-term.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/256x256/cool-retro-term.png](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/256x256/cool-retro-term.png)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/crt.icns](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/crt.icns)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.desktop](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.desktop)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/snap/snapcraft.yaml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/snap/snapcraft.yaml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/scripts/build-appimage.sh](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/scripts/build-appimage.sh)

### Detailed Session Split Source

`````markdown
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
`````

### Mapped Rough Implementation Source

No separate rough implementation-session section existed for Session 08. Its
release-verification scope is preserved in the detailed session split above and
in the global testing plan, risks, resolved decisions, and completion criteria
archived in the Phase 00 PRD.

<!-- FOLDED_SESSION_SOURCE_END -->
