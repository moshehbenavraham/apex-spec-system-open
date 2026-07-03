# Apex Infinite CLI

Autonomous OpenAI Codex CLI session manager -- a standalone Python package that runs the full Apex Spec System workflow in an infinite loop without human intervention.

Originally powered by an n8n workflow with Airtable, Slack, and SSH nodes, this CLI replaces all of that with SQLite, subprocess, terminal output, and an optional visual wrapper.

## How It Works

```text
             +------------------+
             |   Manager LLM    |
             | (decides next    |
             |  command)        |
             +--------+---------+
                      |
          +-----------v-----------+
          |                       |
     +----v----+           +------v------+
     | Codex   |           |   History   |
     | CLI     |           |  (SQLite)   |
     | (Senior |           |  Last 15    |
     |  Dev)   |           |  records    |
     +----+----+           +------+------+
          |                       ^
          +-----------+-----------+
                      |
              (loop until done)
```

1. **Fetch history** -- Last 15 interactions from SQLite
2. **Summarize** -- LLM condenses history to <2000 chars
3. **Decide** -- Manager LLM picks the next command (plansession, implement, creview, validate, etc.)
4. **Execute** -- Runs `codex exec` with the chosen command in your project directory
5. **Log** -- Records the interaction
6. **Repeat** -- Until `alldonebaby` or max iterations reached

Each Apex Spec command ends with a `Next command:` handoff. The manager LLM uses
that line as the primary routing signal, or sends concise custom instructions to
Codex CLI when a fix must happen before the next command.

## Supported Commands

The CLI recognizes the staged Apex Spec commands and routes them through the
skill invocation prompt. The autonomous manager loop is intended for projects
that have already been initialized, so normal manager decisions use only the
session workflow and phase-transition commands.

| Stage | Commands |
|-------|----------|
| Initialization, explicit start only | `initspec`, `createprd`, `createuxprd` |
| Session workflow | `plansession`, `implement`, `creview`, `validate`, `updateprd` |
| Phase transition | `audit`, `pipeline`, `infra`, `carryforward`, `documents`, `phasebuild` |
| Terminal | `alldonebaby` (stops loop) |

Any output not matching a known command is sent as custom instructions directly to Codex CLI, allowing the manager LLM to give ad-hoc instructions (e.g., "Fix the two failing tests then rerun validate"). `help` remains an emergency operator pause in the CLI, but it is not part of the normal Apex workflow.

## Install

```bash
cd apex-infinite-cli
python -m pip install -e .
```

For development, testing, and dependency audits:

```bash
python -m pip install -e ".[dev]"
```

For the optional Linux visual wrapper source mode only:

```bash
python -m pip install -e ".[visual]"
```

`pyproject.toml` is the canonical package, dependency, test, lint, and coverage
configuration. The `requirements*.txt` files are compatibility shims for older
local workflows.

The wrapper dependencies are intentionally separate from the base CLI install.
The base terminal CLI does not import PySide6 or require a graphical display.

## Package Layout

```text
apex-infinite-cli/
|-- pyproject.toml              # package metadata, dependencies, tool config
|-- src/
|   |-- apex_infinite/          # base CLI, events, renderer, default config
|   \-- apex_infinite_visual/   # optional PySide6 visual wrapper
|-- tests/                      # pytest suite
|-- docs/                       # operator and interface docs
|-- scripts/                    # local helper scripts
\-- n8n-workflow/               # original workflow reference archive
```

## Configuration

The packaged default config lives at `src/apex_infinite/config.yaml`. For local
overrides, create `./config.yaml` in the current working directory or pass
`--config /path/to/config.yaml`.

Edit the config to choose your LLM provider and configure the Codex CLI agent:

```yaml
provider: grok  # ollama | grok | openai

# Codex CLI agent configuration
codex:
  binary: "codex"                        # Path to codex binary
  exec_flags: "--dangerously-auto-approve"  # Flags passed to codex exec
  model_reasoning_effort: "high"         # Reasoning effort level

providers:
  ollama:
    base_url: "http://${OLLAMA_HOST}:${OLLAMA_PORT}/v1"
    api_key: "${OLLAMA_API_KEY}"
    model: "${OLLAMA_MODEL}"

  grok:
    base_url: "https://api.x.ai/v1"
    api_key: "${XAI_API_KEY}"       # Set this env var
    model: "grok-4-1-fast-reasoning"

  openai:
    base_url: "https://api.openai.com/v1"
    api_key: "${OPENAI_API_KEY}"    # Set this env var
    model: "gpt-4o"
```

