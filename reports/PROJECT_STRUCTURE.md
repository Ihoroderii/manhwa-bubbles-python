# Project Structure - Quick Reference

## 📦 Manhwa Bubbles v1.1.0

A Python library for creating professional manga/manhwa speech bubbles with YOLO-based auto-detection.

---

## 🗂️ Directory Structure

```
bubble/
├── manhwa_bubbles/          # 🎨 Main Library Package
│   ├── __init__.py          # Public API (40+ bubble styles)
│   ├── speech_bubbles.py    # Core PIL bubbles (10 types)
│   ├── narrators.py         # Narration boxes (5 styles)
│   ├── extended_styles.py   # Extended styles (40+)
│   ├── organic_overlap.py   # Cairo overlapping bubbles
│   └── auto_scale.py        # Auto-sizing engine
│
├── examples/                # 📚 Demos & Experiments
│   ├── demo.py             # Main demo
│   ├── extended_demo.py    # Extended styles demo
│   ├── render_all_bubbles.py
│   ├── auto_scale_demo.py
│   └── experiments/         # 🧪 Experimental Features (24 files)
│       ├── adaptive_bubbles.py
│       ├── overlapping_circles_*.py
│       ├── tail_styles_module.py
│       └── ... (20+ more)
│
├── tests/                   # ✅ Unit Tests
│   ├── test_library.py
│   ├── test_auto_scale.py
│   ├── adaptive_test_800x1200.py
│   └── ...
│
├── pictures/                # 🖼️ Images (64 PNG files)
├── reports/                 # 📄 Documentation (21 files)
├── build_bubbles/          # Build outputs
│
├── 🤖 YOLO Integration Scripts
├── test_yolo_simple.py     # ⭐ Main YOLO script (random placement)
├── yolo_manga_detector.py  # Complete YOLO system
├── fix_detection.py        # Manual click fallback
│
├── 🧪 Test Scripts
├── simple_manga_test.py    # Simple PIL test
├── quick_manga_test.py     # Cairo adaptive test
├── test_manga_composite.py # Advanced compositing
├── cairo_only_test.py      # Pure Cairo
│
└── setup.py                # 📦 PyPI Package Config
```

---

## 🎯 Key Files at a Glance

### **Production Ready** ✅

| File | Purpose | Lines |
|------|---------|-------|
| `manhwa_bubbles/__init__.py` | Main API (40+ styles) | 145 |
| `manhwa_bubbles/speech_bubbles.py` | Core PIL bubbles | ~150 |
| `manhwa_bubbles/extended_styles.py` | Extended styles | ~800 |
| `manhwa_bubbles/auto_scale.py` | Auto-sizing | ~400 |

### **YOLO Integration** 🤖

| File | Purpose | Status |
|------|---------|--------|
| `test_yolo_simple.py` | ⭐ Detect + Place + Render | **Active** |
| `yolo_manga_detector.py` | Full YOLO system | Production |
| `fix_detection.py` | Manual fallback | Production |

### **Testing & Demos** 🧪

| File | Purpose |
|------|---------|
| `examples/demo.py` | Library showcase |
| `simple_manga_test.py` | Basic testing |
| `tests/test_library.py` | Unit tests |

---

## 📊 File Statistics

- **Total Python Files**: 53
- **Core Library**: 6 files
- **Tests**: 13 files
- **Experiments**: 24 files
- **Examples**: 5 files
- **YOLO Integration**: 3 files
- **Configuration**: 2 files

---

## 🚀 Quick Start Paths

### For Users
```
1. examples/demo.py           → See all bubble types
2. test_yolo_simple.py        → Auto-detect & add bubbles
3. simple_manga_test.py       → Basic PIL usage
```

### For Developers
```
1. manhwa_bubbles/__init__.py        → Public API
2. manhwa_bubbles/speech_bubbles.py  → Core functions
3. manhwa_bubbles/auto_scale.py      → Auto-sizing algorithm
4. examples/experiments/             → Advanced features
```

### For YOLO Users
```
1. test_yolo_simple.py        → Main script (random placement)
2. yolo_manga_detector.py     → Full YOLO pipeline
3. fix_detection.py           → Manual fallback
4. reports/YOLO_README.md     → Documentation
```

---

## 🎨 Feature Categories
4
### Bubble Styles (40+)

**Basic** (10): oval, rect, cloud, jagged, wavy, black, heart, spiky, glow, scratchy

**Emotional** (10): whisper, shout, laugh, giggle, cry, nervous, rage, shock, sarcastic

**Supernatural** (8): inverted_aura, horror, magic, arcane, ghost, telepathy, hypnotic

