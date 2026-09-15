@echo off
setlocal enabledelayedexpansion

echo =======================================================
echo   Smart Traffic Violation Detection System - Setup
echo =======================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python 3.10+.
    pause
    exit /b 1
)
echo [OK] Python detected.

:: 2. Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH. Please install Node.js 18+.
    pause
    exit /b 1
)
echo [OK] Node.js detected.

:: 3. Setup Virtual Environment
if not exist "traffic-violation-system\venv" (
    echo [*] Creating virtual environment in traffic-violation-system\venv...
    python -m venv traffic-violation-system\venv
)
echo [OK] Virtual environment ready.

:: 4. Activate Venv and Install Python Requirements
echo [*] Installing Python dependencies...
call traffic-violation-system\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r traffic-violation-system\requirements.txt
echo [OK] Python dependencies installed.

:: 5. Create .env from .env.example if missing
if not exist "traffic-violation-system\.env" (
    echo [*] Generating traffic-violation-system\.env from .env.example...
    copy "traffic-violation-system\.env.example" "traffic-violation-system\.env"
)
echo [OK] Configuration .env verified.

:: 6. Setup Frontend Dependencies
echo [*] Installing frontend npm packages...
cd traffic-violation-system\frontend
call npm install
cd ..\..
echo [OK] Frontend packages installed.

:: 7. Create required runtime directories
echo [*] Verifying runtime directory structures...
python -c "
import os
dirs = ['uploads/original', 'uploads/annotated', 'uploads/thumbnails', 'uploads/evidence', 'storage/vehicle', 'storage/plate', 'storage/lane_evidence', 'storage/no_helmet', 'storage/no_seat_belt', 'storage/distracted_driving', 'storage/smoking_while_driving', 'storage/wrong_lane', 'reports', 'outputs', 'logs']
for d in dirs:
    os.makedirs(os.path.join('traffic-violation-system', d), exist_ok=True)
"
echo [OK] Runtime directories created.

echo.
echo =======================================================
echo   Setup completed successfully!
echo   Run start.bat to launch the application.
echo =======================================================
echo.
pause
