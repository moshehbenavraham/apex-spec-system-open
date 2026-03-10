# Apex Infinite CLI History DB

## Purpose

`history.db` is the CLI's local memory. It stores prior agent responses,
manager decisions, and special stop/help markers so the next iteration can
summarize recent context.

## Location

- Directory: `~/.apex-infinite/`
- Database file: `~/.apex-infinite/history.db`

The directory is created automatically on startup if it does not exist.

## Storage Mode

- SQLite
- `PRAGMA journal_mode=WAL`
- One table: `history`
- One index: `idx_path_created`

WAL improves durability and avoids blocking most reads while writes are active.

## Schema

The current schema is:

| Column | Type | Meaning |
|--------|------|---------|
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | Monotonic record ID |
| `path` | `TEXT NOT NULL` | Project path key used to scope history |
| `cc_response` | `TEXT` | Raw Codex response text for the iteration |
| `ai_decision_output` | `TEXT` | Manager output value, such as `implement` or `help` |
| `ai_decision_reason` | `TEXT` | Manager explanation for the decision |
| `help_or_done_msg` | `TEXT` | Special marker for `help` or `alldonebaby` cases |
| `created_at` | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | Insert time |

## Compatibility Note

The `cc_response` column name is legacy. Python variables now use
`agent_response`, but the database schema intentionally preserves the old
column name to avoid migrating existing history files.

## Path Normalization

History is grouped by the exact `path` value stored in the database.

Before logging, the CLI:

1. Expands `~`
2. Verifies the directory exists
3. Strips any trailing slash
4. Re-appends a single trailing slash

That means `/tmp/project` and `/tmp/project/` collapse to the same history key,
but different symlinked or alternate absolute paths will still be treated as
different projects.

## Write Behavior

One row is written per loop iteration after a decision is made.

- Normal iteration: logs agent response, manager output, and manager reason
- `help`: logs the pause request and stores the help reason in
  `help_or_done_msg`
- `alldonebaby`: logs completion and stores `ALL DONE BABY!` in
  `help_or_done_msg`

## Read Behavior

The CLI uses the database in two ways:

- Decision loop: reads the most recent 15 rows for the current project
- `--history`: shows up to 50 rows, either globally or for one project path

## History Summary Input Format

Before summarization, each fetched row is transformed into this structure:

```text
[Task N: <path>_<id>]
Agent: <cc_response>
Manager: Manager - Output: <ai_decision_output> | Reason: <ai_decision_reason>
```

Those blocks are then joined with blank lines and sent to the summarizer LLM.

## Useful Queries

Inspect the last 20 records:

```bash
sqlite3 ~/.apex-infinite/history.db \
  "SELECT id, path, ai_decision_output, created_at FROM history ORDER BY id DESC LIMIT 20;"
```

Inspect one project:

```bash
sqlite3 ~/.apex-infinite/history.db \
  "SELECT id, ai_decision_output, ai_decision_reason, help_or_done_msg, created_at \
   FROM history WHERE path = '/home/user/projects/my-app/' ORDER BY id DESC LIMIT 20;"
```

Count records by project:

```bash
sqlite3 ~/.apex-infinite/history.db \
  "SELECT path, COUNT(*) FROM history GROUP BY path ORDER BY COUNT(*) DESC;"
```

## Operational Guidance

- Treat the DB as local state, not a shared source of truth across machines.
- Back it up before manual edits if you care about historical continuity.
- Prefer reading with `sqlite3` over editing rows directly.
- If you intentionally want a clean slate, archive or remove the DB file while
  the CLI is not running.

## Related Docs

- [Operator runbook](operator-runbook.md)
- [Prompt contract](prompt-contract.md)
- [Troubleshooting guide](troubleshooting.md)
