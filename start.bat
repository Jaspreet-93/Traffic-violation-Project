@echo off
echo =======================================================
echo   Launching Smart Traffic Violation Detection System
echo =======================================================
echo.

:: 1. Start Backend API Server
echo [*] Starting FastAPI Backend on port 8000...
start "Traffic Backend Server" cmd /k "cd traffic-violation-system && call venv\Scripts\activate && python -m uvicorn app.main:app --port 8000"

:: 2. Wait 3 seconds for backend initialization
timeout /t 3 /nobreak >nul

:: 3. Start Frontend Dev Server
echo [*] Starting Vite Frontend on port 3000...
start "Traffic Frontend Client" cmd /k "cd traffic-violation-system\frontend && npm run dev"

:: 4. Open Application in Default Web Browser
timeout /t 4 /nobreak >nul
start http://localhost:3000

echo.
echo Both servers are launching!
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo =======================================================
