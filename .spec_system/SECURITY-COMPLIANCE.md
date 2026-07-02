# Security & Compliance

> Cumulative security posture, privacy, and license-compliance record.
> **Line budget**: 1000 max | **Last updated**: Phase 00 planning (2026-07-02)

---

## Current Security Posture

### Overall: WATCH

The project is a local autonomous CLI workflow runner. It has useful baseline
controls, but it is not yet in a clean state because Phase 00 has not run and
several planned controls are still unimplemented.

| Metric | Value |
|--------|-------|
| Open Findings | 6 |
| Critical/High | 0 |
| Medium/Low | 6 |
| Phases Audited | 0 |
| Last Clean Phase | -- |

## Protected Assets

- Provider API keys and environment-loaded secrets.
- Target project source trees modified by autonomous subprocesses.
- Local workflow history and operator instructions.
- Manager and summarizer prompt contracts.
- Machine-readable lifecycle payloads planned for future wrapper surfaces.
- Clean-room visual implementation and license boundaries.

## Implemented Controls

| Area | Control | Status |
|------|---------|--------|
| Secrets | Provider keys are configured through environment-expanded values and `.env` is ignored by Git. | Partial |
| Database | Local SQLite history uses parameterized queries and WAL mode. | Present |
| Subprocess | Agent execution uses an argument list rather than shell invocation and has a 30 minute timeout. | Present |
| Runaway guard | The loop has a default max-iteration limit and dry-run mode. | Present |
| Operator stop | Single interrupt requests a pause; second interrupt exits. | Present |
| Compatibility | The legacy history column is preserved to avoid breaking existing databases. | Present |
| Base install | The terminal CLI runtime does not require graphical dependencies. | Present |

## Open Findings

### Critical / High

*No open critical or high findings.*

### Medium / Low

| ID | Severity | Finding | Required Action |
|----|----------|---------|-----------------|
| F001 | Medium | Local history stores raw agent output, manager decisions, reasons, project paths, timestamps, and operator instructions without redaction or retention limits. | Add redaction tests and document retention or purge behavior. |
| F002 | Medium | The default agent execution flags grant broad autonomous approval for target-project changes. | Require operator review of the target path and execution flags before real runs; consider a safer documented default. |
| F003 | Medium | Recent history, latest agent output, summaries, and operator instructions can be sent to the configured LLM provider. | Document third-party data transfer expectations and warn operators not to include secrets or personal data. |
| F004 | Low | Dependency files use lower-bound version ranges and no automated vulnerability audit is configured for the Python runtime dependencies. | Add dependency scanning or a lock/audit workflow. |
| F005 | Low | Planned event-stream payloads are not implemented yet, so no tests currently prove that machine output excludes secrets, ANSI escapes, Rich markup, or frame glyphs. | Add event payload safety tests when the event stream is implemented. |
| F006 | Low | Future visual-wrapper work depends on maintaining a clean-room boundary from GPL-family visual reference material. | Before wrapper release, audit that no code, shaders, images, icons, fonts, resource manifests, build scripts, or profile data were copied. |

## GDPR Compliance Status

### Overall: LIMITED / LOCAL TOOL

The project is not an end-user data service, but it can process operator text,
target-project paths, agent responses, and provider-bound prompts. Treat the
history database and provider requests as potentially sensitive operational
data.

### Personal Data Inventory

| Data Type | Storage / Transfer | Purpose | Risk |
|-----------|--------------------|---------|------|
| Project path | Local SQLite history | Scope workflow history to a project | Low |
| Operator instructions | Local SQLite history and LLM prompts | Guide workflow decisions | Medium |
| Agent responses | Local SQLite history and LLM prompts | Resume and route workflow state | Medium |
| Manager decisions and reasons | Local SQLite history | Audit and resume workflow state | Low |
| Provider API keys | Environment or `.env`; passed to provider client | Authenticate provider calls | Medium |
| Desktop notification text | Local OS notification command | Alert operator on pause or completion | Low |

### Compliance Checklist

| Requirement | Status | Notes |
|------------|--------|-------|
| Data collection has documented purpose | Partial | Local history exists to resume and summarize workflow state. |
| Consent obtained before data storage | Partial | Operator starts the CLI, but there is no explicit first-run privacy notice. |
| Data minimization verified | Partial | Only recent rows are summarized, but raw history is retained indefinitely. |
| Deletion/erasure path exists | Partial | Manual deletion of the local database works; no CLI purge command exists. |
| No PII in application logs | Open | No intentional PII collection, but raw prompts and outputs are not scrubbed. |
| Third-party transfers documented | Partial | Provider-bound prompt traffic is known; provider-specific legal posture is not recorded. |
| Secrets excluded from durable records | Open | Config avoids direct secret storage, but raw agent output can still contain secrets. |

## Dependency Security

Runtime dependencies currently include Click, OpenAI Python SDK, python-dotenv,
Rich, PyYAML, and Python standard library modules including SQLite and
subprocess support. Development dependencies include pytest, pytest-cov,
pytest-mock, black, and pylint.

No automated Python vulnerability audit, dependency lock, or security CI gate
is currently recorded for this CLI scope.

## License Compliance

| Area | Status | Notes |
|------|--------|-------|
| Base CLI dependencies | Acceptable | Runtime dependency set is terminal-only and does not include graphical wrapper dependencies. |
| Visual inspiration boundary | Open | Use independent design tokens, layouts, settings, and effects. Do not copy implementation material or assets. |
| Optional wrapper dependencies | Planned | Any Linux visual wrapper must keep graphical dependencies optional and document LGPLv3/commercial obligations where applicable. |
| Excluded components | Required | Do not add PyQt, terminal-widget libraries, copied terminal-emulator code, copied shader code, copied images, copied icons, copied fonts, copied resource manifests, or copied profile data unless a later explicit decision changes scope. |

## Resolved Findings

*No resolved findings yet.*

## Phase History

| Phase | Sessions | Security | GDPR | Findings Opened | Findings Closed |
|-------|----------|----------|------|-----------------|-----------------|
| 00 | 0 complete / pending phase sessions | WATCH | LIMITED | 6 | 0 |
| 01 | Not started | Not audited | Not audited | 0 | 0 |

## Recommendations

1. Add tests proving SQLite rows and future event payloads exclude API keys, ANSI escapes, Rich markup, and display-only glyphs.
2. Add dependency vulnerability scanning before release verification.
3. Document local history retention and provide a supported purge path.
4. Require explicit operator review of provider, model, target path, and execution flags before non-dry-run autonomous execution.
5. Keep the base CLI free of graphical dependencies and preserve the clean-room boundary for any visual wrapper.

*Updated by documents review. Next security refresh should occur after the first validated Phase 00 session or after any event-stream or wrapper implementation lands.*
