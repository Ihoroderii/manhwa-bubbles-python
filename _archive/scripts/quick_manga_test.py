"""
Quick test: Add a speech bubble to a manga panel.

Usage:
1. Put your manga image as 'my_manga.png' in this folder
2. Edit the character position (where their head is)
3. Run: python quick_manga_test.py
"""

from PIL import Image
import numpy as np
from adaptive_bubbles import adaptive_circle_bubble


# ===== CONFIGURE HERE =====
MANGA_IMAGE = 'my_manga.png'  # Your manga panel image
CHARACTER_HEAD_POSITION = (300, 400)  # (x, y) where character's head/face is
DIALOGUE_TEXT = "This is a test bubble!"
BUBBLE_POSITION = (400, 200)  # Where to place the bubble center

# Bubble style
BUBBLE_VARIANT = 'radial5'  # Options: radial5, radial6, radial7
BUBBLE_SIZE = (600, 600)  # Canvas size for bubble
# ==========================


def add_bubble_to_manga():
    """Add a speech bubble to a manga image."""
    
    # 1. Load your manga panel
    try:
        manga = Image.open(MANGA_IMAGE).convert('RGBA')
        print(f"✅ Loaded manga: {MANGA_IMAGE} ({manga.width}x{manga.height})")
    except FileNotFoundError:
        print(f"⚠️  '{MANGA_IMAGE}' not found. Creating test image...")
        # Create a test manga-style panel
        manga = Image.new('RGBA', (800, 1200), (245, 240, 235, 255))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(manga)
        
        # Draw a simple character placeholder
        cx, cy = CHARACTER_HEAD_POSITION
        draw.ellipse((cx-40, cy-60, cx+40, cy+60), fill=(120, 120, 120))
        draw.ellipse((cx-30, cy-50, cx+30, cy+50), fill=(180, 180, 180))
        draw.text((cx-35, cy+70), "CHARACTER", fill='black')
        
        manga.save('test_manga_panel.png')
        print(f"✅ Created test panel: test_manga_panel.png")
    
    # 2. Calculate tail target (character position relative to bubble canvas)
    manga_w, manga_h = manga.size
    bubble_canvas_w, bubble_canvas_h = BUBBLE_SIZE
    
    # Bubble is drawn centered on its canvas
    bubble_center_x = bubble_canvas_w // 2
    bubble_center_y = bubble_canvas_h // 2
    
    # Where we'll paste the bubble on the manga
    bubble_paste_x = BUBBLE_POSITION[0] - bubble_center_x
    bubble_paste_y = BUBBLE_POSITION[1] - bubble_center_y
    
    # Character position relative to bubble's local canvas
    char_x, char_y = CHARACTER_HEAD_POSITION
    tail_target_local = (
        char_x - bubble_paste_x,
        char_y - bubble_paste_y
    )
    
    print(f"📍 Character at: {CHARACTER_HEAD_POSITION}")
    print(f"📍 Bubble center: {BUBBLE_POSITION}")
    print(f"🎯 Tail points to: {tail_target_local} (in bubble canvas)")
    
    # 3. Generate the bubble with tail pointing to character
    bubble_surf, meta = adaptive_circle_bubble(
        text=DIALOGUE_TEXT,
        variant=BUBBLE_VARIANT,
        canvas_size=BUBBLE_SIZE,
        tail_target=tail_target_local,
        wrap=True,
        max_lines=2,
        target_inner_padding=30,
    )
    
    print(f"✅ Generated bubble: {meta['font_size']:.0f}pt font, "
          f"{len(meta['lines'])} lines, tail: {meta['tail_points'] is not None}")
    
    # 4. Convert Cairo surface to PIL Image
    bubble_pil = Image.frombuffer(
        'RGBA',
        (bubble_surf.get_width(), bubble_surf.get_height()),
        bubble_surf.get_data(),
        'raw', 'BGRA', 0, 1
    )
    
    # 5. Composite bubble onto manga
    result = manga.copy()
    result.paste(bubble_pil, (bubble_paste_x, bubble_paste_y), bubble_pil)
    
    # 6. Save result
    output_path = 'manga_with_bubble.png'
    result.save(output_path)
    print(f"\n✅ SUCCESS! Saved: {output_path}")
    
    # Show the tail pointing correctly
    if meta['tail_points']:
        tail_pts = meta['tail_points']
        # Convert to manga coordinates
        manga_tail_pts = [
            (int(x + bubble_paste_x), int(y + bubble_paste_y))
            for x, y in tail_pts
        ]
        print(f"   Tail triangle in manga coords: {manga_tail_pts}")
    
    return result, meta


