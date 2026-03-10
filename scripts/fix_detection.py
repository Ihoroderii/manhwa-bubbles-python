#!/usr/bin/env python3
"""
Quick fix for manga character detection when YOLO doesn't work.
This uses manual clicking - simple and 100% reliable!
"""

import cv2
from PIL import Image, ImageDraw
import sys

try:
    from manhwa_bubbles import speech_bubble
    MANHWA_AVAILABLE = True
except ImportError:
    MANHWA_AVAILABLE = False

def manual_character_selection(manga_path):
    """Click on characters to mark their positions."""
    
    print("="*70)
    print("MANUAL CHARACTER SELECTION")
    print("="*70)
    print()
    print("Instructions:")
    print("  1. Click on each character's HEAD")
    print("  2. Press ESC when done")
    print()
    
    positions = []
    img = cv2.imread(manga_path)
    
    if img is None:
        print(f"❌ Could not load image: {manga_path}")
        return []
    
    display_img = img.copy()
    
    def mouse_click(event, x, y, flags, param):
        nonlocal display_img
        if event == cv2.EVENT_LBUTTONDOWN:
            positions.append((x, y))
            print(f"  ✅ Character {len(positions)} at ({x}, {y})")
            
            # Draw marker
            cv2.circle(display_img, (x, y), 10, (0, 255, 0), -1)
            cv2.putText(display_img, str(len(positions)), (x+15, y-5),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Mark Characters', display_img)
    
    cv2.imshow('Mark Characters', display_img)
    cv2.setMouseCallback('Mark Characters', mouse_click)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print()
    print(f"✅ Marked {len(positions)} characters")
    return positions


def add_bubbles_manual(manga_path, positions, dialogues, output_path='manga_manual_bubbles.png'):
    """Add bubbles at manually selected positions."""
    
    print()
    print("Adding bubbles...")
    
    # Load manga
    manga = Image.open(manga_path).convert('RGBA')
    draw = ImageDraw.Draw(manga)
    
    # Add bubble for each position
    for i, (pos, text) in enumerate(zip(positions, dialogues)):
        head_x, head_y = pos
        
        # Position bubble above head
        bubble_x = head_x - 125
        bubble_y = head_y - 200
        
        # Keep bubble in bounds
        bubble_x = max(10, min(bubble_x, manga.width - 260))
        bubble_y = max(10, bubble_y)
        
        # Add bubble
        if MANHWA_AVAILABLE:
            speech_bubble(draw, (bubble_x, bubble_y, 250, 80),
                         text, bubble_type='oval', tail_dir='down')
        else:
            # Simple fallback bubble
            draw.ellipse((bubble_x, bubble_y, bubble_x+250, bubble_y+80),
                        fill='white', outline='black', width=3)
            draw.text((bubble_x+20, bubble_y+30), text, fill='black')
        
        print(f"  ✅ Added bubble {i+1}: '{text[:30]}...' at ({bubble_x}, {bubble_y})")
    
    # Save result
    manga.save(output_path)
    print()
    print(f"✅ SUCCESS! Saved: {output_path}")
    return manga


def main():
    """Main function."""
    
    print()
    print("="*70)
    print("MANUAL CHARACTER DETECTION + BUBBLE PLACEMENT")
    print("="*70)
    print()
    print("This method works with ANY manga style!")
    print("(YOLO doesn't work well with stylized manga art)")
    print()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  python3 {sys.argv[0]} manga.png 'Text 1' 'Text 2' 'Text 3'")
        print()
        print("Example:")
        print(f"  python3 {sys.argv[0]} my_manga.png 'Hello!' 'How are you?' 'Great!'")
        return
    
    manga_path = sys.argv[1]
    dialogues = sys.argv[2:] if len(sys.argv) > 2 else []
    
    # Get character positions by clicking
    positions = manual_character_selection(manga_path)
    
    if not positions:
        print("⚠️  No characters marked. Exiting.")
        return
    
    # Get dialogues if not provided
    if not dialogues:
        print()
        print("Enter dialogue for each character (or press Enter to skip):")
        dialogues = []
        for i in range(len(positions)):
            text = input(f"  Character {i+1}: ")
            if text:
                dialogues.append(text)
            else:
                dialogues.append(f"Character {i+1}")
    
    # Ensure we have enough dialogues
    while len(dialogues) < len(positions):
        dialogues.append(f"Character {len(dialogues)+1}")
    
    # Add bubbles
    add_bubbles_manual(manga_path, positions, dialogues)
    
    print()
    print("="*70)
    print("✅ COMPLETE!")
    print("="*70)
    print()
    print("Open manga_manual_bubbles.png to see the result!")
    print()


if __name__ == '__main__':
    main()

