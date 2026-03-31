---
name: security-audit
description: Comprehensive security audit with two modes and two tiers. Planning mode reviews architecture for security gaps (STRIDE threat modeling, auth design, data classification, AI regulatory compliance). Audit mode scans code, infrastructure, dependencies, and secrets for vulnerabilities. Covers OWASP Top 10, ML/AI model security (serialization safety, provenance, poisoning), AI regulatory compliance (EU AI Act, biometric privacy, EU Data Act), web security headers, API boundary security, authentication and session management, CWE references, infrastructure hardening, confidential computing, and privacy-preserving computation. Each phase has Standard (free tools, always actionable) and Enterprise (paid services, aspirational checklist) tiers. Use when asked to "security audit", "threat model", "check for vulnerabilities", "review security", or "harden this".
---

# Security Audit

A comprehensive security skill with two modes and two tiers:

**Modes:**
- **Planning** (before code exists) — threat modeling, auth design, data classification
- **Audit** (on existing code) — vulnerability scanning, infrastructure review, dependency audit

**Tiers** (applied within each phase):
- **Standard** — free tools, code-level patterns, open-source scanners. Always actionable for any developer.
- **Enterprise** — paid services (WAF, SIEM, DAST/SAST), compliance tooling. Serves as a professional checklist documenting what enterprise teams should implement.

**Core question:** "Is this system defensible?"

## When to use this skill

- When the user says "security audit", "threat model", "check for vulnerabilities", "review security", or "harden this"
- Before designing a new system (planning mode) — to identify threats early
- On an existing codebase (audit mode) — to find and fix vulnerabilities
- Before a production deployment — to validate security posture
- After adding authentication, authorization, or data handling features

## Mode detection

Determine which mode to operate in based on the project state:

| Signal | Mode | Rationale |
|--------|------|-----------|
| User says "threat model", "security plan", "design review" | **Planning** | Architecture-level analysis before code |
| User says "audit", "scan", "check for vulnerabilities" | **Audit** | Code and infrastructure scanning |
| No source code exists yet (only docs, diagrams, RFCs) | **Planning** | Nothing to scan — model threats instead |
| Source code and/or IaC files exist | **Audit** | Concrete artifacts to analyze |
| Both code and a request to "threat model" | **Both** | Run planning phases on architecture, audit phases on code |

When in doubt, ask the user. If both modes apply, run all 14 phases.

## Severity classification

Every finding must be assigned a severity:

| Severity | Criteria | Action | SLA |
|----------|----------|--------|-----|
| **Critical** | Actively exploitable, data breach risk, auth bypass, RCE | Fix immediately | Block release |
| **High** | Significant risk but requires specific conditions (SSRF, SQL injection, privilege escalation) | Fix before next release | 1 sprint |
| **Medium** | Defense-in-depth gaps, missing headers, verbose errors, weak crypto | Schedule fix | 2 sprints |
| **Low** | Informational, best practice deviations, minor hardening opportunities | Track in backlog | Best effort |

## Audit process

Execute all applicable phases in order. Skip phases marked for a mode you are not running. Do NOT skip applicable phases. Do NOT claim completion without evidence.

---

### Phase 0: Anti-Pattern Scan (Audit mode)

Fast grep-based scan for dangerous code patterns. Runs first to catch obvious security issues before deeper analysis. These patterns are absorbed from the Anthropic `security-guidance` hook and expanded with additional checks.

#### Standard tier

Scan all source files for these patterns. Each match requires manual review — some may be intentional (e.g., `eval()` in a test helper).

| Pattern | Language | Risk | CWE | OWASP |
|---------|----------|------|-----|-------|
| `eval(` | Python, JS | Arbitrary code execution | CWE-95 | A03 |
| `exec(` | Python | Arbitrary code execution | CWE-95 | A03 |
| `new Function(` | JS | Code injection via string | CWE-95 | A03 |
| `child_process.exec(` | Node.js | OS command injection | CWE-78 | A03 |
| `child_process.execSync(` | Node.js | OS command injection | CWE-78 | A03 |
| `os.system(` | Python | OS command injection | CWE-78 | A03 |
| `subprocess.call(.*shell=True` | Python | OS command injection | CWE-78 | A03 |
| `subprocess.Popen(.*shell=True` | Python | OS command injection | CWE-78 | A03 |
| `pickle.loads(` | Python | Deserialization of untrusted data | CWE-502 | A08 |
| `pickle.load(` | Python | Deserialization of untrusted data | CWE-502 | A08 |
| `yaml.load(` (without `Loader=SafeLoader`) | Python | Deserialization of untrusted data | CWE-502 | A08 |
| `torch.load(` (without `weights_only=True`) | Python | ML model deserialization via pickle | CWE-502 | A08 |
| `joblib.load(` | Python | ML model deserialization via pickle | CWE-502 | A08 |
| `mlflow.pyfunc.load_model(` | Python | Indirect pickle via MLflow Python flavor | CWE-502 | A08 |
| `numpy.load(.*allow_pickle` | Python | NumPy array deserialization via pickle | CWE-502 | A08 |
| `dangerouslySetInnerHTML` | React | Cross-site scripting | CWE-79 | A03 |
| `document.write(` | JS | Cross-site scripting | CWE-79 | A03 |
| `.innerHTML\s*=` | JS | Cross-site scripting | CWE-79 | A03 |
| `render_template_string(` | Flask | Server-side template injection | CWE-1336 | A03 |
| `Markup(.*\+` | Flask/Jinja | XSS via unsafe markup concatenation | CWE-79 | A03 |
| `verify=False` | Python requests | Disabled TLS certificate verification | CWE-295 | A02 |
| `rejectUnauthorized:\s*false` | Node.js | Disabled TLS certificate verification | CWE-295 | A02 |
| `CERT_NONE` | Python ssl | Disabled TLS certificate verification | CWE-295 | A02 |
| `InsecureSkipVerify:\s*true` | Go | Disabled TLS certificate verification | CWE-295 | A02 |
| `__proto__` or `constructor.prototype` | JS | Prototype pollution | CWE-1321 | A03 |
| `hashlib.md5\|hashlib.sha1` (for passwords) | Python | Weak password hashing | CWE-328 | A02 |
| `crypto.createHash\(['"]md5` (for passwords) | Node.js | Weak password hashing | CWE-328 | A02 |
| `DEBUG\s*=\s*True` | Python/Django | Debug mode in production | CWE-489 | A05 |
| `jwt.decode(` (without `verify=True` or `algorithms=`) | Python/Node | JWT signature bypass | CWE-347 | A07 |

