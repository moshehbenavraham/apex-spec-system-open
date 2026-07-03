# Task Checklist

**Session ID**: `phase00-session02-rich-operator-console`
**Total Tasks**: 21
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (3 tasks)

- [x] T001 [S0002] Verify Session 01 validation evidence and current renderer contracts before changing display behavior (`.spec_system/specs/phase00-session01-config-and-renderer-boundary/validation.md`)
- [x] T002 [S0002] Map current startup, iteration, manager, prompt, Codex, DB log, help, completion, interrupt, and safety-stop renderer call sites (`apex-infinite-cli/apex_infinite.py`)
- [x] T003 [S0002] Create operator-console test fixtures for recorded consoles, supported widths, and fallback modes (`apex-infinite-cli/tests/test_operator_console.py`)

---

## Foundation (5 tasks)

- [x] T004 [S0002] Refine independent `crt-green`, `crt-amber`, `ibm-dos`, and `plain` theme tokens and semantic state labels without copying reference constants (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T005 [S0002] Add explicit run or iteration snapshot data for provider, model, project, iteration, elapsed time, dry-run state, and current operation (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T006 [S0002] Implement status-strip and low-fidelity separator helpers with explicit plain, ASCII, compact, and constrained-output states (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T007 [S0002] Implement semantic render states for manager decisions, prompt previews, agent output, DB writes, LLM retries, JSON fallback, help, completion, interrupts, timeouts, and Codex failures (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T008 [S0002] Preserve raw-data boundaries around renderer helpers so display labels, ANSI escapes, Rich markup, separators, and theme tokens are never persisted (`apex-infinite-cli/apex_infinite_ui.py`)

---

## Implementation (8 tasks)

- [x] T009 [S0002] Redesign startup rendering as a compact boot/status panel with product-facing copy only (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T010 [S0002] Replace the current iteration block with a stable iteration frame and status strip that keeps loading, empty, error, and completion states explicit (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T011 [S0002] Wire provider, model, project, dry-run, elapsed-time, and operation context from `main()` and `infinite_loop()` into renderer snapshots (`apex-infinite-cli/apex_infinite.py`)
- [x] T012 [S0002] Add renderer-visible DB write confirmation after successful `db_log()` calls without changing SQLite schema, stored row values, or transaction behavior (`apex-infinite-cli/apex_infinite.py`)
- [x] T013 [S0002] Improve manager decision, prompt preview, and agent response panels with deterministic truncation and critical-state visibility at narrow widths (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T014 [S0002] Improve Codex command state rendering for dry-run, start, non-zero exit, timeout, missing binary, and generic error paths while preserving returned raw strings (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T015 [S0002] Ensure plain, ASCII, compact, `NO_COLOR`, `TERM=dumb`, and non-terminal console fallbacks stay readable and suppress low-effect separators where required (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T016 [S0002] Add minimal README notes for the richer operator console, theme presets, and current fallback guarantees without expanding into runbook or event-stream docs (`apex-infinite-cli/README_apex-infinite-cli.md`)

---

## Testing (5 tasks)

- [x] T017 [S0002] [P] Add operator-console tests for startup, iteration, status strips, DB write visibility, and critical states at 80, 100, and 120 columns (`apex-infinite-cli/tests/test_operator_console.py`)
- [x] T018 [S0002] [P] Add fallback tests for styled, plain, ASCII, compact, `NO_COLOR`, `TERM=dumb`, non-terminal output, and separator suppression (`apex-infinite-cli/tests/test_operator_console.py`)
- [x] T019 [S0002] [P] Extend renderer safety tests proving DB log rendering does not persist renderer labels, ANSI escapes, Rich markup, frame glyphs, separators, or theme tokens (`apex-infinite-cli/tests/test_renderer.py`)
- [x] T020 [S0002] [P] Extend CLI and UI config tests for operator-console context wiring, preset token expectations, and unchanged prompt/routing behavior (`apex-infinite-cli/tests/test_cli_options.py`)
- [x] T021 [S0002] Run CLI tests, formatter check, linter check, and ASCII/LF verification (`cd apex-infinite-cli && pytest tests/ -v && black --check apex_infinite.py apex_infinite_ui.py tests/ && pylint apex_infinite.py apex_infinite_ui.py`)

---

## Completion Checklist

- [x] All tasks marked `[x]`
- [x] All tests and checks passing
- [x] All files ASCII-encoded with LF line endings
- [x] implementation-notes.md updated
- [x] Ready for `creview` to start the creview -> validate sequence

---

## Next Steps

Run the `creview` workflow step.
