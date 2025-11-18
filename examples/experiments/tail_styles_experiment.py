"""
Experimental script for different bubble tail styles using Cairo.
Demonstrates various tail designs for speech bubbles.
"""

import cairo
import math
import random

# Canvas settings
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 1600
BUBBLE_RADIUS_X = 80
BUBBLE_RADIUS_Y = 60
TAIL_LENGTH = 50

def draw_base_bubble(ctx, cx, cy, rx, ry):
    """Draw a base elliptical bubble"""
    ctx.arc(cx, cy, rx, 0, 2 * math.pi)
    ctx.set_source_rgb(1, 1, 1)  # White fill
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)  # Black outline
    ctx.set_line_width(2)
    ctx.stroke()

# ============================================================================
# TAIL STYLE 1: Classic Smooth Tail (Curved Bezier)
# ============================================================================

def tail_classic_smooth(ctx, attach_x, attach_y, direction="bottom", length=50, width=20):
    """Classic smooth curved tail using Bezier curves"""
    if direction == "bottom":
        tip_x, tip_y = attach_x, attach_y + length
        left_x, left_y = attach_x - width/2, attach_y
        right_x, right_y = attach_x + width/2, attach_y
        
        ctx.move_to(left_x, left_y)
        ctx.curve_to(
            attach_x - width/4, attach_y + length/3,
            attach_x - width/6, attach_y + length*2/3,
            tip_x, tip_y
        )
        ctx.curve_to(
            attach_x + width/6, attach_y + length*2/3,
            attach_x + width/4, attach_y + length/3,
            right_x, right_y
        )
    elif direction == "top":
        tip_x, tip_y = attach_x, attach_y - length
        left_x, left_y = attach_x - width/2, attach_y
        right_x, right_y = attach_x + width/2, attach_y
        
        ctx.move_to(left_x, left_y)
        ctx.curve_to(
            attach_x - width/4, attach_y - length/3,
            attach_x - width/6, attach_y - length*2/3,
            tip_x, tip_y
        )
        ctx.curve_to(
            attach_x + width/6, attach_y - length*2/3,
            attach_x + width/4, attach_y - length/3,
            right_x, right_y
        )
    elif direction == "left":
        tip_x, tip_y = attach_x - length, attach_y
        top_x, top_y = attach_x, attach_y - width/2
        bottom_x, bottom_y = attach_x, attach_y + width/2
        
        ctx.move_to(top_x, top_y)
        ctx.curve_to(
            attach_x - length/3, attach_y - width/4,
            attach_x - length*2/3, attach_y - width/6,
            tip_x, tip_y
        )
        ctx.curve_to(
            attach_x - length*2/3, attach_y + width/6,
            attach_x - length/3, attach_y + width/4,
            bottom_x, bottom_y
        )
    else:  # right
        tip_x, tip_y = attach_x + length, attach_y
        top_x, top_y = attach_x, attach_y - width/2
        bottom_x, bottom_y = attach_x, attach_y + width/2
        
        ctx.move_to(top_x, top_y)
        ctx.curve_to(
            attach_x + length/3, attach_y - width/4,
            attach_x + length*2/3, attach_y - width/6,
            tip_x, tip_y
        )
        ctx.curve_to(
            attach_x + length*2/3, attach_y + width/6,
            attach_x + length/3, attach_y + width/4,
            bottom_x, bottom_y
        )
    
    ctx.close_path()
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()

# ============================================================================
# TAIL STYLE 2: Sharp Pointed Tail (Triangle)
# ============================================================================

def tail_sharp_pointed(ctx, attach_x, attach_y, direction="bottom", length=50, width=25):
    """Sharp triangular tail"""
    if direction == "bottom":
        tip = (attach_x, attach_y + length)
        left = (attach_x - width/2, attach_y)
        right = (attach_x + width/2, attach_y)
    elif direction == "top":
        tip = (attach_x, attach_y - length)
        left = (attach_x - width/2, attach_y)
        right = (attach_x + width/2, attach_y)
    elif direction == "left":
        tip = (attach_x - length, attach_y)
        left = (attach_x, attach_y - width/2)
        right = (attach_x, attach_y + width/2)
    else:  # right
        tip = (attach_x + length, attach_y)
        left = (attach_x, attach_y - width/2)
        right = (attach_x, attach_y + width/2)
    
    ctx.move_to(*tip)
    ctx.line_to(*left)
    ctx.line_to(*right)
    ctx.close_path()
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()

