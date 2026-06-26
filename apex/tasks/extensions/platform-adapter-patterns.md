# Task: platform-adapter-patterns

```yaml
id: platform-adapter-patterns
version: "1.0.0"
title: "Platform Adapter Patterns"
description: >
  Designs and implements the adapter pattern for cross-platform code
  that must differ between web and native. Covers platform file
  extensions (.web.tsx/.native.tsx), Platform.select patterns,
  capability detection, progressive enhancement, and adapter
  testing strategy. Produces reusable adapter patterns that
  maximize shared code while handling real platform differences.
elicit: false
owner: cross-plat-eng
executor: cross-plat-eng
outputs:
  - Adapter pattern catalog (when to use which pattern)
  - Platform file extension conventions
  - Capability detection utilities
  - Progressive enhancement patterns
  - Adapter testing strategy
  - Platform adapter specification document
```

---

## When This Task Runs

This task runs when:
- A feature requires different implementations on web vs native
- Platform-specific code is scattered without clear pattern
- Need to add a new platform (e.g., adding native to web-only app)
- Existing Platform.OS checks are unmaintainable
- `*platform-adapters` or `*adapters` is invoked

This task does NOT run when:
- The component is identical on both platforms (use NativeWind or shared code)
- The task is about navigation abstraction (use `solito-navigation-setup`)
- The difference is purely styling (use `shared-tokens-setup` or NativeWind)

---

## Execution Steps

### Step 1: Classify Platform Differences

Categorize what differs between platforms and choose the right pattern.

**Classification matrix:**
| Difference Type | Example | Pattern |
|----------------|---------|---------|
| Same logic, same UI | Button with `onPress` | Shared component (no adapter) |
| Same logic, different UI | Dropdown (select on web, ActionSheet on native) | Platform files |
| Same logic, minor UI diff | Padding (4px web, 8pt native) | `Platform.select` |
| Different API, same result | LocalStorage (web) vs AsyncStorage (native) | Adapter module |
| Platform-only feature | Haptics (native only), hover (web only) | Capability detection |
| Rendering engine diff | `<div>` vs `<View>`, `<p>` vs `<Text>` | Base component library |

**Decision tree:**
```
Is the code identical on both platforms?
  YES → Shared code, no adapter needed
  NO → Is it a minor style difference?
    YES → Platform.select({ web: ..., native: ... })
    NO → Is it the same intent with different implementation?
      YES → Platform file extensions (.web.tsx / .native.tsx)
      NO → Is it a platform-only feature?
        YES → Capability detection + progressive enhancement
```

**Output:** Platform difference classification for the project.

### Step 2: Implement Platform File Extension Pattern

Set up the file extension convention for platform-specific code.

**File structure:**
```
packages/ui/src/
├── Button/
│   ├── Button.tsx          # Re-exports platform variant
│   ├── Button.types.ts     # Shared types
│   ├── Button.web.tsx      # Web implementation
│   ├── Button.native.tsx   # Native implementation
│   └── Button.test.tsx     # Shared behavior tests
├── Dropdown/
│   ├── Dropdown.tsx         # Re-exports
│   ├── Dropdown.types.ts    # Shared types
│   ├── Dropdown.web.tsx     # <select> element
│   └── Dropdown.native.tsx  # ActionSheet / BottomSheet
```

**Re-export file pattern:**
```typescript
// Button/Button.tsx
// Metro and webpack resolve .web.tsx / .native.tsx automatically
// This file is the fallback if no platform extension matches
export { Button } from './Button.native'; // Default to native
```

**Metro configuration (React Native):**
```javascript
// metro.config.js
module.exports = {
  resolver: {
    sourceExts: ['native.tsx', 'native.ts', 'tsx', 'ts', 'jsx', 'js'],
  },
};
```

