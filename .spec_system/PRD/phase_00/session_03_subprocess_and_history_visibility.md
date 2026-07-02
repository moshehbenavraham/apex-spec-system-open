# Session 03: Subprocess And History Visibility

**Session ID**: `phase00-session03-subprocess-and-history-visibility`
**Status**: Not Started
**Estimated Tasks**: ~12-25
**Estimated Duration**: 2-4 hours

---

## Objective

Improve operator awareness during long Codex subprocess runs while preserving
captured-output semantics and history compatibility.

---

## Scope

### In Scope (MVP)

- Add live elapsed subprocess display using Rich status, progress, live
  rendering, or an equivalent renderer wrapper.
- If replacing `subprocess.run()` with `subprocess.Popen`, preserve stdout and
  stderr capture, timeout text, return-code handling, stderr fallback,
  `FileNotFoundError`, and generic exception reporting.
- Show command timeout, elapsed time, and process state during `codex exec`.
- Redesign `--history` as a compact ledger with command, reason, timestamp,
  status, and truncated response summary.
- Extend the existing `--verbose` flag to history mode for expanded row detail.
- Add fake-runner or monkeypatch tests for success, stderr-only output,
  non-zero exit, timeout, dry-run, missing binary, and generic exception paths.

### Out of Scope

- Renaming or migrating the legacy SQLite `cc_response` column.
- Adding a mode-specific `--history-verbose` flag.
- Public event-stream implementation or graphical wrapper work.

---

## Prerequisites

- [ ] Session 01 validated.
- [ ] Session 02 render labels are available or equivalent semantic labels are
  defined.
- [ ] Current subprocess and history behavior is covered by focused tests before
  behavior-preserving rewrites.

---

## Deliverables

1. Live subprocess status display that does not leak styled output into
   durable records.
2. Backward-compatible compact and verbose history rendering.
3. Subprocess and history tests for success, failure, timeout, dry-run, and
   missing-binary cases.

---

## Success Criteria

- [ ] Operators can tell whether Codex is running and how long it has been
  running.
- [ ] Captured stdout, stderr, exit code, timeout, and verbose behavior remain
  compatible with the current CLI.
- [ ] History mode is usable without horizontal scrolling.
- [ ] Styled output never becomes part of stored history rows.

---

## Folded Source Plan Details

<!-- FOLDED_SESSION_SOURCE_START -->

This section carries forward the actionable session material formerly stored in
`docs/ongoing-projects/apex-infinite-cli-upgrade-plan.md`. The Phase 00 PRD
contains the verbatim archive; this stub keeps the session-specific details and
full-path `EXAMPLE/` references close to the session executor.

### EXAMPLE Reference Links

- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/FullContextMenu.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/FullContextMenu.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/ShortContextMenu.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/ShortContextMenu.qml)
- [/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/WindowMenu.qml](/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/WindowMenu.qml)

### Detailed Session Split Source

`````markdown
### Session 03: Subprocess And History Visibility

**Objective**: Improve operator awareness during long Codex subprocess runs while preserving captured-output semantics.

**Scope**:
- Add live elapsed subprocess display using Rich status, progress, live rendering, or an equivalent wrapper.
- If moving from `subprocess.run()` to `subprocess.Popen`, preserve
  stdout/stderr capture, timeout text, return-code handling, stderr fallback,
  `FileNotFoundError`, and generic exception reporting.
- Show command timeout, elapsed time, and process state during `codex exec`.
- Redesign `--history` as a compact ledger with command, reason, timestamp, status, and truncated response summary.
- Extend the existing `--verbose` flag to history mode instead of adding
  `--history-verbose`; verbose history shows larger response/reason detail
  while default history stays compact.
- Add fake-runner or monkeypatch tests for success, stderr-only output,
  non-zero exit, timeout, dry-run, missing binary, and generic exceptions.

**Outputs**:
- Live subprocess status display that does not leak styled output into history.
- Backward-compatible history rendering for empty, short, and long records.
- Tests for subprocess display and history formatting.

**Dependencies / Notes**:
- Depends on Session 01 renderer boundaries and should use Session 02 labels where available.
- Existing `~/.apex-infinite/history.db` files must remain readable without migration.
- The legacy `cc_response` column must not be renamed.
- Preserve current `--verbose` behavior for normal execution while making it
  useful for history output.

**EXAMPLE Reference Paths**:
- Study command-line argument handling and process launch concepts for wrapper
  parity only:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/main.cpp`
- Study session start/finish, terminal source updates, copy/paste, focus,
  resize, and mouse/wheel event handling as a checklist for subprocess status
  and failure visibility:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`
- Study tab lifecycle and session-finished handling:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml`
- Study operator actions and failure-visible window controls:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`
- Study terminal-size overlay concepts for narrow history/status displays:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml`
- Study menu placement for copy, paste, settings, profile, fullscreen, zoom,
  and new tab actions:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/FullContextMenu.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/ShortContextMenu.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/WindowMenu.qml`

**Acceptance Checks**:
- Operators can tell whether Codex is running and how long it has been running.
- Captured stdout, stderr, exit code, timeout, and verbose behavior remain compatible with the current CLI.
- History mode is usable without horizontal scrolling.
- Styled output never becomes part of stored history rows.
`````

### Mapped Rough Implementation Source

`````markdown
### Session 3: Live Execution And Better History

Objective: improve operator awareness during long-running Codex subprocesses.

Tasks:

- Use `rich.status.Status`, `rich.progress`, or `rich.live.Live` for elapsed
  subprocess display while stdout is captured.
- If replacing `subprocess.run()` with `subprocess.Popen`, preserve current
  behavior for stdout/stderr capture, stderr fallback when stdout is empty,
  non-zero exit wrapping, timeout text, `FileNotFoundError`, and generic
  exception reporting.
- Show command timeout, elapsed time, and process state during `codex exec`.
- Redesign `--history` as a compact ledger with command, reason, timestamp,
  status, and truncated response summary.
- Make existing `--verbose` meaningful in history mode by expanding response
  and reason detail; do not add `--history-verbose`.
- Keep the SQLite schema backward compatible.
- Add tests for history formatting with empty, short, and long records.
- Add tests for subprocess success, stderr-only output, non-zero exit, timeout,
  dry-run, and missing binary with a fake command runner or monkeypatch.

Acceptance:

- Operators can tell whether Codex is still running and how long it has been
  running.
- History mode is useful on a normal terminal without horizontal scrolling.
- Existing `~/.apex-infinite/history.db` files remain readable.
- Existing `--verbose` behavior for normal execution remains at least as
  informative as today.
`````

<!-- FOLDED_SESSION_SOURCE_END -->
