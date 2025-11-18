"""
Reusable module for different bubble tail styles using Cairo.
Can be imported and used in other scripts.
"""

import cairo
import math
import random

# ============================================================================
# TAIL STYLE FUNCTIONS
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
# TAIL STYLE REGISTRY
# ============================================================================

TAIL_STYLES = {
    "classic": tail_classic_smooth,
    "smooth": tail_classic_smooth,
    "sharp": tail_sharp_pointed,
    "pointed": tail_sharp_pointed,
    "wavy": tail_wavy,
    "jagged": tail_jagged,
    "spiky": tail_jagged,
    "energy": tail_energy_lines,
    "organic": tail_organic_flowing,
    "flowing": tail_organic_flowing,
}


def get_tail_function(style_name):
    """Get tail function by name"""
    return TAIL_STYLES.get(style_name.lower(), tail_classic_smooth)


def list_available_tails():
    """List all available tail styles"""
    return list(TAIL_STYLES.keys())

