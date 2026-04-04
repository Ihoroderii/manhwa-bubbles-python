import cairo
import math
import random

def create_smooth_square_bubble(ctx, cx, cy, size, text="SQUARE!", corner_style="strict", edge_style="smooth"):
    """Create a smooth square bubble with strict corners but flowing edges"""
    
    # Calculate square corners (strict positioning)
    half_size = size / 2
    corners = [
        (cx - half_size, cy - half_size),  # Top-left
        (cx + half_size, cy - half_size),  # Top-right  
        (cx + half_size, cy + half_size),  # Bottom-right
        (cx - half_size, cy + half_size)   # Bottom-left
    ]
    
    # Generate smooth edges between strict corners
    points = generate_smooth_square_edges(corners, edge_style)
    
    # Draw the smooth square
    draw_smooth_square_path(ctx, points, corners, corner_style)
    
    # Fill with gradient
    draw_square_gradient(ctx, cx, cy, size)
    
    # Smooth outline
    draw_square_outline(ctx, points, corners)
    
    # Add text
    draw_square_text(ctx, cx, cy, text)

def generate_smooth_square_edges(corners, edge_style):
    """Generate smooth points along edges between strict corners"""
    
    all_points = []
    
    for i in range(4):  # 4 edges
        start_corner = corners[i]
        end_corner = corners[(i + 1) % 4]
        
        # Generate smooth points along this edge
        edge_points = generate_edge_points(start_corner, end_corner, edge_style)
        all_points.extend(edge_points)
    
    return all_points

def generate_edge_points(start, end, style):
    """Generate smooth points along one edge"""
    
    points = []
    num_points = 15  # Points per edge for smoothness
    
    for i in range(num_points):
        # Base position along straight edge
        t = i / (num_points - 1)
        base_x = start[0] + t * (end[0] - start[0])
        base_y = start[1] + t * (end[1] - start[1])
        
        # Calculate edge direction
        edge_length = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        if edge_length > 0:
            # Normal vector to edge (for displacement)
            normal_x = -(end[1] - start[1]) / edge_length
            normal_y = (end[0] - start[0]) / edge_length
        else:
            normal_x, normal_y = 0, 0
        
        # Apply smooth displacement based on style
        if style == "smooth":
            # Gentle sine wave displacement
            displacement = 8 * math.sin(t * math.pi * 2) * math.sin(t * math.pi)
        elif style == "wavy":
            # More pronounced waves
            displacement = 12 * math.sin(t * math.pi * 3) * math.sin(t * math.pi)
        elif style == "energy":
            # Energy-like fluctuations
            displacement = 10 * (math.sin(t * math.pi * 4) + 0.5 * math.sin(t * math.pi * 8))
        elif style == "flowing":
            # Flowing organic pattern
            displacement = 6 * math.sin(t * math.pi) * (1 + 0.3 * math.sin(t * math.pi * 6))
        else:  # minimal
            # Very subtle smoothness
            displacement = 3 * math.sin(t * math.pi)
        
        # Apply displacement normal to edge
        smooth_x = base_x + normal_x * displacement
        smooth_y = base_y + normal_y * displacement
        
        points.append((smooth_x, smooth_y))
    
    return points[:-1]  # Remove last point to avoid duplication at corners

