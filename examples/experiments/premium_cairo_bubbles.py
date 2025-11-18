import cairo
import math
import random

def create_hand_drawn_bubble(ctx, cx, cy, width, height, text="Hello!", style="natural"):
    """Create a hand-drawn style bubble with natural imperfections"""
    
    # Generate control points for a natural bubble shape
    points = generate_natural_bubble_points(cx, cy, width, height, style)
    
    # Draw the bubble using smooth curves
    draw_natural_curve(ctx, points)
    
    # Fill with slight transparency for natural look
    ctx.set_source_rgba(1, 1, 1, 0.95)
    ctx.fill_preserve()
    
    # Draw outline with slight variations
    draw_natural_stroke(ctx, points)
    
    # Add organic tail
    add_natural_tail(ctx, cx, cy, width, height)
    
    # Add hand-lettered style text
    draw_natural_text(ctx, cx, cy, text)

def generate_natural_bubble_points(cx, cy, width, height, style):
    """Generate points for a natural-looking bubble outline"""
    
    points = []
    num_segments = random.randint(16, 24)
    
    for i in range(num_segments):
        # Base ellipse angle
        angle = 2 * math.pi * i / num_segments
        
        # Base position on ellipse
        base_x = cx + (width/2) * math.cos(angle)
        base_y = cy + (height/2) * math.sin(angle)
        
        # Add natural variations based on style
        if style == "natural":
            # Subtle hand-drawn wobble
            wobble_x = random.uniform(-width*0.08, width*0.08)
            wobble_y = random.uniform(-height*0.08, height*0.08)
            
        elif style == "quirky":
            # More pronounced variations
            wobble_x = random.uniform(-width*0.15, width*0.15) * math.sin(angle * 3)
            wobble_y = random.uniform(-height*0.15, height*0.15) * math.cos(angle * 2)
            
        elif style == "flowing":
            # Smooth flowing variations
            flow_factor = 0.1 + 0.05 * math.sin(angle * 4)
            wobble_x = width * flow_factor * math.sin(angle * 2.5)
            wobble_y = height * flow_factor * math.cos(angle * 1.8)
            
        elif style == "organic":
            # Complex organic shape
            organic_r = 1 + 0.2 * math.sin(angle * 3) + 0.1 * math.cos(angle * 7)
            organic_angle = angle + 0.1 * math.sin(angle * 5)
            base_x = cx + (width/2) * organic_r * math.cos(organic_angle)
            base_y = cy + (height/2) * organic_r * math.sin(organic_angle)
            wobble_x = random.uniform(-width*0.05, width*0.05)
            wobble_y = random.uniform(-height*0.05, height*0.05)
        
        final_x = base_x + wobble_x
        final_y = base_y + wobble_y
        points.append((final_x, final_y))
    
    return points

def draw_natural_curve(ctx, points):
    """Draw a smooth, natural curve through the points"""
    
    if len(points) < 3:
        return
    
    ctx.move_to(*points[0])
    
    # Use Catmull-Rom spline for smooth, natural curves
    for i in range(len(points)):
        p0 = points[i-2] if i >= 2 else points[-2]
        p1 = points[i-1] if i >= 1 else points[-1] 
        p2 = points[i]
        p3 = points[(i+1) % len(points)]
        
        # Calculate control points for smooth curve
        tension = random.uniform(0.3, 0.7)  # Varying tension for naturalness
        
        cp1_x = p1[0] + (p2[0] - p0[0]) * tension / 6
        cp1_y = p1[1] + (p2[1] - p0[1]) * tension / 6
        cp2_x = p2[0] - (p3[0] - p1[0]) * tension / 6  
        cp2_y = p2[1] - (p3[1] - p1[1]) * tension / 6
        
        ctx.curve_to(cp1_x, cp1_y, cp2_x, cp2_y, p2[0], p2[1])
    
    ctx.close_path()

def draw_natural_stroke(ctx, points):
    """Draw outline with natural line weight variations"""
    
    # Variable line width for hand-drawn effect
    base_width = random.uniform(1.5, 2.5)
    
    ctx.set_source_rgb(0, 0, 0)
    
    # Draw with slightly varying line width
    for i in range(len(points)):
        # Vary line width along the curve
        width_variation = 1 + 0.3 * math.sin(i * 0.8) * random.uniform(0.7, 1.3)
        current_width = base_width * width_variation
        
        ctx.set_line_width(current_width)
        
        # Draw small segments with varying width
        if i == 0:
            ctx.move_to(*points[i])
        else:
            ctx.line_to(*points[i])
    
    ctx.close_path()
    ctx.stroke()

