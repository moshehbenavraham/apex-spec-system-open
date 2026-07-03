# Session Specification

**Session ID**: `phase00-session05-docs-samples-and-runbooks`
**Phase**: 00 - Apex Infinite CLI Upgrade
**Status**: Complete
**Created**: 2026-07-03

---

## 1. Session Overview

This session turns the implemented Apex Infinite CLI operator experience into
complete user-facing documentation, deterministic samples, and runbook guidance.
It covers display flags, UI config, theme behavior, event-stream operation,
history display semantics, prompt-contract impact, fallback modes, and
clean-room visual boundaries.

It is next because the analyzer reports Phase 00 in progress, no active
session, and Sessions 01 through 04 complete. Session 05 is the earliest
unfinished candidate, and its stub depends on implemented UI, history,
subprocess, and event-stream behavior from the first four sessions.

The work stays documentation- and sample-focused. It must not reopen CLI
runtime behavior unless implementation uncovers a concrete documentation or
test failure. The main outcome is that operators and future wrapper developers
can understand the shipped terminal experience, machine-output boundary, and
license-safe visual direction without reading implementation code or reference
material directly.

---

## 2. Objectives

1. Complete README and deep-dive documentation for UI flags, config examples,
   built-in themes, custom themes, event streams, history display, and prompt
   contract impact.
2. Add deterministic ASCII-only transcripts or JSONL samples that demonstrate
   plain fallback, history display, and machine-readable event output without
   binary screenshots.
3. Update the operator runbook and troubleshooting docs for CI, logs, remote
   shells, constrained terminals, `NO_COLOR`, redirected output, `TERM=dumb`,
   non-UTF terminals, terminal width, and event-stream misuse.
4. Document the clean-room visual boundary, ignored `EXAMPLE/` tree, GPL-family
   reference status, PySide6/Qt Quick/QML wrapper direction, PyQt and terminal
   widget exclusions, and pywebview plus xterm.js backup option.
5. Verify documentation consistency, ASCII/LF encoding, no tracked binary
   screenshots or reference assets, and continued CLI/root test health.

---

## 3. Prerequisites

### Required Sessions

- [x] `phase00-session01-config-and-renderer-boundary` - Provides validated UI
      config, display flags, theme resolution, renderer injection, and raw
      history safety boundaries.
- [x] `phase00-session02-rich-operator-console` - Provides the shipped Rich,
      plain, ASCII, compact, and semantic operator-console surfaces to
      document.
- [x] `phase00-session03-subprocess-and-history-visibility` - Provides live
      subprocess visibility and history display semantics to document.
- [x] `phase00-session04-event-stream-boundary` - Provides the importable event
      API, `--event-stream`, `--machine-output`, stdout guardrails, and event
      contract to document.

### Required Tools Or Knowledge

- Current CLI options and config keys in `apex-infinite-cli/apex_infinite.py`,
  `apex-infinite-cli/apex_infinite_ui.py`, and
  `apex-infinite-cli/config.yaml`.
- Current event names and payload safety rules in
  `apex-infinite-cli/apex_infinite_events.py` and
  `apex-infinite-cli/docs/event-stream.md`.
- Phase 00 PRD, Session 05 stub, `CONVENTIONS.md`, `CONSIDERATIONS.md`, and
  `SECURITY-COMPLIANCE.md` documentation and clean-room requirements.
- Local reference evidence under ignored `EXAMPLE/cool-retro-term/` may be
  cited as study material only; implementation material and assets must not be
  copied.

### Environment Requirements

- CLI development environment with `apex-infinite-cli/.venv` or equivalent
  Python dependencies available for test verification.
- No provider API keys, real LLM calls, real Codex subprocess launches, or
  graphical runtime dependencies are required to create deterministic docs and
  samples.
- All authored docs and sample files remain ASCII-only with Unix LF endings.

---

## 4. Scope

### In Scope (MVP)

- Operator can discover and configure `auto`, `crt-green`, `crt-amber`,
  `ibm-dos`, and `plain` themes from README and runbook docs.
- Operator can understand `--plain`, `--ascii`, `--compact`, `--theme`,
  `--event-stream PATH`, `--event-stream -`, and `--machine-output` behavior
  without reading source code.
- README includes current UI config examples, CLI examples, event-stream
  examples, transcript links, and deep-dive documentation links.
