@echo off
REM E-commerce Chatbot Setup Script for Windows
REM This script sets up the complete development environment

echo 🚀 Setting up E-commerce Sales Chatbot...

REM Check if we're in the right directory
if not exist "README.md" (
    echo [ERROR] Please run this script from the project root directory
    pause
    exit /b 1
)

echo [INFO] Starting setup process...

REM Setup Backend
echo [INFO] Setting up backend...
cd backend

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Create virtual environment
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt

REM Create environment file if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating .env file from template...
    copy .env.example .env
    echo [WARNING] Please update .env file with your actual configuration values
)

REM Initialize database
echo [INFO] Initializing database...
python init_db.py

cd ..

REM Setup Frontend
echo [INFO] Setting up frontend...
cd frontend

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 16+ and try again.
    pause
    exit /b 1
)

REM Install dependencies
echo [INFO] Installing Node.js dependencies...
npm install

REM Create environment file if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating .env file from template...
    copy .env.example .env
)

cd ..

echo [SUCCESS] Setup completed successfully! 🎉
echo.
echo 📋 Next Steps:
echo 1. Update backend\.env with your configuration (database, API keys, etc.)
echo 2. Update frontend\.env if needed
echo 3. Start the backend server: cd backend ^&^& venv\Scripts\activate ^&^& python run.py
echo 4. Start the frontend server: cd frontend ^&^& npm start
echo.
echo 🌐 Application URLs:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:5000
echo.
echo 👤 Test Accounts:
echo    Admin: admin@example.com / password123
echo    User: user@example.com / password123

pause
