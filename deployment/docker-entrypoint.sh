#!/bin/sh
# Docker entrypoint for Smart Shop backend
# Runs migrations and seeds database before starting the server

set -e

echo "Running Alembic migrations..."
alembic upgrade head

echo "Checking if database needs seeding..."
python3 -c "
from app.database import SessionLocal
from app.models import Customer

db = SessionLocal()
admin_exists = db.query(Customer).filter_by(email='admin@example.com').first()
db.close()

if not admin_exists:
    print('Database is empty, running seed script...')
    import subprocess
    subprocess.run(['python3', '-m', 'app.seed'], check=True)
else:
    print('Database already seeded, skipping.')
"

echo "Starting application..."
exec "$@"
