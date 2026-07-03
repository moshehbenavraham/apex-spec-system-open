# Apex Infinite CLI Troubleshooting

## First-Line Diagnostics

Start here before deeper debugging:

1. Re-run with `--dry-run` to inspect the chosen prompt and `codex exec` flags.
2. Run `python apex_infinite.py --check-provider` to test provider connectivity
   and configured model availability.
3. Re-run with `--verbose` to inspect more of the Codex response.
4. Check `python apex_infinite.py --history --path <project>` to see the last
   recorded decisions.
5. Confirm `config.yaml` and `.env` are the files you think they are.

## Common Failures

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `No config.yaml found. Use --config to specify path.` | You launched from a directory without `config.yaml` and did not pass `--config` | Run from `apex-infinite-cli/` or pass `--config /abs/path/to/config.yaml` |
| `Config file not found: ...` | Bad `--config` path | Fix the path and retry |
| `Unknown provider: ...` | `provider` does not match a key under `providers` | Fix `config.yaml` or override with `--provider` |
| `Directory not found: ...` | Bad `--path` value | Use an existing directory |
| `Provider preflight failed for ... could not list models` | Provider URL is wrong, Ollama is not running, or a hosted provider is unreachable | Check `.env`, `config.yaml`, and network/provider status; for Ollama run `scripts/check-ollama.sh` |
| `configured model '...' is not available` | The selected model is not installed or not exposed by the provider | Pull/install the model or change `OLLAMA_MODEL`/`--model` |
| `Invalid selection.` | Interactive project number was out of range | Re-run and choose a valid entry |
| `[ERROR] 'codex' command not found. Is Codex CLI installed?` | Codex CLI is missing or not on `PATH` | Install Codex or set `codex.binary` in `config.yaml` |
| `[TIMEOUT] Codex command timed out after 1800s` | The underlying Codex step ran too long | Narrow the task, inspect the project state, or re-run with clearer CEO guidance |
| `LLM call failed after 3 attempts` | Provider outage, bad API key, wrong base URL, or bad model name | Check `.env`, `config.yaml`, connectivity, and provider status |
| `Could not parse LLM response as JSON, using raw output` | Manager returned malformed JSON | Review the raw output in history and decide whether the manager prompt needs tightening |
| `--event-stream - requires --machine-output` | Stdout JSONL was requested while human output was still enabled | Add `--machine-output` or write events to a file path |
| `--machine-output requires --event-stream` | Machine-output mode has no JSONL destination | Pass `--event-stream -` or a file path |
| `Event stream error: ...` | The event path is not writable or a payload failed validation | Use a writable path and inspect recent changes for unsafe event payload values |
| Output colors are unreadable | Terminal palette clashes with the selected theme | Use `--plain`, choose another `--theme`, or set `NO_COLOR=1` |
| Output shows broken glyphs | Terminal encoding cannot render non-ASCII glyphs | Use `--ascii`, usually with `--plain` |
| Output wraps too much | Terminal width or log viewer is narrow | Use `--compact` and inspect details with `--verbose` only when needed |
| JSONL has terminal text mixed in | Human rendering and stdout events were mixed by a wrapper | Use `--event-stream - --machine-output` or write events to a file |
| Visual wrapper shows `CLI missing` | The wrapper could not find the source-tree `apex_infinite.py` script | Run from `apex-infinite-cli/`, reinstall the source tree, or launch the base CLI directly |
| Visual wrapper shows `Timed out` | The wrapped base CLI exceeded the wrapper process timeout | Re-run the base CLI command directly, reduce scope, or increase `--process-timeout-seconds` |

## Path And History Issues

### History looks split across the same project

Cause:

- the CLI normalizes trailing slashes, but it does not canonicalize symlinks or
  convert all equivalent paths to one identity

What to do:

- keep using the same absolute path string for the same project
- avoid mixing symlinked and non-symlinked paths

### `--history --path` shows no rows

Cause:

- the stored path key does not match the exact normalized string you passed

What to do:

- try `python apex_infinite.py --history` without `--path`
- inspect the recorded path values in the history table

## Manager Behavior Issues

### The manager keeps asking for `help`

Common causes:

- the manager ignored the latest command's `Next command:` line
- Codex reported an external blocker and the manager over-escalated it
- recent history lacks the final command summary

What to do:

1. If you already know the correct next command, restart with `--start`.
2. Inspect the latest Codex response for `Next command:` and `Reason:`.
3. If the manager is over-escalating, inspect recent history and the Codex
   response that triggered the pause.

### The manager chooses the wrong next command

What to do:

