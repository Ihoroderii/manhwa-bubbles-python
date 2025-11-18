# Manhwa Bubbles

[![Build and Test](https://github.com/Ihoroderii/manhwa-bubbles/workflows/Build%20and%20Test/badge.svg)](https://github.com/Ihoroderii/manhwa-bubbles/actions)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://pypi.org/project/manhwa-bubbles/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/release/Ihoroderii/manhwa-bubbles.svg)](https://github.com/Ihoroderii/manhwa-bubbles/releases/)

A Python library for creating manhwa-style speech bubbles and narration boxes using PIL (Pillow).

## Features

- **Speech Bubbles**: Multiple bubble types including oval, rectangular, cloud (thought), jagged (shouting), wavy (nervous), black (dark/evil), heart (romantic), spiky (rage), glow (magic/divine), and scratchy (madness/creepy)
- **Organic Overlapping Ovals (Cairo)**: Advanced manga/Manhwa style bubble with intersecting perimeter ovals (supports a laugh variant with energetic rays)
- **Narration Boxes**: Various narrator styles including plain, borderless, dashed, dark, and wavy borders
- **Customizable**: Adjustable positioning, sizing, and tail directions
- **Easy to Use**: Simple API with clear function signatures

## Installation

### From Source
```bash
git clone <your-repo-url>
cd bubble
pip install -e .
```

### From PyPI (once published)
```bash
pip install manhwa-bubbles
```

### With Cairo Support (for organic overlapping bubbles)
```bash
pip install manhwa-bubbles[cairo]
```

## Quick Start

```python
from PIL import Image, ImageDraw
from manhwa_bubbles import speech_bubble, narrator_plain

# Create a canvas
img = Image.new("RGB", (800, 600), "lightblue")
draw = ImageDraw.Draw(img)

# Add speech bubble
speech_bubble(draw, (50, 50, 200, 100), "Hello world!", "oval")

# Add narration
narrator_plain(draw, (300, 50, 250, 80), "The story begins...")

# Save or display
img.save("comic_panel.png")
img.show()
```

## Speech Bubble Types

| Type | Description | Use Case |
|------|-------------|----------|
| `oval` | Standard oval speech bubble | Normal dialogue |
| `rect` | Rectangular bubble | Narration |
| `cloud` | Cloud-like thought bubble | Internal thoughts |
| `jagged` | Spiky/jagged edges | Shouting, anger |
| `wavy` | Wavy borders | Nervous, shaky speech |
| `black` | Black bubble with white text | Evil, dark thoughts |
| `heart` | Heart-shaped bubble | Romantic dialogue |
| `spiky` | Flame-like spiky edges | Rage, intense anger |
| `glow` | Bubble with glowing aura | Magic, divine speech |
| `scratchy` | Rough, scratchy borders | Madness, creepy thoughts |

## Narration Box Types

| Type | Description | Use Case |
|------|-------------|----------|
| `narrator_plain` | Simple rectangular box | Standard narration |
| `narrator_borderless` | Text only, no border | Floating text |
| `narrator_dashed` | Dashed border | Flashbacks, memories |
| `narrator_dark` | Black box with white text | Ominous narration |
| `narrator_wavy` | Wavy borders | Dream sequences |

## API Reference

### Speech Bubbles

#### `speech_bubble(draw, xy, text, bubble_type="oval", tail_dir="down")`

Creates a speech bubble with the specified style.

**Parameters:**
- `draw`: PIL ImageDraw object
- `xy`: Tuple of (x, y, width, height) for bubble position and size
- `text`: Text to display in the bubble
- `bubble_type`: Type of bubble ("oval", "rect", "cloud", "jagged", "wavy", "black", "heart", "spiky", "glow", "scratchy")
- `tail_dir`: Direction for speech tail ("down", "up", "left", "right")

### Narration Boxes

#### `narrator_plain(draw, xy, text)`
#### `narrator_borderless(draw, xy, text)`
#### `narrator_dashed(draw, xy, text)`
#### `narrator_dark(draw, xy, text)`
#### `narrator_wavy(draw, xy, text)`

Creates narration boxes with different styles.

**Parameters:**
- `draw`: PIL ImageDraw object
- `xy`: Tuple of (x, y, width, height) for box position and size
- `text`: Text to display

## Examples

See `examples/demo.py` for comprehensive usage examples.

### Organic Overlapping Bubble (Cairo)

This additional style uses PyCairo for precise overlapping elliptical arcs with an optional minimal interior-ink mode.

Install dependency:

```bash
pip install pycairo
```

Basic usage:

```python
from manhwa_bubbles import generate_overlapping_bubble

surface, ctx = generate_overlapping_bubble(width=200, height=130, show_full_ovals=False)
surface.write_to_png("organic_minimal.png")
```

Show full ovals (debug/design view):

```python
surface, ctx = generate_overlapping_bubble(220, 150, show_full_ovals=True)
surface.write_to_png("organic_full.png")
```

Laugh version (adds energetic rays and denser smaller bumps):

```python
surface, ctx = generate_overlapping_bubble(190, 130, style='laugh', show_full_ovals=False)
surface.write_to_png("laugh_bubble.png")
```

Adjust flags (optional):

```python
import manhwa_bubbles.organic_overlap as oo
oo.FILL_GAPS_ONLY = True          # Fill rectangle then punch out ovals (creates gap network)
oo.DRAW_EMPHASIS_ARCS = True      # Draw only interior arc strokes
oo.DRAW_LAUGH_ENERGY = False      # Disable laugh energy rays
```

Returned `surface` is a Cairo `ImageSurface`; you can composite or convert to Pillow via PNG bytes if needed.

## Requirements

- Python 3.6+
- Pillow (PIL) 8.0.0+
- pycairo>=1.20.0 (optional, required for `generate_overlapping_bubble`)

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.