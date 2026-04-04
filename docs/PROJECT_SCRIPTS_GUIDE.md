# Manhwa Bubbles — Project Scripts Guide

Complete reference for every script in this project: what it does, when to use it, and what technologies it relies on.

---

## Technologies Used Across the Project

| Technology | Purpose |
|---|---|
| **Python 3.7+** | Core language |
| **PyCairo** | High-quality vector bubble rendering (Bézier curves, gradients, anti-aliasing) |
| **Pillow (PIL)** | Image creation/manipulation, text rendering, compositing, fallback bubble drawing |
| **NumPy** | Array conversion between Cairo surfaces and PIL images |
| **Pango + PangoCairo** | Advanced text layout with word-wrapping (used in some experiments) |
| **OpenCV (cv2)** | Manual character selection via mouse clicks |
| **Ultralytics YOLOv8** | Automatic character/person detection in manga panels |
| **pytest** | Unit testing framework |
| **setuptools** | Package distribution (PyPI) |

---

## Core Library — `manhwa_bubbles/`

These are the modules that make up the installable `manhwa-bubbles` package.

### `manhwa_bubbles/__init__.py`
- **What:** Package entry point that re-exports all public API symbols (~40+ functions/classes).
- **Use for:** `from manhwa_bubbles import speech_bubble, parse_scenario, select_bubble_style` — single-import access to everything.
- **Tech:** Python imports only.

### `manhwa_bubbles/pipeline.py`
- **What:** The main end-to-end pipeline. Takes a manga panel image + a scenario JSON (from an LLM), then: detects characters → selects emotion-based bubble styles → computes placement positions → renders bubbles with tails → saves the final composited image.
- **Use for:** Automating the entire bubble-placement workflow in one call: `process_manga_page(image, scenario)`.
- **Tech:** PyCairo (preferred renderer), Pillow (fallback renderer), lazy-loads adaptive bubble module.

### `manhwa_bubbles/placement.py`
- **What:** Smart bubble placement engine. Computes where each bubble should go on the panel — above characters, avoiding faces, preventing bubble-bubble overlaps, handling narration boxes at edges.
- **Use for:** Internally called by the pipeline. Can also be used standalone to get placement coordinates without rendering.
- **Tech:** Math (geometry), optional YOLO integration for character detection.

### `manhwa_bubbles/bubble_selector.py`
- **What:** Maps emotion strings (e.g. "shouting", "laughing", "dark") to visual bubble styles. Supports 26 emotions, alias resolution, random selection among candidates, and Cairo/PIL preference.
- **Use for:** `select_bubble_style("shouting")` → returns a `BubbleStyle` with renderer, colors, and draw parameters.
- **Tech:** Python dataclasses, random selection.

### `manhwa_bubbles/scenario_parser.py`
- **What:** Parses LLM-generated scenario JSON into structured Python objects (`Scenario` → `PanelData` → `DialogueEntry` + `CharacterPosition`). Handles emotion normalization and validation.
- **Use for:** Converting raw JSON scenario into typed objects the pipeline can consume.
- **Tech:** JSON parsing, dataclasses.

### `manhwa_bubbles/speech_bubbles.py`
- **What:** Core PIL-based bubble rendering. Provides 10 bubble types: oval, rect, cloud, jagged, wavy, black, heart, spiky, glow, scratchy. Also draws tails with Bézier curves.
- **Use for:** Drawing individual bubbles with `speech_bubble(draw, xy, text, bubble_type="cloud")`.
- **Tech:** Pillow (ImageDraw), math (Bézier curves).

### `manhwa_bubbles/extended_styles.py`
- **What:** ~40 additional bubble style functions: wide-soft, tall-narrow, shout-burst, rage-flame, laugh-bouncy, ghost-translucent, digital-system, impact-bang, and many more.
- **Use for:** Specialty bubble visuals beyond the 10 core types.
- **Tech:** Pillow (ImageDraw, ImageFont), math, random.

### `manhwa_bubbles/narrators.py`
- **What:** Five narration box styles: plain rectangle, borderless floating text, dashed border, dark/ominous box, wavy/dreamy border.
- **Use for:** Drawing narrator caption boxes: `narrator_dark(draw, xy, text)`.
- **Tech:** Pillow (ImageDraw, ImageFont).

### `manhwa_bubbles/organic_overlap.py`
- **What:** Cairo-based organic overlapping-oval bubble generator. Distributes ovals along rectangle sides with gap-filling and emphasis arcs.
- **Use for:** Generating premium organic bubble shapes: `generate_overlapping_bubble(text, canvas_size)`.
- **Tech:** PyCairo.

