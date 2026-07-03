# Session Specification

**Session ID**: `phase00-session03-subprocess-and-history-visibility`
**Phase**: 00 - Apex Infinite CLI Upgrade
**Status**: Implemented
**Created**: 2026-07-03

---

## 1. Session Overview

This session improves operator visibility during long Codex CLI subprocess
runs and makes history inspection usable as a compact operations ledger. It
builds directly on the renderer, UI configuration, semantic labels, and
operator-console surfaces delivered by Sessions 01 and 02.

It is next because the analyzer reports Phase 00 in progress, no active
session, and Sessions 01 and 02 complete. Session 03 is the earliest unfinished
candidate and provides subprocess lifecycle facts that Session 04 will need for
the event-stream boundary.

The work stays scoped to `apex-infinite-cli/`. It preserves prompt routing,
SQLite schema compatibility, normalized history keys, `cc_response`, dry-run
behavior, verbose execution output, timeout text, stderr fallback, non-zero
exit wrapping, missing-binary handling, and generic exception reporting.

---

## 2. Objectives

1. Show live or durable elapsed subprocess state for `codex exec`, including
   binary, process state, elapsed time, and configured timeout.
2. Preserve captured stdout, stderr fallback, return code, timeout,
   `FileNotFoundError`, generic exception, dry-run, and `--verbose` semantics.
3. Redesign `--history` as a compact ledger that remains readable at 80
   columns and expands row detail through the existing `--verbose` flag.
4. Prove through focused tests that subprocess and history changes do not
   persist styled output, change the DB schema, or alter prompt routing.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase00-session01-config-and-renderer-boundary` - Provides validated UI
      settings, theme tokens, renderer helpers, Click display flags, and raw
      SQLite history safety coverage.
- [x] `phase00-session02-rich-operator-console` - Provides semantic renderer
      labels, iteration frames, Codex execution states, DB log rendering, and
      operator-console fallback behavior.

### Required Tools Or Knowledge

- Python 3.10+ CLI development with Click, Rich, SQLite, pytest, and
  subprocess management.
- Existing `execute_codex()`, `db_show_history()`, `db_log()`, and
  `ApexRenderer.print_history()` behavior.
- Session 03 stub requirements for live execution and compact history.
- Clean-room and raw-data boundaries from the Phase 00 PRD, PRD UX,
  `CONVENTIONS.md`, `CONSIDERATIONS.md`, and `SECURITY-COMPLIANCE.md`.

### Environment Requirements

- CLI dependencies from `apex-infinite-cli/requirements.txt` and
  `apex-infinite-cli/requirements-dev.txt`.
- Local test environment can run `pytest`, `black`, and `pylint` through
  `apex-infinite-cli/.venv/bin/`.
- No provider API keys, real LLM calls, or real Codex subprocesses are required
  for tests; use fake runners, monkeypatching, and temporary DB paths.
- Authored files remain ASCII-only with Unix LF line endings.

---

## 4. Scope

### In Scope (MVP)

- Operator can see that Codex execution is active, how long it has been
  running, which binary is running, and the configured timeout threshold.
- `execute_codex()` preserves stdout capture, stderr fallback when stdout is
  empty, non-zero exit message shape, timeout return text, missing-binary
  return text, generic exception return text, dry-run command text, and verbose
  response rendering.
- If subprocess handling moves from `subprocess.run()` to `subprocess.Popen`,
  process cleanup, timeout termination, and captured stdout/stderr collection
  are handled explicitly.
- `--history` renders a compact ledger with command, reason, timestamp, status,
  project key, and truncated response summary without horizontal scrolling at
  80 columns.
- Existing `--verbose` expands history reason and response detail; no
  `--history-verbose` flag is added.
- Empty, sparse legacy, short, long, plain, ASCII, compact, and styled history
  rows render safely.
- SQLite history rows remain raw workflow facts with no ANSI escapes, Rich
  markup, box/frame glyphs, renderer labels, visual tokens, or truncation-only
  display text.
- Tests cover subprocess success, stderr-only output, non-zero exit, timeout,
  dry-run, missing binary, generic exception, and history formatting.

### Out Of Scope (Deferred)

- Public JSONL event stream, importable event emitter API, or
  `--machine-output` - Reason: Session 04 owns the lifecycle event boundary.
- Linux visual wrapper code, wrapper dependencies, QML, Qt, or graphical
  packaging - Reason: Sessions 06 and 07 own optional wrapper work.
- SQLite schema migration, `cc_response` rename, retention policy, purge
  command, or path canonicalization changes - Reason: this session must keep
  existing history DBs readable without migration.
- Prompt contract changes - Reason: display work must not alter
  `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or
  `build_codex_prompt()`.
