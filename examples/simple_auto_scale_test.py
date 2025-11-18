"""
Simple test script for auto-scaling (works even without pycairo).
Tests import and basic functionality checks.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

print("=" * 60)
print("Simple Auto-Scale Test")
print("=" * 60)

# Test 1: Import check
print("\n1. Testing imports...")
try:
    from manhwa_bubbles.auto_scale import (
        auto_scale_bubble_for_panel,
        auto_scale_bubble_adaptive,
        quick_auto_bubble,
        find_free_bbox_rect
    )
    print("   ✅ All imports successful!")
except ImportError as e:
    print(f"   ⚠️  Import warning: {e}")
    print("   (This is expected if pycairo is not installed)")

# Test 2: Check Cairo availability
print("\n2. Checking Cairo availability...")
try:
    import cairo
    print("   ✅ Cairo is available!")
    cairo_available = True
except ImportError:
    print("   ⚠️  Cairo not available")
    print("   Install with: pip install pycairo")
    cairo_available = False

# Test 3: Check overlapping_circles_squares
print("\n3. Checking overlapping_circles_squares module...")
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples', 'experiments'))
    from overlapping_circles_squares import create_overlapping_circles_square
    print("   ✅ overlapping_circles_squares available!")
    module_available = True
except ImportError as e:
    print(f"   ⚠️  Module not found: {e}")
    module_available = False

# Test 4: Basic functionality test (if dependencies available)
if cairo_available and module_available:
    print("\n4. Testing basic functionality...")
    try:
        from manhwa_bubbles.auto_scale import auto_scale_bubble_for_panel
        
        surface, ctx, metadata = auto_scale_bubble_for_panel(
            panel_width=400,
            panel_height=600,
            text="Test!",
            style="organic",
            seed=42
        )
        
        output_file = "simple_test_output.png"
        surface.write_to_png(output_file)
        
        print(f"   ✅ Basic test passed!")
        print(f"   ✅ Bubble size: {metadata['bubble_size']}")
        print(f"   ✅ Saved: {output_file}")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n4. Skipping functionality test (dependencies missing)")

print("\n" + "=" * 60)
print("Test Summary")
print("=" * 60)
print(f"Cairo available: {'✅' if cairo_available else '❌'}")
print(f"Module available: {'✅' if module_available else '❌'}")

if cairo_available and module_available:
    print("\n✅ All dependencies available! You can run full tests.")
    print("   Run: python tests/test_auto_scale.py")
else:
    print("\n⚠️  Some dependencies missing. Install them to run full tests.")
    print("   See AUTO_SCALE_README.md for installation instructions.")

