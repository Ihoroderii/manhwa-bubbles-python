#!/usr/bin/env python
"""
Bubble Tail Showcase — demonstrates smooth curved tails with PyCairo.

Generates a single image with multiple bubble examples:
  1. Rounded bubble + smooth bottom tail
  2. Rounded bubble + left tail
  3. Rounded bubble + right tail
  4. Rounded bubble + top tail
  5. Asymmetric tail (more natural look)
  6. Thought bubble with small circles trail
  7. Shouting bubble with spiky outline + curved tail
  8. Auto-aimed tail (points at a "character" marker)

Run:
    python examples/bubble_tail_showcase.py

Output:
    bubble_tail_showcase.png
"""

import cairo
import math


# ── Helpers ──────────────────────────────────────────────────────────────────

def rounded_rect_path(ctx, x, y, w, h, r):
    """Add a rounded rectangle sub-path (no stroke/fill)."""
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r,     r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0,             math.pi / 2)
    ctx.arc(x + r,     y + h - r, r, math.pi / 2,   math.pi)
    ctx.arc(x + r,     y + r,     r, math.pi,        3 * math.pi / 2)
    ctx.close_path()


def detect_side(bx, by, bw, bh, tip_x, tip_y):
    """Determine which side of the bubble the tail should come from."""
    cx, cy = bx + bw / 2, by + bh / 2
    dx, dy = tip_x - cx, tip_y - cy
    # Compare angles to decide dominant direction
    if abs(dx) > abs(dy):
        return "right" if dx > 0 else "left"
    else:
        return "bottom" if dy > 0 else "top"


def clamp_base(val, low, high):
    return max(low, min(val, high))


# ── Core: speech bubble with smooth curved tail ─────────────────────────────

