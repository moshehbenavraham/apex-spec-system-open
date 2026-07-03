# Apex Infinite CLI - UX Requirements Document

**Companion to**: [PRD.md](PRD.md)
**Created**: 2026-07-02
**Status**: Authoritative standalone UX source for the Apex Infinite CLI UI upgrade

This document is intended to survive deletion of the original research inputs.
It incorporates the relevant UX facts from the local retro-terminal reference
tree, the Apex Infinite CLI upgrade plan, the current CLI implementation, and
the current CLI docs. Future planning and implementation should use this file
and `PRD.md` as the durable product source of truth.

---

## 1. Design Brief

### Emotional Targets

Focused command, accountable momentum, restrained retro authority.

The interface should make a long autonomous development run feel controlled and
observable. The retro mood is a disciplined operator-console layer, not a toy
theme. Every visible element must help the operator understand state, risk,
current work, captured output, or the next handoff.

### Aesthetic Identity

- **Reference domain**: Mission-control terminal benches, service monitors,
  and late mainframe operator consoles.
- **Era / movement**: Late-1970s and early-1980s CRT computing interpreted
  through Swiss information hierarchy.
- **Material metaphor**: Phosphor text behind smoked glass inside a black metal
  instrument rack.

The visual source material established useful concepts: profile-driven terminal
moods, terminal frame composition, screen/effect/performance settings groups,
operator-oriented menus, persistent settings, viewport status overlays, and a
render pipeline split between source content, dynamic effects, static effects,
and frame treatment. Apex Infinite CLI must translate those ideas clean-room
into independent CLI tokens, labels, layouts, tests, docs, and optional wrapper
code. Do not copy reference source, QML, shader code, shader constants, compiled
shader blobs, colors, profile data, images, icons, fonts, resource manifests,
build scripts, or terminal-emulator code.

### Signature Moment

The screenshot-worthy moment is the iteration frame: one compact operational
cycle shows project, provider, model, selected theme, dry-run state, iteration,
elapsed time, current operation, manager decision, prompt preview, Codex
execution status, response summary, DB log confirmation, and next command or
stop state in a stable scan-friendly order.

### Micro-Narrative

Arrival -> Orientation -> Engagement -> Action -> Resolution

```text
Launch/config -> Boot panel -> Iteration frame -> Manager decision
              -> Prompt preview -> Codex execution -> Result/log
              -> Next command, pause, completion, or safety stop
```

The user should feel that the system is booting an autonomous instrument,
establishing context, acting visibly, recording its work, and handing off to the
next command without drama.

### Experience Principles

- Legibility beats novelty in every theme.
- Every visual element carries operational information.
- Terminal-first behavior remains scriptable, headless-safe, and plain-output
  compatible.
- Styled output never becomes stored workflow data.
- Effects are low by default, configurable, and easy to disable.
- The future Linux wrapper is a companion display for the same workflow engine,
  not a fork of the CLI behavior.

---

## 2. Source Digest And Current Baseline

This section preserves the source-derived facts that would otherwise be lost if
the planning document and local example tree are removed.

### Product Context

Apex Infinite CLI is a Python CLI that repeatedly:

```text
read recent SQLite history -> summarize history -> ask manager LLM
                            -> route decision -> run codex exec
                            -> log result -> repeat
```

The loop stops when the manager emits `alldonebaby`, when the max iteration
limit is reached, when the operator quits from an emergency prompt, or when the
process is externally terminated.

### Current Implementation Baseline

The current implementation is a single-file Click application in
`apex-infinite-cli/apex_infinite.py`.

- Runtime dependencies already include Click, Rich, OpenAI Python SDK,
  python-dotenv, PyYAML, SQLite from the Python standard library, and Codex CLI.
- A global Rich `Console()` currently owns terminal output.
- `config.yaml` currently defines provider settings and Codex settings only;
  it does not yet define a `ui` section.
- Supported provider names are `ollama`, `grok`, and `openai`.
- Codex settings include binary, exec flags, and model reasoning effort.
- Main CLI options today are `--path`, `--start`, `--ceo`, `--provider`,
  `--model`, `--config`, `--history`, `--max-iterations`, `--dry-run`,
  `--verbose`, and `--version`.
- If `--path` is absent, the CLI lists directories under `~/projects/`, accepts
  a number or path, prompts for optional start command, and prompts for optional
  CEO instructions.
- The project path is expanded, checked for existence, normalized to one
  trailing slash, and used as the SQLite history key.
- The default max iteration limit is 50.
- Each Codex command has a 30-minute timeout.
- `execute_codex()` currently uses `subprocess.run(..., capture_output=True)`.
  It returns stdout, falls back to stderr when stdout is empty, wraps non-zero
  exits, reports timeout, reports missing binary, and reports generic
  exceptions.
- `--dry-run` prints the `codex exec` command that would be launched and returns
  a dry-run response without launching Codex.
- `--verbose` currently expands the visible agent response after execution.
- `--history` currently prints up to 50 rows through a Rich table.
- The SQLite DB lives at `~/.apex-infinite/history.db`, uses WAL mode, and
  stores one `history` table with `id`, `path`, `cc_response`,
  `ai_decision_output`, `ai_decision_reason`, `help_or_done_msg`, and
  `created_at`.
- The legacy `cc_response` column must stay intact for backward compatibility.
- The manager recognizes 14 Apex Spec commands for prompt generation:
  `initspec`, `createprd`, `createuxprd`, `plansession`, `implement`,
  `creview`, `validate`, `updateprd`, `audit`, `pipeline`, `infra`,
  `carryforward`, `documents`, and `phasebuild`.
