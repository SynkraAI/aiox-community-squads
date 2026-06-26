# Task: solito-navigation-setup

```yaml
id: solito-navigation-setup
version: "1.0.0"
title: "Solito Navigation Setup"
description: >
  Sets up Solito as the cross-platform navigation abstraction layer
  between Next.js (web) and React Navigation (native). Configures
  shared routing, implements universal Link component, sets up
  useRouter/useParams hooks, handles platform-specific navigation
  patterns, and ensures URL parity between web and native.
elicit: false
owner: cross-plat-eng
executor: cross-plat-eng
outputs:
  - Solito installation and configuration
  - Shared route definitions
  - Universal Link component setup
  - useRouter/useParams cross-platform hooks
  - Platform navigation parity verification
  - Solito navigation specification document
```

---

## When This Task Runs

This task runs when:
- A monorepo needs shared navigation between Next.js and React Native
- Adding new routes that must work on both web and native
- Migrating from separate web/native navigation to unified
- Navigation parity issues between platforms (routes work on web but not native)
- `*solito-nav` or `*solito-setup` is invoked

This task does NOT run when:
- Navigation is native-only (use `rn-navigation-architecture`)
- Navigation is web-only (delegate to `@react-eng`)
- The task is about deep linking without web counterpart (use `rn-navigation-architecture`)

---

## Execution Steps

### Step 1: Install and Configure Solito

Set up Solito in the monorepo.

**Installation:**
```bash
# In the shared app package
cd packages/app
npm install solito
```

**Monorepo structure requirement:**
```
packages/
├── app/           # Shared screens and navigation (Solito)
│   ├── features/
│   │   ├── home/
│   │   │   └── screen.tsx
│   │   └── user/
│   │       ├── detail-screen.tsx
│   │       └── screen.tsx
│   └── navigation/
│       └── native/
│           └── index.tsx
├── ui/            # Shared UI components
├── next-app/      # Next.js app (web entry point)
│   └── pages/ or app/
└── expo-app/      # Expo app (native entry point)
    └── App.tsx
```

**Key principle:** Screens live in `packages/app/`. Each platform entry point (`next-app`, `expo-app`) imports and renders these shared screens.

**Output:** Solito installed with monorepo directory structure.

### Step 2: Define Shared Routes

Create a route map that both platforms implement identically.

**Route definition pattern:**
```typescript
// packages/app/navigation/routes.ts
export const routes = {
  home: '/',
  userList: '/users',
  userDetail: (id: string) => `/users/${id}`,
  settings: '/settings',
  profile: '/profile',
} as const;
```

**Web implementation (Next.js pages/app router):**
```
next-app/
├── pages/              # Pages Router
│   ├── index.tsx       # → routes.home
│   ├── users/
│   │   ├── index.tsx   # → routes.userList
│   │   └── [id].tsx    # → routes.userDetail
│   ├── settings.tsx    # → routes.settings
│   └── profile.tsx     # → routes.profile
```

**Native implementation (React Navigation):**
```typescript
// packages/app/navigation/native/index.tsx
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { HomeScreen } from '../../features/home/screen';
import { UserListScreen } from '../../features/user/screen';
import { UserDetailScreen } from '../../features/user/detail-screen';

const Stack = createNativeStackNavigator();

export function NativeNavigation() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="home" component={HomeScreen} />
      <Stack.Screen name="users" component={UserListScreen} />
      <Stack.Screen name="user-detail" component={UserDetailScreen} />
      <Stack.Screen name="settings" component={SettingsScreen} />
      <Stack.Screen name="profile" component={ProfileScreen} />
    </Stack.Navigator>
  );
}
```

**Linking configuration (maps URLs to screen names):**
```typescript
const linking = {
  prefixes: ['myapp://'],
  config: {
    screens: {
      home: '',
      users: 'users',
      'user-detail': 'users/:id',
      settings: 'settings',
      profile: 'profile',
    },
  },
};
```

**Output:** Shared route definitions with web and native implementations.

### Step 3: Implement Universal Link Component

Use Solito's `Link` as the single link component across platforms.

**Solito Link usage:**
```tsx
// packages/app/features/home/screen.tsx
import { Link } from 'solito/link';

export function HomeScreen() {
  return (
    <View>
      <Link href="/users">
        <Text>View Users</Text>
      </Link>

      <Link href="/users/abc123">
        <Text>User Detail</Text>
      </Link>

      {/* With dynamic route */}
      <Link href={`/users/${userId}`}>
        <Text>{userName}</Text>
      </Link>
    </View>
  );
}
```

**How it works per platform:**
| Platform | Solito `Link` renders as | Navigation method |
|----------|--------------------------|-------------------|
| Web (Next.js) | `<a>` tag via Next.js `Link` | URL-based routing |
| Native (RN) | `<Pressable>` with `navigation.navigate` | Screen-based routing |

