import cairo
import math
import random

# -------------------------------------------------------------
# Configuration flags for minimal (ink-only) manga bubble style
# -------------------------------------------------------------
TRANSPARENT_CANVAS = True          # If True, don't paint a background
RECTANGLE_FILL_IN_MINIMAL = False  # Don't fill whole rectangle in minimal mode
FILL_GAPS_ONLY = True              # New: fill only interior regions between ovals
DRAW_TEXT = False                  # Suppress text to keep interior visually clear
INK_COLOR = (0, 0, 0, 1)
EMPHASIZE_INTERIOR_ARCS = False  # Disabled to remove interior emphasized oval arc strokes

# Style presets (we add a 'laugh' style focusing on frenetic, bouncy perimeter)
SUPPORTED_STYLES = {"varied", "organic", "laugh"}

# Geometry control constants
# How far (inward) each oval should penetrate past the rectangle edge (as fraction of smaller half dimension)
PENETRATION_RATIO_SINGLE = 0.22  # single oval on a short side
PENETRATION_RATIO_DOUBLE = 0.18  # each oval when there are two on a long side

# Minimum required overlap between two ovals placed on the same side (as fraction of side length)
SAME_SIDE_REQUIRED_OVERLAP = 0.28
HORIZONTAL_MIN_OVERLAP_FRAC = 0.14  # fraction of side length that top/bottom pair must overlap
VERTICAL_MIN_OVERLAP_FRAC = 0.14    # fraction for left/right pair

# Corner adjacency extra growth factor so corner ovals meet neighbors from perpendicular sides
CORNER_GROWTH = 1.08

def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def create_overlapping_circles_square(ctx, cx, cy, base_width, base_height,
                                      text="OVERLAP!", circle_style="varied", show_full_ovals=True,
                                      return_circles=False, background_color=None):
    """Create a rectangle with overlapping circles/ovals on all sides.
    If show_full_ovals is False, only the emphasized interior crossing segments are rendered (minimal manga style)."""
    
    # Calculate base rectangle
    half_width = base_width / 2
    half_height = base_height / 2
    
    # Generate overlapping circles for each side
    all_circles = generate_side_circles(cx, cy, half_width, half_height, circle_style)

    # Enforce that corner-adjacent ovals actually overlap (e.g. right with bottom at bottom-right corner)
    enforce_corner_overlaps(all_circles, cx, cy, half_width, half_height)
    
    # Draw the main rectangle FIRST (fill only if we plan to hide covered border portions)
    draw_base_rectangle(ctx, cx, cy, base_width, base_height,
                        stroke=show_full_ovals,
                        fill=show_full_ovals and RECTANGLE_FILL_IN_MINIMAL)
    
    # BEFORE clipping: Draw connection lines to outside intersections
    draw_outside_intersection_connections(ctx, all_circles, cx, cy, half_width, half_height)
    
    # Optionally draw all circles (full ovals) or skip to only show emphasized interior arcs
    if show_full_ovals:
        draw_overlapping_circles(ctx, all_circles, cx, cy, base_width, base_height)

    # Extra laugh style embellishments (after circles so we can sit beneath emphasized arcs if minimal mode)
    if circle_style == "laugh":
        # Detect background color from canvas (if not transparent)
        bg_color = None
        if not TRANSPARENT_CANVAS:
            # Try to sample background color from center of canvas
            # For now, we'll pass None and let the function use default
            # User can override by checking canvas background manually
            pass
        draw_laugh_energy_lines(ctx, cx, cy, half_width, half_height, all_circles, background_color=bg_color)
    
    # Draw only the parts of rectangle border that are NOT covered by circles
    if show_full_ovals:
        # Only show remaining rectangle border in full mode; in minimal mode the rectangle border is defined by arcs only
        draw_uncrossed_rectangle_border(ctx, all_circles, cx, cy, half_width, half_height)
    
    # If minimal mode and gap fill requested, paint only the gaps first
    if not show_full_ovals and FILL_GAPS_ONLY:
        fill_rectangle_gaps_only(ctx, all_circles, cx, cy, half_width, half_height)

    # Find and emphasize only the part of circle borders that are INSIDE the rectangle
    if EMPHASIZE_INTERIOR_ARCS:
        emphasize_border_crossing_pixels(ctx, all_circles, cx, cy, half_width, half_height)
    
    # Add text
    if DRAW_TEXT and text and not return_circles:
        draw_overlap_text(ctx, cx, cy, text)
    
    # Corner ellipses removed for cleaner look
    if return_circles:
        return all_circles

def generate_side_circles(cx, cy, half_width, half_height, style):
    """Generate circles/ovals for each side of the rectangle with automatic oval count"""
    
    all_circles = []
    
    # Define the four sides using width and height
    sides = [
        ("top", cx - half_width, cy - half_height, cx + half_width, cy - half_height),
        ("right", cx + half_width, cy - half_height, cx + half_width, cy + half_height),
        ("bottom", cx + half_width, cy + half_height, cx - half_width, cy + half_height),
        ("left", cx - half_width, cy + half_height, cx - half_width, cy - half_height)
    ]
    
    circle_id = 0
    for side_name, start_x, start_y, end_x, end_y in sides:
        # Calculate side length
        side_length = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        
        # Determine number of circles based on side length
        # Short sides get 1 oval, long sides get 2 ovals
        if side_name in ["top", "bottom"]:
            # Horizontal sides - use width
            num_circles_for_side = 2 if half_width * 2 > half_height * 2 else 1
        else:
            # Vertical sides - use height
            num_circles_for_side = 2 if half_height * 2 > half_width * 2 else 1
        
        # For very small rectangles, always use 1 oval per side
        if side_length < 80:
            num_circles_for_side = 1
            
        side_circles = generate_circles_for_side(
            start_x, start_y, end_x, end_y, side_name, style,
            num_circles_for_side, half_width, half_height, circle_id
        )
        all_circles.extend(side_circles)
        circle_id += len(side_circles)
    
    return all_circles

