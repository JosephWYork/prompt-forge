"""Flask CLI commands for PromptForge.

This module defines custom Flask CLI commands for database management
and other administrative tasks.
"""

import click
from flask import Flask
from flask.cli import with_appcontext

from src.database import init_db


def register_commands(app: Flask) -> None:
    """Register custom CLI commands with the Flask application.

    Args:
        app: The Flask application instance
    """
    app.cli.add_command(init_db_command)


@click.command("db")
@click.option("--init", is_flag=True, help="Initialize the database")
@with_appcontext
def init_db_command(init: bool) -> None:
    """Database management commands.

    Args:
        init: Flag to initialize the database
    """
    if init:
        click.echo("Initializing the database...")
        init_db()
        click.echo("Database initialized successfully!")
    else:
        click.echo("Please specify an action: --init") 