def speech_bubble_with_tail(ctx, x, y, w, h, r,
                            tail_tip_x, tail_tip_y,
                            tail_side="auto",
                            tail_base_center=None,
                            tail_base_width=60,
                            asymmetry=0,
                            fill=(1, 1, 1),
                            stroke=(0, 0, 0),
                            line_width=3.5):
    """
    Draw a rounded-rect speech bubble with a smooth Bezier tail.

    Args:
        x, y, w, h, r:      Bubble rectangle and corner radius.
        tail_tip_x/y:        Where the tail points (speaker location).
        tail_side:           "bottom", "top", "left", "right", or "auto".
        tail_base_center:    Position along the chosen side (None = auto).
        tail_base_width:     Width of the tail base on the bubble edge.
        asymmetry:           Shift control points for a more natural look.
        fill, stroke:        RGB tuples.
        line_width:          Border thickness.
    """
    if tail_side == "auto":
        tail_side = detect_side(x, y, w, h, tail_tip_x, tail_tip_y)

    # Compute base center and clamp away from corners.
    half_base = tail_base_width / 2

    if tail_side == "bottom":
        base_y = y + h
        if tail_base_center is None:
            tail_base_center = clamp_base(tail_tip_x, x + r + 20, x + w - r - 20)
        else:
            tail_base_center = clamp_base(tail_base_center, x + r + 20, x + w - r - 20)
        left_base  = (tail_base_center - half_base, base_y)
        right_base = (tail_base_center + half_base, base_y)
    elif tail_side == "top":
        base_y = y
        if tail_base_center is None:
            tail_base_center = clamp_base(tail_tip_x, x + r + 20, x + w - r - 20)
        else:
            tail_base_center = clamp_base(tail_base_center, x + r + 20, x + w - r - 20)
        left_base  = (tail_base_center + half_base, base_y)
        right_base = (tail_base_center - half_base, base_y)
    elif tail_side == "left":
        base_x = x
        if tail_base_center is None:
            tail_base_center = clamp_base(tail_tip_y, y + r + 20, y + h - r - 20)
        else:
            tail_base_center = clamp_base(tail_base_center, y + r + 20, y + h - r - 20)
        left_base  = (base_x, tail_base_center - half_base)
        right_base = (base_x, tail_base_center + half_base)
    else:  # right
        base_x = x + w
        if tail_base_center is None:
            tail_base_center = clamp_base(tail_tip_y, y + r + 20, y + h - r - 20)
        else:
            tail_base_center = clamp_base(tail_base_center, y + r + 20, y + h - r - 20)
        left_base  = (base_x, tail_base_center + half_base)
        right_base = (base_x, tail_base_center - half_base)

    tip = (tail_tip_x, tail_tip_y)

    # ── Build the full path: rounded rect + merged tail ──

    ctx.new_path()

    if tail_side == "bottom":
        # Top-left → top-right
        ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
        ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
        # Right side
        ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        # Bottom edge → right base → tail → left base → continue
        ctx.line_to(right_base[0], right_base[1])
        ctx.curve_to(
            right_base[0] + asymmetry,       right_base[1],
            tip[0] + 18 + asymmetry,         tip[1] - 12,
            tip[0],                           tip[1]
        )
        ctx.curve_to(
            tip[0] - 18,                     tip[1] - 12,
            left_base[0],                    left_base[1],
            left_base[0],                    left_base[1]
        )
        # Left side
        ctx.line_to(x + r, y + h)
        ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)

    elif tail_side == "top":
        # Bottom-right → bottom-left
        ctx.move_to(x + w - r, y + h)
        ctx.arc(x + w - r, y + h - r, r, math.pi / 2, 0)  # BR corner (reversed)
        # Actually let's build it clockwise from bottom-left
        ctx.new_path()
        # Bottom-left
        ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
        # Left side
        ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
        # Top edge → left base → tail → right base
        ctx.line_to(right_base[0], right_base[1])  # note: right_base is actually left on screen for "top"
        ctx.curve_to(
            right_base[0],                   right_base[1],
            tip[0] - 18,                     tip[1] + 12,
            tip[0],                          tip[1]
        )
        ctx.curve_to(
            tip[0] + 18 + asymmetry,         tip[1] + 12,
            left_base[0] + asymmetry,        left_base[1],
            left_base[0],                    left_base[1]
        )
        # Top-right corner
        ctx.line_to(x + w - r, y)
        ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
        # Right side
        ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        # Bottom
        ctx.line_to(x + r, y + h)

    elif tail_side == "left":
        # Start from top-right, go clockwise
        ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
        ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
        # Left edge → bottom base → tail → top base
        ctx.line_to(left_base[0], left_base[1])
        ctx.curve_to(
            left_base[0],                    left_base[1],
            tip[0] + 12,                     tip[1] + 18 + asymmetry,
            tip[0],                          tip[1]
        )
        ctx.curve_to(
            tip[0] + 12,                     tip[1] - 18,
            right_base[0],                   right_base[1],
            right_base[0],                   right_base[1]
        )
        ctx.line_to(x, y + r)
        ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)

    else:  # right
        ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
        ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
        # Right edge → top base → tail → bottom base
        ctx.line_to(right_base[0], right_base[1])
        ctx.curve_to(
            right_base[0],                   right_base[1],
            tip[0] - 12,                     tip[1] - 18,
            tip[0],                          tip[1]
        )
        ctx.curve_to(
            tip[0] - 12,                     tip[1] + 18 + asymmetry,
            left_base[0],                    left_base[1],
            left_base[0],                    left_base[1]
        )
        ctx.line_to(x + w, y + h - r)
        ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)

    ctx.close_path()

    ctx.set_source_rgb(*fill)
    ctx.fill_preserve()
    ctx.set_source_rgb(*stroke)
    ctx.set_line_width(line_width)
    ctx.stroke()


# ── Thought bubble trail ────────────────────────────────────────────────────

def thought_bubble(ctx, x, y, w, h, r, tip_x, tip_y,
                   num_circles=3, fill=(1, 1, 1), stroke=(0, 0, 0)):
    """Thought bubble = rounded rect + trail of shrinking circles."""
    # Main bubble
    rounded_rect_path(ctx, x, y, w, h, r)
    ctx.set_source_rgb(*fill)
    ctx.fill_preserve()
    ctx.set_source_rgb(*stroke)
    ctx.set_line_width(3)
    ctx.stroke()

    # Small circles trailing toward speaker
    cx, cy = x + w / 2, y + h
    dx = (tip_x - cx) / (num_circles + 1)
    dy = (tip_y - cy) / (num_circles + 1)
    for i in range(1, num_circles + 1):
        frac = 1 - i / (num_circles + 1)
        radius = 6 + 10 * frac
        px = cx + dx * i
        py = cy + dy * i
        ctx.arc(px, py, radius, 0, 2 * math.pi)
        ctx.set_source_rgb(*fill)
        ctx.fill_preserve()
        ctx.set_source_rgb(*stroke)
        ctx.set_line_width(2)
        ctx.stroke()