- The normal autonomous manager loop is scoped to initialized projects and
  normally chooses post-initialization workflow commands.
- Known commands are converted to `Run the apex-spec skill command /<command>`.
  Unknown outputs are sent to Codex as raw instructions.
- Manager output is normalized by trimming whitespace, lowercasing for routing,
  and stripping a leading slash before command matching.
- `help` is an emergency operator pause, not normal workflow routing.
- `Ctrl+C` once requests a pause at the next loop boundary; a second interrupt
  can force quit.
- `notify-send` is used opportunistically for Linux desktop notifications, but
  terminal output remains authoritative.
- Current tests focus on prompt and routing behavior. UI work must add tests for
  config, flags, renderer behavior, history display, environment fallbacks,
  subprocess display, and event output.

### Planned UX Commitments

The UI upgrade must add a renderer/config/event boundary without changing the
workflow contract unless a session explicitly changes prompt behavior and
updates code, tests, README, and prompt-contract docs together.

New UI configuration requirements:

```yaml
ui:
  theme: "auto"
  effect_level: "low"
  ascii: false
  compact: false
  show_elapsed: true
  show_provider: true
  themes: {}
```

New or planned CLI overrides:

```bash
python apex_infinite.py --theme crt-amber
python apex_infinite.py --plain
python apex_infinite.py --ascii
python apex_infinite.py --compact
python apex_infinite.py --event-stream /tmp/apex-infinite-events.jsonl
```

Configuration precedence:

```text
CLI flags -> environment constraints -> config.yaml -> built-in defaults
```

Resolution rules:

- Built-in default theme is `auto`.
- `auto` resolves to `crt-green` on capable interactive TTYs.
- `auto` resolves to `plain` for `NO_COLOR`, `TERM=dumb`, non-TTY output,
  redirected output, or a non-terminal Rich console path.
- `--plain` forces plain theme, color disabled, and effect level off.
- `NO_COLOR` behaves like plain mode unless the operator explicitly opts back
  into a theme.
- `--ascii` changes glyph selection only; it does not automatically disable
  color.
- `--compact` reduces vertical space but must not hide errors, manager reasons,
  command prompts, completion state, help, interrupts, or timeouts.
- Invalid `--theme`, `ui.theme`, and malformed `ui.themes` values fail fast
  with clear Click/config errors. Invalid user configuration must not silently
  fall back to `plain`.
- `--event-stream PATH` writes line-buffered JSONL events to a file without
  changing normal human output.
- `--event-stream -` is allowed only with an explicit human-rendering disable
  mechanism so JSONL never mixes with Rich or plain human output.

### Reference-Derived Visual Concepts

The local retro-terminal reference established the following reusable ideas.
They are requirements as concepts only, not implementation data.

- Profile families: amber CRT, green CRT, DOS-like high contrast, blue/cyan
  variants, old computer moods, minimal "boring" mode, and e-ink-like quiet
  mode. Apex Infinite CLI first ships `auto`, `crt-green`, `crt-amber`,
  `ibm-dos`, and `plain`.
- Settings organization: general/profile settings, terminal/font settings,
  effects settings, advanced/performance settings, import/export/persistence,
  and small reusable controls.
- Terminal viewport concepts: source content, scroll position, selection,
  focus, paste/copy affordances, terminal size feedback, zoom/scaling, and
  stable status display.
- Effect categories: bloom, glow, burn-in trails, static/noise, jitter,
  flicker, scanlines/rasterization, horizontal sync, RGB shift, curvature,
  ambient light, frame size, frame color, and frame shine.
- Performance controls: effects FPS, texture quality, bloom quality, burn-in
  quality, and low-effects fallbacks.
- Render pipeline concepts: source terminal surface, optional bloom source,
  dynamic effect pass, static final pass, frame pass, frame buffer, and timing
  driver.
- Wrapper controls: theme selector, effect intensity, font/scaling, reduced
  effects, plain fallback, copy/log actions, settings import/export, fullscreen,
  and zoom.
- Packaging concepts: graphical wrapper dependencies and release artifacts must
  be documented separately from base CLI installation.

Clean-room limits:

- Rich may translate only mood, hierarchy, labels, simple separators, and
  settings vocabulary.
- The optional Linux wrapper may independently implement glow, scanlines,
  flicker, curvature, trails, and frame treatment after the event boundary is
  available.
- The base CLI must not require Qt, PySide6, PyQt, qmltermwidget,
  QTermWidget, a graphical display, an external terminal emulator, or the
  reference application.
- The selected wrapper path is PySide6 with Qt Quick/QML as an optional
  Linux-only extra. PyQt, qmltermwidget, QTermWidget, copied QML, copied
  shaders, copied assets, copied fonts, copied profile data, and copied
  terminal-emulator code are excluded.

---

## 3. User Flows

### Flow 1: Interactive Project Selection And Startup

**Trigger**: Operator runs `python apex_infinite.py` with no `--path`.
**Goal**: Choose a project and enter the autonomous loop with clear context.

```text
Launch -> Config resolution -> Project list or path prompt
      -> Optional start command -> Optional CEO instruction
      -> Boot panel -> Iteration 1
```

**Happy path**: The user sees resolved provider, model, project path, max
iterations, dry-run state, UI mode, start command, and CEO instruction presence
before work begins.
**Error states**: Missing config, unknown provider, missing API key value,
invalid theme/config, invalid project selection, and nonexistent directory fail
before loop execution.

### Flow 2: Direct Or Resume Autonomous Run

**Trigger**: Operator runs with `--path`, optionally `--start` and `--ceo`.
**Goal**: Start or resume a target project without interactive prompts.

