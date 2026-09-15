#!/usr/bin/env bash
set -e

echo "======================================================="
echo "  Smart Traffic Violation Detection System - Setup (Linux/macOS)"
echo "======================================================="

# 1. Check Python
command -v python3 >/dev/null 2>&1 || { echo "[ERROR] Python 3 is not installed."; exit 1; }
echo "[OK] Python detected."

# 2. Check Node
command -v node >/dev/null 2>&1 || { echo "[ERROR] Node.js is not installed."; exit 1; }
echo "[OK] Node.js detected."

# 3. Virtual Environment
if [ ! -d "traffic-violation-system/venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv traffic-violation-system/venv
fi
echo "[OK] Virtual environment ready."

# 4. Install Python Dependencies
echo "[*] Installing Python dependencies..."
source traffic-violation-system/venv/bin/activate
pip install --upgrade pip
pip install -r traffic-violation-system/requirements.txt
echo "[OK] Python dependencies installed."

# 5. Environment file
if [ ! -f "traffic-violation-system/.env" ]; then
    echo "[*] Generating traffic-violation-system/.env from .env.example..."
    cp "traffic-violation-system/.env.example" "traffic-violation-system/.env"
fi
echo "[OK] Configuration .env verified."

# 6. Frontend
echo "[*] Installing frontend dependencies..."
cd traffic-violation-system/frontend
npm install
cd ../..
echo "[OK] Frontend packages installed."

# 7. Runtime directories
python3 -c "
import os
dirs = ['uploads/original', 'uploads/annotated', 'uploads/thumbnails', 'uploads/evidence', 'storage/vehicle', 'storage/plate', 'storage/lane_evidence', 'storage/no_helmet', 'storage/no_seat_belt', 'storage/distracted_driving', 'storage/smoking_while_driving', 'storage/wrong_lane', 'reports', 'outputs', 'logs']
for d in dirs:
    os.makedirs(os.path.join('traffic-violation-system', d), exist_ok=True)
"
echo "[OK] Runtime directories created."

echo "======================================================="
echo "  Setup complete! Run ./start.sh to run the system."
echo "======================================================="
