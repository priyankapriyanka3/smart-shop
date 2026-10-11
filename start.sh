#!/bin/bash
# start.sh — Start the Smart Shop full-stack application
set -e
trap 'echo "Shutting down..."; [ -f .pids ] && while IFS= read -r pid; do kill "$pid" 2>/dev/null || true; done < .pids; rm -f .pids; exit 0' SIGINT SIGTERM

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Portable sed (macOS + Linux)
portable_sed() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "$@"
    else
        sed -i "$@"
    fi
}

# Port detection
find_available_port() {
    local port=$1
    if command -v lsof &>/dev/null; then
        while lsof -iTCP:$port -sTCP:LISTEN -t >/dev/null 2>&1; do
            port=$((port+1))
        done
    fi
    echo $port
}

# === Prerequisite checks ===
check_prerequisites() {
    local errors=0
    echo "=== Checking prerequisites ==="

    # Python 3.10+ - detect python3 or python (Windows compatibility)
    PYTHON=""
    for cmd in python3 python; do
        if command -v "$cmd" &>/dev/null && "$cmd" -c "import sys" &>/dev/null 2>&1; then
            PYTHON="$cmd"
            break
        fi
    done
    
    if [ -n "$PYTHON" ]; then
        PYTHON_VERSION=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
            echo "❌ Python 3.10+ required (found $PYTHON_VERSION)"
            errors=$((errors+1))
        else
            echo "✓ Python $PYTHON_VERSION"
        fi
    else
        echo "❌ Python 3 not found. Install from https://python.org"
        errors=$((errors+1))
    fi

    # pip
    if [ -n "$PYTHON" ] && ! "$PYTHON" -m pip --version &>/dev/null; then
        echo "❌ pip not found. Run: $PYTHON -m ensurepip"
        errors=$((errors+1))
    fi

    # Node.js 18+
    if command -v node &>/dev/null; then
        NODE_VERSION=$(node --version | sed 's/v//')
        NODE_MAJOR=$(echo $NODE_VERSION | cut -d. -f1)
        if [ "$NODE_MAJOR" -lt 18 ]; then
            echo "❌ Node.js 18+ required (found $NODE_VERSION)"
            errors=$((errors+1))
        else
            echo "✓ Node.js $NODE_VERSION"
        fi
    else
        echo "❌ Node.js not found. Install from https://nodejs.org"
        errors=$((errors+1))
    fi

    # npm
    if ! command -v npm &>/dev/null; then
        echo "❌ npm not found"
        errors=$((errors+1))
    else
        echo "✓ npm $(npm --version)"
    fi

    if [ $errors -gt 0 ]; then
        echo ""
        echo "❌ $errors prerequisite(s) missing. Please install them and retry."
        exit 1
    fi
    echo ""
}

check_prerequisites

# Ensure storage directory exists
mkdir -p storage

# === Backend Setup ===
BACKEND_DIR="backend"
echo "=== Setting up backend ==="
cd "$BACKEND_DIR"

# Copy dev.env to .env if .env doesn't exist
if [ ! -f ".env" ] && [ -f "dev.env" ]; then
    echo "Creating .env from dev.env..."
    cp dev.env .env
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    "$PYTHON" -m venv .venv
fi

# Activate virtual environment (Windows Git Bash uses Scripts/activate, Unix uses bin/activate)
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install dependencies
echo "Installing backend dependencies..."
if [ -f "pyproject.toml" ]; then
    pip install . -q
fi

# Export DATABASE_URL (force override any system variable)
export DATABASE_URL="sqlite:///./storage/app.db"
echo "Database: $DATABASE_URL"

# Run seed script (use 'python' from activated venv, not python3)
if [ -f "app/seed.py" ]; then
    echo "Seeding database..."
    python -m app.seed 2>/dev/null || true
fi

# Find available backend port
BACKEND_PORT=$(find_available_port 9000)
echo "Starting backend on http://localhost:$BACKEND_PORT"
uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT &
BACKEND_PID=$!
cd "$SCRIPT_DIR"

# === Frontend Setup ===
FRONTEND_DIR="frontend"
echo "=== Setting up frontend ==="
cd "$FRONTEND_DIR"

# Install dependencies
echo "Installing frontend dependencies..."
npm install -q

# Find available frontend port
FRONTEND_PORT=$(find_available_port 5173)

# Export BACKEND_PORT for vite.config.ts proxy (don't set VITE_API_URL)
export BACKEND_PORT

echo "Starting frontend on http://localhost:$FRONTEND_PORT"
npm run dev -- --port $FRONTEND_PORT --host &
FRONTEND_PID=$!
cd "$SCRIPT_DIR"

# Update shared_config.json with actual ports using Python (use 'python' not python3)
if [ -f "shared_config.json" ]; then
    python -c "
import json
with open('shared_config.json') as f:
    cfg = json.load(f)
cfg['ports']['backend'] = int('$BACKEND_PORT')
cfg['ports']['frontend_web'] = int('$FRONTEND_PORT')
with open('shared_config.json', 'w') as f:
    json.dump(cfg, f, indent=2)
" 2>/dev/null || true
fi

# Save PIDs
echo "$BACKEND_PID" > .pids
echo "$FRONTEND_PID" >> .pids

echo ""
echo "=== Services running ==="
echo "  Backend:  http://localhost:$BACKEND_PORT"
echo "  Frontend: http://localhost:$FRONTEND_PORT"
echo ""
echo "=== Default Credentials ==="
echo "  Email:    admin@example.com"
echo "  Password: admin123"
echo ""
echo "Press Ctrl+C to stop all services"
wait
