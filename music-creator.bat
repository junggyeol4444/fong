@echo off
REM Auto Music Creator - Batch launcher script for Windows
REM This script provides an easy way to run the Auto Music Creator

setlocal

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher to use Auto Music Creator
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    
    echo Downloading NLTK data...
    python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True)"
    
    echo Setup complete!
)

REM Always activate virtual environment
call venv\Scripts\activate.bat

REM Run the Auto Music Creator with all arguments
python music_creator.py %*

REM Exit with the same code as the Python script
exit /b %errorlevel%
