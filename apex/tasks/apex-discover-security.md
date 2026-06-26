# Task: apex-discover-security

```yaml
id: apex-discover-security
version: "1.0.0"
title: "Frontend Security Discovery"
description: >
  Scans frontend code for security vulnerabilities. Detects XSS
  vectors, unsafe patterns, exposed secrets, insecure storage, and
  missing security headers. Frontend-specific security audit that
  complements backend security. Transforms "is our frontend secure?"
  into "I already scanned every file — here's the threat landscape."
elicit: false
owner: apex-lead
executor: frontend-arch
dependencies:
  - tasks/apex-scan.md
outputs:
  - XSS vulnerability inventory (dangerouslySetInnerHTML, eval, href)
  - Exposed secrets scan (API keys, tokens in source)
  - Insecure storage audit (localStorage with sensitive data)
  - Insecure fetch patterns (HTTP, missing CSRF)
  - Unvalidated redirect detection
  - Security headers check (CSP, X-Frame-Options)
  - Security health score (0-100)
```

---

## Command

### `*discover-security`

Scans the project for frontend security vulnerabilities. Runs as part of `*apex-audit` or independently.

---

## Discovery Phases

### Phase 1: Scan Security Patterns

```yaml
pattern_scan:
  scan:
    - "src/**/*.tsx"
    - "src/**/*.jsx"
    - "src/**/*.ts"
    - "src/**/*.js"
    - "app/**/*.tsx"
    - "app/**/*.ts"
    - "packages/**/src/**/*.ts"
    - "packages/**/src/**/*.tsx"
  exclude:
    - "**/node_modules/**"
    - "**/*.test.*"
    - "**/*.spec.*"
    - "**/*.d.ts"

  also_scan:
    config_files:
      - "next.config.js"
      - "next.config.mjs"
      - "next.config.ts"
      - "vite.config.ts"
      - "vercel.json"
      - ".env.example"
    html_files:
      - "index.html"
      - "public/index.html"
      - "app/layout.tsx"

  secret_patterns:
    api_key: "(api[_-]?key|apikey)\\s*[:=]\\s*['\"][a-zA-Z0-9_-]{20,}['\"]"
    token: "(token|secret|password|auth)\\s*[:=]\\s*['\"][^'\"]{8,}['\"]"
    aws: "AKIA[0-9A-Z]{16}"
    stripe: "sk_(live|test)_[a-zA-Z0-9]{20,}"
    firebase: "AIza[0-9A-Za-z_-]{35}"
    jwt: "eyJ[a-zA-Z0-9_-]*\\.eyJ[a-zA-Z0-9_-]*\\."
    private_key: "-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----"
```

### Phase 2: Detect Vulnerabilities

```yaml
vulnerability_detection:
  - id: xss_dangerouslySetInnerHTML
    scan: "dangerouslySetInnerHTML"
    condition: "Using dangerouslySetInnerHTML without DOMPurify sanitization"
    severity: CRITICAL
    impact: "Attacker can inject and execute arbitrary JavaScript"
    check_mitigation: "DOMPurify.sanitize() wrapping the input"
    suggestion: "Always sanitize with DOMPurify: dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(html) }}"

  - id: xss_href_javascript
    scan: "href={, href=\"javascript:"
    condition: "`href='javascript:'` or `href={userInput}` without URL validation"
    severity: CRITICAL
    impact: "JavaScript execution via link click"
    suggestion: "Validate URLs against allowlist, reject javascript: protocol"

  - id: xss_eval
    scan: "eval(, new Function(, setTimeout( with string arg"
    condition: "Use of eval(), new Function(), or setTimeout/setInterval with string argument"
    severity: CRITICAL
    impact: "Arbitrary code execution, common XSS vector"
    suggestion: "Replace eval with JSON.parse, use function references for timers"

  - id: target_blank_no_rel
    scan: "target=\"_blank\", target='_blank'"
    condition: "`target='_blank'` without `rel='noopener noreferrer'`"
    severity: MEDIUM
    impact: "Opened page can access window.opener (tabnabbing attack)"
    suggestion: "Add rel='noopener noreferrer' to all target='_blank' links"

  - id: exposed_secrets
    scan: "API key patterns, hardcoded tokens"
    condition: "API keys, tokens, or passwords hardcoded in source code (not env vars)"
    severity: CRITICAL
    impact: "Secrets exposed in client bundle, accessible to anyone"
    note: "NEXT_PUBLIC_ vars with sensitive names also flagged (they're in client bundle)"
    suggestion: "Move to server-side env vars, use API routes as proxy"

  - id: insecure_storage
    scan: "localStorage.setItem, sessionStorage.setItem"
    condition: "Sensitive data (tokens, PII, passwords) stored in localStorage/sessionStorage"
    severity: HIGH
    impact: "XSS attack can steal all stored data, no encryption"
    detect_sensitive: "token, jwt, password, email, ssn, credit, auth"
    suggestion: "Use httpOnly cookies for auth tokens, avoid storing PII client-side"

  - id: insecure_fetch
    scan: "fetch(, axios(, http://"
    condition: "HTTP (not HTTPS) API calls in production code"
    severity: HIGH
    impact: "Data transmitted in plaintext, man-in-the-middle attack"
    exclude: "localhost, 127.0.0.1 (dev only)"
    suggestion: "Always use HTTPS for API calls"

  - id: missing_csrf
    scan: "method: 'POST', method: 'PUT', method: 'DELETE'"
    condition: "Form POST/mutation without CSRF token"
    severity: MEDIUM
    impact: "Cross-site request forgery — attacker can submit forms on behalf of user"
    note: "SameSite cookies and Next.js server actions mitigate this"
    suggestion: "Add CSRF token or verify SameSite cookie configuration"

  - id: unvalidated_redirect
    scan: "window.location, router.push, router.replace, redirect("
    condition: "`window.location = userInput` or `router.push(userInput)` without validation"
    severity: HIGH
    impact: "Open redirect — attacker redirects user to phishing site"
    suggestion: "Validate redirect URL against allowlist of internal paths"

  - id: console_log_sensitive
    scan: "console.log, console.debug, console.info"
    condition: "console.log with sensitive data (passwords, tokens, user data objects)"
    severity: MEDIUM
    impact: "Sensitive data visible in browser DevTools"
    suggestion: "Remove console.log with sensitive data, use structured logging"

  - id: iframe_no_sandbox
    scan: "<iframe"
    condition: "`<iframe>` without sandbox attribute"
    severity: MEDIUM
    impact: "Embedded content has full access to parent page APIs"
    suggestion: "Add sandbox attribute with minimal permissions"
```

