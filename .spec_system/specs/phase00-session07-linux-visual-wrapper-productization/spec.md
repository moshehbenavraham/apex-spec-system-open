# Session Specification

**Session ID**: `phase00-session07-linux-visual-wrapper-productization`
**Phase**: 00 - Apex Infinite CLI Upgrade
**Status**: Not Started
**Created**: 2026-07-03
**Base Commit**: `6f774b606856a75d372d62f090575a1eead0b614`

---

## 1. Session Overview

This session turns the accepted Linux visual wrapper spike into a maintainable
optional visual mode for Apex Infinite CLI. It hardens the PySide6/QML wrapper
around settings, launch validation, failure display, smoke testing, and release
documentation while preserving the base terminal CLI as the only workflow
engine.

It is next because the analyzer reports Phase 00 in progress, no active
session, Sessions 01 through 06 complete, and Session 07 as the earliest
unfinished candidate. Session 06 validation passed and its spike record
explicitly recommends proceeding with PySide6/QML productization under the
optional wrapper boundary.

The session productizes the source and operator path, not a final binary
release. AppImage or generated-bundle publishing remains gated on the license,
bundle, and release verification checks that are documented here and completed
in Session 08.

---

## 2. Objectives

1. Convert the accepted prototype into an optional Linux visual mode with
   validated settings for theme presets, effect intensity, font choice, scale,
   reduced effects, and plain fallback.
2. Harden wrapper launch and lifecycle behavior so missing CLI files, missing
   PySide6, display-backend failures, malformed JSONL, subprocess stderr,
   non-zero exits, and timeouts render as explicit product-facing states.
3. Keep wrapper dependencies, QML, graphical startup, and packaging guidance
   outside the base CLI runtime path.
4. Add focused productization tests and a CI-friendly offscreen smoke path for
   wrapper launch, fixture flow, real CLI subprocess invocation, and failure
   handling.
