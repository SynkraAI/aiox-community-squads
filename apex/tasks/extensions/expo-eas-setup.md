# Task: expo-eas-setup

```yaml
id: expo-eas-setup
version: "1.0.0"
title: "Expo & EAS Build/Submit Setup"
description: >
  Configures Expo Application Services (EAS) for building, submitting,
  and updating a React Native app. Sets up build profiles for development,
  preview, and production. Configures OTA updates, app signing,
  environment variables, and CI integration. Produces a complete
  EAS configuration ready for automated builds and submissions.
elicit: false
owner: mobile-eng
executor: mobile-eng
outputs:
  - EAS Build configuration (eas.json)
  - Build profiles (development, preview, production)
  - App signing setup (iOS certificates, Android keystores)
  - EAS Update configuration for OTA updates
  - Environment variable management
  - CI/CD integration plan
```

---

## When This Task Runs

This task runs when:
- A new Expo/React Native project needs build infrastructure
- Migrating from `expo build` (classic) to EAS Build
- Setting up OTA (over-the-air) updates for the first time
- Configuring automated builds in CI/CD pipeline
- Adding new build profiles (e.g., staging environment)
- `*expo-eas` or `*eas-setup` is invoked

This task does NOT run when:
- The project is not using Expo (bare React Native without Expo)
- The task is about Expo Router navigation (use `rn-navigation-architecture`)
- The task is about app architecture (use appropriate architecture task)

---

## Execution Steps

### Step 1: Initialize EAS Configuration

Set up the foundational EAS configuration.

**Prerequisite checks:**
- Verify `expo` is in dependencies: `npx expo --version`
- Verify EAS CLI: `npx eas --version` (install if missing: `npm install -g eas-cli`)
- Verify Expo account: `npx eas whoami`
- Verify `app.json` or `app.config.js` has required fields: `name`, `slug`, `version`

**Initialize EAS:**
```bash
npx eas init           # Link to Expo project
npx eas build:configure # Generate eas.json
```

**Base `eas.json` structure:**
```json
{
  "cli": {
    "version": ">= 12.0.0",
    "appVersionSource": "remote"
  },
  "build": {
    "development": {},
    "preview": {},
    "production": {}
  },
  "submit": {
    "production": {}
  }
}
```

**Output:** Initialized EAS project with base `eas.json`.

### Step 2: Configure Build Profiles

Define build profiles for each environment.

**Development profile (internal testing with dev client):**
```json
{
  "development": {
    "developmentClient": true,
    "distribution": "internal",
    "ios": {
      "simulator": true
    },
    "env": {
      "APP_ENV": "development",
      "API_URL": "http://localhost:3000"
    }
  }
}
```

**Preview profile (stakeholder testing):**
```json
{
  "preview": {
    "distribution": "internal",
    "ios": {
      "simulator": false
    },
    "env": {
      "APP_ENV": "staging",
      "API_URL": "https://staging-api.example.com"
    },
    "channel": "preview"
  }
}
```

**Production profile (App Store / Play Store):**
```json
{
  "production": {
    "autoIncrement": true,
    "env": {
      "APP_ENV": "production",
      "API_URL": "https://api.example.com"
    },
    "channel": "production"
  }
}
```

**Profile selection guide:**
| Profile | Build type | Distribution | Use case |
|---------|-----------|-------------|----------|
| development | Debug + dev client | Internal (simulator) | Daily development |
| preview | Release | Internal (device) | QA and stakeholder testing |
| production | Release | Store | App Store / Play Store submission |

**Output:** Complete build profiles for all environments.

### Step 3: Set Up App Signing

Configure code signing for iOS and Android.

**iOS signing:**
- EAS manages certificates and provisioning profiles automatically
- For internal distribution: Ad Hoc provisioning profile
- For store: App Store Distribution provisioning profile
- Apple Developer account required ($99/year)

```bash
# Let EAS manage signing (recommended)
npx eas credentials --platform ios

# Or manually configure in eas.json:
{
  "production": {
    "ios": {
      "credentialsSource": "remote"  # EAS manages (recommended)
    }
  }
}
```

