import math, cairo, random
from overlapping_circles_circle import (
    create_overlapping_circles_circle_radial5,
    create_overlapping_circles_circle_radial6,
    create_overlapping_circles_circle_radial7,
)
from overlapping_circles_squares import (
    create_overlapping_circles_square,
)

# Simple text measurement helper

def measure_text_block(ctx, text, max_width, font_family="Arial", font_size=64, line_spacing=1.15):
    ctx.select_font_face(font_family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(font_size)
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = w if not cur else cur + " " + w
        xb,yb,wid,hei,xa,ya = ctx.text_extents(trial)
        if wid > max_width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    widths = []
    total_h = 0
    for line in lines:
        xb,yb,wid,hei,xa,ya = ctx.text_extents(line)
        widths.append(wid)
        total_h += hei * line_spacing
    return {
        'lines': lines,
        'width': max(widths) if widths else 0,
        'height': total_h,
        'font_size': font_size
    }

# Free space sampling borrowed conceptually from laugh_boom_simple

def point_in_circle(px, py, cx, cy, r):
    return (px-cx)**2 + (py-cy)**2 <= r*r

def point_in_any(px, py, circles):
    for c in circles:
        dx = (px - c['x'])/c['rx']
        dy = (py - c['y'])/c['ry']
        if dx*dx + dy*dy <= 1.0:
            return True
    return False

def find_free_bbox_circle(cx, cy, radius, circles, samples=120):
    free=[]
    r = radius * 0.97
    for i in range(samples):
        for j in range(samples):
            x = cx - r + 2*r*(i/(samples-1))
            y = cy - r + 2*r*(j/(samples-1))
            if not point_in_circle(x,y,cx,cy,radius):
                continue
            if point_in_any(x,y,circles):
                continue
            free.append((x,y))
    if not free:
        return cx, cy, 0, 0
    min_x = min(p[0] for p in free); max_x = max(p[0] for p in free)
    min_y = min(p[1] for p in free); max_y = max(p[1] for p in free)
    return (min_x+max_x)/2, (min_y+max_y)/2, (max_x-min_x), (max_y-min_y)

def _fit_text_in_free_box(ctx, text, box_w, box_h, max_font_size, min_font_size=14, margin_scale=0.85):
    """Choose a font size so text (single line) fits inside free box with margin.
    For multi-word text we do not re-wrap here; caller may pre-wrap.
    Shrinks until both width and height constraints satisfied or min reached."""
    ctx.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    size = max_font_size
    target_w = box_w * margin_scale
    target_h = box_h * margin_scale
    while size >= min_font_size:
        ctx.set_font_size(size)
        xb,yb,w,h,xa,ya = ctx.text_extents(text)
        if w <= target_w and h <= target_h:
            return size, (w,h,xb,yb,xa,ya)
        size *= 0.92
    ctx.set_font_size(min_font_size)
    xb,yb,w,h,xa,ya = ctx.text_extents(text)
    return min_font_size, (w,h,xb,yb,xa,ya)

def _wrap_two_lines(ctx, text, max_width, start_size, min_font_size, line_spacing=1.1):
    """Attempt to wrap text into up to two lines. Shrink font if needed.
    Returns: (font_size, lines:list[str], metrics:[(w,h,xb,yb,xa,ya)], total_height, wrapped:bool)
    """
    words = text.split()
    if len(words) <= 1:
        ctx.set_font_size(start_size)
        xb,yb,w,h,xa,ya = ctx.text_extents(text)
        return start_size, [text], [(w,h,xb,yb,xa,ya)], h, False
    size = start_size
    while size >= min_font_size:
        ctx.set_font_size(size)
        # Greedy line build for up to two lines
        line1 = []
        for i,w in enumerate(words):
            trial = (" ".join(line1 + [w])).strip()
            xb,yb,wid,hei,xa,ya = ctx.text_extents(trial)
            if wid > max_width and line1:
                # line1 finished
                remaining = words[i:]
                line2 = " ".join(remaining)
                xb2,yb2,wid2,hei2,xa2,ya2 = ctx.text_extents(line2)
                if wid2 <= max_width:
                    total_h = hei + hei2*line_spacing
                    return size, [" ".join(line1), line2], [(wid,hei,xb,yb,xa,ya),(wid2,hei2,xb2,yb2,xa2,ya2)], total_h, True
                else:
                    break  # need to shrink
            else:
                line1.append(w)
        else:
            # all words fit in one line
            full = " ".join(line1)
            xb,yb,wid,hei,xa,ya = ctx.text_extents(full)
            return size, [full], [(wid,hei,xb,yb,xa,ya)], hei, False
        size *= 0.92
    # Fallback minimal size single line
    ctx.set_font_size(min_font_size)
    xb,yb,wid,hei,xa,ya = ctx.text_extents(text)
    return min_font_size, [text], [(wid,hei,xb,yb,xa,ya)], hei, False

def _verify_lines_inside_circle(circles, cx, cy, core_radius, fcx, fcy, lines, line_metrics, total_h, line_spacing=1.1, sample_density=6):
    """Return True if all sampled points of each line's bounding box lie inside base circle and outside all ovals."""
    if not lines:
        return True
    cursor_y = fcy - total_h/2
    for (line,(w,h,xb,yb,xa,ya)) in zip(lines, line_metrics):
        baseline_y = cursor_y + h
        left = fcx - w/2
        top = baseline_y + yb  # yb typically negative
        for sx in range(sample_density):
            for sy in range(sample_density):
                px = left + w * (sx/(sample_density-1))
                py = top + h * (sy/(sample_density-1))
                # inside base circle
                if (px-cx)**2 + (py-cy)**2 > core_radius**2:
                    return False
                # must NOT be inside any oval
                if point_in_any(px,py,circles):
                    return False
        cursor_y += h * line_spacing
    return True

def _verify_lines_inside_rect(circles, cx, cy, half_w, half_h, fcx, fcy, lines, line_metrics, total_h, line_spacing=1.1, sample_density=6):
    if not lines:
        return True
    cursor_y = fcy - total_h/2
    for (line,(w,h,xb,yb,xa,ya)) in zip(lines, line_metrics):
        baseline_y = cursor_y + h
        left = fcx - w/2
        top = baseline_y + yb
        for sx in range(sample_density):
            for sy in range(sample_density):
                px = left + w * (sx/(sample_density-1))
                py = top + h * (sy/(sample_density-1))
                if abs(px-cx) > half_w or abs(py-cy) > half_h:
                    return False
                if point_in_any(px,py,circles):
                    return False
        cursor_y += h * line_spacing
    return True

# Adaptive circle bubble sizing (radial variants)

RADIAL_GENERATORS = {
    'radial5': create_overlapping_circles_circle_radial5,
    'radial6': create_overlapping_circles_circle_radial6,
    'radial7': create_overlapping_circles_circle_radial7,
}

def adaptive_circle_bubble(text, variant='radial5', target_inner_padding=20,
                            canvas_size=(600,600), max_iterations=5, seed=1234,
                            max_panel_fraction=0.3, min_font_size=12,
                            wrap=False, max_lines=2, ensure_inside=True, verify_attempts=8,
                            tail_target=None, tail_length_factor=0.55, tail_width_factor=0.28, tail_style='triangle',
                            whitespace_scale=1.0, auto_whitespace=False):
    random.seed(seed)
    width,height = canvas_size
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.set_source_rgba(0,0,0,0); ctx.paint()

    # 1. Initial text measure (optimistic width)
    measure_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 10,10)
    mctx = cairo.Context(measure_surface)
    tb = measure_text_block(mctx, text, max_width=width*0.55, font_size=64)
    # Compute adaptive whitespace
    if auto_whitespace:
        # scale with panel smaller dimension leaving margin; clamp
        base_pad = min(width, height) * 0.03 + target_inner_padding
        effective_padding = base_pad * whitespace_scale
    else:
        effective_padding = target_inner_padding * whitespace_scale
    required_w = tb['width'] + 2*effective_padding
    required_h = tb['height'] + 2*effective_padding

    core_radius = max(required_w, required_h) * 0.55
    gen = RADIAL_GENERATORS[variant]
    cx = width/2; cy = height/2

    capped = False
    for _ in range(max_iterations):
        surface_tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        tctx = cairo.Context(surface_tmp)
        circles = gen(tctx, cx, cy, core_radius, text="", style='laugh', show_full_ovals=False, return_circles=True)
        fcx, fcy, fw, fh = find_free_bbox_circle(cx, cy, core_radius, circles, samples=120)
        if fw == 0 or fh == 0:
            core_radius *= 1.2
            continue
        scale_w = required_w / fw
        scale_h = required_h / fh
        needed = max(scale_w, scale_h)
        # enforce panel fraction cap (circle cluster overall diameter ~ 2*core_radius)
        max_w = width * max_panel_fraction
        max_h = height * max_panel_fraction
        # if applying needed would exceed cap, clamp and mark capped
        projected_radius = core_radius * needed
        if (projected_radius*2 > max_w) or (projected_radius*2 > max_h):
            # clamp so diameter fits within min(max_w,max_h) respecting aspect neutrality
            limit_diam = min(max_w, max_h)
            core_radius = limit_diam / 2.0
            capped = True
            break
        if 0.92 < needed < 1.08:
            break
        core_radius *= needed

    # Draw final bubble
    circles = gen(ctx, cx, cy, core_radius, text="", style='laugh', show_full_ovals=False, return_circles=True)
    fcx, fcy, fw, fh = find_free_bbox_circle(cx, cy, core_radius, circles, samples=140)
    tail_points = None
    if tail_target is not None:
        tx, ty = tail_target
        # direction vector from bubble center to tail target
        dx = tx - cx; dy = ty - cy
        dist = math.hypot(dx, dy) or 1.0
        ux, uy = dx/dist, dy/dist
        # base attach point on circle boundary
        attach_x = cx + ux * core_radius
        attach_y = cy + uy * core_radius
        # perpendicular for width
        px, py = -uy, ux
        tail_len = core_radius * tail_length_factor
        tail_w = core_radius * tail_width_factor
        tip_x = attach_x + ux * tail_len
        tip_y = attach_y + uy * tail_len
        p1x = attach_x + px * tail_w * 0.5
        p1y = attach_y + py * tail_w * 0.5
        p2x = attach_x - px * tail_w * 0.5
        p2y = attach_y - py * tail_w * 0.5
        ctx.save()
        ctx.set_source_rgba(1,1,1,1)
        ctx.move_to(p1x, p1y)
        ctx.line_to(p2x, p2y)
        ctx.line_to(tip_x, tip_y)
        ctx.close_path()
        ctx.fill_preserve()
        ctx.set_source_rgba(0,0,0,0.95)
        ctx.set_line_width(2.2)
        ctx.stroke()
        ctx.restore()
        tail_points = [(p1x,p1y),(p2x,p2y),(tip_x,tip_y)]
    # place text with safe fitting
    font_shrunk = False
    lines = [text]; line_metrics=[]; size=0; total_h=0; wrapped=False
    if fw>0 and fh>0:
        max_font_attempt = min(fh*0.65, fw*0.40)
        if wrap and max_lines >= 2:
            size, lines, line_metrics, total_h, wrapped = _wrap_two_lines(ctx, text, fw*0.82, max_font_attempt, min_font_size)
            if size == min_font_size and len(lines)==1 and not wrapped:
                font_shrunk = True
        else:
            size,(tw,th,xb,yb,xa,ya)= _fit_text_in_free_box(ctx, text, fw, fh, max_font_size=max_font_attempt, min_font_size=min_font_size, margin_scale=0.82)
            line_metrics=[(tw,th,xb,yb,xa,ya)]; total_h=th; font_shrunk = (size==min_font_size)
    else:
        ctx.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        size = max(min_font_size, 24)
        ctx.set_font_size(size)
        xb,yb,tw,th,xa,ya = ctx.text_extents(text)
        line_metrics=[(tw,th,xb,yb,xa,ya)]; total_h=th

    text_verified = True
    adjust_iterations = 0
    if ensure_inside and fw>0 and fh>0:
        while adjust_iterations < verify_attempts:
            ok = _verify_lines_inside_circle(circles, cx, cy, core_radius, fcx, fcy, lines, line_metrics, total_h)
            if ok:
                break
            # shrink and recompute
            adjust_iterations += 1
            new_start = size * 0.92
            if new_start < min_font_size:
                size = min_font_size
                font_shrunk = True
                # final attempt recompute metrics at min_font_size
                if wrap and max_lines>=2:
                    size, lines, line_metrics, total_h, wrapped = _wrap_two_lines(ctx, text, fw*0.82, size, min_font_size)
                else:
                    ctx.set_font_size(size)
                    xb,yb,tw,th,xa,ya = ctx.text_extents(text)
                    line_metrics=[(tw,th,xb,yb,xa,ya)]; total_h=th
                break
            if wrap and max_lines>=2:
                size, lines, line_metrics, total_h, wrapped = _wrap_two_lines(ctx, text, fw*0.82, new_start, min_font_size)
            else:
                ctx.set_font_size(new_start)
                size = new_start
                xb,yb,tw,th,xa,ya = ctx.text_extents(text)
                line_metrics=[(tw,th,xb,yb,xa,ya)]; total_h=th
        else:
            pass
        # final verification state
        text_verified = _verify_lines_inside_circle(circles, cx, cy, core_radius, fcx, fcy, lines, line_metrics, total_h)
    else:
        text_verified = True
    # Render lines centered
    cursor_y = fcy - total_h/2
    ctx.set_source_rgba(0,0,0,0.95)
    for (line,(tw,th,xb,yb,xa,ya)) in zip(lines,line_metrics):
        ctx.move_to(fcx - tw/2 - xb, cursor_y + th)
        ctx.show_text(line)
        cursor_y += th * 1.1
    return surface, {
        'core_radius': core_radius,
        'free_box': (fcx, fcy, fw, fh),
        'capped': capped,
        'font_shrunk': font_shrunk,
        'max_panel_fraction': max_panel_fraction,
        'wrapped': wrapped,
        'lines': lines,
        'font_size': size,
        'text_verified': text_verified,
        'adjust_iterations': adjust_iterations,
        'tail_points': tail_points,
        'effective_padding': effective_padding,
        'whitespace_scale': whitespace_scale
    }

