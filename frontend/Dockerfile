# Build stage
FROM node:22-alpine as builder

WORKDIR /app/frontend

# Copy package files (relative to repository root)
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm ci

# Copy application files (relative to repository root)
COPY frontend/ .

# Build the application
RUN npm run build

# Runtime stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/frontend/dist /usr/share/nginx/html

# Copy nginx configuration template (relative to repository root)
COPY frontend/nginx.conf.template /etc/nginx/templates/default.conf.template

# Set backend host (can be overridden)
ARG BACKEND_HOST=backend
ENV BACKEND_HOST=${BACKEND_HOST}

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
