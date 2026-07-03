# Implementation Notes

**Session ID**: `phase00-session08-release-verification`
**Started**: 2026-07-03 06:03
**Last Updated**: 2026-07-03 06:43

---

## Session Progress

| Metric | Value |
|--------|-------|
| Tasks Completed | 22 / 22 |
| Estimated Remaining | 0 |
| Blockers | 0 |

---

## Task Log

### 2026-07-03 - Session Start

**Environment verified**:
- [x] Prerequisites confirmed
- [x] Tools available
- [x] Directory structure ready

---

### Task T001 - Verify analyzer state, base commit, prior validations, and tools

**Started**: 2026-07-03 06:03
**Completed**: 2026-07-03 06:04
**Duration**: 1 minute

**Notes**:
- Analyzer reports `phase00-session08-release-verification` as current session,
  the session directory exists, seven sessions are complete, and Session 08 is
  the only incomplete candidate.
- Base commit `0bc58cf8646ac8a71a74a5cb2014103fbfafb8b9` resolves and matches
  current `HEAD`.
- Sessions 01 through 07 validation reports all show `**Result**: PASS`.
- Local release tools are available: Python 3.12.3 in
  `apex-infinite-cli/.venv/`, `bats`, `jq`, `git`, `black`, `pylint`,
  `pyside6-qmllint`, and `pip-audit`.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T001 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T001 complete and updated progress.

**Verification**:
- Command/check: `bash .spec_system/scripts/analyze-project.sh --json | jq -r '.current_session, .current_session_dir_exists, (.completed_sessions | length), .candidate_sessions[-1].completed'`
  - Result: PASS - output was `phase00-session08-release-verification`, `true`, `7`, `false`.
  - Evidence: Deterministic analyzer state confirms this session is ready.
- Command/check: `git rev-parse HEAD && git rev-parse --verify --quiet 0bc58cf8646ac8a71a74a5cb2014103fbfafb8b9^{commit}`
  - Result: PASS - both commands resolved `0bc58cf8646ac8a71a74a5cb2014103fbfafb8b9`.
  - Evidence: Current release verification base commit is valid.
- Command/check: `for d in .spec_system/specs/phase00-session0{1,2,3,4,5,6,7}-*/validation.md; do printf '%s: ' "$d"; grep -F -m1 '**Result**:' "$d" || true; done`
  - Result: PASS - all seven validation reports returned `**Result**: PASS`.
  - Evidence: Required prerequisite sessions have validation evidence.
- Command/check: `test -x apex-infinite-cli/.venv/bin/python && apex-infinite-cli/.venv/bin/python --version && command -v bats || true && command -v jq && command -v git && test -x apex-infinite-cli/.venv/bin/black && echo black-ok && test -x apex-infinite-cli/.venv/bin/pylint && echo pylint-ok && test -x apex-infinite-cli/.venv/bin/pyside6-qmllint && echo qmllint-ok && test -x apex-infinite-cli/.venv/bin/pip-audit && echo pip-audit-ok || true`
  - Result: PASS - Python, Bats, jq, git, black, pylint, QML lint, and pip-audit were found.
  - Evidence: Release verification tools are locally available.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T016 - Run clean-room no-copy scans

**Started**: 2026-07-03 06:35
**Completed**: 2026-07-03 06:37
**Duration**: 2 minutes

**Notes**:
- Confirmed no `EXAMPLE/` reference files are tracked.
- Scanned tracked CLI, docs, requirements, and workflow paths for reference
  asset, shader, generated shader blob, resource manifest, build script,
  terminal-widget, copied QML, and excluded component names.
