import cairo
import math
import random

def create_intruding_ovals_square(ctx, cx, cy, base_size, text="INTRUDE!", layout="sides_corners"):
    """Create square with ovals/circles that intrude into the square space"""
    
    # Calculate base square
    half_size = base_size / 2
    
    # Draw base square first (will be partially covered)
    draw_base_square_outline(ctx, cx, cy, base_size)
    
    if layout == "sides_corners":
        # 2 large ovals on opposite sides + small circles in corners
        create_sides_and_corners_layout(ctx, cx, cy, half_size)
    elif layout == "all_sides":
        # Large ovals on all 4 sides
        create_all_sides_layout(ctx, cx, cy, half_size)
    elif layout == "alternating":
        # Alternating large/small around perimeter
        create_alternating_layout(ctx, cx, cy, half_size)
    else:  # "random"
        # Random intrusions
        create_random_intrusions_layout(ctx, cx, cy, half_size)
    
    # Draw square fill (will show through gaps between ovals)
    draw_square_fill(ctx, cx, cy, base_size)
    
    # Add text
    draw_intrusion_text(ctx, cx, cy, text)

def create_sides_and_corners_layout(ctx, cx, cy, half_size):
    """Create 2 large ovals on sides + small circles in corners"""
    
    # Large ovals on left and right sides (intruding into square)
    large_ovals = [
        {
            'x': cx - half_size + 15,  # Intrude 15px into square from left
            'y': cy,
            'rx': 25,  # Width
            'ry': 45,  # Height (tall oval)
            'type': 'large_side'
        },
        {
            'x': cx + half_size - 15,  # Intrude 15px into square from right
            'y': cy,
            'rx': 25,
            'ry': 45,
            'type': 'large_side'
        }
    ]
    
    # Small circles in corners (intruding into square)
    corner_circles = [
        {
            'x': cx - half_size + 12,  # Top-left corner intrusion
            'y': cy - half_size + 12,
            'rx': 15,
            'ry': 15,
            'type': 'corner'
        },
        {
            'x': cx + half_size - 12,  # Top-right corner intrusion
            'y': cy - half_size + 12,
            'rx': 15,
            'ry': 15,
            'type': 'corner'
        },
        {
            'x': cx + half_size - 12,  # Bottom-right corner intrusion
            'y': cy + half_size - 12,
            'rx': 15,
            'ry': 15,
            'type': 'corner'
        },
        {
            'x': cx - half_size + 12,  # Bottom-left corner intrusion
            'y': cy + half_size - 12,
            'rx': 15,
            'ry': 15,
            'type': 'corner'
        }
    ]
    
    # Draw all shapes
    all_shapes = large_ovals + corner_circles
    for shape in all_shapes:
        draw_intruding_shape(ctx, shape)

def create_all_sides_layout(ctx, cx, cy, half_size):
    """Create large ovals on all 4 sides intruding into square"""
    
    intrusion_depth = 18  # How far into square
    
    side_ovals = [
        {
            'x': cx,  # Top side
            'y': cy - half_size + intrusion_depth,
            'rx': 35,  # Wide oval
            'ry': 20,
            'type': 'side_top'
        },
        {
            'x': cx + half_size - intrusion_depth,  # Right side
            'y': cy,
            'rx': 20,
            'ry': 35,  # Tall oval
            'type': 'side_right'
        },
        {
            'x': cx,  # Bottom side
            'y': cy + half_size - intrusion_depth,
            'rx': 35,  # Wide oval
            'ry': 20,
            'type': 'side_bottom'
        },
        {
            'x': cx - half_size + intrusion_depth,  # Left side
            'y': cy,
            'rx': 20,
            'ry': 35,  # Tall oval
            'type': 'side_left'
        }
    ]
    
    for shape in side_ovals:
        draw_intruding_shape(ctx, shape)

def create_alternating_layout(ctx, cx, cy, half_size):
    """Create alternating large/small shapes around perimeter"""
    
    intrusion = 15
    
    shapes = [
        # Large on top
        {
            'x': cx,
            'y': cy - half_size + intrusion,
            'rx': 30, 'ry': 18,
            'type': 'large_top'
        },
        # Small on top-right corner
        {
            'x': cx + half_size - 10,
            'y': cy - half_size + 10,
            'rx': 12, 'ry': 12,
            'type': 'small_corner'
        },
        # Large on right
        {
            'x': cx + half_size - intrusion,
            'y': cy,
            'rx': 18, 'ry': 30,
            'type': 'large_right'
        },
        # Small on bottom-right corner
        {
            'x': cx + half_size - 10,
            'y': cy + half_size - 10,
            'rx': 12, 'ry': 12,
            'type': 'small_corner'
        },
        # Large on bottom
        {
            'x': cx,
            'y': cy + half_size - intrusion,
            'rx': 30, 'ry': 18,
            'type': 'large_bottom'
        },
        # Small on bottom-left corner
        {
            'x': cx - half_size + 10,
            'y': cy + half_size - 10,
            'rx': 12, 'ry': 12,
            'type': 'small_corner'
        },
        # Large on left
        {
            'x': cx - half_size + intrusion,
            'y': cy,
            'rx': 18, 'ry': 30,
            'type': 'large_left'
        },
        # Small on top-left corner
        {
            'x': cx - half_size + 10,
            'y': cy - half_size + 10,
            'rx': 12, 'ry': 12,
            'type': 'small_corner'
        }
    ]
    
    for shape in shapes:
        draw_intruding_shape(ctx, shape)

