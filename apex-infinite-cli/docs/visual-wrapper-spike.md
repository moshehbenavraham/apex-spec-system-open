# Apex Infinite CLI Visual Wrapper Spike

## Decision

Session 06 accepts PySide6 with Qt Quick/QML as the prototype path for the
optional Linux visual wrapper.

Session 07 may productize this path if it keeps the current boundaries:

- PySide6, QML, graphical startup checks, and wrapper packaging remain outside
  the base terminal CLI runtime path.
- Wrapper state comes from Apex Infinite CLI JSONL events, not Rich panels,
  plain human output, terminal frames, SQLite history display rows, or ANSI
  captures.
- The wrapper remains Linux-only for this phase.
- The release plan must complete license-notice, source, relink/replacement,
  and packaging compliance review before publishing a binary.

## Prototype Evidence

Implemented prototype files:

- `apex-infinite-cli/src/apex_infinite_visual/__init__.py`
- `apex-infinite-cli/src/apex_infinite_visual/events.py`
- `apex-infinite-cli/src/apex_infinite_visual/launcher.py`
- `apex-infinite-cli/src/apex_infinite_visual/main.py`
- `apex-infinite-cli/src/apex_infinite_visual/qml/Main.qml`

The prototype provides:

- A read-only event log derived from JSONL lifecycle events.
- Status panels for run status, stage, iteration, provider, model, and manager
  decision.
- Start, stop, dry-run, project path, start-command, and max-iteration
  controls.
- Theme selection for `crt-green`, `crt-amber`, `ibm-dos`, and `plain`.
- Local glow, scanline, flicker, and curvature controls.
- Reduced-effects fallback that disables animated/effect overlays.
- Offscreen dry-run fixture mode for smoke testing without provider keys or
  live Codex execution.
- Explicit error state for malformed JSONL, subprocess stderr, non-zero return
  codes, wrapper exceptions, and stop events.

Verification performed during the spike:

```bash
cd apex-infinite-cli
./.venv/bin/python -m py_compile \
  src/apex_infinite_visual/__init__.py \
  src/apex_infinite_visual/events.py \
  src/apex_infinite_visual/launcher.py \
  src/apex_infinite_visual/main.py

QT_QPA_PLATFORM=offscreen ./.venv/bin/apex-infinite-visual \
  --dry-run --max-iterations 1 --auto-close-ms 300

LC_ALL=C grep -RInP '[^\x00-\x7F]' src/apex_infinite_visual || true
```

Results:

- Python wrapper modules compile.
- Offscreen PySide6/QML smoke check exits cleanly.
- Wrapper Python and QML files are ASCII-only.
- PySide6 imports from the CLI virtualenv as version `6.11.1`.

## Runtime Boundary

The base CLI remains unchanged for this spike. The wrapper package is imported
only when explicitly invoked:

```bash
cd apex-infinite-cli
apex-infinite-visual --dry-run --max-iterations 1
```

To launch the real base CLI subprocess from the prototype, use:

```bash
cd apex-infinite-cli
apex-infinite-visual \
  --launch-cli \
  --path ~/projects/my-app/ \
  --start-command implement \
  --dry-run \
  --max-iterations 1
```

The launch helper builds this guarded command shape:

```text
apex-infinite --path <project> --event-stream - --machine-output ...
```

Stdout is reserved for JSONL. Stderr remains separate for wrapper failure
display. The wrapper does not require or inspect human terminal output.

## Event Contract

The prototype consumes event schema version `1` from
`apex_infinite.events`. It validates:

- event line is a JSON object
- `version` is the supported integer version
- `event` is in the current event registry
- `timestamp` is text
- `payload` is a JSON object accepted by the base event payload validator

Malformed input does not crash the UI. It becomes an explicit wrapper error
state and a log entry.

The adapter maps the current event family into wrapper state:

- startup and configuration
- project resolution
- iteration lifecycle
- history summary
- manager decision
- prompt dispatch
- Codex dry-run, start, finish, error, and timeout
- DB log start/finish
- workflow completion
- max-iteration and stop states
- event-stream and generic errors

## Clean-Room Evidence

The QML prototype is independently implemented. It does not copy or depend on
reference QML, shaders, shader constants, generated shader blobs, images,
icons, fonts, profiles, resource manifests, build scripts, terminal emulator
code, qmltermwidget, or QTermWidget.

The local `/EXAMPLE/` tree remains ignored reference material. It was not used
as a source dependency.

The visual effects are low-risk local QML constructs:

- a faint full-window glow rectangle
- a simple repeated scanline overlay
- a small opacity flicker animation
- curvature represented by panel radius changes

