import cairo
import math
import random

def create_casual_square_bubble(ctx, cx, cy, size, text="CASUAL!", wave_style="gentle", casualness="medium"):
    """Create a square bubble with casual, relaxed waves"""
    
    # Calculate square corners (strict positioning)
    half_size = size / 2
    corners = [
        (cx - half_size, cy - half_size),  # Top-left
        (cx + half_size, cy - half_size),  # Top-right  
        (cx + half_size, cy + half_size),  # Bottom-right
        (cx - half_size, cy + half_size)   # Bottom-left
    ]
    
    # Generate casual wave edges
    points = generate_casual_wave_edges(corners, wave_style, casualness)
    
    # Draw the casual square
    draw_casual_square_path(ctx, points, corners)
    
    # Soft gradient fill
    draw_casual_gradient(ctx, cx, cy, size)
    
    # Gentle outline
    draw_casual_outline(ctx, points)
    
    # Add text
    draw_casual_text(ctx, cx, cy, text)

def generate_casual_wave_edges(corners, wave_style, casualness):
    """Generate casual, natural wave points along edges"""
    
    all_points = []
    
    for i in range(4):  # 4 edges
        start_corner = corners[i]
        end_corner = corners[(i + 1) % 4]
        
        # Generate casual wave points along this edge
        edge_points = generate_casual_edge_points(start_corner, end_corner, wave_style, casualness, i)
        all_points.extend(edge_points)
    
    return all_points

def generate_casual_edge_points(start, end, style, casualness, edge_index):
    """Generate casual wave points along one edge"""
    
    points = []
    num_points = 25  # More points for smoother casual waves
    
    # Set casualness intensity
    casual_intensities = {
        "low": 0.6,
        "medium": 1.0, 
        "high": 1.4,
        "very_high": 1.8
    }
    intensity = casual_intensities.get(casualness, 1.0)
    
    for i in range(num_points):
        # Base position along straight edge
        t = i / (num_points - 1)
        base_x = start[0] + t * (end[0] - start[0])
        base_y = start[1] + t * (end[1] - start[1])
        
        # Calculate edge direction and normal
        edge_length = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        if edge_length > 0:
            normal_x = -(end[1] - start[1]) / edge_length
            normal_y = (end[0] - start[0]) / edge_length
        else:
            normal_x, normal_y = 0, 0
        
        # Apply casual wave displacement based on style
        if style == "gentle":
            # Very gentle, lazy waves
            wave1 = 8 * math.sin(t * math.pi * 1.5) * math.sin(t * math.pi)
            wave2 = 3 * math.sin(t * math.pi * 4) * (1 - abs(t - 0.5) * 2)  # Fade at edges
            displacement = (wave1 + wave2) * intensity * 0.7
            
        elif style == "lazy":
            # Super casual, almost sleepy waves
            wave1 = 6 * math.sin(t * math.pi * 1.2) * math.sin(t * math.pi * 0.8)
            wave2 = 2 * math.sin(t * math.pi * 3) * math.cos(t * math.pi * 2)
            wave3 = 1 * math.sin(t * math.pi * 7)  # Tiny details
            displacement = (wave1 + wave2 + wave3) * intensity * 0.8
            
        elif style == "relaxed":
            # Comfortable, natural waves
            wave1 = 10 * math.sin(t * math.pi * 2) * math.sin(t * math.pi)
            wave2 = 4 * math.sin(t * math.pi * 5) * (math.sin(t * math.pi * 1.5) ** 2)
            wave3 = 2 * math.cos(t * math.pi * 8) * math.sin(t * math.pi)
            displacement = (wave1 + wave2 + wave3) * intensity * 0.6
            
        elif style == "flowing":
            # Smooth flowing like water
            wave1 = 12 * math.sin(t * math.pi * 1.8) * math.sin(t * math.pi)
            wave2 = 5 * math.sin(t * math.pi * 3.5 + edge_index) * (1 - (t - 0.5)**2 * 4)
            wave3 = 2 * math.sin(t * math.pi * 9) * math.cos(t * math.pi * 2)
            displacement = (wave1 + wave2 + wave3) * intensity * 0.5
            
        elif style == "organic":
            # Natural, organic variations
            wave1 = 9 * math.sin(t * math.pi * 2.2) * math.sin(t * math.pi)
            wave2 = 4 * math.sin(t * math.pi * 4.7 + edge_index * 0.5)
            wave3 = 2 * math.sin(t * math.pi * 7.3) * (1 - abs(t - 0.5))
            wave4 = 1 * math.cos(t * math.pi * 11) * math.sin(t * math.pi * 3)
            displacement = (wave1 + wave2 + wave3 + wave4) * intensity * 0.6
            
        elif style == "dreamy":
            # Soft, dreamy undulations
            wave1 = 7 * math.sin(t * math.pi * 1.3) * math.sin(t * math.pi * 0.7)
            wave2 = 3 * math.sin(t * math.pi * 2.8) * math.cos(t * math.pi * 1.9)
            wave3 = 1.5 * math.sin(t * math.pi * 6) * (math.sin(t * math.pi) ** 3)
            displacement = (wave1 + wave2 + wave3) * intensity * 0.9
            
        else:  # "subtle"
            # Very minimal casual waves
            wave1 = 5 * math.sin(t * math.pi * 1.7) * math.sin(t * math.pi)
            wave2 = 2 * math.sin(t * math.pi * 4.2) * (1 - (t - 0.5)**2 * 3)
            displacement = (wave1 + wave2) * intensity * 0.8
        
        # Add tiny random variations for naturalness
        random_variation = random.uniform(-0.8, 0.8) * intensity
        displacement += random_variation
        
        # Apply displacement normal to edge
        casual_x = base_x + normal_x * displacement
        casual_y = base_y + normal_y * displacement
        
        points.append((casual_x, casual_y))
    
    return points[:-1]  # Remove last point to avoid duplication