**Webpack/Next.js configuration (web):**
```javascript
// next.config.js
module.exports = {
  webpack: (config) => {
    config.resolve.extensions = [
      '.web.tsx', '.web.ts', '.web.jsx', '.web.js',
      ...config.resolve.extensions,
    ];
    return config;
  },
};
```

**Naming conventions:**
| Extension | Platform | Bundler |
|-----------|----------|---------|
| `.web.tsx` | Web (Next.js, CRA) | Webpack, Turbopack |
| `.native.tsx` | iOS + Android | Metro |
| `.ios.tsx` | iOS only | Metro |
| `.android.tsx` | Android only | Metro |
| `.tsx` (no extension) | Fallback / shared | All |

**Output:** Platform file extension conventions with bundler configuration.

### Step 3: Build Adapter Modules

Create adapter modules for platform-specific APIs.

**Storage adapter:**
```typescript
// packages/app/adapters/storage.ts (shared interface)
export interface StorageAdapter {
  getItem(key: string): Promise<string | null>;
  setItem(key: string, value: string): Promise<void>;
  removeItem(key: string): Promise<void>;
}

// packages/app/adapters/storage.web.ts
export const storage: StorageAdapter = {
  getItem: async (key) => localStorage.getItem(key),
  setItem: async (key, value) => localStorage.setItem(key, value),
  removeItem: async (key) => localStorage.removeItem(key),
};

// packages/app/adapters/storage.native.ts
import AsyncStorage from '@react-native-async-storage/async-storage';
export const storage: StorageAdapter = {
  getItem: AsyncStorage.getItem,
  setItem: AsyncStorage.setItem,
  removeItem: AsyncStorage.removeItem,
};
```

**Common adapters needed:**
| Adapter | Web | Native |
|---------|-----|--------|
| Storage | `localStorage` | `AsyncStorage` |
| Clipboard | `navigator.clipboard` | `@react-native-clipboard` |
| Share | `navigator.share` | `Share` API (RN) |
| Haptics | No-op | `expo-haptics` |
| Biometrics | WebAuthn | `expo-local-authentication` |
| Camera | `getUserMedia` | `expo-camera` |
| File system | File API | `expo-file-system` |
| Notifications | Push API | `expo-notifications` |

**Adapter design rules:**
- One adapter file per capability domain
- Shared interface in `.ts`, platform implementations in `.web.ts` / `.native.ts`
- Adapters should be async (even if web is sync) for interface consistency
- No-op implementations for platform-only features (e.g., haptics on web)
- Type-safe: shared interface enforced on both implementations

**Output:** Adapter modules for all platform-specific APIs used in the project.

### Step 4: Implement Capability Detection

Detect platform capabilities at runtime for progressive enhancement.

**Capability detection utility:**
```typescript
// packages/app/utils/capabilities.ts
import { Platform } from 'react-native';

export const capabilities = {
  // Platform detection
  isWeb: Platform.OS === 'web',
  isNative: Platform.OS !== 'web',
  isIOS: Platform.OS === 'ios',
  isAndroid: Platform.OS === 'android',

  // Feature detection
  hasHaptics: Platform.OS !== 'web',
  hasHover: Platform.OS === 'web',
  hasBiometrics: Platform.OS !== 'web',
  hasShareSheet: true, // Both web (navigator.share) and native

  // Runtime detection (async)
  async canUseBiometrics(): Promise<boolean> {
    if (Platform.OS === 'web') return false;
    const { isEnrolledAsync } = await import('expo-local-authentication');
    return isEnrolledAsync();
  },

  async canUseCamera(): Promise<boolean> {
    if (Platform.OS === 'web') {
      return 'mediaDevices' in navigator;
    }
    const { getCameraPermissionsAsync } = await import('expo-camera');
    const { status } = await getCameraPermissionsAsync();
    return status === 'granted';
  },
};
```

