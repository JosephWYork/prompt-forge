@echo off
echo =========================================
echo PromptForge Project Setup (Windows)
echo =========================================

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

:: Check for pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is not installed.
    exit /b 1
)
echo Found pip

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

:: Initialize database
echo Initializing database...
set FLASK_APP=src.app
flask db --init

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo To run the application:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate
echo 2. Run the Flask development server:
echo    python run.py
echo.
echo The application will be available at http://localhost:5000 