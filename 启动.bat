@echo off
title Video to Audio Converter

echo.
echo ========================================
echo         Video to Audio Converter
echo ========================================
echo.

echo Starting...
echo.

if not exist "main.py" (
    echo ERROR: main.py not found
    echo Please make sure all files are in the same folder
    pause
    exit /b 1
)

if not exist "python-portable\python.exe" (
    echo ERROR: Local Python environment not found
    echo Please make sure python-portable folder exists
    pause
    exit /b 1
)

echo Using local Python environment
echo.

set "PYTHON_PATH=%~dp0python-portable\python.exe"
set "PIP_PATH=%~dp0python-portable\Scripts\pip.exe"

echo Checking PyQt5...
"%PYTHON_PATH%" -c "import PyQt5" >nul 2>&1
if not errorlevel 1 (
    echo PyQt5 is installed
    goto :start_program
)

echo PyQt5 not found, installing...
"%PIP_PATH%" install PyQt5 --quiet
if errorlevel 1 (
    echo Trying PySide2...
    "%PIP_PATH%" install PySide2 --quiet
)

echo Installing other dependencies...
"%PIP_PATH%" install ffmpeg-python python-ffmpeg pathlib2 --quiet

:start_program
echo Starting video to audio converter...
echo.

"%PYTHON_PATH%" main.py

if errorlevel 1 (
    echo.
    echo ERROR: Program failed to start
    echo Please check the error message above
)

echo.
pause