**Link patterns:**
```tsx
// Basic link
<Link href="/users">...</Link>

// Link with dynamic params
<Link href={`/users/${id}`}>...</Link>

// Link replacing history (no back)
<Link href="/home" replace>...</Link>

// Link to external URL (web only)
<Link href="https://example.com" target="_blank">...</Link>
```

**Output:** Universal Link component configured for both platforms.

### Step 4: Set Up Cross-Platform Hooks

Configure `useRouter` and `useParams` for shared screen logic.

**useRouter (programmatic navigation):**
```tsx
import { useRouter } from 'solito/router';

function UserCard({ user }) {
  const router = useRouter();

  const handlePress = () => {
    router.push(`/users/${user.id}`);
  };

  const handleBack = () => {
    router.back();
  };

  const handleReplace = () => {
    router.replace('/home');
  };

  return (
    <Pressable onPress={handlePress}>
      <Text>{user.name}</Text>
    </Pressable>
  );
}
```

**useParams (read route parameters):**
```tsx
// packages/app/features/user/detail-screen.tsx
import { useParams } from 'solito/navigation';
// OR for Next.js App Router:
import { useParams } from 'solito/app/navigation';

function UserDetailScreen() {
  const { id } = useParams<{ id: string }>();

  // Use id to fetch user data
  const { data: user } = useUser(id);

  return <Text>{user?.name}</Text>;
}
```

**createParam (type-safe params with defaults):**
```tsx
import { createParam } from 'solito';

const { useParam } = createParam<{ id: string }>();

function UserDetailScreen() {
  const [id] = useParam('id');
  // id is typed as string
}
```

**Platform behavior:**
| Hook | Web | Native |
|------|-----|--------|
| `useRouter().push` | `next/navigation` push | `navigation.navigate` |
| `useRouter().replace` | `next/navigation` replace | `navigation.replace` |
| `useRouter().back` | `window.history.back()` | `navigation.goBack()` |
| `useParams` | URL params | Route params |

**Output:** Cross-platform hooks configured with TypeScript types.

### Step 5: Handle Platform-Specific Navigation

Design escape hatches for navigation that differs between platforms.

**Platform-specific screens:**
```tsx
import { Platform } from 'react-native';

function SettingsScreen() {
  if (Platform.OS === 'web') {
    // Web: full page with URL /settings
    return <WebSettingsPage />;
  }
  // Native: modal presentation
  return <NativeSettingsModal />;
}
```

**Bottom sheet (native) vs sidebar (web):**
```tsx
// packages/app/features/filters/screen.tsx
import { Platform } from 'react-native';

export function FiltersScreen() {
  const content = <FilterForm />;

  if (Platform.OS === 'web') {
    return <Sidebar>{content}</Sidebar>;
  }
  return <BottomSheet>{content}</BottomSheet>;
}
```

**Platform-specific navigation config:**
| Pattern | Web | Native |
|---------|-----|--------|
| Filters | Sidebar panel | Bottom sheet |
| Settings | Full page | Modal stack |
| Image viewer | Lightbox overlay | Full-screen with pinch |
| Search | Page with URL `/search?q=...` | Modal or inline |

**Rules for platform branching:**
- Keep screen LOGIC shared (data fetching, state management)
- Branch only the PRESENTATION layer when needed
- Use `Platform.select` for minor differences
- Use `.web.tsx` / `.native.tsx` for major differences
- Document every platform branch with a comment explaining WHY

**Output:** Platform-specific navigation patterns documented.

### Step 6: Verify Navigation Parity

Test that all routes work identically on both platforms.

**Parity checklist per route:**
| Check | Web | Native |
|-------|-----|--------|
| Route renders correct screen | URL `/users` → UserListScreen | Screen "users" → UserListScreen |
| Params passed correctly | `/users/123` → id="123" | navigate("user-detail", {id:"123"}) → id="123" |
| Back navigation works | Browser back → previous page | Navigation back → previous screen |
| Deep link works | Direct URL access | `myapp://users/123` opens correct screen |
| Link component navigates | Click `<Link>` → correct page | Press `<Link>` → correct screen |

**Test execution:**
1. List all routes from route definition
2. For each route: test on web browser + iOS simulator + Android emulator
3. Verify params are parsed correctly on both platforms
4. Test deep linking on both platforms
5. Test back navigation chain

**Output:** Navigation parity verification report.

---

## Quality Criteria

- All shared routes must render the same screen on web and native
- URL params on web must map to route params on native identically
- `useRouter` hooks must produce equivalent navigation on both platforms
- Deep links must work on both web (URL) and native (custom scheme)
- Platform-specific navigation must be documented and justified

---

*Squad Apex — Solito Navigation Setup Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-solito-navigation-setup
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "All shared routes render same screen on web and native"
    - "URL params map correctly to route params on both platforms"
    - "Deep links work on web and native"
    - "Platform-specific branches are documented and justified"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@mobile-eng` or `@apex-lead` |
| Artifact | Solito navigation configuration with shared routes, Link component, hooks, and parity verification |
| Next action | Implement native navigation details via `@mobile-eng` or test parity via `@qa-xplatform` |