def enforce_corner_overlaps(all_circles, cx, cy, half_width, half_height):
    """Post-process circles so each rectangle corner has an overlap between its adjacent side ovals.
    This addresses cases where (for example) the single right-side oval failed to cross the bottom-right horizontal oval.

    Strategy (approximate, lightweight):
    1. Group circles by side.
    2. For each corner, pick the circle on each side closest to that corner.
    3. Check an axis-aligned overlap approximation: we require both |dx| <= rx1+rx2 - eps and |dy| <= ry1+ry2 - eps.
       (True ellipse intersection is more complex; this heuristic suffices for guaranteeing visible crossing arcs.)
    4. If missing along an axis, enlarge the *smaller* radius on that axis just enough (with a tiny margin) to create overlap.
       We keep adjustments minimal to preserve sharp interior gaps.
    5. Perform a single pass; cumulative adjustments on a single short-side oval allow it to meet both top & bottom if needed.
    """

    # Group by side
    by_side = { 'top': [], 'right': [], 'bottom': [], 'left': [] }
    for c in all_circles:
        if c['side'] in by_side:
            by_side[c['side']].append(c)

    if not all(by_side.values()):
        # If any side missing (shouldn't happen), bail out
        return

    # Helpers to select corner candidates
    def closest_top_left():
        top = min(by_side['top'], key=lambda c: c['x']) if by_side['top'] else None
        left = min(by_side['left'], key=lambda c: c['y']) if by_side['left'] else None  # smaller y is toward top
        return top, left
    def closest_top_right():
        top = max(by_side['top'], key=lambda c: c['x']) if by_side['top'] else None
        right = min(by_side['right'], key=lambda c: c['y']) if by_side['right'] else None
        return top, right
    def closest_bottom_right():
        bottom = max(by_side['bottom'], key=lambda c: c['x']) if by_side['bottom'] else None
        right = max(by_side['right'], key=lambda c: c['y']) if by_side['right'] else None  # larger y is toward bottom
        return bottom, right
    def closest_bottom_left():
        bottom = min(by_side['bottom'], key=lambda c: c['x']) if by_side['bottom'] else None
        left = max(by_side['left'], key=lambda c: c['y']) if by_side['left'] else None
        return bottom, left

    corners = [closest_top_left(), closest_top_right(), closest_bottom_right(), closest_bottom_left()]

    MARGIN = 2.0  # pixels of guaranteed overlap margin per axis

    for a, b in corners:
        if not a or not b:
            continue
        # Axis deltas
        dx = abs(a['x'] - b['x'])
        dy = abs(a['y'] - b['y'])
        sum_rx = a['rx'] + b['rx']
        sum_ry = a['ry'] + b['ry']

        # If no horizontal overlap, enlarge the smaller rx just enough
        if dx > sum_rx - MARGIN:
            needed = dx + MARGIN - sum_rx
            if a['rx'] < b['rx']:
                a['rx'] += needed
            else:
                b['rx'] += needed

        # Recompute after potential rx change
        dx = abs(a['x'] - b['x'])
        sum_rx = a['rx'] + b['rx']

        # If no vertical overlap, enlarge the smaller ry
        if dy > sum_ry - MARGIN:
            needed = dy + MARGIN - sum_ry
            if a['ry'] < b['ry']:
                a['ry'] += needed
            else:
                b['ry'] += needed

        # Optional: very small inward center nudges toward corner to emphasize intersection region inside rectangle
        # (Keep minimal to avoid altering interior negative space.)
        # We only nudge if overlap was adjusted.
        # Determine corner direction by relative positions to rectangle center.
        # For simplicity we skip additional logic; radii enlargement suffices.


def generate_circles_for_side(start_x, start_y, end_x, end_y, side_name, style,
                              num_circles, half_width, half_height, start_id):
    """Generate ovals for one side with these RULES:
    1. Each oval only PARTLY covers the rectangle (small inward penetration).
    2. It must cross its SAME-SIDE neighbor (when there are 2) to create organic chain.
    3. It must cross ONLY adjacent perpendicular side ovals at the corners.
       (Left crosses Top+Bottom; should NOT reach Right; Top crosses Left+Right but not Bottom centrally, etc.)
    4. Opposite side ovals MUST NOT intersect across the free center.
    The parameters are tuned to keep a clear interior for text while preserving corner & chain overlaps.
    """
    
    circles = []
    side_length = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)

    is_horizontal = side_name in ["top", "bottom"]
    long_side = (half_width > half_height and is_horizontal) or (half_height > half_width and not is_horizontal)
    
    # Mild randomness helpers
    def r(a, b):
        return random.uniform(a, b)
    
    # Laughter style tweak: increase count & add random micro-bulges
    if style == "laugh":
        # If rectangle is long on this side, allow 3 bulges, else 2, else keep 1 for very short
        long_threshold = 140  # pixels overall side length
        side_len_pixels = (half_width * 2) if is_horizontal else (half_height * 2)
        if side_len_pixels > long_threshold:
            num_circles = max(num_circles, 3)
        else:
            num_circles = max(num_circles, 2)

    for i in range(num_circles):
        # Parameter t along side: single -> center, double -> near corners
        if num_circles == 1:
            # Center with small random drift to vary interior negative space
            t = 0.5 + r(-0.08, 0.08)
        else:
            if style == "laugh" and num_circles >= 3:
                # Distribute 3 with stronger jitter, center one purposely slightly off-center
                if i == 0:
                    base_t = 0.16
                elif i == 1:
                    base_t = 0.50 + r(-0.06, 0.06)
                else:
                    base_t = 0.84
                t = base_t + r(-0.06, 0.065)
                t = _clamp(t, 0.06, 0.94)
            elif style == "laugh" and num_circles == 2:
                base_t = 0.22 if i == 0 else 0.78
                t = base_t + r(-0.06, 0.06)
                t = _clamp(t, 0.07, 0.93)
            else:
                # Corner-biased with variation to change overlap shape
                base_t = 0.18 if i == 0 else 0.82
                t = base_t + r(-0.05, 0.05)
                t = _clamp(t, 0.08, 0.92)

        # Base coordinate on the side line
        side_x = start_x + t * (end_x - start_x)
        side_y = start_y + t * (end_y - start_y)

        # Outward normals
        if side_name == "top":
            normal_x, normal_y = 0, -1
        elif side_name == "bottom":
            normal_x, normal_y = 0, 1
        elif side_name == "left":
            normal_x, normal_y = -1, 0
        else:  # right
            normal_x, normal_y = 1, 0

        # Base radii strategy:
        # Horizontal sides: rx wider for corner overlap, ry shallow to avoid meeting opposite side.
        # Vertical sides: ry taller for corner overlap, rx narrow to avoid meeting opposite side.
        corner_bias = (num_circles >= 2 and (t < 0.3 or t > 0.7))
        if is_horizontal:
            base_span = 0.74 if num_circles == 1 else 0.46 + r(-0.025, 0.03)
            if corner_bias:
                base_span *= 0.9  # shrink corner ovals to sharpen inner corner gap
            rx = (half_width * base_span) * r(0.94, 1.05)
            ry_base = 0.28 + r(-0.025, 0.035)
            if corner_bias:
                ry_base *= 0.9
            ry = (half_height * ry_base) * r(0.92, 1.08)
        else:
            base_span = 0.74 if num_circles == 1 else 0.46 + r(-0.025, 0.03)
            if corner_bias:
                base_span *= 0.9
            ry = (half_height * base_span) * r(0.94, 1.05)
            rx_base = 0.28 + r(-0.025, 0.035)
            if corner_bias:
                rx_base *= 0.9
            rx = (half_width * rx_base) * r(0.92, 1.08)

        # Laugh style: favor smaller, punchier bumps (reduce radii, then add random micro-swell)
        if style == "laugh":
            scale_down = 0.78 if num_circles >= 3 else 0.85
            rx *= scale_down * r(0.95, 1.08)
            ry *= scale_down * r(0.95, 1.08)
            # Slight random elliptical exaggeration for energy
            if random.random() < 0.4:
                if is_horizontal:
                    ry *= r(1.05, 1.18)
                else:
                    rx *= r(1.05, 1.18)

        # Ensure same-side overlap (two ovals): enlarge along-edge radius if needed
        if num_circles >= 2:
            side_full_length = (half_width * 2) if is_horizontal else (half_height * 2)
            center_sep = (0.8 - 0.2) * side_full_length  # distance between centers
            min_overlap_pixels = (HORIZONTAL_MIN_OVERLAP_FRAC if is_horizontal else VERTICAL_MIN_OVERLAP_FRAC) * side_full_length
            # For two equal radii along axis R: overlap_length = 2R - center_sep
            along_radius = rx if is_horizontal else ry
            current_overlap = 2 * along_radius - center_sep
            if current_overlap < min_overlap_pixels:
                # Need new along_radius so that 2R_new - center_sep = min_overlap_pixels => R_new = (center_sep + min_overlap_pixels)/2
                required_radius = (center_sep + min_overlap_pixels) / 2.0
                scale = required_radius / along_radius
                if is_horizontal:
                    rx *= scale
                else:
                    ry *= scale

        # Corner growth for corner ovals (slight) to guarantee perpendicular crossing
        if num_circles >= 2 and (t < 0.25 or t > 0.75):
            # Slight growth removed for corner sharpness; keep minimal organic jitter
            jitter_scale = 1 + r(-0.01, 0.015)
            if is_horizontal:
                rx *= jitter_scale
            else:
                ry *= jitter_scale

        # Inward penetration: tuned per orientation (horizontal needs shallower to keep interior open)
        if is_horizontal:
            inward_penetration = (ry) * (0.38 + r(-0.035, 0.04))
            if corner_bias:
                inward_penetration *= 0.85
        else:
            inward_penetration = (rx) * (0.48 + r(-0.04, 0.05))
            if corner_bias:
                inward_penetration *= 0.85

        if style == "laugh":
            # Pull laughs slightly further outwards to keep interior loud/airy
            outward_relief = 0.9  # reduce penetration depth
            circle_penetration_adjust = outward_relief
            inward_penetration *= circle_penetration_adjust
        circle_x = side_x - normal_x * inward_penetration
        circle_y = side_y - normal_y * inward_penetration

        # Random gentle jitter limited so we keep constraints
        jitter_amt = 3.0
        circle_x += r(-jitter_amt, jitter_amt)
        circle_y += r(-jitter_amt, jitter_amt)

        circles.append({
            'x': circle_x,
            'y': circle_y,
            'rx': rx,
            'ry': ry,
            'side': side_name,
            'id': start_id + i
        })
    
    return circles

