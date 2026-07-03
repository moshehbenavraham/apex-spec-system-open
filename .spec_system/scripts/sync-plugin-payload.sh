#!/usr/bin/env bash
# =============================================================================
# sync-plugin-payload.sh - Rebuild the Codex plugin skill payload from root
# =============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_ROOT="${ROOT_DIR}/plugins/apex-spec"
PLUGIN_SKILL_DIR="${PLUGIN_ROOT}/skills/apex-spec"

usage() {
    cat <<'EOF'
Usage:
  bash scripts/sync-plugin-payload.sh
  bash scripts/sync-plugin-payload.sh --check

Rebuild or verify the generated Codex plugin skill payload from the canonical
repo-root skill files.
EOF
}

die() {
    printf 'error: %s\n' "$*" >&2
    exit 1
}

require_file() {
    local file="$1"
    [[ -f "$file" ]] || die "Missing required file: ${file#"$ROOT_DIR"/}"
}

require_dir() {
    local dir="$1"
    [[ -d "$dir" ]] || die "Missing required directory: ${dir#"$ROOT_DIR"/}"
}

require_repo_layout() {
    case "$PLUGIN_SKILL_DIR" in
        "$ROOT_DIR"/plugins/apex-spec/skills/apex-spec) ;;
        *) die "Refusing unexpected plugin skill path: $PLUGIN_SKILL_DIR" ;;
    esac

    require_file "${ROOT_DIR}/SKILL.md"
    require_dir "${ROOT_DIR}/references"
    require_dir "${ROOT_DIR}/scripts"
    require_file "${ROOT_DIR}/agents/openai.yaml"
    require_file "${PLUGIN_ROOT}/.codex-plugin/plugin.json"
}

compare_file() {
    local src="$1"
    local dst="$2"
    local label="$3"

    if [[ ! -f "$dst" ]]; then
        printf 'stale: missing %s\n' "$label" >&2
        return 1
    fi

    if ! cmp -s -- "$src" "$dst"; then
        printf 'stale: %s differs\n' "$label" >&2
        return 1
    fi
}

compare_dir() {
    local src="$1"
    local dst="$2"
    local label="$3"

    if [[ ! -d "$dst" ]]; then
        printf 'stale: missing %s\n' "$label" >&2
        return 1
    fi

    if ! diff -qr -- "$src" "$dst"; then
        printf 'stale: %s differs\n' "$label" >&2
        return 1
    fi
}

verify_payload() {
    local failed=0

    compare_file "${ROOT_DIR}/SKILL.md" "${PLUGIN_SKILL_DIR}/SKILL.md" "SKILL.md" || failed=1
    compare_file "${ROOT_DIR}/agents/openai.yaml" "${PLUGIN_SKILL_DIR}/agents/openai.yaml" "agents/openai.yaml" || failed=1
    compare_dir "${ROOT_DIR}/references" "${PLUGIN_SKILL_DIR}/references" "references/" || failed=1
    compare_dir "${ROOT_DIR}/scripts" "${PLUGIN_SKILL_DIR}/scripts" "scripts/" || failed=1

    return "$failed"
}

sync_payload() {
    mkdir -p "${PLUGIN_SKILL_DIR}/agents"

    rm -f -- "${PLUGIN_SKILL_DIR}/SKILL.md"
    rm -rf -- "${PLUGIN_SKILL_DIR}/references" "${PLUGIN_SKILL_DIR}/scripts"
    rm -f -- "${PLUGIN_SKILL_DIR}/agents/openai.yaml"

    cp -p -- "${ROOT_DIR}/SKILL.md" "${PLUGIN_SKILL_DIR}/SKILL.md"
    cp -pR -- "${ROOT_DIR}/references" "${PLUGIN_SKILL_DIR}/references"
    cp -pR -- "${ROOT_DIR}/scripts" "${PLUGIN_SKILL_DIR}/scripts"
    cp -p -- "${ROOT_DIR}/agents/openai.yaml" "${PLUGIN_SKILL_DIR}/agents/openai.yaml"
}

main() {
    local mode="sync"

    case "${1:-}" in
        "") ;;
        --check)
            mode="check"
            ;;
        -h | --help)
            usage
            exit 0
            ;;
        *)
            usage >&2
            exit 2
            ;;
    esac

    if [[ "$#" -gt 1 ]]; then
        usage >&2
        exit 2
    fi

    require_repo_layout

    if [[ "$mode" == "check" ]]; then
        if verify_payload; then
            printf 'Plugin payload is current.\n'
            return 0
        fi
        printf 'Plugin payload is stale. Run: bash scripts/sync-plugin-payload.sh\n' >&2
        return 1
    fi

    sync_payload

    if ! verify_payload; then
        die "Plugin payload sync failed verification."
    fi

    cat <<EOF
Synced plugin skill payload from root canonical files.
- SKILL.md -> plugins/apex-spec/skills/apex-spec/SKILL.md
- references/ -> plugins/apex-spec/skills/apex-spec/references/
- scripts/ -> plugins/apex-spec/skills/apex-spec/scripts/
- agents/openai.yaml -> plugins/apex-spec/skills/apex-spec/agents/openai.yaml
EOF
}

main "$@"
