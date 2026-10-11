/**
 * Integration tests for Docker build configuration
 * Verifies frontend build artifacts and configuration validity
 */

import { describe, it, expect } from 'vitest';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

describe('Docker Build Configuration', () => {
  const repoRoot = join(__dirname, '..', '..', '..');
  const deploymentDir = join(repoRoot, 'deployment');
  const frontendDir = join(repoRoot, 'frontend');

  describe('Build Dependencies', () => {
    it('should have package.json with required build dependencies', () => {
      const packageJsonPath = join(frontendDir, 'package.json');
      expect(existsSync(packageJsonPath)).toBe(true);

      const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));
      
      // Verify native dependencies that require build tools
      expect(packageJson.devDependencies).toHaveProperty('@vitest/coverage-v8');
      expect(packageJson.devDependencies).toHaveProperty('jsdom');
      expect(packageJson.devDependencies).toHaveProperty('vite');
    });

    it('should have package-lock.json for reproducible builds', () => {
      const lockfilePath = join(frontendDir, 'package-lock.json');
      expect(existsSync(lockfilePath)).toBe(true);
      
      const lockfile = readFileSync(lockfilePath, 'utf-8');
      expect(lockfile.length).toBeGreaterThan(0);
    });

    it('should specify Node.js engine version', () => {
      const packageJsonPath = join(frontendDir, 'package.json');
      const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));
      
      expect(packageJson.engines).toHaveProperty('node');
      expect(packageJson.engines.node).toMatch(/>=18/);
    });
  });

  describe('Build Scripts', () => {
    it('should have build script configured', () => {
      const packageJsonPath = join(frontendDir, 'package.json');
      const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));
      
      expect(packageJson.scripts).toHaveProperty('build');
      expect(packageJson.scripts.build).toContain('vite build');
    });

    it('should have TypeScript build step', () => {
      const packageJsonPath = join(frontendDir, 'package.json');
      const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));
      
      // Build script should include TypeScript compilation
      expect(packageJson.scripts.build).toContain('tsc');
    });

    it('should have test script for CI', () => {
      const packageJsonPath = join(frontendDir, 'package.json');
      const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));
      
      expect(packageJson.scripts).toHaveProperty('test');
      expect(packageJson.scripts.test).toContain('vitest');
    });
  });

  describe('Vite Configuration', () => {
    it('should have vite.config.ts file', () => {
      const viteConfigPath = join(frontendDir, 'vite.config.ts');
      expect(existsSync(viteConfigPath)).toBe(true);
    });

    it('should configure React plugin', () => {
      const viteConfigPath = join(frontendDir, 'vite.config.ts');
      const viteConfig = readFileSync(viteConfigPath, 'utf-8');
      
      expect(viteConfig).toContain('@vitejs/plugin-react');
      expect(viteConfig).toContain('react()');
    });
  });

  describe('TypeScript Configuration', () => {
    it('should have tsconfig.json', () => {
      const tsconfigPath = join(frontendDir, 'tsconfig.json');
      expect(existsSync(tsconfigPath)).toBe(true);
    });

    it('should have tsconfig.app.json for application code', () => {
      const tsconfigAppPath = join(frontendDir, 'tsconfig.app.json');
      expect(existsSync(tsconfigAppPath)).toBe(true);
    });

    it('should have tsconfig.node.json for build tools', () => {
      const tsconfigNodePath = join(frontendDir, 'tsconfig.node.json');
      expect(existsSync(tsconfigNodePath)).toBe(true);
    });
  });

  describe('Dockerfile Configuration', () => {
    it('should have Dockerfile.frontend in deployment directory', () => {
      const dockerfilePath = join(deploymentDir, 'Dockerfile.frontend');
      expect(existsSync(dockerfilePath)).toBe(true);
    });

    it('should use node:22-alpine base image', () => {
      const dockerfilePath = join(deploymentDir, 'Dockerfile.frontend');
      const dockerfile = readFileSync(dockerfilePath, 'utf-8');
      
      expect(dockerfile).toContain('FROM node:22-alpine');
      expect(dockerfile).not.toContain('node:22-slim');
    });

    it('should install required build dependencies', () => {
      const dockerfilePath = join(deploymentDir, 'Dockerfile.frontend');
      const dockerfile = readFileSync(dockerfilePath, 'utf-8');
      
      expect(dockerfile).toContain('python3');
      expect(dockerfile).toContain('make');
      expect(dockerfile).toContain('g++');
    });

    it('should use multi-stage build', () => {
      const dockerfilePath = join(deploymentDir, 'Dockerfile.frontend');
      const dockerfile = readFileSync(dockerfilePath, 'utf-8');
      
      expect(dockerfile).toMatch(/FROM node:22-alpine as build/);
      expect(dockerfile).toContain('FROM nginx:alpine');
      expect(dockerfile).toMatch(/COPY --from=build/);
    });

    it('should copy package files before installing dependencies', () => {
      const dockerfilePath = join(deploymentDir, 'Dockerfile.frontend');
      const dockerfile = readFileSync(dockerfilePath, 'utf-8');
      
      // Verify layer caching optimization
      const packageCopyIndex = dockerfile.indexOf('COPY frontend/package');
      const npmCiIndex = dockerfile.indexOf('RUN npm ci');
      const sourceCopyIndex = dockerfile.indexOf('COPY frontend/ /app/');
      
      expect(packageCopyIndex).toBeGreaterThan(-1);
      expect(npmCiIndex).toBeGreaterThan(packageCopyIndex);
      expect(sourceCopyIndex).toBeGreaterThan(npmCiIndex);
    });

    it('should run npm run build', () => {
      const dockerfilePath = join(deploymentDir, 'Dockerfile.frontend');
      const dockerfile = readFileSync(dockerfilePath, 'utf-8');
      
      expect(dockerfile).toContain('RUN npm run build');
    });

    it('should serve from nginx in production stage', () => {
      const dockerfilePath = join(deploymentDir, 'Dockerfile.frontend');
      const dockerfile = readFileSync(dockerfilePath, 'utf-8');
      
      expect(dockerfile).toContain('FROM nginx:alpine');
      expect(dockerfile).toMatch(/COPY --from=build .*dist.*nginx/);
    });
  });

  describe('Nginx Configuration', () => {
    it('should have nginx.conf.template in deployment directory', () => {
      const nginxConfigPath = join(deploymentDir, 'nginx.conf.template');
      expect(existsSync(nginxConfigPath)).toBe(true);
    });

    it('should configure API proxy', () => {
      const nginxConfigPath = join(deploymentDir, 'nginx.conf.template');
      const nginxConfig = readFileSync(nginxConfigPath, 'utf-8');
      
      expect(nginxConfig).toContain('location /api/');
      expect(nginxConfig).toContain('proxy_pass');
      expect(nginxConfig).toContain('${BACKEND_HOST}');
    });

    it('should configure SPA fallback', () => {
      const nginxConfigPath = join(deploymentDir, 'nginx.conf.template');
      const nginxConfig = readFileSync(nginxConfigPath, 'utf-8');
      
      expect(nginxConfig).toContain('try_files');
      expect(nginxConfig).toContain('index.html');
    });

    it('should enable gzip compression', () => {
      const nginxConfigPath = join(deploymentDir, 'nginx.conf.template');
      const nginxConfig = readFileSync(nginxConfigPath, 'utf-8');
      
      expect(nginxConfig).toContain('gzip on');
    });
  });

  describe('Build Artifacts', () => {
    it('should have index.html entry point', () => {
      const indexPath = join(frontendDir, 'index.html');
      expect(existsSync(indexPath)).toBe(true);
      
      const indexHtml = readFileSync(indexPath, 'utf-8');
      expect(indexHtml.toLowerCase()).toContain('<!doctype html>');
      expect(indexHtml).toContain('<div id="root">');
    });

    it('should have src directory with TypeScript files', () => {
      const srcDir = join(frontendDir, 'src');
      expect(existsSync(srcDir)).toBe(true);
    });
  });

  describe('.dockerignore Configuration', () => {
    it('should have .dockerignore file', () => {
      const dockerignorePath = join(deploymentDir, '.dockerignore');
      expect(existsSync(dockerignorePath)).toBe(true);
    });

    it('should exclude node_modules', () => {
      const dockerignorePath = join(deploymentDir, '.dockerignore');
      const dockerignore = readFileSync(dockerignorePath, 'utf-8');
      
      expect(dockerignore).toContain('node_modules');
    });

    it('should exclude .git directory', () => {
      const dockerignorePath = join(deploymentDir, '.dockerignore');
      const dockerignore = readFileSync(dockerignorePath, 'utf-8');
      
      expect(dockerignore).toContain('.git');
    });

    it('should exclude test coverage', () => {
      const dockerignorePath = join(deploymentDir, '.dockerignore');
      const dockerignore = readFileSync(dockerignorePath, 'utf-8');
      
      expect(dockerignore).toMatch(/coverage|\.coverage/);
    });
  });
});

