@echo off
REM Batch script to run the IAS project on Windows

echo ======================================
echo IAS Project - Drone Navigation RL
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
pip show numpy pygame matplotlib >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting training and visualization...
echo.
python main.py

if errorlevel 1 (
    echo Error occurred during execution
    pause
    exit /b 1
)

echo.
echo Project completed successfully!
pause
