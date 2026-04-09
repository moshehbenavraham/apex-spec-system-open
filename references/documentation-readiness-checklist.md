# Documentation Readiness Checklist

Reusable checklist for workflow steps that create, update, or record project
documentation.

## Accuracy

- [ ] Commands shown in docs exist and are the preferred commands for that task
- [ ] File paths, filenames, and directory names match the current repo state
- [ ] Links point to real files, sections, or external resources
- [ ] Version numbers, tool names, and config filenames are current
- [ ] Claims describe implemented behavior, not planned future behavior

## Conciseness

- [ ] No redundant sections when a link to a source of truth is enough
- [ ] No verbose explanations where a short command, table, or checklist is
  clearer
- [ ] No stale examples kept only for completeness

## Completeness

- [ ] Required files and sections exist
- [ ] No placeholder text or unresolved TODO content remains
- [ ] New packages, services, scripts, or workflows introduced by the session
  are reflected in the right documentation surfaces

## Source of Truth Rules

- Root README explains what the repo is and how to start
- Architecture docs describe structure and relationships, not roadmap promises
- Workflow refs keep command-local gates and handoffs; shared checklist docs
  hold reusable cross-cutting guidance
- Prefer linking over duplicating the same explanation in multiple places