def batch_add_bubbles(dialogues):
    """Add multiple bubbles to a manga panel.
    
    Args:
        dialogues: List of dicts with keys: 'text', 'char_pos', 'bubble_pos'
    
    Example:
        dialogues = [
            {
                'text': 'Hello!',
                'char_pos': (200, 400),
                'bubble_pos': (300, 200)
            },
            {
                'text': 'Hi there!',
                'char_pos': (600, 450),
                'bubble_pos': (700, 250)
            }
        ]
    """
    try:
        manga = Image.open(MANGA_IMAGE).convert('RGBA')
    except FileNotFoundError:
        print(f"⚠️  '{MANGA_IMAGE}' not found")
        return None
    
    result = manga.copy()
    
    for i, dialogue in enumerate(dialogues):
        char_pos = dialogue['char_pos']
        bubble_pos = dialogue['bubble_pos']
        text = dialogue['text']
        variant = dialogue.get('variant', 'radial5')
        
        # Calculate bubble canvas and tail target
        bubble_size = dialogue.get('size', (500, 400))
        bubble_center_x, bubble_center_y = bubble_size[0]//2, bubble_size[1]//2
        bubble_paste_x = bubble_pos[0] - bubble_center_x
        bubble_paste_y = bubble_pos[1] - bubble_center_y
        
        tail_target_local = (
            char_pos[0] - bubble_paste_x,
            char_pos[1] - bubble_paste_y
        )
        
        # Generate bubble
        bubble_surf, meta = adaptive_circle_bubble(
            text=text,
            variant=variant,
            canvas_size=bubble_size,
            tail_target=tail_target_local,
            wrap=True,
            max_lines=2,
            target_inner_padding=25,
            seed=1000 + i,
        )
        
        # Convert and composite
        bubble_pil = Image.frombuffer(
            'RGBA',
            (bubble_surf.get_width(), bubble_surf.get_height()),
            bubble_surf.get_data(),
            'raw', 'BGRA', 0, 1
        )
        result.paste(bubble_pil, (bubble_paste_x, bubble_paste_y), bubble_pil)
        
        print(f"  Bubble {i+1}: '{text[:20]}...' @ {bubble_pos} -> char {char_pos}")
    
    output_path = 'manga_with_multiple_bubbles.png'
    result.save(output_path)
    print(f"\n✅ Saved: {output_path}")
    return result


if __name__ == '__main__':
    print("=== Quick Manga Bubble Test ===\n")
    
    # Single bubble test
    add_bubble_to_manga()
    
    print("\n" + "="*40 + "\n")
    print("💡 TIP: To add bubbles to YOUR manga:")
    print(f"   1. Replace '{MANGA_IMAGE}' with your manga image")
    print("   2. Set CHARACTER_HEAD_POSITION to where the face is")
    print("   3. Set BUBBLE_POSITION where you want the bubble")
    print("   4. Edit DIALOGUE_TEXT with your text")
    print("   5. Run this script again!")
    
    # Optional: Multiple bubbles example
    print("\n--- Multiple Bubbles Example ---")
    dialogues_example = [
        {
            'text': 'Watch out!',
            'char_pos': (200, 500),
            'bubble_pos': (250, 300),
            'variant': 'radial5',
            'size': (400, 350)
        },
        {
            'text': "I'll protect you!",
            'char_pos': (600, 520),
            'bubble_pos': (650, 320),
            'variant': 'radial6',
            'size': (450, 350)
        }
    ]
    
    # Uncomment to test multiple bubbles:
    # batch_add_bubbles(dialogues_example)