- Confirmed no release-scoped binary/reference extensions are tracked.
- Keyword matches are documentation of exclusions and backup options, not
  copied implementation material.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md` - recorded T016 scan evidence.
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - recorded T016 PASS evidence.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T016 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T016 complete and updated progress.

**Verification**:
- Command/check: `git ls-files | grep '^EXAMPLE/' || true`
  - Result: PASS - command produced no output.
  - Evidence: No ignored reference tree files are tracked.
- Command/check: `git ls-files apex-infinite-cli apex-infinite-cli .github/workflows | rg -n 'cool-retro-term|EXAMPLE/|allNoise512|crt256|\\.qsb$|\\.png$|\\.icns$|\\.frag$|\\.vert$|resources\\.qrc$|cool-retro-term\\.pro$|app\\.pro$|snapcraft\\.yaml$|build-appimage\\.sh$|fontmanager|fontlistmodel|qmltermwidget|QTermWidget|TerminalWindow|ApplicationSettings|BurnInEffect|ShaderTerminal|PreprocessedTerminal|TerminalFrame|TerminalTabs|TerminalContainer|SettingsGeneralTab|SettingsEffectsTab|SettingsAdvancedTab|SettingsTerminalTab' || true`
  - Result: PASS - command produced no output.
  - Evidence: No tracked release-scoped paths match copied reference names or forbidden reference file names.
- Command/check: `git ls-files apex-infinite-cli apex-infinite-cli .github/workflows | while IFS= read -r f; do case "$f" in *.png|*.jpg|*.jpeg|*.gif|*.icns|*.qsb|*.frag|*.vert|*.qrc|*.pro|*.desktop) printf 'BINARY_OR_REFERENCE_EXT %s\n' "$f";; esac; done`
  - Result: PASS - command produced no output.
  - Evidence: No release-scoped tracked binary/reference extensions found.
- Command/check: `rg -n 'PyQt|pywebview|xterm\\.js|qmltermwidget|QTermWidget|terminal-emulator code|copied terminal' apex-infinite-cli/apex_infinite.py apex-infinite-cli/apex_infinite_events.py apex-infinite-cli/apex_infinite_ui.py apex-infinite-cli/apex_infinite_visual apex-infinite-cli/requirements*.txt apex-infinite-cli | sed -n '1,220p'`
  - Result: PASS - hits are in documentation of exclusions and backup paths only.
  - Evidence: No implementation import or dependency path uses excluded terminal-widget or copied-terminal material.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T017 - Audit and reconcile release documentation

**Started**: 2026-07-03 06:37
**Completed**: 2026-07-03 06:38
**Duration**: 1 minute

**Notes**:
- Audited README, runbook, event-stream, history DB, prompt-contract,
  transcripts, troubleshooting, wrapper boundary, wrapper productization,
  dependency, and license documentation.
- Confirmed documented coverage for UI flags, fallback behavior, prompt-routing
  non-impact, event streams, machine output, history storage boundaries,
  wrapper source mode, optional dependency isolation, packaging gates, and
  license obligations.
- Found final release/security status text that still describes pre-Session-08
  or Session-07 handoff state; T020 owns updating that posture after T018.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - added documentation audit matrix and T017 PASS evidence.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T017 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T017 complete and updated progress.

**Verification**:
- Command/check: `rg -n -- '--plain|--ascii|--compact|--theme' apex-infinite-cli/README_apex-infinite-cli.md apex-infinite-cli`
  - Result: PASS - README, runbook, transcripts, productization, prompt-contract, and troubleshooting docs cover UI flags and fallback controls.
  - Evidence: Matches include CLI options, runbook examples, constrained-output guidance, and transcript modes.
- Command/check: `rg -n -- '--event-stream|--machine-output|history|SQLite|transcript|troubleshooting|requirements-wrapper|PySide6|license|LGPL|prompt-contract|fallback' apex-infinite-cli/README_apex-infinite-cli.md apex-infinite-cli`
  - Result: PASS - event stream, history, wrapper, dependency, license, transcript, and troubleshooting coverage exists.
  - Evidence: Matches include guarded stdout JSONL, SQLite raw-storage docs, optional wrapper lane, PySide6/QML obligations, and troubleshooting sections.
- Command/check: `test -s apex-infinite-cli/docs/transcripts/dry-run-plain.txt && test -s apex-infinite-cli/docs/transcripts/history-ledger.txt && test -s apex-infinite-cli/docs/transcripts/machine-output-events.jsonl`
  - Result: PASS - all three release transcript samples are present and non-empty.
  - Evidence: Deterministic plain, history, and machine-output examples exist.
- Command/check: stale final-status scan for `Session 07 productizes source/dev`, `binary publishing remains gated`, `Session 08 owns final release verification`, `Phase 00 has not run`, `Planned event-stream payloads are not implemented yet`, and `No automated Python vulnerability audit`
  - Result: PASS with follow-up - stale cumulative status text was identified for T020 refresh.
  - Evidence: Hits are in `.spec_system/SECURITY-COMPLIANCE.md`, README/runbook wrapper status, and `visual-wrapper-productization.md`.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T018 - Run dependency and security release checks

**Started**: 2026-07-03 06:38
**Completed**: 2026-07-03 06:39
**Duration**: 1 minute

**Notes**:
- Confirmed `pip-audit` is available in the CLI virtual environment.
- Audited base, dev, and wrapper requirement files together; no known
  vulnerabilities were reported.
- Confirmed the base terminal CLI dependency lane remains free of PySide6, Qt,
  QML, Nuitka, and wrapper display requirements.
- Confirmed the optional wrapper lane keeps PySide6 and Nuitka separate and
  documents license, notice, checksum, source/relink, and binary packaging
  gates.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - recorded dependency and security evidence.
- `.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md` - updated dependency and wrapper boundary results.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T018 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T018 complete and updated progress.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/pip-audit --version`
  - Result: PASS - output was `pip-audit 2.10.1`.
  - Evidence: Dependency vulnerability audit tool is available locally.
- Command/check: `cd apex-infinite-cli && ./.venv/bin/pip-audit -r requirements.txt -r requirements-dev.txt -r requirements-wrapper.txt`
  - Result: PASS - command exited 0 and reported `No known vulnerabilities found`.
  - Evidence: Base, dev, and optional wrapper requirement sets have current local vulnerability-audit evidence.
- Command/check: `rg -n 'PySide6|Qt|QML|Nuitka|pyside6|qml|qtquick|QtQuick' apex-infinite-cli/requirements.txt apex-infinite-cli/apex_infinite.py apex-infinite-cli/apex_infinite_events.py apex-infinite-cli/apex_infinite_ui.py || true`
  - Result: PASS - command produced no output.
  - Evidence: Base dependency and import surfaces remain terminal-only and headless-safe.
- Command/check: wrapper dependency/license documentation scan across `requirements-wrapper.txt`, README, runbook, and wrapper docs.
  - Result: PASS - PySide6 and Nuitka are isolated to `requirements-wrapper.txt`; license, notices, source/relink, checksum, and AppImage gates are documented.
  - Evidence: Matches are documentation and optional wrapper requirements only.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T019 - Apply focused compatibility fixes discovered by release checks

