# CONVENTIONS.md

## Purpose

These conventions govern Apex Infinite CLI work inside this repository. They
are implementation rules, not planning notes. Keep them accurate to the current
codebase while also recording durable boundaries that future sessions must
honor.

## Guiding Principles

- Preserve autonomous workflow behavior before improving presentation.
- Treat the CLI as a scriptable operator tool first and a styled terminal UI
  second.
- Keep output readable in interactive terminals, plain logs, CI, remote shells,
  redirected output, and constrained terminal environments.
- Separate durable workflow facts from human rendering.
- Prefer small, testable helper boundaries inside `src/apex_infinite/` over
  growing the CLI entry point without structure.
- Use repository evidence and record assumptions when requirements are
  incomplete.
- Keep authored files ASCII-only with Unix LF line endings.

## Scope

- Primary development target: `apex-infinite-cli/`.
- Main implementation package today: `apex-infinite-cli/src/apex_infinite/`.
- CLI config file today: `apex-infinite-cli/src/apex_infinite/config.yaml`.
- CLI docs live in `apex-infinite-cli/README.md` and `apex-infinite-cli/docs/`.
- Root skill files remain canonical sources for Apex Spec packaging.
- Do not edit generated plugin payloads under
  `plugins/apex-spec/skills/apex-spec/`.
- After changing canonical skill files, run
  `bash scripts/sync-plugin-payload.sh`.
- Root scripts must stay bash + jq only. Do not add Python or Node
  dependencies to root script workflows.

## Current CLI Baseline

- The CLI is a packaged Click application with a global Rich `Console`.
- Current CLI flags are `--path`, `--start`, `--ceo`, `--provider`, `--model`,
  `--config`, `--history`, `--max-iterations`, `--dry-run`, `--verbose`, and
  `--version`.
- Current config sections are `provider`, `codex`, and `providers`.
- Current runtime dependencies are Click, Rich, OpenAI Python SDK,
  python-dotenv, PyYAML, SQLite from the Python standard library, and Codex CLI.
- Current local history is SQLite at `~/.apex-infinite/history.db`.
- Current tests live in `apex-infinite-cli/tests/`.
- New UI, config, rendering, subprocess, history, or event work must add
  focused tests because that coverage does not exist yet.

## Python Style

- Target Python 3.10+ unless project metadata raises the floor.
- Use black formatting and pylint rules from
  `apex-infinite-cli/pyproject.toml`.
- Use `snake_case` for functions and variables, `PascalCase` for classes, and
  `UPPER_SNAKE_CASE` for constants.
- Keep imports grouped as standard library, third-party, then local imports.
- Add type hints to new helpers when they clarify config, DB, event, renderer,
  or subprocess contracts.
- Prefer explicit return values over mutating globals.
- Split renderer, config, event, DB, or subprocess helpers when the split lowers
  risk or makes behavior independently testable.
- Avoid broad rewrites unless the session explicitly scopes them and preserves
  current prompt, DB, and subprocess behavior with tests.

## CLI Behavior

- Click options use long kebab-case names such as `--max-iterations`.
- Add new CLI flags only when they have a clear operator behavior and test
  coverage.
- Invalid user configuration fails fast with a clear Click or config error.
- Preserve current exit behavior for missing config, unknown provider, invalid
  project path, missing Codex binary, timeout, and known runtime errors.
- `--verbose` controls output depth. Reuse it for expanded history detail
  instead of adding `--history-verbose`.
- `--plain` disables color and effects.
- `--ascii` changes glyph choices only and does not by itself disable color.
- `--compact` reduces vertical space but must not hide errors, manager reasons,
  prompts, command output summaries, help pauses, completion, timeouts, or
  non-zero exits.
- `Ctrl+C`, `help`, `alldonebaby`, timeout, and non-zero subprocess exits must
  remain impossible to miss in every theme and in plain mode.

## UI Configuration

- Add UI settings under a top-level `ui` config section.
- Supported UI keys are `theme`, `effect_level`, `ascii`, `compact`,
  `show_elapsed`, `show_provider`, and `themes`.
