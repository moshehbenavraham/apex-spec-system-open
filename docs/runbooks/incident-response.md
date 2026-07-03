# Incident Response

This runbook covers local development and release incidents. The repository
does not run a hosted service, so incident response is about protecting local
data, release artifacts, and workflow automation.

| Level | Description | Response Time |
|-------|-------------|---------------|
| P0 | Published release or workflow can leak secrets, corrupt project files, or distribute copied reference material | Immediate |
| P1 | CI release or plugin packaging is broken | Same working day |
| P2 | Documentation, local setup, or non-release automation is stale or failing | Next planned maintenance window |

## Common Incidents

### Provider Key Or Secret Exposure

**Symptoms**: A provider key appears in output, docs, history samples, JSONL
events, `.env`, or a committed file.

**Resolution**:

1. Stop any running CLI process.
2. Remove the secret from the file or output path.
3. Rotate the provider key in the provider dashboard.
4. Run `gitleaks detect --source . --verbose` when available.
5. Check docs and the external security-compliance record for stale guidance.

### Dirty Or Generated Plugin Payload

**Symptoms**: CI reports the packaged skill does not mirror root files, or
`bash scripts/sync-plugin-payload.sh --check` fails.

**Resolution**:

1. Edit only canonical root files: `SKILL.md`, `references/`, `scripts/`, and
   `agents/openai.yaml`.
2. Run `bash scripts/sync-plugin-payload.sh`.
3. Run `bash scripts/sync-plugin-payload.sh --check`.
4. Include both canonical and generated payload changes in the same review.

### Release Workflow Fails

**Symptoms**: The tag release workflow fails on encoding, version sync,
inventory, or script executability.

**Resolution**:

1. Verify versions in `README.md`, `SKILL.md`, `AGENTS.md`, and
   `plugins/apex-spec/.codex-plugin/plugin.json`.
2. Run `bash scripts/sync-plugin-payload.sh --check`.
3. Run `bats tests/`.
4. Re-run the tag workflow only after local verification passes.
