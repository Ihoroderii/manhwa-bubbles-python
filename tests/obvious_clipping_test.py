import cairo
import math

def create_obvious_clipping_test():
    """Create a test where clipping is absolutely obvious"""
    
    WIDTH, HEIGHT = 400, 400
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(0.9, 0.9, 0.9)
    ctx.paint()
    
    # Square center and size
    cx, cy = 200, 200
    square_size = 160
    half_size = square_size / 2
    
    # Draw background square (light)
    ctx.rectangle(cx - half_size, cy - half_size, square_size, square_size)
    ctx.set_source_rgb(1.0, 1.0, 1.0)
    ctx.fill()
    
    # Create circles that DEFINITELY extend outside
    circles = [
        # Top circle - extends way above square
        {'x': cx, 'y': cy - half_size + 20, 'r': 60, 'color': (1, 0, 0)},  # Red
        # Right circle - extends way right
        {'x': cx + half_size - 20, 'y': cy, 'r': 60, 'color': (0, 1, 0)},  # Green
        # Bottom circle - extends way below
        {'x': cx, 'y': cy + half_size - 20, 'r': 60, 'color': (0, 0, 1)},  # Blue
        # Left circle - extends way left
        {'x': cx - half_size + 20, 'y': cy, 'r': 60, 'color': (1, 1, 0)},  # Yellow
    ]
    
    print("BEFORE CLIPPING:")
    print(f"Square bounds: {cx - half_size} to {cx + half_size} (x), {cy - half_size} to {cy + half_size} (y)")
    for i, circle in enumerate(circles):
        print(f"Circle {i}: center=({circle['x']}, {circle['y']}), radius={circle['r']}")
        print(f"  Extends from {circle['x'] - circle['r']} to {circle['x'] + circle['r']} (x)")
        print(f"  Extends from {circle['y'] - circle['r']} to {circle['y'] + circle['r']} (y)")
    
    # START CLIPPING
    ctx.save()
    ctx.rectangle(cx - half_size, cy - half_size, square_size, square_size)
    ctx.clip()
    
    # Draw circles (should be clipped)
    for circle in circles:
        ctx.arc(circle['x'], circle['y'], circle['r'], 0, 2 * math.pi)
        ctx.set_source_rgb(*circle['color'])
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(2)
        ctx.stroke()
    
    # END CLIPPING
    ctx.restore()
    
    # Draw square outline on top
    ctx.rectangle(cx - half_size, cy - half_size, square_size, square_size)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(4)
    ctx.stroke()
    
    # Add text
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(16)
    ctx.set_source_rgb(0, 0, 0)
    text = "CLIPPING TEST"
    text_extents = ctx.text_extents(text)
    ctx.move_to(cx - text_extents.width/2, cy + text_extents.height/2)
    ctx.show_text(text)
    
    surface.write_to_png("obvious_clipping_test.png")
    print("✅ Obvious clipping test saved as 'obvious_clipping_test.png'")
    print("If clipping works, you should see circles cut off at square edges!")

def create_no_clipping_comparison():
    """Create the same test WITHOUT clipping for comparison"""
    
    WIDTH, HEIGHT = 400, 400
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(0.9, 0.9, 0.9)
    ctx.paint()
    
    # Square center and size
    cx, cy = 200, 200
    square_size = 160
    half_size = square_size / 2
    
    # Draw background square (light)
    ctx.rectangle(cx - half_size, cy - half_size, square_size, square_size)
    ctx.set_source_rgb(1.0, 1.0, 1.0)
    ctx.fill()
    
    # Create circles that extend outside
    circles = [
        # Top circle - extends way above square
        {'x': cx, 'y': cy - half_size + 20, 'r': 60, 'color': (1, 0, 0)},  # Red
        # Right circle - extends way right
        {'x': cx + half_size - 20, 'y': cy, 'r': 60, 'color': (0, 1, 0)},  # Green
        # Bottom circle - extends way below
        {'x': cx, 'y': cy + half_size - 20, 'r': 60, 'color': (0, 0, 1)},  # Blue
        # Left circle - extends way left
        {'x': cx - half_size + 20, 'y': cy, 'r': 60, 'color': (1, 1, 0)},  # Yellow
    ]
    
    # Draw circles WITHOUT clipping
    for circle in circles:
        ctx.arc(circle['x'], circle['y'], circle['r'], 0, 2 * math.pi)
        ctx.set_source_rgb(*circle['color'])
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(2)
        ctx.stroke()
    
    # Draw square outline on top
    ctx.rectangle(cx - half_size, cy - half_size, square_size, square_size)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(4)
    ctx.stroke()
    
    # Add text
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(16)
    ctx.set_source_rgb(0, 0, 0)
    text = "NO CLIPPING"
    text_extents = ctx.text_extents(text)
    ctx.move_to(cx - text_extents.width/2, cy + text_extents.height/2)
    ctx.show_text(text)
    
    surface.write_to_png("no_clipping_comparison.png")
    print("✅ No clipping comparison saved as 'no_clipping_comparison.png'")
    print("This shows how it looks WITHOUT clipping - circles extend outside!")

if __name__ == "__main__":
    create_obvious_clipping_test()
    create_no_clipping_comparison()
    print("\n🔍 Compare the two images:")
    print("- obvious_clipping_test.png (should show clipped circles)")
    print("- no_clipping_comparison.png (shows unclipped circles)")
    print("If they look the same, then clipping is not working!")