@echo off
REM Complete Application Startup Script for Windows

echo ============================================
echo  E-commerce Sales Chatbot Startup
echo ============================================
echo.

REM Start backend in a new window
echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d "%~dp0" && start-backend.bat"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d "%~dp0" && start-frontend.bat"

echo.
echo ============================================
echo  Application is starting up...
echo ============================================
echo.
echo Backend URL:  http://localhost:5000
echo Frontend URL: http://localhost:3000
echo.
echo Test Accounts:
echo   Admin: admin@example.com / password123
echo   User:  user@example.com / password123
echo.
echo Press any key to close this window...
pause >nul
