---
id: module-federation-design
version: "1.0.0"
title: "Module Federation Architecture"
description: "Design micro-frontend architecture with Module Federation: shared dependencies, runtime integration, versioning strategy, and fallback patterns"
elicit: true
owner: frontend-arch
executor: frontend-arch
outputs:
  - module-federation-spec.md
  - federation-config.yaml
---

# Module Federation Architecture

## When This Task Runs

- Multiple teams need independent deploy cycles
- Large app needs to be split into micro-frontends
- Runtime composition of independently deployed modules
- Shared design system across federated apps

## Execution Steps

### Step 1: Assess Federation Need
```
ANALYZE project for micro-frontend indicators:
- Team size (>2 teams working on same frontend)
- Deploy frequency mismatch (some parts change daily, others monthly)
- Technology diversity need (different frameworks per section)
- Independent scaling requirements
- App size (>100 components, >50 routes)

OUTPUT: Federation justification (or recommendation against)
```

### Step 2: Select Federation Strategy

**elicit: true** — Present architecture options:

| Strategy | Runtime | Build-time | Best For |
|----------|---------|------------|----------|
| **Webpack Module Federation** | Yes | No | Webpack 5+ projects, shared deps |
| **Vite Module Federation** | Yes | No | Vite projects (@originjs/vite-plugin-federation) |
| **Import Maps** | Yes | No | Framework-agnostic, browser-native |
| **Next.js Multi-Zones** | Partial | Partial | Next.js projects, URL-based routing |
| **Single-SPA** | Yes | No | Multiple frameworks in one app |

### Step 3: Design Federation Architecture

```yaml
federation:
  host:
    name: "{shell-app}"
    framework: "{next | vite | webpack}"
    responsibilities:
      - "Routing shell"
      - "Authentication"
      - "Layout (header, sidebar, footer)"
      - "Shared state (user, theme)"

  remotes:
    - name: "{feature-module-1}"
      exposes:
        - "./Component" : "Standalone feature component"
        - "./routes" : "Feature route definitions"
      shared_deps: ["react", "react-dom", "@scope/ui"]
      deploy_independently: true
      fallback: "Loading skeleton or error boundary"

    - name: "{feature-module-2}"
      exposes:
        - "./Widget" : "Embeddable widget"
      shared_deps: ["react", "react-dom"]
      deploy_independently: true

  shared_dependencies:
    singleton:
      - "react"
      - "react-dom"
      - "react-router-dom"
    version_strategy: "eager for shell, lazy for remotes"
    fallback: "If version mismatch, load own copy"
```

### Step 4: Design Failure Handling

```yaml
failure_handling:
  remote_unavailable:
    detection: "Dynamic import timeout (5s)"
    fallback: "Error boundary with retry button"
    user_impact: "Feature unavailable, rest of app works"

  version_mismatch:
    shared_dep: "Load own copy (bundle size increase)"
    breaking_api: "Version pinning + compatibility layer"

  network_degradation:
    strategy: "Cache remote entry in service worker"
    ttl: "24 hours"
    offline: "Show cached version or placeholder"
```

### Step 5: Validate Federation Architecture

- [ ] Each remote builds and deploys independently
- [ ] Host app works even if remotes are unavailable
- [ ] Shared dependencies are truly shared (not duplicated)
- [ ] Error boundaries isolate remote failures
- [ ] No shared mutable state between remotes (event bus only)
- [ ] Type safety across remote boundaries

## Quality Criteria

- Independent deployability of each remote
- Graceful degradation when remotes fail
- Shared dependency deduplication verified
- Type contracts between host and remotes

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Independence | Each remote deploys alone |
| Resilience | Host works with remotes down |
| Bundle | Shared deps not duplicated |
| Types | Type contracts enforced |

## Handoff

- Remote boundaries feed `@react-eng` for component interface design
- Bundle analysis feeds `@perf-eng` for shared dep optimization
- Error boundaries feed error-boundary-architecture task