def create_random_intrusions_layout(ctx, cx, cy, half_size):
    """Create random oval intrusions into the square"""
    
    shapes = []
    
    # Generate random intrusions
    for i in range(random.randint(5, 8)):
        # Random position around square perimeter
        angle = random.uniform(0, 2 * math.pi)
        
        # Distance from center (intrude into square)
        distance = half_size - random.uniform(10, 25)
        
        shape_x = cx + distance * math.cos(angle)
        shape_y = cy + distance * math.sin(angle)
        
        # Random oval size
        base_radius = random.uniform(12, 25)
        
        shapes.append({
            'x': shape_x,
            'y': shape_y,
            'rx': base_radius * random.uniform(0.7, 1.3),
            'ry': base_radius * random.uniform(0.7, 1.3),
            'type': 'random'
        })
    
    for shape in shapes:
        draw_intruding_shape(ctx, shape)

def draw_intruding_shape(ctx, shape):
    """Draw a single intruding oval/circle"""
    
    # Save current state
    ctx.save()
    
    # Create ellipse path
    ctx.translate(shape['x'], shape['y'])
    ctx.scale(shape['rx'], shape['ry'])
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    
    # Restore for gradient
    ctx.restore()
    
    # Create gradient based on shape type
    gradient = cairo.RadialGradient(
        shape['x'], shape['y'], 0,
        shape['x'], shape['y'], max(shape['rx'], shape['ry'])
    )
    
    # Color based on shape type and size
    if shape['type'] == 'large_side':
        # Large side ovals - blue tones
        gradient.add_color_stop_rgb(0, 0.9, 0.95, 1.0)   # Light blue center
        gradient.add_color_stop_rgb(1, 0.7, 0.8, 0.95)   # Blue edge
    elif shape['type'] == 'corner':
        # Corner circles - warm tones
        gradient.add_color_stop_rgb(0, 1.0, 0.95, 0.9)   # Warm center
        gradient.add_color_stop_rgb(1, 0.9, 0.8, 0.7)    # Warm edge
    elif 'side_' in shape['type']:
        # Side ovals - green tones
        gradient.add_color_stop_rgb(0, 0.9, 1.0, 0.9)    # Light green
        gradient.add_color_stop_rgb(1, 0.75, 0.9, 0.75)  # Green edge
    elif 'large_' in shape['type']:
        # Large shapes - purple tones
        gradient.add_color_stop_rgb(0, 0.95, 0.9, 1.0)   # Light purple
        gradient.add_color_stop_rgb(1, 0.8, 0.7, 0.9)    # Purple edge
    elif 'small_' in shape['type']:
        # Small shapes - yellow tones
        gradient.add_color_stop_rgb(0, 1.0, 1.0, 0.9)    # Light yellow
        gradient.add_color_stop_rgb(1, 0.9, 0.9, 0.7)    # Yellow edge
    else:  # random
        # Random shapes - pink tones
        gradient.add_color_stop_rgb(0, 1.0, 0.9, 0.95)   # Light pink
        gradient.add_color_stop_rgb(1, 0.9, 0.7, 0.8)    # Pink edge
    
    # Fill shape
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Shape outline
    ctx.set_source_rgba(0, 0, 0, 0.4)
    ctx.set_line_width(1.5)
    ctx.stroke()

def draw_base_square_outline(ctx, cx, cy, size):
    """Draw just the square outline (to show intrusion)"""
    
    half_size = size / 2
    
    # Square outline only
    ctx.rectangle(cx - half_size, cy - half_size, size, size)
    ctx.set_source_rgba(0, 0, 0, 0.6)
    ctx.set_line_width(2.5)
    ctx.stroke()

def draw_square_fill(ctx, cx, cy, size):
    """Draw square fill that shows through gaps"""
    
    half_size = size / 2
    
    # Create square path
    ctx.rectangle(cx - half_size, cy - half_size, size, size)
    
    # Light fill that shows in gaps
    ctx.set_source_rgba(1.0, 1.0, 1.0, 0.8)  # Semi-transparent white
    ctx.fill()