### `manhwa_bubbles/auto_scale.py`
- **What:** Auto-scaling wrapper that adjusts bubble size to fit a target fraction of the panel. Iteratively resizes until text fits with proper padding.
- **Use for:** `auto_scale_bubble_for_panel(text, panel_w, panel_h)` — get a bubble that's properly sized.
- **Tech:** PyCairo, math, iterative text-fitting.

---

## Main Entry Points

### `run_demo.py` (root)
- **What:** Full working demo. Creates a 1000×1400 manga panel with 3 drawn characters (Hero, Villain, Sidekick), defines a multi-dialogue scenario, and runs the complete pipeline to produce `demo_result.png`.
- **Use for:** Quick visual test of the entire system. Run with `python run_demo.py`.
- **Tech:** Pillow (panel drawing), full pipeline (PyCairo bubbles, placement, selector).

### `setup.py` (root)
- **What:** Package distribution config. Defines the `manhwa-bubbles` v1.1.0 package for PyPI with optional extras: `[cairo]` for PyCairo, `[yolo]` for detection, `[dev]` for testing.
- **Use for:** `pip install .` or `pip install manhwa-bubbles`.
- **Tech:** setuptools.

### `test_quick.py` (root)
- **What:** Quick smoke test that renders multiple bubble types onto one image to verify the library works.
- **Use for:** Fast import/render sanity check.
- **Tech:** Pillow, manhwa_bubbles core.

### `adaptive_bubbles.py` (root)
- **What:** Compatibility shim that re-exports everything from `examples/experiments/adaptive_bubbles.py`. Lets other scripts import adaptive bubbles from the project root.
- **Use for:** `from adaptive_bubbles import adaptive_circle_bubble` without navigating to experiments/.
- **Tech:** sys.path manipulation.

---

## Examples — `examples/`

### `examples/demo.py`
- **What:** Renders all 10 core bubble types + all 5 narration box types on separate canvas images.
- **Use for:** Visual catalog of basic PIL bubble/narration styles.
- **Tech:** Pillow.

### `examples/extended_demo.py`
- **What:** Renders a composite grid of all ~40 extended bubble styles for visual inspection.
- **Use for:** Seeing every extended style at a glance.
- **Tech:** Pillow.

### `examples/render_all_bubbles.py`
- **What:** Renders every available bubble style (core + extended + optional Cairo organic) into individual PNGs plus a composite sheet in `build_bubbles/`.
- **Use for:** Generating a complete bubble asset library.
- **Tech:** Pillow, optional PyCairo.

### `examples/auto_scale_demo.py`
- **What:** Exercises auto-scaling across various panel sizes, text lengths, and styles.
- **Use for:** Testing that bubbles adapt correctly to different panel dimensions.
- **Tech:** PyCairo, auto_scale module.

### `examples/simple_auto_scale_test.py`
- **What:** Diagnostic script checking Cairo availability and running basic auto-scale tests.
- **Use for:** Debugging auto-scale import or rendering issues.
- **Tech:** PyCairo (optional), auto_scale module.

### `examples/test_laugh_colors.py`
- **What:** Tests laugh-style energy lines against different background colors (white, black, gray, blue).
- **Use for:** Verifying that laugh bubble decorations have proper contrast on any background.
- **Tech:** PyCairo, auto_scale module.

---

## Experiments — `examples/experiments/`

Visual bubble R&D scripts. Each explores a specific bubble shape or rendering technique.

### `examples/experiments/adaptive_bubbles.py`
- **What:** **The core adaptive renderer.** Creates circle or square bubbles with overlapping ovals, auto-wrapping text, iterative font sizing, and tails. This is the module the pipeline loads for high-quality bubble rendering.
- **Use for:** Directly imported by the pipeline as the preferred renderer.
- **Tech:** PyCairo, math, random. Depends on `overlapping_circles_circle` and `overlapping_circles_squares`.

### `examples/experiments/overlapping_circles_squares.py`
- **What:** **Foundational geometry module** (~1500 lines). Handles oval generation along rectangle sides, corner overlaps, minimal-ink rendering, gap filling, border emphasis, and laugh energy lines.
- **Use for:** The building block for all overlapping-oval bubble shapes.
- **Tech:** PyCairo, math, random.

### `examples/experiments/overlapping_circles_circle.py`
- **What:** Circle variant of overlapping ovals. Distributes ovals along a circle's perimeter with radial5/6/7 variants.
- **Use for:** Building adaptive_circle_bubble shapes.
- **Tech:** PyCairo, depends on overlapping_circles_squares for geometry.

