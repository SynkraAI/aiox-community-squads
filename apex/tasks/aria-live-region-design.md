> **DEPRECATED** — Scope absorbed into `keyboard-navigation-patterns.md`. See `data/task-consolidation-map.yaml`.

# Task: aria-live-region-design

```yaml
id: aria-live-region-design
version: "1.0.0"
title: "ARIA Live Region Design"
description: >
  Designs ARIA live region architecture for dynamic content updates.
  Covers assertive vs polite announcements, toast/snackbar notifications,
  form validation messages, loading states, real-time data updates,
  and SPA route change announcements. Ensures screen reader users
  receive timely, non-disruptive feedback for all dynamic UI changes.
elicit: false
owner: a11y-eng
executor: a11y-eng
outputs:
  - Live region architecture diagram
  - Announcement priority matrix (assertive/polite/off)
  - Toast/notification live region patterns
  - Form validation announcement patterns
  - Route change announcement pattern
  - Live region specification document
```

---

## When This Task Runs

This task runs when:
- Toast/snackbar notifications need screen reader support
- Form validation messages appear dynamically
- Real-time data updates (chat, dashboards, feeds)
- SPA route changes need announcement
- Loading/progress states need AT feedback
- `*live-region` or `*aria-live` is invoked

This task does NOT run when:
- Static ARIA attributes (use `aria-pattern-implementation`)
- Focus management (use `focus-management-design`)
- Keyboard navigation (use `keyboard-navigation-patterns`)

---

## Execution Steps

### Step 1: Catalog Dynamic Content Updates

Identify every UI change that occurs without page reload.

| Update Type | Example | User Impact |
|-------------|---------|-------------|
| Toast notification | "Saved successfully" | Confirmation |
| Error message | "Email is required" | Blocking |
| Loading state | "Loading appointments..." | Waiting |
| Progress | "Uploading 45%..." | Progress |
| Data update | New message in chat | Information |
| Route change | Navigated to /services | Orientation |
| Status change | "Online" → "Away" | Status |
| Timer/countdown | "Session expires in 5m" | Urgent |

**Output:** Dynamic content update catalog.

### Step 2: Design Announcement Priority Matrix

Map each update type to the correct `aria-live` politeness.

**Politeness levels:**

| Level | Behavior | Use When |
|-------|----------|----------|
| `assertive` | Interrupts current speech immediately | Errors, critical alerts, session expiry |
| `polite` | Waits for current speech to finish | Success messages, status changes, data updates |
| `off` | Not announced (default) | Decorative changes, background updates |

**Priority matrix:**

| Update | Politeness | Atomic | Relevant |
|--------|-----------|--------|----------|
| Error toast | `assertive` | true | — |
| Success toast | `polite` | true | — |
| Form validation error | `assertive` | true | — |
| Loading start | `polite` | true | — |
| Loading complete | `polite` | true | — |
| Progress update | `polite` | true | — |
| Route change | `polite` | true | — |
| Chat message | `polite` | false | — |
| Session expiry warning | `assertive` | true | — |
| Background data refresh | `off` | — | — |

**Rules:**
- Default to `polite` — only use `assertive` for errors/critical
- Set `aria-atomic="true"` when entire region should be re-read
- Never use `aria-live` on elements that update > 1x/second (floods AT)
- Live region must exist in DOM BEFORE content changes

**Output:** Announcement priority matrix.

### Step 3: Implement Live Region Patterns

**Centralized announcer pattern:**
```tsx
function LiveAnnouncer() {
  return (
    <>
      <div
        id="live-polite"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      />
      <div
        id="live-assertive"
        aria-live="assertive"
        aria-atomic="true"
        className="sr-only"
      />
    </>
  );
}

function announce(message: string, priority: 'polite' | 'assertive' = 'polite') {
  const region = document.getElementById(`live-${priority}`);
  if (!region) return;
  // Clear then set — ensures AT detects the change
  region.textContent = '';
  requestAnimationFrame(() => {
    region.textContent = message;
  });
}
```

**Toast notification pattern:**
```tsx
function Toast({ message, type }: { message: string; type: 'success' | 'error' }) {
  useEffect(() => {
    announce(message, type === 'error' ? 'assertive' : 'polite');
  }, [message, type]);

  return (
    <div role={type === 'error' ? 'alert' : 'status'} className="toast">
      {message}
    </div>
  );
}
```

**Form validation pattern:**
```tsx
<div>
  <label htmlFor="email">Email</label>
  <input
    id="email"
    aria-describedby="email-error"
    aria-invalid={!!error}
  />
  <div id="email-error" role="alert" aria-live="assertive">
    {error && <span>{error}</span>}
  </div>
</div>
```

**Route change announcement (SPA):**
```tsx
function RouteAnnouncer() {
  const pathname = usePathname();

  useEffect(() => {
    const pageTitle = document.title;
    announce(`Navigated to ${pageTitle}`, 'polite');
  }, [pathname]);

  return null;
}
```

**Output:** Live region pattern implementations.

### Step 4: Handle Real-Time Data Updates

Design live region strategy for frequently updating data.

**Challenge:** Chat messages, dashboards, feeds update frequently. Announcing every change floods the screen reader.

**Strategies:**

| Strategy | When | How |
|----------|------|-----|
| Batch announce | Updates > 1/sec | "3 new messages" instead of each |
| Summarize | Dashboard metrics | "Revenue updated to $45K" |
| On-demand | Background data | User presses key to hear update |
| Throttle | Real-time feed | Max 1 announcement per 5 seconds |

**Implementation — batched announcements:**
```typescript
let pendingCount = 0;
let announceTimer: NodeJS.Timeout;

function onNewMessage(msg: Message) {
  pendingCount++;
  clearTimeout(announceTimer);
  announceTimer = setTimeout(() => {
    announce(
      pendingCount === 1
        ? `New message from ${msg.sender}`
        : `${pendingCount} new messages`,
      'polite'
    );
    pendingCount = 0;
  }, 2000);
}
```

**Output:** Real-time data announcement strategies.

### Step 5: Document Live Region Architecture

Compile the complete specification.

**Documentation includes:**
- Dynamic content catalog (from Step 1)
- Priority matrix (from Step 2)
- Pattern implementations (from Step 3)
- Real-time strategies (from Step 4)
- AT testing checklist (VoiceOver, NVDA, JAWS behavior)
- Common pitfalls (live region not in DOM, double announcements, stale content)

**Output:** Live region specification document.

---

## Quality Criteria

- Every dynamic UI change has appropriate AT feedback
- No announcement flooding (max 1 per second for polite, immediate for assertive)
- Live regions exist in DOM before content changes
- Form errors announced immediately via `role="alert"`
- SPA route changes announced to screen readers
- VoiceOver + NVDA + JAWS all receive correct announcements

---

*Squad Apex — ARIA Live Region Design Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-aria-live-region-design
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Every dynamic update has AT feedback"
    - "No announcement flooding (< 1/sec)"
    - "Live regions in DOM before content change"
    - "Tested on VoiceOver + NVDA"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@react-eng` or `@apex-lead` |
| Artifact | Live region architecture with announcer, toast, form, and route patterns |
| Next action | Implement centralized announcer via `@react-eng` or validate with AT via screen reader testing |
