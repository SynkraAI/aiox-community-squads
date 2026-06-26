# Task: rn-navigation-architecture

```yaml
id: rn-navigation-architecture
version: "1.0.0"
title: "React Native Navigation Architecture"
description: >
  Designs the navigation architecture for a React Native app.
  Evaluates React Navigation vs Expo Router, defines the navigator
  hierarchy (stack, tab, drawer), plans deep linking, handles auth
  flows, designs screen transitions, and documents the complete
  navigation specification.
elicit: false
owner: mobile-eng
executor: mobile-eng
outputs:
  - Navigation library evaluation and selection
  - Navigator hierarchy diagram
  - Deep linking scheme definition
  - Auth flow navigation design
  - Screen transition specifications
  - Navigation specification document
```

---

## When This Task Runs

This task runs when:
- A new React Native app needs navigation architecture from scratch
- Migrating from React Navigation v5 to v6+ or to Expo Router
- Adding deep linking support to an existing app
- Auth flow needs to be integrated with navigation (protected routes)
- Navigation performance is poor (slow transitions, memory issues)
- `*rn-navigation` or `*navigation-arch` is invoked

This task does NOT run when:
- Navigation is web-only (delegate to `@react-eng` or `@cross-plat-eng`)
- The issue is about cross-platform navigation abstraction (use `solito-navigation-setup`)
- The task is about animation within a screen (use `animation-architecture`)

---

## Execution Steps

### Step 1: Evaluate Navigation Library

Choose between React Navigation and Expo Router based on project needs.

| Criteria | React Navigation | Expo Router |
|----------|-----------------|-------------|
| **Routing model** | Imperative (JS config) | File-based (like Next.js) |
| **Deep linking** | Manual config required | Automatic from file structure |
| **Type safety** | Manual typing | Auto-generated types |
| **Web support** | Limited (react-native-web) | Full (via Expo/Metro web) |
| **Shared with Next.js** | Via Solito abstraction | Native file-based |
| **Flexibility** | Maximum control | Convention over configuration |
| **Learning curve** | Moderate | Low (familiar to Next.js devs) |
| **Dynamic routes** | Full support | `[param].tsx` convention |
| **Nested navigators** | Explicit composition | Directory-based nesting |

**Decision framework:**
- **Expo Router** if: Expo-managed workflow, want file-based routing, need auto deep links
- **React Navigation** if: Bare workflow, need maximum control, complex custom navigators

**Output:** Library selection with rationale.

### Step 2: Design Navigator Hierarchy

Define the complete navigator tree with screen groupings.

**Common patterns:**

```
Root (Stack)
├── Auth (Stack) — unauthenticated screens
│   ├── Login
│   ├── Register
│   └── ForgotPassword
├── Main (Tab) — authenticated screens
│   ├── Home (Stack)
│   │   ├── Feed
│   │   └── PostDetail
│   ├── Search (Stack)
│   │   ├── SearchMain
│   │   └── SearchResults
│   ├── Profile (Stack)
│   │   ├── ProfileMain
│   │   └── Settings
│   └── Notifications
└── Modals (Group) — overlay screens
    ├── CreatePost
    └── ImageViewer
```

**Design rules:**
- Each tab should have its own Stack navigator (independent history)
- Modal screens should use `presentation: 'modal'` or a top-level Modal group
- Auth flow should be a separate navigator switched conditionally
- Avoid nesting more than 3 levels deep (performance + complexity)
- Use `screenOptions` at navigator level, not per-screen (consistency)

**Expo Router equivalent (file structure):**
```
app/
├── (auth)/
│   ├── login.tsx
│   ├── register.tsx
│   └── forgot-password.tsx
├── (tabs)/
│   ├── _layout.tsx        # Tab navigator
│   ├── home/
│   │   ├── index.tsx
│   │   └── [postId].tsx
│   ├── search/
│   │   ├── index.tsx
│   │   └── results.tsx
│   └── profile/
│       ├── index.tsx
│       └── settings.tsx
├── modal/
│   ├── create-post.tsx
│   └── image-viewer.tsx
└── _layout.tsx             # Root Stack
```

**Output:** Navigator hierarchy diagram with screen-to-navigator mapping.

### Step 3: Define Deep Linking Scheme

Design the deep linking URL scheme that maps external URLs to screens.

**URL scheme setup:**
```
// Custom scheme for the app
myapp://home
myapp://post/123
myapp://profile/settings

// Universal links (iOS) / App Links (Android)
https://myapp.com/post/123
https://myapp.com/profile/settings
```

