#!/usr/bin/env bash
# Launch script for testing - runs services in background and saves PIDs

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Kill existing processes from .pids if present
if [ -f .pids ]; then
    while IFS= read -r pid; do
        if [ -n "$pid" ] && ps -p "$pid" > /dev/null 2>&1; then
            kill "$pid" 2>/dev/null || true
        fi
    done < .pids
    rm .pids
fi

# Activate backend venv and start uvicorn in background
cd backend
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null
# Force SQLite for local testing (ignore system DATABASE_URL)
export DATABASE_URL="sqlite:///../storage/app.db"
uvicorn app.main:app --host 0.0.0.0 --port 9000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..
echo "$BACKEND_PID" >> .pids
echo "Started backend on PID $BACKEND_PID"

# Wait for backend to be ready
echo "Waiting for backend to start..."
for i in {1..30}; do
    if curl -s http://localhost:9000/docs > /dev/null 2>&1; then
        echo "Backend is ready"
        break
    fi
    sleep 1
done

# Start frontend in background
cd frontend
npm run dev -- --port 5173 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo "$FRONTEND_PID" >> .pids
echo "Started frontend on PID $FRONTEND_PID"

# Wait for frontend to be ready
echo "Waiting for frontend to start..."
for i in {1..30}; do
    if curl -s http://localhost:5173 > /dev/null 2>&1; then
        echo "Frontend is ready"
        break
    fi
    sleep 1
done

echo ""
echo "=== Services running ==="
echo "  Backend:  http://localhost:9000"
echo "  Frontend: http://localhost:5173"
echo "  Logs:     backend.log, frontend.log"
echo ""
echo "Run ./stop.sh to stop services"
