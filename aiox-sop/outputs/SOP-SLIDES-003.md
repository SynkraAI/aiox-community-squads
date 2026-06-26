# SOP-SLIDES-003 — Slide Deck Creation: Brand-Agnostic LLM Reference

| Field | Value |
|---|---|
| **SOP ID** | SOP-SLIDES-003 |
| **Version** | 1.1.0 |
| **Effective Date** | 2026-03-16 |
| **Classification** | Public |
| **Status** | DRAFT |
| **Consumer** | LLM agents generating slide code for ANY brand |
| **Stack** | React + TypeScript + Framer Motion + Tailwind CSS |
| **Design System** | Agnostic — brand tokens provided via configuration |

---

## 0. BRAND CONFIGURATION — FILL BEFORE USE

Every `{{placeholder}}` in this SOP must be resolved before generating code. Copy this block and fill all values.

```yaml
brand:
  # --- Identity ---
  name: "{{brand.name}}"                    # e.g. "Acme Corp"
  prefix: "{{brand.prefix}}"                # CSS class prefix, e.g. "ac" → generates font-ac-sans
  url: "{{brand.url}}"                      # e.g. "acme.com"
  tagline: "{{brand.tagline}}"              # e.g. "Build Better"

  # --- Colors (hex values) ---
  color:
    bg_primary: "{{brand.color.bg_primary}}"           # Dark background, e.g. "#050505"
    bg_accent: "{{brand.color.bg_accent}}"             # Accent/highlight background, e.g. "#D1FF00"
    surface: "{{brand.color.surface}}"                 # Cards/panels, e.g. "#111111"
    text_primary: "{{brand.color.text_primary}}"       # Primary text on dark bg, e.g. "#FFFDD0"
    text_secondary: "{{brand.color.text_secondary}}"   # Secondary/dim text. MUST be >= #777777 for WCAG AA
    accent: "{{brand.color.accent}}"                   # Inline highlights, emphasis. Same as bg_accent or different
    border: "{{brand.color.border}}"                   # Borders/dividers, e.g. "#222222"
    warning: "{{brand.color.warning}}"                 # Warning/negative accent, e.g. "#FF4444"

  # --- Fonts ---
  font:
    sans: "{{brand.font.sans}}"               # Primary sans-serif, e.g. "Geist"
    sans_fallback: "{{brand.font.sans_fb}}"   # Fallback, e.g. "system-ui, sans-serif"
    mono: "{{brand.font.mono}}"               # Monospace, e.g. "Geist Mono"
    mono_fallback: "{{brand.font.mono_fb}}"   # Fallback, e.g. "monospace"

  # --- Contrast (must verify) ---
  contrast:
    text_primary_on_bg: "{{brand.contrast.primary}}"     # Must be >= 4.5:1 (AA)
    accent_on_bg: "{{brand.contrast.accent}}"             # Must be >= 4.5:1 (AA)
    text_secondary_on_bg: "{{brand.contrast.secondary}}"  # Must be >= 4.5:1 (AA)
    bg_primary_on_accent: "{{brand.contrast.inverted}}"   # For accent-bg slides
```

### Validation: Contrast MUST Pass

Before proceeding, verify all contrast ratios with a WCAG calculator:

| Combination | Minimum | Grade |
|---|---|---|
| `text_primary` on `bg_primary` | ≥ 4.5:1 | AA required, AAA preferred |
| `accent` on `bg_primary` | ≥ 4.5:1 | AA required |
| `text_secondary` on `bg_primary` | ≥ 4.5:1 | AA required |
| `bg_primary` on `bg_accent` | ≥ 4.5:1 | AA required |
| Large text (≥ 24px bold / ≥ 19px) | ≥ 3:1 | AA for large text |

**IF any combination fails → DO NOT PROCEED. Adjust brand colors first.**

---

## 1. CSS VARIABLES — GENERATE THIS BLOCK

From the brand config, generate these CSS custom properties:

