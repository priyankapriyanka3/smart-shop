#!/bin/bash
# Integration Test Runner
# Runs all integration tests for CI/Docker build validation fix

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Repository root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Smart Shop Integration Test Suite${NC}"
echo -e "${BLUE}Epic 1: Product Catalog Management${NC}"
echo -e "${BLUE}Fix: CI/Docker Build Validation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Track test results
BACKEND_TESTS_PASSED=0
FRONTEND_TESTS_PASSED=0
TOTAL_FAILURES=0

# Function to print section header
print_section() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Run Backend Integration Tests
run_backend_tests() {
    print_section "Running Backend Integration Tests"
    
    cd "$REPO_ROOT/backend"
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        print_warning "Virtual environment not found, creating..."
        python3 -m venv .venv
        source .venv/bin/activate
        pip install ".[dev]"
    else
        source .venv/bin/activate
    fi
    
    # Run Docker build validation tests
    echo -e "\n${YELLOW}Test Suite: Docker Build Configuration${NC}"
    if pytest tests/integration/test_docker_build.py -v --tb=short; then
        print_success "Docker build configuration tests passed"
        BACKEND_TESTS_PASSED=$((BACKEND_TESTS_PASSED + 1))
    else
        print_error "Docker build configuration tests failed"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    # Run API integration tests
    echo -e "\n${YELLOW}Test Suite: API Integration & Contract Tests${NC}"
    if OTEL_SDK_DISABLED=true pytest tests/integration/test_api_integration.py -v --tb=short; then
        print_success "API integration tests passed"
        BACKEND_TESTS_PASSED=$((BACKEND_TESTS_PASSED + 1))
    else
        print_error "API integration tests failed"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    # Run all backend tests with coverage
    echo -e "\n${YELLOW}Test Suite: Full Backend Test Suite${NC}"
    if OTEL_SDK_DISABLED=true pytest -v --cov=app --cov-report=term --cov-report=html:htmlcov; then
        print_success "Full backend test suite passed"
        BACKEND_TESTS_PASSED=$((BACKEND_TESTS_PASSED + 1))
    else
        print_error "Full backend test suite had failures"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    deactivate
    cd "$REPO_ROOT"
}

# Run Frontend Integration Tests
run_frontend_tests() {
    print_section "Running Frontend Integration Tests"
    
    cd "$REPO_ROOT/frontend"
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        print_warning "Node modules not found, installing..."
        npm ci
    fi
    
    # Run Docker build validation tests
    echo -e "\n${YELLOW}Test Suite: Docker Build & CI Configuration${NC}"
    if npm run test -- tests/integration/docker-build.test.ts --run; then
        print_success "Frontend Docker build tests passed"
        FRONTEND_TESTS_PASSED=$((FRONTEND_TESTS_PASSED + 1))
    else
        print_error "Frontend Docker build tests failed"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    # Run all frontend tests
    echo -e "\n${YELLOW}Test Suite: Full Frontend Test Suite${NC}"
    if npm run test -- --run; then
        print_success "Full frontend test suite passed"
        FRONTEND_TESTS_PASSED=$((FRONTEND_TESTS_PASSED + 1))
    else
        print_error "Full frontend test suite had failures"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    # Type check
    echo -e "\n${YELLOW}TypeScript Type Check${NC}"
    if npx tsc --noEmit; then
        print_success "TypeScript type check passed"
        FRONTEND_TESTS_PASSED=$((FRONTEND_TESTS_PASSED + 1))
    else
        print_error "TypeScript type check failed"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    cd "$REPO_ROOT"
}

# Verify CI Workflow Configuration
verify_ci_workflow() {
    print_section "Verifying CI Workflow Configuration"
    
    CI_FILE="$REPO_ROOT/.github/workflows/ci.yml"
    
    if [ ! -f "$CI_FILE" ]; then
        print_error "CI workflow file not found: $CI_FILE"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
        return 1
    fi
    
    # Check for required CI jobs
    if grep -q "Docker Build Validation" "$CI_FILE"; then
        print_success "Docker Build Validation job found"
    else
        print_error "Docker Build Validation job not found in CI"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    if grep -q "Dockerfile.frontend" "$CI_FILE"; then
        print_success "Frontend Docker build command found"
    else
        print_error "Frontend Docker build command not found in CI"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    if grep -q "Dockerfile.backend" "$CI_FILE"; then
        print_success "Backend Docker build command found"
    else
        print_error "Backend Docker build command not found in CI"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    if grep -q "docker compose config" "$CI_FILE" || grep -q "docker-compose config" "$CI_FILE"; then
        print_success "Docker Compose validation found"
    else
        print_warning "Docker Compose validation not found (optional)"
    fi
}

