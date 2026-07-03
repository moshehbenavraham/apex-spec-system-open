# Task Checklist

**Session ID**: `phase00-session01-config-and-renderer-boundary`
**Total Tasks**: 20
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-02

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Progress Summary

| Category | Completed | Total |
|----------|-----------|-------|
| Setup | 2 | 2 |
| Foundation | 5 | 5 |
| Implementation | 8 | 8 |
| Testing | 5 | 5 |
| Overall | 20 | 20 |

---

## Setup (2 tasks)

- [x] T001 [S0001] Verify baseline prompt/routing tests and CLI import behavior (`apex-infinite-cli/tests/test_prompts.py`)
- [x] T002 [S0001] Map current operator-facing output call sites and raw data boundaries (`apex-infinite-cli/apex_infinite.py`)

---

## Foundation (5 tasks)

- [x] T003 [S0001] Create theme token, glyph, and UI setting models with built-in `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and `plain` definitions (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T004 [S0001] Implement `ui.themes` custom override validation with schema-validated input and explicit error mapping (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T005 [S0001] Implement UI setting resolution for CLI flags, environment constraints, config values, and defaults with deterministic precedence (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T006 [S0001] Implement injectable renderer helpers and lifecycle snapshot helpers with explicit plain, ASCII, compact, empty, error, and width-aware states (`apex-infinite-cli/apex_infinite_ui.py`)
- [x] T007 [S0001] Add default `ui` configuration keys and built-in values without storing secrets or display-only runtime state (`apex-infinite-cli/config.yaml`)

---

## Implementation (8 tasks)

- [x] T008 [S0001] Wire Click options for `--theme`, `--plain`, `--ascii`, and `--compact` with validation-compatible defaults (`apex-infinite-cli/apex_infinite.py`)
- [x] T009 [S0001] Instantiate resolved UI settings and renderer in `main()` and pass the renderer to display-owning helpers (`apex-infinite-cli/apex_infinite.py`)
- [x] T010 [S0001] Route startup banner, project selection, and interactive prompts through renderer helpers with product-facing copy only (`apex-infinite-cli/apex_infinite.py`)
- [x] T011 [S0001] Route `db_show_history()` through renderer helpers with empty, sparse legacy, long-row, plain, and ASCII-safe display handling (`apex-infinite-cli/apex_infinite.py`)
- [x] T012 [S0001] Route iteration banners, history-summary status, manager decisions, reasons, and prompt previews through renderer helpers (`apex-infinite-cli/apex_infinite.py`)
- [x] T013 [S0001] Route `execute_codex()` dry-run, start, verbose, truncated, non-zero exit, timeout, missing-binary, and generic-error output through renderer helpers while preserving returned raw output (`apex-infinite-cli/apex_infinite.py`)
- [x] T014 [S0001] Route LLM retry notices, interrupt pauses, help pauses, completion, and max-iteration notices through renderer helpers without hiding critical states in compact mode (`apex-infinite-cli/apex_infinite.py`)
- [x] T015 [S0001] Document UI config keys, CLI flags, precedence, constrained-output fallback, and history raw-data guarantees (`apex-infinite-cli/README_apex-infinite-cli.md`)

---

## Testing (5 tasks)

- [x] T016 [S0001] [P] Add resolver tests for defaults, config values, CLI overrides, `NO_COLOR`, `TERM=dumb`, non-terminal consoles, custom themes, and invalid values (`apex-infinite-cli/tests/test_ui_config.py`)
- [x] T017 [S0001] [P] Add Click option tests for the four new flags, invalid combinations, dry-run startup, and history-mode wiring (`apex-infinite-cli/tests/test_cli_options.py`)
- [x] T018 [S0001] [P] Add renderer and history safety tests proving semantic output at 80/100/120 columns and no ANSI, Rich markup, frame glyphs, or renderer labels in stored rows (`apex-infinite-cli/tests/test_renderer.py`)
- [x] T019 [S0001] Run CLI tests, formatter check, and linter check from the CLI directory (`cd apex-infinite-cli && pytest tests/ -v && black --check apex_infinite.py apex_infinite_ui.py tests/ && pylint apex_infinite.py apex_infinite_ui.py`)
- [x] T020 [S0001] Validate authored files are ASCII-only with Unix LF line endings (`.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md`)

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
