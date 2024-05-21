@echo off
echo Creating a Python virtual environment...

start /wait python -m venv djenv
if errorlevel 1 (
    echo Error creating the virtual environment.
    exit /b 1
)

echo Activating the virtual environment...

call djenv\Scripts\activate.bat
if errorlevel 1 (
    echo Error activating the virtual environment.
    exit /b 1
)

echo Installing Python packages from requirements.txt...

start /wait pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing packages.
    exit /b 1
)

echo All operations completed successfully.

pause