```text
CLI flags -> Config/UI resolver -> Path normalization -> Boot panel
          -> Fetch history -> Manager decision or start override
          -> Prompt preview -> Codex execution -> DB log
          -> Next iteration or stop
```

**Happy path**: The operator can confirm project identity and first action from
the boot panel and first iteration frame.
**Error states**: Invalid config, invalid path, invalid theme, missing Codex
binary, provider retry exhaustion, timeout, and non-zero Codex exit render with
severity labels and raw stored facts.

### Flow 3: Dry-Run Confidence Check

**Trigger**: Operator passes `--dry-run`.
**Goal**: Verify route, prompt, provider/model, config, UI mode, and exact
Codex command without launching Codex.

```text
Launch -> Config/UI resolver -> Boot panel -> Manager/start decision
      -> Prompt preview -> Dry-run command panel -> DB log
      -> Next iteration or safety stop
```

**Happy path**: Output clearly says no Codex subprocess was launched and shows
the command that would run.
**Error states**: Invalid config, invalid theme, and invalid project path fail
before the dry-run command panel appears.

### Flow 4: Known Command Routing

**Trigger**: Manager emits a known Apex Spec command or a slash-prefixed known
command.
**Goal**: Run the correct Codex prompt while preserving prompt-contract tests.

```text
Manager JSON/raw output -> Normalize -> Known command?
    yes -> Build skill command prompt -> Preview -> codex exec
    no  -> Send raw instruction -> Preview -> codex exec
```

**Happy path**: Known commands are labeled as workflow commands; custom outputs
are labeled as raw instructions.
**Error states**: Malformed manager JSON falls back to regex or raw output and
shows that fallback clearly without hiding the routed output.

### Flow 5: Monitor Long Codex Execution

**Trigger**: A non-dry-run iteration launches `codex exec`.
**Goal**: Keep the operator aware of active work while preserving captured
stdout/stderr semantics.

```text
Prompt dispatch -> Process start -> Elapsed status
                -> stdout success | stderr fallback | non-zero exit
                -> timeout | missing binary | generic exception
                -> Response panel -> DB log
```

**Happy path**: A live status line or equivalent shows command state, elapsed
time, timeout threshold, binary name, and current operation.
**Error states**: Timeout, non-zero exit, missing binary, generic exception,
and interrupted runs have text labels, plain fallbacks, and raw DB rows.

### Flow 6: Inspect History Ledger

**Trigger**: Operator passes `--history`, optionally with `--path` and
`--verbose`.
**Goal**: Review recent workflow state without horizontal scrolling.

```text
History flag -> Optional path filter -> Compact ledger
             -> Verbose row expansion when --verbose is present
```

**Happy path**: Default history uses ID, timestamp, project, manager output,
status/help marker, concise reason, and truncated response summary. Verbose
history expands reason and response detail.
**Error states**: Empty history, sparse legacy rows, long paths, long reasons,
and long responses remain readable at 80 columns.

### Flow 7: Emergency Help Or Operator Interrupt

**Trigger**: Manager emits `help`, or the operator presses `Ctrl+C` once.
**Goal**: Pause visibly without corrupting workflow state.

```text
Help/interrupt -> Alert block -> Optional desktop notification
               -> Operator input or quit -> Continue/log or stop
```

**Happy path**: The prompt states whether the system is waiting for input, why
it paused, and whether the response becomes CEO instructions.
**Error states**: A second `Ctrl+C` can still force quit. A normal pause and a
force quit are visibly different.

### Flow 8: Plain, ASCII, Compact, And Automation Output

**Trigger**: Operator passes `--plain`, `--ascii`, or `--compact`; environment
sets `NO_COLOR`; terminal is dumb, non-TTY, redirected, or test-injected.
**Goal**: Keep output deterministic and readable outside rich interactive
terminals.

```text
Environment/flags -> UI resolver -> Plain/ascii/compact renderer
                  -> Same semantic states -> Raw DB/events unchanged
```

**Happy path**: Logs contain plain text labels and no ANSI escapes, Rich markup,
box glyphs, or carriage-return-only live output.
**Error states**: Plain mode must still show errors, timeouts, help,
interrupts, manager reasons, prompt previews, DB log notices, and completion.

### Flow 9: Emit Lifecycle Events For Future Surfaces

**Trigger**: Operator passes `--event-stream PATH`, or a future wrapper launches
the CLI as a subprocess.
**Goal**: Provide raw machine-readable lifecycle facts without scraping human
output.

```text
CLI launch -> Event emitter open -> Lifecycle JSONL writes
          -> Human renderer remains separate
          -> Wrapper/test consumes events
```

**Happy path**: Events include startup, config/UI resolution, iteration
lifecycle, history summary, manager decision, prompt dispatch, subprocess
lifecycle, output summary, DB log, help, interrupt, completion, timeout, error,
and stop states.
**Error states**: `--event-stream -` is rejected unless human rendering is
disabled. Event write failures are visible and do not silently corrupt human
output.

### Flow 10: Configure A Visual Theme

**Trigger**: Operator edits `config.yaml` or passes `--theme`, `--plain`,
`--ascii`, `--compact`, or future wrapper settings.
**Goal**: Select a readable presentation without changing workflow behavior.

```text
Config/flags -> Validate theme names and overrides
             -> Resolve environment constraints -> Render token set
             -> Same workflow engine and storage
```

**Happy path**: Built-in themes and valid custom overrides apply consistently
to boot, iteration, history, errors, and completion.
**Error states**: Invalid names or malformed override values fail fast with the
invalid field and accepted values.

---

## 4. Screen Inventory

For this product, "screen" means a distinct terminal surface, output mode, event
surface, or future wrapper view.

