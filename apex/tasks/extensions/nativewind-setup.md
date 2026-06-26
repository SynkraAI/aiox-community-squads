# Task: nativewind-setup

```yaml
id: nativewind-setup
version: "1.0.0"
title: "NativeWind Setup & Architecture"
description: >
  Sets up NativeWind (Tailwind CSS for React Native) in a cross-platform
  monorepo. Configures shared Tailwind config, handles platform-specific
  styling differences, integrates with design tokens, sets up dark mode,
  and establishes responsive design patterns that work across 320px mobile
  to 2560px desktop. Produces a universal styling architecture.
elicit: false
owner: cross-plat-eng
executor: cross-plat-eng
outputs:
  - NativeWind installation and configuration
  - Shared Tailwind config (colors, spacing, typography, breakpoints)
  - Platform-specific styling patterns
  - Dark mode configuration
  - Responsive design patterns (320px → 2560px)
  - NativeWind architecture specification document
```

---

## When This Task Runs

This task runs when:
- Setting up styling for a new cross-platform monorepo
- Migrating from platform-specific styles to NativeWind
- Tailwind config needs to be shared between web and native
- Responsive design patterns need to work on both platforms
- Dark mode needs consistent implementation across platforms
- `*nativewind` or `*nativewind-setup` is invoked

This task does NOT run when:
- Web-only Tailwind setup (delegate to `@css-eng`)
- Design token architecture without NativeWind (use `shared-tokens-setup`)
- Animation styling (use `moti-animation-architecture`)

---

## Execution Steps

### Step 1: Install and Configure NativeWind

Set up NativeWind v4 in the monorepo.

**Installation:**
```bash
# In the shared UI package
cd packages/ui
npm install nativewind tailwindcss

# For React Native
npm install nativewind@^4

# Dev dependencies
npm install -D tailwindcss@^3.4
```

**Tailwind config (`packages/ui/tailwind.config.ts`):**
```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/**/*.{ts,tsx}',
    // Include all packages that use NativeWind classes
    '../../packages/app/**/*.{ts,tsx}',
  ],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      // Design tokens go here (Step 2)
    },
  },
  plugins: [],
};

export default config;
```

**Metro configuration (React Native):**
```javascript
// metro.config.js
const { withNativeWind } = require('nativewind/metro');

const config = {
  // ... existing metro config
};

module.exports = withNativeWind(config, {
  input: './global.css',
});
```

**Next.js integration:**
```javascript
// next.config.js (NativeWind + Next.js)
const { withNativeWind } = require('nativewind/next');

module.exports = withNativeWind({
  // ... existing next config
}, {
  input: './global.css',
});
```

**Global CSS import:**
```css
/* global.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Output:** NativeWind configured for both web and native platforms.

### Step 2: Design Shared Tailwind Config

Create a unified design token configuration.

**Color tokens:**
```typescript
theme: {
  extend: {
    colors: {
      // Brand colors
      brand: {
        50: '#eff6ff',
        100: '#dbeafe',
        500: '#3b82f6',
        600: '#2563eb',
        900: '#1e3a5f',
      },
      // Semantic colors
      surface: {
        DEFAULT: 'var(--color-surface)',
        elevated: 'var(--color-surface-elevated)',
        inverse: 'var(--color-surface-inverse)',
      },
      content: {
        DEFAULT: 'var(--color-content)',
        secondary: 'var(--color-content-secondary)',
        inverse: 'var(--color-content-inverse)',
      },
      // Status colors
      success: { DEFAULT: '#22c55e', light: '#bbf7d0' },
      warning: { DEFAULT: '#f59e0b', light: '#fef3c7' },
      error: { DEFAULT: '#ef4444', light: '#fecaca' },
    },
  },
}
```

**Spacing tokens:**
```typescript
spacing: {
  // 4px grid system
  '0.5': '2px',
  '1': '4px',
  '2': '8px',
  '3': '12px',
  '4': '16px',
  '5': '20px',
  '6': '24px',
  '8': '32px',
  '10': '40px',
  '12': '48px',
  '16': '64px',
  '20': '80px',
},
```

**Typography tokens:**
```typescript
fontFamily: {
  sans: ['Inter', 'system-ui', 'sans-serif'],
  mono: ['JetBrains Mono', 'monospace'],
},
fontSize: {
  xs: ['12px', { lineHeight: '16px' }],
  sm: ['14px', { lineHeight: '20px' }],
  base: ['16px', { lineHeight: '24px' }],
  lg: ['18px', { lineHeight: '28px' }],
  xl: ['20px', { lineHeight: '28px' }],
  '2xl': ['24px', { lineHeight: '32px' }],
  '3xl': ['30px', { lineHeight: '36px' }],
},
```

**Border radius tokens:**
```typescript
borderRadius: {
  sm: '6px',
  DEFAULT: '8px',
  md: '12px',
  lg: '16px',
  xl: '24px',
  full: '9999px',
},
```

**Output:** Shared Tailwind config with complete token set.

### Step 3: Handle Platform-Specific Styling

Address styling differences between web and native.

**Platform differences in NativeWind:**
| Feature | Web | Native | Workaround |
|---------|-----|--------|------------|
| `hover:` | Works | No hover | Use `active:` on native |
| `focus-visible:` | Works | Limited | Platform check |
| Box shadow | Full CSS | Limited (elevation on Android) | Use `shadow-` classes |
| `backdrop-blur` | Works | No support | Platform variant |
| `overflow: hidden` | Works | Works differently | Test both |
| `position: fixed` | Works | Not supported | Use `absolute` on native |
| Text wrapping | Automatic | Must be inside `<Text>` | Always use `<Text>` |

**Platform variant pattern:**
```tsx
// Use platform: prefix in className (NativeWind v4)
<View className="
  p-4 rounded-lg bg-white
  web:shadow-lg web:hover:shadow-xl
  native:shadow-md native:elevation-4
