# Task: rn-performance-optimization

```yaml
id: rn-performance-optimization
version: "1.0.0"
title: "React Native Performance Optimization"
description: >
  Diagnoses and resolves React Native performance bottlenecks.
  Profiles JS thread, UI thread, and bridge usage. Identifies
  unnecessary re-renders, heavy computations on JS thread,
  bridge serialization overhead, and memory leaks. Produces
  optimization plan with measurable before/after metrics.
elicit: false
owner: mobile-eng
executor: mobile-eng
outputs:
  - Performance profile report (JS thread, UI thread, bridge)
  - Re-render analysis with component tree hotspots
  - Memory leak detection results
  - Optimization plan with priority ranking
  - Before/after FPS and TTI metrics
```

---

## When This Task Runs

This task runs when:
- App drops below 60fps during interactions or scrolling
- JS thread utilization exceeds 80% causing UI jank
- Memory usage grows unbounded over time (leak suspected)
- Bridge serialization is a bottleneck (large data transfers)
- Startup time (TTI) exceeds acceptable thresholds
- `*rn-perf` or `*rn-performance` is invoked

This task does NOT run when:
- The performance issue is web-only (delegate to `@perf-eng`)
- The issue is purely animation-related (use `animation-architecture`)
- The issue is network/API latency (not a RN performance problem)

---

## Execution Steps

### Step 1: Profile the Application

Run performance profiling to establish baseline metrics.

**JS Thread profiling:**
- Enable Hermes profiling: `hermes-profile-transformer`
- Capture a 10-second trace during the problematic interaction
- Identify functions consuming >5% of JS thread time
- Flag synchronous operations blocking the JS thread

**UI Thread profiling:**
- Use Flipper Performance plugin or `react-native-perf-monitor`
- Measure FPS during: app launch, navigation, scrolling, gesture interactions
- Identify frames that take >16ms (below 60fps threshold)

**Bridge profiling (Old Architecture):**
- Enable `MessageQueue.spy` to log bridge traffic
- Identify high-frequency bridge calls (>100/second)
- Measure serialization overhead for large payloads
- Flag `JSON.stringify` of large objects crossing the bridge

**New Architecture profiling:**
- Verify Fabric renderer is active
- Check TurboModule adoption (vs legacy native modules)
- Verify JSI bindings are synchronous (no async bridge fallback)

**Baseline metrics to capture:**
| Metric | Target | Tool |
|--------|--------|------|
| JS FPS | 60fps | Perf Monitor |
| UI FPS | 60fps | Perf Monitor |
| TTI (Time to Interactive) | <2s | Flipper |
| Memory (after 5min use) | Stable | Xcode Instruments / Android Profiler |
| Bridge calls/sec | <50 | MessageQueue.spy |

**Output:** Baseline performance profile with bottleneck identification.

### Step 2: Analyze Re-renders

Identify unnecessary React re-renders that waste JS thread cycles.

**Detection methods:**
- Use `React.Profiler` to measure render counts and durations
- Enable React DevTools Profiler highlight updates
- Use `why-did-you-render` library for detailed re-render reasons

**Common re-render causes in RN:**
| Cause | Detection | Fix |
|-------|-----------|-----|
| Inline objects in props | `style={{ margin: 10 }}` | Extract to `StyleSheet.create` or `useMemo` |
| Inline functions | `onPress={() => doSomething(id)}` | `useCallback` with proper deps |
| Context without selector | `useContext(BigContext)` | Split context or use `useSyncExternalStore` |
| FlatList missing keys | Items re-mount on every render | Add stable `keyExtractor` |
| FlatList `renderItem` inline | New function every render | Extract component + `React.memo` |
| Parent re-render cascading | Parent state change re-renders all children | `React.memo` on pure children |

**FlatList optimization checklist:**
- `keyExtractor` returns stable, unique keys
- `renderItem` is a named component wrapped in `React.memo`
- `getItemLayout` provided for fixed-height items (skips measurement)
- `initialNumToRender` set to visible items count
- `maxToRenderPerBatch` tuned (default 10)
- `windowSize` tuned based on item height and screen size
- `removeClippedSubviews={true}` for long lists on Android

