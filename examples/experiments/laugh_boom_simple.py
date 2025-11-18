import cairo, random
from overlapping_circles_circle import (
    create_overlapping_circles_circle,
    create_overlapping_circles_circle_radial5,
    create_overlapping_circles_circle_radial6,
    create_overlapping_circles_circle_radial7,
    TRANSPARENT_CANVAS
)
import math

TEXT = "BOOM!"
STYLE = "laugh"
SEED = 1337
WIDTH = 500
HEIGHT = 380
RADIUS = 130

# Ensure text drawing is enabled (relies on global flag in original module)
# (If user had disabled globally, we still attempt; if not printed, check DRAW_TEXT.)


def _point_in_any(px, py, circles):
    for c in circles:
        dx = (px - c['x'])/c['rx']
        dy = (py - c['y'])/c['ry']
        if dx*dx + dy*dy <= 1.0:
            return True
    return False

def _find_free_space_bbox(cx, cy, radius, circles, samples=140):
    # sample a grid inside the base circle; keep those not inside any oval
    free = []
    r = radius * 0.95
    for i in range(samples):
        for j in range(samples):
            x = cx - r + 2*r*(i/(samples-1))
            y = cy - r + 2*r*(j/(samples-1))
            if (x-cx)**2 + (y-cy)**2 > radius*radius: # outside base circle
                continue
            if _point_in_any(x, y, circles):
                continue
            free.append((x,y))
    if not free:
        return cx, cy, 0, 0
    min_x = min(p[0] for p in free); max_x = max(p[0] for p in free)
    min_y = min(p[1] for p in free); max_y = max(p[1] for p in free)
    return (min_x+max_x)/2, (min_y+max_y)/2, (max_x-min_x), (max_y-min_y)

def render_variant(name, draw_fn):
    random.seed(SEED)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    if not TRANSPARENT_CANVAS:
        ctx.set_source_rgb(1,1,1); ctx.paint()
    cx, cy = WIDTH/2, HEIGHT/2
    circles = draw_fn(ctx, cx, cy, RADIUS, TEXT, STYLE, show_full_ovals=False, return_circles=True)
    # find free region center & size
    fcx, fcy, fw, fh = _find_free_space_bbox(cx, cy, RADIUS, circles, samples=120)
    # choose font size to fit inside free bbox with margin
    if fw > 0 and fh > 0:
        ctx.save()
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        # iterative shrink to fit
        target_w = fw*0.85
        target_h = fh*0.85
        size = min(target_h*1.6, target_w*0.7)  # heuristic mapping
        size = max(24, size)
        ctx.set_font_size(size)
        xb, yb, w, h, xa, ya = ctx.text_extents(TEXT)
        # adjust if overflow
        scale_factor = 1.0
        if w > target_w:
            scale_factor = min(scale_factor, target_w / w)
        if h > target_h:
            scale_factor = min(scale_factor, target_h / h)
        if scale_factor < 0.999:
            ctx.set_font_size(size * scale_factor)
            xb, yb, w, h, xa, ya = ctx.text_extents(TEXT)
        ctx.move_to(fcx - w/2 - xb, fcy + h/2)
        ctx.set_source_rgba(0,0,0,0.95)
        ctx.show_text(TEXT)
        ctx.restore()
    else:
        # fallback: center
        ctx.save(); ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(60)
        xb, yb, w, h, xa, ya = ctx.text_extents(TEXT)
        ctx.move_to(cx - w/2 - xb, cy + h/2)
        ctx.set_source_rgba(0,0,0,0.95); ctx.show_text(TEXT); ctx.restore()
    out = f"laugh_boom_{name}.png"
    surface.write_to_png(out)
    print(f"Saved {out}")


def main():
    render_variant("side", create_overlapping_circles_circle)
    render_variant("radial5", create_overlapping_circles_circle_radial5)
    # 6-oval elongated variant
    render_variant("radial6", create_overlapping_circles_circle_radial6)
    render_variant("radial7", create_overlapping_circles_circle_radial7)

if __name__ == "__main__":
    main()
