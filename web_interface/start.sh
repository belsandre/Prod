#!/bin/bash
# Quick start script for Claude Code Job Queue

echo "====================================="
echo "Claude Code Job Queue - Quick Start"
echo "====================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and change the default credentials!"
    echo "   Edit the file: nano .env"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "====================================="
echo "Starting Flask web server..."
echo "====================================="
echo ""
echo "Web interface will be available at:"
echo "  http://localhost:5001"
echo "  (Using port 5001 - macOS uses 5000 for AirPlay)"
echo ""
echo "Default credentials (CHANGE THESE!):"
echo "  Username: $AUTH_USERNAME"
echo "  Password: $AUTH_PASSWORD"
echo ""
echo "Processing mode: $PROCESSING_MODE"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python app.py
