#!/usr/bin/env bash
# Check local Ollama connectivity and configured model availability.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

PYTHON_BIN="${PYTHON:-python3}"
CONFIG_PATH="${APEX_INFINITE_CONFIG:-${CLI_DIR}/src/apex_infinite/config.yaml}"
MODEL_OVERRIDE=""
CHAT_CHECK=0

usage() {
    cat <<'EOF'
Usage: check-ollama.sh [options]

Options:
  --config PATH       Config file path (default: packaged config.yaml)
  --host HOST         Override OLLAMA_HOST for this check
  --port PORT         Override OLLAMA_PORT for this check
  --api-key KEY       Override OLLAMA_API_KEY for this check
  --model MODEL       Override the configured Ollama model
  --chat              Also run a tiny chat completion
  --python PYTHON     Python executable (default: $PYTHON or python3)
  -h, --help          Show this help
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --config)
            CONFIG_PATH="${2:?missing value for --config}"
            shift 2
            ;;
        --host)
            export OLLAMA_HOST="${2:?missing value for --host}"
            shift 2
            ;;
        --port)
            export OLLAMA_PORT="${2:?missing value for --port}"
            shift 2
            ;;
        --api-key)
            export OLLAMA_API_KEY="${2:?missing value for --api-key}"
            shift 2
            ;;
        --model)
            MODEL_OVERRIDE="${2:?missing value for --model}"
            shift 2
            ;;
        --chat)
            CHAT_CHECK=1
            shift
            ;;
        --python)
            PYTHON_BIN="${2:?missing value for --python}"
            shift 2
            ;;
        -h | --help)
            usage
            exit 0
            ;;
        *)
            printf 'Unknown option: %s\n' "$1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

cmd=(
    env
    "PYTHONPATH=${CLI_DIR}/src${PYTHONPATH:+:${PYTHONPATH}}"
    "$PYTHON_BIN"
    -m apex_infinite
    --config "$CONFIG_PATH"
    --provider ollama
    --check-provider
    --plain
)

if [[ -n "$MODEL_OVERRIDE" ]]; then
    cmd+=(--model "$MODEL_OVERRIDE")
fi

if [[ "$CHAT_CHECK" == "1" ]]; then
    cmd+=(--check-provider-chat)
fi

exec "${cmd[@]}"