def draw_smooth_square_path(ctx, points, corners, corner_style):
    """Draw the smooth square path with strict corners"""
    
    if not points:
        return
    
    ctx.move_to(*points[0])
    
    # Draw smooth curves through all points
    points_per_edge = len(points) // 4
    
    for edge in range(4):
        start_idx = edge * points_per_edge
        end_idx = ((edge + 1) * points_per_edge) if edge < 3 else len(points)
        edge_points = points[start_idx:end_idx]
        
        # Draw smooth curve through edge points
        if len(edge_points) >= 2:
            for i in range(len(edge_points)):
                current = edge_points[i]
                next_point = edge_points[(i + 1) % len(edge_points)] if i < len(edge_points) - 1 else points[(start_idx + len(edge_points)) % len(points)]
                
                if corner_style == "strict":
                    # Approach corners more directly for strict positioning
                    corner_distance = min(
                        math.sqrt((current[0] - corners[edge][0])**2 + (current[1] - corners[edge][1])**2),
                        math.sqrt((current[0] - corners[(edge + 1) % 4][0])**2 + (current[1] - corners[(edge + 1) % 4][1])**2)
                    )
                    
                    if corner_distance < 20:  # Near corner - be more strict
                        ctx.line_to(*current)
                    else:  # Away from corner - be smooth
                        if i > 0:
                            prev_point = edge_points[i - 1]
                            # Control points for smooth curve
                            cp1_x = prev_point[0] + (current[0] - prev_point[0]) * 0.5
                            cp1_y = prev_point[1] + (current[1] - prev_point[1]) * 0.5
                            cp2_x = current[0] - (next_point[0] - prev_point[0]) * 0.3
                            cp2_y = current[1] - (next_point[1] - prev_point[1]) * 0.3
                            
                            ctx.curve_to(cp1_x, cp1_y, cp2_x, cp2_y, current[0], current[1])
                        else:
                            ctx.line_to(*current)
                else:  # rounded corners
                    # Standard smooth curves everywhere
                    if i > 0 and i < len(edge_points) - 1:
                        prev_point = edge_points[i - 1]
                        # Smooth curve
                        cp1_x = prev_point[0] + (current[0] - prev_point[0]) * 0.4
                        cp1_y = prev_point[1] + (current[1] - prev_point[1]) * 0.4
                        cp2_x = current[0] - (next_point[0] - prev_point[0]) * 0.4
                        cp2_y = current[1] - (next_point[1] - prev_point[1]) * 0.4
                        
                        ctx.curve_to(cp1_x, cp1_y, cp2_x, cp2_y, current[0], current[1])
                    else:
                        ctx.line_to(*current)
    
    ctx.close_path()

def draw_square_gradient(ctx, cx, cy, size):
    """Create gradient fill for square bubble"""
    
    # Square gradient from center
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, size * 0.7)
    
    # Cool square colors
    gradient.add_color_stop_rgb(0.0, 1.0, 1.0, 1.0)     # White center
    gradient.add_color_stop_rgb(0.3, 0.95, 0.95, 1.0)   # Light blue
    gradient.add_color_stop_rgb(0.6, 0.85, 0.9, 1.0)    # Blue
    gradient.add_color_stop_rgb(1.0, 0.7, 0.8, 0.95)    # Purple edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()

def draw_square_outline(ctx, points, corners):
    """Draw outline emphasizing the square structure"""
    
    # Main outline
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2.5)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke_preserve()
    
    # Emphasize corners with small marks
    for corner in corners:
        ctx.set_source_rgb(0, 0, 0)
        ctx.arc(corner[0], corner[1], 2, 0, 2 * math.pi)
        ctx.fill()
    
    ctx.new_path()

