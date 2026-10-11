# Deliverability Fixes Summary

All 14 blockers have been fixed. Below is the detailed breakdown:

## 1-2. start-script-windows: Python detection and venv activation

**Files changed:**
- `/repos/smart-shop/start.sh` lines 30-52, 110-121, 125-127, 162-170

**Changes:**
1. Replaced hardcoded `python3` with a loop that tries `python3` then `python` to find a working interpreter
2. Changed venv activation to check for `.venv/Scripts/activate` (Windows) first, then fall back to `.venv/bin/activate` (Unix)
3. Changed venv creation from `python3 -m venv .venv` to `"$PYTHON" -m venv .venv`
4. Changed all activated venv calls from `python3` to `python` (which exists in both `bin/` and `Scripts/`)

**Verification:**
```bash
$ grep -n "PYTHON=" /repos/smart-shop/start.sh
33:    PYTHON=""
34:    for cmd in python3 python; do
36:            PYTHON="$cmd"

$ grep -n "source .venv" /repos/smart-shop/start.sh
118:if [ -f ".venv/Scripts/activate" ]; then
119:    source .venv/Scripts/activate
121:    source .venv/bin/activate
```

## 3. dockerfile: PIP_TARGET variable collision

**File changed:**
- `/repos/smart-shop/backend/Dockerfile` line 17

**Change:**
Renamed `ARG PIP_TARGET=.` to `ARG INSTALL_SPEC=.` to avoid pip reading it as its own `--target` option.

**Verification:**
```bash
$ grep PIP_TARGET /repos/smart-shop/backend/Dockerfile
# (no results - variable renamed)

$ grep INSTALL_SPEC /repos/smart-shop/backend/Dockerfile
ARG INSTALL_SPEC=.
    pip install --no-cache-dir "$INSTALL_SPEC"
```

## 4. packaging: Frontend reads shared_config.json from outside its directory

**Files changed:**
- `/repos/smart-shop/frontend/Dockerfile` (complete rewrite)
- `/repos/smart-shop/docker-compose.yml` service `frontend` build context
- `/repos/smart-shop/frontend/Dockerfile.dockerignore` (created)

**Changes:**
1. Updated frontend Dockerfile to expect build from repo root context
2. Added `COPY shared_config.json /app/shared_config.json` before copying frontend files
3. Changed all COPY paths to be relative to repo root: `COPY frontend/package.json frontend/package-lock.json ./`
4. Updated docker-compose.yml frontend service: `context: .` and `dockerfile: frontend/Dockerfile`
5. Created `frontend/Dockerfile.dockerignore` to exclude other components' build artifacts

**Verification:**
```bash
$ grep "context:" /repos/smart-shop/docker-compose.yml | head -4
      context: ./backend
      context: .

$ head -8 /repos/smart-shop/frontend/Dockerfile
# Frontend Dockerfile for Smart Shop - Multi-stage build
# Stage 1: Build
FROM node:22 AS build

WORKDIR /app

# Copy shared config first (from repo root context)
COPY shared_config.json /app/shared_config.json
```

## 5. packaging: Backend missing x-preview-port

**File changed:**
- `/repos/smart-shop/docker-compose.yml` service `backend`

**Change:**
Added `x-preview-port: 9000` to backend service definition.

**Verification:**
```bash
$ grep -A 1 "9000:9000" /repos/smart-shop/docker-compose.yml
      - "9000:9000"
    x-preview-port: 9000
```

## 6-8. preview-routing: Browser calls localhost URLs from preview

**Files changed:**
- `/repos/smart-shop/frontend/src/lib/api-client.ts` line 9
- `/repos/smart-shop/frontend/.env` (rewritten)
- `/repos/smart-shop/start.sh` lines 147-151

**Changes:**
1. Changed `api-client.ts`: `const BASE_URL = import.meta.env.VITE_API_URL || '/api'` (removed localhost fallback)
2. Rewrote `frontend/.env` to remove `VITE_API_URL=http://localhost:9000`, leaving it unset with a comment
3. Removed the line in `start.sh` that set `VITE_API_URL=http://localhost:$BACKEND_PORT` in .env

