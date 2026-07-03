# Task Checklist

**Session ID**: `phase00-session06-linux-wrapper-spike`
**Total Tasks**: 20
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (4 tasks)

- [x] T001 [S0006] Verify analyzer state, Sessions 01 through 05 validation evidence, PySide6 availability, and Session 06 prerequisites before creating wrapper code (`.spec_system/specs/phase00-session05-docs-samples-and-runbooks/validation.md`, `apex-infinite-cli/requirements-wrapper.txt`)
- [x] T002 [S0006] Audit current event-stream and machine-output contracts for event names, payload safety, stdout guardrails, and wrapper consumption requirements (`apex-infinite-cli/apex_infinite_events.py`, `apex-infinite-cli/docs/event-stream.md`)
- [x] T003 [S0006] Resolve clean-room implementation boundaries by checking the visual wrapper boundary, Phase 00 PRD, `.gitignore`, and reference-material exclusions before using any visual concepts (`apex-infinite-cli/docs/visual-wrapper-boundary.md`, `.spec_system/PRD/phase_00/session_06_linux_wrapper_spike.md`)
- [x] T004 [S0006] Create the isolated optional wrapper package and QML directory without importing PySide6 from the base CLI runtime path (`apex-infinite-cli/apex_infinite_visual/`, `apex-infinite-cli/apex_infinite_visual/qml/`)

---

## Foundation (5 tasks)

- [x] T005 [S0006] [P] Create wrapper package metadata and exported public names for the optional prototype package (`apex-infinite-cli/apex_infinite_visual/__init__.py`)
- [x] T006 [S0006] [P] Implement the JSONL event parser and view-state adapter with schema-validated input and explicit error mapping (`apex-infinite-cli/apex_infinite_visual/events.py`)
- [x] T007 [S0006] [P] Implement the CLI subprocess command builder for `--event-stream - --machine-output` with timeout fields, stderr separation, and cleanup on scope exit for all acquired resources (`apex-infinite-cli/apex_infinite_visual/launcher.py`)
- [x] T008 [S0006] Implement the PySide6 entrypoint, lazy import guard, QML engine loading, and Python-to-QML bridge with missing-dependency and display-backend failure states (`apex-infinite-cli/apex_infinite_visual/main.py`)
- [x] T009 [S0006] Create the independent QML prototype shell with a read-only log viewport, status panels, theme selector, reduced-effects controls, and product-facing copy only (`apex-infinite-cli/apex_infinite_visual/qml/Main.qml`)

---

## Implementation (7 tasks)

- [x] T010 [S0006] Wire event-line ingestion from the launcher into the wrapper bridge with deterministic ordering, bounded log retention, and malformed-line recovery (`apex-infinite-cli/apex_infinite_visual/main.py`, `apex-infinite-cli/apex_infinite_visual/events.py`)
- [x] T011 [S0006] Implement wrapper start, stop, dry-run, max-iteration, project path, and optional start-command controls with duplicate-trigger prevention while in-flight and cleanup on scope exit (`apex-infinite-cli/apex_infinite_visual/main.py`, `apex-infinite-cli/apex_infinite_visual/launcher.py`)
- [x] T012 [S0006] Implement event-driven status updates for startup, iteration, manager decision, prompt dispatch, Codex execution, DB logging, completion, stop, timeout, and error states with explicit loading, empty, error, and offline states (`apex-infinite-cli/apex_infinite_visual/main.py`, `apex-infinite-cli/apex_infinite_visual/qml/Main.qml`)
- [x] T013 [S0006] Implement independent low-risk visual effect controls for glow, scanline, flicker, curvature, theme selection, and reduced-effects fallback with platform-appropriate accessibility labels, focus management, and input support (`apex-infinite-cli/apex_infinite_visual/qml/Main.qml`)
- [x] T014 [S0006] Document spike evidence, PySide6/QML dependency status, LGPLv3/commercial obligations, Nuitka/AppImage packaging risks, qmltermwidget placeholder status, PyQt exclusion, and pywebview plus xterm.js backup (`apex-infinite-cli/docs/visual-wrapper-spike.md`)
- [x] T015 [S0006] Update operator-facing docs with the wrapper prototype run path, optional dependency install, fallback behavior, and link to the spike decision record (`apex-infinite-cli/README_apex-infinite-cli.md`, `apex-infinite-cli/docs/operator-runbook.md`)
- [x] T016 [S0006] Update boundary and troubleshooting docs with confirmed prototype constraints, missing PySide6/display errors, malformed JSONL handling, subprocess failure handling, and no-copy audit expectations (`apex-infinite-cli/docs/visual-wrapper-boundary.md`, `apex-infinite-cli/docs/troubleshooting.md`)

---

## Testing (4 tasks)

- [x] T017 [S0006] Write focused wrapper spike tests for event parsing, malformed JSON, unsupported versions, launcher command construction, stdout guardrails, import-guard behavior, and fixture event flow (`apex-infinite-cli/tests/test_visual_wrapper_spike.py`)
- [x] T018 [S0006] Run the full CLI pytest suite to confirm prompt, renderer, history, subprocess, event-stream, and new wrapper tests remain green (`cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`)
- [x] T019 [S0006] Run an offscreen or display-backed wrapper smoke check against dry-run or fixture events, or record the exact PySide6/display blocker in the spike evidence (`cd apex-infinite-cli && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1`)
- [x] T020 [S0006] Verify ASCII/LF, no copied reference material, no tracked `EXAMPLE/` files, clean whitespace, and unchanged base dependency boundary (`apex-infinite-cli/apex_infinite_visual/`, `apex-infinite-cli/docs/visual-wrapper-spike.md`, `git diff --check`)

---

## Completion Checklist

- [x] All tasks marked `[x]`
- [x] All tests and checks passing
- [x] All files ASCII-encoded with LF line endings
- [x] implementation-notes.md updated
- [x] Ready for `implement` to start the implement -> creview -> validate sequence

---

## Next Steps

Run the `implement` workflow step.
