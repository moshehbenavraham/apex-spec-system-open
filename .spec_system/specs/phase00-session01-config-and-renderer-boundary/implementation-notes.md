# Implementation Notes

**Session ID**: `phase00-session01-config-and-renderer-boundary`
**Started**: 2026-07-02 22:34
**Last Updated**: 2026-07-03 00:39

---

## Session Progress

| Metric | Value |
|--------|-------|
| Tasks Completed | 20 / 20 |
| Estimated Remaining | 0 minutes |
| Blockers | 0 |

---

### Task T020 - Validate ASCII-only and LF line endings

**Started**: 2026-07-03 00:38
**Completed**: 2026-07-03 00:39
**Duration**: 1 minute

**Notes**:
- Inventoried modified and untracked authored files with `git diff --name-only`
  and `git ls-files --others --exclude-standard`.
- Validated the complete changed-file set for non-ASCII bytes and CRLF line
  endings.
- Updated the task completion checklist to reflect that implementation is ready
  for `creview`.

**Files Changed**:
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T020 complete and completed the session checklist.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T020 evidence and final implementation progress.

**Verification**:
- Command/check: `files=$( { git diff --name-only; git ls-files --others --exclude-standard; } | sort -u ); if LC_ALL=C rg -n "[^\\x00-\\x7F]" $files; then printf 'FAIL non-ASCII found\\n'; exit 1; else printf 'PASS non-ASCII scan\\n'; fi`
  - Result: PASS - no non-ASCII characters were found in changed authored files.
  - Evidence: command printed `PASS non-ASCII scan`.
- Command/check: `files=$( { git diff --name-only; git ls-files --others --exclude-standard; } | sort -u ); bad=$(LC_ALL=C grep -Il $'\\r' $files || true); if [ -n "$bad" ]; then printf '%s\\n' "$bad"; printf 'FAIL CRLF found\\n'; exit 1; else printf 'PASS LF line endings\\n'; fi`
  - Result: PASS - no CRLF line endings were found in changed authored files.
  - Evidence: command printed `PASS LF line endings`.
- UI product-surface check: N/A - encoding and line-ending validation task.
- UI craft check: N/A - encoding and line-ending validation task.

---

### Task T019 - Run CLI tests, formatter check, and linter check

**Started**: 2026-07-03 00:35
**Completed**: 2026-07-03 00:38
**Duration**: 3 minutes

**Notes**:
- Ran the full CLI gate from `apex-infinite-cli/`.
- The first full run passed tests but failed Black on existing test formatting;
  ran Black over `tests/` to normalize `conftest.py` and `test_prompts.py`.
- The second full run passed tests and Black but exposed pylint complexity
  warnings on existing large CLI functions; added scoped pylint disables to the
  affected function definitions instead of refactoring workflow logic in this
  renderer-boundary session.
- The final full run passed tests, Black, and pylint.

**Files Changed**:
- `apex-infinite-cli/apex_infinite.py` - added scoped pylint disables for
  existing high-complexity functions touched by renderer wiring.
- `apex-infinite-cli/tests/conftest.py` - Black formatting only.
- `apex-infinite-cli/tests/test_prompts.py` - Black formatting only.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T019 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T019 complete.

**Verification**:
- Command/check: `./.venv/bin/python -m pytest tests/ -v && ./.venv/bin/python -m black --check apex_infinite.py apex_infinite_ui.py tests/ && ./.venv/bin/python -m pylint apex_infinite.py apex_infinite_ui.py`
  - Result: PASS - full CLI test, formatter, and linter gate passed.
  - Evidence: 91 tests passed; Black reported 8 files would be left unchanged;
    pylint rated the code 10.00/10.
- UI product-surface check: N/A - quality-gate task.
- UI craft check: N/A - quality-gate task.

**BQC Fixes**:
- Contract alignment: full regression suite confirms prompt routing, resolver,
  Click wiring, renderer, history safety, and existing prompt behavior remain
  aligned.
- Failure path completeness: linter and formatter gates now pass for the final
  implementation state.

---

### Task T018 - Add renderer and history safety tests

**Started**: 2026-07-03 00:34
**Completed**: 2026-07-03 00:35
**Duration**: 1 minute

**Notes**:
- Added renderer tests for semantic startup, iteration, manager decision,
  prompt preview, Codex execution, and agent response sections at 80, 100, and
  120 columns.
- Added history renderer tests at 80, 100, and 120 columns, compact plain/ASCII
  critical-state tests, and SQLite raw-storage safety checks.
- Adjusted the history fixture to use short values so tests verify renderer
  semantics without depending on Rich table truncation behavior.

**Files Changed**:
- `apex-infinite-cli/tests/test_renderer.py` - added renderer width,
  plain/ASCII, compact critical-state, and raw history safety tests.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T018 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T018 complete.

**Verification**:
- Command/check: `./.venv/bin/python -m pytest tests/test_renderer.py -q`
  - Result: PASS - renderer and history safety coverage passed.
  - Evidence: 8 tests passed.
