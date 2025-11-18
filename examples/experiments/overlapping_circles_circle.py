import cairo, math, random
from overlapping_circles_squares import (
    generate_side_circles,
    enforce_corner_overlaps,
    draw_overlapping_circles,
    fill_rectangle_gaps_only,  # reuse logic for clearing interiors, though name references rectangle
    emphasize_border_crossing_pixels, # we will adapt a circle emphasize variant inline
    point_inside_circle,
    INK_COLOR,
    EMPHASIZE_INTERIOR_ARCS,
    RECTANGLE_FILL_IN_MINIMAL,
    FILL_GAPS_ONLY,
    TRANSPARENT_CANVAS,
    DRAW_TEXT,
    draw_overlap_text
)

# Control whether the base circle outline is drawn at all (user requested to hide it)
DRAW_BASE_CIRCLE_STROKE = False

# Control whether we draw emphasized oval border segments that lie OUTSIDE the base circle.
# User requested to remove those borders, so default is now False.
DRAW_OUTSIDE_OVAL_SEGMENTS = False

# Local copy of functions specialized for circle variant (kept minimal)

def draw_base_circle(ctx, cx, cy, radius, stroke=True, fill=True):
    ctx.save()
    ctx.arc(cx, cy, radius, 0, 2*math.pi)
    if fill:
        ctx.set_source_rgba(1,1,1,1)
        ctx.fill_preserve()
    else:
        ctx.new_path(); ctx.arc(cx, cy, radius, 0, 2*math.pi)
    if stroke and DRAW_BASE_CIRCLE_STROKE:
        ctx.set_source_rgba(*INK_COLOR)
        ctx.set_line_width(2.5)
        ctx.stroke()
    else:
        ctx.new_path()
    ctx.restore()

def draw_uncrossed_circle_border(ctx, all_circles, cx, cy, radius):
    num_samples = 360
    points = []
    for i in range(num_samples+1):
        ang = 2*math.pi * (i/num_samples)
        px = cx + radius * math.cos(ang)
        py = cy + radius * math.sin(ang)
        covered = False
        for circle in all_circles:
            if point_inside_circle(px, py, circle):
                covered = True
                break
        points.append((px, py, covered))
    ctx.set_source_rgba(*INK_COLOR)
    ctx.set_line_width(2.5)
    drawing = False
    for px, py, covered in points:
        if not covered and not drawing:
            ctx.move_to(px, py); drawing = True
        elif not covered and drawing:
            ctx.line_to(px, py)
        elif covered and drawing:
            ctx.stroke(); drawing = False
    if drawing:
        ctx.stroke()

def emphasize_border_crossing_pixels_circle(ctx, all_circles, cx, cy, radius):
    circle_left = cx - radius
    circle_right = cx + radius
    circle_top = cy - radius
    circle_bottom = cy + radius
    # Reuse emphasize logic by calling original rectangle function with square bounds of circle
    for circle in all_circles:
        # import local function from squares file would cause recursion; replicate small part directly
        # simplified from original find_crossing_border_segments -> inline sampling
        crossing_segments = []
        cxm, cym = circle['x'], circle['y']
        rx, ry = circle['rx'], circle['ry']
        num_samples = int(max(rx, ry) * 10)
        border_points = []
        for i in range(num_samples):
            angle = (2 * math.pi * i) / num_samples
            px = cxm + rx * math.cos(angle)
            py = cym + ry * math.sin(angle)
            inside = (circle_left <= px <= circle_right and circle_top <= py <= circle_bottom)
            cov = False
            if inside:
                for other in all_circles:
                    if other is circle:
                        continue
                    if point_inside_circle(px, py, other):
                        cov = True; break
            border_points.append({'x':px,'y':py,'em': inside and not cov})
        seg=[]
        for p in border_points:
            if p['em']:
                seg.append(p)
            else:
                if len(seg)>2:
                    crossing_segments.append(seg)
                seg=[]
        if len(seg)>2:
            crossing_segments.append(seg)
        ctx.set_source_rgba(0,0,0,0.9)
        ctx.set_line_width(4.0)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for seg in crossing_segments:
            ctx.move_to(seg[0]['x'], seg[0]['y'])
            for sp in seg[1:]:
                ctx.line_to(sp['x'], sp['y'])
            ctx.stroke()