### Phase 3: Check Security Headers

```yaml
security_headers:
  scan:
    - "next.config.js (headers function)"
    - "vercel.json (headers)"
    - "index.html (meta tags)"
    - "app/layout.tsx (metadata)"

  check:
    csp:
      detect: "Content-Security-Policy header or meta tag"
      severity_if_missing: MEDIUM
      impact: "No restriction on script sources — XSS has wider attack surface"
      suggestion: "Add CSP header restricting script-src, style-src"

    x_frame_options:
      detect: "X-Frame-Options header"
      severity_if_missing: LOW
      impact: "Page can be embedded in iframe (clickjacking)"
      note: "CSP frame-ancestors supersedes this"
      suggestion: "Add X-Frame-Options: DENY or use CSP frame-ancestors"

    referrer_policy:
      detect: "Referrer-Policy header or meta tag"
      severity_if_missing: LOW
      impact: "Full URL leaked to external sites via Referer header"
      suggestion: "Add Referrer-Policy: strict-origin-when-cross-origin"

    permissions_policy:
      detect: "Permissions-Policy header"
      severity_if_missing: LOW
      impact: "Browser features (camera, microphone, geolocation) not restricted"
      suggestion: "Add Permissions-Policy to restrict unused browser features"
```

### Phase 4: Health Score

```yaml
health_score:
  # **Score Formula SSoT:** `data/health-score-formulas.yaml#discover-security`. The inline formula below is kept for reference but the YAML file is authoritative.
  formula: >
    100 - (xss_critical_count * 20) - (exposed_secrets_count * 20)
    - (insecure_storage_count * 10) - (unvalidated_redirect_count * 10)
    - (insecure_fetch_count * 8) - (iframe_no_sandbox_count * 5)
    - (missing_csrf_count * 5) - (console_sensitive_count * 3)
    - (target_blank_count * 2)
  max: 100
  min: 0
  thresholds:
    secure: ">= 90 — no critical vulnerabilities, good security posture"
    mostly_secure: "70-89 — minor issues, no critical exposures"
    vulnerable: "50-69 — significant security gaps"
    critical: "< 50 — critical vulnerabilities require immediate attention"
```

---

## Output Format

```
FRONTEND SECURITY DISCOVERY
=============================
Project: {name}
Security Score: {score}/100 ({secure | mostly_secure | vulnerable | critical})
Critical Issues: {count}
Total Issues: {count}

VULNERABILITY SCAN
--------------------
 Severity | Category                  | Count | Files
----------|---------------------------|-------|------
 CRITICAL | XSS (dangerouslySetHTML)  | 1     | RichText.tsx
 CRITICAL | Exposed API key           | 1     | api-config.ts
 HIGH     | Insecure storage (token)  | 2     | auth.ts, session.ts
 HIGH     | Unvalidated redirect      | 1     | callback.tsx
 MEDIUM   | target="_blank" no rel    | 3     | Footer.tsx, Links.tsx
 MEDIUM   | console.log (user data)   | 2     | UserProfile.tsx, debug.ts