- Broad documentation refresh, transcripts, or event-stream docs - Reason:
  Session 05 owns docs after implemented behavior and event behavior exist.
- Debug/admin UI surfaces - Reason: diagnostics belong in tests and
  implementation notes, not the primary operator console.

---

## 5. Technical Approach

### Architecture

Start with characterization tests around current `execute_codex()` and history
rendering so compatibility is explicit before behavior-preserving rewrites.
Then add the smallest subprocess execution boundary that makes live status
testable. The likely implementation is either an injectable runner helper or a
small `subprocess.Popen` wrapper inside `apex-infinite-cli/apex_infinite.py`
that returns raw captured stdout, stderr, and return-code facts while keeping
`execute_codex()` as the public workflow boundary.

Extend `apex-infinite-cli/apex_infinite_ui.py` rather than bypassing it. Add
renderer-facing execution facts for elapsed seconds, process state, timeout,
and completion state, and update `print_history()` into a ledger-style display
that uses the existing injected `Console(record=True, width=...)` test pattern.
Plain and constrained modes must emit durable line-oriented states instead of
live-only spinners or carriage-return animation.

Keep DB writes and prompt routing untouched. History display should derive
truncated summaries at render time only; it must not add durable fields,
rewrite legacy rows, or store display labels.

### Design Patterns

- Characterization before rewrite: lock existing subprocess return behavior
  with tests before introducing live status.
- Renderer facade: workflow code reports facts and renderer code chooses Rich,
  plain, ASCII, compact, or constrained presentation.
- Injectable process boundary: fake runners and monkeypatches cover success,
  stderr-only, failure, timeout, missing binary, and generic exception paths
  without launching Codex.
- Display-only derivation: compact history summaries, truncation counts, and
  verbose expansion are render-time concerns, not schema changes.
- Fallback-first output: plain and non-terminal execution paths get durable
  status lines rather than transient live effects.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/tests/test_subprocess_execution.py` | Focused subprocess and `execute_codex()` compatibility tests using fake runners and monkeypatching | ~240 |
| `apex-infinite-cli/tests/test_history_rendering.py` | Compact and verbose history ledger tests for empty, short, long, sparse legacy, plain, ASCII, compact, and width cases | ~220 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/apex_infinite.py` | Add a testable subprocess execution boundary, live/durable elapsed status wiring, and preserved `execute_codex()` return semantics | ~180 |
| `apex-infinite-cli/apex_infinite_ui.py` | Add subprocess elapsed/process-state rendering and redesign history as a compact ledger with verbose expansion | ~220 |
| `apex-infinite-cli/tests/test_renderer.py` | Extend raw-storage safety and renderer semantic coverage for execution status and history display-only summaries | ~80 |
| `apex-infinite-cli/tests/test_cli_options.py` | Extend CLI coverage for `--history --verbose` routing and unchanged prompt routing around display changes | ~60 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] Non-dry-run Codex execution visibly reports active/running state,
      elapsed time, binary, project path, and timeout threshold.
- [ ] Plain, compact, ASCII, non-terminal, `NO_COLOR`, and `TERM=dumb` paths
      do not rely on transient live-only output for subprocess state.