Provider values use `${ENV_VAR}` syntax, expanded at runtime. Ollama defaults
to `localhost`, port `11434`, API key `ollama`, and model `qwen2.5:7b` when
those env vars are not set. The `codex` section controls the agent binary and
execution flags -- customize `binary` if codex is not on your PATH, and adjust
`exec_flags` or `model_reasoning_effort` as needed.

Before real runs, review the target `--path`, provider, model, Codex binary,
and `codex.exec_flags`. Startup runs a provider preflight before the loop:
the CLI lists provider models and fails fast when the configured model is not
available. Use `--check-provider` to run only that preflight, add
`--check-provider-chat` for a tiny chat completion, or pass
`--skip-provider-check` only for deliberate offline wiring checks. The sample
config uses broad autonomous Codex approval flags for unattended operation; use
`--dry-run` first when validating a new project.

### Display Settings

The CLI renders operator output through a UI boundary that keeps terminal
styling separate from workflow data and SQLite history. Add or edit the `ui`
section in `config.yaml`:

```yaml
ui:
  theme: "auto"          # auto | crt-green | crt-amber | ibm-dos | plain
  effect_level: "low"    # off | low | medium
  ascii: false           # use ASCII-safe glyphs
  compact: false         # reduce vertical spacing
  show_elapsed: true
  show_provider: true
  themes: {}
```

Built-in themes are `auto`, `crt-green`, `crt-amber`, `ibm-dos`, and `plain`.
`auto` resolves to `crt-green` for capable interactive terminals and to
`plain` for constrained output such as `NO_COLOR`, `TERM=dumb`, non-terminal
Rich consoles, or redirected/non-TTY output. `--plain` always forces plain
output and disables effects. `--ascii` only changes glyph choices; it does not
disable color by itself. `--compact` reduces spacing but keeps errors, manager
reasons, prompts, command output summaries, help pauses, completion, timeouts,
and non-zero exits visible.

Theme summary:

| Theme | Use when |
|-------|----------|
| `auto` | You want the CLI to pick `crt-green` in capable terminals and `plain` in constrained output. |
| `crt-green` | You want the default styled operator-console look in an interactive terminal. |
| `crt-amber` | You want the same operator hierarchy with amber terminal emphasis. |
| `ibm-dos` | You want high-contrast DOS-like labels and panels. |
| `plain` | You want logs, CI, remote shells, redirected output, or terminals where colors render poorly. |

The normal run surface is a compact operator console. Startup renders a `BOOT`
panel with project, provider, model, config, theme, effects, glyph mode,
dry-run state, and start context. Each loop uses an `ITERATION` frame with the
current operation, provider/model, project, elapsed time, and dry-run state when
those facts are available. Manager choices, prompt previews, Codex execution,
captured responses, DB writes, help, interrupts, timeouts, completion, and
safety stops use stable text labels so the same state remains clear in styled,
plain, ASCII, compact, and non-terminal output.

Display precedence is:

```text
CLI flags -> environment constraints -> config.yaml -> built-in defaults
```

An explicit `--theme` may opt back into color under `NO_COLOR` or other
constraints. Invalid theme names, unknown `ui` keys, malformed `ui.themes`
entries, and invalid effect levels fail fast instead of silently falling back.

Custom themes live under `ui.themes.<name>` and inherit from a built-in base:

```yaml
ui:
  themes:
    night-shift:
      base: "crt-green"
      foreground: "bright_white"
      accent: "cyan"
      warning: "yellow"
```

Theme token overrides must be non-empty strings and can use the same token keys
as the built-in renderer: `foreground`, `accent`, `muted`, `success`,
`warning`, `error`, `info`, `dry_run`, `complete`, `separator`, `panel`,
`border`, `emphasis`, and `dim`.

Low-effect separators are ASCII-safe and are suppressed in `plain` and
`compact` modes. Rendered labels, Rich markup, ANSI escapes, frame glyphs,
separator characters, and theme tokens remain display-only and are not written
to SQLite history.

See [Operator runbook](docs/operator-runbook.md) for
mode-selection guidance and
[dry-run-plain.txt](docs/transcripts/dry-run-plain.txt)
for a deterministic fallback transcript.

## Usage