For each finding: record file path, line number, pattern matched, and whether it is a true positive or intentional usage. Flag true positives as Critical or High.

#### Enterprise tier

Integrate with static analysis tools for deeper coverage:

| Tool | Purpose | Command |
|------|---------|---------|
| Semgrep | Pattern-based SAST with custom rules | `semgrep --config auto .` |
| SonarQube | Continuous code quality + security | Configure via `sonar-project.properties` |
| Snyk Code | AI-powered SAST | `snyk code test` |
| CodeQL | GitHub-native SAST | Configure via `.github/codeql/codeql-config.yml` |

Document which tool is configured and whether it runs in CI.

**Output:** Code pattern findings table with file paths, CWE references, and true/false positive classification.

---

### Phase 1: Discovery (Both modes)

Explore the project to understand its security surface:

- Read `CLAUDE.md`, `README.md`, `AGENTS.md`, and any architecture docs
- Identify the tech stack, frameworks, and language versions
- Map the **security surface**:
  - Entry points: APIs, webhooks, CLI interfaces, message consumers, scheduled jobs
  - Data stores: databases, caches, object storage, file systems
  - Authentication mechanisms: OAuth, JWT, API keys, session cookies, mTLS
  - Authorization model: RBAC, ABAC, ACLs, row-level security
  - External integrations: third-party APIs, SaaS services, cloud provider services
  - Network boundaries: public internet, VPC, internal services, on-prem
  - **Web-specific surface** (if applicable):
    - Public-facing URLs and endpoints (API routes, static assets, health checks)
    - CDN or reverse proxy configuration (Cloudflare, CloudFront, nginx)
    - API gateway (AWS API Gateway, Kong, Apigee)
    - Client-side rendering vs server-side rendering framework
    - Authentication flow type: cookie-based sessions, bearer tokens, OAuth redirect
    - WebSocket or SSE endpoints
    - File upload endpoints
    - Third-party script inclusions (analytics, CDN libraries)
- Identify sensitive data flows: PII, credentials, financial data, health data
- Note the deployment model: containers, serverless, VMs, managed services

**Output:** A security surface summary listing all entry points, data stores, auth mechanisms, and trust boundaries.

---

### Phase 2: Threat Modeling — STRIDE (Planning mode)

Apply the STRIDE framework to each component and trust boundary identified in Phase 1.

Load `templates/stride-threat-model.md` for the full STRIDE reference, trust boundary patterns, and severity scoring matrix.

For each major component or trust boundary:

1. **Spoofing** — Can an attacker impersonate a legitimate user or service?
2. **Tampering** — Can data in transit or at rest be modified without detection?
3. **Repudiation** — Can actions be performed without an audit trail?
4. **Information Disclosure** — Can sensitive data leak through errors, logs, or side channels?
5. **Denial of Service** — Can the system be overwhelmed or made unavailable?
6. **Elevation of Privilege** — Can a low-privilege user gain higher access?

For each identified threat:

| Threat ID | Component | STRIDE Category | Description | Likelihood | Impact | Severity | Mitigation |
|-----------|-----------|-----------------|-------------|------------|--------|----------|------------|
| T-001 | API Gateway | Spoofing | Missing mutual TLS between services | High | High | Critical | Implement mTLS |

**Output:** Completed threat model table with mitigations for every identified threat.

---

### Phase 3: Infrastructure Security (Audit mode)

Scan all Infrastructure-as-Code (IaC) files and deployment configurations. This phase has four sub-phases.

Load `templates/infrastructure-hardening.md` for the full hardening checklist with platform-specific guidance.

#### Phase 3a: IAM and Access Control

- Overly permissive IAM policies (`*` actions or resources)
- Missing least-privilege scoping
- Service accounts with admin roles
- Missing MFA enforcement
- Long-lived credentials instead of short-lived tokens
- Cross-account access without explicit trust policies

#### Phase 3b: Network Security

- Public-facing resources that should be private (databases, caches, internal APIs)
- Missing security groups or overly permissive ingress rules (`0.0.0.0/0`)
- No network segmentation between tiers
- Missing VPC flow logs or network monitoring
- Unencrypted traffic between services

**Note:** SaaS workspace API IP restrictions (e.g., Databricks `ip_access_list`, GitHub IP allow lists) belong to the **enterprise tier** — they require static IPs or VPN egress, which are impractical for individual developers and CI runners with dynamic IPs.

#### Phase 3c: Encryption

- Data at rest without encryption (databases, object storage, EBS volumes)
- Missing TLS for data in transit
- Weak cipher suites or outdated TLS versions (< 1.2)
- Hardcoded encryption keys instead of KMS
- Missing key rotation policies

#### Phase 3d: Container and Compute Security

- Containers running as root
- Missing resource limits (CPU, memory)
- Base images not pinned to digest
- No health checks defined
- Missing read-only root filesystem
- Privileged mode enabled

#### Enterprise tier additions

These controls require paid cloud services or enterprise subscriptions:

| Control | Service | Purpose |
|---------|---------|---------|
| Web Application Firewall | AWS WAF, Cloudflare WAF, Azure Front Door | Layer 7 attack filtering (SQLi, XSS, bot protection) |
| DDoS protection | AWS Shield Advanced, Cloudflare Enterprise, Azure DDoS Protection | Volumetric and application-layer DDoS mitigation |
| Cloud-native SAST/DAST | AWS CodeGuru, Azure DevOps Security, GCP Web Security Scanner | Automated vulnerability scanning in CI/CD |
| CDN security headers | CloudFront response headers policy, Cloudflare Transform Rules | Inject security headers at the edge |
| Container runtime security | Falco, Sysdig Secure, Aqua Security | Runtime threat detection in containers |
| Network intrusion detection | AWS GuardDuty, Azure Sentinel, GCP Chronicle | ML-based anomaly detection on network traffic |
| API source IP restrictions | Databricks `ip_access_list`, GitHub IP allow lists, cloud provider API firewalls | Restrict workspace/API access to known static IPs or VPN egress — requires static IP infrastructure |

For each applicable service: document whether it is enabled, its configuration, and any gaps.

**Output:** Infrastructure findings table with file paths, line numbers, severity, and remediation.

---

