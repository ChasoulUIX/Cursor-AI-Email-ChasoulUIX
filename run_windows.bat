@echo off
echo Starting Cursor Email Handler...
echo ============================

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.7 or higher.
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
)

:: Run the program
echo.
echo Running Email Registration Handler...
echo ============================
python email_registration_handler.py

:: Keep window open after execution
echo.
echo Program finished. Press any key to exit.
pause > nul 