5. Document Linux setup, packaging, release, troubleshooting, license, and
   clean-room boundaries without publishing a binary artifact in this session.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase00-session01-config-and-renderer-boundary` - Provides UI config,
      renderer boundaries, and raw output guarantees.
- [x] `phase00-session02-rich-operator-console` - Provides terminal operator
      semantics that the wrapper must not scrape or fork.
- [x] `phase00-session03-subprocess-and-history-visibility` - Provides
      subprocess and history behavior that wrapper display must preserve.
- [x] `phase00-session04-event-stream-boundary` - Provides
      `--event-stream`, `--machine-output`, and the importable event API.
- [x] `phase00-session05-docs-samples-and-runbooks` - Provides docs, samples,
      wrapper boundary, and clean-room no-copy rules.
- [x] `phase00-session06-linux-wrapper-spike` - Provides accepted PySide6/QML
      prototype evidence and productization recommendation.

### Required Tools Or Knowledge

- Current wrapper prototype under `apex-infinite-cli/apex_infinite_visual/`.
- Current event names and payload validation in
  `apex-infinite-cli/apex_infinite_events.py`.
- Session 06 decision record in
  `apex-infinite-cli/docs/visual-wrapper-spike.md`.
- PySide6/Qt Quick/QML optional dependency behavior from
  `apex-infinite-cli/requirements-wrapper.txt`.
- Clean-room and license boundaries from `CONVENTIONS.md`,
  `SECURITY-COMPLIANCE.md`, and
  `apex-infinite-cli/docs/visual-wrapper-boundary.md`.

### Environment Requirements

- Linux development environment.
- Python virtual environment for `apex-infinite-cli/`.
- Optional wrapper dependencies available from
  `apex-infinite-cli/requirements-wrapper.txt` for smoke checks.
- `QT_QPA_PLATFORM=offscreen` or a graphical display for wrapper smoke tests.
- No provider API keys or live Codex execution required for unit tests;
  fixture events and dry-run subprocess invocation are sufficient.

---

## 4. Scope

### In Scope (MVP)

- Operator can run the optional visual mode from the source tree without
  installing or launching `cool-retro-term`.
- Operator can choose green CRT, amber CRT, IBM DOS, and plain presets with
  independent settings for effect intensity, font, scale, reduced effects, and
  plain fallback.
- Future wrapper developer can rely on typed wrapper settings and explicit
  event-derived state instead of ad hoc QML-only defaults.
- Wrapper launch uses `--event-stream - --machine-output` and keeps stderr,
  return-code, timeout, malformed-event, and missing-CLI failures visible.
- Maintainer can run focused tests for settings validation, launcher command
  construction, subprocess cleanup, bridge state changes, malformed events,
  and optional dependency guards.
- Maintainer can follow Linux development, packaging, AppImage, license-notice,
  checksum, source/relink, and troubleshooting instructions before release.

### Out Of Scope (Deferred)

- Publishing a final AppImage or other binary artifact - Reason: release
  verification and license/bundle review happen after productization.
- Making the base CLI require PySide6, Qt, a graphical display, or wrapper
  assets - Reason: base CLI must remain lightweight and headless-safe.
- Forking manager decisions, prompt routing, SQLite storage, or safety
  behavior - Reason: the terminal CLI remains the workflow engine.
- Scraping Rich output, plain output, terminal frames, or history display rows
  - Reason: the event stream is the wrapper contract.
- Copying reference QML, shader code, generated shader blobs, images, icons,
  fonts, profile data, resource manifests, build scripts, or terminal-emulator
  code - Reason: clean-room and license boundaries forbid it.
- Supporting macOS or Windows wrapper builds - Reason: the phase scope is
  Linux-only.

---

## 5. Technical Approach

### Architecture

Productize the existing optional package at
`apex-infinite-cli/apex_infinite_visual/`. Add a settings/preset module that
owns theme tokens, effect intensity, font defaults, scaling bounds, reduced
effects, and plain fallback rules. The PySide6 bridge consumes those settings
and exposes validated properties and slots to QML.

Keep the base CLI unchanged except where existing event contracts require
tests. The wrapper launcher continues to run `apex_infinite.py` as a subprocess
with `--event-stream - --machine-output`. The launcher validates the CLI script,
builds guarded commands, separates stdout JSONL from stderr, enforces cleanup,
and reports missing CLI, timeout, return-code, and stderr conditions as wrapper
events.

The QML surface remains independently designed and event-driven. It should
become a productized operator surface with stable dimensions, accessible
controls, visible failure states, and no debug/scaffolding text in the primary
view. Packaging work is documentation-first: capture the selected pyside6-deploy
and AppImage path, required notices, checksums, source/relink obligations, and
verification commands without copying third-party build scripts.

### Design Patterns

- Optional package boundary: Keeps graphical imports and runtime dependencies
  out of normal CLI execution.
- Typed settings model: Moves visual presets and validation out of QML-only
  literals and into testable Python.
- Event adapter: Converts raw lifecycle JSONL into wrapper state without
  parsing terminal output or SQLite rows.
- Guarded subprocess launcher: Keeps stdout JSONL isolated and stderr visible.
- Bridge-owned controls: Prevents duplicate starts, revalidates revisitable
  state, and cleans up subprocess resources on stop or exit.
- Clean-room QML surface: Uses independent names, colors, layouts, controls,
  and effects.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/apex_infinite_visual/settings.py` | Validated wrapper presets, effect controls, font/scale bounds, and plain fallback settings | ~190 |
