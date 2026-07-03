# Apex Infinite CLI Operator Runbook

## Purpose

This runbook is for humans operating `apex-infinite` against a real project.
It assumes the CLI, config, and Codex skill are already installed.

## Prerequisites

- Python 3.10+
- Codex CLI installed and available as `codex`, or a custom `codex.binary`
- A valid `config.yaml`
- Required API keys exported through `.env` or the shell environment
- A target project directory that Codex can access

## Startup Checklist

Before the first run:

1. Confirm `src/apex_infinite/config.yaml` or your `--config` file points at the intended provider and model.
2. Confirm the `codex.exec_flags` value matches the autonomy level you want.
3. Run `apex-infinite --check-provider` or
   `scripts/check-ollama.sh --chat` for local Ollama.
4. Verify the target project already has the Apex Spec skill available if the
   run depends on `apex-spec` workflow commands.
5. Decide whether you want a forced starting command with `--start` or manager
   auto-selection from the first iteration.
6. Decide whether you want the first instruction seeded with `--ceo`.
7. Decide which display mode fits the terminal: styled interactive output,
   plain logs, ASCII-safe output, compact output, or machine-output JSONL.

## Common Run Modes

### Interactive selection

```bash
cd apex-infinite-cli
apex-infinite
```

Use this when you want the CLI to list directories under `~/projects/` and
prompt for the project, start command, and optional CEO instruction.

### Direct execution

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --start plansession
```

Use this when the target path and first command are already known.

### Provider preflight

```bash
cd apex-infinite-cli
apex-infinite --check-provider
apex-infinite --check-provider --check-provider-chat
scripts/check-ollama.sh --chat
```

Use this before unattended runs. Normal runs execute the model-list preflight
before the loop starts; `--check-provider-chat` adds a tiny chat completion.
Use `--skip-provider-check` only for intentional offline wiring checks.

### Dry run

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --start plansession --dry-run
```

Use this before changing providers, models, or Codex flags. It exercises the
manager loop and prints the exact `codex exec` command without launching Codex.

### Styled interactive terminal

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --theme crt-green
apex-infinite --path ~/projects/my-app/ --theme crt-amber
apex-infinite --path ~/projects/my-app/ --theme ibm-dos
```

Use this when the terminal supports color and normal Rich rendering. `auto`
selects `crt-green` in capable interactive terminals. Use an explicit
`--theme` when you want to opt back into styled output after an environment
constraint such as `NO_COLOR`.

### Plain, ASCII, and compact fallbacks

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --plain
apex-infinite --path ~/projects/my-app/ --plain --ascii
apex-infinite --path ~/projects/my-app/ --plain --ascii --compact
```

Use `--plain` for CI, logs, redirected output, remote shells, unreadable color
schemes, or `TERM=dumb`. Use `--ascii` when the terminal cannot render
non-ASCII glyphs reliably. Use `--compact` when the terminal height is limited
or you are collecting logs, but still expect errors, manager reasons, prompts,
DB writes, completion, timeouts, interrupts, and non-zero exits to remain
visible.

Environment behavior:

- `NO_COLOR` behaves like plain mode unless you pass an explicit `--theme`.
- `TERM=dumb`, non-TTY output, redirected output, and non-terminal Rich console
  paths default to plain output unless you force a theme.
- Non-UTF terminals should use `--ascii`, usually with `--plain`.
- Narrow terminals should use `--compact` and inspect history with
  `--history --verbose` only when needed.

### Event stream file

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --event-stream /tmp/apex-events.jsonl
```

Use this when another process should observe lifecycle facts while a human
operator still sees the normal CLI surface. The file is JSONL and is flushed
after every event.

### Machine-output JSONL

```bash
cd apex-infinite-cli
apex-infinite --path ~/projects/my-app/ --event-stream - --machine-output
```

Use this for wrappers or automation that read stdout. In this mode stdout is
reserved for JSONL events. Human rendering, terminal bell, and desktop
notifications are disabled.

Do not use `--event-stream -` without `--machine-output`; the CLI rejects that
combination so human output never mixes with JSONL on stdout. If a human should
watch the run while automation observes it, write events to a file path instead
of stdout.

### Optional visual wrapper source mode

```bash
cd apex-infinite-cli
python -m pip install -e ".[visual]"
apex-infinite-visual --dry-run --max-iterations 1
```

Use this only for the Linux visual wrapper source mode. The base CLI install
remains the default `pyproject.toml` dependency set; PySide6 and QML stay in
the optional `visual` extra.
Session 08 release verification keeps source/dev operation shippable after
final gates; final AppImage or binary publication remains gated for future
packaging, license, notice, checksum, and source/relink review.

Source-mode settings can be selected before launch:

```bash
cd apex-infinite-cli
apex-infinite-visual \
  --theme crt-amber \
  --effect-intensity 55 \
  --font-family "monospace" \
  --font-scale 1.05 \
  --plain-fallback
```

The wrapper supports green CRT, amber CRT, IBM DOS, and plain presets, plus
effect intensity, font family, font scale, reduced effects, and plain fallback.

For a headless smoke check:

```bash
cd apex-infinite-cli
QT_QPA_PLATFORM=offscreen apex-infinite-visual \
  --dry-run --max-iterations 1 --auto-close-ms 900
