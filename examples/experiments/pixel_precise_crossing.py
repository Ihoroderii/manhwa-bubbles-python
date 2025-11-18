import cairo
import math
import random

def create_overlapping_circles_square(ctx, cx, cy, base_size, text="OVERLAP!", circle_style="varied", num_circles_per_side=5):
    """Create a square with overlapping circles/ovals on all sides"""
    
    # Calculate base square
    half_size = base_size / 2
    
    # Generate overlapping circles for each side
    all_circles = generate_side_circles(cx, cy, half_size, circle_style, num_circles_per_side)
    
    # Draw the main square FIRST (will be under the circles)
    draw_base_square(ctx, cx, cy, base_size)
    
    # Draw all circles ABOVE the square (they will overlap and cover parts of square)
    draw_overlapping_circles(ctx, all_circles, cx, cy, base_size)
    
    # Find and emphasize only the pixels where circles cross square borders
    emphasize_border_crossing_pixels(ctx, all_circles, cx, cy, half_size)
    
    # Add text
    draw_overlap_text(ctx, cx, cy, text)

def emphasize_border_crossing_pixels(ctx, all_circles, cx, cy, half_size):
    """Find and emphasize only the pixels where circles cross the square border"""
    
    # Square boundaries
    square_left = cx - half_size
    square_right = cx + half_size
    square_top = cy - half_size
    square_bottom = cy + half_size
    
    # For each circle, find pixels that cross the square border
    for circle in all_circles:
        crossing_pixels = find_border_crossing_pixels(circle, square_left, square_right, square_top, square_bottom)
        
        # Draw emphasis only on crossing pixels
        draw_crossing_pixel_emphasis(ctx, crossing_pixels)

def find_border_crossing_pixels(circle, square_left, square_right, square_top, square_bottom):
    """Find all pixels of a circle that cross the square border"""
    
    crossing_pixels = []
    
    # Get circle parameters
    cx, cy = circle['x'], circle['y']
    rx, ry = circle['rx'], circle['ry']
    
    # Sample points around the circle perimeter with high resolution
    num_samples = int(max(rx, ry) * 8)  # High resolution sampling
    
    for i in range(num_samples):
        angle = (2 * math.pi * i) / num_samples
        
        # Calculate point on circle perimeter
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

def generate_side_circles(cx, cy, half_size, style, num_per_side):
    """Generate circles/ovals for each side of the square"""
    
    all_circles = []
    
    # Define the four sides
    sides = [
        ("top", cx - half_size, cy - half_size, cx + half_size, cy - half_size),
        ("right", cx + half_size, cy - half_size, cx + half_size, cy + half_size),
        ("bottom", cx + half_size, cy + half_size, cx - half_size, cy + half_size),
        ("left", cx - half_size, cy + half_size, cx - half_size, cy - half_size)
    ]
    
    circle_id = 0
    for side_name, start_x, start_y, end_x, end_y in sides:
        side_circles = generate_circles_for_side(
            start_x, start_y, end_x, end_y, side_name, style, num_per_side, half_size, circle_id
        )
        all_circles.extend(side_circles)
        circle_id += len(side_circles)
    
    return all_circles

def generate_circles_for_side(start_x, start_y, end_x, end_y, side_name, style, num_circles, base_half_size, start_id):
    """Generate circles for a specific side of the square"""
    
    circles = []
    side_length = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
    
    for i in range(num_circles):
        # Position along the side
        t = (i + 0.5) / num_circles
        base_x = start_x + t * (end_x - start_x)
        base_y = start_y + t * (end_y - start_y)
        
        # Add some randomness
        if style == "varied":
            offset_range = base_half_size * 0.3
            offset_x = random.uniform(-offset_range, offset_range)
            offset_y = random.uniform(-offset_range, offset_range)
        else:
            offset_x = offset_y = 0
        
        circle_x = base_x + offset_x
        circle_y = base_y + offset_y
        
        # Size based on style
        if style == "uniform":
            radius = base_half_size * 0.25
            rx = ry = radius
        elif style == "ovals":
            if side_name in ["top", "bottom"]:
                rx = base_half_size * random.uniform(0.3, 0.5)
                ry = base_half_size * random.uniform(0.15, 0.25)
            else:
                rx = base_half_size * random.uniform(0.15, 0.25)
                ry = base_half_size * random.uniform(0.3, 0.5)
        else:  # varied
            base_radius = base_half_size * random.uniform(0.2, 0.4)
            rx = base_radius * random.uniform(0.8, 1.2)
            ry = base_radius * random.uniform(0.8, 1.2)
        
        circles.append({
            'x': circle_x,
            'y': circle_y,
            'rx': rx,
            'ry': ry,
            'side': side_name,
            'id': start_id + i
        })
    
    return circles

