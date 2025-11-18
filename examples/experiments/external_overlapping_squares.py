import cairo
import math
import random

def create_external_overlapping_square(ctx, cx, cy, base_size, text="OVERLAP!", layout="sides_corners"):
    """Create square with ovals/circles OUTSIDE but overlapping the square"""
    
    # Calculate base square
    half_size = base_size / 2
    
    # Draw shapes FIRST (they're outside/behind the square)
    if layout == "sides_corners":
        # 2 large ovals on opposite sides + small circles in corners
        create_external_sides_and_corners(ctx, cx, cy, half_size)
    elif layout == "all_sides":
        # Large ovals on all 4 sides
        create_external_all_sides(ctx, cx, cy, half_size)
    elif layout == "alternating":
        # Alternating large/small around perimeter
        create_external_alternating(ctx, cx, cy, half_size)
    else:  # "random"
        # Random external overlaps
        create_external_random_overlaps(ctx, cx, cy, half_size)
    
    # Draw square OVER the shapes (square is on top)
    draw_main_square(ctx, cx, cy, base_size)
    
    # Add text in square
    draw_square_text(ctx, cx, cy, text)

def create_external_sides_and_corners(ctx, cx, cy, half_size):
    """Create 2 large ovals on sides + small circles in corners, ALL EXTERNAL"""
    
    # Large ovals OUTSIDE the square on left and right sides
    large_ovals = [
        {
            'x': cx - half_size - 20,  # OUTSIDE left, overlapping edge
            'y': cy,
            'rx': 25,  # Width
            'ry': 45,  # Height (tall oval)
            'overlap': 10,  # How much it overlaps the square edge
            'type': 'large_side'
        },
        {
            'x': cx + half_size + 20,  # OUTSIDE right, overlapping edge
            'y': cy,
            'rx': 25,
            'ry': 45,
            'overlap': 10,
            'type': 'large_side'
        }
    ]
    
    # Small circles OUTSIDE the square at corners
    corner_circles = [
        {
            'x': cx - half_size - 10,  # OUTSIDE top-left corner
            'y': cy - half_size - 10,
            'rx': 15,
            'ry': 15,
            'overlap': 8,
            'type': 'corner'
        },
        {
            'x': cx + half_size + 10,  # OUTSIDE top-right corner
            'y': cy - half_size - 10,
            'rx': 15,
            'ry': 15,
            'overlap': 8,
            'type': 'corner'
        },
        {
            'x': cx + half_size + 10,  # OUTSIDE bottom-right corner
            'y': cy + half_size + 10,
            'rx': 15,
            'ry': 15,
            'overlap': 8,
            'type': 'corner'
        }
    ]
    
    # Draw all external shapes
    all_shapes = large_ovals + corner_circles
    for shape in all_shapes:
        draw_external_shape(ctx, shape)

def create_external_all_sides(ctx, cx, cy, half_size):
    """Create large ovals OUTSIDE all 4 sides, overlapping the square"""
    
    overlap_distance = 15  # How much they overlap the square edge
    external_distance = 25  # How far outside the square they are positioned
    
    side_ovals = [
        {
            'x': cx,  # Top side - OUTSIDE
            'y': cy - half_size - external_distance,
            'rx': 35,  # Wide oval
            'ry': 20,
            'overlap': overlap_distance,
            'type': 'side_top'
        },
        {
            'x': cx + half_size + external_distance,  # Right side - OUTSIDE
            'y': cy,
            'rx': 20,
            'ry': 35,  # Tall oval
            'overlap': overlap_distance,
            'type': 'side_right'
        },
        {
            'x': cx,  # Bottom side - OUTSIDE
            'y': cy + half_size + external_distance,
            'rx': 35,  # Wide oval
            'ry': 20,
            'overlap': overlap_distance,
            'type': 'side_bottom'
        },
        {
            'x': cx - half_size - external_distance,  # Left side - OUTSIDE
            'y': cy,
            'rx': 20,
            'ry': 35,  # Tall oval
            'overlap': overlap_distance,
            'type': 'side_left'
        }
    ]
    
    for shape in side_ovals:
        draw_external_shape(ctx, shape)

