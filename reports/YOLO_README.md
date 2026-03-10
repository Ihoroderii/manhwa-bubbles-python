# 🤖 YOLO Manga Character Detection

Automatically detect people in manga panels and add speech bubbles using AI!

---

## ⚡ Quick Start (3 Steps)

### Step 1: Install

```bash
cd /Users/ihoroderii/wrk/bubble
./install_yolo.sh
```

Or manually:
```bash
pip3 install ultralytics opencv-python pillow
```

### Step 2: Run Demo

```bash
python3 yolo_manga_detector.py
```

This creates a test manga and automatically:
- Detects all people
- Adds speech bubbles above them
- Saves the result

### Step 3: Use With Your Manga

```bash
python3 yolo_manga_detector.py my_manga.png "Hello!" "How are you?" "Great!"
```

**Done!** Check `output_my_manga.png` 🎉

---

## 📂 What I Created For You

### Main Files

1. **`yolo_manga_detector.py`** - Main YOLO detection script
   - Detects people in manga automatically
   - Positions bubbles above detected characters
   - Handles multiple people per panel

2. **`YOLO_USAGE.md`** - Complete documentation
   - Detailed usage examples
   - Configuration options
   - Troubleshooting guide

3. **`requirements-yolo.txt`** - Dependencies list
4. **`install_yolo.sh`** - One-click installer

---

## 🎯 How It Works

```
┌─────────────┐
│ Your Manga  │
└──────┬──────┘
       │
       ▼
┌─────────────┐    Detects people,
│ YOLO Model  │──► estimates head
└──────┬──────┘    positions
       │
       ▼
┌─────────────┐    Positions bubbles
│   Script    │──► above each person
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Final Image │    Manga with bubbles!
└─────────────┘
```

### Detection Process

1. **YOLO scans image** for people/characters
2. **Estimates head position** (top 15% of bounding box)
3. **Sorts left-to-right** (reading order)
4. **Places bubbles** above each head
5. **Adds dialogue** from your list

---

## 💡 Usage Examples

### Example 1: Simple Usage

```python
from yolo_manga_detector import process_your_manga

process_your_manga(
    'chapter1_page5.png',
    dialogues=['Text 1', 'Text 2', 'Text 3']
)
```

### Example 2: Adjust Detection

```python
from yolo_manga_detector import MangaPersonDetector, add_bubbles_to_detected_people

# Initialize with custom settings
detector = MangaPersonDetector(
    model_name='yolov8s.pt',  # Larger model = better accuracy
    confidence=0.3            # Lower = detect more people
)

# Detect
detections = detector.detect_people('my_manga.png', visualize=True)

# Add bubbles
add_bubbles_to_detected_people(
    'my_manga.png',
    detections,
    dialogues=['Hello!', 'Hi there!'],
    bubble_offset_y=250  # Distance above head
)
```

### Example 3: Check What Was Detected

```python
detector = MangaPersonDetector()
detections = detector.detect_people('manga.png', visualize=True)

# See detection details
for i, det in enumerate(detections):
    print(f"Person {i+1}:")
    print(f"  Head at: {det['head_pos']}")
    print(f"  Confidence: {det['confidence']:.2%}")
```

---

## ⚙️ Configuration

### Model Selection

Choose speed vs accuracy:

```python
# Fast (6 MB, good enough for most cases)
MangaPersonDetector(model_name='yolov8n.pt')

# Balanced (22 MB, better accuracy)
MangaPersonDetector(model_name='yolov8s.pt')

# Accurate (52 MB, best results)
MangaPersonDetector(model_name='yolov8m.pt')
```

### Detection Sensitivity

```python
# More sensitive (detects more people, may include false positives)
MangaPersonDetector(confidence=0.15)

# Balanced (default)
MangaPersonDetector(confidence=0.25)

# Conservative (only very clear detections)
MangaPersonDetector(confidence=0.50)
```

### Bubble Positioning

```python
add_bubbles_to_detected_people(
    manga_path='manga.png',
    detections=detections,
    dialogues=['Text'],
    bubble_offset_y=200,  # Adjust distance above head
    # 150 = closer to head
    # 300 = further from head
)
```

---

## 📊 When to Use YOLO

### ✅ YOLO Works Best For:

- **Realistic or semi-realistic manga**
- **Clear human figures** (full body or upper body)
- **Multiple pages** (batch processing)
- **Consistent art style** across pages

### ❌ YOLO May Struggle With:

- **Very stylized/chibi characters**
- **Abstract art styles**
- **Extreme close-ups** (face only)
- **Heavy shadows/occlusion**

