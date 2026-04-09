# CONVENTIONS.md

## Guiding Principles

- Optimize for readability over cleverness
- Code is written once, read many times
- Consistency beats personal preference
- If it can be automated, automate it
- When writing code: Make NO assumptions. Do not be lazy. Pattern match precisely. Do not skim when you need detailed info from documents. Validate systematically.

## Naming

- Markdown files: kebab-case (`initspec.md`, `sculpt-ui.md`, `workflow-overview.md`)
- Bash scripts: kebab-case (`analyze-project.sh`, `check-prereqs.sh`)
- Bash variables: UPPER_SNAKE_CASE for constants and exports (`SPEC_DIR`, `STATE_FILE`)
- Bash local variables: lower_snake_case (`session_dir`, `phase_num`)
- Bash functions: lower_snake_case (`get_project_name`, `check_tool`)
- YAML keys: snake_case (`display_name`, `brand_color`)
- JSON keys: snake_case (`current_phase`, `completed_sessions`)
- Reference files named to match the command they define (e.g., `references/initspec.md` for initspec)

## Files & Structure

- Skill directory follows Agent Skills standard: SKILL.md at root, references/, scripts/, agents/, assets/
- One command definition per reference file in references/
- Scripts in scripts/ are standalone bash with common.sh sourced for shared functions
- SKILL.md is the single entry point (orchestrator) -- all routing logic lives here
- agents/openai.yaml contains Codex-specific metadata only
- Group supporting docs (guidance, utilities, walkthrough) alongside command references in references/
- Keep nesting shallow -- skill directory is flat by design

## Markdown & Reference Files

- Reference files have NO YAML frontmatter (the orchestrator SKILL.md handles routing)
- First line is always a level-1 heading: `# Command Name`
- Use platform-neutral language: "Read the file" not "Use the Read tool"
- Use generic action verbs: "Run", "Create", "Modify", "Search for", "Find files matching"
- Never reference ${CLAUDE_PLUGIN_ROOT} -- use .spec_system/scripts/ (local-first)
- Never use /commandname slash syntax -- use workflow step names
- Keep reference files under 500 lines
- Use fenced code blocks with language tags for all code examples

## Reference Anatomy

Command reference files should follow a predictable internal shape so a reader
can find rules, first steps, quality gates, and handoffs without re-learning
each document.

- Title first: `# command-name`
- Opening summary next: 1-3 sentences stating what the command does
- Workflow position next when relevant: if the command belongs to a staged
  workflow, state what should have happened before it and what usually follows
- Use `## Rules` for durable command rules; do not use alternate capitalization
  such as `## RULES`
- Use `### No Deferral Policy` directly under `## Rules` when the command is
  expected to resolve its own blockers
- Use `## Steps` for the execution flow
- If the command depends on project state, scripts, or current-session facts,
  make the first operational step explicit and mark it `REQUIRED FIRST STEP`
- Put the local-first script resolution pattern inside the first step that needs
  scripts, not in scattered reminders throughout the file
- Keep command-local pass or fail thresholds, bundle ordering, state mutation
  rules, and workflow handoff logic in the command reference itself
- Move reusable cross-cutting guidance into supporting checklist references
  under `references/` when the same guidance appears in multiple workflow docs
- End with `## Output`, and add `## Next Action` when the command has a normal
  handoff to another workflow step or a user decision

For the highest-leverage workflow references, normalize section names and order
before adding more prose. The goal is predictability, not longer files.

## Bash Scripts

- Start every script with `#!/usr/bin/env bash`
- Use `set -euo pipefail` at the top of every script
- Source common.sh for shared functions: `source "$(dirname "$0")/common.sh"`
- Quote all variable expansions: `"${var}"` not `$var`
- Use `[[ ]]` for conditionals, not `[ ]`
- Use `local` for function-scoped variables
- Prefer `printf` over `echo` for portable output
- JSON output uses jq for formatting -- never hand-construct JSON strings
- Exit codes: 0 = success, 1 = general error, 2 = usage error
- Write to stderr for diagnostics, stdout for data: `echo "warning" >&2`
- Target POSIX-compatible bash + jq (no bashisms beyond bash 4.0)
- No external dependencies beyond bash, git, jq, and standard coreutils

