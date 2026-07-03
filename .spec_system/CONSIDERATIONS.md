# Considerations

> Institutional memory for AI assistants. Updated between phases via carryforward.
> **Line budget**: 600 max | **Last updated**: Phase 00 (2026-07-03)

---

## Active Concerns

Items requiring attention in upcoming phases. Review before each session.

### Technical Debt
<!-- Max 5 items -->

- [P00] **Single-file CLI pressure**: `apex-infinite-cli/apex_infinite.py` still owns Click, config loading, LLM calls, SQLite, notifications, and workflow orchestration. Extract helpers only when the split lowers risk and has focused tests.
- [P00] **Prompt contract coupling**: Do not change `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or `build_codex_prompt()` unless prompt tests, README, and prompt-contract docs move in the same session.
- [P00] **History retention gap**: Local SQLite history keeps raw agent output, operator instructions, project paths, decisions, and timestamps without retention, purge, or redaction behavior.
- [P00] **Autonomous execution controls**: Real runs can execute broad Codex approval flags against a target project. Future work should make target path, provider, model, and execution flags explicit before non-dry-run loops.
- [P00] **History compatibility**: Existing `~/.apex-infinite/history.db` files must remain readable without migration. Preserve the legacy `cc_response` column, normalized project path keys, and raw workflow facts.

### External Dependencies
<!-- Max 5 items -->

- [P00] **Provider and Codex prerequisites**: Provider API keys, local provider availability, and the configured Codex binary are runtime prerequisites. Never print, store, or emit API keys in history, events, docs, or tests.
- [P00] **Dependency governance**: Session 08 passed local `pip-audit`, but the CLI still lacks lockfiles or recurring CI/scheduled vulnerability scanning for base, dev, and wrapper requirements.
- [P00] **Optional wrapper obligations**: PySide6/Qt Quick/QML belongs only in the optional Linux visual wrapper path, with LGPLv3/commercial obligations, generated-bundle review, notices, checksums, and source/relink materials before binary release.
- [P00] **Terminal-widget exclusions**: PyQt, qmltermwidget, QTermWidget, copied terminal-emulator code, and embedded pseudo-terminal behavior remain out of scope unless a later explicit decision changes the wrapper architecture.

### Performance / Security
<!-- Max 5 items -->

- [P00] **Raw durable facts only**: SQLite rows and JSONL events must contain operational facts only: no ANSI escapes, Rich markup, frame glyphs, visual tokens, secrets, copied-reference identifiers, or renderer snapshots.
- [P00] **Machine-output isolation**: Writing event JSONL to stdout is valid only with `--machine-output`; never mix JSONL with Rich or plain human output on stdout.
- [P00] **Provider transfer disclosure**: Recent history, latest agent output, summaries, and operator instructions can be sent to the configured LLM provider. Document this clearly before broader release.
- [P00] **Non-TTY control-byte safety**: Redirected, non-TTY, plain, ASCII, compact, event, and wrapper paths must be checked for live-only terminal controls, including notification paths outside the renderer.
- [P00] **Binary release gate**: The optional Linux wrapper is source-shippable only. Any AppImage/binary artifact needs artifact-specific license, notice, checksum, source/relink, and bundle review.

### Architecture
<!-- Max 5 items -->

- [P00] **Renderer boundary ownership**: Startup, iteration frames, manager decisions, prompt previews, execution results, DB notices, history, interrupts, and completion should continue through renderer helpers with injected `Console` support.
- [P00] **Event stream is the wrapper contract**: Visual surfaces must consume the importable emitter or line-buffered JSONL events, not scrape Rich/plain human output or parse terminal frames.
- [P00] **Wrapper as companion surface**: The Linux visual wrapper must launch or reuse the CLI workflow engine through the event boundary and must not fork manager decisions, prompt routing, storage, or safety behavior.
- [P00] **Clean-room visual translation**: Treat retro styling as conceptual requirements only. Do not copy code, QML, shaders, constants, assets, fonts, profiles, resource manifests, icons, build scripts, or terminal-emulator material.
- [P00] **Effect responsibility split**: Rich covers color, labels, layout, framing, status hierarchy, and low-fidelity separators. Glow, curvature, flicker, burn-in trails, RGB shift, and shader-like effects stay behind the optional wrapper boundary.

---

## Lessons Learned

Proven patterns and anti-patterns. Reference during implementation.

### What Worked
<!-- Max 15 items -->

- [P00] **Renderer-only snapshots**: Passing raw workflow facts to renderer snapshot objects enriched output while preserving prompt routing, subprocess behavior, SQLite rows, and tests.
- [P00] **Semantic labels over color**: Stable text labels such as `BOOT`, `ITERATION`, `DECISION`, `DRY RUN`, `LOGGED`, and `STOP` keep critical state visible in plain, ASCII, compact, `NO_COLOR`, and non-TTY modes.
- [P00] **Render-time history summaries**: History readability improved without schema migration by deriving labels, summaries, and truncation at display time only.
- [P00] **Event side channel**: JSONL lifecycle events stayed stable because they observe raw lifecycle facts instead of rendered terminal output.
- [P00] **Guarded machine stdout**: Requiring `--machine-output` for `--event-stream -` kept machine JSONL separate from human rendering and notification output.
- [P00] **Deterministic text fixtures**: ASCII transcripts and JSONL samples are easier to review, diff, and release-check than screenshots or ANSI captures.
- [P00] **Central clean-room boundary**: One visual-wrapper boundary document reduced drift across docs, tests, wrapper implementation, release checks, and license posture.
- [P00] **Optional wrapper lane**: Keeping PySide6/QML in `requirements-wrapper.txt` preserved headless/base CLI behavior while allowing source-mode wrapper productization.
- [P00] **Python-owned wrapper controls**: Validated Python settings, launcher behavior, and event adaptation made QML a display layer rather than a second workflow engine.
- [P00] **Release ledger mapping**: Mapping each PRD criterion to commands, inspections, focused fixes, or explicit gates made release verification auditable and concise.

### What to Avoid
<!-- Max 10 items -->

- [P00] **Styled storage pollution**: Do not persist Rich markup, ANSI escapes, frame glyphs, truncation text, or display-only labels to SQLite or event payloads.
- [P00] **Scraping human output**: Wrappers and automation must not parse Rich frames, plain terminal text, or SQLite history when the JSONL/API event boundary exists.
- [P00] **Decorative opacity**: Do not let retro styling hide manager reasons, prompts, captured output, errors, completion state, or handoff information.
- [P00] **Graphical base install**: Do not make terminal CLI users install Qt, PySide6, PyQt, terminal widgets, image assets, shader assets, or display-server dependencies.
- [P00] **Raw stderr in product UI**: Product-facing wrapper failures should expose safe summaries and state labels, not raw subprocess stderr as UI text.
- [P00] **Binary release by implication**: Source-shippable wrapper status does not make AppImage/binary publication ready; complete artifact-specific legal and packaging gates first.
- [P00] **Prompt drift during UI work**: Do not edit manager routing text to support display-only concerns; use renderer/event metadata instead.

### Tool/Library Notes
<!-- Max 5 items -->

- [P00] **Rich**: Use injected consoles and width-specific records for tests; keep plain and ASCII renderers free of box-drawing glyphs and live-only output.
- [P00] **Click**: Use `CliRunner` coverage for new flags, invalid theme values, config precedence, and incompatible event-output combinations.
- [P00] **SQLite**: Use temporary DB paths or monkeypatched `DB_DIR`/`DB_PATH` in tests; cover empty, sparse legacy, short, and long history rows.
- [P00] **JSONL events**: Serialize with ASCII-safe JSON, validate payload types and unsafe strings, flush line-by-line, and keep event names importable for tests.
- [P00] **PySide6/QML**: Keep imports wrapper-only, run offscreen smoke and QML lint, and validate settings in Python before values reach QML.

---

## Resolved

Recently closed items (buffer - rotates out after 2 phases).

| Phase | Item | Resolution |
|-------|------|------------|
| P00 | UI config gap | Added validated UI settings, built-in/custom themes, CLI overrides, and environment-aware fallback behavior. |
| P00 | Subprocess visibility gap | Added renderer-facing process state, timeout cleanup coverage, compact history, and preserved stdout/stderr semantics. |
| P00 | Event stream gap | Added importable emitter API and guarded JSONL streams for wrapper and automation consumers. |
| P00 | Wrapper productization uncertainty | Completed PySide6/QML spike and source-mode productization while keeping binary distribution gated. |

---

*Auto-generated by carryforward. Direct edits allowed but may be overwritten.*
