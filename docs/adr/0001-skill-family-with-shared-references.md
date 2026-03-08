# 1. Skill Family with Shared References

**Status:** Accepted
**Date:** 2026-03-08

## Context

The Apex Spec System has 22 commands. When porting from a Claude Code plugin
to a Codex CLI Agent Skill, we needed to decide how to structure the skill
directory so that all 22 commands are accessible without polluting the skill
namespace.

## Options Considered

1. **Single Compound Skill** -- One SKILL.md containing all 22 command
   instructions inline. Pro: simple discovery. Con: SKILL.md would exceed
   practical size limits and defeat progressive disclosure.

2. **Individual Skills per Command** -- 22 separate skill directories
   (apex-initspec/, apex-createprd/, etc.), each independently discoverable.
   Pro: granular invocation. Con: pollutes the skill namespace with 22 entries;
   many commands only make sense as part of the workflow.

3. **Skill Family with Shared References** -- Root orchestrator SKILL.md
   with a keyword-based dispatch table that routes to command-specific
   reference files in references/. Shared scripts in scripts/.

## Decision

Option 3: Skill Family with Shared References.

## Rationale

- Keeps the skill namespace clean (one entry: apex-spec)
- Aligns with the Agent Skills standard directory structure
  (SKILL.md + references/ + scripts/)
- Progressive disclosure works naturally -- metadata loads first, full
  dispatch table and reference content loads on selection
- Preserves modularity -- each command is a separate file, independently
  editable and testable
- Reference files stay under 500 lines each

## Consequences

- Users must invoke through the orchestrator ($apex-spec) rather than
  individual commands
- Adding a new command requires: creating a reference file AND updating
  the dispatch table in SKILL.md
- The orchestrator SKILL.md must stay concise enough for the agent to
  parse the dispatch table efficiently
