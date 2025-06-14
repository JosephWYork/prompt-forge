#!/usr/bin/env python
"""Run script for PromptForge Flask application.

This script starts the Flask development server with appropriate settings.
"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import app

if __name__ == "__main__":
    # Development server settings
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5000"))

    print(f"Starting PromptForge on http://{host}:{port}")
    print("Press CTRL+C to quit")

    # Run the development server
    app.run(host=host, port=port, debug=debug) 