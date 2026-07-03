# Session 04: Event Stream Boundary

**Session ID**: `phase00-session04-event-stream-boundary`
**Status**: Complete
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Create the minimum stable machine-readable lifecycle boundary needed by future
renderers and wrappers.

---

## Scope

### In Scope (MVP)

- Separate config loading, DB access, LLM calls, manager decisions, prompt
  building, Codex execution, notification, and rendering as much as practical.
- Promote the internal lifecycle snapshot into a documented event design for
  wrappers.
- Implement `--event-stream PATH` as a line-buffered JSONL file while leaving
  normal human stdout unchanged.
- Guard `--event-stream -` behind explicit human-output disablement so JSONL
  never mixes with Rich or plain human output.
- Expose the same event emitter as an importable Python API for tests and
  future wrappers.
- Add event names for iteration lifecycle, manager decisions, prompt dispatch,
  subprocess lifecycle, output summary, DB logging, help, completion, timeout,
  interrupts, and errors.
- Add dry-run tests for event order, event names, payload stability, file
  flushing, stdout collision prevention, and no real LLM or Codex calls.

### Out of Scope

- Productizing a graphical wrapper.
- Scraping Rich frames or human terminal output for machine state.
- Changing manager prompt routing or SQLite compatibility for event-only needs.

---

## Prerequisites

- [x] Sessions 01 through 03 validated.
- [x] Renderer lifecycle labels and subprocess facts are available.
- [x] Security findings about raw payloads and stdout isolation are reviewed.

---

## Deliverables

1. Documented lifecycle event interface and importable emitter API.
2. `--event-stream PATH` JSONL support with guarded stdout behavior.
3. Event tests proving order, names, raw payloads, flushing, and stdout
   isolation.

---

## Success Criteria

- [x] Rich output and future wrappers can consume the same lifecycle facts.
- [x] A future wrapper can observe state without scraping terminal frames.
- [x] Prompt routing, autonomous handoffs, and SQLite compatibility remain
  unchanged.
- [x] Event payloads contain raw operational facts with no Rich markup, ANSI
  escapes, frame glyphs, copied visual tokens, or secrets.

---

## Folded Source Plan Details

<!-- FOLDED_SESSION_SOURCE_START -->

This section carries forward the actionable session material formerly stored in
`docs/ongoing-projects/apex-infinite-cli-upgrade-plan.md`. The Phase 00 PRD
contains the verbatim archive; this stub keeps the session-specific details and
full-path `EXAMPLE/` references close to the session executor.

### EXAMPLE Reference Links

- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules)

### Detailed Session Split Source

`````markdown
### Session 04: Event Stream Boundary

**Objective**: Create the minimum stable machine-readable lifecycle boundary
needed by future renderers and wrappers.

**Scope**:
- Separate config loading, DB access, LLM calls, manager decisions, prompt
  building, Codex execution, notification, and rendering as much as practical.
- Promote the internal lifecycle snapshot from Session 01 into a documented
  event design for wrappers.
- Implement `--event-stream PATH` as a line-buffered JSONL file while leaving
  normal human stdout unchanged.
- Define the exact human-rendering disable mechanism needed for
  `--event-stream -`; expected implementation is an explicit machine-output
  mode unless an existing flag already guarantees silent human rendering.
- Expose the same event emitter as an importable Python API for tests and
  future wrappers.
- Add event names for iteration lifecycle, manager decisions, prompt dispatch,
  subprocess lifecycle, output summary, DB logging, help, completion, timeout,
  interrupts, and errors.
- Ensure event payloads contain raw operational facts and no Rich markup,
  ANSI escapes, frame glyphs, or reference-derived visual tokens.
- Add dry-run tests for event order, event names, payload stability, file
  flushing, stdout collision prevention, and no real LLM/Codex calls.

**Outputs**:
- Documented lifecycle event interface and importable emitter API.
- `--event-stream PATH` JSONL support, plus guarded stdout JSONL behavior.
- Event tests that verify ordering, names, raw payloads, and stdout isolation.

**Dependencies / Notes**:
- Depends on Sessions 01 through 03 for renderer and subprocess lifecycle
  facts.
- Normal human CLI output remains the default behavior.
- The event stream is the contract future wrappers consume; wrappers must not
  scrape Rich frames or parse human terminal output.
- Open question captured for implementation: whether the silent human-output
  guard is named `--no-human-output`, `--machine-output`, or an equivalent
  internal mode.

**EXAMPLE Reference Paths**:
- Study root application and window creation flow for lifecycle event grouping:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml`
- Study root C++ to QML wiring, arguments, application metadata, and import
  paths:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp`
- Study application-wide settings as the event/context model checklist:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`
- Study lifecycle flow from window to tabs to terminal surface:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`
- Study render-stage separation for event names, not implementation:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml`
- Study persisted settings and file import/export boundaries for event payload
  stability:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h`
- Study submodule declarations only to confirm what not to depend on:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/.gitmodules`

**Acceptance Checks**:
- Rich output and future wrappers can consume the same lifecycle facts.
- A future wrapper can observe state without scraping terminal frames.
- Prompt routing, autonomous handoffs, and SQLite compatibility remain unchanged.
- `--event-stream -` cannot mix JSONL with Rich or plain human output.
`````

### Mapped Rough Implementation Source

The rough implementation plan numbered this as Session 5 because an earlier ordering placed documentation before the event stream. Phase 00 now keeps the event boundary before documentation so docs describe implemented behavior.

`````markdown
### Session 5: Engine Boundary And Event Stream

Objective: create the minimum stable boundary needed by future visual surfaces
without productizing a graphical wrapper yet.

Tasks:

- Separate, as much as practical, config loading, DB access, LLM calls, manager
  decisions, prompt building, Codex execution, notification, and rendering.
  This can be module-level functions first; do not force a large class rewrite
  unless it reduces risk.
- Turn the internal display-event shape from Session 1 into a documented
  wrapper-facing event stream design.
- Implement the machine interface as `--event-stream PATH`, writing
  line-buffered JSONL events to a file while leaving normal human stdout
  unchanged.
- Support `--event-stream -` only with human rendering disabled, so JSONL is
  never mixed with Rich output.
- Expose the same event emitter as an importable Python API for tests and
  future wrappers.
- Add event names for iteration lifecycle, manager decisions, prompt dispatch,
  subprocess lifecycle, output summary, DB logging, help, completion, timeout,
  and errors.
- Ensure event payloads contain raw operational facts, not Rich markup or
  reference-derived visual tokens.
- Add dry-run tests that verify event ordering and payload stability without
  making real LLM or Codex calls.

Acceptance:

- The Rich renderer can consume the same lifecycle facts that a future wrapper
  would need.
- Existing human CLI output remains the default.
- A future wrapper has a documented JSONL/API way to observe state without
  scraping terminal frames.
- Prompt routing and SQLite compatibility remain unchanged.
`````

<!-- FOLDED_SESSION_SOURCE_END -->
