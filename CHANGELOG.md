# Changelog

All notable changes to the Apex Spec System are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.0.13-codex] - 2026-03-09

### Added
- Apex Infinite CLI ported to Codex CLI (Phase 04 complete)
- Codex agent configuration section in config.yaml (binary, exec_flags, model_reasoning_effort)
- 54-test pytest suite for prompt generation and system prompt validation
- Test infrastructure (conftest.py, tests/ directory)

### Changed
- apex_infinite.py: All Claude Code references replaced with Codex CLI equivalents
- Subprocess execution: claude -> codex exec with configurable flags
- Prompt generation: ULTRATHINK pattern replaced with natural language skill invocation
- MANAGER_SYSTEM_PROMPT and SUMMARIZER_SYSTEM_PROMPT rewritten for Codex CLI
- Variable names: cc_response -> agent_response, build_claude_prompt -> build_codex_prompt
- CLI version bumped to 2.0.0, help text updated
- README-apex-infinite-cli.md updated for Codex CLI usage
- COMMAND_ALIASES cleared (Codex skill uses canonical command names)

### Removed
- CLAUDECODE environment variable handling (not needed for Codex CLI)
- implement -> implementation alias (Codex skill uses canonical /implement)

## [2.0.10-codex] - 2026-03-09

### Added
- Skills Catalog submission (PR #244 to openai/skills .experimental catalog)
- Method 4 installation via $skill-installer from catalog
- Catalog-specific README for submission package

### Changed
- README.md updated with Method 4 installation and Phase 03 status

## [2.0.8-codex] - 2026-03-09

### Added
- CHANGELOG.md covering Phases 00-02
- Enhanced release workflow with pre-release verification checks
  (ASCII encoding, version sync, file inventory, script executability)
- Codex CLI installation instructions in release notes
- Annotated tag v2.0.8-codex with automated GitHub Release

---

## Phase 04 - Apex Infinite CLI (Codex Port)

### Session 03: Config, README, and Validation
- Updated architecture diagram and documentation to Codex CLI
- Usage examples, CLI flags, config docs, .env.example updated
- 54-test suite passed, dry-run validated, ASCII/LF verified
- Tagged as v1.1.0 (apex-infinite-cli version)

### Session 02: System Prompt Rewrite and Testing
- Rewrote MANAGER_SYSTEM_PROMPT (18 Claude Code references replaced)
- Updated SUMMARIZER_SYSTEM_PROMPT with agent-neutral language
- Updated llm_manager_decide() user-message template
- Created 54-test pytest suite across 5 test classes
- Removed all slash-command syntax from system prompts

### Session 01: Core Subprocess and Prompt Conversion
- Added codex configuration section to config.yaml
- Renamed build_claude_prompt -> build_codex_prompt with new prompt pattern
- Renamed execute_claude -> execute_codex using codex exec subprocess
- Added get_agent_config() for configurable binary and flags
- Renamed cc_response -> agent_response throughout
- Updated CLI version, help text, module docstrings

---

## Phase 03 - Distribution

### Session 02: Catalog Submission
- Forked openai/skills and submitted PR #244 (skills/.experimental/apex-spec/)
- Created catalog-specific README and LICENSE.txt for submission package
- Validated 33-file submission (SKILL.md, 26 references, 3 scripts, openai.yaml)
- Added Method 4 (Skills Catalog) installation to README.md
- Updated Phase 03 status to Complete

### Session 01: Release Workflow and Tagging
- Created CHANGELOG.md with phase-by-phase history
- Enhanced release.yml with 4 verification steps (ASCII, version sync, file inventory, executability)
- Rewrote release body template for Codex CLI audience
- Tagged v2.0.8-codex and published GitHub Release

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
