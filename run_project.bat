@echo off
echo Running Automated Resume Screening...
"C:\Users\Dagne\AppData\Local\Programs\Python\Python314\python.exe" main.py
if %errorlevel% neq 0 (
    echo.
    echo Error: Python command failed.
    echo Please ensure Python is installed and added to your PATH.
    echo If you just installed it, try restarting this terminal.
    pause
)
pause