### Phase 4: Code Security — OWASP Top 10 (Audit mode)

Scan all source code for vulnerabilities mapped to the OWASP Top 10 (2021). For each category, use the stack-specific grep patterns below and assign CWE references.

#### OWASP Top 10 with CWE mappings

| OWASP ID | Category | Key CWEs | What to look for |
|----------|----------|----------|------------------|
| A01 | Broken Access Control | CWE-200, CWE-284, CWE-285, CWE-352, CWE-639 | Missing auth checks on endpoints, IDOR, CORS misconfiguration, CSRF tokens missing |
| A02 | Cryptographic Failures | CWE-259, CWE-327, CWE-328, CWE-330, CWE-916 | Weak hashing (MD5, SHA1 for passwords), hardcoded keys, HTTP for sensitive data |
| A03 | Injection | CWE-20, CWE-77, CWE-78, CWE-79, CWE-89 | SQL string concatenation, unescaped HTML output, OS command injection, LDAP injection |
| A04 | Insecure Design | CWE-209, CWE-256, CWE-501, CWE-522 | Missing rate limiting, no account lockout, trust boundary violations |
| A05 | Security Misconfiguration | CWE-2, CWE-11, CWE-16, CWE-548 | Debug mode in production, default credentials, directory listing, verbose errors |
| A06 | Vulnerable Components | CWE-1035, CWE-1104 | Known CVEs in dependencies, outdated packages, unmaintained libraries |
| A07 | Auth Failures | CWE-255, CWE-287, CWE-384 | Weak password policies, missing session invalidation, credential stuffing exposure |
| A08 | Data Integrity Failures | CWE-345, CWE-353, CWE-426, CWE-494, CWE-502 | Deserialization of untrusted data, missing integrity checks, auto-update without signing |
| A09 | Logging Failures | CWE-117, CWE-223, CWE-532, CWE-778 | Sensitive data in logs, missing security event logging, no alerting |
| A10 | SSRF | CWE-918 | User-controlled URLs passed to server-side HTTP clients, DNS rebinding |

#### Stack-specific grep patterns

Use these patterns to find common vulnerabilities per language:

| Language | Pattern | Vulnerability | OWASP |
|----------|---------|---------------|-------|
| **Python** | `execute\(.*%s\|execute\(.*\.format\|execute\(.*f"` | SQL injection | A03 |
| **Python** | `eval\(\|exec\(\|pickle\.loads\(\|yaml\.load\(` | Code injection | A03 |
| **Python** | `subprocess\.call\(.*shell=True\|os\.system\(` | OS command injection | A03 |
| **Python** | `verify=False\|CERT_NONE` | Disabled SSL verification | A02 |
| **Python** | `hashlib\.md5\|hashlib\.sha1` (for passwords) | Weak hashing | A02 |
| **Python** | `DEBUG\s*=\s*True` | Debug mode in production | A05 |
| **Python** | `render_template_string\(\|Markup\(.*\+\|\.safe` | XSS / template injection | A03 |
| **Node.js** | `eval\(\|Function\(\|child_process\.exec\(` | Code/command injection | A03 |
| **Node.js** | `innerHTML\|dangerouslySetInnerHTML\|document\.write` | XSS | A03 |
| **Node.js** | `rejectUnauthorized:\s*false` | Disabled SSL verification | A02 |
| **Node.js** | `jwt\.decode\(` (without verify) | JWT bypass | A07 |
| **Node.js** | `\.query\(.*\+\|\.query\(.*\$\{` | SQL injection | A03 |
| **Go** | `fmt\.Sprintf\(.*SELECT\|fmt\.Sprintf\(.*INSERT` | SQL injection | A03 |
| **Go** | `exec\.Command\(.*\+\|exec\.CommandContext\(.*\+` | Command injection | A03 |
| **Go** | `InsecureSkipVerify:\s*true` | Disabled SSL verification | A02 |
| **Rust** | `unsafe\s*\{` | Unsafe blocks (review required) | A04 |
| **Rust** | `format!\(.*SELECT\|format!\(.*INSERT` | SQL injection | A03 |
| **Terraform** | `cidr_blocks\s*=\s*\["0\.0\.0\.0/0"\]` | Open ingress | A05 |
| **Terraform** | `encrypted\s*=\s*false` | Unencrypted storage | A02 |
| **Terraform** | `publicly_accessible\s*=\s*true` | Public database | A01 |

For each finding, record the file path, line number, OWASP category, CWE, severity, and recommended fix.

**Output:** Code security findings table with CWE references and remediation steps.

---

### Phase 4b: ML/AI Model Security (Audit mode)

If the project trains, deploys, or consumes machine learning models, audit the ML-specific security surface. ML models introduce threats that standard code scanning does not cover: unsafe deserialization via model loading, training data leakage through model parameters, and unverified model provenance.

Skip this phase if the project has no ML components (no model training, no model inference, no model artifact storage).

#### Standard tier

**Model serialization safety:**

| Check | What to look for | CWE | Severity |
|-------|-----------------|-----|----------|
| No unsafe pickle loading | `torch.load()` must use `weights_only=True` (PyTorch 2.6+ default). `joblib.load()` and `pickle.load()` must never load untrusted artifacts. | CWE-502 | Critical |
| MLflow flavor audit | `mlflow.pyfunc.load_model()` may use pickle internally depending on the serializer chosen at model log time. Document which serializer each registered model uses. | CWE-502 | High |
| Safe format preference | Prefer `safetensors` (Hugging Face) over pickle-based formats for Transformer weights. Prefer XGBoost JSON (`save_raw("json")`) over pickle for tree models. | CWE-502 | Medium |
| Model artifact integrity | Downloaded model artifacts should be verified (checksums, signatures, or trusted registry with access controls). | CWE-494 | High |
| No `numpy.load(allow_pickle=True)` | NumPy arrays from untrusted sources must not enable pickle deserialization. | CWE-502 | High |

**Grep patterns for ML serialization:**

| Pattern | Issue |
|---------|-------|
| `torch\.load\(` without `weights_only=True` in same call | Unsafe PyTorch model loading |
| `torch\.save\(` | Verify saved models are not redistributed without integrity checks |
| `joblib\.(load\|dump)\(` | Pickle-based serialization — verify trust boundary |
| `mlflow\.pyfunc\.load_model\(` | Audit MLflow serializer flavor (check model metadata) |
| `safetensors` | Good — verify this is used for Transformer weights |
| `\.save_raw\("json"\)` | Good — verify XGBoost uses JSON format, not pickle |

