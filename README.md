# Smart Shop

A unified digital commerce platform for curated retail operations that enables shoppers to discover products quickly, buy confidently, and manage orders with minimal friction while giving internal teams strong operational control.

## Features

Smart Shop provides comprehensive e-commerce capabilities across the following domains:

### Customer-Facing Features
- **Product Catalog** - Browse, search, and filter products across 50+ categories with 100+ products
- **Shopping Cart** - Add items, update quantities, apply promo codes, view order summary
- **Checkout** - Multi-step checkout flow with address, payment, and order review
- **Orders** - View order history, track order status, access order details
- **Product Reviews** - Submit reviews, view ratings, helpful vote mechanism

### Admin Features
- **Inventory Management** - Track stock levels, warehouse locations, reorder thresholds, supplier information
- **Promotions** - Create percentage discounts, fixed discounts, free shipping offers with date ranges and usage limits
- **Review Moderation** - Approve/reject customer reviews, manage product feedback
- **Order Management** - View and update order status, manage customer orders
- **Dashboard** - Real-time stats, low-stock alerts, recent orders overview

### Security & Compliance
- JWT-based authentication with bcrypt password hashing (cost factor 12)
- Role-based access control (admin, inventory_manager, customer_support, customer)
- Rate limiting on authentication endpoints
- Audit logging for operational changes
- GDPR compliance controls with PII masking and soft-delete

## Tech Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy (sync)
- **Validation:** Pydantic
- **Authentication:** PyJWT + bcrypt
- **Migrations:** Alembic
- **Testing:** pytest

### Frontend
- **Language:** TypeScript
- **Framework:** React 18+
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Routing:** React Router v6
- **Testing:** vitest

### Database
- **Development:** SQLite (default, zero-config)
- **Production:** PostgreSQL (via DATABASE_URL)

## Prerequisites

Before running Smart Shop, ensure you have the following installed:

- **Python 3.10+** (Python 3.11+ recommended)
- **Node.js 18+**
- **pip** (Python package installer)
- **npm** (Node package manager)

## Installation

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd smart-shop
   ```

2. **Run the startup script:**
   ```bash
   # macOS/Linux/Git Bash
   ./start.sh

   # Windows (Command Prompt or PowerShell)
   start.bat
   ```

The startup script automatically:
- Checks prerequisites (Python 3.10+, Node.js 18+)
- Creates Python virtual environment (`.venv`)
- Installs backend dependencies
- Installs frontend dependencies
- Creates working `.env` from `dev.env` if needed
- Initializes SQLite database at `storage/app.db`
- Runs database migrations
- Seeds sample data (100+ products, default admin user)
- Detects available ports (defaults: 9000 backend, 5173 frontend)
- Starts backend (uvicorn) and frontend (Vite dev server)
- Prints access URLs and default credentials

## Access URLs

After running the startup script, access the application at:

- **Frontend (Shopper):** http://localhost:5173
- **Admin Dashboard:** http://localhost:5173/admin/dashboard
- **Backend API:** http://localhost:9000
- **API Documentation (Swagger):** http://localhost:9000/docs
- **API Documentation (ReDoc):** http://localhost:9000/redoc

## Default Credentials

For development and testing, use these credentials:

- **Email:** `admin@example.com`
- **Password:** `admin123`

⚠️ **Important:** Change these credentials in production environments.

## Environment Variables

### Backend Configuration

The backend reads configuration from `backend/.env`. A working `backend/dev.env` is provided for local development.

**Available Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./storage/app.db` |
| `SECRET_KEY` | JWT signing key (change in production!) | `dev-secret-key-change-in-production` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time in minutes | `10080` (7 days) |
| `CORS_ORIGINS` | Comma-separated allowed CORS origins | `http://localhost:5173,http://localhost:3000` |
| `API_BASE_PATH` | API route prefix | `/api/v1` |
| `DEBUG` | Enable debug mode | `true` |
| `API_PORT` | Backend server port | `9000` |

**Example `.env` file:**
```bash
DATABASE_URL=sqlite:///./storage/app.db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
DEBUG=true
API_PORT=9000
```