**Deep link configuration:**
| Screen | Path | Params | Example URL |
|--------|------|--------|-------------|
| Home | `/` | — | `myapp://home` |
| PostDetail | `/post/:id` | `id: string` | `myapp://post/abc123` |
| Profile | `/profile` | — | `myapp://profile` |
| Settings | `/profile/settings` | — | `myapp://profile/settings` |
| Search Results | `/search?q=:query` | `query: string` | `myapp://search?q=react` |

**Platform configuration:**
- **iOS:** `Info.plist` URL types + Associated Domains for universal links
- **Android:** `AndroidManifest.xml` intent filters + `assetlinks.json` for App Links
- **Expo:** `app.json` → `expo.scheme` + `expo.ios.associatedDomains`

**Testing deep links:**
```bash
# iOS Simulator
xcrun simctl openurl booted "myapp://post/123"

# Android Emulator
adb shell am start -W -a android.intent.action.VIEW -d "myapp://post/123"

# Expo
npx uri-scheme open "myapp://post/123" --ios
```

**Output:** Complete deep linking scheme with platform configuration.

### Step 4: Design Auth Flow Navigation

Implement authentication-aware navigation that protects routes.

**Pattern: Conditional navigator switching**
```typescript
function RootNavigator() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <SplashScreen />;
  }

  return isAuthenticated ? <MainNavigator /> : <AuthNavigator />;
}
```

**Auth flow states:**
| State | Navigator | Screens |
|-------|-----------|---------|
| Loading | Splash | SplashScreen (checking token) |
| Unauthenticated | Auth Stack | Login, Register, ForgotPassword |
| Authenticated | Main Tabs | Home, Search, Profile, etc. |
| Token expired | Auth Stack | Auto-redirect to Login with returnUrl |

**Key requirements:**
- Token refresh should happen transparently (no flash of login screen)
- Deep links to protected routes should redirect to login, then forward after auth
- Logout should reset navigation state (prevent back-to-authenticated-screen)
- Biometric auth (Face ID / fingerprint) should be a separate screen in Auth flow

**Output:** Auth flow navigation design with state transitions.

### Step 5: Plan Screen Transitions

Design custom screen transitions that feel native and performant.

**Default transitions by platform:**
| Type | iOS Default | Android Default |
|------|-------------|-----------------|
| Stack push | Slide from right | Fade + slide up |
| Stack pop | Slide to right | Fade + slide down |
| Modal present | Slide from bottom | Slide from bottom |
| Modal dismiss | Slide to bottom | Slide to bottom |
| Tab switch | Cross-fade | Cross-fade |

**Custom transition requirements:**
- All transitions must run on UI thread (Reanimated)
- Duration: 250-350ms for standard, 200ms for quick actions
- Use spring physics for natural feel: `damping: 20, stiffness: 300`
- Shared element transitions for content continuity (list → detail)
- Respect `prefers-reduced-motion` (instant transition if enabled)

**Shared element transitions (React Navigation 7+):**
```typescript
// Source screen
<SharedElement id={`post.${id}.image`}>
  <Image source={post.image} />
</SharedElement>

// Destination screen
<SharedElement id={`post.${id}.image`}>
  <Image source={post.image} style={styles.heroImage} />
</SharedElement>
```

**Output:** Screen transition specifications per navigation type.

### Step 6: Document Navigation Architecture

Compile the complete navigation specification.

**Documentation includes:**
- Library selection rationale (from Step 1)
- Navigator hierarchy diagram (from Step 2)
- Deep linking scheme table (from Step 3)
- Auth flow state diagram (from Step 4)
- Transition specifications (from Step 5)
- Navigation-related TypeScript types
- Testing strategy for navigation flows

**Output:** Complete navigation specification document.

---

## Quality Criteria

- Navigator hierarchy must not exceed 3 levels of nesting
- All screens must be reachable via deep link
- Auth flow must handle token expiry without flashing wrong screen
- Screen transitions must run at 60fps on UI thread
- Deep linking must be tested on both iOS and Android

---

*Squad Apex — React Native Navigation Architecture Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-rn-navigation-architecture
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Navigator hierarchy must not exceed 3 levels of nesting"
    - "All screens must be reachable via deep link"
    - "Auth flow must handle token expiry gracefully"
    - "Screen transitions must run at 60fps on UI thread"
    - "Deep linking tested on both iOS and Android"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@cross-plat-eng` or `@apex-lead` |
| Artifact | Navigation architecture document with hierarchy, deep linking, auth flow, and transition specs |
| Next action | Implement cross-platform navigation via `@cross-plat-eng` or validate with `cross-platform-test-setup` via `@qa-xplatform` |