describe('CI Workflow Configuration', () => {
  const repoRoot = join(__dirname, '..', '..', '..');
  const ciWorkflowPath = join(repoRoot, '.github', 'workflows', 'ci.yml');

  it('should have CI workflow file', () => {
    expect(existsSync(ciWorkflowPath)).toBe(true);
  });

  it('should include Docker build validation job', () => {
    const ciWorkflow = readFileSync(ciWorkflowPath, 'utf-8');
    
    expect(ciWorkflow).toContain('Docker Build Validation');
    expect(ciWorkflow).toContain('docker build');
  });

  it('should build frontend image with correct command', () => {
    const ciWorkflow = readFileSync(ciWorkflowPath, 'utf-8');
    
    expect(ciWorkflow).toContain('Dockerfile.frontend');
    expect(ciWorkflow).toContain('smart-shop-frontend:test');
  });

  it('should build backend image with correct command', () => {
    const ciWorkflow = readFileSync(ciWorkflowPath, 'utf-8');
    
    expect(ciWorkflow).toContain('Dockerfile.backend');
    expect(ciWorkflow).toContain('smart-shop-backend:test');
  });

  it('should run builds from deployment directory', () => {
    const ciWorkflow = readFileSync(ciWorkflowPath, 'utf-8');
    
    expect(ciWorkflow).toContain('working-directory: deployment');
  });

  it('should validate docker-compose configuration', () => {
    const ciWorkflow = readFileSync(ciWorkflowPath, 'utf-8');
    
    expect(ciWorkflow).toMatch(/docker.?compose config/);
  });

  it('should include frontend tests', () => {
    const ciWorkflow = readFileSync(ciWorkflowPath, 'utf-8');
    
    expect(ciWorkflow).toContain('Frontend Tests');
    expect(ciWorkflow).toContain('npm ci');
    expect(ciWorkflow).toContain('vitest');
  });

  it('should include backend tests', () => {
    const ciWorkflow = readFileSync(ciWorkflowPath, 'utf-8');
    
    expect(ciWorkflow).toContain('Backend Tests');
    expect(ciWorkflow).toContain('pytest');
  });
});

describe('Docker Compose Configuration', () => {
  const repoRoot = join(__dirname, '..', '..', '..');
  const deploymentDir = join(repoRoot, 'deployment');
  const dockerComposePath = join(deploymentDir, 'docker-compose.yml');

  it('should have docker-compose.yml file', () => {
    expect(existsSync(dockerComposePath)).toBe(true);
  });

  it('should define frontend service', () => {
    const dockerCompose = readFileSync(dockerComposePath, 'utf-8');
    
    expect(dockerCompose).toMatch(/frontend:/);
  });

  it('should define backend service', () => {
    const dockerCompose = readFileSync(dockerComposePath, 'utf-8');
    
    expect(dockerCompose).toMatch(/backend:/);
  });

  it('should reference correct Dockerfiles', () => {
    const dockerCompose = readFileSync(dockerComposePath, 'utf-8');
    
    expect(dockerCompose).toContain('Dockerfile.frontend');
    expect(dockerCompose).toContain('Dockerfile.backend');
  });
});
