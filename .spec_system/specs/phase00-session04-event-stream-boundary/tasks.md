# Task Checklist

**Session ID**: `phase00-session04-event-stream-boundary`
**Total Tasks**: 21
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (3 tasks)

- [x] T001 [S0004] Verify Sessions 01 through 03 validation evidence, analyzer state, and Session 04 stub prerequisites before editing event-stream code (`.spec_system/specs/phase00-session03-subprocess-and-history-visibility/validation.md`)
- [x] T002 [S0004] Map event emission points in `main()`, `infinite_loop()`, `execute_codex()`, `db_log()` call sites, `notify()`, and interrupt handling (`apex-infinite-cli/apex_infinite.py`)
- [x] T003 [S0004] Create event-stream test fixtures for temporary JSONL files, stdout capture, fake LLM decisions, fake Codex runners, fake emitters, and no real provider calls (`apex-infinite-cli/tests/test_event_stream.py`)

---

## Foundation (5 tasks)

- [x] T004 [S0004] [P] Add event API tests for valid JSONL file writes, one-object-per-line format, flush behavior, close cleanup on scope exit, and disabled no-op behavior (`apex-infinite-cli/tests/test_event_stream.py`)
- [x] T005 [S0004] [P] Add CLI guardrail tests for `--event-stream PATH`, rejected `--event-stream -` without `--machine-output`, rejected `--machine-output` without `--event-stream`, and loop wiring (`apex-infinite-cli/tests/test_cli_options.py`)
- [x] T006 [S0004] [P] Add subprocess event characterization tests for dry-run, start, completion, non-zero, timeout, missing-binary, and generic-error paths while preserving return text (`apex-infinite-cli/tests/test_subprocess_execution.py`)
- [x] T007 [S0004] Implement an importable event emitter module with event-name validation, JSON-serializable payload validation, line-buffered file/stdout sinks, flushing, and cleanup on scope exit (`apex-infinite-cli/apex_infinite_events.py`)
- [x] T008 [S0004] Implement raw-payload safety checks for ANSI escapes, Rich markup markers, frame glyphs, visual token leakage, and secret-looking values (`apex-infinite-cli/apex_infinite_events.py`)

---

## Implementation (8 tasks)

- [x] T009 [S0004] Add Click options for `--event-stream` and `--machine-output` with schema-validated flag combinations and explicit error mapping (`apex-infinite-cli/apex_infinite.py`)
- [x] T010 [S0004] Wire event emitter creation, context cleanup, startup/config/UI-resolution events, and event stream write-failure handling into CLI startup (`apex-infinite-cli/apex_infinite.py`)
- [x] T011 [S0004] Add a no-human-output renderer adapter or equivalent suppression hook so machine-output mode cannot print Rich or plain human text to stdout (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T012 [S0004] Emit iteration, history-summary, manager-decision, prompt-dispatch, help, completion, max-iteration, interrupt, and DB-log events with bounded raw payloads (`apex-infinite-cli/apex_infinite.py`)
- [x] T013 [S0004] Emit Codex subprocess dry-run, start, completion, non-zero, timeout, missing-binary, generic-error, and output-summary events without changing captured output semantics (`apex-infinite-cli/apex_infinite.py`)
- [x] T014 [S0004] Disable terminal bell and desktop notifications in `--machine-output` mode while preserving normal notification behavior otherwise (`apex-infinite-cli/apex_infinite.py`)
- [x] T015 [S0004] Ensure event-stream file output coexists with styled, plain, ASCII, compact, `NO_COLOR`, `TERM=dumb`, and non-terminal human rendering without stdout collision (`apex-infinite-cli/apex_infinite.py`)
- [x] T016 [S0004] Preserve prompt routing, manager normalization, SQLite schema, `cc_response`, DB row contents, dry-run output, timeout text, and subprocess error text through event wiring (`apex-infinite-cli/apex_infinite.py`)

---

## Documentation (2 tasks)

- [x] T017 [S0004] [P] Create the event stream contract with event names, payload principles, JSONL examples, `--machine-output` rules, wrapper guidance, and safety boundaries (`apex-infinite-cli/docs/event-stream.md`)
- [x] T018 [S0004] [P] Update README, operator runbook, prompt contract, and troubleshooting docs for `--event-stream`, `--machine-output`, stdout isolation, raw payload safety, and unchanged prompt routing (`apex-infinite-cli/README_apex-infinite-cli.md`, `apex-infinite-cli/docs/operator-runbook.md`, `apex-infinite-cli/docs/prompt-contract.md`, `apex-infinite-cli/docs/troubleshooting.md`)

---

## Testing (3 tasks)

- [x] T019 [S0004] Run focused event, CLI option, subprocess, renderer, and prompt regression tests for event order, payload safety, stdout isolation, and compatibility (`cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/test_event_stream.py tests/test_cli_options.py tests/test_subprocess_execution.py tests/test_renderer.py tests/test_prompts.py -q`)
- [x] T020 [S0004] Run the full CLI test suite and coverage-configured regression tests to confirm no existing UI, history, prompt, or subprocess behavior regressed (`cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`)
- [x] T021 [S0004] Run formatter, linter, whitespace, ASCII, and LF verification over changed authored files (`cd apex-infinite-cli && ./.venv/bin/python -m black --check apex_infinite.py apex_infinite_ui.py apex_infinite_events.py tests/ && ./.venv/bin/python -m pylint apex_infinite.py apex_infinite_ui.py apex_infinite_events.py`)

---

## Completion Checklist

- [x] All tasks marked `[x]`
- [x] All tests and checks passing
- [x] All files ASCII-encoded with LF line endings
- [x] implementation-notes.md updated
- [x] Ready for `implement` to start the implement -> creview -> validate sequence

---

## Next Steps

Session complete. Run the `plansession` workflow step to scope Session 05.
