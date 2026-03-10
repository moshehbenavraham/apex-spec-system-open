# Apex Infinite CLI Troubleshooting

## First-Line Diagnostics

Start here before deeper debugging:

1. Re-run with `--dry-run` to inspect the chosen prompt and `codex exec` flags.
2. Re-run with `--verbose` to inspect more of the Codex response.
3. Check `python apex_infinite.py --history --path <project>` to see the last
   recorded decisions.
4. Confirm `config.yaml` and `.env` are the files you think they are.

## Common Failures

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `No config.yaml found. Use --config to specify path.` | You launched from a directory without `config.yaml` and did not pass `--config` | Run from `apex-infinite-cli/` or pass `--config /abs/path/to/config.yaml` |
| `Config file not found: ...` | Bad `--config` path | Fix the path and retry |
| `Unknown provider: ...` | `provider` does not match a key under `providers` | Fix `config.yaml` or override with `--provider` |
| `Directory not found: ...` | Bad `--path` value | Use an existing directory |
| `Invalid selection.` | Interactive project number was out of range | Re-run and choose a valid entry |
| `[ERROR] 'codex' command not found. Is Codex CLI installed?` | Codex CLI is missing or not on `PATH` | Install Codex or set `codex.binary` in `config.yaml` |
| `[TIMEOUT] Codex command timed out after 1800s` | The underlying Codex step ran too long | Narrow the task, inspect the project state, or re-run with clearer CEO guidance |
| `LLM call failed after 3 attempts` | Provider outage, bad API key, wrong base URL, or bad model name | Check `.env`, `config.yaml`, connectivity, and provider status |
| `Could not parse LLM response as JSON, using raw output` | Manager returned malformed JSON | Review the raw output in history and decide whether the manager prompt needs tightening |

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

- the project needs a real human choice
- the manager lacks a concrete next step
- Codex reported a blocker that the manager treats as requiring CEO input

What to do:

1. Reply with one concise decision, not a long paragraph.
2. If you already know the correct next command, restart with `--start`.
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

What to do:

- nothing, unless you rely on desktop notifications
- the terminal bell still fires

## Config Issues

### API key does not seem to load

Checks:

- confirm the provider `api_key` field uses `${ENV_VAR}` syntax
- confirm the variable exists in `.env` next to `config.yaml` or in the shell
- confirm you are using the provider you think you are using

### Provider override does not change the model

Cause:

- `--provider` changes the active provider, but the selected provider still
  uses the model defined in its config unless you also pass `--model`

What to do:

- pass both `--provider` and `--model` when you want an explicit pair

## Recovery Shortcuts

Use these commands when the system is behaving unexpectedly:

```bash
cd apex-infinite-cli
python apex_infinite.py --history
python apex_infinite.py --path ~/projects/my-app/ --history
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
- [History DB reference](history-db.md)
- [Prompt contract](prompt-contract.md)
