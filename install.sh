#!/bin/bash
# Auto Music Creator - Installation Script for Unix/Linux/Mac

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Auto Music Creator - Installation Script              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠ Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "[4/5] Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"
echo ""

# Download NLTK data
echo "[5/5] Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True)"
echo "✓ NLTK data downloaded"
echo ""

# Make launcher script executable
chmod +x music-creator.sh

echo "════════════════════════════════════════════════════════════"
echo "✅ Installation complete!"
echo ""
echo "To use Auto Music Creator:"
echo "  ./music-creator.sh generate lyrics --genre pop --theme love"
echo "  ./music-creator.sh generate music --genre rock --key D --bpm 140"
echo ""
echo "For help:"
echo "  ./music-creator.sh --help"
echo ""
echo "For detailed documentation, see README.md"
echo "════════════════════════════════════════════════════════════"
