@echo off
REM Wrapper script to run padlet-scraper without manually activating venv (Windows)

REM Check if venv exists
if not exist "%~dp0venv" (
    echo Error: Virtual environment not found.
    echo Please run install.bat first
    exit /b 1
)

REM Activate venv and run padlet-scraper with all arguments
call "%~dp0venv\Scripts\activate.bat"
padlet-scraper %*
