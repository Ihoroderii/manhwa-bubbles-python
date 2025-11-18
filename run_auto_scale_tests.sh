#!/bin/bash
# Quick test runner for auto-scaling functionality

echo "=========================================="
echo "Auto-Scaling Bubble Test Runner"
echo "=========================================="
echo ""

# Check if venv is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated"
    echo "   Activating venv..."
    source venv/bin/activate
fi

# Check for pycairo
echo "Checking dependencies..."
python3 -c "import cairo; print('✅ pycairo available')" 2>/dev/null || {
    echo "❌ pycairo not available"
    echo ""
    echo "To install pycairo:"
    echo "  1. Install system dependencies:"
    echo "     sudo apt-get install libcairo2-dev pkg-config python3-dev"
    echo "  2. Install pycairo:"
    echo "     pip install pycairo"
    echo ""
    exit 1
}

# Check for overlapping_circles_squares
python3 -c "import sys; sys.path.insert(0, 'examples/experiments'); from overlapping_circles_squares import create_overlapping_circles_square; print('✅ overlapping_circles_squares available')" 2>/dev/null || {
    echo "⚠️  overlapping_circles_squares.py not found in examples/experiments/"
    echo "   Some tests may fail"
}

echo ""
echo "Running tests..."
echo ""

# Run tests
python3 tests/test_auto_scale.py

echo ""
echo "=========================================="
echo "Test run complete!"
echo "=========================================="

