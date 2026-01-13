@echo off
REM Auto Music Creator - Installation Script for Windows

echo ================================================================
echo      Auto Music Creator - Installation Script
echo ================================================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo + Python %PYTHON_VERSION% found
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist "venv\" (
    echo ! Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo + Virtual environment created
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo + Virtual environment activated
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo + Dependencies installed
echo.

REM Download NLTK data
echo [5/5] Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True)"
echo + NLTK data downloaded
echo.

echo ================================================================
echo + Installation complete!
echo.
echo To use Auto Music Creator:
echo   music-creator.bat generate lyrics --genre pop --theme love
echo   music-creator.bat generate music --genre rock --key D --bpm 140
echo.
echo For help:
echo   music-creator.bat --help
echo.
echo For detailed documentation, see README.md
echo ================================================================
pause
