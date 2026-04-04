import cairo
import math
import random

def create_faceted_corner_bubble(ctx, cx, cy, width, height, text="FACETED!", corner_segments=3, corner_length=15):
    """Create elongated bubble with multi-segmented faceted corners"""
    
    # Calculate the main rectangle dimensions
    half_w, half_h = width / 2, height / 2
    
    # Generate faceted corners instead of single corner points
    corner_points = generate_faceted_corners(cx, cy, half_w, half_h, corner_segments, corner_length)
    
    # Generate smooth edges between faceted corners
    all_points = generate_faceted_edges(corner_points)
    
    # Draw the faceted shape
    draw_faceted_path(ctx, all_points)
    
    # Fill with gradient
    draw_faceted_gradient(ctx, cx, cy, width, height)
    
    # Draw outline emphasizing facets
    draw_faceted_outline(ctx, all_points, corner_points)
    
    # Add text
    draw_faceted_text(ctx, cx, cy, text)

def generate_faceted_corners(cx, cy, half_w, half_h, segments, length):
    """Generate multiple corner points for each corner (faceted effect)"""
    
    all_corner_points = []
    
    # Define the four main corner regions
    main_corners = [
        (cx - half_w, cy - half_h),  # Top-left
        (cx + half_w, cy - half_h),  # Top-right
        (cx + half_w, cy + half_h),  # Bottom-right
        (cx - half_w, cy + half_h)   # Bottom-left
    ]
    
    for i, corner in enumerate(main_corners):
        corner_x, corner_y = corner
        
        # Generate multiple facet points for this corner
        facet_points = []
        
        if i == 0:  # Top-left corner
            # Create facets going from top edge to left edge
            for j in range(segments + 1):
                t = j / segments
                # Interpolate from (corner_x + length, corner_y) to (corner_x, corner_y + length)
                facet_x = corner_x + length * (1 - t)
                facet_y = corner_y + length * t
                facet_points.append((facet_x, facet_y))
                
        elif i == 1:  # Top-right corner
            # Create facets going from right edge to top edge
            for j in range(segments + 1):
                t = j / segments
                # Interpolate from (corner_x, corner_y + length) to (corner_x - length, corner_y)
                facet_x = corner_x - length * t
                facet_y = corner_y + length * (1 - t)
                facet_points.append((facet_x, facet_y))
                
        elif i == 2:  # Bottom-right corner
            # Create facets going from bottom edge to right edge
            for j in range(segments + 1):
                t = j / segments
                # Interpolate from (corner_x - length, corner_y) to (corner_x, corner_y - length)
                facet_x = corner_x - length * (1 - t)
                facet_y = corner_y - length * t
                facet_points.append((facet_x, facet_y))
                
        else:  # Bottom-left corner (i == 3)
            # Create facets going from left edge to bottom edge
            for j in range(segments + 1):
                t = j / segments
                # Interpolate from (corner_x, corner_y - length) to (corner_x + length, corner_y)
                facet_x = corner_x + length * t
                facet_y = corner_y - length * (1 - t)
                facet_points.append((facet_x, facet_y))
        
        all_corner_points.append(facet_points)
    
    return all_corner_points

def generate_faceted_edges(corner_points):
    """Generate smooth edges between faceted corners"""
    
    all_points = []
    
    for i in range(4):  # 4 edges
        current_corner_facets = corner_points[i]
        next_corner_facets = corner_points[(i + 1) % 4]
        
        # Start from the last facet of current corner
        start_point = current_corner_facets[-1]
        # End at the first facet of next corner
        end_point = next_corner_facets[0]
        
        # Add the current corner facets (except the last one to avoid duplication)
        all_points.extend(current_corner_facets[:-1])
        
        # Generate smooth edge points between corners
        edge_points = generate_smooth_edge_between_facets(start_point, end_point)
        all_points.extend(edge_points)
    
    return all_points

def generate_smooth_edge_between_facets(start, end):
    """Generate smooth wavy points between two faceted corners"""
    
    points = []
    num_points = 20  # Points along the edge
    
    for i in range(num_points):
        t = i / (num_points - 1)
        
        # Base position along straight edge
        base_x = start[0] + t * (end[0] - start[0])
        base_y = start[1] + t * (end[1] - start[1])
        
        # Calculate edge normal for wave displacement
        edge_length = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        if edge_length > 0:
            normal_x = -(end[1] - start[1]) / edge_length
            normal_y = (end[0] - start[0]) / edge_length
        else:
            normal_x, normal_y = 0, 0
        
        # Gentle wave displacement (casual style)
        wave1 = 6 * math.sin(t * math.pi * 2) * math.sin(t * math.pi)
        wave2 = 2 * math.sin(t * math.pi * 5) * (1 - abs(t - 0.5) * 2)
        displacement = wave1 + wave2
        
        # Add tiny randomness
        displacement += random.uniform(-0.5, 0.5)
        
        # Apply displacement
        smooth_x = base_x + normal_x * displacement
        smooth_y = base_y + normal_y * displacement
        
        points.append((smooth_x, smooth_y))
    
    return points[:-1]  # Remove last point to avoid duplication

