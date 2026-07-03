# Security & Compliance

> Cumulative security posture and GDPR compliance record. Updated between phases via carryforward.
> **Line budget**: 1000 max | **Last updated**: Phase 00 (2026-07-03)

---

## Current Security Posture

### Overall: AT RISK

Phase 00 release verification passed for source-mode release of the base CLI
and optional Linux visual wrapper. The posture remains AT RISK because local
history retention, autonomous execution controls, provider-bound data transfer
disclosure, and recurring dependency governance still need follow-up work.

| Metric | Value |
|--------|-------|
| Open Findings | 4 |
| Critical/High | 0 |
| Medium/Low | 4 |
| Phases Audited | 1 |
| Last Clean Phase | -- |

---

## Open Findings

Active security or GDPR issues requiring attention. Ordered by severity.

### Critical / High

No open critical or high findings.

### Medium / Low

- **[P00-S01] Local history has no retention or redaction controls**
  - Severity: Medium
  - File: `apex-infinite-cli/src/apex_infinite/cli.py`
  - Description: Local SQLite history stores raw agent output, manager decisions, reasons, project paths, timestamps, and operator instructions without purge, retention, or redaction behavior.
  - Remediation: Add a purge/retention path and redaction behavior, or document the accepted local-data risk explicitly before broader release.
  - Status: Open
  - Opened: P00 (2026-07-03)

- **[P00-S02] Autonomous execution flags need an explicit operator safety gate**
  - Severity: Medium
  - File: `apex-infinite-cli/src/apex_infinite/config.yaml`
  - Description: Default real-run configuration can grant broad autonomous approval for target-project changes.
  - Remediation: Require review of target path, provider, model, and execution flags before non-dry-run loops, or ship a safer documented default.
  - Status: Open
  - Opened: P00 (2026-07-03)

- **[P00-S03] Provider-bound data transfer disclosure is incomplete**
  - Severity: Medium
  - File: `apex-infinite-cli/README.md`
  - Description: Recent history, latest agent output, summaries, and operator instructions can be sent to the configured LLM provider.
  - Remediation: Document provider-bound prompt traffic and warn operators not to include secrets or personal data in prompts or target-project outputs.
  - Status: Open
  - Opened: P00 (2026-07-03)

- **[P00-S04] Dependency audit is local-only**
  - Severity: Low
  - File: `apex-infinite-cli/pyproject.toml`
  - Description: Session 08 passed local `pip-audit`, but package dependencies use lower-bound ranges and there is no lockfile or recurring CI/scheduled vulnerability gate for this CLI scope.
  - Remediation: Add dependency locking or scheduled/CI vulnerability scanning for base, dev, and visual extra dependencies.
  - Status: Open
  - Opened: P00 (2026-07-03)

---

## GDPR Compliance Status

### Overall: NON-COMPLIANT / LOCAL TOOL

The project is not an end-user data service, but it can process operator text,
target-project paths, agent responses, and provider-bound prompts. Treat local
history and provider requests as potentially sensitive operational data. Until
first-run notice, purge/redaction, and provider-transfer documentation are
implemented, the local-tool privacy posture is non-compliant.

### Personal Data Inventory

| Data Element | Source | Storage | Purpose | Legal Basis | Retention | Deletion Path | Since |
|--------------|--------|---------|---------|-------------|-----------|---------------|-------|
| Project path | CLI `--path` and current project | Local SQLite history | Scope workflow history and resume context | Operator-initiated local processing | Indefinite | Manual DB deletion only | P00 |
| Operator instructions | CLI input and CEO/start options | Local SQLite history and LLM prompts | Guide workflow decisions | Operator-initiated local processing | Indefinite locally; provider policy externally | Manual DB deletion only | P00 |
| Agent responses | Codex subprocess output | Local SQLite history and LLM prompts | Resume and route workflow state | Operator-initiated local processing | Indefinite locally; provider policy externally | Manual DB deletion only | P00 |
| Manager decisions and reasons | Manager LLM response | Local SQLite history | Audit and resume workflow state | Operator-initiated local processing | Indefinite | Manual DB deletion only | P00 |
| Provider API keys | Environment or `.env` | Process environment; provider client | Authenticate provider calls | Operator configuration | Until operator rotates/removes | Remove env or `.env` entry | P00 |
| Desktop notification text | CLI runtime state | Local OS notification surface | Alert operator on pause or completion | Operator-initiated local processing | OS dependent | OS notification cleanup | P00 |

