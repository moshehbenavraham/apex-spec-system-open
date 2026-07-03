# Session Specification

**Session ID**: `phase00-session04-event-stream-boundary`
**Phase**: 00 - Apex Infinite CLI Upgrade
**Status**: Complete
**Created**: 2026-07-03

---

## 1. Session Overview

This session adds the machine-readable lifecycle boundary that future visual
surfaces will consume. It turns the existing renderer and subprocess lifecycle
facts from Sessions 01 through 03 into raw JSONL events without asking wrappers
to scrape Rich frames, plain text, or history rows.

It is next because the analyzer reports Phase 00 in progress, no active
session, and Sessions 01 through 03 complete. Session 04 is the earliest
unfinished candidate and is the prerequisite for documentation polish and the
later Linux wrapper spike.

The work stays scoped to `apex-infinite-cli/` and its CLI documentation. It
preserves prompt routing, manager normalization, SQLite schema compatibility,
`cc_response`, normal human output, dry-run behavior, subprocess return text,
and base terminal-only dependencies.

---

## 2. Objectives

1. Provide an importable event emitter API that writes line-buffered JSONL
   lifecycle events with raw operational facts.
2. Add `--event-stream PATH` and guarded `--event-stream -` support without
   changing normal human output.
3. Add explicit `--machine-output` mode so stdout JSONL cannot mix with Rich or
   plain human rendering.
4. Emit stable event names for startup, iteration, history, manager decisions,
   prompt dispatch, Codex subprocess lifecycle, DB logging, help, completion,
   max-iteration stops, interrupts, timeouts, and errors.
5. Prove through dry-run and unit tests that event payloads are flushed, stable,
   raw, stdout-isolated, and free of secrets, ANSI escapes, Rich markup, frame
   glyphs, and visual tokens.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase00-session01-config-and-renderer-boundary` - Provides validated UI
      settings, Click display flags, renderer injection, and raw history safety
      coverage.
- [x] `phase00-session02-rich-operator-console` - Provides semantic lifecycle
      labels and stable operator-console states for events to mirror as raw
      facts.
- [x] `phase00-session03-subprocess-and-history-visibility` - Provides
      subprocess lifecycle facts, compact history display, and raw DB
      compatibility coverage.

### Required Tools Or Knowledge

- Python 3.10+ CLI development with Click, Rich, SQLite, JSONL, pytest, and
  subprocess testing.
- Existing `main()`, `infinite_loop()`, `execute_codex()`, `db_log()`,
  `notify()`, and `ApexRenderer` integration points.
- Phase 00 PRD, PRD UX Flow 9, Session 04 stub, `CONVENTIONS.md`,
  `CONSIDERATIONS.md`, and `SECURITY-COMPLIANCE.md` event-stream boundaries.

### Environment Requirements

- CLI dependencies from `apex-infinite-cli/requirements.txt` and development
  dependencies from `apex-infinite-cli/requirements-dev.txt`.
- Local tests can use `CliRunner`, temporary event files, fake LLM clients,
  fake Codex process runners, monkeypatching, and recorded consoles.
- No real provider API keys, network calls, or real Codex subprocess launches
  are required for event tests.
- Authored files remain ASCII-only with Unix LF line endings.

---

## 4. Scope

### In Scope (MVP)

- Operator can pass `--event-stream PATH` to write line-buffered JSONL events
  while normal Rich, plain, ASCII, and compact human output remains unchanged.
- Automation can pass `--machine-output --event-stream -` so stdout contains
  only JSONL events and no human renderer output.
- CLI rejects `--event-stream -` without `--machine-output` with a clear Click
  error.
- CLI rejects `--machine-output` without `--event-stream` with a clear Click
  error.
- CLI disables terminal bell and desktop notifications when
  `--machine-output` is active.
- Developer can import an event emitter API from
  `apex-infinite-cli/apex_infinite_events.py`.
- Event payloads include raw lifecycle facts for config/UI resolution,
  startup, iteration start, history summary, manager decision, prompt dispatch,
  Codex start, Codex finish, Codex failure states, DB log, help pause,
  completion, max-iteration stop, interrupts, and errors.
- Event payloads contain raw strings, numbers, booleans, lists, maps, nulls,
  and timestamps only; no Rich renderables, ANSI escapes, box/frame glyphs,
  visual-theme tokens, renderer snapshots, or secrets.
- Event write failures surface as visible human errors unless
  `--machine-output` is active, in which case they are emitted as
  machine-readable errors when possible.
- Dry-run tests prove event order, names, payload stability, file flushing,
  stdout collision prevention, and no real LLM or Codex calls.

### Out Of Scope (Deferred)

- Productizing a graphical Linux wrapper - Reason: Sessions 06 and 07 own
  optional wrapper spike and productization after this boundary exists.
- Rewriting the Rich renderer to consume events internally - Reason: this
  session exposes wrapper-facing facts while preserving current human output.
- Changing `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or
  `build_codex_prompt()` - Reason: event output must not alter prompt routing.