1. Use `--start` to force the next iteration.
2. Add a short `--ceo` instruction for the next run.
3. Review the recent history summary inputs if the run has drifted.

## Codex Execution Issues

### Codex exits non-zero

The CLI wraps the result as:

```text
[ERROR exit code N]
stdout: ...
stderr: ...
```

What to do:

- read stderr first
- inspect the underlying project for missing dependencies or broken state
- rerun with `--verbose` if the default output was truncated

### No desktop notification appears

Cause:

- `notify-send` is optional and Linux-specific
- notifications are intentionally disabled in `--machine-output` mode

What to do:

- nothing, unless you rely on desktop notifications
- the terminal bell still fires
- in machine-output mode, consume the JSONL stop/help/error events instead

## Display And Terminal Issues

### Colors are unreadable

Cause:

- the active terminal palette conflicts with the selected theme
- `auto` selected a styled theme in an interactive terminal
- a remote terminal or multiplexed shell remapped colors

What to do:

- run with `--plain`
- try another explicit theme such as `--theme crt-amber` or `--theme ibm-dos`
- set `NO_COLOR=1` for the shell or CI job
- keep `--event-stream PATH` separate if automation still needs lifecycle
  events

### Non-UTF or non-ASCII terminal renders broken symbols

Cause:

- the terminal cannot render Unicode glyphs used by styled Rich panels
- a remote shell or log collector down-converts output

What to do:

- run with `--ascii`
- add `--plain` when color or panel rendering is also unreliable
- use `--plain --ascii --compact` for the most conservative output

### Narrow terminal or log viewer is hard to scan

Cause:

- the terminal width is too small for comfortable panels
- a CI log viewer wraps long paths, reasons, or responses

What to do:

- run with `--compact`
- use `--history` for the compact ledger
- add `--history --verbose` only when you need expanded reason and response
  detail

### `NO_COLOR` or `TERM=dumb` forced plain output

Cause:

- environment constraints intentionally default to plain output

What to do:

- accept plain output for logs, CI, and constrained terminals
- pass an explicit `--theme` only when the destination really supports styled
  output
- keep `--ascii` if the terminal has encoding limitations

### Redirected output or remote shell lost the operator-console look

Cause:

- non-TTY output defaults to plain so logs do not contain terminal formatting
- remote shells may report limited terminal capabilities

What to do:

- use `--plain --ascii --compact` for deterministic logs
- write lifecycle events to a file with `--event-stream /tmp/apex-events.jsonl`
- use stdout JSONL only with `--event-stream - --machine-output`

## Event Stream Issues

### JSONL output contains human text

Cause:

- `--event-stream -` was not used with `--machine-output`
- another wrapper or shell script is writing to stdout around the CLI

What to do:

- run `python apex_infinite.py --event-stream - --machine-output ...`
- if you need human output too, write events to a file path instead of stdout

### Event file is empty

Cause:

- the process failed before startup events were written
- the path points somewhere different than expected
- the process could not write the file

What to do:

- retry with an absolute path under `/tmp`
- check the terminal for an `Event Stream` error
- verify parent directory permissions

### Wrapper sees malformed events

Cause:

- the wrapper is reading partial lines
- the wrapper is parsing human output instead of JSONL

What to do:

- read one full line at a time
- parse only the JSONL stream from `--event-stream` or the importable event API
- ignore Rich output and history display rows

### Wrapper state disagrees with terminal output

Cause:

- the wrapper scraped Rich panels, plain text, or history rows instead of
  consuming event payloads
- the wrapper treated display-only labels as workflow state

What to do:

- consume JSONL events from `--event-stream PATH`
- use `--event-stream - --machine-output` only when stdout must be JSONL
- keep wrapper state derived from events or the importable event API
- read [Visual wrapper boundary](visual-wrapper-boundary.md) before adding
  wrapper behavior

## Visual Wrapper Source Mode Issues

### `Visual wrapper unavailable: PySide6 is not installed`

Cause:

- the optional wrapper dependencies are not installed in the active Python
  environment

What to do:

```bash
cd apex-infinite-cli
pip install -r requirements-wrapper.txt
python -m apex_infinite_visual.main --dry-run --max-iterations 1
```

### Qt display backend is unavailable

Cause:

- no graphical session is available
- the Qt platform plugin cannot connect to X11 or Wayland
- the wrapper is running in CI or a headless shell

What to do:

```bash
cd apex-infinite-cli
QT_QPA_PLATFORM=offscreen python -m apex_infinite_visual.main \
  --dry-run --max-iterations 1 --auto-close-ms 900
```

If offscreen mode is not enough for local operation, use the base terminal CLI
until the display backend is fixed.

### Wrapper shows `CLI missing`

