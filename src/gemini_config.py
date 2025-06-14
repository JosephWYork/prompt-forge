"""Gemini API configuration and client initialization.

This module handles the setup and configuration of the Google Generative AI (Gemini) API.
It loads the API key from environment variables and provides configured clients.
"""

import os
from typing import Optional
import logging

import google.generativeai as genai

logger = logging.getLogger(__name__)


def configure_gemini() -> None:
    """Configure the Gemini API with the API key from environment variables.
    
    The API key should be set in a .env file at the project root:
    GEMINI_API_KEY=your-api-key-here
    
    Raises:
        ValueError: If GEMINI_API_KEY is not set in environment variables
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment variables. "
            "Please create a .env file in the project root with: "
            "GEMINI_API_KEY=your-api-key-here"
        )
    
    if api_key == "test-key-placeholder":
        logger.warning("Using test API key - chat functionality will not work without a valid key")
    
    genai.configure(api_key=api_key)


def get_chat_model(model_name: str = "gemini-1.5-flash") -> genai.GenerativeModel:
    """Get a configured Gemini generative model for chat.
    
    Args:
        model_name: The name of the model to use (default: gemini-1.5-flash)
        
    Returns:
        genai.GenerativeModel: Configured generative model
    """
    return genai.GenerativeModel(model_name)


def get_refinement_chat() -> genai.ChatSession:
    """Get a chat session configured for prompt refinement.
    
    Returns:
        genai.ChatSession: Chat session with refinement expert persona
    """
    model = get_chat_model()
    
    # System instruction for the hyper-critical prompt refinement expert
    system_instruction = """You are a Prompt Refinement Expert for software project planning. Your role is to be extremely thorough and critical in helping users refine their project requirements.

Your behavior:
1. Ask clarifying questions about EVERY aspect of the project
2. Point out ambiguities, missing information, and potential issues
3. Suggest better ways to phrase requirements
4. Push for specific technical details
5. Question assumptions and vague statements
6. Continue refining until the prompt is crystal clear and comprehensive

Be professional but persistent. Do not accept vague or incomplete requirements. Your goal is to produce a prompt that any developer could use to build exactly what the user wants."""
    
    chat = model.start_chat(history=[
        {
            "role": "model",
            "parts": [system_instruction]
        }
    ])
    
    return chat


def generate_project_data(refined_prompt: str) -> dict:
    """Generate project data from the refined prompt.
    
    Args:
        refined_prompt: The final refined prompt from the chat session
        
    Returns:
        dict: Generated project data containing frameworks, checklist, and cursor rules
    """
    model = get_chat_model()
    
    # Generate frameworks and languages
    frameworks_prompt = f"""Based on this project prompt, suggest the most appropriate coding frameworks and languages:

{refined_prompt}

Format your response as a simple list, like:
Frontend: React, TypeScript, Tailwind CSS
Backend: Python, FastAPI, SQLAlchemy
Database: PostgreSQL
etc."""
    
    frameworks_response = model.generate_content(frameworks_prompt)
    frameworks_languages = frameworks_response.text.strip()
    
    # Generate checklist steps
    checklist_prompt = f"""Create a detailed, granular development checklist for this project:

{refined_prompt}

Format as numbered steps, each step should be specific and actionable. Include at least 10-15 steps covering:
- Project setup
- Core functionality implementation
- Testing
- Deployment preparation"""
    
    checklist_response = model.generate_content(checklist_prompt)
    checklist_steps = checklist_response.text.strip()
    
    # Generate cursor rules content
    cursor_rules_prompt = f"""Generate content for a .cursor/rules file for this project. Use this exact template and fill in the sections based on the project requirements:

Project: {refined_prompt}
Tech Stack: {frameworks_languages}

TEMPLATE TO FILL:
// --- PROJECT CONTEXT AND OBJECTIVES ---
// PROJECT NAME: [Extract from prompt]
// PROJECT TYPE: [Identify type]
// PRIMARY GOAL: [Main objective]
// KEY OUTCOME: [Expected result]
// TARGET AUDIENCE/USERS: [Who will use this]
// DEPLOYMENT ENVIRONMENT: [Where it will run]
// NON-FUNCTIONAL REQUIREMENTS: [Performance, security, etc.]

// --- ARCHITECTURAL AND DESIGN GUIDELINES ---
// ARCHITECTURAL PATTERN: [Suggested pattern]
// DESIGN PRINCIPLES: [Key principles]
// DATA FLOW: [How data moves]
// ERROR HANDLING: [Error strategy]
// SECURITY: [Security considerations]
// SCALABILITY: [Scalability approach]

// --- TECHNOLOGY STACK AND CODING STANDARDS ---
// PRIMARY LANGUAGE: [Main language]
// FRAMEWORK(S): [List frameworks]
// DATABASE(S): [Database choice]
// PACKAGE MANAGER: [Package manager]
// CODING STYLE: [Style guide]
// NAMING CONVENTIONS: [Naming rules]
// TYPE HINTING: [Type hint requirements]
// COMMENTING/DOCSTRINGS: [Documentation standards]

// --- DEVELOPMENT LIFECYCLE AND QA ---
// TEST-DRIVEN DEVELOPMENT (TDD): [TDD approach]
// UNIT TESTING: [Testing framework]
// AUTOMATION: [What to automate]
// VERSION CONTROL: [Git practices]
// CODE REVIEW: [Review process]

// --- AI INTERACTION GUIDELINES ---
// CONTEXTUAL AWARENESS: [AI context rules]
// ITERATIVE REFINEMENT: [How AI should help]
// CLARIFICATION: [When to ask questions]
// PROMPT CRITIQUE: [AI feedback approach]
// ERROR HANDLING: [AI error assistance]"""
    
    cursor_rules_response = model.generate_content(cursor_rules_prompt)
    cursor_rules_content = cursor_rules_response.text.strip()
    
    return {
        "frameworks_languages": frameworks_languages,
        "checklist_steps": checklist_steps,
        "cursor_rules_content": cursor_rules_content
    } 