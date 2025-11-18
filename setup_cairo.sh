#!/bin/bash
# Setup script for Cairo dependencies

echo "=========================================="
echo "Setting up Cairo dependencies for manhwa-bubbles"
echo "=========================================="
echo ""

# Check if running as root or with sudo
if [ "$EUID" -eq 0 ]; then
    echo "Installing system dependencies..."
    apt-get update -qq
    apt-get install -y libcairo2-dev pkg-config python3-dev
    echo "✅ System dependencies installed"
else
    echo "⚠️  This script needs sudo privileges to install system dependencies"
    echo ""
    echo "Please run manually:"
    echo "  sudo apt-get install libcairo2-dev pkg-config python3-dev"
    echo ""
    echo "Then activate your venv and run:"
    echo "  source venv/bin/activate"
    echo "  pip install pycairo"
    echo ""
fi

