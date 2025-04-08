#!/bin/bash

# Adaptive RAG setup script

echo "Setting up Adaptive RAG system..."

# Check for Python 3.9+
python_version=$(python --version 2>&1)
if [[ $python_version != *"Python 3."* ]]; then
    echo "Error: Python 3 is required"
    exit 1
fi

version_num=$(echo $python_version | cut -d' ' -f2 | cut -d'.' -f2)
if [[ $version_num -lt 9 ]]; then
    echo "Warning: Python 3.9 or higher is recommended"
fi

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix/Linux/MacOS
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -e .

# Create .env file
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please edit the .env file with your API keys"
fi

# Install UI dependencies
echo "Installing UI dependencies..."
pip install -r ui/requirements.txt

echo ""
echo "Setup complete! To get started:"
echo ""
echo "1. Edit the .env file with your API keys"
echo "2. Run an example: python examples/simple_question.py"
echo "3. Launch the UI: python ui/launch_ui.py"
echo ""