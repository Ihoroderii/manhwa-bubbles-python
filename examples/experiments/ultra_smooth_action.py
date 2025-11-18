import cairo
import math
import random

def create_ultra_smooth_action_bubble(ctx, cx, cy, base_radius, text="POW!", smoothness="ultra"):
    """Create the smoothest possible action bubble with perfect curves"""
    
    # Generate ultra-smooth control points
    points = generate_ultra_smooth_points(cx, cy, base_radius, smoothness)
    
    # Draw with maximum smoothness
    draw_ultra_smooth_curve(ctx, points)
    
    # Ultra-smooth gradient fill
    draw_ultra_smooth_gradient(ctx, cx, cy, base_radius)
    
    # Perfect smooth outline
    draw_ultra_smooth_outline(ctx, points)
    
    # Smooth text
    draw_ultra_smooth_text(ctx, cx, cy, text)

def generate_ultra_smooth_points(cx, cy, radius, smoothness):
    """Generate points for ultra-smooth action bubble"""
    
    points = []
    
    if smoothness == "ultra":
        # Ultra-high point density for maximum smoothness
        num_points = 60  # Very high density
        
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            
            # Multiple smooth wave layers for ultra-smooth energy
            wave1 = 0.15 * math.sin(angle * 4)      # Primary energy wave
            wave2 = 0.08 * math.sin(angle * 8)      # Secondary detail
            wave3 = 0.04 * math.sin(angle * 12)     # Fine smoothness
            wave4 = 0.02 * math.cos(angle * 16)     # Ultra-fine detail
            
            # Combine waves for ultra-smooth energy effect
            energy_factor = 1 + wave1 + wave2 + wave3 + wave4
            
            # Add gentle randomness for natural feel
            natural_variation = random.uniform(0.98, 1.02)
            
            final_radius = radius * energy_factor * natural_variation
            
            x = cx + final_radius * math.cos(angle)
            y = cy + final_radius * math.sin(angle)
            points.append((x, y))
    
    elif smoothness == "silk":
        # Silk-smooth with flowing patterns
        num_points = 48
        
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            
            # Silk-like flowing pattern
            flow1 = 0.2 * math.sin(angle * 3 + math.pi/4)
            flow2 = 0.1 * math.sin(angle * 6 + math.pi/2)
            flow3 = 0.05 * math.cos(angle * 9)
            
            energy_factor = 1 + flow1 + flow2 + flow3
            
            # Ultra-gentle variation
            silk_variation = 1 + 0.01 * math.sin(angle * 20)
            
            final_radius = radius * energy_factor * silk_variation
            
            x = cx + final_radius * math.cos(angle)
            y = cy + final_radius * math.sin(angle)
            points.append((x, y))
    
    return points

def draw_ultra_smooth_curve(ctx, points):
    """Draw the smoothest possible curve using advanced spline interpolation"""
    
    if len(points) < 4:
        return
    
    ctx.move_to(*points[0])
    
    # Use Catmull-Rom splines with ultra-high precision
    for i in range(len(points)):
        # Get surrounding points
        p0 = points[i-2] if i >= 2 else points[-2]
        p1 = points[i-1] if i >= 1 else points[-1]
        p2 = points[i]
        p3 = points[(i+1) % len(points)]
        
        # Ultra-smooth tension (perfect balance)
        tension = 0.5
        
        # Calculate perfect control points for maximum smoothness
        cp1_x = p1[0] + (p2[0] - p0[0]) * tension / 6
        cp1_y = p1[1] + (p2[1] - p0[1]) * tension / 6
        cp2_x = p2[0] - (p3[0] - p1[0]) * tension / 6
        cp2_y = p2[1] - (p3[1] - p1[1]) * tension / 6
        
        # Draw ultra-smooth curve segment
        ctx.curve_to(cp1_x, cp1_y, cp2_x, cp2_y, p2[0], p2[1])
    
    ctx.close_path()

def draw_ultra_smooth_gradient(ctx, cx, cy, radius):
    """Create ultra-smooth gradient with perfect transitions"""
    
    # Create ultra-smooth radial gradient
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, radius * 1.2)
    
    # Ultra-smooth color transitions (more stops = smoother)
    gradient.add_color_stop_rgb(0.0, 1.0, 1.0, 0.95)    # Pure white center
    gradient.add_color_stop_rgb(0.15, 1.0, 0.98, 0.85)  # Subtle cream
    gradient.add_color_stop_rgb(0.35, 1.0, 0.92, 0.75)  # Light yellow
    gradient.add_color_stop_rgb(0.55, 1.0, 0.85, 0.60)  # Warm yellow
    gradient.add_color_stop_rgb(0.75, 1.0, 0.75, 0.45)  # Orange
    gradient.add_color_stop_rgb(0.90, 0.95, 0.65, 0.35) # Deep orange
    gradient.add_color_stop_rgb(1.0, 0.85, 0.55, 0.25)  # Golden edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()