def emphasize_circle_boundary_crossings(ctx, all_circles, cx, cy, radius):
    """Emphasize portions of the circle boundary that are hidden/covered by side ovals.
    We sample the circle perimeter; any sample point lying inside any oval marks a covered segment.
    Segments are then stroked with a thinner, semi-transparent line to suggest occlusion behind foreground ovals."""
    num_samples = 720
    samples = []
    for i in range(num_samples+1):
        ang = 2*math.pi*(i/num_samples)
        px = cx + radius * math.cos(ang)
        py = cy + radius * math.sin(ang)
        covered = False
        for circle in all_circles:
            if point_inside_circle(px, py, circle):
                covered = True
                break
        samples.append((px, py, covered))
    # collect contiguous covered segments
    segments = []
    cur = []
    for px, py, covered in samples:
        if covered:
            cur.append((px, py))
        else:
            if len(cur) > 2:
                segments.append(cur)
            cur = []
    if len(cur) > 2:
        segments.append(cur)
    if not segments:
        return
    ctx.save()
    ctx.set_source_rgba(0,0,0,0.35)  # lighter ink for behind effect
    ctx.set_line_width(2.0)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for seg in segments:
        ctx.move_to(seg[0][0], seg[0][1])
        for (px,py) in seg[1:]:
            ctx.line_to(px, py)
        ctx.stroke()
    ctx.restore()

def emphasize_oval_segments_outside_circle(ctx, all_circles, cx, cy, radius):
    """Emphasize only the border segments of each oval that lie OUTSIDE the base circle.
    Approach: sample each oval perimeter; classify points as outside (distance to center > radius + small epsilon) and
    not covered by any other oval to avoid double-thick clutter. Then stroke those segments."""
    eps = 0.5
    for circle in all_circles:
        cxm, cym = circle['x'], circle['y']
        rx, ry = circle['rx'], circle['ry']
        num_samples = int(max(rx, ry) * 9)
        pts = []
        for i in range(num_samples):
            ang = 2*math.pi*(i/num_samples)
            px = cxm + rx*math.cos(ang)
            py = cym + ry*math.sin(ang)
            dist_center = math.hypot(px - cx, py - cy)
            outside = dist_center > (radius + eps)
            covered = False
            if outside:
                for other in all_circles:
                    if other is circle:
                        continue
                    if point_inside_circle(px, py, other):
                        covered = True; break
            pts.append((px, py, outside and not covered))
        segments = []
        cur = []
        for px, py, flag in pts:
            if flag:
                cur.append((px, py))
            else:
                if len(cur) > 2:
                    segments.append(cur)
                cur = []
        if len(cur) > 2:
            segments.append(cur)
        if not segments:
            continue
        ctx.save()
        ctx.set_source_rgba(0,0,0,0.9)
        ctx.set_line_width(4.0)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for seg in segments:
            ctx.move_to(seg[0][0], seg[0][1])
            for (px, py) in seg[1:]:
                ctx.line_to(px, py)
            ctx.stroke()
        ctx.restore()

def create_overlapping_circles_circle(ctx, cx, cy, radius, text="", circle_style="varied", show_full_ovals=True, return_circles=False):
    half_w = half_h = radius
    all_circles = generate_side_circles(cx, cy, half_w, half_h, circle_style)
    enforce_corner_overlaps(all_circles, cx, cy, half_w, half_h)
    draw_base_circle(ctx, cx, cy, radius, stroke=show_full_ovals, fill=show_full_ovals and RECTANGLE_FILL_IN_MINIMAL)
    if show_full_ovals:
        draw_overlapping_circles(ctx, all_circles, cx, cy, radius*2, radius*2)
        draw_uncrossed_circle_border(ctx, all_circles, cx, cy, radius)
    else:
        if FILL_GAPS_ONLY:
            ctx.save(); ctx.set_source_rgba(1,1,1,1); ctx.arc(cx, cy, radius, 0, 2*math.pi); ctx.fill(); ctx.set_operator(cairo.OPERATOR_CLEAR)
            for circle in all_circles:
                ctx.save(); ctx.translate(circle['x'], circle['y']); ctx.scale(circle['rx'], circle['ry']); ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); ctx.fill()
            ctx.set_operator(cairo.OPERATOR_OVER); ctx.restore()
    if EMPHASIZE_INTERIOR_ARCS:
        emphasize_border_crossing_pixels_circle(ctx, all_circles, cx, cy, radius)
    else:
        if DRAW_OUTSIDE_OVAL_SEGMENTS:
            emphasize_oval_segments_outside_circle(ctx, all_circles, cx, cy, radius)
    if DRAW_TEXT and text and not return_circles:
        draw_overlap_text(ctx, cx, cy, text)
    if return_circles:
        return all_circles