**Model provenance and trust:**

| Check | What to look for | CWE | Severity |
|-------|-----------------|-----|----------|
| Model source authentication | Models loaded from external registries (HF Hub, MLflow) must use authenticated connections with explicit tokens | CWE-287 | High |
| Model scanning | External model artifacts should be scanned for malware before loading (HuggingFace `safetensors` includes built-in pickle scanning) | CWE-506 | Medium |
| Model versioning | Model artifacts must be versioned and traceable to a specific training run, dataset, and code commit | CWE-1059 | Medium |
| Access control on model registry | Write access to model registries restricted to training pipelines; inference consumers have read-only access | CWE-284 | High |

#### Enterprise tier

| Control | Purpose | Tool / Service |
|---------|---------|----------------|
| Model artifact signing | Cryptographic proof of model provenance and integrity | Sigstore/Cosign for ML artifacts, MLflow model signatures |
| ML-specific SAST | Scan model files for embedded malicious code | `modelscan` (Protect AI), HuggingFace malware scanning |
| Model cards / datasheets | Document training data, intended use, limitations, and ethical considerations | HuggingFace Model Cards, Google Model Cards Toolkit |
| Inference endpoint security | Rate limiting, input validation, and output filtering on model serving endpoints | AWS SageMaker endpoint policies, HuggingFace Inference Endpoints ACLs |
| Adversarial robustness testing | Test model behavior under adversarial inputs | IBM Adversarial Robustness Toolbox (ART), Microsoft Counterfit |
| Model monitoring for drift/attack | Detect distribution shifts that may indicate data poisoning or adversarial manipulation | NannyML, Evidently AI, WhyLabs |

**Output:** ML model security findings table with CWE references, affected model artifacts, and remediation.

---

### Phase 5: Web Security Headers & Transport (Audit mode)

Verify that the application sets appropriate HTTP security headers and enforces secure transport. Missing headers are defense-in-depth gaps that increase the blast radius of other vulnerabilities.

Load `templates/web-security-headers.md` for the full header reference with framework-specific implementation examples.

#### Standard tier

Check for the following headers and controls in application code, middleware configuration, and server config:

| Header / Control | Purpose | Severity if missing | What to grep |
|------------------|---------|---------------------|-------------|
| `Content-Security-Policy` | Prevents XSS by restricting script sources | High | Framework middleware config, `<meta>` tags, server config |
| `Strict-Transport-Security` | Forces HTTPS for all future requests | High | Response headers, server config, `max-age` value |
| `X-Content-Type-Options: nosniff` | Prevents MIME type sniffing attacks | Medium | Middleware config, response headers |
| `X-Frame-Options` or CSP `frame-ancestors` | Prevents clickjacking | Medium | Response headers, CSP directive |
| `Referrer-Policy` | Controls referrer header leakage | Medium | Response headers |
| `Permissions-Policy` | Restricts browser features (camera, geolocation, etc.) | Low | Response headers |
| Cookie `Secure` flag | Cookies only sent over HTTPS | High | `set_cookie`, `Set-Cookie`, session config |
| Cookie `HttpOnly` flag | Cookies inaccessible to JavaScript | High | Same |
| Cookie `SameSite` flag | Prevents CSRF via cross-site cookie sending | High | Same |
| TLS 1.2+ enforcement | Prevents downgrade attacks | High | Server config, SSL context, load balancer policy |
| HSTS preload | Domain added to browser preload list | Low | `includeSubDomains; preload` in HSTS header |
| CORS origin allowlist | Restricts cross-origin access | High | `Access-Control-Allow-Origin` must not be `*` for authenticated endpoints |

**Framework-specific locations:**

| Framework | Where headers are typically set |
|-----------|-------------------------------|
| Django | `SECURE_*` settings in `settings.py`, `django-csp` middleware |
| Flask | `flask-talisman` or `after_request` hook |
| FastAPI | `starlette.middleware`, custom `Middleware` class |
| Express | `helmet` middleware |
| Next.js | `next.config.js` `headers()` function |
| Streamlit | Not directly configurable — relies on Databricks Apps / reverse proxy |

For each missing header: record the framework, where it should be configured, and provide the specific configuration snippet.

#### Enterprise tier

| Control | Purpose | Tool / Service |
|---------|---------|----------------|
| CSP with nonce/hash | Eliminate `unsafe-inline` from CSP | Server-generated nonces per request |
| Subresource Integrity (SRI) | Verify CDN assets aren't tampered | `integrity` attribute on `<script>` and `<link>` tags |
| Certificate Transparency monitoring | Detect rogue certificates for your domain | CT log monitoring (e.g., crt.sh, Cloudflare CT Monitor) |
| WAF header injection | Add security headers at the edge | CloudFront response headers policy, Cloudflare Transform Rules |
| TLS certificate pinning | Prevent MITM with rogue CA certs | Mobile apps only (deprecated for browsers) |

**Output:** Web security headers findings table with severity, current state, and remediation.

---

### Phase 6: API Boundary Security (Audit mode)

Verify that all API endpoints validate input, enforce rate limits, and don't leak internal information. APIs are the primary attack surface for most modern applications.

Load `templates/api-security-checklist.md` for the full checklist with grep patterns per framework.

#### Standard tier

| Check | What to look for | CWE | Severity |
|-------|-----------------|-----|----------|
| Input validation at boundaries | All user input validated before processing (type, length, format, range) | CWE-20 | High |
| Parameterized queries | SQL uses `%s`/`$1`/`?` placeholders — never string interpolation with user input | CWE-89 | Critical |
| Rate limiting | Rate limiting middleware or patterns (`slowapi`, `express-rate-limit`, API gateway throttling) | CWE-770 | High |
| Error message leakage | Error responses don't expose stack traces, SQL errors, file paths, or framework versions | CWE-209 | Medium |
| CORS configuration | `Access-Control-Allow-Origin` is not `*` for authenticated endpoints; only trusted origins listed | CWE-346 | High |
| JWT validation | Tokens validated for signature, expiration, issuer, and audience — not just decoded | CWE-347 | Critical |
| Request size limits | Body size limits configured (`max_content_length`, body parser `limit` option) | CWE-400 | Medium |
| Content-Type validation | API rejects unexpected content types (e.g., sending XML to a JSON endpoint) | CWE-436 | Medium |
| HTTP method restrictions | Endpoints only accept intended methods (no unintended PUT/DELETE on read-only endpoints) | CWE-749 | Medium |
| Path traversal prevention | File paths from user input are validated and sandboxed | CWE-22 | Critical |

