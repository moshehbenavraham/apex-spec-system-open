# Implementation Notes

**Session ID**: `phase00-session06-linux-wrapper-spike`
**Started**: 2026-07-03 04:22
**Last Updated**: 2026-07-03 05:39

---

## Session Progress

| Metric | Value |
|--------|-------|
| Tasks Completed | 20 / 20 |
| Estimated Remaining | 0 minutes |
| Blockers | 0 |

---

## Task Log

### 2026-07-03 - Session Start

**Environment verified**:
- [x] Prerequisites confirmed
- [x] Tools available
- [x] Directory structure ready

---

### Task T001 - Verify analyzer state and wrapper prerequisites

**Started**: 2026-07-03 04:21
**Completed**: 2026-07-03 04:22
**Duration**: 1 minute

**Notes**:
- Verified the spec-system analyzer selects `phase00-session06-linux-wrapper-spike`.
- Confirmed Sessions 01 through 05 are validated and Session 05 validation is PASS.
- Confirmed PySide6 is isolated in `requirements-wrapper.txt` and imports from the CLI virtualenv.

**Files Changed**:
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - created progress log.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `bash .spec_system/scripts/analyze-project.sh --json`
  - Result: PASS - analyzer reports current session `phase00-session06-linux-wrapper-spike`, Sessions 01-05 completed, monorepo false.
  - Evidence: JSON output recorded `completed_sessions_count: 5` and current session directory present.
- Command/check: `bash .spec_system/scripts/check-prereqs.sh --json --env`
  - Result: PASS - spec-system, jq, and git prerequisites available.
  - Evidence: JSON output recorded `overall: pass`.
- Command/check: `sed -n '1,220p' .spec_system/specs/phase00-session05-docs-samples-and-runbooks/validation.md`
  - Result: PASS - prior session validation result is PASS with 234/234 tests passing.
  - Evidence: validation report says `Result: PASS`.
- Command/check: `sed -n '1,220p' apex-infinite-cli/requirements-wrapper.txt`
  - Result: PASS - PySide6 and Nuitka are listed only in the optional wrapper requirements file.
  - Evidence: file describes optional Linux visual wrapper dependencies.
- Command/check: `apex-infinite-cli/.venv/bin/python - <<'PY' ... import PySide6 ... PY`
  - Result: PASS - PySide6 imports successfully.
  - Evidence: command printed `PySide6 OK 6.11.1`.
- UI product-surface check: N/A - setup verification only.
- UI craft check: N/A - setup verification only.

**BQC Fixes**: None.

---

## Final Verification Summary

- Tasks completed: 20 / 20.
- Focused wrapper tests: 13 / 13 passed.
- Full CLI pytest suite: 186 / 186 passed.
- Offscreen wrapper smoke: PASS.
- ASCII/LF check: PASS.
- Whitespace check: PASS.
- Clean-room wrapper source scan: PASS.
- Base CLI dependency boundary: PASS.
- Remaining blockers: none.

---

### Task T020 - Verify ASCII, no-copy hygiene, whitespace, and dependency boundary

**Started**: 2026-07-03 05:28
**Completed**: 2026-07-03 05:39
**Duration**: 11 minutes

