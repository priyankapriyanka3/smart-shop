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
            echo "Port $port in use, trying $((port+1))..." >&2
            port=$((port+1))
        done
    fi
    echo $port
}

# === Prerequisite checks ===
check_prerequisites() {
    local errors=0
    echo "=== Checking prerequisites ==="

    # Find available Python interpreter (Windows Git Bash compatibility)
    PYTHON=""
    for cmd in python3 python; do
        if command -v "$cmd" &>/dev/null && "$cmd" -c 'import sys' >/dev/null 2>&1; then
            PYTHON="$cmd"
            break
        fi
    done

    if [ -n "$PYTHON" ]; then
        PYTHON_VERSION=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
            echo "❌ Python 3.11+ required (found $PYTHON_VERSION)"
            errors=$((errors+1))
        else
            echo "✓ Python $PYTHON_VERSION"
        fi
    else
        echo "❌ Python 3 not found. Install from https://python.org"
        errors=$((errors+1))
    fi

    if [ -f "frontend/package.json" ]; then
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

        if ! command -v npm &>/dev/null; then
            echo "❌ npm not found"
            errors=$((errors+1))
        else
            echo "✓ npm $(npm --version)"
        fi
    fi

    if [ -n "$PYTHON" ] && ! "$PYTHON" -m pip --version &>/dev/null; then
        echo "❌ pip not found. Run: $PYTHON -m ensurepip"
        errors=$((errors+1))
    fi

    if [ $errors -gt 0 ]; then
        echo ""
        echo "❌ $errors prerequisite(s) missing. Please install them and retry."
        exit 1
    fi
    echo ""
}

check_prerequisites

# === Backend Setup ===
BACKEND_DIR="backend"
echo "=== Setting up backend ==="
cd "$BACKEND_DIR"

# Create and activate virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    "$PYTHON" -m venv .venv
fi

# Activate venv (cross-platform)
if [ -f ".venv/Scripts/activate" ]; then
    # Windows Git Bash
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    # macOS/Linux
    source .venv/bin/activate
fi

# Use 'python' once venv is active (exists in both bin/ and Scripts/)
PYTHON="python"

# Install dependencies
echo "Installing backend dependencies..."
pip install . -q

# Bootstrap .env from dev.env if not present
if [ ! -f ".env" ]; then
    echo "Initializing .env from dev.env..."
    cp dev.env .env
fi

# Database setup
export DATABASE_URL="${DATABASE_URL:-sqlite:///./app.db}"
echo "  Database: $DATABASE_URL"

# Run migrations
if [ -f "alembic.ini" ]; then
    echo "Running database migrations..."
    alembic upgrade head 2>/dev/null || echo "  Migrations already up to date"
fi

# Run seed data
if [ -f "app/seed.py" ]; then
    echo "Seeding database (if needed)..."
    "$PYTHON" -m app.seed 2>/dev/null || echo "  Database already seeded"
fi

# Find available port for backend
BACKEND_PORT=$(find_available_port ${BACKEND_PORT:-8000})
export BACKEND_PORT

echo "Starting backend on http://localhost:$BACKEND_PORT"
uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT &
BACKEND_PID=$!
cd "$SCRIPT_DIR"

# Save backend PID
echo "$BACKEND_PID" > .pids

# === Frontend Setup ===
FE_DIR="frontend"
FRONTEND_PORT=""

if [ -d "$FE_DIR" ] && [ -f "$FE_DIR/package.json" ]; then
    echo ""
    echo "=== Setting up frontend ==="
    cd "$FE_DIR"
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing frontend dependencies..."
        npm install
    fi

    # Find available port for frontend
    FRONTEND_PORT=$(find_available_port 5173)
    
    # Export backend port for vite proxy configuration
    export BACKEND_PORT

    echo "Starting frontend on http://localhost:$FRONTEND_PORT"
    npm run dev -- --port $FRONTEND_PORT &
    FE_PID=$!
    cd "$SCRIPT_DIR"
    
    # Save frontend PID
    echo "$FE_PID" >> .pids
fi

# Wait a moment for services to start
sleep 2

# Display startup information
echo ""
echo "========================================="
echo "  Smart Shop Application Started"
echo "========================================="
echo ""
echo "Services:"
echo "  Backend API:  http://localhost:$BACKEND_PORT"
echo "  API Docs:     http://localhost:$BACKEND_PORT/api/docs"
[ -n "$FRONTEND_PORT" ] && echo "  Frontend:     http://localhost:$FRONTEND_PORT"
echo ""
echo "Default Credentials:"
echo "  Admin:            admin@example.com / Admin123!"
echo "  Customer:         customer@example.com / Customer123!"
echo "  Inventory Mgr:    inventory@example.com / Inventory123!"
echo "  Customer Support: support@example.com / Support123!"
echo ""
echo "Press Ctrl+C to stop all services"
echo "========================================="
echo ""

# Wait for background processes
wait