# Verify Dockerfile Configuration
verify_dockerfiles() {
    print_section "Verifying Dockerfile Configuration"
    
    FRONTEND_DOCKERFILE="$REPO_ROOT/deployment/Dockerfile.frontend"
    BACKEND_DOCKERFILE="$REPO_ROOT/deployment/Dockerfile.backend"
    
    # Check frontend Dockerfile
    if [ ! -f "$FRONTEND_DOCKERFILE" ]; then
        print_error "Frontend Dockerfile not found"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
        return 1
    fi
    
    if grep -q "FROM node:22-alpine" "$FRONTEND_DOCKERFILE"; then
        print_success "Frontend Dockerfile uses node:22-alpine"
    else
        print_error "Frontend Dockerfile does not use node:22-alpine"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    if grep -q "python3.*make.*g++" "$FRONTEND_DOCKERFILE" || (grep -q "python3" "$FRONTEND_DOCKERFILE" && grep -q "make" "$FRONTEND_DOCKERFILE" && grep -q "g++" "$FRONTEND_DOCKERFILE"); then
        print_success "Frontend Dockerfile installs required build tools"
    else
        print_error "Frontend Dockerfile missing build dependencies"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    if grep -q "FROM nginx:alpine" "$FRONTEND_DOCKERFILE"; then
        print_success "Frontend Dockerfile uses nginx:alpine for production"
    else
        print_error "Frontend Dockerfile missing nginx:alpine stage"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
    
    # Check backend Dockerfile
    if [ ! -f "$BACKEND_DOCKERFILE" ]; then
        print_error "Backend Dockerfile not found"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
        return 1
    fi
    
    if grep -q "FROM python:3.11" "$BACKEND_DOCKERFILE"; then
        print_success "Backend Dockerfile uses Python 3.11"
    else
        print_error "Backend Dockerfile does not use Python 3.11"
        TOTAL_FAILURES=$((TOTAL_FAILURES + 1))
    fi
}

# Print final summary
print_summary() {
    print_section "Test Summary"
    
    echo -e "Backend Test Suites Passed: ${GREEN}$BACKEND_TESTS_PASSED${NC}"
    echo -e "Frontend Test Suites Passed: ${GREEN}$FRONTEND_TESTS_PASSED${NC}"
    echo -e "Total Failures: ${RED}$TOTAL_FAILURES${NC}"
    echo ""
    
    if [ $TOTAL_FAILURES -eq 0 ]; then
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}✓ ALL INTEGRATION TESTS PASSED${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo -e "${GREEN}The CI/Docker Build Validation fix is verified and working correctly.${NC}"
        echo -e "${GREEN}PR #4 (Epic 1 - Product Catalog Management) is ready for merge.${NC}"
        return 0
    else
        echo -e "${RED}========================================${NC}"
        echo -e "${RED}✗ INTEGRATION TESTS FAILED${NC}"
        echo -e "${RED}========================================${NC}"
        echo ""
        echo -e "${RED}Please review the failures above and fix the issues.${NC}"
        return 1
    fi
}

# Main execution
main() {
    # Parse command line arguments
    RUN_BACKEND=true
    RUN_FRONTEND=true
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --backend-only)
                RUN_FRONTEND=false
                shift
                ;;
            --frontend-only)
                RUN_BACKEND=false
                shift
                ;;
            --help)
                echo "Usage: $0 [--backend-only] [--frontend-only] [--help]"
                echo ""
                echo "Options:"
                echo "  --backend-only   Run only backend integration tests"
                echo "  --frontend-only  Run only frontend integration tests"
                echo "  --help          Show this help message"
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
    
    # Run tests
    if [ "$RUN_BACKEND" = true ]; then
        run_backend_tests
    fi
    
    if [ "$RUN_FRONTEND" = true ]; then
        run_frontend_tests
    fi
    
    # Run verifications
    verify_ci_workflow
    verify_dockerfiles
    
    # Print summary and exit
    print_summary
    exit $?
}

# Run main function
main "$@"
