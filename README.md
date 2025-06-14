# PromptForge

A Flask web application designed to streamline project creation by refining requirements with AI, generating standardized project files, and outlining granular development steps.

## 🚀 Quick Start

### Prerequisites
- Python 3.13+ (Note: If using Python 3.13, SQLAlchemy 2.0.30+ is required)
- pip

### Installation

#### Windows
```powershell
# Clone the repository
git clone <your-repo-url>
cd prompt-forge

# Run the setup script
.\setup.bat
```

#### Unix/Linux/macOS
```bash
# Clone the repository
git clone <your-repo-url>
cd prompt-forge

# Run the setup script
bash setup.sh
```

### Running the Application

1. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/Linux/macOS: `source venv/bin/activate`

2. Set up Gemini API (REQUIRED for chat functionality):
   ```bash
   # Create a .env file in the project root
   # Add your Gemini API key:
   echo "GEMINI_API_KEY=your-api-key-here" > .env
   ```
   
   Get your API key from: https://makersuite.google.com/app/apikey

3. Initialize the database (first time only):
   ```bash
   # Windows PowerShell
   $env:FLASK_APP="src.app"; flask db --init
   
   # Unix/Linux/macOS
   export FLASK_APP=src.app
   flask db --init
   ```

4. Run the application:
   ```bash
   python run.py
   ```

5. Open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
prompt-forge/
├── .cursor/            # Cursor Pro configuration
│   └── rules          # Project-specific AI guidelines
├── src/               # Application source code
│   ├── static/        # CSS, JavaScript, images
│   ├── templates/     # Jinja2 HTML templates
│   ├── app.py         # Flask application factory
│   ├── models.py      # SQLAlchemy database models
│   ├── routes.py      # Application routes
│   ├── database.py    # Database configuration
│   └── commands.py    # Flask CLI commands
├── instance/          # Instance-specific files (gitignored)
│   └── app.db         # SQLite database (created on init)
├── venv/              # Virtual environment (gitignored)
├── requirements.txt   # Python dependencies
├── setup.sh          # Unix setup script
├── setup.bat         # Windows setup script
├── run.py            # Application entry point
└── README.md         # This file
```

## 🔧 Features

### Current Features
- ✅ Project listing and management
- ✅ Project detail view with all metadata
- ✅ SQLite database with SQLAlchemy ORM
- ✅ Clean, modern UI with responsive design
- ✅ Flask best practices and modular architecture

### Planned Features
- 🚧 Interactive AI-powered project requirement refinement
- 🚧 Automatic project structure generation
- 🚧 Development checklist generation
- 🚧 Cursor Pro rules export

## 🛠️ Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black src/
```

### Linting
```bash
flake8 src/
```

### Type Checking
```bash
mypy src/
```

## 📝 Configuration

Environment variables can be set in a `.env` file:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///instance/app.db
```

## 🤝 Contributing

1. Follow PEP 8 style guidelines
2. Use type hints for all new code
3. Write comprehensive docstrings
4. Ensure all tests pass before submitting
5. Use atomic commits with clear messages

## 📄 License

[Your License Here]

## 🐛 Troubleshooting

### Python 3.13 Compatibility
If you encounter SQLAlchemy errors with Python 3.13, ensure you're using SQLAlchemy 2.0.30 or later. The requirements.txt has been updated to use SQLAlchemy 2.0.41 which fully supports Python 3.13.

### Database Errors
If you see "unable to open database file" errors:
1. Ensure the database is initialized: `flask db --init`
2. Check that the `instance/` directory exists
3. Verify file permissions on the `instance/` directory 