# Task Checklist

**Session ID**: `phase00-session08-release-verification`
**Total Tasks**: 22
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Progress Summary

| Metric | Value |
|--------|-------|
| Tasks Completed | 22 / 22 |
| Estimated Remaining | 0 |
| Blockers | 0 |

---

## Setup (4 tasks)

- [x] T001 [S0008] Verify analyzer state, current base commit, Sessions 01 through 07 validation evidence, and local release tool availability before running release checks (`.spec_system/scripts/analyze-project.sh`, `.spec_system/specs/phase00-session07-linux-visual-wrapper-productization/validation.md`, `apex-infinite-cli/.venv/`)
- [x] T002 [S0008] Create the release verification ledger, compatibility-fix log, and clean-room audit files with the PRD completion criteria mapped to evidence rows (`.spec_system/specs/phase00-session08-release-verification/release-verification.md`, `.spec_system/specs/phase00-session08-release-verification/compatibility-fixes.md`, `.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md`)
- [x] T003 [S0008] Audit the PRD, UX PRD, Session 08 stub, prior validations, docs, transcripts, requirements, and workflow files to define the exact release verification matrix (`.spec_system/PRD/PRD.md`, `.spec_system/PRD/PRD_UX.md`, `.spec_system/PRD/phase_00/session_08_release_verification.md`, `apex-infinite-cli/`, `.github/workflows/`)
- [x] T004 [S0008] Confirm clean-room, license, optional dependency, and reference-material boundaries before running no-copy scans (`apex-infinite-cli/docs/visual-wrapper-boundary.md`, `apex-infinite-cli/docs/visual-wrapper-productization.md`, `EXAMPLE/cool-retro-term/`, `.gitignore`)

---

## Foundation (4 tasks)

- [x] T005 [S0008] Build the release verification checklist with every Phase 00 PRD success criterion tied to a command, inspection, fix, or explicit deferral (`.spec_system/specs/phase00-session08-release-verification/release-verification.md`)
- [x] T006 [S0008] Build the CLI smoke matrix for `--dry-run`, `--history`, `--verbose`, `--plain`, `--ascii`, `--compact`, every built-in theme, `NO_COLOR`, `TERM=dumb`, redirected output, and non-TTY fallback behavior (`.spec_system/specs/phase00-session08-release-verification/release-verification.md`, `apex-infinite-cli/apex_infinite.py`)
- [x] T007 [S0008] Build the raw-data safety matrix for SQLite history rows and JSONL event payloads with secret, ANSI, Rich markup, frame glyph, visual-token, and copied-reference checks (`.spec_system/specs/phase00-session08-release-verification/release-verification.md`, `apex-infinite-cli/apex_infinite_events.py`, `apex-infinite-cli/tests/test_history_rendering.py`)
- [x] T008 [S0008] Build the wrapper release-state matrix for source-mode smoke, optional dependency isolation, PySide6/QML license obligations, packaging gates, checksums, notices, and source/relink obligations (`.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md`, `apex-infinite-cli/requirements-wrapper.txt`, `apex-infinite-cli/docs/visual-wrapper-productization.md`)

---

## Verification (10 tasks)

