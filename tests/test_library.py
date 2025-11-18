"""
Simple test script to verify the manhwa_bubbles library is working correctly.
"""

def test_import():
    """Test that all modules can be imported."""
    try:
        from manhwa_bubbles import (
            speech_bubble, 
            draw_tail,
            bubble_heart,
            bubble_spiky,
            bubble_glow,
            bubble_scratchy,
            narrator_plain, 
            narrator_borderless,
            narrator_dashed, 
            narrator_dark, 
            narrator_wavy
        )
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality with minimal examples."""
    try:
        from PIL import Image, ImageDraw
        from manhwa_bubbles import speech_bubble, narrator_plain
        
        # Create a small test image
        img = Image.new("RGB", (400, 300), "white")
        draw = ImageDraw.Draw(img)
        
        # Test speech bubble
        speech_bubble(draw, (50, 50, 150, 80), "Test!", "oval")
        
        # Test narrator
        narrator_plain(draw, (50, 150, 200, 60), "Test narration")
        
        # Save test image
        img.save("test_output.png")
        print("✅ Basic functionality test passed!")
        print("✅ Test image saved as 'test_output.png'")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def test_all_bubble_types():
    """Test all bubble types work without errors."""
    try:
        from PIL import Image, ImageDraw
        from manhwa_bubbles import speech_bubble
        
        img = Image.new("RGB", (800, 600), "lightblue")
        draw = ImageDraw.Draw(img)
        
        bubble_types = ["oval", "rect", "cloud", "jagged", "wavy", "black", "heart", "spiky", "glow", "scratchy"]
        
        for i, bubble_type in enumerate(bubble_types):
            x = (i % 5) * 150 + 20
            y = (i // 5) * 120 + 20
            speech_bubble(draw, (x, y, 120, 80), f"{bubble_type}", bubble_type)
        
        img.save("all_bubbles_test.png")
        print("✅ All bubble types test passed!")
        print(f"✅ Tested {len(bubble_types)} bubble types: {', '.join(bubble_types)}")
        print("✅ All bubbles image saved as 'all_bubbles_test.png'")
        return True
        
    except Exception as e:
        print(f"❌ All bubble types test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing Manhwa Bubbles Library")
    print("=" * 35)
    
    tests = [
        test_import,
        test_basic_functionality,
        test_all_bubble_types
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        if test():
            passed += 1
        print()
    
    print("=" * 35)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your library is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)