- Changing SQLite schema, renaming `cc_response`, adding durable event tables,
  or migrating existing history DBs - Reason: event streams are side-channel
  output, not local history storage.
- Adding graphical, webview, Qt, PySide6, PyQt, qmltermwidget, QTermWidget, or
  terminal-emulator dependencies to the base CLI - Reason: base CLI remains
  lightweight and headless-safe.
- Copying reference source, QML, shaders, constants, profile data, images,
  fonts, icons, resource manifests, or build scripts - Reason: clean-room
  boundaries remain active.
- Debug/admin UI surfaces - Reason: diagnostics belong in tests, event payloads,
  and docs, not primary human output.

---

## 5. Technical Approach

### Architecture

Create a small `apex-infinite-cli/apex_infinite_events.py` module that owns the
event data shape, JSON serialization, file/stdout stream handling, flushing,
and raw-payload validation. Keep this module independent from Rich renderer
types so future wrappers can depend on it without importing terminal UI code.

Wire an optional event emitter through `main()`, `infinite_loop()`,
`execute_codex()`, `db_log()` call sites, and interrupt/notification paths.
The emitter should observe existing facts rather than changing workflow
decisions. Normal runs with `--event-stream PATH` continue using
`ApexRenderer`; machine-output mode uses a no-human-output adapter so fallback
console prints do not corrupt stdout.

Use Click validation for incompatible flag combinations before the loop starts.
Open event streams with explicit cleanup and line buffering. Treat stdout as a
special sink: it is allowed only in machine-output mode. When writing to a file,
human output remains on the existing console path.

Keep event payloads narrow and stable. Include event name, timestamp, and a
payload object. Payloads should carry raw facts such as project path, provider,
model, theme name, iteration number, manager output/reason, prompt length,
known-command status, Codex process state, return code, elapsed seconds,
timeout seconds, DB stored state, and stop reason. Do not include API keys,
full config maps, Rich markup, renderer labels as styling, frame glyphs, or
visual token values.

Use an initial event registry with names such as `config_resolved`,
`startup`, `iteration_started`, `history_summary_started`,
`history_summary_completed`, `manager_decision_started`,
`manager_decision_completed`, `prompt_dispatched`, `codex_dry_run`,
`codex_started`, `codex_completed`, `codex_failed`, `output_summary`,
`db_logged`, `help_requested`, `completion`, `max_iterations_reached`,
`interrupt_requested`, `interrupt_quit`, and `error`. The implementation may
add narrower state names only when tests and docs define the contract.

### Design Patterns

- Side-channel observer: events mirror workflow facts without changing manager,
  prompt, DB, or subprocess contracts.
- Context-managed stream: event files/stdout are opened, flushed, and closed
  with cleanup on scope exit for all acquired resources.
- Explicit machine mode: stdout JSONL requires `--machine-output`, preventing
  accidental mixed human and machine output.
- Schema-light validation: event names and payload values are checked before
  writes so callers cannot emit renderer objects or non-JSON data.
- Test-first wiring: dry-run and monkeypatched loop tests cover order and
  payload stability without real provider or Codex calls.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/apex_infinite_events.py` | Importable event emitter API, JSONL writer, stdout/file sink validation, payload safety checks, and no-op emitter | ~220 |
| `apex-infinite-cli/tests/test_event_stream.py` | Event API, CLI flag validation, dry-run event order, stdout isolation, flushing, and raw-payload safety tests | ~280 |
| `apex-infinite-cli/docs/event-stream.md` | Wrapper-facing event stream contract, event names, payload principles, CLI examples, and safety notes | ~180 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/apex_infinite.py` | Add `--event-stream`, `--machine-output`, event emitter lifecycle, loop emissions, subprocess emissions, DB log emissions, and notification suppression | ~260 |
| `apex-infinite-cli/apex_infinite_ui.py` | Add a no-human-output renderer adapter or equivalent suppression hook for machine-output mode | ~90 |
| `apex-infinite-cli/tests/test_cli_options.py` | Cover event flag validation, machine-output guardrails, and loop wiring with fake emitters | ~120 |
| `apex-infinite-cli/tests/test_subprocess_execution.py` | Cover Codex start, finish, dry-run, timeout, missing-binary, non-zero, and generic-error event emissions | ~120 |
| `apex-infinite-cli/tests/test_renderer.py` | Cover no-human-output adapter behavior and stdout-safe rendering suppression | ~80 |
| `apex-infinite-cli/README_apex-infinite-cli.md` | Document event-stream usage, `--machine-output`, stdout guardrails, and raw event safety | ~100 |
| `apex-infinite-cli/docs/operator-runbook.md` | Add operator guidance for event files, machine-output mode, wrapper consumption, and failure handling | ~80 |
| `apex-infinite-cli/docs/prompt-contract.md` | Clarify event and machine-output behavior do not change manager parsing or Codex prompt generation | ~60 |
| `apex-infinite-cli/docs/troubleshooting.md` | Add event-stream misuse, write failure, stdout collision, and machine-output troubleshooting | ~70 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] `--event-stream PATH` writes one valid JSON object per line to the target
      file and flushes after each event.
