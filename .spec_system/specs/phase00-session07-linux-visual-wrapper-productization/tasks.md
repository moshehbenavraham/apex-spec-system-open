# Task Checklist

**Session ID**: `phase00-session07-linux-visual-wrapper-productization`
**Total Tasks**: 20
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (3 tasks)

- [x] T001 [S0007] Verify analyzer state, Session 06 validation, spike acceptance, optional wrapper dependencies, and Session 07 prerequisites before editing wrapper files (`.spec_system/scripts/analyze-project.sh`, `.spec_system/specs/phase00-session06-linux-wrapper-spike/validation.md`, `apex-infinite-cli/docs/visual-wrapper-spike.md`)
- [x] T002 [S0007] Audit the current wrapper prototype, event stream contract, and machine-output guardrails for productization gaps (`apex-infinite-cli/apex_infinite_visual/`, `apex-infinite-cli/apex_infinite_events.py`, `apex-infinite-cli/docs/event-stream.md`)
- [x] T003 [S0007] Confirm clean-room, license, optional dependency, and base CLI boundary constraints before changing visual wrapper behavior (`apex-infinite-cli/docs/visual-wrapper-boundary.md`, `.spec_system/SECURITY-COMPLIANCE.md`, `apex-infinite-cli/requirements-wrapper.txt`)

---

## Foundation (5 tasks)

- [x] T004 [S0007] [P] Create a validated productized wrapper settings model for theme presets, effect intensity, font family, font scale, reduced effects, and plain fallback (`apex-infinite-cli/apex_infinite_visual/settings.py`)
- [x] T005 [S0007] [P] Extend event-state mappings for launch, timeout, non-zero exit, stderr, missing CLI, and malformed event conditions with schema-validated input and explicit error mapping (`apex-infinite-cli/apex_infinite_visual/events.py`)
- [x] T006 [S0007] [P] Harden the CLI launcher with source-tree validation, missing CLI checks, process timeout handling, stderr and return-code failure summaries, and cleanup on scope exit for all acquired resources (`apex-infinite-cli/apex_infinite_visual/launcher.py`)
- [x] T007 [S0007] Wire the PySide6 bridge to the settings model with launch validation, state reset on re-entry, duplicate-trigger prevention while in-flight, and cleanup on stop or wrapper exit (`apex-infinite-cli/apex_infinite_visual/main.py`)
- [x] T008 [S0007] Update package exports, productized wrapper metadata, and CLI help text without importing PySide6 from the base CLI runtime path (`apex-infinite-cli/apex_infinite_visual/__init__.py`, `apex-infinite-cli/apex_infinite_visual/main.py`)

---

## Implementation (7 tasks)

- [x] T009 [S0007] Update the QML surface with productized run, status, failure, theme, effect intensity, font, scale, reduced-effects, and plain fallback controls with platform-appropriate accessibility labels, focus management, and input support (`apex-infinite-cli/apex_infinite_visual/qml/Main.qml`)
- [x] T010 [S0007] Wire green CRT, amber CRT, IBM DOS, and plain presets through Python settings and QML state without copied profile data or literal reference constants (`apex-infinite-cli/apex_infinite_visual/settings.py`, `apex-infinite-cli/apex_infinite_visual/main.py`, `apex-infinite-cli/apex_infinite_visual/qml/Main.qml`)
- [x] T011 [S0007] Implement product-facing failure surfaces for missing CLI, missing PySide6, display-backend failure, malformed JSONL, timeout, stderr, non-zero exit, and operator stop with explicit loading, empty, error, and offline states (`apex-infinite-cli/apex_infinite_visual/main.py`, `apex-infinite-cli/apex_infinite_visual/qml/Main.qml`)
- [x] T012 [S0007] Clarify optional wrapper and packaging dependency boundaries for PySide6, pyside6-deploy, Nuitka, AppImage review, and base CLI isolation (`apex-infinite-cli/requirements-wrapper.txt`, `apex-infinite-cli/docs/visual-wrapper-productization.md`)
- [x] T013 [S0007] Create the productization guide with Linux source setup, run commands, smoke checks, packaging path, release gates, license notices, checksums, source/relink obligations, and clean-room verification (`apex-infinite-cli/docs/visual-wrapper-productization.md`)
- [x] T014 [S0007] Update README, operator runbook, and wrapper boundary docs with source visual mode usage, settings behavior, release status, and Session 07 boundaries (`apex-infinite-cli/README_apex-infinite-cli.md`, `apex-infinite-cli/docs/operator-runbook.md`, `apex-infinite-cli/docs/visual-wrapper-boundary.md`)
- [x] T015 [S0007] Update troubleshooting with missing dependency, display backend, malformed event, timeout, stderr, non-zero exit, AppImage packaging, and clean-room audit recovery steps (`apex-infinite-cli/docs/troubleshooting.md`)

---

## Testing (5 tasks)

- [x] T016 [S0007] Write productization tests for settings presets, validation errors, plain fallback, reduced effects, font/scale bounds, and package import isolation (`apex-infinite-cli/tests/test_visual_wrapper_productization.py`)
- [x] T017 [S0007] Write productization tests for launcher validation, missing CLI handling, timeout mapping, stderr and return-code mapping, bridge state reset, duplicate start prevention, and malformed event recovery (`apex-infinite-cli/tests/test_visual_wrapper_productization.py`)
- [x] T018 [S0007] Run the full CLI pytest suite to confirm prompt, renderer, history, subprocess, event-stream, spike wrapper, and productization wrapper tests remain green (`cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`)
- [x] T019 [S0007] Run formatter, linter, compile, QML lint, and offscreen smoke checks for the productized wrapper (`cd apex-infinite-cli && ./.venv/bin/python -m black --check apex_infinite_visual tests/test_visual_wrapper_productization.py && ./.venv/bin/python -m pylint apex_infinite.py apex_infinite_events.py apex_infinite_ui.py apex_infinite_visual && ./.venv/bin/python -m py_compile apex_infinite_visual/__init__.py apex_infinite_visual/events.py apex_infinite_visual/launcher.py apex_infinite_visual/main.py apex_infinite_visual/settings.py && ./.venv/bin/pyside6-qmllint apex_infinite_visual/qml/Main.qml && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300`)
- [x] T020 [S0007] Verify ASCII/LF, clean whitespace, no copied reference material, no tracked `EXAMPLE/` files, unchanged base dependency boundary, and productized documentation links (`apex-infinite-cli/apex_infinite_visual/`, `apex-infinite-cli/docs/visual-wrapper-productization.md`, `git diff --check`)

---

## Completion Checklist

- [x] All tasks marked `[x]`
- [x] All tests and checks passing
- [x] All files ASCII-encoded with LF line endings
- [x] implementation-notes.md updated
- [x] Ready for `creview` to continue the implement -> creview -> validate sequence

---

## Next Steps

Run the `creview` workflow step.
