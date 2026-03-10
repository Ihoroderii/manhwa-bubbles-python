#!/usr/bin/env python3
"""
Pure PyCairo bubble test - NO PIL/Pillow needed!

This creates bubble PNG files that you can manually composite
in GIMP, Photoshop, or any image editor.
"""

import cairo

def create_simple_cairo_bubble(text, output_file='bubble_only.png'):
    """Create a bubble using only PyCairo - no PIL needed."""
    
    # Create transparent canvas
    width, height = 600, 400
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    
    # Transparent background
    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.paint()
    
    # Draw bubble (white oval with black outline)
    cx, cy = width // 2, height // 2
    radius_x, radius_y = 250, 150
    
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(radius_x, radius_y)
    ctx.arc(0, 0, 1, 0, 2 * 3.14159)
    ctx.restore()
    
    # Fill white
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill_preserve()
    
    # Black outline
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.set_line_width(3)
    ctx.stroke()
    
    # Draw tail (triangle pointing down)
    tail_base_y = cy + radius_y
    ctx.move_to(cx - 30, tail_base_y)
    ctx.line_to(cx + 30, tail_base_y)
    ctx.line_to(cx, tail_base_y + 80)
    ctx.close_path()
    
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.set_line_width(3)
    ctx.stroke()
    
    # Add text
    ctx.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(36)
    
    # Center text
    x_bearing, y_bearing, text_width, text_height, x_advance, y_advance = ctx.text_extents(text)
    ctx.move_to(cx - text_width / 2, cy + text_height / 2)
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.show_text(text)
    
    # Save as PNG
    surface.write_to_png(output_file)
    print(f"✅ Created: {output_file}")
    print(f"   Size: {width}x{height} with transparent background")
    print(f"   You can overlay this on your manga in any image editor!")
    
    return surface


def test_cairo_only():
    """Test creating bubbles with PyCairo only."""
    
    print("="*60)
    print("CAIRO-ONLY BUBBLE TEST (No PIL needed!)")
    print("="*60)
    print()
    
    # Create a few bubbles
    create_simple_cairo_bubble("Hello!", 'bubble_hello.png')
    create_simple_cairo_bubble("Watch out!", 'bubble_warning.png')
    create_simple_cairo_bubble("Amazing!", 'bubble_amazing.png')
    
    print()
    print("="*60)
    print("✅ DONE!")
    print("="*60)
    print()
    print("Created bubbles:")
    print("  - bubble_hello.png")
    print("  - bubble_warning.png")
    print("  - bubble_amazing.png")
    print()
    print("These are PNG files with transparent backgrounds.")
    print("You can manually place them on your manga in:")
    print("  - GIMP (free)")
    print("  - Photoshop")
    print("  - Affinity Photo")
    print("  - Any image editor with layer support")


if __name__ == '__main__':
    try:
        import cairo
        test_cairo_only()
    except ImportError:
        print("❌ PyCairo not installed!")
        print("Install it with:")
        print("  pip3 install pycairo")
        print()
        print("Or on Mac:")
        print("  brew install cairo")
        print("  pip3 install pycairo")