def create_external_alternating(ctx, cx, cy, half_size):
    """Create alternating large/small shapes OUTSIDE square perimeter"""
    
    external_dist = 20
    
    shapes = [
        # Large on top - OUTSIDE
        {
            'x': cx,
            'y': cy - half_size - external_dist,
            'rx': 30, 'ry': 18,
            'overlap': 12,
            'type': 'large_top'
        },
        # Small on top-right corner - OUTSIDE
        {
            'x': cx + half_size + 15,
            'y': cy - half_size - 15,
            'rx': 12, 'ry': 12,
            'overlap': 8,
            'type': 'small_corner'
        },
        # Large on right - OUTSIDE
        {
            'x': cx + half_size + external_dist,
            'y': cy,
            'rx': 18, 'ry': 30,
            'overlap': 12,
            'type': 'large_right'
        },
        # Small on bottom-right corner - OUTSIDE
        {
            'x': cx + half_size + 15,
            'y': cy + half_size + 15,
            'rx': 12, 'ry': 12,
            'overlap': 8,
            'type': 'small_corner'
        },
        # Large on bottom - OUTSIDE
        {
            'x': cx,
            'y': cy + half_size + external_dist,
            'rx': 30, 'ry': 18,
            'overlap': 12,
            'type': 'large_bottom'
        },
        # Small on bottom-left corner - OUTSIDE
        {
            'x': cx - half_size - 15,
            'y': cy + half_size + 15,
            'rx': 12, 'ry': 12,
            'overlap': 8,
            'type': 'small_corner'
        },
        # Large on left - OUTSIDE
        {
            'x': cx - half_size - external_dist,
            'y': cy,
            'rx': 18, 'ry': 30,
            'overlap': 12,
            'type': 'large_left'
        },
        # Small on top-left corner - OUTSIDE
        {
            'x': cx - half_size - 15,
            'y': cy - half_size - 15,
            'rx': 12, 'ry': 12,
            'overlap': 8,
            'type': 'small_corner'
        }
    ]
    
    for shape in shapes:
        draw_external_shape(ctx, shape)

def create_external_random_overlaps(ctx, cx, cy, half_size):
    """Create random oval overlaps OUTSIDE the square"""
    
    shapes = []
    
    # Generate random external overlaps
    for i in range(random.randint(5, 8)):
        # Random position OUTSIDE square perimeter
        angle = random.uniform(0, 2 * math.pi)
        
        # Distance from center (OUTSIDE the square)
        distance = half_size + random.uniform(15, 30)
        
        shape_x = cx + distance * math.cos(angle)
        shape_y = cy + distance * math.sin(angle)
        
        # Random oval size
        base_radius = random.uniform(12, 25)
        
        shapes.append({
            'x': shape_x,
            'y': shape_y,
            'rx': base_radius * random.uniform(0.7, 1.3),
            'ry': base_radius * random.uniform(0.7, 1.3),
            'overlap': random.uniform(8, 15),
            'type': 'random'
        })
    
    for shape in shapes:
        draw_external_shape(ctx, shape)

