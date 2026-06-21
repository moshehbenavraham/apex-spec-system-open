# seshsplit

Create or refresh a session-based implementation plan inside the same text or
Markdown document that contains the rough plan. The command is a utility: it is
always allowed, does not require `.spec_system/`, and must not create new files.

## Rules

- Accept exactly one source file path plus optional natural-language
  instructions.
- Support only plain text and Markdown-like files. Reject PDFs, DOCX files,
  images, archives, binaries, and unreadable files.
- Modify only the source file named by the user. Do not create companion files,
  scratch files, summaries, specs, tasks, or `.spec_system/` artifacts.
- Preserve the original rough plan content exactly, except for inserting or
  replacing the generated `Session Split Plan` section near the top.
- If a `Session Split Plan` section already exists near the top, replace it
  with a fresh plan based on the current full document and optional
  instructions.
- For this utility command, use a rough 100k-token context window as the
  internal session breadth boundary. Do not apply the staged workflow's 2-4 hour
  or 12-25 task session limits unless the user explicitly asks for them.
- Do not mention tokens, context windows, sizing metrics, or internal boundary
  calculations in the generated plan.
- Create as many sessions as needed to cover everything materially described in
  the source plan. Do not collapse unrelated work into one session just to keep
  the list short.
- Each session must have one clear objective, concrete scope, expected outputs,
  dependencies or ordering notes, and acceptance checks.
- Carry forward ambiguity as assumptions or open questions inside the generated
  plan instead of silently inventing requirements.
- Keep generated text ASCII-only and use plain Markdown.

## Steps

1. Parse the request.
   - Required: one source file path, usually written as `@path/to/file.md`.
   - Optional: additional instructions after the file path.
   - If the file path is missing or more than one source file is supplied, stop
     and ask for a single target file.
2. Validate the source file.
   - Confirm the file exists and is readable.
   - Confirm it appears to be text or Markdown. Reject binary or rich document
     formats.
   - Confirm the file can be safely updated in place.
3. Read the full document.
   - Treat existing content below the generated section as the source of truth.
   - If a prior `Session Split Plan` exists near the top, use the rest of the
     document plus any optional user instructions as the current source.
4. Identify the update location.
   - If the first substantial section near the top is `Session Split Plan`,
     replace that section through the line before the next heading at the same
     or higher level.
   - Otherwise insert the new section after YAML frontmatter, if present, and
     after the first document title heading, if present.
   - If there is no frontmatter or title heading, insert the section at the top
     of the file.
5. Build the plan.
   - Remember the rough 100k-token context window as the internal session breadth boundary
   - Inventory every meaningful work item, feature, fix, decision, migration,
     integration, test, documentation update, and deployment concern in the
     source document.
   - Group work by dependency order and implementation cohesion.
   - Split sessions when the work would become difficult to complete in one
     focused agent session, when risk domains differ, or when later work depends
     on validation from earlier work.
   - Ensure every source concern is covered by at least one session.
6. Write the `Session Split Plan` section.
   - Use this structure:

```markdown
## Session Split Plan

### Session 01: <short title>

**Objective**: <single clear objective>

**Scope**:
- <included work>
- <included work>

**Outputs**:
- <expected deliverable>
- <expected deliverable>

**Dependencies / Notes**:
- <ordering note, assumption, or open question>

**Acceptance Checks**:
- <how to know this session is complete>
- <how to know this session is complete>
```

   - Use `None` for dependencies or notes only when there truly are none.
   - Keep session titles short and implementation-oriented.
   - Preserve the source document content below the generated section.
7. Update the file in place.
   - Write only the source file.
   - Preserve LF line endings.
   - Report the number of sessions created or updated and the file path.

## Output

Return a concise summary with:

- the updated file path
- the number of sessions in the generated plan
- any major assumptions or open questions captured in the plan