**Notes**:
- Formatted the new wrapper Python files and focused tests with Black.
- Re-ran full tests and offscreen smoke after formatting.
- Verified changed files are ASCII/LF, whitespace-clean, and do not track `EXAMPLE/` material.
- Verified base CLI entrypoint and base dependency files remain unchanged.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_visual/__init__.py` - Black formatting.
- `apex-infinite-cli/apex_infinite_visual/events.py` - Black formatting.
- `apex-infinite-cli/apex_infinite_visual/launcher.py` - Black formatting.
- `apex-infinite-cli/apex_infinite_visual/main.py` - Black formatting.
- `apex-infinite-cli/tests/test_visual_wrapper_spike.py` - Black formatting.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged final hygiene evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m black apex_infinite_visual tests/test_visual_wrapper_spike.py`
  - Result: PASS - formatter completed successfully.
  - Evidence: Black reformatted five new Python files.
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`
  - Result: PASS - full CLI test suite passes after formatting.
  - Evidence: 186/186 tests passed in 10.69s.
- Command/check: `cd apex-infinite-cli && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1`
  - Result: PASS - offscreen wrapper smoke passes after formatting.
  - Evidence: command exited 0 with no output.
- Command/check: `files=$( { git diff --name-only --diff-filter=ACM HEAD; git ls-files --others --exclude-standard; } | sort -u ); if [ -n "$files" ]; then LC_ALL=C grep -nP '[^\\x00-\\x7F]' $files || true; grep -n $'\\r' $files || true; fi`
  - Result: PASS - changed and untracked files are ASCII-only with LF line endings.
  - Evidence: command produced no matches.
- Command/check: `git diff --check`
  - Result: PASS - no whitespace errors.
  - Evidence: command exited 0.
- Command/check: `git ls-files | rg '^EXAMPLE/' || true`
  - Result: PASS - no tracked `EXAMPLE/` files.
  - Evidence: command produced no matches.
- Command/check: `rg -n 'cool-retro-term|TerminalWindow|ShaderTerminal|BurnInEffect|resources\\.qrc|qmltermwidget|QTermWidget|EXAMPLE/' apex-infinite-cli/apex_infinite_visual || true`
  - Result: PASS - wrapper source contains no copied-reference markers.
  - Evidence: command produced no matches.
- Command/check: `git diff -- apex-infinite-cli/apex_infinite.py apex-infinite-cli/requirements.txt apex-infinite-cli/requirements-wrapper.txt`
  - Result: PASS - base CLI runtime and dependency boundary unchanged.
  - Evidence: command produced no diff.
- UI product-surface check: PASS - offscreen smoke loads the wrapper console without implementation diagnostics or scaffolding copy.
- UI craft check: PASS - final QML retains status hierarchy, log priority, accessible controls, and reduced-effects fallback.

**BQC Fixes**: None.

---

### Task T019 - Run offscreen wrapper smoke check

**Started**: 2026-07-03 05:27
**Completed**: 2026-07-03 05:28
**Duration**: 1 minute

**Notes**:
- Ran the exact task-list offscreen smoke command against fixture-backed dry-run events.
- No PySide6 or display blocker remains for the spike environment.

**Files Changed**:
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged smoke evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `cd apex-infinite-cli && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1`
  - Result: PASS - wrapper starts, loads QML, plays dry-run fixture events, auto-closes in offscreen mode, and exits cleanly.
  - Evidence: command exited 0 with no output.
- UI product-surface check: PASS - offscreen QML smoke loaded the wrapper console without debug/runtime/scaffolding copy.
- UI craft check: PASS - offscreen smoke exercised the normal QML surface, status/log panels, controls, and reduced offscreen backend path.

**BQC Fixes**: None.

---

### Task T018 - Run full CLI pytest suite

**Started**: 2026-07-03 05:14
**Completed**: 2026-07-03 05:26
**Duration**: 12 minutes

**Notes**:
- Ran the full CLI pytest suite after adding wrapper package, docs, and focused tests.

**Files Changed**:
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged test evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`
  - Result: PASS - full CLI test suite passes.
  - Evidence: 186/186 tests passed in 10.71s.
- BQC check: regression coverage for prompt, renderer, history, subprocess, event-stream, and wrapper behavior.
  - Result: PASS - full test suite includes existing CLI contracts and 13 new wrapper spike tests.
  - Evidence: pytest output includes `tests/test_visual_wrapper_spike.py` and all existing suites.
- UI product-surface check: N/A - automated test run only.
- UI craft check: N/A - automated test run only.

**BQC Fixes**: None.

---

### Task T017 - Write focused wrapper spike tests

**Started**: 2026-07-03 05:07
**Completed**: 2026-07-03 05:14
**Duration**: 7 minutes

**Notes**:
- Added focused tests for valid event parsing, malformed JSON, unsupported versions, unsafe payload values, bounded adapter logs, fixture event flow, launcher command construction, stdout guardrails, process cleanup, parse defaults, PySide6 import guard behavior, and package import boundary.

