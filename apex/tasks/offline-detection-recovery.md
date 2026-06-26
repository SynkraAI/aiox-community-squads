---
id: offline-detection-recovery
version: "1.0.0"
title: "Offline Detection & Recovery"
description: "Design offline-first patterns: network state detection, mutation queue, sync strategies, cached data display, and PWA offline support"
elicit: true
owner: react-eng
executor: react-eng
outputs:
  - offline-strategy-spec.md
  - sync-architecture.yaml
---

# Offline Detection & Recovery

## When This Task Runs

- App needs to work without network connection
- Users on unstable connections (mobile, low bandwidth)
- Forms need to queue submissions when offline
- PWA offline support needed
- `*apex-error-boundary` identified offline gaps

## Execution Steps

### Step 1: Assess Offline Requirements

**elicit: true** — Define offline scope:

| Capability | Needed? | Priority |
|-----------|---------|----------|
| **Read cached data** | Yes/No | View previously loaded content |
| **Queue mutations** | Yes/No | Submit forms when back online |
| **Background sync** | Yes/No | Auto-sync queued changes |
| **Offline-first** | Yes/No | App works fully offline (SW + IndexedDB) |
| **Stale indicator** | Yes/No | Show data age badge when offline |

### Step 2: Design Network Detection

```yaml
network_detection:
  apis:
    - "navigator.onLine (boolean, limited reliability)"
    - "online/offline events (transition detection)"
    - "Network Information API (connection type, downlink)"
    - "Heartbeat ping (reliable but adds traffic)"

  implementation:
    hook: "useNetworkStatus"
    returns:
      online: "boolean"
      connectionType: "4g | 3g | 2g | slow-2g | unknown"
      effectiveType: "string"
      downlink: "number (Mbps estimate)"
      rtt: "number (round trip time ms)"
      saveData: "boolean (user prefers reduced data)"

  reliability:
    strategy: "Combine navigator.onLine + heartbeat for critical apps"
    heartbeat_interval: "30s when app is active"
    heartbeat_endpoint: "/api/health (returns 204)"
    debounce: "500ms before announcing state change"
```

### Step 3: Design Offline Data Strategy

```yaml
offline_data:
  cache_layers:
    - layer: "Service Worker cache"
      stores: "Static assets, API responses"
      strategy: "stale-while-revalidate for content, cache-first for assets"

    - layer: "React Query / SWR cache"
      stores: "API response data"
      strategy: "Show stale data, refetch when online"
      config: |
        const queryClient = new QueryClient({
          defaultOptions: {
            queries: {
              staleTime: 5 * 60 * 1000,
              gcTime: 24 * 60 * 60 * 1000,
              networkMode: 'offlineFirst',
            }
          }
        })

    - layer: "IndexedDB (Dexie)"
      stores: "User data, drafts, queued mutations"
      strategy: "Persist important user data for offline access"

  stale_indicator:
    when: "Data is from cache, not fresh"
    ui: "Badge: 'Dados de {tempo atrás}' + subtle background change"
    a11y: "aria-label includes data freshness"
```

### Step 4: Design Mutation Queue

```yaml
mutation_queue:
  trigger: "Network unavailable during form submission or action"

  queue_structure:
    storage: "IndexedDB"
    schema: |
      {
        id: string,           // Unique mutation ID
        action: string,       // 'create' | 'update' | 'delete'
        endpoint: string,     // API endpoint
        payload: object,      // Request body
        timestamp: number,    // When queued
        retries: number,      // Retry count
        status: string,       // 'pending' | 'syncing' | 'failed' | 'synced'
      }

  sync_strategy:
    trigger: "online event + heartbeat confirmation"
    order: "FIFO (oldest first)"
    conflict_resolution: "Last-write-wins (server timestamp)"
    max_retries: 3
    backoff: "1s → 2s → 4s"

  user_feedback:
    queued: "Toast: 'Salvo offline. Será enviado quando reconectar.'"
    syncing: "Badge: 'Sincronizando {n} alterações...'"
    synced: "Toast: 'Todas as alterações sincronizadas.'"
    failed: "Alert: 'Falha ao sincronizar. Tente manualmente.'"
    conflict: "Modal: 'Conflito detectado. Qual versão manter?'"
```

### Step 5: Design Offline UI

```yaml
offline_ui:
  banner:
    position: "Top of viewport, below header"
    style: "Warning color, dismissible"
    content: "Sem conexão. Você pode continuar usando dados salvos."
    auto_dismiss: "When connection restored"

  disabled_features:
    approach: "Visually dim + tooltip explaining why"
    examples:
      - "Search: disabled, shows 'Disponível quando conectar'"
      - "Payment: disabled, shows 'Requer conexão'"
      - "Real-time: paused, shows last known state"

  available_features:
    approach: "Normal appearance, works from cache"
    examples:
      - "Read cached content"
      - "Fill and queue forms"
      - "Navigate cached pages"

  reconnection:
    animation: "Banner slides away"
    sync: "Auto-sync queued mutations"
    notification: "Toast: 'Conexão restaurada. Sincronizando...'"
```

### Step 6: Validate Offline Strategy

- [ ] App detects online/offline transitions reliably
- [ ] Cached data displayed when offline
- [ ] Forms queue mutations for later sync
- [ ] Sync resolves without data loss
- [ ] Offline UI is clear (not confusing)
- [ ] Reconnection triggers auto-sync

## Quality Criteria

- Reliable network state detection
- Zero data loss during offline→online transitions
- User always knows they're offline
- Queued mutations sync in correct order

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Detection | Online/offline detected within 2s |
| Data | Cached data visible offline |
| Queue | Mutations queued and synced |
| UI | Offline state clearly communicated |

## Handoff

- Service worker config feeds `@perf-eng` for caching strategy
- Offline UI feeds `@interaction-dsgn` for empty/error state design
- Sync architecture feeds `@frontend-arch` for data layer design
