# Behavioral Quality Checklist

Reusable checklist for application-code sessions during implementation and
validation.

## Applicability

Use this checklist when the session produces application code. Skip it for pure
documentation, configuration, or infrastructure-only sessions unless those
changes still introduce runtime behavior.

## Full Implementation Checklist

Before marking a task complete, verify the relevant items:

- [ ] **Resource cleanup**: Every resource acquired in a scoped lifecycle is
  released when that scope ends. No leaked timers, dangling subscriptions,
  unclosed connections, or orphaned async tasks.
- [ ] **Duplicate action prevention**: Every state-mutating operation is
  protected against duplicate triggers while in-flight. No double-submits, no
  unguarded retries, no concurrent write races.
- [ ] **State freshness on re-entry**: When a context is re-entered
  (reopened, revisited, reconnected, retried), state is explicitly reset or
  revalidated. No stale data from a prior lifecycle.
- [ ] **Trust boundary enforcement**: Inputs crossing a trust boundary are
  validated with explicit schema or type checks, and access is authorized at
  the enforcement point closest to the protected resource.
- [ ] **Failure path completeness**: Every operation that can fail has an
  explicit, caller-visible failure path. No silent swallows, blank screens,
  infinite spinners, or generic 500s without controlled handling.
- [ ] **Concurrency safety**: Shared mutable state accessed from multiple
  execution contexts is protected against races. No unguarded
  read-modify-write sequences.
- [ ] **External dependency resilience**: Calls to external systems have a
  timeout, a retry or backoff strategy when appropriate, and a defined failure
  path. No unbounded waits.
- [ ] **Contract alignment**: Interfaces between components match declared
  contracts. Response shapes, event payloads, schemas, and enum handling stay
  aligned.
- [ ] **Error information boundaries**: Errors exposed to external callers
  reveal only stable, intentional information. No stack traces, internal paths,
  or secrets in responses or logs.
- [ ] **Accessibility and platform compliance**: Interactive elements
  participate in the platform's accessibility model with appropriate labels,
  focus handling, and input support.

## Priority Spot-Check for Validation

When validation needs a bounded spot-check, prioritize these categories:

| Priority | Category | FAIL if... |
|----------|----------|------------|
| 1 | Trust boundary enforcement | External input is processed without validation, or access is granted without an authorization check |
| 2 | Resource cleanup | Scoped lifecycle code acquires resources without releasing them on exit |
| 3 | Mutation safety | State-mutating actions can be triggered multiple times while in-flight, or the write path lacks idempotency protection |
| 4 | Failure path completeness | An operation can fail but has no explicit caller-visible failure handling |
| 5 | Contract alignment | The interface between components has a shape mismatch, schema drift, or missing enum handling |

## Usage Notes

- Not every item applies to every task, but every runtime-facing session should
  satisfy the relevant items somewhere
- Implementation uses the full checklist
- Validation uses the priority spot-check when a full re-review is unnecessary
