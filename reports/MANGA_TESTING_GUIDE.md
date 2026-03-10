# Testing Bubbles on Manga Images - Complete Guide

This guide shows you how to add speech bubbles to manga/manhwa panels with automatic tail positioning toward characters.

## 🎯 What You'll Learn

1. **Position bubbles** on manga panels
2. **Detect character positions** (manually or automatically)
3. **Point tails** toward the speaking character
4. **Composite bubbles** onto your manga artwork

---

## 📋 Prerequisites

```bash
# Install required packages
pip install pillow pycairo numpy

# Optional: For automatic person detection
pip install opencv-python
```

---

## 🚀 Quick Start

### Method 1: Simple Single Bubble

Use `quick_manga_test.py` for the easiest approach:

```python
# Edit these variables at the top of quick_manga_test.py:

MANGA_IMAGE = 'my_manga.png'  # Your manga panel
CHARACTER_HEAD_POSITION = (300, 400)  # Where the character's head is
DIALOGUE_TEXT = "This is a test bubble!"
BUBBLE_POSITION = (400, 200)  # Where to place the bubble

# Then run:
python quick_manga_test.py
```

**Output**: `manga_with_bubble.png` with your bubble added!

---

## 📐 How Coordinates Work

### Understanding the Coordinate System

```
Manga Panel (800x1200):
┌─────────────────────────────┐
│ (0,0)              (800,0)  │
│                              │
│     Bubble at (400,200)      │
│         ╭─────────╮          │
│         │ Hello!  │          │
│         ╰─────┬───╯          │
│               │ tail         │
│               ▼              │
│         Character (300,400)  │
│            👤                │
│                              │
│ (0,1200)          (800,1200)│
└─────────────────────────────┘
```

### Key Coordinate Concepts

1. **Character Position**: `(x, y)` of the character's head/face
2. **Bubble Position**: `(x, y)` where you want the bubble center
3. **Tail Target**: Calculated automatically to point from bubble → character

---

## 💡 Step-by-Step Workflow

### Step 1: Find Character Position

Open your manga image in any image editor and hover over the character's head to get coordinates:

- **GIMP**: Bottom-left corner shows coordinates
- **Photoshop**: Info panel shows cursor position  
- **Preview (Mac)**: Tools → Show Inspector → hover over image
- **Paint.NET**: Status bar shows coordinates

**Example**:
```
Character head at pixel (320, 450)
→ Use CHARACTER_HEAD_POSITION = (320, 450)
```

### Step 2: Choose Bubble Position

Position the bubble where you want it (usually above/beside the character):

```python
# Above character
BUBBLE_POSITION = (320, 250)  # Same x, smaller y

# Above-left
BUBBLE_POSITION = (200, 250)

# Above-right  
BUBBLE_POSITION = (450, 250)
```

### Step 3: Run the Script

```bash
python quick_manga_test.py
```

The tail will automatically point from the bubble toward the character! 🎉

---

## 🎨 Multiple Bubbles (Dialogue)

For conversations between multiple characters:

```python
from quick_manga_test import batch_add_bubbles

dialogues = [
    {
        'text': 'We have to stop him!',
        'char_pos': (200, 600),      # Left character
        'bubble_pos': (250, 400),    # Bubble above-left
        'variant': 'radial5',
        'size': (450, 350)
    },
    {
        'text': "I'm with you!",
        'char_pos': (600, 620),      # Right character  
        'bubble_pos': (650, 420),    # Bubble above-right
        'variant': 'radial6',
        'size': (400, 320)
    },
]

batch_add_bubbles(dialogues)
```

---

## 🤖 Automatic Person Detection (Advanced)

For automatic character detection using OpenCV:

```python
import cv2
from adaptive_bubbles import adaptive_circle_bubble
from PIL import Image

# Load manga panel
manga = cv2.imread('my_manga.png')

# Detect faces
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
gray = cv2.cvtColor(manga, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# For each detected face
for (x, y, w, h) in faces:
    char_pos = (x + w//2, y + h//2)  # Face center
    bubble_pos = (char_pos[0], char_pos[1] - 200)  # Above face
    
    # Generate bubble with tail pointing to face
    # ... (see quick_manga_test.py for complete code)
```

**Note**: Face detection works best on:
- Clear, frontal faces
- Well-lit panels
- Manga with detailed character art

For stylized/simplified manga art, manual positioning is more reliable.

---

## 🎭 Bubble Variants

Choose different bubble styles:

| Variant | Description | Best For |
|---------|-------------|----------|
| `radial5` | 5 overlapping ovals | Normal speech |
| `radial6` | 6 overlapping ovals | Excited speech |
| `radial7` | 7 overlapping ovals | Energetic/laugh |

