@echo off
echo ========================================
echo   Question Filter System - Startup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Change to backend directory
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
echo Checking dependencies...
pip list | findstr "fastapi" >nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo ✅ Dependencies installed
) else (
    echo ✅ Dependencies already installed
)

REM Create uploads directory if it doesn't exist
if not exist "..\uploads" (
    mkdir "..\uploads"
    echo ✅ Created uploads directory
)

REM Start the backend server
echo.
echo ========================================
echo   Starting Backend Server...
echo ========================================
echo.
echo Backend will run at: http://localhost:8000
echo.
echo To access the frontend:
echo 1. Open frontend/index.html in your browser
echo 2. Or run: python -m http.server 8080 from frontend directory
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

REM Deactivate virtual environment when done
deactivate
cd ..

echo.
echo ========================================
echo   Server stopped
echo ========================================
pause