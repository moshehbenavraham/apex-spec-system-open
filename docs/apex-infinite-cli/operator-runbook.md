# Apex Infinite CLI Operator Runbook

## Purpose

This runbook is for humans operating `apex_infinite.py` against a real project.
It assumes the CLI, config, and Codex skill are already installed.

## Prerequisites

- Python 3.10+
- Codex CLI installed and available as `codex`, or a custom `codex.binary`
- A valid `config.yaml`
- Required API keys exported through `.env` or the shell environment
- A target project directory that Codex can access

## Startup Checklist

Before the first run:

1. Confirm `apex-infinite-cli/config.yaml` points at the intended provider and model.
2. Confirm the `codex.exec_flags` value matches the autonomy level you want.
3. Verify the target project already has the Apex Spec skill available if the
   run depends on `apex-spec` workflow commands.
4. Decide whether you want a forced starting command with `--start` or manager
   auto-selection from the first iteration.
5. Decide whether you want the first instruction seeded with `--ceo`.

## Common Run Modes

### Interactive selection

```bash
cd apex-infinite-cli
python apex_infinite.py
```

Use this when you want the CLI to list directories under `~/projects/` and
prompt for the project, start command, and optional CEO instruction.

### Direct execution

```bash
cd apex-infinite-cli
python apex_infinite.py --path ~/projects/my-app/ --start plansession
```

Use this when the target path and first command are already known.

### Dry run

```bash
cd apex-infinite-cli
python apex_infinite.py --path ~/projects/my-app/ --start plansession --dry-run
```

Use this before changing providers, models, or Codex flags. It exercises the
manager loop and prints the exact `codex exec` command without launching Codex.

### History inspection

```bash
cd apex-infinite-cli
python apex_infinite.py --history
python apex_infinite.py --history --path ~/projects/my-app/
```

Use this to inspect the last 50 logged records globally or for a single
normalized project path.

## What Happens Per Iteration

1. Load up to 15 prior records for the project from SQLite.
2. Summarize that history through the summarizer LLM prompt.
3. Choose the next action through the manager LLM prompt, unless `--start`
   overrides iteration 1.
4. Route the decision:
   - Known workflow command -> build a Codex skill invocation prompt
   - `help` -> pause for CEO input
   - `alldonebaby` -> stop and mark the run complete
   - Any other string -> send it to Codex as raw instructions
5. Execute `codex exec`, unless `--dry-run` is enabled.
6. Log the result into `history.db`.
7. Clear the CEO message after one iteration unless a new interruption occurs.

## Operator Controls

### CEO input

- `--ceo "..."` seeds the first iteration with explicit human guidance.
- If the manager outputs `help`, the CLI pauses and prompts for a CEO response.
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
| `*** MANAGER NEEDS CEO HELP ***` | Manager cannot proceed autonomously | Provide one concise unblocker |
| `*** PROJECT COMPLETE! ***` | Manager emitted `alldonebaby` | Stop the run and review deliverables |
| `[TIMEOUT]` | `codex exec` exceeded the timeout | Narrow scope or inspect the underlying command |
| `[ERROR exit code N]` | Codex exited non-zero | Read stderr in the logged response |
| `LLM call failed after 3 attempts` | Provider call exhausted retries | Check API key, base URL, model, or connectivity |

## Safe Shutdown

- Preferred: respond `quit` when prompted after `help` or a CEO interrupt.
- Acceptable: terminate the process if you do not need another history record.
- After exit, use `--history --path ...` to confirm the last recorded state.

## Related Docs

- [History DB reference](history-db.md)
- [Prompt contract](prompt-contract.md)
- [Troubleshooting guide](troubleshooting.md)