def draw_faceted_path(ctx, points):
    """Draw path through all points with smooth curves"""
    
    if not points:
        return
    
    ctx.move_to(*points[0])
    
    # Draw smooth curves through all points
    for i in range(len(points)):
        current = points[i]
        next_point = points[(i + 1) % len(points)]
        prev_point = points[i - 1]
        next_next = points[(i + 2) % len(points)]
        
        # Smooth curve control points
        tension = 0.3
        cp1_x = current[0] + (next_point[0] - prev_point[0]) * tension * 0.4
        cp1_y = current[1] + (next_point[1] - prev_point[1]) * tension * 0.4
        cp2_x = next_point[0] - (next_next[0] - current[0]) * tension * 0.4
        cp2_y = next_point[1] - (next_next[1] - current[1]) * tension * 0.4
        
        ctx.curve_to(cp1_x, cp1_y, cp2_x, cp2_y, next_point[0], next_point[1])
    
    ctx.close_path()

def draw_faceted_gradient(ctx, cx, cy, width, height):
    """Create gradient for faceted bubble"""
    
    # Use linear gradient for elongated shapes
    gradient = cairo.LinearGradient(cx - width/2, cy - height/2, cx + width/2, cy + height/2)
    
    gradient.add_color_stop_rgb(0.0, 1.0, 1.0, 0.95)    # Light start
    gradient.add_color_stop_rgb(0.3, 0.95, 0.98, 1.0)   # Light blue
    gradient.add_color_stop_rgb(0.7, 0.88, 0.92, 0.98)  # Medium blue
    gradient.add_color_stop_rgb(1.0, 0.8, 0.85, 0.92)   # Darker end
    
    ctx.set_source(gradient)
    ctx.fill_preserve()

def draw_faceted_outline(ctx, all_points, corner_points):
    """Draw outline emphasizing the faceted corners"""
    
    # Main outline
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2.0)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke_preserve()
    
    # Emphasize facet lines
    ctx.set_source_rgba(0, 0, 0, 0.4)
    ctx.set_line_width(1.0)
    
    for corner_facets in corner_points:
        # Draw lines between facet points to show segmentation
        for i in range(len(corner_facets) - 1):
            ctx.move_to(*corner_facets[i])
            ctx.line_to(*corner_facets[i + 1])
            ctx.stroke()
    
    ctx.new_path()

def create_thin_elongated_bubble(ctx, cx, cy, length, thickness, text="THIN!", orientation="horizontal", segments=4):
    """Create very thin, elongated bubble with faceted corners"""
    
    if orientation == "horizontal":
        width, height = length, thickness
    else:  # vertical
        width, height = thickness, length
    
    # Use more corner segments for thin shapes
    corner_length = min(width, height) * 0.3  # Proportional to thickness
    
    create_faceted_corner_bubble(ctx, cx, cy, width, height, text, segments, corner_length)

def create_diamond_faceted_bubble(ctx, cx, cy, size, text="DIAMOND!", segments=3):
    """Create diamond-shaped bubble with faceted corners"""
    
    # Calculate diamond points
    half_size = size / 2
    diamond_points = [
        (cx, cy - half_size),      # Top
        (cx + half_size, cy),      # Right  
        (cx, cy + half_size),      # Bottom
        (cx - half_size, cy)       # Left
    ]
    
    # Generate faceted corners for diamond
    all_corner_points = []
    facet_length = size * 0.15
    
    for i, corner in enumerate(diamond_points):
        corner_x, corner_y = corner
        facet_points = []
        
        # Get adjacent points for faceting direction
        prev_corner = diamond_points[i - 1]
        next_corner = diamond_points[(i + 1) % 4]
        
        # Create facets between the two adjacent edges
        for j in range(segments + 1):
            t = j / segments
            
            # Direction vectors to adjacent corners
            to_prev_x = prev_corner[0] - corner_x
            to_prev_y = prev_corner[1] - corner_y
            prev_len = math.sqrt(to_prev_x**2 + to_prev_y**2)
            
            to_next_x = next_corner[0] - corner_x  
            to_next_y = next_corner[1] - corner_y
            next_len = math.sqrt(to_next_x**2 + to_next_y**2)
            
            if prev_len > 0 and next_len > 0:
                # Normalize direction vectors
                to_prev_x, to_prev_y = to_prev_x / prev_len, to_prev_y / prev_len
                to_next_x, to_next_y = to_next_x / next_len, to_next_y / next_len
                
                # Interpolate between the two directions
                dir_x = to_prev_x * (1 - t) + to_next_x * t
                dir_y = to_prev_y * (1 - t) + to_next_y * t
                
                # Normalize interpolated direction
                dir_len = math.sqrt(dir_x**2 + dir_y**2)
                if dir_len > 0:
                    dir_x, dir_y = dir_x / dir_len, dir_y / dir_len
                
                # Create facet point
                facet_x = corner_x + dir_x * facet_length
                facet_y = corner_y + dir_y * facet_length
                facet_points.append((facet_x, facet_y))
        
        all_corner_points.append(facet_points)
    
    # Generate edges between faceted corners
    all_points = generate_faceted_edges(all_corner_points)
    
    # Draw diamond
    draw_faceted_path(ctx, all_points)
    
    # Diamond gradient
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, size * 0.6)
    gradient.add_color_stop_rgb(0, 1.0, 0.98, 0.9)      # Golden center
    gradient.add_color_stop_rgb(0.5, 0.95, 0.9, 0.75)   # Gold
    gradient.add_color_stop_rgb(1, 0.85, 0.75, 0.55)    # Dark gold
    
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Outline
    draw_faceted_outline(ctx, all_points, all_corner_points)
    
    # Add text
    draw_faceted_text(ctx, cx, cy, text)