def draw_intrusion_text(ctx, cx, cy, text):
    """Draw text in center of intruding square"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(12)
    
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    text_x = cx - text_width / 2
    text_y = cy + text_height / 2
    
    # Text shadow for visibility
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.move_to(text_x + 1, text_y + 1)
    ctx.show_text(text)
    
    # Main text
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_bubble_square_with_intrusions(ctx, cx, cy, base_size, text="BUBBLE!", num_intrusions=6):
    """Create a more bubble-like square with multiple intrusions"""
    
    half_size = base_size / 2
    
    # Draw base square outline
    draw_base_square_outline(ctx, cx, cy, base_size)
    
    # Create bubble-like intrusions around the perimeter
    intrusions = []
    
    # Main large intrusions (4 sides)
    main_intrusions = [
        # Top
        {'x': cx, 'y': cy - half_size + 20, 'rx': 25, 'ry': 18, 'type': 'main'},
        # Right  
        {'x': cx + half_size - 20, 'y': cy, 'rx': 18, 'ry': 25, 'type': 'main'},
        # Bottom
        {'x': cx, 'y': cy + half_size - 20, 'rx': 25, 'ry': 18, 'type': 'main'},
        # Left
        {'x': cx - half_size + 20, 'y': cy, 'rx': 18, 'ry': 25, 'type': 'main'}
    ]
    
    # Additional smaller intrusions
    for i in range(num_intrusions - 4):
        angle = random.uniform(0, 2 * math.pi)
        distance = half_size - random.uniform(8, 15)
        
        intrusion_x = cx + distance * math.cos(angle)
        intrusion_y = cy + distance * math.sin(angle)
        
        size = random.uniform(8, 16)
        
        main_intrusions.append({
            'x': intrusion_x,
            'y': intrusion_y,
            'rx': size,
            'ry': size,
            'type': 'bubble'
        })
    
    # Draw all intrusions
    for intrusion in main_intrusions:
        draw_intruding_shape(ctx, intrusion)
    
    # Draw square fill
    draw_square_fill(ctx, cx, cy, base_size)
    
    # Add text
    draw_intrusion_text(ctx, cx, cy, text)

def create_intrusion_demo():
    """Create demo with various intrusion layouts"""
    
    random.seed(888)
    
    WIDTH, HEIGHT = 1200, 1000
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(0.96, 0.96, 0.98)
    ctx.paint()
    
    # Row 1: Basic intrusion layouts
    create_intruding_ovals_square(ctx, 150, 140, 100, "SIDES!", "sides_corners")
    create_intruding_ovals_square(ctx, 350, 140, 100, "ALL SIDES!", "all_sides") 
    create_intruding_ovals_square(ctx, 550, 140, 100, "ALTERNATE!", "alternating")
    create_intruding_ovals_square(ctx, 750, 140, 100, "RANDOM!", "random")
    create_bubble_square_with_intrusions(ctx, 950, 140, 100, "BUBBLE!", 6)
    
    # Row 2: Larger versions
    create_intruding_ovals_square(ctx, 200, 320, 130, "BIG SIDES!", "sides_corners")
    create_intruding_ovals_square(ctx, 450, 320, 130, "BIG ALL!", "all_sides")
    create_intruding_ovals_square(ctx, 700, 320, 130, "BIG ALT!", "alternating")
    create_bubble_square_with_intrusions(ctx, 950, 320, 130, "BIG BUBBLE!", 8)
    
    # Row 3: Different bubble counts
    create_bubble_square_with_intrusions(ctx, 150, 520, 120, "FEW!", 4)
    create_bubble_square_with_intrusions(ctx, 350, 520, 120, "SOME!", 6)
    create_bubble_square_with_intrusions(ctx, 550, 520, 120, "MANY!", 8)
    create_bubble_square_with_intrusions(ctx, 750, 520, 120, "LOTS!", 10)
    create_intruding_ovals_square(ctx, 950, 520, 120, "MEGA!", "random")
    
    # Row 4: Extra large examples
    create_intruding_ovals_square(ctx, 200, 720, 150, "HUGE SIDES!", "sides_corners")
    create_bubble_square_with_intrusions(ctx, 500, 720, 150, "HUGE BUBBLE!", 9)
    create_intruding_ovals_square(ctx, 800, 720, 150, "HUGE RANDOM!", "random")
    
    # Row 5: Final variations
    create_intruding_ovals_square(ctx, 150, 880, 110, "ULTIMATE!", "alternating")
    create_bubble_square_with_intrusions(ctx, 350, 880, 110, "SUPREME!", 7)
    create_intruding_ovals_square(ctx, 550, 880, 110, "MAXIMUM!", "all_sides")
    create_bubble_square_with_intrusions(ctx, 750, 880, 110, "EXTREME!", 12)
    create_intruding_ovals_square(ctx, 950, 880, 110, "PERFECT!", "sides_corners")
    
    # Title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(30)
    ctx.set_source_rgb(0.2, 0.2, 0.4)
    ctx.move_to(350, 50)
    ctx.show_text("INTRUDING OVALS & CIRCLES")
    
    # Subtitle
    ctx.set_font_size(16)
    ctx.move_to(450, 80)
    ctx.show_text("Taking Space Inside the Square")
    
    surface.write_to_png("intruding_ovals_squares.png")
    print("✅ Intruding ovals squares saved as 'intruding_ovals_squares.png'")

if __name__ == "__main__":
    create_intrusion_demo()
    print("🟦 Created squares with intruding ovals! They take up space INSIDE the square! 🔵✨")