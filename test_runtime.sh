#!/bin/bash
# test_runtime.sh — Runtime verification test script
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Runtime Verification Tests ==="
echo ""

# Clean up any existing processes
if [ -f .pids ]; then
    echo "Cleaning up existing processes..."
    while IFS= read -r pid; do
        kill "$pid" 2>/dev/null || true
    done < .pids
    rm -f .pids
fi

# Remove any existing database to ensure clean state
rm -f backend/app.db 2>/dev/null || true

# Start services in background
echo "Starting services..."
unset DATABASE_URL
cd backend
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null
pip install . -q
alembic upgrade head 2>&1 | grep -v "INFO"
python -m app.seed 2>&1 | grep -v "INFO" | head -5
uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "$BACKEND_PID" > ../.pids
cd ..

cd frontend
npm install -q 2>/dev/null || true
npm run dev -- --port 5173 > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "$FRONTEND_PID" >> .pids
cd ..

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 5

# Test backend API
echo ""
echo "Test 1: Backend API responds to /api/products"
PRODUCTS_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:8000/api/products?page=1&per_page=10)
PRODUCTS_CODE=$(echo "$PRODUCTS_RESPONSE" | tail -1)
if [ "$PRODUCTS_CODE" = "200" ]; then
    echo "  ✓ Backend API responds correctly (HTTP 200)"
    PRODUCTS_DATA=$(echo "$PRODUCTS_RESPONSE" | head -n -1)
    PRODUCT_COUNT=$(echo "$PRODUCTS_DATA" | grep -o '"total":[0-9]*' | head -1 | cut -d: -f2)
    echo "  ✓ Returned $PRODUCT_COUNT total products"
else
    echo "  ✗ Backend API failed (HTTP $PRODUCTS_CODE)"
    cat backend.log | tail -20
    bash stop.sh
    exit 1
fi

# Test frontend
echo ""
echo "Test 2: Frontend serves HTML"
FRONTEND_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:5173)
FRONTEND_CODE=$(echo "$FRONTEND_RESPONSE" | tail -1)
if [ "$FRONTEND_CODE" = "200" ]; then
    echo "  ✓ Frontend serves correctly (HTTP 200)"
    if echo "$FRONTEND_RESPONSE" | head -n -1 | grep -q "<!DOCTYPE html>"; then
        echo "  ✓ HTML content detected"
    else
        echo "  ⚠ Warning: HTML content not detected in response"
    fi
else
    echo "  ✗ Frontend failed (HTTP $FRONTEND_CODE)"
    cat frontend.log | tail -20
    bash stop.sh
    exit 1
fi

# Test seed data
echo ""
echo "Test 3: Verify seed admin user exists"
cd backend
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null
SEED_CHECK=$(python -c "from app.models import Customer; from app.database import SessionLocal; db = SessionLocal(); admin = db.query(Customer).filter_by(email='admin@example.com').first(); assert admin is not None; assert admin.role == 'admin'; print('Seed admin user verified')" 2>&1)
if echo "$SEED_CHECK" | grep -q "Seed admin user verified"; then
    echo "  ✓ Seed admin user verified (admin@example.com with admin role)"
else
    echo "  ✗ Seed admin user verification failed"
    echo "$SEED_CHECK"
    cd ..
    bash stop.sh
    exit 1
fi
cd ..

# Test documentation
echo ""
echo "Test 4: Verify seed credentials documented in README"
if grep -q "admin@example.com" README.md && grep -q "Admin123!" README.md; then
    echo "  ✓ Seed credentials documented in README"
else
    echo "  ✗ Seed credentials missing from README"
    bash stop.sh
    exit 1
fi

echo ""
echo "Test 5: Verify seed credentials referenced in .env.example"
if grep -q "customer@example.com" .env.example; then
    echo "  ✓ Seed credentials referenced in .env.example"
else
    echo "  ✗ Seed credentials missing from .env.example"
    bash stop.sh
    exit 1
fi

# Stop services
echo ""
echo "Stopping services..."
bash stop.sh

echo ""
echo "========================================="
echo "  All Runtime Verification Tests Passed"
echo "========================================="
