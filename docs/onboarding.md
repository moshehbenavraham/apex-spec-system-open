# Onboarding

Zero-to-hero checklist for using and contributing to the Apex Spec System.

## Prerequisites

- [ ] bash 4.0+ installed (pre-installed on macOS/Linux)
- [ ] git installed (pre-installed or `apt install git`)
- [ ] jq installed (`apt install jq` or `brew install jq`)
- [ ] shellcheck installed (`apt install shellcheck` or `brew install shellcheck`) -- for contributing only
- [ ] shfmt installed (`go install mvdan.cc/sh/v3/cmd/shfmt@latest` or `brew install shfmt`) -- for contributing only

Verify with: `bash scripts/check-prereqs.sh --env`

## Using the Skill

### 1. Install

```bash
git clone https://github.com/aiwithapex/apex-spec-system-open.git \
  ~/.agents/skills/apex-spec
```

### 2. Initialize in Your Project

```bash
cd your-project
# Invoke the skill and request initialization
$apex-spec initspec
```

This creates a `.spec_system/` directory with state tracking, scripts, and conventions.

### 3. Follow the Workflow

```
initspec -> createprd -> phasebuild -> plansession -> implement -> validate -> updateprd
```

See [references/workflow-overview.md](../references/workflow-overview.md) for the full command reference.

## Contributing

### 1. Clone the Repository

```bash
git clone https://github.com/aiwithapex/apex-spec-system-open.git
cd apex-spec-system-open
```

### 2. Verify Setup

```bash
bash scripts/analyze-project.sh --json | jq .
bash scripts/check-prereqs.sh --json --env | jq .
shellcheck scripts/*.sh
```

### 3. Understand the Layout

| Directory | Purpose |
|-----------|---------|
| SKILL.md | Root orchestrator (entry point) |
| references/ | Command and supporting reference files |
| scripts/ | Bash utilities |
| apex-infinite-cli/ | Autonomous session manager (Python CLI) |
| docs/ | Development documentation |

### 4. Make Changes

See [development.md](development.md) for the full development guide and
[CONTRIBUTING.md](../CONTRIBUTING.md) for branch conventions and PR process.

## Common Issues

### jq not found
**Solution**: Install jq (`apt install jq` or `brew install jq`)

### shellcheck warnings on scripts
**Solution**: Run `shellcheck scripts/*.sh` and address warnings before committing

### Non-ASCII characters in files
**Solution**: Check with `LC_ALL=C grep -n '[^[:print:][:space:]]' <file>` and replace offending characters with ASCII equivalents