- Operator runbook includes fallback guidance for CI, logs, remote shells,
  constrained terminals, `NO_COLOR`, redirected output, `TERM=dumb`, terminal
  width, and non-UTF terminals.
- History DB docs describe display-time status labels, truncation rules,
  verbose history behavior, and the raw SQLite storage boundary.
- Prompt contract docs clearly state whether UI and event-stream changes alter
  `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`,
  `build_codex_prompt()`, manager normalization, or known-command routing.
- Event-stream docs include current JSONL examples, machine-output guardrails,
  wrapper consumption guidance, and payload safety expectations.
- Troubleshooting docs cover unreadable colors, non-UTF terminals, terminal
  width, `NO_COLOR`, `TERM=dumb`, redirected output, remote shells, and
  event-stream misuse.
- Deterministic ASCII-only transcripts or JSONL samples are added under
  `apex-infinite-cli/docs/transcripts/`.
- Clean-room visual documentation identifies `EXAMPLE/` as ignored,
  reference-only, GPL-family study material and documents the no-copying rule.
- Wrapper direction docs identify PySide6/Qt Quick/QML as the selected optional
  Linux wrapper path, PyQt/qmltermwidget/QTermWidget exclusions, and pywebview
  plus xterm.js as a backup option.
- Root `docs/CREDITS.md` is aligned with the clean-room boundary where current
  wording conflicts with the PRD.

### Out Of Scope (Deferred)

- Productizing the Linux visual wrapper - Reason: Sessions 06 and 07 own spike
  and productization after documentation captures the boundary.
- Adding PySide6, Qt, PyQt, qmltermwidget, QTermWidget, webview, terminal
  emulator, shader, image, font, icon, or graphical dependencies to the base
  CLI - Reason: this is a documentation session and the base CLI remains
  terminal-only.
- Copying QML, shaders, source code, constants, images, icons, fonts, resource
  manifests, build scripts, terminal-emulator code, or profile data from
  reference material - Reason: clean-room no-copy boundary is mandatory.
- Reopening implemented UI, history, subprocess, event, prompt, or DB behavior
  without a concrete documentation or test failure - Reason: Sessions 01
  through 04 already implemented and validated those behaviors.
- Adding binary screenshots - Reason: repository examples must be deterministic
  ASCII text or JSONL.
- Changing `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, command
  normalization, `build_codex_prompt()`, SQLite schema, `cc_response`, or
  history retention behavior - Reason: documentation should describe the
  existing contract, not change it.

---

## 5. Technical Approach

### Architecture

Start with a documentation crosswalk from implemented behavior to user-facing
docs. Use the current CLI code, config, tests, Session 04 validation evidence,
and Phase 00 PRD as source of truth. Update docs to remove drift and duplicate
ambiguity instead of adding parallel explanations.

Create deterministic samples under `apex-infinite-cli/docs/transcripts/`.
Samples should be small, ASCII-only, and hand-verifiable against the documented
contract. They must not include real provider keys, real operator secrets,
binary screenshots, ANSI escapes, Rich markup, box glyphs, copied reference
assets, or live-only terminal control data.

Create a focused visual-wrapper boundary document instead of burying licensing
and clean-room details across multiple files. Link it from README, runbook,
event-stream docs, and troubleshooting where relevant. The document should cite
`EXAMPLE/` as ignored and local-only, name the excluded reference materials,
and prepare Sessions 06 and 07 to use the event stream rather than Rich output
or copied terminal assets.

Use documentation verification as the main quality gate: ASCII/LF checks,
cross-link checks, no binary screenshots or reference assets in tracked docs,
current test suites, and root script smoke checks. No production code changes
are expected unless docs reveal a failing contract.

### Design Patterns

- Behavior-to-doc crosswalk: every documented flag, config key, event mode, and
  history display claim maps to current code, tests, or validation evidence.
- Sample-as-contract: transcripts are deterministic examples of documented
  behavior, not screenshots or live terminal captures.
- Clean-room boundary: docs can credit conceptual inspiration while forbidding
  copied source, QML, shaders, assets, fonts, profile data, manifests, build
  scripts, and terminal-emulator code.
- Wrapper consumes events: future visual surfaces read JSONL events or the
  importable event API, never Rich frames or human terminal output.
- Verification-first docs: run encoding, link/reference, test, and repository
  hygiene checks before marking the session ready for implementation review.

---

## 6. Deliverables

### Files To Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/docs/visual-wrapper-boundary.md` | Clean-room visual boundary, ignored reference tree, optional wrapper direction, dependency/license notes, and exclusions | ~180 |
| `apex-infinite-cli/docs/transcripts/README_transcripts.md` | Index and usage notes for deterministic transcript and JSONL samples | ~80 |
| `apex-infinite-cli/docs/transcripts/dry-run-plain.txt` | ASCII-only plain/compact dry-run sample showing operator fallback output | ~90 |
| `apex-infinite-cli/docs/transcripts/history-ledger.txt` | ASCII-only history display sample showing compact and verbose semantics | ~90 |
| `apex-infinite-cli/docs/transcripts/machine-output-events.jsonl` | Deterministic JSONL event sample for machine-output consumers | ~12 |

