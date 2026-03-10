# Why YOLO Isn't Detecting People

## 🔍 The Problem

YOLO detected 0 people in your manga. Here's why and how to fix it:

---

## 💡 Why This Happens

### **YOLO is trained on real photos, not manga art**

YOLO's training data (COCO dataset) contains:
- ✅ Real photos of people
- ✅ Realistic 3D shapes and proportions
- ✅ Natural lighting and textures

Your manga has:
- ❌ Stylized 2D art
- ❌ Simplified shapes (big eyes, small nose, etc.)
- ❌ Flat colors and line art

**Result:** YOLO doesn't recognize stylized manga characters as "people"

---

## 🔧 Solutions (In Order of Effectiveness)

### **Solution 1: Use Anime Face Detector** ⭐ **BEST FOR MANGA**

Specialized library trained specifically on anime/manga:

```bash
# Install
pip3 install anime-face-detector

# Use it
python3 -c "
from anime_face_detector import create_detector
detector = create_detector('yolov3')
preds = detector('my_manga.png')
print(f'Found {len(preds)} anime faces!')
for pred in preds:
    print(f'  Face at: {pred[\"bbox\"]}')
"
```

**Why this works:** Trained on anime/manga art, not photos!

---

### **Solution 2: Manual Click Method** ⭐⭐ **100% RELIABLE**

Use the manual character selection:

```python
import cv2

def select_characters(manga_path):
    positions = []
    img = cv2.imread(manga_path)
    
    def click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            positions.append((x, y))
            print(f"Character {len(positions)} at ({x}, {y})")
            cv2.circle(img, (x, y), 10, (0, 255, 0), -1)
            cv2.imshow('Click on heads (ESC when done)', img)
    
    cv2.imshow('Click on heads (ESC when done)', img)
    cv2.setMouseCallback('Click on heads (ESC when done)', click)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return positions

# Use it
characters = select_characters('my_manga.png')
print(f"Marked {len(characters)} characters")

# Then add bubbles at those positions
```

**Why this works:** You know where characters are better than any AI!

---

### **Solution 3: Lower YOLO Confidence** 

Try extremely low confidence (might work for semi-realistic manga):

```python
from yolo_manga_detector import MangaPersonDetector

detector = MangaPersonDetector(confidence=0.05)  # Very low!
detections = detector.detect_people('my_manga.png', visualize=True)
```

**Try these confidence levels:**
- `0.05` - Extremely sensitive (many false positives)
- `0.10` - Very sensitive
- `0.15` - Sensitive
- `0.20` - Moderate

**Check the visualization** (`detected_people.png`) to see what YOLO thinks are people.

---

### **Solution 4: Use Larger YOLO Model**

Larger models are sometimes better at stylized art:

```python
detector = MangaPersonDetector(
    model_name='yolov8m.pt',  # Larger model
    confidence=0.1
)
```

Models in order of size/accuracy:
- `yolov8n.pt` - Nano (6 MB) - what you tried
- `yolov8s.pt` - Small (22 MB)
- `yolov8m.pt` - Medium (52 MB) - better for manga
- `yolov8l.pt` - Large (87 MB) - best but slowest

---

### **Solution 5: Train Custom YOLO**

Train YOLO specifically on manga art:

1. Collect 100+ manga panels
2. Label people in each panel
3. Train YOLO on your dataset

See: https://docs.ultralytics.com/modes/train/

**Time investment:** Several hours to days

---

## 🎯 Recommended Approach

### For Your Situation:

1. **First, try Anime Face Detector** (specifically designed for manga)
2. **If that fails, use Manual Click** (always works, takes 2 seconds per character)
3. **Skip YOLO for now** (better for realistic art)

---

## 🔍 Diagnostic Test

Run this to see what YOLO actually detects:

```bash
python3 test_yolo_simple.py my_manga.png
```

This will:
- Check all dependencies
- Test different confidence levels
- Show what YOLO sees
- Recommend best approach

---

## 📊 When to Use Each Method

| Your Manga Style | Best Method | Why |
|------------------|-------------|-----|
| Very stylized/chibi | **Manual Click** | AI won't recognize it |
| Anime-style | **Anime Face Detector** | Trained on anime art |
| Semi-realistic | **YOLO (low confidence)** | Might work with conf=0.05 |
| Realistic | **YOLO (normal)** | Works great |

---

## 💡 Quick Fix Right Now

### **Option A: Use Manual Selection** (2 minutes)

```python
# File: quick_fix.py
import cv2
from PIL import Image, ImageDraw
from manhwa_bubbles import speech_bubble

# 1. Load manga and select characters
positions = []
img = cv2.imread('my_manga.png')

def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        positions.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('Click heads', img)

cv2.imshow('Click heads', img)
cv2.setMouseCallback('Click heads', click)
print("Click on character heads, then press ESC")
cv2.waitKey(0)
cv2.destroyAllWindows()

# 2. Add bubbles
manga = Image.open('my_manga.png').convert('RGBA')
draw = ImageDraw.Draw(manga)

dialogues = ["Text 1", "Text 2", "Text 3"]
for pos, text in zip(positions, dialogues):
    bubble_x = pos[0] - 125
    bubble_y = pos[1] - 200
    speech_bubble(draw, (bubble_x, bubble_y, 250, 80), text)

manga.save('result.png')
print("✅ Saved result.png")
```

Run it:
```bash
python3 quick_fix.py
```

---

### **Option B: Install Anime Face Detector**

```bash
pip3 install anime-face-detector

python3 -c "
from anime_face_detector import create_detector
detector = create_detector('yolov3')
faces = detector('my_manga.png')
print(f'Detected {len(faces)} anime faces:')
for i, face in enumerate(faces):
    x, y, w, h = face['bbox']
    print(f'  Face {i+1} at ({x+w//2}, {y+h//2})')
"
```

---

## ✅ Summary

**YOLO didn't detect people because:**
- YOLO is trained on photos, not manga art
- Your manga art is too stylized for photo-trained models

**Best solutions:**
1. ⭐ **Anime Face Detector** - Built for manga/anime
2. ⭐⭐ **Manual Click** - Always works, very fast
3. Lower YOLO confidence to 0.05 (might work)

**Try this now:**
```bash
python3 test_yolo_simple.py my_manga.png
```

This will diagnose the issue and recommend the best approach for your manga style.

