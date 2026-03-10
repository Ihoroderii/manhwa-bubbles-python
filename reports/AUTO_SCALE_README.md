# Auto-Scaling Bubble Functions

This module provides automatic scaling functionality for manga/manhwa speech bubbles that adapts bubble size based on panel dimensions.

## Features

- **Automatic Size Calculation**: Bubbles scale proportionally to panel size
- **Text-Aware Scaling**: Adjusts size based on text content
- **Adaptive Fitting**: Iteratively adjusts to fit text perfectly
- **Position Control**: Place bubbles anywhere on panel using ratios
- **Panel Constraints**: Respects min/max panel fraction limits
- **Multiple Styles**: Works with organic, laugh, and varied styles

## Installation

Auto-scaling requires:
- `pycairo` (for Cairo rendering)
- `overlapping_circles_squares.py` module (in examples/experiments/)

```bash
# Install Cairo dependencies (Ubuntu/Debian)
sudo apt-get install libcairo2-dev pkg-config python3-dev

# Install pycairo
pip install pycairo
```

## Quick Start

### Basic Auto-Scaling

```python
from manhwa_bubbles.auto_scale import auto_scale_bubble_for_panel
import cairo

# Create auto-scaled bubble for 800x1200 panel
surface, ctx, metadata = auto_scale_bubble_for_panel(
    panel_width=800,
    panel_height=1200,
    text="Hello!",
    style="organic",
    max_panel_fraction=0.3
)

# Save result
surface.write_to_png("bubble.png")
print(f"Bubble size: {metadata['bubble_size']}")
```

### Adaptive Scaling (Fits Text Perfectly)

```python
from manhwa_bubbles.auto_scale import auto_scale_bubble_adaptive

surface, ctx, metadata = auto_scale_bubble_adaptive(
    panel_width=800,
    panel_height=1200,
    text="This is a longer text that needs perfect fitting!",
    style="laugh",
    target_text_padding=25,
    max_panel_fraction=0.35
)

surface.write_to_png("adaptive_bubble.png")
print(f"Iterations: {metadata['iterations']}")
```

### Quick Helper

```python
from manhwa_bubbles.auto_scale import quick_auto_bubble

# One-line function call
surface = quick_auto_bubble((800, 1200), "Quick!", "laugh")
surface.write_to_png("quick.png")
```

## API Reference

### `auto_scale_bubble_for_panel()`

Automatically scale bubble to fit manga panel.

**Parameters:**
- `panel_width` (int): Width of manga panel in pixels
- `panel_height` (int): Height of manga panel in pixels
- `text` (str): Text content (affects size if provided)
- `style` (str): Bubble style ("organic", "laugh", "varied")
- `position` (tuple, optional): (x_ratio, y_ratio) position (0.0-1.0), None = center
- `max_panel_fraction` (float): Maximum fraction of panel size (default: 0.4)
- `min_panel_fraction` (float): Minimum fraction of panel size (default: 0.15)
- `text_padding` (float): Padding around text as fraction (default: 0.1)
- `aspect_ratio` (float, optional): Fixed aspect ratio, None = auto
- `show_full_ovals` (bool): Show full ovals or minimal mode (default: False)
- `seed` (int, optional): Random seed for reproducibility

**Returns:**
- `(surface, ctx, metadata)` tuple
  - `surface`: Cairo ImageSurface
  - `ctx`: Cairo Context
  - `metadata`: Dict with bubble_size, position, panel_size, scale_factor, panel_fraction

### `auto_scale_bubble_adaptive()`

Adaptive auto-scaling: iteratively adjusts size to fit text perfectly.

**Parameters:**
- `panel_width` (int): Panel width
- `panel_height` (int): Panel height
- `text` (str): Text to fit inside bubble
- `style` (str): Bubble style
- `target_text_padding` (int): Desired padding around text in pixels (default: 20)
- `max_panel_fraction` (float): Maximum fraction of panel (default: 0.35)
- `min_font_size` (int): Minimum font size (default: 12)
- `max_iterations` (int): Max iterations for adaptive sizing (default: 6)
- `show_full_ovals` (bool): Show full ovals (default: False)
- `seed` (int, optional): Random seed

**Returns:**
- `(surface, ctx, metadata)` tuple with iterations count

### `quick_auto_bubble()`

Quick helper function for simple use cases.

**Parameters:**
- `panel_size` (tuple): (width, height) tuple
- `text` (str): Text content
- `style` (str): Bubble style

**Returns:**
- Cairo ImageSurface

## Examples

### Multiple Panel Sizes

```python
panel_sizes = [
    (800, 1200),   # Standard manga
    (600, 800),    # Small panel
    (1200, 1600),  # Large panel
]

for w, h in panel_sizes:
    surface, _, meta = auto_scale_bubble_for_panel(w, h, "Auto!", seed=42)
    surface.write_to_png(f"panel_{w}x{h}.png")
```

### Positioned Bubbles

```python
# Top-left corner
surface, _, _ = auto_scale_bubble_for_panel(
    800, 1200, "Top-left!", position=(0.2, 0.2)
)

# Bottom-right corner
surface, _, _ = auto_scale_bubble_for_panel(
    800, 1200, "Bottom-right!", position=(0.8, 0.8)
)
```

### Multiple Bubbles on Panel

```python
panel_w, panel_h = 800, 1200
panel_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, panel_w, panel_h)
panel_ctx = cairo.Context(panel_surface)
panel_ctx.set_source_rgb(0.95, 0.95, 0.95)
panel_ctx.paint()

# Add multiple bubbles
bubbles = [
    ("First!", (0.3, 0.2)),
    ("Second!", (0.7, 0.3)),
    ("Third!", (0.5, 0.7)),
]

for text, pos in bubbles:
    surf, _, _ = auto_scale_bubble_for_panel(panel_w, panel_h, text, position=pos)
    panel_ctx.set_source_surface(surf, 0, 0)
    panel_ctx.paint()

panel_surface.write_to_png("multi_bubble.png")
```

## Testing

Run the test suite:

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
python tests/test_auto_scale.py

# Run demo
python examples/auto_scale_demo.py
```

## Notes

- Auto-scaling works best with panel sizes between 400x600 and 2000x3000 pixels
- Text estimation is approximate; use adaptive scaling for precise text fitting
- Random seed ensures reproducible results
- Panel fractions are relative to panel dimensions, not absolute pixels

## Troubleshooting

**Import Error**: Make sure `overlapping_circles_squares.py` is in `examples/experiments/`

**Cairo Error**: Install system dependencies: `sudo apt-get install libcairo2-dev pkg-config python3-dev`

**Bubble Too Small/Large**: Adjust `max_panel_fraction` and `min_panel_fraction` parameters

