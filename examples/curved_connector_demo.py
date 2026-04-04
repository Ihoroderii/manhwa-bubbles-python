#!/usr/bin/env python3
"""Demo: curved line connectors between speech bubbles and speakers.

Shows four styles of curved connector arrows drawn with PyCairo's
curve_to() — tapered lines, S-curves, dotted curves, thought circles.

Usage:
    python examples/curved_connector_demo.py
"""
import cairo
import math


def draw_bubble(ctx, cx, cy, rx, ry, text=""):
    """Draw a simple oval bubble."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.set_line_width(2.5)
    ctx.stroke()

    if text:
        ctx.set_font_size(14)
        ext = ctx.text_extents(text)
        ctx.move_to(cx - ext.width / 2, cy + ext.height / 2)
        ctx.set_source_rgba(0, 0, 0, 1)
        ctx.show_text(text)


def draw_speaker(ctx, x, y, color=(0.3, 0.5, 0.8)):
    """Draw a simple character head."""
    # Head
    ctx.arc(x, y, 22, 0, 2 * math.pi)
    ctx.set_source_rgba(*color, 1)
    ctx.fill_preserve()
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.set_line_width(2)
    ctx.stroke()
    # Eyes
    ctx.arc(x - 8, y - 5, 3, 0, 2 * math.pi)
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.fill()
    ctx.arc(x + 8, y - 5, 3, 0, 2 * math.pi)
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.fill()


# ---------------------------------------------------------------------------
# Connector styles
# ---------------------------------------------------------------------------

def connector_tapered_curve(ctx, bx, by, sx, sy):
    """Style 2: Tapered curve — thick at bubble, thin at speaker.

    Smoothly blends into the bubble: the base is pushed slightly inside
    the bubble so a white fill erases the bubble outline, and only the
    outer side-curves are stroked (not the base), so no seam is visible.
    """
    mx = (bx + sx) / 2
    my = (by + sy) / 2
    offset = 50

    # Direction perpendicular to the line
    dx = sx - bx
    dy = sy - by
    dist = math.sqrt(dx * dx + dy * dy) or 1
    nx, ny = dx / dist, dy / dist   # unit along tail
    px, py = -dy / dist, dx / dist  # unit perpendicular

    base_w = 10  # half-width at bubble end
    tip_w = 1    # half-width at speaker end

    cp1x = mx + offset * px + 30
    cp1y = my + offset * py - 30

    # --- Step 1: fill a shape whose base is pushed INSIDE the bubble ------
    # This white fill covers the bubble's black outline at the junction.
    inset = 10  # how far inside the bubble the base extends
    ibx = bx - nx * inset
    iby = by - ny * inset

    ctx.move_to(ibx + px * base_w, iby + py * base_w)
    ctx.curve_to(cp1x + px * base_w * 0.5, cp1y + py * base_w * 0.5,
                 cp1x + px * tip_w, cp1y + py * tip_w,
                 sx + px * tip_w, sy + py * tip_w)
    ctx.line_to(sx - px * tip_w, sy - py * tip_w)
    ctx.curve_to(cp1x - px * tip_w, cp1y - py * tip_w,
                 cp1x - px * base_w * 0.5, cp1y - py * base_w * 0.5,
                 ibx - px * base_w, iby - py * base_w)
    ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill()   # white fill only — no stroke on this shape

    # --- Step 2: stroke only the outer side curves (no base line) ---------
    # Left side curve
    ctx.move_to(bx + px * base_w, by + py * base_w)
    ctx.curve_to(cp1x + px * base_w * 0.5, cp1y + py * base_w * 0.5,
                 cp1x + px * tip_w, cp1y + py * tip_w,
                 sx + px * tip_w, sy + py * tip_w)
    # Tip connection
    ctx.line_to(sx - px * tip_w, sy - py * tip_w)
    # Right side curve (back toward bubble)
    ctx.curve_to(cp1x - px * tip_w, cp1y - py * tip_w,
                 cp1x - px * base_w * 0.5, cp1y - py * base_w * 0.5,
                 bx - px * base_w, by - py * base_w)
    # NOTE: no close_path() — the base stays open so no line at the bubble

    ctx.set_source_rgba(0, 0, 0, 0.9)
    ctx.set_line_width(1.5)
    ctx.stroke()


def connector_s_curve(ctx, bx, by, sx, sy):
    """Style 3: S-shaped double curve — elegant connector."""
    dx = sx - bx
    dy = sy - by

    # Two control points on opposite sides for S-shape
    cp1x = bx + dx * 0.3 + 50
    cp1y = by + dy * 0.3 - 20
    cp2x = bx + dx * 0.7 - 50
    cp2y = by + dy * 0.7 + 20

    ctx.move_to(bx, by)
    ctx.curve_to(cp1x, cp1y, cp2x, cp2y, sx, sy)
    ctx.set_source_rgba(0, 0, 0, 0.85)
    ctx.set_line_width(2.5)
    ctx.stroke()

    # Small arrowhead at speaker end
    angle = math.atan2(sy - cp2y, sx - cp2x)
    arrow_len = 10
    a1 = angle + 2.7
    a2 = angle - 2.7
    ctx.move_to(sx, sy)
    ctx.line_to(sx + arrow_len * math.cos(a1), sy + arrow_len * math.sin(a1))
    ctx.move_to(sx, sy)
    ctx.line_to(sx + arrow_len * math.cos(a2), sy + arrow_len * math.sin(a2))
    ctx.set_line_width(2.5)
    ctx.stroke()


def connector_dotted_curve(ctx, bx, by, sx, sy):
    """Style 4: Dotted/dashed curved line — for thought or whisper."""
    mx = (bx + sx) / 2
    cpx = mx + 35
    cpy = (by + sy) / 2 - 35

    ctx.move_to(bx, by)
    ctx.curve_to(cpx, cpy, cpx, cpy, sx, sy)
    ctx.set_source_rgba(0.3, 0.3, 0.3, 0.8)
    ctx.set_dash([8, 6])
    ctx.set_line_width(2)
    ctx.stroke()
    ctx.set_dash([])  # reset


def connector_thought_bubbles(ctx, bx, by, sx, sy):
    """Style 5: Chain of small circles from bubble to speaker (thought style)."""
    dx = sx - bx
    dy = sy - by
    dist = math.sqrt(dx * dx + dy * dy)
    n_dots = 5
    cpx = (bx + sx) / 2 + 40
    cpy = (by + sy) / 2 - 30

    for i in range(n_dots):
        t = (i + 1) / (n_dots + 1)
        u = 1 - t
        # Quadratic bezier for the path
        px = u * u * bx + 2 * u * t * cpx + t * t * sx
        py = u * u * by + 2 * u * t * cpy + t * t * sy
        # Dots get smaller toward speaker
        r = 7 - i * 1.0

        ctx.arc(px, py, max(r, 2), 0, 2 * math.pi)
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgba(0, 0, 0, 0.9)
        ctx.set_line_width(1.5)
        ctx.stroke()


# ---------------------------------------------------------------------------
# Main — render the showcase
# ---------------------------------------------------------------------------

def main():
    W, H = 1400, 500
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surface)

    # Background
    ctx.rectangle(0, 0, W, H)
    ctx.set_source_rgba(0.95, 0.93, 0.90, 1)
    ctx.fill()

    # Title
    ctx.set_font_size(22)
    ctx.set_source_rgba(0.15, 0.15, 0.15, 1)
    title = "PyCairo Curved Connector Lines — Bubble to Speaker"
    ext = ctx.text_extents(title)
    ctx.move_to(W / 2 - ext.width / 2, 35)
    ctx.show_text(title)

    # Layout: 1 row x 4 cols
    styles = [
        ("1. Tapered Curve",     connector_tapered_curve),
        ("2. S-Curve + Arrow",   connector_s_curve),
        ("3. Dotted Curve",      connector_dotted_curve),
        ("4. Thought Circles",   connector_thought_bubbles),
    ]

    cols, rows = 4, 1
    cell_w = W / cols
    cell_h = (H - 60) / rows

    for idx, (label, func) in enumerate(styles):
        col = idx % cols
        row = idx // cols
        ox = col * cell_w
        oy = 55 + row * cell_h

        # Cell border
        ctx.rectangle(ox + 5, oy + 5, cell_w - 10, cell_h - 10)
        ctx.set_source_rgba(0.85, 0.83, 0.80, 1)
        ctx.set_line_width(1)
        ctx.stroke()

        # Label
        ctx.set_font_size(13)
        ctx.set_source_rgba(0.2, 0.2, 0.2, 1)
        lext = ctx.text_extents(label)
        ctx.move_to(ox + cell_w / 2 - lext.width / 2, oy + 25)
        ctx.show_text(label)

        # Bubble position (upper area of cell)
        bub_cx = ox + cell_w / 2
        bub_cy = oy + cell_h * 0.35
        bub_rx, bub_ry = 70, 35

        # Speaker position (lower-right of cell)
        spk_x = ox + cell_w * 0.7
        spk_y = oy + cell_h * 0.82

        # Draw bubble
        draw_bubble(ctx, bub_cx, bub_cy, bub_rx, bub_ry, "Hello!")

        # Draw speaker
        draw_speaker(ctx, spk_x, spk_y,
                     color=(0.3 + col * 0.15, 0.4, 0.7 - row * 0.2))

        # Attach point: bottom of bubble
        attach_x = bub_cx + 10
        attach_y = bub_cy + bub_ry

        # Draw connector
        func(ctx, attach_x, attach_y, spk_x, spk_y - 22)

    # Save
    surface.write_to_png("curved_connector_demo.png")
    print("Saved: curved_connector_demo.png")
    print(f"  Size: {W}x{H}")
    print("  4 connector styles between bubbles and speakers")
    print("  Open with: start curved_connector_demo.png")


if __name__ == "__main__":
    main()
