# 2. Dedicated creview Step

**Status:** Accepted
**Date:** 2026-06-22

## Context

The staged session workflow previously routed directly from `implement` to
`validate`. `implement` is task execution, while `validate` is a read-mostly
gate that decides whether a session can be marked complete. That left no
required remediation pass that inspected all uncommitted work before validation.

Manual edits, generated files, and cross-file side effects can appear outside
the session deliverable list. A session-scoped validation check can miss those
changes, and folding active repair into `validate` would blur the gate's role.

## Decision

Add `creview` as a required staged workflow command between `implement` and
`validate`.

`creview` reviews all uncommitted changes in the working tree, records findings
in `.spec_system/specs/[current-session]/code-review.md`, repairs every
repo-fixable issue it finds, and hands off to `validate` only when the report is
resolved.

## Rationale

- Keeps `implement` focused on completing the planned tasks.
- Keeps `validate` as the objective pass/fail gate.
- Adds a required remediation pass for the full uncommitted surface, including
  manual edits and cross-file drift outside session deliverables.
- Preserves autonomous workflow rules by resolving ambiguity with
  evidence-backed assumptions rather than waiting for human review.

## Consequences

- The staged workflow now has 14 commands and 24 commands total.
- `implement` hands off to `creview`; `creview` hands off to `validate`.
- `validate` requires `code-review.md` with `Result: RESOLVED`.
- Missing, blocked, or unresolved code review routes back to `creview`; ordinary
  validation failures still route to `implement`.
