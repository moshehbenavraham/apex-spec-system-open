#!/usr/bin/env bash
# test_helper.bash - Shared setup for bats tests

# Load bats helpers (search multiple paths for cross-platform support)
_bats_lib=""
for _candidate in /usr/local/lib/bats /usr/lib/bats; do
    if [[ -d "${_candidate}/bats-support" ]]; then
        _bats_lib="${_candidate}"
        break
    fi
done
if [[ -z "${_bats_lib}" ]]; then
    echo "ERROR: bats-support not found in /usr/local/lib/bats or /usr/lib/bats" >&2
    exit 1
fi
load "${_bats_lib}/bats-support/load"
load "${_bats_lib}/bats-assert/load"
unset _bats_lib _candidate

# Project root (parent of tests/)
PROJECT_ROOT="$(cd "$(dirname "${BATS_TEST_FILENAME}")/.." && pwd)"
# shellcheck disable=SC2034  # used by bats test files that load this helper
SCRIPTS_DIR="${PROJECT_ROOT}/scripts"

# Create a temporary spec system for each test
setup_spec_system() {
    TEST_SPEC_DIR="$(mktemp -d)"
    mkdir -p "${TEST_SPEC_DIR}/.spec_system"
    cat > "${TEST_SPEC_DIR}/.spec_system/state.json" <<'EOF'
{
  "version": "2.0",
  "project_name": "test-project",
  "current_phase": 1,
  "current_session": null,
  "monorepo": false,
  "phases": {
    "0": {
      "name": "Foundation",
      "status": "complete",
      "session_count": 2
    },
    "1": {
      "name": "Features",
      "status": "in_progress",
      "session_count": 3
    }
  },
  "completed_sessions": [
    "phase00-session01-setup",
    "phase00-session02-core"
  ],
  "next_session_history": []
}
EOF
}

teardown_spec_system() {
    if [[ -n "${TEST_SPEC_DIR:-}" && -d "${TEST_SPEC_DIR}" ]]; then
        rm -rf "${TEST_SPEC_DIR}"
    fi
}
