# Apex Infinite CLI - Product Requirements Document

## Overview

Apex Infinite CLI is the autonomous OpenAI Codex CLI session manager inside the Apex Spec System repository. It runs initialized Apex Spec projects through the staged workflow loop by asking a manager LLM for the next action, executing Codex CLI, storing history in SQLite, and repeating until the workflow reaches completion or a safety stop.

The current CLI already supports provider configuration, `codex exec` subprocess calls, history storage, dry runs, operator interrupts, and prompt/routing tests. This PRD focuses the Apex Spec System development workflow on evolving that `apex-infinite-cli/` subproject into a polished, testable operator console while preserving the existing autonomous workflow contract.

The near-term product direction is a Rich-based terminal experience with explicit plain-output fallbacks, then a raw lifecycle event boundary for future visual surfaces. A later Linux visual wrapper may build on that event boundary, but the base CLI must remain lightweight, scriptable, and safe for headless operation.

## Goals

1. Preserve the autonomous Apex Spec workflow loop, including manager decisions, `Next command:` handoffs, Codex execution, history logging, and stop conditions.
2. Improve the interactive operator experience with a cohesive terminal UI that remains readable during long-running autonomous sessions.
3. Add explicit, validated UI configuration and CLI flags for themes, plain output, ASCII output, compact output, and event streaming.
4. Maintain backward compatibility for existing `~/.apex-infinite/history.db` files and prompt/routing behavior.
5. Provide a raw lifecycle event stream that future visual surfaces can consume without scraping terminal output.
6. Explore a standalone Linux visual wrapper as an optional companion surface without adding graphical dependencies to the base CLI.

## Non-Goals

- Replacing Codex CLI or changing the Apex Spec staged workflow.
- Rewriting the manager or summarizer prompt contract unless a scoped session explicitly changes prompt behavior and updates tests and docs together.
- Requiring `cool-retro-term`, qmltermwidget, QTermWidget, PyQt, an external terminal emulator, or a graphical display for normal CLI use.
- Copying `cool-retro-term` code, QML, shaders, images, icons, fonts, resource manifests, profile data, or build scripts.
- Migrating or renaming the legacy SQLite `cc_response` column.
- Shipping macOS or Windows visual-wrapper support in this project.
- Broadly rebuilding the root Apex Spec skill package except where CLI integration docs or command routing require it.

## Users and Use Cases

### Primary Users

- **Operator**: Runs Apex Infinite CLI against initialized projects and needs clear progress, errors, history, and safe interruption.
- **Apex Spec maintainer**: Develops and verifies the CLI, command prompts, docs, tests, and release artifacts.
- **Automation environment**: Runs the CLI in dry-run, redirected, non-TTY, CI, log-file, or headless contexts where stable plain output matters.
- **Future visual wrapper developer**: Builds optional UI surfaces from raw lifecycle events without depending on Rich output internals.

### Key Use Cases

1. Operator starts or resumes an autonomous Apex Spec workflow for a target project with optional starting command and CEO instruction.
2. Operator runs dry-run mode to confirm provider, model, Codex binary, and generated prompt before executing Codex.
3. Operator monitors a long-running Codex subprocess with clear elapsed-time, timeout, error, and completion states.
4. Operator inspects recent history for a project and expands detail with `--verbose`.
5. Automation runs the CLI with plain or ASCII output and receives deterministic logs without styled control data.
6. Future wrapper consumes JSONL lifecycle events and renders its own display without scraping terminal frames.

## Requirements

### MVP Requirements