# ============================================================================
# TAIL STYLE 3: Wavy Tail
# ============================================================================

def tail_wavy(ctx, attach_x, attach_y, direction="bottom", length=50, width=20, waves=3):
    """Wavy/serpentine tail"""
    points = []
    steps = 30
    
    if direction == "bottom":
        for i in range(steps + 1):
            t = i / steps
            x = attach_x + (width/2) * math.sin(t * waves * math.pi)
            y = attach_y + t * length
            points.append((x, y))
    elif direction == "top":
        for i in range(steps + 1):
            t = i / steps
            x = attach_x + (width/2) * math.sin(t * waves * math.pi)
            y = attach_y - t * length
            points.append((x, y))
    elif direction == "left":
        for i in range(steps + 1):
            t = i / steps
            x = attach_x - t * length
            y = attach_y + (width/2) * math.sin(t * waves * math.pi)
            points.append((x, y))
    else:  # right
        for i in range(steps + 1):
            t = i / steps
            x = attach_x + t * length
            y = attach_y + (width/2) * math.sin(t * waves * math.pi)
            points.append((x, y))
    
    # Create closed path
    ctx.move_to(*points[0])
    for p in points[1:]:
        ctx.line_to(*p)
    
    # Mirror for other side
    if direction in ["bottom", "top"]:
        for p in reversed(points):
            ctx.line_to(2*attach_x - p[0], p[1])
    else:
        for p in reversed(points):
            ctx.line_to(p[0], 2*attach_y - p[1])
    
    ctx.close_path()
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()

# ============================================================================
# TAIL STYLE 4: Jagged/Spiky Tail
# ============================================================================

