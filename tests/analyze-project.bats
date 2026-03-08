#!/usr/bin/env bats
# Tests for scripts/analyze-project.sh

load test_helper

setup() {
    setup_spec_system
    export SPEC_SYSTEM_DIR="${TEST_SPEC_DIR}/.spec_system"
    export STATE_FILE="${SPEC_SYSTEM_DIR}/state.json"
    export SPECS_DIR="${SPEC_SYSTEM_DIR}/specs"
}

teardown() {
    teardown_spec_system
}

# ---------------------------------------------------------------------------
# Help / usage
# ---------------------------------------------------------------------------

@test "analyze-project.sh --help shows usage" {
    run bash "${SCRIPTS_DIR}/analyze-project.sh" --help
    assert_success
    assert_output --partial "Usage:"
    assert_output --partial "--json"
}

# ---------------------------------------------------------------------------
# Human-readable output
# ---------------------------------------------------------------------------

@test "analyze-project.sh produces human output" {
    cd "${TEST_SPEC_DIR}"
    run bash "${SCRIPTS_DIR}/analyze-project.sh"
    assert_success
    assert_output --partial "PROJECT ANALYSIS SUMMARY"
    assert_output --partial "test-project"
}

# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

@test "analyze-project.sh --json produces valid JSON" {
    cd "${TEST_SPEC_DIR}"
    run bash "${SCRIPTS_DIR}/analyze-project.sh" --json
    assert_success
    # Validate it is parseable JSON
    echo "$output" | jq empty
}

@test "analyze-project.sh --json contains expected fields" {
    cd "${TEST_SPEC_DIR}"
    output=$(bash "${SCRIPTS_DIR}/analyze-project.sh" --json)
    project=$(echo "$output" | jq -r '.project')
    assert_equal "$project" "test-project"

    phase=$(echo "$output" | jq '.current_phase')
    assert_equal "$phase" "1"

    count=$(echo "$output" | jq '.completed_sessions_count')
    assert_equal "$count" "2"

    monorepo=$(echo "$output" | jq '.monorepo')
    assert_equal "$monorepo" "false"
}

@test "analyze-project.sh --json lists completed sessions" {
    cd "${TEST_SPEC_DIR}"
    output=$(bash "${SCRIPTS_DIR}/analyze-project.sh" --json)
    sessions=$(echo "$output" | jq -r '.completed_sessions[]')
    echo "$sessions" | grep -q "phase00-session01-setup"
    echo "$sessions" | grep -q "phase00-session02-core"
}

@test "analyze-project.sh --json lists phases" {
    cd "${TEST_SPEC_DIR}"
    output=$(bash "${SCRIPTS_DIR}/analyze-project.sh" --json)
    phase_count=$(echo "$output" | jq '.phases | length')
    assert_equal "$phase_count" "2"
}

# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

@test "analyze-project.sh fails without spec system" {
    local empty_dir
    empty_dir="$(mktemp -d)"
    cd "${empty_dir}"
    unset SPEC_SYSTEM_DIR STATE_FILE SPECS_DIR
    run bash "${SCRIPTS_DIR}/analyze-project.sh"
    assert_failure
    rm -rf "${empty_dir}"
}

@test "analyze-project.sh rejects unknown options" {
    cd "${TEST_SPEC_DIR}"
    run bash "${SCRIPTS_DIR}/analyze-project.sh" --badopt
    assert_failure
}