- [ ] Success returns captured stdout exactly as before.
- [ ] Stderr-only success returns stderr when stdout is blank.
- [ ] Non-zero exits return the existing wrapped error text with stdout,
      stderr, and return code.
- [ ] Timeout, missing binary, generic exception, dry-run, and verbose output
      behavior remain compatible.
- [ ] `--history` default output is compact and readable at 80 columns.
- [ ] `--history --verbose` expands reason and response detail without adding
      a new flag.
- [ ] Existing SQLite history databases remain readable without migration.
- [ ] No prompt contract, manager command normalization, DB schema, or
      `cc_response` column behavior changes.

### Testing Requirements

- [ ] Subprocess tests cover success, stderr-only output, non-zero exit,
      timeout cleanup, dry-run, missing binary, and generic exception.
- [ ] History tests cover empty, short, long, sparse legacy, compact, verbose,
      styled, plain, ASCII, and compact output at 80, 100, and 120 columns.
- [ ] Tests prove history rows contain raw values only and no renderer labels,
      ANSI escapes, Rich markup, box/frame glyphs, or truncation-only display
      text.
- [ ] Existing prompt/routing tests pass unchanged.
- [ ] CLI tests cover `--history --verbose` and verify no
      `--history-verbose` flag is introduced.

### Non-Functional Requirements

- [ ] No graphical runtime dependency is added to the base CLI.
- [ ] Live subprocess display does not introduce deadlocks or unbounded memory
      growth for captured output.
- [ ] Process timeout cleanup terminates or kills the child process and
      preserves timeout return text.
- [ ] History rendering for 50 rows stays bounded and readable.
- [ ] API keys and environment secrets are not printed, stored, or exposed by
      new tests or renderer output.
- [ ] All changed authored files are ASCII-only with Unix LF line endings.

### Quality Gates

- [ ] All files ASCII-encoded
- [ ] Unix LF line endings
- [ ] Code follows project conventions
- [ ] Primary operator surfaces contain product-facing copy only
- [ ] `pytest tests/ -v` passes from `apex-infinite-cli/`
- [ ] `black --check apex_infinite.py apex_infinite_ui.py tests/` passes
- [ ] `pylint apex_infinite.py apex_infinite_ui.py` passes

---

## 8. Implementation Notes

### Working Assumptions

- Session 03 remains scoped to `apex-infinite-cli/` even though the repo is
  not configured as a formal monorepo. Evidence: the analyzer reports
  `monorepo: false`, the master PRD says CLI sessions target
  `apex-infinite-cli/` by path, and `CONVENTIONS.md` names that directory as
  the primary development target. Planning can proceed because all deliverables
  are concrete files under that path.
- It is acceptable to introduce a small process-runner boundary if tests show
  it lowers risk versus continuing to expand `execute_codex()` directly.
  Evidence: `CONVENTIONS.md` says to split subprocess helpers when that lowers
  risk, and Session 03 requires fake-runner or monkeypatch tests. Planning can
  proceed because either a helper or an internal function keeps the public CLI
  behavior unchanged.
- Documentation updates are intentionally minimal or deferred unless tests
  expose a behavior/documentation mismatch. Evidence: Session 05 owns broad
  README, runbook, history, prompt-contract, troubleshooting, transcript, and
  clean-room documentation after implemented behavior and event behavior exist.
  Planning can proceed because Session 03 success criteria are enforced by
  tests and implementation notes.

### Key Considerations

- Preserve raw durable facts: history rows are operational records, not
  renderer snapshots.
- Test before replacing `subprocess.run()` so return strings and edge cases are
  not accidentally changed.
- Use renderer labels for operator visibility, but never persist those labels.
- Keep live rendering optional and degraded to durable lines for constrained
  output.

### Potential Challenges

- Subprocess live display can change capture semantics: mitigate with
  characterization tests and a small runner boundary that returns raw captured
  stdout, stderr, and return code facts.
