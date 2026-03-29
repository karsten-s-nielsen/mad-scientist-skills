# Authentication & Session Management Checklist

Reference for securing authentication, session handling, and credential management. Covers password hashing, token lifecycle, OAuth flows, and account protection.

## Purpose

Answer: "Is authentication implemented securely? Are sessions protected from hijacking, fixation, and replay attacks?"

## Checklist

Before auditing, identify:

- [ ] Which authentication method(s) are used (passwords, OAuth, API keys, SSO, certificates)
- [ ] Which session mechanism is used (server-side sessions, JWT, hybrid)
- [ ] Where credentials are stored (application database, identity provider, cloud IAM)
- [ ] Whether there is an account recovery flow (password reset, MFA recovery)
- [ ] Whether the application has admin/privileged user roles

## Password Hashing

### Recommended Algorithms

| Algorithm | Recommended Config | Library |
|-----------|-------------------|---------|
| **bcrypt** | Cost factor >= 12 | Python: `bcrypt`, Node.js: `bcrypt`, Go: `golang.org/x/crypto/bcrypt` |
| **argon2id** | m=65536, t=3, p=4 | Python: `argon2-cffi`, Node.js: `argon2`, Go: `golang.org/x/crypto/argon2` |
| **scrypt** | N=32768, r=8, p=1 | Python: `hashlib.scrypt`, Node.js: `crypto.scrypt` |

### Weak Algorithms (flag as Critical)

| Algorithm | Why it's weak |
|-----------|--------------|
| MD5 | Collision attacks, no salting, GPU-crackable in seconds |
| SHA-1 | Collision attacks, no salting, GPU-crackable |
| SHA-256 (direct) | Fast hash — no work factor, GPU-crackable. Only safe inside PBKDF2 with 600,000+ iterations |
| PBKDF2-SHA1 | Deprecated hash — use PBKDF2-SHA256 with 600,000+ iterations or switch to bcrypt/argon2 |
| Plaintext | Self-explanatory |
| Reversible encryption | AES/DES-encrypted passwords can be decrypted if key is compromised |

### Framework Examples

**Python (Django):**
```python
# GOOD — Django default uses PBKDF2-SHA256 with 720,000 iterations (as of 5.0)
# Verify in settings.py:
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',  # best
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]
```

**Python (standalone):**
```python
# GOOD
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
bcrypt.checkpw(password.encode(), hashed)

# BAD
import hashlib
hashed = hashlib.sha256(password.encode()).hexdigest()  # no salt, fast hash
```

**Node.js:**
```javascript
// GOOD
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(password, 12);
const match = await bcrypt.compare(password, hash);

// BAD
const crypto = require('crypto');
const hash = crypto.createHash('sha256').update(password).digest('hex');
```

## Session Management

### Session Fixation Prevention

After successful login, always regenerate the session ID:

| Framework | How to regenerate |
|-----------|------------------|
| Django | `request.session.cycle_key()` (automatic on login) |
| Flask | `session.regenerate()` or `flask-login` handles it |
| Express | `req.session.regenerate(callback)` |
| Go | Create new session, invalidate old one |

### Session Cookie Configuration

Every session cookie must have:

| Flag | Value | Why |
|------|-------|-----|
| `Secure` | `true` | Prevent transmission over HTTP |
| `HttpOnly` | `true` | Prevent JavaScript access (XSS mitigation) |
| `SameSite` | `Lax` or `Strict` | Prevent CSRF |
| `Path` | `/` or specific path | Limit cookie scope |
| `Max-Age` / `Expires` | Bounded lifetime | Don't allow indefinite sessions |

### Server-Side Session Destruction

On logout, destroy the session server-side — don't just delete the client cookie:

```python
# Django
from django.contrib.auth import logout
logout(request)  # clears session from DB and cookie

# Flask
session.clear()

# Express
req.session.destroy(callback)
```

## OAuth 2.0 / OIDC Security

