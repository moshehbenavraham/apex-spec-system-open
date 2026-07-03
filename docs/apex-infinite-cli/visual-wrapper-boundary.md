# Apex Infinite CLI Visual Wrapper Boundary

## Purpose

This document defines the clean-room boundary for the optional Linux visual
wrapper path. It exists so future wrapper work can study visual concepts
without copying implementation material from local reference projects or adding
graphical dependencies to the base terminal CLI.

The base CLI remains a headless-safe Python terminal tool. The visual wrapper,
if productized later, is a companion surface for the same workflow engine.

## Source Of Truth

Authoritative product and implementation rules live in:

- `.spec_system/PRD/PRD_UX.md`
- `.spec_system/PRD/phase_00/PRD_phase_00.md`
- `.spec_system/CONVENTIONS.md`
- `.spec_system/SECURITY-COMPLIANCE.md`
- `.spec_system/CONSIDERATIONS.md`
- `docs/apex-infinite-cli/event-stream.md`

The local `EXAMPLE/` tree is not a source dependency. It is an ignored,
reference-only study tree.

## Ignored Reference Tree

The repository `.gitignore` excludes:

```text
/EXAMPLE/
```

The local path `EXAMPLE/cool-retro-term/` may exist on a developer machine.
Treat it as GPL-family reference material for conceptual study only. Do not
commit files from that tree and do not make runtime behavior depend on it.

Reference files that were considered during planning include README, GPL
license files, packaging metadata, QML files, shader-related files, resource
manifests, images, icons, profile data, build scripts, and terminal-widget
submodules. Their presence is evidence for what must stay outside this
codebase, not a source for implementation.

## Allowed Concept Translation

Future Apex Infinite CLI work may translate broad concepts into independent
implementation:

- Operator-console mood, hierarchy, and status language.
- Theme families such as green, amber, DOS-like, and plain.
- Settings groups such as profile, screen, terminal, effects, advanced,
  performance, import/export, and persistence.
- Render pipeline ideas such as source events, static display state, dynamic
  effects, final frame treatment, and fallback paths.
- Effect categories such as glow, scanlines, flicker, curvature, bloom,
  ambient light, low-effects mode, scaling, font controls, and reduced motion.

Every translated element must use independently chosen names, colors, data
models, layouts, code, assets, and tests.

## Forbidden Copying

Do not copy, vendor, transcribe, adapt mechanically, or derive implementation
from reference material in any of these categories:

- Source code.
- QML files or component structures.
- Shader code, shader constants, generated shader blobs, or texture data.
- Image assets, icons, fonts, and profile files.
- Resource manifests and build scripts.
- Packaging manifests or desktop files.
- Terminal-emulator code, terminal-widget code, or submodule contents.
- Literal effect formulas, color tables, profile values, or settings schemas.

This no-copy rule applies to the base CLI, optional wrapper, tests, docs,
examples, transcripts, screenshots, and generated release assets.

## Base CLI Boundary

The base CLI must stay terminal-only and lightweight. Do not add these to the
base CLI runtime path:

- Qt, PySide6, PyQt, pywebview, xterm.js, or GUI framework imports.
- qmltermwidget, QTermWidget, copied terminal widgets, or embedded terminal
  emulator code.
- QML, shader, image, icon, font, or graphical resource files.
- Display-server requirements or graphical startup checks.

The base CLI owns workflow behavior:

- Manager and summarizer prompts.
- Command normalization and `build_codex_prompt()`.
- Codex subprocess execution.
- SQLite history writes and reads.
- Interrupts, help pauses, completion, max-iteration stops, and errors.
- Human terminal rendering and plain fallbacks.
- JSONL event emission.

Visual surfaces display this state. They do not fork or replace it.

## Selected Wrapper Direction

The selected optional Linux wrapper direction is PySide6 with Qt Quick/QML.
This direction is for future wrapper sessions, not the current base CLI.

Expected wrapper shape:

- Launch or reuse the Python CLI workflow engine.
- Consume `--event-stream PATH` JSONL or the importable event API.
- Keep stdout/stderr handling separate from machine events.
- Provide a read-only operator log viewport and status panels.
- Offer theme, effect intensity, font, scaling, reduced-effects, and plain
  fallback controls.
- Detect unsupported graphics paths and fall back to a low-effects scene.
- Keep packaging, checksums, license notices, and source/dev install steps
  separate from base CLI installation.

Before release, document PySide6 LGPLv3/commercial obligations and confirm
which Qt modules are used.

## Exclusions

Do not use PyQt unless a later explicit license decision changes the scope.
Do not use qmltermwidget or QTermWidget as the selected wrapper path. Do not
embed a copied terminal emulator. Do not make a wrapper parse Rich frames,
plain human output, history display rows, ANSI output, or terminal-control
sequences as state.

The wrapper state boundary is:

```text
CLI workflow facts -> JSONL events or importable event API -> wrapper state
```

It is not:

```text
Rich panel text -> scraper -> wrapper state
plain history rows -> parser -> wrapper state
reference terminal emulator -> copied implementation -> wrapper state
```

## Backup Option

pywebview plus xterm.js is a backup only if a future spike proves that a true
terminal-emulator viewport is mandatory. That backup still must be optional,
license-reviewed, isolated from the base CLI, and event-driven for workflow
state.

## Documentation And Sample Rules

Tracked docs and samples may include Markdown, plain text, JSONL, and other
small ASCII fixtures that describe behavior. They must not include:

- Binary screenshots.
- ANSI escape captures.
- Rich markup snapshots.
- QML, shaders, image data, icons, fonts, or copied resource files.
- Real provider keys, operator secrets, private project paths, or customer
  data.

Use deterministic text transcripts under `docs/apex-infinite-cli/transcripts/`
when a visual example is needed.

## Future Wrapper Checklist

Before starting wrapper implementation:

- Re-read this document, the UX PRD, and the event-stream contract.
- Prove the required state exists in events or the importable API.
- Add missing events in the base CLI before writing wrapper-specific state
  scrapers.
- Keep wrapper dependencies in optional requirements only.
- Record license obligations and packaging assumptions.
- Verify low-effects and plain fallbacks.
- Confirm no copied reference material is tracked with `git ls-files`.

## Related Docs

- [Event stream contract](event-stream.md)
- [Operator runbook](operator-runbook.md)
- [Troubleshooting guide](troubleshooting.md)
- [Transcript samples](transcripts/README.md)