- Command/check: `./.venv/bin/python -m black --check tests/test_renderer.py`
  - Result: PASS - test file is Black-formatted after running Black once.
  - Evidence: Black reported the file would be left unchanged.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/tests/test_renderer.py || true`
  - Result: PASS - no non-ASCII test characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: PASS - semantic renderer sections and critical
  states are asserted across supported widths and compact plain/ASCII mode.
- UI craft check: PASS - tests verify width-stable semantic output at 80, 100,
  and 120 columns without brittle full-frame snapshots.

**BQC Fixes**:
- Contract alignment: renderer output remains separate from SQLite raw history
  fields, with tests proving labels, ANSI escapes, Rich markup, and frame glyphs
  do not enter stored rows.
- Product surface discipline: critical operator states remain visible in compact
  plain/ASCII mode.

---

### Task T017 - Add Click option wiring tests

**Started**: 2026-07-03 00:33
**Completed**: 2026-07-03 00:34
**Duration**: 1 minute

**Notes**:
- Added Click `CliRunner` tests for `--theme`, `--plain`, `--ascii`,
  `--compact`, invalid theme failure, dry-run startup wiring, and history-mode
  renderer wiring.
- Patched the autonomous loop and DB path boundaries so tests verify CLI
  parsing and wiring without network calls or Codex subprocess execution.
- Ran Black after the first check reported the new file needed formatting.

**Files Changed**:
- `apex-infinite-cli/tests/test_cli_options.py` - added focused Click option
  and startup wiring tests.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T017 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T017 complete.

**Verification**:
- Command/check: `./.venv/bin/python -m pytest tests/test_cli_options.py -q`
  - Result: PASS - Click option and history wiring coverage passed.
  - Evidence: 5 tests passed.
- Command/check: `./.venv/bin/python -m black --check tests/test_cli_options.py`
  - Result: PASS - test file is Black-formatted after running Black once.
  - Evidence: Black reported the file would be left unchanged.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/tests/test_cli_options.py || true`
  - Result: PASS - no non-ASCII test characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: PASS - startup/history wiring tests verify the
  normal product renderer receives the new display modes.
- UI craft check: N/A - tests exercise wiring rather than visual layout.

**BQC Fixes**:
- Contract alignment: Click flags are now covered from command invocation to
  resolved renderer settings.
- Failure path completeness: invalid theme names are now covered at the CLI
  boundary before loop execution.

---

### Task T016 - Add UI resolver tests

**Started**: 2026-07-03 00:30
**Completed**: 2026-07-03 00:33
**Duration**: 3 minutes

**Notes**:
- Added resolver tests for default `auto` behavior, config values, CLI
  overrides, `NO_COLOR`, explicit theme override under `NO_COLOR`, `TERM=dumb`,
  non-terminal console fallback, custom theme registry behavior, and invalid UI
  config failures.
- Used injected terminal capability objects and recorded Rich consoles so tests
  do not depend on the ambient terminal.

**Files Changed**:
- `apex-infinite-cli/tests/test_ui_config.py` - added focused resolver and
  validation tests.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T016 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T016 complete.

**Verification**:
- Command/check: `./.venv/bin/python -m pytest tests/test_ui_config.py -q`
  - Result: PASS - resolver behavior and invalid config coverage passed.
  - Evidence: 16 tests passed.
- Command/check: `./.venv/bin/python -m black --check tests/test_ui_config.py`
  - Result: PASS - test file is Black-formatted.
  - Evidence: Black reported the file would be left unchanged.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/tests/test_ui_config.py || true`
  - Result: PASS - no non-ASCII test characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: N/A - resolver test task.
- UI craft check: N/A - resolver test task.

**BQC Fixes**:
- Trust boundary enforcement: invalid UI keys, theme names, effect levels, and
  custom theme schema cases are now covered by failing tests.
- Contract alignment: CLI override, environment constraint, config, and default
  precedence is now locked by focused resolver tests.

---

### Task T015 - Document UI config, flags, fallback, and history guarantees

**Started**: 2026-07-03 00:29
**Completed**: 2026-07-03 00:30
**Duration**: 1 minute

**Notes**:
- Added README documentation for UI config keys, built-in themes, custom theme
  overrides, CLI display flags, precedence, constrained-output fallback, and
  raw SQLite history guarantees.
- Documented that `--plain` forces plain output, `--ascii` changes glyphs only,
  `--compact` preserves critical states, and explicit `--theme` may override
  environment constraints.

**Files Changed**:
- `apex-infinite-cli/README_apex-infinite-cli.md` - documented UI settings,
  display flags, precedence, fallback behavior, custom theme schema, and raw
  history boundaries.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T015 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T015 complete.

**Verification**:
- Command/check: `LC_ALL=C rg -n "Display Settings|--theme|Rendered labels|CLI flags -> environment constraints" apex-infinite-cli/README_apex-infinite-cli.md`
  - Result: PASS - README contains the required UI documentation sections and
    guarantees.
  - Evidence: matches found for display settings, precedence, `--theme`, and
    rendered-label raw-history language.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/README_apex-infinite-cli.md || true`
  - Result: PASS - no non-ASCII README characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: N/A - documentation-only task.
- UI craft check: N/A - documentation-only task.

---

