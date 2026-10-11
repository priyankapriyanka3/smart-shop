# Smart Shop

Smart Shop is a multi-platform shopping solution with native Android and iOS apps powered by a centralized API. It provides a seamless shopping experience with product browsing, cart, orders, authentication, payments, and inventory management.

## Repository Structure

```
smart-shop/
├── backend/           # FastAPI backend API
├── frontend/          # React + Vite frontend
├── docker-compose.yml # Docker deployment configuration
├── start.sh           # Development startup script (Unix/macOS/Windows Git Bash)
└── stop.sh            # Development shutdown script
```

## Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 18+** (for frontend)
- **Docker & Docker Compose** (for containerized deployment)

## Quick Start (Development)

### Unix/macOS/Linux
```bash
./start.sh
```

### Windows
```cmd
start.bat
```

This will:
1. Create a Python virtual environment and install backend dependencies
2. Initialize `.env` from `backend/dev.env` if not present
3. Run database migrations and seed initial data
4. Start the backend API on http://localhost:8000
5. Install frontend dependencies and start the development server on http://localhost:5173

**API Documentation**: http://localhost:8000/api/docs

## Docker Deployment

### Security Setup (Required)

**IMPORTANT**: Before running Docker, you must set a secure JWT secret:

```bash
# Generate a secure JWT secret
openssl rand -base64 32

# Set it as an environment variable
export JWT_SECRET="<paste-the-generated-secret-here>"

# Or create a .env file (recommended)
echo "JWT_SECRET=$(openssl rand -base64 32)" > .env
```

The application will refuse to start without a valid JWT_SECRET for security reasons.

### Build and Run

Build and run the full stack with Docker Compose:

```bash
docker-compose up --build
```

Services:
- **Frontend**: http://localhost (port 80)
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

The preview deployment uses SQLite on a named volume for the database.

## Default Credentials

| Role              | Email                        | Password        |
|-------------------|------------------------------|-----------------|
| Admin             | admin@example.com            | Admin123!       |
| Customer          | customer@example.com         | Customer123!    |
| Inventory Manager | inventory@example.com        | Inventory123!   |
| Customer Support  | support@example.com          | Support123!     |

## Configuration

The backend loads configuration from `backend/.env`. For local development, this file is automatically created from `backend/dev.env` by `start.sh`.

### Security Configuration

**JWT_SECRET**: A strong, randomly generated secret key for signing authentication tokens. This is REQUIRED and must be at least 32 characters long.

Generate with:
```bash
openssl rand -base64 32
```

For development, `backend/dev.env` includes a development-only secret. **Never use development secrets in production.**

For production deployment:
1. Copy `.env.example` to `.env`
2. Generate a secure JWT secret: `openssl rand -base64 32`
3. Set `JWT_SECRET` in `.env`
4. Never commit `.env` to version control

## Testing

### Backend
```bash
cd backend
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pytest
```

### Frontend
```bash
cd frontend
npm test
```

## Stopping Services

Press `Ctrl+C` in the terminal running `start.sh`, or run:
```bash
./stop.sh
```

For Docker:
```bash
docker-compose down
```
