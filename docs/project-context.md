# Manhwa Bubbles — Project Context

> **Purpose**: This file is a comprehensive reference for AI coding assistants.
> When the conversation context window is overloaded, attach this file to
> quickly restore full project understanding.
>
> **Last updated**: 2026-03-12

---

## 1. Project Overview

**manhwa-bubbles-python** is a Python library for creating professional
manhwa/manga-style speech bubbles and narration boxes. It takes an
AI-generated panel image + an LLM-generated scenario JSON and produces a
final manga page with speech bubbles automatically placed, styled, and
rendered.

- **Author**: Ihor Oderii (`ihor.oderii@gmail.com`)
- **Repo**: `https://github.com/ihoroderii/manhwa-bubbles`
- **Version**: 1.1.0
- **License**: MIT
- **Branch**: `improvements-and-experiments`

---

## 2. Environment

| Item | Value |
|------|-------|
| OS | Windows (Git Bash / MINGW64) |
| Machine | `ams-vm-io01` |
| Python | 3.7.8 (only version available) |
| Venv | `venv/` at project root, created with `--without-pip` |
| pip bootstrap | Used `get-pip.py` due to venv pip issues |

**Terminal quirk**: Git Bash has significant output lag — command results
often appear 1-2 commands behind. Use `echo` flushes or background + log
file pattern when running long commands.

---

## 3. Dependencies (`requirements.txt`)

```
Pillow>=8.0.0              # PIL image manipulation (always required)
pycairo>=1.20.0            # Cairo-based bubble rendering (preferred)
ultralytics==8.0.151       # YOLO character detection (pinned for Py3.7)
opencv-python>=4.8.0       # Image processing
numpy==1.21.6              # Pinned for Python 3.7 compat
```

**Why pinned**: `numpy>=1.24.0` and `ultralytics>=8.0.152` both require
Python 3.8+. These pins are the last Python 3.7-compatible versions.

Dev deps (`requirements-dev.txt`): `pytest>=7.0.0`

---

## 4. Project Structure

```
manhwa-bubbles-python/
├── manhwa_bubbles/              # Main library package
│   ├── __init__.py              # Public API exports
│   ├── pipeline.py              # ★ Main entry — end-to-end rendering pipeline
│   ├── scenario_parser.py       # Parses LLM scenario JSON → PanelData
│   ├── bubble_selector.py       # Maps emotions → BubbleStyle (Cairo/PIL)
│   ├── placement.py             # Smart bubble placement + YOLO detection
│   ├── speech_bubbles.py        # PIL-based bubble shapes + tails (Cairo-enhanced)
│   ├── extended_styles.py       # 40+ PIL bubble style functions
│   ├── narrators.py             # Narration box renderers (plain/dark/dashed/etc)
│   ├── organic_overlap.py       # Cairo organic overlapping-oval bubble generator
│   └── auto_scale.py            # Auto-scaling wrapper for panel-aware sizing
│
├── examples/
│   ├── bubble_tail_showcase.py  # ★ Standalone PyCairo tail demo (8 examples)
│   ├── demo.py                  # Basic demo
│   ├── extended_demo.py         # Extended styles demo
│   ├── render_all_bubbles.py    # Render every style
│   └── experiments/             # Cairo rendering experiments
│       ├── adaptive_bubbles.py  # ★ Cairo adaptive circle/square bubble renderers
│       ├── overlapping_circles_squares.py  # Core overlapping ovals algorithm
│       ├── tail_styles_module.py           # Tail rendering experiments
│       └── ... (20+ experiment files)
│
├── tests/                       # pytest test suite
├── scripts/                     # Utility scripts
├── reports/                     # Documentation / guides
├── run_demo.py                  # ★ Main demo entry point
├── setup.py                     # Package setup (v1.1.0)
├── requirements.txt
└── yolov8n.pt                   # YOLO model weights
```

---

## 5. Architecture — The Rendering Pipeline

### 5.1 Data Flow

```
LLM Scenario JSON
       │
       ▼
 scenario_parser.py  →  PanelData (dialogues + character positions)
       │
       ▼
 bubble_selector.py  →  BubbleStyle per dialogue (engine + draw_func)
       │
       ▼
 placement.py        →  BubblePlacement[] (position, size, tail target)
       │
       ▼
 pipeline.py         →  Render bubbles onto image → save output
```

