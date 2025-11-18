"""
Demo script showing auto-scaling bubble functionality.
Demonstrates various panel sizes and configurations.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    import cairo
    from manhwa_bubbles.auto_scale import (
        auto_scale_bubble_for_panel,
        auto_scale_bubble_adaptive,
        quick_auto_bubble
    )
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("   Make sure pycairo is installed and overlapping_circles_squares.py is available")
    sys.exit(1)


def demo_basic_scaling():
    """Demonstrate basic auto-scaling with different panel sizes."""
    print("\n" + "=" * 60)
    print("Demo 1: Basic Auto-Scaling")
    print("=" * 60)
    
    panel_configs = [
        (800, 1200, "Standard manga panel"),
        (600, 800, "Small panel"),
        (1200, 1600, "Large panel"),
        (400, 600, "Tiny panel"),
    ]
    
    for panel_w, panel_h, name in panel_configs:
        print(f"\n📐 {name} ({panel_w}x{panel_h})")
        
        surface, ctx, metadata = auto_scale_bubble_for_panel(
            panel_width=panel_w,
            panel_height=panel_h,
            text="Auto-scaled!",
            style="organic",
            max_panel_fraction=0.3,
            seed=42
        )
        
        output_file = f"demo_basic_{panel_w}x{panel_h}.png"
        surface.write_to_png(output_file)
        
        print(f"   ✓ Bubble size: {int(metadata['bubble_size'][0])}x{int(metadata['bubble_size'][1])}")
        print(f"   ✓ Panel fraction: {metadata['panel_fraction'][0]:.2%} x {metadata['panel_fraction'][1]:.2%}")
        print(f"   ✓ Saved: {output_file}")


def demo_adaptive_scaling():
    """Demonstrate adaptive scaling that fits text perfectly."""
    print("\n" + "=" * 60)
    print("Demo 2: Adaptive Scaling (Text-Fitting)")
    print("=" * 60)
    
    texts = [
        "Short",
        "This is a medium length text",
        "This is a much longer text that needs more space to fit properly inside the bubble!",
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\n📝 Text {i}: '{text}'")
        
        surface, ctx, metadata = auto_scale_bubble_adaptive(
            panel_width=800,
            panel_height=1200,
            text=text,
            style="laugh",
            target_text_padding=25,
            max_panel_fraction=0.35,
            seed=123
        )
        
        output_file = f"demo_adaptive_{i}.png"
        surface.write_to_png(output_file)
        
        print(f"   ✓ Bubble size: {int(metadata['bubble_size'][0])}x{int(metadata['bubble_size'][1])}")
        print(f"   ✓ Iterations: {metadata['iterations']}")
        print(f"   ✓ Saved: {output_file}")


def demo_positioning():
    """Demonstrate bubble positioning on panel."""
    print("\n" + "=" * 60)
    print("Demo 3: Bubble Positioning")
    print("=" * 60)
    
    positions = [
        (None, "Center"),
        ((0.25, 0.2), "Top-Left"),
        ((0.75, 0.2), "Top-Right"),
        ((0.25, 0.8), "Bottom-Left"),
        ((0.75, 0.8), "Bottom-Right"),
        ((0.5, 0.5), "Center (explicit)"),
    ]
    
    # Create panel with background
    panel_w, panel_h = 800, 1200
    panel_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, panel_w, panel_h)
    panel_ctx = cairo.Context(panel_surface)
    
    # Light gray background
    panel_ctx.set_source_rgb(0.95, 0.95, 0.95)
    panel_ctx.paint()
    
    for pos, name in positions:
        print(f"\n📍 {name}")
        
        surface, ctx, metadata = auto_scale_bubble_for_panel(
            panel_width=panel_w,
            panel_height=panel_h,
            text=name,
            position=pos,
            style="organic",
            max_panel_fraction=0.2,
            seed=42
        )
        
        # Composite onto panel
        panel_ctx.set_source_surface(surface, 0, 0)
        panel_ctx.paint()
        
        print(f"   ✓ Position: {metadata['position']}")
    
    output_file = "demo_positioning.png"
    panel_surface.write_to_png(output_file)
    print(f"\n   ✓ Saved combined panel: {output_file}")


def demo_multiple_bubbles():
    """Demonstrate multiple bubbles on same panel."""
    print("\n" + "=" * 60)
    print("Demo 4: Multiple Bubbles on Panel")
    print("=" * 60)
    
    panel_w, panel_h = 800, 1200
    
    # Create panel with background
    panel_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, panel_w, panel_h)
    panel_ctx = cairo.Context(panel_surface)
    panel_ctx.set_source_rgb(0.98, 0.98, 0.99)  # Very light background
    panel_ctx.paint()
    
    # Define multiple bubbles
    bubbles = [
        {"text": "First!", "pos": (0.3, 0.2), "style": "organic"},
        {"text": "Second bubble!", "pos": (0.7, 0.3), "style": "laugh"},
        {"text": "Third!", "pos": (0.2, 0.7), "style": "organic"},
        {"text": "Fourth!", "pos": (0.8, 0.8), "style": "varied"},
    ]
    
    print(f"\n📦 Creating {len(bubbles)} bubbles on panel...")
    
    for i, bubble_config in enumerate(bubbles, 1):
        print(f"   Bubble {i}: '{bubble_config['text']}' at {bubble_config['pos']}")
        
        surface, ctx, metadata = auto_scale_bubble_for_panel(
            panel_width=panel_w,
            panel_height=panel_h,
            text=bubble_config['text'],
            position=bubble_config['pos'],
            style=bubble_config['style'],
            max_panel_fraction=0.25,
            seed=42 + i
        )
        
        # Composite onto panel
        panel_ctx.set_source_surface(surface, 0, 0)
        panel_ctx.paint()
    
    output_file = "demo_multiple_bubbles.png"
    panel_surface.write_to_png(output_file)
    print(f"\n   ✓ Saved: {output_file}")


def demo_style_comparison():
    """Compare different bubble styles with auto-scaling."""
    print("\n" + "=" * 60)
    print("Demo 5: Style Comparison")
    print("=" * 60)
    
    styles = ["organic", "laugh", "varied"]
    panel_w, panel_h = 600, 400
    
    for style in styles:
        print(f"\n🎨 Style: {style}")
        
        surface, ctx, metadata = auto_scale_bubble_for_panel(
            panel_width=panel_w,
            panel_height=panel_h,
            text=f"{style.title()} style",
            style=style,
            max_panel_fraction=0.4,
            seed=42
        )
        
        output_file = f"demo_style_{style}.png"
        surface.write_to_png(output_file)
        
        print(f"   ✓ Saved: {output_file}")


def demo_quick_helper():
    """Demonstrate quick helper function."""
    print("\n" + "=" * 60)
    print("Demo 6: Quick Helper Function")
    print("=" * 60)
    
    print("\n⚡ Using quick_auto_bubble() helper...")
    
    surface = quick_auto_bubble((800, 1200), "Quick and easy!", "laugh")
    
    output_file = "demo_quick.png"
    surface.write_to_png(output_file)
    
    print(f"   ✓ Saved: {output_file}")
    print("   ✓ One-line function call for simple use cases!")


def main():
    """Run all demos."""
    print("=" * 60)
    print("Auto-Scaling Bubble Demo")
    print("=" * 60)
    print("\nThis demo shows various auto-scaling features:")
    print("  • Basic scaling for different panel sizes")
    print("  • Adaptive text-fitting")
    print("  • Position control")
    print("  • Multiple bubbles on one panel")
    print("  • Style comparisons")
    print("  • Quick helper function")
    
    try:
        demo_basic_scaling()
        demo_adaptive_scaling()
        demo_positioning()
        demo_multiple_bubbles()
        demo_style_comparison()
        demo_quick_helper()
        
        print("\n" + "=" * 60)
        print("✅ All demos completed!")
        print("=" * 60)
        print("\nGenerated files:")
        print("  • demo_basic_*.png - Basic scaling examples")
        print("  • demo_adaptive_*.png - Adaptive text-fitting")
        print("  • demo_positioning.png - Position examples")
        print("  • demo_multiple_bubbles.png - Multiple bubbles")
        print("  • demo_style_*.png - Style comparisons")
        print("  • demo_quick.png - Quick helper example")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