# --- 7-Oval Radial Variant (reintroduced only for circle base on request) ---
def generate_radial_ovals_7(cx, cy, core_radius, style="organic"):
    """Generate exactly 7 ovals arranged radially around a center circle boundary.
    Keeps mild overlaps & inward intrusion for interior arcs while preserving a clear central void.
    Simplified (no rotation) per earlier revert preference."""
    total = 7
    circles = []
    ring_radius = core_radius * 1.42  # distance of centers from center
    for i in range(total):
        t = i / total
        ang = 2*math.pi*t
        # jitter
        ang += random.uniform(-0.06, 0.06)
        radial_jitter = random.uniform(-4,4)
        ca, sa = math.cos(ang), math.sin(ang)
        center_dist = ring_radius + radial_jitter
        cx_i = cx + ca*center_dist
        cy_i = cy + sa*center_dist
        # base radii slightly elongated tangentially (approx by weighting cos/sin)
        base_r = core_radius * 0.55
        if style == "laugh":
            base_r *= random.uniform(0.8, 0.92)
        # Variation outward vs inward
        rx = base_r * (1.0 + 0.22*abs(ca) * random.uniform(0.7,1.05))
        ry = base_r * (1.0 + 0.22*abs(sa) * random.uniform(0.7,1.05))
        # inward pull to ensure intersection with central boundary for interior emphasis lines
        inward_pull = core_radius * 0.28
        cx_i -= ca * inward_pull * random.uniform(0.8, 1.05)
        cy_i -= sa * inward_pull * random.uniform(0.8, 1.05)
        circles.append({'x': cx_i, 'y': cy_i, 'rx': rx, 'ry': ry, 'side': 'radial7', 'id': i})
    # First, enforce at least touching between neighbors by shifting centers inward or toward each other
    _ensure_min_touch(circles, min_overlap_frac=0.02, max_iterations=3)
    # Light pass scaling (kept but mild) to guarantee minimal overlap thickness
    _ensure_neighbor_overlap_simple(circles, target_overlap_frac=0.12)
    return circles

def _ensure_neighbor_overlap_simple(circles, target_overlap_frac=0.16):
    if len(circles) < 2:
        return
    # order by angle about centroid
    avg_x = sum(c['x'] for c in circles)/len(circles)
    avg_y = sum(c['y'] for c in circles)/len(circles)
    ordered = sorted(circles, key=lambda c: math.atan2(c['y']-avg_y, c['x']-avg_x))
    n = len(ordered)
    for i in range(n):
        a = ordered[i]; b = ordered[(i+1)%n]
        dx = b['x'] - a['x']; dy = b['y'] - a['y']
        center_dist = math.hypot(dx, dy)
        eff_a = min(a['rx'], a['ry'])
        eff_b = min(b['rx'], b['ry'])
        required = target_overlap_frac * 0.5 * (eff_a + eff_b)
        current = eff_a + eff_b - center_dist
        if current < required:
            deficit = required - current
            if eff_a < eff_b:
                scale = (eff_a + deficit/2)/eff_a
                a['rx'] *= scale; a['ry'] *= scale
            else:
                scale = (eff_b + deficit/2)/eff_b
                b['rx'] *= scale; b['ry'] *= scale

