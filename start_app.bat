@echo off
echo Starting Resume AI System...

:: Start Backend (in a new window)
start "Resume AI Backend" cmd /k "cd . && "C:\Users\Dagne\AppData\Local\Programs\Python\Python314\python.exe" server.py"

:: Start Frontend (in a new window)
start "Resume AI Frontend" cmd /k "cd ui && npm run dev"

echo.
echo Servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Please wait a moment for the windows to open!
pause
