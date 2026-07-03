# Session 05: Docs Samples And Runbooks

**Session ID**: `phase00-session05-docs-samples-and-runbooks`
**Status**: Complete
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Document the operator experience, fallback behavior, event contract, and
clean-room visual boundary after the implemented behavior exists.

---

## Scope

### In Scope (MVP)

- Update `apex-infinite-cli/README_apex-infinite-cli.md` with UI flags, config
  examples, theme descriptions, event-stream usage, and examples.
- Update the operator runbook with theme guidance and plain-output guidance for
  CI, logs, remote shells, constrained terminals, `NO_COLOR`, redirected
  output, and `TERM=dumb`.
- Update `apex-infinite-cli/docs/history-db.md` if display changes add status
  labels, truncation rules, or verbose history behavior.
- Update `apex-infinite-cli/docs/prompt-contract.md` with matching
  prompt-contract changes or a note that UI and event changes do not alter
  prompt routing.
- Add deterministic ASCII-only terminal transcripts or asciinema `.cast` files
  from fixture or dry-run output; do not commit binary screenshots.
- Document the local `EXAMPLE/` tree as ignored, reference-only,
  GPL-family-licensed study material and document the no-copying rule.
- Document the selected PySide6/QML wrapper path, qmltermwidget/QTermWidget and
  PyQt exclusions, and the pywebview plus xterm.js backup option.
- Add troubleshooting for unreadable colors, non-UTF terminals, terminal
  width, `NO_COLOR`, `TERM=dumb`, redirected output, remote shells, and
  event-stream misuse.

### Out of Scope

- Productizing the Linux visual wrapper.
- Adding binary screenshots or copied reference assets.
- Reopening implemented UI behavior without a concrete documentation or test
  failure.

---

## Prerequisites

- [x] Sessions 01 through 04 validated.
- [x] Implemented flags, config keys, event behavior, and fallback behavior are
  available to document.
- [x] Clean-room and license boundaries are reviewed against the phase PRD.

---

## Deliverables

1. Updated README and deep-dive docs for UI, history, prompt-contract impact,
   event stream, fallback behavior, and wrapper direction.
2. ASCII-only transcripts or `.cast` recordings when useful.
3. Troubleshooting guidance for fallback and compatibility modes.

---

## Success Criteria

- [x] Users can discover and configure the new look from documentation.
- [x] Operators have clear fallback instructions for poor terminal rendering.
- [x] Docs preserve the Apex Spec workflow contract and no-copying boundary.
- [x] Event-stream usage is documented without implying that wrappers parse
  Rich output.

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
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml)

### Detailed Session Split Source

`````markdown
### Session 05: Docs Samples And Runbooks

**Objective**: Document the operator experience, fallback behavior, event
contract, and clean-room visual boundary after the implemented behavior exists.

**Scope**:
- Update `apex-infinite-cli/README_apex-infinite-cli.md` with UI flags,
  config examples, theme descriptions, event-stream usage, and examples.
- Update the operator runbook with theme guidance and plain-output guidance for
  CI, logs, remote shells, constrained terminals, `NO_COLOR`, redirected
  output, and `TERM=dumb`.
- Update `apex-infinite-cli/docs/history-db.md` if display changes add status
  labels, truncation rules, or verbose history behavior.
- Update `apex-infinite-cli/docs/prompt-contract.md` with either matching
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
`````

### Mapped Rough Implementation Source

The rough implementation plan numbered this as Session 4 because an earlier ordering placed documentation before the event stream. Phase 00 now keeps the event boundary before documentation so docs describe implemented behavior.

`````markdown
### Session 4: Documentation, Samples, And Polish

Objective: make the upgrade easy to understand and maintain.

Tasks:

- Update `apex-infinite-cli/README_apex-infinite-cli.md` with UI flags,
  config examples, and theme descriptions.
- Update the operator runbook with recommended theme settings and plain-output
  guidance for CI or remote shells.
- Update `apex-infinite-cli/docs/history-db.md` if history display changes
  expose new status labels or summary rules.
- Update `apex-infinite-cli/docs/prompt-contract.md` only if prompt routing or
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
`````

<!-- FOLDED_SESSION_SOURCE_END -->