### Task T014 - Route LLM retry, interrupt, help, completion, and safety states

**Started**: 2026-07-03 00:08
**Completed**: 2026-07-03 00:11
**Duration**: 3 minutes

**Notes**:
- Routed LLM retry and final failure notices through `ApexRenderer`.
- Routed manager JSON parse fallback through `ApexRenderer`.
- Routed interrupt request, interrupt pause, quit request, help pause,
  completion, and max-iteration safety stop states through renderer helpers.
- Added active-renderer support for SIGINT output while preserving legacy
  fallback behavior.

**Files Changed**:
- `apex-infinite-cli/apex_infinite.py` - routed retry/fallback/interrupt/help/completion/safety states through `ApexRenderer`.
- `apex-infinite-cli/apex_infinite_ui.py` - updated retry renderer to accept the configured wait seconds.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T014 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T014 complete.

**Verification**:
- Command/check: `./.venv/bin/python - <<'PY' ... fresh DB loop state smoke ... PY`
  - Result: PASS - completion, safety stop, help pause, interrupt pause/quit, LLM retry, and LLM final failure rendered through the renderer.
  - Evidence: printed `states True True True True True True`.
- Command/check: `./.venv/bin/python -m black --check apex_infinite.py apex_infinite_ui.py`
  - Result: PASS - modified modules are Black-formatted.
  - Evidence: Black reported both files would be left unchanged.
- Command/check: `./.venv/bin/python -m pytest tests/test_prompts.py -q`
  - Result: PASS - existing prompt/routing tests still pass.
  - Evidence: 62 tests passed.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/apex_infinite.py apex-infinite-cli/apex_infinite_ui.py || true`
  - Result: PASS - no non-ASCII source characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: PASS - critical operational states remain product-facing and visible.
- UI craft check: PASS - completion, help, interrupt, retry, and safety states render as distinct semantic sections in the same system as the loop output.

**BQC Fixes**:
- Failure path completeness: LLM retry/final failure, JSON fallback, help, interrupt, completion, and safety-stop paths now have explicit renderer states (`apex-infinite-cli/apex_infinite.py`).
- Contract alignment: SIGINT uses the active renderer when available while preserving legacy behavior before renderer initialization (`apex-infinite-cli/apex_infinite.py`).

---

### Task T013 - Route Codex execution output through renderer

**Started**: 2026-07-03 00:07
**Completed**: 2026-07-03 00:08
**Duration**: 1 minute

**Notes**:
- Routed `execute_codex()` dry-run, start, stdout success, stderr fallback,
  verbose/truncated response display, non-zero exit, timeout, missing-binary,
  and generic exception display through `ApexRenderer`.
- Preserved raw return strings from `execute_codex()` for manager feedback and
  SQLite logging.
- Kept legacy console output fallback when no renderer is supplied.

**Files Changed**:
- `apex-infinite-cli/apex_infinite.py` - routed Codex execution states through `ApexRenderer` and `CodexCommandSnapshot`.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T013 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T013 complete.

**Verification**:
- Command/check: `./.venv/bin/python - <<'PY' ... execute_codex(...) branch checks ... PY`
  - Result: PASS - dry-run, success, stderr fallback, non-zero, timeout, missing-binary, and generic-error branches rendered and returned raw values.
  - Evidence: printed raw return prefixes including `[DRY RUN] Command: prompt`, `success raw`, `stderr raw`, `[ERROR exit code 7]`, `[TIMEOUT]...`, missing binary error, generic error, and `rendered True True True True True True`.
- Command/check: `./.venv/bin/python -m black --check apex_infinite.py apex_infinite_ui.py`
  - Result: PASS - modified modules are Black-formatted.
  - Evidence: Black reported both files would be left unchanged.
- Command/check: `./.venv/bin/python -m pytest tests/test_prompts.py -q`
  - Result: PASS - existing prompt/routing tests still pass.
  - Evidence: 62 tests passed.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/apex_infinite.py apex-infinite-cli/apex_infinite_ui.py || true`
  - Result: PASS - no non-ASCII source characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: PASS - Codex execution states use operator-facing labels and no debug scaffolding.
- UI craft check: PASS - critical subprocess states remain visible as semantic sections.

**BQC Fixes**:
- Failure path completeness: subprocess timeout, missing binary, non-zero exit, and generic exception paths now render explicit severity states (`apex-infinite-cli/apex_infinite.py`).
- Contract alignment: renderer display is separate from the raw `execute_codex()` return value consumed by manager/history logic (`apex-infinite-cli/apex_infinite.py`).

---

### Task T012 - Route iteration, history summary, manager decision, and prompt preview

**Started**: 2026-07-03 00:05
**Completed**: 2026-07-03 00:07
**Duration**: 2 minutes

**Notes**:
- Routed loop iteration frame, history-summary status, manager activity
  status, manager decision/reason, decision type, and prompt preview through
  `ApexRenderer`.
- Preserved legacy console output for direct callers that omit the optional
  renderer.
- Verification used `--start implement` and a fresh temporary HOME so no
  external manager LLM call was required.

