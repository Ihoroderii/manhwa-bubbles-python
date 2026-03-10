"""
Test script for compositing adaptive bubbles onto manga/manhwa images.

This demonstrates:
1. Loading a manga panel image
2. Defining character/speaker positions
3. Positioning bubbles with tails pointing toward characters
4. Compositing bubbles onto the manga background
"""

import cairo
from PIL import Image
import numpy as np
from adaptive_bubbles import adaptive_circle_bubble, adaptive_square_bubble


def composite_bubble_on_manga(background_path, bubble_surface, bubble_x, bubble_y, 
                               alpha=1.0):
    """Composite a Cairo bubble surface onto a PIL manga image.
    
    Args:
        background_path: Path to manga image
        bubble_surface: Cairo ImageSurface with the bubble
        bubble_x, bubble_y: Top-left position to place bubble
        alpha: Overall opacity (0-1)
    
    Returns:
        PIL Image with composited bubble
    """
    # Load background manga image
    bg = Image.open(background_path).convert('RGBA')
    
    # Convert Cairo surface to PIL Image
    buf = bubble_surface.get_data()
    bubble_pil = Image.frombuffer(
        'RGBA', 
        (bubble_surface.get_width(), bubble_surface.get_height()),
        buf, 'raw', 'BGRA', 0, 1
    )
    
    # Apply alpha if needed
    if alpha < 1.0:
        bubble_array = np.array(bubble_pil).astype(float)
        bubble_array[:, :, 3] *= alpha
        bubble_pil = Image.fromarray(bubble_array.astype(np.uint8))
    
    # Composite bubble onto background
    bg.paste(bubble_pil, (bubble_x, bubble_y), bubble_pil)
    
    return bg


def demo_simple_positioning():
    """Demo: Manual character positioning (simplest approach)"""
    
    # 1. Define your manga panel and character positions
    manga_path = 'your_manga_panel.png'  # Replace with actual manga image
    panel_width, panel_height = 800, 1200
    
    # Character positions (x, y) - where the character's head/face is
    character_positions = {
        'hero': (200, 400),      # Left character
        'villain': (600, 300),   # Right character
    }
    
    # 2. Create bubbles positioned away from characters, tails pointing to them
    dialogues = [
        {
            'text': "You won't get away with this!",
            'speaker': 'hero',
            'bubble_center': (400, 200),  # Bubble positioned above/between
        },
        {
            'text': "It's already too late!",
            'speaker': 'villain',
            'bubble_center': (600, 150),  # Bubble near villain
        }
    ]
    
    # Create a composite background
    try:
        result = Image.open(manga_path).convert('RGBA')
    except FileNotFoundError:
        # Create a dummy manga-style background for testing
        result = Image.new('RGBA', (panel_width, panel_height), (245, 245, 240, 255))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(result)
        # Draw simple character placeholders
        for name, (cx, cy) in character_positions.items():
            draw.ellipse((cx-30, cy-40, cx+30, cy+40), fill=(100, 100, 100))
            draw.text((cx-20, cy+50), name, fill='black')
    
    # 3. Generate and composite each bubble
    for i, dialogue in enumerate(dialogues):
        speaker_pos = character_positions[dialogue['speaker']]
        bubble_cx, bubble_cy = dialogue['bubble_center']
        
        # Generate bubble with tail pointing to speaker
        bubble_surf, meta = adaptive_circle_bubble(
            text=dialogue['text'],
            variant='radial5',
            canvas_size=(panel_width, panel_height),
            tail_target=speaker_pos,  # Tail points to character
            wrap=True,
            max_lines=2,
            target_inner_padding=30,
        )
        
        # Composite onto result (bubble is drawn at center, so offset)
        result.paste(
            Image.frombuffer('RGBA', 
                           (bubble_surf.get_width(), bubble_surf.get_height()),
                           bubble_surf.get_data(), 'raw', 'BGRA', 0, 1),
            (0, 0),  # Full overlay since bubble is drawn at canvas center
            Image.frombuffer('RGBA', 
                           (bubble_surf.get_width(), bubble_surf.get_height()),
                           bubble_surf.get_data(), 'raw', 'BGRA', 0, 1)
        )
        
        print(f"Bubble {i+1}: {dialogue['text'][:20]}... -> {dialogue['speaker']}")
        print(f"  Tail points to: {speaker_pos}, Metadata: {meta['tail_points']}")
    
    result.save('manga_with_bubbles_simple.png')
    print("\n✅ Saved: manga_with_bubbles_simple.png")
    return result


