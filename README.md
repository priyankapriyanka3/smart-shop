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
