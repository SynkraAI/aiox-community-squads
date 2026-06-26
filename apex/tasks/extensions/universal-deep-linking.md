# Task: universal-deep-linking

```yaml
id: universal-deep-linking
version: "1.0.0"
title: "Universal Deep Linking"
description: >
  Designs and implements deep linking that works across web (URLs),
  iOS (Universal Links), and Android (App Links). Handles deferred
  deep links, authentication-gated routes, fallback behavior when
  app is not installed, attribution tracking, and URL scheme
  management. Produces a complete deep linking architecture.
elicit: false
owner: cross-plat-eng
executor: cross-plat-eng
outputs:
  - URL scheme design (custom + universal links)
  - Platform configuration (iOS, Android, web)
  - Deferred deep link handling
  - Auth-gated deep link flow
  - Fallback behavior specification
  - Deep linking architecture document
```

---

## When This Task Runs

This task runs when:
- App needs deep linking from external sources (email, push, QR, social)
- Universal Links (iOS) or App Links (Android) need configuration
- Deferred deep links needed (install app first, then navigate)
- Push notifications need to navigate to specific screens
- Deep link conflicts between web and native need resolution
- `*deep-linking` or `*universal-links` is invoked

This task does NOT run when:
- Internal app navigation only (use `solito-navigation-setup`)
- Navigation architecture design (use `rn-navigation-architecture`)
- Web-only URL routing (delegate to `@react-eng`)

---

## Execution Steps

### Step 1: Design URL Scheme

Define the complete URL scheme supporting all entry points.

**Three link types:**
| Type | Format | Opens |
|------|--------|-------|
| Custom scheme | `myapp://users/123` | App directly (if installed) |
| Universal Link (iOS) | `https://myapp.com/users/123` | App (if installed) or website |
| App Link (Android) | `https://myapp.com/users/123` | App (if installed) or website |

**URL scheme design:**
```
Domain: myapp.com
Custom scheme: myapp://

Routes:
  /                          → Home
  /users                     → User list
  /users/:id                 → User detail
  /users/:id/posts           → User's posts
  /settings                  → Settings
  /invite/:code              → Invite code handler
  /reset-password/:token     → Password reset
  /share/:type/:id           → Shared content
```

**URL parameter standards:**
- Path params for resource IDs: `/users/abc123`
- Query params for filters/options: `/users?sort=name&page=2`
- Fragment for section targeting: `/settings#notifications`
- Reserved params: `utm_source`, `utm_medium`, `utm_campaign` (attribution)

**Output:** Complete URL scheme with all routes and parameter types.

### Step 2: Configure Platform-Specific Setup

Set up Universal Links (iOS) and App Links (Android).

**iOS Universal Links:**

1. Apple App Site Association file (`/.well-known/apple-app-site-association`):
```json
{
  "applinks": {
    "details": [
      {
        "appIDs": ["TEAMID.com.myapp.ios"],
        "components": [
          { "/": "/users/*", "comment": "User routes" },
          { "/": "/settings", "comment": "Settings" },
          { "/": "/invite/*", "comment": "Invite links" },
          { "/": "/share/*", "comment": "Shared content" }
        ]
      }
    ]
  }
}
```

2. Xcode configuration:
- Associated Domains: `applinks:myapp.com`
- In `Info.plist` or `app.json`:
```json
{
  "expo": {
    "ios": {
      "associatedDomains": ["applinks:myapp.com"]
    }
  }
}
```

**Android App Links:**

1. Digital Asset Links (`/.well-known/assetlinks.json`):
```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.myapp.android",
    "sha256_cert_fingerprints": ["AA:BB:CC:..."]
  }
}]
```

2. AndroidManifest.xml intent filter:
```xml
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="https" android:host="myapp.com" />
</intent-filter>
```

**Expo configuration (both platforms):**
```json
{
  "expo": {
    "scheme": "myapp",
    "ios": {
      "associatedDomains": ["applinks:myapp.com"]
    },
    "android": {
      "intentFilters": [
        {
          "action": "VIEW",
          "autoVerify": true,
          "data": [{ "scheme": "https", "host": "myapp.com" }],
          "category": ["BROWSABLE", "DEFAULT"]
        }
      ]
    }
  }
}
```

**Output:** Platform configuration for iOS, Android, and web.

### Step 3: Handle Deferred Deep Links

Implement deep links that survive app installation.

**Deferred deep link flow:**
1. User taps link → app not installed
2. Redirect to App Store / Play Store
3. User installs and opens app
4. App retrieves original deep link → navigates to target

**Implementation options:**
| Method | Complexity | Reliability |
|--------|-----------|-------------|
| Clipboard-based | Low | Low (user may clear clipboard) |
| Branch.io / Firebase Dynamic Links | Low (SDK) | High (tracks install) |
| Server-side with fingerprint | Medium | Medium |
| Custom server with install token | High | High |