**Android signing:**
- EAS generates and manages keystores by default
- Production keystore MUST be backed up (lost keystore = can't update app)

```bash
# Let EAS manage keystore (recommended)
npx eas credentials --platform android

# View keystore info
npx eas credentials --platform android
```

**Key security rules:**
- NEVER commit keystores or certificates to git
- Use `credentialsSource: "remote"` (EAS manages securely)
- Back up production keystore offline
- Rotate signing keys for development profile periodically

**Output:** App signing configuration for both platforms.

### Step 4: Configure EAS Update (OTA)

Set up over-the-air updates for instant JS bundle updates.

**EAS Update configuration in `eas.json`:**
```json
{
  "build": {
    "preview": {
      "channel": "preview"
    },
    "production": {
      "channel": "production"
    }
  }
}
```

**App configuration (`app.json`):**
```json
{
  "expo": {
    "updates": {
      "url": "https://u.expo.dev/YOUR_PROJECT_ID"
    },
    "runtimeVersion": {
      "policy": "appVersion"
    }
  }
}
```

**Update commands:**
```bash
# Publish update to preview channel
npx eas update --channel preview --message "Fix: header alignment"

# Publish update to production channel
npx eas update --channel production --message "v1.2.1 hotfix"

# Check update status
npx eas update:list
```

**Runtime version policy:**
| Policy | When to use |
|--------|-------------|
| `appVersion` | Simple — matches app version in `app.json` |
| `nativeVersion` | When native code changes require new build |
| `fingerprint` | Auto-detect — hash of native dependencies |

**OTA update rules:**
- OTA can update JS bundle and assets ONLY
- Native code changes require a new build
- Always test OTA on preview channel before production
- Rollback plan: publish previous bundle as new update

**Output:** EAS Update configuration with channel strategy.

### Step 5: Set Up Environment Variables

Configure environment management for different build profiles.

**EAS Secrets (for sensitive values):**
```bash
# Set secret (not visible in logs)
npx eas secret:create --scope project --name API_SECRET --value "sk_live_..."
npx eas secret:create --scope project --name SENTRY_DSN --value "https://..."

# List secrets
npx eas secret:list
```

**Build-time env vars (in `eas.json`):**
```json
{
  "build": {
    "production": {
      "env": {
        "APP_ENV": "production",
        "API_URL": "https://api.example.com",
        "ENABLE_ANALYTICS": "true"
      }
    }
  }
}
```

**Accessing env vars in code:**
```typescript
// Using expo-constants
import Constants from 'expo-constants';
const apiUrl = Constants.expoConfig?.extra?.apiUrl;

// Or via app.config.js
export default ({ config }) => ({
  ...config,
  extra: {
    apiUrl: process.env.API_URL,
    appEnv: process.env.APP_ENV,
  },
});
```

**Security rules:**
- NEVER hardcode secrets in source code
- Use EAS Secrets for API keys, tokens, DSNs
- Use `eas.json` env for non-sensitive config (API URLs, feature flags)
- Review `eas.json` env vars — they are visible in build logs

**Output:** Environment variable strategy with secrets management.

### Step 6: Plan CI/CD Integration

Design automated build pipeline using EAS with GitHub Actions.

**GitHub Actions workflow:**
```yaml
name: EAS Build
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - name: Build Preview
        if: github.event_name == 'pull_request'
        run: eas build --profile preview --platform all --non-interactive
      - name: Build Production
        if: github.ref == 'refs/heads/main'
        run: eas build --profile production --platform all --non-interactive
```

**Build triggers:**
| Event | Profile | Platforms |
|-------|---------|-----------|
| PR opened/updated | preview | iOS + Android |
| Merge to main | production | iOS + Android |
| Manual dispatch | Any | Configurable |
| Tag `v*` | production + submit | iOS + Android |

**Output:** CI/CD integration plan with GitHub Actions workflow.

---

## Quality Criteria

- All three build profiles must produce successful builds
- App signing must be configured for both iOS and Android
- EAS Update must deliver OTA updates to correct channels
- Environment variables must not leak secrets in build logs
- CI/CD pipeline must trigger builds on correct events

---

*Squad Apex — Expo & EAS Build/Submit Setup Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-expo-eas-setup
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "All build profiles must produce successful builds"
    - "App signing configured for both platforms"
    - "EAS Update delivers OTA to correct channels"
    - "No secrets exposed in build logs or source code"
    - "CI/CD pipeline triggers on correct events"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@devops` or `@apex-lead` |
| Artifact | EAS configuration (eas.json), signing setup, update channels, CI/CD workflow |
| Next action | Integrate with `@devops` CI/CD pipeline or configure store submission via `eas submit` |