**Files Changed**:
- `apex-infinite-cli/tests/test_visual_wrapper_spike.py` - added 13 focused wrapper spike tests.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/test_visual_wrapper_spike.py -v`
  - Result: PASS - focused wrapper spike tests pass.
  - Evidence: 13/13 tests passed in 0.03s.
- BQC check: trust boundary enforcement, resource cleanup, duplicate/stdout guard alignment, external dependency resilience, and contract alignment.
  - Result: PASS - tests cover parser rejection, adapter recovery, launcher guardrails, cleanup, fixture flow, and PySide6 import guard.
  - Evidence: `tests/test_visual_wrapper_spike.py` assertions cover each boundary.
- UI product-surface check: N/A - automated non-render tests only.
- UI craft check: N/A - automated non-render tests only.

**BQC Fixes**: None.

---

### Task T016 - Update boundary and troubleshooting docs

**Started**: 2026-07-03 05:04
**Completed**: 2026-07-03 05:07
**Duration**: 3 minutes

**Notes**:
- Updated the visual wrapper boundary with confirmed prototype constraints and spike evidence link.
- Added troubleshooting entries for missing PySide6, display backend failures, malformed JSONL, subprocess failures, and clean-room audit failures.

**Files Changed**:
- `apex-infinite-cli/docs/visual-wrapper-boundary.md` - added confirmed prototype constraints and spike link.
- `apex-infinite-cli/docs/troubleshooting.md` - added visual wrapper prototype failure modes and recovery steps.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `LC_ALL=C grep -nP '[^\\x00-\\x7F]' apex-infinite-cli/docs/visual-wrapper-boundary.md apex-infinite-cli/docs/troubleshooting.md || true`
  - Result: PASS - changed docs are ASCII-only.
  - Evidence: command produced no matches.
- Command/check: `rg -n "Confirmed Prototype Constraints|Visual wrapper spike|PySide6 imports|requirements.txt|malformed|stderr|non-zero|AppImage|Visual Wrapper Prototype Issues|PySide6 is not installed|display backend|Clean-room audit|--event-stream - --machine-output" apex-infinite-cli/docs/visual-wrapper-boundary.md apex-infinite-cli/docs/troubleshooting.md`
  - Result: PASS - required boundary and troubleshooting topics are present.
  - Evidence: matches cover constraints, missing dependency/display errors, malformed JSONL, subprocess failure, no-copy audit, and event boundary.
- UI product-surface check: N/A - documentation only.
- UI craft check: N/A - documentation only.

**BQC Fixes**: None.

---

### Task T015 - Update operator-facing wrapper docs

**Started**: 2026-07-03 05:00
**Completed**: 2026-07-03 05:04
**Duration**: 4 minutes

**Notes**:
- Updated README install and wrapper sections from deferred/future wording to the optional prototype path.
- Added fixture-backed and offscreen wrapper run commands.
- Added real subprocess launch notes, optional dependency boundary, fallback behavior, and spike record links to operator docs.

**Files Changed**:
- `apex-infinite-cli/README_apex-infinite-cli.md` - added visual wrapper prototype install/run instructions and spike link.
- `apex-infinite-cli/docs/operator-runbook.md` - added optional wrapper prototype operating mode and fallback behavior.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `LC_ALL=C grep -nP '[^\\x00-\\x7F]' apex-infinite-cli/README_apex-infinite-cli.md apex-infinite-cli/docs/operator-runbook.md || true`
  - Result: PASS - changed docs are ASCII-only.
  - Evidence: command produced no matches.
- Command/check: `rg -n "Visual Wrapper Prototype|visual-wrapper-spike|requirements-wrapper|python -m apex_infinite_visual.main|QT_QPA_PLATFORM=offscreen|--launch-cli|--event-stream - --machine-output|PySide6 is missing|malformed|subprocess" apex-infinite-cli/README_apex-infinite-cli.md apex-infinite-cli/docs/operator-runbook.md`
  - Result: PASS - required run path, optional dependency, fallback, and decision-record references are present.
  - Evidence: matches cover both docs.
- UI product-surface check: N/A - documentation only.
- UI craft check: N/A - documentation only.

**BQC Fixes**: None.

---

### Task T014 - Document spike evidence and dependency decision

**Started**: 2026-07-03 04:52
**Completed**: 2026-07-03 05:00
**Duration**: 8 minutes

**Notes**:
- Added the Session 06 spike decision record and evidence ledger.
- Recorded PySide6/QML acceptance for Session 07 with release compliance constraints.
- Documented dependency status, LGPLv3/commercial obligations, Nuitka and `pyside6-deploy` risks, qmltermwidget/QTermWidget exclusion, PyQt exclusion, and pywebview plus xterm.js backup criteria.
- Checked current official Qt/PySide6/Nuitka/Riverbank sources before writing the license and packaging notes.

**Files Changed**:
- `apex-infinite-cli/docs/visual-wrapper-spike.md` - added spike evidence, decision, dependency/license assessment, packaging risks, exclusions, and Session 07 recommendation.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `LC_ALL=C grep -nP '[^\\x00-\\x7F]' apex-infinite-cli/docs/visual-wrapper-spike.md || true`
  - Result: PASS - spike document is ASCII-only.
  - Evidence: command produced no matches.
- Command/check: `rg -n "Decision|PySide6|LGPL|Nuitka|qmltermwidget|QTermWidget|PyQt|pywebview|xterm|AppImage|offscreen|--event-stream - --machine-output" apex-infinite-cli/docs/visual-wrapper-spike.md`
  - Result: PASS - required decision and evidence topics are present.
  - Evidence: matches cover the accepted path, license obligations, packaging risks, exclusions, backup decision, and event boundary.
- Source check: official Qt for Python commercial use, PySide6 PyPI metadata, Qt `pyside6-deploy`, Nuitka license note, and Riverbank PyQt FAQ.
  - Result: PASS - document links to the checked sources and uses them for current licensing/package risk statements.
  - Evidence: source links are listed in `visual-wrapper-spike.md`.
- UI product-surface check: N/A - documentation only.
- UI craft check: N/A - documentation only.

**BQC Fixes**: None.

---

### Task T013 - Implement low-risk visual effect controls

**Started**: 2026-07-03 04:46
**Completed**: 2026-07-03 04:51
**Duration**: 5 minutes

**Notes**:
- Added independent glow, scanline, flicker, curvature, theme, and reduced-effects controls.
- Implemented effects with local QML rectangles and simple animation, not copied shaders, image assets, profile values, or external terminal code.
- Added accessible names and disabled effect toggles when reduced effects are active.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_visual/main.py` - exposed effect state and slots to QML.
- `apex-infinite-cli/apex_infinite_visual/qml/Main.qml` - added theme selector, reduced-effects fallback, effect toggles, and simple local effects.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `rg -n "Glow|Scanlines|Flicker|Curvature|Reduced effects|setReducedEffects|setEffectEnabled|glowEnabled|scanlinesEnabled|flickerEnabled|curvatureEnabled|Accessible.name" apex_infinite_visual/qml/Main.qml apex_infinite_visual/main.py`
  - Result: PASS - effect controls, reduced-effects fallback, and accessibility labels are present.
  - Evidence: matches show bridge properties/slots and QML controls.
