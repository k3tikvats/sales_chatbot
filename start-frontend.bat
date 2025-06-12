@echo off
REM Start Frontend Server Script for Windows

echo Starting E-commerce Chatbot Frontend Server...

cd /d "%~dp0frontend"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Dependencies not installed. Installing now...
    npm install
)

REM Check if .env file exists
if not exist ".env" (
    echo .env file not found. Creating from template...
    copy .env.example .env
)

REM Start the React development server
echo Frontend server starting on http://localhost:3000
npm start
