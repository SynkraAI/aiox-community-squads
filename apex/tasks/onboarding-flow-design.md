---
id: onboarding-flow-design
version: "1.0.0"
title: "Onboarding Flow Design"
description: "Design first-run experiences: tooltip tours, coachmarks, progressive disclosure, feature discovery, and contextual help patterns"
elicit: true
owner: interaction-dsgn
executor: interaction-dsgn
outputs:
  - onboarding-flow-spec.md
  - onboarding-steps.yaml
---

# Onboarding Flow Design

## When This Task Runs

- New feature needs user introduction
- App has poor feature discovery metrics
- First-time user experience needs design
- Complex workflow needs guided walkthrough

## Execution Steps

### Step 1: Map User Journey
```
IDENTIFY critical first-time user paths:
- First login → what should user do first?
- First feature use → what needs explanation?
- Feature discovery → what's hidden but valuable?
- Complex workflows → where do users get stuck?

OUTPUT: User journey map with friction points
```

### Step 2: Select Onboarding Pattern

**elicit: true** — Present patterns for user choice:

| Pattern | Best For | Intrusiveness |
|---------|----------|---------------|
| **Tooltip tour** | Feature-rich UI, sequential discovery | Medium |
| **Coachmarks** | Single feature highlight, contextual | Low |
| **Progressive disclosure** | Complex forms, gradual complexity reveal | Low |
| **Welcome modal** | First-time setup, account configuration | High |
| **Inline hints** | Contextual help, persistent guidance | Low |
| **Empty state CTAs** | Natural discovery through empty states | None |
| **Checklist** | Multi-step setup, gamified completion | Medium |

### Step 3: Design Onboarding Steps

For each onboarding flow:

```yaml
onboarding_flow:
  name: "{flow-name}"
  trigger: "{first-login | first-feature-use | manual}"
  pattern: "{tooltip-tour | coachmarks | progressive-disclosure | ...}"
  dismissible: true
  remember_progress: true  # Don't repeat completed steps
  steps:
    - step: 1
      target: "{CSS selector or component ref}"
      placement: "{top | bottom | left | right}"
      content:
        title: "{short, action-oriented title}"
        body: "{1-2 sentences, what and why}"
        media: "{gif | image | none}"
      action:
        type: "{next | try-it | dismiss}"
        label: "{button text}"
      highlight:
        element: "{target element}"
        overlay: true  # Dim rest of UI
        pulse: true    # Attract attention
  completion:
    action: "{what happens when all steps done}"
    celebration: "{confetti | checkmark | toast}"
    dont_show_again: true
```

### Step 4: Design Skip/Dismiss Behavior

```yaml
skip_behavior:
  skip_button: "Always visible ('Pular' or 'Já sei')"
  dismiss_action: "Saves progress, can resume later"
  re-trigger: "Settings → 'Ver tour novamente'"
  partial_completion: "Resumes from last step"
  storage: "localStorage or user preferences DB"
```

### Step 5: Validate Onboarding Flow

- [ ] Tour is skippable at any step
- [ ] Progress persists across sessions
- [ ] Works with keyboard navigation (focus management)
- [ ] Tooltip/coachmark positions are responsive
- [ ] Overlay doesn't trap focus outside target
- [ ] Screen readers announce step content
- [ ] No CLS from overlay/tooltip insertion

## Quality Criteria

- Every onboarding step is skippable
- Progress persists (no repeating completed tours)
- Keyboard and screen reader accessible
- Responsive — works on mobile viewports
- Performance: overlay doesn't block interaction thread

## Quality Gate

| Check | Pass Criteria |
|-------|---------------|
| Skippable | Every step has dismiss/skip option |
| Persistence | Progress saved, no repetition |
| A11y | Keyboard navigable, screen reader announces |
| Responsive | Works on 320px+ viewports |

## Handoff

- Visual design feeds `@css-eng` for overlay/tooltip styling
- Interaction patterns feed `@react-eng` for component implementation
- A11y requirements feed `@a11y-eng` for focus management validation