```css
:root {
  /* Colors */
  --slide-bg:           {{brand.color.bg_primary}};
  --slide-accent:       {{brand.color.bg_accent}};
  --slide-surface:      {{brand.color.surface}};
  --slide-text:         {{brand.color.text_primary}};
  --slide-text-dim:     {{brand.color.text_secondary}};
  --slide-border:       {{brand.color.border}};
  --slide-warning:      {{brand.color.warning}};

  /* Fonts */
  --font-slide-sans:    "{{brand.font.sans}}", {{brand.font.sans_fb}};
  --font-slide-mono:    "{{brand.font.mono}}", {{brand.font.mono_fb}};

  /* Typography Scale (universal — do not change per brand) */
  --slide-title-xl:     clamp(48px, 6.8vw, 130px);
  --slide-title-lg:     clamp(40px, 3.3vw, 64px);
  --slide-title-md:     clamp(32px, 2.5vw, 48px);
  --slide-body:         clamp(24px, 1.9vw, 36px);
  --slide-caption:      clamp(16px, 1.5vw, 28px);
  --slide-label:        clamp(13px, 0.7vw, 14px);

  /* Spacing (universal) */
  --slide-space-xs:     clamp(4px, 0.4vw, 8px);
  --slide-space-sm:     clamp(8px, 0.8vw, 16px);
  --slide-space-md:     clamp(16px, 1.7vw, 32px);
  --slide-space-lg:     clamp(32px, 3.3vw, 64px);
  --slide-space-xl:     clamp(64px, 5vw, 96px);

  /* Margins / Safe Area (universal) */
  --slide-margin-x:     clamp(48px, 7.3vw, 200px);
  --slide-margin-top:   clamp(40px, 5vw, 136px);
  --slide-margin-bottom: clamp(24px, 2.1vw, 40px);
}

/* Live mode safe zones */
.mode-live {
  --slide-safe-right:   20%;
  --slide-safe-bottom:  15%;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 2. SHARED MODULE — IMPLEMENT OR ADAPT

The slide system requires a shared module exporting these. Implement for your project:

### 2.1 Font Constants

```tsx
export const FONT_SANS = { fontFamily: "var(--font-slide-sans)" } as const
export const FONT_MONO = { fontFamily: "var(--font-slide-mono)" } as const
```

**RULE**: Every text element MUST have `style={FONT_SANS}` or `style={FONT_MONO}` inline.

### 2.2 Animation Presets

```tsx
import { type Transition } from "framer-motion"

export type Ease = [number, number, number, number]
export const EASE_SMOOTH: Ease = [0.25, 0.1, 0.25, 1]
export const EASE_SPRING: Ease = [0.34, 1.56, 0.64, 1]

export const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5, delay, ease: EASE_SMOOTH } as Transition,
})

export const fadeIn = (delay = 0) => ({
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  transition: { duration: 0.4, delay, ease: EASE_SMOOTH } as Transition,
})

export const slideRight = (delay = 0) => ({
  initial: { opacity: 0, x: -40 },
  animate: { opacity: 1, x: 0 },
  transition: { duration: 0.6, delay, ease: EASE_SMOOTH } as Transition,
})

export const slideLeft = (delay = 0) => ({
  initial: { opacity: 0, x: 40 },
  animate: { opacity: 1, x: 0 },
  transition: { duration: 0.6, delay, ease: EASE_SMOOTH } as Transition,
})

export const scaleIn = (delay = 0) => ({
  initial: { opacity: 0, scale: 0.88 },
  animate: { opacity: 1, scale: 1 },
  transition: { duration: 0.45, delay, ease: EASE_SPRING } as Transition,
})

export const growWidth = (delay = 0) => ({
  initial: { scaleX: 0 },
  animate: { scaleX: 1 },
  transition: { duration: 0.7, delay, ease: EASE_SMOOTH } as Transition,
})

export const growHeight = (delay = 0, duration = 0.7) => ({
  initial: { scaleY: 0 },
  animate: { scaleY: 1 },
  transition: { duration, delay, ease: EASE_SMOOTH } as Transition,
})

export const stagger = (i: number, base = 0.1) => base + i * 0.08
```

### 2.3 SlideLayout

```tsx
import { type ReactNode } from "react"
import { motion } from "framer-motion"

export function SlideLayout({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <motion.div
      className={`relative h-[1080px] w-[1920px] overflow-hidden ${className}`}
      style={{
        background: "var(--slide-bg)",
        color: "var(--slide-text)",
        ...FONT_SANS,
      }}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  )
}
```

For accent background: `<SlideLayout className="!bg-[var(--slide-accent)]">`

### 2.4 Decorative Components

```tsx
export function SectionTag({ label, delay = 0 }: { label: string; delay?: number }) {
  return (
    <motion.span
      className="text-[14px] uppercase tracking-[0.3em]"
      style={{ ...FONT_MONO, color: "var(--slide-text-dim)" }}
      {...fadeUp(delay)}
    >
      {label}
    </motion.span>
  )
}

export function CornerMarks({ color = "var(--slide-accent)", opacity = 0.3 }: { color?: string; opacity?: number }) {
  const mark = (pos: string) => (
    <div className={`absolute h-[20px] w-[20px] ${pos}`} style={{ opacity }}>
      <div className="absolute left-0 top-1/2 h-[1px] w-full" style={{ background: color }} />
      <div className="absolute left-1/2 top-0 h-full w-[1px]" style={{ background: color }} />
    </div>
  )
  return (
    <>
      {mark("left-[40px] top-[40px]")}
      {mark("right-[40px] top-[40px]")}
      {mark("bottom-[40px] left-[40px]")}
      {mark("bottom-[40px] right-[40px]")}
    </>
  )
}