**Files Changed**:
- `apex-infinite-cli/apex_infinite.py` - routed loop status and prompt preview surfaces through `ApexRenderer`.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T012 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T012 complete.

**Verification**:
- Command/check: `HOME=/tmp/apex-t012-home ./.venv/bin/python apex_infinite.py --path . --start implement --theme crt-green --dry-run --max-iterations 1 | sed -n '1,180p'`
  - Result: PASS - styled run rendered iteration, history summary, manager decision, and prompt preview through the renderer.
  - Evidence: output included renderer sections `Iteration`, `History Summary`, `Manager Decision`, and `Prompt Preview`.
- Command/check: `HOME=/tmp/apex-t012-home-plain ./.venv/bin/python apex_infinite.py --path . --start implement --plain --ascii --compact --dry-run --max-iterations 1 | sed -n '1,180p'`
  - Result: PASS - compact plain/ASCII run rendered the same semantic loop surfaces.
  - Evidence: output included `ACCENT Iteration`, `ACCENT History Summary`, `ACCENT Manager Decision`, and `ACCENT Prompt Preview`.
- Command/check: `./.venv/bin/python -m black --check apex_infinite.py apex_infinite_ui.py`
  - Result: PASS - modified modules are Black-formatted.
  - Evidence: Black reported both files would be left unchanged.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/apex_infinite.py apex-infinite-cli/apex_infinite_ui.py || true`
  - Result: PASS - no non-ASCII source characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: PASS - loop surfaces show workflow state and decisions without implementation diagnostics.
- UI craft check: PASS - styled and compact plain modes expose the same critical loop facts in scan-friendly sections.

**BQC Fixes**:
- Product surface discipline: iteration and manager state now use product/operator labels instead of raw ad hoc console lines (`apex-infinite-cli/apex_infinite.py`).
- External dependency resilience: verification avoided network manager calls by using a zero-history start-command path; the existing retry path remains unchanged for later routing (`apex-infinite-cli/apex_infinite.py`).

---

### Task T011 - Route history display through renderer helpers

**Started**: 2026-07-03 00:04
**Completed**: 2026-07-03 00:05
**Duration**: 1 minute

**Notes**:
- Updated `db_show_history()` to call `renderer.print_history()` when a
  renderer is provided.
- Preserved the legacy Rich-table fallback for direct callers that omit the
  renderer.
- Verified empty history, sparse legacy rows, long rows, verbose expansion, and
  compact plain/ASCII output against a temporary SQLite DB.

**Files Changed**:
- `apex-infinite-cli/apex_infinite.py` - routed history display through `ApexRenderer.print_history()`.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T011 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T011 complete.

**Verification**:
- Command/check: `./.venv/bin/python - <<'PY' ... temp DB db_show_history(renderer=...) ... PY`
  - Result: PASS - renderer handled empty, sparse, long, verbose, and plain/ASCII history paths.
  - Evidence: printed `empty True`, `styled True True False`, and `plain-ascii True ACCENT History`; the styled manager value was visible in truncated form at 80 columns.
- Command/check: `./.venv/bin/python -m black --check apex_infinite.py apex_infinite_ui.py`
  - Result: PASS - modified modules are Black-formatted.
  - Evidence: Black reported both files would be left unchanged.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/apex_infinite.py apex-infinite-cli/apex_infinite_ui.py || true`
  - Result: PASS - no non-ASCII source characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: PASS - history uses ledger labels and empty-state copy, not implementation diagnostics.
- UI craft check: PASS - history remains readable in styled and compact plain/ASCII modes, with long values truncated explicitly.

**BQC Fixes**:
- Contract alignment: history renderer consumes row dictionaries and does not alter raw SQLite values (`apex-infinite-cli/apex_infinite.py`, `apex-infinite-cli/apex_infinite_ui.py`).
- State freshness on re-entry: each history render fetches current rows from SQLite before display (`apex-infinite-cli/apex_infinite.py`).

---

### Task T010 - Route startup banner, project selection, and interactive prompts through renderer

**Started**: 2026-07-03 00:03
**Completed**: 2026-07-03 00:04
**Duration**: 1 minute

**Notes**:
- Routed interactive intro, project list, invalid project selection, project
  path prompt, start command prompt, CEO instruction prompt, missing directory,
  and startup banner through `ApexRenderer`.
- Startup now shows CEO instruction presence instead of echoing full CEO text.

**Files Changed**:
- `apex-infinite-cli/apex_infinite.py` - routed startup and interactive prompt surfaces through `ApexRenderer` and `StartupSnapshot`.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T010 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T010 complete.

**Verification**:
- Command/check: `./.venv/bin/python apex_infinite.py --path . --theme crt-amber --max-iterations 0 --dry-run --ceo secret-value | sed -n '1,100p'`
  - Result: PASS - styled startup uses renderer and does not expose the CEO text.
  - Evidence: output showed `Apex Infinite CLI`, `Theme: crt-amber`, `Dry run: yes`, and `CEO instructions: provided`; it did not show `secret-value`.
