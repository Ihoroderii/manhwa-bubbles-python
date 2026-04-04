#!/usr/bin/env python3
"""
Simple test: Add speech bubbles to manga using existing bubble functions.

This uses the organic_overlap bubble style that's already in your manhwa_bubbles package.

QUICK START:
1. python3 simple_manga_test.py
2. Opens test_manga_with_bubble.png
"""

from PIL import Image, ImageDraw, ImageFont
import sys

try:
    from manhwa_bubbles import speech_bubble
    print("✅ manhwa_bubbles package loaded")
except ImportError:
    print("⚠️  Installing from source...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
    from manhwa_bubbles import speech_bubble


def create_test_manga_panel():
    """Create a simple manga panel for testing."""
    # Create a manga-style panel
    panel = Image.new('RGB', (800, 1200), 'white')
    draw = ImageDraw.Draw(panel)
    
    # Add some manga-style elements
    # Border
    draw.rectangle([10, 10, 790, 1190], outline='black', width=3)
    
    # Draw simple characters (circles for heads)
    characters = [
        {'pos': (200, 900), 'name': 'Hero', 'color': (100, 150, 200)},
        {'pos': (600, 920), 'name': 'Friend', 'color': (150, 100, 150)},
    ]
    
    for char in characters:
        x, y = char['pos']
        # Head
        draw.ellipse([x-40, y-60, x+40, y+60], fill=char['color'], outline='black', width=2)
        # Body
        draw.ellipse([x-30, y+10, x+30, y+80], fill=char['color'], outline='black', width=2)
        # Label
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        except:
            font = ImageFont.load_default()
        draw.text((x-30, y+90), char['name'], fill='black', font=font)
    
    return panel, characters


def add_bubble_pil_style(panel, text, position, tail_direction='down'):
    """Add a bubble using PIL's built-in speech_bubble function."""
    draw = ImageDraw.Draw(panel)
    
    x, y = position
    # Create bubble region (x, y, width, height)
    bubble_region = (x, y, 250, 80)
    
    # Use the manhwa_bubbles speech_bubble function
    speech_bubble(draw, bubble_region, text, bubble_type='oval', tail_dir=tail_direction)
    
    return panel


def demo_simple():
    """Simplest demo - one bubble."""
    print("Creating test manga panel...")
    panel, characters = create_test_manga_panel()
    
    # Add speech bubble for the hero
    hero_pos = characters[0]['pos']
    bubble_pos = (hero_pos[0] - 125, hero_pos[1] - 200)  # Above hero
    
    print(f"Adding bubble at {bubble_pos} for character at {hero_pos}")
    panel = add_bubble_pil_style(panel, "We can do this!", bubble_pos, tail_direction='down')
    
    # Save result
    output = 'test_manga_with_bubble.png'
    panel.save(output)
    print(f"\n✅ SUCCESS! Saved: {output}")
    print(f"   Open this file to see your manga with a speech bubble!")
    
    return panel


def demo_multiple_bubbles():
    """Demo with multiple characters talking."""
    print("Creating manga panel with dialogue...")
    panel, characters = create_test_manga_panel()
    
    # Hero speaks
    hero_pos = characters[0]['pos']
    bubble1_pos = (hero_pos[0] - 125, hero_pos[1] - 220)
    panel = add_bubble_pil_style(panel, "We can do this!", bubble1_pos, tail_direction='down')
    
    # Friend responds
    friend_pos = characters[1]['pos']
    bubble2_pos = (friend_pos[0] - 125, friend_pos[1] - 160)
    panel = add_bubble_pil_style(panel, "I'm with you!", bubble2_pos, tail_direction='down')
    
    # Save result
    output = 'test_manga_dialogue.png'
    panel.save(output)
    print(f"\n✅ SUCCESS! Saved: {output}")
    print(f"   Multiple character dialogue added!")
    
    return panel


def demo_your_manga():
    """Example showing how to use with YOUR manga image."""
    print("\n" + "="*60)
    print("HOW TO USE WITH YOUR OWN MANGA:")
    print("="*60)
    
    example_code = '''
from PIL import Image, ImageDraw
from manhwa_bubbles import speech_bubble

# 1. Load your manga
manga = Image.open('your_manga.png')
draw = ImageDraw.Draw(manga)

# 2. Find character position (use image editor to get x,y)
character_head = (300, 800)  # Where character's head is

# 3. Position bubble above character
bubble_x = character_head[0] - 125  # Center bubble over character
bubble_y = character_head[1] - 200  # 200 pixels above head

# 4. Add bubble
bubble_region = (bubble_x, bubble_y, 250, 80)
speech_bubble(draw, bubble_region, "Your text here!", 
              bubble_type='oval', tail_dir='down')

# 5. Save
manga.save('manga_with_bubble.png')
print("Done!")
'''
    
    print(example_code)
    print("="*60)
    print("\n💡 TIP: Open your manga in any image editor")
    print("   Hover over character's head to get (x, y) coordinates")
    print("   Use those coordinates in 'character_head' above")
    print()


if __name__ == '__main__':
    print("="*60)
    print("MANGA BUBBLE TESTING - Simple Version")
    print("="*60)
    print()
    
    # Run demos
    print("DEMO 1: Single bubble")
    print("-" * 40)
    demo_simple()
    
    print("\n" + "-" * 40)
    print("DEMO 2: Multiple bubbles (dialogue)")
    print("-" * 40)
    demo_multiple_bubbles()
    
    # Show how to use with user's manga
    demo_your_manga()
    
    print("\n" + "="*60)
    print("✅ ALL DONE! Check the generated images:")
    print("   - test_manga_with_bubble.png")
    print("   - test_manga_dialogue.png")
    print("="*60)