### 5.2 Two Rendering Engines

The pipeline has **two distinct rendering paths** selected per-bubble:

#### Cairo Engine (`cairo_circle` / `cairo_square`)
- Uses PyCairo for professional overlapping-oval bubbles
- Implemented in `examples/experiments/adaptive_bubbles.py`
- Functions: `adaptive_circle_bubble()`, `adaptive_square_bubble()`
- Features: organic shapes, auto text-fitting, word-wrap, Bezier tails
- Tail rendering: native `ctx.curve_to()` Bezier curves
- Result: Cairo `ImageSurface` → converted to PIL → composited

#### PIL Engine (`pil`)
- Uses Pillow `ImageDraw` for simpler/specialty bubble shapes
- Implemented across `speech_bubbles.py`, `extended_styles.py`, `narrators.py`
- 40+ styles: `shout_burst`, `inverted_aura`, `shock_mini_spike`, etc.
- **Tail rendering**: Now uses PyCairo `curve_to()` when available
  - `_draw_tail_cairo()` in `pipeline.py` — creates Cairo surface, draws
    Bezier tail, composites onto PIL image
  - `draw_tail_cairo()` in `speech_bubbles.py` — same approach for
    `speech_bubble()` function
  - Falls back to `_draw_tail_pil_fallback()` / `draw_tail()` (PIL polygon
    Bezier approximation) when Cairo is not installed

### 5.3 The Render Loop (`pipeline.py` lines ~420-430)

```python
draw = ImageDraw.Draw(image)
for p in placements:
    if p.style.engine in ("cairo_circle", "cairo_square"):
        image = _render_cairo_adaptive(image, p)
        draw = ImageDraw.Draw(image)
    else:
        image = _render_pil_bubble(draw, p, image=image)
        draw = ImageDraw.Draw(image)
```

**Key detail**: After every render that does Cairo compositing, a new
`ImageDraw` must be created because `Image.alpha_composite()` returns a
new `Image` object.

---

## 6. Key Files — Quick Reference

### `pipeline.py` (~513 lines)
- **Entry points**: `process_manga_page()`, `process_panel()`, `process_all_panels()`
- **Cairo tail**: `_draw_tail_cairo(image, placement)` — PyCairo Bezier tail
- **PIL tail fallback**: `_draw_tail_pil_fallback(draw, placement)`
- **PIL bubble render**: `_render_pil_bubble(draw, placement, image=None)`
- **Cairo bubble render**: `_render_cairo_adaptive(image, placement)`
- **Lazy load**: `_load_adaptive_bubbles()` — imports from `examples/experiments/`

### `bubble_selector.py` (~324 lines)
- **`_EMOTION_MAP`**: Dict mapping 26+ emotions → candidate style lists
- **`select_bubble_style(emotion, seed, prefer_cairo)`**: Picks one style
- Cairo candidates listed first; PIL fallbacks follow
- Aliases: `"angry"→"shouting"`, `"sad"→"crying"`, `"evil"→"dark"`, etc.
- **`BubbleStyle` dataclass**: `name`, `engine`, `draw_func`, `bubble_type`, `pil_kwargs`, `cairo_kwargs`

### `scenario_parser.py` (~264 lines)
- **Input**: JSON with `panels[].dialogues[]` and optional `panels[].characters[]`
- **Output**: `Scenario` → `PanelData` → `DialogueEntry` + `CharacterPosition`
- Character `head` auto-estimated from `bbox` if not provided

### `placement.py` (~551 lines)
- **`compute_placements()`**: Main placement algorithm
- **`detect_characters()`**: YOLO wrapper (returns `[]` if not installed)
- **`merge_detections()`**: Combines YOLO + manual detections
- **`positions_to_detections()`**: Converts `CharacterPosition` → `Detection`
- Data: `Rect`, `Detection`, `BubblePlacement`

### `speech_bubbles.py` (~307 lines)
- `speech_bubble(draw, xy, text, bubble_type, tail_dir, image=None)`
- `draw_tail(draw, x, y, direction, length, width)` — PIL fallback
- `draw_tail_cairo(image, x, y, direction, length, width)` — PyCairo version
- Bubble types: oval, rect, cloud, jagged, wavy, black, heart, spiky, glow, scratchy
- `_cairo_available` flag, `_bezier_point()` helper