- Command/check: `cd apex-infinite-cli && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300`
  - Result: PASS - QML effect surface loads in offscreen mode.
  - Evidence: command exited 0 with no output.
- Command/check: `cd apex-infinite-cli && LC_ALL=C grep -RInP '[^\\x00-\\x7F]' apex_infinite_visual || true`
  - Result: PASS - QML and wrapper Python remain ASCII-only.
  - Evidence: command produced no matches.
- BQC check: accessibility/platform compliance and product surface discipline.
  - Result: PASS - controls have accessible names and effect toggles are product settings, not diagnostics.
  - Evidence: QML `Accessible.name` entries and reduced-effects disabling are present.
- UI product-surface check: PASS - visual controls are part of the wrapper experience and do not expose implementation telemetry.
- UI craft check: PASS - effects are subtle, independently implemented, and can be reduced.

**BQC Fixes**: None.

---

### Task T012 - Implement event-driven status updates

**Started**: 2026-07-03 04:46
**Completed**: 2026-07-03 04:50
**Duration**: 4 minutes

**Notes**:
- Mapped startup, iteration, history, manager decision, prompt dispatch, Codex dry-run/start/finish/error/timeout, DB logging, completion, max-iteration, stop, and error events into wrapper status.
- Added explicit offline, loading/running, empty/default, stopped, and error states.
- Exposed status, stage, iteration, provider/model, manager decision, and error text to QML panels.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_visual/events.py` - added event-to-state mapping and product-facing log text.
- `apex-infinite-cli/apex_infinite_visual/main.py` - exposed status snapshot fields to QML.
- `apex-infinite-cli/apex_infinite_visual/qml/Main.qml` - rendered status panels and error/status line.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `rg -n "startup_begin|iteration_started|manager_decision|prompt_dispatched|codex_dry_run|codex_started|codex_finished|codex_error|codex_timeout|db_log|workflow_completed|max_iterations_reached|run_stopped|Offline|Input issue|Attention needed" apex_infinite_visual/events.py apex_infinite_visual/main.py`
  - Result: PASS - required lifecycle events and explicit default/error states are mapped.
  - Evidence: matches show status mapping in `events.py` and fixture coverage in `main.py`.
- Command/check: `cd apex-infinite-cli && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300`
  - Result: PASS - fixture status flow renders through QML and exits cleanly.
  - Evidence: command exited 0 with no output.
- BQC check: contract alignment and failure path completeness.
  - Result: PASS - wrapper statuses derive from declared event names and error events become visible state.
  - Evidence: `EventStateAdapter._apply_event_state()` maps known events and `ingest_line()` maps malformed lines.
- UI product-surface check: PASS - status panels show project workflow state and errors without debug telemetry.
- UI craft check: PASS - status hierarchy keeps current status, stage, iteration, provider/model, and decision scannable.

**BQC Fixes**: None.

---

### Task T011 - Implement wrapper run controls and cleanup

**Started**: 2026-07-03 04:45
**Completed**: 2026-07-03 04:49
**Duration**: 4 minutes

**Notes**:
- Added start, stop, dry-run, max-iteration, project path, and optional start-command controls.
- Added duplicate-trigger prevention while running and cleanup for fixture timers and real subprocesses.
- Added `--launch-cli` as the explicit path for launching the guarded real CLI; default dry-run smoke uses fixture events to avoid provider credentials.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_visual/main.py` - added bridge control slots, process launch options, duplicate prevention, and stop cleanup.
- `apex-infinite-cli/apex_infinite_visual/qml/Main.qml` - wired controls to bridge slots and disabled mutating controls while running.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `rg -n "startRun|stopRun|setProjectPath|setStartCommand|setMaxIterations|setDryRun|_running|_process\\.terminate|launch_cli|ApexCliLaunchOptions" apex_infinite_visual/main.py apex_infinite_visual/qml/Main.qml`
  - Result: PASS - run controls, duplicate guard, real launch options, and cleanup are present.
  - Evidence: matches show QML control bindings and bridge slots.