### Compliance Checklist

| Requirement | Status | Notes |
|-------------|--------|-------|
| Data collection has documented purpose | PASS | History exists to resume and summarize workflow state. |
| Consent obtained before data storage | FAIL | Operator starts the CLI, but there is no explicit first-run privacy notice. |
| Data minimization verified | FAIL | Recent rows are summarized, but raw history is retained indefinitely. |
| Deletion/erasure path exists | FAIL | Manual database deletion works; no CLI purge command exists. |
| No PII in application logs | FAIL | No intentional PII collection, but raw prompts and outputs are not scrubbed. |
| Third-party transfers documented | FAIL | Provider-bound prompt traffic is known; provider-specific legal posture is not recorded. |

---

## Dependency Security

### Current Vulnerabilities

No known vulnerable dependencies from the Phase 00 local audit.

| Package | Version | Severity | CVE | Status |
|---------|---------|----------|-----|--------|
| - | - | - | - | No known vulnerabilities from local `pip-audit` evidence on 2026-07-03. |

Notes:

- Base runtime dependencies remain terminal-only: Click, OpenAI Python SDK, python-dotenv, Rich, PyYAML, and Python standard library SQLite/subprocess modules.
- Development dependencies include pytest, pytest-cov, pytest-mock, black, pylint, and pip-audit.
- Optional wrapper dependencies remain isolated in the `visual` extra and include PySide6 and Nuitka.
- Recurring dependency audit automation and dependency locking remain open under [P00-S04].

---

## License Compliance

| Area | Status | Notes |
|------|--------|-------|
| Base CLI dependencies | PASS | Runtime dependency set is terminal-only and does not include graphical wrapper dependencies. |
| Visual inspiration boundary | PASS | Phase 00 scans found no tracked reference implementation material or assets in source/docs. |
| Optional wrapper source mode | PASS | PySide6/QML remains optional in the `visual` extra; source mode is separate from the base CLI. |
| Binary/AppImage distribution | GATED | No binary artifact is published. Future binary release must complete generated-bundle review, license/module review, notices, SHA256 checksums, and source/relink instructions. |
| Excluded components | REQUIRED | Do not add PyQt, terminal-widget libraries, copied terminal-emulator code, copied shader code, copied images, copied icons, copied fonts, copied resource manifests, or copied profile data unless scope changes explicitly. |

---

## Resolved Findings

Recently closed items. Compressed after 2 phases.

| ID | Finding | Severity | Resolved | Phase | Resolution |
|----|---------|----------|----------|-------|------------|
| P00-S05 | Event-stream payload safety and stdout isolation | Medium | 2026-07-03 | P00 | Guarded `--event-stream -` with `--machine-output`; release smokes verified JSONL schema and unsafe-token exclusion. |
| P00-S06 | Visual-wrapper clean-room uncertainty | Medium | 2026-07-03 | P00 | Clean-room scans found no copied reference source/assets; binary publication remains gated for artifact-specific review. |

---

## Phase History

| Phase | Sessions | Security | GDPR | Findings Opened | Findings Closed |
|-------|----------|----------|------|-----------------|-----------------|
| P00 | 8 | AT RISK | NON-COMPLIANT / LOCAL TOOL | 6 | 2 |

---

## Recommendations

1. Add retention, purge, and redaction behavior for local history or explicitly document the accepted local-data risk.
2. Require explicit operator review of provider, model, target path, and execution flags before non-dry-run autonomous execution.
3. Document provider-bound data transfer expectations and warn operators not to place secrets or personal data in prompts or target-project outputs.
4. Add dependency locking or recurring vulnerability scanning in CI.
5. Keep the base CLI free of graphical dependencies and preserve the clean-room boundary for future visual-wrapper artifacts.

---

*Auto-generated by carryforward. Direct edits allowed but may be overwritten.*
