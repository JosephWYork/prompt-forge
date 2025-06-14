"""Database models for PromptForge application.

This module defines the SQLAlchemy models used throughout the application.
All models follow the project's architectural guidelines for modularity
and maintainability.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class Project(Base):
    """Model representing a project created in PromptForge.

    This model stores all information related to a project including its
    refined prompt, suggested technologies, development steps, and Cursor
    rules content.

    Attributes:
        id: Unique identifier for the project
        name: Unique name of the project (max 255 characters)
        description: Detailed description of the project
        refined_prompt: The final AI-refined prompt for Cursor Pro
        frameworks_languages: Suggested frameworks and languages (stored as text)
        checklist_steps: Granular development steps (stored as text)
        cursor_rules_content: Content for the project's .cursor/rules file
        created_at: Timestamp when the project was created
        updated_at: Timestamp when the project was last updated
    """

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    refined_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    frameworks_languages: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    checklist_steps: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cursor_rules_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        """String representation of the Project model."""
        return f"<Project(id={self.id}, name='{self.name}')>" 