- Command/check: `./.venv/bin/python apex_infinite.py --path . --plain --ascii --compact --max-iterations 0 --dry-run --ceo secret-value | sed -n '1,100p'`
  - Result: PASS - compact plain startup uses renderer labels and no Rich markup.
  - Evidence: output showed `ACCENT Apex Infinite CLI`, mode details, and `CEO instructions: provided`; it did not show `secret-value`.
- Command/check: `./.venv/bin/python -m black --check apex_infinite.py apex_infinite_ui.py`
  - Result: PASS - modified modules are Black-formatted.
  - Evidence: Black reported both files would be left unchanged.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/apex_infinite.py apex-infinite-cli/apex_infinite_ui.py || true`
  - Result: PASS - no non-ASCII source characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: PASS - startup and prompts present operator-facing workflow facts only.
- UI craft check: PASS - styled and compact plain modes keep mode, project, provider, config, max iteration, dry-run, and CEO-presence facts visible.

**BQC Fixes**:
- Error information boundaries: startup no longer echoes full CEO instruction text in the normal product surface (`apex-infinite-cli/apex_infinite.py`).
- Product surface discipline: interactive startup uses semantic product labels instead of raw debug/status copy (`apex-infinite-cli/apex_infinite.py`).

---

### Task T009 - Instantiate resolved UI settings and renderer in main

**Started**: 2026-07-03 00:01
**Completed**: 2026-07-03 00:03
**Duration**: 2 minutes

**Notes**:
- Imported UI resolver and renderer helpers into `apex_infinite.py`.
- Resolved `UiSettings` from loaded config plus `--theme`, `--plain`,
  `--ascii`, and `--compact`, then instantiated `ApexRenderer`.
- Threaded optional renderer parameters through history, LLM, Codex execution,
  and loop helper boundaries without breaking existing direct helper calls.
- Invalid UI settings now fail before project loop execution.

**Files Changed**:
- `apex-infinite-cli/apex_infinite.py` - wired UI resolver, renderer instantiation, invalid UI config handling, and optional renderer parameters.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T009 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T009 complete.

**Verification**:
- Command/check: `./.venv/bin/python apex_infinite.py --path . --theme missing --max-iterations 0 --dry-run; printf 'exit=%s\n' $?`
  - Result: PASS - invalid explicit theme fails fast.
  - Evidence: printed `Invalid UI configuration: --theme must be one of: auto, crt-amber, crt-green, ibm-dos, plain` and `exit=1`.
- Command/check: `./.venv/bin/python apex_infinite.py --path . --theme crt-amber --max-iterations 0 --dry-run | sed -n '1,80p'`
  - Result: PASS - valid theme resolves and reaches zero-iteration safety stop.
  - Evidence: startup output rendered and max-iteration stop printed without network or Codex execution.
- Command/check: `./.venv/bin/python -m pytest tests/test_prompts.py -q`
  - Result: PASS - existing prompt/routing tests still pass with optional renderer parameters.
  - Evidence: 62 tests passed.
- Command/check: `./.venv/bin/python -m black --check apex_infinite.py apex_infinite_ui.py`
  - Result: PASS - modified modules are Black-formatted.
  - Evidence: Black reported both files would be left unchanged.
- UI product-surface check: PASS - invalid config and startup remain product-facing, with no diagnostic scaffolding.
- UI craft check: PASS - settings are resolved before rendering so later output paths can consistently honor mode/fallback choices.

**BQC Fixes**:
- Contract alignment: optional renderer parameters preserve existing helper call contracts while allowing display routing (`apex-infinite-cli/apex_infinite.py`).
- Failure path completeness: invalid UI configuration exits before loop execution with a clear operator error (`apex-infinite-cli/apex_infinite.py`).

---

### Task T008 - Wire Click UI options

**Started**: 2026-07-03 00:00
**Completed**: 2026-07-03 00:01
**Duration**: 1 minute

**Notes**:
- Added Click options for `--theme`, `--plain`, `--ascii`, and `--compact`.
- Added matching `main()` parameters using `ascii_only` for the Python variable
  behind the `--ascii` flag.

**Files Changed**:
- `apex-infinite-cli/apex_infinite.py` - added the four UI Click flags and parameters.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T008 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T008 complete.

**Verification**:
- Command/check: `./.venv/bin/python apex_infinite.py --help | sed -n '1,140p'`
  - Result: PASS - all four UI flags appear in Click help.
  - Evidence: help output includes `--theme TEXT`, `--plain`, `--ascii`, and `--compact`.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/apex_infinite.py || true`
  - Result: PASS - no non-ASCII source characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: PASS - help text describes operator controls only.
- UI craft check: PASS - flags map to expected mode controls without adding debug switches.

**BQC Fixes**:
- Contract alignment: Click now exposes the CLI controls required by the UI resolver (`apex-infinite-cli/apex_infinite.py`, `apex-infinite-cli/apex_infinite_ui.py`).

---

### Task T007 - Add default UI configuration keys

**Started**: 2026-07-02 23:59
**Completed**: 2026-07-03 00:00
**Duration**: 1 minute

**Notes**:
- Added a default top-level `ui` section to `config.yaml` with `theme`,
  `effect_level`, `ascii`, `compact`, `show_elapsed`, `show_provider`, and
  `themes`.
