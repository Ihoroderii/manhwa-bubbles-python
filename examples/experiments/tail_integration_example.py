"""
Example showing how to integrate tail styles with bubble creation.
Demonstrates using different tail styles with overlapping circles bubbles.
"""

import cairo
import math
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from examples.experiments.tail_styles_module import (
    get_tail_function,
    list_available_tails,
    tail_classic_smooth,
    tail_wavy,
    tail_energy_lines,
    tail_organic_flowing
)
from examples.experiments.overlapping_circles_squares import (
    create_overlapping_circles_square
)

def create_bubble_with_tail(ctx, cx, cy, base_width, base_height, 
                            text="", circle_style="organic", 
                            tail_style="classic", tail_direction="bottom",
                            tail_length=50, tail_width=20):
    """Create overlapping circles bubble with custom tail"""
    
    # Create the main bubble
    create_overlapping_circles_square(
        ctx, cx, cy, base_width, base_height,
        text=text, circle_style=circle_style,
        show_full_ovals=False
    )
    
    # Calculate tail attachment point based on direction
    half_width = base_width / 2
    half_height = base_height / 2
    
    if tail_direction == "bottom":
        attach_x, attach_y = cx, cy + half_height
    elif tail_direction == "top":
        attach_x, attach_y = cx, cy - half_height
    elif tail_direction == "left":
        attach_x, attach_y = cx - half_width, cy
    else:  # right
        attach_x, attach_y = cx + half_width, cy
    
    # Get tail function
    tail_func = get_tail_function(tail_style)
    
    # Draw tail
    tail_func(ctx, attach_x, attach_y, tail_direction, tail_length, tail_width)


def demo_tails_with_bubbles():
    """Demo showing different tail styles with organic bubbles"""
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1200)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(0.95, 0.95, 0.95)
    ctx.paint()
    
    # Title
    ctx.set_source_rgb(0.2, 0.2, 0.2)
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(24)
    ctx.move_to(20, 40)
    ctx.show_text("Organic Bubbles with Different Tail Styles")
    
    # Configuration
    tail_configs = [
        ("classic", "Classic Smooth", (200, 150)),
        ("wavy", "Wavy Tail", (500, 150)),
        ("energy", "Energy Lines", (800, 150)),
        ("organic", "Organic Flowing", (200, 400)),
        ("sharp", "Sharp Pointed", (500, 400)),
        ("jagged", "Jagged", (800, 400)),
    ]
    
    for tail_style, label, (cx, cy) in tail_configs:
        # Create bubble with tail
        create_bubble_with_tail(
            ctx, cx, cy, 150, 100,
            text="", circle_style="organic",
            tail_style=tail_style, tail_direction="bottom",
            tail_length=60, tail_width=25
        )
        
        # Add label
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.set_font_size(12)
        ctx.move_to(cx - len(label) * 3, cy + 100 + 60 + 20)
        ctx.show_text(label)
    
    # Direction examples
    ctx.set_font_size(16)
    ctx.move_to(20, 700)
    ctx.show_text("Different Directions:")
    
    directions = ["bottom", "top", "left", "right"]
    dir_positions = [(200, 800), (500, 800), (200, 1000), (500, 1000)]
    
    for direction, (cx, cy) in zip(directions, dir_positions):
        create_bubble_with_tail(
            ctx, cx, cy, 120, 90,
            text="", circle_style="laugh",
            tail_style="classic", tail_direction=direction,
            tail_length=50, tail_width=20
        )
        
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.set_font_size(11)
        ctx.move_to(cx - len(direction) * 3, cy + 90 + 50 + 20)
        ctx.show_text(direction.capitalize())
    
    output_file = "bubbles_with_tails_demo.png"
    surface.write_to_png(output_file)
    print(f"✅ Demo saved as '{output_file}'")


def demo_custom_tail_combinations():
    """Demo showing custom tail combinations"""
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 600)
    ctx = cairo.Context(surface)
    
    ctx.set_source_rgb(0.98, 0.98, 0.99)
    ctx.paint()
    
    # Example 1: Laugh bubble with energy tail
    create_bubble_with_tail(
        ctx, 200, 150, 140, 100,
        text="", circle_style="laugh",
        tail_style="energy", tail_direction="bottom",
        tail_length=70, tail_width=30
    )
    
    # Example 2: Organic bubble with wavy tail
    create_bubble_with_tail(
        ctx, 500, 150, 140, 100,
        text="", circle_style="organic",
        tail_style="wavy", tail_direction="bottom",
        tail_length=60, tail_width=25
    )
    
    # Example 3: Varied bubble with organic tail
    create_bubble_with_tail(
        ctx, 200, 400, 140, 100,
        text="", circle_style="varied",
        tail_style="organic", tail_direction="bottom",
        tail_length=65, tail_width=28
    )
    
    # Example 4: Laugh bubble with classic tail (left direction)
    create_bubble_with_tail(
        ctx, 500, 400, 140, 100,
        text="", circle_style="laugh",
        tail_style="classic", tail_direction="left",
        tail_length=60, tail_width=25
    )
    
    output_file = "custom_tail_combinations.png"
    surface.write_to_png(output_file)
    print(f"✅ Custom combinations saved as '{output_file}'")


if __name__ == "__main__":
    print("=" * 60)
    print("Tail Integration Examples")
    print("=" * 60)
    
    print("\nAvailable tail styles:")
    for style in list_available_tails():
        print(f"  • {style}")
    
    print("\nCreating demos...")
    demo_tails_with_bubbles()
    demo_custom_tail_combinations()
    
    print("\n✅ All demos completed!")

