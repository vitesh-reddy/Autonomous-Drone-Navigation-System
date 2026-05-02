#!/bin/bash

# Bash script to run the IAS project on Unix-like systems

echo "======================================"
echo "IAS Project - Drone Navigation RL"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Check/install dependencies
echo "Checking dependencies..."
python3 -m pip list | grep -q numpy
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "Starting training and visualization..."
echo ""

python3 main.py

if [ $? -ne 0 ]; then
    echo "Error occurred during execution"
    exit 1
fi

echo ""
echo "Project completed successfully!"
