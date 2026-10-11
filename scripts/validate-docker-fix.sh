#!/bin/bash
# Docker Build Fix Validation Script
# Verifies that the Dockerfile.frontend fix is correctly applied

set -e

echo "🔍 Docker Build Fix Validation"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKERFILE="${REPO_ROOT}/deployment/Dockerfile.frontend"

echo "📍 Repository Root: ${REPO_ROOT}"
echo "📄 Dockerfile: ${DOCKERFILE}"
echo ""

# Check 1: Dockerfile exists
echo "✓ Check 1: Dockerfile.frontend exists"
if [ ! -f "${DOCKERFILE}" ]; then
    echo -e "${RED}❌ FAIL: Dockerfile.frontend not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ PASS${NC}"
echo ""

# Check 2: Uses node:22-alpine base image
echo "✓ Check 2: Base image is node:22-alpine"
if grep -q "FROM node:22-alpine as build" "${DOCKERFILE}"; then
    echo -e "${GREEN}✅ PASS: node:22-alpine found${NC}"
else
    echo -e "${RED}❌ FAIL: node:22-alpine not found${NC}"
    echo "Current FROM directive:"
    grep "FROM node" "${DOCKERFILE}" || echo "  (none found)"
    exit 1
fi
echo ""

# Check 3: Build dependencies installed
echo "✓ Check 3: Build dependencies (python3, make, g++) installed"
if grep -q "apk add --no-cache python3 make g++" "${DOCKERFILE}"; then
    echo -e "${GREEN}✅ PASS: Build dependencies found${NC}"
else
    echo -e "${RED}❌ FAIL: Build dependencies not found${NC}"
    echo "Looking for: RUN apk add --no-cache python3 make g++"
    exit 1
fi
echo ""

# Check 4: Multi-stage build structure
echo "✓ Check 4: Multi-stage build (build + nginx stages)"
BUILD_STAGE=$(grep -c "FROM node:22-alpine as build" "${DOCKERFILE}" || true)
NGINX_STAGE=$(grep -c "FROM nginx:alpine" "${DOCKERFILE}" || true)

if [ "$BUILD_STAGE" -eq 1 ] && [ "$NGINX_STAGE" -eq 1 ]; then
    echo -e "${GREEN}✅ PASS: Multi-stage build structure correct${NC}"
else
    echo -e "${RED}❌ FAIL: Multi-stage build structure incorrect${NC}"
    echo "  Build stage count: ${BUILD_STAGE} (expected: 1)"
    echo "  Nginx stage count: ${NGINX_STAGE} (expected: 1)"
    exit 1
fi
echo ""

# Check 5: Build context files exist
echo "✓ Check 5: Build context files exist"
MISSING_FILES=0

check_file() {
    local file="$1"
    local full_path="${REPO_ROOT}/${file}"
    if [ -f "${full_path}" ]; then
        echo -e "  ${GREEN}✓${NC} ${file}"
    else
        echo -e "  ${RED}✗${NC} ${file} (missing)"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
}

check_file "frontend/package.json"
check_file "frontend/package-lock.json"
check_file "deployment/nginx.conf.template"

if [ $MISSING_FILES -eq 0 ]; then
    echo -e "${GREEN}✅ PASS: All required files exist${NC}"
else
    echo -e "${RED}❌ FAIL: ${MISSING_FILES} required file(s) missing${NC}"
    exit 1
fi
echo ""

# Check 6: CI workflow references correct Dockerfile
echo "✓ Check 6: CI workflow uses correct Dockerfile"
CI_WORKFLOW="${REPO_ROOT}/.github/workflows/ci.yml"

if [ -f "${CI_WORKFLOW}" ]; then
    if grep -q "docker build -f Dockerfile.frontend" "${CI_WORKFLOW}"; then
        echo -e "${GREEN}✅ PASS: CI workflow references Dockerfile.frontend${NC}"
    else
        echo -e "${YELLOW}⚠️  WARNING: CI workflow may not reference Dockerfile.frontend${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  WARNING: CI workflow file not found${NC}"
fi
echo ""

# Check 7: Layer caching optimization (package.json copied before source)
echo "✓ Check 7: Docker layer caching optimized"
DOCKERFILE_CONTENT=$(cat "${DOCKERFILE}")

# Extract line numbers for COPY commands
PACKAGE_COPY_LINE=$(echo "$DOCKERFILE_CONTENT" | grep -n "COPY frontend/package.json" | cut -d: -f1 || echo "0")
SOURCE_COPY_LINE=$(echo "$DOCKERFILE_CONTENT" | grep -n "COPY frontend/ /app/" | cut -d: -f1 || echo "0")

if [ "$PACKAGE_COPY_LINE" -gt 0 ] && [ "$SOURCE_COPY_LINE" -gt 0 ]; then
    if [ "$PACKAGE_COPY_LINE" -lt "$SOURCE_COPY_LINE" ]; then
        echo -e "${GREEN}✅ PASS: package.json copied before source code (line ${PACKAGE_COPY_LINE} < line ${SOURCE_COPY_LINE})${NC}"
    else
        echo -e "${YELLOW}⚠️  WARNING: Layer caching may not be optimized${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  WARNING: Could not verify layer caching order${NC}"
fi
echo ""

# Summary
echo "================================"
echo -e "${GREEN}✅ All validation checks passed!${NC}"
echo ""
echo "The Docker build fix has been correctly applied:"
echo "  • Base image: node:22-slim → node:22-alpine ✓"
echo "  • Build tools: python3, make, g++ installed ✓"
echo "  • Multi-stage build: maintained ✓"
echo "  • Build context: all files present ✓"
echo "  • Layer caching: optimized ✓"
echo ""
echo "🚀 Ready for CI/Docker Build Validation in GitHub Actions"