# ── Shouting bubble (spiky outline + curved tail) ───────────────────────────

def shout_bubble_with_tail(ctx, x, y, w, h,
                           tip_x, tip_y,
                           spikes=14, spike_depth=15,
                           tail_base_width=50,
                           fill=(1, 1, 1), stroke=(0, 0, 0)):
    """Spiky/shouting bubble with a smooth curved tail."""
    cx, cy = x + w / 2, y + h / 2
    rx, ry = w / 2, h / 2

    # Build spiky ellipse outline points
    points = []
    for i in range(spikes * 2):
        angle = 2 * math.pi * i / (spikes * 2)
        depth = spike_depth if i % 2 == 0 else 0
        px = cx + (rx + depth) * math.cos(angle)
        py = cy + (ry + depth) * math.sin(angle)
        points.append((px, py))

    ctx.new_path()
    ctx.move_to(*points[0])
    for p in points[1:]:
        ctx.line_to(*p)
    ctx.close_path()

    ctx.set_source_rgb(*fill)
    ctx.fill_preserve()
    ctx.set_source_rgb(*stroke)
    ctx.set_line_width(3)
    ctx.stroke()

    # Now add a curved tail from the bottom
    side = detect_side(x, y, w, h, tip_x, tip_y)
    if side == "bottom":
        attach_x, attach_y = cx, y + h + spike_depth
    elif side == "top":
        attach_x, attach_y = cx, y - spike_depth
    elif side == "left":
        attach_x, attach_y = x - spike_depth, cy
    else:
        attach_x, attach_y = x + w + spike_depth, cy

    dx = tip_x - attach_x
    dy = tip_y - attach_y
    dist = math.hypot(dx, dy) or 1
    ux, uy = dx / dist, dy / dist
    px, py = -uy, ux
    hw = tail_base_width / 2

    p1 = (attach_x + px * hw, attach_y + py * hw)
    p2 = (attach_x - px * hw, attach_y - py * hw)
    cp1 = (attach_x + px * hw * 0.4 + ux * dist * 0.5,
           attach_y + py * hw * 0.4 + uy * dist * 0.5)
    cp2 = (attach_x - px * hw * 0.4 + ux * dist * 0.5,
           attach_y - py * hw * 0.4 + uy * dist * 0.5)

    ctx.new_path()
    ctx.move_to(*p1)
    ctx.curve_to(*cp1, tip_x, tip_y, tip_x, tip_y)
    ctx.curve_to(tip_x, tip_y, *cp2, *p2)
    ctx.close_path()
    ctx.set_source_rgb(*fill)
    ctx.fill_preserve()
    ctx.set_source_rgb(*stroke)
    ctx.set_line_width(3)
    ctx.stroke()


# ── Text helper ─────────────────────────────────────────────────────────────

def draw_text(ctx, x, y, w, h, text, size=16, color=(0, 0, 0), padding=18):
    ctx.set_source_rgb(*color)
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    # Simple word-wrap
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        ext = ctx.text_extents(test)
        if ext.width > w - padding * 2 and line:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)

    total_h = len(lines) * (size + 4)
    start_y = y + (h - total_h) / 2 + size
    for i, ln in enumerate(lines):
        ext = ctx.text_extents(ln)
        lx = x + (w - ext.width) / 2
        ly = start_y + i * (size + 4)
        ctx.move_to(lx, ly)
        ctx.show_text(ln)


def draw_label(ctx, x, y, text, size=13, color=(0.4, 0.4, 0.4)):
    ctx.set_source_rgb(*color)
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ctx.move_to(x, y)
    ctx.show_text(text)


def draw_character_marker(ctx, x, y, label="", color=(0.2, 0.6, 0.9)):
    """Small circle + label to show where the 'speaker' is."""
    ctx.arc(x, y, 8, 0, 2 * math.pi)
    ctx.set_source_rgb(*color)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()
    if label:
        ctx.set_font_size(11)
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.move_to(x + 12, y + 4)
        ctx.show_text(label)