### Files To Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `apex-infinite-cli/README_apex-infinite-cli.md` | Complete UI flag/config/theme examples, event-stream examples, transcript links, deep-dive docs, and wrapper boundary links | ~140 |
| `apex-infinite-cli/docs/operator-runbook.md` | Add theme selection, fallback-mode, CI/log, remote-shell, event-stream, and sample-use guidance | ~140 |
| `apex-infinite-cli/docs/event-stream.md` | Cross-link JSONL sample, wrapper guidance, stdout isolation, and no-Rich-parsing boundary | ~80 |
| `apex-infinite-cli/docs/history-db.md` | Document display-time status labels, truncation, verbose history behavior, raw storage, and sample links | ~80 |
| `apex-infinite-cli/docs/prompt-contract.md` | Confirm UI/event docs do not change prompt routing and document wrapper/event observation boundary | ~60 |
| `apex-infinite-cli/docs/troubleshooting.md` | Add fallback rendering, terminal width, non-UTF terminal, remote shell, redirected output, and event-stream misuse fixes | ~120 |
| `docs/CREDITS.md` | Replace conflicting direct-code wording with clean-room conceptual-inspiration wording | ~20 |

---

## 7. Success Criteria

### Functional Requirements

- [ ] README documents all current display flags, built-in themes, custom theme
      config, event-stream modes, and relevant examples.
- [ ] Operator runbook gives concrete mode choices for interactive terminals,
      CI/logs, remote shells, constrained terminals, `NO_COLOR`, redirected
      output, and `TERM=dumb`.
- [ ] Event-stream docs and JSONL sample describe file mode and
      `--event-stream - --machine-output` without implying wrappers parse Rich
      output.
- [ ] History DB docs describe display-time labels, truncation, verbose output,
      and raw SQLite storage without implying schema changes.
- [ ] Prompt-contract docs state that UI and event-stream behavior do not
      change manager prompts, summarizer prompts, command normalization, or
      `build_codex_prompt()`.
- [ ] Clean-room docs identify `EXAMPLE/` as ignored, reference-only, and
      GPL-family study material with a no-copying rule.
- [ ] Wrapper direction docs identify PySide6/Qt Quick/QML as optional Linux
      wrapper path, PyQt/qmltermwidget/QTermWidget exclusions, and pywebview
      plus xterm.js as backup only.

### Testing Requirements

- [ ] Existing CLI pytest suite passes.
- [ ] Root Bats suite passes.
- [ ] Root script smoke checks pass.
- [ ] Documentation and transcript files pass ASCII-only and LF-only checks.
- [ ] Verification confirms no binary screenshots or copied reference assets
      are tracked in docs or CLI examples.

### Non-Functional Requirements

- [ ] Documentation is accurate to implemented code and validation evidence.
- [ ] Samples contain no provider API keys, personal data, ANSI escapes, Rich
      markup, frame glyphs, binary data, or reference assets.
- [ ] The base CLI remains free of graphical runtime dependencies.
- [ ] Clean-room language is consistent across README, runbook, visual-wrapper
      boundary docs, and credits.

### Quality Gates

- [ ] All files ASCII-encoded.
- [ ] Unix LF line endings.
- [ ] Documentation follows project conventions and uses fenced code blocks
      with language tags for code examples.
- [ ] No generated plugin payloads under `plugins/apex-spec/skills/apex-spec/`
      are edited.
- [ ] Root skill packaging sync check remains clean.

---

## 8. Implementation Notes

### Working Assumptions

