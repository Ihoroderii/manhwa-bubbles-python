import math
import cairo

def draw_shout_bubble(ctx, x, y, r=80, spikes=24, 
                      spike_ratio=0.6, stroke_width=3):
    """
    Draw a jagged shout/scream bubble.
    
    :param ctx: Cairo context
    :param x, y: center of bubble
    :param r: average radius
    :param spikes: number of jagged points
    :param spike_ratio: ratio for inner vs outer spike length
    :param stroke_width: outline thickness
    """
    # Precompute angles
    step = 2 * math.pi / spikes
    angle = 0

    # Move to first point
    ctx.move_to(
        x + r * math.cos(0),
        y + r * math.sin(0)
    )

    for i in range(1, spikes + 1):
        # Alternate radius for jagged effect
        radius = r * (1.0 if i % 2 == 0 else spike_ratio)
        angle = i * step
        px = x + radius * math.cos(angle)
        py = y + radius * math.sin(angle)
        ctx.line_to(px, py)

    ctx.close_path()

    # Style
    ctx.set_source_rgb(1, 1, 1)   # white fill
    ctx.fill_preserve()

    ctx.set_source_rgb(0, 0, 0)   # black stroke
    ctx.set_line_width(stroke_width)
    ctx.stroke()


# Example render
WIDTH, HEIGHT = 400, 300
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

# White background
ctx.rectangle(0, 0, WIDTH, HEIGHT)
ctx.set_source_rgb(1, 1, 1)
ctx.fill()

# Draw scream bubble
draw_shout_bubble(ctx, 200, 150, r=100, spikes=32, spike_ratio=0.6)

# Add sample text
ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(30)
ctx.set_source_rgb(0, 0, 0)
ctx.move_to(140, 160)
ctx.show_text("AAAH!!!")

# Save
surface.write_to_png("shout_bubble.png")
print("Saved shout_bubble.png")