def create_rectangular_action_bubble(ctx, cx, cy, width, height, text="RECT!", orientation="horizontal"):
    """Create smooth rectangular action bubble with strict corners"""
    
    # Calculate rectangle corners
    half_w, half_h = width / 2, height / 2
    corners = [
        (cx - half_w, cy - half_h),  # Top-left
        (cx + half_w, cy - half_h),  # Top-right
        (cx + half_w, cy + half_h),  # Bottom-right
        (cx - half_w, cy + half_h)   # Bottom-left
    ]
    
    # Generate action-style smooth edges
    points = []
    
    for i in range(4):
        start_corner = corners[i]
        end_corner = corners[(i + 1) % 4]
        
        # Edge points with action energy
        edge_points = []
        num_points = 20
        
        for j in range(num_points):
            t = j / (num_points - 1)
            base_x = start_corner[0] + t * (end_corner[0] - start_corner[0])
            base_y = start_corner[1] + t * (end_corner[1] - start_corner[1])
            
            # Action energy displacement
            edge_length = math.sqrt((end_corner[0] - start_corner[0])**2 + (end_corner[1] - start_corner[1])**2)
            if edge_length > 0:
                normal_x = -(end_corner[1] - start_corner[1]) / edge_length
                normal_y = (end_corner[0] - start_corner[0]) / edge_length
            else:
                normal_x, normal_y = 0, 0
            
            # Action-style energy waves
            if orientation == "horizontal" and i in [0, 2]:  # Top and bottom edges
                energy = 8 * math.sin(t * math.pi * 4) * math.sin(t * math.pi)
            elif orientation == "vertical" and i in [1, 3]:  # Left and right edges
                energy = 8 * math.sin(t * math.pi * 4) * math.sin(t * math.pi)
            else:
                energy = 5 * math.sin(t * math.pi * 2) * math.sin(t * math.pi)
            
            action_x = base_x + normal_x * energy
            action_y = base_y + normal_y * energy
            
            edge_points.append((action_x, action_y))
        
        points.extend(edge_points[:-1])
    
    # Draw action rectangle
    ctx.move_to(*points[0])
    for point in points[1:]:
        ctx.line_to(*point)
    ctx.close_path()
    
    # Action gradient
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, max(width, height) * 0.6)
    gradient.add_color_stop_rgb(0, 1.0, 1.0, 0.9)      # Light center
    gradient.add_color_stop_rgb(0.5, 1.0, 0.9, 0.6)    # Yellow
    gradient.add_color_stop_rgb(1, 0.9, 0.7, 0.3)      # Orange edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Outline
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(3)
    ctx.stroke()
    
    # Mark strict corners
    for corner in corners:
        ctx.set_source_rgb(0, 0, 0)
        ctx.arc(corner[0], corner[1], 3, 0, 2 * math.pi)
        ctx.fill()
    
    # Add text
    draw_square_text(ctx, cx, cy, text)

def draw_square_text(ctx, cx, cy, text):
    """Draw text in square bubble"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(14)
    
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

def create_smooth_square_demo():
    """Create demo with smooth squares having strict corners"""
    
    random.seed(777)
    
    WIDTH, HEIGHT = 1200, 900
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(0.97, 0.97, 0.99)
    ctx.paint()
    
    # Row 1: Different edge styles with strict corners
    create_smooth_square_bubble(ctx, 150, 150, 120, "SMOOTH!", "strict", "smooth")
    create_smooth_square_bubble(ctx, 400, 150, 120, "WAVY!", "strict", "wavy")
    create_smooth_square_bubble(ctx, 650, 150, 120, "ENERGY!", "strict", "energy")
    create_smooth_square_bubble(ctx, 900, 150, 120, "FLOWING!", "strict", "flowing")
    
    # Row 2: Rectangular action bubbles
    create_rectangular_action_bubble(ctx, 200, 350, 160, 100, "HORIZONTAL!", "horizontal")
    create_rectangular_action_bubble(ctx, 500, 350, 120, 140, "VERTICAL!", "vertical")
    create_rectangular_action_bubble(ctx, 800, 350, 150, 110, "ACTION!", "horizontal")
    
    # Row 3: More square variations
    create_smooth_square_bubble(ctx, 150, 600, 110, "MINIMAL!", "strict", "minimal")
    create_smooth_square_bubble(ctx, 400, 600, 130, "STRICT!", "strict", "smooth")
    create_rectangular_action_bubble(ctx, 650, 600, 140, 120, "POWER!", "vertical")
    create_smooth_square_bubble(ctx, 900, 600, 115, "PERFECT!", "strict", "flowing")
    
    # Row 4: Large showcase
    create_smooth_square_bubble(ctx, 300, 780, 150, "MEGA SQUARE!", "strict", "energy")
    create_rectangular_action_bubble(ctx, 700, 780, 180, 130, "MEGA RECT!", "horizontal")
    
    # Title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(28)
    ctx.set_source_rgb(0.2, 0.2, 0.4)
    ctx.move_to(350, 50)
    ctx.show_text("SMOOTH SQUARES WITH STRICT CORNERS")
    
    surface.write_to_png("smooth_square_bubbles.png")
    print("✅ Smooth square bubbles saved as 'smooth_square_bubbles.png'")

if __name__ == "__main__":
    create_smooth_square_demo()
    print("🔷 Created smooth square bubbles with strict corners! Perfect geometry + organic flow! 📐✨")