No shader code or texture assets are included.

## Dependency And License Assessment

The optional wrapper dependency surface is:

```text
the `visual` optional dependency extra in `pyproject.toml`
```

It keeps graphical dependencies out of the base dependency set.

Current sources checked:

- Qt for Python commercial use:
  <https://doc.qt.io/qtforpython-6/commercial/index.html>
- PySide6 package metadata:
  <https://pypi.org/project/PySide6/>
- Qt for Python `pyside6-deploy`:
  <https://doc.qt.io/qtforpython-6/deployment/deployment-pyside6-deploy.html>
- Nuitka license note:
  <https://nuitka.net/doc/download.html#license>
- Riverbank PyQt commercial FAQ:
  <https://riverbankcomputing.com/commercial/license-faq>

PySide6 status:

- Qt for Python has Community Edition licensing under LGPLv3/GPLv3 and a
  Commercial Edition.
- PyPI metadata for PySide6 lists open source licensing as LGPLv3 or GPLv2 or
  GPLv3, plus commercial licensing.
- Productization should use the LGPLv3-compatible path only after legal review,
  or use commercial Qt for Python packages if the distribution model requires
  that.

Minimum release obligations to verify before binary distribution:

- Include required Qt/PySide6 license notices.
- Include source-offer or relink/replacement instructions required by the
  chosen Qt/PySide6 license path.
- Confirm the packaged Qt modules are not GPL-only modules.
- Confirm the AppImage or other bundle does not block required library
  replacement rights.
- Keep wrapper source and dependency installation instructions available.
- Keep base CLI installation independent of PySide6.

Nuitka and `pyside6-deploy` status:

- Qt documents `pyside6-deploy` as a wrapper around Nuitka.
- Qt documents Linux output from `pyside6-deploy` as a `.bin` executable.
- Nuitka documents AGPLv3 licensing and an exception for created binaries so
  the user's code and binaries are not bound by AGPLv3 solely by compiling with
  Nuitka.
- Productization still needs a packaging review because `pyside6-deploy` may
  generate `pysidedeploy.spec`, collect Qt plugins, and alter bundled
  dependency contents.

PyQt exclusion:

- PyQt remains excluded. Riverbank's commercial FAQ makes PyQt distribution a
  separate commercial-license decision for proprietary distribution.
- Do not switch to PyQt without a future explicit license decision.

## Packaging Risks

Session 07 must resolve these before release:

- Qt platform plugin availability for X11, Wayland, and headless smoke paths.
- QML import/plugin collection for AppImage builds.
- AppImage contents, license notices, and source/relink instructions.
- Binary size and startup time from bundling Qt and Python.
- Whether `pyside6-deploy` generated files are stable enough for CI.
- Whether direct Nuitka invocation is more predictable than `pyside6-deploy`.
- Whether a `.bin` from `pyside6-deploy` should be wrapped into
  `apex-infinite-visual-linux-x86_64.AppImage`.
- Whether offscreen smoke tests should run in CI with `QT_QPA_PLATFORM=offscreen`
  and `QT_QUICK_BACKEND=software`.

## qmltermwidget And QTermWidget

The selected prototype does not use qmltermwidget or QTermWidget.

No true terminal emulator viewport is required for the current product shape.
The wrapper displays workflow state from events and a read-only operational log.
That is enough for the Session 06 spike and avoids terminal-widget licensing,
maintenance, and clean-room risk.

## pywebview Plus xterm.js Backup

pywebview plus xterm.js remains a backup only if Session 07 proves a true
terminal-emulator viewport is mandatory.

Reopen criteria for the backup:

- Event-driven read-only logs cannot satisfy an accepted product requirement.
- The requirement truly needs terminal emulation semantics such as shell
  control sequences, selection behavior, alternate screen, or pseudo-terminal
  interaction.
- A license review accepts pywebview, browser runtime, xterm.js, and packaging
  obligations.
- The workflow state still comes from JSONL events, not terminal scraping.

## Session 07 Recommendation

Proceed with PySide6/QML productization, with these constraints:

- Keep the base CLI dependency boundary unchanged.
- Add automated tests for parser, launcher, import guard, fixture flow, and
  smoke launch.
- Add a CI-friendly offscreen smoke check if PySide6 is available.
- Decide AppImage packaging only after license and generated-bundle review.
- Keep qmltermwidget, QTermWidget, PyQt, copied QML, copied shaders, copied
  images, copied icons, copied fonts, copied profiles, copied resource
  manifests, copied build scripts, and copied terminal-emulator code excluded.
