# Smart Shop Deployment Guide

This document provides production deployment guidance, security configuration, and operational checklist for Smart Shop.

## Table of Contents

- [Production Deployment](#production-deployment)
- [Environment Configuration](#environment-configuration)
- [Security Checklist](#security-checklist)
- [Database Configuration](#database-configuration)
- [Performance Tuning](#performance-tuning)
- [Monitoring and Logging](#monitoring-and-logging)
- [Backup and Recovery](#backup-and-recovery)
- [Health Checks](#health-checks)

---

## Production Deployment

### Docker Compose (Recommended)

**For SQLite (Preview/Small-Scale):**
```bash
docker compose up --build -d
```

**For PostgreSQL (Production):**
```bash
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up --build -d
```

### Frontend Preview Port
The frontend service includes `x-preview-port: 80` for preview environments. Ensure the deployment routes traffic to port 80 on the frontend container.

### Container Architecture
- **Backend**: Python 3.11 with FastAPI, runs migrations on startup via `docker-entrypoint.sh`
- **Frontend**: Nginx serving static assets with `/api` proxy to backend
- **Database**: SQLite by default (data volume at `/data`), PostgreSQL optional override

---

## Environment Configuration

### Critical Environment Variables

All services require proper environment configuration. Never use development defaults in production.

#### Backend Environment Variables

| Variable | Required | Default (Dev) | Production Value |
|----------|----------|---------------|------------------|
| `DATABASE_URL` | Yes | `sqlite:///./storage/app.db` | `postgresql+psycopg://user:pass@host:5432/dbname` |
| `SECRET_KEY` | **Yes** | `dev-secret-key-change-in-production` | **Generate random 32+ character string** |
| `CORS_ORIGINS` | Yes | `http://localhost:5173,http://localhost:5174` | `https://yourdomain.com,https://www.yourdomain.com` |
| `DEBUG` | No | `true` | `false` |
| `API_BASE_PATH` | No | `/api/v1` | `/api/v1` (or custom) |
| `JWT_ALGORITHM` | No | `HS256` | `HS256` |
| `JWT_EXPIRATION_MINUTES` | No | `1440` | `30` (or as required) |

**Generate SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Frontend Environment Variables

| Variable | Required | Default (Dev) | Production Value |
|----------|----------|---------------|------------------|
| `VITE_API_URL` | No | `/api` | `/api` (relative, proxied by nginx) |

**Note**: Frontend uses relative `/api` paths by default. The nginx template proxies `/api/*` to the backend service.

---

## Security Checklist

### Pre-Deployment Security Verification

- [ ] **SECRET_KEY**: Change from default value to cryptographically random string (32+ characters)
- [ ] **DATABASE_URL**: Update to production PostgreSQL connection string with strong password
- [ ] **CORS_ORIGINS**: Set to production domain(s) only (remove `localhost` origins)
- [ ] **DEBUG**: Set to `false` in production
- [ ] **JWT_EXPIRATION**: Reduce from 1440 minutes to 30 minutes (or as required)
- [ ] **Default Credentials**: Disable or remove `admin@example.com / admin123` after creating real admin accounts
- [ ] **TLS/SSL**: Enable HTTPS with TLS 1.2+ on all public-facing services
- [ ] **Security Headers**: Verify headers present (see Health Checks section)
- [ ] **Dependency Scan**: Run `npm audit` and `pip-audit` to verify zero critical/high vulnerabilities
- [ ] **Rate Limiting**: Confirm rate limiting active on `/api/v1/auth/login` (5 attempts/15 minutes)
- [ ] **Firewall**: Restrict database port access to backend service only

### Security Headers (Configured)

The backend includes the following security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

Frontend nginx template includes:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

**Verify headers:**
```bash
curl -I https://yourdomain.com/api/v1/products | grep -E "X-Content-Type|X-Frame|X-XSS"
```

---

## Database Configuration

### SQLite (Development/Preview)

**Location**: `/data/app.db` inside container, persisted via named volume

**Configuration**:
```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - DATABASE_URL=sqlite:////data/app.db
    volumes:
      - data:/data
volumes:
  data:
```

**Limitations**: Single-writer, no horizontal scaling, file locking issues under high concurrency

### PostgreSQL (Production Recommended)

**Configuration**:
```yaml
# docker-compose.postgres.yml override
services:
  database:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: smartshop
      POSTGRES_PASSWORD: <STRONG_PASSWORD>
      POSTGRES_DB: smartshop
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U smartshop"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      args:
        PIP_TARGET: ".[postgres]"
    environment:
      - DATABASE_URL=postgresql+psycopg://smartshop:<PASSWORD>@database:5432/smartshop
    depends_on:
      database:
        condition: service_healthy

volumes:
  pgdata:
```

**Deploy**:
```bash
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up --build -d
```

### Database Indexes (Configured)

High-traffic columns have indexes:
- `users.email` (unique)
- `products.sku` (unique)
- `orders.customer_id`
- `reviews.product_id`
- `inventory.product_id`

**Verify indexes in PostgreSQL**:
```sql
\d products
-- Should show: ix_products_sku index on sku column
```

**Verify query uses index**:
```sql
EXPLAIN QUERY PLAN SELECT * FROM products WHERE sku = 'TEST-SKU';
-- Should show: SEARCH using index ix_products_sku
```

### Migrations

Migrations run automatically on backend container startup via `docker-entrypoint.sh`:
```bash
alembic upgrade head
```

**Manual migration** (if needed):
```bash
docker compose exec backend alembic upgrade head
```

---

## Performance Tuning

### Target Performance Metrics

Based on requirements:
- **Shopper page load**: ≤ 2.5 seconds p95
- **API response times**: ≤ 500ms p95, ≤ 1000ms p99 for core endpoints
- **Checkout validation**: ≤ 750ms p95

### Backend Performance

**Uvicorn workers** (adjust based on CPU cores):
```yaml
# docker-compose.yml
services:
  backend:
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000", "--workers", "4"]
```

**Database connection pooling** (for PostgreSQL):
```python
# app/database.py
engine = create_engine(
    settings.database_url,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)
```

### Frontend Performance

**Nginx caching** (already configured in `nginx.conf.template`):
- Static assets (JS/CSS/images): `Cache-Control: public, max-age=31536000` (1 year)
- HTML: `Cache-Control: no-cache` (revalidate)

**Nginx gzip compression** (add to template if needed):
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
gzip_min_length 1000;
```

### Load Testing

**Test API response times**:
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:9000/api/v1/products

# Using wrk
wrk -t4 -c100 -d30s http://localhost:9000/api/v1/products
```

**Monitor metrics**:
- Requests per second (RPS)
- p50, p95, p99 latency
- Error rate

---

## Monitoring and Logging

### Structured Logging

Backend logs to **stdout in JSON format** for easy ingestion by log aggregators (e.g., ELK, CloudWatch, Datadog).

**Log format** (configured):
```json
{
  "timestamp": "2026-10-11T05:46:27.123Z",
  "level": "INFO",
  "message": "Order created",
  "order_id": 12345,
  "customer_id": 67890,
  "total": 299.99
}
```

**View logs**:
```bash
docker compose logs -f backend
docker compose logs -f frontend
```

### Health Checks

**Backend health check** (configured in `docker-compose.yml`):
```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -f http://localhost:9000/api/v1/catalog/categories || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**Manual health check**:
```bash
curl http://localhost:9000/api/v1/catalog/categories
# Should return 200 OK with category list
```

### Application Metrics

Consider integrating:
- **Prometheus** for metrics collection
- **Grafana** for visualization
- **Sentry** for error tracking

Key metrics to monitor:
- Request count and rate
- Response time percentiles (p50, p95, p99)
- Error rate by endpoint
- Database query performance
- Authentication failures
- Cart abandonment rate
- Order completion rate

---

## Backup and Recovery

### Recovery Objectives

- **RTO (Recovery Time Objective)**: 60 minutes
- **RPO (Recovery Point Objective)**: 15 minutes

### Database Backup Strategy

#### SQLite Backup

**Automated daily backup script**:
```bash
#!/bin/bash
# backup-sqlite.sh
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker compose exec backend sqlite3 /data/app.db ".backup /data/backup_${TIMESTAMP}.db"
docker compose cp backend:/data/backup_${TIMESTAMP}.db ${BACKUP_DIR}/
# Retain backups for 30 days
find ${BACKUP_DIR} -name "backup_*.db" -mtime +30 -delete
```

**Schedule with cron**:
```bash
0 2 * * * /path/to/backup-sqlite.sh
```

#### PostgreSQL Backup

**Automated daily backup**:
```bash
#!/bin/bash
# backup-postgres.sh
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker compose exec database pg_dump -U smartshop smartshop > ${BACKUP_DIR}/smartshop_${TIMESTAMP}.sql
gzip ${BACKUP_DIR}/smartshop_${TIMESTAMP}.sql
# Retain backups for 30 days
find ${BACKUP_DIR} -name "smartshop_*.sql.gz" -mtime +30 -delete
```

**Schedule with cron**:
```bash
0 2 * * * /path/to/backup-postgres.sh
```

### Restore Procedures

#### SQLite Restore

```bash
docker compose down
docker compose cp backup_TIMESTAMP.db backend:/data/app.db
docker compose up -d
```

#### PostgreSQL Restore

```bash
docker compose down
docker compose up database -d
# Wait for database to be ready
gunzip -c smartshop_TIMESTAMP.sql.gz | docker compose exec -T database psql -U smartshop smartshop
docker compose up -d
```

### Disaster Recovery Checklist

- [ ] Verify backups stored in separate physical location or cloud storage
- [ ] Test restore procedure monthly
- [ ] Document restore runbook with step-by-step instructions
- [ ] Maintain backup retention policy (30 days recommended)
- [ ] Monitor backup success/failure notifications

---

## Production Deployment Checklist

Use this checklist before launching to production:

### Infrastructure
- [ ] Deploy with PostgreSQL (not SQLite) for production workloads
- [ ] Configure TLS/SSL certificates (Let's Encrypt or purchased)
- [ ] Enable HTTPS on all services
- [ ] Set up firewall rules (allow only 80/443, block database port from public)
- [ ] Configure load balancer (if horizontal scaling required)
- [ ] Set up CDN for static assets (optional, for performance)

### Configuration
- [ ] Generate and set random `SECRET_KEY` (32+ characters)
- [ ] Update `DATABASE_URL` to production PostgreSQL connection string
- [ ] Set `CORS_ORIGINS` to production domain(s) only
- [ ] Set `DEBUG=false`
- [ ] Reduce `JWT_EXPIRATION_MINUTES` to 30 (or as required)
- [ ] Verify no default credentials in use or disable `admin@example.com / admin123`

### Security
- [ ] Run `npm audit` and `pip-audit`: verify zero critical/high vulnerabilities
- [ ] Verify security headers present: `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`
- [ ] Verify CORS allows only production origins (no wildcard `*`)
- [ ] Verify rate limiting active on login endpoint (5 attempts/15 min)
- [ ] Review and remove any debug endpoints or development-only routes
- [ ] Ensure passwords hashed with bcrypt cost factor ≥12

### Database
- [ ] Run `alembic upgrade head` to apply all migrations
- [ ] Verify database indexes present on high-traffic columns
- [ ] Test query performance with `EXPLAIN QUERY PLAN` (SQLite) or `EXPLAIN ANALYZE` (PostgreSQL)
- [ ] Configure database connection pooling (PostgreSQL)
- [ ] Set up automated daily backups

### Performance
- [ ] Load test API endpoints: verify p95 ≤ 500ms for core endpoints
- [ ] Load test checkout validation: verify p95 ≤ 750ms
- [ ] Test frontend page load: verify ≤ 3 seconds p95 under simulated 3G
- [ ] Configure uvicorn workers based on CPU cores (4+ recommended)
- [ ] Enable nginx gzip compression for text/JSON responses

### Monitoring
- [ ] Configure centralized logging (ELK, CloudWatch, Datadog, etc.)
- [ ] Set up health check monitoring (Pingdom, UptimeRobot, etc.)
- [ ] Configure error tracking (Sentry, Rollbar, etc.)
- [ ] Set up application metrics (Prometheus + Grafana)
- [ ] Create alerting rules for critical errors and performance degradation

### Backup & Recovery
- [ ] Configure automated daily database backups
- [ ] Store backups in separate location (cloud storage, offsite)
- [ ] Test restore procedure
- [ ] Document disaster recovery runbook
- [ ] Verify backup retention policy (30 days recommended)

### Accessibility
- [ ] Run axe DevTools scan on key pages: verify zero critical, zero serious violations
- [ ] Test keyboard navigation on all forms
- [ ] Verify ARIA labels on interactive elements
- [ ] Test screen reader compatibility

### Documentation
- [ ] Update README.md with production URLs
- [ ] Document deployment procedure
- [ ] Document rollback procedure
- [ ] Create operational runbook with common tasks and troubleshooting
- [ ] Document API endpoints and authentication

### Post-Deployment
- [ ] Smoke test all critical user flows: browse, add to cart, checkout, view orders
- [ ] Verify admin dashboard accessible with production credentials
- [ ] Monitor error logs for first 24 hours
- [ ] Verify backups running successfully
- [ ] Test disaster recovery procedure within 7 days

---

## Troubleshooting

### Common Production Issues

**High database latency:**
- Check connection pool size (increase if exhausted)
- Verify indexes on queried columns: `EXPLAIN QUERY PLAN` / `EXPLAIN ANALYZE`
- Consider read replicas for read-heavy workloads

**CORS errors:**
- Verify `CORS_ORIGINS` includes exact production domain (with protocol: `https://`)
- Check browser console for specific CORS error message
- Verify preflight OPTIONS requests return correct headers

**Authentication failures:**
- Verify `SECRET_KEY` consistent across all backend instances
- Check JWT expiration setting (not too short)
- Verify system clock synchronized (JWT `exp` claim time-sensitive)

**502 Bad Gateway:**
- Check backend health: `docker compose ps`
- Verify backend listening on correct port (9000)
- Check backend logs: `docker compose logs backend`
- Verify nginx proxy configuration

**Database connection errors:**
- Verify `DATABASE_URL` correct and database accessible
- Check database container running: `docker compose ps database`
- Verify database credentials correct
- Check network connectivity between backend and database

---

## Performance Benchmarks

Expected baseline performance (local testing):
- **GET /api/v1/products**: 50-150ms (SQLite), 30-100ms (PostgreSQL)
- **GET /api/v1/cart**: 30-80ms
- **GET /api/v1/orders**: 40-100ms
- **POST /api/v1/checkout/validate**: 100-300ms (includes inventory + promotion validation)
- **POST /api/v1/auth/login**: 150-250ms (bcrypt hashing intentionally slow)

Production performance will vary based on:
- Database type and configuration
- Network latency
- Server resources (CPU, RAM)
- Concurrent user load

---

## Scaling Considerations

### Horizontal Scaling

To scale backend horizontally:
1. **Use PostgreSQL** (not SQLite) as shared database
2. **Deploy multiple backend containers** behind load balancer
3. **Ensure SECRET_KEY identical** across all instances
4. **Use external session store** if needed (Redis)
5. **Consider read replicas** for read-heavy workloads

### Vertical Scaling

To scale backend vertically:
1. **Increase uvicorn workers**: `--workers 8` (based on CPU cores)
2. **Increase database connection pool**: `pool_size=50`
3. **Allocate more container resources**: increase CPU/memory limits

### Caching Layer

Consider adding Redis for:
- Session storage
- Product catalog cache (reduce database reads)
- Cart state (alternative to database)
- Rate limiting state (shared across backend instances)

---

## Support and Maintenance

For ongoing support:
- Review application logs daily for errors
- Monitor performance metrics weekly
- Apply security updates monthly
- Review and rotate secrets quarterly
- Test disaster recovery annually

**Emergency Contacts:**
- Operations Team: [Contact Info]
- Database Administrator: [Contact Info]
- Security Team: [Contact Info]

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

**Document Version**: 1.0  
**Last Updated**: 2026-10-11  
**Maintained By**: Smart Shop Engineering Team