| Screen | Entry/Route | Purpose | Key Components |
|--------|-------------|---------|----------------|
| Interactive Project Selection | `python apex_infinite.py` with no `--path` | Select project, starting command, and CEO instruction | Project list, number/path prompt, validation error |
| Config Error Surface | Startup/config load | Fail before loop execution on invalid setup | Error label, invalid field, accepted values, source file |
| Boot Status Panel | Normal and dry-run startup | Establish operational context | Project, provider, model, config path, theme, max iterations, dry-run, start command |
| Iteration Frame | Main loop | Group one autonomous cycle | Iteration, operation, elapsed time, provider/model, project, dry-run |
| History Summary Notice | Iteration start | Show memory context preparation | Prior row count, summarizer status, retry label |
| Manager Decision Panel | After manager response | Separate manager choice from Codex output | Output command/instruction, reason, known/custom label, parse fallback label |
| Prompt Preview | Before Codex execution | Show what will be sent to Codex without flooding output | Truncated prompt, command class, custom instruction marker |
| Codex Execution Status | During subprocess | Show active process and elapsed time | Binary, timeout threshold, elapsed time, process state |
| Agent Response Panel | After subprocess | Summarize captured output | Truncated response, verbose expansion, stderr fallback, error state |
| DB Log Notice | End of iteration | Confirm durable history write | Project key, manager output, timestamp/status |
| Help Pause | `help` decision | Request external operator input | Alert label, reason, input prompt, notification note |
| Interrupt Pause | `Ctrl+C` once | Collect new CEO instruction after current step | Alert label, input prompt, quit option |
| Completion State | `alldonebaby` | End workflow visibly | Completion label, reason, iteration count, DB marker |
| Max Iteration Stop | Safety limit reached | Stop runaway loops safely | Warning, max count, next operator action hint |
| Timeout/Error State | Subprocess or provider failure | Make failure unmistakable | Severity label, raw reason, recovery hint |
| History Ledger | `--history` | Review recent interactions | Compact rows, optional path filter, verbose detail, empty state |
| Plain Output Mode | Auto or `--plain` | Serve logs, CI, non-TTY, dumb terminals | Line labels, no ANSI, no box glyphs, no live-only UI |
| ASCII Output Mode | `--ascii` | Avoid non-ASCII glyphs while allowing color if supported | ASCII separators, ASCII status markers |
| Compact Output Mode | `--compact` | Reduce vertical space without losing semantics | Short labels, fewer blank lines, no hidden critical states |
| Event Stream | `--event-stream PATH` | Machine-readable lifecycle boundary | JSONL events, raw payload facts, no markup |
| Linux Wrapper Main Window | Optional future mode | Event-driven visual console | Read-only log viewport, status panels, theme selector, effect controls |
| Linux Wrapper Settings | Optional future mode | Configure visual-only wrapper preferences | Theme, effect level, font/scaling, reduced effects, plain fallback |
| Wrapper Failure Surface | Optional future mode | Show subprocess or malformed-event failures | Missing CLI, non-zero exit, timeout, malformed JSON, reconnect guidance |

---

## 5. Navigation Structure

```text
apex_infinite.py
|-- Interactive startup
|   |-- Project selection
|   |-- Start command prompt
|   \-- CEO instruction prompt
|-- Direct run
|   |-- Boot status panel
|   |-- Iteration loop
|   |   |-- History summary
|   |   |-- Manager decision
|   |   |-- Prompt preview
|   |   |-- Codex execution
|   |   |-- Response panel
|   |   \-- DB log
|   |-- Help or interrupt pause
|   \-- Completion, timeout, error, or max-iteration stop
|-- Dry run
|   \-- Same semantic loop with no Codex subprocess launch
|-- History
|   \-- Compact ledger with optional verbose expansion
|-- Event stream
|   \-- JSONL side channel for wrappers/tests
\-- Optional Linux wrapper
    |-- Main visual console
    |-- Settings
    \-- Failure surface
```

**Navigation pattern**: CLI flags determine entry mode. Inside normal runs, the
only interactive navigation is startup selection and emergency help/interrupt
input.

**Deep linking**: Project history is scoped by normalized project path. Event
streams are addressed by file path. Future wrapper views consume event names and
payloads, not Rich terminal frames.

**State ownership**: The CLI workflow engine owns manager decisions, prompt
building, Codex execution, history logging, stop conditions, and safety
behavior. Renderers and wrappers display this state but do not fork it.

---

## 6. Interaction Patterns

### Forms And Prompts

- Startup prompts are line-oriented and keyboard-first.
- Click/config validation happens before loop execution.
- Invalid values show one visible severity label, the field/value, and accepted
  values or environmental reason.
- Success feedback appears in the boot panel before the first manager decision.
- Help and interrupt prompts must clearly own input focus.

### Config And Theme Resolution

- A single resolver owns UI setting precedence.
- Theme validation is fail-fast for user errors.
- Environmental constraints choose plain defaults only when the user did not
  explicitly force a styled theme.
- Custom theme overrides are validated data, not executable style hooks.
- `--plain`, `--ascii`, and `--compact` are orthogonal where possible:
  plain disables color/effects, ascii changes glyphs, compact changes density.

### Loading States

- LLM summarization shows the number of prior rows and retry state.
- Manager decision shows active decision state and retry state.
- Codex subprocess shows elapsed time, timeout threshold, process state, and
  binary name.
- Plain mode emits durable lines instead of relying on spinners, live-only
  refresh, or carriage-return animation.
- Wrapper mode may animate event arrivals, but active status remains pinned and
  readable.

### Notifications

- Terminal output is always the source of truth.
- Terminal bell and `notify-send` can support help, completion, interrupt, and
  safety-stop states.