| `apex-infinite-cli/tests/test_visual_wrapper_productization.py` | Productization tests for settings, launch validation, bridge failure states, and smoke helpers | ~280 |
| `apex-infinite-cli/docs/visual-wrapper-productization.md` | Linux visual mode setup, packaging, release checklist, license obligations, and verification plan | ~240 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/apex_infinite_visual/__init__.py` | Export productized wrapper metadata and stable public names | ~20 |
| `apex-infinite-cli/apex_infinite_visual/events.py` | Extend product-facing state mappings for launch, timeout, non-zero, stderr, and malformed-event failures | ~70 |
| `apex-infinite-cli/apex_infinite_visual/launcher.py` | Add Linux/source-tree validation, missing CLI checks, timeout handling, failure summaries, and cleanup coverage | ~120 |
| `apex-infinite-cli/apex_infinite_visual/main.py` | Wire settings, bridge controls, launch validation, duplicate-trigger prevention, and productized failure handling | ~190 |
| `apex-infinite-cli/apex_infinite_visual/qml/Main.qml` | Add productized controls, presets, failure surfaces, stable layout sizing, accessibility labels, and plain fallback | ~180 |
| `apex-infinite-cli/requirements-wrapper.txt` | Clarify optional wrapper and packaging dependency boundaries | ~20 |
| `apex-infinite-cli/README_apex-infinite-cli.md` | Update visual mode setup, run commands, packaging status, and productization doc links | ~45 |
| `apex-infinite-cli/docs/operator-runbook.md` | Update operator flow for source visual mode, settings, smoke, and failure recovery | ~45 |
| `apex-infinite-cli/docs/troubleshooting.md` | Add productized wrapper failure modes and recovery steps | ~45 |
| `apex-infinite-cli/docs/visual-wrapper-boundary.md` | Record Session 07 productization boundaries and release gates | ~35 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] Optional visual mode launches from source and consumes fixture or dry-run
      CLI events through the JSONL event boundary.
- [ ] Wrapper settings expose green CRT, amber CRT, IBM DOS, and plain presets
      plus effect intensity, font, scale, reduced-effects, and plain fallback
      controls.
- [ ] Missing CLI, missing PySide6, display-backend failure, malformed JSONL,
      subprocess stderr, non-zero exit, timeout, and stop states are visible
      product-facing states.
- [ ] Base CLI install and normal terminal execution remain free of PySide6,
      QML, graphical imports, and wrapper assets.
- [ ] Linux setup, packaging, release, license, checksum, source/relink, and
      troubleshooting instructions are documented before release verification.

### Testing Requirements

- [ ] Unit tests cover settings validation, preset selection, plain fallback,
      launcher command construction, missing CLI checks, timeout handling,
      stderr/return-code mapping, and duplicate start prevention.
- [ ] Focused wrapper tests cover malformed event input, fixture event flow,
      bridge state reset, productized controls, and import-guard behavior.
- [ ] Offscreen or display-backed wrapper smoke check passes, or the exact
      PySide6/display blocker is recorded in productization docs.
- [ ] Existing CLI tests remain passing.

### Non-Functional Requirements

- [ ] Wrapper source and docs contain no copied reference code, QML, shaders,
      assets, fonts, profile data, resource manifests, build scripts,
      terminal-emulator code, or literal effect formulas.
- [ ] Event payloads and wrapper logs exclude provider API keys, ANSI escapes,
      Rich markup, frame glyphs, visual-token storage, and copied reference
      identifiers.
- [ ] QML layout remains readable at supported desktop sizes with stable
      dimensions and no overlapping controls.
- [ ] Packaging docs preserve LGPLv3/commercial review gates before any binary
      distribution.

### Quality Gates

- [ ] All files ASCII-encoded
- [ ] Unix LF line endings
- [ ] Code follows project conventions
- [ ] Primary user-facing wrapper surface contains product-facing copy only
- [ ] Diagnostics remain in tests, docs, logs, or explicit failure surfaces

---

## 8. Implementation Notes

### Working Assumptions

- Productization should proceed instead of deferral: Session 06 validation
  passed, `visual-wrapper-spike.md` accepts PySide6/QML, and the analyzer
  marks Session 06 complete.
- Productization means source/dev visual mode plus packaging and release
  instructions, not publishing a binary in this session: Session 08 owns final
  release verification, and the spike record requires license and generated
  bundle review before binary distribution.
- Wrapper code remains under `apex-infinite-cli/apex_infinite_visual/`: the
  analyzer reports `monorepo: false`, while PRD and conventions identify
  `apex-infinite-cli/` as the active project area.

### Conflict Resolutions

- The UX PRD describes the Linux wrapper as a future optional visual mode,
  while the Phase 00 PRD, state, and stubs place spike and productization in
  Sessions 06 and 07. Current phase artifacts and analyzer state win, so this
  session productizes the Phase 00 wrapper path while keeping binary release
  gates explicit.
- Session 06 already added parser, launcher, import-guard, and fixture-flow
  tests. This session should not duplicate those unchanged spike tests; it
  should add productization coverage for settings, launch validation, bridge
  failure states, and packaging-facing behavior.

### Key Considerations

- Keep PySide6, QML, pyside6-deploy, Nuitka, and any wrapper smoke commands in
  the optional wrapper lane.
- Preserve `--event-stream - --machine-output` as the only stdout JSONL path
  for wrapper subprocess consumption.
- Keep base CLI prompt routing, manager decisions, SQLite schema, and stored
  history semantics unchanged.

### Potential Challenges

- PySide6 or offscreen display may be unavailable in some environments:
  Preserve lazy import guards and record exact smoke blockers if they occur.
- AppImage packaging may require generated files and license review: Document
  release gates and avoid checking in generated bundles during this session.
- Wrapper UI controls can become visually crowded: Use stable layout sizing,
  compact labels, and accessible controls without in-app implementation notes.

### Relevant Considerations

- [P01] **Optional wrapper obligations**: Document LGPLv3/commercial
  obligations, packaging notes, checksums, and license notices before release.
- [P01] **Wrapper as companion surface**: Launch or reuse the CLI workflow
  engine through the event boundary without forking workflow behavior.
- [P01] **Effect responsibility split**: True visual effects stay behind the
  optional wrapper boundary and do not affect the terminal CLI.
- [P00] **Raw durable facts only**: Events and storage must not contain Rich
  markup, ANSI escapes, secrets, frame glyphs, or visual snapshots.

### Behavioral Quality Focus

Checklist active: Yes
Top behavioral risks for this session:
- Wrapper subprocess resources can survive stop or error paths if cleanup is
  incomplete.
- User controls can trigger duplicate starts or stale state when the visual
  surface is revisited.
- Event and subprocess failures can become invisible if they only appear in
  stderr or tests instead of product-facing wrapper states.

---

## 9. Testing Strategy

### Unit Tests

- Test wrapper settings validation, preset selection, effect intensity bounds,
  font/scale bounds, and plain fallback behavior.
- Test launcher command construction, missing CLI validation, timeout handling,
  stderr and return-code failure mapping, and subprocess cleanup.
- Test bridge methods for duplicate start prevention, state reset, malformed
  event recovery, and productized settings controls.

### Integration Tests

- Run the existing CLI test suite from `apex-infinite-cli/` with
  `./.venv/bin/python -m pytest tests/ -v`.
- Add productization tests beside the existing visual wrapper spike tests.
- Run `pyside6-qmllint` against `apex_infinite_visual/qml/Main.qml` when the
  optional wrapper environment provides it.

### Runtime Verification

- Run an offscreen smoke check:
  `QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300`.
- Run a guarded launch smoke with `--launch-cli`, `--dry-run`, and
  `--max-iterations 1` when local environment supports it.

### Edge Cases

- Missing `apex_infinite.py` path.
- Missing PySide6.
- Headless or unsupported Qt platform backend.
- Malformed JSONL and unsupported event versions.
- Subprocess stderr without stdout, non-zero return code, timeout, and
  operator stop.
- Plain fallback and reduced effects enabled together.

---

## 10. Dependencies

### Other Sessions

- Depends on: `phase00-session01-config-and-renderer-boundary`,
  `phase00-session02-rich-operator-console`,
  `phase00-session03-subprocess-and-history-visibility`,
  `phase00-session04-event-stream-boundary`,
  `phase00-session05-docs-samples-and-runbooks`,
  `phase00-session06-linux-wrapper-spike`
- Depended by: `phase00-session08-release-verification`

---

## Next Steps

Run the `implement` workflow step to begin implementation.
