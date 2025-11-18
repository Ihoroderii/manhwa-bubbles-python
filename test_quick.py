"""
Quick test script to verify the library works after improvements.
"""
from PIL import Image, ImageDraw
from manhwa_bubbles import (
    speech_bubble,
    narrator_plain,
    narrator_dark,
    bubble_wide_soft,
    bubble_laugh_bouncy,
    bubble_shout_burst,
)

def main():
    print("=" * 60)
    print("Manhwa Bubbles - Quick Test")
    print("=" * 60)
    
    # Create test canvas
    img = Image.new("RGB", (1000, 700), "lightblue")
    draw = ImageDraw.Draw(img)
    
    # Add title
    draw.text((20, 10), "Manhwa Bubbles Test - Post Improvements", fill="black")
    
    print("\n✅ Testing core speech bubbles...")
    # Test core bubbles
    speech_bubble(draw, (50, 50, 200, 100), "Hello!", "oval")
    speech_bubble(draw, (300, 50, 200, 100), "Shouting!", "jagged")
    speech_bubble(draw, (550, 50, 200, 100), "Love!", "heart")
    speech_bubble(draw, (800, 50, 200, 100), "Rage!", "spiky")
    print("   ✓ Core bubbles created")
    
    print("\n✅ Testing narration boxes...")
    # Test narrators
    narrator_plain(draw, (50, 200, 250, 80), "Plain narration box")
    narrator_dark(draw, (350, 200, 250, 80), "Dark narration")
    print("   ✓ Narration boxes created")
    
    print("\n✅ Testing extended styles...")
    # Test extended styles
    bubble_wide_soft(draw, (50, 320, 200, 100), "Wide soft")
    bubble_laugh_bouncy(draw, (300, 320, 200, 100), "Ha ha!")
    bubble_shout_burst(draw, (550, 320, 200, 100), "BURST!")
    print("   ✓ Extended styles created")
    
    # Save output
    output_file = "test_output.png"
    img.save(output_file)
    print(f"\n✅ Test completed successfully!")
    print(f"✅ Output saved to: {output_file}")
    print(f"✅ Image size: {img.size}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

