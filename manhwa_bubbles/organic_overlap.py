"""Organic overlapping oval speech bubble (Cairo-based).

This module integrates the previously standalone overlapping_circles_squares logic
into the manhwa_bubbles library with a simplified public API.

Requires: pycairo
"""
import math, random
try:
    import cairo  # type: ignore
except ImportError as e:  # pragma: no cover
    cairo = None
    _CAIRO_IMPORT_ERROR = e
else:
    _CAIRO_IMPORT_ERROR = None

# Public flags (can be overridden by user before calling)
TRANSPARENT_CANVAS = True
FILL_GAPS_ONLY = True          # minimal ink mode gap filling behavior
DRAW_EMPHASIS_ARCS = True      # draw interior emphasized arcs
DRAW_LAUGH_ENERGY = True       # allow energy ticks when style == 'laugh'
INK_COLOR = (0, 0, 0, 1)

HORIZONTAL_MIN_OVERLAP_FRAC = 0.14
VERTICAL_MIN_OVERLAP_FRAC = 0.14

__all__ = [
    'generate_overlapping_bubble'
]

def _ensure_cairo():
    if cairo is None:
        raise RuntimeError(
            "pycairo is required for generate_overlapping_bubble but is not installed: "
            f"{_CAIRO_IMPORT_ERROR}"
        )

def generate_overlapping_bubble(width=180, height=120, style='organic', show_full_ovals=False,
                                 seed=None, laugh=False):
    """Generate an organic overlapping-ovals speech bubble as a Cairo ImageSurface.

    Args:
        width, height: Interior rectangle dimensions.
        style: 'organic' (default) or 'laugh'.
        show_full_ovals: If True, draw full ovals; else minimal interior arcs mode.
        seed: Optional RNG seed for reproducibility.
        laugh: Convenience flag (if True forces style='laugh').

    Returns:
        (surface, ctx) tuple with rendered bubble on ARGB32 surface.
    """
    _ensure_cairo()
    if laugh:
        style = 'laugh'
    if seed is not None:
        random.seed(seed)

    canvas_w = int(width + 160)
    canvas_h = int(height + 140)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, canvas_w, canvas_h)
    ctx = cairo.Context(surface)
    if not TRANSPARENT_CANVAS:
        ctx.set_source_rgb(1,1,1)
        ctx.paint()

    cx, cy = canvas_w/2, canvas_h/2
    half_w, half_h = width/2, height/2

    circles = _generate_all_side_circles(cx, cy, half_w, half_h, style)
    _enforce_corner_overlaps(circles, cx, cy, half_w, half_h)

    # Base rectangle (only for reference when full ovals shown)
    if show_full_ovals:
        _draw_base_rectangle(ctx, cx, cy, width, height, stroke=True, fill=False)

    if show_full_ovals:
        _draw_full_circles(ctx, circles)

    if style == 'laugh' and DRAW_LAUGH_ENERGY:
        _draw_laugh_energy_lines(ctx, cx, cy, half_w, half_h, circles, background_color=background_color)

    if not show_full_ovals and FILL_GAPS_ONLY:
        _fill_rectangle_gaps_only(ctx, circles, cx, cy, half_w, half_h)

    if DRAW_EMPHASIS_ARCS:
        _emphasize_interior_arcs(ctx, circles, cx, cy, half_w, half_h)

    return surface, ctx

# ---------------- Core geometry / generation ----------------

def _generate_all_side_circles(cx, cy, half_w, half_h, style):
    all_circles = []
    sides = [
        ("top", cx - half_w, cy - half_h, cx + half_w, cy - half_h),
        ("right", cx + half_w, cy - half_h, cx + half_w, cy + half_h),
        ("bottom", cx + half_w, cy + half_h, cx - half_w, cy + half_h),
        ("left", cx - half_w, cy + half_h, cx - half_w, cy - half_h)
    ]
    cid = 0
    for side_name, sx, sy, ex, ey in sides:
        side_len = math.dist((sx,sy),(ex,ey))
        if side_name in ("top","bottom"):
            n = 2 if half_w*2 > half_h*2 else 1
        else:
            n = 2 if half_h*2 > half_w*2 else 1
        if side_len < 80:
            n = 1
        circles = _generate_circles_for_side(sx, sy, ex, ey, side_name, style, n, half_w, half_h, cid)
        all_circles.extend(circles)
        cid += len(circles)
    return all_circles