**Started**: 2026-07-03 06:39
**Completed**: 2026-07-03 06:40
**Duration**: 1 minute

**Notes**:
- Closed the single compatibility fix found by release verification: F001
  suppresses terminal BEL output for non-TTY stdout while preserving desktop
  notification behavior.
- Re-ran the focused regression test after T018; it still passes.
- Inspected the compatibility diff and confirmed the fix scope is limited to
  `notify()` plus the focused test.
- No additional compatibility fixes were found by T013 through T018.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/compatibility-fixes.md` - closed compatibility fix log.
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - recorded T019 PASS evidence.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T019 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T019 complete and updated progress.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/test_cli_options.py::test_notify_does_not_emit_terminal_bell_to_redirected_stdout -v`
  - Result: PASS - output ended with `1 passed in 0.34s`.
  - Evidence: Focused regression still proves redirected stdout receives no terminal bell.
- Command/check: `git diff -- apex-infinite-cli/apex_infinite.py apex-infinite-cli/tests/test_cli_options.py`
  - Result: PASS - diff is limited to the `sys.stdout.isatty()` bell guard and focused regression test.
  - Evidence: No unrelated compatibility changes were introduced.
- UI product-surface check: PASS - notification behavior remains active for interactive terminals and desktop notifications; non-TTY logs no longer receive live-only control bytes.
- UI craft check: PASS - conservative output modes keep logs clean without changing styled interactive rendering.

### Task T020 - Update final release posture records

**Started**: 2026-07-03 06:40
**Completed**: 2026-07-03 06:41
**Duration**: 1 minute

**Notes**:
- Updated final release status to source-shippable after T021/T022 final gates
  for the base terminal CLI and optional Linux visual wrapper source mode.
- Recorded the Linux visual wrapper binary/AppImage path as intentionally
  binary-gated, not a source-release blocker.
- Refreshed cumulative security posture with Session 08 evidence, resolved
  event-stream and clean-room findings, and remaining open WATCH risks.
- Updated README, runbook, and wrapper productization status text so release
  docs no longer describe only the Session 07 handoff.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - added final release position and updated PRD status map.
- `.spec_system/specs/phase00-session08-release-verification/compatibility-fixes.md` - added final compatibility posture review.
- `.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md` - updated source-shippable and binary-gated release position.
- `.spec_system/SECURITY-COMPLIANCE.md` - refreshed cumulative security posture.
- `apex-infinite-cli/README_apex-infinite-cli.md` - updated wrapper source/binary status.
- `apex-infinite-cli/docs/operator-runbook.md` - updated wrapper source/binary status.
- `apex-infinite-cli/docs/visual-wrapper-productization.md` - updated release position and packaging handoff.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T020 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T020 complete and updated progress.

**Verification**:
- Command/check: T020 document reconciliation by inspection.
  - Result: PASS - release records now distinguish source-shippable, binary-gated, deferred, and open-risk statuses.
  - Evidence: Release ledger, clean-room audit, compatibility fixes, security posture, README, runbook, and wrapper productization docs were updated together.
- Command/check: stale final-status phrases from T017 were removed or reworded.
  - Result: PASS - pre-Session-08 security status and wrapper handoff wording now reflect Session 08 release evidence.
  - Evidence: `.spec_system/SECURITY-COMPLIANCE.md` resolves F005/F006 and documents remaining F001-F004 risks; wrapper docs state binary publication remains gated.
- UI product-surface check: PASS - docs use release-facing source/binary status and avoid internal handoff ambiguity.
- UI craft check: N/A - no user-facing UI changed.

### Task T021 - Re-run affected tests and full release gate set

**Started**: 2026-07-03 06:41
**Completed**: 2026-07-03 06:42
**Duration**: 1 minute

**Notes**:
- Re-ran the full CLI pytest suite after F001 and documentation updates.
- Re-ran root Bats, plugin payload sync, analyzer, and prereq checks.
- Re-ran Python formatting, lint, bytecode compile, QML lint, and offscreen
  wrapper smoke.