- Notifications must never be the only place an important state appears.
- CI, non-TTY, `NO_COLOR`, `TERM=dumb`, and redirected output use plain text
  with no ANSI escapes or box glyphs.

### Error, Warning, And Empty States

- Every error has a severity label, failing subsystem, raw reason, and recovery
  direction when known.
- Empty history is a first-class state, not an empty table.
- Sparse legacy DB rows render with blank-safe cells.
- Non-zero subprocess exits show return code plus captured stdout/stderr
  semantics.
- Timeout text uses the configured timeout threshold.
- Invalid UI config fails before any misleading themed output appears.

### History Interaction

- Default history is compact and readable at 80 columns.
- `--verbose` expands reason and response detail in history mode; do not add
  `--history-verbose`.
- Long response summaries truncate with explicit counts.
- History display does not mutate the DB.
- History rows remain raw workflow facts, not renderer snapshots.

### Event Stream Interaction

- Events are opt-in.
- Events are line-buffered JSONL.
- Event payloads contain raw facts, not Rich markup, ANSI escapes, box glyphs,
  frame tokens, or reference-derived visual tokens.
- Human rendering and machine stdout JSONL are mutually exclusive unless an
  explicit human-rendering disable mode is active.
- Event errors are visible in human output unless human rendering is disabled,
  in which case they must be machine-readable.

### Product Surface Boundaries

- Primary surfaces: boot panel, iteration frame, manager decision, prompt
  preview, execution status, response panel, history ledger, pause states,
  completion states, and user-facing wrapper views.
- Developer/admin/debug surfaces: pytest output, renderer fixture recordings,
  raw event JSONL files, config validation traces, wrapper spike logs, and
  reference-clean-room audit notes.
- Excluded from primary UI: renderer internals, route ownership notes,
  frame/glyph diagnostics, visual test scaffolding labels, raw event dumps,
  shader reference details, copied profile metadata, and implementation-only
  file paths.

---

## 7. Motion And Animation Strategy

### Philosophy

Motion communicates liveness, elapsed time, and event arrival. It must never
hide commands, errors, handoffs, or captured output.

### Base CLI

- Page load: output appears in stable sections: boot, iteration, decision,
  prompt, execution, result, log, next state.
- Scroll-driven animation: none.
- Live display: limited to status/progress while preserving captured output.
- Plain/compact/non-TTY: degrade to durable line-oriented messages.
- Error/help/interrupt/completion text is never animated over or replaced by
  transient spinners.

### Future Wrapper

- Event arrival may use subtle opacity or position changes.
- Active status remains pinned while the log scrolls.
- Theme and settings controls show immediate state changes.
- Effects may include independently implemented glow, scanlines, flicker,
  curvature, phosphor trails, and frame treatment.
- Reduced effects keeps state visible through text, color, and simple layout
  changes rather than removing status feedback.

### Animation Constraints

- Target locked 60fps for live terminal updates and wrapper effects.
- Maximum 3 simultaneous animated elements per viewport region in the wrapper.
- Rich terminal animations must be disabled or simplified under `--plain`,
  `--compact`, `NO_COLOR`, `TERM=dumb`, non-TTY, redirected output, or a
  non-terminal console path.
- Do not use linear easing for wrapper motion; use gentle eased transitions.
- Test performance-sensitive interactions under constrained CPU assumptions.

---

## 8. Layout Philosophy

### Composition Approach

Dense and information-rich, with enough rhythm to separate phases of work. The
base CLI should feel like one instrument panel, not unrelated print statements.

### Visual Hierarchy

- Labels, borders, spacing, and color roles matter more than large text.
- Important states use concise uppercase labels only when they need immediate
  attention.
- Default mode may use one blank line between major sections.
- Compact mode removes decorative spacing while preserving semantic labels.
- Every iteration uses the same order so operators can scan by habit.

### Section Transitions

Use hard terminal section boundaries: boot, iteration, history, decision,
prompt, execution, result, log, next step. Rich themes may use faint repeated
ASCII-compatible separators for a low-fidelity scanline feel; plain and compact
modes use simple line labels.

### Framing Rules

- Do not nest UI cards or heavy panels inside panels.
- Avoid wide tables for primary history at 80 columns.
- Keep the current command and current failure visible without horizontal
  scrolling.
- Let wrapper frame treatment stay full-window and functional; do not put the
  primary terminal viewport inside decorative cards.

---

## 9. Responsive Strategy

| Breakpoint | Target | Layout Approach |
|------------|--------|-----------------|
| `< 80 columns` | Narrow terminal/logs | Single-column labels, no wide tables, no hidden errors, truncate only with explicit counts |
| `80 columns` | Baseline terminal | Compact status strip, wrapped reason text, readable history ledger |
| `100 columns` | Comfortable terminal | Full iteration frame, concise panels, response summaries |
| `120+ columns` | Wide terminal | Wider response/history columns without extra decorative noise |
| `non-TTY/log` | CI, redirected output, dumb terminal | Plain line output, no color, no live rendering, no box glyphs |
| `wrapper small window` | Future visual wrapper | Collapsible side/status areas, log remains primary |
| `wrapper large window` | Future visual wrapper | Pinned status panels plus wide read-only log viewport |

**Approach**: Terminal-width adaptive, with plain-output fallbacks ahead of
visual polish.

**Touch targets**: Future wrapper controls must be at least 44x44px. Base CLI
interactions remain keyboard-first.

---

## 10. Accessibility

**Target**: WCAG 2.1 AA intent for contrast and non-color semantics, adapted to
terminal constraints.

- Keyboard navigation: All base CLI interactions must be keyboard-accessible.
  Future wrapper controls require normal tab order and visible focus.