def draw_casual_square_path(ctx, points, corners):
    """Draw ultra-smooth casual square path"""
    
    if not points:
        return
    
    ctx.move_to(*points[0])
    
    # Draw with ultra-smooth curves
    for i in range(len(points)):
        current = points[i]
        next_point = points[(i + 1) % len(points)]
        prev_point = points[i - 1]
        next_next = points[(i + 2) % len(points)]
        
        # Ultra-smooth tension for casual feel
        tension = 0.35 + 0.1 * math.sin(i * 0.3)  # Variable tension
        
        # Calculate smooth control points
        cp1_x = current[0] + (next_point[0] - prev_point[0]) * tension * 0.4
        cp1_y = current[1] + (next_point[1] - prev_point[1]) * tension * 0.4
        cp2_x = next_point[0] - (next_next[0] - current[0]) * tension * 0.4
        cp2_y = next_point[1] - (next_next[1] - current[1]) * tension * 0.4
        
        ctx.curve_to(cp1_x, cp1_y, cp2_x, cp2_y, next_point[0], next_point[1])
    
    ctx.close_path()

def draw_casual_gradient(ctx, cx, cy, size):
    """Create soft, casual gradient"""
    
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, size * 0.8)
    
    # Soft, casual colors
    gradient.add_color_stop_rgb(0.0, 1.0, 1.0, 0.98)    # Soft white
    gradient.add_color_stop_rgb(0.2, 0.98, 0.98, 1.0)   # Very light blue
    gradient.add_color_stop_rgb(0.5, 0.92, 0.95, 1.0)   # Light blue
    gradient.add_color_stop_rgb(0.8, 0.85, 0.9, 0.98)   # Soft blue-gray
    gradient.add_color_stop_rgb(1.0, 0.78, 0.85, 0.95)  # Gentle edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()

def draw_casual_outline(ctx, points):
    """Draw soft, casual outline"""
    
    # Main outline - soft and gentle
    ctx.set_source_rgba(0, 0, 0, 0.7)  # Softer black
    ctx.set_line_width(2.0)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke_preserve()
    
    # Subtle glow for casual softness
    ctx.set_source_rgba(0.6, 0.7, 0.9, 0.3)
    ctx.set_line_width(4.0)
    ctx.stroke()

def create_casual_rectangle(ctx, cx, cy, width, height, text="CASUAL RECT!", wave_style="gentle"):
    """Create casual rectangular bubble"""
    
    # Rectangle corners
    half_w, half_h = width / 2, height / 2
    corners = [
        (cx - half_w, cy - half_h),  # Top-left
        (cx + half_w, cy - half_h),  # Top-right
        (cx + half_w, cy + half_h),  # Bottom-right
        (cx - half_w, cy + half_h)   # Bottom-left
    ]
    
    # Generate casual waves for rectangle
    points = []
    
    for i in range(4):
        start_corner = corners[i]
        end_corner = corners[(i + 1) % 4]
        
        # More casual points for rectangles
        edge_points = []
        num_points = 30
        
        for j in range(num_points):
            t = j / (num_points - 1)
            base_x = start_corner[0] + t * (end_corner[0] - start_corner[0])
            base_y = start_corner[1] + t * (end_corner[1] - start_corner[1])
            
            # Edge normal
            edge_length = math.sqrt((end_corner[0] - start_corner[0])**2 + (end_corner[1] - start_corner[1])**2)
            if edge_length > 0:
                normal_x = -(end_corner[1] - start_corner[1]) / edge_length
                normal_y = (end_corner[0] - start_corner[0]) / edge_length
            else:
                normal_x, normal_y = 0, 0
            
            # Casual waves for rectangles
            if wave_style == "gentle":
                wave = 6 * math.sin(t * math.pi * 2.3) * math.sin(t * math.pi) * 0.8
            elif wave_style == "lazy":
                wave = 4 * math.sin(t * math.pi * 1.5) * math.sin(t * math.pi * 0.9) * 0.9
            else:  # relaxed
                wave = 8 * math.sin(t * math.pi * 2.1) * math.sin(t * math.pi) * 0.7
            
            wave += random.uniform(-0.5, 0.5)  # Tiny randomness
            
            casual_x = base_x + normal_x * wave
            casual_y = base_y + normal_y * wave
            
            edge_points.append((casual_x, casual_y))
        
        points.extend(edge_points[:-1])
    
    # Draw casual rectangle
    draw_casual_square_path(ctx, points, corners)
    
    # Rectangle gradient
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, max(width, height) * 0.6)
    gradient.add_color_stop_rgb(0, 1.0, 0.98, 0.95)     # Warm white
    gradient.add_color_stop_rgb(0.4, 0.98, 0.94, 0.88)  # Cream
    gradient.add_color_stop_rgb(0.8, 0.92, 0.88, 0.82)  # Light brown
    gradient.add_color_stop_rgb(1, 0.85, 0.82, 0.78)    # Soft edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Soft outline
    draw_casual_outline(ctx, points)
    
    # Add text
    draw_casual_text(ctx, cx, cy, text)