- Re-ran event-stream safety, dependency vulnerability audit, base dependency
  boundary scan, and local documentation link checks.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - recorded T021 PASS evidence.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T021 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T021 complete and updated progress.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`
  - Result: PASS - 222 tests collected and 222 passed in 10.86s.
  - Evidence: Full CLI, event, history, renderer, subprocess, prompt, UI config, and wrapper test suite passed.
- Command/check: `bats tests/`
  - Result: PASS - 61 Bats tests passed.
  - Evidence: Root script and reference autonomy tests passed.
- Command/check: `bash scripts/sync-plugin-payload.sh --check && bash scripts/analyze-project.sh --json | jq . && bash scripts/check-prereqs.sh --json --env | jq .`
  - Result: PASS - plugin payload current; analyzer current session is Session 08; prereqs overall pass.
  - Evidence: Root workflow state and generated payload checks passed.
- Command/check: Python quality/QML/wrapper command from T011.
  - Result: PASS - black unchanged 20 files; pylint 10.00/10; py_compile passed; QML lint exited 0 with known unqualified-access warnings; offscreen wrapper smoke exited 0.
  - Evidence: Quality and wrapper source smoke gates passed.
- Command/check: T021 event safety rerun.
  - Result: PASS - file event stream and machine stdout each emitted 19 valid JSONL events; unguarded stdout stream failed with exit 2.
  - Evidence: Unsafe-token scans passed and machine stderr was empty.
- Command/check: dependency audit and base boundary scan.
  - Result: PASS - `pip-audit` reported no known vulnerabilities and base dependency boundary scan passed.
  - Evidence: Base CLI remains free of PySide6, Qt, QML, and Nuitka references.
- Command/check: local documentation link check.
  - Result: PASS - 10 markdown files checked with no missing local relative links.
  - Evidence: README, runbook, and deep-dive docs remain link-consistent.
- UI product-surface check: PASS - wrapper source smoke and CLI output-mode tests passed after the notification fix.
- UI craft check: PASS - history, renderer, fallback, and wrapper tests cover supported widths and constrained modes.

### Task T022 - Verify final artifact hygiene and ledger completeness

**Started**: 2026-07-03 06:42
**Completed**: 2026-07-03 06:43
**Duration**: 1 minute

**Notes**:
- Ran final whitespace, ASCII/LF, plugin payload sync, tracked
  reference-material, and ledger completion checks.
- Initial T022 scan found one trailing space in the release ledger reject
  pattern block; removed it and reran the scan successfully.
- Updated task checklist, release ledger, and clean-room audit to complete
  status and `creview` handoff.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - removed trailing whitespace and recorded final PASS evidence.
- `.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md` - finalized clean-room status.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T022 evidence and final progress.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T022 and completion checklist complete.

**Verification**:
- Command/check: `git diff --check`
  - Result: PASS - command produced no output.
  - Evidence: Modified tracked files have no diff whitespace errors.
- Command/check: `bash scripts/sync-plugin-payload.sh --check`
  - Result: PASS - output was `Plugin payload is current.`
  - Evidence: Generated plugin payload remains in sync.
- Command/check: changed-file ASCII/LF/whitespace scan across modified and untracked files.
  - Result: PASS - scan passed for 13 files.
  - Evidence: No non-ASCII bytes, CRLF endings, or trailing whitespace remain in changed files.
- Command/check: tracked reference-material scans.
  - Result: PASS - no tracked `EXAMPLE/` files, copied reference names, or release-scoped binary/reference extensions were found.
  - Evidence: Scan output was `tracked reference-material scans passed`.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T011 - Run Python quality, compile, QML lint, and wrapper smoke

**Started**: 2026-07-03 06:22
**Completed**: 2026-07-03 06:24
**Duration**: 2 minutes

**Notes**:
- Ran the combined Python quality, bytecode compile, QML lint, and offscreen
  wrapper smoke gate.
- Black reported 20 files would be left unchanged.
- Pylint rated checked modules 10.00/10.
- `py_compile` passed for CLI and wrapper Python files.
- `pyside6-qmllint` exited 0 and emitted known unqualified-access warnings.
- Offscreen wrapper smoke exited 0.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - recorded T011 PASS evidence.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T011 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T011 complete and updated progress.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m black --check apex_infinite.py apex_infinite_events.py apex_infinite_ui.py apex_infinite_visual tests && ./.venv/bin/python -m pylint apex_infinite.py apex_infinite_events.py apex_infinite_ui.py apex_infinite_visual && ./.venv/bin/python -m py_compile apex_infinite.py apex_infinite_events.py apex_infinite_ui.py apex_infinite_visual/*.py && ./.venv/bin/pyside6-qmllint apex_infinite_visual/qml/Main.qml && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300`
  - Result: PASS - command exited 0.
  - Evidence: Black unchanged 20 files; pylint 10.00/10; bytecode compile passed; QML lint exited 0 with unqualified-access warnings; offscreen smoke exited 0.
- UI product-surface check: PASS - offscreen wrapper smoke completed without showing blocking diagnostics in normal launch.
- UI craft check: PASS - wrapper source mode launched under offscreen Qt with productized settings and event fixture path.

### Task T012 - Run CLI option smoke checks

**Started**: 2026-07-03 06:24
**Completed**: 2026-07-03 06:29
**Duration**: 5 minutes

**Notes**:
- Ran the CLI smoke matrix for help, dry-run, history, verbose history, plain,
  ASCII, compact, all built-in themes, `NO_COLOR`, `TERM=dumb`, redirected
  output, invalid theme, empty history, and startup/loading state coverage.
- Initial smoke found BEL (`0x07`) in `--plain --ascii` and redirected output
  after max-iteration notification.
- Applied compatibility fix F001: `notify()` now writes terminal bell only when
  `sys.stdout.isatty()` is true.
- Added a focused regression test for redirected stdout notification behavior.
- Reran the full smoke matrix successfully in `/tmp/tmp.FegBh5VPsv`.