- Screen reader: Plain mode should produce sequential, meaningful text without
  relying on Rich layout. Live statuses must also emit durable state changes.
- Color contrast: Styled themes must keep normal text, muted text, warnings,
  errors, success, and borders readable on common dark terminals.
- Color independence: Every status has a text label in addition to color.
- Focus management: Help and interrupt prompts must clearly own input focus.
- Reduced motion: `--plain`, `--compact`, `ui.effect_level: off`, `NO_COLOR`,
  `TERM=dumb`, non-TTY output, and redirected output remove live-only or
  decorative effects while preserving state changes.
- Non-ASCII: `--ascii` and plain mode must use code points 0-127 only.
- Width resilience: Text wraps or truncates with counts; it must not overlap,
  disappear, or require horizontal scrolling for critical states.
- Secrets: API keys and environment-derived secrets must not be printed,
  written to SQLite, or emitted in JSONL events.

---

## 11. Design System

### Color Architecture

- **Dominant surface (60%)**: Terminal background or wrapper viewport. Default
  interactive theme should feel dark, quiet, and high contrast.
- **Secondary surfaces (25%)**: Panels, iteration frames, response blocks, and
  history rows. Use low-contrast borders or muted color, not heavy decoration.
- **Accent (10%)**: Active command, current operation, elapsed time, selected
  theme, and focused prompt.
- **Signal colors (5%)**: Success, warning, error, timeout, help, interrupt,
  dry-run, completion, and invalid configuration.

Palette character: Synthetic, dark, restrained, and high-contrast. Use
independent token names and values. Do not copy reference profile colors.

### Built-In Theme Intents

| Theme | Intent | Primary Use |
|-------|--------|-------------|
| `auto` | Resolve to the right default for the terminal | First-run default |
| `crt-green` | Focused green-phosphor operator console | Capable interactive TTY default |
| `crt-amber` | Warm amber maintenance terminal | Operator preference |
| `ibm-dos` | Crisp DOS-like contrast with minimal effects | High-legibility retro mode |
| `plain` | Deterministic unstyled text | Logs, CI, non-TTY, dumb terminals |

### Status Vocabulary

Use stable labels across themes and plain mode:

- `BOOT`
- `ITERATION`
- `HISTORY`
- `DECISION`
- `PROMPT`
- `EXECUTING`
- `DRY RUN`
- `RESPONSE`
- `LOGGED`
- `HELP`
- `INTERRUPT`
- `TIMEOUT`
- `ERROR`
- `COMPLETE`
- `STOP`

### Typography

- **Display font**: The user's terminal font in bold or high-emphasis style.
  Do not ship copied or bundled reference fonts in the base CLI.
- **Body font**: The user's terminal monospace font.
- **Monospace**: Primary typography for every base CLI surface.
- **Scale ratio**: Terminal emphasis scale: normal, dim, bold, panel title,
  alert title. Do not depend on viewport-width font scaling.
- **Minimum body size**: Controlled by terminal. Future wrapper should default
  to a readable system monospace size and expose scaling controls.

### Spacing Scale

Terminal spacing uses rows and columns:

```text
0 rows: compact inline labels
1 row: default section separation
2 rows: major state transition
4 columns: nested detail indent
8 columns: table padding or status grouping when width allows
```

Future wrapper spacing uses an 8px base scale:

```text
4, 8, 12, 16, 24, 32, 48, 64
```

### Elevation And Depth

Base CLI depth comes from ordering, borders, labels, and muted text. Do not
simulate physical depth with heavy boxes inside boxes. Future wrapper may use
subtle glow, dark glass, and frame treatment, but text legibility remains the
priority.

### Texture And Atmosphere

Rich milestone:

- Low-fidelity scanline-like separators may use simple repeated characters.
- Disable decorative separators in `plain` and compact modes.
- Never write box glyphs, ANSI escapes, or Rich markup to SQLite history.

Future wrapper:

- Effects may include independently implemented glow, scanlines, flicker,
  curvature, phosphor trail, and frame treatment.
- Do not use copied noise images, CRT images, shaders, constants, fonts, icons,
  profile data, or resource manifests.

---

## 12. Component Patterns

| Component | Used In | Behavior |
|-----------|---------|----------|
| UI Config Resolver | Startup | Resolves CLI flags, environment constraints, config, and defaults deterministically |
| Theme Token Set | Renderer, wrapper | Supplies color, severity, border, glyph, emphasis, and fallback tokens |
| Glyph Set | Renderer | Switches between styled, ASCII, compact, and plain symbols |
| Renderer Facade | All human output | Centralizes `Console` usage and supports injected test consoles |
| Boot Panel | Normal and dry-run startup | Shows provider, model, project, config, theme, max iterations, dry-run, start command |
| Status Strip | Iteration frame | Shows iteration, operation, elapsed time, provider/model, project, dry-run |
| Iteration Frame | Main loop | Groups one autonomous cycle with stable section order |
| History Summary Notice | Main loop | Shows prior record count and summarizer activity |
| Decision Panel | Manager output | Separates command/custom instruction and reason from agent output |
| Prompt Preview | Before Codex | Shows generated Codex prompt with truncation and command classification |
| Execution Status | Codex subprocess | Shows process state, elapsed time, timeout, and binary name |
| Response Panel | After Codex | Shows captured output summary, verbose expansion, and error labels |
| History Ledger | `--history` | Shows compact rows, path filter, verbose expansion, empty state |
| Alert Block | Help, interrupt, timeout, error | Uses text labels plus color/severity; impossible to miss in plain mode |
| DB Log Notice | End of iteration | Confirms history write without exposing debug internals |
| Event Emitter | Event stream | Writes raw JSONL facts and exposes importable API for tests/wrappers |
| Wrapper Log Viewport | Future Linux wrapper | Read-only event-driven operational log, not a terminal emulator clone |
| Wrapper Status Panels | Future Linux wrapper | Show provider/model, project, iteration, operation, elapsed time, stop state |
| Wrapper Settings Panel | Future Linux wrapper | Theme, effect intensity, font/scaling, reduced effects, plain fallback |
| Wrapper Failure Surface | Future Linux wrapper | Shows malformed events, missing CLI, subprocess exit, timeout, and recovery |

