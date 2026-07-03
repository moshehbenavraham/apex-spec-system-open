# Environments

The Apex Spec System is a plain-files skill and Codex plugin wrapper. The
runtime environments below describe where the files are validated and consumed;
there is no hosted application environment.

| Environment | Location | Purpose | Verification |
|-------------|----------|---------|--------------|
| Local development | Repository checkout | Edit skill files, scripts, and docs | `bats tests/`, `bash scripts/sync-plugin-payload.sh --check` |
| GitHub Actions | `.github/workflows/` | Validate shell scripts, reference integrity, plugin payload sync, release inventory, and secrets patterns | Push, pull request, scheduled security, and tag workflows |
| Installed skill | Agent skills directory or Codex plugin install | Consume `SKILL.md`, `references/`, `scripts/`, and `agents/openai.yaml` | `ls ~/.agents/skills/apex-spec/SKILL.md` or plugin install verification |

## Environment Variables

| Variable | Used By | Purpose | Required |
|----------|---------|---------|----------|
| `NO_COLOR` | Terminal tools | Disables color for tools that honor the convention | Optional |
| `TERM=dumb` | Terminal tools | Signals a constrained terminal environment | Optional |

## Local Data

The Apex Spec skill itself stores project state inside `.spec_system/` in each
initialized project. Do not commit provider keys, local `.env` files, or
operator-local history from companion tools.

## Deployment Notes

The base skill has no server, database, or cloud runtime. Release distribution
is described in [Deployment](deployment.md).