**Files Changed**:
- `apex-infinite-cli/apex_infinite.py` - suppress terminal bell for non-TTY stdout in `notify()`.
- `apex-infinite-cli/tests/test_cli_options.py` - added focused regression test for redirected stdout notification behavior.
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - recorded T012 PASS evidence and smoke row statuses.
- `.spec_system/specs/phase00-session08-release-verification/compatibility-fixes.md` - recorded fix F001.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T012 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T012 complete and updated progress.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/test_cli_options.py::test_notify_does_not_emit_terminal_bell_to_redirected_stdout -v`
  - Result: PASS - 1 focused regression test passed.
  - Evidence: Test proves redirected stdout receives no terminal bell from `notify()`.
- Command/check: T012 smoke matrix rerun from `apex-infinite-cli/` with isolated `HOME=<tmp>` per loop smoke.
  - Result: PASS - all matrix rows passed.
  - Evidence: `/tmp/tmp.FegBh5VPsv/results.txt` records PASS for help flags, dry-run prompt, empty history, verbose history, ASCII, compact, all five themes, `NO_COLOR`, `TERM=dumb`, redirected no-ANSI/ASCII, and invalid-theme clear error.
- UI product-surface check: PASS - smoke output showed product-facing startup, history summary, manager decision, prompt preview, dry-run execution, DB log, and safety stop labels without debug/scaffolding copy.
- UI craft check: PASS - plain, ASCII, compact, constrained, and theme modes kept critical labels visible; no ANSI or non-ASCII/control bytes remained in redirected conservative output.

**BQC Fixes**:
- Failure path completeness: prevented a notification BEL control byte from leaking into non-TTY logs while preserving desktop notification execution (`apex-infinite-cli/apex_infinite.py`).

### Task T013 - Run event-stream smoke checks

**Started**: 2026-07-03 06:29
**Completed**: 2026-07-03 06:31
**Duration**: 2 minutes

**Notes**:
- Ran file JSONL and guarded stdout JSONL dry-run smokes with isolated
  temporary `HOME` directories.
- Parsed every JSONL row with Python and validated event names against
  `apex_infinite_events.EVENT_NAMES`.
- Verified machine-output stdout contains JSONL only and stderr is empty.
- Verified unguarded `--event-stream -` fails with the required usage error.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - recorded T013 PASS evidence and raw-data matrix statuses.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T013 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T013 complete and updated progress.

**Verification**:
- Command/check: T013 event-stream smoke script from `apex-infinite-cli/`.
  - Result: PASS - all event-stream checks passed.
  - Evidence: `/tmp/tmp.A15goG7gW8/results.txt` records 19 valid events for file JSONL, 19 valid events for machine stdout JSONL, no unsafe token matches, empty machine-output stderr, and unguarded stdout event stream exit 2.
- Command/check: Unsafe payload scans for ANSI, Rich markup, human-output collisions, visual token names, copied reference identifiers, and secret-like values.
  - Result: PASS - no matches in event file or machine stdout JSONL.
  - Evidence: `event-file unsafe-token`, `machine-output human-collision`, and `machine-output unsafe-token` checks all passed.
- UI product-surface check: PASS - normal event-file mode preserved human dry-run output; machine-output mode emitted no human surface.
- UI craft check: N/A - no UI changed.

### Task T014 - Run initialized-project dry-run smoke

**Started**: 2026-07-03 06:31
**Completed**: 2026-07-03 06:33
**Duration**: 2 minutes

**Notes**:
- Ran Apex Infinite CLI against this repository with `--start plansession`,
  `--dry-run`, `--max-iterations 1`, plain output, and event capture.
- Used an isolated temporary `HOME` so the smoke did not use or mutate the
  operator's real history DB.
- No live provider call or real Codex subprocess was required.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - recorded T014 PASS evidence.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T014 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T014 complete and updated progress.

**Verification**:
- Command/check: `HOME=<tmp> ./.venv/bin/python apex_infinite.py --path /home/aiwithapex/projects/apex-spec-system-open --start plansession --dry-run --max-iterations 1 --plain --event-stream <tmp>/plansession-events.jsonl`
  - Result: PASS - command exited 0 with empty stderr.
  - Evidence: `/tmp/tmp.ZIrzsR5zae` captured stdout and events; prompt output contained `Run the apex-spec skill command /plansession`.
- Command/check: JSONL schema validation of `<tmp>/plansession-events.jsonl`.
  - Result: PASS - 19 events parsed, all with version 1, accepted event names, and mapping payloads.
  - Evidence: Event sequence included startup, config, UI, project, iteration, history, manager decision, prompt, dry-run, DB log, max-iterations, and stop events.
- Command/check: Plain output scans.
  - Result: PASS - no ANSI escapes and no non-ASCII/control bytes.
  - Evidence: `stdout-ansi=PASS` and `stdout-ascii=PASS`.
- UI product-surface check: PASS - output showed normal product-facing startup, iteration, manager decision, prompt, dry-run execution, DB log, and stop labels.
- UI craft check: PASS - constrained plain output stayed readable and line-oriented.

### Task T015 - Verify SQLite history safety

**Started**: 2026-07-03 06:33
**Completed**: 2026-07-03 06:35
**Duration**: 2 minutes

**Notes**:
- Ran a fresh isolated dry-run with temporary `HOME` and inspected the created
  SQLite DB directly.
- Confirmed the legacy `cc_response` column remains present.
- Confirmed the stored row contains raw `implement` dry-run facts and excludes
  renderer labels, ANSI escapes, Rich markup, visual tokens, copied reference
  identifiers, secret-like values, and BEL control bytes.
- Reran history-rendering tests for the render/storage boundary.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - recorded T015 PASS evidence and raw-data matrix statuses.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T015 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T015 complete and updated progress.

**Verification**:
- Command/check: `HOME=<tmp> ./.venv/bin/python apex_infinite.py --path /home/aiwithapex/projects/apex-spec-system-open --start implement --dry-run --max-iterations 1 --plain --ascii`
  - Result: PASS - command exited 0 with empty stderr.
  - Evidence: Temp DB created at `/tmp/tmp.qdf69f9Uva/home/.apex-infinite/history.db`.
- Command/check: Python SQLite schema and raw-row scan.
  - Result: PASS - DB has columns `id,path,cc_response,ai_decision_output,ai_decision_reason,help_or_done_msg,created_at`; one row stored; raw scan passed.
  - Evidence: Stored `ai_decision_output` was `implement` and reason was `User-specified start command`.
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/test_history_rendering.py -v`
  - Result: PASS - 12 history-rendering tests passed.
  - Evidence: Output ended with `12 passed in 0.38s`.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T009 - Run the full CLI pytest suite

