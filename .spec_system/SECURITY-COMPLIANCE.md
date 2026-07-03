# Security & Compliance

> Cumulative security posture, privacy, and license-compliance record.
> **Line budget**: 1000 max | **Last updated**: Session 08 release verification (2026-07-03)

---

## Current Security Posture

### Overall: WATCH

The project is a local autonomous CLI workflow runner. Session 08 release
verification improved the posture for machine output, dependency checks,
SQLite/event raw-data boundaries, optional wrapper isolation, and clean-room
evidence. The posture remains WATCH because local history retention, autonomous
execution flags, provider-bound data transfer disclosure, and recurring
dependency governance still need follow-up work.

| Metric | Value |
|--------|-------|
| Open Findings | 4 |
| Critical/High | 0 |
| Medium/Low | 4 |
| Findings Resolved This Refresh | 2 |
| Phases Audited | 1 |
| Last Clean Phase | -- |

## Protected Assets

- Provider API keys and environment-loaded secrets.
- Target project source trees modified by autonomous subprocesses.
- Local workflow history and operator instructions.
- Manager and summarizer prompt contracts.
- Machine-readable lifecycle payloads used by wrappers and automation.
- Clean-room visual implementation and license boundaries.

## Implemented Controls

| Area | Control | Status |
|------|---------|--------|
| Secrets | Provider keys are configured through environment-expanded values and `.env` is ignored by Git. | Partial |
| Database | Local SQLite history uses parameterized queries, WAL mode, and the legacy `cc_response` column for compatibility. | Present |
| Durable data | Session 08 tests and scans verify release smoke rows/events exclude ANSI escapes, Rich markup, frame glyphs, visual tokens, copied reference identifiers, and secret-like values. | Present |
| Event stream | JSONL output has schema validation, guarded stdout machine mode, and tests preventing human-output collision. | Present |
| Subprocess | Agent execution uses an argument list rather than shell invocation and has a 30 minute timeout. | Present |
| Runaway guard | The loop has a default max-iteration limit and dry-run mode. | Present |
| Operator stop | Single interrupt requests a pause; second interrupt exits. | Present |
| Output fallback | Plain, ASCII, compact, `NO_COLOR`, `TERM=dumb`, non-TTY, redirected output, and machine-output paths have smoke evidence. | Present |
| Dependency audit | Session 08 ran `pip-audit` 2.10.1 across base, dev, and wrapper requirements with no known vulnerabilities found. | Present |
| Base install | The terminal CLI runtime does not require graphical dependencies. | Present |
| Clean room | Tracked source/docs scans found no copied reference source, QML, shaders, images, icons, fonts, profiles, resource manifests, build scripts, or terminal-widget material. | Present |

## Open Findings

### Critical / High

*No open critical or high findings.*

### Medium / Low

| ID | Severity | Finding | Required Action |
|----|----------|---------|-----------------|
| F001 | Medium | Local history stores raw agent output, manager decisions, reasons, project paths, timestamps, and operator instructions without redaction or retention limits. | Add retention, purge, and redaction behavior or document the accepted local-data risk explicitly. |
| F002 | Medium | The default agent execution flags grant broad autonomous approval for target-project changes. | Require operator review of target path and execution flags before real runs; consider a safer documented default. |
| F003 | Medium | Recent history, latest agent output, summaries, and operator instructions can be sent to the configured LLM provider. | Document third-party data transfer expectations and warn operators not to include secrets or personal data. |
| F004 | Low | Dependency files use lower-bound version ranges; Session 08 has local audit evidence but no lockfile or recurring CI vulnerability gate for this CLI scope. | Add dependency locking or a scheduled/CI audit workflow. |

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
| Secrets excluded from durable records | Partial | Release smokes and scans passed, but arbitrary raw agent output can still contain secrets. |

## Dependency Security

Runtime dependencies currently include Click, OpenAI Python SDK, python-dotenv,
Rich, PyYAML, and Python standard library modules including SQLite and
subprocess support. Development dependencies include pytest, pytest-cov,
pytest-mock, black, pylint, and pip-audit. Optional wrapper dependencies are in
`requirements-wrapper.txt` and include PySide6 and Nuitka.

Session 08 evidence:

- `pip-audit` 2.10.1 is available in the CLI virtual environment.
- `pip-audit -r requirements.txt -r requirements-dev.txt -r requirements-wrapper.txt` reported no known vulnerabilities.
- The base CLI dependency/import scan found no PySide6, Qt, QML, or Nuitka references in `requirements.txt`, `apex_infinite.py`, `apex_infinite_events.py`, or `apex_infinite_ui.py`.

Recurring dependency audit automation and dependency locking remain open under
F004.

## License Compliance

| Area | Status | Notes |
|------|--------|-------|
| Base CLI dependencies | Acceptable | Runtime dependency set is terminal-only and does not include graphical wrapper dependencies. |
| Visual inspiration boundary | Verified | Session 08 clean-room scans found no copied reference implementation material or assets in tracked source/docs. |
| Optional wrapper source mode | Acceptable | PySide6/QML remains optional in `requirements-wrapper.txt`; source mode is separate from the base CLI. |
| Binary/AppImage distribution | Gated | No binary artifact is published in Session 08. Future binary release must complete generated-bundle review, license/module review, notices, SHA256 checksums, and source/relink instructions for the concrete artifact. |
| Excluded components | Required | Do not add PyQt, terminal-widget libraries, copied terminal-emulator code, copied shader code, copied images, copied icons, copied fonts, copied resource manifests, or copied profile data unless a later explicit decision changes scope. |

## Resolved Findings

| ID | Resolution | Evidence |
|----|------------|----------|
| F005 | Event-stream payloads are implemented and release-verified for guarded stdout, schema validity, and unsafe-token exclusion in smoke outputs. | Session 08 T013 and T015 passed event JSONL and SQLite raw-data checks. |
| F006 | The visual-wrapper clean-room boundary was audited for tracked source/docs and binary publication remains gated. | Session 08 T016 and T020 clean-room scans and release posture records passed. |

## Phase History

| Phase | Sessions | Security | GDPR | Findings Opened | Findings Closed |
|-------|----------|----------|------|-----------------|-----------------|
| 00 | Sessions 01-08 implemented or locally verified; creview complete, validate pending | WATCH | LIMITED | 6 | 2 |
| 01 | Not started | Not audited | Not audited | 0 | 0 |

## Recommendations

1. Add retention, purge, and redaction behavior for local history or explicitly document the accepted local-data risk.
2. Require explicit operator review of provider, model, target path, and execution flags before non-dry-run autonomous execution.
3. Document provider-bound data transfer expectations and warn operators not to place secrets or personal data in prompts or target-project outputs.
4. Add dependency locking or recurring vulnerability scanning in CI.
5. Keep the base CLI free of graphical dependencies and preserve the clean-room boundary for future visual-wrapper artifacts.

*Updated by Session 08 release verification. Next security refresh should occur during creview/validate if a release blocker appears, or when future binary packaging is scoped.*