### Frontend Configuration

The frontend reads configuration from `frontend/.env`.

**Available Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL (optional, uses relative `/api` if not set) | `/api` |

**Note:** The startup script automatically configures `VITE_API_URL` based on the detected backend port.

## Local Development

### Starting Services

Use the provided startup scripts:

```bash
# macOS/Linux/Git Bash
./start.sh

# Windows
start.bat
```

### Stopping Services

```bash
# macOS/Linux/Git Bash
./stop.sh

# Windows
stop.bat
```

The stop scripts gracefully terminate all services using saved process IDs.

### Manual Development

If you prefer to run services manually:

**Backend:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install .
alembic upgrade head
python3 -m app.seed
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Testing

### Backend Tests

Run the backend test suite with pytest:

```bash
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pytest tests/
```

**With coverage report:**
```bash
pytest tests/ --cov=app --cov-report=term
```

**Test coverage includes:**
- Authentication (login, JWT validation, RBAC)
- Catalog (search, filtering, category navigation)
- Cart (add/update/remove, stock validation)
- Checkout (promotion validation, inventory checks, idempotency)
- Orders (creation, history, authorization)
- Inventory (stock updates, oversell prevention)
- Promotions (eligibility validation, usage limits)

### Frontend Tests

Run the frontend test suite with vitest:

```bash
cd frontend
npm run test
```

**Test coverage includes:**
- LoginPage (form submission, auth integration)
- HomePage (category grid, product grid)
- ProductDetailPage (add to cart)
- CartPage (quantity updates, item removal)
- RequireAuth (route protection)
- api-client (401 handling, token attachment)

## Deployment

### Docker Compose (Recommended)

Smart Shop includes production-ready Docker configuration.

**Development/Preview (SQLite):**
```bash
docker compose up --build
```

Access at: http://localhost:80

**Production (PostgreSQL):**
```bash
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up --build
```

**What's included:**
- Backend service with Python 3.11 + FastAPI
- Frontend service with nginx serving static assets
- Automatic database migrations on startup
- Health checks and service dependencies
- Volume persistence for SQLite database
- Optional PostgreSQL database service

### Production Environment

Before deploying to production:

1. **Set secure environment variables:**
   ```bash
   DATABASE_URL=postgresql+psycopg://user:password@host:5432/smartshop
   SECRET_KEY=<generate-random-32-char-string>
   CORS_ORIGINS=https://yourdomain.com
   DEBUG=false
   ```

2. **Generate secure secret key:**
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Configure PostgreSQL:**
   - Use the optional `docker-compose.postgres.yml` override
   - Or configure an external PostgreSQL instance

4. **Enable HTTPS/TLS:**
   - Use a reverse proxy (nginx, Caddy, Traefik)
   - Enforce TLS 1.2 or higher

5. **Configure backups:**
   - Schedule daily database backups
   - Store backups in secure, offsite location
   - Test restoration procedures

## Troubleshooting

### Port Conflicts

**Problem:** Default ports (9000, 5173) are already in use.

**Solution:** The startup script automatically detects available ports and updates configuration. If you need specific ports, stop conflicting services or modify `shared_config.json` before starting.

```bash
# Check what's using a port (Linux/macOS)
lsof -i :9000

# Check what's using a port (Windows)
netstat -ano | findstr :9000
```

### Prerequisites Not Installed

**Problem:** `python3` or `node` command not found.

**Solution:** Install the required versions:
- **Python 3.10+**: https://www.python.org/downloads/
- **Node.js 18+**: https://nodejs.org/

Verify installation:
```bash
python3 --version  # Should be 3.10+
node --version     # Should be 18+
```

### Database Issues

**Problem:** Database connection errors or schema issues.

**Solution:**
1. Stop the application
2. Delete the database file: `rm storage/app.db` (Linux/macOS) or `del storage\app.db` (Windows)
3. Restart with `./start.sh` - the database will be recreated with fresh data

**Problem:** Migration conflicts.

**Solution:**
```bash
cd backend
source .venv/bin/activate
alembic downgrade base
alembic upgrade head
```