def draw_overlapping_circles(ctx, all_circles, cx, cy, base_size):
    """Draw all circles with proper overlapping order"""
    
    # Sort circles by distance from center for proper overlap
    circles_with_distance = []
    for circle in all_circles:
        distance = math.sqrt((circle['x'] - cx)**2 + (circle['y'] - cy)**2)
        circles_with_distance.append((distance, circle))
    
    circles_with_distance.sort(key=lambda x: x[0], reverse=True)
    
    # Draw circles from farthest to nearest for proper overlapping
    for distance, circle in circles_with_distance:
        draw_single_circle(ctx, circle, cx, cy, base_size)

def draw_single_circle(ctx, circle, cx, cy, base_size):
    """Draw a single circle/oval with gradient"""
    
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
    
    # Light circle outline (the border crossing emphasis will be separate)
    ctx.set_source_rgba(0, 0, 0, 0.2)
    ctx.set_line_width(1.0)
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
    
    # Light square outline (border crossing emphasis will be separate)
    ctx.set_source_rgba(0, 0, 0, 0.3)
    ctx.set_line_width(1.5)
    ctx.stroke()

def draw_overlap_text(ctx, cx, cy, text):
    """Draw text in center of overlapping area"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(12)
    
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

def create_pixel_precise_demo():
    """Create demo with pixel-precise border crossing emphasis"""
    
    random.seed(777)
    
    WIDTH, HEIGHT = 1200, 800
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(0.96, 0.96, 0.98)
    ctx.paint()
    
    # Row 1: Different circle styles with pixel-precise emphasis
    create_overlapping_circles_square(ctx, 150, 140, 100, "VARIED!", "varied", 4)
    create_overlapping_circles_square(ctx, 350, 140, 100, "UNIFORM!", "uniform", 5) 
    create_overlapping_circles_square(ctx, 550, 140, 100, "OVALS!", "ovals", 4)
    create_overlapping_circles_square(ctx, 750, 140, 100, "BUBBLES!", "varied", 6)
    create_overlapping_circles_square(ctx, 950, 140, 100, "DENSE!", "varied", 8)
    
    # Row 2: Larger versions
    create_overlapping_circles_square(ctx, 200, 320, 130, "BIG VARIED!", "varied", 5)
    create_overlapping_circles_square(ctx, 450, 320, 130, "BIG OVALS!", "ovals", 4)
    create_overlapping_circles_square(ctx, 700, 320, 130, "BIG BUBBLES!", "varied", 7)
    create_overlapping_circles_square(ctx, 950, 320, 130, "BIG DENSE!", "varied", 9)
    
    # Row 3: Different densities
    create_overlapping_circles_square(ctx, 150, 520, 120, "FEW!", "varied", 3)
    create_overlapping_circles_square(ctx, 350, 520, 120, "SOME!", "varied", 5)
    create_overlapping_circles_square(ctx, 550, 520, 120, "MANY!", "varied", 7)
    create_overlapping_circles_square(ctx, 750, 520, 120, "LOTS!", "varied", 9)
    create_overlapping_circles_square(ctx, 950, 520, 120, "MEGA!", "varied", 12)
    
    # Row 4: Extra large examples
    create_overlapping_circles_square(ctx, 200, 680, 150, "HUGE VARIED!", "varied", 6)
    create_overlapping_circles_square(ctx, 500, 680, 150, "HUGE OVALS!", "ovals", 5)
    create_overlapping_circles_square(ctx, 800, 680, 150, "HUGE BUBBLES!", "varied", 8)
    
    # Title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(28)
    ctx.set_source_rgb(0.2, 0.2, 0.4)
    ctx.move_to(350, 50)
    ctx.show_text("PIXEL-PRECISE BORDER CROSSING")
    
    # Subtitle
    ctx.set_font_size(16)
    ctx.move_to(450, 80)
    ctx.show_text("Only Pixels That Cross Square Borders Are Emphasized")
    
    surface.write_to_png("pixel_precise_crossing.png")
    print("✅ Pixel-precise border crossing saved as 'pixel_precise_crossing.png'")

if __name__ == "__main__":
    create_pixel_precise_demo()
    print("🎯 Created pixel-precise border crossing emphasis! Only crossing pixels highlighted! ⚫✨")