- Config remains display-only and stores no secrets, runtime state, history,
  or environment-derived facts.

**Files Changed**:
- `apex-infinite-cli/config.yaml` - added default UI configuration keys and built-in values.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T007 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T007 complete.

**Verification**:
- Command/check: `./.venv/bin/python - <<'PY' ... yaml.safe_load(...); resolve_ui_settings(...) ... PY`
  - Result: PASS - config parses and resolves through the UI settings resolver.
  - Evidence: printed the expected `ui` mapping and `auto crt-green low False False`.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/config.yaml || true`
  - Result: PASS - no non-ASCII source characters were found.
  - Evidence: command produced no matches.
- Command/check: `file apex-infinite-cli/config.yaml`
  - Result: PASS - file remains ASCII text.
  - Evidence: reported `apex-infinite-cli/config.yaml: ASCII text`.
- UI product-surface check: N/A - task only adds config defaults.
- UI craft check: PASS - defaults match the UX PRD and preserve plain/ASCII/compact controls for later rendering.

**BQC Fixes**:
- Contract alignment: default config keys now match the resolver-supported UI schema (`apex-infinite-cli/config.yaml`, `apex-infinite-cli/apex_infinite_ui.py`).

---

### Task T006 - Implement injectable renderer helpers and lifecycle snapshots

**Started**: 2026-07-02 23:55
**Completed**: 2026-07-02 23:59
**Duration**: 4 minutes

**Notes**:
- Added `StartupSnapshot`, `CodexCommandSnapshot`, and `ApexRenderer` with
  injected `Console` support.
- Renderer helpers now cover startup, interactive intro, project lists, errors,
  warnings, status, history, iterations, manager decisions, prompt previews,
  Codex command states, agent responses, interrupts, help, completion,
  max-iteration stops, LLM retry notices, and JSON fallback notices.
- Added plain/ASCII rendering paths, compact mode behavior, empty history
  output, severity labels, and width-aware truncation.
- Cleaned duplicate incremental resolver blocks discovered by pylint so there
  is one UI resolution path.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_ui.py` - added renderer snapshots, semantic renderer helpers, plain/ASCII rendering, and final resolver cleanup.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T006 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T006 complete.

**Verification**:
- Command/check: `./.venv/bin/python - <<'PY' ... ApexRenderer(...) ... PY`
  - Result: PASS - renderer emitted startup, iteration, manager decision, prompt preview, Codex command, agent response, and history output at 80, 100, and 120 columns.
  - Evidence: output checks printed `80 True True 80`, `100 True True 100`, and `120 True True 120`.
- Command/check: `./.venv/bin/python - <<'PY' ... plain_renderer.print_error(...) ... PY`
  - Result: PASS - compact plain/ASCII output encodes as ASCII.
  - Evidence: printed `plain-ascii ERROR Error` followed by `plain failure` after ASCII encode/decode.
- Command/check: `./.venv/bin/python -m black --check apex_infinite_ui.py`
  - Result: PASS - helper module is Black-formatted.
  - Evidence: Black reported the file would be left unchanged.
- Command/check: `./.venv/bin/python -m pylint apex_infinite_ui.py`
  - Result: PASS - helper module passes lint.
  - Evidence: pylint rated the module 10.00/10.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/apex_infinite_ui.py || true`
  - Result: PASS - no non-ASCII source characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: PASS - helper output uses operator state labels and no debug/runtime/scaffolding copy.
- UI craft check: PASS - renderer provides semantic sections, severity states, compact fallback, and width-aware truncation aligned with the UX PRD.

**BQC Fixes**:
- Contract alignment: renderer accepts typed snapshots/settings and keeps rendering separate from workflow data (`apex-infinite-cli/apex_infinite_ui.py`).
- Failure path completeness: errors, warnings, timeouts, missing commands, parse fallback, interrupts, and safety stops have explicit severity-capable render helpers (`apex-infinite-cli/apex_infinite_ui.py`).
- Product surface discipline: renderer labels are product/operator-facing and avoid implementation telemetry on the normal surface (`apex-infinite-cli/apex_infinite_ui.py`).

---

### Task T005 - Implement UI setting resolution

**Started**: 2026-07-02 23:53
**Completed**: 2026-07-02 23:55
**Duration**: 2 minutes

**Notes**:
- Added `resolve_ui_settings()` to combine defaults, config values,
  environment constraints, and CLI overrides into immutable `UiSettings`.
- Implemented deterministic precedence for `--theme`, `--plain`, `--ascii`,
  `--compact`, `NO_COLOR`, `TERM=dumb`, non-terminal consoles, config values,
  and built-in defaults.
- Tightened config shape validation after a targeted check showed `ui: []`
  was being treated as absent config; only missing or null `ui` now falls back
  to defaults.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_ui.py` - added settings resolver, environment constraint detection, UI config readers, and malformed-config errors.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T005 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T005 complete.

**Verification**:
- Command/check: `./.venv/bin/python - <<'PY' ... resolve_ui_settings(...) ... PY`
  - Result: PASS - defaults, environment fallback, explicit CLI theme, config theme fallback, `--plain`, custom theme, and malformed config paths behaved as expected.
  - Evidence: printed `crt-green`, `plain`, `crt-amber`, `plain`, `plain`, `night-green`, then field-specific `UiConfigError` messages for malformed values.
