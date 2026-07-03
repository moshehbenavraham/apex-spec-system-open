# Session Specification

**Session ID**: `phase00-session08-release-verification`
**Phase**: 00 - Apex Infinite CLI Upgrade
**Status**: Not Started
**Created**: 2026-07-03
**Base Commit**: `0bc58cf8646ac8a71a74a5cb2014103fbfafb8b9`

---

## 1. Session Overview

This session performs the final release verification for the Apex Infinite CLI
upgrade. It verifies the complete terminal UI, event stream, history safety,
optional Linux visual wrapper, documentation, dependency boundary, and clean-room
license posture before Phase 00 leaves the session loop.

It is next because the analyzer reports Phase 00 in progress, no active
session, Sessions 01 through 07 completed, and Session 08 as the only
unfinished candidate. The Session 07 validation passed and explicitly left
final release verification as the next step before any binary wrapper release or
phase transition.

The session is verification-first. It may produce no product code changes if all
checks pass. If a release check exposes a small compatibility issue, the fix
must stay tightly scoped to the failing CLI, wrapper, test, or documentation
surface and must be recorded in the release verification ledger.

---

## 2. Objectives

1. Verify workflow compatibility, prompt routing, CLI flags, UI modes, event
   stream behavior, SQLite history safety, and optional wrapper behavior against
   the Phase 00 PRD.
2. Run the CLI, wrapper, root script, quality, dependency, and release-readiness
   checks needed to make the upgrade shippable.
3. Smoke test constrained terminal and machine-output modes including plain,
   ASCII, compact, `NO_COLOR`, `TERM=dumb`, redirected output,
   `--event-stream PATH`, and guarded `--event-stream - --machine-output`.
4. Audit documentation, transcripts, security posture, clean-room boundaries,
   optional dependency isolation, packaging gates, and license obligations.
