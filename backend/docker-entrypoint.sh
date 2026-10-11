#!/bin/sh
set -e

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Run seed data (idempotent)
echo "Seeding database..."
python3 -m app.seed

# Execute the command passed to the container
exec "$@"