# ── Main showcase ───────────────────────────────────────────────────────────

def main():
    W, H = 1400, 1100

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surface)

    # Background
    ctx.set_source_rgb(0.96, 0.95, 0.93)
    ctx.paint()

    # Title
    ctx.set_source_rgb(0.15, 0.15, 0.15)
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(28)
    ctx.move_to(30, 40)
    ctx.show_text("Smooth Curved Bubble Tails — PyCairo Showcase")

    # ─── Row 1: Basic directions ──────────────────────────────────────

    # 1) Bottom tail
    bx, by, bw, bh = 50, 80, 260, 120
    draw_label(ctx, bx, by - 5, "1. Bottom tail")
    speech_bubble_with_tail(ctx, bx, by, bw, bh, 20,
                            tail_tip_x=160, tail_tip_y=290,
                            tail_side="bottom", tail_base_width=60)
    draw_text(ctx, bx, by, bw, bh, "Hello! I'm below.")
    draw_character_marker(ctx, 160, 290, "speaker")

    # 2) Left tail
    bx2, by2 = 400, 80
    draw_label(ctx, bx2, by2 - 5, "2. Left tail")
    speech_bubble_with_tail(ctx, bx2, by2, bw, bh, 20,
                            tail_tip_x=350, tail_tip_y=175,
                            tail_side="left", tail_base_width=50)
    draw_text(ctx, bx2, by2, bw, bh, "Speaker is to my left!")
    draw_character_marker(ctx, 350, 175, "speaker")

    # 3) Right tail
    bx3, by3 = 730, 80
    draw_label(ctx, bx3, by3 - 5, "3. Right tail")
    speech_bubble_with_tail(ctx, bx3, by3, bw, bh, 20,
                            tail_tip_x=1050, tail_tip_y=160,
                            tail_side="right", tail_base_width=50)
    draw_text(ctx, bx3, by3, bw, bh, "Looking right...")
    draw_character_marker(ctx, 1050, 160, "speaker")

    # 4) Top tail
    bx4, by4 = 1060, 130
    draw_label(ctx, bx4, by4 - 5, "4. Top tail")
    speech_bubble_with_tail(ctx, bx4, by4, 280, bh, 20,
                            tail_tip_x=1200, tail_tip_y=70,
                            tail_side="top", tail_base_width=55)
    draw_text(ctx, bx4, by4, 280, bh, "Above me!")
    draw_character_marker(ctx, 1200, 70, "speaker")

    # ─── Row 2: Variations ────────────────────────────────────────────

    # 5) Asymmetric tail (more natural)
    bx5, by5 = 50, 370
    draw_label(ctx, bx5, by5 - 5, "5. Asymmetric (natural)")
    speech_bubble_with_tail(ctx, bx5, by5, 280, 130, 22,
                            tail_tip_x=200, tail_tip_y=600,
                            tail_side="bottom",
                            tail_base_width=65,
                            asymmetry=15)
    draw_text(ctx, bx5, by5, 280, 130, "Slight asymmetry makes it feel more organic.")
    draw_character_marker(ctx, 200, 600, "speaker")

    # 6) Thought bubble
    bx6, by6 = 400, 370
    draw_label(ctx, bx6, by6 - 5, "6. Thought bubble")
    thought_bubble(ctx, bx6, by6, 260, 130, 20,
                   tip_x=480, tip_y=600)
    draw_text(ctx, bx6, by6, 260, 130, "Hmm, I wonder...", size=15)
    draw_character_marker(ctx, 480, 600, "thinker")

    # 7) Shouting bubble + curved tail
    bx7, by7 = 730, 360
    draw_label(ctx, bx7, by7 - 5, "7. Shout + curved tail")
    shout_bubble_with_tail(ctx, bx7, by7, 280, 130,
                           tip_x=870, tip_y=590,
                           spikes=12, spike_depth=14,
                           tail_base_width=45)
    draw_text(ctx, bx7, by7, 280, 130, "STOP RIGHT THERE!!", size=18,
              color=(0.8, 0.1, 0.1))
    draw_character_marker(ctx, 870, 590, "shouter")

    # 8) Auto-aimed tail
    bx8, by8 = 1060, 370
    draw_label(ctx, bx8, by8 - 5, '8. Auto-aimed (side="auto")')
    speaker_x, speaker_y = 1350, 530
    speech_bubble_with_tail(ctx, bx8, by8, 280, 130, 22,
                            tail_tip_x=speaker_x,
                            tail_tip_y=speaker_y,
                            tail_side="auto",
                            tail_base_width=55)
    draw_text(ctx, bx8, by8, 280, 130, "Auto-detects nearest side!")
    draw_character_marker(ctx, speaker_x, speaker_y, "auto")

    # ─── Row 3: Comparison — triangle vs. curved ─────────────────────

    row3_y = 680
    draw_label(ctx, 50, row3_y - 5, "Comparison: OLD triangle tail vs. NEW curved tail")

    # OLD — plain triangle
    ox, oy, ow, oh = 80, row3_y + 10, 260, 120
    rounded_rect_path(ctx, ox, oy, ow, oh, 20)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(3)
    ctx.stroke()
    # Triangle tail
    tri_cx = ox + ow / 2
    tri_by = oy + oh
    ctx.move_to(tri_cx - 25, tri_by)
    ctx.line_to(tri_cx + 25, tri_by)
    ctx.line_to(tri_cx, tri_by + 70)
    ctx.close_path()
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(3)
    ctx.stroke()
    draw_text(ctx, ox, oy, ow, oh, "OLD: stiff triangle", size=14, color=(0.6, 0, 0))
    draw_character_marker(ctx, tri_cx, tri_by + 70 + 15, "speaker")

    # Label arrow
    ctx.set_source_rgb(0.6, 0.6, 0.6)
    ctx.set_font_size(40)
    ctx.move_to(380, row3_y + 80)
    ctx.show_text("→")

    # NEW — smooth curve
    nx, ny = 460, row3_y + 10
    speech_bubble_with_tail(ctx, nx, ny, 260, 120, 20,
                            tail_tip_x=nx + 130, tail_tip_y=ny + 120 + 70,
                            tail_side="bottom", tail_base_width=60)
    draw_text(ctx, nx, ny, 260, 120, "NEW: smooth curve", size=14, color=(0, 0.5, 0))
    draw_character_marker(ctx, nx + 130, ny + 120 + 70 + 15, "speaker")

    # ─── Row 3 continued: wide tail, narrow tail ─────────────────────

    # Wide tail
    wx, wy = 800, row3_y + 10
    draw_label(ctx, wx, row3_y - 5, "Wide base (80px)")
    speech_bubble_with_tail(ctx, wx, wy, 240, 110, 20,
                            tail_tip_x=wx + 120, tail_tip_y=wy + 200,
                            tail_side="bottom",
                            tail_base_width=80)
    draw_text(ctx, wx, wy, 240, 110, "Wide tail base", size=14)
    draw_character_marker(ctx, wx + 120, wy + 200, "")

    # Narrow tail
    rwx, rwy = 1100, row3_y + 10
    draw_label(ctx, rwx, row3_y - 5, "Narrow base (30px)")
    speech_bubble_with_tail(ctx, rwx, rwy, 240, 110, 20,
                            tail_tip_x=rwx + 120, tail_tip_y=rwy + 200,
                            tail_side="bottom",
                            tail_base_width=30)
    draw_text(ctx, rwx, rwy, 240, 110, "Narrow tail", size=14)
    draw_character_marker(ctx, rwx + 120, rwy + 200, "")

    # ─── Footer ──────────────────────────────────────────────────────
    ctx.set_source_rgb(0.5, 0.5, 0.5)
    ctx.set_font_size(12)
    ctx.move_to(30, H - 15)
    ctx.show_text("manhwa-bubbles-python — Bubble Tail Showcase — all tails use curve_to() Bezier paths")

    # Save
    out = "bubble_tail_showcase.png"
    surface.write_to_png(out)
    print(f"Saved: {out}")
    print(f"  Size: {W}x{H}")
    print(f"  8 bubble examples with smooth curved tails")
    print(f"  Open with: start {out}")


if __name__ == "__main__":
    main()