**Technical** (6): digital, radio, robotic, ai, static, sfx

**Effects** (6): impact, chain, trailing, echo, fragmented, breath

**Mood** (5): sleepy, drunk, cold, choral, thought

**Meta** (3): text_only, bracketed, bold_plate

### Rendering Engines

- **PIL/Pillow**: Basic bubbles, fast, no dependencies
- **Cairo**: Advanced shapes, overlapping patterns, professional quality
- **Auto-scale**: Adaptive sizing, text fitting, free space detection

### Detection Methods

- **YOLO v8**: AI person detection, works with realistic manga
- **Manual Click**: 100% accurate, works with ANY art style
- **Anime Face Detector**: Specialized for anime/manga art (optional)

---

## 🔧 Dependencies

### Core Library
```python
Pillow >= 8.0.0  # Required
```

### Advanced Features
```python
pycairo >= 1.20.0  # Cairo bubbles, auto-scaling
```

### YOLO Integration
```python
ultralytics >= 8.0.0   # YOLO v8
opencv-python >= 4.8.0  # Image processing
numpy >= 1.24.0         # Arrays
```

---

## 📝 Documentation Files

Location: `reports/`

### Setup & Installation
- `HOW_TO_RUN.md` - Installation and basic usage
- `START_HERE.md` - Quick start guide
- `CAIRO_SETUP.md` - Cairo installation

### YOLO Integration
- `YOLO_README.md` - YOLO overview
- `YOLO_USAGE.md` - Detailed usage (337 lines)
- `YOLO_QUICKSTART.txt` - Quick reference
- `WHY_NO_DETECTION.md` - Troubleshooting
- `MANGA_TESTING_GUIDE.md` - Complete workflow

### Project Status
- `AUTO_SCALE_README.md` - Auto-scaling documentation
- `TEST_RESULTS.md` - Test results
- `AUTOMATION_SUCCESS.md` - CI/CD status
- `IMPROVEMENTS.md` - Enhancement notes

### Development
- `CONTRIBUTING.md` - Contribution guidelines
- `GITHUB_ACTIONS_GUIDE.md` - CI/CD guide
- `PYPI_GUIDE.md` - PyPI publishing
- `TESTING_SETUP.md` - Test setup

### Configuration
- `requirements-yolo.txt` - YOLO dependencies
- `github_setup.txt` - GitHub config

---

## 🎯 Current Project State

### ✅ Complete
- Core library (speech bubbles, narrators)
- 40+ extended bubble styles
- Auto-scaling engine
- YOLO person detection
- Manual click fallback
- PyPI package (v1.1.0)
- Comprehensive tests
- Full documentation

### 🚀 Active Features
- **Random bubble placement** (7 zones, face avoidance)
- **Multi-person detection** (color-coded visualization)
- **Smart tail direction** (vector-based pointing)
- **Reproducible randomness** (seeded placement)

### 🧪 Experimental
- 24 files in `examples/experiments/`
- Advanced Cairo patterns
- Tail style variations (10+ styles)
- Pixel-perfect intersections
- Ultra-smooth rendering

---

## 💡 Usage Examples

### Basic (PIL)
```python
from manhwa_bubbles import speech_bubble
speech_bubble(draw, (50, 50, 200, 100), "Hello!", "oval")
```

### Auto-scaled (Cairo)
```python
from manhwa_bubbles import auto_scale_bubble_adaptive
surface, meta = auto_scale_bubble_adaptive("Text", canvas_size=(600, 400))
```

### YOLO Auto-detection
```bash
python test_yolo_simple.py manga.png "Text 1" "Text 2" "Text 3"
```

### Manual Selection
```bash
python fix_detection.py manga.png "Text 1" "Text 2"
```

---

## 📈 Project Metrics

- **Python Files**: 53
- **Total Lines of Code**: ~15,000+
- **Bubble Styles**: 40+
- **Documentation Pages**: 21
- **Test Files**: 13
- **Example Scripts**: 29
- **PyPI Version**: 1.1.0
- **Python Support**: 3.6+

---

## 🔗 Related Documentation

For detailed information on each file, see:
- **`PYTHON_FILES_REFERENCE.md`** - Complete file-by-file documentation
- **`README.md`** - Project overview
- **`reports/YOLO_USAGE.md`** - YOLO detailed guide
- **`reports/MANGA_TESTING_GUIDE.md`** - Testing workflow

---

**Last Updated**: 2026-01-25  
**Project Status**: Production Ready  
**Main Features**: Speech bubbles, YOLO detection, auto-scaling, 40+ styles