def draw_laugh_energy_lines(ctx, cx, cy, half_width, half_height, circles, background_color=None):
    """Add radiating short energy ticks around exterior to suggest explosive laughter.
    Drawn very lightly so they don't dominate the ink arcs.
    
    Args:
        background_color: Optional tuple (r, g, b, a) or (r, g, b) for background color.
                         If None or light, uses black lines. If dark, uses white/yellow lines.
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
    # Radius just outside bounding box of circles
    outer_rx = half_width + 24
    outer_ry = half_height + 24
    for i in range(num_rays):
        ang = (2*math.pi) * (i / num_rays) + random.uniform(-0.05,0.05)
        # Skip some rays randomly for irregularity
        if random.random() < 0.18:
            continue
        base_len = random.uniform(10, 24)
        # Start slightly outside rectangle ellipse
        sx = cx + math.cos(ang) * (outer_rx + random.uniform(-4,4))
        sy = cy + math.sin(ang) * (outer_ry + random.uniform(-4,4))
        ex = sx + math.cos(ang) * base_len
        ey = sy + math.sin(ang) * base_len
        ctx.move_to(sx, sy)
        ctx.line_to(ex, ey)
    ctx.stroke()
    ctx.restore()

def draw_overlapping_circles(ctx, circles, cx, cy, base_width, base_height):
    """Draw all circles with overlapping effect"""
    
    # Sort circles by distance from center (draw farthest first)
    circles_with_distance = []
    for circle in circles:
        distance = math.sqrt((circle['x'] - cx)**2 + (circle['y'] - cy)**2)
        circles_with_distance.append((distance, circle))
    
    circles_with_distance.sort(key=lambda x: x[0], reverse=True)
    
    # Draw circles from farthest to nearest for proper overlapping
    for distance, circle in circles_with_distance:
        draw_single_circle(ctx, circle, cx, cy, base_width, base_height)

def draw_single_circle(ctx, circle, cx, cy, base_width, base_height):
    """Draw a single circle/oval with gradient (no rotation)."""
    ctx.save()
    ctx.translate(circle['x'], circle['y'])
    ctx.scale(circle['rx'], circle['ry'])
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    
    # Create gradient for this circle
    gradient = cairo.RadialGradient(
        circle['x'], circle['y'], 0,
        circle['x'], circle['y'], max(circle['rx'], circle['ry'])
    )
    
    # Different colors based on position/side
    if circle['side'] == 'top':
        gradient.add_color_stop_rgb(0, 1.0, 0.95, 0.9)   # Light cream
        gradient.add_color_stop_rgb(1, 0.9, 0.85, 0.75)  # Cream edge
    elif circle['side'] == 'right':
        gradient.add_color_stop_rgb(0, 0.95, 1.0, 0.9)   # Light green
        gradient.add_color_stop_rgb(1, 0.85, 0.9, 0.75)  # Green edge
    elif circle['side'] == 'bottom':
        gradient.add_color_stop_rgb(0, 0.9, 0.95, 1.0)   # Light blue
        gradient.add_color_stop_rgb(1, 0.75, 0.85, 0.9)  # Blue edge
    else:  # left
        gradient.add_color_stop_rgb(0, 1.0, 0.9, 0.95)   # Light pink
        gradient.add_color_stop_rgb(1, 0.9, 0.75, 0.85)  # Pink edge
    
    # Fill circle
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Enhanced circle outline - thicker and darker for contact emphasis
    ctx.set_source_rgba(0, 0, 0, 0.6)
    ctx.set_line_width(2.0)
    ctx.stroke()

def draw_base_square(ctx, cx, cy, size):
    """Draw the base square (will be partially covered by circles)"""
    
    half_size = size / 2
    
    # Square path
    ctx.rectangle(cx - half_size, cy - half_size, size, size)
    
    # Square gradient
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, size * 0.7)
    gradient.add_color_stop_rgb(0, 1.0, 1.0, 1.0)      # White center
    gradient.add_color_stop_rgb(0.7, 0.95, 0.95, 0.98) # Light gray
    gradient.add_color_stop_rgb(1, 0.85, 0.85, 0.9)    # Gray edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Enhanced square outline - thicker and darker to emphasize contact with circles
    ctx.set_source_rgba(0, 0, 0, 0.7)
    ctx.set_line_width(2.5)
    ctx.stroke()

def draw_base_rectangle(ctx, cx, cy, width, height, stroke=True, fill=True):
    """Draw the base rectangle (optionally only fill) respecting minimal mode flags."""
    
    half_width = width / 2
    half_height = height / 2
    
    # Rectangle path
    ctx.rectangle(cx - half_width, cy - half_height, width, height)
    
    if fill:
        # Solid white (can be changed) - avoids gradients which look too rendered for manga style
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.fill_preserve()
    else:
        # No fill, keep hollow
        ctx.new_path()
    
    if stroke:
        ctx.set_source_rgba(*INK_COLOR)
        ctx.set_line_width(2.5)
        ctx.stroke()
    else:
        ctx.new_path()

## Circle-base drawing moved to overlapping_circles_circle.py

def fill_rectangle_gaps_only(ctx, all_circles, cx, cy, half_width, half_height):
    """Restore original behavior: fill entire rectangle white then CLEAR each oval interior,
    leaving all gap regions (possibly multiple)."""
    ctx.save()
    # Paint full rectangle white
    ctx.set_source_rgba(1,1,1,1)
    ctx.rectangle(cx - half_width, cy - half_height, half_width*2, half_height*2)
    ctx.fill()

    # Punch out ovals
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    for circle in all_circles:
        ctx.save()
        ctx.translate(circle['x'], circle['y'])
        ctx.scale(circle['rx'], circle['ry'])
        ctx.arc(0, 0, 1, 0, 2*math.pi)
        ctx.restore()
        ctx.fill()

    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.restore()

def find_circle_intersections_outside_rect(all_circles, rect_left, rect_right, rect_top, rect_bottom):
    """Find intersection points between circles that are OUTSIDE the rectangle"""
    intersections = []
    
    for i in range(len(all_circles)):
        for j in range(i + 1, len(all_circles)):
            circle1 = all_circles[i]
            circle2 = all_circles[j]
            
            cx1, cy1 = circle1['x'], circle1['y']
            rx1, ry1 = circle1['rx'], circle1['ry']
            cx2, cy2 = circle2['x'], circle2['y']
            rx2, ry2 = circle2['rx'], circle2['ry']
            
            # Find approximate intersection points by sampling
            for angle in range(0, 360, 10):  # Check every 10 degrees
                rad = math.radians(angle)
                
                # Point on first circle
                x1 = cx1 + rx1 * math.cos(rad)
                y1 = cy1 + ry1 * math.sin(rad)
                
                # Check if this point is also inside the second circle AND outside rectangle
                if point_inside_circle(x1, y1, circle2):
                    # Only add if intersection is OUTSIDE the rectangle
                    if not (x1 >= rect_left and x1 <= rect_right and y1 >= rect_top and y1 <= rect_bottom):
                        intersections.append((x1, y1))
                
                # Point on second circle
                x2 = cx2 + rx2 * math.cos(rad)
                y2 = cy2 + ry2 * math.sin(rad)
                
                # Check if this point is also inside the first circle AND outside rectangle
                if point_inside_circle(x2, y2, circle1):
                    # Only add if intersection is OUTSIDE the rectangle
                    if not (x2 >= rect_left and x2 <= rect_right and y2 >= rect_top and y2 <= rect_bottom):
                        intersections.append((x2, y2))
    
    # Remove duplicates by rounding to nearest pixel
    unique_intersections = []
    for ix, iy in intersections:
        rounded = (round(ix), round(iy))
        is_duplicate = False
        for ux, uy in unique_intersections:
            if abs(rounded[0] - round(ux)) <= 2 and abs(rounded[1] - round(uy)) <= 2:
                is_duplicate = True
                break
        if not is_duplicate:
            unique_intersections.append((ix, iy))
    
    return unique_intersections

def draw_outside_intersection_connections(ctx, all_circles, cx, cy, half_width, half_height):
    """No additional connection lines - keep it clean"""
    # Function exists but does nothing - no additional visual elements
    pass

def emphasize_border_crossing_pixels(ctx, all_circles, cx, cy, half_width, half_height):
    """Emphasize only the part of circle borders that are INSIDE the rectangle"""
    
    # Rectangle boundaries
    rect_left = cx - half_width
    rect_right = cx + half_width
    rect_top = cy - half_height
    rect_bottom = cy + half_height
    
    # For each circle, find and emphasize only the border segments that are inside
    for circle in all_circles:
        inside_segments = find_crossing_border_segments(circle, rect_left, rect_right, rect_top, rect_bottom, all_circles)
        
        # Draw emphasis only on the inside border segments that don't overlap other circles
        draw_crossing_border_emphasis_simple(ctx, inside_segments)

def draw_crossing_border_emphasis_simple(ctx, inside_segments):
    """Draw simple emphasis on border segments that are INSIDE the square - no underlines"""
    
    if not inside_segments:
        return
    
    ctx.set_source_rgba(0, 0, 0, 0.9)  # Strong black emphasis
    ctx.set_line_width(4.0)  # Thick line for visibility
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    
    for segment in inside_segments:
        if len(segment) < 2:
            continue
        
        # Draw the segment as a smooth curve - single emphasis only
        ctx.move_to(segment[0]['x'], segment[0]['y'])
        
        for point in segment[1:]:
            ctx.line_to(point['x'], point['y'])
        
        ctx.stroke()

def find_crossing_border_segments(circle, rect_left, rect_right, rect_top, rect_bottom, all_circles):
    """Find segments of circle border that are INSIDE the rectangle boundary and NOT covered by other circles"""
    
    crossing_segments = []
    
    # Get circle parameters
    cx, cy = circle['x'], circle['y']
    rx, ry = circle['rx'], circle['ry']
    
    # Sample points around the circle perimeter with high resolution
    num_samples = int(max(rx, ry) * 10)  # High resolution for smooth segments
    border_points = []
    
    for i in range(num_samples):
        angle = (2 * math.pi * i) / num_samples
        px = cx + rx * math.cos(angle)
        py = cy + ry * math.sin(angle)
        
        # Check if this point is INSIDE the rectangle
        is_inside = (px >= rect_left and px <= rect_right and 
                    py >= rect_top and py <= rect_bottom)
        
        # Check if this point is covered by any OTHER circle
        is_covered_by_other = False
        if is_inside:  # Only check coverage if point is inside square
            for other_circle in all_circles:
                if other_circle != circle:  # Don't check against itself
                    if point_inside_circle(px, py, other_circle):
                        is_covered_by_other = True
                        break
        
        # Point should be emphasized only if it's inside square AND not covered by other circles
        should_emphasize = is_inside and not is_covered_by_other
        
        border_points.append({
            'x': px,
            'y': py,
            'angle': angle,
            'should_emphasize': should_emphasize
        })
    
    # Find continuous segments of border points that should be emphasized
    current_segment = []
    
    for point in border_points:
        if point['should_emphasize']:
            current_segment.append(point)
        else:
            # End of emphasizable segment
            if len(current_segment) > 2:  # Only keep segments with multiple points
                crossing_segments.append(current_segment)
            current_segment = []
    
    # Handle wrap-around case (segment continues from end to beginning)
    if current_segment and crossing_segments and crossing_segments[0]:
        # Check if first segment and last segment should be connected
        first_segment = crossing_segments[0]
        if (abs(current_segment[-1]['angle'] - (first_segment[0]['angle'] + 2*math.pi)) < 0.2 or
            abs(current_segment[-1]['angle'] - first_segment[0]['angle']) < 0.2):
            # Connect the segments
            crossing_segments[0] = current_segment + first_segment
        else:
            if len(current_segment) > 2:
                crossing_segments.append(current_segment)
    elif len(current_segment) > 2:
        crossing_segments.append(current_segment)
    
    return crossing_segments

## Circle emphasis helper moved to overlapping_circles_circle.py

def draw_crossing_border_emphasis(ctx, inside_segments):
    """Draw emphasis on border segments that are INSIDE the square with underlines"""
    
    if not inside_segments:
        return

    for segment in inside_segments:
        if len(segment) < 2:
            continue
        
        # Draw main oval border emphasis
        ctx.set_source_rgba(0, 0, 0, 0.9)  # Strong black emphasis
        ctx.set_line_width(4.0)  # Thick line for visibility
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        
        # Draw the main segment as a smooth curve
        ctx.move_to(segment[0]['x'], segment[0]['y'])
        for point in segment[1:]:
            ctx.line_to(point['x'], point['y'])
        ctx.stroke()
        
        # Draw underline effect for the oval border
        if len(segment) >= 2:
            ctx.set_source_rgba(0, 0, 0, 0.6)  # Slightly lighter for underline
            ctx.set_line_width(2.0)  # Thinner underline
            
            # Create underline by drawing a parallel line with slight offset
            underline_points = []
            for i, point in enumerate(segment):
                # Calculate offset direction (perpendicular to the curve)
                if i == 0 and len(segment) > 1:
                    # First point: use direction to next point
                    dx = segment[1]['x'] - point['x']
                    dy = segment[1]['y'] - point['y']
                elif i == len(segment) - 1:
                    # Last point: use direction from previous point
                    dx = point['x'] - segment[i-1]['x']
                    dy = point['y'] - segment[i-1]['y']
                else:
                    # Middle points: use average direction
                    dx = segment[i+1]['x'] - segment[i-1]['x']
                    dy = segment[i+1]['y'] - segment[i-1]['y']
                
                # Calculate perpendicular offset (rotate 90 degrees)
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    offset = 3  # Underline offset distance
                    perp_x = -dy / length * offset
                    perp_y = dx / length * offset
                    
                    underline_points.append({
                        'x': point['x'] + perp_x,
                        'y': point['y'] + perp_y
                    })
            
            # Draw the underline
            if len(underline_points) >= 2:
                ctx.move_to(underline_points[0]['x'], underline_points[0]['y'])
                for upoint in underline_points[1:]:
                    ctx.line_to(upoint['x'], upoint['y'])
                ctx.stroke()

def find_border_crossing_pixels(circle, square_left, square_right, square_top, square_bottom):
    """Find all pixels of a circle that cross the square border"""
    
    crossing_pixels = []
    
    # Get circle parameters
    cx, cy = circle['x'], circle['y']
    rx, ry = circle['rx'], circle['ry']
    
    # Sample points around the circle perimeter with high resolution
    num_samples = int(max(rx, ry) * 6)  # High resolution sampling
    
    for i in range(num_samples):
        angle = (2 * math.pi * i) / num_samples
        px = cx + rx * math.cos(angle)
        py = cy + ry * math.sin(angle)
        
        # Check if this pixel is ON or very close to a square border
        is_crossing = False
        border_type = None
        
        # Check left border crossing
        if (abs(px - square_left) < 1.5 and 
            square_top <= py <= square_bottom):
            is_crossing = True
            border_type = "left"
        
        # Check right border crossing  
        elif (abs(px - square_right) < 1.5 and 
              square_top <= py <= square_bottom):
            is_crossing = True
            border_type = "right"
        
        # Check top border crossing
        elif (abs(py - square_top) < 1.5 and 
              square_left <= px <= square_right):
            is_crossing = True
            border_type = "top"
        
        # Check bottom border crossing
        elif (abs(py - square_bottom) < 1.5 and 
              square_left <= px <= square_right):
            is_crossing = True
            border_type = "bottom"
        
        if is_crossing:
            crossing_pixels.append({
                'x': px,
                'y': py,
                'border': border_type,
                'circle_id': circle.get('id', 0)
            })
    
    return crossing_pixels

def draw_crossing_pixel_emphasis(ctx, crossing_pixels):
    """Draw emphasis on specific crossing pixels"""
    
    if not crossing_pixels:
        return
    
    # Group consecutive crossing pixels for smooth lines
    pixel_groups = group_consecutive_pixels(crossing_pixels)
    
    for group in pixel_groups:
        if len(group) < 2:
            # Single pixel - draw as small circle
            pixel = group[0]
            ctx.arc(pixel['x'], pixel['y'], 1.5, 0, 2 * math.pi)
            ctx.set_source_rgba(0, 0, 0, 0.9)
            ctx.fill()
        else:
            # Multiple consecutive pixels - draw as thick line
            ctx.set_source_rgba(0, 0, 0, 0.9)
            ctx.set_line_width(3.0)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            
            # Start path at first pixel
            ctx.move_to(group[0]['x'], group[0]['y'])
            
            # Draw through all pixels in group
            for pixel in group[1:]:
                ctx.line_to(pixel['x'], pixel['y'])
            
            ctx.stroke()

def group_consecutive_pixels(crossing_pixels):
    """Group consecutive crossing pixels that are close together"""
    
    if not crossing_pixels:
        return []
    
    # Sort pixels by border and position
    crossing_pixels.sort(key=lambda p: (p['border'], p['x'] + p['y']))
    
    groups = []
    current_group = [crossing_pixels[0]]
    
    for i in range(1, len(crossing_pixels)):
        prev_pixel = crossing_pixels[i-1]
        curr_pixel = crossing_pixels[i]
        
        # Check if pixels are consecutive (same border and close distance)
        distance = math.sqrt((curr_pixel['x'] - prev_pixel['x'])**2 + 
                           (curr_pixel['y'] - prev_pixel['y'])**2)
        
        if (curr_pixel['border'] == prev_pixel['border'] and 
            distance < 3.0):  # Pixels are close and on same border
            current_group.append(curr_pixel)
        else:
            # Start new group
            groups.append(current_group)
            current_group = [curr_pixel]
    
    # Add the last group
    groups.append(current_group)
    
    return groups

def draw_unified_contour(ctx, all_circles, cx, cy, half_size):
    """Draw the unified contour outline of the combined square+circles shape"""
    
    # Create a path that traces the outer contour of the combined shape
    ctx.set_source_rgba(0, 0, 0, 0.9)  # Strong black outline
    ctx.set_line_width(3.0)  # Thick contour line
    
    # Square boundaries
    square_left = cx - half_size
    square_right = cx + half_size
    square_top = cy - half_size
    square_bottom = cy + half_size
    
    # Trace the contour by following the outermost boundary
    # Start from top-left corner of square
    ctx.move_to(square_left, square_top)
    
    # Trace top edge, deviating around circles that extend beyond
    trace_edge_with_circles(ctx, "top", square_left, square_top, square_right, square_top, all_circles)
    
    # Trace right edge
    trace_edge_with_circles(ctx, "right", square_right, square_top, square_right, square_bottom, all_circles)
    
    # Trace bottom edge
    trace_edge_with_circles(ctx, "bottom", square_right, square_bottom, square_left, square_bottom, all_circles)
    
    # Trace left edge
    trace_edge_with_circles(ctx, "left", square_left, square_bottom, square_left, square_top, all_circles)
    
    # Close the path and stroke
    ctx.close_path()
    ctx.stroke()

def trace_edge_with_circles(ctx, edge_name, start_x, start_y, end_x, end_y, circles):
    """Trace an edge of the square, following circle contours where they extend beyond"""
    
    # Collect circles that affect this edge
    affecting_circles = []
    
    for circle in circles:
        if edge_affects_circle(edge_name, start_x, start_y, end_x, end_y, circle):
            affecting_circles.append(circle)
    
    if not affecting_circles:
        # No circles affect this edge, draw straight line
        ctx.line_to(end_x, end_y)
        return
    
    # Sort circles by position along the edge
    affecting_circles.sort(key=lambda c: get_circle_position_on_edge(edge_name, c))
    
    current_x, current_y = start_x, start_y
    
    for circle in affecting_circles:
        # Draw to the start of the circle's influence
        circle_start_x, circle_start_y = get_circle_influence_start(edge_name, circle, start_x, start_y, end_x, end_y)
        
        if distance(current_x, current_y, circle_start_x, circle_start_y) > 2:
            ctx.line_to(circle_start_x, circle_start_y)
        
        # Draw the circle's contour that extends beyond the square
        draw_circle_contour_extension(ctx, edge_name, circle)
        
        # Update current position
        current_x, current_y = get_circle_influence_end(edge_name, circle, start_x, start_y, end_x, end_y)
    
    # Draw the remaining straight line to the end
    if distance(current_x, current_y, end_x, end_y) > 2:
        ctx.line_to(end_x, end_y)

def edge_affects_circle(edge_name, start_x, start_y, end_x, end_y, circle):
    """Check if a circle extends beyond this edge of the square"""
    
    if edge_name == "top":
        return (circle['y'] - circle['ry'] < start_y and 
                circle['x'] - circle['rx'] < end_x and 
                circle['x'] + circle['rx'] > start_x)
    elif edge_name == "right":
        return (circle['x'] + circle['rx'] > start_x and 
                circle['y'] - circle['ry'] < end_y and 
                circle['y'] + circle['ry'] > start_y)
    elif edge_name == "bottom":
        return (circle['y'] + circle['ry'] > start_y and 
                circle['x'] - circle['rx'] < start_x and 
                circle['x'] + circle['rx'] > end_x)
    elif edge_name == "left":
        return (circle['x'] - circle['rx'] < start_x and 
                circle['y'] - circle['ry'] < start_y and 
                circle['y'] + circle['ry'] > end_y)
    return False

def get_circle_position_on_edge(edge_name, circle):
    """Get the position of a circle along an edge for sorting"""
    if edge_name in ["top", "bottom"]:
        return circle['x']
    else:  # left or right
        return circle['y']

def get_circle_influence_start(edge_name, circle, start_x, start_y, end_x, end_y):
    """Get where the circle's influence starts on an edge"""
    if edge_name == "top":
        return (max(start_x, circle['x'] - circle['rx']), start_y)
    elif edge_name == "right":
        return (start_x, max(start_y, circle['y'] - circle['ry']))
    elif edge_name == "bottom":
        return (min(start_x, circle['x'] + circle['rx']), start_y)
    elif edge_name == "left":
        return (start_x, min(start_y, circle['y'] + circle['ry']))

