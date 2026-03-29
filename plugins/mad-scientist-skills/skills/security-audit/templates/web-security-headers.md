# Web Security Headers Reference

HTTP security headers that every web application should set. Includes framework-specific implementation examples and testing commands.

## Purpose

Answer: "Does this application set appropriate security headers? Is transport security enforced?"

## Checklist

Before auditing, identify:

- [ ] Which web framework is used (Django, Flask, FastAPI, Express, Next.js, Streamlit)
- [ ] Whether a reverse proxy or CDN sits in front of the application (nginx, CloudFront, Cloudflare)
- [ ] Whether the application uses cookies for authentication or sessions
- [ ] Whether the application serves user-generated content or embeds third-party scripts

## Header Reference

### Content-Security-Policy (CSP)

**Purpose:** Prevents XSS by allowlisting allowed script, style, image, and frame sources.

**Minimum viable policy:**
```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'
```

**Framework examples:**

| Framework | Implementation |
|-----------|---------------|
| Django | `django-csp` middleware: `CSP_DEFAULT_SRC = ("'self'",)` |
| Flask | `flask-talisman`: `Talisman(app, content_security_policy={...})` |
| Express | `helmet`: `app.use(helmet.contentSecurityPolicy({directives: {...}}))` |
| Next.js | `next.config.js`: `headers()` returning CSP header |
| nginx | `add_header Content-Security-Policy "default-src 'self'" always;` |

**Common mistakes:**
- Using `unsafe-inline` for scripts (defeats CSP purpose) — use nonces or hashes instead
- Using `unsafe-eval` (allows `eval()`) — refactor code to avoid it
- Setting CSP in a `<meta>` tag but not as an HTTP header (meta tags don't support `frame-ancestors`)

---

### Strict-Transport-Security (HSTS)

**Purpose:** Forces the browser to always use HTTPS for the domain, preventing downgrade attacks.

**Recommended value:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

**Framework examples:**

| Framework | Implementation |
|-----------|---------------|
| Django | `SECURE_HSTS_SECONDS = 31536000`, `SECURE_HSTS_INCLUDE_SUBDOMAINS = True` |
| Flask | `flask-talisman`: `Talisman(app, strict_transport_security=True)` |
| Express | `helmet`: `app.use(helmet.hsts({maxAge: 31536000}))` |
| nginx | `add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;` |

**Common mistakes:**
- Setting `max-age=0` (disables HSTS)
- Adding `preload` before testing (difficult to undo — domain is hardcoded into browsers)
- Not including `includeSubDomains` when subdomains also serve HTTPS content

---

### X-Content-Type-Options

**Purpose:** Prevents browsers from MIME-sniffing a response away from the declared Content-Type.

**Value:** `X-Content-Type-Options: nosniff`

Always set this. There are no downsides.

---

### X-Frame-Options / frame-ancestors

**Purpose:** Prevents clickjacking by controlling whether the page can be framed.

**Recommended:** Use CSP `frame-ancestors 'none'` (modern replacement for X-Frame-Options).

**Legacy fallback:** `X-Frame-Options: DENY` or `X-Frame-Options: SAMEORIGIN`

---

### Referrer-Policy

**Purpose:** Controls how much referrer information is sent with requests.

**Recommended:** `Referrer-Policy: strict-origin-when-cross-origin`

---

### Permissions-Policy

**Purpose:** Restricts browser features (camera, microphone, geolocation, etc.).

**Recommended minimum:**
```
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
```

Only enable features the application actually uses.

---

### Cookie Security Flags

| Flag | Purpose | When to use |
|------|---------|-------------|
| `Secure` | Only send cookie over HTTPS | Always (for all cookies) |
| `HttpOnly` | Prevent JavaScript access to cookie | Always (for session/auth cookies) |
| `SameSite=Lax` | Prevent CSRF via cross-site requests | Default for most cookies |
| `SameSite=Strict` | Block cookie on all cross-site requests | For highly sensitive operations |
| `__Host-` prefix | Require Secure + no Domain attribute | For session cookies (strongest protection) |

**Framework examples:**

| Framework | Implementation |
|-----------|---------------|
| Django | `SESSION_COOKIE_SECURE = True`, `SESSION_COOKIE_HTTPONLY = True`, `SESSION_COOKIE_SAMESITE = 'Lax'` |
| Flask | `app.config['SESSION_COOKIE_SECURE'] = True`, etc. |
| Express | `cookie: { secure: true, httpOnly: true, sameSite: 'lax' }` |

---

### TLS Configuration

**Minimum:** TLS 1.2. **Recommended:** TLS 1.3.

**Where to check:**
- Load balancer / reverse proxy SSL policy
- Application server SSL context
- Database connection string (`sslmode=require` or `sslmode=verify-full`)

**Testing:**
```bash
# Test TLS version and cipher suites
nmap --script ssl-enum-ciphers -p 443 example.com

# Quick check with curl
curl -v --tls-max 1.1 https://example.com  # should fail if TLS 1.2+ required

# OpenSSL test
openssl s_client -connect example.com:443 -tls1_2
```

---

## CORS Configuration

**Rules:**
- Never use `Access-Control-Allow-Origin: *` for authenticated endpoints
- Allowlist specific origins, don't reflect the `Origin` header blindly
- Set `Access-Control-Allow-Credentials: true` only with explicit origin (not `*`)
- Restrict `Access-Control-Allow-Methods` to only needed methods
- Set `Access-Control-Max-Age` to cache preflight responses

**Dangerous pattern (reflecting origin):**
```python
# BAD — reflects any origin, effectively disabling CORS
response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
```

---

## Testing Security Headers

```bash
# Check all headers at once
curl -s -D- https://example.com | grep -iE '(content-security|strict-transport|x-content-type|x-frame|referrer-policy|permissions-policy|set-cookie)'

# Online scanner
# https://securityheaders.com (enter your URL)
# https://observatory.mozilla.org (comprehensive check)
```

## Best practices

- Set headers at the reverse proxy / CDN level when possible (catches all routes)
- Test headers in staging before production (especially CSP — can break functionality)
- Use CSP report-only mode first: `Content-Security-Policy-Report-Only: ...`
- Monitor CSP violation reports to catch legitimate breakage
- Review headers after every deployment (new dependencies may require CSP updates)

## Anti-patterns

- "We'll add headers later" — headers are trivial to add and should be present from day one
- Using `unsafe-inline` and `unsafe-eval` in CSP to "make it work" — defeats the purpose
- Setting HSTS `preload` without testing — extremely difficult to undo
- Relying on framework defaults without verifying they're enabled
- Not setting headers on error pages (404, 500) — these are also attack surfaces
