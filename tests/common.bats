#!/usr/bin/env bats
# Tests for scripts/common.sh

load test_helper

setup() {
    setup_spec_system
    # Override SPEC_SYSTEM_DIR so common.sh functions use the test fixture
    export SPEC_SYSTEM_DIR="${TEST_SPEC_DIR}/.spec_system"
    export STATE_FILE="${SPEC_SYSTEM_DIR}/state.json"
    export SPECS_DIR="${SPEC_SYSTEM_DIR}/specs"
}

teardown() {
    teardown_spec_system
}

# ---------------------------------------------------------------------------
# Sourcing
# ---------------------------------------------------------------------------

@test "common.sh sources without error" {
    source "${SCRIPTS_DIR}/common.sh"
}

@test "common.sh --help prints usage" {
    run bash "${SCRIPTS_DIR}/common.sh"
    assert_success
    assert_output --partial "Apex Spec System"
}

# ---------------------------------------------------------------------------
# String helpers
# ---------------------------------------------------------------------------

@test "trim removes leading and trailing whitespace" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(trim "  hello world  ")
    assert_equal "$result" "hello world"
}

@test "trim handles empty string" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(trim "")
    assert_equal "$result" ""
}

# ---------------------------------------------------------------------------
# JSON operations
# ---------------------------------------------------------------------------

@test "json_get reads a string value" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(json_get "$STATE_FILE" '.project_name')
    assert_equal "$result" "test-project"
}

@test "json_get reads a numeric value" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(json_get "$STATE_FILE" '.current_phase')
    assert_equal "$result" "1"
}

@test "json_get reads null as literal string" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(json_get "$STATE_FILE" '.current_session')
    assert_equal "$result" "null"
}

@test "json_set updates a value" {
    source "${SCRIPTS_DIR}/common.sh"
    json_set "$STATE_FILE" '.current_session' '"phase01-session01-test"'
    result=$(json_get "$STATE_FILE" '.current_session')
    assert_equal "$result" "phase01-session01-test"
}

@test "validate_json accepts valid JSON" {
    source "${SCRIPTS_DIR}/common.sh"
    run validate_json "$STATE_FILE"
    assert_success
}

@test "validate_json rejects invalid JSON" {
    source "${SCRIPTS_DIR}/common.sh"
    local bad_file="${TEST_SPEC_DIR}/bad.json"
    echo "not json" > "$bad_file"
    run validate_json "$bad_file"
    assert_failure
}

# ---------------------------------------------------------------------------
# Session ID parsing
# ---------------------------------------------------------------------------

@test "parse_session_id extracts phase number" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_phase_from_session_id "phase01-session03-feature-work")
    assert_equal "$result" "01"
}

@test "parse_session_id extracts session number" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_session_number_from_id "phase01-session03-feature-work")
    assert_equal "$result" "03"
}

@test "parse_session_id extracts suffix" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_session_suffix_from_id "phase01-session03b-refinements")
    assert_equal "$result" "b"
}

@test "parse_session_id extracts name" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_session_name_from_id "phase01-session03-feature-work")
    assert_equal "$result" "feature-work"
}

@test "parse_session_id rejects invalid format" {
    source "${SCRIPTS_DIR}/common.sh"
    run parse_session_id "invalid-format" "" "" "" ""
    assert_failure
}

@test "build_session_id creates correct format" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(build_session_id 1 3 "feature-work")
    assert_equal "$result" "phase01-session03-feature-work"
}

@test "build_session_ref creates correct format" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(build_session_ref 1 3)
    assert_equal "$result" "S0103"
}

# ---------------------------------------------------------------------------
# State queries
# ---------------------------------------------------------------------------

@test "get_project_name returns project name" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_project_name)
    assert_equal "$result" "test-project"
}

@test "get_current_phase returns phase number" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_current_phase)
    assert_equal "$result" "1"
}

@test "get_completed_sessions lists sessions" {
    source "${SCRIPTS_DIR}/common.sh"
    run get_completed_sessions
    assert_success
    assert_output --partial "phase00-session01-setup"
    assert_output --partial "phase00-session02-core"
}