def _ensure_min_touch(circles, min_overlap_frac=0.0, max_iterations=2):
    """Adjust neighboring radial ovals so every adjacent pair at least touches (or slightly overlaps).

    We keep the original radii (to preserve intended negative space) and instead translate centers
    along the line connecting each pair to close gaps. Iterative passes help because moving one pair
    can open/close gaps with its other neighbor.

    min_overlap_frac: fraction of the average (min-axis) radii we want as positive overlap. 0 means just touching.
    """
    if len(circles) < 2:
        return
    for _ in range(max_iterations):
        # recompute ordering each iteration (centers may shift)
        avg_x = sum(c['x'] for c in circles)/len(circles)
        avg_y = sum(c['y'] for c in circles)/len(circles)
        ordered = sorted(circles, key=lambda c: math.atan2(c['y']-avg_y, c['x']-avg_x))
        n = len(ordered)
        any_change = False
        for i in range(n):
            a = ordered[i]; b = ordered[(i+1)%n]
            dx = b['x'] - a['x']; dy = b['y'] - a['y']
            d = math.hypot(dx, dy)
            eff_a = min(a['rx'], a['ry'])
            eff_b = min(b['rx'], b['ry'])
            desired_max_dist = eff_a + eff_b - min_overlap_frac * 0.5 * (eff_a + eff_b)
            if d > desired_max_dist and d > 1e-6:
                gap = d - desired_max_dist
                ux = dx / d; uy = dy / d
                # Move each center half the needed gap toward the other
                shift = gap * 0.5
                a['x'] += ux * shift
                a['y'] += uy * shift
                b['x'] -= ux * shift
                b['y'] -= uy * shift
                any_change = True
        if not any_change:
            break

def create_overlapping_circles_circle_radial7(ctx, cx, cy, radius, text="", style="organic", show_full_ovals=False, return_circles=False):
    """Circle base variant using exactly 7 radial ovals instead of side-based generation."""
    all_circles = generate_radial_ovals_7(cx, cy, radius, style)
    draw_base_circle(ctx, cx, cy, radius, stroke=show_full_ovals, fill=show_full_ovals and RECTANGLE_FILL_IN_MINIMAL)
    if show_full_ovals:
        draw_overlapping_circles(ctx, all_circles, cx, cy, radius*2, radius*2)
        draw_uncrossed_circle_border(ctx, all_circles, cx, cy, radius)
    else:
        if FILL_GAPS_ONLY:
            ctx.save(); ctx.set_source_rgba(1,1,1,1); ctx.arc(cx, cy, radius, 0, 2*math.pi); ctx.fill(); ctx.set_operator(cairo.OPERATOR_CLEAR)
            for circle in all_circles:
                ctx.save(); ctx.translate(circle['x'], circle['y']); ctx.scale(circle['rx'], circle['ry']); ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); ctx.fill()
            ctx.set_operator(cairo.OPERATOR_OVER); ctx.restore()
    if EMPHASIZE_INTERIOR_ARCS:
        emphasize_border_crossing_pixels_circle(ctx, all_circles, cx, cy, radius)
    else:
        if DRAW_OUTSIDE_OVAL_SEGMENTS:
            emphasize_oval_segments_outside_circle(ctx, all_circles, cx, cy, radius)
    if DRAW_TEXT and text and not return_circles:
        draw_overlap_text(ctx, cx, cy, text)
    if return_circles:
        return all_circles

def generate_radial_ovals_5(cx, cy, core_radius, style="organic"):
    """Generate exactly 5 CIRCLES (not elongated ovals) with enlarged central space.

    Changes:
      - Perfect circles: rx == ry for uniform look.
      - Larger ring radius for more interior negative space.
      - Reduced inward pull so circles intrude less toward center.
      - Slightly lower overlap fraction keeps them just touching.
    """
    total = 5
    circles = []
    ring_radius = core_radius * 1.70  # further increased for more interior space
    for i in range(total):
        t = i / total
        ang = 2*math.pi*t + random.uniform(-0.05, 0.05)
        radial_jitter = random.uniform(-5,5)
        ca, sa = math.cos(ang), math.sin(ang)
        center_dist = ring_radius + radial_jitter
        cx_i = cx + ca*center_dist
        cy_i = cy + sa*center_dist
        base_r = core_radius * 0.46  # smaller circles to widen center void
        if style == "laugh":
            base_r *= random.uniform(0.82, 0.92)
        rx = ry = base_r  # enforce circle
        inward_pull = core_radius * 0.10  # even less inward intrusion
        cx_i -= ca * inward_pull * random.uniform(0.75, 0.95)
        cy_i -= sa * inward_pull * random.uniform(0.75, 0.95)
        circles.append({'x': cx_i, 'y': cy_i, 'rx': rx, 'ry': ry, 'side': 'radial5', 'id': i})
    _ensure_min_touch(circles, min_overlap_frac=0.003, max_iterations=3)
    _ensure_neighbor_overlap_simple(circles, target_overlap_frac=0.045)
    return circles

