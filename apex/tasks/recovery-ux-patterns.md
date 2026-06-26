> **DEPRECATED** — Scope absorbed into `offline-detection-recovery.md`. See `data/task-consolidation-map.yaml`.

---
id: recovery-ux-patterns
version: "1.0.0"
title: "Error Recovery UX Patterns"
description: "Design error recovery experiences: retry strategies, partial failure handling, graceful degradation, reconnection flows, and user-facing error communication"
elicit: true
owner: react-eng
executor: react-eng
outputs:
  - recovery-ux-spec.md
  - error-handling-patterns.yaml
---

# Error Recovery UX Patterns

## When This Task Runs

- App needs error handling beyond technical error boundaries
- Users encounter white screens or cryptic error messages
- Network errors need graceful handling
- Partial page failures need isolation strategy
- `*apex-error-boundary` audit identified gaps

## Execution Steps

### Step 1: Map Error Scenarios
```
IDENTIFY all error scenarios in the app:
- Network failures (offline, timeout, DNS)
- API errors (400, 401, 403, 404, 500)
- Runtime errors (null reference, type errors)
- Data errors (invalid response shape, empty data)
- Auth errors (expired session, revoked access)
- Rate limiting (429 Too Many Requests)
- External service failures (payment, maps, analytics)

OUTPUT: Error scenario catalog + current handling assessment
```

### Step 2: Design Error Hierarchy

**elicit: true** — Confirm error severity levels:

| Level | User Impact | UX Pattern |
|-------|-------------|------------|
| **Informational** | Feature degraded, not blocked | Subtle toast, badge |
| **Recoverable** | Action failed, can retry | Inline error + retry button |
| **Section failure** | Part of page unavailable | Error card with retry, rest works |
| **Page failure** | Page cannot render | Full-page error with navigation |
| **App failure** | Nothing works | Minimal error page, support link |

### Step 3: Design Recovery Patterns

```yaml
recovery_patterns:
  auto_retry:
    trigger: "Network error or 5xx response"
    strategy: "Exponential backoff: 1s → 2s → 4s → stop"
    max_retries: 3
    user_feedback: "Subtle spinner, then manual retry button"
    cancel: "User can cancel and proceed without data"

  manual_retry:
    trigger: "After auto-retry exhausted, or user-visible error"
    ui: "Error message + 'Tentar novamente' button"
    on_retry: "Reset error state, re-fetch, show loading"
    on_give_up: "Alternative path or contact support"

  partial_failure:
    trigger: "One section fails, rest of page is fine"
    ui: "Failed section shows error card, rest renders normally"
    isolation: "Error boundary per section (React ErrorBoundary)"
    retry: "Retry button remounts the failed section only"

  graceful_degradation:
    trigger: "Non-critical service unavailable"
    examples:
      - "Analytics fails → log locally, don't show error"
      - "Chat widget fails → hide chat, show email alternative"
      - "Maps fails → show address text instead of map"
    rule: "Never block core functionality for optional services"

  session_recovery:
    trigger: "Auth token expired during use"
    ui: "Modal: 'Sua sessão expirou. Faça login novamente.'"
    preserve: "Save unsaved form data to localStorage before redirect"
    resume: "After login, restore saved data and return to same page"

  offline_recovery:
    trigger: "Network disconnected"
    detection: "navigator.onLine + online/offline events"
    ui: "Banner: 'Sem conexão. Alterações serão salvas quando reconectar.'"
    queue: "Queue mutations, sync when online"
    read: "Show cached data with 'offline' badge"
```

### Step 4: Design Error Communication

```yaml
error_messages:
  principles:
    - "Tell the user WHAT happened (not HTTP 500)"
    - "Tell the user WHAT TO DO (not just 'try again later')"
    - "Be empathetic, not blaming"
    - "Provide alternatives when possible"

  examples:
    bad: "Error 500: Internal Server Error"
    good: "Não conseguimos carregar seus dados. Tente novamente ou entre em contato."

    bad: "Network Error"
    good: "Parece que você está sem conexão. Verifique sua internet e tente novamente."

    bad: "null is not an object"
    good: "Algo inesperado aconteceu. Nossa equipe foi notificada."

  templates:
    - type: "network"
      title: "Sem conexão"
      message: "Verifique sua internet e tente novamente."
      action: "Tentar novamente"

    - type: "server"
      title: "Erro no servidor"
      message: "Nosso time foi notificado. Tente novamente em alguns minutos."
      action: "Tentar novamente"

    - type: "not_found"
      title: "Página não encontrada"
      message: "O conteúdo que você procura não existe ou foi removido."
      action: "Voltar para o início"

    - type: "auth"
      title: "Sessão expirada"
      message: "Faça login novamente para continuar."
      action: "Fazer login"
```

### Step 5: Design Error Boundary Architecture

```yaml
error_boundary_layers:
  layer_1_app:
    scope: "Entire application"
    catches: "Unrecoverable React errors"
    fallback: "Minimal error page with support contact"
    reports: "Error tracking service (Sentry)"

  layer_2_route:
    scope: "Per page/route"
    catches: "Page-level render errors"
    fallback: "Error page with navigation intact"
    retry: "Remount page on retry"

  layer_3_section:
    scope: "Independent UI sections"
    catches: "Section render errors"
    fallback: "Error card with retry button"
    isolation: "Rest of page unaffected"

  layer_4_component:
    scope: "Critical inline content"
    catches: "Component-level errors"
    fallback: "Inline placeholder"
    retry: "Auto-retry once, then manual"
```

### Step 6: Validate Error Recovery

- [ ] No white screens (every render error has boundary)
- [ ] User-friendly messages (no technical jargon)
- [ ] Retry mechanism for all recoverable errors
- [ ] Partial failures don't crash full page
- [ ] Offline mode shows cached data
- [ ] Unsaved data preserved on auth expiry

## Quality Criteria

- Zero white screens in production
- All error messages are user-friendly
- Retry mechanism for every recoverable error
- Error boundaries at 4 architectural layers

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Coverage | Every error scenario has designed handling |
| Messages | All user-facing, no technical jargon |
| Retry | Recoverable errors have retry path |
| Isolation | Section failure doesn't crash page |

## Handoff

- Error boundary architecture feeds `@react-eng` for implementation
- Error UI specs feed `@interaction-dsgn` for empty/error state design
- Offline patterns feed `@perf-eng` for service worker strategy
- Error reporting feeds `@frontend-arch` for monitoring setup
