"""
Test script to demonstrate laugh energy lines with different background colors.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    import cairo
    from manhwa_bubbles.auto_scale import auto_scale_bubble_for_panel
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

print("=" * 60)
print("Testing Laugh Energy Lines with Background Colors")
print("=" * 60)

# Test 1: Light background (should use black lines)
print("\n1. Testing with light background (white)...")
surface, ctx, meta = auto_scale_bubble_for_panel(
    panel_width=600,
    panel_height=400,
    text="Laugh!",
    style="laugh",
    background_color=(1.0, 1.0, 1.0),  # White background
    seed=42
)
surface.write_to_png("test_laugh_light_bg.png")
print("   ✓ Saved: test_laugh_light_bg.png (should have black lines)")

# Test 2: Dark background (should use bright/yellow lines)
print("\n2. Testing with dark background (black)...")
surface, ctx, meta = auto_scale_bubble_for_panel(
    panel_width=600,
    panel_height=400,
    text="Laugh!",
    style="laugh",
    background_color=(0.0, 0.0, 0.0),  # Black background
    seed=42
)
surface.write_to_png("test_laugh_dark_bg.png")
print("   ✓ Saved: test_laugh_dark_bg.png (should have bright yellow/white lines)")

# Test 3: Dark gray background
print("\n3. Testing with dark gray background...")
surface, ctx, meta = auto_scale_bubble_for_panel(
    panel_width=600,
    panel_height=400,
    text="Laugh!",
    style="laugh",
    background_color=(0.2, 0.2, 0.2),  # Dark gray
    seed=42
)
surface.write_to_png("test_laugh_darkgray_bg.png")
print("   ✓ Saved: test_laugh_darkgray_bg.png (should have bright lines)")

# Test 4: Medium gray background
print("\n4. Testing with medium gray background...")
surface, ctx, meta = auto_scale_bubble_for_panel(
    panel_width=600,
    panel_height=400,
    text="Laugh!",
    style="laugh",
    background_color=(0.5, 0.5, 0.5),  # Medium gray
    seed=42
)
surface.write_to_png("test_laugh_mediumgray_bg.png")
print("   ✓ Saved: test_laugh_mediumgray_bg.png")

# Test 5: Colored dark background (dark blue)
print("\n5. Testing with dark blue background...")
surface, ctx, meta = auto_scale_bubble_for_panel(
    panel_width=600,
    panel_height=400,
    text="Laugh!",
    style="laugh",
    background_color=(0.1, 0.1, 0.3),  # Dark blue
    seed=42
)
surface.write_to_png("test_laugh_darkblue_bg.png")
print("   ✓ Saved: test_laugh_darkblue_bg.png (should have bright lines)")

print("\n" + "=" * 60)
print("✅ All tests completed!")
print("=" * 60)
print("\nCheck the generated PNG files to see:")
print("  • Light backgrounds → Black laugh lines")
print("  • Dark backgrounds → Bright yellow/white laugh lines")

