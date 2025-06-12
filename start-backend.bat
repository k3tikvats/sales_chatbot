@echo off
REM Start Backend Server Script for Windows

echo Starting E-commerce Chatbot Backend Server...

cd /d "%~dp0backend"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo .env file not found. Creating from template...
    copy .env.example .env
    echo Please update .env file with your configuration values.
    pause
)

REM Start the Flask server
echo Backend server starting on http://localhost:5000
python run.py