def tail_jagged(ctx, attach_x, attach_y, direction="bottom", length=50, width=25, spikes=5):
    """Jagged/spiky tail with multiple points"""
    points = []
    
    if direction == "bottom":
        # Left side
        for i in range(spikes + 1):
            t = i / spikes
            x = attach_x - width/2 + (width if i % 2 == 0 else 0)
            y = attach_y + t * length
            points.append((x, y))
        # Right side (mirror)
        for i in range(spikes, -1, -1):
            t = i / spikes
            x = attach_x + width/2 - (width if i % 2 == 0 else 0)
            y = attach_y + t * length
            points.append((x, y))
    elif direction == "top":
        for i in range(spikes + 1):
            t = i / spikes
            x = attach_x - width/2 + (width if i % 2 == 0 else 0)
            y = attach_y - t * length
            points.append((x, y))
        for i in range(spikes, -1, -1):
            t = i / spikes
            x = attach_x + width/2 - (width if i % 2 == 0 else 0)
            y = attach_y - t * length
            points.append((x, y))
    elif direction == "left":
        for i in range(spikes + 1):
            t = i / spikes
            x = attach_x - t * length
            y = attach_y - width/2 + (width if i % 2 == 0 else 0)
            points.append((x, y))
        for i in range(spikes, -1, -1):
            t = i / spikes
            x = attach_x - t * length
            y = attach_y + width/2 - (width if i % 2 == 0 else 0)
            points.append((x, y))
    else:  # right
        for i in range(spikes + 1):
            t = i / spikes
            x = attach_x + t * length
            y = attach_y - width/2 + (width if i % 2 == 0 else 0)
            points.append((x, y))
        for i in range(spikes, -1, -1):
            t = i / spikes
            x = attach_x + t * length
            y = attach_y + width/2 - (width if i % 2 == 0 else 0)
            points.append((x, y))
    
    ctx.move_to(*points[0])
    for p in points[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()

# ============================================================================
# TAIL STYLE 5: Double Tail (Split)
# ============================================================================

def tail_double_split(ctx, attach_x, attach_y, direction="bottom", length=50, width=20, split_offset=15):
    """Double tail that splits into two"""
    if direction == "bottom":
        # Left tail
        left_tip = (attach_x - split_offset, attach_y + length)
        left_left = (attach_x - width/2, attach_y)
        left_right = (attach_x - width/4, attach_y)
        
        ctx.move_to(*left_left)
        ctx.line_to(*left_tip)
        ctx.line_to(*left_right)
        ctx.close_path()
        
        # Right tail
        right_tip = (attach_x + split_offset, attach_y + length)
        right_left = (attach_x + width/4, attach_y)
        right_right = (attach_x + width/2, attach_y)
        
        ctx.move_to(*right_left)
        ctx.line_to(*right_tip)
        ctx.line_to(*right_right)
        ctx.close_path()
    elif direction == "top":
        left_tip = (attach_x - split_offset, attach_y - length)
        right_tip = (attach_x + split_offset, attach_y - length)
        # Similar logic but upward
        ctx.move_to(attach_x - width/2, attach_y)
        ctx.line_to(*left_tip)
        ctx.line_to(attach_x - width/4, attach_y)
        ctx.close_path()
        ctx.move_to(attach_x + width/4, attach_y)
        ctx.line_to(*right_tip)
        ctx.line_to(attach_x + width/2, attach_y)
        ctx.close_path()
    # Similar for left/right directions...
    
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()

# ============================================================================
# TAIL STYLE 6: Curved Hook Tail
# ============================================================================

def tail_curved_hook(ctx, attach_x, attach_y, direction="bottom", length=50, width=20, hook_angle=30):
    """Curved tail that hooks at the end"""
    hook_rad = math.radians(hook_angle)
    
    if direction == "bottom":
        # Main tail path
        tip_x = attach_x
        tip_y = attach_y + length * 0.7
        
        # Hook end
        hook_x = tip_x + length * 0.3 * math.cos(hook_rad)
        hook_y = tip_y + length * 0.3 * math.sin(hook_rad)
        
        left = (attach_x - width/2, attach_y)
        right = (attach_x + width/2, attach_y)
        
        ctx.move_to(*left)
        ctx.curve_to(
            attach_x - width/4, attach_y + length/3,
            attach_x - width/6, tip_y,
            tip_x, tip_y
        )
        ctx.curve_to(
            attach_x + width/6, tip_y,
            attach_x + width/4, attach_y + length/3,
            *right
        )
        # Add hook
        ctx.line_to(hook_x, hook_y)
        ctx.close_path()
    
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()

# ============================================================================
# TAIL STYLE 7: Bubbly Tail (Multiple Small Bubbles)
# ============================================================================

def tail_bubbly(ctx, attach_x, attach_y, direction="bottom", length=50, width=20, num_bubbles=3):
    """Tail made of connected small bubbles"""
    bubble_size = length / (num_bubbles + 1)
    
    if direction == "bottom":
        for i in range(num_bubbles):
            bubble_y = attach_y + (i + 1) * bubble_size
            bubble_x = attach_x + (width/2) * math.sin(i * math.pi / num_bubbles)
            ctx.arc(bubble_x, bubble_y, bubble_size/2, 0, 2*math.pi)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill_preserve()
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(2)
            ctx.stroke()
            
            # Connect bubbles
            if i > 0:
                prev_y = attach_y + i * bubble_size
                prev_x = attach_x + (width/2) * math.sin((i-1) * math.pi / num_bubbles)
                ctx.move_to(prev_x, prev_y + bubble_size/2)
                ctx.line_to(bubble_x, bubble_y - bubble_size/2)
                ctx.set_source_rgb(0, 0, 0)
                ctx.set_line_width(2)
                ctx.stroke()

# ============================================================================
# TAIL STYLE 8: Thick Bold Tail
# ============================================================================

def tail_thick_bold(ctx, attach_x, attach_y, direction="bottom", length=50, width=30):
    """Thick, bold tail with rounded end"""
    if direction == "bottom":
        tip_x, tip_y = attach_x, attach_y + length
        
        # Rounded tip
        ctx.arc(tip_x, tip_y, width/3, 0, 2*math.pi)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(3)
        ctx.stroke()
        
        # Main body
        left = (attach_x - width/2, attach_y)
        right = (attach_x + width/2, attach_y)
        
        ctx.move_to(*left)
        ctx.curve_to(
            attach_x - width/3, attach_y + length/2,
            tip_x - width/3, tip_y - width/3,
            tip_x - width/3, tip_y
        )
        ctx.arc_negative(tip_x, tip_y, width/3, math.pi, 0)
        ctx.curve_to(
            tip_x + width/3, tip_y - width/3,
            attach_x + width/3, attach_y + length/2,
            *right
        )
        ctx.close_path()
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(3)
        ctx.stroke()

# ============================================================================
# TAIL STYLE 9: Energy Tail (Radiating Lines)
# ============================================================================

def tail_energy_lines(ctx, attach_x, attach_y, direction="bottom", length=50, width=25, num_lines=8):
    """Tail with radiating energy lines"""
    if direction == "bottom":
        tip_x, tip_y = attach_x, attach_y + length
        
        # Main tail shape
        left = (attach_x - width/2, attach_y)
        right = (attach_x + width/2, attach_y)
        
        ctx.move_to(*left)
        ctx.line_to(tip_x - width/4, tip_y)
        ctx.line_to(*right)
        ctx.close_path()
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(2)
        ctx.stroke()
        
        # Energy lines
        for i in range(num_lines):
            angle = (i / num_lines) * math.pi - math.pi/2
            line_length = length * 0.4
            start_x = tip_x + (width/4) * math.cos(angle)
            start_y = tip_y + (width/4) * math.sin(angle)
            end_x = start_x + line_length * math.cos(angle)
            end_y = start_y + line_length * math.sin(angle)
            
            ctx.move_to(start_x, start_y)
            ctx.line_to(end_x, end_y)
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(1.5)
            ctx.stroke()

# ============================================================================
# TAIL STYLE 10: Organic Flowing Tail
# ============================================================================

def tail_organic_flowing(ctx, attach_x, attach_y, direction="bottom", length=50, width=20):
    """Organic, flowing tail with natural curves"""
    steps = 20
    
    if direction == "bottom":
        points_left = []
        points_right = []
        
        for i in range(steps + 1):
            t = i / steps
            # Natural curve variation
            curve = math.sin(t * math.pi) * width/3
            x_left = attach_x - width/2 + curve
            x_right = attach_x + width/2 - curve
            y = attach_y + t * length
            
            # Add some organic variation
            if i > 0 and i < steps:
                x_left += random.uniform(-3, 3)
                x_right += random.uniform(-3, 3)
            
            points_left.append((x_left, y))
            points_right.append((x_right, y))
        
        ctx.move_to(*points_left[0])
        for p in points_left[1:]:
            ctx.line_to(*p)
        for p in reversed(points_right):
            ctx.line_to(*p)
        ctx.close_path()
    
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(2)
    ctx.stroke()

# ============================================================================
# DEMO FUNCTION
# ============================================================================

def create_tail_styles_demo():
    """Create a demo showing all tail styles"""
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, CANVAS_WIDTH, CANVAS_HEIGHT)
    ctx = cairo.Context(surface)
    
    # Light background
    ctx.set_source_rgb(0.98, 0.98, 0.99)
    ctx.paint()
    
    # Grid layout: 3 columns, multiple rows
    col_width = CANVAS_WIDTH // 3
    row_height = 200
    start_y = 100
    
    tail_styles = [
        ("Classic Smooth", tail_classic_smooth, "bottom"),
        ("Sharp Pointed", tail_sharp_pointed, "bottom"),
        ("Wavy", tail_wavy, "bottom"),
        ("Jagged", tail_jagged, "bottom"),
        ("Double Split", tail_double_split, "bottom"),
        ("Curved Hook", tail_curved_hook, "bottom"),
        ("Bubbly", tail_bubbly, "bottom"),
        ("Thick Bold", tail_thick_bold, "bottom"),
        ("Energy Lines", tail_energy_lines, "bottom"),
        ("Organic Flowing", tail_organic_flowing, "bottom"),
    ]
    
    # Add labels
    ctx.set_source_rgb(0.3, 0.3, 0.3)
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(20)
    ctx.move_to(20, 40)
    ctx.show_text("Bubble Tail Styles Experiment")
    
    ctx.set_font_size(12)
    
    row = 0
    col = 0
    
    for style_name, tail_func, direction in tail_styles:
        cx = col * col_width + col_width // 2
        cy = start_y + row * row_height
        
        # Draw base bubble
        draw_base_bubble(ctx, cx, cy, BUBBLE_RADIUS_X, BUBBLE_RADIUS_Y)
        
        # Calculate attachment point
        if direction == "bottom":
            attach_x, attach_y = cx, cy + BUBBLE_RADIUS_Y
        elif direction == "top":
            attach_x, attach_y = cx, cy - BUBBLE_RADIUS_Y
        elif direction == "left":
            attach_x, attach_y = cx - BUBBLE_RADIUS_X, cy
        else:
            attach_x, attach_y = cx + BUBBLE_RADIUS_X, cy
        
        # Draw tail
        tail_func(ctx, attach_x, attach_y, direction, TAIL_LENGTH)
        
        # Add label
        ctx.set_source_rgb(0.2, 0.2, 0.2)
        ctx.set_font_size(11)
        text_x = cx - len(style_name) * 3
        text_y = cy + BUBBLE_RADIUS_Y + TAIL_LENGTH + 25
        ctx.move_to(text_x, text_y)
        ctx.show_text(style_name)
        
        # Move to next position
        col += 1
        if col >= 3:
            col = 0
            row += 1
    
    # Add directional examples
    ctx.set_font_size(14)
    ctx.move_to(20, start_y + (row + 1) * row_height + 50)
    ctx.show_text("Directional Examples:")
    
    directions = ["bottom", "top", "left", "right"]
    dir_labels = ["Bottom", "Top", "Left", "Right"]
    
    for i, (direction, label) in enumerate(zip(directions, dir_labels)):
        cx = 200 + i * 250
        cy = start_y + (row + 1) * row_height + 100
        
        draw_base_bubble(ctx, cx, cy, BUBBLE_RADIUS_X, BUBBLE_RADIUS_Y)
        
        if direction == "bottom":
            attach_x, attach_y = cx, cy + BUBBLE_RADIUS_Y
        elif direction == "top":
            attach_x, attach_y = cx, cy - BUBBLE_RADIUS_Y
        elif direction == "left":
            attach_x, attach_y = cx - BUBBLE_RADIUS_X, cy
        else:
            attach_x, attach_y = cx + BUBBLE_RADIUS_X, cy
        
        tail_classic_smooth(ctx, attach_x, attach_y, direction, TAIL_LENGTH)
        
        ctx.set_source_rgb(0.2, 0.2, 0.2)
        ctx.set_font_size(11)
        ctx.move_to(cx - len(label) * 3, cy + BUBBLE_RADIUS_Y + TAIL_LENGTH + 25)
        ctx.show_text(label)
    
    # Save
    output_file = "tail_styles_experiment.png"
    surface.write_to_png(output_file)
    print(f"✅ Tail styles experiment saved as '{output_file}'")
    print(f"   Generated {len(tail_styles)} different tail styles")
    print(f"   Canvas size: {CANVAS_WIDTH}x{CANVAS_HEIGHT}")