### `extended_styles.py` (~606 lines)
- 40+ `bubble_*` functions for specialty styles
- All use PIL `ImageDraw`
- `_center_text()` helper — uses `draw.textbbox()` (fixed from broken `font.size`)

### `narrators.py` (~104 lines)
- `narrator_plain()`, `narrator_borderless()`, `narrator_dashed()`,
  `narrator_dark()`, `narrator_scroll()`

### `adaptive_bubbles.py` (in `examples/experiments/`, ~579 lines)
- `adaptive_circle_bubble(text, variant, canvas_size, seed, ...)`
- `adaptive_square_bubble(text, canvas_size, seed, ...)`
- Both generate organic overlapping-oval bubbles on Cairo surfaces
- Tail: `ctx.curve_to()` Bezier curves (updated from flat `line_to` triangles)
- Variants: `radial5` (calm), `radial6` (normal), `radial7` (energetic)

### `run_demo.py` (~205 lines)
- Creates a test panel with 3 characters (Hero, Villain, Sidekick)
- Demo scenario: 4 dialogues (shouting, dark, nervous, narration)
- With `seed=42`: Hero→`cairo_circle_radial7`, Villain→`cairo_circle_radial7`,
  Sidekick→`shock_mini_spike` (PIL), Narrator→`narrator_dark` (PIL)
- Outputs: `demo_manga_panel.png` (input), `demo_result.png` (output)

---

## 7. Supported Emotions (26 primary + aliases)

| Emotion | Cairo Variants | PIL Styles |
|---------|---------------|------------|
| normal | radial5, radial6, square | oval |
| shouting | radial7, radial6 | jagged, shout_burst |
| rage | radial7 | rage_flame |
| whispering | radial5 | whisper_dotted, whisper_thought |
| thinking | radial5, square | cloud, thought_cloud_chain |
| laughing | radial7, radial6 | laugh_bouncy |
| crying | radial5 | cry_drip |
| scared | radial6 | shock_mini_spike, nervous_wobble |
| narration | square | narrator_plain/dark/borderless |
| magic | radial7 | magic_glow_frame, arcane_glyph |
| telepathy | radial5 | telepathy_wave |
| ghost | radial5 | ghost_translucent |
| horror | radial7 | dripping_horror, scratchy |
| digital | square | digital_system, ai_card |
| radio | square | radio_comms |
| robotic | square | robotic_panel |
| sfx | radial7 | sfx_capsule, impact_bang |
| sarcastic | square | sarcastic_geometric |
| cold | radial5 | breath_cold |
| drunk | radial6 | drunk_slur |
| sleepy | radial5 | sleepy_slump |
| romantic | radial5 | heart |
| dark | radial7, square | black, inverted_aura |
| hypnotic | radial6 | hypnotic_spiral |
| choral | radial7 | chant_choral |
| echo | radial6 | echo_layers |

**Aliases**: neutral→normal, angry/yelling→shouting, quiet→whispering,
internal/thought→thinking, happy/giggling→laughing, sad→crying,
shocked/nervous→scared, narrator/caption→narration, supernatural→magic,
creepy→horror, frozen→cold, dizzy→drunk, tired→sleepy, love→romantic,
evil→dark, chanting→choral, impact/sound_effect→sfx

---

## 8. Bugs Fixed (History)

1. **`font.size` AttributeError** in `extended_styles.py`:
   `_center_text()` used `font.size` which doesn't exist on PIL default font.
   Fixed → `draw.textbbox()`.

2. **Flat triangle tails** in `adaptive_bubbles.py`:
   Both `adaptive_circle_bubble` and `adaptive_square_bubble` used `ctx.line_to`
   flat triangles. Fixed → `ctx.curve_to()` Bezier curves.

3. **PIL-only tail rendering** in `pipeline.py` and `speech_bubbles.py`:
   All tails were drawn with PIL `draw.polygon()`. Fixed → PyCairo
   `_draw_tail_cairo()` / `draw_tail_cairo()` using real `curve_to()`,
   with PIL polygon as fallback.

4. **Python 3.7 dependency issues**:
   `numpy>=1.24.0` and `ultralytics>=8.0.152` require Python 3.8+.
   Fixed → pinned `numpy==1.21.6`, `ultralytics==8.0.151`.

---

## 9. How to Run

