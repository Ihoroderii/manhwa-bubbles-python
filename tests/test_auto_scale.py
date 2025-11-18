"""
Test suite for auto-scaling bubble functions.
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Test that auto-scaling module can be imported."""
    try:
        from manhwa_bubbles.auto_scale import (
            auto_scale_bubble_for_panel,
            auto_scale_bubble_adaptive,
            quick_auto_bubble,
            find_free_bbox_rect
        )
        print("✅ Auto-scaling imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("   Note: This requires pycairo and the overlapping_circles_squares module")
        return False


def test_basic_auto_scale():
    """Test basic auto-scaling functionality."""
    try:
        import cairo
        from manhwa_bubbles.auto_scale import auto_scale_bubble_for_panel
        
        print("\n🧪 Testing basic auto-scaling...")
        
        # Test with different panel sizes
        test_cases = [
            (800, 1200, "Small text"),
            (1200, 1600, "Medium sized panel with longer text content"),
            (600, 800, "Hi!"),
        ]
        
        for panel_w, panel_h, text in test_cases:
            try:
                surface, ctx, metadata = auto_scale_bubble_for_panel(
                    panel_w, panel_h, text, style="organic", seed=42
                )
                
                print(f"   ✓ Panel {panel_w}x{panel_h}: Bubble {metadata['bubble_size']}")
                print(f"     Panel fraction: {metadata['panel_fraction']}")
                
                # Save test output
                output_file = f"test_auto_scale_{panel_w}x{panel_h}.png"
                surface.write_to_png(output_file)
                print(f"     Saved: {output_file}")
                
            except Exception as e:
                print(f"   ❌ Failed for {panel_w}x{panel_h}: {e}")
                return False
        
        print("✅ Basic auto-scaling test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Cairo not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_adaptive_scaling():
    """Test adaptive scaling functionality."""
    try:
        import cairo
        from manhwa_bubbles.auto_scale import auto_scale_bubble_adaptive
        
        print("\n🧪 Testing adaptive scaling...")
        
        surface, ctx, metadata = auto_scale_bubble_adaptive(
            panel_width=800,
            panel_height=1200,
            text="This is a longer text that needs adaptive fitting!",
            style="laugh",
            target_text_padding=25,
            max_panel_fraction=0.35,
            seed=123
        )
        
        print(f"   ✓ Adaptive scaling completed")
        print(f"     Bubble size: {metadata['bubble_size']}")
        print(f"     Iterations: {metadata['iterations']}")
        print(f"     Panel fraction: {metadata['panel_fraction']}")
        
        output_file = "test_adaptive_scale.png"
        surface.write_to_png(output_file)
        print(f"     Saved: {output_file}")
        
        print("✅ Adaptive scaling test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Cairo not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_positioning():
    """Test bubble positioning."""
    try:
        import cairo
        from manhwa_bubbles.auto_scale import auto_scale_bubble_for_panel
        
        print("\n🧪 Testing bubble positioning...")
        
        positions = [
            (None, "center"),
            ((0.2, 0.2), "top-left"),
            ((0.8, 0.2), "top-right"),
            ((0.5, 0.8), "bottom-center"),
        ]
        
        for pos, name in positions:
            try:
                surface, ctx, metadata = auto_scale_bubble_for_panel(
                    panel_width=800,
                    panel_height=1200,
                    text="Positioned!",
                    position=pos,
                    style="organic",
                    seed=42
                )
                
                print(f"   ✓ {name}: Position {metadata['position']}")
                
                output_file = f"test_position_{name.replace('-', '_')}.png"
                surface.write_to_png(output_file)
                
            except Exception as e:
                print(f"   ❌ Failed for {name}: {e}")
                return False
        
        print("✅ Positioning test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Cairo not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_quick_helper():
    """Test quick helper function."""
    try:
        import cairo
        from manhwa_bubbles.auto_scale import quick_auto_bubble
        
        print("\n🧪 Testing quick helper...")
        
        surface = quick_auto_bubble((800, 1200), "Quick test!", "laugh")
        
        output_file = "test_quick_auto.png"
        surface.write_to_png(output_file)
        print(f"   ✓ Quick helper works! Saved: {output_file}")
        
        print("✅ Quick helper test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Cairo not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Auto-Scaling Bubble Tests")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Basic Auto-Scale", test_basic_auto_scale),
        ("Adaptive Scaling", test_adaptive_scaling),
        ("Positioning", test_positioning),
        ("Quick Helper", test_quick_helper),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check output above for details.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

