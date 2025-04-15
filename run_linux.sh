#!/bin/bash

echo "Starting Cursor Email Handler..."
echo "============================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed! Please install Python 3.7 or higher."
    exit 1
fi

# Make sure pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip is not installed! Installing pip..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Check if virtual environment module is installed
if ! python3 -m venv --help &> /dev/null; then
    echo "Python venv module is not installed! Installing venv..."
    sudo apt-get install -y python3-venv
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the program
echo
echo "Running Email Registration Handler..."
echo "============================"
python3 email_registration_handler.py

# Deactivate virtual environment
deactivate

echo
echo "Program finished. Press Enter to exit."
read 