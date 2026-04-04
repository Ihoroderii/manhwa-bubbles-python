import cairo
import math
import random

def create_organic_bubble(ctx, cx, cy, base_radius, text="Hello!", tail_position="bottom", bubble_style="smooth"):
    """Create an organic, hand-drawn style speech bubble with unique shape"""
    
    # Generate unique organic shape
    points = []
    num_points = random.randint(12, 20)  # Variable number of control points
    
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        
        # Create organic variations
        radius_variation = random.uniform(0.7, 1.3)
        angle_offset = random.uniform(-0.3, 0.3)
        
        # Add some smoothness patterns
        if bubble_style == "wavy":
            radius_variation *= (1 + 0.3 * math.sin(angle * 3))
        elif bubble_style == "bumpy":
            radius_variation *= (1 + 0.2 * math.sin(angle * 5) + 0.1 * math.sin(angle * 8))
        elif bubble_style == "irregular":
            radius_variation *= (1 + 0.4 * math.sin(angle * 2.3) * math.cos(angle * 1.7))
        
        radius = base_radius * radius_variation
        actual_angle = angle + angle_offset
        
        x = cx + radius * math.cos(actual_angle)
        y = cy + radius * math.sin(actual_angle)
        points.append((x, y))
    
    # Create smooth curve through points using Catmull-Rom splines
    draw_smooth_curve(ctx, points)
    
    # Fill bubble
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    
    # Outline with variable width
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(random.uniform(1.5, 3.0))
    ctx.stroke()
    
    # Add organic tail
    draw_organic_tail(ctx, cx, cy, base_radius, tail_position)
    
    # Add text
    draw_text(ctx, cx, cy, text)

def draw_smooth_curve(ctx, points):
    """Draw a smooth curve through points using Bézier curves"""
    if len(points) < 3:
        return
    
    # Start the path
    ctx.move_to(*points[0])
    
    # Create smooth curves between points
    for i in range(len(points)):
        current = points[i]
        next_point = points[(i + 1) % len(points)]
        next_next = points[(i + 2) % len(points)]
        
        # Calculate control points for smooth curve
        cp1_x = current[0] + (next_point[0] - points[i-1][0]) * 0.2
        cp1_y = current[1] + (next_point[1] - points[i-1][1]) * 0.2
        cp2_x = next_point[0] - (next_next[0] - current[0]) * 0.2
        cp2_y = next_point[1] - (next_next[1] - current[1]) * 0.2
        
        ctx.curve_to(cp1_x, cp1_y, cp2_x, cp2_y, next_point[0], next_point[1])
    
    ctx.close_path()

def draw_organic_tail(ctx, cx, cy, radius, position="bottom"):
    """Draw an organic, curved tail"""
    
    # Tail parameters with randomness
    tail_length = radius * random.uniform(0.8, 1.2)
    tail_width = radius * random.uniform(0.15, 0.25)
    curve_intensity = random.uniform(0.3, 0.7)
    
    if position == "bottom":
        # Attachment points on bubble
        attach_left = (cx - tail_width, cy + radius * 0.7)
        attach_right = (cx + tail_width, cy + radius * 0.7)
        
        # Tail tip with slight randomness
        tip_x = cx + random.uniform(-tail_width/2, tail_width/2)
        tip_y = cy + radius + tail_length
        tail_tip = (tip_x, tip_y)
        
        # Create curved tail using Bézier curves
        ctx.move_to(*attach_left)
        
        # Left curve
        cp1_x = attach_left[0] - tail_width * curve_intensity
        cp1_y = attach_left[1] + tail_length * 0.3
        cp2_x = tail_tip[0] - tail_width * 0.3
        cp2_y = tail_tip[1] - tail_length * 0.2
        ctx.curve_to(cp1_x, cp1_y, cp2_x, cp2_y, *tail_tip)
        
        # Right curve
        cp3_x = tail_tip[0] + tail_width * 0.3
        cp3_y = tail_tip[1] - tail_length * 0.2
        cp4_x = attach_right[0] + tail_width * curve_intensity
        cp4_y = attach_right[1] + tail_length * 0.3
        ctx.curve_to(cp3_x, cp3_y, cp4_x, cp4_y, *attach_right)
        
    elif position == "left":
        attach_top = (cx - radius * 0.7, cy - tail_width)
        attach_bottom = (cx - radius * 0.7, cy + tail_width)
        
        tip_x = cx - radius - tail_length
        tip_y = cy + random.uniform(-tail_width/2, tail_width/2)
        tail_tip = (tip_x, tip_y)
        
        ctx.move_to(*attach_top)
        
        # Top curve
        cp1_x = attach_top[0] - tail_length * 0.3
        cp1_y = attach_top[1] - tail_width * curve_intensity
        cp2_x = tail_tip[0] + tail_length * 0.2
        cp2_y = tail_tip[1] - tail_width * 0.3
        ctx.curve_to(cp1_x, cp1_y, cp2_x, cp2_y, *tail_tip)
        
        # Bottom curve
        cp3_x = tail_tip[0] + tail_length * 0.2
        cp3_y = tail_tip[1] + tail_width * 0.3
        cp4_x = attach_bottom[0] - tail_length * 0.3
        cp4_y = attach_bottom[1] + tail_width * curve_intensity
        ctx.curve_to(cp3_x, cp3_y, cp4_x, cp4_y, *attach_bottom)
    
    ctx.close_path()
    
    # Fill and stroke tail
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(random.uniform(1.5, 2.5))
    ctx.stroke()

