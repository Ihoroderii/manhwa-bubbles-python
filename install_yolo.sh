#!/bin/bash
# Quick installation script for YOLO manga detection

echo "=========================================="
echo "🚀 YOLO Manga Detection - Installation"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python..."
python3 --version || {
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
}
echo "✅ Python found"
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
echo ""

pip3 install -r requirements-yolo.txt || {
    echo "⚠️  requirements-yolo.txt not found, installing manually..."
    pip3 install ultralytics opencv-python pillow numpy
}

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "Test the installation:"
echo "  python3 yolo_manga_detector.py"
echo ""
echo "Or process your manga:"
echo "  python3 yolo_manga_detector.py my_manga.png 'Text 1' 'Text 2'"
echo ""
echo "See YOLO_USAGE.md for detailed instructions"
echo ""