**Minimal implementation (server-based):**
```typescript
// On first app open after install
async function handleDeferredDeepLink() {
  const installReferrer = await getInstallReferrer(); // Platform API
  if (installReferrer?.url) {
    const route = parseDeepLink(installReferrer.url);
    router.replace(route);
  }
}
```

**Expo implementation:**
```typescript
import * as Linking from 'expo-linking';

// Get initial URL (app opened via deep link)
const initialUrl = await Linking.getInitialURL();

// Listen for deep links while app is running
Linking.addEventListener('url', ({ url }) => {
  const route = parseDeepLink(url);
  router.push(route);
});
```

**Output:** Deferred deep link handling with selected strategy.

### Step 4: Design Auth-Gated Deep Links

Handle deep links that target authenticated-only screens.

**Auth-gated flow:**
```
Deep link: myapp://users/123
  ├── User is authenticated?
  │   ├── YES → Navigate to /users/123
  │   └── NO → Save target route
  │       └── Show login screen
  │           └── Login success?
  │               ├── YES → Navigate to saved /users/123
  │               └── NO → Navigate to home (discard saved route)
```

**Implementation:**
```typescript
function DeepLinkHandler({ children }) {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const pendingDeepLink = useRef<string | null>(null);

  useEffect(() => {
    const handleUrl = (url: string) => {
      const route = parseDeepLink(url);

      if (isProtectedRoute(route) && !isAuthenticated) {
        // Save and redirect to login
        pendingDeepLink.current = route;
        router.replace('/login');
      } else {
        router.push(route);
      }
    };

    // Handle initial URL
    Linking.getInitialURL().then(url => url && handleUrl(url));

    // Handle URLs while app is open
    const sub = Linking.addEventListener('url', ({ url }) => handleUrl(url));
    return () => sub.remove();
  }, [isAuthenticated]);

  // After login, navigate to pending deep link
  useEffect(() => {
    if (isAuthenticated && pendingDeepLink.current) {
      router.replace(pendingDeepLink.current);
      pendingDeepLink.current = null;
    }
  }, [isAuthenticated]);

  return children;
}
```

**Protected routes definition:**
```typescript
const protectedRoutes = ['/users', '/settings', '/profile'];
const publicRoutes = ['/', '/login', '/register', '/invite', '/reset-password'];

function isProtectedRoute(route: string): boolean {
  return !publicRoutes.some(pub => route.startsWith(pub));
}
```

**Output:** Auth-gated deep link flow with pending route handling.

### Step 5: Define Fallback Behavior

Design what happens when the app is not installed or the link is invalid.

**Fallback matrix:**
| Scenario | iOS | Android | Web |
|----------|-----|---------|-----|
| App installed | Open in app | Open in app | N/A (already web) |
| App not installed | Open App Store | Open Play Store | Show web page |
| Route not found | Navigate to home | Navigate to home | 404 page |
| Invalid params | Navigate to parent route | Navigate to parent route | 400 page |
| Expired link | Show "link expired" | Show "link expired" | Show expiry page |

**Smart banner (web → app):**
```html
<!-- iOS Smart App Banner -->
<meta name="apple-itunes-app" content="app-id=123456789, app-argument=myapp://users/123">

<!-- Android equivalent (custom) -->
<link rel="alternate" href="android-app://com.myapp.android/https/myapp.com/users/123">
```

**Output:** Fallback behavior specification for all scenarios.

### Step 6: Document Deep Linking Architecture

Compile the complete deep linking specification.

**Documentation includes:**
- URL scheme reference (from Step 1)
- Platform configuration guides (from Step 2)
- Deferred deep link flow (from Step 3)
- Auth-gated flow (from Step 4)
- Fallback behavior matrix (from Step 5)
- Testing guide (how to test deep links on each platform)
- Attribution tracking setup

**Output:** Complete deep linking architecture document.

---

## Quality Criteria

- Universal Links must open the app on iOS without browser redirect flash
- App Links must be auto-verified on Android
- Auth-gated deep links must redirect to target after login
- Deferred deep links must survive app installation
- All routes must have defined fallback behavior

---

*Squad Apex — Universal Deep Linking Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-universal-deep-linking
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Universal Links open app without browser redirect"
    - "App Links auto-verified on Android"
    - "Auth-gated deep links redirect to target after login"
    - "All routes have defined fallback behavior"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@mobile-eng` or `@apex-lead` |
| Artifact | Deep linking architecture with URL scheme, platform configs, auth flow, and fallback behavior |
| Next action | Implement platform-specific config via `@mobile-eng` or test parity via `@qa-xplatform` |
