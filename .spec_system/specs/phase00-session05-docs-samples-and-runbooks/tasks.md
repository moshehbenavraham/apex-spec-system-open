# Task Checklist

**Session ID**: `phase00-session05-docs-samples-and-runbooks`
**Total Tasks**: 20
**Estimated Duration**: 3-4 hours
**Created**: 2026-07-03

---

Legend: `[x]` completed; `[ ]` pending; `[P]` parallelizable; `[SNNMM]` session ref; `TNNN` task ID.

---

## Setup (4 tasks)

- [x] T001 [S0005] Verify analyzer state, Sessions 01 through 04 validation evidence, and Session 05 stub prerequisites before editing documentation (`.spec_system/specs/phase00-session04-event-stream-boundary/validation.md`)
- [x] T002 [S0005] Audit current README and deep-dive docs against implemented flags, config keys, themes, event names, history behavior, prompt contract, and troubleshooting needs (`apex-infinite-cli/README_apex-infinite-cli.md`, `apex-infinite-cli/`)
- [x] T003 [S0005] Resolve clean-room documentation evidence by checking `.gitignore`, Phase 00 PRD boundaries, Session 05 reference notes, local `EXAMPLE/` availability, and conflicting credits wording (`docs/CREDITS.md`)
- [x] T004 [S0005] Create the deterministic samples directory and transcript index with usage rules for ASCII text, JSONL, no secrets, and no binary screenshots (`apex-infinite-cli/docs/transcripts/README_transcripts.md`)

---

## Foundation (4 tasks)

- [x] T005 [S0005] [P] Create the visual wrapper boundary doc covering ignored `EXAMPLE/`, GPL-family reference status, no-copy categories, PySide6/Qt Quick/QML direction, PyQt/qmltermwidget/QTermWidget exclusions, and pywebview plus xterm.js backup (`apex-infinite-cli/docs/visual-wrapper-boundary.md`)
- [x] T006 [S0005] [P] Create a deterministic plain/ASCII dry-run transcript covering startup, theme resolution, prompt preview, dry-run execution, and safety-stop visibility without ANSI escapes or Rich markup (`apex-infinite-cli/docs/transcripts/dry-run-plain.txt`)
- [x] T007 [S0005] [P] Create a deterministic history transcript covering compact ledger labels, truncation behavior, verbose detail expansion, and raw-storage boundaries (`apex-infinite-cli/docs/transcripts/history-ledger.txt`)
- [x] T008 [S0005] [P] Create a deterministic machine-output JSONL sample covering startup, UI resolution, prompt dispatch, dry-run event, DB log, and stop events with one JSON object per line (`apex-infinite-cli/docs/transcripts/machine-output-events.jsonl`)

---

## Implementation (8 tasks)

- [x] T009 [S0005] Update README display documentation for UI config, built-in themes, custom theme overrides, CLI display flags, event-stream usage, transcript links, wrapper boundary links, and deep-dive doc navigation (`apex-infinite-cli/README_apex-infinite-cli.md`)
- [x] T010 [S0005] Update the operator runbook with theme selection, plain/ASCII/compact guidance, CI/log usage, remote shell guidance, constrained terminal fallbacks, event-stream operating modes, and sample references (`apex-infinite-cli/docs/operator-runbook.md`)
- [x] T011 [S0005] Update the event-stream contract with transcript links, wrapper consumption guidance, stdout isolation rules, payload safety notes, and explicit no-Rich-parsing language (`apex-infinite-cli/docs/event-stream.md`)
- [x] T012 [S0005] Update the history DB reference with render-time status labels, truncation rules, verbose output semantics, raw SQLite storage boundaries, and transcript links (`apex-infinite-cli/docs/history-db.md`)
- [x] T013 [S0005] Update the prompt contract to confirm UI, history display, event-stream, machine-output, and wrapper documentation do not change manager prompts, summarizer prompts, routing normalization, or `build_codex_prompt()` (`apex-infinite-cli/docs/prompt-contract.md`)
- [x] T014 [S0005] Update troubleshooting for unreadable colors, non-UTF terminals, narrow terminal width, `NO_COLOR`, `TERM=dumb`, redirected output, remote shells, event-stream misuse, and wrapper-consumption mistakes (`apex-infinite-cli/docs/troubleshooting.md`)
- [x] T015 [S0005] Update credits to acknowledge `cool-retro-term` as conceptual visual inspiration without implying copied code, assets, shaders, QML, fonts, profiles, manifests, or build scripts (`docs/CREDITS.md`)
- [x] T016 [S0005] Cross-link the README, runbook, event-stream docs, troubleshooting guide, transcript index, and visual wrapper boundary so operators and wrapper developers can navigate the complete documentation set (`apex-infinite-cli/README_apex-infinite-cli.md`, `apex-infinite-cli/`)

---

## Testing (4 tasks)

- [x] T017 [S0005] Run ASCII-only and LF-only checks over all changed README, docs, transcript, and session artifact files (`apex-infinite-cli/README_apex-infinite-cli.md`, `docs/`, `.spec_system/specs/phase00-session05-docs-samples-and-runbooks/`)
- [x] T018 [S0005] Verify no binary screenshots, copied reference assets, copied shaders, copied QML, copied fonts, copied icons, copied resource manifests, or copied build scripts are tracked in the documentation deliverables (`apex-infinite-cli/`, `apex-infinite-cli/README_apex-infinite-cli.md`)
- [x] T019 [S0005] Run the full CLI pytest suite to confirm prompt, UI config, renderer, history, subprocess, and event-stream contracts remain green (`cd apex-infinite-cli && ./.venv/bin/python -m pytest tests/ -v`)
- [x] T020 [S0005] Run root workflow verification for script tests, plugin payload sync, project analysis, prerequisite checks, and whitespace hygiene (`bats tests/ && bash scripts/sync-plugin-payload.sh --check && bash scripts/analyze-project.sh --json | jq . && bash scripts/check-prereqs.sh --json --env | jq . && git diff --check`)

---

## Completion Checklist

- [x] All tasks marked `[x]`
- [x] All tests and checks passing
- [x] All files ASCII-encoded with LF line endings
- [x] implementation-notes.md updated
- [x] Session marked complete by `updateprd`

---

## Next Steps

Session complete. Run the `plansession` workflow step to scope Session 06.