export function WatermarkNumber({ n, className = "" }: { n: string; className?: string }) {
  return (
    <motion.span
      className={`pointer-events-none absolute select-none text-[16rem] font-black leading-[0.8] ${className}`}
      style={{ color: "var(--slide-accent)", opacity: 0.04, fontWeight: 900, ...FONT_SANS }}
      {...fadeIn(0.2)}
    >
      {n}
    </motion.span>
  )
}

export function MetaBar({ left, center, right }: { left: string; center?: string; right: string }) {
  return (
    <div className="flex h-[56px] items-center justify-between px-[60px]"
      style={{ borderBottom: "1px solid var(--slide-border)", ...FONT_MONO }}>
      <span className="text-[11px] uppercase tracking-[0.3em]" style={{ color: "var(--slide-text-dim)", opacity: 0.6 }}>{left}</span>
      {center && <span className="text-[11px] uppercase tracking-[0.3em]" style={{ color: "var(--slide-accent)", opacity: 0.6 }}>{center}</span>}
      <span className="text-[11px] uppercase tracking-[0.3em]" style={{ color: "var(--slide-text-dim)", opacity: 0.6 }}>{right}</span>
    </div>
  )
}

export function TechFrame({ children, className = "" }: { children: ReactNode; className?: string }) {
  return (
    <div className={`relative ${className}`}
      style={{ clipPath: "polygon(0 12px, 12px 0, calc(100% - 12px) 0, 100% 12px, 100% calc(100% - 12px), calc(100% - 12px) 100%, 12px 100%, 0 calc(100% - 12px))" }}>
      {children}
    </div>
  )
}
```

### 2.5 PageFooter Pattern (inline, not a component)

```tsx
<div className="absolute bottom-[40px] left-[200px] right-[200px] flex items-center pt-3"
  style={{ borderTop: "1px solid var(--slide-border)", opacity: 0.2, ...FONT_MONO }}>
  <span className="text-[11px] uppercase tracking-[0.15em]" style={{ color: "var(--slide-text-dim)", opacity: 0.4 }}>
    {{section_name}}
  </span>
  <span className="mx-4 h-px flex-1" style={{ background: "var(--slide-border)", opacity: 0.1 }} />
  <span className="text-[11px] uppercase tracking-[0.15em]" style={{ color: "var(--slide-text-dim)", opacity: 0.4 }}>
    {{slide_number}}
  </span>
  <span className="mx-4 h-px flex-1" style={{ background: "var(--slide-border)", opacity: 0.1 }} />
  <span className="text-[11px] uppercase tracking-[0.15em]" style={{ color: "var(--slide-text-dim)", opacity: 0.4 }}>
    {{brand.name}}
  </span>
</div>
```

### 2.6 Inline Highlight

```tsx
<span style={{ background: "var(--slide-accent)", color: "var(--slide-bg)", padding: "0.05em 0.2em" }}>
  KEYWORD
</span>
```

Max 2 per slide.

---

## 3. DECISION TREES

### 3.0 Format Selection (FIRST — determines mode and overrides)

```
IF format == "ted_keynote":
  mode = "palco", bullets = NEVER, text = minimal, slides = 40-90
  dominant_types = [STATEMENT, IMAGE, METRIC]
  narrative = "hook → tension → resolution → CTA"
  rule: slide supports narrator — if it works alone, it steals attention

ELSE IF format == "pitch_deck":
  mode = "palco" (live) + "async" (leave-behind)
  slides = 10-15, data = essential, min_font = 30pt
  structure = Sequoia or YC, versions = 2 (live + leave-behind)
  fatal_anti_pattern: "We have no competition"

ELSE IF format == "sales_deck":
  mode = "palco" (live) + "async" (champion leave-behind)
  slides = SMB:8-12 / Mid:12-18 / Enterprise:18-25
  framework = SCR (Situation → Complication → Resolution)
  deck must work as autonomous seller for internal champion

ELSE IF format == "technical":
  mode = "palco", CODE type = legitimate, code_font >= 20pt
  backup_slides = 5-10 for Q&A
  test: "Step back 2m. Can you read it?"

ELSE IF format == "zoom_virtual":
  mode = "live" (mandatory)
  visual_movements = 2+ per minute, interaction every 3-5 min
  slide is main focus (no body language visible)