- Session 05 is the next executable session: the analyzer reports no active
  session, Phase 00 in progress, Sessions 01 through 04 complete, and
  `session_05_docs_samples_and_runbooks.md` as the first unfinished candidate.
  Planning can proceed because the stub prerequisites are satisfied by
  completed session IDs and validation artifacts.
- This session should be documentation-first, not runtime-first: Session 05
  scope says to document implemented behavior and explicitly defers reopening
  UI behavior unless a concrete documentation or test failure is found.
  Planning can proceed with documentation and sample deliverables as the main
  work.
- Deterministic transcripts can be authored from fixture-style output instead
  of a live provider run: the stub allows fixture or dry-run output, and the
  security posture forbids leaking provider keys or real operator-sensitive
  text.

### Conflict Resolutions

- `docs/CREDITS.md` currently says `cool-retro-term` provided direct
  influence/code examples, while the PRD, Session 05 stub, and security record
  require clean-room visual translation and forbid copied reference material.
  The chosen interpretation is the PRD/stub/security boundary: update credits
  to acknowledge conceptual inspiration without implying code copying.

### Key Considerations

- Session 04 already created core event-stream docs. This session should
  consolidate and cross-link them, not duplicate conflicting event contracts.
- Root `EXAMPLE/` is ignored by `.gitignore`, but docs must still make clear
  that ignored local reference material is not a runtime dependency and must
  not be copied.
- Documentation should describe the selected wrapper direction for future
  sessions without productizing the wrapper in this session.

### Potential Challenges

- Documentation drift from implemented flags or event names: mitigate by
  checking current Click options, UI config keys, event names, and tests before
  editing docs.
- Accidentally implying screenshots or visual assets are tracked deliverables:
  mitigate by using only text transcripts and JSONL samples under
  `apex-infinite-cli/docs/transcripts/`.
- Clean-room wording becoming too vague for future sessions: mitigate by naming
  explicit forbidden material categories and the event-stream consumption
  boundary.

### Relevant Considerations

- [P00] **Prompt contract coupling**: Keep docs explicit that prompt functions
  and routing did not change unless implementation proves otherwise.
- [P00] **History compatibility**: Describe history display as render-time
  behavior over raw rows and preserve the legacy `cc_response` column.
- [P00] **Base runtime dependency control**: Document optional wrapper
  dependencies without adding them to the base CLI path.
- [P00] **Raw durable facts only**: Samples and docs must keep history and event
  payloads raw, without Rich markup, ANSI escapes, visual tokens, secrets, or
  frame glyphs.
- [P00] **Clean-room visual translation**: Treat the reference project as a
  concept checklist only and document no-copy categories.
- [P00] **Docs move with behavior**: README, runbook, history DB docs,
  troubleshooting, event-stream docs, and prompt-contract docs should reflect
  the current shipped behavior together.

---

## 9. Testing Strategy

### Unit Tests

- Run the full existing CLI pytest suite from `apex-infinite-cli/` to confirm
  prompt, UI config, renderer, history, subprocess, and event-stream contracts
  remain green.

### Integration Tests

- Run root Bats tests and script smoke checks to confirm spec-system scripts
  and packaging checks remain healthy after documentation changes.

### Runtime Verification

- Inspect README, runbook, event-stream docs, history DB docs, prompt-contract
  docs, troubleshooting, transcripts, and visual-wrapper boundary docs for
  consistent flag names, event modes, clean-room language, and links.
- Confirm no tracked binary screenshots, copied reference assets, copied
  shaders, copied QML, copied fonts, copied icons, or copied resource manifests
  were added.

### Edge Cases

- `NO_COLOR`, `TERM=dumb`, redirected output, non-TTY output, remote shells,
  non-UTF terminals, and narrow terminal width are documented with fallback
  guidance.
- `--event-stream -` without `--machine-output` and `--machine-output` without
  `--event-stream` are documented as invalid combinations.
- Prompt-contract docs do not imply event-stream or wrapper behavior changes
  manager routing.

---

## 10. Dependencies

### Other Sessions

- Depends on: `phase00-session01-config-and-renderer-boundary`,
  `phase00-session02-rich-operator-console`,
  `phase00-session03-subprocess-and-history-visibility`,
  `phase00-session04-event-stream-boundary`.
- Depended by: `phase00-session06-linux-wrapper-spike`,
  `phase00-session07-linux-visual-wrapper-productization`,
  `phase00-session08-release-verification`.

---

## Next Steps

Session complete. Run the `plansession` workflow step to scope Session 06.
