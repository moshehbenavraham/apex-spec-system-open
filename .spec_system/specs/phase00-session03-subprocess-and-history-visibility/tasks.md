# Task Checklist

**Session ID**: `phase00-session03-subprocess-and-history-visibility`
**Total Tasks**: 20
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (3 tasks)

- [x] T001 [S0003] Verify Session 01 and Session 02 validation evidence plus analyzer state before changing subprocess or history behavior (`.spec_system/specs/phase00-session02-rich-operator-console/validation.md`)
- [x] T002 [S0003] Map current `execute_codex()`, `db_show_history()`, `ApexRenderer.print_codex_command()`, and `ApexRenderer.print_history()` behavior and record compatibility notes (`apex-infinite-cli/apex_infinite.py`)
- [x] T003 [S0003] Create subprocess and history test fixtures using fake runners, monkeypatching, temporary DB paths, and recorded Rich consoles (`apex-infinite-cli/tests/test_subprocess_execution.py`)

---

## Foundation (5 tasks)

- [x] T004 [S0003] [P] Add characterization tests for dry-run, success, stderr-only success, non-zero exit, timeout, missing binary, generic exception, and verbose response behavior (`apex-infinite-cli/tests/test_subprocess_execution.py`)
- [x] T005 [S0003] [P] Add history characterization tests for empty, short, long, sparse legacy, styled, plain, ASCII, compact, and verbose rows at supported widths (`apex-infinite-cli/tests/test_history_rendering.py`)
- [x] T006 [S0003] Add a minimal process execution boundary or runner helper with raw stdout, stderr, return-code, timeout, and cleanup semantics (`apex-infinite-cli/apex_infinite.py`)
- [x] T007 [S0003] Add renderer-facing execution status facts for elapsed time, process state, timeout threshold, binary, project, and return code (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T008 [S0003] Add history row formatting helpers for compact summaries, verbose expansion, blank-safe legacy values, and truncation counts (`apex-infinite-cli/apex_infinite_ui.py`)

---

## Implementation (8 tasks)

- [x] T009 [S0003] Replace or wrap `subprocess.run()` with live-status-compatible execution while preserving stdout, stderr fallback, return code, and raw returned output (`apex-infinite-cli/apex_infinite.py`)
- [x] T010 [S0003] Implement timeout handling with explicit child-process cleanup on scope exit for all acquired resources (`apex-infinite-cli/apex_infinite.py`)
- [x] T011 [S0003] Render active Codex process state, elapsed time, timeout threshold, and completion/failure states through the existing renderer boundary (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T012 [S0003] Preserve dry-run, missing-binary, non-zero exit, timeout, generic exception, and `--verbose` response rendering behavior through the new execution path (`apex-infinite-cli/apex_infinite.py`)
- [x] T013 [S0003] Redesign styled history output as a compact ledger with command, reason, timestamp, status, project key, and truncated response summary (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T014 [S0003] Extend plain, ASCII, compact, and non-terminal history output with deterministic labels, blank-safe cells, verbose detail, and explicit truncation counts (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T015 [S0003] Wire `--history --verbose` to expanded history detail without adding `--history-verbose` and without starting the autonomous loop (`apex-infinite-cli/apex_infinite.py`)
- [x] T016 [S0003] Preserve SQLite schema and raw stored values so display labels, ANSI escapes, Rich markup, frame glyphs, and truncation text are never persisted (`apex-infinite-cli/apex_infinite.py`)

---

## Testing (4 tasks)

- [x] T017 [S0003] [P] Run and repair subprocess execution tests for success, stderr-only, non-zero, timeout, dry-run, missing binary, generic exception, cleanup, and verbose paths (`cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/test_subprocess_execution.py -q`)
- [x] T018 [S0003] [P] Run and repair history rendering tests for ledger layout, verbose expansion, empty/sparse rows, display fallbacks, supported widths, and raw DB safety (`cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/test_history_rendering.py tests/test_renderer.py -q`)
- [x] T019 [S0003] Run CLI, prompt, renderer, and UI config regression tests to confirm prompt routing, Click wiring, and fallback behavior remain compatible (`cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`)
- [x] T020 [S0003] Run formatter, linter, ASCII, and LF verification over changed authored files (`cd apex-infinite-cli && ./.venv/bin/python -m black --check apex_infinite.py apex_infinite_ui.py tests/ && ./.venv/bin/python -m pylint apex_infinite.py apex_infinite_ui.py`)

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