**Started**: 2026-07-03 06:18
**Completed**: 2026-07-03 06:20
**Duration**: 2 minutes

**Notes**:
- Ran the complete CLI pytest suite from `apex-infinite-cli/`.
- No failures, skips, or compatibility fixes were required.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - recorded T009 PASS evidence.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T009 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T009 complete and updated progress.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`
  - Result: PASS - 221 tests collected and 221 passed.
  - Evidence: Pytest completed in 10.83s with exit code 0.
- UI product-surface check: PASS - wrapper and terminal UI product-surface tests passed as part of the 221-test suite.
- UI craft check: PASS - renderer, history, operator console, fallback, and wrapper settings tests passed at supported widths and modes.

### Task T010 - Run root workflow checks

**Started**: 2026-07-03 06:20
**Completed**: 2026-07-03 06:22
**Duration**: 2 minutes

**Notes**:
- Ran root Bats tests, plugin payload sync check, analyzer smoke, and prereq
  smoke.
- All root checks passed.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - recorded T010 PASS evidence.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T010 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T010 complete and updated progress.

**Verification**:
- Command/check: `bats tests/`
  - Result: PASS - 61 Bats tests passed.
  - Evidence: TAP output ended at `ok 61 workflow docs do not contain interactive handoff phrases`.
- Command/check: `bash scripts/sync-plugin-payload.sh --check`
  - Result: PASS - plugin payload is current.
  - Evidence: Command output was `Plugin payload is current.`
- Command/check: `bash scripts/analyze-project.sh --json | jq .`
  - Result: PASS - analyzer emitted valid JSON for `phase00-session08-release-verification`.
  - Evidence: `current_session_dir_exists` is true and seven sessions are completed.
- Command/check: `bash scripts/check-prereqs.sh --json --env | jq .`
  - Result: PASS - prereq checker reported `overall: pass`.
  - Evidence: `.spec_system`, jq 1.7, and git 2.43.0 detected; no issues.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T008 - Build the wrapper release-state matrix

**Started**: 2026-07-03 06:16
**Completed**: 2026-07-03 06:18
**Duration**: 2 minutes

**Notes**:
- Audited wrapper source, optional requirements, productization tests, launcher
  code, and wrapper docs before defining source-shippable and binary-gated
  states.
- Added a wrapper release-state matrix to `clean-room-audit.md`.
- Explicitly separated source/dev wrapper evidence from AppImage, notices,
  checksum, source/relink, generated bundle, and legal review gates.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md` - added wrapper release-state matrix.
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - added T008 command evidence row.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T008 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T008 complete and updated progress.

**Verification**:
- Command/check: `rg -n "PySide6|QML|qt|AppImage|SHA256|source/relink|license|LGPL|commercial|requirements-wrapper|dry-run|auto-close|timeout|malformed|stderr|Process failed|Timed out|CLI missing|plain fallback|effect|font|reduced|theme|fixture|event-stream|machine-output" apex-infinite-cli/apex_infinite_visual apex-infinite-cli/requirements-wrapper.txt apex-infinite-cli/tests/test_visual_wrapper_spike.py apex-infinite-cli/tests/test_visual_wrapper_productization.py apex-infinite-cli/visual-wrapper-*.md | sed -n '1,260p'`
  - Result: PASS - source wrapper, tests, optional dependency, license, and binary gate evidence are present.
  - Evidence: Hits include PySide6/QML, guarded event-stream command, source smoke, failure states, settings controls, LGPL/commercial, AppImage, SHA256, and source/relink.
- Command/check: Targeted reads of `tests/test_visual_wrapper_productization.py`, `apex_infinite_visual/main.py`, and `apex_infinite_visual/launcher.py`.
  - Result: PASS - wrapper command construction, import isolation, settings, failure states, and cleanup behavior have testable surfaces.
  - Evidence: `clean-room-audit.md` now maps source-shippable and binary-gated checks to T009, T011, T013, T018, T020, and T021.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T007 - Build the raw-data safety matrix

**Started**: 2026-07-03 06:14
**Completed**: 2026-07-03 06:16
**Duration**: 2 minutes

**Notes**:
- Audited event-stream code/tests and history-rendering tests before defining
  durable-data checks.
- Added JSONL file, JSONL stdout, guard-failure, schema, payload, SQLite temp
  history, raw row, and history render-boundary checks to
  `release-verification.md`.
- Listed reject patterns for ANSI escapes, Rich markup, frame glyphs, visual
  token names, copied reference identifiers, and secret-like values.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - added raw-data safety matrix.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T007 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T007 complete and updated progress.

**Verification**:
- Command/check: `rg -n "ANSI|Rich|markup|frame|glyph|token|secret|api|history|SQLite|cc_response|event|payload|validate|secret-looking|visual" apex-infinite-cli/tests/test_history_rendering.py apex-infinite-cli/tests/test_event_stream.py apex-infinite-cli/apex_infinite_events.py apex-infinite-cli/apex_infinite.py | sed -n '1,260p'`
  - Result: PASS - current code and tests expose the safety points needed for release verification.
  - Evidence: Hits include event payload validation, secret-like key/value checks, ANSI/Rich/frame rejection, and history raw-row tests.
