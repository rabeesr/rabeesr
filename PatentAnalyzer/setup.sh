#!/bin/bash

# Stop script on error
set -e

echo "Setting up the Patent application..."

#create contents directory if it does not already exist
if [ ! -d "./contents" ]; then
  mkdir ./contents
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 not found. Please install Python3."
    exit 1
fi

# Create a virtual environment if it does not exist
if [ ! -d "venv" ]; then
    echo "Creating a virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip3 install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Run FastAPI in the background using & and run it on port 8000. Start streamlit app
echo "Running FastAPI server..."
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 &
streamlit run app.py 


