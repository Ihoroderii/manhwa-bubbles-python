# YOLO Manga Character Detection - Usage Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip3 install ultralytics opencv-python pillow
```

This installs:
- **ultralytics**: YOLO v8 (AI person detection)
- **opencv-python**: Image processing
- **pillow**: Image manipulation

### 2. Run the Demo

```bash
cd /Users/ihoroderii/wrk/bubble
python3 yolo_manga_detector.py
```

This will:
1. Create a test manga panel with 3 characters
2. Detect people using YOLO
3. Automatically add speech bubbles above them
4. Save results

**Output files:**
- `test_manga_for_yolo.png` - Test manga panel
- `detected_people.png` - Shows where YOLO found people
- `manga_with_yolo_bubbles.png` - Final result with bubbles

---

## 📖 Use With Your Own Manga

### Method 1: Command Line

```bash
python3 yolo_manga_detector.py my_manga.png "Hello!" "How are you?" "Great!"
```

- First argument: Your manga image file
- Remaining arguments: Dialogue for each detected person (left to right)

### Method 2: Python Script

Create `my_yolo_test.py`:

```python
from yolo_manga_detector import process_your_manga

# Process your manga
process_your_manga(
    manga_path='my_manga.png',
    dialogues=[
        "We need to escape!",
        "I'll cover you!",
        "Let's go!"
    ],
    confidence=0.3  # Lower = detect more people (0.1-0.9)
)
```

Run it:
```bash
python3 my_yolo_test.py
```

### Method 3: Advanced Usage

```python
from yolo_manga_detector import MangaPersonDetector, add_bubbles_to_detected_people

# Initialize detector
detector = MangaPersonDetector(
    model_name='yolov8n.pt',  # Options: yolov8n, yolov8s, yolov8m, yolov8l
    confidence=0.25           # Detection threshold
)

# Detect people
detections = detector.detect_people('my_manga.png', visualize=True)

# Check what was detected
for i, det in enumerate(detections):
    print(f"Person {i+1}:")
    print(f"  Head position: {det['head_pos']}")
    print(f"  Bounding box: {det['bbox']}")
    print(f"  Confidence: {det['confidence']:.2f}")

# Add bubbles
add_bubbles_to_detected_people(
    manga_path='my_manga.png',
    detections=detections,
    dialogues=["Text 1", "Text 2", "Text 3"],
    bubble_offset_y=200,  # Distance above head
    output_path='result.png'
)
```

---

## ⚙️ Configuration Options

### YOLO Model Selection

| Model | Speed | Accuracy | File Size |
|-------|-------|----------|-----------|
| `yolov8n.pt` | ⚡⚡⚡ Fastest | 🎯🎯 Good | 6 MB |
| `yolov8s.pt` | ⚡⚡ Fast | 🎯🎯🎯 Better | 22 MB |
| `yolov8m.pt` | ⚡ Medium | 🎯🎯🎯🎯 Great | 52 MB |
| `yolov8l.pt` | 🐌 Slow | 🎯🎯🎯🎯🎯 Best | 87 MB |

**Recommendation:** Start with `yolov8n.pt` (fastest, good enough)

### Confidence Threshold

```python
confidence=0.25  # Default (balanced)
confidence=0.15  # Detect more people (more false positives)
confidence=0.50  # Detect fewer people (more conservative)
```

**Lower confidence** = More detections (may include false positives)  
**Higher confidence** = Fewer detections (only very clear people)

### Bubble Positioning

```python
add_bubbles_to_detected_people(
    manga_path='my_manga.png',
    detections=detections,
    dialogues=["Text"],
    bubble_offset_y=200,  # ← Adjust this
    # 150 = Close to head
    # 250 = Far from head
)
```

---

## 🎯 How It Works

### 1. YOLO Detection

```
Your Manga → YOLO Model → Bounding Boxes
                         ↓
                    [Person 1: (x1,y1,x2,y2)]
                    [Person 2: (x3,y3,x4,y4)]
```

YOLO finds people in the image and returns bounding boxes.

### 2. Head Position Estimation

```
Bounding Box:
┌─────────────┐
│   (Head)    │ ← Top 15% of box
│      🙂     │
│             │
│    Body     │
│             │
└─────────────┘
```

We estimate the head is in the upper 15% of the detected person's bounding box.

### 3. Bubble Placement

```
        Bubble
       ╭───────╮
       │ Text! │
       ╰───┬───╯
           │
           ▼
        (Head)