def _generate_circles_for_side(sx, sy, ex, ey, side, style, num, half_w, half_h, start_id):
    circles = []
    is_horizontal = side in ("top","bottom")
    def r(a,b):
        return random.uniform(a,b)
    # laugh may upgrade counts
    if style == 'laugh':
        side_len_pixels = (half_w*2) if is_horizontal else (half_h*2)
        if side_len_pixels > 140:
            num = max(num,3)
        else:
            num = max(num,2)
    for i in range(num):
        if num == 1:
            t = 0.5 + r(-0.08,0.08)
        else:
            if style=='laugh' and num>=3:
                if i==0: base_t=0.16
                elif i==1: base_t=0.5+r(-0.06,0.06)
                else: base_t=0.84
                t = base_t + r(-0.06,0.065)
                t = max(0.06,min(0.94,t))
            elif style=='laugh' and num==2:
                base_t = 0.22 if i==0 else 0.78
                t = base_t + r(-0.06,0.06)
                t = max(0.07,min(0.93,t))
            else:
                base_t = 0.18 if i==0 else 0.82
                t = base_t + r(-0.05,0.05)
                t = max(0.08,min(0.92,t))
        x = sx + t*(ex-sx)
        y = sy + t*(ey-sy)
        if side=='top': nx,ny=0,-1
        elif side=='bottom': nx,ny=0,1
        elif side=='left': nx,ny=-1,0
        else: nx,ny=1,0
        corner_bias = (num>=2 and (t<0.3 or t>0.7))
        if is_horizontal:
            base_span = 0.74 if num==1 else 0.46 + r(-0.025,0.03)
            if corner_bias: base_span*=0.9
            rx = (half_w*base_span)*r(0.94,1.05)
            ry_base = 0.28 + r(-0.025,0.035)
            if corner_bias: ry_base*=0.9
            ry = (half_h*ry_base)*r(0.92,1.08)
        else:
            base_span = 0.74 if num==1 else 0.46 + r(-0.025,0.03)
            if corner_bias: base_span*=0.9
            ry = (half_h*base_span)*r(0.94,1.05)
            rx_base = 0.28 + r(-0.025,0.035)
            if corner_bias: rx_base*=0.9
            rx = (half_w*rx_base)*r(0.92,1.08)
        if style=='laugh':
            scale_down = 0.78 if num>=3 else 0.85
            rx*=scale_down*r(0.95,1.08)
            ry*=scale_down*r(0.95,1.08)
            if random.random()<0.4:
                if is_horizontal: ry*=r(1.05,1.18)
                else: rx*=r(1.05,1.18)
        if num>=2:
            side_full = (half_w*2) if is_horizontal else (half_h*2)
            center_sep = (0.8-0.2)*side_full
            min_overlap = (HORIZONTAL_MIN_OVERLAP_FRAC if is_horizontal else VERTICAL_MIN_OVERLAP_FRAC)*side_full
            along = rx if is_horizontal else ry
            current = 2*along - center_sep
            if current < min_overlap:
                required = (center_sep + min_overlap)/2.0
                scale = required/along
                if is_horizontal: rx*=scale
                else: ry*=scale
        if num>=2 and (t<0.25 or t>0.75):
            jitter_scale = 1 + r(-0.01,0.015)
            if is_horizontal: rx*=jitter_scale
            else: ry*=jitter_scale
        if is_horizontal:
            inward = ry*(0.38 + r(-0.035,0.04))
            if corner_bias: inward*=0.85
        else:
            inward = rx*(0.48 + r(-0.04,0.05))
            if corner_bias: inward*=0.85
        if style=='laugh':
            inward *= 0.9
        cx_final = x - nx*inward + r(-3.0,3.0)
        cy_final = y - ny*inward + r(-3.0,3.0)
        circles.append({'x':cx_final,'y':cy_final,'rx':rx,'ry':ry,'side':side,'id':start_id+i})
    return circles

def _enforce_corner_overlaps(circles, cx, cy, half_w, half_h):
    by = {'top':[],'right':[],'bottom':[],'left':[]}
    for c in circles:
        if c['side'] in by: by[c['side']].append(c)
    if not all(by.values()): return
    def top_left(): return (min(by['top'], key=lambda c:c['x']), min(by['left'], key=lambda c:c['y']))
    def top_right(): return (max(by['top'], key=lambda c:c['x']), min(by['right'], key=lambda c:c['y']))
    def bottom_right(): return (max(by['bottom'], key=lambda c:c['x']), max(by['right'], key=lambda c:c['y']))
    def bottom_left(): return (min(by['bottom'], key=lambda c:c['x']), max(by['left'], key=lambda c:c['y']))
    corners = [top_left(), top_right(), bottom_right(), bottom_left()]
    MARGIN = 2.0
    for a,b in corners:
        dx = abs(a['x']-b['x'])
        dy = abs(a['y']-b['y'])
        if dx > (a['rx']+b['rx'])-MARGIN:
            need = dx + MARGIN - (a['rx']+b['rx'])
            (a if a['rx']<b['rx'] else b)['rx'] += need
        if dy > (a['ry']+b['ry'])-MARGIN:
            need = dy + MARGIN - (a['ry']+b['ry'])
            (a if a['ry']<b['ry'] else b)['ry'] += need