def create_cloud_thought_bubble(ctx, cx, cy, base_radius, text="Thinking..."):
    """Create a more organic cloud thought bubble"""
    
    # Main cloud with multiple organic bumps
    num_bumps = random.randint(6, 10)
    cloud_points = []
    
    for i in range(num_bumps):
        angle = 2 * math.pi * i / num_bumps
        
        # Create varied bump sizes
        bump_size = random.uniform(0.6, 1.4)
        bump_radius = base_radius * bump_size
        
        # Add some wobble
        angle_wobble = random.uniform(-0.4, 0.4)
        radius_wobble = random.uniform(0.8, 1.2)
        
        actual_angle = angle + angle_wobble
        actual_radius = bump_radius * radius_wobble
        
        x = cx + actual_radius * math.cos(actual_angle)
        y = cy + actual_radius * math.sin(actual_angle)
        cloud_points.append((x, y))
    
    # Draw smooth cloud shape
    draw_smooth_curve(ctx, cloud_points)
    
    # Fill and stroke
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()
    
    # Add organic thought trail
    trail_bubbles = []
    for i in range(4):
        bubble_radius = base_radius * (0.3 - i * 0.05) * random.uniform(0.8, 1.2)
        bubble_x = cx + (i + 1) * 25 + random.uniform(-8, 8)
        bubble_y = cy + base_radius + (i + 1) * 20 + random.uniform(-5, 5)
        trail_bubbles.append((bubble_x, bubble_y, bubble_radius))
    
    for x, y, r in trail_bubbles:
        # Make each small bubble slightly organic too
        small_points = []
        for j in range(8):
            angle = 2 * math.pi * j / 8
            radius_var = r * random.uniform(0.9, 1.1)
            px = x + radius_var * math.cos(angle)
            py = y + radius_var * math.sin(angle)
            small_points.append((px, py))
        
        draw_smooth_curve(ctx, small_points)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1)
        ctx.stroke()
    
    # Add text
    draw_text(ctx, cx, cy, text, italic=True)

def draw_text(ctx, cx, cy, text, italic=False):
    """Draw text centered in the bubble"""
    
    slant = cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL
    ctx.select_font_face("Arial", slant, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(14)
    
    # Get text dimensions
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    # Center the text
    text_x = cx - text_width / 2
    text_y = cy + text_height / 2
    
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_unique_bubbles_demo():
    """Create a demo with uniquely shaped organic bubbles"""
    
    # Set random seed for reproducible but varied results
    random.seed(42)
    
    WIDTH, HEIGHT = 900, 700
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Soft background
    ctx.set_source_rgb(0.98, 0.98, 0.95)
    ctx.paint()
    
    # Create various organic bubbles with different styles
    bubbles = [
        # (cx, cy, radius, text, tail_pos, style)
        (150, 120, 60, "Hello there!", "bottom", "smooth"),
        (400, 120, 65, "How are you?", "left", "wavy"),
        (650, 120, 70, "Great day!", "bottom", "bumpy"),
        (150, 300, 75, "This is amazing!", "left", "irregular"),
        (400, 300, 80, "I love this!", "bottom", "wavy"),
        (650, 300, 65, "So cool!", "left", "smooth"),
        (150, 480, 70, "Fantastic!", "bottom", "bumpy"),
        (650, 480, 75, "Wonderful!", "bottom", "irregular"),
    ]
    
    for cx, cy, radius, text, tail_pos, style in bubbles:
        # Reset random seed slightly for each bubble to get variation
        random.seed(42 + cx + cy)
        create_organic_bubble(ctx, cx, cy, radius, text, tail_pos, style)
    
    # Add some thought bubbles
    random.seed(100)
    create_cloud_thought_bubble(ctx, 400, 480, 60, "Hmm...")
    
    # Save result
    surface.write_to_png("organic_manga_bubbles.png")
    print("✅ Organic manga bubbles saved as 'organic_manga_bubbles.png'")

if __name__ == "__main__":
    create_unique_bubbles_demo()
    print("🎨 Each bubble now has a unique, smooth organic shape!")