```bash
# Activate venv
source venv/Scripts/activate   # Git Bash on Windows

# Run end-to-end demo
python run_demo.py

# Run with custom image
python run_demo.py your_panel.png

# Run PyCairo tail showcase
python examples/bubble_tail_showcase.py

# Run tests
pytest tests/
```

### Programmatic Usage

```python
from manhwa_bubbles.pipeline import process_manga_page

result = process_manga_page(
    "panel.png",
    {
        "panels": [{
            "panel_id": 1,
            "image": "panel.png",
            "characters": [
                {"name": "Hero", "bbox": [100, 200, 200, 400], "head": [150, 220]}
            ],
            "dialogues": [
                {"character": "Hero", "text": "Hello!", "emotion": "normal"}
            ]
        }]
    },
    output_path="output.png",
    seed=42,
)
```

---

## 10. Cairo-PIL Compositing Pattern

This pattern is used throughout the codebase when rendering Cairo content
onto PIL images:

```python
import cairo
from PIL import Image

# 1. Create Cairo surface matching image size
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# 2. Draw with Cairo (curve_to, arc, etc.)
ctx.move_to(x1, y1)
ctx.curve_to(cp1x, cp1y, cp2x, cp2y, x2, y2)
ctx.set_source_rgba(1, 1, 1, 1)  # white fill
ctx.fill_preserve()
ctx.set_source_rgba(0, 0, 0, 0.95)  # black stroke
ctx.set_line_width(2.5)
ctx.stroke()

# 3. Convert Cairo surface → PIL Image (note BGRA → RGBA)
pil_layer = Image.frombuffer(
    "RGBA",
    (surface.get_width(), surface.get_height()),
    surface.get_data(),
    "raw", "BGRA", 0, 1,
)

# 4. Composite onto base image
image = image.convert("RGBA")
image = Image.alpha_composite(image, pil_layer)
# IMPORTANT: Recreate ImageDraw after composite (new Image object!)
draw = ImageDraw.Draw(image)
```

---

## 11. Scenario JSON Format

```json
{
  "panels": [
    {
      "panel_id": 1,
      "image": "panel_001.png",
      "characters": [
        {
          "name": "Hero",
          "bbox": [175, 560, 265, 900],
          "head": [220, 600]
        }
      ],
      "dialogues": [
        {
          "character": "Hero",
          "text": "Let's go!",
          "emotion": "shouting",
          "position_hint": "left"
        },
        {
          "character": "Narrator",
          "text": "And so it began...",
          "emotion": "narration"
        }
      ]
    }
  ]
}
```

- `characters` is optional — provides known positions so bubbles anchor
  near the correct speaker without relying on YOLO
- `head` is optional — auto-estimated from upper-center of `bbox`
- `position_hint`: `"left"`, `"right"`, `"center"`, `"top"`, `"bottom"`
- `emotion`: any key from the emotion table (Section 7)

---

## 12. Testing

```bash
pytest tests/ -v
```

Key test files:
- `tests/test_pipeline.py` — end-to-end pipeline tests
- `tests/test_bubble_selector.py` — emotion→style mapping
- `tests/test_scenario_parser.py` — JSON parsing
- `tests/test_placement.py` — bubble placement algorithm
- `tests/test_library.py` — library imports and basic API

---

## 13. Things to Know / Gotchas

1. **Terminal lag on this VM**: Commands in Git Bash often show output 1-2
   commands behind. Use `echo` flush commands or redirect to log files.

2. **Cairo lazy-loading**: `adaptive_bubbles.py` is loaded at runtime from
   `examples/experiments/` via `sys.path` manipulation in
   `_load_adaptive_bubbles()`. Not a proper package import.

3. **`_render_pil_bubble` returns Image**: After the Cairo tail compositing
   change, `_render_pil_bubble()` returns the updated `Image` object. The
   render loop must capture it and recreate `ImageDraw`.

4. **`speech_bubble()` returns Image**: When Cairo is available and `image`
   parameter is passed, `speech_bubble()` returns the updated image (with
   Cairo-rendered tail). The caller must handle the return value.

5. **YOLO often finds 0 characters**: On simple/drawn panels, YOLO rarely
   detects anything useful. The pipeline falls back to `characters[]`
   positions from the scenario JSON.

6. **Python 3.7**: numpy and ultralytics are pinned to old versions.
   `setup.py` says `python_requires=">=3.8"` but the actual VM runs 3.7.
   The pinned `requirements.txt` makes it work.
