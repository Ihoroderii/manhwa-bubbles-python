# How to Run Manga Bubble Tests

## 🚀 Quick Start (2 steps!)

```bash
# 1. Install dependencies
pip3 install pillow pycairo

# 2. Run the test
python3 simple_manga_test.py
```

**That's it!** Open `test_manga_with_bubble.png` to see the result.

---

## 📋 What You Need

### Required
- Python 3.7+
- Pillow (PIL): `pip3 install pillow`

### Optional (for advanced Cairo bubbles)
- PyCairo: `pip3 install pycairo`

---

## 🎯 Available Test Scripts

### 1. **`simple_manga_test.py`** ⭐ START HERE
The easiest way to test bubbles:

```bash
python3 simple_manga_test.py
```

**What it does:**
- Creates a test manga panel with characters
- Adds speech bubbles
- Saves `test_manga_with_bubble.png`
- Shows you example code for your own manga

**No configuration needed** - just run it!

---

### 2. **`quick_manga_test.py`** (Advanced Cairo bubbles)
Uses the adaptive Cairo bubble system:

```bash
# Edit these lines first:
MANGA_IMAGE = 'my_manga.png'
CHARACTER_HEAD_POSITION = (300, 400)
BUBBLE_POSITION = (400, 200)
DIALOGUE_TEXT = "Your text!"

# Then run:
python3 quick_manga_test.py
```

**Requires:** `pycairo` installed

---

### 3. **`test_manga_composite.py`** (Full examples)
Complete examples with multiple characters:

```bash
python3 test_manga_composite.py
```

---

## 📖 Using With Your Own Manga

### Method 1: Simple PIL Bubbles (Easiest)

```python
from PIL import Image, ImageDraw
from manhwa_bubbles import speech_bubble

# Load your manga
manga = Image.open('my_manga.png')
draw = ImageDraw.Draw(manga)

# Add bubble (x, y, width, height)
speech_bubble(draw, (100, 50, 250, 80), "Hello!", 
              bubble_type='oval', tail_dir='down')

# Save
manga.save('output.png')
```

**Run it:**
```bash
python3 your_script.py
```

---

### Method 2: Get Character Positions

**Option A: Use an Image Editor**
1. Open your manga in GIMP / Photoshop / Preview
2. Hover cursor over character's head
3. Note the (x, y) coordinates shown
4. Use those in your script

**Option B: Quick Coordinate Checker**
```python
from PIL import Image

img = Image.open('my_manga.png')
print(f"Image size: {img.width} x {img.height}")

# Character roughly in center?
center_x = img.width // 2
center_y = img.height // 2
print(f"Center: ({center_x}, {center_y})")
```

---

## 🔧 Troubleshooting

### Error: `No module named 'PIL'`
**Fix:**
```bash
pip3 install pillow
# or
pip install pillow
```

### Error: `No module named 'cairo'`
**Fix:**
```bash
pip3 install pycairo
# or on Mac:
brew install cairo
pip3 install pycairo
```

### Error: `command not found: python3`
**Fix:** Use `python` instead:
```bash
python simple_manga_test.py
```

### My manga doesn't show up
Make sure the image file is in the same folder:
```bash
ls -l my_manga.png
```

---

## 📁 Project Structure

```
bubble/
├── simple_manga_test.py          ← START HERE (easiest)
├── quick_manga_test.py            ← Cairo bubbles
├── test_manga_composite.py        ← Full examples
├── HOW_TO_RUN.md                  ← This file
├── MANGA_TESTING_GUIDE.md         ← Detailed guide
├── manhwa_bubbles/                ← Main package
│   ├── speech_bubbles.py
│   ├── narrators.py
│   └── ...
└── examples/
    └── ...
```

---

## 🎓 Step-by-Step Tutorial

### Step 1: Run the test
```bash
python3 simple_manga_test.py
```

### Step 2: Check the output
```bash
open test_manga_with_bubble.png
# or on Linux:
xdg-open test_manga_with_bubble.png
```

### Step 3: Try with your manga
```python
# Create test_my_manga.py
from PIL import Image, ImageDraw
from manhwa_bubbles import speech_bubble

manga = Image.open('YOUR_FILE.png')  # ← Change this
draw = ImageDraw.Draw(manga)

# Adjust these coordinates:
bubble_region = (150, 100, 250, 80)  # (x, y, width, height)

speech_bubble(draw, bubble_region, "Test text!", 
              bubble_type='oval', tail_dir='down')

manga.save('result.png')
print("✅ Done! Check result.png")
```

### Step 4: Run your script
```bash
python3 test_my_manga.py
```

---

## 💡 Quick Tips

1. **Start simple** - Use `simple_manga_test.py` first
2. **Find coordinates** - Open manga in any image viewer, hover to get x,y
3. **Test positions** - Adjust bubble x,y until it looks good
4. **Save often** - Save intermediate results as you adjust

---

## 📚 More Help

- **Detailed guide:** Read `MANGA_TESTING_GUIDE.md`
- **Example code:** Check `simple_manga_test.py` for working examples
- **Bubble styles:** See `manhwa_bubbles/speech_bubbles.py` for all bubble types

---

## ✅ Checklist

Before running:
- [ ] Python 3 installed (`python3 --version`)
- [ ] Pillow installed (`pip3 list | grep -i pillow`)
- [ ] In the bubble directory (`ls simple_manga_test.py` works)

Ready to run:
```bash
python3 simple_manga_test.py
```

That's it! 🎉