def get_circle_influence_end(edge_name, circle, start_x, start_y, end_x, end_y):
    """Get where the circle's influence ends on an edge"""
    if edge_name == "top":
        return (min(end_x, circle['x'] + circle['rx']), start_y)
    elif edge_name == "right":
        return (start_x, min(end_y, circle['y'] + circle['ry']))
    elif edge_name == "bottom":
        return (max(end_x, circle['x'] - circle['rx']), start_y)
    elif edge_name == "left":
        return (start_x, max(end_y, circle['y'] - circle['ry']))

def draw_circle_contour_extension(ctx, edge_name, circle):
    """Draw the part of the circle that extends beyond the square edge"""
    
    # Calculate the arc of the circle that extends beyond the square
    cx, cy = circle['x'], circle['y']
    rx, ry = circle['rx'], circle['ry']
    
    # Create several points along the circle's contour that extends beyond
    num_points = 10
    if edge_name == "top":
        # Arc from left intersection to right intersection, going above the square
        start_angle = math.pi * 0.75  # Upper left
        end_angle = math.pi * 0.25    # Upper right
    elif edge_name == "right":
        # Arc going to the right of the square
        start_angle = math.pi * 1.75  # Lower right
        end_angle = math.pi * 0.25    # Upper right
    elif edge_name == "bottom":
        # Arc going below the square
        start_angle = math.pi * 1.25  # Lower left
        end_angle = math.pi * 1.75    # Lower right
    elif edge_name == "left":
        # Arc going to the left of the square
        start_angle = math.pi * 0.75  # Upper left
        end_angle = math.pi * 1.25    # Lower left
    
    # Draw smooth arc
    for i in range(num_points + 1):
        t = i / num_points
        angle = start_angle + (end_angle - start_angle) * t
        
        # Calculate point on ellipse
        px = cx + rx * math.cos(angle)
        py = cy + ry * math.sin(angle)
        
        ctx.line_to(px, py)