def demo_offset_bubbles():
    """Demo: Bubbles positioned in specific locations with tails"""
    
    panel_width, panel_height = 800, 1200
    
    # Create test manga background
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, panel_width, panel_height)
    ctx = cairo.Context(surface)
    
    # Manga-style background
    ctx.set_source_rgb(0.96, 0.96, 0.94)
    ctx.paint()
    
    # Draw character placeholder (simple oval)
    character_x, character_y = 300, 800
    ctx.set_source_rgb(0.4, 0.4, 0.4)
    ctx.arc(character_x, character_y, 50, 0, 2 * 3.14159)
    ctx.fill()
    
    # Label
    ctx.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(20)
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(character_x - 40, character_y + 80)
    ctx.show_text("CHARACTER")
    
    # Save background
    surface.write_to_png('manga_background.png')
    
    # Generate bubble positioned above character
    bubble_surf, meta = adaptive_circle_bubble(
        text="I must protect everyone!",
        variant='radial6',
        canvas_size=(400, 300),  # Smaller canvas for the bubble
        tail_target=(200, 280),  # Tail points downward to character (relative to bubble canvas)
        wrap=True,
        max_lines=2,
        target_inner_padding=25,
    )
    
    # Composite bubble onto manga
    bg = Image.open('manga_background.png').convert('RGBA')
    bubble_pil = Image.frombuffer(
        'RGBA',
        (bubble_surf.get_width(), bubble_surf.get_height()),
        bubble_surf.get_data(), 'raw', 'BGRA', 0, 1
    )
    
    # Position bubble above character
    bubble_x = character_x - bubble_surf.get_width() // 2
    bubble_y = character_y - 400  # Above character
    
    bg.paste(bubble_pil, (bubble_x, bubble_y), bubble_pil)
    bg.save('manga_with_bubble_positioned.png')
    
    print("✅ Saved: manga_with_bubble_positioned.png")
    print(f"Bubble metadata: {meta}")
    print(f"Tail points: {meta['tail_points']}")