def draw_casual_text(ctx, cx, cy, text):
    """Draw text with casual feel"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(13)
    
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    # Slightly casual positioning
    text_x = cx - text_width / 2 + random.uniform(-0.5, 0.5)
    text_y = cy + text_height / 2 + random.uniform(-0.5, 0.5)
    
    # Soft text shadow
    ctx.set_source_rgba(0, 0, 0, 0.2)
    ctx.move_to(text_x + 0.8, text_y + 0.8)
    ctx.show_text(text)
    
    # Main text - softer black
    ctx.set_source_rgba(0.1, 0.1, 0.1, 0.8)
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_casual_wave_demo():
    """Create demo with casual, relaxed wave bubbles"""
    
    random.seed(888)  # For gentle randomness
    
    WIDTH, HEIGHT = 1300, 1000
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Soft background
    ctx.set_source_rgb(0.98, 0.98, 0.97)
    ctx.paint()
    
    # Row 1: Different casual wave styles
    create_casual_square_bubble(ctx, 130, 140, 110, "GENTLE!", "gentle", "medium")
    create_casual_square_bubble(ctx, 320, 140, 110, "LAZY!", "lazy", "high")
    create_casual_square_bubble(ctx, 510, 140, 110, "RELAXED!", "relaxed", "medium")
    create_casual_square_bubble(ctx, 700, 140, 110, "FLOWING!", "flowing", "high")
    create_casual_square_bubble(ctx, 890, 140, 110, "ORGANIC!", "organic", "medium")
    
    # Row 2: Dreamy and subtle styles
    create_casual_square_bubble(ctx, 130, 320, 115, "DREAMY!", "dreamy", "high")
    create_casual_square_bubble(ctx, 320, 320, 115, "SUBTLE!", "subtle", "low")
    create_casual_square_bubble(ctx, 510, 320, 115, "CHILL!", "gentle", "very_high")
    create_casual_square_bubble(ctx, 700, 320, 115, "SOFT!", "lazy", "medium")
    create_casual_square_bubble(ctx, 890, 320, 115, "SMOOTH!", "flowing", "low")
    
    # Row 3: Casual rectangles
    create_casual_rectangle(ctx, 200, 520, 140, 100, "CASUAL!", "gentle")
    create_casual_rectangle(ctx, 450, 520, 130, 110, "LAZY RECT!", "lazy")
    create_casual_rectangle(ctx, 700, 520, 150, 95, "RELAXED!", "relaxed")
    create_casual_rectangle(ctx, 950, 520, 135, 105, "FLOWING!", "gentle")
    
    # Row 4: Large casual bubbles
    create_casual_square_bubble(ctx, 200, 720, 140, "BIG CASUAL!", "organic", "high")
    create_casual_square_bubble(ctx, 500, 720, 145, "MEGA LAZY!", "lazy", "very_high")
    create_casual_rectangle(ctx, 800, 720, 180, 120, "HUGE CHILL!", "flowing")
    
    # Row 5: Extra casual examples
    create_casual_square_bubble(ctx, 150, 880, 120, "SUPER SOFT!", "dreamy", "high")
    create_casual_square_bubble(ctx, 400, 880, 125, "ULTRA CALM!", "gentle", "very_high")
    create_casual_square_bubble(ctx, 650, 880, 115, "ZEN MODE!", "subtle", "medium")
    create_casual_square_bubble(ctx, 900, 880, 130, "PEACEFUL!", "flowing", "high")
    
    # Title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(30)
    ctx.set_source_rgba(0.2, 0.2, 0.3, 0.8)
    ctx.move_to(380, 50)
    ctx.show_text("CASUAL WAVE BUBBLES")
    
    # Subtitle
    ctx.set_font_size(16)
    ctx.move_to(450, 80)
    ctx.show_text("Relaxed & Natural")
    
    surface.write_to_png("casual_wave_bubbles.png")
    print("✅ Casual wave bubbles saved as 'casual_wave_bubbles.png'")

if __name__ == "__main__":
    create_casual_wave_demo()
    print("🌊 Created super casual, relaxed wave bubbles! Like gentle ocean waves! 🏖️✨")