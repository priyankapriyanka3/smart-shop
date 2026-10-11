"""Integration tests for Docker build validation.

These tests verify that:
1. Dockerfile configurations are valid
2. All referenced files exist in the build context
3. Docker build commands match CI workflow expectations
4. Multi-stage builds are properly structured
"""
import os
import re
from pathlib import Path

import pytest


@pytest.fixture
def repo_root():
    """Get repository root path."""
    # Navigate from backend/tests/integration to repo root
    current_dir = Path(__file__).resolve()
    return current_dir.parent.parent.parent.parent


@pytest.fixture
def deployment_dir(repo_root):
    """Get deployment directory path."""
    return repo_root / "deployment"


class TestDockerfileStructure:
    """Test Dockerfile structure and validity."""

    def test_frontend_dockerfile_exists(self, deployment_dir):
        """Verify frontend Dockerfile exists."""
        dockerfile = deployment_dir / "Dockerfile.frontend"
        assert dockerfile.exists(), "Dockerfile.frontend not found"
        assert dockerfile.stat().st_size > 0, "Dockerfile.frontend is empty"

    def test_backend_dockerfile_exists(self, deployment_dir):
        """Verify backend Dockerfile exists."""
        dockerfile = deployment_dir / "Dockerfile.backend"
        assert dockerfile.exists(), "Dockerfile.backend not found"
        assert dockerfile.stat().st_size > 0, "Dockerfile.backend is empty"

    def test_frontend_dockerfile_uses_alpine_base(self, deployment_dir):
        """Verify frontend Dockerfile uses node:22-alpine base image."""
        dockerfile = deployment_dir / "Dockerfile.frontend"
        content = dockerfile.read_text()
        
        # Check for node:22-alpine in FROM directive
        assert "FROM node:22-alpine" in content, \
            "Frontend Dockerfile should use node:22-alpine base image"
        
        # Ensure node:22-slim is NOT used (would cause npm ci failures)
        assert "node:22-slim" not in content, \
            "Frontend Dockerfile should NOT use node:22-slim (lacks build tools)"

    def test_frontend_dockerfile_has_build_dependencies(self, deployment_dir):
        """Verify frontend Dockerfile installs required build dependencies."""
        dockerfile = deployment_dir / "Dockerfile.frontend"
        content = dockerfile.read_text()
        
        # Check for build dependency installation
        assert "apk add" in content, "Missing apk add command for Alpine packages"
        assert "python3" in content, "Missing python3 dependency (required by node-gyp)"
        assert "make" in content, "Missing make dependency (required for native builds)"
        assert "g++" in content, "Missing g++ dependency (required for C++ compilation)"

    def test_backend_dockerfile_structure(self, deployment_dir):
        """Verify backend Dockerfile has correct base image and structure."""
        dockerfile = deployment_dir / "Dockerfile.backend"
        content = dockerfile.read_text()
        
        # Check for Python 3.11 base image
        assert "FROM python:3.11" in content, "Backend should use Python 3.11 base image"
        
        # Check for required RUN commands
        assert "pip install" in content, "Missing pip install command"
        assert "WORKDIR /app" in content, "Missing WORKDIR directive"

    def test_frontend_multistage_build_structure(self, deployment_dir):
        """Verify frontend Dockerfile uses multi-stage build correctly."""
        dockerfile = deployment_dir / "Dockerfile.frontend"
        content = dockerfile.read_text()
        
        # Check for build stage
        assert re.search(r'FROM\s+node:22-alpine\s+as\s+build', content), \
            "Missing build stage definition"
        
        # Check for production stage with nginx
        assert "FROM nginx:alpine" in content, \
            "Missing nginx:alpine production stage"
        
        # Check for COPY --from=build
        assert re.search(r'COPY\s+--from=build', content), \
            "Missing COPY --from=build directive for multi-stage optimization"

    def test_dockerignore_exists(self, deployment_dir):
        """Verify .dockerignore file exists to optimize build context."""
        dockerignore = deployment_dir / ".dockerignore"
        assert dockerignore.exists(), ".dockerignore file not found"
        
        content = dockerignore.read_text()
        # Check for common exclusions
        assert "node_modules" in content, "Should exclude node_modules"
        assert "__pycache__" in content, "Should exclude __pycache__"
        assert ".git" in content, "Should exclude .git directory"