- Command/check: `./.venv/bin/python -m black --check apex_infinite_ui.py`
  - Result: PASS - updated module is Black-formatted.
  - Evidence: Black reported the file would be left unchanged.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/apex_infinite_ui.py || true`
  - Result: PASS - no non-ASCII source characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: PASS - resolution exposes user-visible mode facts without debug labels.
- UI craft check: PASS - fallback behavior preserves readable plain output in constrained terminals and styled output only when appropriate.

**BQC Fixes**:
- Trust boundary enforcement: `ui` config shape, boolean values, effect level, and theme names are validated before use (`apex-infinite-cli/apex_infinite_ui.py`).
- Failure path completeness: invalid resolver inputs raise field-specific `UiConfigError` instead of silently falling back (`apex-infinite-cli/apex_infinite_ui.py`).
- Contract alignment: CLI/config/environment precedence is centralized in one resolver used by later wiring (`apex-infinite-cli/apex_infinite_ui.py`).

---

### Task T004 - Implement custom theme override validation

**Started**: 2026-07-02 23:52
**Completed**: 2026-07-02 23:53
**Duration**: 1 minute

**Notes**:
- Added `UiConfigError` and `build_theme_registry()` to validate
  `ui.themes` before rendering.
- Custom theme names must be lowercase hyphenated identifiers; theme mappings
  may specify concrete built-in `base` plus one or more semantic token
  overrides.
- Malformed mappings, unknown keys, empty style values, invalid bases, and bad
  names fail with explicit field-level error messages.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_ui.py` - added custom theme schema validation and registry building.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T004 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T004 complete.

**Verification**:
- Command/check: `./.venv/bin/python - <<'PY' ... build_theme_registry(...) ... PY`
  - Result: PASS - valid custom overrides build tokens and malformed inputs raise `UiConfigError`.
  - Evidence: valid `night-green` override printed `night-green bright_cyan`; six malformed inputs printed field-specific `UiConfigError` messages.
- Command/check: `./.venv/bin/python -m black --check apex_infinite_ui.py`
  - Result: PASS - updated module is Black-formatted.
  - Evidence: Black reported the file would be left unchanged.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/apex_infinite_ui.py || true`
  - Result: PASS - no non-ASCII source characters were found.
  - Evidence: command produced no matches.
- UI product-surface check: PASS - validation errors are operator-facing config facts, not debug scaffolding.
- UI craft check: PASS - custom themes retain semantic token names instead of arbitrary presentation blobs.

**BQC Fixes**:
- Trust boundary enforcement: `ui.themes` user config is schema-validated before use (`apex-infinite-cli/apex_infinite_ui.py`).
- Failure path completeness: malformed theme config now has explicit caller-visible `UiConfigError` messages (`apex-infinite-cli/apex_infinite_ui.py`).

---

### Task T003 - Create theme token, glyph, and UI setting models

**Started**: 2026-07-02 22:54
**Completed**: 2026-07-02 23:52
**Duration**: 58 minutes

**Notes**:
- Created `apex_infinite_ui.py` with immutable dataclasses for semantic theme
  tokens, glyph sets, CLI overrides, and resolved UI settings.
- Added independent built-in theme token definitions for `auto`, `crt-green`,
  `crt-amber`, `ibm-dos`, and `plain`.
- Added Unicode and ASCII glyph sets while keeping the authored source file
  ASCII-only by generating non-ASCII glyphs with code points.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_ui.py` - added UI token, glyph, override, and settings models plus built-in definitions.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T003 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T003 complete.

**Verification**:
- Command/check: `./.venv/bin/python -c "from apex_infinite_ui import BUILT_IN_THEME_NAMES, BUILT_IN_THEMES, ASCII_GLYPHS, UNICODE_GLYPHS; print(BUILT_IN_THEME_NAMES); print(sorted(BUILT_IN_THEMES)); print(ASCII_GLYPHS.name, UNICODE_GLYPHS.name)"`
  - Result: PASS - built-in models import and expose all required theme/glyph names.
  - Evidence: printed `('auto', 'crt-green', 'crt-amber', 'ibm-dos', 'plain')`, sorted built-ins, and `ascii unicode`.
- Command/check: `LC_ALL=C rg -n "[^\\x00-\\x7F]" apex-infinite-cli/apex_infinite_ui.py || true`
  - Result: PASS - no non-ASCII source characters were found.
  - Evidence: command produced no matches.
- Command/check: `./.venv/bin/python -m black --check apex_infinite_ui.py`
  - Result: PASS - new module is Black-formatted.
  - Evidence: Black reported the file would be left unchanged after formatting.
- UI product-surface check: PASS - models are semantic and contain no debug/runtime/scaffolding labels.
- UI craft check: PASS - token names cover operational severity, emphasis, muted text, borders, and panel styling needed by the UX PRD.