- Operator can configure provider, model, Codex binary, Codex exec flags, and reasoning effort through `config.yaml` and supported CLI overrides.
- Operator can start the autonomous loop with a project path, starting command, CEO instruction, dry-run mode, verbose mode, history mode, and max-iteration safety limit.
- Manager LLM can route known Apex Spec workflow commands from structured JSON output, slash-prefixed command output, or normalized text output.
- Manager LLM can pass unknown output through as raw high-level instructions to Codex CLI.
- CLI can execute `codex exec` with configured flags and preserve stdout, stderr, return code, timeout, missing-binary, and generic-exception behavior.
- CLI can write one SQLite history row per iteration using WAL mode and a normalized project path key.
- CLI can show a compact project history ledger and expand row detail when `--verbose` is used.
- Operator can select built-in UI modes for `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and `plain`.
- Operator can use `--plain`, `--ascii`, `--compact`, and `--theme` overrides without editing config.
- CLI can resolve UI settings with deterministic precedence: CLI flags, environment constraints, config, then built-in defaults.
- CLI can choose plain output by default under `NO_COLOR`, `TERM=dumb`, non-TTY output, redirected output, or non-terminal Console paths.
- CLI can fail fast on invalid theme names or malformed custom theme configuration with clear Click or config errors.
- CLI can render startup, iteration, manager decision, prompt, Codex execution, result, DB log, help, completion, timeout, and error states through centralized renderer helpers.
- CLI can keep ANSI escapes, Rich markup, box glyphs, and styled output out of SQLite history rows.
- Developer can test renderer behavior with injected Rich `Console(record=True, width=...)` objects.
- Developer can verify config parsing, Click flags, prompt routing, subprocess behavior, history rendering, plain mode, `NO_COLOR`, and non-TTY behavior through pytest.
- CLI can emit opt-in line-buffered JSONL lifecycle events to `--event-stream PATH` without changing normal human output.
- Developer can import an event emitter API for tests and future wrappers.

### Deferred Requirements

- Operator can launch a standalone Linux visual wrapper that uses the Python CLI as the workflow engine.
- Operator can control wrapper theme, effect intensity, font, scaling, and plain fallback without affecting base CLI behavior.
- Future wrapper can demonstrate glow, curvature, flicker, phosphor trails, and scanline overlays that Rich cannot faithfully render.
- Developer can package PySide6/Qt Quick/QML wrapper dependencies as an optional extra separate from base CLI installation.
- Developer can document pywebview plus xterm.js as a backup if a true terminal-emulator viewport becomes mandatory.

## Non-Functional Requirements

- **Performance**: Startup config loading and history rendering for 50 rows must complete in under 2 seconds on a local development machine, excluding network LLM calls and Codex subprocess runtime.
- **Security**: API keys must be loaded from environment-backed config values and must not be printed, written to SQLite history, or emitted in JSONL events in normal operation.
- **Privacy**: SQLite history and JSONL events must store raw workflow facts only; tests must verify 0 Rich markup strings and 0 ANSI escape sequences are stored.
- **Reliability**: Existing prompt/routing tests must remain green, and new subprocess tests must cover success, stderr-only output, non-zero exit, timeout, dry-run, and missing binary paths.
- **Accessibility**: Plain and ASCII modes must avoid non-ASCII frame glyphs and remain readable at 80, 100, and 120 terminal columns.
- **Compatibility**: Existing `~/.apex-infinite/history.db` files must remain readable without migration, and the legacy `cc_response` column must remain intact.
- **Portability**: Base CLI must run on Python 3.10+ with terminal-only dependencies and no graphical runtime dependency.
- **Maintainability**: Renderer, config, event, subprocess, DB, and prompt-routing changes must have focused tests before a session is validated.

## Constraints and Dependencies

- The base CLI runtime is Python 3.10+.
- The base CLI depends on Click, Rich, OpenAI Python SDK, python-dotenv, PyYAML, SQLite from the Python standard library, and Codex CLI.
- Development verification uses pytest, pytest-cov, pytest-mock, black, and pylint.
- The root Apex Spec scripts remain bash + jq only; do not add Python dependencies to root scripts.
- The project uses ASCII-only authored files with Unix LF line endings.
- The repository has no formal workspace manager config; CLI sessions should
  target `apex-infinite-cli/` by path rather than by monorepo package metadata.
- `EXAMPLE/cool-retro-term` is reference-only and ignored by Git.
- `cool-retro-term` material is GPL-family reference material; product work must use clean-room visual translation only.
- PySide6/Qt Quick/QML is allowed only for an optional Linux visual wrapper path, with LGPLv3/commercial obligations documented.
- PyQt, qmltermwidget, QTermWidget, copied QML, copied shaders, copied assets, copied fonts, and copied terminal-emulator code are excluded unless a future explicit decision changes scope.
- The CLI must preserve existing prompt contract behavior unless `apex_infinite.py`, tests, README, and prompt-contract docs are updated together.

## Phases

This system delivers the product via phases. Each phase is implemented via multiple 2-4 hour sessions (12-25 tasks each).

| Phase | Name | Sessions | Status |
|-------|------|----------|--------|
| 00 | Apex Infinite CLI Upgrade | 8 | In Progress |

## Phase 00: Apex Infinite CLI Upgrade

### Objectives

1. Centralize Rich rendering and UI configuration without changing workflow behavior.
2. Deliver the first complete CRT-inspired terminal operator experience with robust plain-output fallbacks.
3. Improve live subprocess visibility and history readability while preserving captured output semantics.
4. Document and test the UI upgrade, then expose a raw event stream for future wrappers.
5. Spike and productize the optional Linux visual wrapper without adding graphical dependencies to the base CLI.
6. Verify the complete upgrade against compatibility, testing, documentation, release, and clean-room criteria.

### Sessions

Session stubs are defined under `.spec_system/PRD/phase_00/`.

| Session | Name | Source Theme |
|---------|------|--------------|
| 01 | Config And Renderer Boundary | UI architecture and theme tokens |
| 02 | Rich Operator Console | CRT-inspired operator console |
| 03 | Subprocess And History Visibility | Live execution and better history |
| 04 | Event Stream Boundary | Engine boundary and event stream |
| 05 | Docs Samples And Runbooks | Documentation, samples, and polish |
| 06 | Linux Wrapper Spike | Linux visual wrapper spike |
| 07 | Linux Visual Wrapper Productization | Linux visual wrapper productization |
| 08 | Release Verification | Release verification |

## Technical Stack

- Python 3.10+ - base CLI runtime and standard library support.
- Click - command-line parser and validation layer.
- Rich - terminal rendering, panels, tables, status, and testable recorded consoles.
- SQLite WAL - local interaction history at `~/.apex-infinite/history.db`.
- OpenAI-compatible API client - manager and summarizer LLM calls.
- python-dotenv and PyYAML - environment expansion and YAML config loading.
- Codex CLI - autonomous agent execution through `codex exec`.
- pytest, pytest-mock, pytest-cov - automated verification.
- black and pylint - formatting and linting for Python code.
- PySide6 with Qt Quick/QML - optional deferred Linux visual wrapper path.

## Success Criteria

- [ ] Existing prompt/routing behavior remains compatible and covered by tests.
- [ ] CLI users can enable `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and `plain` themes.
- [ ] CLI users can disable styling with `--plain` and avoid non-ASCII glyphs with `--ascii`.
- [ ] Plain output is selected automatically for constrained terminal environments unless explicitly overridden.
- [ ] History display is readable without horizontal scrolling at 80 columns.
- [ ] SQLite history rows remain raw and backward compatible with existing databases.
- [ ] JSONL event stream emits raw lifecycle facts without Rich markup.
- [ ] README and deep-dive docs describe UI flags, config, event stream, and troubleshooting.
- [ ] No reference source, shader, image, icon, font, resource manifest, or literal profile data is copied into the CLI.
- [ ] Optional Linux wrapper path has documented dependency, license, packaging, and interface boundaries.