---

## 13. Event Model And Wrapper Boundary

### Event Stream Purpose

The event stream is the machine-readable interface for future renderers,
wrappers, tests, and diagnostics. It prevents wrappers from parsing Rich output
or terminal frames.

### Required Event Names

Use stable snake_case names:

- `startup_begin`
- `config_loaded`
- `ui_resolved`
- `project_resolved`
- `iteration_started`
- `history_fetched`
- `history_summarize_started`
- `history_summarize_finished`
- `manager_decision_started`
- `manager_decision_finished`
- `prompt_built`
- `codex_started`
- `codex_finished`
- `codex_timeout`
- `codex_error`
- `response_summarized`
- `db_log_started`
- `db_log_finished`
- `help_requested`
- `operator_interrupt_requested`
- `operator_input_received`
- `workflow_completed`
- `max_iterations_reached`
- `run_stopped`
- `event_stream_error`

### Payload Rules

- Include timestamp, project path key, iteration number when applicable,
  operation name, severity when applicable, and concise raw facts.
- Do not include API keys, secrets, Rich markup, ANSI escapes, box glyphs,
  renderer tokens, reference-derived visual constants, or human-only frames.
- Keep event payloads JSON-serializable with primitive values and simple
  objects.
- Flush line-buffered writes so wrapper state stays current.
- Preserve event order in dry-run tests.
- Keep event versioning explicit if payload shape changes.

### Wrapper Contract

The optional Linux wrapper:

- Launches or observes the Python CLI as the workflow engine.
- Consumes JSONL events or an importable event emitter API.
- Renders a read-only terminal-like log viewport and operational panels.
- Does not embed a pseudo-terminal in the selected path unless a future
  decision proves it necessary.
- Does not scrape Rich frames.
- Does not depend on the reference terminal application.
- Keeps graphical dependencies optional and Linux-scoped.
- Documents PySide6 LGPLv3/commercial obligations and packaging requirements.

---

## 14. Implementation Coverage Matrix

This matrix captures the source plan's UX scope without making exact session
numbering authoritative. `phasebuild` owns final session stubs and counts.

| Coverage Area | UX Deliverables | Verification |
|---------------|-----------------|--------------|
| UI architecture and theme tokens | Renderer boundary, injected `Console`, UI resolver, token model, built-in themes, custom override validation | Prompt tests unchanged, config/Click tests, no styled DB rows |
| CRT-inspired operator console | Boot panel, iteration frame, status strip, manager/prompt/response/log surfaces, help/completion/error render states | 80/100/120 column checks, plain/ascii/compact checks |
| Live execution and history | Elapsed subprocess status, preserved capture semantics, compact history ledger, verbose history expansion | Fake subprocess tests for success, stderr-only, non-zero, timeout, dry-run, missing binary |
| Documentation and samples | README/runbook/history/prompt-contract/troubleshooting updates, ASCII transcripts or asciinema casts, clean-room note | Docs describe implemented flags, fallback modes, event stream, no-copy boundary |
| Event stream boundary | `--event-stream PATH`, guarded stdout JSONL mode, importable emitter API, raw event payloads | Dry-run event order tests, no markup/ANSI/reference tokens |
| Linux wrapper spike | Optional PySide6/QML prototype or explicit deferral, read-only event-driven log, effects feasibility, license/dependency assessment | Prototype launches/displays events or documents exact blocker |
| Wrapper productization or deferral | Optional Linux visual mode with settings and failure surfaces, or named blocker and reopen criteria | Wrapper smoke tests if shipped; deferral is explicit if not |
| Release verification | Compatibility, docs, clean-room audit, smoke run, fallback behavior, source encoding | Full applicable test suite, ASCII/LF checks, no copied reference material |

---

## 15. UX Acceptance Checklist

- The default interactive run presents a cohesive operator-console experience.
- The first visible surface identifies project, provider, model, config/theme,
  max iterations, dry-run state, and first command when available.
- Every iteration has stable sections in the same order.
- Manager decisions are visually distinct from Codex output.
- Prompt preview is visible but truncated safely.
- Operators can tell whether Codex is running and how long it has been running.
- Timeout, non-zero exit, missing binary, provider retry failure, help,
  interrupt, completion, and max-iteration stop are impossible to miss.
- `--dry-run` clearly shows that Codex was not launched.
- `--history` is readable at 80 columns without horizontal scrolling.
- `--verbose` expands normal execution output and history detail.
- `--plain` emits deterministic unstyled text.
- `--ascii` avoids non-ASCII glyphs.
- `--compact` reduces density without hiding critical information.
- `NO_COLOR`, `TERM=dumb`, non-TTY, redirected output, and non-terminal console
  paths choose plain output by default.
- Explicit `--theme` can override environmental color defaults only where
  documented.
- Invalid theme values fail fast with clear error text.
- SQLite history rows contain raw workflow facts only.
- JSONL events contain raw workflow facts only.
- API keys and secrets are never printed, stored, or emitted.
- Existing history DBs remain readable without migration.
- Prompt contract behavior remains unchanged unless code, tests, README, and
  prompt-contract docs change together.