```

Bubble is placed `bubble_offset_y` pixels above the estimated head position.

---

## 🐛 Troubleshooting

### "No people detected"

**Solutions:**
1. Lower confidence threshold:
   ```python
   detector = MangaPersonDetector(confidence=0.15)
   ```

2. Check your manga:
   - YOLO works best with clear human figures
   - Very stylized/chibi characters may not be detected
   - Try with more realistic manga art

3. Use visualization to debug:
   ```python
   detections = detector.detect_people('my_manga.png', visualize=True)
   # Check detected_people.png to see what YOLO found
   ```

### "Wrong people detected"

- Increase confidence threshold (0.4 or 0.5)
- Use a larger model (`yolov8s.pt` or `yolov8m.pt`)

### "Bubbles in wrong position"

- Adjust `bubble_offset_y`:
  ```python
  bubble_offset_y=150  # Closer to head
  bubble_offset_y=300  # Further from head
  ```

### "ModuleNotFoundError: No module named 'ultralytics'"

```bash
pip3 install ultralytics
```

---

## 📊 Example Results

### Detection Output

```
✅ Detected 3 people
Person 1:
  Head position: (250, 850)
  Bounding box: (200, 800, 300, 1150)
  Confidence: 0.87

Person 2:
  Head position: (500, 900)
  Bounding box: (450, 850, 550, 1200)
  Confidence: 0.92

Person 3:
  Head position: (750, 870)
  Bounding box: (700, 820, 800, 1170)
  Confidence: 0.85
```

### Bubble Placement

```
Added bubble 1: 'We need to escape!' at (125, 650)
Added bubble 2: 'I'll cover you!' at (375, 700)
Added bubble 3: 'Let's go!' at (625, 670)
```

---

## 🎓 Advanced: Training Custom Model

If YOLO doesn't work well with your manga style, you can train a custom model:

```python
from ultralytics import YOLO

# Train on your manga dataset
model = YOLO('yolov8n.pt')
model.train(data='manga_dataset.yaml', epochs=100)

# Use your custom model
detector = MangaPersonDetector(model_name='runs/detect/train/weights/best.pt')
```

See: https://docs.ultralytics.com/modes/train/

---

## 💡 Tips & Best Practices

1. **Test first**: Run demo to see if YOLO works with your manga style
2. **Adjust confidence**: Start at 0.25, adjust based on results
3. **Check visualization**: Always use `visualize=True` first time
4. **Sort detection**: Script sorts left-to-right automatically (reading order)
5. **Manual fallback**: If YOLO fails, use the manual click method instead

---

## 🆚 YOLO vs Other Methods

| Method | Manga Style | Speed | Accuracy | Setup |
|--------|-------------|-------|----------|-------|
| **YOLO** | Realistic | ⚡ Fast | 🎯🎯🎯🎯 | Medium |
| Anime Face Detector | Anime/Stylized | ⚡ Fast | 🎯🎯🎯🎯🎯 | Medium |
| OpenCV Cascade | Semi-realistic | ⚡⚡ Very Fast | 🎯🎯🎯 | Easy |
| Manual Click | Any | 🐌 Slow | 🎯🎯🎯🎯🎯 | Easy |

**YOLO is best for:**
- Realistic or semi-realistic manga
- Batch processing many pages
- When you need automation

**Not recommended for:**
- Very stylized/chibi art (use Anime Face Detector)
- Simple one-off pages (use Manual Click)

---

## 📚 Further Reading

- **YOLO Documentation**: https://docs.ultralytics.com/
- **Model Zoo**: https://github.com/ultralytics/ultralytics
- **Training Guide**: https://docs.ultralytics.com/modes/train/

---

## ✅ Quick Reference

```bash
# Install
pip3 install ultralytics opencv-python pillow

# Run demo
python3 yolo_manga_detector.py

# Process your manga
python3 yolo_manga_detector.py my_manga.png "Text 1" "Text 2"

# In Python
from yolo_manga_detector import process_your_manga
process_your_manga('manga.png', ['Hello!', 'Hi!'], confidence=0.3)
```

That's it! 🎉

