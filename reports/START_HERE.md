# 🎯 START HERE - Testing Bubbles on Manga

## ⚡ One-Command Quick Start

```bash
# Install dependencies and run test
pip3 install pillow && python3 simple_manga_test.py
```

**Done!** Check `test_manga_with_bubble.png` 🎉

---

## 📦 What I Created For You

### Files Ready to Use:

1. **`simple_manga_test.py`** ⭐ **USE THIS FIRST**
   - Easiest way to test
   - Creates test manga panels
   - Shows working code examples
   - No configuration needed

2. **`HOW_TO_RUN.md`**
   - Step-by-step instructions
   - Troubleshooting guide
   - All commands you need

3. **`MANGA_TESTING_GUIDE.md`**
   - Complete documentation
   - Advanced techniques
   - Coordinate system explained

4. **`quick_manga_test.py`** & **`test_manga_composite.py`**
   - Advanced Cairo bubble examples
   - Multiple character dialogues

---

## 🚀 How To Run (3 Steps)

### Step 1: Install Dependencies

```bash
pip3 install pillow
```

**Optional** (for advanced Cairo bubbles):
```bash
pip3 install pycairo
```

### Step 2: Run The Test

```bash
cd /Users/ihoroderii/wrk/bubble
python3 simple_manga_test.py
```

### Step 3: View Results

```bash
open test_manga_with_bubble.png
```

Or just double-click the file in Finder!

---

## 💡 Using With Your Manga

### Option A: Simple Way (Copy This Code)

Create a new file `my_test.py`:

```python
from PIL import Image, ImageDraw
from manhwa_bubbles import speech_bubble

# 1. Load your manga
manga = Image.open('my_manga.png')  # ← Your file here
draw = ImageDraw.Draw(manga)

# 2. Add bubble (adjust coordinates to fit your manga)
#    Format: (x, y, width, height)
speech_bubble(draw, (150, 100, 250, 80), 
              "Your dialogue here!",
              bubble_type='oval', 
              tail_dir='down')

# 3. Save
manga.save('manga_with_bubble.png')
print("✅ Done! Check manga_with_bubble.png")
```

Run it:
```bash
python3 my_test.py
```

### Option B: Finding Coordinates

1. Open your manga in any image editor (Preview, GIMP, Photoshop, etc.)
2. Hover your mouse over the character's head
3. Note the (x, y) coordinates shown
4. Use those coordinates in your script

**Example:**
```
Character head at: (320, 850)
↓
Place bubble above: (320 - 125, 850 - 200) = (195, 650)
↓
speech_bubble(draw, (195, 650, 250, 80), "Text here!")
```

---

## 🎨 Bubble Types Available

```python
# Normal speech
speech_bubble(draw, xy, text, bubble_type='oval')

# Thought bubble
speech_bubble(draw, xy, text, bubble_type='cloud')

# Shouting
speech_bubble(draw, xy, text, bubble_type='jagged')

# Nervous/shaky
speech_bubble(draw, xy, text, bubble_type='wavy')

# Evil/dark
speech_bubble(draw, xy, text, bubble_type='black')
```

**Tail directions:** `'down'`, `'up'`, `'left'`, `'right'`

---

## 🔍 Quick Test Checklist

Before running, make sure:

```bash
# Check Python is installed
python3 --version
# Should show: Python 3.x.x

# Check you're in the right directory
pwd
# Should show: /Users/ihoroderii/wrk/bubble

# Check Pillow is installed
python3 -c "import PIL; print('✅ PIL installed')"
# Should show: ✅ PIL installed

# Run the test
python3 simple_manga_test.py
# Should create test_manga_with_bubble.png
```

---

## ❓ Common Issues

### "No module named 'PIL'"
```bash
pip3 install pillow
```

### "python3: command not found"
Try `python` instead:
```bash
python simple_manga_test.py
```

### "No such file or directory: 'my_manga.png'"
Make sure your manga image is in the same folder:
```bash
ls my_manga.png
```

---

## 📖 What Each File Does

| File | Purpose | When to Use |
|------|---------|-------------|
| `simple_manga_test.py` | Creates test manga with bubbles | **Start here!** Learn how it works |
| `my_test.py` | Your custom script | After understanding the test |
| `HOW_TO_RUN.md` | Detailed instructions | If you need help |
| `MANGA_TESTING_GUIDE.md` | Full documentation | For advanced usage |

---

## 🎯 Workflow Summary

```
1. Run test script → See how it works
   python3 simple_manga_test.py
   
2. Create your script → Copy the example code
   nano my_test.py
   
3. Find coordinates → Open manga in image viewer
   open my_manga.png
   
4. Adjust positions → Edit x,y values
   speech_bubble(draw, (x, y, 250, 80), ...)
   
5. Run your script → Generate result
   python3 my_test.py
   
6. Check output → View final image
   open manga_with_bubble.png
```

---

## ✅ Next Steps

1. **Right now:** Run `python3 simple_manga_test.py`
2. **Then:** Look at the generated `test_manga_with_bubble.png`
3. **Then:** Read the example code in `simple_manga_test.py`
4. **Then:** Try with your own manga!

---

## 🆘 Need More Help?

- **Quick how-to:** `HOW_TO_RUN.md`
- **Full guide:** `MANGA_TESTING_GUIDE.md`
- **Code examples:** Look inside `simple_manga_test.py`

---

## 📝 TL;DR

```bash
# Install
pip3 install pillow

# Test
python3 simple_manga_test.py

# View
open test_manga_with_bubble.png

# Done! 🎉
```

That's literally all you need to get started!

