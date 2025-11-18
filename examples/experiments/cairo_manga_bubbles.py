import cairo
import math
import gi
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo

def create_ellipse_bubble(ctx, cx, cy, rx, ry, text="Hello!", tail_position="bottom"):
    """Create an elliptical speech bubble with variable stroke width"""
    
    # Variable stroke thickness function
    def stroke_width(theta):
        return 3 + 4 * (0.5 + 0.5 * math.sin(theta))
    
    # Tail parameters
    tail_angles = {
        "bottom": math.pi/2,
        "top": -math.pi/2,
        "left": math.pi,
        "right": 0
    }
    tail_angle = tail_angles.get(tail_position, math.pi/2)
    tail_width = 0.4  # radians
    
    # Compute ellipse outline with gap for tail
    outer, inner = [], []
    steps = 200
    for i in range(steps+1):
        theta = 2*math.pi*i/steps
        # Skip arc where tail attaches
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
    
    # Draw ellipse body
    ctx.set_source_rgb(1, 1, 1)  # white fill
    ctx.move_to(*outer[0])
    for p in outer:
        ctx.line_to(*p)
    for p in reversed(inner):
        ctx.line_to(*p)
    ctx.close_path()
    ctx.fill_preserve()
    
    # Black outline
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(1)
    ctx.stroke()
    
    # Draw tail
    draw_tail(ctx, cx, cy, rx, ry, tail_position)
    
    # Add text
    draw_centered_text(ctx, cx, cy, rx*1.5, ry*1.5, text)

def draw_tail(ctx, cx, cy, rx, ry, position="bottom"):
    """Draw a smooth tail for the speech bubble"""
    
    if position == "bottom":
        tail_tip = (cx, cy + ry + 50)
        left_attach = (cx - 20, cy + ry - 5)
        right_attach = (cx + 20, cy + ry - 5)
        
        ctx.move_to(*left_attach)
        ctx.curve_to(cx - 10, cy + ry + 15, cx - 5, cy + ry + 35, *tail_tip)
        ctx.curve_to(cx + 5, cy + ry + 35, cx + 10, cy + ry + 15, *right_attach)
        
    elif position == "left":
        tail_tip = (cx - rx - 50, cy)
        top_attach = (cx - rx + 5, cy - 20)
        bottom_attach = (cx - rx + 5, cy + 20)
        
        ctx.move_to(*top_attach)
        ctx.curve_to(cx - rx - 15, cy - 10, cx - rx - 35, cy - 5, *tail_tip)
        ctx.curve_to(cx - rx - 35, cy + 5, cx - rx - 15, cy + 10, *bottom_attach)
    
    ctx.close_path()
    
    # Fill white
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    
    # Outline black
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()

def create_cloud_bubble(ctx, cx, cy, radius, text="Thinking..."):
    """Create a thought bubble with cloud-like edges"""
    
    # Main cloud shape
    num_bumps = 8
    for i in range(num_bumps):
        angle = 2 * math.pi * i / num_bumps
        bump_radius = radius * (0.8 + 0.3 * math.sin(3 * angle))
        bump_x = cx + bump_radius * math.cos(angle)
        bump_y = cy + bump_radius * math.sin(angle)
        
        if i == 0:
            ctx.move_to(bump_x, bump_y)
        else:
            ctx.line_to(bump_x, bump_y)
    
    ctx.close_path()
    
    # Fill white
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    
    # Outline
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Add small thought bubbles
    for i, (dx, dy, r) in enumerate([(30, 60, 8), (50, 80, 5), (65, 95, 3)]):
        ctx.arc(cx + dx, cy + dy, r, 0, 2*math.pi)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()
    
    # Add text
    draw_centered_text(ctx, cx, cy, radius*1.5, radius*1.5, text)