- [ ] Normal human output is unchanged when `--event-stream PATH` is used
      without `--machine-output`.
- [ ] `--event-stream -` is rejected unless `--machine-output` is present.
- [ ] `--machine-output` is rejected unless `--event-stream` is present.
- [ ] `--machine-output --event-stream -` writes JSONL only to stdout and does
      not emit Rich or plain human output, terminal bell, or desktop
      notifications.
- [ ] Event names cover startup, iteration lifecycle, history summary, manager
      decision, prompt dispatch, Codex subprocess lifecycle, output summary,
      DB logging, help, completion, max-iteration stop, timeout, interrupt,
      and errors.
- [ ] Event payloads include raw operational facts and exclude provider API
      keys, full provider config maps, ANSI escapes, Rich markup, box/frame
      glyphs, renderer snapshots, visual-theme token values, and copied visual
      reference data.
- [ ] Event API is importable by tests and future wrappers without importing
      Rich renderer classes.
- [ ] Prompt routing, autonomous handoffs, `build_codex_prompt()` output,
      `execute_codex()` return text, and SQLite schema remain compatible.

### Testing Requirements

- [ ] Event API tests cover file writes, stdout writes, flush behavior,
      disabled/no-op emitters, invalid event names, invalid payload values, and
      raw-payload safety checks.
- [ ] Click tests cover `--event-stream PATH`, `--event-stream -`,
      `--machine-output`, invalid flag combinations, and loop wiring.
- [ ] Dry-run loop tests cover event order and event names without real LLM or
      Codex calls.
- [ ] Subprocess tests cover event emissions for dry-run, start, completion,
      non-zero exit, timeout, missing binary, and generic exception paths.
- [ ] Tests prove stdout machine mode does not contain human renderer labels.
- [ ] Existing prompt, renderer, history, UI config, CLI option, and subprocess
      tests pass.

### Non-Functional Requirements

- [ ] Event writing is line-buffered and bounded to one JSON object per event.
- [ ] Event stream failures do not corrupt SQLite history or change manager
      decisions.
- [ ] Event stream support adds no new runtime dependencies.
- [ ] File handles and stdout writer ownership are cleaned up safely.
- [ ] Authored files remain ASCII-only with Unix LF line endings.

### Quality Gates

- [ ] All files ASCII-encoded
- [ ] Unix LF line endings
- [ ] Code follows project conventions
- [ ] Primary human surfaces contain product-facing copy only
- [ ] Machine stdout contains JSONL only when machine-output mode is active
- [ ] `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v` passes
- [ ] `cd apex-infinite-cli && ./.venv/bin/python -m black --check apex_infinite.py apex_infinite_ui.py apex_infinite_events.py tests/` passes
- [ ] `cd apex-infinite-cli && ./.venv/bin/python -m pylint apex_infinite.py apex_infinite_ui.py apex_infinite_events.py` passes

---

## 8. Implementation Notes

### Working Assumptions

- Session 04 targets `apex-infinite-cli/` inside a single repository rather
  than formal monorepo package metadata. Evidence: analyzer reports
  `monorepo: false`, PRD constraints say CLI sessions should target the
  `apex-infinite-cli/` path, and Phase 00 stubs omit package metadata. Planning
  can proceed because all deliverables are path-scoped.

### Conflict Resolutions

- Session 04 stub records an open question between `--no-human-output`,
  `--machine-output`, or an equivalent internal mode. The chosen
  interpretation is `--machine-output` because `PRD_UX.md` Flow 9 and
  `.spec_system/CONVENTIONS.md` explicitly name it as the supported
  human-rendering disable mode.
- Session 04 says to separate config, DB, LLM, manager, prompt, subprocess,
  notification, and rendering as much as practical, while considerations warn
  against broad rewrites. The chosen interpretation is incremental observer
  wiring plus a separate event module, not a class-based engine rewrite,
  because existing Sessions 01 through 03 already provide tested boundaries.