def draw_faceted_text(ctx, cx, cy, text):
    """Draw text in faceted bubble"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(12)
    
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    text_x = cx - text_width / 2
    text_y = cy + text_height / 2
    
    # Text shadow
    ctx.set_source_rgba(0, 0, 0, 0.3)
    ctx.move_to(text_x + 1, text_y + 1)
    ctx.show_text(text)
    
    # Main text
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_faceted_corners_demo():
    """Create demo with various faceted corner bubbles"""
    
    random.seed(999)
    
    WIDTH, HEIGHT = 1400, 1000
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(0.96, 0.96, 0.98)
    ctx.paint()
    
    # Row 1: Regular faceted rectangles with different corner segments
    create_faceted_corner_bubble(ctx, 150, 130, 160, 80, "3 FACETS!", 3, 12)
    create_faceted_corner_bubble(ctx, 400, 130, 160, 80, "4 FACETS!", 4, 12)
    create_faceted_corner_bubble(ctx, 650, 130, 160, 80, "5 FACETS!", 5, 12)
    create_faceted_corner_bubble(ctx, 900, 130, 160, 80, "6 FACETS!", 6, 12)
    
    # Row 2: Thin elongated horizontal bubbles
    create_thin_elongated_bubble(ctx, 200, 280, 220, 50, "THIN HORIZONTAL!", "horizontal", 3)
    create_thin_elongated_bubble(ctx, 600, 280, 240, 45, "SUPER THIN!", "horizontal", 4)
    create_thin_elongated_bubble(ctx, 1000, 280, 200, 55, "ELONGATED!", "horizontal", 5)
    
    # Row 3: Thin elongated vertical bubbles  
    create_thin_elongated_bubble(ctx, 150, 480, 180, 60, "VERTICAL!", "vertical", 3)
    create_thin_elongated_bubble(ctx, 350, 480, 200, 50, "TALL THIN!", "vertical", 4)
    create_thin_elongated_bubble(ctx, 550, 480, 160, 55, "TOWER!", "vertical", 5)
    create_thin_elongated_bubble(ctx, 750, 480, 190, 45, "SLIM!", "vertical", 6)
    create_thin_elongated_bubble(ctx, 950, 480, 170, 50, "NARROW!", "vertical", 3)
    
    # Row 4: Diamond shapes with faceted corners
    create_diamond_faceted_bubble(ctx, 150, 680, 120, "DIAMOND!", 3)
    create_diamond_faceted_bubble(ctx, 350, 680, 130, "FACETED!", 4)
    create_diamond_faceted_bubble(ctx, 550, 680, 125, "GEM!", 5)
    create_diamond_faceted_bubble(ctx, 750, 680, 135, "CRYSTAL!", 6)
    create_diamond_faceted_bubble(ctx, 950, 680, 115, "JEWEL!", 4)
    
    # Row 5: More variations
    create_faceted_corner_bubble(ctx, 200, 850, 180, 90, "BIG FACETS!", 6, 18)
    create_thin_elongated_bubble(ctx, 500, 850, 260, 40, "ULTRA THIN!", "horizontal", 4)
    create_faceted_corner_bubble(ctx, 850, 850, 140, 110, "CHUNKY!", 4, 20)
    
    # Title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(32)
    ctx.set_source_rgb(0.2, 0.2, 0.4)
    ctx.move_to(420, 50)
    ctx.show_text("FACETED CORNER BUBBLES")
    
    # Subtitle
    ctx.set_font_size(16)
    ctx.move_to(500, 80)
    ctx.show_text("Thin & Long with Segmented Corners")
    
    surface.write_to_png("faceted_corner_bubbles.png")
    print("✅ Faceted corner bubbles saved as 'faceted_corner_bubbles.png'")

if __name__ == "__main__":
    create_faceted_corners_demo()
    print("💎 Created faceted corner bubbles! Thin, long shapes with segmented corners! ✨📐")