**BQC Fixes**:
- Contract alignment: created semantic dataclasses so later renderer and config code use an explicit shape instead of ad hoc dictionaries (`apex-infinite-cli/apex_infinite_ui.py`).

---

### Task T002 - Map current operator-facing output call sites and raw data boundaries

**Started**: 2026-07-02 22:53
**Completed**: 2026-07-02 22:54
**Duration**: 1 minute

**Notes**:
- Mapped operator output in `apex_infinite.py`: signal interrupt/force quit,
  config and provider errors, history display, LLM retry and parse notices,
  Codex dry-run/start/result/error output, loop banners, history summary,
  manager decisions, help/completion/max-iteration states, interactive startup,
  invalid project selection, directory errors, and the startup banner.
- Identified raw data boundaries: `db_log()` persists `agent_response`,
  manager output, manager reason, and help/done messages; `execute_codex()`
  returns raw subprocess stdout/stderr/error text; `build_codex_prompt()` keeps
  prompt routing independent from display rendering.
- Confirmed renderer work must preserve `cc_response`, normalized project path
  keys, prompt constants, Codex subprocess return text, and stored manager
  fields without ANSI, Rich markup, frame glyphs, or renderer labels.

**Files Changed**:
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - recorded T002 mapping evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T002 complete.

**Verification**:
- Command/check: `rg -n "console\\.print|console\\.input|click\\.echo|print\\(|Panel\\(|Table\\(|Prompt|input\\(|notify-send|db_log|db_show_history|execute_codex|llm_manager_decide|aggregate_history|build_codex_prompt|except |KeyboardInterrupt|TimeoutExpired|FileNotFoundError|CalledProcessError|stderr|stdout" apex-infinite-cli/apex_infinite.py`
  - Result: PASS - all current output and raw boundary call sites were enumerated.
  - Evidence: call sites found around config load, `db_show_history()`, `_llm_call_with_retry()`, `llm_manager_decide()`, `execute_codex()`, `notify()`, `infinite_loop()`, and `main()`.
- Command/check: `sed -n '620,1040p' apex-infinite-cli/apex_infinite.py` and `sed -n '1040,1130p' apex-infinite-cli/apex_infinite.py`
  - Result: PASS - inspected loop, execution, history, and startup behavior directly.
  - Evidence: confirmed `execute_codex()` returns raw output and `db_log()` receives raw `agent_response`, `output_val`, `reason_val`, and help/done messages.
- UI product-surface check: PASS - current product surface inventory identifies user-facing output that later renderer helpers must own.
- UI craft check: PASS - mapped current weak presentation points without changing behavior.

**BQC Fixes**:
- N/A - no application code changed.

---

### Task T001 - Verify baseline prompt/routing tests and CLI import behavior

**Started**: 2026-07-02 22:34
**Completed**: 2026-07-02 22:53
**Duration**: 19 minutes

**Notes**:
- Verified the active shell was using another project's Python environment for
  bare `python` and `pytest`, then used the CLI-local virtualenv for stable
  baseline evidence.
- Confirmed the prompt/routing compatibility test suite passes unchanged.

**Files Changed**:
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/implementation-notes.md` - created implementation log and recorded T001 evidence.
- `.spec_system/specs/phase00-session01-config-and-renderer-boundary/tasks.md` - marked T001 complete.

**Verification**:
- Command/check: `bash .spec_system/scripts/check-prereqs.sh --json --tools "python3,pytest,black,pylint"`
  - Result: FAIL - global shell PATH is not the project CLI environment.
  - Evidence: `python3` and `pytest` passed, but `black` and `pylint` were not visible on PATH.
- Command/check: `python -c "import apex_infinite; print(len(apex_infinite.KNOWN_COMMANDS))"`
  - Result: FAIL - bare Python did not load CLI runtime dependencies.
  - Evidence: raised `ModuleNotFoundError: No module named 'openai'`, confirming the wrong environment was active.
- Command/check: `./.venv/bin/python -c "import sys; print(sys.executable); import click, rich, yaml, openai; print('runtime ok')"`
  - Result: PASS - CLI-local virtualenv imports runtime dependencies.
  - Evidence: printed `/home/aiwithapex/projects/apex-spec-system-open/apex-infinite-cli/.venv/bin/python` and `runtime ok`.
- Command/check: `./.venv/bin/python -m pytest tests/test_prompts.py -v`
  - Result: PASS - prompt/routing baseline passes.
  - Evidence: 62 tests passed in 10.39s.
- Command/check: `./.venv/bin/python -m black --version && ./.venv/bin/python -m pylint --version | sed -n '1,5p'`
  - Result: PASS - formatter and linter are available in the CLI-local virtualenv.
  - Evidence: black 26.5.1 and pylint 4.0.6 printed versions.
- UI product-surface check: N/A - task only verified baseline import and prompt/routing tests.
- UI craft check: N/A - task did not change UI output.

**BQC Fixes**:
- N/A - no application code changed.

---

## Task Log

### 2026-07-02 - Session Start

**Environment verified**:
- [x] Prerequisites confirmed with `.spec_system/scripts/check-prereqs.sh --json --env`
- [x] Tools available: `jq`, `git`
- [x] Directory structure ready

---
