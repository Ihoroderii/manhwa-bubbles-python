# Cleanup Recommendations — Scripts to Remove

This document lists scripts recommended for removal, organized by confidence level.
Removing these ~22 files would clean out ~40% of the codebase while keeping everything
the pipeline actually uses, all tests, and useful demos.

---

## 1. Definitely Remove — Superseded by Core Library

These are basic experiments that were fully absorbed into the library.

| Script | Reason |
|---|---|
| `examples/experiments/bubble.py` | Basic single-bubble demo; fully superseded by core library |
| `examples/experiments/simple_cairo_bubbles.py` | Intro-level Cairo learning exercise; no unique value |
| `examples/experiments/single_example.py` | 4 hardcoded ovals crossing a rectangle; one-off geometry test |
| `examples/experiments/pixel_precise_crossing.py` | Pixel-level debugging tool; no longer needed |
| `examples/experiments/shout_bubble.py` | Already implemented in `speech_bubbles.py` as "jagged" type |
| `examples/experiments/laugh_boom_simple.py` | One-off "BOOM!" text test |
| `examples/experiments/organic_cairo_bubbles.py` | Superseded by `manhwa_bubbles/organic_overlap.py` (integrated) |

---

## 2. Strongly Recommend Removing — Never-Adopted Experiments

These explored a visual style that was never integrated into the pipeline.

| Script | Reason |
|---|---|
| `examples/experiments/external_overlapping_squares.py` | Explored external-overlap style — not used anywhere |
| `examples/experiments/intruding_ovals_squares.py` | Explored inward-overlap style — not used anywhere |
| `examples/experiments/faceted_corner_bubbles.py` | Diamond-cut corners experiment — never integrated |
| `examples/experiments/casual_wave_bubbles.py` | Wavy square edges — never integrated |
| `examples/experiments/smooth_square_bubbles.py` | Smooth deformed squares — never integrated |
| `examples/experiments/smooth_action_bubbles.py` | Action/explosion experiment — never integrated |
| `examples/experiments/premium_cairo_bubbles.py` | Hand-drawn premium style — never integrated |
| `examples/experiments/cairo_manga_bubbles.py` | Depends on Pango/GTK (hard to install); never integrated |

---

## 3. Recommend Removing — Redundant Diagnostics

One-time setup checks and tests that are already covered by the test suite.

| Script | Reason |
|---|---|
| `scripts/cairo_only_test.py` | One-time Cairo install verification; redundant with test suite |
| `scripts/test_yolo_simple.py` | One-time YOLO setup check |
| `scripts/simple_manga_test.py` | Minimal PIL-only test; covered by `tests/test_library.py` |
| `scripts/quick_manga_test.py` | Quick adaptive test; covered by test suite |
| `scripts/test_manga_composite.py` | Compositing test; covered by test suite |
| `test_quick.py` (root) | Smoke test; redundant with `pytest tests/` |

---

## 4. Consider Removing — Borderline

| Script | Reason to Remove | Reason to Keep |
|---|---|---|
| `examples/simple_auto_scale_test.py` | Diagnostic; `test_auto_scale.py` covers it | Useful for quick debugging |
| `examples/test_laugh_colors.py` | Narrow test | Validates contrast across backgrounds |
| `scripts/fix_detection.py` | Rarely used manual tool | Only manual fallback when YOLO fails |

---

## MUST KEEP — Do Not Touch

These are critical to the project and must NOT be removed.

### Core Library (`manhwa_bubbles/`)
All files — this is the installable package.

### Pipeline Dependencies (in `examples/experiments/`)
| Script | Why |
|---|---|
| `adaptive_bubbles.py` | **Imported by the pipeline** — the main renderer |
| `overlapping_circles_squares.py` | **Imported by adaptive_bubbles** — foundational geometry |
| `overlapping_circles_circle.py` | **Imported by adaptive_bubbles** — circle variant |
| `tail_styles_experiment.py` | Useful visual catalog of tail designs |
| `tail_integration_example.py` | Useful tail + bubble integration reference |

### Entry Points & Config
| Script | Why |
|---|---|
| `run_demo.py` | Main demo entry point |
| `setup.py` | Package distribution |
| `adaptive_bubbles.py` (root) | Compatibility shim for imports |

### Showcase Demos (`examples/`)
| Script | Why |
|---|---|
| `demo.py` | Visual catalog of core bubble types |
| `extended_demo.py` | Visual catalog of extended styles |
| `render_all_bubbles.py` | Generates complete bubble asset library |
| `auto_scale_demo.py` | Auto-scale testing across panel sizes |

### Production Scripts (`scripts/`)
| Script | Why |
|---|---|
| `yolo_manga_detector.py` | Production YOLO detection class |

### Test Suite (`tests/`)
All `test_*.py` files — regression testing.