| Check | Why | Severity |
|-------|-----|----------|
| Use PKCE for public clients | Prevents authorization code interception | Critical |
| Validate `state` parameter | Prevents CSRF in OAuth flow | High |
| Exact-match redirect URIs | Prevents open redirect to attacker-controlled page | Critical |
| Use `id_token` validation | Verify signature, issuer, audience, expiration | High |
| Short authorization code lifetime | Codes should expire in < 10 minutes | Medium |
| Rotate refresh tokens | Single-use refresh tokens detect token theft | High |

### PKCE Flow

```
Client generates:
  code_verifier = random(43-128 chars)
  code_challenge = BASE64URL(SHA256(code_verifier))

Authorization request includes:
  &code_challenge=xxx&code_challenge_method=S256

Token request includes:
  &code_verifier=xxx  (server verifies SHA256 matches challenge)
```

## Token Lifecycle

| Token Type | Max Lifetime | Storage | Rotation |
|-----------|-------------|---------|----------|
| Access token | 15-60 minutes | Memory or `HttpOnly` cookie | Issued fresh on refresh |
| Refresh token | 7-30 days | `HttpOnly` cookie with `Secure` + `SameSite=Strict` | Rotated on each use |
| API key | Until rotated | Server-side only (env var, secrets manager) | Rotate quarterly minimum |
| Session ID | Until logout (max 24h idle) | `HttpOnly` cookie | Regenerated on login |

## Account Protection

### Brute Force Prevention

| Mechanism | Implementation | Threshold |
|-----------|---------------|-----------|
| Account lockout | Lock account after N failures, unlock after timeout | 5 failures, 15-min lockout |
| Progressive delay | Increase response time after each failure | 1s, 2s, 4s, 8s... |
| CAPTCHA | Present after N failures | After 3 failures |
| IP rate limiting | Rate limit login endpoint per IP | 10/minute per IP |

### Password Reset Security

| Check | Correct implementation |
|-------|----------------------|
| Token is single-use | Invalidated after use |
| Token expires | 15-60 minutes maximum |
| Token is unpredictable | Cryptographically random (>= 128 bits) |
| Old password not required | (for "forgot password" flow) |
| Email confirmation | Reset link sent to email on file, not user-supplied email |
| No user enumeration | Same response whether email exists or not |

## Grep Patterns

| Pattern | Language | Issue |
|---------|----------|-------|
| `hashlib\.(md5\|sha1\|sha256)\(.*password` | Python | Weak password hashing |
| `crypto.createHash\(['"]sha256` with password context | Node.js | Weak password hashing |
| `session\[.*\]\s*=.*password\|req.session.password` | Any | Password stored in session |
| `localStorage.setItem\(.*token` | JS | Token in XSS-accessible storage |
| `jwt.decode\(` without `verify` parameter | Python | JWT signature not verified |
| `jsonwebtoken.decode\(` (vs `verify`) | Node.js | JWT signature not verified |
| `set.cookie.*secure.*false\|secure:\s*false` | Any | Missing Secure flag on cookie |
| `password.*=.*request\.(form\|json\|body)` without hashing nearby | Any | Possible plaintext password storage |

## Best practices

- Use a well-tested auth library (Passport.js, django-allauth, NextAuth.js) — don't roll your own
- Hash passwords with bcrypt (cost 12+) or argon2id — never use fast hashes
- Regenerate session IDs on login, re-authentication, and privilege changes
- Validate JWT signatures with explicit algorithm allowlist
- Use `HttpOnly` + `Secure` + `SameSite` cookies for token storage
- Implement account lockout with exponential backoff
- Log all auth events (login success/failure, password change, token refresh) for monitoring

## Anti-patterns

- "We'll add MFA later" — auth is the most critical component, secure it first
- Storing passwords with reversible encryption "for admin access"
- Using `localStorage` for JWT tokens (XSS-accessible)
- Implementing JWT without expiration or with very long expiration (> 1 hour)
- Not regenerating session IDs after login (session fixation)
- Relying on client-side validation for authentication logic
- Using the same secret for all token types (access, refresh, API keys)