class TestBuildContextFiles:
    """Test that all files referenced in Dockerfiles exist in build context."""

    def test_frontend_package_files_exist(self, repo_root):
        """Verify frontend package.json and package-lock.json exist."""
        frontend_dir = repo_root / "frontend"
        
        assert (frontend_dir / "package.json").exists(), \
            "frontend/package.json not found (required by Dockerfile.frontend)"
        assert (frontend_dir / "package-lock.json").exists(), \
            "frontend/package-lock.json not found (required for npm ci)"

    def test_backend_pyproject_exists(self, repo_root):
        """Verify backend pyproject.toml exists."""
        backend_dir = repo_root / "backend"
        
        assert (backend_dir / "pyproject.toml").exists(), \
            "backend/pyproject.toml not found (required by Dockerfile.backend)"

    def test_nginx_config_template_exists(self, deployment_dir):
        """Verify nginx.conf.template exists for frontend serving."""
        nginx_config = deployment_dir / "nginx.conf.template"
        assert nginx_config.exists(), \
            "deployment/nginx.conf.template not found (required by Dockerfile.frontend)"
        
        content = nginx_config.read_text()
        # Verify it contains essential nginx configuration
        assert "server {" in content, "Invalid nginx configuration"
        assert "location" in content, "Missing location blocks"

    def test_docker_entrypoint_exists(self, deployment_dir):
        """Verify docker-entrypoint.sh exists for backend."""
        entrypoint = deployment_dir / "docker-entrypoint.sh"
        assert entrypoint.exists(), \
            "deployment/docker-entrypoint.sh not found (required by Dockerfile.backend)"
        
        # Check if executable bit is set (important for Docker)
        assert os.access(entrypoint, os.X_OK), \
            "docker-entrypoint.sh should be executable"

    def test_backend_app_directory_exists(self, repo_root):
        """Verify backend/app directory exists."""
        app_dir = repo_root / "backend" / "app"
        assert app_dir.exists(), "backend/app directory not found"
        assert app_dir.is_dir(), "backend/app should be a directory"

    def test_backend_alembic_directory_exists(self, repo_root):
        """Verify backend/alembic directory exists."""
        alembic_dir = repo_root / "backend" / "alembic"
        assert alembic_dir.exists(), "backend/alembic directory not found"
        assert (repo_root / "backend" / "alembic.ini").exists(), \
            "backend/alembic.ini not found"


class TestCIWorkflowConfiguration:
    """Test CI workflow Docker build commands."""

    def test_ci_workflow_file_exists(self, repo_root):
        """Verify CI workflow file exists."""
        ci_workflow = repo_root / ".github" / "workflows" / "ci.yml"
        assert ci_workflow.exists(), ".github/workflows/ci.yml not found"

    def test_ci_docker_build_commands(self, repo_root):
        """Verify CI workflow contains correct Docker build commands."""
        ci_workflow = repo_root / ".github" / "workflows" / "ci.yml"
        content = ci_workflow.read_text()
        
        # Check for Docker Build Validation job
        assert "Docker Build Validation" in content, \
            "Missing 'Docker Build Validation' job in CI workflow"
        
        # Check for backend build command
        assert "docker build -f Dockerfile.backend" in content, \
            "Missing backend Docker build command"
        assert "smart-shop-backend:test" in content, \
            "Missing backend image tag"
        
        # Check for frontend build command
        assert "docker build -f Dockerfile.frontend" in content, \
            "Missing frontend Docker build command"
        assert "smart-shop-frontend:test" in content, \
            "Missing frontend image tag"
        
        # Verify build context is '..' (repository root)
        # The working-directory is 'deployment', so build context should be '..'
        assert "working-directory: deployment" in content, \
            "Docker builds should run from deployment directory"

    def test_ci_docker_compose_validation(self, repo_root):
        """Verify CI workflow includes docker-compose validation."""
        ci_workflow = repo_root / ".github" / "workflows" / "ci.yml"
        content = ci_workflow.read_text()
        
        # Check for docker-compose validation
        assert "docker compose config" in content or "docker-compose config" in content, \
            "Missing docker-compose configuration validation"