**Output:** Re-render hotspot map with specific fix recommendations.

### Step 3: Optimize JS Thread

Move heavy computations off the JS thread.

**Strategies:**
| Strategy | When | Implementation |
|----------|------|----------------|
| Reanimated worklets | Animation calculations | `'worklet';` directive, `runOnUI` |
| InteractionManager | Post-navigation setup | `InteractionManager.runAfterInteractions()` |
| Web Workers (Hermes) | CPU-intensive computation | `new Worker()` with Hermes |
| useDeferredValue | Non-urgent UI updates | Wrap slow-rendering values |
| Lazy initialization | Heavy state init | `useState(() => expensiveInit())` |

**Hermes-specific optimizations:**
- Verify Hermes is enabled (`global.HermesInternal !== undefined`)
- Use Hermes bytecode precompilation for faster startup
- Avoid `eval()` and `new Function()` (Hermes doesn't optimize these)
- Prefer `for` loops over `Array.map/filter/reduce` for hot paths

**Output:** JS thread optimization plan with implementation details.

### Step 4: Address Memory Leaks

Detect and fix memory leaks that degrade performance over time.

**Common RN memory leak sources:**
| Source | Detection | Fix |
|--------|-----------|-----|
| Uncleared timers | `setTimeout`/`setInterval` without cleanup | Clear in `useEffect` cleanup |
| Event listeners | `addEventListener` without `removeEventListener` | Remove in cleanup |
| Reanimated shared values | `useSharedValue` in unmounted component | Cancel animations on unmount |
| Image cache | Unbounded image cache growth | Set `Image.cacheSize` limit |
| Navigation listeners | `navigation.addListener` without unsubscribe | Return unsubscribe from `useEffect` |
| Closures holding refs | Callbacks capturing stale component refs | Use `useRef` for mutable refs |

**Detection process:**
1. Open Memory profiler (Xcode Instruments / Android Studio Profiler)
2. Navigate through 5 screens back and forth 3 times
3. Take heap snapshot after each round
4. Compare snapshots — retained objects should not grow
5. Identify objects that survive GC despite component unmount

**Output:** Memory leak inventory with fixes.

### Step 5: Optimize Startup Time

Reduce Time to Interactive (TTI) for app launch.

**Startup phases and optimizations:**
| Phase | Optimization |
|-------|-------------|
| Native init | Reduce native module count, lazy-load non-essential modules |
| JS bundle load | Hermes bytecode, inline requires, RAM bundles |
| React tree mount | Reduce initial component tree, defer non-visible content |
| Data fetch | Prefetch critical data, use placeholder/skeleton screens |
| Navigation ready | Lazy-load non-initial screens with `React.lazy` |

**Inline requires pattern:**
```typescript
// Instead of top-level import (loads at startup)
// import HeavyModule from './HeavyModule';

// Use inline require (loads on first use)
const getHeavyModule = () => require('./HeavyModule').default;
```

**Output:** Startup optimization plan with estimated TTI improvement.

### Step 6: Create Optimization Report

Compile all findings into a structured report with before/after metrics.

**Report structure:**
- Executive summary (key bottlenecks found)
- Baseline metrics table
- Optimization plan (ordered by impact × effort)
- Estimated post-optimization metrics
- Platform-specific notes (iOS vs Android differences)
- Monitoring recommendations (ongoing perf tracking)

**Output:** Complete optimization report with actionable plan.

---

## Quality Criteria

- Every optimization must have measurable before/after metrics
- FlatList optimizations must be verified with >1000 item lists
- Memory leak fixes must be verified with heap snapshot comparison
- JS thread optimizations must show reduced CPU utilization
- Startup optimizations must show reduced TTI

---

*Squad Apex — React Native Performance Optimization Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-rn-performance-optimization
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Every optimization must have measurable before/after metrics"
    - "FPS must not drop below 60fps during profiled interactions"
    - "Memory must remain stable after 5 minutes of use"
    - "Startup TTI must be within defined threshold"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@perf-eng` or `@apex-lead` |
| Artifact | Performance profile, re-render analysis, optimization plan with before/after metrics |
| Next action | Implement optimizations via `@mobile-eng` or validate with `performance-budget-review` via `@perf-eng` |
