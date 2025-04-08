@echo off
REM Adaptive RAG setup script for Windows

echo Setting up Adaptive RAG system...

REM Check for Python 3.9+
python --version > NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -e .

REM Create .env file
if not exist .env (
    echo Creating .env file from example...
    copy .env.example .env
    echo Please edit the .env file with your API keys
)

REM Install UI dependencies
echo Installing UI dependencies...
pip install -r ui\requirements.txt

echo.
echo Setup complete! To get started:
echo.
echo 1. Edit the .env file with your API keys
echo 2. Run an example: python examples\simple_question.py
echo 3. Launch the UI: python ui\launch_ui.py
echo.

pause