- Command/check: `cd apex-infinite-cli && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300`
  - Result: PASS - dry-run smoke starts fixture flow and exits cleanly.
  - Evidence: command exited 0 with no output.
- BQC check: duplicate action prevention, resource cleanup, state freshness, and external dependency resilience.
  - Result: PASS - `startRun()` returns while running, control setters ignore changes while running, `stopRun()` stops timers and terminates subprocesses, and dry-run fixture mode does not require provider credentials.
  - Evidence: bridge slots and `ApexCliProcess.terminate()` implement those behaviors.
- UI product-surface check: PASS - controls are normal product controls, not runtime diagnostics.
- UI craft check: PASS - controls are stable, labeled, and disabled during in-flight runs.

**BQC Fixes**: None.

---

### Task T008 - Implement PySide6 entrypoint and QML bridge

**Started**: 2026-07-03 04:32
**Completed**: 2026-07-03 04:44
**Duration**: 12 minutes

**Notes**:
- Added a lazy PySide6 import guard so base package imports remain headless-safe.
- Added wrapper CLI arguments for project path, start command, config/provider/model overrides, max iterations, dry-run mode, real CLI launch mode, theme, reduced effects, and offscreen auto-close.
- Added a QObject bridge that exposes event-driven status, run controls, effect controls, bounded log state, fixture playback, and guarded subprocess launch/cleanup.
- Added an offscreen dry-run path that feeds deterministic fixture events without provider API keys or live Codex execution.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_visual/main.py` - added PySide6 entrypoint, import guard, bridge model, fixture flow, launcher integration, and startup flow.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m py_compile apex_infinite_visual/__init__.py apex_infinite_visual/events.py apex_infinite_visual/launcher.py apex_infinite_visual/main.py`
  - Result: PASS - wrapper Python modules compile.
  - Evidence: command exited 0.
- Command/check: `cd apex-infinite-cli && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300`
  - Result: PASS - PySide6 entrypoint starts, loads QML, runs fixture events, and exits without stderr warnings.
  - Evidence: command exited 0 with no output.
- BQC check: resource cleanup, duplicate action prevention, state freshness, failure paths, and concurrency safety.
  - Result: PASS - duplicate starts return while running; fixture and process state reset on start; process worker reports stderr, return code, and exceptions through synthetic error events; queue draining keeps UI updates on the Qt thread; `stopRun()` terminates scoped process work.
  - Evidence: `WrapperBridge.startRun()`, `_start_fixture_flow()`, `_run_process()`, `_drain_queue()`, and `stopRun()` implement those paths.
- UI product-surface check: PASS - offscreen route loaded normal wrapper UI without debug labels, runtime diagnostics, route ownership copy, or readiness badges.
- UI craft check: PASS - QML bridge exposes status panels, controls, and bounded log state needed by the product surface.

