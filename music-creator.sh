#!/bin/bash
# Auto Music Creator - Shell launcher script for Unix/Linux/Mac
# This script provides an easy way to run the Auto Music Creator

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher to use Auto Music Creator"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    
    echo "Downloading NLTK data..."
    python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True)"
    
    echo "Setup complete!"
fi

# Activate virtual environment
source venv/bin/activate

# Run the Auto Music Creator with all arguments
python3 music_creator.py "$@"

# Exit with the same code as the Python script
exit $?
