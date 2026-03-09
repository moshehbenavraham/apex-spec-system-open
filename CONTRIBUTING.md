# Contributing

## Prerequisites

- bash 4.0+
- git
- jq
- shellcheck (for linting scripts)
- shfmt (for formatting scripts)

## Setup

```bash
git clone https://github.com/aiwithapex/apex-spec-system-open.git
cd apex-spec-system-open
```

No build step required -- the skill is plain files (markdown, YAML, bash, JSON).

## Branch Conventions

- `master` - Production-ready code
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation changes

## Commit Style

Use conventional commits in imperative mood:

- `feat:` New feature (e.g., `feat: Add validate reference file`)
- `fix:` Bug fix (e.g., `fix: Correct script path resolution in initspec`)
- `docs:` Documentation (e.g., `docs: Update README for Codex CLI`)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## Making Changes

### Reference Files (references/*.md)

1. No YAML frontmatter -- the orchestrator SKILL.md handles routing
2. First line must be a level-1 heading: `# Command Name`
3. Use platform-neutral language ("Read the file" not "Use the Read tool")
4. Keep under 500 lines
5. Update the dispatch table in SKILL.md if adding a new command

### Scripts (scripts/*.sh)

1. Start with `#!/usr/bin/env bash` and `set -euo pipefail`
2. Source common.sh for shared functions
3. Test on macOS, Ubuntu/Debian, and WSL2
4. Only bash, git, jq, and standard coreutils as dependencies

### Encoding (Non-Negotiable)

- ASCII-only characters (code points 0-127)
- No Unicode, emoji, smart quotes, or em-dashes
- Unix LF line endings (no CRLF)
- Validate: `LC_ALL=C grep -n '[^[:print:][:space:]]' file`

## Pull Request Process

1. Create feature branch from `master`
2. Make changes with clear, atomic commits
3. Run shellcheck and shfmt on any modified scripts
4. Verify ASCII encoding on all changed files
5. Open PR with description of what and why
6. Address review feedback

## Code Review Norms

- Review within 24 hours
- Be constructive and specific
- Verify encoding and line endings on new files

## Version Updates

When bumping the version, update both files:

- `README.md` (version badge/line)
- `SKILL.md` (frontmatter `version:` field)

## Project Structure

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full skill structure
and design rationale.
