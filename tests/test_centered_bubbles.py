"""
Enhanced test script with centered text in bubbles.
"""

from PIL import Image, ImageDraw, ImageFont


def get_text_center(draw, text, font, x, y, w, h):
    """Calculate centered position for text within a rectangle."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    center_x = x + (w - text_w) // 2
    center_y = y + (h - text_h) // 2
    
    return center_x, center_y


def test_centered_bubbles():
    """Test bubbles with properly centered text."""
    try:
        from manhwa_bubbles import speech_bubble
        
        # Create a larger image for better visibility
        img = Image.new("RGB", (1200, 800), "lightgray")
        draw = ImageDraw.Draw(img)
        
        # Define bubble types and their display text
        bubble_configs = [
            ("oval", "Oval", "Basic oval bubble"),
            ("rect", "Rect", "Rectangle bubble"),
            ("cloud", "Cloud", "Fluffy cloud"),
            ("jagged", "Jagged", "Angry/excited"),
            ("wavy", "Wavy", "Dreamy wavy"),
            ("black", "Black", "Dark/serious"),
            ("heart", "Heart", "Love/cute"),
            ("spiky", "Spiky", "Aggressive"),
            ("glow", "Glow", "Magical glow"),
            ("scratchy", "Scratchy", "Creepy/mad")
        ]
        
        # Create a grid of bubbles
        cols = 5
        rows = 2
        bubble_width = 200
        bubble_height = 120
        margin = 40
        
        for i, (bubble_type, title, description) in enumerate(bubble_configs):
            col = i % cols
            row = i // cols
            
            x = margin + col * (bubble_width + margin)
            y = margin + row * (bubble_height + margin * 2)
            
            # Draw the bubble
            speech_bubble(draw, (x, y, bubble_width, bubble_height), title, bubble_type)
            
            # Add description below bubble
            desc_y = y + bubble_height + 10
            draw.text((x, desc_y), description, fill="black")
        
        # Add title
        title_font = ImageFont.load_default()
        draw.text((50, 10), "Manhwa Bubbles - All Types with Centered Text", fill="black", font=title_font)
        
        img.save("centered_bubbles_test.png")
        print("✅ Centered bubbles test completed!")
        print("✅ Image saved as 'centered_bubbles_test.png'")
        return True
        
    except Exception as e:
        print(f"❌ Centered bubbles test failed: {e}")
        return False


def test_single_centered_bubble():
    """Create a single large bubble with perfectly centered text."""
    try:
        from manhwa_bubbles import speech_bubble
        
        img = Image.new("RGB", (400, 300), "white")
        draw = ImageDraw.Draw(img)
        
        # Large bubble with multiline text
        bubble_text = "Hello\nWorld!"
        speech_bubble(draw, (50, 50, 300, 200), bubble_text, "oval")
        
        img.save("single_centered_bubble.png")
        print("✅ Single centered bubble test completed!")
        print("✅ Image saved as 'single_centered_bubble.png'")
        return True
        
    except Exception as e:
        print(f"❌ Single centered bubble test failed: {e}")
        return False


def test_comparison():
    """Create a comparison showing different text positioning."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        from manhwa_bubbles import speech_bubble
        
        img = Image.new("RGB", (800, 400), "lightblue")
        draw = ImageDraw.Draw(img)
        
        # Test different bubble types with same text
        test_text = "CENTER"
        bubbles = [
            ("oval", 50, 50),
            ("heart", 250, 50),
            ("cloud", 450, 50),
            ("spiky", 650, 50),
            ("glow", 150, 200),
            ("scratchy", 350, 200),
            ("jagged", 550, 200)
        ]
        
        for bubble_type, x, y in bubbles:
            speech_bubble(draw, (x, y, 120, 100), test_text, bubble_type)
            # Add label below
            draw.text((x, y + 110), bubble_type, fill="black")
        
        img.save("bubble_comparison.png")
        print("✅ Bubble comparison test completed!")
        print("✅ Image saved as 'bubble_comparison.png'")
        return True
        
    except Exception as e:
        print(f"❌ Bubble comparison test failed: {e}")
        return False


def main():
    """Run all centered bubble tests."""
    print("Testing Manhwa Bubbles with Centered Text")
    print("=" * 45)
    
    tests = [
        test_centered_bubbles,
        test_single_centered_bubble,
        test_comparison
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        if test():
            passed += 1
        print()
    
    print("=" * 45)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All centered bubble tests passed!")
        print("📁 Check the generated images:")
        print("   - centered_bubbles_test.png")
        print("   - single_centered_bubble.png") 
        print("   - bubble_comparison.png")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)