def demo_multiple_bubbles():
    """Demo: Multiple characters with dialogue"""
    
    panel_width, panel_height = 1000, 1400
    
    # Create manga panel background
    background = Image.new('RGBA', (panel_width, panel_height), (250, 248, 245, 255))
    
    # Define scene with multiple characters
    characters = [
        {'name': 'Hero', 'pos': (200, 1000), 'color': (100, 150, 200)},
        {'name': 'Sidekick', 'pos': (400, 1050), 'color': (150, 100, 150)},
        {'name': 'Villain', 'pos': (750, 950), 'color': (200, 100, 100)},
    ]
    
    # Draw character placeholders
    from PIL import ImageDraw
    draw = ImageDraw.Draw(background)
    for char in characters:
        x, y = char['pos']
        draw.ellipse((x-40, y-60, x+40, y+60), fill=char['color'])
        draw.text((x-30, y+70), char['name'], fill='black')
    
    background.save('manga_scene.png')
    
    # Dialogue sequence
    dialogues = [
        {
            'text': 'We have to stop him now!',
            'speaker_pos': characters[0]['pos'],
            'bubble_pos': (200, 700),  # Upper left
            'variant': 'radial5',
        },
        {
            'text': "I'm with you!",
            'speaker_pos': characters[1]['pos'],
            'bubble_pos': (450, 780),  # Upper middle
            'variant': 'radial6',
        },
        {
            'text': 'You fools cannot defeat me!',
            'speaker_pos': characters[2]['pos'],
            'bubble_pos': (750, 650),  # Upper right
            'variant': 'radial7',
        },
    ]
    
    # Create composite with all bubbles
    result = background.copy()
    
    for i, dialogue in enumerate(dialogues):
        # Calculate tail target (relative to canvas)
        bubble_canvas_w, bubble_canvas_h = 450, 350
        bubble_center_x = bubble_canvas_w // 2
        bubble_center_y = bubble_canvas_h // 2
        
        # Speaker position in panel coordinates
        speaker_x, speaker_y = dialogue['speaker_pos']
        # Bubble position in panel coordinates
        bubble_x, bubble_y = dialogue['bubble_pos']
        
        # Tail target in bubble's local canvas
        tail_target_local = (
            speaker_x - (bubble_x - bubble_center_x),
            speaker_y - (bubble_y - bubble_center_y)
        )
        
        # Generate bubble
        bubble_surf, meta = adaptive_circle_bubble(
            text=dialogue['text'],
            variant=dialogue['variant'],
            canvas_size=(bubble_canvas_w, bubble_canvas_h),
            tail_target=tail_target_local,
            wrap=True,
            max_lines=2,
            target_inner_padding=28,
            seed=1000 + i,
        )
        
        # Convert to PIL
        bubble_pil = Image.frombuffer(
            'RGBA',
            (bubble_surf.get_width(), bubble_surf.get_height()),
            bubble_surf.get_data(), 'raw', 'BGRA', 0, 1
        )
        
        # Composite at position
        paste_x = bubble_x - bubble_center_x
        paste_y = bubble_y - bubble_center_y
        result.paste(bubble_pil, (paste_x, paste_y), bubble_pil)
        
        print(f"Bubble {i+1}: '{dialogue['text'][:30]}...'")
        print(f"  Position: ({bubble_x}, {bubble_y}) -> Speaker: {dialogue['speaker_pos']}")
        print(f"  Tail points: {meta['tail_points']}")
    
    result.save('manga_multiple_bubbles.png')
    print("\n✅ Saved: manga_multiple_bubbles.png")


# Advanced: Using OpenCV for person detection (optional)
def demo_with_face_detection():
    """Demo: Automatic character detection using OpenCV (requires opencv-python)"""
    
    try:
        import cv2
    except ImportError:
        print("⚠️  OpenCV not installed. Run: pip install opencv-python")
        print("   This demo shows how you would integrate face/person detection")
        return
    
    manga_path = 'your_manga_panel.png'
    
    # Load image
    img = cv2.imread(manga_path)
    if img is None:
        print(f"Could not load {manga_path}")
        return
    
    # Use Haar Cascade for face detection (simple approach)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    print(f"Detected {len(faces)} faces")
    
    # For each detected face, you can position a bubble
    for i, (x, y, w, h) in enumerate(faces):
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Position bubble above face
        bubble_pos = (center_x, y - 200)
        
        print(f"Face {i+1} at ({center_x}, {center_y}), bubble at {bubble_pos}")
        
        # Generate bubble with tail pointing to face center
        # ... (similar to previous examples)


if __name__ == '__main__':
    print("=== Manga Bubble Compositing Demo ===\n")
    
    print("1. Simple manual positioning:")
    demo_simple_positioning()
    print()
    
    print("2. Offset bubble positioning:")
    demo_offset_bubbles()
    print()
    
    print("3. Multiple character dialogue:")
    demo_multiple_bubbles()
    print()
    
    print("\n=== Summary ===")
    print("✅ Generated test images with bubbles positioned on manga panels")
    print("✅ Tails automatically point toward character positions")
    print("\nTo use with your own manga:")
    print("1. Replace 'your_manga_panel.png' with your image path")
    print("2. Adjust character_positions coordinates")
    print("3. Set bubble_pos for each dialogue")
    print("4. Run the script!")