def distance(x1, y1, x2, y2):
    """Calculate distance between two points"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def draw_contact_emphasis(ctx, all_circles, cx, cy, half_size):
    """Draw emphasis lines where circles make contact with square edges"""
    
    # Square boundaries
    square_left = cx - half_size
    square_right = cx + half_size
    square_top = cy - half_size
    square_bottom = cy + half_size
    
    for circle in all_circles:
        # Check if circle intersects with square edges
        circle_left = circle['x'] - circle['rx']
        circle_right = circle['x'] + circle['rx']
        circle_top = circle['y'] - circle['ry']
        circle_bottom = circle['y'] + circle['ry']
        
        # Draw contact emphasis for each edge that intersects
        ctx.set_source_rgba(0, 0, 0, 0.8)  # Dark emphasis line
        ctx.set_line_width(3.0)
        
        # Left edge contact
        if (circle_left <= square_left <= circle_right and 
            circle_top <= cy <= circle_bottom):
            contact_start_y = max(circle_top, square_top)
            contact_end_y = min(circle_bottom, square_bottom)
            if contact_end_y > contact_start_y:
                ctx.move_to(square_left, contact_start_y)
                ctx.line_to(square_left, contact_end_y)
                ctx.stroke()
        
        # Right edge contact
        if (circle_left <= square_right <= circle_right and 
            circle_top <= cy <= circle_bottom):
            contact_start_y = max(circle_top, square_top)
            contact_end_y = min(circle_bottom, square_bottom)
            if contact_end_y > contact_start_y:
                ctx.move_to(square_right, contact_start_y)
                ctx.line_to(square_right, contact_end_y)
                ctx.stroke()
        
        # Top edge contact
        if (circle_top <= square_top <= circle_bottom and 
            circle_left <= cx <= circle_right):
            contact_start_x = max(circle_left, square_left)
            contact_end_x = min(circle_right, square_right)
            if contact_end_x > contact_start_x:
                ctx.move_to(contact_start_x, square_top)
                ctx.line_to(contact_end_x, square_top)
                ctx.stroke()
        
        # Bottom edge contact
        if (circle_top <= square_bottom <= circle_bottom and 
            circle_left <= cx <= circle_right):
            contact_start_x = max(circle_left, square_left)
            contact_end_x = min(circle_right, square_right)
            if contact_end_x > contact_start_x:
                ctx.move_to(contact_start_x, square_bottom)
                ctx.line_to(contact_end_x, square_bottom)
                ctx.stroke()

def draw_uncrossed_rectangle_border(ctx, all_circles, cx, cy, half_width, half_height):
    """Draw rectangle border with underlines where it intersects with ovals"""
    
    # Rectangle boundaries
    rect_left = cx - half_width
    rect_right = cx + half_width
    rect_top = cy - half_height
    rect_bottom = cy + half_height
    
    # Set up border drawing properties
    ctx.set_source_rgba(0, 0, 0, 0.7)
    ctx.set_line_width(2.5)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    
    # For each edge of the rectangle, find segments that are NOT covered by circles
    edges = [
        ("top", rect_left, rect_top, rect_right, rect_top),
        ("right", rect_right, rect_top, rect_right, rect_bottom),
        ("bottom", rect_right, rect_bottom, rect_left, rect_bottom),
        ("left", rect_left, rect_bottom, rect_left, rect_top)
    ]
    
    for edge_name, start_x, start_y, end_x, end_y in edges:
        uncovered_segments = find_uncrossed_edge_segments(
            edge_name, start_x, start_y, end_x, end_y, all_circles, max(half_width, half_height)
        )
        covered_segments = find_covered_edge_segments(
            edge_name, start_x, start_y, end_x, end_y, all_circles, max(half_width, half_height)
        )
        
        # Draw ONLY uncovered segments; fully omit covered ones
        for segment_start, segment_end in uncovered_segments:
            ctx.move_to(segment_start[0], segment_start[1])
            ctx.line_to(segment_end[0], segment_end[1])
            ctx.stroke()

def find_covered_edge_segments(edge_name, start_x, start_y, end_x, end_y, all_circles, half_size):
    """Find segments of rectangle edge that ARE covered by circles"""
    
    # Sample points along the edge
    num_samples = 100
    edge_points = []
    
    for i in range(num_samples + 1):
        t = i / num_samples
        px = start_x + t * (end_x - start_x)
        py = start_y + t * (end_y - start_y)
        
        # Check if this point is covered (inside) any circle
        is_covered = False
        for circle in all_circles:
            if point_inside_circle(px, py, circle):
                is_covered = True
                break
        
        edge_points.append({
            'x': px,
            'y': py,
            'position': t,
            'is_covered': is_covered
        })
    
    # Find continuous segments that ARE covered
    covered_segments = []
    current_segment_start = None
    
    for i, point in enumerate(edge_points):
        if point['is_covered']:  # Point IS covered by a circle
            if current_segment_start is None:
                current_segment_start = point
        else:  # Point is NOT covered by any circle
            if current_segment_start is not None:
                # End the current covered segment
                prev_point = edge_points[i-1] if i > 0 else current_segment_start
                if current_segment_start != prev_point:
                    covered_segments.append([
                        (current_segment_start['x'], current_segment_start['y']),
                        (prev_point['x'], prev_point['y'])
                    ])
                current_segment_start = None
    
    # Handle final segment if it ends covered
    if current_segment_start is not None:
        final_point = edge_points[-1]
        if current_segment_start != final_point:
            covered_segments.append([
                (current_segment_start['x'], current_segment_start['y']),
                (final_point['x'], final_point['y'])
            ])
    
    return covered_segments

def find_uncrossed_edge_segments(edge_name, start_x, start_y, end_x, end_y, all_circles, half_size):
    """Find segments of square edge that are NOT covered by any circles"""
    
    # Sample points along the edge
    num_samples = 100
    edge_points = []
    
    for i in range(num_samples + 1):
        t = i / num_samples
        px = start_x + t * (end_x - start_x)
        py = start_y + t * (end_y - start_y)
        
        # Check if this point is covered (inside) any circle
        is_covered = False
        for circle in all_circles:
            if point_inside_circle(px, py, circle):
                is_covered = True
                break
        
        edge_points.append({
            'x': px,
            'y': py,
            'position': t,
            'is_covered': is_covered
        })
    
    # Find continuous segments that are NOT covered
    uncovered_segments = []
    current_segment_start = None
    
    for i, point in enumerate(edge_points):
        if not point['is_covered']:  # Point is NOT covered by any circle
            if current_segment_start is None:
                current_segment_start = point
        else:  # Point IS covered by a circle
            if current_segment_start is not None:
                # End the current uncovered segment
                prev_point = edge_points[i-1] if i > 0 else current_segment_start
                if current_segment_start != prev_point:
                    uncovered_segments.append([
                        (current_segment_start['x'], current_segment_start['y']),
                        (prev_point['x'], prev_point['y'])
                    ])
                current_segment_start = None
    
    # Handle final segment if it ends uncovered
    if current_segment_start is not None:
        final_point = edge_points[-1]
        if current_segment_start != final_point:
            uncovered_segments.append([
                (current_segment_start['x'], current_segment_start['y']),
                (final_point['x'], final_point['y'])
            ])
    
    return uncovered_segments

## Circle border drawing moved to overlapping_circles_circle.py

## Radial circle helpers removed (not part of rectangle-focused module)

def point_inside_circle(px, py, circle):
    cx, cy = circle['x'], circle['y']
    rx, ry = circle['rx'], circle['ry']
    dx = (px - cx) / rx
    dy = (py - cy) / ry
    return (dx*dx + dy*dy) <= 1.0

def create_cloud_overlap_square(ctx, cx, cy, size, text="CLOUD!", density="medium"):
    """Create square with cloud-like overlapping circles"""
    
    # Density settings - more minimal approach
    densities = {
        "low": 2,
        "medium": 3,
        "high": 4,
        "very_high": 5
    }
    num_circles = densities.get(density, 5)
    
    # Generate cloud-like circles
    all_circles = []
    half_size = size / 2
    
    # Add circles around the perimeter - more minimal approach
    for angle in range(0, 360, 45):  # Every 45 degrees (8 positions instead of 12)
        rad = math.radians(angle)
        
        # Base position on square perimeter
        base_distance = half_size + random.uniform(5, 15)
        base_x = cx + base_distance * math.cos(rad)
        base_y = cy + base_distance * math.sin(rad)
        
        # Add 1-2 circles at this angle (reduced from 1-3)
        for i in range(random.randint(1, 2)):
            circle_x = base_x + random.uniform(-10, 10)
            circle_y = base_y + random.uniform(-10, 10)
            
            radius = random.uniform(15, 25)
            
            all_circles.append({
                'x': circle_x,
                'y': circle_y,
                'rx': radius * random.uniform(0.8, 1.2),
                'ry': radius * random.uniform(0.8, 1.2),
                'side': 'cloud'
            })
    
    # Draw cloud circles
    for circle in all_circles:
        draw_cloud_circle(ctx, circle)
    
    # Draw base square
    draw_base_square(ctx, cx, cy, size)
    
    # Add text
    draw_overlap_text(ctx, cx, cy, text)

def draw_cloud_circle(ctx, circle):
    """Draw a cloud-style circle"""
    
    ctx.save()
    ctx.translate(circle['x'], circle['y'])
    ctx.scale(circle['rx'], circle['ry'])
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    
    # Cloud-like gradient
    gradient = cairo.RadialGradient(
        circle['x'], circle['y'], 0,
        circle['x'], circle['y'], max(circle['rx'], circle['ry'])
    )
    gradient.add_color_stop_rgb(0, 1.0, 1.0, 1.0)       # Pure white
    gradient.add_color_stop_rgb(0.6, 0.98, 0.98, 1.0)   # Very light blue
    gradient.add_color_stop_rgb(1, 0.9, 0.9, 0.95)      # Light edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Soft outline
    ctx.set_source_rgba(0, 0, 0, 0.2)
    ctx.set_line_width(0.8)
    ctx.stroke()

def add_corner_ellipses(ctx, cx, cy, half_width, half_height):
    """Add small ellipses in some corners for extra detail"""
    
    # Define corner positions
    corners = [
        (cx - half_width, cy - half_height, "top-left"),
        (cx + half_width, cy - half_height, "top-right"), 
        (cx + half_width, cy + half_height, "bottom-right"),
        (cx - half_width, cy + half_height, "bottom-left")
    ]
    
    # Randomly add small ellipses to 1-2 corners
    num_corners = random.randint(1, 2)
    selected_corners = random.sample(corners, num_corners)
    
    for corner_x, corner_y, corner_name in selected_corners:
        # Create small ellipse near the corner
        offset_distance = random.uniform(8, 15)
        
        # Offset slightly away from the exact corner
        if "top" in corner_name:
            ellipse_y = corner_y - offset_distance
        else:
            ellipse_y = corner_y + offset_distance
            
        if "left" in corner_name:
            ellipse_x = corner_x - offset_distance
        else:
            ellipse_x = corner_x + offset_distance
        
        # Small ellipse size
        radius_x = random.uniform(6, 12)
        radius_y = random.uniform(6, 12)
        
        # Draw the small corner ellipse
        ctx.save()
        ctx.translate(ellipse_x, ellipse_y)
        ctx.scale(radius_x, radius_y)
        ctx.arc(0, 0, 1, 0, 2 * math.pi)
        ctx.restore()
        
        # Small ellipse gradient
        gradient = cairo.RadialGradient(
            ellipse_x, ellipse_y, 0,
            ellipse_x, ellipse_y, max(radius_x, radius_y)
        )
        gradient.add_color_stop_rgb(0, 0.95, 0.95, 1.0)   # Light center
        gradient.add_color_stop_rgb(1, 0.85, 0.85, 0.9)   # Darker edge
        
        ctx.set_source(gradient)
        ctx.fill_preserve()
        
        # Small outline
        ctx.set_source_rgba(0, 0, 0, 0.5)
        ctx.set_line_width(1.0)
        ctx.stroke()

def draw_overlap_text(ctx, cx, cy, text):
    """Draw text in the overlapping bubble"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(14)
    
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    text_x = cx - text_width / 2
    text_y = cy + text_height / 2
    
    # Text shadow
    ctx.set_source_rgba(0, 0, 0, 0.3)
    ctx.move_to(text_x + 1, text_y + 1)
    ctx.show_text(text)
    
    # Main text
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_overlapping_demo():
    """Create demo with one example of overlapping circle styles"""
    
    random.seed(777)
    
    WIDTH, HEIGHT = 500, 400
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Optional background (leave transparent if flag set)
    if not TRANSPARENT_CANVAS:
        ctx.set_source_rgb(0.97, 0.97, 0.99)
        ctx.paint()
    
    # Single example - organic style with good crossing (casual variation)
    create_overlapping_circles_square(ctx, 250, 200, 180, 120, "", "organic", show_full_ovals=False)
    
    # (Title and subtitle removed as per request)
    
    surface.write_to_png("overlapping_circles_squares.png")
    print("✅ Overlapping circles squares saved as 'overlapping_circles_squares.png'")