5. Apply only small compatibility or documentation fixes found by verification
   and record whether the PySide6/QML wrapper is source-shippable, binary-gated,
   or explicitly deferred.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase00-session01-config-and-renderer-boundary` - Provides UI config,
      renderer boundaries, and raw-output guarantees.
- [x] `phase00-session02-rich-operator-console` - Provides terminal operator
      surfaces and fallback semantics.
- [x] `phase00-session03-subprocess-and-history-visibility` - Provides live
      subprocess display and history rendering behavior.
- [x] `phase00-session04-event-stream-boundary` - Provides `--event-stream`,
      `--machine-output`, and event payload safety checks.
- [x] `phase00-session05-docs-samples-and-runbooks` - Provides docs,
      transcripts, runbooks, and the wrapper boundary.
- [x] `phase00-session06-linux-wrapper-spike` - Provides PySide6/QML spike
      evidence and wrapper acceptance criteria.
- [x] `phase00-session07-linux-visual-wrapper-productization` - Provides the
      productized optional wrapper source path and release-gate docs.

### Required Tools Or Knowledge

- Python virtual environment under `apex-infinite-cli/.venv/`.
- CLI test suite under `apex-infinite-cli/tests/`.
- Root script and reference tests under `tests/`.
- Wrapper source under `apex-infinite-cli/apex_infinite_visual/`.
- CLI docs under `apex-infinite-cli/README_apex-infinite-cli.md` and
  `apex-infinite-cli/`.
- Clean-room and license rules from `.spec_system/CONVENTIONS.md`,
  `.spec_system/SECURITY-COMPLIANCE.md`, and
  `apex-infinite-cli/docs/visual-wrapper-boundary.md`.

### Environment Requirements

- Linux development environment with bash, jq, Git, Python, and the CLI virtual
  environment available.
- `bats` available for root script tests, or the release ledger must record the
  missing tool as a release blocker if it cannot be installed locally.
- `QT_QPA_PLATFORM=offscreen` or a display-backed environment for wrapper smoke
  testing.
- No live provider API key or real Codex run is required; use dry-run, fixture,
  and machine-output smoke paths for release verification.

---

## 4. Scope

### In Scope (MVP)

- Maintainer can run and record the full CLI pytest suite, root Bats tests,
  plugin payload sync check, analyzer smoke checks, formatter, linter,
  bytecode compile, QML lint, wrapper smoke, and dependency audit.
- Operator can run `--dry-run`, `--history`, `--verbose`, `--plain`,
  `--ascii`, `--compact`, every built-in theme, `--event-stream PATH`, guarded
  `--event-stream - --machine-output`, and constrained environment modes
  without styled data leaking into durable records.
- Maintainer can verify event JSONL and SQLite history rows contain raw facts
  only: no provider API keys, ANSI escapes, Rich markup, frame glyphs, copied
  reference identifiers, or visual-token storage.
- Maintainer can verify documentation covers UI controls, prompt-contract
  impact, fallback behavior, event streams, machine output, history behavior,
  wrapper boundary, packaging gates, dependency plan, troubleshooting, and
  license obligations.
- Maintainer can verify the optional PySide6/QML wrapper source path is
  shippable while AppImage or generated-bundle publication remains gated by
  release checklist evidence.
- Maintainer can apply small compatibility fixes discovered by verification,
  with focused tests and explicit release-ledger entries.

### Out Of Scope (Deferred)

- New feature work that belongs to Sessions 01 through 07 - Reason: this
  session verifies the completed upgrade and fixes only release-blocking
  compatibility gaps.
- Reopening wrapper architecture decisions without a failing verification
  result - Reason: Session 07 productized the accepted PySide6/QML path.
- Publishing an AppImage, generated binary, or package artifact - Reason:
  release verification can approve gates, but binary publication is outside
  this session.
- Adding graphical dependencies to the base CLI install - Reason: the base CLI
  must remain terminal-only and headless-safe.
- Creating binary screenshots or copying reference assets - Reason: repo output
  should use text evidence and the clean-room rule forbids copied material.

---

## 5. Technical Approach

### Architecture

Create a release verification ledger in the Session 08 spec directory and map
each PRD completion criterion to a command, inspection, or explicit deferral.
Run verification from the repo root and `apex-infinite-cli/` without depending
on real LLM calls or live Codex execution. Use dry-run, temp files, redirected
output, constrained environment variables, and machine-output JSONL to exercise
operator paths safely.

Treat tests and docs as release artifacts. If verification finds a bug, repair
the narrowest responsible surface, add or adjust focused tests, re-run the
affected checks, and record the before/after result in
`compatibility-fixes.md`. If verification finds stale release documentation or
security posture, update the exact document that owns the stale fact and record
the evidence in the release ledger.

Keep the wrapper verification source-mode first. Confirm the wrapper remains an
optional PySide6/QML path, consumes the JSONL event boundary, keeps graphical
dependencies outside `requirements.txt`, and has documented packaging,
checksum, notice, source/relink, and clean-room gates before any binary release.

### Design Patterns

- Evidence ledger: One release checklist ties every completion criterion to a
  command result, inspection, fix, or explicit deferral.
- Dry-run smoke path: Exercises real CLI option routing and event output
  without live provider or Codex calls.
- Raw-data safety scan: Separates renderer output from SQLite and JSONL
  durable facts.
- Optional dependency boundary: Verifies PySide6/QML remains outside the base
  CLI import path and base requirements.
- Clean-room audit: Checks tracked files and docs against the reference-material
  no-copy boundary.
- Narrow repair loop: Any discovered issue gets a focused fix, focused test,
  and targeted re-run before final gates.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| `.spec_system/specs/phase00-session08-release-verification/release-verification.md` | Final release verification matrix, command evidence, smoke results, release status, and deferrals | ~260 |
| `.spec_system/specs/phase00-session08-release-verification/compatibility-fixes.md` | Log of verification failures, small fixes applied, test evidence, or explicit no-fix result | ~120 |
| `.spec_system/specs/phase00-session08-release-verification/clean-room-audit.md` | Clean-room, optional dependency, license, packaging, and no-copy audit evidence | ~180 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/apex_infinite.py` | Small CLI compatibility fixes only if smoke or tests expose release-blocking behavior | ~0-80 |
| `apex-infinite-cli/apex_infinite_ui.py` | Small renderer, fallback, width, ASCII, or plain-mode fixes only if verification fails | ~0-80 |
| `apex-infinite-cli/apex_infinite_events.py` | Small event-stream safety or machine-output fixes only if verification fails | ~0-60 |
| `apex-infinite-cli/apex_infinite_visual/` | Small wrapper smoke, failure-state, or optional dependency fixes only if verification fails | ~0-100 |
| `apex-infinite-cli/tests/` | Focused regression tests for any compatibility fix applied during verification | ~0-160 |
| `apex-infinite-cli/README_apex-infinite-cli.md` | Release-status, CLI flag, event, history, wrapper, or troubleshooting corrections found by audit | ~0-80 |
| `apex-infinite-cli/` | Documentation corrections for event stream, history DB, operator runbook, prompt contract, transcripts, troubleshooting, or wrapper release gates | ~0-160 |
| `.spec_system/SECURITY-COMPLIANCE.md` | Updated cumulative security, GDPR, dependency, and clean-room release posture after verification | ~0-160 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] Existing prompt routing and workflow behavior remain compatible, or any
      intentional change has matching tests and documentation.
