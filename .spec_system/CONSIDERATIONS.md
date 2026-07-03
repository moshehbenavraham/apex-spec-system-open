# Considerations

> Institutional memory for AI assistants. Updated between phases via carryforward.
> **Line budget**: 600 max | **Last updated**: Phase 00 (2026-07-02)

---

## Active Concerns

Items requiring attention in upcoming phases. Review before each session.

### Technical Debt <!-- Max 5 items -->

- [P00] **Single-file CLI pressure**: `apex-infinite-cli/apex_infinite.py` currently owns Click, config, Rich output, SQLite, LLM calls, signals, notifications, and subprocess execution. Extract renderer/config/event helpers when that lowers risk versus extending the file.
- [P00] **UI config gap**: `apex-infinite-cli/config.yaml` has provider and Codex settings only. Add one validated UI resolver for CLI flags, environment constraints, config values, and defaults before adding visual polish.
- [P00] **Prompt contract coupling**: Do not change `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, or `build_codex_prompt()` during UI work unless prompt tests, README, and prompt-contract docs are updated in the same session.
- [P00] **History compatibility**: Existing history databases must remain readable without migration. Preserve the legacy `cc_response` column, normalized project path keys, and raw stored workflow data.
- [P00] **Subprocess behavior lock**: Live execution display must preserve stdout capture, stderr fallback, non-zero exit wrapping, timeout text, dry-run output, missing-binary handling, generic exception reporting, and `--verbose` semantics.

### External Dependencies <!-- Max 5 items -->

- [P00] **Base runtime dependency control**: The first UI milestone should use existing terminal dependencies (`rich`, `click`, `openai`, `python-dotenv`, `pyyaml`) and avoid adding graphical dependencies to the base CLI.
- [P00] **Provider and Codex prerequisites**: Provider API keys, local provider availability, and the configured Codex binary are runtime prerequisites. Never print, store, or emit API keys in history, events, docs, or tests.
- [P01] **Optional wrapper obligations**: PySide6/Qt Quick/QML belongs only in an optional Linux visual wrapper path, with LGPLv3/commercial obligations, packaging notes, checksums, and license notices documented before release.
- [P01] **Terminal-widget exclusions**: PyQt, qmltermwidget, QTermWidget, copied terminal-emulator code, and embedded pseudo-terminal behavior are out of scope unless a later explicit decision changes the wrapper architecture.

### Performance / Security <!-- Max 5 items -->

- [P00] **Plain-output safety**: `auto` must resolve to plain output for `NO_COLOR`, `TERM=dumb`, non-TTY output, redirected output, or non-terminal Rich consoles unless the operator explicitly forces a theme.
- [P00] **Critical-state visibility**: `help`, `alldonebaby`, interrupts, timeouts, provider failures, non-zero Codex exits, DB writes, and max-iteration stops must remain visible in styled, plain, ASCII, and compact modes.
- [P00] **Raw durable facts only**: SQLite rows and JSONL events must contain operational facts only: no ANSI escapes, Rich markup, box/frame glyphs, visual tokens, secrets, or renderer snapshots.
- [P00] **Machine-output isolation**: Writing event JSONL to stdout is valid only when human rendering is explicitly disabled. Never mix JSONL with Rich or plain human output on stdout.
- [P00] **Width and log readability**: Verify changed output at 80, 100, and 120 columns. Plain mode must be deterministic enough for logs and tests without live-only carriage-return behavior.

### Architecture <!-- Max 5 items -->

- [P00] **Renderer boundary first**: Route startup, iteration frames, manager decisions, prompt previews, execution results, DB notices, history, interrupts, and completion through renderer helpers with injected `Console` support.
- [P00] **Event stream is the wrapper contract**: Future visual surfaces must consume an importable emitter or line-buffered JSONL events, not scrape human terminal output or parse Rich frames.
- [P00] **Clean-room visual translation**: Treat retro styling as conceptual requirements only: mood, hierarchy, settings categories, and effect categories. Do not copy code, shaders, constants, assets, fonts, profiles, resource manifests, icons, or build scripts.
- [P01] **Wrapper as companion surface**: The Linux visual wrapper must launch or reuse the CLI workflow engine through the event boundary and must not fork manager decisions, prompt routing, storage, or safety behavior.
- [P01] **Effect responsibility split**: Rich should cover color, labels, layout, framing, status hierarchy, and low-fidelity separators. True glow, curvature, flicker, burn-in trails, RGB shift, and shader-like effects belong behind the optional wrapper boundary.

---

## Lessons Learned

Proven patterns and anti-patterns. Reference during implementation.

### What Worked <!-- Max 15 items -->

- [P00] **Small testable boundaries**: Injecting `Console(record=True, width=...)` into renderer helpers makes output behavior testable without coupling tests to the global console.
- [P00] **Fail-fast user config**: Invalid theme names or malformed custom theme maps should raise clear Click/config errors. Use plain fallback for environment constraints, not for invalid user input.
- [P00] **One depth flag**: Reuse `--verbose` for expanded history detail instead of adding a mode-specific duplicate flag.
- [P00] **Semantic render tests**: Assert labels, sections, fallback paths, and stored raw data rather than full-frame Rich snapshots.
- [P00] **Docs move with behavior**: README, operator runbook, history DB docs, troubleshooting, and prompt-contract docs should change in the same session as the user-facing behavior they describe.
- [P00] **Dry-run fixtures reduce risk**: Config, event ordering, renderer, history, and subprocess tests should use fixtures, temp DB paths, and monkeypatching instead of real LLM or Codex calls.

### What to Avoid <!-- Max 10 items -->

- [P00] **Styled storage pollution**: Do not persist Rich markup, ANSI escapes, frame glyphs, truncation text, or display-only labels to SQLite or event payloads.
- [P00] **Decorative opacity**: Do not let retro styling hide manager reasons, prompts, captured output, errors, completion state, or handoff information.
- [P00] **Broad rewrites without tests**: Avoid converting the CLI to a large class hierarchy unless smaller helper extraction cannot preserve behavior cleanly.
- [P00] **Graphical base install**: Do not make terminal CLI users install Qt, PySide6, PyQt, terminal widgets, image assets, shader assets, or display-server dependencies.
- [P01] **Premature wrapper productization**: Do not productize the Linux wrapper until the event boundary exists and a spike proves dependency, license, packaging, and fallback behavior.
- [P00] **Prompt drift during UI work**: Do not edit manager routing text to support display-only concerns; use renderer/event metadata instead.

### Tool/Library Notes <!-- Max 5 items -->

- [P00] **Rich**: Use injected consoles and width-specific records for tests; keep plain and ASCII renderers free of box-drawing glyphs and live-only output.
- [P00] **Click**: Use `CliRunner` coverage for new flags, invalid theme values, config precedence, and incompatible event-output combinations.
- [P00] **SQLite**: Use temporary DB paths or monkeypatched `DB_DIR`/`DB_PATH` in tests; cover empty, sparse legacy, short, and long history rows.
- [P01] **Qt Quick/QML**: Treat graphical effects as optional and provide a low-effects fallback for unsupported scene graph backends or headless environments.
- [P01] **App packaging**: Keep Linux visual packaging separate from the base CLI and document release artifacts, checksums, license notices, and source/dev install paths.

---

## Resolved

Recently closed items (buffer - rotates out after 2 phases).

| Phase | Item | Resolution |
|-------|------|------------|
| - | *No resolved items yet* | - |

*Auto-generated by initspec. Updated by carryforward between phases.*
