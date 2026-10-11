#!/bin/sh
set -e

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Seed database if needed
if [ -f "app/seed.py" ]; then
    echo "Seeding database..."
    python -m app.seed 2>/dev/null || echo "Database already seeded"
fi

# Execute the main command
exec "$@"
