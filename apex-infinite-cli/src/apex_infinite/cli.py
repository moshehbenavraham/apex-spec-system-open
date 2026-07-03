#!/usr/bin/env python3
# pylint: disable=too-many-lines
"""Apex Spec System Infinite CLI - Autonomous Codex CLI session manager.

Drives the Apex Spec System workflow via Codex CLI subprocess calls,
with SQLite history, LLM-based manager decisions, and terminal output.
"""

import json
import os
import re
import signal
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import click
import yaml
from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from apex_infinite.events import (
    EventStreamError,
    NoOpEventEmitter,
    open_event_stream,
    summarize_text,
)
from apex_infinite.ui import (
    ApexRenderer,
    CodexCommandSnapshot,
    DbLogSnapshot,
    IterationSnapshot,
    NoHumanOutputRenderer,
    StartupSnapshot,
    UiCliOverrides,
    UiConfigError,
    resolve_ui_settings,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DB_DIR = Path.home() / ".apex-infinite"
DB_PATH = DB_DIR / "history.db"

KNOWN_COMMANDS = {
    "initspec",
    "createprd",
    "createuxprd",
    "plansession",
    "implement",
    "creview",
    "validate",
    "updateprd",
    "audit",
    "pipeline",
    "infra",
    "carryforward",
    "documents",
    "phasebuild",
}

# Codex skill commands use canonical names; no aliases needed currently
COMMAND_ALIASES: dict[str, str] = {}

COMMAND_TIMEOUT = 1800  # 30 minutes
PROCESS_CLEANUP_TIMEOUT = 5
DEFAULT_MAX_ITERATIONS = 50
LLM_RETRY_COUNT = 3
LLM_RETRY_WAIT = 5  # seconds (matches n8n waitBetweenTries: 5000)
PROVIDER_PREFLIGHT_TIMEOUT = 10

console = Console()
_ACTIVE_RENDERER = None
_ACTIVE_EVENT_EMITTER = None
_MACHINE_OUTPUT_ACTIVE = False


class CliStartupError(RuntimeError):
    """Raised for startup failures that need CLI-aware reporting."""


@dataclass(frozen=True)
class ProviderPreflightResult:
    """Facts returned by a successful provider preflight."""

    provider_name: str
    base_url: str
    model_name: str
    model_count: int
    completion_checked: bool


def _emit_event(
    event_emitter,
    name,
    payload=None,
    renderer=None,
    machine_output=False,
):
    """Emit an event without letting event failures alter workflow state."""
    if not event_emitter or not getattr(event_emitter, "enabled", False):
        return
    try:
        event_emitter.emit(name, payload or {})
    except EventStreamError as exc:
        if name != "event_stream_error" and machine_output:
            try:
                event_emitter.emit(
                    "event_stream_error",
                    {
                        "source_event": name,
                        "error_type": exc.__class__.__name__,
                        "message": str(exc),
                    },
                )
            except EventStreamError:
                return
        if renderer and not machine_output:
            renderer.print_error(f"Event stream error: {exc}", "Event Stream")
        elif not machine_output:
            console.print(f"[red]Event stream error: {exc}[/red]")


def _exit_with_startup_error(
    message,
    event_emitter=None,
    machine_output=False,
    renderer=None,
    title="Startup",
):
    """Report a startup failure without contaminating machine-output stdout."""
    _emit_event(
        event_emitter,
        "error",
        {"stage": title.lower().replace(" ", "_"), "message": message},
        renderer=renderer,
        machine_output=machine_output,
    )
    if not machine_output:
        if renderer:
            renderer.print_error(message, title)
        else:
            console.print(f"[red]{message}[/red]")
    sys.exit(1)


@dataclass(frozen=True)
class CodexProcessResult:
    """Raw facts returned by a Codex subprocess run."""

    stdout: str
    stderr: str
    returncode: int


def run_codex_process(cmd: list[str], cwd: str, timeout: int) -> CodexProcessResult:
    """Run Codex and return raw captured process facts."""
    process = subprocess.Popen(  # pylint: disable=consider-using-with
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=PROCESS_CLEANUP_TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
        raise subprocess.TimeoutExpired(
            cmd=cmd,
            timeout=timeout,
            output=stdout,
            stderr=stderr,
        ) from exc
    except Exception:
        if process.poll() is None:
            process.kill()
            process.communicate()
        raise
    return CodexProcessResult(
        stdout=stdout or "",
        stderr=stderr or "",
        returncode=process.returncode,
    )


# ---------------------------------------------------------------------------
# System Prompts (verbatim from n8n JSON)
# ---------------------------------------------------------------------------

MANAGER_SYSTEM_PROMPT = r"""# Role

You are a **managing software engineer** -- the kind that obsesses over perfect project structure. You approach implementation like a craftsperson: methodical, patient, and uncompromising on quality. You specifically manage an AI Coding Agent called 'Codex CLI' which acts as your Senior Developer.

# Input

Both:
- A summary of previous historical messages from Codex CLI and your responses.
OR
  -- The last message from Codex CLI, your Senior Developer.
  -- Instructions from the CEO

# Your Senior Developer Codex CLI

## Codex CLI Commands

Codex CLI is pre-armed with Apex Spec staged workflow commands. This manager is used after a project has already been initialized, so the command reference below intentionally covers the post-initialization staged loop only. Do not choose initialization commands as normal manager output.

Codex CLI ends every command with a `Next command:` handoff. Treat that line as the primary routing signal unless it conflicts with a concrete failure in the same message. If Codex CLI mentions a problem that it did not create or calls something a "pre-existing issue", that issue is still part of the project quality bar and must be addressed.

## Issues

If Codex CLI reports any issues, first read its `Next command:` and `Reason:` lines. If the next command is a known workflow command, output that command. If the next command is the same command because fixes are required, output that command or concise high-level instructions that tell Codex CLI to fix the issue and then rerun the command. Codex CLI is -extremely- intelligent and does not need code snippets or examples, so keep instructions concise and high level.

Codex CLI has shell access and can handle most anything outside of SUDO commands, secrets, billing, or external platform access, such as running snapshot updates, unit tests, installing/running pnpm, and GitHub operations where gh access exists.

If validation fails because the code review report is missing, blocked, or unresolved, route back to creview. If validation fails because implementation is incomplete or buggy, instruct Codex CLI to fix the issue and rerun the command indicated by its handoff.

### Issues - Special Cases

If Codex CLI reports the pipeline command ran into billing issues, move on to infra instead of bugging the CEO.

## CEO

If the CEO sends instructions, your job is simply to relay the instructions to Codex CLI.

### Try Not to Bug CEO

This is an autonomous system. Do not bug the User, who effectively you can consider the CEO, for workflow decisions, confirmations, reviews, package selection, missing context, test failures, dependency installs, GitHub operations where gh access exists, or anything Codex CLI can resolve. Normal command output should be another known command, `alldonebaby`, or concise high-level instructions for Codex CLI. The CLI still supports `help` as an emergency operator pause, but it is not part of the Apex workflow and should not be used for ordinary command blockers.

## All Done Baby!

If Codex CLI has completed all sessions and phases and the final phase transition has completed through audit, pipeline, infra, carryforward, and documents, output "alldonebaby".

# Output

Your output MUST be clean valid JSON. The `output` value MUST be one of:
- a single post-initialization staged workflow command from the command reference below
- CEO instructions as simple text
- high-level instructions to Codex CLI as simple text
- `alldonebaby` if everything has been fully completed
- `help` only for an unrecoverable external blocker that Codex CLI truly cannot solve

Use the command's `Next command:` line whenever present. Include a concise reason for your output.

Examples of valid outputs:

{ "output": "plansession", "reason": "Codex CLI reported the phase still has unfinished sessions and handed off to plansession." }
OR
{ "output": "run phasebuild", "reason": "The CEO sent instructions and my job is to relay them straight to Codex CLI our Senior Developer." }
OR
{ "output": "Fix the two bugs, then rerun validate.", "reason": "Codex CLI reported validation failed on two repo-fixable issues." }
OR
{ "output": "carryforward", "reason": "Codex CLI completed infra and handed off to carryforward." }

# Senior Developer's Commands

---
---

  Codex CLI Senior Developer - Command Reference

  Apex Spec has 14 staged workflow commands total. This manager controls only the 11 post-initialization staged commands below because projects entering this loop are already initialized.

  Important rules:
  - When all sessions of a phase are completed, start phase transition with audit.
  - After implement succeeds, the next command is creview.
  - After creview succeeds and its report is resolved, the next command is validate.
  - Phase transition order is audit -> pipeline -> infra -> carryforward -> documents -> phasebuild if another phase remains.

  The post-initialization workflow has 2 stages that loop: Sessions (a collection of sessions completes a phase) -> Phase Transition (prepare for a new set of sessions if any phases remain).

```
Stage 1: SESSIONS WORKFLOW (Repeat until phase complete)

---

plansession

Purpose: Plan, spec, and task-generate for the next session in one shot

Steps:
1. Run analyze-project.sh --json for state (phase, completed sessions, candidates)
2. Read PRD.md, candidate sessions, CONSIDERATIONS.md (Active Concerns, Lessons Learned), CONVENTIONS.md
3. Evaluate candidates by: prerequisites, dependencies, logical flow, MVP focus
4. Create NEXT_SESSION.md: recommendation, rationale, deliverables, alternatives
5. Create .spec_system/specs/phaseNN-sessionNN-name/
6. Generate spec.md (10 sections): Overview, Objectives, Prerequisites, Scope, Technical Approach, Deliverables, Success Criteria, Implementation Notes, Testing Strategy, Dependencies
7. Archive NEXT_SESSION.md to session directory
8. Generate tasks.md:
   - Progress table (Setup/Foundation/Implementation/Testing)
   - Tasks: - [ ] TNNN [SPPSS] [P] Action + what + where (path)
   - [P] marks parallelizable tasks
   - Completion checklist
9. Update state.json: set current_session, append next_session_history, status -> tasks_created
Rules:
- If phase complete, use audit instead. Trust script JSON as ground truth.
- Max 25 tasks, max 4 hours, single objective (reject if exceeded)
- Task sweet spot: 20 tasks, ~20-25 min each

Categories: Setup (2-4), Foundation (4-8), Implementation (8-15), Testing (3-5)

Next: implement

---

implement

Purpose: AI-led task-by-task implementation

Steps:
1. Run analyze-project.sh --json for current session
2. Run check-prereqs.sh --json --env (STOP if fails); optionally --tools "tool1,tool2"
3. Read AGENTS.md if present, spec.md, tasks.md, CONVENTIONS.md
4. Create/update implementation-notes.md
5. Per task:
   - Implement per AGENTS.md + CONVENTIONS.md
   - Mark - [ ] -> - [x] in tasks.md
   - Log: timestamps, notes, files changed
6. Document blockers and decisions
7. Checkpoint every 3-5 tasks

Rules: ASCII-only, LF endings, follow conventions, implement spec exactly (no extras)

Next: creview

---
creview

Purpose: Review and repair all uncommitted changes before validation

Steps:
1. Run analyze-project.sh --json for current session context
2. Inventory all uncommitted changes with git status, git diff HEAD, git diff --cached, and git ls-files --others --exclude-standard
3. Read spec.md, tasks.md, implementation-notes.md, CONVENTIONS.md, and CONSIDERATIONS.md
4. Review every changed hunk for correctness, spec adherence, security, error handling, edge cases, data integrity, tests, dead code, consistency, and performance
5. Write code-review.md with findings grouped by severity, assumptions, behavior changes, and verification evidence
6. Fix every repo-fixable finding with minimal edits and add or update tests for every bug fixed
7. Run applicable tests, linter, formatter, type checker, and re-read the final diff

Rules: Review ALL uncommitted changes, no human decision gate, no QUESTION outcome, record evidence-backed assumptions and continue

Next: validate

---
validate

Purpose: Verify session completeness and quality gates

Steps:
1. Run analyze-project.sh --json for current session
2. Read spec.md, tasks.md, implementation-notes.md, code-review.md, CONVENTIONS.md
3. Run 7 checks:
   - 0. Code review gate (code-review.md Result: RESOLVED)
   - A. Task completion (100% [x])
   - B. Deliverables exist (non-empty)
   - C. ASCII encoding (no non-ASCII, no CRLF)
   - D. Tests passing
   - E. Success criteria met
   - F. Conventions compliance
4. Generate validation.md: PASS/FAIL per check
5. Update state.json status -> validated or validation_failed

PASS: All checks pass. FAIL: Any issue -> resolve -> re-run validate

Next: updateprd (if PASS)

---
updateprd

Purpose: Mark session complete, update docs, commit

Steps:
1. Verify validation.md shows PASS
2. Update state.json: add to completed_sessions[], clear current_session, mark history completed
3. Update phase PRD: mark session Complete
4. Create IMPLEMENTATION_SUMMARY.md: overview, deliverables, decisions, tests, lessons, future, stats
5. If last session: archive phase to archive/phases/, update master PRD
6. Increment version (patch) in package.json/pyproject.toml/Cargo.toml/etc.
7. Commit and push (no co-authors)

Commit format: Complete phaseNN-sessionNN-name: [description] + deliverables

Next: plansession (if phase incomplete) or audit (if phase complete)

---
Stage 2: PHASE TRANSITION

---
audit

Purpose: Add/validate local dev tooling, one bundle at a time

Steps:
1. DETECT: Read CONVENTIONS.md, known-issues.md, check git status
2. COMPARE: Check 5 bundles against master list
3. SELECT: Pick highest-priority missing bundle
4. IMPLEMENT: Install tool + generate config
5. VALIDATE: Run ALL tools (formatter -> linter -> types -> tests -> hooks)
6. FIX: Auto-fix; revert if syntax breaks after 2 retries
7. RECORD: Update CONVENTIONS.md Local Dev Tools table
8. REPORT: Summary of additions, fixes, remaining issues
9. RECOMMEND: Rerun audit or proceed to pipeline

Bundles (priority): Formatting -> Linting -> Type Safety -> Testing -> Git Hooks

Flags: --dry-run, --skip-install, --verbose

Rules: One bundle per run. Never break syntax (revert after 2 failures).

When: After phase complete, before pipeline

---
pipeline

Purpose: Add/validate CI/CD workflows, one bundle at a time

Steps:
1. DETECT: Read CONVENTIONS.md, detect CI platform, check PRs with issues
2. COMPARE: Check 5 bundles against master list
3. SELECT: Pick highest-priority missing bundle
4. IMPLEMENT: Generate workflow YAML, commit, push
5. VALIDATE: Poll CI (3 min timeout), check PR status
6. FIX: Parse CI logs, fix errors, address PR review comments
7. RECORD: Update CONVENTIONS.md CI/CD table
8. REPORT: Summary of workflows, fixes, CI/PR status
9. RECOMMEND: Fix issues, merge PR, or proceed to infra

Bundles (priority): Code Quality -> Build & Test -> Security -> Integration -> Operations

Flags: --dry-run, --skip-install, --verbose, --pr <number>

Rules: One bundle per run. PR-aware: fixes CI failures AND review comments. Documents secrets (never creates them).

When: After audit, before infra

---
infra

Purpose: Add/validate production infrastructure, one bundle at a time

Steps:
1. DETECT: Read CONVENTIONS.md Infrastructure table, detect platform (Cloudflare/Coolify/Vercel/Fly.io/etc.)
2. COMPARE: Check 4 bundles against master list
3. SELECT: Pick highest-priority missing bundle
4. IMPLEMENT: Add platform-specific config/code
5. VALIDATE: Verify (curl /health, test rate limiting, check backups, trigger deploy)
6. FIX: Address validation failures
7. RECORD: Update CONVENTIONS.md Infrastructure table
8. REPORT: Summary of infra, validation results, manual steps
9. RECOMMEND: Fix issues or proceed to carryforward

Bundles (priority): Health -> Security -> Backup -> Deploy

Flags: --dry-run, --skip-install, --verbose

Rules: One bundle per run. Stack-agnostic. Documents manual steps/env vars (never creates secrets).

When: After pipeline, before carryforward

---
carryforward

Purpose: Extract lessons learned, update CONSIDERATIONS.md between phases

Steps:
1. Verify phase complete in state.json
2. Read all IMPLEMENTATION_SUMMARY.md from completed phase
3. Extract:
   - Active Concerns: Tech debt, external deps, performance/security, architecture
   - Lessons Learned: What worked, what to avoid, tool notes
   - Resolved: Previous concerns addressed
4. Update .spec_system/CONSIDERATIONS.md: add new, remove resolved, merge similar
   - Limits: 20 Active Concerns, 30 Lessons Learned, 15 Resolved
5. Enforce 600-line limit (trim oldest/least relevant)

Format: Tag items with [P##] for traceability

When: After infra, before documents. Recommended for all phases.

---
documents

Purpose: Create/maintain project documentation

Steps:
1. Run analyze-project.sh --json
2. Determine scope:
   - Phase-Focused: Prioritize changes from just-completed phase
   - Full Audit: Initial setup, milestones, or explicit request
3. Audit standard files:
   - Root: README.md, LICENSE
   - docs/: CONTRIBUTING.md, ARCHITECTURE.md, CODEOWNERS, onboarding.md, development.md, environments.md, deployment.md, adr/, runbooks/, api/
   - Per-package: README_<dirname>.md (not README.md)
4. Create missing files from templates (.spec_system/doc-templates/ first)
5. Update existing docs to current state
6. Generate docs-audit.md report

Naming: Only root gets README.md; subdirs use README_<dirname>.md

Principle: Current over complete -- small accurate doc beats comprehensive stale one

When: After carryforward, before phasebuild if another phase remains. If no phases remain, the project is complete.

---
phasebuild

Purpose: Create structure for new phase with session stubs (last transition step)

Steps:
1. Read state.json and PRD for next phase number
2. Read CONSIDERATIONS.md for lessons to apply
3. Create PRD/phase_NN/ directory
4. Create PRD_phase_NN.md (phase tracker with progress table)
5. Create session stubs (session_NN_name.md): objectives, scope, deliverables
6. Update state.json with new phase
7. Update master PRD.md phases table

Stub format: Objective, scope (in/out), prerequisites, deliverables, success criteria

Guidelines: 4-8 sessions typical, 12-25 tasks each, 2-4 hours each

Next: plansession

---
Quick Reference

| Command       | Stage      | Input                  | Output                              |
|---------------|------------|------------------------|-------------------------------------|
| plansession   | Sessions   | State, PRD, candidates | NEXT_SESSION.md spec.md tasks.md    |
| implement     | Sessions   | spec.md, tasks.md      | Code + implementation-notes.md      |
| creview       | Sessions   | Uncommitted changes    | code-review.md                      |
| validate      | Sessions   | All session files      | validation.md                       |
| updateprd     | Sessions   | validation.md          | Summary, commit, push, version bump |
| audit         | Transition | Codebase               | Local dev tooling, report           |
| pipeline      | Transition | Codebase               | CI/CD workflows, report             |
| infra         | Transition | Codebase               | Infrastructure, report              |
| carryforward  | Transition | Phase artifacts        | Updated CONSIDERATIONS.md           |
| documents     | Transition | State, PRD, codebase   | Updated docs                        |
| phasebuild    | Transition | PRD, state             | Phase dir + session stubs           |
```

---
---
"""

SUMMARIZER_SYSTEM_PROMPT = """# Role

You are a **master AI coding agent response/decision summarizer** -- the kind that obsesses over perfection.  You approach summarizing like a craftsperson: methodical, patient, and uncompromising on quality.

# Input

Between 0 to 15 aggregated records in newest to oldest of responses between a Senior Developer (Codex CLI) and their Manager.

# Output

A concise summary that does not leave out important details in plain text.  Maximum 2000 characters.  No preamble. No conclusion. No meta-commentary. Output only the summary.
"""

# ---------------------------------------------------------------------------
# Signal handling
# ---------------------------------------------------------------------------

_INTERRUPTED = False


def _handle_sigint(_sig, _frame):
    global _INTERRUPTED  # pylint: disable=global-statement
    if _INTERRUPTED:
        _emit_event(
            _ACTIVE_EVENT_EMITTER,
            "operator_interrupt_quit",
            {"state": "force-quit"},
            renderer=_ACTIVE_RENDERER,
            machine_output=_MACHINE_OUTPUT_ACTIVE,
        )
        if _ACTIVE_RENDERER:
            _ACTIVE_RENDERER.print_interrupt("force-quit", "Force quit.")
        else:
            console.print("\n[bold red]Force quit.[/bold red]")
        sys.exit(1)
    _INTERRUPTED = True
    _emit_event(
        _ACTIVE_EVENT_EMITTER,
        "operator_interrupt_requested",
        {"state": "requested"},
        renderer=_ACTIVE_RENDERER,
        machine_output=_MACHINE_OUTPUT_ACTIVE,
    )
    if _ACTIVE_RENDERER:
        _ACTIVE_RENDERER.print_interrupt("requested", "Will pause after current step.")
    else:
        console.print(
            "\n[bold yellow][CEO INTERRUPT] Will pause after current step...[/bold yellow]"
        )


signal.signal(signal.SIGINT, _handle_sigint)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def load_config(config_path, provider_override=None, model_override=None):
    """Load YAML config, apply overrides, expand provider env vars."""
    path = Path(config_path)
    if not path.exists():
        raise CliStartupError(f"Config file not found: {config_path}")

    with open(path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if provider_override:
        config["provider"] = provider_override

    provider_name = config["provider"]
    if provider_name not in config["providers"]:
        raise CliStartupError(f"Unknown provider: {provider_name}")

    # Load .env from cwd first; config-local values take precedence.
    load_dotenv(Path.cwd() / ".env")
    load_dotenv(path.parent / ".env", override=True)

    # Expand env vars in provider string fields.
    provider_cfg = config["providers"][provider_name]
    env_defaults = _provider_env_defaults(provider_name)
    for key, value in list(provider_cfg.items()):
        if isinstance(value, str):
            provider_cfg[key] = _expand_config_env(value, env_defaults)

    if model_override:
        provider_cfg["model"] = model_override

    return config


def resolve_default_config_path():
    """Find the default config for source-tree and installed package runs."""
    source_root = Path(__file__).resolve().parents[2]
    candidates = [
        Path.cwd() / "config.yaml",
        Path(__file__).resolve().parent / "config.yaml",
    ]
    if (source_root / "pyproject.toml").exists():
        candidates.insert(1, source_root / "config.yaml")
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


def _provider_env_defaults(provider_name):
    """Return provider-specific defaults for optional env-backed config."""
    if provider_name != "ollama":
        return {}
    return {
        "OLLAMA_HOST": "localhost",
        "OLLAMA_PORT": "11434",
        "OLLAMA_API_KEY": "ollama",
        "OLLAMA_MODEL": "qwen2.5:7b",
    }


def _expand_config_env(value, defaults):
    """Expand $VAR and ${VAR}, using defaults only for known optional vars."""

    def replace(match):
        name = match.group(1) or match.group(2)
        if name in os.environ:
            return os.environ[name]
        if name in defaults:
            return defaults[name]
        return match.group(0)

    return re.sub(r"\$(\w+)|\$\{([^}]+)\}", replace, value)


def get_llm_client(config):
    """Create OpenAI client from active provider config. Returns (client, model)."""
    provider = config["providers"][config["provider"]]
    return (
        OpenAI(base_url=provider["base_url"], api_key=provider["api_key"]),
        provider["model"],
    )


def run_provider_preflight(config, check_completion=False):
    """Verify the active OpenAI-compatible provider and configured model."""
    provider_name = config["provider"]
    provider = config["providers"][provider_name]
    base_url = _required_provider_string(provider, "base_url", provider_name)
    api_key = _required_provider_string(provider, "api_key", provider_name)
    model_name = _required_provider_string(provider, "model", provider_name)
    timeout_seconds = _provider_preflight_timeout()

    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=timeout_seconds,
    )
    try:
        model_ids = _list_provider_model_ids(client)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        raise CliStartupError(
            "Provider preflight failed for "
            f"{provider_name} at {base_url}: could not list models "
            f"({exc.__class__.__name__}: {exc})"
        ) from exc

    if not model_ids:
        raise CliStartupError(
            f"Provider preflight failed for {provider_name} at {base_url}: "
            "the provider returned no models."
        )

    if not _model_is_available(model_name, model_ids):
        raise CliStartupError(
            f"Provider preflight failed for {provider_name} at {base_url}: "
            f"configured model '{model_name}' is not available. "
            f"Available models: {_format_model_sample(model_ids)}"
        )

    if check_completion:
        _check_provider_chat_completion(client, provider_name, base_url, model_name)

    return ProviderPreflightResult(
        provider_name=provider_name,
        base_url=base_url,
        model_name=model_name,
        model_count=len(model_ids),
        completion_checked=check_completion,
    )


def _required_provider_string(provider, key, provider_name):
    """Read a provider string field and reject blank or unresolved values."""
    value = provider.get(key)
    if not isinstance(value, str) or not value.strip():
        raise CliStartupError(
            f"Provider '{provider_name}' is missing required string field '{key}'."
        )
    if "$" in value:
        raise CliStartupError(
            f"Provider '{provider_name}' field '{key}' still contains an "
            "unresolved env placeholder."
        )
    return value.strip()


def _provider_preflight_timeout():
    """Read optional provider preflight timeout from the environment."""
    raw_timeout = os.environ.get(
        "APEX_INFINITE_PROVIDER_CHECK_TIMEOUT",
        str(PROVIDER_PREFLIGHT_TIMEOUT),
    )
    try:
        timeout_seconds = float(raw_timeout)
    except ValueError as exc:
        raise CliStartupError(
            "APEX_INFINITE_PROVIDER_CHECK_TIMEOUT must be a positive number."
        ) from exc
    if timeout_seconds <= 0:
        raise CliStartupError(
            "APEX_INFINITE_PROVIDER_CHECK_TIMEOUT must be a positive number."
        )
    return timeout_seconds


def _list_provider_model_ids(client):
    """Return sorted model ids from an OpenAI-compatible models response."""
    response = client.models.list()
    raw_models = getattr(response, "data", None)
    if raw_models is None:
        raw_models = response

    model_ids = []
    for model in raw_models:
        model_id = getattr(model, "id", None)
        if model_id is None and isinstance(model, dict):
            model_id = model.get("id")
        if model_id:
            model_ids.append(str(model_id))
    return tuple(sorted(set(model_ids)))


def _model_is_available(model_name, model_ids):
    """Accept exact model ids and Ollama-style implicit latest tags."""
    if model_name in model_ids:
        return True
    if ":" not in model_name and f"{model_name}:latest" in model_ids:
        return True
    return False


def _format_model_sample(model_ids, limit=8):
    """Format a short, deterministic model list for startup errors."""
    sample = list(model_ids[:limit])
    if len(model_ids) > limit:
        sample.append(f"... {len(model_ids) - limit} more")
    return ", ".join(sample)


def _check_provider_chat_completion(client, provider_name, base_url, model_name):
    """Run a tiny completion against the configured model."""
    try:
        client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Reply with ok."}],
            max_tokens=8,
            temperature=0,
        )
    except Exception as exc:  # pylint: disable=broad-exception-caught
        raise CliStartupError(
            "Provider preflight failed for "
            f"{provider_name} at {base_url}: tiny chat completion failed "
            f"({exc.__class__.__name__}: {exc})"
        ) from exc


def _run_provider_preflight_or_exit(
    config,
    check_completion=False,
    renderer=None,
    event_emitter=None,
    machine_output=False,
):
    """Run provider preflight and report errors through CLI startup handling."""
    provider_name = config["provider"]
    provider = config["providers"][provider_name]
    model_name = provider.get("model", "")
    base_url = provider.get("base_url", "")
    _emit_event(
        event_emitter,
        "provider_check_started",
        {
            "provider_name": provider_name,
            "model_name": model_name,
            "base_url": base_url,
            "completion_check": check_completion,
        },
        renderer=renderer,
        machine_output=machine_output,
    )
    if renderer:
        renderer.print_status(
            f"Checking {provider_name} provider at {base_url} for model {model_name}.",
            "Provider Preflight",
        )
    try:
        result = run_provider_preflight(config, check_completion=check_completion)
    except CliStartupError as exc:
        _emit_event(
            event_emitter,
            "provider_check_failed",
            {
                "provider_name": provider_name,
                "model_name": model_name,
                "base_url": base_url,
                "message": str(exc),
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        _exit_with_startup_error(
            str(exc),
            event_emitter=event_emitter,
            machine_output=machine_output,
            renderer=renderer,
            title="Provider Preflight",
        )

    _emit_event(
        event_emitter,
        "provider_check_finished",
        {
            "provider_name": result.provider_name,
            "model_name": result.model_name,
            "base_url": result.base_url,
            "model_count": result.model_count,
            "completion_checked": result.completion_checked,
        },
        renderer=renderer,
        machine_output=machine_output,
    )
    if renderer:
        detail = (
            "models plus chat completion"
            if result.completion_checked
            else "models endpoint"
        )
        renderer.print_status(
            f"Provider check passed via {detail}; {result.model_count} models visible.",
            "Provider Preflight",
        )
    return result


def get_agent_config(config):
    """Read codex agent settings from config. Returns dict with binary, exec_flags, model_reasoning_effort."""
    defaults = {
        "binary": "codex",
        "exec_flags": "--dangerously-auto-approve",
        "model_reasoning_effort": "high",
    }
    codex_cfg = config.get("codex", {}) or {}
    return {k: codex_cfg.get(k, v) for k, v in defaults.items()}


def build_iteration_snapshot(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    path,
    config,
    iteration,
    operation,
    dry_run,
    run_started_at,
):
    """Build renderer-only loop context without changing workflow state."""
    provider_name = config["provider"]
    return IterationSnapshot(
        project_path=path,
        provider_name=provider_name,
        model_name=config["providers"][provider_name]["model"],
        iteration=iteration,
        operation=operation,
        dry_run=dry_run,
        elapsed_seconds=time.monotonic() - run_started_at,
    )


def build_db_log_snapshot(path, manager_output, stored_state):
    """Build renderer-only history write context after a successful DB commit."""
    return DbLogSnapshot(
        project_path=path,
        manager_output=manager_output,
        stored_state=stored_state,
        created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
    )


# ---------------------------------------------------------------------------
# Database layer
# ---------------------------------------------------------------------------


def db_init():
    """Create database directory and tables."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            cc_response TEXT,
            ai_decision_output TEXT,
            ai_decision_reason TEXT,
            help_or_done_msg TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_path_created
        ON history(path, created_at DESC)
    """)
    conn.commit()
    conn.close()


def db_fetch_history(path, limit=15):
    """Fetch last N history records for a project path."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM history WHERE path = ? ORDER BY created_at DESC LIMIT ?",
        (path, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def db_log(path, agent_response, ai_output, ai_reason, help_or_done_msg=None):
    """Log an iteration to the database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        """INSERT INTO history (path, cc_response, ai_decision_output,
           ai_decision_reason, help_or_done_msg)
           VALUES (?, ?, ?, ?, ?)""",
        (path, agent_response, ai_output, ai_reason, help_or_done_msg),
    )
    conn.commit()
    conn.close()


def db_show_history(path=None, renderer=None, verbose=False):
    """Display history records as a Rich table."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    if path:
        rows = conn.execute(
            "SELECT * FROM history WHERE path = ? ORDER BY created_at DESC LIMIT 50",
            (path,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM history ORDER BY created_at DESC LIMIT 50"
        ).fetchall()
    conn.close()

    if not rows:
        if renderer:
            renderer.print_history([], verbose=verbose)
            return
        console.print("[dim]No history records found.[/dim]")
        return

    if renderer:
        renderer.print_history([dict(row) for row in rows], verbose=verbose)
        return

    table = Table(title="Apex Infinite - History", show_lines=True)
    table.add_column("ID", style="dim", width=5)
    table.add_column("Path", style="cyan", max_width=30)
    table.add_column("AI Output", style="green", max_width=20)
    table.add_column("AI Reason", max_width=40)
    table.add_column("Agent Response", max_width=40)
    table.add_column("Help/Done", style="yellow", max_width=20)
    table.add_column("Time", style="dim", width=19)

    for row in rows:
        row = dict(row)
        resp = (row["cc_response"] or "")[:80]
        if len(row.get("cc_response") or "") > 80:
            resp += "..."
        table.add_row(
            str(row["id"]),
            row["path"],
            row["ai_decision_output"] or "",
            (row["ai_decision_reason"] or "")[:80],
            resp,
            row["help_or_done_msg"] or "",
            row["created_at"] or "",
        )

    console.print(table)


# ---------------------------------------------------------------------------
# LLM functions
# ---------------------------------------------------------------------------


def aggregate_history(records):
    """Format history records for LLM summarization.

    Format: [Task N: name]\nAgent: response\nManager: ai_decision
    """
    parts = []
    for i, rec in enumerate(records, 1):
        name = f"{rec.get('path', 'unknown')}_{rec.get('id', i)}"
        response = rec.get("cc_response", "") or ""
        decision = (
            f"Manager - Output: {rec.get('ai_decision_output', '')} "
            f"| Reason: {rec.get('ai_decision_reason', '')}"
        )
        parts.append(f"[Task {i}: {name}]\nAgent: {response}\nManager: {decision}")
    return "\n\n".join(parts)


def _llm_call_with_retry(client, model, messages, json_mode=False, renderer=None):
    """Call LLM with retry logic matching n8n retryOnFail + waitBetweenTries: 5000."""
    kwargs = {"model": model, "messages": messages}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    last_error = None
    for attempt in range(1, LLM_RETRY_COUNT + 1):
        try:
            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:  # pylint: disable=broad-exception-caught
            last_error = e
            if attempt < LLM_RETRY_COUNT:
                if renderer:
                    renderer.print_llm_retry(
                        attempt, LLM_RETRY_COUNT, e, wait_seconds=LLM_RETRY_WAIT
                    )
                else:
                    console.print(
                        f"  [yellow]LLM call failed (attempt {attempt}/{LLM_RETRY_COUNT}): {e}[/yellow]"
                    )
                    console.print(f"  [dim]Retrying in {LLM_RETRY_WAIT}s...[/dim]")
                time.sleep(LLM_RETRY_WAIT)
            else:
                message = f"LLM call failed after {LLM_RETRY_COUNT} attempts: {e}"
                if renderer:
                    renderer.print_error(message, "LLM Error")
                else:
                    console.print(f"  [red]{message}[/red]")
                raise last_error from e
    return None


def llm_summarize(client, model, records, renderer=None):
    """Summarize history records via LLM. Matches n8n 'Summarize History' node."""
    if not records:
        return "No prior interaction history."

    aggregated = aggregate_history(records)
    # Exact n8n user message template
    user_msg = f"INPUT:\n{aggregated}"

    messages = [
        {"role": "system", "content": SUMMARIZER_SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    return _llm_call_with_retry(client, model, messages, renderer=renderer)


def llm_manager_decide(  # pylint: disable=too-many-positional-arguments
    client, model, agent_response, ceo_msg, summary, renderer=None
):
    """Get manager LLM decision. Matches n8n 'LLM Generate Response' node."""
    user_msg = (
        f"IF EXISTS, CODEX CLI SENIOR DEVELOPER LATEST MESSAGE:\n{agent_response}\n\n"
        f"IF EXISTS, CEO'S INSTRUCTIONS:\n{ceo_msg}\n\n"
        f"HISTORICAL INTERACTIONS SUMMARY:\n{summary}"
    )

    messages = [
        {"role": "system", "content": MANAGER_SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    # Try JSON mode first, fall back to regex extraction
    try:
        raw = _llm_call_with_retry(
            client, model, messages, json_mode=True, renderer=renderer
        )
        result = json.loads(raw)
        if "output" in result and "reason" in result:
            return result
    except (json.JSONDecodeError, Exception):  # pylint: disable=broad-exception-caught
        pass

    # Fallback: try without json_mode and parse with regex
    try:
        raw = _llm_call_with_retry(
            client, model, messages, json_mode=False, renderer=renderer
        )
        # Try to extract JSON from the response
        json_match = re.search(
            r'\{[^{}]*"output"\s*:\s*"[^"]*"[^{}]*"reason"\s*:\s*"[^"]*"[^{}]*\}', raw
        )
        if json_match:
            return json.loads(json_match.group())
        # Last resort: try to parse the whole response as JSON
        return json.loads(raw)
    except (json.JSONDecodeError, Exception):  # pylint: disable=broad-exception-caught
        # Absolute fallback
        if renderer:
            renderer.print_json_fallback()
        else:
            console.print(
                "  [yellow]Could not parse LLM response as JSON, using raw output[/yellow]"
            )
        return {"output": raw.strip(), "reason": "Raw LLM output (JSON parse failed)"}


# ---------------------------------------------------------------------------
# Command execution
# ---------------------------------------------------------------------------


def build_codex_prompt(output_cmd, raw_output):
    """Build the prompt string for codex exec.

    Known commands: invoke apex-spec skill command via natural language prompt.
    Custom: pass raw output as the prompt.
    """
    cmd_lower = output_cmd.strip().lower().lstrip("/")

    if cmd_lower in KNOWN_COMMANDS:
        actual_cmd = COMMAND_ALIASES.get(cmd_lower, cmd_lower)
        return f"Run the apex-spec skill command /{actual_cmd}"
    # Custom instructions fallback
    return raw_output


def execute_codex(  # pylint: disable=too-many-positional-arguments,too-many-branches,too-many-statements,too-many-locals
    path,
    prompt,
    agent_cfg,
    dry_run=False,
    verbose=False,
    renderer=None,
    event_emitter=None,
    machine_output=False,
):
    """Run codex exec subprocess in project directory. Returns stdout."""
    expanded_path = os.path.expanduser(path)
    binary = agent_cfg["binary"]
    exec_flags = agent_cfg["exec_flags"]
    emitter = event_emitter or NoOpEventEmitter()

    def build_command_snapshot(
        snapshot_prompt,
        return_code=None,
        process_state=None,
        elapsed_seconds=None,
    ):
        return CodexCommandSnapshot(
            binary=binary,
            exec_flags=exec_flags,
            prompt=snapshot_prompt,
            project_path=expanded_path,
            timeout=COMMAND_TIMEOUT,
            return_code=return_code,
            process_state=process_state,
            elapsed_seconds=elapsed_seconds,
        )

    if dry_run:
        _emit_event(
            emitter,
            "codex_dry_run",
            {
                "binary": binary,
                "project_path": expanded_path,
                "prompt_length": len(prompt),
                "timeout_seconds": COMMAND_TIMEOUT,
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        if renderer:
            renderer.print_codex_command(
                "dry-run",
                build_command_snapshot(prompt, process_state="not launched"),
            )
        else:
            console.print(f"  [dim][DRY RUN] Would execute in {expanded_path}:[/dim]")
            console.print(f'  [dim]{binary} exec {exec_flags} "{prompt}"[/dim]')
        output = f"[DRY RUN] Command: {prompt}"
        _emit_event(
            emitter,
            "response_summarized",
            {"source": "codex_dry_run", **summarize_text(output, limit=0)},
            renderer=renderer,
            machine_output=machine_output,
        )
        return output

    if renderer:
        renderer.print_codex_command(
            "start",
            build_command_snapshot(
                prompt,
                process_state="running",
                elapsed_seconds=0,
            ),
        )
    else:
        console.print(
            f"  [dim]Executing {binary} in {expanded_path} "
            f"(timeout {COMMAND_TIMEOUT}s)...[/dim]"
        )

    started_at = time.monotonic()
    _emit_event(
        emitter,
        "codex_started",
        {
            "binary": binary,
            "project_path": expanded_path,
            "prompt_length": len(prompt),
            "timeout_seconds": COMMAND_TIMEOUT,
        },
        renderer=renderer,
        machine_output=machine_output,
    )
    try:
        cmd = [binary, "exec", *exec_flags.split(), prompt]

        result = run_codex_process(cmd, expanded_path, COMMAND_TIMEOUT)
        elapsed_seconds = time.monotonic() - started_at

        output = result.stdout
        if not output.strip() and result.stderr.strip():
            output = result.stderr

        if result.returncode != 0:
            error_msg = result.stderr or "Unknown error"
            output = f"[ERROR exit code {result.returncode}]\nstdout: {result.stdout}\nstderr: {error_msg}"
            _emit_event(
                emitter,
                "codex_error",
                {
                    "error_type": "non_zero_exit",
                    "return_code": result.returncode,
                    "elapsed_seconds": elapsed_seconds,
                    "stdout_length": len(result.stdout or ""),
                    "stderr_length": len(result.stderr or ""),
                },
                renderer=renderer,
                machine_output=machine_output,
            )
            if renderer:
                renderer.print_codex_command(
                    "non-zero",
                    build_command_snapshot(
                        prompt,
                        return_code=result.returncode,
                        process_state="exited non-zero",
                        elapsed_seconds=elapsed_seconds,
                    ),
                )
            else:
                console.print(
                    f"  [red]Codex exited with code {result.returncode}[/red]"
                )
        else:
            _emit_event(
                emitter,
                "codex_finished",
                {
                    "return_code": result.returncode,
                    "elapsed_seconds": elapsed_seconds,
                    "stdout_length": len(result.stdout or ""),
                    "stderr_length": len(result.stderr or ""),
                },
                renderer=renderer,
                machine_output=machine_output,
            )
            if renderer:
                renderer.print_codex_command(
                    "complete",
                    build_command_snapshot(
                        prompt,
                        return_code=result.returncode,
                        process_state="completed",
                        elapsed_seconds=elapsed_seconds,
                    ),
                )
            else:
                console.print(f"  [dim]Codex completed in {elapsed_seconds:.1f}s[/dim]")

        if renderer:
            renderer.print_agent_response(output, verbose=verbose)
        elif verbose:
            console.print(
                Panel(output[:2000], title="Agent Response (full)", border_style="blue")
            )
        else:
            truncated = output[:500]
            if len(output) > 500:
                truncated += (
                    f"\n... ({len(output)} chars total, use --verbose for full)"
                )
            console.print(Panel(truncated, title="Agent Response", border_style="blue"))

        _emit_event(
            emitter,
            "response_summarized",
            {"source": "codex", **summarize_text(output, limit=0)},
            renderer=renderer,
            machine_output=machine_output,
        )
        return output

    except subprocess.TimeoutExpired:
        msg = f"[TIMEOUT] Codex command timed out after {COMMAND_TIMEOUT}s"
        elapsed_seconds = time.monotonic() - started_at
        _emit_event(
            emitter,
            "codex_timeout",
            {
                "elapsed_seconds": elapsed_seconds,
                "timeout_seconds": COMMAND_TIMEOUT,
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        if renderer:
            renderer.print_codex_command(
                "timeout",
                build_command_snapshot(
                    msg,
                    process_state="timed out",
                    elapsed_seconds=elapsed_seconds,
                ),
            )
        else:
            console.print(f"  [red]{msg}[/red]")
        _emit_event(
            emitter,
            "response_summarized",
            {"source": "codex_timeout", **summarize_text(msg, limit=0)},
            renderer=renderer,
            machine_output=machine_output,
        )
        return msg
    except FileNotFoundError:
        msg = f"[ERROR] '{binary}' command not found. Is Codex CLI installed?"
        elapsed_seconds = time.monotonic() - started_at
        _emit_event(
            emitter,
            "codex_error",
            {
                "error_type": "missing_binary",
                "elapsed_seconds": elapsed_seconds,
                "binary": binary,
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        if renderer:
            renderer.print_codex_command(
                "missing",
                build_command_snapshot(
                    msg,
                    process_state="missing binary",
                    elapsed_seconds=elapsed_seconds,
                ),
            )
        else:
            console.print(f"  [red]{msg}[/red]")
        _emit_event(
            emitter,
            "response_summarized",
            {"source": "codex_missing", **summarize_text(msg, limit=0)},
            renderer=renderer,
            machine_output=machine_output,
        )
        return msg
    except Exception as e:  # pylint: disable=broad-exception-caught
        msg = f"[ERROR] Failed to execute {binary}: {e}"
        elapsed_seconds = time.monotonic() - started_at
        _emit_event(
            emitter,
            "codex_error",
            {
                "error_type": e.__class__.__name__,
                "elapsed_seconds": elapsed_seconds,
                "binary": binary,
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        if renderer:
            renderer.print_codex_command(
                "error",
                build_command_snapshot(
                    msg,
                    process_state="failed",
                    elapsed_seconds=elapsed_seconds,
                ),
            )
        else:
            console.print(f"  [red]{msg}[/red]")
        _emit_event(
            emitter,
            "response_summarized",
            {"source": "codex_error", **summarize_text(msg, limit=0)},
            renderer=renderer,
            machine_output=machine_output,
        )
        return msg


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------


def notify(title, message):
    """Terminal bell + desktop notification."""
    # Terminal bell is useful interactively, but must not leak into redirected
    # logs, plain output captures, or machine-readable wrappers.
    if sys.stdout.isatty():
        sys.stdout.write("\a")
        sys.stdout.flush()

    # Linux desktop notification
    try:
        subprocess.run(
            ["notify-send", title, message],
            capture_output=True,
            timeout=5,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def infinite_loop(  # pylint: disable=too-many-positional-arguments,too-many-arguments,too-many-statements,too-many-locals,too-many-branches
    path,
    config,
    start_command=None,
    ceo_message="",
    max_iterations=DEFAULT_MAX_ITERATIONS,
    dry_run=False,
    verbose=False,
    renderer=None,
    event_emitter=None,
    machine_output=False,
    notifications_enabled=True,
):
    """The main autonomous loop replacing n8n webhook->LLM->SSH->webhook cycle."""
    global _INTERRUPTED  # pylint: disable=global-statement

    emitter = event_emitter or NoOpEventEmitter()
    client, model = get_llm_client(config)
    agent_cfg = get_agent_config(config)
    agent_response = ""
    ceo_msg = ceo_message or ""
    iteration = 0
    run_started_at = time.monotonic()

    while iteration < max_iterations:
        iteration += 1

        # Check interrupt flag
        if _INTERRUPTED:
            _INTERRUPTED = False
            _emit_event(
                emitter,
                "operator_interrupt_requested",
                {"state": "pause", "iteration": iteration},
                renderer=renderer,
                machine_output=machine_output,
            )
            if renderer:
                renderer.print_interrupt("pause", "CEO interrupt - input requested.")
            else:
                console.print("\n[bold yellow]--- CEO INTERRUPT ---[/bold yellow]")
            if notifications_enabled:
                notify("Apex Infinite", "CEO interrupt - input requested")
            ceo_input = console.input(
                renderer.input_prompt("CEO instructions (or 'quit')")
                if renderer
                else "[bold]CEO instructions (or 'quit'): [/bold]"
            )
            if ceo_input.strip().lower() == "quit":
                _emit_event(
                    emitter,
                    "operator_input_received",
                    {"context": "interrupt", "action": "quit"},
                    renderer=renderer,
                    machine_output=machine_output,
                )
                if renderer:
                    renderer.print_interrupt("quit", "Quitting by CEO request.")
                else:
                    console.print("[bold red]Quitting by CEO request.[/bold red]")
                _emit_event(
                    emitter,
                    "run_stopped",
                    {"reason": "operator_quit", "iteration": iteration},
                    renderer=renderer,
                    machine_output=machine_output,
                )
                break
            _emit_event(
                emitter,
                "operator_input_received",
                {
                    "context": "interrupt",
                    "action": "continue",
                    "input_length": len(ceo_input),
                },
                renderer=renderer,
                machine_output=machine_output,
            )
            ceo_msg = ceo_input

        # Banner
        provider_name = config["provider"]
        _emit_event(
            emitter,
            "iteration_started",
            {
                "project_path": path,
                "provider_name": provider_name,
                "model_name": config["providers"][provider_name]["model"],
                "iteration": iteration,
                "operation": "history summary",
                "dry_run": dry_run,
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        if renderer:
            renderer.print_iteration(
                build_iteration_snapshot(
                    path,
                    config,
                    iteration,
                    "history summary",
                    dry_run,
                    run_started_at,
                )
            )
        else:
            console.print(f"\n[bold]{'=' * 60}[/bold]")
            console.print(f"  [bold cyan]ITERATION {iteration}[/bold cyan]")
            console.print(f"[bold]{'=' * 60}[/bold]")

        # 1. Fetch + summarize history
        records = db_fetch_history(path, limit=15)
        _emit_event(
            emitter,
            "history_fetched",
            {
                "project_path": path,
                "iteration": iteration,
                "record_count": len(records),
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        if renderer:
            renderer.print_status(
                f"Summarizing history from {len(records)} prior records.",
                "History Summary",
            )
        else:
            console.print(f"  Summarizing history... ({len(records)} prior records)")
        _emit_event(
            emitter,
            "history_summarize_started",
            {"iteration": iteration, "record_count": len(records)},
            renderer=renderer,
            machine_output=machine_output,
        )
        try:
            summary = llm_summarize(client, model, records, renderer=renderer)
        except Exception as exc:
            _emit_event(
                emitter,
                "error",
                {
                    "stage": "history_summary",
                    "iteration": iteration,
                    "error_type": exc.__class__.__name__,
                },
                renderer=renderer,
                machine_output=machine_output,
            )
            raise
        _emit_event(
            emitter,
            "history_summarize_finished",
            {"iteration": iteration, "summary_length": len(summary or "")},
            renderer=renderer,
            machine_output=machine_output,
        )

        # 2. Manager LLM decides next action
        _emit_event(
            emitter,
            "manager_decision_started",
            {
                "iteration": iteration,
                "source": (
                    "start_command"
                    if start_command and iteration == 1
                    else "manager_llm"
                ),
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        if start_command and iteration == 1:
            decision = {
                "output": start_command,
                "reason": "User-specified start command",
            }
        else:
            if renderer:
                renderer.print_status("Manager deciding next action.", "Manager")
            else:
                console.print("  Manager deciding next action...")
            try:
                decision = llm_manager_decide(
                    client, model, agent_response, ceo_msg, summary, renderer=renderer
                )
            except Exception as exc:
                _emit_event(
                    emitter,
                    "error",
                    {
                        "stage": "manager_decision",
                        "iteration": iteration,
                        "error_type": exc.__class__.__name__,
                    },
                    renderer=renderer,
                    machine_output=machine_output,
                )
                raise

        output_val = decision.get("output", "").strip()
        reason_val = decision.get("reason", "")

        # 3. Route on decision
        # Strip leading slash - LLM sometimes outputs "/plansession" instead of "plansession"
        output_lower = output_val.lower().lstrip("/")
        _emit_event(
            emitter,
            "manager_decision_finished",
            {
                "iteration": iteration,
                "output": output_val,
                "reason": reason_val,
                "known_command": output_lower in KNOWN_COMMANDS,
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        if renderer:
            renderer.print_manager_decision(
                output_val, reason_val, output_lower in KNOWN_COMMANDS
            )
        else:
            console.print(f"  [bold green]Manager Decision:[/bold green] {output_val}")
            console.print(f"  [dim]Reason: {reason_val}[/dim]")

        if output_lower == "help":
            if renderer:
                renderer.print_help(reason_val)
            else:
                console.print(
                    "\n[bold yellow]*** MANAGER NEEDS CEO HELP ***[/bold yellow]"
                )
                console.print(f"[yellow]Reason: {reason_val}[/yellow]")
            _emit_event(
                emitter,
                "help_requested",
                {"iteration": iteration, "reason": reason_val},
                renderer=renderer,
                machine_output=machine_output,
            )
            if notifications_enabled:
                notify("Apex Infinite - HELP", reason_val)
            _emit_event(
                emitter,
                "db_log_started",
                {
                    "project_path": path,
                    "iteration": iteration,
                    "stored_state": "help pause",
                },
                renderer=renderer,
                machine_output=machine_output,
            )
            db_log(
                path,
                agent_response,
                output_val,
                reason_val,
                help_or_done_msg=reason_val,
            )
            _emit_event(
                emitter,
                "db_log_finished",
                {
                    "project_path": path,
                    "iteration": iteration,
                    "stored_state": "help pause",
                },
                renderer=renderer,
                machine_output=machine_output,
            )
            if renderer:
                renderer.print_db_log(
                    build_db_log_snapshot(path, output_val, "help pause")
                )
            ceo_input = console.input(
                renderer.input_prompt("CEO response (or 'quit')")
                if renderer
                else "[bold]CEO response (or 'quit'): [/bold]"
            )
            if ceo_input.strip().lower() == "quit":
                _emit_event(
                    emitter,
                    "operator_input_received",
                    {"context": "help", "action": "quit"},
                    renderer=renderer,
                    machine_output=machine_output,
                )
                _emit_event(
                    emitter,
                    "run_stopped",
                    {"reason": "operator_quit", "iteration": iteration},
                    renderer=renderer,
                    machine_output=machine_output,
                )
                break
            _emit_event(
                emitter,
                "operator_input_received",
                {
                    "context": "help",
                    "action": "continue",
                    "input_length": len(ceo_input),
                },
                renderer=renderer,
                machine_output=machine_output,
            )
            ceo_msg = ceo_input
            continue

        if output_lower == "alldonebaby":
            _emit_event(
                emitter,
                "workflow_completed",
                {
                    "iteration": iteration,
                    "reason": reason_val,
                },
                renderer=renderer,
                machine_output=machine_output,
            )
            if renderer:
                renderer.print_completion(reason_val, iteration)
            else:
                console.print("\n[bold green]*** PROJECT COMPLETE! ***[/bold green]")
                console.print(f"[green]Reason: {reason_val}[/green]")
            if notifications_enabled:
                notify("Apex Infinite - ALL DONE!", "Project complete!")
            _emit_event(
                emitter,
                "db_log_started",
                {
                    "project_path": path,
                    "iteration": iteration,
                    "stored_state": "completion",
                },
                renderer=renderer,
                machine_output=machine_output,
            )
            db_log(
                path,
                agent_response,
                output_val,
                reason_val,
                help_or_done_msg="ALL DONE BABY!",
            )
            _emit_event(
                emitter,
                "db_log_finished",
                {
                    "project_path": path,
                    "iteration": iteration,
                    "stored_state": "completion",
                },
                renderer=renderer,
                machine_output=machine_output,
            )
            if renderer:
                renderer.print_db_log(
                    build_db_log_snapshot(path, output_val, "completion")
                )
            if not renderer:
                console.print(f"\n[bold]Total iterations: {iteration}[/bold]")
            _emit_event(
                emitter,
                "run_stopped",
                {"reason": "workflow_completed", "iteration": iteration},
                renderer=renderer,
                machine_output=machine_output,
            )
            break

        # 4. Build prompt and execute codex
        prompt = build_codex_prompt(output_lower, output_val)
        _emit_event(
            emitter,
            "prompt_built",
            {
                "iteration": iteration,
                "manager_output": output_val,
                "known_command": output_lower in KNOWN_COMMANDS,
                "prompt_length": len(prompt),
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        if renderer:
            renderer.print_prompt_preview(prompt)
        else:
            console.print(f"  [dim]Prompt: {prompt[:100]}...[/dim]")

        _emit_event(
            emitter,
            "prompt_dispatched",
            {"iteration": iteration, "prompt_length": len(prompt)},
            renderer=renderer,
            machine_output=machine_output,
        )
        agent_response = execute_codex(
            path,
            prompt,
            agent_cfg,
            dry_run=dry_run,
            verbose=verbose,
            renderer=renderer,
            event_emitter=emitter,
            machine_output=machine_output,
        )

        # 5. Log to DB
        _emit_event(
            emitter,
            "db_log_started",
            {
                "project_path": path,
                "iteration": iteration,
                "stored_state": "iteration result",
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        db_log(path, agent_response, output_val, reason_val)
        _emit_event(
            emitter,
            "db_log_finished",
            {
                "project_path": path,
                "iteration": iteration,
                "stored_state": "iteration result",
            },
            renderer=renderer,
            machine_output=machine_output,
        )
        if renderer:
            renderer.print_db_log(
                build_db_log_snapshot(path, output_val, "iteration result")
            )

        # 6. Clear CEO message after first use
        ceo_msg = ""

    else:
        if renderer:
            renderer.print_max_iterations(max_iterations)
        else:
            console.print(
                f"\n[bold yellow]Reached max iterations ({max_iterations}). Stopping.[/bold yellow]"
            )
        _emit_event(
            emitter,
            "max_iterations_reached",
            {"max_iterations": max_iterations},
            renderer=renderer,
            machine_output=machine_output,
        )
        if notifications_enabled:
            notify("Apex Infinite", f"Reached max iterations ({max_iterations})")
        _emit_event(
            emitter,
            "run_stopped",
            {"reason": "max_iterations", "max_iterations": max_iterations},
            renderer=renderer,
            machine_output=machine_output,
        )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


@click.command()
@click.option(
    "--path", "project_path", default=None, help="Project path (prompted if not given)"
)
@click.option("--start", default=None, help='Starting command (e.g. "plansession")')
@click.option("--ceo", default=None, help="Initial CEO instructions")
@click.option(
    "--provider", default=None, help="LLM provider override: ollama|grok|openai"
)
@click.option("--model", default=None, help="Model override")
@click.option(
    "--config",
    "config_path",
    default=None,
    help="Config file path (default: ./config.yaml, then packaged config)",
)
@click.option("--history", is_flag=True, help="Show interaction history")
@click.option(
    "--max-iterations",
    default=DEFAULT_MAX_ITERATIONS,
    type=int,
    help=f"Safety limit (default: {DEFAULT_MAX_ITERATIONS})",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would execute without running codex"
)
@click.option("--verbose", is_flag=True, help="Show full agent output")
@click.option(
    "--theme", default=None, help="UI theme: auto|crt-green|crt-amber|ibm-dos|plain"
)
@click.option("--plain", is_flag=True, help="Disable color and effects")
@click.option("--ascii", "ascii_only", is_flag=True, help="Use ASCII-safe glyphs")
@click.option("--compact", is_flag=True, help="Reduce vertical spacing")
@click.option(
    "--check-provider",
    is_flag=True,
    help="Run provider connectivity and model preflight, then exit.",
)
@click.option(
    "--check-provider-chat",
    is_flag=True,
    help="Include a tiny chat completion in provider checks.",
)
@click.option(
    "--skip-provider-check",
    is_flag=True,
    help="Skip startup provider preflight before the loop.",
)
@click.option(
    "--event-stream",
    default=None,
    help="Write machine-readable lifecycle JSONL to PATH, or '-' with --machine-output.",
)
@click.option(
    "--machine-output",
    is_flag=True,
    help="Disable human output and reserve stdout for event JSONL.",
)
@click.version_option(version="2.0.0", prog_name="apex-infinite")
def main(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals,too-many-branches,too-many-statements
    project_path,
    start,
    ceo,
    provider,
    model,
    config_path,
    history,
    max_iterations,
    dry_run,
    verbose,
    theme,
    plain,
    ascii_only,
    compact,
    check_provider,
    check_provider_chat,
    skip_provider_check,
    event_stream,
    machine_output,
):
    """Apex Spec System Infinite CLI - Autonomous Codex CLI session manager."""
    global _ACTIVE_RENDERER, _ACTIVE_EVENT_EMITTER  # pylint: disable=global-statement
    global _MACHINE_OUTPUT_ACTIVE  # pylint: disable=global-statement

    if machine_output and not event_stream:
        raise click.UsageError("--machine-output requires --event-stream")
    if event_stream == "-" and not machine_output:
        raise click.UsageError("--event-stream - requires --machine-output")
    if check_provider and skip_provider_check:
        raise click.UsageError(
            "--check-provider cannot be combined with --skip-provider-check"
        )

    try:
        event_stream_context = open_event_stream(
            event_stream, stdout_allowed=machine_output
        )
    except EventStreamError as exc:
        raise click.ClickException(str(exc)) from exc

    with event_stream_context as event_emitter:
        _ACTIVE_EVENT_EMITTER = event_emitter
        _MACHINE_OUTPUT_ACTIVE = machine_output
        _emit_event(
            event_emitter,
            "startup_begin",
            {
                "event_stream": bool(event_stream),
                "machine_output": machine_output,
                "dry_run": dry_run,
                "max_iterations": max_iterations,
                "check_provider": check_provider,
                "provider_completion_check": check_provider_chat,
            },
            machine_output=machine_output,
        )

        try:
            _run_main(
                project_path,
                start,
                ceo,
                provider,
                model,
                config_path,
                history,
                max_iterations,
                dry_run,
                verbose,
                theme,
                plain,
                ascii_only,
                compact,
                check_provider,
                check_provider_chat,
                skip_provider_check,
                event_emitter,
                event_stream,
                machine_output,
            )
        finally:
            _ACTIVE_RENDERER = None
            _ACTIVE_EVENT_EMITTER = None
            _MACHINE_OUTPUT_ACTIVE = False


def _run_main(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals,too-many-branches,too-many-statements
    project_path,
    start,
    ceo,
    provider,
    model,
    config_path,
    history,
    max_iterations,
    dry_run,
    verbose,
    theme,
    plain,
    ascii_only,
    compact,
    check_provider,
    check_provider_chat,
    skip_provider_check,
    event_emitter,
    event_stream,
    machine_output,
):
    """Run CLI startup after event stream validation."""
    global _ACTIVE_RENDERER  # pylint: disable=global-statement

    # Init database
    db_init()

    if config_path is None:
        config_path = resolve_default_config_path()
        if config_path is None:
            _exit_with_startup_error(
                "No config.yaml found. Use --config to specify path.",
                event_emitter=event_emitter,
                machine_output=machine_output,
                title="Config",
            )

    try:
        config = load_config(
            config_path, provider_override=provider, model_override=model
        )
    except CliStartupError as exc:
        _exit_with_startup_error(
            str(exc),
            event_emitter=event_emitter,
            machine_output=machine_output,
            title="Config",
        )
    provider_name = config["provider"]
    model_name = config["providers"][provider_name]["model"]
    _emit_event(
        event_emitter,
        "config_loaded",
        {
            "config_path": config_path,
            "provider_name": provider_name,
            "model_name": model_name,
        },
        machine_output=machine_output,
    )
    try:
        ui_settings = resolve_ui_settings(
            config,
            UiCliOverrides(
                theme=theme,
                plain=plain,
                ascii_only=ascii_only,
                compact=compact,
            ),
            env=os.environ,
            console=console,
        )
    except UiConfigError as exc:
        _exit_with_startup_error(
            f"Invalid UI configuration: {exc}",
            event_emitter=event_emitter,
            machine_output=machine_output,
            title="UI Configuration",
        )
    _emit_event(
        event_emitter,
        "ui_resolved",
        {
            "requested_theme": ui_settings.requested_theme,
            "theme_name": ui_settings.theme_name,
            "effect_level": ui_settings.effect_level,
            "plain": ui_settings.plain,
            "ascii_only": ui_settings.ascii_only,
            "compact": ui_settings.compact,
            "color_enabled": ui_settings.color_enabled,
            "constraint_reason": ui_settings.constraint_reason,
        },
        machine_output=machine_output,
    )
    renderer = (
        NoHumanOutputRenderer(ui_settings)
        if machine_output
        else ApexRenderer(ui_settings, console)
    )
    _ACTIVE_RENDERER = renderer

    if check_provider:
        _run_provider_preflight_or_exit(
            config,
            check_completion=check_provider_chat,
            renderer=renderer,
            event_emitter=event_emitter,
            machine_output=machine_output,
        )
        return

    # History mode
    if history:
        db_show_history(project_path, renderer=renderer, verbose=verbose)
        return

    # Interactive mode if no path given
    if not project_path:
        renderer.print_intro()

        # List ~/projects/ directories
        projects_dir = Path.home() / "projects"
        if projects_dir.exists():
            dirs = sorted(
                [
                    d
                    for d in projects_dir.iterdir()
                    if d.is_dir() and not d.name.startswith(".")
                ]
            )
            renderer.print_project_list(dirs)

            selection = console.input(
                renderer.input_prompt("Select project [number or path]")
            ).strip()
            if selection.isdigit():
                idx = int(selection) - 1
                if 0 <= idx < len(dirs):
                    project_path = str(dirs[idx])
                else:
                    renderer.print_error("Invalid selection.", "Project Selection")
                    sys.exit(1)
            else:
                project_path = selection
        else:
            project_path = console.input(renderer.input_prompt("Project path")).strip()

        if not start:
            start_input = console.input(
                renderer.input_prompt(
                    'Starting command (e.g. "plansession", Enter for auto)'
                )
            ).strip()
            if start_input:
                start = start_input

        if not ceo:
            ceo_input = console.input(
                renderer.input_prompt("CEO instructions (optional, Enter to skip)")
            ).strip()
            if ceo_input:
                ceo = ceo_input

    # Expand and validate path
    project_path = os.path.expanduser(project_path)
    if not os.path.isdir(project_path):
        _exit_with_startup_error(
            f"Directory not found: {project_path}",
            event_emitter=event_emitter,
            machine_output=machine_output,
            renderer=renderer,
            title="Project Path",
        )

    # Normalize path (remove trailing slash for consistent DB keys)
    project_path = project_path.rstrip("/") + "/"
    _emit_event(
        event_emitter,
        "project_resolved",
        {"project_path": project_path},
        renderer=renderer,
        machine_output=machine_output,
    )

    if not skip_provider_check:
        _run_provider_preflight_or_exit(
            config,
            check_completion=check_provider_chat,
            renderer=renderer,
            event_emitter=event_emitter,
            machine_output=machine_output,
        )

    # Display startup banner
    renderer.print_startup(
        StartupSnapshot(
            project_path=project_path,
            provider_name=provider_name,
            model_name=model_name,
            config_path=config_path,
            max_iterations=max_iterations,
            theme_name=ui_settings.theme_name,
            requested_theme=ui_settings.requested_theme,
            dry_run=dry_run,
            start_command=start,
            ceo_present=bool(ceo),
        )
    )
    _emit_event(
        event_emitter,
        "startup",
        {
            "project_path": project_path,
            "provider_name": provider_name,
            "model_name": model_name,
            "config_path": config_path,
            "theme_name": ui_settings.theme_name,
            "max_iterations": max_iterations,
            "dry_run": dry_run,
            "start_command": start,
            "ceo_present": bool(ceo),
            "event_stream_path": event_stream,
            "machine_output": machine_output,
        },
        renderer=renderer,
        machine_output=machine_output,
    )

    # Run the loop
    infinite_loop(
        path=project_path,
        config=config,
        start_command=start,
        ceo_message=ceo or "",
        max_iterations=max_iterations,
        dry_run=dry_run,
        verbose=verbose,
        renderer=renderer,
        event_emitter=event_emitter,
        machine_output=machine_output,
        notifications_enabled=not machine_output,
    )


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