```python
bubble_surf, meta = adaptive_circle_bubble(
    text="Amazing!",
    variant='radial7',  # More energetic
    canvas_size=(500, 400),
    tail_target=(char_x, char_y),
    wrap=True,
    max_lines=2,
)
```

---

## 🔧 Troubleshooting

### Problem: Tail points wrong direction

**Solution**: Check your coordinate calculations:

```python
# Bubble canvas is (600, 600), centered at (300, 300)
# Character in manga at (400, 800)
# Bubble paste position in manga: (200, 100)

# Correct tail target (relative to bubble canvas):
tail_target = (
    400 - 200,  # char_x - bubble_paste_x = 200
    800 - 100   # char_y - bubble_paste_y = 700
)
```

### Problem: Bubble too large/small

**Solution**: Adjust bubble canvas size:

```python
# Larger bubble for long text
canvas_size=(700, 500)

# Smaller bubble for short text  
canvas_size=(400, 300)
```

### Problem: Text doesn't fit

**Solution**: Enable wrapping and increase padding:

```python
adaptive_circle_bubble(
    text="Very long text that needs wrapping",
    wrap=True,
    max_lines=3,  # Allow more lines
    target_inner_padding=40,  # More space
)
```

---

## 📖 Complete Example

Here's a full workflow example:

```python
from PIL import Image
from adaptive_bubbles import adaptive_circle_bubble

# 1. Load your manga panel
manga = Image.open('chapter1_page5.png').convert('RGBA')

# 2. Define character position (measured in image editor)
hero_head = (320, 850)

# 3. Choose bubble position (above hero)
bubble_center = (350, 600)

# 4. Calculate canvas and tail target
bubble_size = (500, 400)
bubble_canvas_center = (250, 200)  # bubble_size[0]//2, bubble_size[1]//2

bubble_paste_x = bubble_center[0] - bubble_canvas_center[0]
bubble_paste_y = bubble_center[1] - bubble_canvas_center[1]

tail_local = (
    hero_head[0] - bubble_paste_x,
    hero_head[1] - bubble_paste_y
)

# 5. Generate bubble
bubble_surf, meta = adaptive_circle_bubble(
    text="I won't give up!",
    variant='radial6',
    canvas_size=bubble_size,
    tail_target=tail_local,
    wrap=True,
    max_lines=2,
)

# 6. Composite onto manga
bubble_pil = Image.frombuffer(
    'RGBA',
    (bubble_surf.get_width(), bubble_surf.get_height()),
    bubble_surf.get_data(),
    'raw', 'BGRA', 0, 1
)

result = manga.copy()
result.paste(bubble_pil, (bubble_paste_x, bubble_paste_y), bubble_pil)
result.save('chapter1_page5_lettered.png')

print(f"✅ Saved! Tail points from {meta['tail_points']}")
```

---

## 🎓 Tips & Best Practices

### Positioning Tips

1. **Place bubbles in empty space** (sky, walls, backgrounds)
2. **Above or beside** characters, not covering their faces
3. **Reading order**: Top-to-bottom, right-to-left (manga) or left-to-right (manhwa)
4. **Tail length**: Default 55% of bubble radius usually works well

### Text Tips

1. **Keep it short**: 1-2 lines per bubble for readability
2. **ALL CAPS** for shouting (use `variant='radial7'`)
3. **lowercase** for whispers or thoughts
4. **Break long speeches** into multiple bubbles

### Visual Tips

1. **Avoid tail crossing**: Position bubbles so tails don't cross each other
2. **Group by speaker**: Keep one character's bubbles together
3. **Z-order**: Add bubbles back-to-front so they layer correctly

---

## 📦 Files in This Project

- `quick_manga_test.py` - **Start here!** Simplest single-bubble test
- `test_manga_composite.py` - Advanced multi-bubble examples
- `adaptive_bubbles.py` - Core bubble generation engine
- `MANGA_TESTING_GUIDE.md` - This guide

---

## 🚀 Next Steps

1. Try `quick_manga_test.py` with a test image
2. Measure character positions in your manga
3. Adjust bubble positions and run again
4. Experiment with different variants and sizes
5. Batch process multiple pages!

---

## ❓ FAQ

**Q: Can I change the tail style?**  
A: Yes! The `tail_style` parameter supports different styles (though currently only 'triangle' is fully implemented).

**Q: How do I make bubbles without tails?**  
A: Set `tail_target=None` when calling `adaptive_circle_bubble()`.

**Q: Can I use rectangular bubbles?**  
A: Yes! Use `adaptive_square_bubble()` instead of `adaptive_circle_bubble()`.

**Q: How do I adjust font size?**  
A: The font auto-scales to fit. Use `target_inner_padding` to control spacing (more padding = smaller font).

---

## 🆘 Need Help?

1. Check the examples in `quick_manga_test.py`
2. Review the coordinate calculations in this guide
3. Test with a simple image first before using complex manga panels

Happy lettering! 🎨📖