**Alternative:** Use the manual click method (`simple_manga_test.py`) for difficult art styles.

---

## 🔍 Troubleshooting

### Problem: No People Detected

**Solutions:**
1. Lower confidence threshold:
   ```python
   detector = MangaPersonDetector(confidence=0.15)
   ```

2. Check visualization:
   ```python
   detector.detect_people('manga.png', visualize=True)
   # Look at detected_people.png
   ```

3. Try different model:
   ```python
   MangaPersonDetector(model_name='yolov8s.pt')  # More accurate
   ```

### Problem: Too Many False Detections

**Solutions:**
1. Increase confidence:
   ```python
   MangaPersonDetector(confidence=0.45)
   ```

2. Use larger model:
   ```python
   MangaPersonDetector(model_name='yolov8m.pt')
   ```

### Problem: Bubbles in Wrong Position

**Solutions:**
1. Adjust offset:
   ```python
   bubble_offset_y=300  # Try different values: 150, 200, 250, 300
   ```

2. Check head position estimation:
   ```python
   for det in detections:
       print(f"Head estimated at: {det['head_pos']}")
   ```

---

## 📖 Complete Workflow Example

```python
#!/usr/bin/env python3
"""Complete manga processing workflow."""

from yolo_manga_detector import MangaPersonDetector, add_bubbles_to_detected_people
from pathlib import Path

# Configuration
MANGA_FOLDER = Path('manga_pages')
OUTPUT_FOLDER = Path('processed_pages')
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Dialogues for each page
page_dialogues = {
    'page_01.png': ['We need to hurry!', 'I know!', 'This way!'],
    'page_02.png': ['Watch out!', 'Got it!'],
    'page_03.png': ['Are you okay?', 'I\'m fine, thanks!'],
}

# Initialize detector once
detector = MangaPersonDetector(model_name='yolov8s.pt', confidence=0.3)

# Process all pages
for page_file, dialogues in page_dialogues.items():
    print(f"\nProcessing {page_file}...")
    
    manga_path = MANGA_FOLDER / page_file
    
    # Detect people
    detections = detector.detect_people(str(manga_path), visualize=False)
    
    if len(detections) == 0:
        print(f"  ⚠️  No people detected in {page_file}")
        continue
    
    print(f"  ✅ Found {len(detections)} people")
    
    # Add bubbles
    output_path = OUTPUT_FOLDER / f'lettered_{page_file}'
    add_bubbles_to_detected_people(
        str(manga_path),
        detections,
        dialogues,
        bubble_offset_y=220,
        output_path=str(output_path)
    )
    
    print(f"  💾 Saved: {output_path}")

print("\n✅ All pages processed!")
```

---

## 🎓 Advanced: Custom Training

If YOLO doesn't work well with your manga style, train a custom model:

```python
from ultralytics import YOLO

# 1. Prepare dataset (see YOLO docs)
# 2. Train custom model
model = YOLO('yolov8n.pt')
results = model.train(
    data='manga_dataset.yaml',
    epochs=100,
    imgsz=640
)

# 3. Use custom model
detector = MangaPersonDetector(
    model_name='runs/detect/train/weights/best.pt'
)
```

See: https://docs.ultralytics.com/modes/train/

---

## 📚 Documentation

- **Quick Start**: This file (YOLO_README.md)
- **Detailed Guide**: `YOLO_USAGE.md`
- **General Manga Testing**: `MANGA_TESTING_GUIDE.md`
- **YOLO Official Docs**: https://docs.ultralytics.com/

---

## 🆚 Comparison with Other Methods

| Feature | YOLO | Anime Face Detector | Manual Click | OpenCV |
|---------|------|---------------------|--------------|---------|
| Setup | Medium | Medium | Easy | Easy |
| Speed | Fast | Fast | Slow | Very Fast |
| Accuracy (realistic) | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Accuracy (stylized) | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Batch processing | ✅ | ✅ | ❌ | ✅ |

**Recommendation:** Try YOLO first, fall back to manual if detection fails.

---

## ✅ Summary

You now have a complete YOLO-based manga character detection system!

**To use it:**

```bash
# 1. Install
./install_yolo.sh

# 2. Test
python3 yolo_manga_detector.py

# 3. Use
python3 yolo_manga_detector.py my_manga.png "Text 1" "Text 2"
```

**For help:**
- Read `YOLO_USAGE.md` for detailed instructions
- Check `yolo_manga_detector.py` code for examples
- See `MANGA_TESTING_GUIDE.md` for alternative methods

Happy manga lettering! 🎨📖

