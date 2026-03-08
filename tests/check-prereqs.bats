#!/usr/bin/env bats
# Tests for scripts/check-prereqs.sh

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

@test "check-prereqs.sh --help shows usage" {
    run bash "${SCRIPTS_DIR}/check-prereqs.sh" --help
    assert_success
    assert_output --partial "Usage:"
    assert_output --partial "--tools"
}

# ---------------------------------------------------------------------------
# Environment checks
# ---------------------------------------------------------------------------

@test "check-prereqs.sh --env passes in valid environment" {
    cd "${TEST_SPEC_DIR}"
    run bash "${SCRIPTS_DIR}/check-prereqs.sh" --env
    assert_success
    assert_output --partial "All prerequisites met"
}

@test "check-prereqs.sh --json --env produces valid JSON" {
    cd "${TEST_SPEC_DIR}"
    run bash "${SCRIPTS_DIR}/check-prereqs.sh" --json --env
    assert_success
    echo "$output" | jq empty
}

@test "check-prereqs.sh --json --env reports pass overall" {
    cd "${TEST_SPEC_DIR}"
    output=$(bash "${SCRIPTS_DIR}/check-prereqs.sh" --json --env)
    overall=$(echo "$output" | jq -r '.overall')
    assert_equal "$overall" "pass"
}

@test "check-prereqs.sh --json --env detects spec system" {
    cd "${TEST_SPEC_DIR}"
    output=$(bash "${SCRIPTS_DIR}/check-prereqs.sh" --json --env)
    status=$(echo "$output" | jq -r '.environment.spec_system.status')
    assert_equal "$status" "pass"
}

@test "check-prereqs.sh --json --env detects jq" {
    cd "${TEST_SPEC_DIR}"
    output=$(bash "${SCRIPTS_DIR}/check-prereqs.sh" --json --env)
    status=$(echo "$output" | jq -r '.environment.jq.status')
    assert_equal "$status" "pass"
}

# ---------------------------------------------------------------------------
# Tool checks
# ---------------------------------------------------------------------------

@test "check-prereqs.sh detects installed tool (bash)" {
    cd "${TEST_SPEC_DIR}"
    run bash "${SCRIPTS_DIR}/check-prereqs.sh" --tools "bash"
    assert_success
}

@test "check-prereqs.sh detects missing tool" {
    cd "${TEST_SPEC_DIR}"
    run bash "${SCRIPTS_DIR}/check-prereqs.sh" --tools "nonexistent_tool_xyz_12345"
    assert_failure
}

@test "check-prereqs.sh --json reports tool status" {
    cd "${TEST_SPEC_DIR}"
    output=$(bash "${SCRIPTS_DIR}/check-prereqs.sh" --json --tools "bash" 2>/dev/null || true)
    status=$(echo "$output" | jq -r '.tools.bash.status')
    assert_equal "$status" "pass"
}

# ---------------------------------------------------------------------------
# File checks
# ---------------------------------------------------------------------------

@test "check-prereqs.sh detects existing file" {
    cd "${TEST_SPEC_DIR}"
    touch "${TEST_SPEC_DIR}/testfile.txt"
    run bash "${SCRIPTS_DIR}/check-prereqs.sh" --files "testfile.txt"
    assert_success
}

@test "check-prereqs.sh detects missing file" {
    cd "${TEST_SPEC_DIR}"
    run bash "${SCRIPTS_DIR}/check-prereqs.sh" --files "nonexistent.txt"
    assert_failure
}

# ---------------------------------------------------------------------------
# Session prerequisite checks
# ---------------------------------------------------------------------------

@test "check-prereqs.sh passes for completed prerequisite" {
    cd "${TEST_SPEC_DIR}"
    run bash "${SCRIPTS_DIR}/check-prereqs.sh" --prereqs "phase00-session01-setup"
    assert_success
}

@test "check-prereqs.sh fails for incomplete prerequisite" {
    cd "${TEST_SPEC_DIR}"
    run bash "${SCRIPTS_DIR}/check-prereqs.sh" --prereqs "phase01-session99-nonexistent"
    assert_failure
}

# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

@test "check-prereqs.sh rejects unknown options" {
    cd "${TEST_SPEC_DIR}"
    run bash "${SCRIPTS_DIR}/check-prereqs.sh" --badopt
    assert_failure
}
