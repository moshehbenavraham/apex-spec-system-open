# Incident Response

This runbook covers local development, release, and Apex Infinite CLI operator
incidents. The repository does not run a hosted service, so incident response is
about protecting local data, release artifacts, and workflow automation.

| Level | Description | Response Time |
|-------|-------------|---------------|
| P0 | Published release or workflow can leak secrets, corrupt project files, or distribute copied reference material | Immediate |
| P1 | CI release, plugin packaging, or Apex Infinite CLI real-run behavior is broken | Same working day |
| P2 | Documentation, local setup, wrapper source mode, or non-release automation is stale or failing | Next planned maintenance window |

## Common Incidents

### Provider Key Or Secret Exposure

**Symptoms**: A provider key appears in output, docs, history samples, JSONL
events, `.env`, or a committed file.

**Resolution**:

1. Stop any running CLI process.
2. Remove the secret from the file or output path.
3. Rotate the provider key in the provider dashboard.
4. Run `gitleaks detect --source . --verbose` when available.
5. Check `apex-infinite-cli/.env.example`, docs, transcript samples, and
   `.spec_system/SECURITY-COMPLIANCE.md` for stale guidance.

### Dirty Or Generated Plugin Payload

**Symptoms**: CI reports the packaged skill does not mirror root files, or
`bash scripts/sync-plugin-payload.sh --check` fails.

**Resolution**:

1. Edit only canonical root files: `SKILL.md`, `references/`, `scripts/`, and
   `agents/openai.yaml`.
2. Run `bash scripts/sync-plugin-payload.sh`.
3. Run `bash scripts/sync-plugin-payload.sh --check`.
4. Include both canonical and generated payload changes in the same review.

### Apex Infinite CLI Real Run Needs To Stop

**Symptoms**: The CLI is running against the wrong project, provider, model, or
Codex execution flags.

**Resolution**:

1. Press Ctrl+C once to request an operator pause after the current step.
2. Press Ctrl+C again only when the process must exit immediately.
3. Inspect `apex-infinite-cli/config.yaml` for provider, model, binary, and
   `exec_flags`.
4. Inspect `~/.apex-infinite/history.db` only as local sensitive data.
5. Restart with `--dry-run`, `--path`, `--provider`, `--model`, and
   `--max-iterations` set explicitly.

### Machine Output Contains Human Text

**Symptoms**: JSONL consumers see Rich/plain text mixed with event objects.

**Resolution**:

1. Use `--event-stream - --machine-output` when stdout must be JSONL only.
2. Use `--event-stream PATH` when human output should remain on stdout.
3. Keep wrapper and automation code on the event stream or importable event API,
   not on Rich frames, plain human output, or SQLite history display rows.

### Optional Visual Wrapper Fails To Launch

**Symptoms**: The wrapper reports missing PySide6, display backend errors,
malformed events, subprocess failure, or timeout state.

**Resolution**:

1. Install optional dependencies with `pip install -r requirements-wrapper.txt`.
2. Run the headless smoke check:

   ```bash
   QT_QPA_PLATFORM=offscreen python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 900
   ```

3. Run the equivalent base CLI command directly with `--event-stream -` and
   `--machine-output`.
4. Follow [Troubleshooting](../apex-infinite-cli/troubleshooting.md) for the
   exact wrapper failure label.

### Release Workflow Fails

**Symptoms**: The tag release workflow fails on encoding, version sync,
inventory, script executability, or CLI health.

**Resolution**:

1. Verify versions in `README.md`, `SKILL.md`, `AGENTS.md`, and
   `plugins/apex-spec/.codex-plugin/plugin.json`.
2. Run `bash scripts/sync-plugin-payload.sh --check`.
3. Run `bats tests/`.
4. Run `python apex-infinite-cli/apex_infinite.py --help` after installing
   `apex-infinite-cli/requirements.txt`.
5. Re-run the tag workflow only after local verification passes.