ELSE IF format == "carousel_stories":
  mode = "async", ratio = 9:16 or 1:1, slides = 5-10
  first = visual hook, last = CTA (Save/Share/Link)
  bullets = NEVER, max_words = 15, font = extra-large
```

### Format Comparison Table

| Format | Slides | Text | Bullets | Self-explanatory |
|---|---|---|---|---|
| TED/Keynote | 40-90 | Minimal | Never | Never |
| Pitch Deck | 10-15 | Moderate | Rare | Yes (leave-behind) |
| Sales Deck | 8-25 | Moderate | Allowed | Yes (champion) |
| Technical | 20-40 | Moderate+ | Allowed | Partial (backup) |
| Zoom/Virtual | Variable | Reduced | Cautious | Depends |
| Carousel | 5-10 | Minimal | Never | Always |

### 3.1 Mode Selection

```
IF context in [conference, keynote, workshop, presencial]:
  mode = "palco"
  max_words = 15, min_font = "2.2vw", whitespace >= 50%
  animations = true, speaker_notes = required

ELSE IF context in [youtube, twitch, screenshare, live_call]:
  mode = "live"
  max_words = 15, min_font = "2.2vw", whitespace >= 45%
  animations = true (reduce delays 30%)
  safe_zone: right 20%, bottom 15%

ELSE IF context in [post_event, course, onboarding, pdf]:
  mode = "async"
  max_words = 30, min_font = "1.6vw", whitespace >= 40%
  animations = false