### `examples/experiments/bubble.py`
- **What:** Standalone single-bubble demo — elliptical bubble with variable stroke width and smooth Bézier tail.
- **Use for:** Understanding basic Cairo bubble drawing.
- **Tech:** PyCairo.

### `examples/experiments/cairo_manga_bubbles.py`
- **What:** Full manga bubble library with elliptical bubbles, thought bubbles, shout bubbles, plus Pango text rendering with word-wrapping.
- **Use for:** Bubbles that need advanced text layout (multi-language, word-wrap).
- **Tech:** PyCairo, Pango, PangoCairo (GTK introspection).

### `examples/experiments/casual_wave_bubbles.py`
- **What:** Square bubbles with wave-style edges at different intensities (gentle, bouncy, ocean, glitchy).
- **Use for:** Casual/relaxed mood bubbles.
- **Tech:** PyCairo.

### `examples/experiments/external_overlapping_squares.py`
- **What:** Square bubbles with ovals placed *outside* overlapping the edges.
- **Use for:** Exploring external-overlap visual style.
- **Tech:** PyCairo.

### `examples/experiments/faceted_corner_bubbles.py`
- **What:** Elongated bubbles with diamond-cut faceted corners.
- **Use for:** Futuristic/geometric bubble aesthetic.
- **Tech:** PyCairo.

### `examples/experiments/intruding_ovals_squares.py`
- **What:** Square bubbles with ovals intruding inward from each side.
- **Use for:** Exploring inward-overlap visual style.
- **Tech:** PyCairo.

### `examples/experiments/laugh_boom_simple.py`
- **What:** Renders "BOOM!" text in circular overlapping-ovals bubbles with text-fitting.
- **Use for:** Testing text-fitting inside organic shapes.
- **Tech:** PyCairo, overlapping_circles_circle.

### `examples/experiments/organic_cairo_bubbles.py`
- **What:** Hand-drawn style bubbles with Catmull-Rom spline outlines and variable stroke.
- **Use for:** Organic, sketch-like bubble look.
- **Tech:** PyCairo.

### `examples/experiments/premium_cairo_bubbles.py`
- **What:** Premium hand-drawn bubbles with natural imperfections, gradient fills, and hand-lettered text.
- **Use for:** High-quality artisanal bubble aesthetic.
- **Tech:** PyCairo.

### `examples/experiments/shout_bubble.py`
- **What:** Jagged shout/scream bubble with alternating spike radii.
- **Use for:** Shout/scream visual effect.
- **Tech:** PyCairo.

### `examples/experiments/simple_cairo_bubbles.py`
- **What:** Basic Cairo examples: elliptical speech bubble + thought bubble with trailing dots.
- **Use for:** Learning Cairo bubble fundamentals.
- **Tech:** PyCairo.

### `examples/experiments/single_example.py`
- **What:** Four manually-positioned ovals crossing a rectangle with gradient fills.
- **Use for:** Understanding oval-rectangle crossing geometry.
- **Tech:** PyCairo.

### `examples/experiments/smooth_action_bubbles.py`
- **What:** Action/explosion bubbles with flowing energy waves and radial gradients.
- **Use for:** Action/impact scenes.
- **Tech:** PyCairo.

### `examples/experiments/smooth_square_bubbles.py`
- **What:** Square bubbles with smooth/flowing/wavy edge deformations.
- **Use for:** Styled speech with soft-edged squares.
- **Tech:** PyCairo.

### `examples/experiments/pixel_precise_crossing.py`
- **What:** Finds exact pixels where circle perimeters cross square borders for precision rendering.
- **Use for:** Debugging/refining border emphasis rendering.
- **Tech:** PyCairo.

### `examples/experiments/tail_styles_experiment.py`
- **What:** Visual catalog of diverse tail styles: classic smooth, wavy, zigzag, energy lines, organic flowing, double curve, spiral, etc.
- **Use for:** Choosing/previewing tail designs.
- **Tech:** PyCairo.

### `examples/experiments/tail_integration_example.py`
- **What:** Demonstrates integrating different tail styles with overlapping-circle bubbles.
- **Use for:** Testing tail + bubble combinations.
- **Tech:** PyCairo, tail_styles_experiment module, overlapping_circles_squares.

---

## Scripts — `scripts/`

Utility and diagnostic scripts.

### `scripts/cairo_only_test.py`
- **What:** Pure PyCairo test — creates bubble PNGs with transparent backgrounds, no PIL needed.
- **Use for:** Verifying PyCairo installation works in isolation.
- **Tech:** PyCairo only.