def draw_external_shape(ctx, shape):
    """Draw a single external oval/circle that overlaps the square"""
    
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
    
    # Color based on shape type
    if shape['type'] == 'large_side':
        # Large side ovals - blue tones
        gradient.add_color_stop_rgb(0, 0.8, 0.9, 1.0)   # Light blue center
        gradient.add_color_stop_rgb(1, 0.6, 0.7, 0.9)   # Blue edge
    elif shape['type'] == 'corner':
        # Corner circles - warm tones
        gradient.add_color_stop_rgb(0, 1.0, 0.9, 0.8)   # Warm center
        gradient.add_color_stop_rgb(1, 0.9, 0.7, 0.6)    # Warm edge
    elif 'side_' in shape['type']:
        # Side ovals - green tones
        gradient.add_color_stop_rgb(0, 0.8, 1.0, 0.8)    # Light green
        gradient.add_color_stop_rgb(1, 0.6, 0.8, 0.6)  # Green edge
    elif 'large_' in shape['type']:
        # Large shapes - purple tones
        gradient.add_color_stop_rgb(0, 0.9, 0.8, 1.0)   # Light purple
        gradient.add_color_stop_rgb(1, 0.7, 0.6, 0.8)    # Purple edge
    elif 'small_' in shape['type']:
        # Small shapes - yellow tones
        gradient.add_color_stop_rgb(0, 1.0, 0.95, 0.8)    # Light yellow
        gradient.add_color_stop_rgb(1, 0.9, 0.8, 0.6)    # Yellow edge
    else:  # random
        # Random shapes - pink tones
        gradient.add_color_stop_rgb(0, 1.0, 0.85, 0.9)   # Light pink
        gradient.add_color_stop_rgb(1, 0.8, 0.6, 0.7)    # Pink edge
    
    # Fill shape
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Shape outline
    ctx.set_source_rgba(0, 0, 0, 0.3)
    ctx.set_line_width(1.5)
    ctx.stroke()

