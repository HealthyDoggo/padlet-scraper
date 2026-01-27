@echo off
REM Easy installation script for Padlet Scraper (Windows)

echo ================================================
echo   Padlet Scraper Installation
echo ================================================
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Found Python
python --version

REM Check for pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed
    pause
    exit /b 1
)

echo Found pip
echo.

REM Install the package
echo Installing Padlet Scraper...
pip install -e .

echo.
echo ================================================
echo   Installation Complete!
echo ================================================
echo.
echo Usage:
echo   padlet-scraper "https://padlet.com/user/board" -o output.json
echo.
echo For more help:
echo   padlet-scraper --help
echo.
pause
