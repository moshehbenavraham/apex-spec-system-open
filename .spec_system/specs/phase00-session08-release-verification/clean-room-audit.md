# Clean-Room Audit

**Session ID**: `phase00-session08-release-verification`
**Status**: Complete
**Last Updated**: 2026-07-03 06:43

---

## Boundary Summary

The `EXAMPLE/cool-retro-term/` tree is reference-only material. Product work may
use independent concepts such as terminal mood, status hierarchy, operator
controls, and effect categories. Product work must not copy reference source,
QML, shader code, compiled shader blobs, images, icons, fonts, profile data,
resource manifests, build scripts, GPL code, or terminal-emulator code.

---

## Audit Matrix

| Boundary | Evidence Task | Method | Status |
|----------|---------------|--------|--------|
| `EXAMPLE/` reference material is not tracked in product files. | T016 | `git ls-files` and path scan | PASS |
| Base CLI stays free of PySide6, Qt Quick, QML, and display-server imports. | T008, T018 | requirements and base CLI import scan | PASS |
| Wrapper dependencies stay optional and documented separately. | T008, T018 | `requirements-wrapper.txt` and docs audit | PASS |
| PySide6 LGPLv3/commercial obligations are documented before binary release. | T008, T017, T020 | wrapper productization docs and security posture audit | PASS; binary gated |
| Binary artifacts remain gated by packaging, checksum, notices, and source/relink evidence. | T008, T020 | release documentation and security posture audit | PASS; binary gated |
| No copied QML, shader, image, icon, font, profile data, resource manifest, build script, or GPL code was added. | T016 | tracked-file no-copy keyword and path scans | PASS |
| Event stream and wrapper use raw JSONL/API facts, not scraped terminal frames. | T013, T017 | event smoke and docs audit | PASS |

---

## Boundary Confirmation

| Check | Result | Evidence |
|-------|--------|----------|
| Reference tree ignored | PASS | `.gitignore` contains `/EXAMPLE/`; local `EXAMPLE/cool-retro-term/` exists only as ignored reference material. |
| Forbidden-copy rules documented | PASS | `visual-wrapper-boundary.md` defines forbidden source, QML, shader, asset, font, profile, resource, build-script, and terminal-emulator copying. |
| Optional dependency lane documented | PASS | `visual-wrapper-productization.md` keeps `requirements-wrapper.txt` separate and says not to move PySide6 into `requirements.txt`. |
| License gates documented | PASS | Wrapper productization docs list LGPLv3/commercial review, notices, AppImage replacement/relink, source availability, and SHA256 gates. |
| Base CLI dependency boundary | PASS | Scan of `requirements.txt`, `apex_infinite.py`, `apex_infinite_events.py`, and `apex_infinite_ui.py` found no PySide6, Qt Quick, QML, wrapper, or Nuitka references. |
| Security posture input | PASS | `.spec_system/SECURITY-COMPLIANCE.md` records clean-room and optional wrapper findings that T020 must refresh after verification. |

---

## Scans

Boundary confirmation completed in T004. Full tracked-file no-copy scans ran in
T016.

| Scan | Result | Evidence |
|------|--------|----------|
| Tracked `EXAMPLE/` paths | PASS | `git ls-files | grep '^EXAMPLE/' || true` produced no output. |
| Reference path/name scan | PASS | Tracked CLI/docs/workflow paths contain no reference asset, shader, generated shader blob, resource manifest, build script, terminal-widget, or copied QML names. |
| Binary/reference extension scan | PASS | No tracked `.png`, `.jpg`, `.gif`, `.icns`, `.qsb`, `.frag`, `.vert`, `.qrc`, `.pro`, or `.desktop` files under release-scoped paths. |
| Excluded component keyword scan | PASS | Hits are documentation of exclusions and backup options, not implementation imports or tracked copied material. |
| Base dependency/import scan | PASS | `requirements.txt`, `apex_infinite.py`, `apex_infinite_events.py`, and `apex_infinite_ui.py` contain no PySide6, Qt, QML, or Nuitka references. |
| Dependency vulnerability audit | PASS | `pip-audit -r requirements.txt -r requirements-dev.txt -r requirements-wrapper.txt` reported no known vulnerabilities. |

---

## Wrapper Release-State Matrix

| Release Area | Source Evidence | Release Position | Verification Owner |
|--------------|-----------------|------------------|--------------------|
| Source wrapper entrypoint | `python -m apex_infinite_visual.main --dry-run --max-iterations 1 --auto-close-ms 300` | Source-shippable; T011 smoke passed and T021 rerun passed | T011, T021 |
| QML lint | `./.venv/bin/pyside6-qmllint apex_infinite_visual/qml/Main.qml` | Source-shippable; lint exits 0 with known non-blocking warnings and T021 rerun passed | T011, T021 |
| Optional PySide6 import | `tests/test_visual_wrapper_productization.py` import-guard tests | Source-shippable; base import remains headless-safe | T009, T011, T018 |
| Guarded wrapper command | `build_apex_cli_command()` tests and launcher inspection | Source-shippable; wrapper uses `--event-stream - --machine-output` | T009, T013, T017 |
| Failure states | Productization tests for missing CLI, missing PySide6, malformed JSONL, timeout, stderr, non-zero exit, and stop | Source-shippable; tests passed | T009, T011 |
| Settings controls | Productization tests for theme, effect intensity, font family, font scale, reduced effects, and plain fallback | Source-shippable; tests passed | T009, T011 |
| Base dependency isolation | `requirements.txt` scan and base CLI import scan | Required for source and binary release | T018 |
| Optional dependency lane | `requirements-wrapper.txt` contains PySide6 and Nuitka only in wrapper lane | PASS for source wrapper; binary gate remains open | T018, T020 |
| PySide6/Qt license path | Wrapper docs list LGPLv3/commercial review and no GPL-only module checks | Binary-gated until legal/module review for an actual artifact | T020 |
| AppImage packaging | Wrapper docs name `apex-infinite-visual-linux-x86_64.AppImage` path | Deferred; no binary artifact published in this session | T020 |
| Checksums and notices | Wrapper docs require SHA256, Qt/PySide6 notices, and source/dev install instructions | Binary-gated until artifact exists | T020 |
| Source/relink obligations | Wrapper docs require source availability or relink/replacement instructions | Binary-gated until artifact exists | T020 |

---

## Release Position

The tracked source and documentation pass the clean-room release checks run in
T004, T016, T017, T018, and T020. The base terminal CLI remains independent of
PySide6, Qt Quick, QML, Nuitka, wrapper assets, and display-server requirements.

The optional PySide6/QML wrapper source mode is source-shippable. No AppImage
or binary artifact is published in this session. Binary publication remains
gated until a future release completes generated-bundle review, license/module
review, notices, checksum publication, and source/relink instructions for the
concrete artifact.
