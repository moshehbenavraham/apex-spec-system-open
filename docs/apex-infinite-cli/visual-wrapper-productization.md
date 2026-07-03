# Apex Infinite CLI Visual Wrapper Productization

## Status

Session 07 productizes the optional Linux source visual mode. It does not
publish an AppImage or other binary artifact.

The base terminal CLI remains the workflow engine. The wrapper launches that
CLI with the guarded event-stream command and renders lifecycle state from
JSONL events:

```text
python apex_infinite.py --event-stream - --machine-output ...
```

The wrapper must not parse Rich output, plain terminal text, SQLite history
rows, ANSI captures, or reference terminal frames.

## Source Setup

Install the base CLI first:

```bash
cd apex-infinite-cli
python -m pip install -r requirements.txt
```

Install the optional visual wrapper only when running the Linux visual mode:

```bash
python -m pip install -r requirements-wrapper.txt
```

`requirements-wrapper.txt` includes PySide6 and packaging review tooling in the
optional lane. The base CLI install stays free of Qt, PySide6, QML, graphical
display requirements, Nuitka, AppImage tooling, and wrapper assets.

## Run Commands

Fixture-backed source visual mode:

```bash
cd apex-infinite-cli
python -m apex_infinite_visual.main --dry-run --max-iterations 1
```

Launch the real CLI subprocess from the wrapper:

```bash
python -m apex_infinite_visual.main \
  --launch-cli \
  --path ~/projects/my-app/ \
  --start-command implement \
  --dry-run \
  --max-iterations 1
```

Use the productized visual settings from the command line:

```bash
python -m apex_infinite_visual.main \
  --theme crt-amber \
  --effect-intensity 55 \
  --font-family "monospace" \
  --font-scale 1.05 \
  --reduced-effects \
  --plain-fallback
```

Headless smoke check:

```bash
QT_QPA_PLATFORM=offscreen python -m apex_infinite_visual.main \
  --dry-run --max-iterations 1 --auto-close-ms 300
```

The wrapper sets `QT_QUICK_BACKEND=software` automatically when
`QT_QPA_PLATFORM=offscreen`.

## Settings

The Python settings model owns all productized visual settings:

- `crt-green`, `crt-amber`, `ibm-dos`, and `plain` presets.
- Effect intensity from 0 to 100.
- Font family as non-empty ASCII text.
- Font scale from 0.8 to 1.4.
- Reduced effects, which disables optional effects.
- Plain fallback, which switches to the plain preset and disables effects.

QML consumes settings through the bridge. Normal QML rendering should not own
duplicated preset logic.

## Failure States

The wrapper renders or reports these product-facing states:

| Condition | Surface |
|-----------|---------|
| PySide6 missing | Entrypoint prints `Visual wrapper unavailable` with install guidance. |
| Display backend unavailable | Entrypoint reports a display or Qt runtime unavailable state. |
| Missing base CLI script | QML failure state: `CLI missing`. |
| Invalid project path | QML failure state: `Project unavailable`. |
| Malformed JSONL | QML failure state: `Malformed event`. |
| Subprocess timeout | QML failure state: `Timed out`. |
| Subprocess stderr | QML failure state: `Subprocess stderr`. |
| Non-zero subprocess exit | QML failure state: `Process failed`. |
| Operator stop | QML state: `Stopped`. |

The wrapper keeps stderr separate from stdout JSONL. Stderr is summarized before
display. Event payload validation still excludes secrets, ANSI escapes,
Rich markup, frame glyphs, and visual token values.

## Smoke And Verification

Recommended source checks before release verification:

```bash
cd apex-infinite-cli
./.venv/bin/python -m pytest tests/test_visual_wrapper_spike.py \
  tests/test_visual_wrapper_productization.py -v
./.venv/bin/python -m py_compile \
  apex_infinite_visual/__init__.py \
  apex_infinite_visual/events.py \
  apex_infinite_visual/launcher.py \
  apex_infinite_visual/main.py \
  apex_infinite_visual/settings.py
./.venv/bin/pyside6-qmllint apex_infinite_visual/qml/Main.qml
QT_QPA_PLATFORM=offscreen ./.venv/bin/python -m apex_infinite_visual.main \
  --dry-run --max-iterations 1 --auto-close-ms 300
```

If `pyside6-qmllint` is unavailable because optional wrapper dependencies are
not installed, record that exact environment blocker before release
verification. Do not move PySide6 into `requirements.txt` to make the check
pass.

## Packaging Path

Binary packaging is deferred to release verification. The intended Linux path
is:

1. Build and review the source visual mode.
2. Run `pyside6-deploy` or an explicitly reviewed Nuitka path in an isolated
   packaging workspace.
3. Inspect generated files, collected Qt plugins, and licenses.
4. Wrap the reviewed Linux output as
   `apex-infinite-visual-linux-x86_64.AppImage` only after license review.
5. Publish SHA256 checksums and source/dev install instructions with the
   binary artifact.

Do not commit generated packaging outputs unless a later release session
explicitly scopes them.

## License And Release Gates

Before publishing a binary artifact:

- Confirm the selected Qt for Python license path: LGPLv3-compatible or
  commercial.
- Include required Qt/PySide6 notices.
- Confirm no GPL-only Qt modules are bundled.
- Confirm the AppImage does not block required library replacement or relink
  rights.
- Provide source availability or relink/replacement instructions required by
  the chosen license path.
- Publish SHA256 checksums for the final artifact.
- Keep `requirements.txt` independent of PySide6 and graphical display
  dependencies.

Experienced legal review is recommended when there is doubt about LGPLv3,
commercial Qt terms, generated bundle contents, or AppImage replacement rights.

## Clean-Room Verification

Tracked wrapper source, tests, docs, and release assets must not include copied
reference source code, QML, shaders, shader constants, generated shader blobs,
images, icons, fonts, profile data, resource manifests, build scripts,
terminal-emulator code, qmltermwidget, or QTermWidget material.

Use these checks during implementation and release verification:

```bash
git ls-files | grep '^EXAMPLE/' && exit 1 || true
LC_ALL=C grep -RInP '[^\x00-\x7F]' apex_infinite_visual docs/apex-infinite-cli || true
git diff --check
```

The local `EXAMPLE/` tree remains ignored reference material only. It is not a
runtime dependency and not a source for implementation details.

## Session 08 Handoff

Session 08 owns final release verification. It should decide whether packaging
uses `pyside6-deploy`, direct Nuitka invocation, or a different reviewed path,
then verify generated bundle contents, AppImage behavior, notices, checksums,
source/relink instructions, and clean-room boundaries before any artifact is
published.
