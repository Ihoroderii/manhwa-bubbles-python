# Cairo Setup Instructions

The `overlapping_circles_squares.py` script requires Cairo (pycairo) to run.

## Quick Setup

Run these commands in your terminal:

```bash
# Install system dependencies (requires sudo)
sudo apt-get install libcairo2-dev pkg-config python3-dev

# Activate your virtual environment
source venv/bin/activate

# Install pycairo
pip install pycairo
```

## Verify Installation

```bash
python3 -c "import cairo; print('✅ Cairo is ready!')"
```

## Run the Script

Once Cairo is installed:

```bash
source venv/bin/activate
python3 examples/experiments/overlapping_circles_squares.py
```

This will generate:
- `overlapping_circles_squares.png` - Main demo
- `bubble_laugh.png` - Laugh style bubble

## Alternative: Use Pre-built Wheel (if available)

If you have issues building from source, you can try:

```bash
pip install --only-binary :all: pycairo
```

However, this may not work on all systems and building from source is recommended.