**BQC Fixes**:
- Failure path completeness: routed subprocess stderr, non-zero return codes, and wrapper exceptions to explicit error events (`apex-infinite-cli/apex_infinite_visual/main.py`).

---

### Task T009 - Create independent QML prototype surface

**Started**: 2026-07-03 04:36
**Completed**: 2026-07-03 04:45
**Duration**: 9 minutes

**Notes**:
- Added a full-window QML prototype with status panels, run controls, theme selector, reduced-effects control, effect toggles, and read-only event log.
- Used independently chosen QML, layout, color values, names, and simple effects; no reference QML, shaders, assets, fonts, images, or profiles were copied.
- Added a QML fallback bridge object so shutdown and offscreen teardown do not produce null-binding warnings.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_visual/qml/Main.qml` - added independent Qt Quick prototype surface.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `cd apex-infinite-cli && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300`
  - Result: PASS - QML loads and exits cleanly in offscreen mode.
  - Evidence: command exited 0 with no QML warnings after adding the safe bridge fallback.
- Command/check: `cd apex-infinite-cli && LC_ALL=C grep -RInP '[^\\x00-\\x7F]' apex_infinite_visual || true`
  - Result: PASS - wrapper source and QML are ASCII-only.
  - Evidence: command produced no matches.
- BQC check: accessibility/platform compliance and product surface discipline.
  - Result: PASS - controls expose accessible names and the visible surface shows product state, run controls, event log, and visual settings only.
  - Evidence: QML uses `Accessible.name` on controls and contains no route/debug/runtime-readiness labels.
- UI product-surface check: PASS - first surface is the usable wrapper console, not a landing page or implementation telemetry panel.
- UI craft check: PASS - layout keeps log primary, status scannable, controls stable, and reduced effects available.

**BQC Fixes**:
- Failure path completeness: added `safeBridge` fallback object to prevent QML null-binding warnings during offscreen/shutdown paths (`apex-infinite-cli/apex_infinite_visual/qml/Main.qml`).

---

### Task T010 - Wire event-line ingestion into the wrapper bridge

**Started**: 2026-07-03 04:45
**Completed**: 2026-07-03 04:48
**Duration**: 3 minutes

**Notes**:
- Connected launcher stdout JSONL and fixture JSONL to `EventStateAdapter`.
- Preserved deterministic sequence numbers, bounded log retention, and malformed-line recovery.
- Queue-based process ingestion keeps UI mutations on the Qt thread.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_visual/events.py` - maintains sequence order, bounded log state, and malformed-line error mapping.
- `apex-infinite-cli/apex_infinite_visual/main.py` - drains process stdout lines and fixture rows through the adapter.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python - <<'PY' ... EventStateAdapter(max_entries=3) ... PY`
  - Result: PASS - bounded retention kept the last three sequence numbers and malformed JSON became error state.
  - Evidence: command printed `Input issue`, `True`, `[3, 4, 5]`, and `invalid_json`.
- Command/check: `rg -n "line|_drain_queue|ingest_line|build_fixture_event_lines" apex_infinite_visual/main.py apex_infinite_visual/events.py`
  - Result: PASS - launcher and fixture lines route through adapter ingestion.
  - Evidence: matches show `_drain_queue()` and `_emit_next_fixture()` call `ingest_line()`.
- BQC check: concurrency safety and failure path completeness.
  - Result: PASS - worker thread writes to a queue; Qt timer drains queue and malformed input produces visible error state.
  - Evidence: `_queue`, `_drain_queue()`, and `EventStateAdapter.ingest_line()` implement the boundary.
- UI product-surface check: PASS - malformed input appears as wrapper error state, not raw stack trace.
- UI craft check: PASS - log remains bounded and ordered for readable scanning.

**BQC Fixes**: None.

---

### Task T007 - Implement guarded CLI subprocess launcher

**Started**: 2026-07-03 04:26
**Completed**: 2026-07-03 04:32
**Duration**: 6 minutes

**Notes**:
- Added command construction for the existing `apex_infinite.py` entrypoint with `--event-stream - --machine-output`.
- Added project path, start command, config, provider, model, max-iteration, dry-run, environment, timeout, stderr, and cleanup fields.
- Added context-managed subprocess cleanup that terminates first and kills only after the cleanup timeout.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_visual/launcher.py` - added launch options, guarded command builder, process wrapper, stdout iteration, stderr reads, and cleanup.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python - <<'PY' ... build_apex_cli_command(...) ... PY`
  - Result: PASS - command includes the base CLI script, project path, `--event-stream -`, `--machine-output`, `--start implement`, `--max-iterations 1`, and `--dry-run`.
  - Evidence: command printed the full guarded subprocess command.
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m py_compile apex_infinite_visual/__init__.py apex_infinite_visual/events.py apex_infinite_visual/launcher.py`
  - Result: PASS - launcher compiles.
  - Evidence: command exited 0.