```bash
# Interactive mode -- prompts for project selection
apex-infinite

# Direct mode
apex-infinite --path ~/projects/my-app/ --start plansession

# With CEO instructions
apex-infinite --path ~/projects/my-app/ --start plansession --ceo "focus on auth first"

# Dry run -- see LLM decisions without executing codex
apex-infinite --path ~/projects/my-app/ --start plansession --dry-run

# View history
apex-infinite --history
apex-infinite --history --path ~/projects/my-app/
apex-infinite --history --verbose

# Override provider/model
apex-infinite --path ~/projects/my-app/ --provider ollama --model "qwen2.5:72b"

# Check provider connectivity and model availability
apex-infinite --provider ollama --check-provider
apex-infinite --provider ollama --check-provider --check-provider-chat
./scripts/check-ollama.sh --chat

# Limit iterations
apex-infinite --path ~/projects/my-app/ --start plansession --max-iterations 5

# Choose display modes
apex-infinite --path ~/projects/my-app/ --theme crt-amber
apex-infinite --path ~/projects/my-app/ --plain --ascii --compact

# Write machine-readable events to a file while keeping human output
apex-infinite --path ~/projects/my-app/ --event-stream /tmp/apex-events.jsonl

# Reserve stdout for JSONL events
apex-infinite --path ~/projects/my-app/ --event-stream - --machine-output
```

## Options

```text
--path TEXT               Project path (prompted if not given)
--start TEXT              Starting command (e.g. "plansession")
--ceo TEXT                Initial CEO instructions
--provider TEXT           LLM provider override: ollama|grok|openai
--model TEXT              Model override
--config TEXT             Config file path (default: ./config.yaml, then packaged config)
--history                 Show interaction history
--max-iterations INTEGER  Safety limit (default: 50)
--dry-run                 Show what would execute without running codex
--verbose                 Show full agent output
--theme TEXT              UI theme: auto|crt-green|crt-amber|ibm-dos|plain
--plain                   Disable color and effects
--ascii                   Use ASCII-safe glyphs
--compact                 Reduce vertical spacing
--check-provider          Run provider connectivity and model preflight, then exit
--check-provider-chat     Include a tiny chat completion in provider checks
--skip-provider-check     Skip startup provider preflight before the loop
--event-stream TEXT       Write lifecycle JSONL to PATH, or '-' with --machine-output
--machine-output          Disable human output and reserve stdout for JSONL
--version                 Show version
```

## Operator Intervention

Operator intervention is outside the normal autonomous workflow:

- **Ctrl+C interrupt** -- Press once to pause after the current step for operator input. Press twice to force quit.
- **Emergency `help` pause** -- Supported by the CLI for unrecoverable external blockers, but the manager prompt tells the LLM to follow `Next command:` instead for ordinary workflow routing.

## Safety Features

- **Max iterations** -- Default 50, prevents runaway loops
- **30-min timeout** -- Per codex execution
- **Dry run mode** -- See decisions without executing
- **Error feedback** -- Failed commands feed error text back to the manager LLM
- **Graceful interrupt** -- Single Ctrl+C pauses, double exits

## Data

Interaction history is stored at `~/.apex-infinite/history.db` (SQLite with WAL mode).
Rendered labels, ANSI escapes, Rich markup, frame glyphs, theme tokens, and
display-only status text are not written to history rows. The database keeps
raw agent responses, manager output, manager reasons, and terminal help/done
state so styled, plain, and ASCII modes do not change durable workflow data.
History display derives a compact ledger at render time with timestamp,
status, project key, command, reason, and response summary. `--history
--verbose` expands reason, response, and stored-state detail without adding a
separate history-only flag or changing the SQLite schema.

The manager and summarizer can send recent history, latest agent output,
operator instructions, summaries, and project paths to the configured LLM
provider. Do not include provider keys, secrets, personal data, or customer
data in operator instructions or target-project outputs. The local history
database currently has no CLI purge, retention, or redaction command; remove or
protect `~/.apex-infinite/history.db` manually when needed.

See [history-ledger.txt](docs/transcripts/history-ledger.txt)
for compact and verbose history examples.

## Event Stream

Use `--event-stream PATH` to write line-buffered JSONL lifecycle events for
automation or future wrappers. File event streams are a side channel and do not
change normal human output. Use `--event-stream - --machine-output` when stdout
must contain JSONL only; this disables human rendering, terminal bell, and
desktop notifications.

The stream emits startup, config/UI resolution, iteration, history summary,
manager decision, prompt dispatch, Codex subprocess, DB log, help, interrupt,
completion, max-iteration, and stop events. Payloads contain bounded raw facts
and exclude provider API keys, Rich markup, ANSI escapes, frame glyphs, theme
token values, and renderer snapshots.

