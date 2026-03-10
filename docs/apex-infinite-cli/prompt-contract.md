# Apex Infinite CLI Prompt Contract

## Purpose

This document describes the behavior that sits between the manager LLM,
summarizer LLM, and `codex exec`. It is the contract the CLI currently
implements, not a generic design note.

## Actors

- Summarizer LLM: compresses recent history into a short context block
- Manager LLM: chooses the next action
- Codex CLI: executes the chosen action or raw instruction

## Known Command Set

The CLI recognizes 13 Apex Spec workflow commands as structured outputs:

- `initspec`
- `createprd`
- `createuxprd`
- `plansession`
- `implement`
- `validate`
- `updateprd`
- `audit`
- `pipeline`
- `infra`
- `carryforward`
- `documents`
- `phasebuild`

Anything else is treated as free-form instructions unless it is `help` or
`alldonebaby`.

## Summarizer Contract

### Input

System message:

- `SUMMARIZER_SYSTEM_PROMPT`

User message shape:

```text
INPUT:
<aggregated history>
```

Aggregated history is built from the latest fetched records:

```text
[Task N: <path>_<id>]
Agent: <cc_response>
Manager: Manager - Output: <ai_decision_output> | Reason: <ai_decision_reason>
```

### Output

The summarizer returns free-form text. The CLI does not parse it as JSON. The
string is forwarded directly into the manager user message.

## Manager Contract

### Input

System message:

- `MANAGER_SYSTEM_PROMPT`

User message shape:

```text
IF EXISTS, CODEX CLI SENIOR DEVELOPER LATEST MESSAGE:
<agent_response>

IF EXISTS, CEO'S INSTRUCTIONS:
<ceo_msg>

HISTORICAL INTERACTIONS SUMMARY:
<summary>
```

### Expected Output

The preferred output is a JSON object with two keys:

```json
{"output": "implement", "reason": "tests passed"}
```

`output` drives routing. `reason` is logged and shown to the operator.

### Allowed Output Classes

- Known workflow command, such as `validate`
- `help`
- `alldonebaby`
- Arbitrary instruction text, such as `Fix the two failing tests then rerun validate`

## Parsing Behavior

The CLI uses a three-step parse strategy:

1. Call the manager LLM in JSON mode and parse the full response as JSON.
2. If that fails, call again without JSON mode and extract the first JSON
   object matching `output` and `reason`.
3. If that also fails, return the raw response text as `output` and set
   `reason` to `Raw LLM output (JSON parse failed)`.

This fallback chain is covered by the local pytest suite.

## Command Routing Contract

After parsing, the CLI normalizes the manager output by:

- trimming whitespace
- lowercasing for routing
- stripping a leading slash before command matching

That last step exists because the manager sometimes emits `/plansession`
instead of `plansession`.

## Prompt Generation For Codex

For known commands, the CLI emits this exact runtime prompt string:

```text
Run the apex-spec skill command /<command>
```

Examples:

- `plansession` -> `Run the apex-spec skill command /plansession`
- `implement` -> `Run the apex-spec skill command /implement`

For unknown manager outputs, the CLI passes the raw text straight to Codex.

## Important Nuance

The runtime prompt string above is a wrapper convention used by
`build_codex_prompt()`. It is separate from the manager prompt prose.

The test suite enforces two related but different rules:

- manager prompt prose should not contain workflow slash-command syntax outside
  code blocks
- runtime prompt generation for known commands should currently produce the
  exact `Run the apex-spec skill command /<command>` string

## Test Coverage

The prompt contract is verified by these test groups:

- `TestManagerSystemPrompt`
- `TestSummarizerSystemPrompt`
- `TestUserMessageTemplate`
- `TestBuildCodexPrompt`
- `TestJsonParsing`

## Change Safety Rules

If you change any of these behaviors, update all of the following together:

1. `apex_infinite.py`
2. `apex-infinite-cli/tests/test_prompts.py`
3. `apex-infinite-cli/README-apex-infinite-cli.md`
4. This document

## Related Docs

- [Operator runbook](operator-runbook.md)
- [History DB reference](history-db.md)
- [Troubleshooting guide](troubleshooting.md)
