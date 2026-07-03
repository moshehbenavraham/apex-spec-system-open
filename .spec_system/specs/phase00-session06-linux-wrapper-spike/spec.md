# Session Specification

**Session ID**: `phase00-session06-linux-wrapper-spike`
**Phase**: 00 - Apex Infinite CLI Upgrade
**Status**: Not Started
**Created**: 2026-07-03
**Base Commit**: `df713021c172c3c04344908c6b25afe6e8207cea`

---

## 1. Session Overview

This session proves whether the optional Linux visual wrapper can display Apex
Infinite CLI lifecycle state from the Session 04 event stream without changing
the base workflow engine. It creates an isolated PySide6/Qt Quick prototype,
launches the existing CLI through the guarded JSONL stdout mode, maps events to
wrapper state, and records the dependency, license, packaging, and fallback
evidence needed before productization.

It is next because the analyzer reports Phase 00 in progress, no active
session, and Sessions 01 through 05 complete. Session 06 is the earliest
unfinished candidate, and its stub depends on the event stream plus the
documentation and clean-room boundary delivered by the prior sessions.

The work is a spike, not the release wrapper. The prototype must stay under the
optional wrapper boundary, avoid graphical dependencies in the base CLI path,
and produce enough evidence for Session 07 to either productize PySide6/QML or
defer with a precise blocker.

---

## 2. Objectives

1. Create an isolated Linux visual wrapper prototype package that can consume
   Apex Infinite CLI JSONL events without scraping Rich output, plain output,
   SQLite history, or terminal frames.
2. Implement a minimal PySide6/Qt Quick surface with a read-only event log,
   status panels, theme/effect controls, and independently designed low-risk
   CRT-style effects for feasibility review.
3. Preserve base CLI behavior and dependency boundaries by keeping PySide6,
   QML, subprocess launch helpers, and wrapper docs outside the normal terminal
   runtime path.
4. Add focused tests for event-line parsing, launcher command construction,
   malformed-event handling, optional dependency guards, and no-human-output
   stdout isolation.
