"""
Demo script showing how to use the manhwa_bubbles library.
Run this script to see examples of all bubble and narration types.
"""

from PIL import Image, ImageDraw
from manhwa_bubbles import (
    speech_bubble, 
    narrator_plain, 
    narrator_borderless,
    narrator_dashed, 
    narrator_dark, 
    narrator_wavy
)


def demo_speech_bubbles():
    """Demonstrates all speech bubble types."""
    print("Creating speech bubbles demo...")
    
    # Create canvas
    img = Image.new("RGB", (1200, 800), "lightblue")
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((10, 10), "Manhwa Speech Bubbles Demo - All Types", fill="black")
    
    # Examples of different bubble types (original 6)
    speech_bubble(draw, (50, 50, 180, 80), "Normal speech", "oval")
    speech_bubble(draw, (250, 50, 180, 80), "Narration", "rect")
    speech_bubble(draw, (450, 50, 180, 80), "Thinking...", "cloud")
    
    speech_bubble(draw, (50, 200, 180, 100), "HEY!!", "jagged")
    speech_bubble(draw, (250, 200, 180, 100), "I'm nervous...", "wavy")
    speech_bubble(draw, (450, 200, 180, 100), "Dark thoughts", "black")
    
    # NEW: Examples of new bubble types
    speech_bubble(draw, (650, 50, 180, 120), "Love~", "heart")
    speech_bubble(draw, (850, 50, 180, 120), "RAGE!!", "spiky")
    # Simple oval bubble (no tail) — most common manga bubble shape
    x, y, w, h = 650, 220, 180, 120
    draw.ellipse((x, y, x+w, y+h), fill="white", outline="black", width=3)
    draw.text((x+30, y+45), "Simple oval", fill="black")

    speech_bubble(draw, (850, 220, 180, 120), "Madness...", "scratchy")
    
    # Add labels for original types
    draw.text((50, 140), "Normal", fill="black")
    draw.text((250, 140), "Narration", fill="black")
    draw.text((450, 140), "Thought", fill="black")
    draw.text((50, 310), "Shouting", fill="black")
    draw.text((250, 310), "Nervous", fill="black")
    draw.text((450, 310), "Dark", fill="black")
    
    # Add labels for new types
    draw.text((650, 180), "Heart", fill="red")
    draw.text((850, 180), "Spiky", fill="black")
    draw.text((650, 350), "Simple", fill="black")
    draw.text((850, 350), "Scratchy", fill="black")
    
    img.save("examples/speech_bubbles_demo.png")
    print("Saved: examples/speech_bubbles_demo.png")
    return img


def demo_narration_boxes():
    """Demonstrates all narration box types."""
    print("Creating narration boxes demo...")
    
    # Create canvas
    img = Image.new("RGB", (800, 600), "lightgray")
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((10, 10), "Manhwa Narration Boxes Demo", fill="black")
    
    # Examples of each narrator type
    narrator_plain(draw, (50, 50, 250, 80), "Plain narration box")
    narrator_borderless(draw, (350, 70, 200, 50), "Borderless narration")
    narrator_dashed(draw, (50, 180, 250, 80), "Dashed border narration")
    narrator_dark(draw, (350, 180, 250, 80), "Dark narration box")
    narrator_wavy(draw, (200, 320, 300, 100), "Wavy narration (dreamy)")
    
    # Add labels
    draw.text((50, 140), "Plain", fill="black")
    draw.text((350, 130), "Borderless", fill="black")
    draw.text((50, 270), "Dashed", fill="black")
    draw.text((350, 270), "Dark", fill="black")
    draw.text((200, 430), "Wavy", fill="black")
    
    img.save("examples/narration_boxes_demo.png")
    print("Saved: examples/narration_boxes_demo.png")
    return img


def demo_comic_panel():
    """Creates a sample comic panel using multiple elements including new bubble types."""
    print("Creating comic panel demo...")
    
    # Create canvas
    img = Image.new("RGB", (1200, 800), "white")
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((10, 10), "Sample Comic Panel - All Bubble Types", fill="black")
    
    # Scene setup narration
    narrator_plain(draw, (50, 50, 300, 60), "Meanwhile, in the dark forest...")
    
    # Character dialogue with original types
    speech_bubble(draw, (100, 150, 180, 80), "Who's there?", "oval", "down")
    speech_bubble(draw, (400, 120, 200, 90), "Show yourself!", "jagged", "left")
    
    # Thought bubble
    speech_bubble(draw, (650, 200, 180, 100), "This feels dangerous...", "cloud", "down")
    
    # NEW: Using new bubble types
    speech_bubble(draw, (100, 300, 180, 100), "I love you!", "heart", "down")
    speech_bubble(draw, (350, 280, 200, 120), "IMPOSSIBLE!!", "spiky", "up")
    # Simple oval bubble (no tail)
    gx, gy, gw, gh = 600, 350, 200, 100
    draw.ellipse((gx, gy, gx+gw, gy+gh), fill="white", outline="black", width=3)
    draw.text((gx+20, gy+35), "By the gods...", fill="black")
    speech_bubble(draw, (850, 300, 200, 120), "Must... kill...", "scratchy", "down")
    
    # Internal monologue
    narrator_dark(draw, (50, 500, 350, 80), "Little did she know, danger was approaching...")
    
    # Nervous speech
    speech_bubble(draw, (500, 520, 200, 80), "I should run...", "wavy", "up")
    
    # Sound effect area
    narrator_borderless(draw, (800, 500, 200, 50), "CRACK!")
    
    # Flashback narration
    narrator_dashed(draw, (100, 650, 300, 80), "She remembered her father's warning...")
    
    img.save("examples/comic_panel_demo.png")
    print("Saved: examples/comic_panel_demo.png")
    return img


def main():
    """Run all demos."""
    print("Running Manhwa Bubbles Library Demo")
    print("=" * 40)
    
    try:
        # Run demos
        speech_img = demo_speech_bubbles()
        narration_img = demo_narration_boxes()
        comic_img = demo_comic_panel()
        
        print("\nDemo completed successfully!")
        print("Check the 'examples/' folder for generated images.")
        
        # Optionally show the images (comment out if running headless)
        # speech_img.show()
        # narration_img.show() 
        # comic_img.show()
        
    except Exception as e:
        print(f"Error running demo: {e}")
        print("Make sure you have installed the manhwa_bubbles package:")
        print("pip install -e .")


if __name__ == "__main__":
    main()