- BQC check: resource cleanup, duplicate action prevention, external dependency resilience, and contract alignment.
  - Result: PASS - process resources are scoped, duplicate starts raise, cleanup timeout is explicit, and stdout guardrails are asserted.
  - Evidence: `ApexCliProcess.__exit__()` calls `terminate()`, `start()` rejects an already running process, and `assert_machine_output_command()` checks stdout JSONL isolation.
- UI product-surface check: N/A - launcher only.
- UI craft check: N/A - launcher only.

**BQC Fixes**: None.

---

### Task T006 - Implement JSONL event parser and state adapter

**Started**: 2026-07-03 04:25
**Completed**: 2026-07-03 04:31
**Duration**: 6 minutes

**Notes**:
- Added validated JSONL event parsing for schema version, event name, timestamp, and payload object shape.
- Reused base event payload validation so wrapper inputs reject unsafe strings and secret-looking payloads.
- Added `EventStateAdapter` with bounded log retention and malformed-line recovery that records product-visible error state.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_visual/events.py` - added parser, event records, wrapper snapshots, log entries, and state adapter.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python - <<'PY' ... EventStateAdapter ... PY`
  - Result: PASS - valid startup event parses, malformed JSON maps to adapter error state, and log retention remains bounded.
  - Evidence: command printed `startup_begin 1`, `Input issue`, `True`, and `2`.
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m py_compile apex_infinite_visual/__init__.py apex_infinite_visual/events.py apex_infinite_visual/launcher.py`
  - Result: PASS - event adapter compiles.
  - Evidence: command exited 0.
- BQC check: trust boundary enforcement and failure path completeness.
  - Result: PASS - event lines are schema-validated and malformed input is converted into explicit wrapper error state.
  - Evidence: `parse_event_line()` raises `EventLineError`; `EventStateAdapter.ingest_line()` catches it and records an error log entry.
- UI product-surface check: N/A - adapter state only, no rendered surface yet.
- UI craft check: N/A - adapter state only, no rendered surface yet.

**BQC Fixes**: None.

---

### Task T005 - Create wrapper package metadata and public exports

**Started**: 2026-07-03 04:25
**Completed**: 2026-07-03 04:30
**Duration**: 5 minutes

**Notes**:
- Added optional package metadata and public exports.
- Exported only parser and launcher APIs from package import; PySide6 remains lazy and outside `__init__.py`.

**Files Changed**:
- `apex-infinite-cli/apex_infinite_visual/__init__.py` - added package docstring, public exports, and spike version.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged implementation evidence.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python - <<'PY' ... from apex_infinite_visual import __version__, build_apex_cli_command ... PY`
  - Result: PASS - package imports and exposes version plus launcher API.
  - Evidence: command printed `0.1.0-spike` and a guarded wrapper command.
