#!/bin/bash
# Easy installation script for Padlet Scraper

set -e  # Exit on error

echo "================================================"
echo "  Padlet Scraper Installation"
echo "================================================"
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install/check for Chromium
echo ""
echo "Checking for Chromium browser..."
if [ -d "/Applications/Chromium.app" ]; then
    echo "✓ Chromium is already installed"
elif command -v brew &> /dev/null; then
    echo "Installing Chromium via Homebrew..."
    brew install --cask chromium
    # Remove quarantine attribute
    xattr -dr com.apple.quarantine /Applications/Chromium.app 2>/dev/null || true
    echo "✓ Chromium installed"
else
    echo "⚠️  Chromium not found. Please install from:"
    echo "   https://www.chromium.org/getting-involved/download-chromium/"
    echo "   Or install Homebrew and run this script again"
fi

# Install the package
echo ""
echo "Installing Padlet Scraper..."
pip install -e .

echo ""
echo "================================================"
echo "  ✓ Installation Complete!"
echo "================================================"
echo ""
echo "To use the scraper:"
echo ""
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the scraper:"
echo "     padlet-scraper 'https://padlet.com/user/board' -o output.json"
echo ""
echo "Or use the included wrapper script:"
echo "  ./run-scraper.sh 'https://padlet.com/user/board' -o output.json"
echo ""
echo "For more help:"
echo "  padlet-scraper --help"
echo ""