def create_individual_tail_tests():
    """Create individual test images for each tail style"""
    
    tail_styles = [
        ("classic_smooth", tail_classic_smooth),
        ("sharp_pointed", tail_sharp_pointed),
        ("wavy", tail_wavy),
        ("jagged", tail_jagged),
        ("double_split", tail_double_split),
        ("curved_hook", tail_curved_hook),
        ("bubbly", tail_bubbly),
        ("thick_bold", tail_thick_bold),
        ("energy_lines", tail_energy_lines),
        ("organic_flowing", tail_organic_flowing),
    ]
    
    for style_name, tail_func in tail_styles:
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 300, 400)
        ctx = cairo.Context(surface)
        
        ctx.set_source_rgb(0.95, 0.95, 0.95)
        ctx.paint()
        
        cx, cy = 150, 150
        draw_base_bubble(ctx, cx, cy, BUBBLE_RADIUS_X, BUBBLE_RADIUS_Y)
        
        attach_x, attach_y = cx, cy + BUBBLE_RADIUS_Y
        tail_func(ctx, attach_x, attach_y, "bottom", TAIL_LENGTH)
        
        # Add label
        ctx.set_source_rgb(0.2, 0.2, 0.2)
        ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(14)
        ctx.move_to(20, 350)
        ctx.show_text(style_name.replace("_", " ").title())
        
        output_file = f"tail_{style_name}.png"
        surface.write_to_png(output_file)
        print(f"   ✓ Saved: {output_file}")

if __name__ == "__main__":
    print("=" * 60)
    print("Bubble Tail Styles Experiment")
    print("=" * 60)
    
    print("\nCreating comprehensive demo...")
    create_tail_styles_demo()
    
    print("\nCreating individual tail style images...")
    create_individual_tail_tests()
    
    print("\n" + "=" * 60)
    print("✅ Experiment complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  • tail_styles_experiment.png - All styles overview")
    print("  • tail_*.png - Individual style examples")