- Built-in theme names are `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and
  `plain`.
- Built-in themes are Python token definitions, not copied external profile
  data.
- Custom theme overrides live under `ui.themes.<name>` and must be validated
  before use.
- Invalid `--theme`, `ui.theme`, or malformed `ui.themes` values fail fast. Do
  not silently fall back to `plain` for malformed user config.
- Resolve UI settings in this order:
  1. CLI flags
  2. Environment constraints
  3. Config file
  4. Built-in defaults
- The default `ui.theme` is `auto`.
- `auto` resolves to `crt-green` only for capable interactive terminals.
- `auto` resolves to `plain` for `NO_COLOR`, `TERM=dumb`, non-TTY output,
  redirected output, or `Console().is_terminal == false`.
- `--plain` forces `theme: plain`, `effect_level: off`, and color disabled.
- `NO_COLOR` behaves like `--plain` unless the operator explicitly passes
  `--theme`.
- An explicit `--theme` may opt back into color under `NO_COLOR` only when that
  behavior is documented and tested.
- Non-TTY output, redirected output, `TERM=dumb`, and non-terminal Console paths
  default to plain unless the operator explicitly forces a theme.
- `--event-stream PATH` writes line-buffered JSONL events without changing
  normal human output.
- `--event-stream -` is valid only when human rendering is disabled so JSONL
  never mixes with Rich or plain human output.

## Rendering

- Route all operator-facing Rich output through renderer helpers.
- Inject `Console` into renderers so tests can use
  `Console(record=True, width=...)`.
- Renderer token models should cover colors, emphasis, borders, status labels,
  severity labels, muted text, glyph sets, and plain/ascii fallbacks.
- Choose independent colors, labels, glyphs, layouts, and effect names.
- Treat every visual element as operational information, not decoration.
- Startup should show project, provider, model, config, max iterations, dry-run
  state, and selected theme when those facts are available.
- Iteration rendering should keep stable sections for history summary, manager
  decision, prompt, Codex execution, result, DB log, and next wait.
- Manager decisions, Codex prompts, agent output, DB writes, retries, errors,
  interrupts, timeouts, help pauses, and completion need distinct semantic
  labels.
- Low-fidelity scanline or separator effects must use independently chosen
  repeated characters and disable automatically in `plain` and compact modes.
- In `ascii` mode, rendered output uses only code points 0-127.
- Store raw workflow data only. Never write ANSI escapes, Rich markup, box
  glyphs, frame characters, or visual tokens to SQLite or event payloads.
- Test semantic labels and sections instead of brittle full-frame snapshots.
- Verify changed renderers at 80, 100, and 120 columns.

## Prompt And Routing

- Keep `MANAGER_SYSTEM_PROMPT`, `SUMMARIZER_SYSTEM_PROMPT`, and
  `build_codex_prompt()` stable unless the session explicitly changes prompt
  behavior.
- The manager prompt is scoped to initialized projects and normally chooses the
  11 post-initialization staged commands.
- The CLI still recognizes initialization commands for explicit starts and
  external routing.
- Known Apex Spec commands route through the exact prompt
  `Run the apex-spec skill command /<command>`.
- Unknown manager output passes through as raw high-level Codex instructions.
- Keep slash tolerance, case normalization, and whitespace trimming behavior
  covered by tests.
- When prompt behavior changes, update `src/apex_infinite/cli.py`, prompt
  tests, README, and `apex-infinite-cli/docs/prompt-contract.md` together.
- UI and event-stream work does not change the prompt contract unless prompt
  functions or routing behavior actually change.

## Subprocess Handling

- Preserve stdout capture, stderr fallback, return-code wrapping, timeout text,
  dry-run output, missing-binary handling, and generic exception reporting.
- Keep `COMMAND_TIMEOUT` explicit and visible to operators.
- If replacing `subprocess.run()` with `subprocess.Popen`, cover success,
  stderr-only output, non-zero exit, timeout, dry-run, missing binary, and
  generic exception paths with tests.
- Live execution status must not change captured output semantics.
- Show elapsed time, timeout, and process state during long `codex exec` runs
  when UI work adds live status.
- Do not let live displays, carriage-return animations, or terminal-only
  effects leak into plain output, history rows, or event payloads.

## Database Layer

### Connection

- SQLite database path: `~/.apex-infinite/history.db`.
- Directory creation happens before first DB use.
- Use WAL mode for history durability.

### Schema

- Preserve the legacy `cc_response` column for backward compatibility.
- Do not require a migration for existing local history databases unless a
  session explicitly calls for one.
- New durable fields must be optional or backward-compatible.
- Do not rename existing history columns for display polish.

### Queries

- Use parameterized SQLite queries only.
- Normalize project paths the same way current code does before storing or
  reading history: expand `~`, validate the directory, strip trailing slashes,
  and append one trailing slash.
- Do not assume symlinked and non-symlinked paths are the same project unless a
  session explicitly changes path canonicalization and migrates/tests history
  behavior.
- Keep history rows raw. Derived summaries belong in display or event output,
  not schema rewrites.

### Testing

- Use temporary DB paths or monkeypatched `DB_DIR` and `DB_PATH` in tests.
- Test empty, short, long, and legacy rows for history display changes.
- Test that history rows contain no ANSI escapes, Rich markup, frame glyphs, or
  styled output.

## Event Stream

- Event payloads contain raw operational facts, not Rich markup, ANSI escapes,
  frame glyphs, or visual-theme tokens.
- `--event-stream PATH` writes line-buffered JSONL without changing normal
  human output.
- `--event-stream -` requires an explicit machine-output or no-human-output
  guard.
- Provide an importable event emitter API for tests and future renderers.
- Event names should cover iteration lifecycle, manager decision, prompt
  dispatch, subprocess lifecycle, output summary, DB logging, help,
  completion, timeout, interrupt, and errors.
- Test event order, event names, payload stability, file flushing, stdout
  collision prevention, and dry-run behavior without real LLM or Codex calls.
- Future renderers and wrappers consume events or importable APIs, not Rich
  frames and not human terminal output.

## Optional Visual Wrapper

- Keep the base CLI lightweight, headless-safe, and free of graphical runtime
  dependencies.
- Treat any graphical wrapper as an optional Linux companion surface for the
  same workflow engine.
- The accepted wrapper path is PySide6 with Qt Quick/QML as an optional extra.
- The wrapper launches the Python CLI as a subprocess and consumes the JSONL
  event stream or importable event API.
- Do not scrape Rich output, plain human output, or terminal frames for wrapper
  state.
- The wrapper may provide a read-only terminal-like log viewport, status
  panels, theme selection, effect intensity, font, scaling, reduced effects,
  and plain fallback controls.
- Document PySide6 LGPLv3/commercial obligations before productizing a wrapper.
- Do not use PyQt unless a future explicit license decision allows it.
- Do not depend on qmltermwidget, QTermWidget, a copied terminal emulator, or an
  external terminal emulator for the selected path.
- pywebview plus xterm.js is only a backup if evidence shows a true terminal
  emulator viewport is mandatory.
- Keep wrapper code isolated from the base CLI until the interface and license
  story are accepted.

## Testing

- Run CLI tests from `apex-infinite-cli/` with `pytest tests/ -v`.
- Install CLI dev dependencies with `python -m pip install -e ".[dev]"` when
  needed.
- Keep existing prompt/routing tests green unless the prompt contract is
  intentionally updated.
- Add focused tests for config parsing, Click options, renderer behavior,
  environment color behavior, subprocess behavior, history display, plain mode,
  ascii mode, compact mode, and event streaming.
- Use Click `CliRunner` tests for new flags and invalid option combinations.
- Use `Console(record=True, width=...)` tests for rendered output.
- Prefer fixture-driven tests and monkeypatching over real LLM or Codex calls.
- Validate 80, 100, and 120 column widths for changed rendering.
- Exercise `--dry-run`, `--history`, `--verbose`, `--plain`, `--ascii`,
  `--compact`, `--event-stream PATH`, guarded `--event-stream -`, every
  built-in theme, `NO_COLOR`, `TERM=dumb`, non-TTY output, and redirected output
  when those features exist.
- Confirm ASCII-only and LF-only output for generated docs, transcripts, and
  source files.
- Root script and reference changes still require `bats tests/` and
  `bash scripts/sync-plugin-payload.sh --check`.

## Documentation

- Update the CLI README when user-facing flags, config keys, themes, event
  stream behavior, run modes, or install requirements change.
- Update the operator runbook for operational guidance, fallback behavior,
  remote shells, CI/log usage, and troubleshooting.
- Update history DB docs when schema, displayed history semantics, truncation,
  status labels, or verbose history behavior change.
- Update prompt-contract docs only when prompts, command routing, event
  boundaries, or machine-output behavior affect that contract. Otherwise state
  that UI/event changes do not alter prompt routing.
- Update troubleshooting docs for unreadable colors, terminal width, non-UTF
  terminals, `NO_COLOR`, `TERM=dumb`, redirected output, remote shells, provider
  failures, Codex failures, and event-stream misuse.
- Do not commit binary screenshots. Use deterministic ASCII transcripts or
  asciinema `.cast` files for repo-tracked examples.
- When user docs discuss visual inspiration or licensing, keep the clean-room
  boundary explicit and avoid implying runtime dependency on third-party
  visual tools.

## Security And Licensing

- Load API keys from environment-backed config values. Never hardcode secrets.
- Do not print or store provider API keys in history, events, docs, tests, or
  transcripts.
- Treat SQLite history and event streams as local operational records that may
  contain project-sensitive text.
- Do not copy third-party GPL-family source code, QML, shader code, compiled
  shader blobs, images, icons, fonts, profile data, resource manifests, build
  scripts, or terminal-emulator code.
- Use clean-room visual translation: independently chosen names, colors,
  layouts, controls, event models, and assets.
- Keep the repository's MIT-compatible codebase free of copied GPL-family
  implementation material unless a future explicit legal decision changes
  scope.
- Keep graphical wrapper dependencies optional and document their license and
  packaging obligations before release.

## Project Areas

| Area | Path | Stack |
|------|------|-------|
| apex-infinite-cli | `apex-infinite-cli/` | Python, Click, Rich, SQLite |
| apex-spec-skill | `.` | Markdown, bash, jq, Codex plugin |

### Cross-Area Rules

- Prefer path-scoped sessions for `apex-infinite-cli/` work.
- Root skill changes require regenerated plugin payload checks.
- Do not let CLI UI work alter root Apex Spec command contracts unless the
  session scope says so.
- Cross-area sessions must name the primary area and the secondary area touched.

## Local Dev Tools

| Category | Tool | Config |
|----------|------|--------|
| Python formatter | black | `apex-infinite-cli/pyproject.toml` |
| Python linter | pylint | `apex-infinite-cli/pyproject.toml` |
| Python type safety | mypy | `apex-infinite-cli/pyproject.toml`, CLI dev extra |
| Python testing | pytest, pytest-cov, pytest-mock | `apex-infinite-cli/pyproject.toml`, CLI dev extra |
| Script formatter | shfmt | `.pre-commit-config.yaml`, `.github/workflows/quality.yml` |
| Script linter | shellcheck | `.pre-commit-config.yaml`, `.github/workflows/quality.yml` |
| Script testing | bats | `tests/`, `.github/workflows/test.yml` |
| Git hooks | pre-commit | `.pre-commit-config.yaml` |
| Database | SQLite | `~/.apex-infinite/history.db` |

## Infrastructure

| Component | Provider | Details |
|-----------|----------|---------|
| Health | GitHub Actions release workflow | Apex Infinite CLI entrypoint health gate installs the package, runs `apex-infinite --version`, and checks `apex-infinite --help` output on tag releases. |
| CDN/DNS | N/A | No hosted web service; the skill and CLI source are distributed as repository files. |
| Hosting | GitHub repository and Codex plugin wrapper | Plain-file skill payload, plugin wrapper, and CLI source are distributed from the repository. |
| Database | Local SQLite | Operator-local `~/.apex-infinite/history.db`; no hosted production database. |
| Backup | N/A | No production database or object storage exists for this repo; operator-local history backup is outside repository infrastructure. |
| WAF/Rate Limit | N/A | No public HTTP service surface; release and repository security controls are workflow based. |
| Security | GitHub Actions | `security.yml` runs gitleaks, sensitive-file detection, and script security checks. |
| Deploy | GitHub Actions release workflow | Tag `v*` creates a GitHub Release after encoding, version sync, inventory, and CLI health gates pass. |

## CI/CD

| Bundle | Status | Workflow |
|--------|--------|----------|
| Code Quality | configured | `.github/workflows/quality.yml` |
| Build & Test | configured | `.github/workflows/test.yml` |
| Security | configured | `.github/workflows/security.yml` |
| Integration | configured | `.github/workflows/integration.yml` |
| Operations | configured | `.github/workflows/release.yml`, `.github/dependabot.yml` |

## When In Doubt

- Decide from repository evidence and document the assumption.
- Keep base CLI behavior stable before adding visual polish.
- Add tests around every changed boundary.
- Prefer current, accurate documentation over broad claims.