- [ ] CLI users can enable the new UI, disable it cleanly, and operate safely in
      constrained terminal, plain, ASCII, compact, redirected, and machine-output
      modes.
- [ ] Event JSONL and SQLite history rows store raw workflow facts only and do
      not include provider API keys, ANSI escapes, Rich markup, frame glyphs,
      visual tokens, copied reference identifiers, or renderer snapshots.
- [ ] Optional wrapper source mode launches or the exact local display/tool
      blocker is recorded; binary distribution remains gated by documented
      release checks.
- [ ] Documentation describes UI controls, prompt-contract impact, fallback
      behavior, event stream behavior, history behavior, wrapper boundary,
      dependency plan, license assessment, and troubleshooting.
- [ ] Completion criteria in the PRD and Session 08 stub are satisfied or
      explicitly deferred with rationale.

### Testing Requirements

- [ ] `cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v` passes.
- [ ] Formatter, linter, bytecode compile, QML lint, offscreen wrapper smoke,
      and dependency audit pass or have recorded release-blocking evidence.
- [ ] Root checks pass: `bats tests/`,
      `bash scripts/sync-plugin-payload.sh --check`,
      `bash scripts/analyze-project.sh --json | jq .`, and
      `bash scripts/check-prereqs.sh --json --env | jq .`.
- [ ] CLI smoke matrix covers `--dry-run`, `--history`, `--verbose`,
      `--plain`, `--ascii`, `--compact`, every built-in theme,
      `--event-stream PATH`, guarded `--event-stream - --machine-output`,
      `NO_COLOR`, `TERM=dumb`, non-TTY behavior, and redirected output.
- [ ] Clean-room scan confirms no tracked reference source, shader, image, icon,
      font, resource manifest, literal profile data, build script, copied QML,
      copied compiled shader blob, or GPL code was added.

### Non-Functional Requirements

- [ ] Base CLI installation remains free of PySide6, QML, graphical imports,
      wrapper assets, and display-server requirements.
- [ ] Plain and ASCII output stay readable at 80, 100, and 120 terminal columns.
- [ ] Startup and history rendering for release smoke paths remain fast enough
      for local use and avoid live-only control sequences in durable logs.
- [ ] API keys and secret-like payload keys are not printed, stored, emitted, or
      documented in release transcripts.

### Quality Gates

- [ ] All files ASCII-encoded
- [ ] Unix LF line endings
- [ ] Code follows project conventions
- [ ] `git diff --check` passes
- [ ] Release verification ledger is complete and contains no unresolved
      placeholder or interactive follow-up text

---

## 8. Implementation Notes

### Working Assumptions

- Session 08 is executable now: the analyzer reports no active session, Phase
  00 in progress, Sessions 01 through 07 complete, and Session 08 as the only
  incomplete candidate. Planning can proceed without user arbitration because
  the deterministic script output, state history, and validation reports agree.
- The optional wrapper is source-shippable but binary-gated: Session 07
  validation passed the source-mode PySide6/QML wrapper, while PRD and wrapper
  docs keep AppImage or generated-bundle publication behind license, bundle,
  checksum, notice, source/relink, and release verification gates.
- Verification may produce no product code changes: the Session 08 stub names
  final verification notes as a deliverable and allows small compatibility
  fixes only when release testing finds them.
- The release smoke path should avoid live provider and Codex execution:
  dry-run, fixture, temp event streams, and machine-output commands cover the
  operator behaviors without requiring credentials or modifying a target
  project.

### Conflict Resolutions

- `.spec_system/SECURITY-COMPLIANCE.md` still records pre-Phase-00 posture for
  several planned controls, while Session 04 through Session 07 validations
  show event stream and wrapper controls implemented and tested. This plan uses
  the latest session validations as implementation evidence and includes a task
  to update the cumulative security posture if release verification confirms
  those controls.
- The Session 08 stub asks for a real initialized Apex Spec project smoke test,
  while live Codex execution would require provider credentials and could
  modify a target project. The chosen interpretation is an initialized-project
  dry-run and machine-output smoke against this repository, because it exercises
  CLI routing and event output without external credentials or unsafe writes.