**Verification:**
```bash
$ grep "BASE_URL" /repos/smart-shop/frontend/src/lib/api-client.ts
const BASE_URL = import.meta.env.VITE_API_URL || '/api';

$ cat /repos/smart-shop/frontend/.env
# Frontend environment variables
# Leave VITE_API_URL unset to use relative /api path

$ grep "VITE_API_URL=" /repos/smart-shop/start.sh
# (no results - line removed)
```

## 9. python-install: Missing asyncpg dependency

**File changed:**
- `/repos/smart-shop/backend/pyproject.toml` dependencies list

**Change:**
Added `"asyncpg>=0.29.0",` to the dependencies array.

**Verification:**
```bash
$ grep asyncpg /repos/smart-shop/backend/pyproject.toml
    "asyncpg>=0.29.0",
```

## 10. python-types: customers.py:29 missing password_hash argument

**File changed:**
- `/repos/smart-shop/backend/app/routes/customers.py` register_user function (lines 18-29)

**Change:**
Added bcrypt import and password hashing before calling `service.create_user(data, password_hash)`.

**Verification:**
```bash
$ grep -A 3 "import bcrypt" /repos/smart-shop/backend/app/routes/customers.py
    import bcrypt
    
    service = CustomerService(db)
    # Hash the password before creating user

$ grep "create_user(data" /repos/smart-shop/backend/app/routes/customers.py
    return service.create_user(data, password_hash)
```

## 11. python-types: customers.py:52 incorrect method name

**File changed:**
- `/repos/smart-shop/backend/app/routes/customers.py` list_addresses function (line 57)

**Change:**
Changed `service.get_user_addresses(user_id)` to `service.get_addresses(user_id)`.

**Verification:**
```bash
$ grep "get_addresses" /repos/smart-shop/backend/app/routes/customers.py
    return service.get_addresses(user_id)

$ grep "get_user_addresses" /repos/smart-shop/backend/app/routes/customers.py
# (no results - method name corrected)
```

## 12. python-types: reviews.py:32 unexpected customer_id parameter

**File changed:**
- `/repos/smart-shop/backend/app/routes/reviews.py` list_reviews function (lines 30-36)

**Change:**
Removed `customer_id=customer_id,` from the `service.get_reviews()` call since the service method doesn't accept this parameter.

**Verification:**
```bash
$ grep -A 5 "service.get_reviews" /repos/smart-shop/backend/app/routes/reviews.py
    service = ReviewService(db)
    return service.get_reviews(
        product_id=product_id,
        status=status,
        page=page,
        page_size=page_size,
```

## 13. python-types: reviews.py:82 incorrect method name

**File changed:**
- `/repos/smart-shop/backend/app/routes/reviews.py` get_product_review_summary function (line 82)

**Change:**
Changed `service.get_product_review_summary(product_id)` to `service.get_aggregate_ratings(product_id)`.

**Verification:**
```bash
$ grep "get_aggregate_ratings" /repos/smart-shop/backend/app/routes/reviews.py
    return service.get_aggregate_ratings(product_id)

$ grep "service.get_product_review_summary" /repos/smart-shop/backend/app/routes/reviews.py
# (no results - method call corrected, only function name remains)
```

## 14. python-types: promotions.py:75 incorrect method name

**File changed:**
- `/repos/smart-shop/backend/app/routes/promotions.py` validate_promotion function (line 75)

**Change:**
Changed `service.validate_promotion(data.code, data.order_total)` to `service.check_eligibility(data.code, data.order_total)`.

**Verification:**
```bash
$ grep "check_eligibility" /repos/smart-shop/backend/app/routes/promotions.py
        return service.check_eligibility(data.code, data.order_total)

$ grep "service.validate_promotion" /repos/smart-shop/backend/app/routes/promotions.py
# (no results - method call corrected)
```

## Summary

All 14 blockers have been resolved:
- 2 Windows compatibility issues in start.sh (Python detection and venv activation)
- 1 Dockerfile ARG naming collision with pip
- 1 Docker packaging issue (frontend reading shared file outside context)
- 1 missing x-preview-port for backend service
- 3 preview routing issues (hardcoded localhost URLs)
- 1 missing Python dependency (asyncpg)
- 5 Python type errors (incorrect method calls and missing arguments)

No application logic, tests, or refactoring was performed. Only the specific blockers listed in the findings were addressed.