- Timeout cleanup can leave a child process alive: mitigate with explicit
  terminate/kill handling and timeout-path tests.
- History tables can become too wide at 80 columns: mitigate with ledger-style
  rows, deterministic truncation, and width-specific renderer tests.
- Long agent responses can make tests brittle: mitigate with semantic
  assertions and explicit truncation-count checks instead of full-frame
  snapshots.

### Relevant Considerations

- [P00] **History compatibility**: Preserve existing history databases, the
  legacy `cc_response` column, normalized project path keys, and raw stored
  workflow data.
- [P00] **Subprocess behavior lock**: Live execution display must preserve
  stdout capture, stderr fallback, non-zero exit wrapping, timeout text,
  dry-run output, missing-binary handling, generic exception reporting, and
  `--verbose` semantics.
- [P00] **Raw durable facts only**: SQLite rows must not contain ANSI escapes,
  Rich markup, box/frame glyphs, visual tokens, secrets, or renderer snapshots.
- [P00] **Width and log readability**: Changed output must be verified at 80,
  100, and 120 columns, and plain mode must stay deterministic for logs.
- [P00] **One depth flag**: Reuse `--verbose` for expanded history detail
  instead of adding a mode-specific duplicate flag.

### Behavioral Quality Focus

Checklist active: Yes

Top behavioral risks for this session:
- Scoped subprocess lifecycle work must clean up acquired child-process
  resources on timeout or exception.
- External command execution must keep timeout, process-state, and failure-path
  handling explicit while preserving raw output contracts.
- History display consumes legacy external data shape and must handle empty,
  sparse, long, and malformed-ish row values without breaking the UI or durable
  storage boundary.
- User-facing operator output must remain product-facing, with diagnostics
  confined to tests and implementation notes.

---

## 9. Testing Strategy

### Unit Tests

- Test `execute_codex()` dry-run, success, stderr-only success, non-zero exit,
  timeout, missing binary, generic exception, and verbose rendering with fake
  subprocess boundaries.
- Test any new process-runner helper for cleanup on timeout and raw
  stdout/stderr/return-code capture.
- Test history row formatting for empty, short, long, sparse legacy, help/done,
  completion, and normal iteration records.

### Integration Tests

- Use `CliRunner` for `--history`, `--history --verbose`, `--plain`,
  `--ascii`, and `--compact` combinations without starting the autonomous
  loop.
- Use temporary DB paths or monkeypatched `DB_DIR` and `DB_PATH` to verify
  displayed summaries do not mutate stored history rows.
- Run existing prompt/routing tests to confirm no prompt contract drift.

### Runtime Verification

- Run `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`.
- Run `cd apex-infinite-cli && ./.venv/bin/python -m black --check apex_infinite.py apex_infinite_ui.py tests/`.
- Run `cd apex-infinite-cli && ./.venv/bin/python -m pylint apex_infinite.py apex_infinite_ui.py`.
- Run ASCII and LF checks over changed authored files.

### Edge Cases

- Codex emits stdout and stderr; stdout remains preferred on success.
- Codex emits only stderr with return code 0; stderr is returned.
- Codex exits non-zero with empty stderr; fallback error text remains stable.
- Codex times out after partial output; timeout text remains stable and child
  cleanup runs.
- Codex binary is missing; missing-binary text remains stable.
- History rows contain long paths, long manager reasons, long agent responses,
  blank legacy columns, help pauses, completion markers, and no current path
  filter.

---

## 10. Dependencies

### Other Sessions

- Depends on:
  - `phase00-session01-config-and-renderer-boundary`
  - `phase00-session02-rich-operator-console`
- Depended by:
  - `phase00-session04-event-stream-boundary`
  - `phase00-session05-docs-samples-and-runbooks`
  - `phase00-session06-linux-wrapper-spike`
  - `phase00-session07-linux-visual-wrapper-productization`
  - `phase00-session08-release-verification`

---

## Next Steps

Run the `creview` workflow step to review and repair the implementation changes.
