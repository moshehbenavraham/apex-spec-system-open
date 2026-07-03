# Apex Infinite CLI Transcripts

This directory contains deterministic text fixtures for documentation and
wrapper planning. They are not live terminal captures and they are not
screenshots. Keep every file ASCII-only with Unix LF endings.

## Samples

| File | Purpose |
|------|---------|
| `dry-run-plain.txt` | Plain, ASCII, compact dry-run output showing startup, UI resolution, prompt preview, dry-run execution, DB logging, and safety stop visibility. |
| `history-ledger.txt` | History display output showing compact ledger fields, truncation counts, verbose expansion, and raw-storage boundaries. |
| `machine-output-events.jsonl` | One JSON object per line for a dry-run machine-output event stream. |

## Usage Rules

- Treat samples as documentation fixtures, not golden snapshots for tests.
- Do not paste real provider keys, operator secrets, private project names, or
  customer data into samples.
- Do not include ANSI escapes, Rich markup, box-drawing glyphs, QML, shaders,
  image data, fonts, icons, binary screenshots, or terminal-control sequences.
- Keep sample paths generic, such as `/home/user/projects/my-app/`.
- Keep prompt and response text bounded. Show lengths or summaries when full
  text is not needed to explain behavior.
- Update the related README, runbook, event-stream, history, and
  troubleshooting docs when a sample changes a documented behavior.

## Relationship To The CLI

The samples reflect the current CLI contracts:

- Human output stays human-readable unless `--machine-output` is active.
- File event streams are side channels and do not change terminal output.
- `--event-stream - --machine-output` reserves stdout for JSONL only.
- History display derives labels and truncation at render time; SQLite keeps
  raw workflow facts.
- Future visual wrappers consume JSONL events or the importable event API, not
  Rich panels, plain human output, or history display rows.

## Regeneration Guidance

When behavior changes, prefer fixture-style regeneration from isolated
dry-runs, temporary projects, and temporary history databases. Real provider
calls and real Codex subprocesses are not required for these documentation
samples.

## Related Docs

- [CLI README](../../README.md)
- [Operator runbook](../operator-runbook.md)
- [Event stream contract](../event-stream.md)
- [History DB reference](../history-db.md)
- [Prompt contract](../prompt-contract.md)
- [Troubleshooting guide](../troubleshooting.md)
- [Visual wrapper boundary](../visual-wrapper-boundary.md)
