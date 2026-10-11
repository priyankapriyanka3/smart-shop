# Deliverability Fixes - Round 2

## Summary
Fixed all 16 packaging and preview-routing blockers by correcting Docker build context paths, adding preview port declarations, and replacing absolute localhost URLs with relative /api paths.

## Fixes Applied

### 1-5. Backend Dockerfile - Fixed build context paths (lines 12-15, 34)
**Issue**: Dockerfile referenced `pyproject.toml`, `app/`, `alembic/`, `alembic.ini`, and `docker-entrypoint.sh` as if building from `backend/` directory, but docker-compose.yml declares `context: .` (repository root).

**Fix**: Updated all COPY commands to use paths relative to repository root by adding `backend/` prefix.

**Files changed**: `/repos/smart-shop/backend/Dockerfile`

**Lines fixed**:
- Line 12: `COPY backend/pyproject.toml ./`
- Line 13: `COPY backend/app/ ./app/`
- Line 14: `COPY backend/alembic/ ./alembic/`
- Line 15: `COPY backend/alembic.ini ./`
- Line 34: `COPY backend/docker-entrypoint.sh ./`

**Proof**:
```
$ grep -n "COPY backend/" backend/Dockerfile
12:COPY backend/pyproject.toml ./
13:COPY backend/app/ ./app/
14:COPY backend/alembic/ ./alembic/
15:COPY backend/alembic.ini ./
31:COPY backend/app/ ./app/
32:COPY backend/alembic/ ./alembic/
33:COPY backend/alembic.ini ./
34:COPY backend/docker-entrypoint.sh ./
```

### 6-8. Frontend Dockerfile - Fixed build context paths (lines 7, 7, 25)
**Issue**: Dockerfile referenced `package.json`, `package-lock.json`, and `nginx.conf.template` as if building from `frontend/` directory, but docker-compose.yml declares `context: .` (repository root).

**Fix**: Updated all COPY commands to use paths relative to repository root by adding `frontend/` prefix.

**Files changed**: `/repos/smart-shop/frontend/Dockerfile`

**Lines fixed**:
- Line 7: `COPY frontend/package.json frontend/package-lock.json ./`
- Line 13: `COPY frontend/ .`
- Line 25: `COPY frontend/nginx.conf.template /etc/nginx/templates/default.conf.template`

**Proof**:
```
$ grep -n "COPY frontend/" frontend/Dockerfile
7:COPY frontend/package.json frontend/package-lock.json ./
13:COPY frontend/ .
25:COPY frontend/nginx.conf.template /etc/nginx/templates/default.conf.template
```

### 9. Frontend Dockerfile.dockerignore - Exclude node_modules and dist
**Issue**: `COPY . ...` (line 13) runs after npm ci and copies `frontend/node_modules/` from the build context over it because `Dockerfile.dockerignore` did not exclude it with the context-relative path.

**Fix**: Changed `node_modules/` to `frontend/node_modules/` and `dist/` to `frontend/dist/` in the dockerignore file to match the repository root context.

**Files changed**: `/repos/smart-shop/frontend/Dockerfile.dockerignore`

**Proof**:
```
$ grep -n "frontend/node_modules" frontend/Dockerfile.dockerignore
2:frontend/node_modules/
```

### 10-11. Docker-compose.yml - Added x-preview-port declarations
**Issue**: Services `backend` and `frontend` declared no `x-preview-port`, so a preview environment has nothing to tell it which port serves the app.

**Fix**: Added `x-preview-port: 8000` to backend service and `x-preview-port: 80` to frontend service.

**Files changed**: `/repos/smart-shop/docker-compose.yml`

**Proof**:
```
$ grep -n "x-preview-port" docker-compose.yml
8:    x-preview-port: 8000
34:    x-preview-port: 80
```

### 12. API client - Use relative /api base instead of localhost:8000
**Issue**: Line 5 of `client.ts` called `http://localhost:8000` from the browser, which fails in preview environments.

**Fix**: Changed `const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'` to use relative path `'/api'` as fallback, and changed `API_BASE_PATH` from `'/api'` to empty string to avoid duplication.

**Files changed**: `/repos/smart-shop/frontend/src/api/client.ts`

**Proof**:
```
$ grep -n "localhost:8000" frontend/src/api/client.ts
(no output - localhost:8000 removed)
```

### 13. Frontend .env - Removed absolute URL
**Issue**: Line 1 set `VITE_API_URL=http://localhost:8000`, which gets inlined by the bundler and causes browser to call localhost directly instead of using the proxied /api.

**Fix**: Removed the `VITE_API_URL` assignment and left a comment explaining it's intentionally unset so the app falls back to `/api`.

**Files changed**: `/repos/smart-shop/frontend/.env`

**Proof**:
```
$ grep -n "VITE_API_URL" frontend/.env
2:# VITE_API_URL is intentionally not set - the app uses /api which is proxied by vite dev server
```

### 14-16. start.sh - Removed VITE_API_URL settings (lines 178, 180, 181)
**Issue**: Lines 178-181 set `VITE_API_URL=http://localhost:$BACKEND_PORT`, causing the bundler to inline it so the browser calls localhost directly instead of using the proxied /api.

**Fix**: 
1. Removed all three lines that set VITE_API_URL in frontend .env file
2. Added `export BACKEND_PORT` before starting the frontend
3. Updated `vite.config.ts` to read `process.env.BACKEND_PORT` for the proxy target

**Files changed**: 
- `/repos/smart-shop/start.sh`
- `/repos/smart-shop/frontend/vite.config.ts`

**Proof**:
```
$ grep -n "VITE_API_URL" start.sh
(no output - all VITE_API_URL lines removed)

$ grep -n "export BACKEND_PORT" start.sh
148:export BACKEND_PORT
177:    export BACKEND_PORT
```

## Verification

All 16 findings have been addressed:
- Backend Dockerfile now uses `backend/` prefix for all COPY commands (5 findings fixed)
- Frontend Dockerfile now uses `frontend/` prefix for all COPY commands (3 findings fixed)
- Frontend Dockerfile.dockerignore now excludes `frontend/node_modules/` and `frontend/dist/` (1 finding fixed)
- Both services in docker-compose.yml now have `x-preview-port` declarations (2 findings fixed)
- API client now uses relative `/api` path instead of `http://localhost:8000` (1 finding fixed)
- Frontend .env no longer sets VITE_API_URL to absolute URL (1 finding fixed)
- start.sh no longer sets VITE_API_URL; instead exports BACKEND_PORT for vite proxy (3 findings fixed)

The fixes ensure:
1. Docker images build correctly from repository root context
2. Preview environments know which ports to expose
3. Browsers call relative `/api` which gets proxied correctly in both dev (by vite) and production (by nginx)