def draw_ultra_smooth_outline(ctx, points):
    """Draw ultra-smooth outline with perfect anti-aliasing"""
    
    # Main outline with perfect smoothness
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2.5)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)  # Ultra-smooth line caps
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)  # Ultra-smooth joins
    ctx.stroke_preserve()
    
    # Ultra-smooth glow layers
    glow_colors = [
        (1.0, 0.8, 0.4, 0.25),  # Golden glow
        (1.0, 0.6, 0.2, 0.15),  # Orange glow
        (1.0, 0.4, 0.1, 0.08),  # Deep orange glow
    ]
    
    for i, (r, g, b, a) in enumerate(glow_colors):
        ctx.set_source_rgba(r, g, b, a)
        ctx.set_line_width(2.5 + (i + 1) * 1.5)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke_preserve()
    
    ctx.new_path()

def create_butter_smooth_bubble(ctx, cx, cy, radius, text="SMOOTH!", pattern="waves"):
    """Create a butter-smooth action bubble with flowing patterns"""
    
    points = []
    num_points = 72  # Ultra-high density for butter smoothness
    
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        
        if pattern == "waves":
            # Gentle wave pattern
            energy = 1 + 0.12 * math.sin(angle * 5) + 0.06 * math.sin(angle * 10)
        elif pattern == "flow":
            # Flowing energy pattern
            energy = 1 + 0.15 * math.sin(angle * 3) + 0.08 * math.cos(angle * 7)
        elif pattern == "pulse":
            # Pulsing energy pattern
            energy = 1 + 0.18 * math.sin(angle * 4) * math.cos(angle * 2)
        else:  # ripple
            # Ripple effect
            energy = 1 + 0.1 * math.sin(angle * 6) + 0.05 * math.sin(angle * 12)
        
        # Ultra-gentle variation
        smooth_var = 1 + 0.005 * math.sin(angle * 24)
        
        final_radius = radius * energy * smooth_var
        
        x = cx + final_radius * math.cos(angle)
        y = cy + final_radius * math.sin(angle)
        points.append((x, y))
    
    # Draw butter-smooth curve
    draw_ultra_smooth_curve(ctx, points)
    
    # Butter-smooth gradient
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, radius)
    gradient.add_color_stop_rgb(0, 0.95, 0.95, 1.0)     # Light blue center
    gradient.add_color_stop_rgb(0.3, 0.85, 0.9, 1.0)    # Soft blue
    gradient.add_color_stop_rgb(0.6, 0.75, 0.85, 0.95)  # Blue-gray
    gradient.add_color_stop_rgb(1, 0.65, 0.75, 0.85)    # Soft edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Ultra-smooth outline
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.stroke()
    
    # Add text
    draw_ultra_smooth_text(ctx, cx, cy, text)

def draw_ultra_smooth_text(ctx, cx, cy, text):
    """Draw text with ultra-smooth rendering"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(16)
    
    # Enable font smoothing
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    
    # Get text dimensions
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    # Perfect centering
    text_x = cx - text_width / 2
    text_y = cy + text_height / 2
    
    # Ultra-smooth text shadow
    ctx.set_source_rgba(0, 0, 0, 0.2)
    ctx.move_to(text_x + 1.5, text_y + 1.5)
    ctx.show_text(text)
    
    # Main text with perfect smoothness
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_ultra_smooth_demo():
    """Create demo with the smoothest possible action bubbles"""
    
    random.seed(999)  # For consistent ultra-smoothness
    
    WIDTH, HEIGHT = 1200, 800
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Enable maximum anti-aliasing
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    
    # Ultra-smooth background
    ctx.set_source_rgb(0.98, 0.98, 1.0)
    ctx.paint()
    
    # Row 1: Ultra-smooth action bubbles
    create_ultra_smooth_action_bubble(ctx, 150, 150, 70, "ULTRA!", "ultra")
    create_ultra_smooth_action_bubble(ctx, 400, 150, 75, "SMOOTH!", "silk")
    create_ultra_smooth_action_bubble(ctx, 650, 150, 80, "PERFECT!", "ultra")
    create_ultra_smooth_action_bubble(ctx, 900, 150, 75, "SILK!", "silk")
    
    # Row 2: Butter-smooth bubbles with different patterns
    create_butter_smooth_bubble(ctx, 200, 400, 80, "WAVES!", "waves")
    create_butter_smooth_bubble(ctx, 500, 400, 85, "FLOW!", "flow")
    create_butter_smooth_bubble(ctx, 800, 400, 80, "PULSE!", "pulse")
    
    # Row 3: Maximum smoothness
    create_butter_smooth_bubble(ctx, 150, 650, 75, "RIPPLE!", "ripple")
    create_ultra_smooth_action_bubble(ctx, 400, 650, 85, "MAXIMUM!", "ultra")
    create_butter_smooth_bubble(ctx, 650, 650, 80, "BUTTER!", "waves")
    create_ultra_smooth_action_bubble(ctx, 900, 650, 75, "SILKY!", "silk")
    
    # Ultra-smooth title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(32)
    ctx.set_source_rgb(0.1, 0.1, 0.3)
    ctx.move_to(350, 60)
    ctx.show_text("ULTRA SMOOTH ACTION BUBBLES")
    
    surface.write_to_png("ultra_smooth_action.png")
    print("✅ Ultra-smooth action bubbles saved as 'ultra_smooth_action.png'")

if __name__ == "__main__":
    create_ultra_smooth_demo()
    print("🌟 Created the SMOOTHEST action bubbles possible! Like butter! 🧈✨")