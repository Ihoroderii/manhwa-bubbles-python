import cairo
import math
import random

def create_smooth_action_bubble(ctx, cx, cy, base_radius, text="POW!", intensity="medium"):
    """Create a smooth action bubble with flowing energy waves"""
    
    # Generate smooth action bubble points
    points = []
    num_waves = random.randint(8, 12)  # Number of energy waves
    
    for i in range(num_waves * 3):  # More points for smoother curves
        angle = 2 * math.pi * i / (num_waves * 3)
        
        # Create wave intensity based on style
        if intensity == "low":
            wave_factor = 1 + 0.3 * math.sin(angle * num_waves)
        elif intensity == "medium": 
            wave_factor = 1 + 0.5 * math.sin(angle * num_waves) + 0.2 * math.sin(angle * num_waves * 2)
        elif intensity == "high":
            wave_factor = 1 + 0.7 * math.sin(angle * num_waves) + 0.3 * math.sin(angle * num_waves * 1.5)
        else:  # explosive
            wave_factor = 1 + 0.9 * math.sin(angle * num_waves) + 0.4 * math.cos(angle * num_waves * 0.7)
        
        # Add smooth randomness
        smooth_variation = random.uniform(0.9, 1.1)
        radius = base_radius * wave_factor * smooth_variation
        
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    
    # Draw smooth action bubble
    draw_smooth_action_curve(ctx, points)
    
    # Gradient fill for energy effect
    draw_action_gradient_fill(ctx, cx, cy, base_radius)
    
    # Smooth outline with energy glow
    draw_action_outline(ctx, points, intensity)
    
    # Add dynamic text
    draw_action_text(ctx, cx, cy, text)

def draw_smooth_action_curve(ctx, points):
    """Draw ultra-smooth curves for action bubble"""
    
    if len(points) < 3:
        return
    
    ctx.move_to(*points[0])
    
    # Use smooth interpolation with varying tension
    for i in range(len(points)):
        current = points[i]
        next_point = points[(i + 1) % len(points)]
        prev_point = points[i - 1]
        next_next = points[(i + 2) % len(points)]
        
        # Dynamic tension for energy effect
        tension = 0.4 + 0.2 * math.sin(i * 0.5)
        
        # Calculate smooth control points
        cp1_x = current[0] + (next_point[0] - prev_point[0]) * tension * 0.3
        cp1_y = current[1] + (next_point[1] - prev_point[1]) * tension * 0.3
        cp2_x = next_point[0] - (next_next[0] - current[0]) * tension * 0.3
        cp2_y = next_point[1] - (next_next[1] - current[1]) * tension * 0.3
        
        ctx.curve_to(cp1_x, cp1_y, cp2_x, cp2_y, next_point[0], next_point[1])
    
    ctx.close_path()

def draw_action_gradient_fill(ctx, cx, cy, radius):
    """Create gradient fill for dynamic energy effect"""
    
    # Create radial gradient from center outward
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, radius)
    
    # Action bubble colors (bright energetic)
    gradient.add_color_stop_rgb(0, 1.0, 1.0, 0.9)    # Bright white center
    gradient.add_color_stop_rgb(0.3, 1.0, 0.95, 0.7)  # Light yellow
    gradient.add_color_stop_rgb(0.7, 1.0, 0.85, 0.5)  # Orange tint
    gradient.add_color_stop_rgb(1.0, 0.95, 0.8, 0.4)  # Golden edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()

def draw_action_outline(ctx, points, intensity):
    """Draw smooth outline with energy glow effect"""
    
    # Base outline
    base_width = 2.5 if intensity == "low" else 3.0 if intensity == "medium" else 3.5
    
    # Main outline
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(base_width)
    ctx.stroke_preserve()
    
    # Add energy glow layers
    glow_layers = 3 if intensity in ["medium", "high"] else 2
    
    for layer in range(glow_layers):
        glow_width = base_width + (layer + 1) * 1.5
        glow_alpha = 0.3 - layer * 0.1
        
        # Glow color (orange/yellow energy)
        ctx.set_source_rgba(1.0, 0.6, 0.2, glow_alpha)
        ctx.set_line_width(glow_width)
        ctx.stroke_preserve()
    
    # Clear the path
    ctx.new_path()

