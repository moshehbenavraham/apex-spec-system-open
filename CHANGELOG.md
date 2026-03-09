# Changelog

All notable changes to the Apex Spec System are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.0.8-codex] - 2026-03-09

### Added
- CHANGELOG.md covering Phases 00-02
- Enhanced release workflow with pre-release verification checks
- Codex CLI installation instructions in release notes

## [Unreleased]

Phase 03 (Distribution) work in progress.

---

## Phase 02 - Documentation and Polish

### Session 02: Regression and Release Prep
- Full regression pass across all 22 commands and 26 reference files
- Release workflow (release.yml) with tag-triggered GitHub Releases
- Dependabot configuration for dependency updates
- Integration CI workflow: cross-platform tests, reference integrity checks
- All CI/CD bundles marked configured (Quality, Build, Security, Integration, Operations)

### Session 01: Documentation and References
- Finalized public-facing documentation (README.md, CONTRIBUTING.md)
- Architecture documentation (docs/ARCHITECTURE.md)
- Development guide (docs/development.md)
- Onboarding checklist (docs/onboarding.md)
- Deployment guide (docs/deployment.md)
- Guidance, walkthrough, and workflow-overview reference files
- Security CI workflow: gitleaks, sensitive file detection, script pattern checks

---

## Phase 01 - Full Command Migration

### Session 03: Complex Utilities and Regression
- Converted 4 complex utility commands to platform-neutral references
  (qimpl, qfrontdev, qbackenddev, sculpt-ui)
- Full regression across all converted commands

### Session 02: Transition and Simple Utilities
- Converted 10 command files to platform-neutral references
  (copush, dockbuild, dockcleanbuild, up2imp, pullndoc, audit, pipeline,
  infra, carryforward, documents)

### Session 01: Workflow Completion
- Converted 7 remaining workflow files to platform-neutral references
  (createprd, createuxprd, phasebuild, validate, updateprd, implement,
  plansession)
- Build & Test CI workflow for script validation

---

## Phase 00 - Proof of Concept

### Session 02: Core Command Conversion
- Converted 4 core commands to platform-neutral reference files
  (initspec, createprd, plansession, implement)
- Code Quality CI workflow with shellcheck and ASCII enforcement
- Fixed shellcheck warnings and shfmt formatting in scripts

### Session 01: Skill Structure and Orchestrator
- Created SKILL.md root orchestrator with 22-command dispatch table
- Created agents/openai.yaml for Codex CLI UI metadata
- Established references/ directory with command reference file pattern
- Created scripts/ directory (analyze-project.sh, check-prereqs.sh, common.sh)
- Initial project structure following Agent Skills standard

---

## Pre-Codex

### [1.6.12-beta]
- Original Claude Code plugin implementation
- Source files preserved in commands/ directory (archive)