### Key Considerations

- Preserve prompt routing and manager prompt text unless behavior explicitly
  changes with matching docs and tests.
- Keep `cc_response`, SQLite schema, normalized path keys, and raw history rows
  unchanged.
- Keep event payloads raw and safe: no secrets, markup, ANSI, visual tokens, or
  copied reference material.
- Keep graphical wrapper dependencies out of the base CLI.

### Potential Challenges

- Machine-output mode can accidentally leak human output through fallback
  `console.print()` paths: use a no-human-output adapter and explicit tests
  against stdout.
- Event writing can fail after the loop starts: handle file/open/write errors
  explicitly and avoid partial state changes beyond reporting the failure.
- Emitting full prompts or responses can leak sensitive project text: keep
  payloads to bounded metadata and raw summaries unless a specific event needs
  full raw text for the documented contract.

### Relevant Considerations

- [P00] **Single-file CLI pressure**: Extract the event emitter only where it
  lowers risk; keep workflow logic recognizable.
- [P00] **Prompt contract coupling**: Do not edit prompt constants or prompt
  generation for display-only event needs.
- [P00] **History compatibility**: Preserve local SQLite history shape and raw
  stored facts.
- [P00] **Subprocess behavior lock**: Event emissions must not change
  subprocess return text, fallback behavior, timeout text, or verbose behavior.
- [P00] **Raw durable facts only**: JSONL events must exclude ANSI, Rich markup,
  frame glyphs, visual tokens, secrets, and renderer snapshots.
- [P00] **Machine-output isolation**: stdout JSONL is valid only under explicit
  `--machine-output`.
- [P00] **Event stream is the wrapper contract**: Future wrappers consume the
  event API or JSONL, not human output.

### Behavioral Quality Focus

Checklist active: Yes
Top behavioral risks for this session:
- stdout contamination when machine-output mode writes JSONL to stdout.
- file handle leaks or unflushed JSONL events on normal completion, timeout,
  interrupt, or write failure.
- sensitive values leaking through overly broad event payloads.
- prompt, DB, or subprocess compatibility drift caused by observer wiring.

---

## 9. Testing Strategy

### Unit Tests

- Test `EventEmitter`, no-op emitter, stdout/file sinks, invalid event names,
  invalid payloads, JSON serialization, newline separation, and flush calls in
  `apex-infinite-cli/tests/test_event_stream.py`.
- Test `execute_codex()` event emissions for dry-run, start, completion,
  non-zero exit, timeout, missing binary, generic error, and preserved return
  text in `apex-infinite-cli/tests/test_subprocess_execution.py`.
- Test no-human-output adapter semantics in renderer tests.

### Integration Tests

- Use `CliRunner` with temporary config, temporary project path, fake loop, and
  fake emitter to verify `--event-stream`, `--machine-output`, and invalid
  combinations in `apex-infinite-cli/tests/test_cli_options.py`.
- Use a dry-run loop with monkeypatched LLM and DB functions to verify event
  order, event names, payload fields, and no real provider or Codex calls.
- Verify prompt-routing tests remain unchanged and passing.

### Runtime Verification

- Run `python apex_infinite.py --path <tmp-project> --start implement --dry-run --event-stream <tmp-jsonl>` with monkeypatched or test fixtures and inspect JSONL line count, names, and flushing behavior.
- Run `python apex_infinite.py --path <tmp-project> --start implement --dry-run --machine-output --event-stream -` in tests and assert stdout parses as JSONL only.
- Run the full CLI pytest suite plus Black and Pylint for changed modules.

### Edge Cases

- `--event-stream -` without `--machine-output`.
- `--machine-output` without `--event-stream`.
- Event path parent directory missing or unwritable.
- Event payload contains non-JSON objects, ANSI escapes, Rich markup-like
  strings, frame glyphs, or secret-looking values.
- Event stream write failure during an iteration.
- Help, interrupt, completion, max-iteration stop, timeout, missing binary, and
  non-zero exit events.
- `NO_COLOR`, `TERM=dumb`, plain, ASCII, compact, and non-terminal modes with
  event-stream file output.

---

## 10. Dependencies

### Other Sessions

- Depends on: `phase00-session01-config-and-renderer-boundary`,
  `phase00-session02-rich-operator-console`,
  `phase00-session03-subprocess-and-history-visibility`
- Depended by: `phase00-session05-docs-samples-and-runbooks`,
  `phase00-session06-linux-wrapper-spike`,
  `phase00-session07-linux-visual-wrapper-productization`,
  `phase00-session08-release-verification`

---

## Next Steps

Session complete. Run the `plansession` workflow step to scope Session 05.