def create_smooth_burst_bubble(ctx, cx, cy, base_radius, text="BOOM!", burst_type="explosion"):
    """Create a smooth burst/explosion bubble with flowing energy"""
    
    # Generate burst pattern
    points = []
    
    if burst_type == "explosion":
        # Explosive radiating pattern
        num_bursts = 12
        for i in range(num_bursts):
            angle = 2 * math.pi * i / num_bursts
            
            # Create smooth explosion waves
            for sub_i in range(4):  # 4 points per burst for smoothness
                sub_angle = angle + (sub_i - 1.5) * 0.2
                
                if sub_i in [0, 3]:  # Inner points
                    radius = base_radius * 0.7
                else:  # Outer burst points
                    burst_intensity = 1.5 + 0.3 * math.sin(angle * 3)
                    radius = base_radius * burst_intensity
                
                x = cx + radius * math.cos(sub_angle)
                y = cy + radius * math.sin(sub_angle)
                points.append((x, y))
    
    elif burst_type == "energy":
        # Flowing energy pattern
        num_flows = 8
        for i in range(num_flows * 4):
            angle = 2 * math.pi * i / (num_flows * 4)
            
            # Smooth energy flow
            flow_factor = 1 + 0.6 * math.sin(angle * num_flows) * math.cos(angle * 2)
            radius = base_radius * flow_factor
            
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((x, y))
    
    # Draw the burst
    draw_smooth_action_curve(ctx, points)
    
    # Special burst gradient
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, base_radius * 1.5)
    if burst_type == "explosion":
        gradient.add_color_stop_rgb(0, 1.0, 0.9, 0.8)   # Bright center
        gradient.add_color_stop_rgb(0.5, 1.0, 0.7, 0.3)  # Orange
        gradient.add_color_stop_rgb(1.0, 0.9, 0.4, 0.1)  # Dark orange
    else:  # energy
        gradient.add_color_stop_rgb(0, 0.9, 0.9, 1.0)   # Light blue center
        gradient.add_color_stop_rgb(0.5, 0.7, 0.8, 1.0)  # Blue
        gradient.add_color_stop_rgb(1.0, 0.5, 0.6, 0.9)  # Purple edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Smooth outline
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(3)
    ctx.stroke()
    
    # Add text
    draw_action_text(ctx, cx, cy, text)

def draw_action_text(ctx, cx, cy, text):
    """Draw dynamic action text with effects"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(18)
    
    # Get text dimensions
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    # Center the text
    text_x = cx - text_width / 2
    text_y = cy + text_height / 2
    
    # Text shadow for pop effect
    ctx.set_source_rgba(0, 0, 0, 0.3)
    ctx.move_to(text_x + 2, text_y + 2)
    ctx.show_text(text)
    
    # Main text
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_smooth_action_demo():
    """Create a demo with various smooth action bubbles"""
    
    random.seed(456)  # For consistent results
    
    WIDTH, HEIGHT = 1000, 700
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Dynamic background
    ctx.set_source_rgb(0.95, 0.95, 0.98)
    ctx.paint()
    
    # Create various smooth action bubbles
    
    # Row 1: Different intensities
    create_smooth_action_bubble(ctx, 150, 140, 70, "POW!", "low")
    create_smooth_action_bubble(ctx, 350, 140, 75, "BAM!", "medium") 
    create_smooth_action_bubble(ctx, 550, 140, 80, "WHAM!", "high")
    create_smooth_action_bubble(ctx, 750, 140, 85, "BOOM!", "explosive")
    
    # Row 2: Different burst types
    create_smooth_burst_bubble(ctx, 200, 350, 80, "CRASH!", "explosion")
    create_smooth_burst_bubble(ctx, 450, 350, 75, "ZAP!", "energy")
    create_smooth_action_bubble(ctx, 700, 350, 85, "KAPOW!", "high")
    
    # Row 3: More variations
    random.seed(789)
    create_smooth_action_bubble(ctx, 150, 550, 75, "THUD!", "medium")
    create_smooth_burst_bubble(ctx, 400, 550, 80, "BLAST!", "explosion")
    create_smooth_action_bubble(ctx, 650, 550, 70, "SMASH!", "explosive")
    
    # Add title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(28)
    ctx.set_source_rgb(0.2, 0.2, 0.2)
    ctx.move_to(300, 50)
    ctx.show_text("Smooth Action Bubbles")
    
    surface.write_to_png("smooth_action_bubbles.png")
    print("✅ Smooth action bubbles saved as 'smooth_action_bubbles.png'")

if __name__ == "__main__":
    create_smooth_action_demo()
    print("💥 Created smooth action bubbles with flowing energy effects!")