## YAML

- Use 2-space indentation
- Quote strings containing special characters
- Keep agents/openai.yaml minimal -- only Codex-required fields

## JSON

- state.json uses 2-space indentation
- All keys use snake_case
- Boolean values: true/false (never strings)
- Null for unknown/unset (never empty string)

## Comments

- Explain *why*, not *what*
- Delete commented-out code -- that is what git is for
- TODOs include context: `# TODO(name): reason, ticket if applicable`
- Update or remove comments when code changes
- In bash: use `#` comments; align inline comments when grouping related lines

## Error Handling

- Fail fast and loud in scripts (set -euo pipefail)
- Provide actionable error messages with context: what failed and what to do
- Validate inputs at script entry points (check arguments, file existence)
- Reference files should include clear failure conditions and recovery steps

## Testing

- Test scripts on macOS (zsh/bash), Ubuntu/Debian (bash), and WSL2 (bash)
- Verify ASCII-only encoding: `LC_ALL=C grep -n '[^[:print:][:space:]]' file`
- Verify LF line endings: `grep -n "$(printf '\r')" file`
- Test each command dispatch independently via the orchestrator
- End-to-end test: initspec -> plansession -> implement -> validate

## Git & Version Control

- Commit messages: imperative mood, concise (`Add user validation` not `Added some validation stuff`)
- One logical change per commit
- Branch names: `type/short-description` (e.g., `feat/orchestrator-skillmd`, `fix/script-path`)
- Keep commits atomic enough to revert safely

## Pull Requests

- Small PRs get better reviews
- Description explains the *what* and *why* -- reviewers can see the *how*
- Link relevant tickets/context
- Review your own PR before requesting others

## Dependencies

- Runtime: bash, git, jq only -- no additional package managers
- No build step required -- skill is plain files (markdown, yaml, bash, json)
- Pin nothing -- scripts use whatever version of bash/jq is installed

## Encoding (Non-Negotiable)

- All files must be ASCII-only (code points 0-127)
- No Unicode, no emoji, no smart quotes, no em-dashes
- Use straight quotes (" ') and hyphens (-) only
- Unix LF line endings (no CRLF)
- Validate: `file filename.txt` should show "ASCII text"

## Local Dev Tools

| Category | Tool | Config |
|----------|------|--------|
| Formatter | shfmt (scripts) | .editorconfig |
| Linter | shellcheck (scripts) | default rules + --source-path=scripts |
| Type Safety | N/A | - |
| Testing | bats-core (scripts) | tests/*.bats |
| Observability | N/A | - |
| Git Hooks | pre-commit | .pre-commit-config.yaml |
| Database | N/A | - |

## CI/CD

| Bundle | Status | Workflow |
|--------|--------|----------|
| Code Quality | configured | .github/workflows/quality.yml |
| Build & Test | configured | .github/workflows/test.yml |
| Security | configured | .github/workflows/security.yml |
| Integration | configured | .github/workflows/integration.yml |
| Operations | configured | .github/workflows/release.yml, .github/dependabot.yml |

## Infrastructure

| Component | Provider | Details |
|-----------|----------|---------|
| CDN/DNS | N/A | Plugin distributed via Git clone, not hosted |
| WAF | N/A | No web-facing application |
| Rate Limiting | N/A | No web-facing application |
| Hosting | GitHub | Source repo + GitHub Releases |
| Database | N/A | No database -- static files only |
| Backup | Git | Repository is the canonical backup |
| Deploy | GitHub Actions | release.yml: tag-triggered GitHub Release |
| Health | N/A | No server process to monitor |

Notes:
- This project is a Claude Code plugin/skill (static files: markdown, bash, YAML, JSON)
- Distribution is via Git clone or copying files into ~/.claude/plugins/
- The only "deploy" is creating a GitHub Release when a version tag is pushed

## When In Doubt

- Ask
- Leave it better than you found it
- Ship, learn, iterate