class TestDockerComposeConfiguration:
    """Test docker-compose.yml configuration."""

    def test_docker_compose_file_exists(self, deployment_dir):
        """Verify docker-compose.yml exists."""
        compose_file = deployment_dir / "docker-compose.yml"
        assert compose_file.exists(), "deployment/docker-compose.yml not found"

    def test_docker_compose_references_dockerfiles(self, deployment_dir):
        """Verify docker-compose.yml references the correct Dockerfiles."""
        compose_file = deployment_dir / "docker-compose.yml"
        content = compose_file.read_text()
        
        # Check for Dockerfile references
        assert "Dockerfile.backend" in content or "dockerfile: Dockerfile.backend" in content, \
            "docker-compose.yml should reference Dockerfile.backend"
        assert "Dockerfile.frontend" in content or "dockerfile: Dockerfile.frontend" in content, \
            "docker-compose.yml should reference Dockerfile.frontend"

    def test_docker_compose_service_names(self, deployment_dir):
        """Verify docker-compose.yml defines backend and frontend services."""
        compose_file = deployment_dir / "docker-compose.yml"
        content = compose_file.read_text()
        
        # Check for service definitions
        assert "backend:" in content or "  backend:" in content, \
            "docker-compose.yml should define backend service"
        assert "frontend:" in content or "  frontend:" in content, \
            "docker-compose.yml should define frontend service"


class TestNpmPackageDependencies:
    """Test npm package dependencies that require native compilation."""

    def test_frontend_package_json_has_native_dependencies(self, repo_root):
        """Verify frontend package.json includes packages requiring native build tools."""
        import json
        
        package_json = repo_root / "frontend" / "package.json"
        data = json.loads(package_json.read_text())
        
        dev_deps = data.get("devDependencies", {})
        
        # These packages require native compilation and necessitate build tools
        native_packages = ["@vitest/coverage-v8", "jsdom"]
        
        for package in native_packages:
            assert package in dev_deps, \
                f"{package} not found (requires python3/make/g++ for npm ci)"

    def test_vite_dependency_exists(self, repo_root):
        """Verify Vite is included (uses esbuild which may need native compilation)."""
        import json
        
        package_json = repo_root / "frontend" / "package.json"
        data = json.loads(package_json.read_text())
        
        dev_deps = data.get("devDependencies", {})
        assert "vite" in dev_deps, "vite dependency not found"


class TestDockerBuildOptimization:
    """Test Docker build optimization strategies."""

    def test_frontend_dockerfile_layer_caching(self, deployment_dir):
        """Verify frontend Dockerfile uses layer caching optimization."""
        dockerfile = deployment_dir / "Dockerfile.frontend"
        content = dockerfile.read_text()
        
        # Find the position of package file copy and npm ci
        package_copy_pos = content.find("COPY frontend/package")
        npm_ci_pos = content.find("RUN npm ci")
        source_copy_pos = content.find("COPY frontend/ /app/")
        
        # Package files should be copied before source code
        assert package_copy_pos > 0, "Missing package.json copy"
        assert npm_ci_pos > 0, "Missing npm ci command"
        assert source_copy_pos > 0, "Missing source code copy"
        
        # Verify correct order for layer caching
        assert package_copy_pos < npm_ci_pos < source_copy_pos, \
            "Incorrect Dockerfile layer order (should be: COPY package.json, RUN npm ci, COPY source)"

    def test_backend_dockerfile_layer_caching(self, deployment_dir):
        """Verify backend Dockerfile uses layer caching optimization."""
        dockerfile = deployment_dir / "Dockerfile.backend"
        content = dockerfile.read_text()
        
        # Find the position of pyproject copy and pip install
        pyproject_copy_pos = content.find("COPY backend/pyproject.toml")
        pip_install_pos = content.find("pip install")
        app_copy_pos = content.find("COPY backend/app")
        
        # pyproject.toml should be copied before app source
        assert pyproject_copy_pos > 0, "Missing pyproject.toml copy"
        assert pip_install_pos > 0, "Missing pip install command"
        assert app_copy_pos > 0, "Missing app source copy"
        
        # Verify correct order for layer caching
        assert pyproject_copy_pos < pip_install_pos < app_copy_pos, \
            "Incorrect Dockerfile layer order (should be: COPY pyproject.toml, pip install, COPY app)"

    def test_frontend_final_image_is_lightweight(self, deployment_dir):
        """Verify frontend final stage uses nginx:alpine (lightweight)."""
        dockerfile = deployment_dir / "Dockerfile.frontend"
        content = dockerfile.read_text()
        
        # Final production image should be nginx:alpine (not nginx:latest which is larger)
        assert "FROM nginx:alpine" in content, \
            "Final stage should use nginx:alpine for minimal image size"
        
        # Build tools should NOT be in the final image
        lines_after_nginx = content.split("FROM nginx:alpine", 1)[1]
        assert "apk add" not in lines_after_nginx, \
            "Build tools should not be installed in final nginx stage"
