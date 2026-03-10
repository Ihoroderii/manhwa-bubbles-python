# Python Files Reference - Manhwa Bubbles Project

**Project**: Manhwa Bubbles v1.1.0  
**Description**: A Python library for creating manhwa-style speech bubbles and narration boxes  
**Last Updated**: 2026-01-25

---

## Table of Contents

1. [Core Library Files](#core-library-files)
2. [Test & Demo Scripts](#test--demo-scripts)
3. [Experimental Files](#experimental-files)
4. [YOLO Integration](#yolo-integration)
5. [Project Configuration](#project-configuration)

---

## Core Library Files

### `manhwa_bubbles/` (Main Package)

#### **`manhwa_bubbles/__init__.py`**
- **Purpose**: Package initialization and public API
- **Exports**: All public functions for speech bubbles, narrators, extended styles
- **Key Functions**: 
  - Speech bubbles: `speech_bubble()`, `bubble_heart()`, `bubble_spiky()`, etc.
  - Narrators: `narrator_plain()`, `narrator_dark()`, etc.
  - Auto-scaling: `auto_scale_bubble_for_panel()`, `auto_scale_bubble_adaptive()`
  - 40+ extended bubble styles

#### **`manhwa_bubbles/speech_bubbles.py`**
- **Purpose**: Core speech bubble drawing functions using PIL
- **Key Functions**:
  - `speech_bubble(draw, xy, text, bubble_type, tail_dir)` - Main bubble function
  - `draw_tail(draw, x, y, direction)` - Draw bubble tails
  - `bubble_heart(draw, xy, text)` - Heart-shaped romantic bubbles
  - `bubble_spiky(draw, xy, text)` - Flame-like rage bubbles
  - `bubble_glow(draw, xy, text)` - Glowing magic/divine bubbles
  - `bubble_scratchy(draw, xy, text)` - Rough creepy bubbles
- **Bubble Types**: oval, rect, cloud, jagged, wavy, black, heart, spiky, glow, scratchy

#### **`manhwa_bubbles/narrators.py`**
- **Purpose**: Narration box styles for storytelling
- **Key Functions**:
  - `narrator_plain(draw, xy, text)` - Standard rectangular box
  - `narrator_borderless(draw, xy, text)` - Text only, no border
  - `narrator_dashed(draw, xy, text)` - Dashed border for flashbacks
  - `narrator_dark(draw, xy, text)` - Black box with white text
  - `narrator_wavy(draw, xy, text)` - Wavy borders for dreams

#### **`manhwa_bubbles/extended_styles.py`**
- **Purpose**: Extended catalog of 40+ specialized bubble styles
- **Categories**:
  - **Emotional**: whisper_dotted, shout_burst, laugh_bouncy, cry_drip, nervous_wobble
  - **Supernatural**: inverted_aura, dripping_horror, magic_glow, arcane_glyph, ghost_translucent
  - **Technical**: digital_system, radio_comms, robotic_panel, ai_card, static_electric
  - **Effects**: impact_bang, sfx_capsule, chain_overlap, echo_layers, fragmented_arc
  - **Mood**: breath_cold, sleepy_slump, drunk_slur, hypnotic_spiral
  - **Meta**: text_only, bracketed_text, bold_plate
- **Total**: 40+ unique bubble styles

#### **`manhwa_bubbles/organic_overlap.py`**
- **Purpose**: Advanced organic overlapping bubble generation using Cairo
- **Key Function**: `generate_overlapping_bubble(text, config)` - Creates professional manga-style bubbles with overlapping oval patterns

#### **`manhwa_bubbles/auto_scale.py`**
- **Purpose**: Automatic bubble sizing for manga panels
- **Dependencies**: Requires pycairo and overlapping_circles_squares
- **Key Functions**:
  - `auto_scale_bubble_for_panel(text, panel_size, target_inner_padding)` - Auto-scale to fit panel
  - `auto_scale_bubble_adaptive(text, canvas_size, max_iterations)` - Adaptive sizing with iterations
  - `quick_auto_bubble(text, panel_width, panel_height)` - Quick auto-sizing wrapper
- **Features**: Iterative sizing, free space detection, text fitting

---

## Test & Demo Scripts

### Root Level Test Scripts

#### **`test_yolo_simple.py`** ⭐ **Main YOLO Script**
- **Purpose**: YOLO person detection + automatic bubble placement
- **Features**:
  - Detects people in manga using YOLOv8
  - Multi-person detection with colored visualization
  - **Random bubble placement** with face avoidance (7 placement zones)
  - Cairo bubble rendering with smart tail direction
  - Automatic text wrapping
  - Face overlap detection and retry logic
- **Output**: 
  - `detected_people_visualization.png` - Detection boxes (green/blue/red per person)
  - `manga_with_cairo_bubbles.png` - Final lettered manga
- **Usage**: `python test_yolo_simple.py manga.png "Text 1" "Text 2" "Text 3"`

#### **`yolo_manga_detector.py`**
- **Purpose**: Complete YOLO-based manga lettering system
- **Classes**:
  - `MangaPersonDetector` - Person detection with YOLO
- **Key Functions**:
  - `detect_people(image_path, visualize)` - Detect all people
  - `add_bubbles_to_detected_people(manga, detections, dialogues)` - Add bubbles
  - `process_your_manga(manga_path, dialogues, confidence)` - Full pipeline
- **Features**: Confidence tuning, visualization, batch processing

#### **`fix_detection.py`**
- **Purpose**: Manual character selection fallback when YOLO fails
- **Features**:
  - Click-based character marking
  - Works with ANY manga art style
  - Automatic bubble placement after manual selection
- **Usage**: `python fix_detection.py manga.png "Text 1" "Text 2"`

#### **`simple_manga_test.py`**
- **Purpose**: Simple PIL-based manga bubble testing
- **Features**: Creates test manga panels, adds basic bubbles
- **Usage**: Demo script, educational example

#### **`test_manga_composite.py`**
- **Purpose**: Advanced compositing examples
- **Features**: Multiple bubbles, dialogue sequences, manual positioning
- **Includes**: OpenCV face detection integration example

#### **`quick_manga_test.py`**
- **Purpose**: Quick test using Cairo adaptive bubbles
- **Features**: Adaptive bubble sizing, tail targeting, configuration examples

#### **`cairo_only_test.py`**
- **Purpose**: Pure Cairo bubble generation (no PIL)
- **Features**: Standalone bubble PNG files, transparent backgrounds
- **Output**: Individual bubble images for manual compositing

#### **`test_quick.py`**
- **Purpose**: Quick testing/debugging script
- **Status**: Utility test file

### `tests/` Directory

#### **`tests/__init__.py`**
- **Purpose**: Test package initialization
- **Status**: Empty module marker

#### **`tests/test_library.py`**
- **Purpose**: Unit tests for library functions
- **Tests**: Speech bubbles, narrators, basic functionality

#### **`tests/test_auto_scale.py`**
- **Purpose**: Tests for auto-scaling functionality
- **Tests**: Panel sizing, adaptive scaling, free space detection

#### **`tests/test_centered_bubbles.py`**
- **Purpose**: Tests for bubble centering and positioning
- **Tests**: Text centering, bubble alignment

#### **`tests/adaptive_test_800x1200.py`**
- **Purpose**: Adaptive bubble tests with 800x1200 panels
- **Tests**: Different text lengths, wrapping, variants

#### **`tests/clipping_test.py`**
- **Purpose**: Tests for bubble clipping issues
- **Tests**: Border clipping, overflow handling

#### **`tests/obvious_clipping_test.py`**
- **Purpose**: Edge case clipping tests
- **Tests**: Extreme cases, boundary conditions

---

## Experimental Files

### `examples/experiments/` Directory

#### **`examples/experiments/adaptive_bubbles.py`**
- **Purpose**: Experimental adaptive bubble sizing engine
- **Features**: Advanced text fitting, free space detection, iteration-based sizing
- **Status**: Prototype for manhwa_bubbles/auto_scale.py

#### **`examples/experiments/overlapping_circles_circle.py`**
- **Purpose**: Circular overlapping pattern generation
- **Functions**: `create_overlapping_circles_circle_radial5/6/7()`
- **Features**: Radial oval patterns, laugh variant, return_circles mode

#### **`examples/experiments/overlapping_circles_squares.py`**
- **Purpose**: Square/rectangle overlapping patterns
- **Function**: `create_overlapping_circles_square()`
- **Features**: Rectangle-based bubble generation, oval patterns

#### **`examples/experiments/laugh_boom_simple.py`**
- **Purpose**: Energy/laugh lines for dynamic bubbles
- **Features**: Radial lines, background-aware coloring

#### **`examples/experiments/cairo_manga_bubbles.py`**
- **Purpose**: Professional Cairo manga bubble rendering
- **Features**: Natural shapes, Pango text rendering, multiple styles

#### **`examples/experiments/organic_cairo_bubbles.py`**
- **Purpose**: Organic bubble shape generation
- **Features**: Varied shapes (smooth, wavy, bumpy, irregular), tail positioning

#### **`examples/experiments/premium_cairo_bubbles.py`**
- **Purpose**: Premium quality natural bubble rendering
- **Features**: Hand-drawn appearance, natural curves, professional quality

#### **`examples/experiments/casual_wave_bubbles.py`**
- **Purpose**: Casual wavy bubble styles
- **Features**: Relaxed wave patterns, friendly appearance

#### **`examples/experiments/faceted_corner_bubbles.py`**
- **Purpose**: Angular/faceted bubble designs
- **Features**: Sharp corners, geometric style

#### **`examples/experiments/smooth_square_bubbles.py`**
- **Purpose**: Smooth rounded square bubbles
- **Features**: Rounded corners, clean look

#### **`examples/experiments/smooth_action_bubbles.py`**
- **Purpose**: Action/impact bubble effects
- **Features**: Dynamic shapes for "POW", "BANG" effects

#### **`examples/experiments/ultra_smooth_action.py`**
- **Purpose**: Ultra-smooth action bubble rendering
- **Features**: High-quality smooth curves for action text

#### **`examples/experiments/shout_bubble.py`**
- **Purpose**: Shouting/yelling bubble styles
- **Features**: Jagged edges, explosive appearance

#### **`examples/experiments/simple_cairo_bubbles.py`**
- **Purpose**: Simple Cairo bubble examples
- **Features**: Basic shapes, educational examples

#### **`examples/experiments/tail_styles_module.py`**
- **Purpose**: Tail style library (10+ styles)
- **Styles**: classic, wavy, jagged, energy, organic, minimal, double, curved, spiky, rounded
- **Function**: `draw_tail(ctx, cx, cy, target, style, params)`

#### **`examples/experiments/tail_styles_experiment.py`**
- **Purpose**: Tail style testing and visualization
- **Features**: Generates examples of all tail styles

#### **`examples/experiments/tail_integration_example.py`**
- **Purpose**: Demonstrates tail integration with bubbles
- **Features**: Complete bubble + tail examples

#### **`examples/experiments/pixel_precise_crossing.py`**
- **Purpose**: Pixel-perfect path crossing detection
- **Features**: Advanced geometry for clean bubble intersections

#### **`examples/experiments/intruding_ovals_squares.py`**
- **Purpose**: Oval intrusion into square bubbles
- **Features**: Complex overlapping patterns

#### **`examples/experiments/external_overlapping_squares.py`**
- **Purpose**: External square overlay patterns
- **Features**: Border decoration with overlapping shapes

#### **`examples/experiments/bubble.py`**
- **Purpose**: General bubble experimentation
- **Status**: Prototype/testing file

#### **`examples/experiments/single_example.py`**
- **Purpose**: Single bubble example for quick testing
- **Status**: Minimal test file

### `examples/` Directory

#### **`examples/demo.py`**
- **Purpose**: Main library demonstration
- **Features**: Shows all bubble types, narrators, usage examples
- **Output**: Comprehensive demo image

#### **`examples/extended_demo.py`**
- **Purpose**: Extended styles demonstration
- **Features**: Shows all 40+ extended bubble styles
- **Output**: Gallery of all available styles

#### **`examples/render_all_bubbles.py`**
- **Purpose**: Renders all bubble types to individual files
- **Features**: Batch generation, organized output
- **Output**: Individual PNG for each bubble style

#### **`examples/auto_scale_demo.py`**
- **Purpose**: Auto-scaling feature demonstration
- **Features**: Shows adaptive sizing, panel fitting
- **Output**: Auto-scaled bubble examples

#### **`examples/simple_auto_scale_test.py`**
- **Purpose**: Simple auto-scale testing
- **Features**: Basic auto-scale functionality test

#### **`examples/test_laugh_colors.py`**
- **Purpose**: Tests laugh line color variations
- **Features**: Background-aware energy line coloring

---

## YOLO Integration

### Files

#### **`test_yolo_simple.py`** (Main Script)
- See [Test & Demo Scripts](#test--demo-scripts) section above

#### **`yolo_manga_detector.py`**
- See [Test & Demo Scripts](#test--demo-scripts) section above

#### **`fix_detection.py`**
- See [Test & Demo Scripts](#test--demo-scripts) section above

### Dependencies
- `ultralytics` - YOLOv8 implementation
- `opencv-python` - Image processing and visualization
- `pillow` - Image manipulation

### Documentation
- `reports/YOLO_README.md` - Overview and quick start
- `reports/YOLO_USAGE.md` - Detailed usage guide
- `reports/YOLO_QUICKSTART.txt` - Quick reference
- `reports/WHY_NO_DETECTION.md` - Troubleshooting guide
- `reports/MANGA_TESTING_GUIDE.md` - Complete testing workflow

---

## Project Configuration

### `setup.py`
- **Purpose**: Package configuration for PyPI distribution
- **Package Name**: manhwa-bubbles
- **Version**: 1.1.0
- **Dependencies**: 
  - Required: Pillow >= 8.0.0
  - Optional: pycairo >= 1.20.0 (for Cairo features)
- **Python**: >= 3.6
- **Status**: Published to PyPI

### `adaptive_bubbles.py` (Root)
- **Purpose**: Compatibility shim
- **Functionality**: Forwards imports to `manhwa_bubbles.adaptive_bubbles`
- **Status**: Wrapper for backward compatibility

### `adaptive_bubbles_full.py`
- **Purpose**: Full adaptive bubbles implementation (legacy)
- **Status**: Superseded by manhwa_bubbles package

---

## File Categories Summary

### By Purpose

| Category | Count | Files |
|----------|-------|-------|
| **Core Library** | 6 | manhwa_bubbles/*.py |
| **Main Tests** | 7 | test_*.py, *_test.py (root) |
| **Unit Tests** | 6 | tests/*.py |
| **Experiments** | 24 | examples/experiments/*.py |
| **Examples** | 5 | examples/*.py |
| **YOLO** | 3 | yolo_manga_detector.py, test_yolo_simple.py, fix_detection.py |
| **Config** | 2 | setup.py, adaptive_bubbles.py |

**Total Python Files**: 53

### By Functionality

- **Bubble Rendering**: 35 files
- **Auto-scaling**: 5 files
- **YOLO Integration**: 3 files
- **Testing**: 13 files
- **Configuration**: 2 files

---

## Quick Reference

### Most Important Files

1. **`manhwa_bubbles/__init__.py`** - Main library API
2. **`manhwa_bubbles/speech_bubbles.py`** - Core bubble functions
3. **`manhwa_bubbles/extended_styles.py`** - 40+ bubble styles
4. **`test_yolo_simple.py`** - YOLO + auto-bubbling ⭐
5. **`yolo_manga_detector.py`** - Complete YOLO system
6. **`examples/demo.py`** - Library demonstration
7. **`setup.py`** - Package configuration

### For New Users

Start with:
1. `examples/demo.py` - See what's available
2. `test_yolo_simple.py` - Auto-detect and add bubbles
3. `manhwa_bubbles/speech_bubbles.py` - Learn core functions

### For Developers

Explore:
1. `manhwa_bubbles/auto_scale.py` - Auto-scaling algorithm
2. `examples/experiments/adaptive_bubbles.py` - Adaptive sizing
3. `examples/experiments/overlapping_circles_*.py` - Pattern generation
4. `examples/experiments/tail_styles_module.py` - Tail variations

---

## Dependencies Overview

### Required (All Features)
```python
Pillow >= 8.0.0          # Core library
```

### Optional (Cairo Features)
```python
pycairo >= 1.20.0        # Advanced bubbles, auto-scaling
```

### Optional (YOLO Features)
```python
ultralytics >= 8.0.0     # YOLO v8
opencv-python >= 4.8.0   # Image processing
numpy >= 1.24.0          # Array operations
```

---

## Usage Examples

### Basic Bubble (PIL)
```python
from PIL import Image, ImageDraw
from manhwa_bubbles import speech_bubble

img = Image.new("RGB", (800, 600), "white")
draw = ImageDraw.Draw(img)
speech_bubble(draw, (50, 50, 200, 100), "Hello!", "oval")
img.save("output.png")
```

### Auto-scaled Bubble (Cairo)
```python
from manhwa_bubbles import auto_scale_bubble_adaptive

surface, metadata = auto_scale_bubble_adaptive(
    "Your text here",
    canvas_size=(600, 400),
    max_iterations=5
)
surface.write_to_png("bubble.png")
```

### YOLO Auto-detection
```bash
python test_yolo_simple.py my_manga.png "Text 1" "Text 2" "Text 3"
```

---

## Notes

- **Production Ready**: Core library (manhwa_bubbles package)
- **Experimental**: files in examples/experiments/
- **Active Development**: YOLO integration features
- **Stable Version**: 1.1.0 (PyPI)

---

**For more information**: See individual file docstrings and `reports/` documentation.
