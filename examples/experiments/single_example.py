import cairo
import math
import random

def point_inside_circle(px, py, circle):
    """Check if a point is inside an ellipse/circle"""
    cx, cy = circle['x'], circle['y']
    rx, ry = circle['rx'], circle['ry']
    
    # Ellipse equation: ((x-cx)/rx)^2 + ((y-cy)/ry)^2 <= 1
    normalized_x = (px - cx) / rx
    normalized_y = (py - cy) / ry
    return (normalized_x * normalized_x + normalized_y * normalized_y) <= 1

def create_single_bubble_example():
    """Create one example of a speech bubble with crossing ovals"""
    
    # Create surface and context
    width, height = 400, 300
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    
    # White background
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    
    # Rectangle parameters
    cx, cy = 200, 150  # Center
    rect_width, rect_height = 180, 100
    half_width = rect_width / 2
    half_height = rect_height / 2
    
    # Draw base rectangle
    ctx.set_source_rgba(0.95, 0.95, 0.98, 1.0)
    ctx.rectangle(cx - half_width, cy - half_height, rect_width, rect_height)
    ctx.fill()
    
    # Create ovals that will cross inside
    ovals = []
    
    # Top oval - positioned to cross with side ovals
    top_oval = {
        'x': cx - 30,  # Offset to the left
        'y': cy - half_height - 25,  # Above rectangle
        'rx': 45,
        'ry': 35
    }
    ovals.append(top_oval)
    
    # Bottom oval
    bottom_oval = {
        'x': cx + 30,  # Offset to the right
        'y': cy + half_height + 25,  # Below rectangle
        'rx': 45,
        'ry': 35
    }
    ovals.append(bottom_oval)
    
    # Left oval - positioned to cross with top/bottom ovals INSIDE rectangle
    left_oval = {
        'x': cx - half_width - 25,  # Left of rectangle
        'y': cy - 20,  # Offset up
        'rx': 35,
        'ry': 45
    }
    ovals.append(left_oval)
    
    # Right oval
    right_oval = {
        'x': cx + half_width + 25,  # Right of rectangle
        'y': cy + 20,  # Offset down
        'rx': 35,
        'ry': 45
    }
    ovals.append(right_oval)
    
    # Draw all ovals with gradient
    for oval in ovals:
        ctx.save()
        ctx.translate(oval['x'], oval['y'])
        ctx.scale(oval['rx'], oval['ry'])
        
        # Create radial gradient
        gradient = cairo.RadialGradient(0, 0, 0, 0, 0, 1)
        gradient.add_color_stop_rgb(0, 1.0, 1.0, 1.0)      # White center
        gradient.add_color_stop_rgb(0.7, 0.95, 0.95, 0.98) # Light edge
        gradient.add_color_stop_rgb(1, 0.8, 0.8, 0.85)     # Darker border
        
        ctx.set_source(gradient)
        ctx.arc(0, 0, 1, 0, 2 * math.pi)
        ctx.fill()
        ctx.restore()
    
    # Emphasize oval borders inside rectangle
    ctx.set_source_rgba(0, 0, 0, 0.9)
    ctx.set_line_width(3.0)
    
    rect_left = cx - half_width
    rect_right = cx + half_width
    rect_top = cy - half_height
    rect_bottom = cy + half_height
    
    for oval in ovals:
        # Sample points around oval perimeter
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            px = oval['x'] + oval['rx'] * math.cos(rad)
            py = oval['y'] + oval['ry'] * math.sin(rad)
            
            # If point is inside rectangle, draw small emphasis
            if (px >= rect_left and px <= rect_right and 
                py >= rect_top and py <= rect_bottom):
                ctx.arc(px, py, 1.5, 0, 2 * math.pi)
                ctx.fill()
    
    # Draw rectangle border
    ctx.set_source_rgba(0, 0, 0, 0.7)
    ctx.set_line_width(2.0)
    ctx.rectangle(cx - half_width, cy - half_height, rect_width, rect_height)
    ctx.stroke()
    
    # Add text
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(20)
    ctx.set_source_rgb(0.2, 0.2, 0.4)
    
    text = "CROSSING!"
    text_extents = ctx.text_extents(text)
    text_x = cx - text_extents.width / 2
    text_y = cy + text_extents.height / 2
    
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)
    
    # Save the image
    surface.write_to_png("single_bubble_example.png")
    print("✅ Single bubble example saved as 'single_bubble_example.png'")

if __name__ == "__main__":
    create_single_bubble_example()