@test "get_completed_sessions_count returns count" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_completed_sessions_count)
    assert_equal "$result" "2"
}

@test "is_session_completed returns true for completed session" {
    source "${SCRIPTS_DIR}/common.sh"
    run is_session_completed "phase00-session01-setup"
    assert_success
}

@test "is_session_completed returns false for incomplete session" {
    source "${SCRIPTS_DIR}/common.sh"
    run is_session_completed "phase01-session01-new"
    assert_failure
}

@test "get_phase_status returns correct status" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_phase_status "0")
    assert_equal "$result" "complete"
    result=$(get_phase_status "1")
    assert_equal "$result" "in_progress"
}

# ---------------------------------------------------------------------------
# State updates
# ---------------------------------------------------------------------------

@test "set_current_session updates state" {
    source "${SCRIPTS_DIR}/common.sh"
    set_current_session "phase01-session01-test"
    result=$(get_current_session)
    assert_equal "$result" "phase01-session01-test"
}

@test "clear_current_session sets null" {
    source "${SCRIPTS_DIR}/common.sh"
    set_current_session "phase01-session01-test"
    clear_current_session
    result=$(get_current_session)
    assert_equal "$result" "null"
}

@test "add_completed_session appends to list" {
    source "${SCRIPTS_DIR}/common.sh"
    add_completed_session "phase01-session01-new"
    result=$(get_completed_sessions_count)
    assert_equal "$result" "3"
    run is_session_completed "phase01-session01-new"
    assert_success
}

# ---------------------------------------------------------------------------
# Monorepo queries
# ---------------------------------------------------------------------------

@test "get_monorepo_flag returns false for single repo" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_monorepo_flag)
    assert_equal "$result" "false"
}

@test "get_packages returns empty array for single repo" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_packages)
    assert_equal "$result" "[]"
}

# ---------------------------------------------------------------------------
# File validation
# ---------------------------------------------------------------------------

@test "validate_ascii accepts ASCII file" {
    source "${SCRIPTS_DIR}/common.sh"
    local ascii_file="${TEST_SPEC_DIR}/ascii.txt"
    printf 'Hello world\n' > "$ascii_file"
    run validate_ascii "$ascii_file"
    assert_success
}

@test "validate_ascii rejects file with CRLF" {
    source "${SCRIPTS_DIR}/common.sh"
    local crlf_file="${TEST_SPEC_DIR}/crlf.txt"
    printf 'Hello\r\nworld\r\n' > "$crlf_file"
    run validate_ascii "$crlf_file"
    assert_failure
}

# ---------------------------------------------------------------------------
# Directory operations
# ---------------------------------------------------------------------------

@test "ensure_dir creates missing directory" {
    source "${SCRIPTS_DIR}/common.sh"
    local new_dir="${TEST_SPEC_DIR}/new/nested/dir"
    ensure_dir "$new_dir"
    [ -d "$new_dir" ]
}

@test "get_session_dir returns correct path" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_session_dir "phase01-session01-test")
    assert_equal "$result" "${SPECS_DIR}/phase01-session01-test"
}

# ---------------------------------------------------------------------------
# Date utilities
# ---------------------------------------------------------------------------

@test "get_date returns YYYY-MM-DD format" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_date)
    [[ "$result" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]
}

@test "get_datetime returns YYYY-MM-DD HH:MM:SS format" {
    source "${SCRIPTS_DIR}/common.sh"
    result=$(get_datetime)
    [[ "$result" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\ [0-9]{2}:[0-9]{2}:[0-9]{2}$ ]]
}

# ---------------------------------------------------------------------------
# Initialization check
# ---------------------------------------------------------------------------

@test "check_spec_system passes with valid setup" {
    source "${SCRIPTS_DIR}/common.sh"
    run check_spec_system
    assert_success
}

@test "check_spec_system fails when directory missing" {
    source "${SCRIPTS_DIR}/common.sh"
    SPEC_SYSTEM_DIR="${TEST_SPEC_DIR}/nonexistent"
    run check_spec_system
    assert_failure
}