# ---------------- Drawing helpers ----------------

def _draw_base_rectangle(ctx, cx, cy, w, h, stroke=True, fill=False):
    hw, hh = w/2, h/2
    ctx.rectangle(cx-hw, cy-hh, w, h)
    if fill:
        ctx.set_source_rgba(1,1,1,1)
        ctx.fill_preserve()
    else:
        ctx.new_path()
    if stroke:
        ctx.set_source_rgba(*INK_COLOR)
        ctx.set_line_width(2.5)
        ctx.stroke()
    else:
        ctx.new_path()

def _draw_full_circles(ctx, circles):
    for c in sorted(circles, key=lambda cc: math.hypot(cc['x'], cc['y']), reverse=True):
        ctx.save()
        ctx.translate(c['x'], c['y'])
        ctx.scale(c['rx'], c['ry'])
        ctx.arc(0,0,1,0,2*math.pi)
        ctx.restore()
        ctx.set_source_rgba(0,0,0,0.6)
        ctx.set_line_width(2.0)
        ctx.stroke()

def _fill_rectangle_gaps_only(ctx, circles, cx, cy, hw, hh):
    ctx.save()
    ctx.set_source_rgba(1,1,1,1)
    ctx.rectangle(cx-hw, cy-hh, hw*2, hh*2)
    ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    for c in circles:
        ctx.save(); ctx.translate(c['x'], c['y']); ctx.scale(c['rx'], c['ry']); ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.restore()

def _point_inside_circle(px, py, c):
    dx = (px - c['x'])/c['rx']
    dy = (py - c['y'])/c['ry']
    return dx*dx + dy*dy <= 1.0

def _emphasize_interior_arcs(ctx, circles, cx, cy, hw, hh):
    rect_left, rect_right = cx-hw, cx+hw
    rect_top, rect_bottom = cy-hh, cy+hh
    ctx.save()
    ctx.set_source_rgba(0,0,0,1)
    ctx.set_line_width(2.4)
    for c in circles:
        samples = 120
        pts = []
        for i in range(samples+1):
            ang = 2*math.pi * i / samples
            px = c['x'] + c['rx']*math.cos(ang)
            py = c['y'] + c['ry']*math.sin(ang)
            if rect_left <= px <= rect_right and rect_top <= py <= rect_bottom:
                pts.append((px,py))
            else:
                if len(pts) > 3:
                    ctx.move_to(*pts[0])
                    for q in pts[1:]:
                        ctx.line_to(*q)
                    ctx.stroke()
                pts = []
        if len(pts) > 3:
            ctx.move_to(*pts[0])
            for q in pts[1:]:
                ctx.line_to(*q)
            ctx.stroke()
    ctx.restore()

def _draw_laugh_energy_lines(ctx, cx, cy, hw, hh, circles, background_color=None):
    """Draw laugh energy lines with background-aware color.
    
    Args:
        background_color: Optional tuple (r, g, b, a) or (r, g, b) for background color.
                         If dark, uses bright lines; if light, uses black lines.
    """
    ctx.save()
    
    # Determine line color based on background
    if background_color is not None:
        # Extract RGB values (handle both 3 and 4 component tuples)
        if len(background_color) >= 3:
            bg_r, bg_g, bg_b = background_color[0], background_color[1], background_color[2]
            # Calculate luminance to determine if background is dark
            luminance = 0.299 * bg_r + 0.587 * bg_g + 0.114 * bg_b
            
            if luminance < 0.5:  # Dark background
                # Use bright color (white or yellow) for contrast
                ctx.set_source_rgba(1.0, 1.0, 0.7, 0.8)  # Light yellow/white
            else:  # Light background
                ctx.set_source_rgba(0, 0, 0, 0.65)  # Black
        else:
            ctx.set_source_rgba(0, 0, 0, 0.65)  # Default black
    else:
        # Default: assume light background, use black lines
        ctx.set_source_rgba(0, 0, 0, 0.65)
    
    ctx.set_line_width(2.0)
    num_rays = 18
    outer_rx = hw + 24
    outer_ry = hh + 24
    for i in range(num_rays):
        ang = (2*math.pi) * (i/num_rays) + random.uniform(-0.05,0.05)
        if random.random() < 0.18:
            continue
        base_len = random.uniform(10,24)
        sx = cx + math.cos(ang)*(outer_rx + random.uniform(-4,4))
        sy = cy + math.sin(ang)*(outer_ry + random.uniform(-4,4))
        ex = sx + math.cos(ang)*base_len
        ey = sy + math.sin(ang)*base_len
        ctx.move_to(sx, sy); ctx.line_to(ex, ey)
    ctx.stroke()
    ctx.restore()
