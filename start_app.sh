#!/bin/bash

# Step 1: Check if the 'school' virtual environment exists, if not, create it
if [ ! -d "school" ]; then
    echo "Virtual environment 'school' not found. Creating it..."
    python3 -m venv school
    echo "Virtual environment 'school' created."
fi

# Step 2: Activate the 'school' virtual environment
source school/bin/activate
echo "Virtual environment 'school' activated."

# Step 3: Install requirements from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
    echo "Requirements installed."
else
    echo "Error: requirements.txt file not found!"
    exit 1
fi

# Step 4: Load environment variables from .env file
if [ -f ".env" ]; then
    echo "Setting environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
    echo "Environment variables set."
else
    echo "Error: .env file not found!"
    exit 1
fi

# Step 5: Start the Python app
echo "Starting the Python application..."
python school_notifier.py