- The base CLI remains usable without Qt, PySide6, PyQt, qmltermwidget,
  QTermWidget, a graphical display, or an external terminal emulator.
- No reference source, shader, image, icon, font, resource manifest, literal
  color/profile data, or build script is copied into the product.
- All authored files stay ASCII-only with Unix LF line endings.

---

## 16. Anti-Patterns To Avoid

- Do not copy reference source, QML, shader code, shader constants, profile
  JSON, literal colors, images, icons, fonts, resource manifests, terminal
  emulator code, or build scripts.
- Do not make the base CLI require Qt, PySide6, PyQt, qmltermwidget,
  QTermWidget, a graphical display, or an external terminal emulator.
- Do not make operators run Apex Infinite CLI inside another terminal emulator
  to get the upgraded experience.
- Do not let styling alter manager prompts, command normalization, path
  normalization, timeout behavior, DB schema compatibility, or autonomous
  `Next command:` handoffs.
- Do not store styled output, ANSI escapes, Rich markup, frame glyphs, or
  visual tokens in SQLite rows or JSONL events.
- Do not hide errors, timeouts, help pauses, interrupts, non-zero exits, or
  completion states in compact or styled output.
- Do not use wide history tables that require horizontal scrolling at
  80 columns.
- Do not turn primary operator surfaces into debug dashboards. Renderer tests,
  raw event payloads, and frame diagnostics belong in developer surfaces.
- Do not use decorative effects that make text harder to read.
- Do not add brittle full-frame snapshot tests where semantic renderer tests
  would be more stable.
- Do not ship binary screenshots in source docs; use ASCII transcripts or
  deterministic asciinema casts when documentation needs examples.

---

## 17. Assumptions And Conflict Resolutions

### Working Assumptions

- Apex Infinite CLI is terminal-first and operator-facing, not a web or
  marketing surface. Evidence: `PRD.md`, the CLI README, operator runbook, and
  current implementation all describe a Python CLI around manager decisions,
  Codex subprocess execution, SQLite history, and terminal output. It is safe
  to proceed because this UX PRD defines terminal surfaces plus optional wrapper
  surfaces only.
- The first visual milestone should use Rich only. Evidence: Rich is already a
  runtime dependency, the base CLI must stay lightweight, and the functional
  PRD defers graphical dependencies to an optional Linux wrapper. It is safe
  because wrapper-only effects are separated behind the event boundary.
- `auto` should resolve to `crt-green` only for capable interactive terminals
  and to `plain` for constrained output. Evidence: the product PRD and source
  plan both require this fallback model. It is safe because invalid user theme
  configuration still fails fast.
- The reference terminal project informs UX vocabulary but not implementation
  data. Evidence: the reference material is GPL-family and the product PRD
  forbids copying source, shaders, assets, fonts, profile data, or build
  scripts. It is safe because the PRD records clean-room translation boundaries
  as explicit product requirements.
- Operational telemetry is part of the product only when it helps the operator.
  Status strip, elapsed time, timeout, provider/model, manager decision, prompt
  preview, DB log confirmation, and history ledger are primary surfaces because
  the product is an autonomous workflow runner. Renderer internals and raw event
  payload dumps remain developer/debug surfaces.
- The user named the examples source in plural, while the repo's available
  source tree used a singular examples directory. It is safe to use that actual
  local tree as the intended source because it was the only matching local
  source and every detailed reference in the plan pointed there.
- This UX PRD must be self-contained with respect to the source example tree
  and upgrade plan. It is safe because this file embeds the relevant current
  behavior, visual concepts, no-copy boundaries, configuration rules, event
  requirements, wrapper direction, acceptance checks, and open decisions.

### Conflict Resolutions

- The functional PRD defines Phase 00 with 5 sessions and Phase 01 with 2
  sessions, while the detailed upgrade plan includes a broader 8-session
  planning split with release verification. The UX PRD resolves this by
  defining coverage areas and acceptance criteria without making exact session
  numbering authoritative. `phasebuild` owns final phase/session structure.
- The visual source is a full graphical terminal emulator with tabs, menus,
  settings dialogs, shader passes, copied assets, and external submodules,
  while Apex Infinite CLI is a Python workflow manager. The chosen
  interpretation is clean-room visual translation: Rich gets status hierarchy,
  framing, profile-like themes, and low-fidelity separators; the optional Linux
  wrapper later gets event-driven visual effects without depending on the
  reference app, qmltermwidget, or QTermWidget.
- The current CLI already uses Rich but does not yet have the planned UI flags,
  `ui` config, event stream, renderer boundary, compact history ledger, or
  wrapper. This document labels those as planned requirements, not current
  shipped behavior.
- `NO_COLOR` normally means no color, while explicit `--theme` can opt back
  into styled output per the source plan. The chosen interpretation is that
  environmental constraints set safe defaults, while explicit operator choices
  can override them when documented and tested.
- `--event-stream -` is useful for machine pipelines but unsafe if human output
  also goes to stdout. The chosen interpretation is to require an explicit
  human-rendering disable mode before stdout JSONL is allowed.

---

## 18. Open UX Decisions

1. Finalize the exact flag or mode name that disables human rendering when
   `--event-stream -` writes JSONL to stdout.
2. After the Linux wrapper spike, decide whether wrapper productization ships
   with PySide6/QML or is deferred with named blocker evidence.
3. Decide the first optional Linux wrapper release artifact format after
   dependency, packaging, and license evidence is available.
4. Decide whether a true terminal-emulator viewport becomes mandatory. If it
   does, evaluate the documented pywebview plus xterm.js backup path before
   changing the selected wrapper architecture.