## Risks

- **Retro styling reduces readability**: Keep contrast high, effects low by default, and provide `--plain`, `--ascii`, and compact modes.
- **Terminal compatibility varies**: Respect `NO_COLOR`, `TERM=dumb`, non-TTY output, redirected output, and common terminal widths.
- **Styled output pollutes durable records**: Store raw workflow data only and test for 0 ANSI or Rich markup in SQLite and event payloads.
- **Live subprocess display changes behavior**: Preserve current stdout, stderr, return code, timeout, and verbose semantics with subprocess tests.
- **Dependency creep slows base CLI use**: Finish Rich milestones first and keep wrapper dependencies optional.
- **GPL contamination concerns**: Use `cool-retro-term` only as visual reference and document no-copy boundaries.
- **Wrapper diverges from CLI behavior**: Keep one workflow engine and make the wrapper a display/runtime shell over JSONL events.
- **Single-file CLI becomes harder to maintain**: Split renderer, config, event, DB, or subprocess helpers when that lowers risk versus extending `apex_infinite.py`.

## Assumptions

- The master PRD scope is Apex Infinite CLI development inside the Apex Spec System repository: the user requested `createprd apex-infinite-cli`, README identifies `apex-infinite-cli/` as the autonomous session manager, and the Phase 00 PRD plus session stubs contain the folded CLI upgrade plan.
- The repository should be treated as a single repo with a primary subproject path: the user named `apex-infinite-cli` as the focus, while local tooling has no workspace manager config.
- Prompt routing should remain stable during UI work: `docs/apex-infinite-cli/prompt-contract.md` and the upgrade plan both require prompt changes to be made only with matching tests and docs.
- `cool-retro-term` is inspiration only: the upgrade plan records GPL/license boundaries and forbids copying source, shader, asset, font, or profile data.

### Conflict Resolutions

- No workspace config exists, but the user explicitly named `apex-infinite-cli` as the development focus. The chosen interpretation is single-repo planning with CLI sessions scoped by path, not formal monorepo package metadata.
- Visual direction references `cool-retro-term`, while license boundaries forbid copying. The chosen interpretation is clean-room visual translation: use concepts such as terminal mood, status hierarchy, and effect categories while creating independent tokens, code, docs, and assets.

## Open Decisions

1. Decide after the wrapper spike whether Session 07 productization should proceed with PySide6/QML or document a blocker and defer.
2. Decide the first Linux wrapper release artifact format after dependency and packaging evidence is gathered.
3. Decide whether a true terminal-emulator viewport becomes mandatory; if it does, evaluate the documented pywebview plus xterm.js backup path.