- Command/check: `git diff -- apex-infinite-cli/apex_infinite.py apex-infinite-cli/requirements.txt apex-infinite-cli/requirements-wrapper.txt`
  - Result: PASS - no base CLI entrypoint or dependency file changes.
  - Evidence: no diff output for those files.
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m py_compile apex_infinite_visual/__init__.py apex_infinite_visual/events.py apex_infinite_visual/launcher.py`
  - Result: PASS - package metadata and current dependency modules compile.
  - Evidence: command exited 0.
- UI product-surface check: N/A - package metadata only.
- UI craft check: N/A - package metadata only.

**BQC Fixes**: None.

---

### Task T004 - Create optional wrapper package directory

**Started**: 2026-07-03 04:24
**Completed**: 2026-07-03 04:25
**Duration**: 1 minute

**Notes**:
- Created `apex-infinite-cli/apex_infinite_visual/` and `apex-infinite-cli/apex_infinite_visual/qml/`.
- No PySide6 import was added to the base CLI runtime path.

**Files Changed**:
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged directory creation.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `mkdir -p apex-infinite-cli/apex_infinite_visual/qml && find apex-infinite-cli/apex_infinite_visual -maxdepth 2 -type d | sort`
  - Result: PASS - optional wrapper package and QML directories exist.
  - Evidence: command printed both `apex-infinite-cli/apex_infinite_visual` and `apex-infinite-cli/apex_infinite_visual/qml`.
- Command/check: `git diff -- apex-infinite-cli/apex_infinite.py apex-infinite-cli/requirements.txt`
  - Result: PASS - no base CLI runtime path or base requirements changes for this task.
  - Evidence: no diff output for the base CLI entrypoint or base requirements.
- UI product-surface check: N/A - directory setup only.
- UI craft check: N/A - directory setup only.

**BQC Fixes**: None.

---

### Task T003 - Resolve clean-room implementation boundaries

**Started**: 2026-07-03 04:23
**Completed**: 2026-07-03 04:24
**Duration**: 1 minute

**Notes**:
- Reviewed the wrapper boundary, Session 06 PRD stub, UX PRD wrapper requirements, and `.gitignore`.
- Confirmed `/EXAMPLE/` is ignored reference material and is not a source dependency.
- Confirmed PyQt, qmltermwidget, QTermWidget, copied terminal emulator code, copied QML, shaders, images, icons, fonts, profiles, resource manifests, and build scripts remain excluded.

**Files Changed**:
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged boundary audit.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `sed -n '1,260p' apex-infinite-cli/docs/visual-wrapper-boundary.md`
  - Result: PASS - clean-room allowed concepts and forbidden-copying categories are explicit.
  - Evidence: docs define the event-driven wrapper boundary and selected PySide6/QML direction.
- Command/check: `sed -n '1,260p' .spec_system/PRD/phase_00/session_06_linux_wrapper_spike.md`
  - Result: PASS - Session 06 scope allows a PySide6/QML spike and excludes copied reference material.
  - Evidence: PRD stub names PyQt, qmltermwidget, QTermWidget, copied QML, copied shaders, and terminal emulator code as out of scope.
- Command/check: `sed -n '1,120p' .gitignore`
  - Result: PASS - `/EXAMPLE/` is ignored.
  - Evidence: `.gitignore` includes `/EXAMPLE/`.
- Command/check: `sed -n '240,520p' .spec_system/PRD/PRD_UX.md`
  - Result: PASS - wrapper UI expectations and clean-room constraints are documented.
  - Evidence: UX PRD defines read-only event-driven wrapper views, status panels, theme/effect controls, and no-copy limits.
- UI product-surface check: N/A - boundary audit only.
- UI craft check: N/A - boundary audit only.

**BQC Fixes**: None.

---

### Task T002 - Audit event-stream and machine-output contracts

**Started**: 2026-07-03 04:22
**Completed**: 2026-07-03 04:23
**Duration**: 1 minute

**Notes**:
- Reviewed current event registry, schema version, payload validation, stdout guardrails, and docs for wrapper consumption.
- Confirmed the wrapper must consume JSONL from `--event-stream - --machine-output` and must keep stderr separate.
- Confirmed event payloads reject ANSI escapes, Rich markup, frame glyphs, visual tokens, secret-looking keys, and secret-looking values.

**Files Changed**:
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/implementation-notes.md` - logged event-contract audit.
- `.spec_system/specs/phase00-session06-linux-wrapper-spike/tasks.md` - marked task completion.

**Verification**:
- Command/check: `sed -n '1,520p' apex-infinite-cli/apex_infinite_events.py`
  - Result: PASS - `EVENT_VERSION = 1`, `EVENT_NAMES` registry, `open_event_stream`, and payload validators are present.
  - Evidence: file includes event names for startup, iteration, manager decision, prompt dispatch, Codex, DB, completion, stop, and errors.
- Command/check: `sed -n '1,320p' apex-infinite-cli/docs/event-stream.md`
  - Result: PASS - docs define JSONL shape, stdout machine-output guardrails, and wrapper guidance.
  - Evidence: docs state `--event-stream -` requires `--machine-output` and wrappers must not parse human output.
- Command/check: `rg -n "event_stream|machine_output|@click.option|def main|def infinite_loop|_emit_event" apex-infinite-cli/apex_infinite.py`
  - Result: PASS - CLI entrypoint enforces machine-output/event-stream relationship and emits lifecycle events.
  - Evidence: matches include Click options, startup validation, and loop emission sites.
- UI product-surface check: N/A - contract audit only.
- UI craft check: N/A - contract audit only.

**BQC Fixes**: None.
