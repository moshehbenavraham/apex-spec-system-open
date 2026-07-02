# Apex Infinite CLI Upgrade Plan

Status: proposed

## Goal

Upgrade `apex-infinite-cli` from a functional autonomous loop runner into a
polished operator console for long-running Apex Spec workflows.

The highest-priority improvement is the look and feel. The CLI should still be
fast, readable, scriptable, and safe to run unattended, but its default
interactive experience should feel intentional instead of like raw diagnostic
output.

## Visual Direction

Take look inspiration directly from
[Swordfish90/cool-retro-term](https://github.com/Swordfish90/cool-retro-term).
The target is a retro CRT operator console mood: amber and green phosphor theme
presets, IBM DOS style contrast, compact status readouts, strong terminal
framing, and subtle scanline-like separation.

This is visual inspiration only. Do not copy `cool-retro-term` code, shaders,
images, fonts, themes, or bundled assets.

The work has two visual milestones:

1. First pass: implement a standalone Rich-based terminal experience that
   captures the operator-console layout, colors, framing, and status language.
2. Soon after: build a standalone Linux-only Qt/QML wrapper or equivalent
   renderer for the visual effects Rich cannot provide, such as glow, screen
   curvature, flicker, and shader-like scanlines.

Do not require users to run `apex-infinite-cli` inside `cool-retro-term`. The
upgraded experience must remain standalone.

## Local cool-retro-term Feature Reference Map

The local reference copy is ignored by Git and exists only for visual study:

- Local root:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term`
- README and visual overview:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/README.md`
- License boundary for the reference project:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-2.0.txt`
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/gpl-3.0.txt`

Use these paths for analysis only. Do not copy source code, shader code,
compiled shader blobs, image assets, font assets, profile JSON, or resource
manifests into `apex-infinite-cli`.

### Visual Feature Sources

| Feature area | What to study | Local full path references |
|--------------|---------------|----------------------------|
| Application shell | QML application root, window creation, global settings, time driver | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/main.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml` |
| Built-in profiles | Amber, green, DOS-like, IBM, and other theme presets; study the grouped choices, not the literal values | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml` |
| Settings window | Profile, screen, terminal, effects, advanced, import, and export organization | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml` |
| Theme color controls | Font, background, frame color, chroma, saturation, brightness, contrast | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ColorButton.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/utils.js` |
| CRT effects controls | Bloom, burn-in, static noise, jitter, glow line, curvature, ambient light, flicker, horizontal sync, RGB shift, frame shininess | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml` |
| Performance controls | Effects FPS, texture quality, bloom quality, burn-in quality | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsAdvancedTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TimeManager.qml` |
| Terminal viewport | PTY terminal, scroll bar, font handling, selection, paste, mouse, wheel, focus, corrected mouse coordinates under distortion | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/qmltermwidget` |
| Render pipeline | Preprocessed terminal source, bloom source, dynamic shader pass, static shader pass, frame buffer | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalContainer.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/PreprocessedTerminal.qml` |
| Burn-in trail | Burn-in source accumulation, update timing, quality scaling | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/BurnInEffect.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.vert` |
| Screen frame | Physical monitor frame color, ambient light, curvature, radius, frame size, shininess | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.vert` |
| Dynamic CRT shader | Rasterization, burn-in overlay, display frame influence, chroma, flicker, horizontal sync, glow line, jitter, static noise | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert` |
| Static CRT shader | RGB shift, bloom, screen curvature, frame shininess, brightness, final composition | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ShaderTerminal.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.vert` |
| Compiled shader variants | Qt Shader Baker output for raster, burn-in, frame, chroma, RGB shift, bloom, curvature, and shine combinations | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc` |
| Noise and texture assets | Static noise texture and CRT image reference | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/allNoise512.png`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/images/crt256.png` |
| Font source and rendering modes | Bundled vs system fonts, default/scanline/pixel/subpixel/modern rasterization, scaling, width, line spacing | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.cpp`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontmanager.h`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.cpp`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fontlistmodel.h`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsTerminalTab.qml` |
| Menus and profile switching | Context menu, menu bar, profile menu, copy/paste/settings/fullscreen/zoom/new tab actions | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/FullContextMenu.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/ShortContextMenu.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/menus/WindowMenu.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml` |
| Tabs and window controls | New tab, close tab, title normalization, fullscreen, size overlay, zoom shortcuts | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalTabs.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalWindow.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml` |
| Profile persistence | Settings storage, custom profile import/export, file IO bridge | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Storage.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.cpp`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/fileio.h` |
| Dialog and small controls | About dialog, profile naming dialog, sliders, checkable sliders, sized labels | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/AboutDialog.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/InsertNameDialog.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SimpleSlider.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/CheckableSlider.qml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/Components/SizedLabel.qml` |
| Qt resource manifest | QML, images, fonts, icons, and compiled shader inclusion | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc` |
| Linux build and packaging | Qt modules, qmake build, shader baking, Linux icon install, desktop entry, Snap packaging reference | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.pro`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/app.pro`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/cool-retro-term.desktop`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/snap/snapcraft.yaml`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/scripts/build-appimage.sh` |
| Icons | Linux desktop/app icon shape and sizes | `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/32x32/cool-retro-term.png`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/64x64/cool-retro-term.png`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/128x128/cool-retro-term.png`, `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/icons/256x256/cool-retro-term.png` |

### Built-In Profile Reference

The local copy defines these built-in profile names in
`/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`.
Use them as a checklist for visual moods, not as data to copy:

- Default Amber
- Monochrome Green
- Deep Blue
- Commodore 64
- Commodore PET
- Apple ][
- Atari 400
- IBM VGA 8x16
- IBM 3278 Reborn
- Neon Cyan
- Ghost Terminal
- Plasma
- Boring
- E-Ink

### Shader Source Reference

Study the shader source categories at these full paths:

- Burn-in fragment:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.frag`
- Burn-in vertex:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/burn_in.vert`
- Pass-through vertex:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/passthrough.vert`
- Dynamic terminal fragment:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`
- Dynamic terminal vertex:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.vert`
- Terminal frame fragment:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.frag`
- Terminal frame vertex:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_frame.vert`
- Static terminal fragment:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.frag`
- Static terminal vertex:
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_static.vert`

Compiled `.qsb` shader blobs are reference artifacts only. They live in
`/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders`
and are enumerated in
`/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/resources.qrc`.

### Bundled Font Asset Reference

Do not copy these fonts or their licenses. Use them to understand the visual
range of CRT and old-computer typography:

- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/apple2/PRNumber3.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/apple2/PrintChar21.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/atari-400-800/AtariClassic-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/bigblue-terminal/BigBlueTerm437NerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/cozette/CozetteVector.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/departure-mono/DepartureMonoNerdFontMono-Regular.otf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/fira-code/FiraCodeNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/fixedsys-excelsior/FSEX301-L2.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/gohu/GohuFont11NerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/greybeard/Greybeard-12px.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/greybeard/Greybeard-16px.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/hack/HackNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/ibm-3278/3270NerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/iosevka/IosevkaTermNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/jetbrains-mono/JetBrainsMonoNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/oldschool-pc-fonts/PxPlus_IBM_EGA_8x8.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/oldschool-pc-fonts/PxPlus_IBM_VGA8.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/oldschool-pc-fonts/PxPlus_IBM_VGA_8x16.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/opendyslexic/OpenDyslexicMNerdFontMono-Regular.otf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/pet-me/PetMe.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/pet-me/PetMe64.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/source-code-pro/SauceCodeProNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/terminus/TerminessNerdFontMono-Regular.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/unscii/unscii-16-full.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/unscii/unscii-8-thin.ttf`
- `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/fonts/unscii/unscii-8.ttf`

### Rich Milestone Translation Targets

The first Rich milestone can translate only these local reference ideas:

- Color mood, contrast, and profile naming from
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/ApplicationSettings.qml`.
- Operator settings grouping from
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsWindow.qml`.
- Frame, margin, status, and size-overlay concepts from
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/TerminalFrame.qml`,
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsGeneralTab.qml`,
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SizeOverlay.qml`.
- Low-fidelity scanline/noise suggestion from
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/qml/SettingsEffectsTab.qml`
  and
  `/home/aiwithapex/projects/apex-spec-system-open/EXAMPLE/cool-retro-term/app/shaders/terminal_dynamic.frag`.

The Linux wrapper milestone is responsible for features that require a real
rendering layer: glow, bloom, curvature, burn-in trails, flicker, shader
scanlines, RGB shift, and frame shine.

## Design Principles

- Prioritize legibility over novelty.
- Make the retro look configurable and easy to disable.
- Preserve unattended automation and plain terminal output behavior.
- Keep source files ASCII-only and LF-only.
- Prefer the existing `rich` dependency before adding new dependencies.
- Provide a low-effects fallback for CI, log files, dumb terminals, and
  `NO_COLOR` environments.
- Treat every visual element as operational information, not decoration.
- Treat the Linux visual wrapper as a companion execution surface for the same
  autonomous engine, not a fork of workflow behavior.

## Target Experience

The upgraded CLI should feel like a mission-control terminal for autonomous
development sessions:

- Startup shows a compact boot screen with project, provider, model, config,
  max iterations, dry-run state, and selected theme.
- Each iteration renders as a framed cycle with stable sections: history,
  manager decision, prompt, Codex execution, result, log write, and next wait.
- Active work uses a live status line with elapsed time and subprocess state.
- Manager decisions are visually distinct from Codex output.
- Errors and operator interrupts are impossible to miss without overwhelming
  normal output.
- History mode becomes a readable operations ledger, not just a wide table.

## Scope

In scope:

First Rich milestone:

- Theme tokens for colors, emphasis, borders, and status states.
- Built-in themes: `crt-green`, `crt-amber`, `ibm-dos`, and `plain`.
- Centralized rendering helpers around `rich.console.Console`.
- Improved startup banner, iteration frame, decision panel, output panel, and
  history view.
- Config support for theme selection and effect level.
- CLI flags for theme and plain/ascii output.
- Documentation and screenshots or terminal recordings.
- Tests for rendering paths, config parsing, and plain output behavior.

Soon-future Linux visual milestone:

- A standalone Linux-only Qt/QML wrapper or equivalent renderer.
- Reuse of the existing Python CLI as the workflow engine or subprocess target.
- CRT effects that Rich cannot faithfully render: glow, curvature, flicker,
  phosphor trails, and full-viewport scanline overlays.
- Packaging notes for Linux distribution, local development, and operator use.

Out of scope:

- Replacing Codex CLI.
- Requiring `cool-retro-term` or any external terminal emulator at runtime.
- Copying `cool-retro-term` implementation details or assets.
- Rewriting the manager or summarizer prompt contract unless UI changes require
  clearer display metadata.
- Shipping macOS or Windows visual-wrapper support in this project.

## Proposed Configuration

Add a `ui` section to `apex-infinite-cli/config.yaml`:

```yaml
ui:
  theme: "crt-green"       # crt-green | crt-amber | ibm-dos | plain
  effect_level: "low"      # off | low | medium
  ascii: false
  compact: false
  show_elapsed: true
  show_provider: true
```

Add command-line overrides:

```bash
python apex_infinite.py --theme crt-amber
python apex_infinite.py --plain
python apex_infinite.py --ascii
python apex_infinite.py --compact
```

`--plain` should disable color and effects. `--ascii` should avoid box-drawing
glyphs where possible. `NO_COLOR` should behave like `--plain` unless the user
explicitly opts back into a theme.

## Implementation Sessions

### Session 1: UI Architecture And Theme Tokens

Objective: create the rendering foundation without changing workflow behavior.

Tasks:

- Add a small renderer module or internal renderer section that owns all
  operator-facing `rich` output.
- Define theme token data for color names, border styles, emphasis, status
  labels, warning labels, and muted text.
- Move startup banner, history table, iteration banner, decision output, and
  agent response panels through renderer helpers.
- Add config parsing for `ui.theme`, `ui.effect_level`, `ui.ascii`, and
  `ui.compact`.
- Add CLI overrides for `--theme`, `--plain`, `--ascii`, and `--compact`.
- Add tests for config defaults, CLI overrides, and unknown theme fallback.

Acceptance:

- Existing commands still work with the default config.
- `--history`, `--dry-run`, and direct execution still function.
- The default output path is visually changed only through renderer helpers.

### Session 2: CRT-Inspired Operator Console

Objective: implement the first complete visual pass inspired by
`cool-retro-term`.

Tasks:

- Add `crt-green`, `crt-amber`, and `ibm-dos` theme presets.
- Redesign the startup banner as a compact boot/status panel.
- Replace the plain iteration separator with a stable iteration frame.
- Add a small status strip for provider, model, project, iteration, elapsed
  time, dry-run state, and current operation.
- Distinguish manager decisions, Codex prompts, agent output, errors, and
  database writes with consistent labels.
- Add subtle scanline-like separators using plain repeated characters, with
  automatic disablement in `plain`, `ascii`, and compact modes.
- Ensure terminal width handling works at 80, 100, and 120 columns.

Acceptance:

- The normal interactive run presents a cohesive retro terminal look.
- The visual direction clearly references `cool-retro-term` without copying any
  external assets.
- Output remains readable in narrow terminals and under color-disabled modes.

### Session 3: Live Execution And Better History

Objective: improve operator awareness during long-running Codex subprocesses.

Tasks:

- Use `rich.status.Status`, `rich.progress`, or `rich.live.Live` for elapsed
  subprocess display when stdout is captured.
- Show command timeout, elapsed time, and process state during `codex exec`.
- Redesign `--history` as a compact ledger with command, reason, timestamp,
  status, and truncated response summary.
- Add `--history --verbose` or equivalent detail mode for full stored records.
- Keep the SQLite schema backward compatible.
- Add tests for history formatting with empty, short, and long records.

Acceptance:

- Operators can tell whether Codex is still running and how long it has been
  running.
- History mode is useful on a normal terminal without horizontal scrolling.
- Existing `~/.apex-infinite/history.db` files remain readable.

### Session 4: Documentation, Samples, And Polish

Objective: make the upgrade easy to understand and maintain.

Tasks:

- Update `apex-infinite-cli/README-apex-infinite-cli.md` with UI flags,
  config examples, and theme descriptions.
- Update the operator runbook with recommended theme settings and plain-output
  guidance for CI or remote shells.
- Add terminal screenshots or asciinema recordings if the repo accepts them.
- Document the visual inspiration from
  `https://github.com/Swordfish90/cool-retro-term` and the no-copying
  constraint.
- Add a troubleshooting entry for unreadable colors, non-UTF terminals, and
  `NO_COLOR`.
- Run the existing test suite and add focused rendering/config tests.

Acceptance:

- Users can discover and configure the new look from the README.
- Operators have clear fallback instructions when a terminal renders poorly.
- The upgrade is documented without changing the Apex Spec workflow contract.

### Session 5: Linux Visual Wrapper Spike

Objective: prove the standalone Linux visual-wrapper approach without changing
the autonomous workflow engine.

Tasks:

- Evaluate a Linux-only Qt/QML wrapper and one equivalent renderer option.
- Decide whether the wrapper launches the Python CLI as a subprocess, embeds a
  pseudo-terminal, or calls a separated Python engine API.
- Prototype a window with a terminal viewport, theme selector, and enough CRT
  effects to validate glow, scanlines, flicker, and curvature feasibility.
- Confirm the prototype does not depend on `cool-retro-term` at runtime.
- Document build dependencies, packaging risks, and the interface contract
  between the wrapper and `apex_infinite.py`.
- Keep all prototype code isolated from the Rich milestone until the approach is
  accepted.

Acceptance:

- A standalone Linux prototype can launch or display an Apex Infinite session.
- The prototype demonstrates visual effects that cannot be done well in Rich.
- The prototype uses `cool-retro-term` only as visual reference material.
- The team has enough evidence to choose Qt/QML, another renderer, or defer the
  wrapper.

### Session 6: Linux Visual Wrapper Productization

Objective: turn the accepted prototype into the near-future standalone visual
mode.

Tasks:

- Implement the selected Linux-only wrapper in a maintainable directory
  structure.
- Add a stable process or API boundary to the Python workflow engine.
- Add theme presets inspired by amber CRT, green CRT, and IBM DOS visuals.
- Add user controls for effect intensity, font, scaling, and plain fallback.
- Add packaging instructions for Linux development and release artifacts.
- Add smoke tests for wrapper launch, CLI subprocess invocation, and failure
  display.

Acceptance:

- Users can run the standalone visual mode without installing or launching
  `cool-retro-term`.
- The visual mode preserves the same workflow decisions and safety behavior as
  the CLI.
- Linux setup and troubleshooting docs are complete enough for operators.

## Testing Plan

- Run `pytest tests/ -v` from `apex-infinite-cli/`.
- Use `Console(record=True)` tests for representative rendered output.
- Validate 80, 100, and 120 column widths.
- Exercise `--dry-run`, `--history`, `--verbose`, `--plain`, `--ascii`, and
  every built-in theme.
- Verify `NO_COLOR=1` disables color unless explicitly overridden.
- Confirm source files remain ASCII-only and LF-only.
- Smoke test with a real initialized Apex Spec project and a very small
  `--max-iterations` value.

## Risks And Mitigations

| Risk | Mitigation |
|------|------------|
| Retro styling reduces readability | Keep contrast high, make effects low by default, and provide `--plain` |
| Terminal compatibility varies | Add `--ascii`, respect `NO_COLOR`, and test common widths |
| Output becomes hard to parse in logs | Keep plain mode stable and avoid hiding important text behind live-only views |
| Dependency creep | Finish the Rich milestone first; isolate Linux wrapper dependencies |
| GPL contamination concerns | Use `cool-retro-term` only as visual inspiration; do not copy code or assets |
| Snapshot tests become brittle | Test semantic output markers and config behavior more than exact full frames |
| Wrapper diverges from CLI behavior | Keep one workflow engine and make the wrapper a display/runtime shell |

## Open Decisions

- Should the default theme change to `crt-green`, or should the first release
  keep current styling and require `--theme crt-green`?
- Should the Linux visual wrapper be Qt/QML, a webview/canvas renderer, or
  another native rendering approach?
- Should the wrapper launch the Python CLI as a subprocess or call a separated
  Python engine API?
- Should terminal recordings be committed to the repo, linked from releases, or
  generated only for docs?
- Should theme presets be hardcoded Python data or user-editable YAML?

## Completion Criteria

This project is complete when:

- The CLI has a coherent CRT-inspired default or opt-in look.
- The look directly references `cool-retro-term` as inspiration in docs.
- Users can disable styling cleanly for automation and constrained terminals.
- All existing workflow behavior remains compatible.
- Tests cover config parsing, renderer behavior, history output, and plain mode.
- The CLI README and deep-dive docs describe the new UI controls.
- The near-future Linux wrapper path is documented as standalone and not
  dependent on running inside `cool-retro-term`.
