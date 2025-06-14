#!/bin/bash

# PromptForge Setup Script
# This script sets up the development environment for the PromptForge Flask application

echo "========================================="
echo "PromptForge Project Setup"
echo "========================================="

# Check for Python 3.9+
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
required_version="3.9"

if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed."
    exit 1
fi

# Compare versions
if ! python -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "Error: Python 3.9 or higher is required. Found: $python_version"
    exit 1
fi

echo "✓ Python $python_version found"

# Check for pip
echo "Checking for pip..."
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed."
    exit 1
fi
echo "✓ pip found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix-like systems
    source venv/bin/activate
fi
echo "✓ Virtual environment activated"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Initialize database
echo "Initializing database..."
export FLASK_APP=src.app
flask db init
echo "✓ Database initialized"

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   venv\\Scripts\\activate"
else
    echo "   source venv/bin/activate"
fi
echo "2. Run the Flask development server:"
echo "   python run.py"
echo ""
echo "The application will be available at http://localhost:5000" 