```

### 3.2 Aspect Ratio

```
IF channel in [projector, monitor, stream]: 16:9 (1920x1080)
ELSE IF channel in [macbook]:              16:10 (1920x1200)
ELSE IF channel in [stories, reels]:       9:16 (1080x1920)
ELSE IF channel in [instagram, carousel]:  1:1 (1080x1080)
ELSE: 16:9 (default)
```

For mobile: use `100svh` not `100vh`. `svh` (small viewport) measures height with browser chrome visible. Avoid `dvh` (layout shifts) and `lvh` (legacy).

### 3.3 Slide Type Selection

```
IF content = opening/title/speaker     → TITLE
IF content = section transition        → SECTION_BREAK
IF content = impact phrase/manifesto   → STATEMENT
IF content = third-party quote         → QUOTE
IF content = bullets/keywords/features → CONTENT
IF content = before/after/A vs B       → COMPARISON
IF content = 1-3 big numbers           → METRIC
IF content = chart/graph/table         → DATA_VIZ
IF content = photo/screenshot          → IMAGE
IF content = step-by-step/timeline     → BUILD
IF content = code/terminal             → CODE
IF content = CTA/thank you/contact     → CLOSING
```

---

## 4. SLIDE TYPE PATTERNS — BRAND-AGNOSTIC

### 4.1 TITLE

```tsx
export function SlideTitleHero() {
  return (
    <SlideLayout>
      <CornerMarks />
      <WatermarkNumber n="01" className="right-[80px] top-[80px]" />
      <MetaBar left="{{brand.name}}" center="Confidential" right="2026" />
      <div className="absolute inset-0 flex flex-col justify-center px-[140px]">
        <SectionTag label="[01] — Introduction" delay={0.1} />
        <motion.h1
          style={FONT_SANS}
          className="mt-8 text-[130px] font-black leading-[0.85] tracking-[-4px]"
          {...fadeUp(0.3)}
        >
          MAIN
          <br />
          <span style={{ color: "var(--slide-accent)" }}>TITLE</span>
        </motion.h1>
        <motion.div className="mt-14 flex items-center gap-4" {...fadeUp(0.6)}>
          <motion.div className="h-[2px] w-16 origin-left" style={{ background: "var(--slide-accent)" }} {...growWidth(0.7)} />
          <p className="text-[18px] tracking-[0.3em]" style={{ ...FONT_MONO, color: "var(--slide-text-dim)" }}>
            {{brand.name}} // {{date}}
          </p>
        </motion.div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Title xl/Black/max 5 words. CornerMarks + MetaBar allowed. First slide.

---

### 4.2 SECTION-BREAK

```tsx
export function SlideSectionBreak() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 opacity-[0.04]"
        style={{ background: `radial-gradient(ellipse at 50% 50%, var(--slide-accent), transparent 60%)` }} />
      <CornerMarks opacity={0.2} />
      <WatermarkNumber n="02" className="left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2" />
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <motion.div className="h-[100px] w-[1px] origin-top"
          style={{ background: "var(--slide-accent)", opacity: 0.4 }} {...growHeight(0.1)} />
        <motion.span className="my-8 text-[16px] uppercase tracking-[0.5em]"
          style={{ ...FONT_MONO, color: "var(--slide-text-dim)" }} {...fadeIn(0.3)}>
          Part 02
        </motion.span>
        <motion.h2 style={FONT_SANS} className="text-[140px] font-black leading-none tracking-[-3px]" {...scaleIn(0.4)}>
          SECTION
        </motion.h2>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Title lg/Black/max 3 words. Full center. NO PageFooter. 3-5s on screen.

---

### 4.3 STATEMENT

```tsx
export function SlideStatement() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 flex items-center justify-center px-[120px] text-center">
        <motion.h1
          className="text-[110px] font-black uppercase leading-[0.9] tracking-[-3px]"
          style={FONT_SANS}
          {...scaleIn(0.2)}
        >
          BOLD CLAIM
          <br />
          <span style={{ color: "var(--slide-text-dim)" }}>SUPPORTING</span>
          <br />
          <span style={{ color: "var(--slide-accent)" }}>HIGHLIGHT</span>
        </motion.h1>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Max 10 words. Full center. bg_primary only. Whitespace ≥ 60%. Max 2 accent highlights.

---

### 4.4 CONTENT

```tsx
export function SlideContent() {
  const items = [
    { num: "I", title: "FIRST POINT", desc: "Short keyword description." },
    { num: "II", title: "SECOND POINT", desc: "Another keyword fragment." },
    { num: "III", title: "THIRD POINT", desc: "Final keyword fragment." },
  ]

  return (
    <SlideLayout>
      <div className="absolute inset-0 flex flex-col justify-center px-[200px]">
        <motion.div className="mb-2 pt-4"
          style={{ borderTop: `4px solid var(--slide-accent)` }} {...fadeUp(0.1)}>
          <span className="text-[52px] font-black" style={FONT_SANS}>SLIDE TITLE.</span>
        </motion.div>
        <motion.span className="mb-10 text-[14px] tracking-[0.2em]"
          style={{ ...FONT_MONO, color: "var(--slide-text-dim)" }} {...fadeIn(0.2)}>
          SUBTITLE // CONTEXT
        </motion.span>
        <div className="flex flex-col">
          {items.map((item, i) => (
            <motion.div key={item.num} className="flex gap-6 py-6"
              style={{ borderBottom: i < items.length - 1 ? `1px solid var(--slide-border)` : "none", opacity: 0.1 }}
              {...slideRight(stagger(i, 0.3))}
            >
              <div className="flex h-[56px] w-[56px] shrink-0 items-center justify-center"
                style={{ background: "var(--slide-accent)", ...FONT_MONO }}>
                <span className="text-[22px] font-bold" style={{ color: "var(--slide-bg)" }}>{item.num}</span>
              </div>
              <div>
                <h3 className="mb-2 text-[26px] font-black uppercase" style={FONT_SANS}>{item.title}</h3>
                <p className="text-[24px] leading-[1.3]" style={{ ...FONT_SANS, color: "var(--slide-text-dim)" }}>{item.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
      {/* PageFooter inline — see section 2.5 */}
    </SlideLayout>
  )
}
```

**Rules**: 3-4 keywords (not sentences). Left-aligned. PageFooter. Whitespace ≥ 50%.

---

### 4.5 COMPARISON

```tsx
export function SlideComparison() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 flex flex-col justify-center px-[140px]">
        <SectionTag label="[08] — Comparison" delay={0.1} />
        <motion.h2 style={FONT_SANS} className="mb-12 mt-6 text-[52px] font-black" {...fadeUp(0.2)}>
          BEFORE <span style={{ color: "var(--slide-text-dim)" }}>&</span>{" "}
          <span style={{ color: "var(--slide-accent)" }}>AFTER</span>
        </motion.h2>
        <div className="grid grid-cols-2 gap-16">
          <motion.div className="p-12" style={{ border: `1px solid var(--slide-border)` }} {...slideRight(0.3)}>
            <span className="text-[14px] tracking-[0.3em]" style={{ ...FONT_MONO, color: "var(--slide-warning)" }}>BEFORE</span>
            <ul className="mt-8 space-y-5">
              {["Problem one", "Problem two", "Problem three"].map((text, i) => (
                <motion.li key={text} className="flex items-center gap-4 text-[20px]"
                  style={{ ...FONT_MONO, color: "var(--slide-text-dim)" }} {...fadeUp(stagger(i, 0.4))}>
                  <span style={{ color: "var(--slide-warning)" }}>x</span> {text}
                </motion.li>
              ))}
            </ul>
          </motion.div>
          <motion.div className="p-12"
            style={{ border: `1px solid var(--slide-accent)`, opacity: 0.3, background: `var(--slide-accent)`, backgroundOpacity: 0.03 }}
            {...slideLeft(0.3)}>
            <span className="text-[14px] tracking-[0.3em]" style={{ ...FONT_MONO, color: "var(--slide-accent)" }}>AFTER</span>
            <ul className="mt-8 space-y-5">
              {["Solution one", "Solution two", "Solution three"].map((text, i) => (
                <motion.li key={text} className="flex items-center gap-4 text-[20px]"
                  style={FONT_MONO} {...fadeUp(stagger(i, 0.4))}>
                  <span style={{ color: "var(--slide-accent)" }}>+</span> {text}
                </motion.li>
              ))}
            </ul>
          </motion.div>
        </div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Split 50/50 or 60/40. Differentiate by color+form, never color alone. 16:9=horizontal, 9:16=vertical stack.

---

### 4.6 METRIC

```tsx
export function SlideBigNumber() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <motion.span className="text-[16px] uppercase tracking-[0.3em]"
          style={{ ...FONT_MONO, color: "var(--slide-text-dim)" }} {...fadeUp(0.1)}>
          Key metric label
        </motion.span>
        <motion.span
          className="mt-4 text-[240px] font-black leading-none tracking-tighter"
          style={{ ...FONT_SANS, color: "var(--slide-accent)" }}
          initial={{ opacity: 0, scale: 0.7 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.3, ease: EASE_SPRING } as Transition}
        >
          10x
        </motion.span>
        <motion.span className="mt-6 text-[24px]" style={FONT_MONO} {...fadeUp(0.6)}>
          Compared to baseline
        </motion.span>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: 1-3 metrics. Value=title_xl/Black/mono. Label=caption. scaleIn stagger 0.15s.

---

### 4.7 DATA-VIZ (Bar Chart)

```tsx
export function SlideBarChart() {
  const data = [
    { label: "JAN", value: 45 }, { label: "FEB", value: 62 },
    { label: "MAR", value: 78 }, { label: "APR", value: 91 },
  ]
  const max = Math.max(...data.map((d) => d.value))

  return (
    <SlideLayout>
      <div className="absolute inset-0 flex flex-col justify-center px-[180px]">
        <SectionTag label="[12] — Revenue" delay={0.1} />
        <motion.h2 style={FONT_SANS} className="mt-6 text-[52px] font-black" {...fadeUp(0.2)}>
          REVENUE <span style={{ color: "var(--slide-accent)" }}>GREW 40%</span>
        </motion.h2>
        <div className="mt-16 flex h-[420px] items-end gap-6">
          {data.map((item, i) => {
            const height = (item.value / max) * 100
            return (
              <motion.div key={item.label} className="flex flex-1 flex-col items-center gap-4" {...fadeUp(stagger(i, 0.3))}>
                <span className="text-[18px]" style={{ ...FONT_MONO, color: "var(--slide-accent)" }}>{item.value}%</span>
                <div className="relative w-full origin-bottom" style={{ height: `${height * 3.6}px` }}>
                  <motion.div className="absolute inset-0 origin-bottom"
                    style={{ border: `1px solid var(--slide-accent)`, opacity: 0.4, background: "var(--slide-accent)", backgroundOpacity: 0.2 }}
                    {...growHeight(stagger(i, 0.35), 1)} />
                </div>
                <span className="text-[14px] tracking-wider" style={{ ...FONT_MONO, color: "var(--slide-text-dim)" }}>{item.label}</span>
              </motion.div>
            )
          })}
        </div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Title=CONCLUSION not description. Chart ≥ 60%. Max 3 series. Colors: primary=accent, secondary=text@60%, tertiary=text_dim. Never color-only. Source in label/mono bottom. Max elements: 6 bars, 8 horiz, 12 line points, 4 pie slices. No scatter/heatmap/treemap/sankey.

---

### 4.8 IMAGE

```tsx
export function SlideFullImage() {
  return (
    <SlideLayout>
      <motion.img src="{{image_url}}" alt="{{image_alt}}" className="h-full w-full object-cover"
        initial={{ scale: 1.1, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 1.2, ease: EASE_SMOOTH } as Transition}
      />
      <div className="absolute inset-0"
        style={{ background: `linear-gradient(to top, var(--slide-bg) 0%, transparent 60%)` }} />
      <motion.div className="absolute bottom-[100px] left-[140px]" {...fadeUp(0.5)}>
        <SectionTag label="[07] — Impact" delay={0.5} />
        <motion.h2 style={FONT_SANS} className="mt-4 text-[72px] font-black leading-[0.95]" {...fadeUp(0.7)}>
          VISIBLE
          <br />
          <span style={{ color: "var(--slide-accent)" }}>RESULTS</span>
        </motion.h2>
      </motion.div>
    </SlideLayout>
  )
}
```

**Rules**: Image ≥ 60%. Caption max 8 words. Overlay 60-80% if text over image. Min 1920px. WebP ≤ 500KB. Screenshots: TechFrame or border. No stock photos.

---

### 4.9 BUILD (Timeline)

```tsx
export function SlideTimeline() {
  const phases = [
    { num: "01", title: "PHASE 1", desc: "Description", time: "Week 1-2" },
    { num: "02", title: "PHASE 2", desc: "Description", time: "Week 3-4" },
    { num: "03", title: "PHASE 3", desc: "Description", time: "Week 5-6" },
  ]

  return (
    <SlideLayout>
      <div className="absolute inset-0 flex flex-col justify-center px-[140px]">
        <SectionTag label="[11] — Roadmap" delay={0.1} />
        <motion.h2 style={FONT_SANS} className="mb-16 mt-6 text-[52px] font-black" {...fadeUp(0.2)}>
          EXECUTION <span style={{ color: "var(--slide-accent)" }}>ROADMAP</span>
        </motion.h2>
        <div className="flex gap-0">
          {phases.map((phase, i) => (
            <motion.div key={phase.num} className="relative flex-1 p-8"
              style={{ border: `1px solid var(--slide-border)` }} {...scaleIn(stagger(i, 0.3))}>
              <span className="text-[48px] font-black leading-none" style={{ ...FONT_SANS, color: "var(--slide-accent)" }}>{phase.num}</span>
              <h3 className="mt-4 text-[24px] font-black" style={FONT_SANS}>{phase.title}</h3>
              <p className="mt-3 text-[16px]" style={{ ...FONT_MONO, color: "var(--slide-text-dim)" }}>{phase.desc}</p>
              <span className="mt-4 inline-block text-[12px] tracking-wider"
                style={{ ...FONT_MONO, color: "var(--slide-accent)", opacity: 0.6 }}>{phase.time}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: 2-5 steps. Future=15% opacity (progressive). Async=all visible. Horizontal or vertical.

---

### 4.10 CODE

```tsx
export function SlideCode() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 flex flex-col justify-center px-[200px]">
        <SectionTag label="[XX] — Code" delay={0.1} />
        <motion.h2 style={FONT_SANS} className="mt-6 mb-12 text-[52px] font-black" {...fadeUp(0.2)}>
          IMPLEMENTATION
        </motion.h2>
        <motion.div className="overflow-hidden rounded"
          style={{ border: `1px solid var(--slide-border)`, background: "var(--slide-surface)" }}
          {...scaleIn(0.3)}>
          <div className="flex items-center gap-2 px-6 py-3"
            style={{ borderBottom: `1px solid var(--slide-border)` }}>
            <span className="text-[13px] tracking-wider" style={{ ...FONT_MONO, color: "var(--slide-accent)" }}>
              typescript
            </span>
          </div>
          <pre className="p-8 text-[24px] leading-relaxed" style={FONT_MONO}>
            <code>{`const agent = new Agent({
  name: "architect",
  tools: ["read", "write"],
});

await agent.execute(task);`}</code>
          </pre>
        </motion.div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Mono font, min body size. Language label on top. Highlight=accent@15% bg. Max 12 lines. NEVER screenshot code.

---

### 4.11 CLOSING

```tsx
export function SlideCTA() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 opacity-[0.08]"
        style={{ background: `radial-gradient(ellipse at 50% 40%, var(--slide-accent), transparent 60%)` }} />
      <CornerMarks opacity={0.15} />
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <motion.h2 style={FONT_SANS} className="text-[90px] font-black leading-[0.9] tracking-[-2px]" {...fadeUp(0.2)}>
          THANK YOU.
        </motion.h2>
        <motion.div className="mt-10 flex items-center gap-6" {...fadeUp(0.4)}>
          <motion.div className="h-[2px] w-16 origin-left" style={{ background: "var(--slide-accent)" }} {...growWidth(0.5)} />
          <span className="text-[20px] tracking-[0.3em]" style={{ ...FONT_MONO, color: "var(--slide-text-dim)" }}>QUESTIONS?</span>
          <motion.div className="h-[2px] w-16 origin-right" style={{ background: "var(--slide-accent)" }} {...growWidth(0.5)} />
        </motion.div>
        <motion.div className="mt-16 flex flex-col items-center gap-3" {...fadeUp(0.7)}>
          <span className="text-[16px] tracking-[0.2em]" style={{ ...FONT_MONO, color: "var(--slide-text-dim)" }}>{{brand.url}}</span>
        </motion.div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Title lg/Black/max 5 words. Text CTA only — no buttons. CornerMarks allowed. Last slide.

---

### 4.12 QUOTE

```tsx
export function SlideQuote() {
  return (
    <SlideLayout>
      <CornerMarks opacity={0.2} />
      <div className="absolute inset-0 flex flex-col items-center justify-center px-[240px] text-center">
        <motion.div className="text-[140px] font-black leading-none"
          style={{ ...FONT_SANS, color: "var(--slide-accent)" }} {...scaleIn(0.1)}>
          &ldquo;
        </motion.div>
        <motion.blockquote className="mt-[-24px] text-[44px] leading-[1.3]" style={FONT_MONO} {...fadeUp(0.3)}>
          Quote text goes here.
          <span style={{ color: "var(--slide-accent)" }}> Highlighted portion.</span>
        </motion.blockquote>
        <motion.div className="mt-14 flex items-center gap-4" {...fadeUp(0.6)}>
          <motion.div className="h-[1px] w-12 origin-left" style={{ background: "var(--slide-accent)" }} {...growWidth(0.7)} />
          <span className="text-[16px] uppercase tracking-[0.25em]" style={{ ...FONT_MONO, color: "var(--slide-text-dim)" }}>
            Name — Company
          </span>
          <motion.div className="h-[1px] w-12 origin-right" style={{ background: "var(--slide-accent)" }} {...growWidth(0.7)} />
        </motion.div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Third-party quotes with attribution. Visual `&ldquo;`. Mono for quote text.

---

## 5. SEQUENCE RULES

```
FIRST  = TITLE
LAST   = CLOSING
BREAKS = SECTION_BREAK between thematic blocks

Max consecutive same type = 3
Max time per slide = 120s
Insert rhythm resets in long sequences
```

| Type | Duration (s) |
|---|---|
| TITLE | 10-15 |
| SECTION-BREAK | 3-5 |
| STATEMENT | 5-10 |
| CONTENT | 20-40 |
| COMPARISON | 20-40 |
| METRIC | 10-20 |
| DATA-VIZ | 30-60 |
| IMAGE | 5-15 |
| BUILD | 15-30/step |
| CODE | 30-60 |
| CLOSING | 10-20 |

---

## 6. ANIMATION RULES

```
IF mode == "async": SKIP ALL
IF mode == "live":  Reduce delays 30%
IF mode == "palco": Normal

Max 3 animation types per slide
Max total delay 1.5s
Flash ≤ 3 per second
```

Implement `prefers-reduced-motion` and `useReducedMotion` hook (see section 1 CSS).

For complex animations, validate with **PEAT** (Photosensitive Epilepsy Analysis Tool). Note: current version (2017) has limitations with modern video formats — convert to .AVI if needed.

---

## 7. VALIDATION CHECKLIST

### Per slide (ALL must pass)

- [ ] Single idea
- [ ] Comprehensible in 3 seconds
- [ ] `style={FONT_SANS}` or `style={FONT_MONO}` on every text element
- [ ] All colors via `var(--slide-*)` — zero hardcoded hex
- [ ] Whitespace ≥ mode minimum
- [ ] Zero paragraphs (except Async max 1)
- [ ] Zero clickable buttons
- [ ] Alt text on images
- [ ] Unique accessible slide title

### KILLER ITEMS (block approval)

1. Contrast < WCAG AA (4.5:1 body / 3:1 title)
2. Missing font inline style
3. More than 15 words in Palco/Live
4. Paragraph in Palco/Live
5. Code as screenshot
6. `text_secondary` below `#777777`
7. Hardcoded brand color (hex instead of CSS var)

### Per sequence

- [ ] First = TITLE, Last = CLOSING
- [ ] Section breaks between thematic blocks
- [ ] No slide > 2 minutes
- [ ] Never > 3 consecutive same type

---

## 8. ANTI-PATTERNS

| Forbidden | Why |
|---|---|
| Text paragraphs | Slides are not documents |
| Font < body in Palco | Illegible on projector |
| > 4 bullets (Palco/Live) | Cognitive overload |
| Clickable buttons | No mouse on stage |
| Hover effects | No mouse on stage |
| Fill all space | Whitespace = focus |
| > 3 colors per slide | Visual pollution |
| Animations > 1.5s total | Audience loses patience |
| Hardcoded px for sizing | Breaks responsiveness |
| Code screenshots | Inaccessible |
| Generic stock photos | Destroys credibility |
| > 1 chart per slide | Visual competition |
| Color-only differentiation | Colorblind inaccessible |
| No accessible title | Invisible to screen readers |
| Hardcoded hex colors | Breaks brand portability |

---

*SOP-SLIDES-003 v1.1.0 — Brand-Agnostic LLM Execution Reference*
*Stack: React + TypeScript + Framer Motion + Tailwind*
*Template: sop-human-tmpl.md | SOP Factory | Synkra AIOX*
