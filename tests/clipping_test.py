import cairo
import math
import random

def create_clipped_circles_square(ctx, cx, cy, base_size, text="CLIPPED!", circle_style="varied", num_circles_per_side=5):
    """Create a square with circles clipped to square boundaries"""
    
    # Calculate base square
    half_size = base_size / 2
    
    # Generate overlapping circles for each side
    all_circles = generate_side_circles(cx, cy, half_size, circle_style, num_circles_per_side)
    
    # Draw the main square FIRST
    draw_base_square(ctx, cx, cy, base_size)
    
    # CRITICAL: Set clipping region to EXACTLY the square area
    ctx.save()
    ctx.rectangle(cx - half_size, cy - half_size, base_size, base_size)
    ctx.clip()
    
    # Draw all circles - only parts inside square will be visible
    for circle in all_circles:
        draw_single_circle_clipped(ctx, circle)
    
    # Restore clipping
    ctx.restore()
    
    # Draw square outline OVER the clipped circles for clean edges
    draw_square_outline_only(ctx, cx, cy, base_size)
    
    # Add text
    draw_overlap_text(ctx, cx, cy, text)

def generate_side_circles(cx, cy, half_size, style, num_per_side):
    """Generate circles that DEFINITELY extend outside the square"""
    
    all_circles = []
    
    # Make circles that clearly extend beyond square boundaries
    for i in range(num_per_side):
        # Top side circles - extend upward
        circle_x = cx + (i - num_per_side/2) * (half_size * 0.4)
        circle_y = cy - half_size + 10  # Positioned to cross top border
        radius = half_size * 0.4  # Large enough to extend outside
        
        all_circles.append({
            'x': circle_x,
            'y': circle_y,
            'rx': radius,
            'ry': radius,
            'side': 'top'
        })
        
        # Right side circles - extend rightward
        circle_x = cx + half_size - 10  # Positioned to cross right border
        circle_y = cy + (i - num_per_side/2) * (half_size * 0.4)
        
        all_circles.append({
            'x': circle_x,
            'y': circle_y,
            'rx': radius,
            'ry': radius,
            'side': 'right'
        })
        
        # Bottom side circles - extend downward
        circle_x = cx + (i - num_per_side/2) * (half_size * 0.4)
        circle_y = cy + half_size - 10  # Positioned to cross bottom border
        
        all_circles.append({
            'x': circle_x,
            'y': circle_y,
            'rx': radius,
            'ry': radius,
            'side': 'bottom'
        })
        
        # Left side circles - extend leftward
        circle_x = cx - half_size + 10  # Positioned to cross left border
        circle_y = cy + (i - num_per_side/2) * (half_size * 0.4)
        
        all_circles.append({
            'x': circle_x,
            'y': circle_y,
            'rx': radius,
            'ry': radius,
            'side': 'left'
        })
    
    return all_circles

def draw_single_circle_clipped(ctx, circle):
    """Draw a single circle that will be clipped"""
    
    # Save current state
    ctx.save()
    
    # Move to circle center and create ellipse
    ctx.translate(circle['x'], circle['y'])
    ctx.scale(circle['rx'], circle['ry'])
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    
    # Restore for gradient calculation
    ctx.restore()
    
    # Create gradient for this circle
    gradient = cairo.RadialGradient(
        circle['x'], circle['y'], 0,
        circle['x'], circle['y'], max(circle['rx'], circle['ry'])
    )
    
    # Different bright colors to make clipping obvious
    if circle['side'] == 'top':
        gradient.add_color_stop_rgb(0, 1.0, 0.8, 0.8)   # Bright red
        gradient.add_color_stop_rgb(1, 0.8, 0.4, 0.4)   # Dark red
    elif circle['side'] == 'right':
        gradient.add_color_stop_rgb(0, 0.8, 1.0, 0.8)   # Bright green
        gradient.add_color_stop_rgb(1, 0.4, 0.8, 0.4)   # Dark green
    elif circle['side'] == 'bottom':
        gradient.add_color_stop_rgb(0, 0.8, 0.8, 1.0)   # Bright blue
        gradient.add_color_stop_rgb(1, 0.4, 0.4, 0.8)   # Dark blue
    else:  # left
        gradient.add_color_stop_rgb(0, 1.0, 1.0, 0.8)   # Bright yellow
        gradient.add_color_stop_rgb(1, 0.8, 0.8, 0.4)   # Dark yellow
    
    # Fill circle (will be clipped)
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Circle outline (will be clipped)
    ctx.set_source_rgba(0, 0, 0, 0.5)
    ctx.set_line_width(2.0)
    ctx.stroke()

def draw_base_square(ctx, cx, cy, size):
    """Draw the base square"""
    
    half_size = size / 2
    
    # Square path
    ctx.rectangle(cx - half_size, cy - half_size, size, size)
    
    # Light square fill
    ctx.set_source_rgba(1.0, 1.0, 1.0, 0.9)  # Almost white
    ctx.fill()

def draw_square_outline_only(ctx, cx, cy, size):
    """Draw just the square outline"""
    
    half_size = size / 2
    
    # Square outline
    ctx.rectangle(cx - half_size, cy - half_size, size, size)
    ctx.set_source_rgba(0, 0, 0, 0.8)
    ctx.set_line_width(3.0)
    ctx.stroke()

def draw_overlap_text(ctx, cx, cy, text):
    """Draw text in center"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(14)
    
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    text_x = cx - text_width / 2
    text_y = cy + text_height / 2
    
    # Text shadow
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.move_to(text_x + 1, text_y + 1)
    ctx.show_text(text)
    
    # Main text
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_clipping_test_demo():
    """Create demo showing clear clipping effect"""
    
    random.seed(555)
    
    WIDTH, HEIGHT = 800, 600
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(0.9, 0.9, 0.9)
    ctx.paint()
    
    # Test different clipping scenarios
    create_clipped_circles_square(ctx, 150, 150, 120, "CLIPPED 1!", "varied", 3)
    create_clipped_circles_square(ctx, 350, 150, 120, "CLIPPED 2!", "varied", 4)
    create_clipped_circles_square(ctx, 550, 150, 120, "CLIPPED 3!", "varied", 5)
    
    create_clipped_circles_square(ctx, 200, 350, 140, "BIG CLIP!", "varied", 4)
    create_clipped_circles_square(ctx, 450, 350, 140, "HUGE CLIP!", "varied", 6)
    
    create_clipped_circles_square(ctx, 300, 500, 160, "MEGA CLIP!", "varied", 7)
    
    # Title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(24)
    ctx.set_source_rgb(0.2, 0.2, 0.4)
    ctx.move_to(250, 50)
    ctx.show_text("CLIPPING TEST - CIRCLES CUT AT SQUARE EDGES")
    
    surface.write_to_png("clipping_test.png")
    print("✅ Clipping test saved as 'clipping_test.png'")

if __name__ == "__main__":
    create_clipping_test_demo()
    print("✂️ Created clipping test! Circles should be cut off at square boundaries! 🔵⬜✨")