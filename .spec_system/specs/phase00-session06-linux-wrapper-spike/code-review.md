# Code Review and Repair Report

**Session ID**: `phase00-session06-linux-wrapper-spike`
**Reviewed**: 2026-07-03
**Scope**: All uncommitted changes in the working tree
**Result**: RESOLVED

## Review Surface

**Files reviewed** (all uncommitted changes):
- `.spec_system/state.json` - tracked-modified
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/spec.md` - untracked
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - untracked
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - untracked
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/code-review.md` - untracked, this report
- `apex-infinite-cli/README_apex-infinite-cli.md` - tracked-modified
- `apex-infinite-cli/apex_infinite_visual/__init__.py` - untracked
- `apex-infinite-cli/apex_infinite_visual/events.py` - untracked
- `apex-infinite-cli/apex_infinite_visual/launcher.py` - untracked
- `apex-infinite-cli/apex_infinite_visual/main.py` - untracked
- `apex-infinite-cli/apex_infinite_visual/qml/Main.qml` - untracked
- `apex-infinite-cli/tests/test_visual_wrapper_spike.py` - untracked
- `apex-infinite-cli/docs/operator-runbook.md` - tracked-modified
- `apex-infinite-cli/docs/troubleshooting.md` - tracked-modified
- `apex-infinite-cli/docs/visual-wrapper-boundary.md` - tracked-modified
- `apex-infinite-cli/docs/visual-wrapper-spike.md` - untracked

**Inventory commands**: `git status`, `git diff HEAD`, `git diff --cached`,
`git ls-files --others --exclude-standard`

## Findings by Severity

### Critical

No findings.

### High

No findings.

### Medium

- `apex-infinite-cli/apex_infinite_visual/launcher.py:88` - `terminate()`
  used `communicate()` during cleanup while the wrapper worker can be reading
  stdout as a stream. That creates competing pipe consumers and can drop or
  block stream cleanup. | Fix: changed cleanup to `wait()` after terminate and
  kill, leaving pipe ownership with the streaming worker. | Status: FIXED
- `apex-infinite-cli/apex_infinite_visual/main.py:334` - the real CLI worker
  drained stderr only after stdout closed and the process was waited on. A
  subprocess that writes enough stderr could block before stdout closes. | Fix:
  added a dedicated stderr reader thread before stdout iteration and joined it
  after process exit. | Status: FIXED
- `apex-infinite-cli/apex_infinite_visual/main.py:230` - operator Stop could be
  overwritten by a later non-zero terminated-process return code, showing a
  failure state for an intentional stop. | Fix: added `_stop_requested` and
  suppress stderr/return-code error mapping after an intentional stop. | Status:
  FIXED

### Low

- `apex-infinite-cli/apex_infinite_visual/main.py:309` - a new run reused the
  prior adapter snapshot until the first new event arrived, so an old error or
  log could remain visible briefly on re-entry. | Fix: reset the adapter,
  snapshot, and log before fixture or subprocess startup. | Status: FIXED
- `apex-infinite-cli/apex_infinite_visual/qml/Main.qml:286` - layout-managed
  separator rectangles used `height`, which `pyside6-qmllint` reports as
  undefined behavior in layouts. | Fix: replaced separator `height` with
  `Layout.preferredHeight`. | Status: FIXED
- `apex-infinite-cli/apex_infinite_visual/main.py:14` and wrapper modules -
  pylint surfaced one unused import plus intentional QML bridge and event-map
  shape warnings. | Fix: removed the unused import, changed the launcher
  iterator to `yield from`, and added targeted pylint disables for lazy Qt
  imports, QML camelCase slots, and mapping-table shape. | Status: FIXED

## Assumptions and Deliberate Non-Fixes

- `spec.md` still says `Status: Not Started`, while `tasks.md` and
  `implementation-notes.md` show 20/20 implementation tasks complete. I left
  `spec.md` unchanged because the session artifacts and analyzer state already
  identify this as the active implemented session, and status synchronization
  belongs to the later validation/updateprd workflow gates.
- `pyside6-qmllint` is not configured as a project gate and exits 0. I fixed
  the concrete layout undefined-behavior warnings. Remaining unqualified-access
  suggestions are informational style guidance, not observed runtime defects,
  and the offscreen QML smoke passes.
- The spike document's external license and packaging claims were checked
  against current official sources:
  `https://doc.qt.io/qtforpython-6/commercial/index.html`,
  `https://pypi.org/project/PySide6/`,
  `https://doc.qt.io/qtforpython-6/deployment/deployment-pyside6-deploy.html`,
  `https://nuitka.net/doc/download.html#license`, and
  `https://riverbankcomputing.com/commercial/license-faq`. No doc correction
  was required.

## Behavior Changes

- Operator Stop now remains a stopped state instead of being overwritten by a
  terminated-process error.
- Starting a new wrapper run clears stale status and log state immediately.
- Subprocess stderr is drained concurrently with stdout event consumption.
- Wrapper termination no longer consumes stdout/stderr pipes during cleanup.

## Verification

- Tests: `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v` -
  PASS - 189/189 passed.
- Focused tests: `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/test_visual_wrapper_spike.py -v` -
  PASS - 16/16 passed.
- Linter: `cd apex-infinite-cli && ./.venv/bin/python -m pylint apex_infinite.py apex_infinite_events.py apex_infinite_ui.py apex_infinite_visual` -
  PASS - 10.00/10.
- Formatter: `cd apex-infinite-cli && ./.venv/bin/python -m black --check apex_infinite_visual tests/test_visual_wrapper_spike.py` -
  PASS.
- Type checker: N/A - no Python type checker is configured for this project.
- Compile: `cd apex-infinite-cli && ./.venv/bin/python -m py_compile apex_infinite_visual/__init__.py apex_infinite_visual/events.py apex_infinite_visual/launcher.py apex_infinite_visual/main.py` -
  PASS.
- Wrapper smoke: `cd apex-infinite-cli && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300` -
  PASS.
- QML lint spot-check: `cd apex-infinite-cli && ./.venv/bin/pyside6-qmllint apex_infinite_visual/qml/Main.qml` -
  PASS exit 0; layout-positioning/error spot-check has no matches after fixes.
- Whitespace: `git diff --check` - PASS.
- ASCII/LF: changed and untracked review-surface files scanned with
  `grep -nP '[^\x00-\x7F]'` and CR checks - PASS.
- Source/package boundary: `git diff -- apex-infinite-cli/apex_infinite.py apex-infinite-cli/requirements.txt apex-infinite-cli/requirements-wrapper.txt` -
  PASS - no base CLI runtime or dependency boundary changes.
- Final diff re-read: no remaining code-review findings.

## Summary

1. Reviewed 16 uncommitted files covering session specs, optional wrapper
   package, QML surface, tests, docs, and state.
2. Findings: 0 critical, 0 high, 3 medium, 3 low; all resolved.
3. Deliberate non-fixes: `spec.md` status left for later workflow gates;
   remaining QML unqualified-access lint suggestions are informational and not
   a configured project gate.
4. Verification passed: full pytest, focused wrapper tests, pylint, black
   check, py_compile, offscreen wrapper smoke, QML layout spot-check,
   whitespace, ASCII/LF, and source boundary checks.