**Grep patterns for common issues:**

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `request\.(args\|form\|json)\[` without validation | Unvalidated user input |
| Python | `f"SELECT.*{` or `"SELECT.*".format(` | SQL injection via f-string/format |
| Node.js | `req\.(body\|query\|params)\.` without validation | Unvalidated user input |
| Node.js | `\.query\(.*\+\|\.query\(.*\$\{` | SQL injection via concatenation |
| Go | `r\.URL\.Query\(\)\.Get\(` without validation | Unvalidated query parameter |
| Go | `fmt\.Sprintf\(.*SELECT\|fmt\.Sprintf\(.*INSERT` | SQL injection via Sprintf |

For each finding: record endpoint, input source, validation status, and recommended fix.

#### Enterprise tier

| Control | Purpose | Tool / Service |
|---------|---------|----------------|
| API gateway WAF rules | Block common attack patterns at the gateway | AWS API Gateway + WAF, Kong + ModSecurity |
| Mutual TLS (mTLS) | Authenticate both client and server for service-to-service calls | Service mesh (Istio, Linkerd), custom CA |
| GraphQL depth/complexity limiting | Prevent deeply nested or expensive GraphQL queries | `graphql-depth-limit`, `graphql-query-complexity` |
| OpenAPI schema validation | Reject requests not matching the API spec | `connexion` (Python), `express-openapi-validator` |
| Request signing (HMAC) | Verify request integrity and authenticity | Custom middleware with shared secret |
| API versioning security | Ensure deprecated API versions are sunset | `Sunset` header, version lifecycle policy |
| Bot protection | Distinguish humans from automated abuse | Cloudflare Bot Management, AWS WAF Bot Control |

**Output:** API security findings table with endpoint, CWE, severity, and remediation.

---

### Phase 7: Authentication & Session Management (Both modes)

Verify that authentication and session handling follow current best practices. Auth flaws are consistently in the OWASP Top 10 (A07: Identification and Authentication Failures).

Load `templates/auth-session-checklist.md` for the full checklist with framework-specific patterns.

**Planning mode:** Evaluate the planned authentication architecture:
- Which authentication method? (session cookies, JWT, OAuth 2.0, API keys, mTLS)
- Where are credentials stored? (database, identity provider, cloud IAM)
- How are sessions managed? (server-side, stateless JWT, hybrid)
- What is the token lifecycle? (expiration, refresh, revocation)
- Is there an account recovery flow? (email reset, MFA recovery codes)

**Audit mode:** Scan code and configuration for auth vulnerabilities:

#### Standard tier

| Check | What to look for | CWE | Severity |
|-------|-----------------|-----|----------|
| Password hashing algorithm | bcrypt, argon2, or scrypt — not MD5, SHA-1, SHA-256, or plaintext | CWE-916 | Critical |
| Salt usage | Unique per-password salt (bcrypt/argon2 do this automatically) | CWE-916 | Critical |
| Session ID regeneration | Session ID regenerated after login to prevent session fixation | CWE-384 | High |
| CSRF protection | CSRF tokens on all state-changing requests (POST, PUT, DELETE) | CWE-352 | High |
| Secure cookie flags | `Secure`, `HttpOnly`, `SameSite=Lax` or `Strict` on session cookies | CWE-614 | High |
| Logout invalidation | Server-side session destruction on logout (not just client cookie deletion) | CWE-613 | Medium |
| Access token expiration | Access tokens expire in < 1 hour; refresh tokens have bounded lifetime | CWE-613 | High |
| Refresh token rotation | Refresh tokens are single-use and rotated on each use | CWE-384 | Medium |
| Account lockout | Brute-force protection: lockout or progressive delay after N failed attempts | CWE-307 | High |
| Password policy | Minimum length (12+), no common password list, no complexity-only rules | CWE-521 | Medium |
| Credential storage | No plaintext passwords in database, config files, or logs | CWE-256 | Critical |
| OAuth PKCE | Public OAuth clients use PKCE (Proof Key for Code Exchange) | CWE-287 | High |
| OAuth state parameter | State parameter validated to prevent CSRF in OAuth flows | CWE-352 | High |
| Redirect URI validation | OAuth redirect URIs are exact-match validated (no open redirects) | CWE-601 | High |

**Grep patterns:**

| Language | Pattern | Issue |
|----------|---------|-------|
| Python | `hashlib\.(md5\|sha1\|sha256)\(.*password` | Weak password hashing |
| Python | `check_password_hash\|pbkdf2_sha256\|bcrypt\.checkpw\|argon2\.verify` | Good — verify these are used everywhere |
| Node.js | `crypto\.createHash\(['"]sha256['"]\).*password` | Weak password hashing |
| Node.js | `bcrypt\.compare\|argon2\.verify\|scrypt` | Good — verify these are used everywhere |
| Any | `session\[.*\]\s*=.*password\|session\.password` | Password stored in session |
| Any | `localStorage\.setItem\(.*token\|sessionStorage\.setItem\(.*token` | Token in browser storage (XSS-accessible) |

#### Enterprise tier

| Control | Purpose | Tool / Service |
|---------|---------|----------------|
| Multi-factor authentication | Require MFA for all users or privileged operations | TOTP (Google Authenticator), WebAuthn, SMS (less secure) |
| Adaptive authentication | Risk-based step-up auth (new device, unusual location, sensitive action) | Auth0 Adaptive MFA, Okta Risk Engine |
| SSO / SAML / OIDC | Centralized identity with enterprise identity provider | Okta, Azure AD, Auth0, Keycloak |
| Passwordless authentication | Eliminate password-based attacks entirely | WebAuthn/FIDO2, magic links, passkeys |
| Credential stuffing protection | Block automated login attempts with stolen credentials | Breached password database checks (Have I Been Pwned API), CAPTCHA, bot detection |
| Privileged Access Management | Time-bounded, audited access for admin operations | HashiCorp Vault, CyberArk, AWS SSO |
| Certificate-based auth | Client certificates for machine-to-machine auth | mTLS with custom CA, SPIFFE/SPIRE |

**Output:** Authentication findings table with CWE, severity, and remediation. Planning mode: auth design recommendations table.

