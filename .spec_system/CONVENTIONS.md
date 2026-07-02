# CONVENTIONS.md

## Guiding Principles

- Preserve autonomous workflow behavior before improving presentation.
- Keep operator output clear in both styled terminals and plain logs.
- Prefer small, testable helpers over extending `apex_infinite.py` blindly.
- Use repository evidence and record assumptions when requirements are incomplete.
- Keep authored files ASCII-only with Unix LF line endings.

## Scope

- Primary package: `apex-infinite-cli/`.
- Root skill files remain canonical sources for Apex Spec packaging.
- Do not edit generated plugin payloads under `plugins/apex-spec/skills/apex-spec/`.
- After changing canonical skill files, run `bash scripts/sync-plugin-payload.sh`.

## Python Style

- Target Python 3.10+ unless project metadata raises the floor.
- Follow PEP 8, black formatting, and pylint configuration from `pyproject.toml`.
- Use `snake_case` for functions and variables, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for constants.
- Keep imports grouped as standard library, third-party, then local imports.
- Add type hints to new helpers when they clarify config, DB, event, or renderer contracts.
- Prefer explicit return values over mutating globals.

## CLI Behavior

- Click options use long kebab-case names such as `--max-iterations`.
- Invalid user configuration fails fast with a clear Click or config error.
- Preserve current exit behavior for missing config, invalid project paths, and known runtime errors.
- `--verbose` controls output depth; do not add duplicate verbose flags for one mode.
- `--plain` disables color and effects; `--ascii` changes glyph choices only.
- Do not hide errors, timeouts, `help`, `alldonebaby`, or non-zero exits in compact mode.

## Rendering

- Route operator-facing Rich output through renderer helpers.
- Inject `Console` into renderers so tests can use `Console(record=True, width=...)`.
- Store raw workflow data only; never write ANSI escapes, Rich markup, or frame glyphs to SQLite.
- Test semantic labels and sections instead of brittle full-frame snapshots.
- Verify styled and plain output at 80, 100, and 120 columns for changed renderers.

## Config

- Load YAML through the existing config loader path.
- Resolve UI settings in this order: CLI flags, environment constraints, config, defaults.
- `auto` resolves to a styled theme only for capable interactive terminals.
- `NO_COLOR`, `TERM=dumb`, non-TTY output, or redirected output default to `plain`.
- Explicit `--theme` can override environment color constraints only when documented and tested.
- Validate custom theme maps before use; do not silently fall back for malformed user config.

## Prompt And Routing

- Keep `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, and `build_codex_prompt()` stable unless the session explicitly changes prompt behavior.
- When prompt behavior changes, update `apex_infinite.py`, prompt tests, README, and `docs/apex-infinite-cli/prompt-contract.md` together.
- Known Apex Spec commands route through the canonical `Run the apex-spec skill command /<command>` prompt.
- Unknown manager output passes through as raw high-level Codex instructions.

## Subprocess Handling

- Preserve stdout capture, stderr fallback, return-code wrapping, timeout text, dry-run output, missing-binary handling, and generic exception reporting.
- If replacing `subprocess.run()`, cover success, stderr-only output, non-zero exit, timeout, dry-run, and missing binary with tests.
- Keep `COMMAND_TIMEOUT` explicit and visible to operators.

## Database Layer

### Connection

- SQLite database path: `~/.apex-infinite/history.db`.
- Directory creation happens before first DB use.
- Use WAL mode for history durability.

### Schema

- Preserve the legacy `cc_response` column for backward compatibility.
- Do not require a migration for existing local history databases unless a PRD/session explicitly calls for one.
- New durable fields must be optional or backward-compatible.

### Queries

- Use parameterized SQLite queries only.
- Normalize project paths before storing or reading history.
- Keep history rows raw; derived summaries belong in display or event output, not schema rewrites.

### Testing

- Use temporary DB paths or monkeypatched `DB_DIR`/`DB_PATH` in tests.
- Test empty, short, long, and legacy rows for history display changes.

## Events

- Event payloads contain raw operational facts, not Rich markup or visual tokens.
- `--event-stream PATH` writes line-buffered JSONL without changing normal human output.
- `--event-stream -` is valid only when human rendering is disabled.
- Event names should cover iteration lifecycle, manager decision, prompt dispatch, subprocess lifecycle, DB logging, help, completion, timeout, and errors.

## Testing

- Run CLI tests from `apex-infinite-cli/` with `pytest tests/ -v`.
- Keep existing prompt/routing tests green unless the prompt contract is intentionally updated.
- Add focused tests for config parsing, Click options, renderer behavior, subprocess behavior, history display, and event streaming.
- Prefer fixture-driven tests and monkeypatching over real LLM or Codex calls.
- Confirm ASCII-only and LF-only output for generated docs and transcripts.

## Documentation

- Update the CLI README when user-facing flags, config, themes, or run modes change.
- Update operator runbook for operational guidance and fallback behavior.
- Update history DB docs when displayed history semantics change.
- Update prompt-contract docs only when prompts, command routing, or event boundaries affect that contract.
- Do not commit binary screenshots; use deterministic ASCII transcripts or asciinema `.cast` files.

## Security And Licensing

- Load API keys from environment-backed config values; never hardcode secrets.
- Do not print or store provider API keys in history, events, docs, or tests.
- Treat `EXAMPLE/cool-retro-term` as reference-only.
- Do not copy external GPL code, shaders, images, icons, fonts, profile data, resource manifests, or build scripts.
- Keep PySide6/Qt obligations documented before wrapper productization.

## Project Areas

| Area | Path | Stack |
|---------|------|-------|
| apex-infinite-cli | apex-infinite-cli | Python CLI |
| apex-spec-skill | . | Markdown, bash, jq, Codex plugin |

### Cross-Area Rules

- Prefer path-scoped sessions for `apex-infinite-cli/` work.
- Root skill changes require regenerated plugin payload checks.
- Do not let CLI UI work alter root Apex Spec command contracts unless the session scope says so.
- Cross-area sessions must name the primary area and the secondary area touched.

## Local Dev Tools

| Category | Tool | Config |
|----------|------|--------|
| Formatter | black | `pyproject.toml` |
| Linter | pylint | `pyproject.toml` |
| Type Safety | not configured | - |
| Testing | pytest, bats | `pyproject.toml`, `tests/` |
| Observability | local logs/history | SQLite history |
| Git Hooks | not configured | - |
| Database | SQLite | `~/.apex-infinite/history.db` |

## When In Doubt

- Decide from repository evidence and document the assumption.
- Keep base CLI behavior stable before adding visual polish.
- Add tests around every changed boundary.