def create_jagged_bubble(ctx, cx, cy, width, height, text="ANGRY!"):
    """Create an angry/shouting bubble with jagged edges"""
    
    # Create jagged path
    points = []
    sides = 4  # rectangle-ish
    base_points = [
        (cx - width/2, cy - height/2),  # top-left
        (cx + width/2, cy - height/2),  # top-right
        (cx + width/2, cy + height/2),  # bottom-right
        (cx - width/2, cy + height/2)   # bottom-left
    ]
    
    for i in range(len(base_points)):
        start = base_points[i]
        end = base_points[(i + 1) % len(base_points)]
        
        # Add jagged points along each edge
        num_jags = 6
        for j in range(num_jags + 1):
            t = j / num_jags
            x = start[0] + t * (end[0] - start[0])
            y = start[1] + t * (end[1] - start[1])
            
            # Add random jag
            if j > 0 and j < num_jags:
                jag_size = 15
                if i % 2 == 0:  # horizontal edges
                    y += jag_size * (1 if i == 0 else -1) * (0.5 + 0.5 * math.sin(j * 2))
                else:  # vertical edges
                    x += jag_size * (1 if i == 1 else -1) * (0.5 + 0.5 * math.sin(j * 2))
            
            points.append((x, y))
    
    # Draw jagged shape
    ctx.move_to(*points[0])
    for point in points[1:]:
        ctx.line_to(*point)
    ctx.close_path()
    
    # Fill white
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    
    # Thick black outline
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(3)
    ctx.stroke()
    
    # Add text
    draw_centered_text(ctx, cx, cy, width, height, text, font_size=24, bold=True)

def draw_centered_text(ctx, cx, cy, width, height, text, font_size=16, bold=False):
    """Draw text centered in the given area using Pango"""
    
    layout = PangoCairo.create_layout(ctx)
    
    # Set font
    font_weight = Pango.Weight.BOLD if bold else Pango.Weight.NORMAL
    fontdesc = Pango.FontDescription(f"Sans {font_size}")
    fontdesc.set_weight(font_weight)
    layout.set_font_description(fontdesc)
    
    # Set text and wrapping
    layout.set_text(text, -1)
    layout.set_width(int(width * 0.8 * Pango.SCALE))  # 80% of bubble width
    layout.set_alignment(Pango.Alignment.CENTER)
    
    # Get text dimensions
    text_width, text_height = layout.get_pixel_size()
    
    # Position text at center
    text_x = cx - text_width / 2
    text_y = cy - text_height / 2
    
    # Draw text
    ctx.set_source_rgb(0, 0, 0)  # black text
    ctx.move_to(text_x, text_y)
    PangoCairo.show_layout(ctx, layout)

def create_manga_bubbles_demo():
    """Create a demo with various manga-style speech bubbles"""
    
    WIDTH, HEIGHT = 800, 600
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Light background
    ctx.set_source_rgb(0.95, 0.95, 0.95)
    ctx.paint()
    
    # Create different bubble types
    
    # 1. Normal speech bubble
    create_ellipse_bubble(ctx, 150, 120, 80, 60, "Hello there!", "bottom")
    
    # 2. Thought bubble
    create_cloud_bubble(ctx, 400, 120, 70, "I wonder...")
    
    # 3. Angry bubble
    create_jagged_bubble(ctx, 650, 120, 120, 80, "WHAT?!")
    
    # 4. Speech bubble with left tail
    create_ellipse_bubble(ctx, 150, 300, 90, 70, "Look over here!", "left")
    
    # 5. Large speech bubble
    create_ellipse_bubble(ctx, 450, 320, 120, 90, "This is a longer speech that wraps nicely inside the bubble!", "bottom")
    
    # 6. Another angry bubble
    create_jagged_bubble(ctx, 150, 480, 100, 70, "NO WAY!")
    
    # 7. Another thought bubble
    create_cloud_bubble(ctx, 450, 480, 80, "Hmm...")
    
    # Save the result
    surface.write_to_png("manga_bubbles_demo.png")
    print("✅ Manga bubbles demo saved as 'manga_bubbles_demo.png'")

if __name__ == "__main__":
    create_manga_bubbles_demo()