- [x] T009 [S0008] Run the full CLI pytest suite and record pass or failure evidence (`cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`)
- [x] T010 [S0008] Run root workflow checks and record pass or failure evidence (`bats tests/`, `bash scripts/sync-plugin-payload.sh --check`, `bash scripts/analyze-project.sh --json | jq .`, `bash scripts/check-prereqs.sh --json --env | jq .`)
- [x] T011 [S0008] Run Python quality, compile, QML lint, and offscreen wrapper smoke checks with cleanup on scope exit for wrapper subprocess resources (`cd apex-infinite-cli && ./.venv/bin/python -m black --check apex_infinite.py apex_infinite_events.py apex_infinite_ui.py apex_infinite_visual tests && ./.venv/bin/python -m pylint apex_infinite.py apex_infinite_events.py apex_infinite_ui.py apex_infinite_visual && ./.venv/bin/python -m py_compile apex_infinite.py apex_infinite_events.py apex_infinite_ui.py apex_infinite_visual/*.py && ./.venv/bin/pyside6-qmllint apex_infinite_visual/qml/Main.qml && QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300`)
- [x] T012 [S0008] Run CLI option smoke checks for dry-run, history, verbose, plain, ASCII, compact, and each built-in theme with explicit loading, empty, error, and constrained-output state coverage (`apex-infinite-cli/apex_infinite.py`, `.spec_system/specs/phase00-session08-release-verification/release-verification.md`)
- [x] T013 [S0008] Run event-stream smoke checks for file JSONL and guarded stdout machine output with schema validation and explicit stdout-collision failure mapping (`apex-infinite-cli/apex_infinite_events.py`, `apex-infinite-cli/docs/event-stream.md`, `.spec_system/specs/phase00-session08-release-verification/release-verification.md`)
- [x] T014 [S0008] Run initialized-project dry-run smoke against this repository with `--start plansession`, small `--max-iterations`, and event capture without live provider or Codex writes (`apex-infinite-cli/apex_infinite.py`, `/home/aiwithapex/projects/apex-spec-system-open`, `.spec_system/specs/phase00-session08-release-verification/release-verification.md`)
- [x] T015 [S0008] Verify SQLite history safety using tests or a temp DB scan so stored rows keep raw workflow data and exclude renderer labels, ANSI escapes, Rich markup, frame glyphs, visual tokens, copied reference identifiers, and secrets (`apex-infinite-cli/tests/test_history_rendering.py`, `apex-infinite-cli/apex_infinite.py`, `.spec_system/specs/phase00-session08-release-verification/release-verification.md`)
- [x] T016 [S0008] Run clean-room no-copy scans across tracked CLI, wrapper, docs, requirements, and workflow files while confirming no `EXAMPLE/` reference material is tracked (`git ls-files`, `EXAMPLE/cool-retro-term/`, `.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md`)
- [x] T017 [S0008] Audit and reconcile release documentation for UI flags, prompt-contract impact, fallback behavior, event stream, history DB, transcripts, wrapper boundary, productization, troubleshooting, dependency plan, and license assessment (`apex-infinite-cli/README_apex-infinite-cli.md`, `apex-infinite-cli/`)
- [x] T018 [S0008] Run dependency and security release checks, including base requirement isolation from PySide6/QML and available pip vulnerability audit evidence (`apex-infinite-cli/requirements.txt`, `apex-infinite-cli/requirements-dev.txt`, `apex-infinite-cli/requirements-wrapper.txt`, `.spec_system/SECURITY-COMPLIANCE.md`)

---

## Repair And Documentation (2 tasks)

- [x] T019 [S0008] Apply focused compatibility fixes discovered by release checks with duplicate-trigger prevention, explicit failure mapping, raw durable data guarantees, and regression tests scoped to the failing surface (`apex-infinite-cli/apex_infinite.py`, `apex-infinite-cli/apex_infinite_ui.py`, `apex-infinite-cli/apex_infinite_events.py`, `apex-infinite-cli/apex_infinite_visual/`, `apex-infinite-cli/tests/`)
- [x] T020 [S0008] Update final release verification, compatibility-fix, clean-room, documentation, and cumulative security posture records with shipped, binary-gated, deferred, or blocker status for every release criterion (`.spec_system/specs/phase00-session08-release-verification/release-verification.md`, `.spec_system/specs/phase00-session08-release-verification/compatibility-fixes.md`, `.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md`, `.spec_system/SECURITY-COMPLIANCE.md`, `apex-infinite-cli/`)

---

## Final Gates (2 tasks)

- [x] T021 [S0008] Re-run affected tests and the full release gate set after any fixes, including pytest, root checks, quality checks, wrapper smoke, event safety, dependency boundary, and documentation link checks (`apex-infinite-cli/tests/`, `tests/`, `apex-infinite-cli/`, `.spec_system/specs/phase00-session08-release-verification/release-verification.md`)
- [x] T022 [S0008] Verify ASCII/LF, clean whitespace, no open planning markers, no tracked copied reference material, plugin payload sync, and complete release ledger evidence before handing off to review (`git diff --check`, `bash scripts/sync-plugin-payload.sh --check`, `.spec_system/specs/phase00-session08-release-verification/`)

---

## Completion Checklist

- [x] All tasks marked `[x]`
- [x] All tests and checks passing or release blockers recorded with evidence
- [x] All files ASCII-encoded with LF line endings
- [x] implementation-notes.md updated
- [x] Ready for `creview` to continue the implement -> creview -> validate sequence

---

## Next Steps

Run the `creview` workflow step.
