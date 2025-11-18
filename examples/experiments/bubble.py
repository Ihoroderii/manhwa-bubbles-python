import cairo, math

WIDTH, HEIGHT = 500, 400
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

# ------------------------------------------------------------------
# Configuration flags
# ------------------------------------------------------------------
PAINT_BACKGROUND = False   # Set True if you still want an opaque white rectangle
FILL_TAIL_WHITE   = True    # Tail interior fill (set False to keep entirely transparent)

# Optional background paint (kept conditional so PNG can be transparent)
if PAINT_BACKGROUND:
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.paint()

# Ellipse parameters
cx, cy = 250, 200   # center
rx, ry = 150, 100   # radii

# Variable stroke thickness function
def stroke_width(theta):
    # Thin at top, thick at bottom
    return 3 + 6 * (0.5 + 0.5 * math.sin(theta))

# Tail placement
tail_angle = math.pi/2   # bottom (90°)
tail_width = 0.5         # radians: size of gap

# Compute ellipse outline with gap for tail
outer, inner = [], []
steps = 300
for i in range(steps+1):
    theta = 2*math.pi*i/steps
    # skip arc where tail attaches
    if tail_angle-tail_width/2 < theta < tail_angle+tail_width/2:
        continue

    x = cx + rx*math.cos(theta)
    y = cy + ry*math.sin(theta)

    # Normal vector
    nx = math.cos(theta) / rx
    ny = math.sin(theta) / ry
    norm = math.sqrt(nx*nx + ny*ny)
    nx, ny = nx/norm, ny/norm

    w = stroke_width(theta)
    outer.append((x + nx*w/2, y + ny*w/2))
    inner.append((x - nx*w/2, y - ny*w/2))

# Draw ellipse (as filled polygon with variable width)
ctx.set_source_rgb(0, 0, 0)
ctx.move_to(*outer[0])
for p in outer:
    ctx.line_to(*p)
for p in reversed(inner):
    ctx.line_to(*p)
ctx.close_path()
ctx.fill()

# --- Draw smoother, natural tail ---
tail_tip = (cx, cy + ry + 70)      # tip of tail
left_attach = (cx - 25, cy + ry)   # left base of gap
right_attach = (cx + 25, cy + ry)  # right base of gap

ctx.move_to(*left_attach)
ctx.curve_to(cx - 15, cy + ry + 20, cx - 10, cy + ry + 40, *tail_tip)
ctx.curve_to(cx + 10, cy + ry + 40, cx + 15, cy + ry + 20, *right_attach)
ctx.close_path()

if FILL_TAIL_WHITE:
    # Fill white tail interior then outline
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
else:
    # Just outline (tail interior remains transparent)
    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.new_path()  # discard fill

# Outline black (tail border)
ctx.set_source_rgb(0, 0, 0)
ctx.set_line_width(2)
ctx.stroke()

# Save
surface.write_to_png("ellipse_natural_tail.png")
print("✅ Saved bubble with natural white tail -> ellipse_natural_tail.png")


# (Removed unrelated text wrapping and font test demos to keep output focused.)

