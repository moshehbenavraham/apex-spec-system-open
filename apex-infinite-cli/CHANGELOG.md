# Changelog

All notable changes to Apex Infinite CLI are documented in this file.

Format follows Keep a Changelog.

## [Unreleased]

### Changed
- Converted the project into a self-contained Python package with CLI-local
  `pyproject.toml`, `src/` layout, console scripts, and package data.
- Moved the base CLI runtime into `src/apex_infinite/` and the optional visual
  wrapper into `src/apex_infinite_visual/`.
- Made `apex-infinite` and `apex-infinite-visual` the documented entry points.
- Replaced parent-root Python tooling assumptions with CLI-local pytest,
  coverage, black, pylint, and mypy configuration.
- Kept `requirements*.txt` as compatibility shims that install the package and
  optional extras from `pyproject.toml`.

## [2.0.0] - 2026-03-09

### Changed
- Ported the autonomous session manager to Codex CLI.
- Replaced Claude-specific subprocess and prompt handling with Codex CLI
  equivalents.
- Added provider configuration, prompt-routing tests, and Codex skill
  invocation prompts.