---

### Phase 8: Supply Chain Security (Audit mode)

Audit dependencies, lockfiles, and CI/CD pipelines for supply chain risks.

Load `templates/dependency-audit.md` for ecosystem-specific audit commands, lockfile integrity checks, and CI/CD security patterns.

#### 8a: Dependency Audit

Run the appropriate audit command for each ecosystem found in the project:

| Ecosystem | Audit command | Lockfile |
|-----------|---------------|----------|
| Node.js | `npm audit` or `yarn audit` or `pnpm audit` | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` |
| Python | `pip-audit` or `safety check` or `uv run pip-audit` | `requirements.txt`, `poetry.lock`, `uv.lock` |
| Go | `govulncheck ./...` | `go.sum` |
| Rust | `cargo audit` | `Cargo.lock` |
| Java | `mvn dependency-check:check` | `pom.xml` |

#### 8b: Lockfile Integrity

- Verify lockfiles exist and are committed
- Check for lockfile drift (lockfile out of sync with manifest)
- Verify lockfile is not in `.gitignore`

#### 8c: CI/CD Pipeline Security

- Pinned action versions (use SHA, not tags like `@latest` or `@v3`)
- Minimal permissions on workflow tokens (`permissions:` block)
- No secrets in workflow logs
- Protected branches and required reviews
- No `pull_request_target` with checkout of PR code (command injection risk)

#### 8d: SBOM and Dependency Governance (Standard)

- **SBOM generation**: Verify the project can generate a Software Bill of Materials
  - Python: `cyclonedx-bom`, `pip-audit --format cyclonedx`
  - Node.js: `cdxgen`, `npm sbom`
  - Go: `syft`, `cyclonedx-gomod`
  - Container: `syft <image>`, `trivy image --format cyclonedx`
- **Dependabot / Renovate**: Check for automated dependency update configuration
  - GitHub: `.github/dependabot.yml` exists
  - GitLab: Dependency Scanning CI template included
  - Renovate: `renovate.json` or `renovate.json5` exists
- **GitHub Actions OIDC**: For cloud deployments, verify OIDC is used instead of long-lived secrets
  - `aws-actions/configure-aws-credentials` with `role-to-assume` (no `aws-access-key-id`)
  - `google-github-actions/auth` with `workload_identity_provider` (no `credentials_json`)

#### Enterprise tier additions

| Control | Purpose | Tool / Service |
|---------|---------|----------------|
| Artifact signing | Prove build provenance with cryptographic signatures | Sigstore / Cosign |
| Private registry | Gate all dependencies through a scanning proxy | Artifactory, Nexus, GitHub Packages |
| Dependency firewalling | Block known-malicious packages before install | Socket.dev, Artifactory policies |
| SLSA compliance | Supply chain security maturity assessment | SLSA framework (levels 1-4) |
| Reproducible builds | Same source always produces identical artifacts | Docker `--build-arg BUILDKIT_INLINE_CACHE=1`, Bazel |

**Output:** Supply chain findings with affected packages, CVE IDs where applicable, and upgrade paths.

---

### Phase 9: Secrets Management (Both modes)

**Planning mode:** Evaluate the planned secrets management approach:
- Where will secrets be stored? (vault, cloud secrets manager, env vars)
- How will secrets be rotated?
- How will secrets be injected at runtime?
- Is there separation between environments (dev/staging/prod)?

**Audit mode:** Scan for hardcoded secrets and exposed credentials:

#### Secret detection patterns

| Pattern | What it catches |
|---------|-----------------|
| `(?i)(api[_-]?key\|apikey)\s*[:=]\s*['"][A-Za-z0-9]` | API keys |
| `(?i)(secret\|password\|passwd\|pwd)\s*[:=]\s*['"][^'"]{8,}` | Passwords and secrets |
| `(?i)(token\|bearer)\s*[:=]\s*['"][A-Za-z0-9]` | Tokens |
| `AKIA[0-9A-Z]{16}` | AWS access key IDs |
| `(?i)aws[_-]?secret[_-]?access[_-]?key\s*[:=]` | AWS secret keys |
| `ghp_[A-Za-z0-9]{36}` | GitHub personal access tokens |
| `sk-[A-Za-z0-9]{48}` | OpenAI API keys |
| `-----BEGIN (RSA\|EC\|DSA\|OPENSSH) PRIVATE KEY-----` | Private keys |
| `mongodb(\+srv)?://[^/\s]+:[^/\s]+@` | MongoDB connection strings with credentials |
| `postgres(ql)?://[^/\s]+:[^/\s]+@` | PostgreSQL connection strings with credentials |
| `mysql://[^/\s]+:[^/\s]+@` | MySQL connection strings with credentials |

Also check:
- `.env` files committed to version control (should be in `.gitignore`)
- Terraform state files with secrets (`terraform.tfstate` should never be committed)
- Docker build args containing secrets
- CI/CD logs that might print secrets
- Git history for previously committed secrets (`git log -p --all -S 'password'`)

#### Secrets strategy assessment (Both modes)

Beyond detecting exposed secrets, evaluate whether the overall secrets management strategy is appropriate for the project's infrastructure footprint. Over-engineering (adding a vault to a single-platform project) wastes effort; under-engineering (scattered env vars with no rotation) creates risk.

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Platform-native store utilization | Are platform-native secret stores fully utilized before introducing external vaults? (e.g., Databricks secrets scopes, HF Spaces secrets, GitHub Actions OIDC, AWS Parameter Store, GCP Secret Manager). Adding AWS Secrets Manager to a project that runs entirely on Databricks + HF Spaces adds an AWS account dependency for no operational benefit — a circular dependency where you need credentials to retrieve credentials | Medium |
| Centralization vs sprawl | Count the distinct secret stores in use. 1-2 stores aligned to deployment targets is healthy. 5+ stores with overlapping scope is sprawl that increases the attack surface for misconfiguration. Document each store's scope and whether it is the authoritative source for its secrets | High |
| Long-lived credential inventory | List all credentials with lifetimes >90 days (PATs, API keys, service account keys). Each must have a documented expiry date and rotation procedure. Missing rotation documentation is a High finding; missing expiry date is Critical | High |
| Rotation capability | For each long-lived credential: can it be rotated without downtime? Is there a documented rotation runbook? Is rotation automated (Lambda, cron, CI pipeline) or manual? Manual rotation without a runbook is High; no rotation capability at all is Critical for production credentials | High |
| Environment separation | Are dev, staging, and production secrets stored in separate scopes/paths/namespaces? Shared credentials across environments mean a dev compromise escalates to production | High |
| Vault appropriateness heuristic | A centralized vault (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault) adds value when: (a) the project spans 3+ deployment platforms that lack native secret stores, (b) automatic rotation is required for compliance, (c) cross-team secret sharing needs audit trails, or (d) dynamic short-lived credentials are needed. If none of these apply, platform-native stores are sufficient — flag vault adoption as over-engineering, not a gap | Medium |
| Fallback credential hygiene | When code has a primary credential path (e.g., OAuth M2M) with an env-var fallback (e.g., PAT), verify the fallback is not the de facto production path. Grep for fallback patterns: `os.environ.get("...", "")`, `or os.getenv(...)`, `except: ... fallback`. Each active fallback path should be documented and have its own rotation policy | Medium |

**Planning mode:**
- Which credential types will the system use? (OAuth M2M, PATs, API keys, JWTs, mTLS certs)
- For each credential type: what is the planned lifetime, rotation mechanism, and injection method?
- Is there a single authoritative secret store per deployment target, or will secrets be duplicated across stores?
- How will secret rotation be tested before production rollout?

**Output:** Secrets findings with file locations and remediation (rotate + remove from history if committed). Secrets strategy assessment with store inventory, rotation gaps, and appropriateness evaluation.

---

### Phase 10: Data Classification & AI Regulatory Compliance (Both modes)

Classify all data stores and data flows by sensitivity level:

| Level | Classification | Examples | Required Controls |
|-------|---------------|----------|-------------------|
| 1 | **Public** | Marketing content, public APIs, open-source code | Standard access controls |
| 2 | **Internal** | Employee data, internal docs, non-sensitive configs | Authentication required, TLS in transit |
| 3 | **Confidential** | Customer PII, financial records, business IP | Encryption at rest + in transit, access logging, need-to-know |
| 4 | **Restricted** | Payment card data (PCI), health data (HIPAA), credentials | All of above + dedicated encryption keys, audit trails, DLP |

For each data store identified in Phase 1:

1. Assign a classification level
2. Verify controls match the required level
3. Flag gaps where controls are insufficient

Also check:
- **PII in logs**: Search for logging statements that might include email, name, address, SSN, phone
- **PII in error messages**: Stack traces or error responses that expose user data
- **GDPR/CCPA**: If the system handles EU/California user data, check for consent mechanisms, data deletion capabilities, and data portability
- **Data retention**: Are there policies for how long data is kept? Are they enforced?

#### AI Regulatory Compliance

If the project trains or deploys ML models, evaluate compliance with emerging AI-specific regulations. These laws impose obligations beyond traditional data protection, targeting the AI system itself — its risk classification, transparency, and governance.

**EU AI Act** (enforceable August 2, 2026):

| Check | What to look for | Severity |
|-------|-----------------|----------|
| High-risk classification | Does any model output influence employment decisions (hiring, performance evaluation, contract renewal, task allocation, termination)? Education decisions? Credit/insurance decisions? If yes, the system is likely high-risk under Annex III. | Critical |
| Prohibited practices | Does the system use emotion recognition in the workplace? Biometric categorization to infer protected characteristics? Social scoring? If yes, these are prohibited (effective February 2025). | Critical |
| Conformity assessment | For high-risk systems: is there documentation of the intended purpose, risk management measures, training data governance, human oversight mechanisms, and accuracy/robustness metrics? | High |
| Human oversight | For high-risk systems: can a human effectively oversee the AI output and override or disregard it? Is this documented? | High |
| Transparency | For systems interacting with people: are users informed they are interacting with an AI system? For generative AI: is AI-generated content labeled? | Medium |
| Technical documentation | For high-risk systems: system description, design specifications, monitoring and logging capabilities, instructions for use, accuracy metrics, and known limitations. | High |

**Biometric data regulations:**

| Regulation | Scope | What to check | Severity |
|------------|-------|---------------|----------|
| **Illinois BIPA** | Biometric identifiers (face geometry, fingerprints, iris scans, voiceprints) and data derived from them | Written informed consent before collection; published retention/destruction policy; no sale of biometric data. Private right of action: $1,000-$5,000 per violation. | Critical |
| **CCPA/CPRA** | "Sensitive personal information" including biometric data processed to uniquely identify a consumer | Opt-in consent for processing; right to limit use; privacy policy disclosure. Applies to California residents. | High |
| **Texas CUBI / Washington WFBPA** | Biometric identifiers | Similar consent and retention requirements. Texas: no private right of action. Washington: private right of action. | High |

**EU Data Act** (applicable September 12, 2025):

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Connected product data | Does the system process data generated by IoT devices, wearables, or sensors? If yes, the EU Data Act creates portability rights for the users of those devices. | High |
| Data holder obligations | If the system holds connected product data, users have a right to access and port that data — including to third parties. This right cannot be contractually overridden. | High |
| Cloud switching | Chapter VI imposes obligations on data processing services to facilitate switching and interoperability. Relevant for SaaS/PaaS analytics platforms. | Medium |

**UK Data (Use and Access) Act 2025** (Royal Assent June 19, 2025):

| Check | What to look for | Severity |
|-------|-----------------|----------|
| UK GDPR divergence | If the system processes data of UK residents: UK now has "recognised legitimate interests" as an expanded lawful basis. Solely automated decision-making rules have been broadened. | Medium |
| EU adequacy | If data flows between EU and UK: EU adequacy decision was extended to December 27, 2025. If the system relies on adequacy (not SCCs) for cross-border transfers, verify current status. | High |

For each applicable regulation: document which requirements apply, current compliance status, and gaps requiring remediation.

**Output:** Data classification table and AI regulatory compliance assessment with gaps and required remediation.

---

### Phase 11: Monitoring & Incident Response (Both modes)

Evaluate the system's ability to detect and respond to security incidents:

#### Logging

- Are security-relevant events logged? (auth success/failure, permission changes, data access, admin actions)
- Are logs structured (JSON) and centralized?
- Are logs tamper-proof? (immutable storage, separate from application)
- Is sensitive data excluded from logs?

#### Alerting

- Are alerts configured for suspicious activity? (brute force, unusual access patterns, privilege escalation)
- Are alert thresholds appropriate? (not too noisy, not too quiet)
- Is there an on-call rotation or escalation path?

#### Audit Trails

- Can all data modifications be traced to a user and timestamp?
- Are audit logs retained long enough for compliance requirements?
- Are audit logs separate from application logs?

#### Incident Response

- Is there a documented incident response plan?
- Are there runbooks for common security incidents?
- Has the team practiced incident response (tabletop exercises)?
- Is there a communication plan for security incidents?

#### Enterprise tier additions

| Control | Purpose | Tool / Service |
|---------|---------|----------------|
| SIEM integration | Centralized security event correlation and analysis | Splunk, Datadog Security, Elastic Security, AWS Security Hub |
| Agentic SIEM | AI-assisted threat detection, triage, and response using LLM agents over security telemetry | Databricks Lakewatch, Microsoft Security Copilot (Sentinel), Google Chronicle + Gemini |
| SOC alerting rules | Predefined detection rules for common attack patterns | Sigma rules, Splunk Security Essentials, Datadog OOTB rules |
| Automated incident response | Auto-remediate common incidents (block IP, revoke token, isolate host) | AWS Lambda + Security Hub, PagerDuty Automation, Tines |
| Compliance dashboards | Map security controls to compliance frameworks | SOC2 (Vanta, Drata), ISO 27001, PCI-DSS, HIPAA |
| Threat intelligence feeds | Correlate events with known threat indicators (IOCs) | MISP, AlienVault OTX, CrowdStrike Threat Intel |
| Red team / pen testing | Periodic adversarial testing of detection capabilities | Cobalt.io, HackerOne, Synack, internal red team |

For each applicable service: document whether it is active, its configuration, and detection coverage gaps.

**Output:** Monitoring gaps table with priority and recommendations.

---

### Phase 12: Findings Report (Both modes)

Generate the final report. The format depends on the mode.

#### Planning mode report

Present the threat model and design recommendations:

```markdown
## Security Threat Model — [System Name]

### Security Surface Summary
- Entry points: [list]
- Data stores: [list]
- Auth mechanisms: [list]
- Trust boundaries: [list]

### Threat Model (STRIDE)
| Threat ID | Component | STRIDE | Description | Likelihood | Impact | Severity | Mitigation |
|-----------|-----------|--------|-------------|------------|--------|----------|------------|
| T-001 | ... | ... | ... | ... | ... | ... | ... |

### Design Recommendations
| # | Area | Recommendation | Priority |
|---|------|----------------|----------|
| 1 | Authentication | Implement OAuth 2.0 + PKCE | Critical |
| 2 | Data | Encrypt PII at rest with AES-256 | High |

### Data Classification
| Data Store | Classification | Current Controls | Required Controls | Gap |
|------------|---------------|-----------------|-------------------|-----|

### Security Design Checklist
- [ ] Authentication mechanism selected and threat-modeled
- [ ] Authorization model defined with least privilege
- [ ] Data classification completed for all stores
- [ ] Encryption strategy defined (at rest + in transit)
- [ ] Secrets management approach selected
- [ ] Logging and monitoring strategy defined
- [ ] Incident response plan drafted
```

#### Audit mode report

Present concrete findings with fix status:

```markdown
## Security Audit Report — [System Name]

### Executive Summary
- Total findings: X
- Critical: X | High: X | Medium: X | Low: X
- Fixed during audit: X
- Remaining: X

### Findings
| # | Severity | Category | File:Line | CWE | Description | Status |
|---|----------|----------|-----------|-----|-------------|--------|
| 1 | Critical | A03 Injection | src/db.py:42 | CWE-89 | SQL string concatenation | Fixed |
| 2 | High | Secrets | .env | - | API key committed to repo | Fixed |

> **Schema note:** The base columns (#, Severity, Phase, File:Line, Description, Status) are shared across all audit skills. The CWE column is specific to security-audit.

### Infrastructure Findings
| # | Severity | Resource | File:Line | Issue | Status |
|---|----------|----------|-----------|-------|--------|
| 1 | High | S3 bucket | infra/s3.tf:12 | Missing encryption | Fixed |

### Supply Chain
| Package | Current | Vulnerability | CVE | Severity | Fix Version |
|---------|---------|--------------|-----|----------|-------------|

### Recommendations
| Priority | Area | Recommendation |
|----------|------|----------------|

### Tier Coverage
| Phase | Standard | Enterprise |
|-------|----------|------------|
| Phase 0: Code Patterns | [X checks run / Y findings] | [SAST tool: configured/not configured] |
| Phase 4b: ML/AI Model Security | [X/5 serialization checks / X/4 provenance checks] | [Model scanning: configured/not configured] |
| Phase 5: Web Headers | [X/12 headers present] | [WAF headers: configured/not configured] |
| Phase 6: API Security | [X/10 checks passed] | [API gateway WAF: configured/not configured] |
| Phase 7: Auth & Session | [X/14 checks passed] | [MFA: enabled/not enabled] |
| Phase 10: AI Regulatory | [X regulations assessed / Y gaps] | [Conformity assessment: complete/not started] |
| ... | ... | ... |

### Security Posture Rating
- **Standard tier**: X/Y checks passed (Z% coverage)
- **Enterprise tier**: X/Y controls configured (Z% coverage)
- **Overall**: [Strong / Adequate / Needs Improvement / Critical Gaps]

### Ready for deployment: Yes / No (with blockers)
```

---

## Important rules

- **Fix as you go.** Don't just report — remediate. Fix Critical and High issues during the audit.
- **Evidence-based claims.** Every finding must include file path, line number, or specific evidence. Never say "probably vulnerable."
- **CWE references.** Every code vulnerability finding must include at least one CWE identifier.
- **No assumptions.** Read the actual code, configs, and IaC files. Don't assume security controls exist because a framework is used.
- **Verify fixes.** After fixing a vulnerability, re-run the check that found it to confirm the fix works.
- **Respect existing patterns.** If the project has established security patterns, extend them rather than introducing new ones.
- **Scope awareness.** Don't flag framework-managed security as a finding (e.g., CSRF protection in Django when middleware is enabled).
- **Prioritize.** Fix Critical and High findings. Track Medium and Low in the backlog. Don't let perfect be the enemy of secure.
- **Two-tier awareness.** Standard tier checks are always actionable — fix issues found. Enterprise tier items serve as a professional reference — document which are applicable and which are configured, but don't block releases on Enterprise items the team hasn't adopted yet.
