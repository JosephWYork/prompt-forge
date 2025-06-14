"""Flask routes for PromptForge application.

This module defines all web routes and their corresponding handlers
for the PromptForge application.
"""

from typing import Union
import json

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from sqlalchemy.orm import Session
from werkzeug.wrappers import Response

from src.database import get_db
from src.models import Project
from src.gemini_config import get_refinement_chat, generate_project_data

# Create blueprint for routes
main = Blueprint("main", __name__)


@main.route("/")
def index() -> str:
    """Render the homepage.

    Returns:
        str: Rendered HTML template for the homepage
    """
    return render_template("index.html")


@main.route("/projects")
def projects() -> str:
    """Display a list of all projects.

    Returns:
        str: Rendered HTML template with projects list
    """
    # Get database session
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        # Query all projects
        projects = db.query(Project).order_by(Project.created_at.desc()).all()
        return render_template("projects.html", projects=projects)
    finally:
        # Ensure session is closed
        try:
            next(db_gen)
        except StopIteration:
            pass


@main.route("/create_project", methods=["GET", "POST"])
def create_project() -> Union[str, Response]:
    """Handle project creation with Gemini chat refinement.

    Returns:
        Union[str, Response]: Rendered template or redirect response
    """
    # Initialize chat session in Flask session if not exists
    if "chat_history" not in session:
        session["chat_history"] = []
        session["chat_active"] = False
        session["project_name"] = ""
        session["project_description"] = ""
    
    if request.method == "POST":
        action = request.form.get("action")
        
        # Start new chat session
        if action == "start_chat":
            name = request.form.get("name", "").strip()
            description = request.form.get("description", "").strip()
            
            if not name:
                return render_template(
                    "create_project.html",
                    message="Project name is required.",
                    chat_history=session.get("chat_history", [])
                )
            
            # Store project info in session
            session["project_name"] = name
            session["project_description"] = description
            session["chat_active"] = True
            session["chat_history"] = []
            
            # Initial message to Gemini
            initial_prompt = f"I want to create a project called '{name}'. {description}"
            
            try:
                # Get chat model and send initial message
                chat = get_refinement_chat()
                response = chat.send_message(initial_prompt)
                
                # Update chat history
                session["chat_history"].append({
                    "role": "user",
                    "content": initial_prompt
                })
                session["chat_history"].append({
                    "role": "assistant",
                    "content": response.text
                })
                session.modified = True
                
            except Exception as e:
                return render_template(
                    "create_project.html",
                    message=f"Error starting chat: {str(e)}",
                    chat_history=session.get("chat_history", [])
                )
        
        # Send chat message
        elif action == "send_message":
            user_message = request.form.get("message", "").strip()
            
            if user_message and session.get("chat_active"):
                try:
                    # Recreate chat with history
                    chat = get_refinement_chat()
                    
                    # Send all previous messages to maintain context
                    for msg in session["chat_history"]:
                        if msg["role"] == "user":
                            chat.send_message(msg["content"])
                    
                    # Send new message
                    response = chat.send_message(user_message)
                    
                    # Update chat history
                    session["chat_history"].append({
                        "role": "user",
                        "content": user_message
                    })
                    session["chat_history"].append({
                        "role": "assistant", 
                        "content": response.text
                    })
                    session.modified = True
                    
                except Exception as e:
                    return render_template(
                        "create_project.html",
                        message=f"Error sending message: {str(e)}",
                        chat_history=session.get("chat_history", [])
                    )
        
        # Approve prompt and generate project data
        elif action == "approve_prompt":
            if not session.get("chat_active") or not session.get("chat_history"):
                return render_template(
                    "create_project.html",
                    message="No active chat session to approve.",
                    chat_history=session.get("chat_history", [])
                )
            
            try:
                # Compile refined prompt from chat history
                refined_prompt = f"Project: {session['project_name']}\n"
                refined_prompt += f"Description: {session['project_description']}\n\n"
                refined_prompt += "Refined Requirements based on conversation:\n"
                
                # Extract key points from chat history
                for msg in session["chat_history"]:
                    if msg["role"] == "user":
                        refined_prompt += f"\nUser requirement: {msg['content']}\n"
                
                # Generate project data
                project_data = generate_project_data(refined_prompt)
                
                # Get database session
                db_gen = get_db()
                db: Session = next(db_gen)
                
                try:
                    # Check if project name already exists
                    existing = db.query(Project).filter(
                        Project.name == session["project_name"]
                    ).first()
                    
                    if existing:
                        return render_template(
                            "create_project.html",
                            message=f"Project '{session['project_name']}' already exists.",
                            chat_history=session.get("chat_history", [])
                        )
                    
                    # Create new project
                    new_project = Project(
                        name=session["project_name"],
                        description=session["project_description"],
                        refined_prompt=refined_prompt,
                        frameworks_languages=project_data["frameworks_languages"],
                        checklist_steps=project_data["checklist_steps"],
                        cursor_rules_content=project_data["cursor_rules_content"]
                    )
                    
                    db.add(new_project)
                    db.commit()
                    
                    # Clear session
                    session.pop("chat_history", None)
                    session.pop("chat_active", None)
                    session.pop("project_name", None)
                    session.pop("project_description", None)
                    
                    return redirect(url_for("main.project_detail", project_id=new_project.id))
                    
                except Exception as e:
                    db.rollback()
                    return render_template(
                        "create_project.html",
                        message=f"Error creating project: {str(e)}",
                        chat_history=session.get("chat_history", [])
                    )
                finally:
                    try:
                        next(db_gen)
                    except StopIteration:
                        pass
                        
            except Exception as e:
                return render_template(
                    "create_project.html",
                    message=f"Error generating project data: {str(e)}",
                    chat_history=session.get("chat_history", [])
                )

    # GET request - show the form
    return render_template(
        "create_project.html",
        chat_history=session.get("chat_history", []),
        chat_active=session.get("chat_active", False)
    )


@main.route("/project/<int:project_id>")
def project_detail(project_id: int) -> Union[str, tuple[str, int]]:
    """Display details of a specific project.

    Args:
        project_id: The ID of the project to display

    Returns:
        Union[str, tuple[str, int]]: Rendered template or 404 error
    """
    # Get database session
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        # Query for the specific project
        project = db.query(Project).filter(Project.id == project_id).first()

        if not project:
            return render_template("404.html"), 404

        return render_template("project_detail.html", project=project)
    finally:
        # Ensure session is closed
        try:
            next(db_gen)
        except StopIteration:
            pass 