- Command/check: Targeted reads of `tests/test_event_stream.py`, `tests/test_history_rendering.py`, and `apex_infinite_events.py`.
  - Result: PASS - event and history behavior can be verified without live provider or Codex execution.
  - Evidence: Tests cover JSONL writing, stdout guardrails, payload validation, history render modes, and no persistence of display derivations.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T006 - Build the CLI smoke matrix

**Started**: 2026-07-03 06:12
**Completed**: 2026-07-03 06:14
**Duration**: 2 minutes

**Notes**:
- Checked the current CLI help output and UI resolver/test coverage before
  defining smoke commands.
- Expanded the CLI smoke matrix with exact T012 command shapes for dry-run,
  history, verbose history, plain, ASCII, compact, built-in themes, `NO_COLOR`,
  `TERM=dumb`, non-TTY, redirected output, invalid theme, empty history, and
  loading/startup state coverage.
- Planned isolated `HOME=<tmp>` execution to avoid mutating the operator's
  local history DB during smoke checks.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - expanded CLI smoke matrix with exact command shapes.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T006 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T006 complete and updated progress.

**Verification**:
- Command/check: `cd apex-infinite-cli && ./.venv/bin/python apex_infinite.py --help | sed -n '1,180p'`
  - Result: PASS - help output lists all smoke-target flags.
  - Evidence: Output includes `--theme`, `--plain`, `--ascii`, `--compact`, `--event-stream`, and `--machine-output`.
- Command/check: `rg -n "theme|plain|ascii|compact|event_stream|machine_output|NO_COLOR|TERM|is_terminal|dry_run|history" apex-infinite-cli/apex_infinite.py apex-infinite-cli/apex_infinite_ui.py apex-infinite-cli/tests/test_cli_options.py apex-infinite-cli/tests/test_ui_config.py | sed -n '1,240p'`
  - Result: PASS - implementation and tests contain the expected option and environment coverage points.
  - Evidence: Hits include click options, UI resolution, `NO_COLOR`, `TERM=dumb`, non-terminal console handling, history, and event guard tests.
- Command/check: `rg -n "crt-green|crt-amber|ibm-dos|plain|auto" apex-infinite-cli/apex_infinite_ui.py apex-infinite-cli/tests/test_ui_config.py apex-infinite-cli/config.yaml`
  - Result: PASS - built-in theme names and tests match the smoke matrix.
  - Evidence: `BUILT_IN_THEME_NAMES` lists `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and `plain`.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T005 - Build the Phase 00 release verification checklist

**Started**: 2026-07-03 06:10
**Completed**: 2026-07-03 06:12
**Duration**: 2 minutes

**Notes**:
- Expanded `release-verification.md` with release checklist items R001 through
  R030.
- Mapped every PRD success criterion and Session 08 functional, testing,
  non-functional, quality, and repair criterion to a task owner and required
  result.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - added R001-R030 release checklist.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T005 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T005 complete and updated progress.

**Verification**:
- Command/check: Targeted inspection of `.spec_system/PRD/PRD.md`, `.spec_system/specs/phase00-session08-release-verification/spec.md`, and `.spec_system/specs/phase00-session08-release-verification/release-verification.md`.
  - Result: PASS - every PRD success criterion and Session 08 success criterion has a release checklist row and an evidence owner.
  - Evidence: `release-verification.md` now contains R001 through R030.
- Command/check: `rg -n "R00[1-9]|R0[1-3][0-9]" .spec_system/specs/phase00-session08-release-verification/release-verification.md`
  - Result: PASS - release checklist IDs R001-R030 are present.
  - Evidence: Checklist rows map criteria to T009 through T022 evidence tasks and T019/T020 repair/documentation paths.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T004 - Confirm clean-room, license, optional dependency, and reference boundaries

**Started**: 2026-07-03 06:08
**Completed**: 2026-07-03 06:10
**Duration**: 2 minutes

**Notes**:
- Confirmed `/EXAMPLE/` is ignored and the local `EXAMPLE/cool-retro-term/`
  tree is reference-only material.
- Confirmed wrapper docs define forbidden copying, optional PySide6/QML
  isolation, AppImage and checksum gates, LGPLv3/commercial review, source and
  relink obligations, and excluded terminal-widget paths.
- Confirmed base CLI files and base requirements do not reference PySide6, Qt
  Quick, QML, wrapper imports, or Nuitka.
- Recorded that the cumulative security posture still needs a T020 refresh
  because it predates the completed event-stream and wrapper sessions.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md` - added boundary confirmation evidence.
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - added T004 command evidence row.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T004 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T004 complete and updated progress.

**Verification**:
- Command/check: `grep -n '^/EXAMPLE/' .gitignore && test -d EXAMPLE/cool-retro-term && printf 'example tree present and ignored by rule\n' || true`
  - Result: PASS - `.gitignore` contains `/EXAMPLE/` and the local reference tree exists under that ignored path.
  - Evidence: Output reported line 8 and `example tree present and ignored by rule`.
