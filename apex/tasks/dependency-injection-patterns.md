---
id: dependency-injection-patterns
version: "1.0.0"
title: "Dependency Injection Patterns for React"
description: "Design DI patterns using React Context providers, service layer abstraction, and inversion of control for testable, decoupled frontend architecture"
elicit: true
owner: frontend-arch
executor: frontend-arch
outputs:
  - di-architecture-spec.md
  - service-layer-design.yaml
---

# Dependency Injection Patterns for React

## When This Task Runs

- Components have hard dependencies on APIs/services
- Testing requires mocking at module level (fragile)
- Same component needs different backends (dev/staging/prod)
- Service layer needs to be swappable (analytics, auth, storage)

## Execution Steps

### Step 1: Identify Hard Dependencies
```
SCAN project for non-injectable dependencies:
- Direct fetch/axios calls in components
- Direct localStorage/sessionStorage access
- Direct analytics calls (gtag, mixpanel)
- Direct auth SDK calls (Firebase, Supabase, Auth0)
- Direct third-party SDK usage in components

OUTPUT: Dependency inventory with coupling assessment
```

### Step 2: Select DI Strategy

**elicit: true** — Present DI approaches:

| Pattern | Complexity | Testability | Best For |
|---------|-----------|-------------|----------|
| **Context Providers** | Low | High | React-native, small apps |
| **Service Locator** | Medium | High | Larger apps, many services |
| **Factory Pattern** | Medium | High | Swappable implementations |
| **Module Injection** | Low | Medium | Simple cases, env-based |

### Step 3: Design Service Layer

```yaml
service_layer:
  services:
    - name: "ApiService"
      interface: |
        interface ApiService {
          get<T>(url: string): Promise<T>
          post<T>(url: string, data: unknown): Promise<T>
          put<T>(url: string, data: unknown): Promise<T>
          delete(url: string): Promise<void>
        }
      implementations:
        production: "FetchApiService"
        testing: "MockApiService"
        development: "FetchApiService with logging middleware"

    - name: "AuthService"
      interface: |
        interface AuthService {
          login(credentials: Credentials): Promise<User>
          logout(): Promise<void>
          getSession(): Promise<Session | null>
          onAuthChange(callback: (user: User | null) => void): Unsubscribe
        }
      implementations:
        production: "SupabaseAuthService"
        testing: "InMemoryAuthService"

    - name: "AnalyticsService"
      interface: |
        interface AnalyticsService {
          track(event: string, properties?: Record<string, unknown>): void
          identify(userId: string, traits?: Record<string, unknown>): void
          page(name: string): void
        }
      implementations:
        production: "MixpanelAnalytics"
        testing: "NoopAnalytics"
        development: "ConsoleAnalytics"

    - name: "StorageService"
      interface: |
        interface StorageService {
          get<T>(key: string): T | null
          set<T>(key: string, value: T): void
          remove(key: string): void
          clear(): void
        }
      implementations:
        production: "LocalStorageService"
        testing: "InMemoryStorageService"
        ssr: "NoopStorageService"
```

### Step 4: Implement Context-Based DI

```typescript
// Service context pattern
const ServiceContext = createContext<Services | null>(null)

function ServiceProvider({ children, services }: Props) {
  return (
    <ServiceContext.Provider value={services}>
      {children}
    </ServiceContext.Provider>
  )
}

// Hook for consuming services
function useService<K extends keyof Services>(key: K): Services[K] {
  const services = useContext(ServiceContext)
  if (!services) throw new Error('ServiceProvider missing')
  return services[key]
}

// Usage in component (decoupled)
function UserProfile() {
  const api = useService('api')
  const auth = useService('auth')
  // Component never knows about fetch, Supabase, etc.
}

// Test setup (zero module mocking)
render(
  <ServiceProvider services={createTestServices()}>
    <UserProfile />
  </ServiceProvider>
)
```

### Step 5: Validate DI Architecture

- [ ] Components don't import implementation modules directly
- [ ] All services accessible via typed hooks
- [ ] Tests use injected mocks, not module-level mocking
- [ ] Service implementations swappable without component changes
- [ ] TypeScript catches missing service implementations at compile time
- [ ] SSR-safe (no browser-only services on server)

## Quality Criteria

- Zero direct SDK/API calls in components
- All services accessed through typed context hooks
- Tests work with injected implementations only
- Service interfaces defined, not just implementations

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Decoupling | Components import hooks, not implementations |
| Testability | Tests use DI, not module mocks |
| Type safety | Service interfaces enforce contract |
| SSR safe | No browser APIs in server context |

## Handoff

- Service interfaces feed `@react-eng` for hook design
- Testing patterns feed `@react-eng` for Testing Library integration
- API layer feeds `@perf-eng` for request caching strategy