5. Document the spike evidence, license obligations, packaging risks,
   qmltermwidget/QTermWidget exclusion, PyQt exclusion, and pywebview plus
   xterm.js backup decision.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase00-session01-config-and-renderer-boundary` - Provides UI config,
      display flags, renderer injection, and raw data boundaries.
- [x] `phase00-session02-rich-operator-console` - Provides the terminal
      operator-console semantics that the wrapper must not scrape or fork.
- [x] `phase00-session03-subprocess-and-history-visibility` - Provides
      subprocess visibility expectations and history compatibility constraints.
- [x] `phase00-session04-event-stream-boundary` - Provides
      `--event-stream`, `--machine-output`, the importable event emitter API,
      and JSONL stdout guardrails.
- [x] `phase00-session05-docs-samples-and-runbooks` - Provides the visual
      wrapper boundary, transcript samples, fallback docs, and clean-room
      no-copy rules.

### Required Tools Or Knowledge

- Current event names, event version, and payload validation in
  `apex-infinite-cli/apex_infinite_events.py`.
- Current Click flags and machine-output guardrails in
  `apex-infinite-cli/apex_infinite.py`.
- PySide6/Qt Quick/QML basics for an optional Linux-only wrapper.
- Existing docs in `apex-infinite-cli/docs/event-stream.md` and
  `apex-infinite-cli/docs/visual-wrapper-boundary.md`.
- Clean-room visual rules from `CONVENTIONS.md`,
  `SECURITY-COMPLIANCE.md`, and the Phase 00 PRD.

### Environment Requirements

- Linux development environment.
- Python virtual environment for `apex-infinite-cli/`.
- `PySide6` available through `apex-infinite-cli/requirements-wrapper.txt`.
- `QT_QPA_PLATFORM=offscreen` or a graphical display for wrapper smoke tests.
- No provider API keys or live Codex execution required for unit tests; dry-run
  and fixture event streams are sufficient for the spike.

---

## 4. Scope

### In Scope (MVP)

- Operator can launch or display an Apex Infinite session through
  `--event-stream - --machine-output` using an isolated wrapper launch helper.
- Future wrapper developer can inspect a PySide6/QML prototype with read-only
  log viewport, status panels, theme selector, effect intensity or toggles, and
  low-effects fallback behavior.
- Maintainer can run tests that validate event parsing, malformed-event error
  mapping, launcher args, subprocess cleanup expectations, and stdout JSONL
  isolation without a real LLM or Codex subprocess.
- Maintainer can read a spike decision record covering PySide6/QML,
  pywebview plus xterm.js backup, AppImage/Nuitka risks, LGPLv3/commercial
  obligations, empty qmltermwidget placeholder, and clean-room evidence.

### Out Of Scope (Deferred)

- Productizing the wrapper for release - Reason: Session 07 owns accepted
  prototype hardening, packaging, release artifacts, and smoke coverage.
- Building a true terminal emulator or pseudo-terminal viewport - Reason: The
  selected path is event-driven read-only workflow state.
- Adding PySide6, QML, or graphical imports to the base CLI runtime path -
  Reason: The base CLI must stay lightweight and headless-safe.
- Copying QML, shader code, assets, fonts, profiles, icons, resource manifests,
  build scripts, terminal-emulator code, or effect formulas from reference
  material - Reason: Clean-room and license boundaries forbid it.
- Supporting macOS or Windows wrapper builds - Reason: The phase scope is
  Linux-only.

---

## 5. Technical Approach

### Architecture

Create a new optional package at `apex-infinite-cli/apex_infinite_visual/`.
The package is importable only when wrapper code is explicitly invoked. It
contains a JSONL event adapter, a CLI subprocess launcher, and a PySide6/QML
entrypoint. The base CLI continues to own prompts, manager routing, Codex
execution, SQLite history, machine-output mode, event emission, and human
terminal rendering.

The launcher builds a subprocess command for the existing `apex_infinite.py`
entrypoint with `--event-stream - --machine-output`, captures stdout as JSONL,
and keeps stderr separate for wrapper failure display. The event adapter parses
one line at a time, validates the event version and required fields, maps known
events to simple view-model records, and reports malformed lines as explicit
wrapper errors instead of crashing the UI.

The QML surface is independently designed. It uses local QML controls and
simple visual effects to validate read-only log display, status hierarchy,
theme selection, glow/scanline/flicker/curvature feasibility, and reduced
effects. It must not import, copy, or transcribe reference QML, shaders,
assets, profile values, or terminal-widget behavior.

### Design Patterns

- Optional package boundary: Keeps graphical imports and runtime dependencies
  out of normal CLI execution.
- Event adapter: Converts raw lifecycle JSONL into wrapper state without
  parsing terminal output or SQLite rows.
- Subprocess command builder: Makes stdout JSONL guardrails testable without
  launching a live autonomous run.
- Import guard: Fails clearly when PySide6 or a display backend is unavailable
  while preserving base CLI operation.
- Clean-room QML prototype: Uses independent names, colors, layouts, controls,
  and effects.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/apex_infinite_visual/__init__.py` | Optional wrapper package metadata and public exports | ~25 |