def draw_main_square(ctx, cx, cy, size):
    """Draw the main square that sits ON TOP of the external shapes"""
    
    half_size = size / 2
    
    # Create square path
    ctx.rectangle(cx - half_size, cy - half_size, size, size)
    
    # Square gradient fill
    gradient = cairo.LinearGradient(cx - half_size, cy - half_size, cx + half_size, cy + half_size)
    gradient.add_color_stop_rgb(0, 0.98, 0.98, 1.0)   # Very light center
    gradient.add_color_stop_rgb(1, 0.92, 0.92, 0.96)  # Slightly darker edges
    
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Square outline (stronger to show it's on top)
    ctx.set_source_rgba(0, 0, 0, 0.7)
    ctx.set_line_width(2.5)
    ctx.stroke()

def draw_square_text(ctx, cx, cy, text):
    """Draw text in center of the square"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(12)
    
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    text_x = cx - text_width / 2
    text_y = cy + text_height / 2
    
    # Text shadow for visibility
    ctx.set_source_rgba(0.8, 0.8, 0.8, 0.6)
    ctx.move_to(text_x + 1, text_y + 1)
    ctx.show_text(text)
    
    # Main text
    ctx.set_source_rgb(0.1, 0.1, 0.2)
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_external_bubble_square(ctx, cx, cy, base_size, text="BUBBLE!", num_bubbles=6):
    """Create a square with external bubble-like overlaps"""
    
    half_size = base_size / 2
    
    # Create external bubble overlaps
    bubbles = []
    
    # Main bubbles on sides (EXTERNAL)
    main_bubbles = [
        # Top
        {'x': cx, 'y': cy - half_size - 22, 'rx': 20, 'ry': 15, 'overlap': 10, 'type': 'main'},
        # Right  
        {'x': cx + half_size + 22, 'y': cy, 'rx': 15, 'ry': 20, 'overlap': 10, 'type': 'main'},
        # Bottom
        {'x': cx, 'y': cy + half_size + 22, 'rx': 20, 'ry': 15, 'overlap': 10, 'type': 'main'},
        # Left
        {'x': cx - half_size - 22, 'y': cy, 'rx': 15, 'ry': 20, 'overlap': 10, 'type': 'main'}
    ]
    
    # Additional smaller external bubbles
    for i in range(num_bubbles - 4):
        angle = random.uniform(0, 2 * math.pi)
        distance = half_size + random.uniform(18, 28)  # EXTERNAL distance
        
        bubble_x = cx + distance * math.cos(angle)
        bubble_y = cy + distance * math.sin(angle)
        
        size = random.uniform(8, 16)
        
        main_bubbles.append({
            'x': bubble_x,
            'y': bubble_y,
            'rx': size,
            'ry': size,
            'overlap': random.uniform(6, 12),
            'type': 'bubble'
        })
    
    # Draw all external bubbles
    for bubble in main_bubbles:
        draw_external_shape(ctx, bubble)
    
    # Draw square on top
    draw_main_square(ctx, cx, cy, base_size)
    
    # Add text
    draw_square_text(ctx, cx, cy, text)

def create_external_overlap_demo():
    """Create demo with various external overlap layouts"""
    
    random.seed(999)
    
    WIDTH, HEIGHT = 1200, 1000
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(0.94, 0.94, 0.96)
    ctx.paint()
    
    # Row 1: Basic external overlap layouts
    create_external_overlapping_square(ctx, 150, 140, 100, "SIDES!", "sides_corners")
    create_external_overlapping_square(ctx, 350, 140, 100, "ALL SIDES!", "all_sides") 
    create_external_overlapping_square(ctx, 550, 140, 100, "ALTERNATE!", "alternating")
    create_external_overlapping_square(ctx, 750, 140, 100, "RANDOM!", "random")
    create_external_bubble_square(ctx, 950, 140, 100, "BUBBLE!", 6)
    
    # Row 2: Larger versions
    create_external_overlapping_square(ctx, 200, 320, 130, "BIG SIDES!", "sides_corners")
    create_external_overlapping_square(ctx, 450, 320, 130, "BIG ALL!", "all_sides")
    create_external_overlapping_square(ctx, 700, 320, 130, "BIG ALT!", "alternating")
    create_external_bubble_square(ctx, 950, 320, 130, "BIG BUBBLE!", 8)
    
    # Row 3: Different bubble counts
    create_external_bubble_square(ctx, 150, 520, 120, "FEW!", 4)
    create_external_bubble_square(ctx, 350, 520, 120, "SOME!", 6)
    create_external_bubble_square(ctx, 550, 520, 120, "MANY!", 8)
    create_external_bubble_square(ctx, 750, 520, 120, "LOTS!", 10)
    create_external_overlapping_square(ctx, 950, 520, 120, "MEGA!", "random")
    
    # Row 4: Extra large examples
    create_external_overlapping_square(ctx, 200, 720, 150, "HUGE SIDES!", "sides_corners")
    create_external_bubble_square(ctx, 500, 720, 150, "HUGE BUBBLE!", 9)
    create_external_overlapping_square(ctx, 800, 720, 150, "HUGE RANDOM!", "random")
    
    # Row 5: Final variations
    create_external_overlapping_square(ctx, 150, 880, 110, "ULTIMATE!", "alternating")
    create_external_bubble_square(ctx, 350, 880, 110, "SUPREME!", 7)
    create_external_overlapping_square(ctx, 550, 880, 110, "MAXIMUM!", "all_sides")
    create_external_bubble_square(ctx, 750, 880, 110, "EXTREME!", 12)
    create_external_overlapping_square(ctx, 950, 880, 110, "PERFECT!", "sides_corners")
    
    # Title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(30)
    ctx.set_source_rgb(0.2, 0.2, 0.4)
    ctx.move_to(300, 50)
    ctx.show_text("EXTERNAL OVERLAPPING SHAPES")
    
    # Subtitle
    ctx.set_font_size(16)
    ctx.move_to(430, 80)
    ctx.show_text("Outside the Square, Overlapping Edges")
    
    surface.write_to_png("external_overlapping_squares.png")
    print("✅ External overlapping squares saved as 'external_overlapping_squares.png'")

if __name__ == "__main__":
    create_external_overlap_demo()
    print("🟦 Created squares with EXTERNAL overlapping ovals! They're outside but touching! 🔵✨")