def create_multiple_casual_examples(count=5, seed=None, width=420, height=320):
    """Generate several bubble examples each with casual varied negative-space arcs.
    Saves files: bubble_casual_1.png ... bubble_casual_n.png"""
    if seed is not None:
        random.seed(seed)
    for i in range(1, count+1):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(surface)
        if not TRANSPARENT_CANVAS:
            ctx.set_source_rgb(1,1,1)
            ctx.paint()
        # Vary rectangle size slightly
        base_w = 170 + random.uniform(-15, 15)
        base_h = 115 + random.uniform(-12, 12)
        # Slight center jitter
        cx = width/2 + random.uniform(-8, 8)
        cy = height/2 + random.uniform(-6, 6)
        create_overlapping_circles_square(ctx, cx, cy, base_w, base_h, "", "organic", show_full_ovals=False)
        fname = f"bubble_casual_{i}.png"
        surface.write_to_png(fname)
        print(f"💠 Saved {fname}")

def create_laugh_demo(seed=123, width=420, height=320):
    """Generate a single 'laugh' style bubble example (minimal arcs mode)."""
    random.seed(seed)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    if not TRANSPARENT_CANVAS:
        ctx.set_source_rgb(1,1,1)
        ctx.paint()
    cx, cy = width/2, height/2
    create_overlapping_circles_square(ctx, cx, cy, 190, 130, "", "laugh", show_full_ovals=False)
    out = "bubble_laugh.png"
    surface.write_to_png(out)
    print(f"😂 Saved laugh bubble '{out}'")

## Circle variant creation & demo moved to overlapping_circles_circle.py


if __name__ == "__main__":
    # Rectangle-focused demos only (circle variant now in overlapping_circles_circle.py)
    create_overlapping_demo()
    create_laugh_demo()
    print("🔴 Created rectangle-based overlapping bubbles (circle variant separated).")