### Key Considerations

- The base CLI must remain terminal-only and safe for headless, CI, remote
  shell, redirected, and log-file usage.
- Durable records must store raw operational facts, not display labels,
  renderer tokens, ANSI escapes, Rich markup, or box/frame glyphs.
- Clean-room verification must treat the `EXAMPLE/cool-retro-term/` tree as
  reference-only and ignored by Git.
- Release verification should close or explicitly carry forward security and
  dependency findings instead of leaving stale posture text.

### Potential Challenges

- Missing local tools: Record missing Bats, pip-audit, PySide6, QML lint, or
  display support as release blockers only after preserving all other completed
  evidence.
- Environment-specific wrapper smoke: Prefer `QT_QPA_PLATFORM=offscreen` and
  record the exact local failure state if the display backend is unavailable.
- Broad test surface: Run focused re-checks immediately after any fix, then the
  full release gate set before completion.
- Security posture drift: Update only the cumulative security facts supported
  by command evidence and leave unresolved findings open with rationale.

### Relevant Considerations

- [P00] **Prompt contract coupling**: Keep prompt functions stable unless tests,
  README, and prompt-contract docs are updated together.
- [P00] **History compatibility**: Preserve the legacy `cc_response` column,
  normalized project path keys, and raw stored workflow data.
- [P00] **Plain-output safety**: Verify `auto` resolves to plain output under
  `NO_COLOR`, `TERM=dumb`, non-TTY output, redirected output, or non-terminal
  console paths unless an explicit theme is provided.
- [P00] **Raw durable facts only**: Verify SQLite rows and JSONL events exclude
  ANSI escapes, Rich markup, frame glyphs, visual tokens, secrets, and renderer
  snapshots.
- [P01] **Optional wrapper obligations**: Keep PySide6/Qt Quick/QML optional and
  document LGPLv3/commercial, packaging, checksum, and source/relink obligations
  before release.
- [P00] **Docs move with behavior**: Correct README, runbook, history, event,
  prompt-contract, troubleshooting, and wrapper docs when verification finds
  behavior or release-status drift.

### Behavioral Quality Focus

Checklist active: Yes
Top behavioral risks for this session:
- Verification commands accidentally exercising live provider or Codex paths
  instead of dry-run and fixture paths.
- Machine-output JSONL mixing with human Rich or plain output on stdout.
- Release docs overstating wrapper binary readiness before license and bundle
  gates are complete.

---

## 9. Testing Strategy

### Unit Tests

- Run all existing CLI tests under `apex-infinite-cli/tests/`.
- Add focused regression tests only if release verification finds a CLI,
  renderer, event, history, or wrapper compatibility bug.

### Integration Tests

- Run root Bats tests and script smoke checks.
- Run CLI smoke commands for dry-run, history, UI modes, constrained terminal
  modes, event-stream file output, and guarded machine-output stdout.
- Run wrapper offscreen smoke with dry-run or fixture events.

### Runtime Verification

- Execute initialized-project dry-run smoke against this repository with
  `--path /home/aiwithapex/projects/apex-spec-system-open`,
  `--start plansession`, and a small `--max-iterations` value.
- Capture event-stream output to a temp file and inspect JSONL payloads for
  schema validity and raw-data safety.
- Confirm history display is readable in normal, plain, ASCII, compact, and
  verbose modes without mutating stored rows.

### Edge Cases

- `NO_COLOR` and explicit `--theme` override precedence.
- `TERM=dumb`, non-TTY, and redirected output fallback behavior.
- `--event-stream -` without `--machine-output` guard failure.
- Missing PySide6 or display backend wrapper failure surfaces.
- Empty, sparse legacy, short, and long history rows.
- Secret-like payload keys, ANSI escapes, Rich markup, and frame glyphs rejected
  by event payload validation.

---

## 10. Dependencies

### Other Sessions

- Depends on: `phase00-session01-config-and-renderer-boundary`,
  `phase00-session02-rich-operator-console`,
  `phase00-session03-subprocess-and-history-visibility`,
  `phase00-session04-event-stream-boundary`,
  `phase00-session05-docs-samples-and-runbooks`,
  `phase00-session06-linux-wrapper-spike`,
  `phase00-session07-linux-visual-wrapper-productization`
- Depended by: Phase Transition workflow beginning with `audit`

---

## Next Steps

Run the `implement` workflow step to begin release verification.