Cause:

- the wrapper cannot resolve the source-tree `apex_infinite.py` file
- the wrapper is being launched from a moved or partial source checkout

What to do:

- run from the `apex-infinite-cli/` source directory
- confirm `apex_infinite.py` exists next to `apex_infinite_visual/`
- use the base terminal CLI until the source checkout is repaired

### Wrapper shows malformed event state

Cause:

- the wrapper received partial JSONL
- stdout contained non-JSON text
- an event used an unsupported version or event name
- an event payload failed the base event payload validator

What to do:

- launch the real CLI through wrapper `--launch-cli` or use
  `python apex_infinite.py --event-stream - --machine-output`
- read complete lines only
- keep stderr separate from stdout JSONL
- inspect the wrapper log for the rejected event reason

### Wrapper shows subprocess failure state

Cause:

- the base CLI process wrote stderr
- the base CLI process exited non-zero
- the configured project path, config path, provider, or model is invalid

What to do:

- rerun the equivalent base CLI command directly with `--event-stream -`
  and `--machine-output`
- fix the base CLI startup error first
- use fixture-backed wrapper dry-run when provider credentials are unavailable

### Wrapper shows timeout state

Cause:

- the wrapped base CLI exceeded `--process-timeout-seconds`
- the underlying Codex or provider step is slow or waiting on an external
  requirement

What to do:

- rerun the equivalent base CLI command directly with `--verbose`
- narrow the target project task or use `--dry-run`
- increase `--process-timeout-seconds` only when the longer wait is expected

### AppImage or packaging review fails

Cause:

- generated bundle contents, Qt modules, notices, source/relink instructions,
  or checksums have not been reviewed
- `pyside6-deploy` or Nuitka generated files are unstable in the local
  environment

What to do:

- do not publish the binary artifact
- keep generated files out of the repo unless a release session scopes them
- follow [Visual wrapper productization](visual-wrapper-productization.md)
  for license notices, checksums, source/relink obligations, and clean-room
  checks
- use source visual mode until release verification passes

### Clean-room audit fails

Cause:

- copied reference QML, shaders, assets, fonts, icons, profiles, resource
  manifests, build scripts, terminal-emulator code, qmltermwidget, or
  QTermWidget material entered the tracked wrapper files

What to do:

- remove the copied material
- keep only independently written QML, Python, docs, and tests
- re-read [Visual wrapper boundary](visual-wrapper-boundary.md)
- compare against [Visual wrapper spike](visual-wrapper-spike.md) for the
  accepted prototype constraints

## Config Issues

### API key does not seem to load

Checks:

- confirm the provider string field uses `${ENV_VAR}` syntax
- confirm the variable exists in `.env` next to `config.yaml` or in the shell
- confirm you are using the provider you think you are using

### Provider override does not change the model

Cause:

- `--provider` changes the active provider, but the selected provider still
  uses the model defined in its config unless you also pass `--model`

What to do:

- pass both `--provider` and `--model` when you want an explicit pair

### Local Ollama check fails

Checks:

- confirm Ollama is running and serving the configured `OLLAMA_PORT`
- run `scripts/check-ollama.sh --chat` from `apex-infinite-cli/`
- run `ollama list` and confirm the configured `OLLAMA_MODEL` is present
- set `APEX_INFINITE_PROVIDER_CHECK_TIMEOUT=30` for slow local hardware
- use `--skip-provider-check` only when intentionally testing offline CLI wiring

## Recovery Shortcuts

Use these commands when the system is behaving unexpectedly:

```bash
cd apex-infinite-cli
python apex_infinite.py --history
python apex_infinite.py --path ~/projects/my-app/ --history
python apex_infinite.py --check-provider --provider ollama
scripts/check-ollama.sh --chat
python apex_infinite.py --path ~/projects/my-app/ --start plansession --dry-run
python apex_infinite.py --path ~/projects/my-app/ --start implement --verbose
```

## When To Edit Code Instead Of Configuration

Configuration is usually enough for:

- provider selection
- model changes
- Codex binary path
- Codex execution flags

Code changes are justified for:

- different history schema
- different manager output parsing
- different prompt templates
- different interrupt or notification behavior

## Related Docs

- [Operator runbook](operator-runbook.md)
- [Event stream contract](event-stream.md)
- [History DB reference](history-db.md)
- [Prompt contract](prompt-contract.md)
- [Visual wrapper productization](visual-wrapper-productization.md)
- [Visual wrapper spike](visual-wrapper-spike.md)
- [Visual wrapper boundary](visual-wrapper-boundary.md)
- [Transcript samples](transcripts/README_transcripts.md)
