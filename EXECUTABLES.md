# Executable Files Guide

## Overview

Auto Music Creator now includes executable launcher scripts for easy use across all platforms.

## Available Executable Files

### For Linux/Mac (Unix-like systems)

**Installation Script:**
- `install.sh` - Automatic installation and setup script

**Launcher Script:**
- `music-creator.sh` - Main executable launcher for the application

### For Windows

**Installation Script:**
- `install.bat` - Automatic installation and setup script

**Launcher Script:**
- `music-creator.bat` - Main executable launcher for the application

## Usage

### Initial Setup

**Linux/Mac:**
```bash
chmod +x install.sh music-creator.sh  # Make scripts executable (usually automatic)
./install.sh                          # Run installation
```

**Windows:**
```cmd
install.bat                           REM Run installation
```

### Running the Application

**Linux/Mac:**
```bash
./music-creator.sh [command] [options]
```

**Windows:**
```cmd
music-creator.bat [command] [options]
```

## Examples

### Generate Lyrics

**Linux/Mac:**
```bash
./music-creator.sh generate lyrics --genre pop --theme love --num-verses 2
```

**Windows:**
```cmd
music-creator.bat generate lyrics --genre pop --theme love --num-verses 2
```

### Generate Music

**Linux/Mac:**
```bash
./music-creator.sh generate music --genre rock --key D --bpm 140
```

**Windows:**
```cmd
music-creator.bat generate music --genre rock --key D --bpm 140
```

### Get Help

**Linux/Mac:**
```bash
./music-creator.sh --help
```

**Windows:**
```cmd
music-creator.bat --help
```

## Features

### Automatic Setup
- Creates virtual environment automatically on first run
- Installs all dependencies
- Downloads required NLTK data
- No manual Python environment management needed

### Cross-Platform
- Works on Linux, macOS, and Windows
- Unified command interface across all platforms
- Automatic Python detection

### Easy to Use
- No need to activate virtual environments manually
- No need to type `python music_creator.py` every time
- Just run the script!

## Troubleshooting

### Linux/Mac: Permission Denied

If you get "Permission denied" error:
```bash
chmod +x install.sh music-creator.sh
```

### Windows: Script Not Found

Make sure you're in the correct directory:
```cmd
cd path\to\fong
dir  # Should show install.bat and music-creator.bat
```

### Python Not Found

The scripts will check for Python installation. If Python is not found:
- **Linux/Mac:** Install Python 3.8+ using your package manager
- **Windows:** Download from https://www.python.org/downloads/

### Dependencies Installation Fails

Some dependencies (like TTS) may require specific Python versions. If installation fails:
1. Check Python version: `python --version` or `python3 --version`
2. Ensure Python 3.8 to 3.11 is installed
3. For TTS issues, see README.md for alternative installation methods

## Alternative: Direct Python Execution

You can still run the application directly with Python:
```bash
python music_creator.py [command] [options]
```

This method requires manual virtual environment activation:
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

## File Structure

```
fong/
├── install.sh          # Installation script (Linux/Mac)
├── install.bat         # Installation script (Windows)
├── music-creator.sh    # Launcher script (Linux/Mac)
├── music-creator.bat   # Launcher script (Windows)
├── music_creator.py    # Python main entry point
└── ...
```