# --- 6-Oval Radial Variant (elongated ovals) ---
def generate_radial_ovals_6(cx, cy, core_radius, style="organic"):
    """Generate exactly 6 ovals radially but make each oval longer (more elongated).

    Design choices:
      - Ring radius sits between 5 + 7 variants.
      - Base radius slightly larger, then stretch one axis to exaggerate length.
      - Orientation: since we keep axis-aligned ellipses (no rotation), we choose which axis to stretch
        based on whether the oval is predominantly positioned horizontally or vertically around the ring.
      - Reduced inward pull to keep interior openness despite longer shapes.
    """
    total = 6
    circles = []
    ring_radius = core_radius * 1.46
    for i in range(total):
        t = i / total
        ang = 2*math.pi*t + random.uniform(-0.05, 0.05)
        radial_jitter = random.uniform(-5,5)
        ca, sa = math.cos(ang), math.sin(ang)
        center_dist = ring_radius + radial_jitter
        cx_i = cx + ca*center_dist
        cy_i = cy + sa*center_dist
        # Start with a moderate base radius then elongate
        base_r = core_radius * 0.58
        if style == "laugh":
            base_r *= random.uniform(0.80, 0.9)
        # Initial anisotropy similar to others
        rx = base_r * (1.0 + 0.20*abs(ca) * random.uniform(0.7,1.05))
        ry = base_r * (1.0 + 0.20*abs(sa) * random.uniform(0.7,1.05))
        # Elongation pass: stretch dominant axis depending on placement for a "long" look
        if abs(ca) > abs(sa):
            # Mostly left/right; stretch vertical axis to create tall side ovals
            ry *= random.uniform(1.25, 1.42)
        else:
            # Mostly top/bottom; stretch horizontal axis to create wide top/bottom ovals
            rx *= random.uniform(1.25, 1.42)
        # Slight global random extra elongation
        elong_boost = random.uniform(1.0, 1.08)
        rx *= elong_boost; ry *= elong_boost
        inward_pull = core_radius * 0.22
        cx_i -= ca * inward_pull * random.uniform(0.75, 1.0)
        cy_i -= sa * inward_pull * random.uniform(0.75, 1.0)
        circles.append({'x': cx_i, 'y': cy_i, 'rx': rx, 'ry': ry, 'side': 'radial6', 'id': i})
    # Ensure touching, then mild overlap scaling
    _ensure_min_touch(circles, min_overlap_frac=0.015, max_iterations=3)
    _ensure_neighbor_overlap_simple(circles, target_overlap_frac=0.09)
    return circles

def create_overlapping_circles_circle_radial6(ctx, cx, cy, radius, text="", style="organic", show_full_ovals=False, return_circles=False):
    all_circles = generate_radial_ovals_6(cx, cy, radius, style)
    draw_base_circle(ctx, cx, cy, radius, stroke=show_full_ovals, fill=show_full_ovals and RECTANGLE_FILL_IN_MINIMAL)
    if show_full_ovals:
        draw_overlapping_circles(ctx, all_circles, cx, cy, radius*2, radius*2)
        draw_uncrossed_circle_border(ctx, all_circles, cx, cy, radius)
    else:
        if FILL_GAPS_ONLY:
            ctx.save(); ctx.set_source_rgba(1,1,1,1); ctx.arc(cx, cy, radius, 0, 2*math.pi); ctx.fill(); ctx.set_operator(cairo.OPERATOR_CLEAR)
            for circle in all_circles:
                ctx.save(); ctx.translate(circle['x'], circle['y']); ctx.scale(circle['rx'], circle['ry']); ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); ctx.fill()
            ctx.set_operator(cairo.OPERATOR_OVER); ctx.restore()
    if EMPHASIZE_INTERIOR_ARCS:
        emphasize_border_crossing_pixels_circle(ctx, all_circles, cx, cy, radius)
    else:
        if DRAW_OUTSIDE_OVAL_SEGMENTS:
            emphasize_oval_segments_outside_circle(ctx, all_circles, cx, cy, radius)
    if DRAW_TEXT and text and not return_circles:
        draw_overlap_text(ctx, cx, cy, text)
    if return_circles:
        return all_circles