### Backend Won't Start

**Problem:** Import errors or dependency issues.

**Solution:**
```bash
cd backend
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .
```

### Frontend Build Errors

**Problem:** TypeScript errors or missing modules.

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Docker Issues

**Problem:** Container build failures.

**Solution:**
```bash
# Clean Docker build cache
docker compose down -v
docker system prune -a
docker compose up --build
```

**Problem:** Permission errors in container.

**Solution:** Ensure volume directories have correct permissions:
```bash
mkdir -p storage
chmod 755 storage
```

## Project Structure

```
smart-shop/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # Database connection
│   │   ├── dependencies.py    # Dependency injection
│   │   ├── seed.py            # Database seeding
│   │   ├── auth/              # Authentication & authorization
│   │   ├── audit/             # Audit logging
│   │   ├── middleware/        # Rate limiting, etc.
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── privacy/           # GDPR compliance
│   │   ├── routes/            # API route handlers
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   └── services/          # Business logic layer
│   ├── tests/                 # Backend test suite
│   ├── alembic/               # Database migrations
│   ├── pyproject.toml         # Python dependencies
│   ├── dev.env                # Working local config
│   ├── Dockerfile             # Backend container image
│   └── docker-entrypoint.sh   # Container startup script
├── frontend/                   # React TypeScript frontend
│   ├── src/
│   │   ├── main.tsx           # Application entry point
│   │   ├── App.tsx            # Root component with routing
│   │   ├── index.css          # Tailwind CSS entry
│   │   ├── components/        # Reusable UI components
│   │   ├── lib/               # Utilities, API client, auth context
│   │   ├── pages/             # Page components (shopper + admin)
│   │   ├── services/          # API service layer
│   │   └── types/             # TypeScript interfaces
│   ├── tests/                 # Frontend test suite
│   ├── package.json           # Node dependencies
│   ├── vite.config.ts         # Vite configuration
│   ├── tailwind.config.js     # Tailwind design system
│   ├── Dockerfile             # Frontend container image
│   └── nginx.conf.template    # nginx reverse proxy config
├── storage/                    # Database and file storage
│   └── app.db                 # SQLite database (gitignored)
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI pipeline
├── shared_config.json         # Shared configuration contract
├── docker-compose.yml         # Container orchestration (SQLite)
├── docker-compose.postgres.yml # PostgreSQL override (production)
├── start.sh                   # Startup script (Unix/Git Bash)
├── stop.sh                    # Shutdown script (Unix/Git Bash)
├── start.bat                  # Startup script (Windows, generated)
├── stop.bat                   # Shutdown script (Windows, generated)
├── .gitignore                 # Git exclusions
└── README.md                  # This file
```

## API Documentation

Once the backend is running, explore the API at:

- **Swagger UI:** http://localhost:9000/docs
- **ReDoc:** http://localhost:9000/redoc

**API Endpoints:**

All endpoints are mounted under `/api/v1` prefix:

- **Authentication:** `POST /api/v1/auth/login`
- **Catalog:** `GET /api/v1/catalog/categories`, `GET /api/v1/catalog/products`, `GET /api/v1/catalog/search`
- **Cart:** `GET /api/v1/cart`, `POST /api/v1/cart`, `PATCH /api/v1/cart/{item_id}`, `DELETE /api/v1/cart/{item_id}`
- **Checkout:** `POST /api/v1/checkout/validate`, `POST /api/v1/checkout/submit`
- **Orders:** `GET /api/v1/orders`, `GET /api/v1/orders/{order_id}`
- **Admin:** `GET /api/v1/admin/dashboard`, `PATCH /api/v1/admin/orders/{order_id}`, `PATCH /api/v1/admin/reviews/{review_id}`
- **Inventory:** `GET /api/v1/inventory`, `POST /api/v1/inventory/adjust`
- **Promotions:** `GET /api/v1/promotions`, `POST /api/v1/promotions`
- **Reviews:** `GET /api/v1/reviews/product/{product_id}`, `POST /api/v1/reviews`

## License

Copyright © 2024 Smart Shop. All rights reserved.