```

By default, wrapper dry-run uses fixture events so it does not require provider
API keys or live Codex execution. To launch the real CLI subprocess, pass
`--launch-cli`; the wrapper will build a guarded
`--event-stream - --machine-output` command and keep stderr separate for
failure display.

Fallback behavior:

- If PySide6 is missing, install `.[visual]`.
- If a display backend is unavailable, run the offscreen smoke command or use
  the base terminal CLI.
- If events are malformed, the wrapper shows an error state and keeps the log
  bounded instead of crashing.
- If the subprocess writes stderr or exits non-zero, the wrapper maps that to a
  visible error state.
- If the subprocess times out or the base CLI module cannot be launched, the
  wrapper maps that to `Timed out` or `CLI missing`.

### History inspection

```bash
cd apex-infinite-cli
apex-infinite --history
apex-infinite --history --path ~/projects/my-app/
apex-infinite --history --verbose
```

Use this to inspect the last 50 logged records globally or for a single
normalized project path. Default history is a compact ledger with timestamp,
status, project key, command, reason, and response summary. Add `--verbose` to
expand reason, response, and stored-state detail.

## What Happens Per Iteration

1. Load up to 15 prior records for the project from SQLite.
2. Summarize that history through the summarizer LLM prompt.
3. Choose the next action through the manager LLM prompt, unless `--start`
   overrides iteration 1.
4. Route the decision:
   - Known workflow command -> build a Codex skill invocation prompt
   - `help` -> emergency operator pause outside the normal workflow
   - `alldonebaby` -> stop and mark the run complete
   - Any other string -> send it to Codex as raw instructions
5. Execute `codex exec`, unless `--dry-run` is enabled.
6. Log the result into `history.db`.
7. Clear the CEO message after one iteration unless a new interruption occurs.

## Operator Controls

### Operator input

- `--ceo "..."` seeds the first iteration with explicit operator guidance.
- Normal manager routing should follow the latest command's `Next command:`
  line, not pause for input.
- If the manager outputs `help`, the CLI pauses and prompts for an operator
  response. Treat this as an emergency escape hatch, not standard workflow.
- If the manager does not need help, the CEO message is consumed once and then
  cleared.

### Interrupt handling

- Press `Ctrl+C` once to request a pause after the current step.
- At the next loop boundary the CLI prompts for CEO instructions or `quit`.
- Press `Ctrl+C` twice if you want to force exit immediately.

### Output depth

- Default mode prints a truncated agent response panel.
- `--verbose` prints a larger panel with up to 2000 characters of the full
  response.
- With `--history`, `--verbose` expands ledger details instead of adding a
  separate history-only flag.

## Recommended Operating Pattern

For a new project:

1. Run with `--dry-run` first.
2. Confirm the chosen provider, model, and Codex binary are correct.
3. Start with an explicit command such as `--start plansession`.
4. Add `--ceo` only for real constraints or priorities, not for routine noise.
5. Inspect history after major transitions with `--history --path ...`.

For an existing project:

1. Reuse the exact same path string you used before.
2. Review the recent history table before resuming.
3. Resume with `--start` only if you want to override manager autonomy.

## Signals To Watch

| Signal | Meaning | Action |
|--------|---------|--------|
| `Manager Decision:` | Current loop decision | Confirm it matches the project state |
| `*** MANAGER NEEDS CEO HELP ***` | Emergency pause outside normal workflow | Provide one concise external unblocker or restart with `--start` |
| `*** PROJECT COMPLETE! ***` | Manager emitted `alldonebaby` | Stop the run and review deliverables |
| `[TIMEOUT]` | `codex exec` exceeded the timeout | Narrow scope or inspect the underlying command |
| `[ERROR exit code N]` | Codex exited non-zero | Read stderr in the logged response |
| `LLM call failed after 3 attempts` | Provider call exhausted retries | Check API key, base URL, model, or connectivity |
| `event_stream_error` | Machine-readable event stream failure | Inspect the source event and retry with a writable path |
| `Output fallback: NO_COLOR` | Color was disabled by environment | Use plain output or pass an explicit `--theme` if color is intentional |
| `Output fallback: TERM=dumb` | Terminal reported a constrained mode | Use `--plain --ascii --compact` or a richer terminal |
| `Output fallback: non-terminal output` | Output is redirected or not attached to a terminal | Keep plain logs or pass an explicit `--theme` only for a capable destination |

## Safe Shutdown

- Preferred: respond `quit` when prompted after `help` or an operator interrupt.
- Acceptable: terminate the process if you do not need another history record.
- After exit, use `--history --path ...` to confirm the last recorded state.

## Sample References

- [Plain dry-run transcript](transcripts/dry-run-plain.txt) shows a
  deterministic `--plain --ascii --compact --dry-run` run.
- [History ledger transcript](transcripts/history-ledger.txt) shows compact and
  verbose history display semantics.
- [Machine-output JSONL sample](transcripts/machine-output-events.jsonl) shows
  the stdout JSONL shape for wrappers and automation.
- [Visual wrapper productization](visual-wrapper-productization.md) records
  source-mode setup, settings, packaging gates, checksums, license notes, and
  clean-room verification.
- [Visual wrapper spike](visual-wrapper-spike.md) records the original wrapper
  decision, license notes, packaging risks, and backup path.

## Related Docs

- [History DB reference](history-db.md)
- [Event stream contract](event-stream.md)
- [Prompt contract](prompt-contract.md)
- [Troubleshooting guide](troubleshooting.md)
- [Visual wrapper productization](visual-wrapper-productization.md)
- [Visual wrapper spike](visual-wrapper-spike.md)
- [Visual wrapper boundary](visual-wrapper-boundary.md)
- [Transcript samples](transcripts/README_transcripts.md)