CRITICAL FINDINGS (fix immediately)
--------------------------------------
 XSS  RichText.tsx:42
   dangerouslySetInnerHTML={{ __html: content }}
   No DOMPurify sanitization detected.
   FIX: import DOMPurify from 'dompurify'
        dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(content) }}

 SECRET  api-config.ts:8
   const API_KEY = "sk_live_abc123def456..."
   Hardcoded Stripe key in source code — exposed in client bundle.
   FIX: Move to server-side env var, use API route as proxy.

HIGH FINDINGS
--------------
 STORAGE  auth.ts:15
   localStorage.setItem('auth_token', token)
   Auth token in localStorage — vulnerable to XSS theft.
   FIX: Use httpOnly cookie via API response header.

 REDIRECT  callback.tsx:22
   router.push(searchParams.get('redirect'))
   Unvalidated redirect — attacker controls destination.
   FIX: Validate against allowlist of internal paths.

SECURITY HEADERS
------------------
 Header                | Status  | Impact
-----------------------|---------|-------
 Content-Security-Policy | MISSING | No script source restriction
 X-Frame-Options        | OK      | DENY
 Referrer-Policy        | MISSING | Full URL leaked to externals
 Permissions-Policy     | MISSING | Browser features unrestricted

MEDIUM/LOW FINDINGS
---------------------
 BLANK  Footer.tsx:28 — target="_blank" without rel="noopener noreferrer"
 BLANK  Links.tsx:15, Links.tsx:22 — same issue (2 occurrences)
 LOG    UserProfile.tsx:45 — console.log(userData) exposes PII in DevTools
 LOG    debug.ts:12 — console.log(authResponse) exposes tokens

=============================
Next steps:
  1. FIX CRITICAL: Sanitize dangerouslySetInnerHTML in RichText.tsx
  2. FIX CRITICAL: Remove hardcoded API key from api-config.ts
  3. FIX HIGH: Move auth token to httpOnly cookie
  4. FIX HIGH: Validate redirect URL in callback.tsx
  5. Add Content-Security-Policy header

What do you want to do?
```

---

## Integration with Other Tasks

```yaml
feeds_into:
  apex-suggest:
    what: "Security vulnerabilities become proactive suggestions"
    how: "XSS, exposed secrets, insecure storage flagged automatically"

  apex-audit:
    what: "Security health score feeds audit report"
    how: "Health score becomes part of project readiness assessment"

  frontend-arch:
    what: "Architecture receives security threat map"
    how: "Knows which patterns to avoid and which mitigations are missing"

  apex-code-review:
    what: "Security dimension in code review"
    how: "New code checked against security patterns automatically"
```

---

## Veto Conditions

```yaml
veto_conditions:
  - id: VC-DISC-SEC-001
    condition: "dangerouslySetInnerHTML found without DOMPurify sanitization"
    action: VETO
    severity: CRITICAL
    blocking: true
    feeds_gate: QG-AX-010
    available_check: "manual"
    on_unavailable: MANUAL_CHECK

  - id: VC-DISC-SEC-002
    condition: "Exposed API key or secret in source code"
    action: VETO
    severity: CRITICAL
    blocking: true
    feeds_gate: QG-AX-010
    available_check: "manual"
    on_unavailable: MANUAL_CHECK
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | apex-lead (routing enrichment), frontend-arch (security architecture), apex-code-review (security checks) |
| Next action | User fixes critical vulnerabilities first, then high/medium, or continues to other commands |

---

## Cache

```yaml
cache:
  location: ".aios/apex-context/security-cache.yaml"
  ttl: "Until source files change"
  invalidate_on:
    - "Any .ts/.tsx/.js/.jsx file created, deleted, or modified"
    - ".env or .env.* files modified"
    - "Config files modified (next.config, vercel.json)"
    - "User runs *discover-security explicitly"
```

---

## Edge Cases

```yaml
edge_cases:
  - condition: "Static site with no API calls"
    action: "ADAPT — focus on XSS vectors and exposed secrets only, skip fetch/CSRF checks"
  - condition: "No sensitive data handling (brochure site)"
    action: "REPORT — score 100 if no vulnerabilities found"
  - condition: "SSR project (Next.js with server components)"
    action: "ADAPT — also scan server-side code for secrets, separate client/server findings"
  - condition: "Monorepo with multiple apps"
    action: "ADAPT — scan each app independently, report per-app scores"
  - condition: "Third-party scripts (analytics, chat widgets)"
    action: "WARN — flag external scripts as potential attack surface, check CSP coverage"
```

---

`schema_ref: data/discovery-output-schema.yaml`

---

*Apex Squad — Frontend Security Discovery Task v1.0.0*
