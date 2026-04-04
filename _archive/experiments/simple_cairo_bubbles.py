import cairo
import math

def create_simple_speech_bubble():
    """Create a simple speech bubble with tail"""
    
    WIDTH, HEIGHT = 300, 200
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    # Bubble parameters
    cx, cy = 150, 80  # center
    rx, ry = 100, 50  # radii
    
    # Draw main ellipse
    ctx.arc(cx, cy, rx, 0, 2 * math.pi)
    ctx.scale(1, ry/rx)  # Make it elliptical
    
    # Fill white
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    
    # Black outline
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Reset transformation
    ctx.identity_matrix()
    
    # Draw tail manually
    ctx.move_to(cx - 15, cy + ry)
    ctx.line_to(cx - 30, cy + ry + 40)  # tail tip
    ctx.line_to(cx + 15, cy + ry)
    ctx.close_path()
    
    # Fill tail white
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    
    # Outline tail
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Add simple text
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(14)
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(cx - 30, cy)
    ctx.show_text("Hello!")
    
    surface.write_to_png("simple_bubble.png")
    print("✅ Simple speech bubble saved as 'simple_bubble.png'")

def create_thought_bubble():
    """Create a thought bubble with small circles"""
    
    WIDTH, HEIGHT = 300, 200
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    # Main thought bubble (cloud-like)
    cx, cy = 150, 70
    radius = 60
    
    # Create cloud effect with multiple circles
    circles = [
        (cx, cy, radius),
        (cx - 30, cy - 20, radius * 0.7),
        (cx + 25, cy - 25, radius * 0.6),
        (cx - 35, cy + 15, radius * 0.5),
        (cx + 30, cy + 20, radius * 0.55)
    ]
    
    for x, y, r in circles:
        ctx.arc(x, y, r, 0, 2 * math.pi)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(2)
        ctx.stroke()
    
    # Small thought circles leading to bubble
    thought_circles = [(cx + 40, cy + 60, 8), (cx + 55, cy + 80, 5), (cx + 65, cy + 95, 3)]
    for x, y, r in thought_circles:
        ctx.arc(x, y, r, 0, 2 * math.pi)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1)
        ctx.stroke()
    
    # Add text
    ctx.select_font_face("Arial", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(12)
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(cx - 25, cy)
    ctx.show_text("Thinking...")
    
    surface.write_to_png("thought_bubble.png")
    print("✅ Thought bubble saved as 'thought_bubble.png'")

def create_action_bubble():
    """Create an action/explosion bubble with jagged edges"""
    
    WIDTH, HEIGHT = 300, 200
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    # Jagged bubble center
    cx, cy = 150, 100
    
    # Create star/explosion shape
    points = []
    num_points = 12
    outer_radius = 80
    inner_radius = 50
    
    for i in range(num_points * 2):
        angle = math.pi * i / num_points
        if i % 2 == 0:
            radius = outer_radius
        else:
            radius = inner_radius
        
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    
    # Draw the shape
    ctx.move_to(*points[0])
    for point in points[1:]:
        ctx.line_to(*point)
    ctx.close_path()
    
    # Fill yellow for action effect
    ctx.set_source_rgb(1, 1, 0.8)
    ctx.fill_preserve()
    
    # Thick black outline
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(3)
    ctx.stroke()
    
    # Add bold text
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(16)
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(cx - 25, cy)
    ctx.show_text("POW!")
    
    surface.write_to_png("action_bubble.png")
    print("✅ Action bubble saved as 'action_bubble.png'")

if __name__ == "__main__":
    create_simple_speech_bubble()
    create_thought_bubble()
    create_action_bubble()
    print("\n🎨 All bubble examples created!")