# Adaptive rectangle bubble (square/rectangle base)

def find_free_bbox_rect(cx, cy, half_w, half_h, circles, samples=140):
    free=[]
    for i in range(samples):
        for j in range(samples):
            x = cx - half_w + 2*half_w*(i/(samples-1))
            y = cy - half_h + 2*half_h*(j/(samples-1))
            if point_in_any(x,y,circles):
                continue
            free.append((x,y))
    if not free:
        return cx, cy, 0, 0
    min_x = min(p[0] for p in free); max_x = max(p[0] for p in free)
    min_y = min(p[1] for p in free); max_y = max(p[1] for p in free)
    return (min_x+max_x)/2, (min_y+max_y)/2, (max_x-min_x), (max_y-min_y)

def adaptive_square_bubble(text, target_inner_padding=20, canvas_size=(600,600), aspect_ratio=1.1,
                            max_iterations=6, seed=5678, max_panel_fraction=0.3, min_font_size=12,
                            wrap=False, max_lines=2, ensure_inside=True, verify_attempts=8,
                            tail_target=None, tail_length_factor=0.55, tail_width_factor=0.28, tail_style='triangle',
                            whitespace_scale=1.0, auto_whitespace=False):
    random.seed(seed)
    width,height = canvas_size
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.set_source_rgba(0,0,0,0); ctx.paint()

    measure_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 10,10)
    mctx = cairo.Context(measure_surface)
    tb = measure_text_block(mctx, text, max_width=width*0.55, font_size=64)
    if auto_whitespace:
        base_pad = min(width, height) * 0.03 + target_inner_padding
        effective_padding = base_pad * whitespace_scale
    else:
        effective_padding = target_inner_padding * whitespace_scale
    required_w = tb['width'] + 2*effective_padding
    required_h = tb['height'] + 2*effective_padding

    half_w = required_w * 0.55 / 2
    half_h = (required_h * 0.55 / aspect_ratio) / 2
    cx = width/2; cy = height/2

    capped = False
    for _ in range(max_iterations):
        surface_tmp = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        tctx = cairo.Context(surface_tmp)
        circles = create_overlapping_circles_square(tctx, cx, cy, half_w*2, half_h*2, text="", circle_style='laugh', show_full_ovals=False, return_circles=True)
        fcx,fcy,fw,fh = find_free_bbox_rect(cx, cy, half_w, half_h, circles, samples=120)
        if fw==0 or fh==0:
            half_w *= 1.2; half_h *= 1.2
            continue
        scale_w = required_w / fw
        scale_h = required_h / fh
        needed = max(scale_w, scale_h)
        max_w = width * max_panel_fraction
        max_h = height * max_panel_fraction
        projected_w = half_w * 2 * needed
        projected_h = half_h * 2 * needed
        if (projected_w > max_w) or (projected_h > max_h):
            # clamp preserving current aspect
            scale_limit = min(max_w / (half_w*2), max_h / (half_h*2))
            half_w *= scale_limit
            half_h *= scale_limit
            capped = True
            break
        if 0.92 < needed < 1.08:
            break
        half_w *= needed; half_h *= needed

    circles = create_overlapping_circles_square(ctx, cx, cy, half_w*2, half_h*2, text="", circle_style='laugh', show_full_ovals=False, return_circles=True)
    fcx,fcy,fw,fh = find_free_bbox_rect(cx, cy, half_w, half_h, circles, samples=150)
    tail_points = None
    if tail_target is not None:
        tx, ty = tail_target
        dx = tx - cx; dy = ty - cy
        dist = math.hypot(dx, dy) or 1.0
        ux, uy = dx/dist, dy/dist
        # clamp attach along rectangle edge by intersecting ray with rectangle bounds
        # param t where cx+ux*t hits edge
        t_vals = []
        if ux != 0:
            t_vals.append(( (cx + half_w - cx)/ux ))  # right
            t_vals.append(( (cx - half_w - cx)/ux ))  # left
        if uy != 0:
            t_vals.append(( (cy + half_h - cy)/uy ))  # bottom
            t_vals.append(( (cy - half_h - cy)/uy ))  # top
        # choose smallest positive t
        attach_t = None
        for tv in t_vals:
            if tv>0 and (attach_t is None or tv < attach_t):
                attach_t = tv
        if attach_t is None:
            attach_t = half_w  # fallback
        attach_x = cx + ux * attach_t
        attach_y = cy + uy * attach_t
        px, py = -uy, ux
        tail_len = max(half_w, half_h) * tail_length_factor
        tail_w = max(half_w, half_h) * tail_width_factor
        tip_x = attach_x + ux * tail_len
        tip_y = attach_y + uy * tail_len
        p1x = attach_x + px * tail_w * 0.5
        p1y = attach_y + py * tail_w * 0.5
        p2x = attach_x - px * tail_w * 0.5
        p2y = attach_y - py * tail_w * 0.5
        ctx.save()
        ctx.set_source_rgba(1,1,1,1)
        ctx.move_to(p1x, p1y)
        ctx.line_to(p2x, p2y)
        ctx.line_to(tip_x, tip_y)
        ctx.close_path()
        ctx.fill_preserve()
        ctx.set_source_rgba(0,0,0,0.95)
        ctx.set_line_width(2.2)
        ctx.stroke()
        ctx.restore()
        tail_points = [(p1x,p1y),(p2x,p2y),(tip_x,tip_y)]

    font_shrunk = False
    lines=[text]; line_metrics=[]; size=0; total_h=0; wrapped=False
    if fw>0 and fh>0:
        max_font_attempt = min(fh*0.62, fw*0.38)
        if wrap and max_lines >= 2:
            size, lines, line_metrics, total_h, wrapped = _wrap_two_lines(ctx, text, fw*0.80, max_font_attempt, min_font_size)
            if size == min_font_size and len(lines)==1 and not wrapped:
                font_shrunk = True
        else:
            size,(tw,th,xb,yb,xa,ya)= _fit_text_in_free_box(ctx, text, fw, fh, max_font_size=max_font_attempt, min_font_size=min_font_size, margin_scale=0.80)
            line_metrics=[(tw,th,xb,yb,xa,ya)]; total_h=th; font_shrunk=(size==min_font_size)
    else:
        ctx.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        size = max(min_font_size, 24)
        ctx.set_font_size(size)
        xb,yb,tw,th,xa,ya = ctx.text_extents(text)
        line_metrics=[(tw,th,xb,yb,xa,ya)]; total_h=th
    text_verified = True
    adjust_iterations = 0
    if ensure_inside and fw>0 and fh>0:
        while adjust_iterations < verify_attempts:
            ok = _verify_lines_inside_rect(circles, cx, cy, half_w, half_h, fcx, fcy, lines, line_metrics, total_h)
            if ok:
                break
            adjust_iterations += 1
            new_start = size * 0.92
            if new_start < min_font_size:
                size = min_font_size
                font_shrunk = True
                if wrap and max_lines>=2:
                    size, lines, line_metrics, total_h, wrapped = _wrap_two_lines(ctx, text, fw*0.80, size, min_font_size)
                else:
                    ctx.set_font_size(size)
                    xb,yb,tw,th,xa,ya = ctx.text_extents(text)
                    line_metrics=[(tw,th,xb,yb,xa,ya)]; total_h=th
                break
            if wrap and max_lines>=2:
                size, lines, line_metrics, total_h, wrapped = _wrap_two_lines(ctx, text, fw*0.80, new_start, min_font_size)
            else:
                ctx.set_font_size(new_start)
                size = new_start
                xb,yb,tw,th,xa,ya = ctx.text_extents(text)
                line_metrics=[(tw,th,xb,yb,xa,ya)]; total_h=th
        text_verified = _verify_lines_inside_rect(circles, cx, cy, half_w, half_h, fcx, fcy, lines, line_metrics, total_h)
    else:
        text_verified = True
    cursor_y = fcy - total_h/2
    ctx.set_source_rgba(0,0,0,0.95)
    for (line,(tw,th,xb,yb,xa,ya)) in zip(lines,line_metrics):
        ctx.move_to(fcx - tw/2 - xb, cursor_y + th)
        ctx.show_text(line)
        cursor_y += th * 1.1
    return surface, {
        'half_w': half_w,
        'half_h': half_h,
        'free_box': (fcx,fcy,fw,fh),
        'capped': capped,
        'font_shrunk': font_shrunk,
        'max_panel_fraction': max_panel_fraction,
        'wrapped': wrapped,
        'lines': lines,
        'font_size': size,
        'text_verified': text_verified,
        'adjust_iterations': adjust_iterations,
        'tail_points': tail_points,
        'effective_padding': effective_padding,
        'whitespace_scale': whitespace_scale
    }

# Demo runner

def demo():
    circ_surf, circ_meta = adaptive_circle_bubble("BOOM ENERGY", variant='radial5')
    circ_surf.write_to_png('adaptive_circle_radial5.png')
    print('Saved adaptive_circle_radial5.png', circ_meta)
    sq_surf, sq_meta = adaptive_square_bubble("WHISPER CORE")
    sq_surf.write_to_png('adaptive_square.png')
    print('Saved adaptive_square.png', sq_meta)

if __name__ == '__main__':
    demo()
