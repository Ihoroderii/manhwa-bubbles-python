#!/bin/bash
# Quick run script - installs dependencies and runs test

echo "==================================="
echo "🚀 MANGA BUBBLE TEST - QUICK RUN"
echo "==================================="
echo ""

# Check if we're in the right directory
if [ ! -f "simple_manga_test.py" ]; then
    echo "❌ Error: Run this from /Users/ihoroderii/wrk/bubble"
    exit 1
fi

echo "Step 1: Installing Pillow..."
pip3 install pillow --user --quiet || {
    echo "⚠️  Using system Python installation..."
    pip3 install pillow --quiet
}
echo "✅ Pillow installed"
echo ""

echo "Step 2: Running test script..."
python3 simple_manga_test.py
echo ""

echo "==================================="
echo "✅ DONE!"
echo "==================================="
echo ""
echo "Check these files:"
echo "  - test_manga_with_bubble.png"
echo "  - test_manga_dialogue.png"
echo ""
echo "Open them with:"
echo "  open test_manga_with_bubble.png"