def circle_demo_6(seed=777, width=420, height=320):
    random.seed(seed)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    if not TRANSPARENT_CANVAS:
        ctx.set_source_rgb(1,1,1); ctx.paint()
    cx, cy = width/2, height/2
    create_overlapping_circles_circle_radial6(ctx, cx, cy, 110, "", "organic", show_full_ovals=False)
    out = "overlapping_circles_center_circle_6.png"
    surface.write_to_png(out)
    print(f"🟠 Saved 6-radial elongated center-circle variant '{out}'")

def create_overlapping_circles_circle_radial5(ctx, cx, cy, radius, text="", style="organic", show_full_ovals=False, return_circles=False):
    all_circles = generate_radial_ovals_5(cx, cy, radius, style)
    draw_base_circle(ctx, cx, cy, radius, stroke=show_full_ovals, fill=show_full_ovals and RECTANGLE_FILL_IN_MINIMAL)
    if show_full_ovals:
        draw_overlapping_circles(ctx, all_circles, cx, cy, radius*2, radius*2)
        draw_uncrossed_circle_border(ctx, all_circles, cx, cy, radius)
    else:
        if FILL_GAPS_ONLY:
            ctx.save(); ctx.set_source_rgba(1,1,1,1); ctx.arc(cx, cy, radius, 0, 2*math.pi); ctx.fill(); ctx.set_operator(cairo.OPERATOR_CLEAR)
            for circle in all_circles:
                ctx.save(); ctx.translate(circle['x'], circle['y']); ctx.scale(circle['rx'], circle['ry']); ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); ctx.fill()
            ctx.set_operator(cairo.OPERATOR_OVER); ctx.restore()
    if EMPHASIZE_INTERIOR_ARCS:
        emphasize_border_crossing_pixels_circle(ctx, all_circles, cx, cy, radius)
    else:
        if DRAW_OUTSIDE_OVAL_SEGMENTS:
            emphasize_oval_segments_outside_circle(ctx, all_circles, cx, cy, radius)
    if DRAW_TEXT and text and not return_circles:
        draw_overlap_text(ctx, cx, cy, text)
    if return_circles:
        return all_circles

def circle_demo_5(seed=654, width=420, height=320):
    random.seed(seed)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    if not TRANSPARENT_CANVAS:
        ctx.set_source_rgb(1,1,1); ctx.paint()
    cx, cy = width/2, height/2
    create_overlapping_circles_circle_radial5(ctx, cx, cy, 110, "", "organic", show_full_ovals=False)
    out = "overlapping_circles_center_circle_5.png"
    surface.write_to_png(out)
    print(f"🟢 Saved 5-radial center-circle variant '{out}'")

def circle_demo_7(seed=987, width=420, height=320):
    random.seed(seed)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    if not TRANSPARENT_CANVAS:
        ctx.set_source_rgb(1,1,1); ctx.paint()
    cx, cy = width/2, height/2
    create_overlapping_circles_circle_radial7(ctx, cx, cy, 110, "", "organic", show_full_ovals=False)
    out = "overlapping_circles_center_circle_7.png"
    surface.write_to_png(out)
    print(f"🟣 Saved 7-radial center-circle variant '{out}'")


def circle_demo(seed=321, width=420, height=320):
    random.seed(seed)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    if not TRANSPARENT_CANVAS:
        ctx.set_source_rgb(1,1,1); ctx.paint()
    cx, cy = width/2, height/2
    create_overlapping_circles_circle(ctx, cx, cy, 110, "", "organic", show_full_ovals=False)
    out = "overlapping_circles_center_circle.png"
    surface.write_to_png(out)
    print(f"🔵 Saved center-circle variant '{out}' (separate file)")

if __name__ == "__main__":
    circle_demo()
    circle_demo_7()
    circle_demo_5()
    circle_demo_6()
