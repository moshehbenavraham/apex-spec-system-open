# Deployment

## Overview

The Apex Spec System is a plain-files skill (markdown, YAML, bash, JSON). There
is no build step, compilation, or artifact generation. Deployment means
distributing these files to the user's agent skills directory.

## Installation Methods

### Method 1: Git Clone (Recommended)

```bash
git clone https://github.com/aiwithapex/apex-spec-system-open.git \
  ~/.agents/skills/apex-spec
```

### Method 2: Skill Installer

```bash
codex install-skill https://github.com/aiwithapex/apex-spec-system-open.git
```

### Method 3: Manual Download

```bash
mkdir -p ~/.agents/skills/apex-spec
curl -L https://github.com/aiwithapex/apex-spec-system-open/archive/refs/heads/master.tar.gz \
  | tar xz --strip-components=1 -C ~/.agents/skills/apex-spec
```

### Method 4: Skills Catalog (Experimental)

Install from the [openai/skills](https://github.com/openai/skills) catalog
using the skill installer inside Codex:

```
$skill-installer install the apex-spec skill from the .experimental folder
```

### Verify Installation

```bash
ls ~/.agents/skills/apex-spec/SKILL.md
```

## CI/CD Pipeline

```
Push --> Quality (shellcheck, shfmt, encoding) --> Tests (bats) --> Security (audit)
```

### Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| quality.yml | Push, PR | Shellcheck, shfmt, ASCII encoding checks |
| test.yml | Push, PR | Bats tests for scripts |
| integration.yml | Push, PR | Cross-platform tests, reference integrity |
| security.yml | Push, PR | Security audit |
| release.yml | Tag | Release automation |

## Release Process

1. Update version in `SKILL.md` (frontmatter) and `README.md`
2. Commit with `chore: bump version to X.Y.Z`
3. Tag the release: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
4. Push tag: `git push origin vX.Y.Z`
5. release.yml workflow runs automatically:
   - Verify ASCII encoding (no non-ASCII in core files)
   - Verify version sync (SKILL.md and README.md match tag)
   - Verify file inventory (26+ references, 3 scripts, all executable)
   - Create GitHub Release with installation instructions

## Updating an Existing Installation

```bash
cd ~/.agents/skills/apex-spec
git pull origin master
```

For projects already using the skill, re-run the initspec workflow to update
`.spec_system/scripts/` with the latest versions.