See [Event stream contract](docs/event-stream.md) for the
full event contract and
[machine-output-events.jsonl](docs/transcripts/machine-output-events.jsonl)
for a deterministic JSONL sample.

## Visual Wrapper Source Mode

The optional Linux visual wrapper is separate from the base terminal CLI. It
uses PySide6 with Qt Quick/QML as an optional dependency and consumes the JSONL
event stream through the guarded `--event-stream - --machine-output` boundary.
Session 08 release verification keeps source/dev visual mode shippable after
final gates; binary publishing remains gated for future packaging, license,
notice, checksum, and source/relink review.

Install the optional dependencies, then run the fixture-backed smoke path:

```bash
cd apex-infinite-cli
python -m pip install -e ".[visual]"
apex-infinite-visual --dry-run --max-iterations 1
```

The wrapper exposes green CRT, amber CRT, IBM DOS, and plain presets, effect
intensity, font family, font scale, reduced effects, and plain fallback
controls. The same settings can be passed on the command line:

```bash
apex-infinite-visual \
  --theme crt-amber \
  --effect-intensity 55 \
  --font-family "monospace" \
  --font-scale 1.05 \
  --plain-fallback
```

For headless smoke checks:

```bash
QT_QPA_PLATFORM=offscreen apex-infinite-visual \
  --dry-run --max-iterations 1 --auto-close-ms 900
```

To launch the real CLI subprocess from the wrapper, opt in explicitly:

```bash
apex-infinite-visual \
  --launch-cli \
  --path ~/projects/my-app/ \
  --start-command implement \
  --dry-run \
  --max-iterations 1
```

PyQt, qmltermwidget, QTermWidget, copied terminal emulators, copied QML, copied
shaders, copied images, copied icons, copied fonts, copied resource manifests,
copied build scripts, and copied profile data remain excluded. The wrapper
does not parse Rich panels, plain human output, terminal frames, or history
display rows.

See [Visual wrapper productization](docs/visual-wrapper-productization.md)
for source-mode setup, packaging gates, license notes, checksums, and clean-room
verification. See [Visual wrapper spike](docs/visual-wrapper-spike.md)
for the original decision record and
[Visual wrapper boundary](docs/visual-wrapper-boundary.md)
for the clean-room no-copy rules.

## Testing

```bash
cd apex-infinite-cli
python -m pip install -e ".[dev]"
pytest tests/ -v
pip-audit
python -m mypy
```

The test suite covers prompt/routing compatibility, UI setting resolution,
Click option wiring, renderer semantics, and SQLite history safety.

## Deep-Dive Docs

- [Operator runbook](docs/operator-runbook.md)
- [Event stream contract](docs/event-stream.md)
- [History DB reference](docs/history-db.md)
- [Prompt contract](docs/prompt-contract.md)
- [Troubleshooting guide](docs/troubleshooting.md)
- [Visual wrapper productization](docs/visual-wrapper-productization.md)
- [Visual wrapper spike](docs/visual-wrapper-spike.md)
- [Visual wrapper boundary](docs/visual-wrapper-boundary.md)
- [Transcript samples](docs/transcripts/README_transcripts.md)

## Notes

- **Nesting**: The CLI launches `codex exec` subprocesses. Codex CLI does not require special environment variable handling for nested invocations.
- **Slash tolerance**: The manager LLM sometimes outputs `/plansession` instead of `plansession`. The CLI strips leading slashes before routing.
- **LLM retries**: Both LLM calls (summarizer and manager) retry 3 times with a 5-second wait between attempts, matching the original n8n workflow's `retryOnFail` + `waitBetweenTries: 5000`.
- **Provider preflight**: Normal runs check provider connectivity and model availability before the loop starts. Set `APEX_INFINITE_PROVIDER_CHECK_TIMEOUT` to tune the timeout, and set `APEX_INFINITE_LIVE_OLLAMA=1` to include the opt-in live Ollama pytest.
- **Reference workflow**: The original n8n workflow JSON is preserved in `n8n-workflow/` for reference.
- **DB column naming**: The SQLite `cc_response` column name is preserved for backward compatibility with existing databases. Python variable names use `agent_response` but the DB schema was not migrated to avoid breaking existing history.

## Requirements

- Python 3.10+
- Codex CLI (`codex`) installed and accessible
- An LLM provider API key (Grok, OpenAI) or local Ollama instance
- Optional Linux visual wrapper: PySide6/Qt Quick/QML and Nuitka from
  the `visual` optional dependency extra