**Usage in components:**
```tsx
import { capabilities } from '@app/utils/capabilities';

function ActionButton({ onPress }) {
  const handlePress = async () => {
    if (capabilities.hasHaptics) {
      const { impactAsync } = await import('expo-haptics');
      await impactAsync();
    }
    onPress();
  };

  return (
    <Pressable
      onPress={handlePress}
      // Hover effect only on web
      {...(capabilities.hasHover && {
        onHoverIn: () => setHovered(true),
        onHoverOut: () => setHovered(false),
      })}
    >
      {children}
    </Pressable>
  );
}
```

**Output:** Capability detection utilities with async feature checking.

### Step 5: Design Adapter Testing Strategy

Plan how to test platform-specific code on both platforms.

**Testing layers:**
| Layer | Tests | How |
|-------|-------|-----|
| Shared interface | Contract tests | Test against interface type |
| Web adapter | Unit tests | Jest with jsdom |
| Native adapter | Unit tests | Jest with react-native preset |
| Integration | Parity tests | Same test suite, different runner |

**Shared behavior test pattern:**
```typescript
// Button.test.tsx (runs on both platforms)
import { render, fireEvent } from '@testing-library/react-native';
import { Button } from './Button';

describe('Button (shared behavior)', () => {
  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <Button onPress={onPress}>Click me</Button>
    );
    fireEvent.press(getByText('Click me'));
    expect(onPress).toHaveBeenCalledTimes(1);
  });

  it('does not call onPress when disabled', () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <Button onPress={onPress} disabled>Click me</Button>
    );
    fireEvent.press(getByText('Click me'));
    expect(onPress).not.toHaveBeenCalled();
  });
});
```

**Adapter contract test pattern:**
```typescript
// storage.contract-test.ts
import { StorageAdapter } from './storage';

export function testStorageAdapter(storage: StorageAdapter) {
  it('stores and retrieves values', async () => {
    await storage.setItem('key', 'value');
    expect(await storage.getItem('key')).toBe('value');
  });

  it('returns null for missing keys', async () => {
    expect(await storage.getItem('nonexistent')).toBeNull();
  });

  it('removes values', async () => {
    await storage.setItem('key', 'value');
    await storage.removeItem('key');
    expect(await storage.getItem('key')).toBeNull();
  });
}

// storage.web.test.ts
import { storage } from './storage.web';
import { testStorageAdapter } from './storage.contract-test';
describe('WebStorage', () => testStorageAdapter(storage));

// storage.native.test.ts
import { storage } from './storage.native';
import { testStorageAdapter } from './storage.contract-test';
describe('NativeStorage', () => testStorageAdapter(storage));
```

**Output:** Adapter testing strategy with shared behavior and contract tests.

### Step 6: Document Platform Adapter Specification

Compile the complete adapter pattern documentation.

**Documentation includes:**
- Classification matrix (from Step 1)
- File extension conventions (from Step 2)
- Adapter module catalog (from Step 3)
- Capability detection API (from Step 4)
- Testing strategy (from Step 5)
- Decision flowchart for choosing the right pattern
- Migration guide for converting platform-scattered code to adapters

**Output:** Complete platform adapter specification document.

---

## Quality Criteria

- Platform files must resolve correctly in both Metro and Webpack
- Adapter interfaces must be identical on both platforms (TypeScript enforced)
- Capability detection must not crash on unsupported platforms
- Contract tests must pass on both web and native
- No `Platform.OS` checks scattered in component code (centralize in adapters)

---

*Squad Apex — Platform Adapter Patterns Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-platform-adapter-patterns
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Platform files resolve correctly in Metro and Webpack"
    - "Adapter interfaces identical on both platforms"
    - "Capability detection handles all platforms without crashes"
    - "Contract tests pass on both web and native"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@react-eng` or `@apex-lead` |
| Artifact | Platform adapter specification with patterns, adapters, capability detection, and testing strategy |
| Next action | Apply adapter patterns to components via `@cross-plat-eng` or test parity via `@qa-xplatform` |