def add_natural_tail(ctx, cx, cy, width, height):
    """Add a natural, hand-drawn tail"""
    
    # Tail attachment point (with some randomness)
    attach_x = cx + random.uniform(-width*0.2, width*0.2)
    attach_y = cy + height/2 + random.uniform(-10, 5)
    
    # Tail tip
    tail_length = random.uniform(height*0.6, height*0.9)
    tip_x = attach_x + random.uniform(-width*0.1, width*0.1)
    tip_y = attach_y + tail_length
    
    # Tail width
    tail_width = random.uniform(width*0.1, width*0.15)
    
    # Create natural tail curve
    left_attach = (attach_x - tail_width/2, attach_y)
    right_attach = (attach_x + tail_width/2, attach_y)
    
    # Control points for natural curve
    mid_left_x = (left_attach[0] + tip_x) / 2 + random.uniform(-tail_width*0.3, 0)
    mid_left_y = (left_attach[1] + tip_y) / 2 + random.uniform(-tail_length*0.1, tail_length*0.1)
    
    mid_right_x = (right_attach[0] + tip_x) / 2 + random.uniform(0, tail_width*0.3)
    mid_right_y = (right_attach[1] + tip_y) / 2 + random.uniform(-tail_length*0.1, tail_length*0.1)
    
    # Draw tail
    ctx.move_to(*left_attach)
    ctx.curve_to(mid_left_x, mid_left_y, 
                 tip_x - tail_width*0.2, tip_y - tail_length*0.1, 
                 tip_x, tip_y)
    ctx.curve_to(tip_x + tail_width*0.2, tip_y - tail_length*0.1,
                 mid_right_x, mid_right_y,
                 *right_attach)
    ctx.close_path()
    
    # Fill and stroke tail
    ctx.set_source_rgba(1, 1, 1, 0.95)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(random.uniform(1.5, 2.2))
    ctx.stroke()

def draw_natural_text(ctx, cx, cy, text):
    """Draw text with slight hand-lettered variations"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    font_size = random.uniform(12, 16)
    ctx.set_font_size(font_size)
    
    # Get text dimensions
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    # Add slight randomness to text position for hand-lettered effect
    text_x = cx - text_width/2 + random.uniform(-2, 2)
    text_y = cy + text_height/2 + random.uniform(-2, 2)
    
    # Slightly vary text color for natural look
    gray_value = random.uniform(0, 0.1)
    ctx.set_source_rgb(gray_value, gray_value, gray_value)
    
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_premium_bubbles_demo():
    """Create a demo with premium, smooth, natural-looking bubbles"""
    
    # Set seed for reproducible results
    random.seed(123)
    
    WIDTH, HEIGHT = 1000, 800
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Subtle textured background
    ctx.set_source_rgb(0.99, 0.98, 0.96)
    ctx.paint()
    
    # Add subtle paper texture
    for _ in range(50):
        x = random.uniform(0, WIDTH)
        y = random.uniform(0, HEIGHT)
        ctx.set_source_rgba(0.9, 0.9, 0.9, 0.1)
        ctx.arc(x, y, random.uniform(0.5, 2), 0, 2*math.pi)
        ctx.fill()
    
    # Create various natural bubbles
    bubbles = [
        # (cx, cy, width, height, text, style)
        (150, 140, 140, 100, "Natural speech!", "natural"),
        (400, 140, 150, 110, "Quirky bubble!", "quirky"), 
        (700, 140, 160, 95, "Flowing words!", "flowing"),
        (150, 320, 170, 120, "Organic shape!", "organic"),
        (400, 320, 145, 105, "Smooth curves!", "natural"),
        (700, 320, 155, 115, "Hand-drawn!", "quirky"),
        (150, 520, 140, 100, "Beautiful!", "flowing"),
        (400, 520, 165, 110, "Amazing!", "organic"),
        (700, 520, 150, 95, "Perfect!", "natural"),
    ]
    
    for cx, cy, width, height, text, style in bubbles:
        # Vary random seed for each bubble
        random.seed(123 + cx + cy)
        create_hand_drawn_bubble(ctx, cx, cy, width, height, text, style)
    
    # Add title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(24)
    ctx.set_source_rgb(0.2, 0.2, 0.2)
    ctx.move_to(300, 50)
    ctx.show_text("Premium Natural Speech Bubbles")
    
    surface.write_to_png("premium_natural_bubbles.png")
    print("✅ Premium natural bubbles saved as 'premium_natural_bubbles.png'")

if __name__ == "__main__":
    create_premium_bubbles_demo()
    print("🎨 Created smooth, unique bubbles with natural hand-drawn variations!")