- Command/check: `rg -n "Forbidden Copying|EXAMPLE|reference-only|PySide6|LGPL|AppImage|SHA256|source/relink|requirements-wrapper|base CLI|graphical|QTermWidget|qmltermwidget|copied|shader|GPL" apex-infinite-cli/docs/visual-wrapper-boundary.md apex-infinite-cli/docs/visual-wrapper-productization.md apex-infinite-cli/docs/visual-wrapper-spike.md .spec_system/SECURITY-COMPLIANCE.md .gitignore | sed -n '1,220p'`
  - Result: PASS - boundary, license, optional dependency, packaging, and no-copy terms are documented.
  - Evidence: Hits include forbidden copying, base CLI graphical exclusions, PySide6 LGPL/commercial gates, AppImage, SHA256, source/relink, and `requirements-wrapper`.
- Command/check: `rg -n "PySide6|QtQuick|Qt Quick|qml|apex_infinite_visual|Nuitka" apex-infinite-cli/requirements.txt apex-infinite-cli/apex_infinite.py apex-infinite-cli/apex_infinite_events.py apex-infinite-cli/apex_infinite_ui.py || true`
  - Result: PASS - command produced no output.
  - Evidence: Base CLI runtime files and base requirements have no wrapper dependency references.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T003 - Audit release artifacts and define exact matrix

**Started**: 2026-07-03 06:05
**Completed**: 2026-07-03 06:08
**Duration**: 3 minutes

**Notes**:
- Audited the PRD, UX PRD, Session 08 stub, prior validation reports, CLI
  README, docs, transcripts, requirements files, and GitHub workflows.
- Added an artifact audit matrix and workflow gate matrix to
  `release-verification.md`.
- Confirmed release evidence must cover UI flags, prompt contract, event
  stream, history DB, wrapper source mode, dependency isolation,
  troubleshooting, transcripts, root scripts, security, and release checks.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - added artifact and workflow gate matrices.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T003 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T003 complete and updated progress.

**Verification**:
- Command/check: `rg -n "theme|plain|ascii|compact|event-stream|machine-output|history|prompt|wrapper|PySide6|LGPL|AppImage|SHA256|NO_COLOR|TERM=dumb|license|dependency|troubleshoot|transcript" apex-infinite-cli/README_apex-infinite-cli.md apex-infinite-cli .spec_system/PRD .github/workflows apex-infinite-cli/requirements*.txt | sed -n '1,260p'`
  - Result: PASS - required release topics were found across README, docs, transcripts, PRD, workflows, and requirements.
  - Evidence: Hits include UI modes, event stream guardrails, history, prompt contract, PySide6, AppImage, SHA256, LGPL, and troubleshooting.
- Command/check: `rg -n "name:|pytest|bats|black|pylint|sync-plugin|pip-audit|shellcheck|pyside6|qmllint|AppImage|release|upload" .github/workflows`
  - Result: PASS - local verification matrix can map to workflow checks for quality, test, integration, security, and release.
  - Evidence: Workflow hits include Bats, sync check, shellcheck/shfmt, ASCII/LF, security, and release file/version gates.
- Command/check: `rg -n "^#|^##|PASS|Tests Passing|Quality gate|Clean-room|Security|Next command" .spec_system/specs/phase00-session0{1,2,3,4,5,6,7}-*/validation.md | sed -n '1,260p'`
  - Result: PASS - prior validation reports contain PASS evidence, test evidence, security posture, and handoffs.
  - Evidence: Sessions 01 through 07 validations are available and Session 07 records source wrapper PASS.
- Command/check: Targeted reads of README, operator runbook, event stream, history DB, prompt contract, wrapper boundary, wrapper productization, and requirements.
  - Result: PASS - docs and requirements support the exact release verification matrix.
  - Evidence: `release-verification.md` now maps each artifact set to tasks and gates.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.

### Task T002 - Create release verification artifacts

**Started**: 2026-07-03 06:04
**Completed**: 2026-07-03 06:05
**Duration**: 1 minute

**Notes**:
- Created the release verification ledger with PRD completion criteria mapped
  to release tasks, commands, inspections, and pending statuses.
- Created the compatibility-fix log with repair rules and a no-fix-yet row.
- Created the clean-room audit with optional dependency, license, packaging,
  and no-copy boundaries mapped to later verification tasks.

**Files Changed**:
- `.spec_system/specs/phase00-session08-release-verification/release-verification.md` - added initial release ledger and PRD criteria map.
- `.spec_system/specs/phase00-session08-release-verification/compatibility-fixes.md` - added compatibility-fix log.
- `.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md` - added clean-room audit.
- `.spec_system/specs/phase00-session08-release-verification/implementation-notes.md` - added T002 evidence.
- `.spec_system/specs/phase00-session08-release-verification/tasks.md` - marked T002 complete and updated progress.

**Verification**:
- Command/check: `test -s .spec_system/specs/phase00-session08-release-verification/release-verification.md && test -s .spec_system/specs/phase00-session08-release-verification/compatibility-fixes.md && test -s .spec_system/specs/phase00-session08-release-verification/clean-room-audit.md`
  - Result: PASS - all three release artifacts exist and are non-empty.
  - Evidence: Files were created in the Session 08 spec directory.
- Command/check: Targeted inspection of the new ledgers.
  - Result: PASS - PRD completion criteria, command evidence rows, repair rules, and clean-room boundaries are mapped to release tasks.
  - Evidence: `release-verification.md`, `compatibility-fixes.md`, and `clean-room-audit.md` contain task-linked tables.
- UI product-surface check: N/A - no user-facing UI changed.
- UI craft check: N/A - no UI changed.