">
```

**Platform-specific utility classes:**
```typescript
// In tailwind.config.ts plugins
plugins: [
  ({ addUtilities }) => {
    addUtilities({
      '.elevation-1': {
        elevation: 1,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.1,
        shadowRadius: 2,
      },
      '.elevation-4': {
        elevation: 4,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.15,
        shadowRadius: 8,
      },
    });
  },
],
```

**Output:** Platform-specific styling patterns and utilities.

### Step 4: Configure Dark Mode

Set up dark mode that works on both web and native.

**Tailwind dark mode configuration:**
```typescript
// tailwind.config.ts
{
  darkMode: 'class', // Use class strategy for both platforms
}
```

**CSS variables for theme:**
```css
/* global.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --color-surface: #ffffff;
    --color-surface-elevated: #f8fafc;
    --color-content: #0f172a;
    --color-content-secondary: #64748b;
  }

  .dark {
    --color-surface: #0f172a;
    --color-surface-elevated: #1e293b;
    --color-content: #f1f5f9;
    --color-content-secondary: #94a3b8;
  }
}
```

**Theme provider (cross-platform):**
```tsx
import { useColorScheme } from 'nativewind';

function ThemeProvider({ children }) {
  const { colorScheme, setColorScheme, toggleColorScheme } = useColorScheme();

  return (
    <ThemeContext.Provider value={{ colorScheme, toggleColorScheme }}>
      <View className={colorScheme === 'dark' ? 'dark' : ''}>
        {children}
      </View>
    </ThemeContext.Provider>
  );
}
```

**Dark mode usage:**
```tsx
<View className="bg-surface dark:bg-surface">
  <Text className="text-content dark:text-content">
    Adapts to theme automatically
  </Text>
</View>
```

**Output:** Dark mode configuration working on web and native.

### Step 5: Design Responsive Patterns

Create responsive design patterns for 320px → 2560px range.

**NativeWind breakpoints:**
```typescript
screens: {
  sm: '640px',   // Large phones landscape
  md: '768px',   // Tablets portrait
  lg: '1024px',  // Tablets landscape / small desktop
  xl: '1280px',  // Desktop
  '2xl': '1536px', // Large desktop
},
```

**Responsive patterns:**
```tsx
// Stack on mobile, row on desktop
<View className="flex-col sm:flex-row gap-4">
  <View className="w-full sm:w-1/2">Left</View>
  <View className="w-full sm:w-1/2">Right</View>
</View>

// Responsive padding
<View className="p-4 md:p-6 lg:p-8">

// Responsive text
<Text className="text-base md:text-lg lg:text-xl">

// Responsive grid
<View className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
```

**React Native Dimensions (where breakpoints don't apply):**
```tsx
import { useWindowDimensions } from 'react-native';

function ResponsiveLayout({ children }) {
  const { width } = useWindowDimensions();
  const columns = width < 640 ? 1 : width < 1024 ? 2 : 3;

  return (
    <FlatList
      numColumns={columns}
      key={columns} // Force re-render on column change
      data={items}
      renderItem={renderItem}
    />
  );
}
```

**Output:** Responsive design patterns for the full viewport range.

### Step 6: Document NativeWind Architecture

Compile the complete NativeWind specification.

**Documentation includes:**
- Installation and configuration (from Step 1)
- Design token reference (from Step 2)
- Platform-specific patterns (from Step 3)
- Dark mode setup (from Step 4)
- Responsive patterns (from Step 5)
- className vs style prop guidelines
- Common pitfalls and solutions

**Output:** Complete NativeWind architecture specification document.

---

## Quality Criteria

- NativeWind must resolve classes correctly on both Metro (native) and Webpack (web)
- Design tokens must produce visually consistent results across platforms
- Dark mode must switch seamlessly without flicker
- Responsive layouts must work from 320px to 2560px
- No hardcoded style values that bypass the token system

---

*Squad Apex — NativeWind Setup & Architecture Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-nativewind-setup
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Classes resolve correctly on Metro and Webpack"
    - "Design tokens produce consistent visuals across platforms"
    - "Dark mode switches without flicker"
    - "Responsive layouts work 320px to 2560px"
    - "No hardcoded values bypassing token system"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@css-eng` or `@apex-lead` |
| Artifact | NativeWind architecture with shared config, dark mode, responsive patterns, and platform utilities |
| Next action | Apply to components via `@cross-plat-eng` or integrate with design system via `@design-sys-eng` |
