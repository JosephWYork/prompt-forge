"""Main Flask application module for PromptForge.

This module creates and configures the Flask application instance,
registers blueprints, and sets up necessary extensions.
"""

import os
from typing import Optional

from dotenv import load_dotenv
from flask import Flask

from src.commands import register_commands
from src.routes import main
from src.gemini_config import configure_gemini


def create_app(config: Optional[dict] = None) -> Flask:
    """Create and configure the Flask application.

    Args:
        config: Optional configuration dictionary to override defaults

    Returns:
        Flask: Configured Flask application instance
    """
    # Load environment variables
    load_dotenv()

    # Create Flask app
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Configure app
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///instance/app.db"
    )
    
    # Configure session for chat state management
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True
    
    # Configure Gemini API
    try:
        configure_gemini()
        app.logger.info("Gemini API configured successfully")
    except ValueError as e:
        app.logger.warning(f"Gemini API configuration failed: {e}")
        app.logger.warning("Chat functionality will not be available")

    # Apply additional config if provided
    if config:
        app.config.update(config)

    # Register blueprints
    app.register_blueprint(main)

    # Register CLI commands
    register_commands(app)

    return app


# Create app instance
app = create_app() 