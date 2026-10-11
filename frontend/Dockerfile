# Frontend Dockerfile for Smart Shop - Multi-stage build
# Stage 1: Build
FROM node:22 AS build

WORKDIR /app

# Copy shared config first (from repo root context)
COPY shared_config.json /app/shared_config.json

# Copy dependency files
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY frontend/ ./

# Build application
# BACKEND_HOST is provided by docker-compose at build time
ARG BACKEND_HOST=backend
ENV VITE_BACKEND_HOST=${BACKEND_HOST}

RUN npm run build

# Stage 2: Runtime with nginx
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Accept BACKEND_HOST as build arg and set as env var for template substitution
ARG BACKEND_HOST=backend
ENV BACKEND_HOST=${BACKEND_HOST}

# Copy nginx configuration template
COPY frontend/nginx.conf.template /etc/nginx/templates/default.conf.template

# Expose frontend port
EXPOSE 80

# nginx will automatically substitute env vars in templates and start
CMD ["nginx", "-g", "daemon off;"]
