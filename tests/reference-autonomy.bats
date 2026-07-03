#!/usr/bin/env bats
# Tests for autonomous command-reference handoffs

load test_helper

COMMAND_REFERENCES=(
    "references/initspec.md"
    "references/createprd.md"
    "references/createuxprd.md"
    "references/phasebuild.md"
    "references/plansession.md"
    "references/implement.md"
    "references/creview.md"
    "references/validate.md"
    "references/updateprd.md"
    "references/audit.md"
    "references/pipeline.md"
    "references/infra.md"
    "references/carryforward.md"
    "references/documents.md"
    "references/copush.md"
    "references/sculpt-ui.md"
    "references/seshsplit.md"
    "references/dockbuild.md"
    "references/dockcleanbuild.md"
    "references/up2imp.md"
    "references/qimpl.md"
    "references/qfrontdev.md"
    "references/qbackenddev.md"
    "references/pullndoc.md"
)

@test "all command references include a Next command handoff" {
    cd "${PROJECT_ROOT}"

    local ref
    for ref in "${COMMAND_REFERENCES[@]}"; do
        run grep -q 'Next command:' "$ref"
        assert_success "$ref is missing a literal Next command: handoff"
    done
}

@test "workflow docs do not contain interactive handoff phrases" {
    cd "${PROJECT_ROOT}"

    run grep -RniE 'ask the user|prompt user|prompt the user|User Action|manual testing|manual response|manual review|human review gate' \
        SKILL.md README.md AGENTS.md references docs/CONVENTIONS.md
    assert_failure "interactive handoff phrase found: $output"
}
