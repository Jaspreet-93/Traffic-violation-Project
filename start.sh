#!/usr/bin/env bash

echo "======================================================="
echo "  Starting Traffic Violation Detection System"
echo "======================================================="

# Trap to kill both processes on Ctrl+C
trap 'kill $(jobs -p)' EXIT

cd traffic-violation-system
source venv/bin/activate
python -m uvicorn app.main:app --port 8000 &
BACKEND_PID=$!

cd frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
wait
