# Laugh Energy Lines - Background-Aware Colors

## ✅ Update Complete!

The laugh energy lines now automatically adjust their color based on the background:

- **Light backgrounds** → **Black laugh lines** (default)
- **Dark backgrounds** → **Bright yellow/white laugh lines** (for visibility)

## How It Works

The system calculates the luminance of the background color:
- If luminance < 0.5 (dark): Uses bright yellow/white lines `rgba(1.0, 1.0, 0.7, 0.8)`
- If luminance >= 0.5 (light): Uses black lines `rgba(0, 0, 0, 0.65)`

## Usage

### With Auto-Scaling Functions

```python
from manhwa_bubbles.auto_scale import auto_scale_bubble_for_panel

# Dark background - laugh lines will be bright
surface, ctx, meta = auto_scale_bubble_for_panel(
    panel_width=800,
    panel_height=1200,
    text="Laugh!",
    style="laugh",
    background_color=(0.0, 0.0, 0.0)  # Black background
)
surface.write_to_png("laugh_dark_bg.png")

# Light background - laugh lines will be black
surface, ctx, meta = auto_scale_bubble_for_panel(
    panel_width=800,
    panel_height=1200,
    text="Laugh!",
    style="laugh",
    background_color=(1.0, 1.0, 1.0)  # White background
)
surface.write_to_png("laugh_light_bg.png")
```

### Direct Usage

```python
from examples.experiments.overlapping_circles_squares import (
    create_overlapping_circles_square
)
import cairo

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 600, 400)
ctx = cairo.Context(surface)

# Paint dark background
ctx.set_source_rgb(0, 0, 0)  # Black
ctx.paint()

# Create bubble with background color info
create_overlapping_circles_square(
    ctx, 300, 200, 180, 120,
    text="Laugh!",
    circle_style="laugh",
    background_color=(0.0, 0.0, 0.0)  # Tell function about dark background
)

surface.write_to_png("output.png")
```

## Background Color Format

The `background_color` parameter accepts:
- `(r, g, b)` - RGB values 0.0-1.0
- `(r, g, b, a)` - RGBA values 0.0-1.0

Examples:
- `(0.0, 0.0, 0.0)` - Black
- `(1.0, 1.0, 1.0)` - White
- `(0.2, 0.2, 0.2)` - Dark gray
- `(0.1, 0.1, 0.3)` - Dark blue

## Test Files

Run the test script to see examples:

```bash
python examples/test_laugh_colors.py
```

This generates:
- `test_laugh_light_bg.png` - White background with black lines
- `test_laugh_dark_bg.png` - Black background with bright lines
- `test_laugh_darkgray_bg.png` - Dark gray with bright lines
- `test_laugh_mediumgray_bg.png` - Medium gray
- `test_laugh_darkblue_bg.png` - Dark blue with bright lines

## Updated Functions

The following functions now support `background_color` parameter:

1. `create_overlapping_circles_square()` - Main bubble creation
2. `draw_laugh_energy_lines()` - Laugh energy lines drawing
3. `_draw_laugh_energy_lines()` - Internal function in organic_overlap.py
4. `auto_scale_bubble_for_panel()` - Auto-scaling wrapper
5. `auto_scale_bubble_adaptive()` - Adaptive scaling wrapper
6. `generate_overlapping_bubble()` - Organic overlap generator

## Notes

- If `background_color` is `None`, defaults to black lines (assumes light background)
- Luminance calculation uses standard RGB weights: `0.299*R + 0.587*G + 0.114*B`
- Bright lines use light yellow/white color for good visibility on dark backgrounds
- The background color is also used to paint the canvas background if provided to auto-scaling functions

