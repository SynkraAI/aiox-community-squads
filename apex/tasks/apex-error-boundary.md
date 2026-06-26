# Task: apex-error-boundary

```yaml
id: apex-error-boundary
version: "1.0.0"
title: "Apex Error Boundary Architecture"
description: >
  Designs and implements error boundary architecture for the project.
  Audits existing boundaries, identifies unprotected routes and async components,
  designs a layered boundary strategy, and implements recovery patterns.
elicit: false
owner: apex-lead
executor: react-eng
dependencies:
  - tasks/apex-scan.md
  - tasks/apex-discover-routes.md
  - tasks/apex-discover-components.md
outputs:
  - Error boundary audit report
  - Boundary architecture recommendation
  - Implementation plan
```

---

## Command

### `*apex-error-boundary`

Audits and designs error boundary architecture for the project.

---

## How It Works

### Step 1: Audit Current Error Boundaries

```yaml
audit:
  scan_for:
    - "class components with componentDidCatch / getDerivedStateFromError"
    - "ErrorBoundary from react-error-boundary library"
    - "error.tsx / error.js files (Next.js App Router)"
    - "Custom error boundary implementations"

  per_boundary:
    component: "{name}"
    path: "{file path}"
    type: "class | react-error-boundary | next-error | custom"
    wraps: "[{components/routes protected}]"
    has_fallback_ui: true | false
    has_reset_action: true | false
    has_error_reporting: true | false
    has_retry_mechanism: true | false
```

### Step 2: Identify Unprotected Areas

```yaml
unprotected:
  routes_without_boundary:
    description: "Routes/pages with no error boundary in their component tree"
    severity: CRITICAL
    risk: "Unhandled error = white screen for the user"

  async_without_suspense_boundary:
    description: "Async components (React.lazy, data fetching) without Suspense + ErrorBoundary"
    severity: HIGH
    risk: "Network failure = unrecoverable crash"

  third_party_without_boundary:
    description: "Third-party components (maps, charts, embeds) without isolation boundary"
    severity: HIGH
    risk: "Third-party crash takes down the entire page"

  form_without_error_handling:
    description: "Forms with server actions but no error boundary for submission failures"
    severity: MEDIUM
    risk: "Failed submission = lost user input"
```

### Step 3: Design Layered Boundary Strategy

```yaml
boundary_layers:
  layer_1_app:
    description: "Top-level catch-all — prevents white screen of death"
    location: "App root / layout.tsx"
    fallback: "Full-page error with 'Go Home' + 'Try Again'"
    error_reporting: true
    catches: "Any unhandled error that escapes lower boundaries"

  layer_2_route:
    description: "Per-route boundary — isolates page crashes"
    location: "Each route/page wrapper"
    fallback: "Page-level error with 'Go Back' + 'Retry'"
    catches: "Route-specific errors without affecting navigation"

  layer_3_feature:
    description: "Feature-level boundary — isolates widget/section crashes"
    location: "Around complex features (charts, maps, rich editors)"
    fallback: "Inline error with 'Retry' or degraded content"
    catches: "Feature crash without affecting the rest of the page"

  layer_4_component:
    description: "Granular boundary — around third-party or unstable components"
    location: "Around individual risky components"
    fallback: "Placeholder or hidden"
    catches: "Component crash with minimal visual impact"
```

### Step 4: Recovery Patterns

```yaml
recovery_patterns:
  retry:
    description: "Reset error state and re-render the subtree"
    implementation: "resetErrorBoundary() from react-error-boundary or key prop change"
    use_when: "Transient errors (network, race conditions)"

  fallback_content:
    description: "Show degraded but functional content"
    implementation: "FallbackComponent with reduced functionality"
    use_when: "Non-critical feature failure (chart fails → show table)"

  redirect:
    description: "Navigate away from broken page"
    implementation: "useRouter().push() in fallback component"
    use_when: "Unrecoverable route error"

  report_and_dismiss:
    description: "Log error, show brief message, continue"
    implementation: "Toast notification + error logger"
    use_when: "Background feature failure that doesn't block user"
```

### Step 5: Output

```yaml
output_format: |
  ## Error Boundary Audit

  **Existing Boundaries:** {count}
  **Unprotected Routes:** {unprotected_routes}
  **Unprotected Async:** {unprotected_async}

  ### Current Coverage
  | Boundary | Type | Protects | Fallback UI | Reset | Report |
  |----------|------|----------|-------------|-------|--------|
  | AppError | react-error-boundary | App root | Yes | Yes | No |

  ### Gaps Found
  | Gap | Count | Severity | Risk |
  |-----|-------|----------|------|
  | Routes without boundary | {n} | CRITICAL | White screen |
  | Async without boundary | {n} | HIGH | Unrecoverable crash |
  | Third-party without isolation | {n} | HIGH | Cascade failure |

  ### Recommended Architecture
  - Layer 1 (App): {status}
  - Layer 2 (Route): {n} boundaries needed
  - Layer 3 (Feature): {n} boundaries needed
  - Layer 4 (Component): {n} boundaries needed

  ### Options
  1. Implement all layers ({total} boundaries)
  2. Start with CRITICAL only (routes)
  3. Just the audit report
```

---

## Veto Conditions

```yaml
veto_conditions:
  - id: VC-EB-001
    condition: "Route has no error boundary in component tree"
    action: "WARN — Unhandled error in this route causes white screen of death."
    available_check: "manual"
    on_unavailable: MANUAL_CHECK
```

---

*Apex Squad — Error Boundary Architecture Task v1.0.0*
