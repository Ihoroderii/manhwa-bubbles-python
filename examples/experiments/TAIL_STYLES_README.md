# Bubble Tail Styles Experiment

This directory contains experimental implementations of different tail styles for speech bubbles using Cairo.

## Available Tail Styles

### 1. **Classic Smooth** (`tail_classic_smooth`)
- Smooth curved tail using Bezier curves
- Traditional manga style
- Best for: Normal dialogue, standard speech

### 2. **Sharp Pointed** (`tail_sharp_pointed`)
- Triangular, sharp tail
- Simple and clean
- Best for: Direct speech, emphasis

### 3. **Wavy** (`tail_wavy`)
- Serpentine, wavy tail
- Multiple sine waves
- Best for: Playful dialogue, casual speech

### 4. **Jagged** (`tail_jagged`)
- Spiky, jagged edges
- Multiple sharp points
- Best for: Shouting, anger, intense emotion

### 5. **Double Split** (`tail_double_split`)
- Splits into two tails
- Unique visual effect
- Best for: Multiple speakers, confusion

### 6. **Curved Hook** (`tail_curved_hook`)
- Curved tail with hook at end
- Points back toward bubble
- Best for: Questioning, pointing

### 7. **Bubbly** (`tail_bubbly`)
- Made of connected small bubbles
- Playful appearance
- Best for: Light-hearted dialogue

### 8. **Thick Bold** (`tail_thick_bold`)
- Thick, bold tail with rounded end
- Strong visual presence
- Best for: Important dialogue, emphasis

### 9. **Energy Lines** (`tail_energy_lines`)
- Tail with radiating energy lines
- Dynamic, energetic feel
- Best for: Excitement, energy, action

### 10. **Organic Flowing** (`tail_organic_flowing`)
- Natural, flowing curves
- Organic variation
- Best for: Natural speech, organic style

## Usage

### Basic Usage

```python
import cairo
from examples.experiments.tail_styles_module import tail_classic_smooth

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 500)
ctx = cairo.Context(surface)

# Draw bubble
ctx.arc(200, 200, 80, 0, 2*math.pi)
ctx.set_source_rgb(1, 1, 1)
ctx.fill_preserve()
ctx.set_source_rgb(0, 0, 0)
ctx.stroke()

# Add tail
tail_classic_smooth(ctx, 200, 280, "bottom", length=60, width=25)

surface.write_to_png("bubble.png")
```

### Using Tail Registry

```python
from examples.experiments.tail_styles_module import get_tail_function

# Get tail function by name
tail_func = get_tail_function("wavy")

# Use it
tail_func(ctx, attach_x, attach_y, "bottom", length=50, width=20)
```

### Integration with Overlapping Circles Bubbles

```python
from examples.experiments.tail_integration_example import create_bubble_with_tail

create_bubble_with_tail(
    ctx, cx=300, cy=200, base_width=150, base_height=100,
    text="Hello!", circle_style="organic",
    tail_style="energy", tail_direction="bottom",
    tail_length=60, tail_width=25
)
```

## Parameters

All tail functions accept:
- `ctx`: Cairo context
- `attach_x, attach_y`: Attachment point coordinates
- `direction`: "bottom", "top", "left", or "right"
- `length`: Length of tail in pixels (default: 50)
- `width`: Width of tail at attachment point (default: 20-25)

Some tails have additional parameters:
- `tail_wavy`: `waves` - number of waves (default: 3)
- `tail_jagged`: `spikes` - number of spikes (default: 5)
- `tail_energy_lines`: `num_lines` - number of energy lines (default: 8)
- `tail_bubbly`: `num_bubbles` - number of bubbles (default: 3)

## Running Experiments

```bash
# Generate all tail style examples
python examples/experiments/tail_styles_experiment.py

# See integration examples
python examples/experiments/tail_integration_example.py
```

## Generated Files

- `tail_styles_experiment.png` - Overview of all tail styles
- `tail_*.png` - Individual tail style examples
- `bubbles_with_tails_demo.png` - Tails with organic bubbles
- `custom_tail_combinations.png` - Custom combinations

## Customization

You can easily create custom tail styles by following the pattern:

```python
def tail_custom(ctx, attach_x, attach_y, direction="bottom", length=50, width=20):
    """Your custom tail implementation"""
    # Create path
    ctx.move_to(...)
    ctx.line_to(...)
    # ... more path operations
    
    # Fill and stroke
    ctx.close_path()
    ctx.set_source_rgb(1, 1, 1)  # White fill
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)  # Black outline
    ctx.set_line_width(2)
    ctx.stroke()
```

## Tips

1. **Direction Handling**: Always support all 4 directions (bottom, top, left, right)
2. **Attachment Point**: Calculate based on bubble edge and direction
3. **Proportions**: Keep tail length proportional to bubble size
4. **Style Matching**: Match tail style to bubble style (e.g., energy tail with laugh bubble)
5. **Background Awareness**: Consider background color for visibility

## Examples

See `tail_integration_example.py` for complete examples of:
- Combining tails with overlapping circles bubbles
- Using different directions
- Customizing tail parameters
- Creating unique combinations

