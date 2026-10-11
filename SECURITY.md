# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Smart Shop, please report it by emailing security@smartshop.example.com. Do not create a public GitHub issue.

## Security Updates

### 2026-10-11: Security Remediation (Phase 4 - Epic 1)

#### Critical Fixes

1. **JWT Secret Security**
   - **Issue**: Weak default JWT secret allowed authentication bypass
   - **Fix**: 
     - Removed all hardcoded JWT secrets from code
     - Implemented startup validation requiring JWT_SECRET environment variable
     - Enforced minimum 32-character length requirement
     - Added validation to reject known weak secrets
   - **Impact**: Prevents authentication bypass and token forgery attacks
   - **Affected Files**: `backend/app/config.py`, `deployment/docker-compose.yml`, `docker-compose.yml`

2. **Hardcoded Secrets in Docker Compose**
   - **Issue**: JWT secrets hardcoded in docker-compose files exposed in version control
   - **Fix**: 
     - Changed to environment variable substitution with required validation
     - Created `.env.example` templates for secure secret generation
     - Updated documentation with secret generation instructions
   - **Impact**: Prevents secret exposure in Git history and enables proper secret rotation
   - **Affected Files**: `deployment/docker-compose.yml`, `docker-compose.yml`, `.env.example`, `deployment/.env.example`

3. **Vulnerable npm Dependencies (react-router-dom)**
   - **Issue**: react-router-dom 6.28.0 contained CVE-2025-68470 (open redirect) and constructor injection vulnerabilities
   - **Fix**: Upgraded to react-router-dom 7.18.4
   - **Impact**: Prevents open redirect phishing attacks and prototype pollution
   - **Affected Files**: `frontend/package.json`

#### High Priority Fixes

1. **Rate Limiting on Authentication Endpoints**
   - **Issue**: Missing rate limiting allowed unlimited brute force attempts
   - **Fix**: 
     - Implemented in-memory rate limiting middleware
     - Login: 5 attempts per minute
     - Register: 3 attempts per hour
     - Discount validation: 10 attempts per minute
   - **Impact**: Prevents brute force password attacks and account enumeration
   - **Affected Files**: `backend/app/middleware/rate_limit.py`, `backend/app/main.py`

2. **Security Headers**
   - **Issue**: Missing modern security headers reduced defense-in-depth
   - **Fix**: Added to nginx configuration:
     - Content-Security-Policy (CSP)
     - Permissions-Policy
     - Referrer-Policy
     - Prepared HSTS for HTTPS deployment
   - **Impact**: Provides additional XSS protection and restricts browser capabilities
   - **Affected Files**: `deployment/nginx.conf.template`

## Security Best Practices

### JWT Secret Management

**Never use default or weak secrets in production.** Generate strong secrets with:

```bash
openssl rand -base64 32
```

Set via environment variable:
```bash
export JWT_SECRET="<generated-secret>"
```

Or create a `.env` file:
```bash
echo "JWT_SECRET=$(openssl rand -base64 32)" > .env
```

**Important**: 
- Secrets must be at least 32 characters long
- Never commit `.env` files to version control
- Rotate secrets regularly (at least annually)
- Use secrets management tools in production (AWS Secrets Manager, HashiCorp Vault, etc.)

### Rate Limiting

Current rate limits:
- `/api/auth/login`: 5 requests per minute per IP
- `/api/auth/register`: 3 requests per hour per IP
- `/api/discounts/validate`: 10 requests per minute per IP

For production, consider Redis-based rate limiting with `slowapi` or similar for distributed deployments.

### Authentication

- Passwords require: uppercase, lowercase, digits (8+ characters)
- JWT tokens expire after 24 hours (configurable via `JWT_EXPIRATION_HOURS`)
- Inactive accounts are rejected at login
- Failed logins use generic error messages to prevent user enumeration

### HTTPS/TLS

**Production deployments MUST use HTTPS.** To enable HSTS in nginx:

1. Obtain SSL/TLS certificates (Let's Encrypt, AWS Certificate Manager, etc.)
2. Configure nginx for HTTPS
3. Uncomment the HSTS header in `deployment/nginx.conf.template`:
   ```nginx
   add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
   ```

### Content Security Policy

The default CSP allows:
- Scripts/styles from same origin only
- Images from self, data URIs, and HTTPS sources
- API connections to the backend only

Adjust `deployment/nginx.conf.template` if you need to allow additional sources (CDNs, analytics, etc.).

## Dependency Security

### Backend (Python)

Scan for vulnerabilities:
```bash
cd backend
pip install pip-audit
pip-audit
```

### Frontend (npm)

Scan for vulnerabilities:
```bash
cd frontend
npm audit
npm audit fix  # Apply automatic fixes
```

### CI/CD Integration

Add to `.github/workflows/ci.yml`:
```yaml
- name: Security scan (backend)
  run: pip install pip-audit && pip-audit

- name: Security scan (frontend)
  working-directory: frontend
  run: npm audit --audit-level=high
```

## Known Limitations

### Current Implementation

1. **Rate Limiting**: Uses in-memory storage (not suitable for multi-instance deployments)
   - **Production recommendation**: Use Redis-based rate limiting
   
2. **JWT Token Storage**: Tokens stored in browser localStorage
   - **Risk**: Vulnerable to XSS attacks
   - **Future improvement**: Migrate to httpOnly cookies with CSRF protection

3. **Password Policy**: Does not require special characters
   - **Current**: uppercase, lowercase, digits (8+ min)
   - **Future improvement**: Add special character requirement

### Medium Priority Improvements (Planned)

- Implement CSRF protection for cookie-based authentication
- Migrate to httpOnly cookies for token storage
- Add special character requirement to password policy
- Implement constant-time response for discount code validation
- Add application-level security event logging

## Compliance

### Current Status

- ✅ OWASP Top 10 2021: 60% compliant (6/10 categories)
- ⚠️ PCI-DSS: Not compliant (requires Critical/High fixes + additional controls)
- ⚠️ GDPR: Partial compliance (requires audit logging, data retention policies)
- ⚠️ SOC 2: Not compliant (requires security monitoring, incident response)

### Production Deployment Requirements

Before deploying to production:

1. ✅ Generate and set strong JWT_SECRET (completed)
2. ✅ Update all vulnerable dependencies (completed)
3. ✅ Enable rate limiting (completed)
4. ✅ Configure security headers (completed)
5. ⬜ Enable HTTPS/TLS with valid certificates
6. ⬜ Implement security event logging
7. ⬜ Set up vulnerability scanning in CI/CD
8. ⬜ Conduct penetration testing
9. ⬜ Implement backup and disaster recovery
10. ⬜ Document incident response procedures

## Security Testing

### Manual Testing

Test authentication security:
```bash
# Test rate limiting (should fail after 5 attempts)
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"wrong"}'
  sleep 1
done
```

### Automated Scanning

Use OWASP ZAP or similar:
```bash
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://localhost
```

## Contact

For security concerns, contact: security@smartshop.example.com

**Last Updated**: 2026-10-11
