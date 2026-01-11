#!/usr/bin/env python3
"""Basic structure verification without requiring dependencies."""

import os
import sys
from pathlib import Path

def verify_structure():
    """Verify project structure."""
    print("Verifying Auto Music Creator project structure...\n")
    
    required_files = [
        'README.md',
        'QUICKSTART.md',
        'requirements.txt',
        'setup.py',
        'music_creator.py',
        'test_system.py',
        'examples.json',
        '.gitignore',
    ]
    
    required_dirs = [
        'src/crawler',
        'src/analysis',
        'src/generation',
        'src/voice_synthesis',
        'src/cli',
        'data/raw',
        'data/analyzed',
        'data/generated',
        'data/templates',
    ]
    
    required_modules = [
        'src/__init__.py',
        'src/crawler/__init__.py',
        'src/crawler/youtube_crawler.py',
        'src/analysis/__init__.py',
        'src/analysis/lyrics_analyzer.py',
        'src/analysis/music_analyzer.py',
        'src/generation/__init__.py',
        'src/generation/lyrics_generator.py',
        'src/generation/music_generator.py',
        'src/voice_synthesis/__init__.py',
        'src/voice_synthesis/voice_synthesizer.py',
        'src/cli/__init__.py',
        'src/cli/main_cli.py',
    ]
    
    # Check files
    print("Checking required files:")
    for file in required_files:
        exists = os.path.exists(file)
        status = "✓" if exists else "✗"
        print(f"  {status} {file}")
    
    # Check directories
    print("\nChecking required directories:")
    for dir_path in required_dirs:
        exists = os.path.isdir(dir_path)
        status = "✓" if exists else "✗"
        print(f"  {status} {dir_path}")
    
    # Check modules
    print("\nChecking Python modules:")
    for module in required_modules:
        exists = os.path.exists(module)
        status = "✓" if exists else "✗"
        print(f"  {status} {module}")
    
    # Count lines of code
    total_lines = 0
    for module in required_modules:
        if os.path.exists(module):
            with open(module, 'r') as f:
                total_lines += len(f.readlines())
    
    print(f"\nTotal lines of code: {total_lines}")
    print("\n" + "="*50)
    print("Project structure verification complete!")
    print("To install dependencies and run tests:")
    print("  pip install -r requirements.txt")
    print("  python test_system.py")

if __name__ == '__main__':
    verify_structure()