### `scripts/fix_detection.py`
- **What:** Manual character detection fallback. Opens a manga image and lets you click on character heads. Positions are used for bubble placement when YOLO fails.
- **Use for:** Manually marking character positions for bubble placement.
- **Tech:** OpenCV (mouse interface), Pillow.

### `scripts/yolo_manga_detector.py`
- **What:** YOLO-based automatic character detection class. Detects people in manga panels, estimates head positions, and places speech bubbles above them.
- **Use for:** Automated character detection in production pipelines.
- **Tech:** Ultralytics YOLOv8, OpenCV, NumPy, Pillow.

### `scripts/test_yolo_simple.py`
- **What:** Diagnostic script that checks YOLO/OpenCV/Pillow deps, loads a model, runs detection, and reports results.
- **Use for:** Debugging YOLO setup issues.
- **Tech:** Ultralytics YOLOv8 (optional), OpenCV (optional), Pillow (optional).

### `scripts/quick_manga_test.py`
- **What:** Quick test adding an adaptive Cairo bubble to a manga panel with Cairo→PIL compositing.
- **Use for:** Testing adaptive bubble on real manga images.
- **Tech:** PyCairo (via adaptive_bubbles), Pillow, NumPy.

### `scripts/simple_manga_test.py`
- **What:** Simplest possible test — adds PIL speech bubbles to a generated test panel with two characters.
- **Use for:** Minimal PIL-only test without Cairo.
- **Tech:** Pillow only.

### `scripts/test_manga_composite.py`
- **What:** Tests compositing Cairo adaptive bubbles (circle + square) onto manga images with alpha blending.
- **Use for:** Verifying Cairo→PIL compositing pipeline.
- **Tech:** PyCairo, Pillow, NumPy.

---

## Tests — `tests/`

### `tests/test_pipeline.py`
- **What:** End-to-end pipeline tests. Validates output creation, image dimensions, placement counts, mixed emotions, and multi-panel processing.
- **Use for:** `pytest tests/test_pipeline.py` — CI/regression testing.
- **Tech:** pytest, Pillow, full pipeline.

### `tests/test_placement.py`
- **What:** Tests placement engine: Rect overlap logic, Detection face-rects, bubble sizing, positioning with hints, overlap avoidance.
- **Use for:** `pytest tests/test_placement.py`.
- **Tech:** pytest.

### `tests/test_bubble_selector.py`
- **What:** Tests emotion→style mapping: emotion listing, deterministic selection, alias resolution, Cairo preference.
- **Use for:** `pytest tests/test_bubble_selector.py`.
- **Tech:** pytest.

### `tests/test_scenario_parser.py`
- **What:** Tests JSON parsing: emotion normalization, character positions, head estimation, error handling, narration detection.
- **Use for:** `pytest tests/test_scenario_parser.py`.
- **Tech:** pytest, JSON.

### `tests/test_library.py`
- **What:** Basic import + render validation for all core bubble types and narrators.
- **Use for:** Quick library sanity check.
- **Tech:** Pillow.

### `tests/test_auto_scale.py`
- **What:** Tests auto-scaling across multiple panel sizes and text lengths.
- **Use for:** Validating auto-scale behavior.
- **Tech:** PyCairo (optional).

### `tests/test_centered_bubbles.py`
- **What:** Tests that text is properly centered in all 10 bubble types.
- **Use for:** Visual text-centering validation.
- **Tech:** Pillow.

### `tests/adaptive_test_800x1200.py`
- **What:** Tests adaptive renderers at 800×1200 with multiple text samples and radial variants.
- **Use for:** High-resolution adaptive bubble testing.
- **Tech:** PyCairo, adaptive_bubbles module.

### `tests/clipping_test.py` / `tests/obvious_clipping_test.py`
- **What:** Cairo clipping tests — verify that circles are properly clipped to square boundaries.
- **Use for:** Debugging Cairo clip behavior.
- **Tech:** PyCairo.

---

## Quick Reference — When to Use What

| Goal | Script to Run |
|---|---|
| **Full demo (one command)** | `python run_demo.py` |
| **See all bubble styles** | `python examples/render_all_bubbles.py` |
| **See extended styles** | `python examples/extended_demo.py` |
| **Test auto-scaling** | `python examples/auto_scale_demo.py` |
| **Run all tests** | `pytest tests/` |
| **Manual character marking** | `python scripts/fix_detection.py your_image.png` |
| **YOLO auto-detection** | `python scripts/yolo_manga_detector.py` |
| **Install as package** | `pip install .` |