| `apex-infinite-cli/apex_infinite_visual/events.py` | JSONL event parser, event-state adapter, and malformed-event error mapping | ~180 |
| `apex-infinite-cli/apex_infinite_visual/launcher.py` | CLI subprocess command builder and launch/cleanup helpers for machine-output JSONL | ~170 |
| `apex-infinite-cli/apex_infinite_visual/main.py` | PySide6 entrypoint, import guard, bridge model, and wrapper startup flow | ~280 |
| `apex-infinite-cli/apex_infinite_visual/qml/Main.qml` | Independent QML prototype surface with log viewport, status panels, controls, and effects | ~280 |
| `apex-infinite-cli/tests/test_visual_wrapper_spike.py` | Unit tests for event adapter, launcher args, import guard, and fixture event flow | ~240 |
| `apex-infinite-cli/docs/visual-wrapper-spike.md` | Spike evidence, dependency/license assessment, packaging risks, and decision record | ~220 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/README_apex-infinite-cli.md` | Add optional wrapper prototype run notes and link to spike evidence | ~35 |
| `apex-infinite-cli/docs/visual-wrapper-boundary.md` | Link the spike evidence and record confirmed prototype boundary decisions | ~35 |
| `apex-infinite-cli/docs/operator-runbook.md` | Add operator-facing notes for optional wrapper spike usage and fallbacks | ~35 |
| `apex-infinite-cli/docs/troubleshooting.md` | Add wrapper spike failure modes for missing PySide6, display backend, malformed JSONL, and subprocess failures | ~35 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] Wrapper prototype launches or displays fixture and dry-run Apex Infinite
      events through the JSONL event boundary without scraping terminal output.
- [ ] Prototype surface contains a read-only event log, current status panels,
      theme selection, reduced-effects handling, and simple effect toggles.
- [ ] Launcher builds guarded `--event-stream - --machine-output` commands and
      separates stdout JSONL from stderr or human text.
- [ ] Event adapter accepts current event stream objects and maps malformed or
      unsupported input to explicit wrapper error state.
- [ ] Spike document records whether PySide6/QML is accepted for Session 07 or
      names the exact blocker and reopen criteria.

### Testing Requirements

- [ ] Unit tests cover event parsing, event ordering, malformed JSON,
      unsupported event version, launcher command construction, stdout guard,
      and optional dependency failure paths.
- [ ] Offscreen or display-backed wrapper smoke test completed, or the exact
      environment blocker is recorded in `visual-wrapper-spike.md`.
- [ ] Existing CLI tests remain passing.

### Non-Functional Requirements

- [ ] Base CLI install path remains free of graphical runtime imports and
      dependencies.
- [ ] Wrapper code and docs contain no copied reference code, QML, shaders,
      assets, fonts, profile data, resource manifests, build scripts, terminal
      emulator code, or literal effect formulas.
- [ ] Event payloads and wrapper logs exclude provider API keys, ANSI escapes,
      Rich markup, frame glyphs, and visual-token storage.
- [ ] QML and wrapper Python files are ASCII-only with Unix LF line endings.

### Quality Gates

- [ ] All files ASCII-encoded
- [ ] Unix LF line endings
- [ ] Code follows project conventions
- [ ] Primary user-facing wrapper surface contains product-facing copy only
- [ ] Diagnostics remain in tests, docs, logs, or explicit failure surfaces

---

## 8. Implementation Notes

### Working Assumptions

- PySide6 is available in the current `apex-infinite-cli/.venv`; the plan still
  requires optional import guards and offscreen/display fallback handling
  because wrapper dependencies must never be required for normal CLI use.
- Wrapper code belongs under `apex-infinite-cli/apex_infinite_visual/` even
  though the repository is not configured as a formal monorepo; the PRD,
  conventions, and state all identify `apex-infinite-cli/` as the active
  project area.
- A read-only event log is sufficient for the spike; neither the PRD nor the
  Session 06 stub requires an interactive terminal emulator, and the selected
  path explicitly excludes pseudo-terminal and terminal-widget behavior.

### Conflict Resolutions

- The UX PRD refers to the Linux wrapper as a future Phase 01 optional visual
  mode, while current Phase 00 PRD, state, and session stubs place the wrapper
  spike and productization in Sessions 06 and 07 of Phase 00. The current phase
  artifacts and analyzer state win, so this session performs the Phase 00
  spike while leaving release productization to Session 07.
- Current README text calls the wrapper future work, while Session 06 is now
  selected. The chosen interpretation is that future work means "not
  productized"; a prototype spike can proceed and then update docs with its
  evidence.

### Key Considerations

- Keep graphical imports lazy and wrapper-only.
- Use current event names and machine-output guardrails instead of adding a
  second machine interface.
- Make missing dependency, display backend, malformed event, non-zero
  subprocess exit, timeout, and stderr states visible in the wrapper.
- Keep visual effects low-risk and independently implemented.

### Potential Challenges

- PySide6 or Qt display backend may fail in headless environments: Provide
  import/display failure messages, non-GUI tests, and offscreen smoke coverage
  where available.
- QML prototype could grow into productization scope: Keep the deliverable a
  feasibility surface and record hardening work for Session 07.
- Clean-room risk can be hard to audit after the fact: Record allowed concepts,
  forbidden categories, and reference non-dependence in the spike decision
  record.

### Relevant Considerations

- [P00] **Event stream is the wrapper contract**: The wrapper must consume
  JSONL events or the importable API, not Rich frames or human terminal output.
- [P01] **Wrapper as companion surface**: The wrapper displays the same
  workflow engine state and must not fork manager decisions, routing, storage,
  or safety behavior.
- [P01] **Optional wrapper obligations**: PySide6/Qt Quick/QML must remain
  optional, with LGPLv3/commercial obligations and packaging notes documented.
- [P01] **Terminal-widget exclusions**: PyQt, qmltermwidget, QTermWidget,
  copied terminal-emulator code, and embedded pseudo-terminal behavior remain
  out of scope.
- [P00] **Clean-room visual translation**: Use concepts only; do not copy
  reference code, shader constants, assets, fonts, profiles, manifests, or
  build scripts.

### Behavioral Quality Focus

Checklist active: Yes
Top behavioral risks for this session:

- Wrapper subprocesses can outlive the UI or leave pipes/temp files open unless
  cleanup is explicit.
- Malformed JSONL or unexpected event payloads can crash the wrapper unless
  parsing and error mapping are defensive.
- Missing PySide6, missing display backend, non-zero subprocess exits, and
  stderr-only failures can look like blank UI unless failure states are
  product-visible.
- Theme/effect controls can become visual-only diagnostics unless they have
  accessible labels, focus behavior, and reduced-effects fallbacks.

---

## 9. Testing Strategy

### Unit Tests

- Test JSONL parsing for valid current events, unsupported event versions,
  malformed JSON, missing fields, unexpected payload types, and bounded log
  ordering in `apex-infinite-cli/tests/test_visual_wrapper_spike.py`.
- Test launcher command construction includes `--event-stream -`,
  `--machine-output`, project path, optional start command, optional dry-run,
  and max iteration arguments without launching a real subprocess.
- Test optional PySide6 import guard or wrapper bootstrap failure mapping with
  monkeypatched imports where feasible.

### Integration Tests

- Run `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`.
- Run an offscreen wrapper smoke command with fixture events or dry-run mode if
  the Qt backend supports it.
- Confirm `python apex_infinite.py --event-stream - --machine-output
  --dry-run --max-iterations 1` still emits JSONL-only stdout in existing
  event tests.

### Runtime Verification

- Start the wrapper with a temporary project path and dry-run settings.
- Confirm the log viewport receives startup, UI, prompt, dry-run, DB, and stop
  events.
- Toggle theme and reduced-effects controls and confirm status/log text remains
  readable.
- Force malformed event input and confirm the wrapper shows an explicit error
  state.

### Edge Cases

- PySide6 missing.
- Qt display backend unavailable.
- Event stream emits an unknown compatibility event.
- Subprocess exits non-zero or writes stderr-only output.
- JSONL stream closes mid-event.
- Long project path, long manager reason, and long response summary.
- `NO_COLOR`, plain mode, and machine-output stdout isolation remain separate
  from wrapper display state.

---

## 10. Dependencies

### Other Sessions

- Depends on:
  `phase00-session01-config-and-renderer-boundary`,
  `phase00-session02-rich-operator-console`,
  `phase00-session03-subprocess-and-history-visibility`,
  `phase00-session04-event-stream-boundary`,
  `phase00-session05-docs-samples-and-runbooks`
- Depended by: `phase00-session07-linux-visual-wrapper-productization`

---

## Next Steps

Run the `implement` workflow step to begin implementation.
