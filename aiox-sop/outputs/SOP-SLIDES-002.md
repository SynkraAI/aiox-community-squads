# SOP-SLIDES-002 — AIOX Slide Creation: LLM Execution Reference

| Field | Value |
|---|---|
| **SOP ID** | SOP-SLIDES-002 |
| **Version** | 1.1.0 |
| **Effective Date** | 2026-03-16 |
| **Classification** | Internal |
| **Status** | DRAFT |
| **Companion To** | SOP-SLIDES-001 (human-readable process) |
| **Consumer** | LLM agents generating slide code |
| **Source of Truth** | AIOX Slide Design Manual v2.1 |
| **Codebase** | `apps/ds/src/components/brandbook/slides/` |

---

## 1. IMPORTS — COPY THIS BLOCK

Every slide file starts with this import. Select only what you use.

```tsx
"use client"

import { motion, type Transition } from "framer-motion"

import {
  CornerMarks,
  EASE_SMOOTH,
  EASE_SPRING,
  fadeIn,
  fadeUp,
  FONT_MONO,
  FONT_SANS,
  growHeight,
  growWidth,
  ImagePlaceholder,
  MetaBar,
  scaleIn,
  SectionTag,
  slideLeft,
  slideRight,
  SlideLayout,
  stagger,
  TechFrame,
  Watermark,
  WatermarkNumber,
} from "@/components/brandbook/slides/shared"
```

---

## 2. COMPONENT API — SHARED.TSX CONTRACTS

### 2.1 SlideLayout

```tsx
<SlideLayout className="">
  {children}
</SlideLayout>
```

- Renders `motion.div` at **1920×1080**, `overflow-hidden`
- Default: `bg: --bb-dark`, `color: --bb-cream`, `font: FONT_SANS`
- For lime background: `<SlideLayout className="!bg-[var(--bb-lime)]">`

### 2.2 Font Constants

```tsx
export const FONT_SANS = { fontFamily: "var(--font-bb-sans, 'Geist', system-ui, sans-serif)" }
export const FONT_MONO = { fontFamily: "var(--font-bb-mono, 'Geist Mono', monospace)" }
```

**RULE**: Every element with custom font MUST have `style={FONT_SANS}` or `style={FONT_MONO}` inline.

### 2.3 Animation Presets

| Function | Returns | Use for |
|---|---|---|
| `fadeUp(delay)` | `{ initial: {opacity:0, y:20}, animate: {opacity:1, y:0}, transition: {duration:0.5, delay, ease:EASE_SMOOTH} }` | Titles, text blocks |
| `fadeIn(delay)` | `{ initial: {opacity:0}, animate: {opacity:1}, transition: {duration:0.4, delay, ease:EASE_SMOOTH} }` | Backgrounds, subtle elements |
| `slideRight(delay)` | `{ initial: {opacity:0, x:-40}, animate: {opacity:1, x:0}, transition: {duration:0.6, delay, ease:EASE_SMOOTH} }` | Content entering from left |
| `slideLeft(delay)` | `{ initial: {opacity:0, x:40}, animate: {opacity:1, x:0}, transition: {duration:0.6, delay, ease:EASE_SMOOTH} }` | Content entering from right |
| `scaleIn(delay)` | `{ initial: {opacity:0, scale:0.88}, animate: {opacity:1, scale:1}, transition: {duration:0.45, delay, ease:EASE_SPRING} }` | Cards, metrics, grids |
| `growWidth(delay)` | `{ initial: {scaleX:0}, animate: {scaleX:1}, transition: {duration:0.7, delay, ease:EASE_SMOOTH} }` | Horizontal lines, progress |
| `growHeight(delay, dur?)` | `{ initial: {scaleY:0}, animate: {scaleY:1}, transition: {duration:dur\|0.7, delay, ease:EASE_SMOOTH} }` | Vertical lines, bar charts |
| `stagger(i, base)` | `base + i * 0.08` | Lists and grids timing |

**Usage**: Spread on `motion.*` elements: `<motion.h1 {...fadeUp(0.3)}>`

**Easing**:
- `EASE_SMOOTH: [0.25, 0.1, 0.25, 1]`
- `EASE_SPRING: [0.34, 1.56, 0.64, 1]`

### 2.4 Decorative Components

```tsx
// Corner registration marks — max 2 per deck section
<CornerMarks color="var(--bb-lime)" opacity={0.3} />

// Giant semi-transparent number — 16rem, 4% opacity
<WatermarkNumber n="02" className="left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2" />

// Top metadata bar — 56px height
<MetaBar left="AIOX SQUAD" center="Confidential" right="2026" />

// Section label — uppercase mono, animated
<SectionTag label="[01] - Apresentacao" delay={0.1} />

// Clipped-corner frame
<TechFrame className="">{children}</TechFrame>

// Bottom watermark
<Watermark />

// Image placeholder (dev only)
<ImagePlaceholder label="IMG" size="1920 x 1080" />
```

### 2.5 PageFooter Pattern

Not a shared component. Inline it manually:

```tsx
<div className="absolute bottom-[40px] left-[200px] right-[200px] flex items-center border-t border-bb-border/20 pt-3" style={FONT_MONO}>
  <span className="text-[11px] uppercase tracking-[0.15em] text-bb-dim/40">Section Name</span>
  <span className="mx-4 h-px flex-1 bg-bb-border/10" />
  <span className="text-[11px] uppercase tracking-[0.15em] text-bb-dim/40">02</span>
  <span className="mx-4 h-px flex-1 bg-bb-border/10" />
  <span className="text-[11px] uppercase tracking-[0.15em] text-bb-dim/40">AIOX SQUAD.</span>
</div>
```

### 2.6 Inline Highlight Pattern

```tsx
<span style={{ background: "var(--bb-lime)", color: "var(--bb-dark)", padding: "0.05em 0.2em" }}>
  KEYWORD
</span>
```

Max 2 per slide.

---

## 3. DESIGN TOKENS — HARD VALUES

### Colors

| Token | Value | Use |
|---|---|---|
| `--bb-dark` | `#050505` | Default background (80% of slides) |
| `--bb-lime` | `#D1FF00` | Accent, emphasis, section breaks |
| `--bb-cream` | `#FFFDD0` | Primary text on dark |
| `--bb-dim` | Must be ≥ `#777777` | Secondary text. WCAG AA minimum |
| `--bb-surface` | Theme-defined | Cards, internal panels |
| `--bb-border` | Theme-defined | Borders, dividers |
| `--bb-flare` | Theme-defined | Warning/alert accent |

### Contrast (verified)

| Combo | Ratio |
|---|---|
| cream on dark | 19.62:1 AAA |
| lime on dark | 17.48:1 AAA |
| dark on lime | 17.48:1 AAA |
| dim (#777) on dark | 4.55:1 AA |
| dim (#999) on dark | 7.15:1 AAA |

### Typography Scale

| Token | Value | Use |
|---|---|---|
| `--slide-title-xl` | `clamp(48px, 6.8vw, 130px)` | Hero statements |
| `--slide-title-lg` | `clamp(40px, 3.3vw, 64px)` | Slide titles |
| `--slide-title-md` | `clamp(32px, 2.5vw, 48px)` | Subtitles |
| `--slide-body` | `clamp(24px, 1.9vw, 36px)` | Keywords, bullets |
| `--slide-caption` | `clamp(16px, 1.5vw, 28px)` | Captions |
| `--slide-label` | `clamp(13px, 0.7vw, 14px)` | Metadata, tags |

**Floor**: No text below 13px. In Palco mode, labels must render ≥ 16px.

### Font Weights

| Weight | CSS | Use |
|---|---|---|
| 900 (Black) | `font-black` | Impact titles, big numbers |
| 700 (Bold) | `font-bold` | Subtitles, names |
| 500 (Medium) | `font-medium` | Labels, metadata |
| 400 (Regular) | — | Body text (Async mode only) |

---

## 4. DECISION: FORMAT → MODE → OVERRIDES

**IMPORTANT**: Determine the presentation FORMAT first. Format defines the mode and applies overrides.

### 4.0 Format Selection

```
IF format == "ted_keynote":
  mode = "palco"
  overrides: bullets = NEVER, text = minimal (0-1 sentence), slides = 40-90
  slides_per_min = 2-3, self_explanatory = NEVER
  dominant_types = [STATEMENT, IMAGE, METRIC, SECTION_BREAK]
  rare_types = [CONTENT, CODE, DATA_VIZ]
  narrative = "hook → tension → resolution → CTA"
  anti_pattern = "slide that works without narrator steals attention"

ELSE IF format == "pitch_deck":
  mode = "palco" (live) + "async" (leave-behind)
  overrides: slides = 10-15, data = essential, min_font = 30pt
  structure = "Sequoia: Purpose→Problem→Solution→Why Now→Market→Competition→Product→Model→Team→Financials"
  alt_structure = "YC: Title→Problem→Solution→Traction→Market→Product→Model→Team→Financials→Ask"
  versions = 2 (live + leave-behind with more text)
  anti_pattern_fatal = "We have no competition"
  dominant_types = [TITLE, CONTENT, METRIC, DATA_VIZ, COMPARISON, CLOSING]

ELSE IF format == "sales_deck":
  mode = "palco" (live) + "async" (leave-behind for champion)
  overrides: slides = SMB:8-12 / Mid:12-18 / Enterprise:18-25
  framework = "SCR: Situation → Complication → Resolution"
  structure = "Hook→Pain→Cost of inaction→Solution→How it works→Proof→Differentiation→Pricing/Next step"
  personalization = "customize per ICP, minimum: opening slide"
  leave_behind = "must work as autonomous seller for internal champion"
  dominant_types = [TITLE, CONTENT, COMPARISON, METRIC, DATA_VIZ, IMAGE, CLOSING]

ELSE IF format == "technical":
  mode = "palco"
  overrides: slides_per_min = 1-2, CODE type = legitimate
  code_min_font = "20pt (mono is wider)", backup_slides = "5-10 for Q&A"
  structure = "Problem→Context→Approach→Implementation(BUILD)→Results(DATA_VIZ)→Limitations→Conclusion"
  legibility_test = "Step back 2m from monitor. Can you read it?"
  dominant_types = [CONTENT, BUILD, CODE, DATA_VIZ, COMPARISON, IMAGE]
  anti_pattern = "copy academic paper to slides"

ELSE IF format == "zoom_virtual":
  mode = "live" (mandatory)
  overrides: visual_movements = "2+ per minute", interaction_placeholder = "every 3-5 min"
  slide_is_main_focus = true (no body language visible)
  breathing_slides = "section breaks + recaps per section"
  center_text = true (edges may be cropped)
  dominant_types = all (STATEMENT and SECTION_BREAK gain importance as attention reset)

ELSE IF format == "carousel_stories":
  mode = "async"
  overrides: ratio = "9:16 or 1:1", slides = 5-10, bullets = NEVER
  first_slide = "visual hook (decides if viewer continues)"
  last_slide = "CTA: Save, Share, Link in bio"
  max_words = 15, font = extra-large (fast scroll at ~30cm)
  dominant_types = [STATEMENT, CONTENT (simplified), METRIC, CLOSING]
```

### 4.1 Mode Selection (after format)

```
IF context in [conference, keynote, workshop, presencial]:
  mode = "palco"
  max_words = 15
  min_font = "2.2vw"
  whitespace >= 50%
  animations = true
  speaker_notes = required

ELSE IF context in [youtube, twitch, screenshare, live_call]:
  mode = "live"
  max_words = 15
  min_font = "2.2vw"
  whitespace >= 45%
  animations = true (reduce delays 30%)
  safe_zone_right = 20%
  safe_zone_bottom = 15%
  speaker_notes = required

ELSE IF context in [post_event, course, onboarding, pdf_export]:
  mode = "async"
  max_words = 30
  min_font = "1.6vw"
  whitespace >= 40%
  animations = false
  speaker_notes = not_needed (content on slide)
```

---

## 5. DECISION: ASPECT RATIO

```
IF channel in [projector, monitor, stream]: ratio = "16:9", ref = "1920x1080"
ELSE IF channel in [macbook, mac_projector]:  ratio = "16:10", ref = "1920x1200"
ELSE IF channel in [stories, reels, vertical]: ratio = "9:16", ref = "1080x1920"
ELSE IF channel in [instagram, carousel]:     ratio = "1:1", ref = "1080x1080"
ELSE: ratio = "16:9" (default)
```

For mobile containers: use `100svh` not `100vh`. `svh` (small viewport) measures height with browser chrome visible — guarantees the slide fits. Avoid `dvh` (causes layout shifts) and `lvh` (legacy behavior).

---

## 6. SLIDE TYPE PATTERNS — 1 CANONICAL EXAMPLE EACH

### 6.1 TITLE

```tsx
export function SlideTitleHero() {
  return (
    <SlideLayout>
      <CornerMarks />
      <WatermarkNumber n="01" className="right-[80px] top-[80px]" />
      <MetaBar left="AIOX SQUAD" center="Confidential" right="2026" />
      <div className="absolute inset-0 flex flex-col justify-center px-[140px]">
        <SectionTag label="[01] - Apresentacao" delay={0.1} />
        <motion.h1
          style={FONT_SANS}
          className="mt-8 font-bb-sans text-[130px] font-black leading-[0.85] tracking-[-4px]"
          {...fadeUp(0.3)}
        >
          STRATEGIC
          <br />
          <span className="text-bb-lime">BRIEFING</span>
        </motion.h1>
        <motion.div className="mt-14 flex items-center gap-4" {...fadeUp(0.6)}>
          <motion.div className="h-[2px] w-16 origin-left bg-bb-lime" {...growWidth(0.7)} />
          <p className="font-bb-mono text-[18px] tracking-[0.3em] text-bb-dim">AIOX SQUAD // Q1 2026</p>
        </motion.div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Title xl/Black/max 5 words. CornerMarks + MetaBar allowed. First slide.

---

### 6.2 SECTION-BREAK

```tsx
export function SlideSectionBreak() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 opacity-[0.04]" style={{ background: "radial-gradient(ellipse at 50% 50%, var(--bb-lime), transparent 60%)" }} />
      <CornerMarks opacity={0.2} />
      <WatermarkNumber n="02" className="left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2" />
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <motion.div className="h-[100px] w-[1px] origin-top bg-bb-lime/40" {...growHeight(0.1)} />
        <motion.span className="my-8 font-bb-mono text-[16px] uppercase tracking-[0.5em] text-bb-dim" {...fadeIn(0.3)}>
          Parte 02
        </motion.span>
        <motion.h2 style={FONT_SANS} className="font-bb-sans text-[140px] font-black leading-none tracking-[-3px]" {...scaleIn(0.4)}>
          FRAMEWORK
        </motion.h2>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Title lg/Black/max 3 words. Full center. WatermarkNumber 4% opacity. NO PageFooter. 3-5s on screen.

---

### 6.3 STATEMENT

```tsx
export function SlideStatementBold() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 flex items-center justify-center px-[120px] text-center">
        <motion.h1
          className="font-bb-sans text-[110px] font-black uppercase leading-[0.9] tracking-[-3px]"
          style={FONT_SANS}
          {...scaleIn(0.2)}
        >
          3 PROJETOS
          <br />
          <span className="text-bb-dim">+ 6 DIGITOS</span>
          <br />
          <span className="text-bb-lime">15 DIAS</span>
        </motion.h1>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Max 10 words total. Full center. bg dark only. Whitespace ≥ 60%. Max 2 lime highlights.

---

### 6.4 CONTENT

```tsx
export function SlideBulletList() {
  const items = [
    { num: "I", title: "SETUP", desc: "Workspace configurado com 10+ agentes especializados." },
    { num: "II", title: "INTEGRACAO", desc: "Workflows conectados ao seu stack existente." },
    { num: "III", title: "DASHBOARD", desc: "Metricas e performance em tempo real." },
    { num: "IV", title: "ESCALA", desc: "Quality gates automaticos. Suporte continuo." },
  ]

  return (
    <SlideLayout>
      <CornerMarks opacity={0.12} />
      <div className="absolute inset-0 flex flex-col justify-center px-[200px]">
        <motion.div className="mb-2 border-t-[4px] border-bb-lime pt-4" {...fadeUp(0.1)}>
          <span className="font-bb-sans text-[52px] font-black" style={FONT_SANS}>
            6. O QUE VOCE RECEBE.
          </span>
        </motion.div>
        <motion.span className="mb-10 font-bb-mono text-[14px] tracking-[0.2em] text-bb-dim" style={FONT_MONO} {...fadeIn(0.2)}>
          JORNADA DE IMPLEMENTACAO // 4 FASES
        </motion.span>
        <div className="flex flex-col">
          {items.map((item, i) => (
            <motion.div key={item.num} className="flex gap-6 py-6"
              style={{ borderBottom: i < items.length - 1 ? "1px solid rgba(244, 244, 232, 0.1)" : "none" }}
              {...slideRight(stagger(i, 0.3))}
            >
              <div className="flex h-[56px] w-[56px] shrink-0 items-center justify-center bg-bb-lime" style={FONT_MONO}>
                <span className="text-[22px] font-bold" style={{ color: "var(--bb-dark)" }}>{item.num}</span>
              </div>
              <div>
                <h3 className="mb-2 font-bb-sans text-[26px] font-black uppercase" style={FONT_SANS}>{item.title}</h3>
                <p className="text-[24px] leading-[1.3] text-bb-dim" style={FONT_SANS}>{item.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
      {/* PageFooter inline */}
      <div className="absolute bottom-[40px] left-[200px] right-[200px] flex items-center border-t border-bb-border/20 pt-3" style={FONT_MONO}>
        <span className="text-[11px] uppercase tracking-[0.15em] text-bb-dim/40">Entrega</span>
        <span className="mx-4 h-px flex-1 bg-bb-border/10" />
        <span className="text-[11px] uppercase tracking-[0.15em] text-bb-dim/40">06</span>
        <span className="mx-4 h-px flex-1 bg-bb-border/10" />
        <span className="text-[11px] uppercase tracking-[0.15em] text-bb-dim/40">AIOX SQUAD.</span>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: SectionTag + title lg/Black + 3-4 keywords. Left-aligned. PageFooter. Whitespace ≥ 50%. Keywords not sentences.

---

### 6.5 COMPARISON

```tsx
export function SlideComparison() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 flex flex-col justify-center px-[140px]">
        <SectionTag label="[08] - Comparativo" delay={0.1} />
        <motion.h2 style={FONT_SANS} className="mb-12 mt-6 font-bb-sans text-[52px] font-black" {...fadeUp(0.2)}>
          ANTES <span className="text-bb-dim">&</span> <span className="text-bb-lime">DEPOIS</span>
        </motion.h2>
        <div className="grid grid-cols-2 gap-16">
          <motion.div className="border border-bb-border p-12" {...slideRight(0.3)}>
            <span className="font-bb-mono text-[14px] tracking-[0.3em] text-bb-flare">ANTES</span>
            <ul className="mt-8 space-y-5">
              {["Processos manuais", "Horas em tarefas operacionais", "Sem padrao de qualidade"].map((text, i) => (
                <motion.li key={text} className="flex items-center gap-4 font-bb-mono text-[20px] text-bb-dim" {...fadeUp(stagger(i, 0.4))}>
                  <span className="text-bb-flare">x</span> {text}
                </motion.li>
              ))}
            </ul>
          </motion.div>
          <motion.div className="border border-bb-lime/30 bg-bb-lime/[0.03] p-12" {...slideLeft(0.3)}>
            <span className="font-bb-mono text-[14px] tracking-[0.3em] text-bb-lime">DEPOIS</span>
            <ul className="mt-8 space-y-5">
              {["Agentes executam autonomamente", "Minutos para resultados", "Quality gates automaticos"].map((text, i) => (
                <motion.li key={text} className="flex items-center gap-4 font-bb-mono text-[20px]" {...fadeUp(stagger(i, 0.4))}>
                  <span className="text-bb-lime">+</span> {text}
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

**Rules**: Split 50/50 or 60/40. Differentiate by color+form (border style, icon), never color alone. 16:9=horizontal, 9:16=stack vertical.

---

### 6.6 METRIC

```tsx
export function SlideBigNumber() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <motion.span className="font-bb-mono text-[16px] uppercase tracking-[0.3em] text-bb-dim" {...fadeUp(0.1)}>
          Velocidade de entrega
        </motion.span>
        <motion.span
          style={FONT_SANS}
          className="mt-4 font-bb-sans text-[240px] font-black leading-none tracking-tighter text-bb-lime"
          initial={{ opacity: 0, scale: 0.7 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.3, ease: EASE_SPRING } as Transition}
        >
          10x
        </motion.span>
        <motion.span className="mt-6 font-bb-mono text-[24px]" {...fadeUp(0.6)}>
          Mais rapido que o processo manual
        </motion.span>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: 1-3 metrics. Value in title-xl/Black/mono. Label in caption/Medium. scaleIn with stagger 0.15s. Grid 1×1, 1×2, or 1×3.

---

### 6.7 DATA-VIZ (Bar Chart)

```tsx
export function SlideBarChart() {
  const data = [
    { label: "JAN", value: 45 }, { label: "FEV", value: 62 },
    { label: "MAR", value: 78 }, { label: "ABR", value: 55 },
    { label: "MAI", value: 91 }, { label: "JUN", value: 84 },
  ]
  const max = Math.max(...data.map((d) => d.value))

  return (
    <SlideLayout>
      <div className="absolute inset-0 flex flex-col justify-center px-[180px]">
        <SectionTag label="[33] - Revenue" delay={0.1} />
        <motion.h2 style={FONT_SANS} className="mt-6 font-bb-sans text-[52px] font-black" {...fadeUp(0.2)}>
          CRESCIMENTO <span className="text-bb-lime">MENSAL</span>
        </motion.h2>
        <div className="mt-16 flex h-[420px] items-end gap-6">
          {data.map((item, i) => {
            const height = (item.value / max) * 100
            return (
              <motion.div key={item.label} className="flex flex-1 flex-col items-center gap-4" {...fadeUp(stagger(i, 0.3))}>
                <span className="font-bb-mono text-[18px] text-bb-lime">{item.value}%</span>
                <div className="relative w-full origin-bottom" style={{ height: `${height * 3.6}px` }}>
                  <motion.div className="absolute inset-0 origin-bottom border border-bb-lime/40 bg-bb-lime/20" {...growHeight(stagger(i, 0.35), 1)} />
                </div>
                <span className="font-bb-mono text-[14px] tracking-wider text-bb-dim">{item.label}</span>
              </motion.div>
            )
          })}
        </div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Title = CONCLUSION not description. Chart ≥ 60% area. Max 3 series. Max 6 bars (vertical), 8 (horizontal), 12 points (line), 4 slices (donut). Colors: primary=lime, secondary=cream@60%, tertiary=dim. Never differentiate by color alone. Source in label/mono bottom corner.

---

### 6.8 IMAGE

```tsx
export function SlideFullImage() {
  return (
    <SlideLayout>
      <motion.div className="h-full w-full"
        initial={{ scale: 1.1, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 1.2, ease: EASE_SMOOTH } as Transition}
      >
        <ImagePlaceholder />
      </motion.div>
      <div className="absolute inset-0" style={{ background: "linear-gradient(to top, var(--bb-dark) 0%, var(--bb-dark)/60 40%, transparent 100%)" }} />
      <motion.div className="absolute bottom-[100px] left-[140px]" {...fadeUp(0.5)}>
        <SectionTag label="[07] - Impact" delay={0.5} />
        <motion.h2 style={FONT_SANS} className="mt-4 font-bb-sans text-[72px] font-black leading-[0.95]" {...fadeUp(0.7)}>
          RESULTADOS
          <br />
          <span className="text-bb-lime">VISIVEIS</span>
        </motion.h2>
      </motion.div>
    </SlideLayout>
  )
}
```

**Rules**: Image ≥ 60% slide. Caption max 8 words. Overlay gradient 60-80% opacity if text over image. Min resolution 1920px for full-bleed. WebP preferred, max 500KB. Screenshots need TechFrame or 1px border. No stock photos.

---

### 6.9 BUILD (Timeline)

```tsx
export function SlideTimeline() {
  const phases = [
    { num: "01", title: "SETUP", desc: "Configuracao do workspace", weeks: "Sem 1-2" },
    { num: "02", title: "TRAINING", desc: "Treinamento dos agentes", weeks: "Sem 3-4" },
    { num: "03", title: "LAUNCH", desc: "Ativacao do sistema", weeks: "Sem 5-6" },
    { num: "04", title: "SCALE", desc: "Escalar a operacao", weeks: "Sem 7+" },
  ]

  return (
    <SlideLayout>
      <div className="absolute inset-0 flex flex-col justify-center px-[140px]">
        <SectionTag label="[11] - Jornada" delay={0.1} />
        <motion.h2 style={FONT_SANS} className="mb-16 mt-6 font-bb-sans text-[52px] font-black" {...fadeUp(0.2)}>
          ROADMAP DE <span className="text-bb-lime">EXECUCAO</span>
        </motion.h2>
        <div className="flex gap-0">
          {phases.map((phase, i) => (
            <motion.div key={phase.num} className="relative flex-1 border border-bb-border p-8" {...scaleIn(stagger(i, 0.3))}>
              <span style={FONT_SANS} className="font-bb-sans text-[48px] font-black leading-none text-bb-lime">{phase.num}</span>
              <h3 style={FONT_SANS} className="mt-4 font-bb-sans text-[24px] font-black">{phase.title}</h3>
              <p className="mt-3 font-bb-mono text-[16px] text-bb-dim">{phase.desc}</p>
              <span className="mt-4 inline-block font-bb-mono text-[12px] tracking-wider text-bb-lime/60">{phase.weeks}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: 2-5 steps. Future steps at 15% opacity (when progressive). Async mode: all visible. Horizontal (timeline) or vertical (list).

---

### 6.10 CODE

No template exists in codebase yet. Canonical pattern:

```tsx
export function SlideCode() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 flex flex-col justify-center px-[200px]">
        <SectionTag label="[XX] - Code" delay={0.1} />
        <motion.h2 style={FONT_SANS} className="mt-6 mb-12 font-bb-sans text-[52px] font-black" {...fadeUp(0.2)}>
          IMPLEMENTATION
        </motion.h2>
        <motion.div className="overflow-hidden rounded border border-bb-border bg-bb-surface" {...scaleIn(0.3)}>
          <div className="flex items-center gap-2 border-b border-bb-border px-6 py-3">
            <span className="font-bb-mono text-[13px] tracking-wider text-bb-lime" style={FONT_MONO}>typescript</span>
          </div>
          <pre className="p-8 font-bb-mono text-[24px] leading-relaxed" style={FONT_MONO}>
            <code>
{`const agent = new Agent({
  name: "architect",
  tools: ["read", "write", "bash"],
});

await agent.execute(task);`}
            </code>
          </pre>
        </motion.div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Geist Mono, min slide-body size. Language label on top. Highlight lines with lime@15% bg. Max 12 visible lines. Never screenshot code.

---

### 6.11 CLOSING

```tsx
export function SlideCTA() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 opacity-[0.08]" style={{ background: "radial-gradient(ellipse at 50% 40%, var(--bb-lime), transparent 60%)" }} />
      <CornerMarks opacity={0.15} />
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <motion.h2 style={FONT_SANS} className="relative z-10 font-bb-sans text-[90px] font-black leading-[0.9] tracking-[-2px]" {...fadeUp(0.2)}>
          OBRIGADO.
        </motion.h2>
        <motion.div className="relative z-10 mt-10 flex items-center gap-6" {...fadeUp(0.4)}>
          <motion.div className="h-[2px] w-16 origin-left bg-bb-lime" {...growWidth(0.5)} />
          <span className="font-bb-mono text-[20px] tracking-[0.3em] text-bb-dim">PERGUNTAS?</span>
          <motion.div className="h-[2px] w-16 origin-right bg-bb-lime" {...growWidth(0.5)} />
        </motion.div>
        <motion.div className="relative z-10 mt-16 flex flex-col items-center gap-3" {...fadeUp(0.7)}>
          <span className="font-bb-mono text-[16px] tracking-[0.2em] text-bb-dim">contato@aioxsquad.ai</span>
          <span className="font-bb-mono text-[16px] tracking-[0.2em] text-bb-dim">aioxsquad.ai</span>
        </motion.div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Title lg/Black/max 5 words. Contact in caption. CornerMarks allowed. Full center. Text CTA only — no clickable buttons. Last slide.

---

### 6.12 QUOTE (variant of STATEMENT)

```tsx
export function SlideQuote() {
  return (
    <SlideLayout>
      <div className="absolute inset-0 opacity-[0.03]" style={{ background: "radial-gradient(ellipse at 50% 30%, var(--bb-lime), transparent 60%)" }} />
      <CornerMarks opacity={0.2} />
      <div className="absolute inset-0 flex flex-col items-center justify-center px-[240px] text-center">
        <motion.div style={FONT_SANS} className="font-bb-sans text-[140px] font-black leading-none text-bb-lime" {...scaleIn(0.1)}>
          &ldquo;
        </motion.div>
        <motion.blockquote className="mt-[-24px] font-bb-mono text-[44px] leading-[1.3]" {...fadeUp(0.3)}>
          O AIOX transformou completamente a forma como eu opero meu negocio.
          <span className="text-bb-lime"> O que antes levava semanas, agora leva horas.</span>
        </motion.blockquote>
        <motion.div className="mt-14 flex items-center gap-4" {...fadeUp(0.6)}>
          <motion.div className="h-[1px] w-12 origin-left bg-bb-lime" {...growWidth(0.7)} />
          <span className="font-bb-mono text-[16px] uppercase tracking-[0.25em] text-bb-dim">Nome — Empresa</span>
          <motion.div className="h-[1px] w-12 origin-right bg-bb-lime" {...growWidth(0.7)} />
        </motion.div>
      </div>
    </SlideLayout>
  )
}
```

**Rules**: Use for third-party quotes with attribution. Visual quotes `&ldquo;`. Mono font for quote text. Attribution with dash separators.

---

## 7. SEQUENCE RULES

```
FIRST slide  = TITLE (always)
LAST slide   = CLOSING (always)
Between      = SECTION-BREAK between thematic blocks

Max consecutive same type = 3
Max time per slide = 120s (2 minutes)
Insert rhythm resets (SECTION-BREAK, IMAGE, STATEMENT) in long sequences
```

### Duration per type

| Type | Seconds |
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

### Rhythm patterns

| Sequence | Narrative effect |
|---|---|
| STATEMENT → CONTENT → CONTENT | Impact → detail → detail |
| METRIC → DATA-VIZ → CONTENT | Number → context → explanation |
| IMAGE → STATEMENT | Visual → emotional message |
| BUILD (3 steps) | Narrative progression |
| COMPARISON → STATEMENT | Contrast → conclusion |

---

## 8. ANIMATION RULES

```
IF mode == "async":
  DO NOT animate. Skip entirely.

IF mode == "live":
  Reduce all delays by 30%.

IF mode == "palco":
  Apply animations normally.

CONSTRAINTS:
  max_animation_types_per_slide = 3
  max_total_delay = 1.5s
  flash_per_second <= 3

ANIMATE:
  - Sequential steps (timeline, build)
  - Impact data reveal (big number)
  - Chart data (comparative)

DO NOT ANIMATE:
  - Decorative backgrounds
  - Slide title (must be immediate)
  - Content that makes sense all at once
```

### prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

```tsx
import { useReducedMotion } from "framer-motion"
const shouldReduceMotion = useReducedMotion()
```

For complex animations, validate with **PEAT** (Photosensitive Epilepsy Analysis Tool). Note: current version (2017) has limitations with modern video formats — convert to .AVI if needed.

---

## 9. VALIDATION CHECKLIST

### Per slide (MUST ALL PASS)

- [ ] Single idea
- [ ] Comprehensible in 3 seconds
- [ ] Type from taxonomy (section 6)
- [ ] `style={FONT_SANS}` or `style={FONT_MONO}` on every text element
- [ ] Zero hardcoded `px` outside of the fixed 1920×1080 canvas
- [ ] Whitespace ≥ mode minimum
- [ ] Zero paragraphs (except Async max 1 short)
- [ ] Zero clickable buttons/CTAs
- [ ] `prefers-reduced-motion` respected
- [ ] Alt text on images
- [ ] Unique accessible slide title

### KILLER ITEMS (block approval)

1. Contrast < WCAG AA (4.5:1 body / 3:1 title)
2. Missing `style={FONT_SANS}` or `style={FONT_MONO}` inline
3. More than 15 words in Palco/Live mode
4. Paragraph in Palco/Live mode
5. Code as screenshot instead of rendered text
6. `--bb-dim` below `#777777`

### Per sequence

- [ ] First = TITLE, Last = CLOSING
- [ ] Section breaks between thematic blocks
- [ ] No slide > 2 minutes on screen
- [ ] Never > 3 consecutive same type
- [ ] `npm run lint && npm run typecheck` = 0 errors

---

## 10. ANTI-PATTERNS — DO NOT GENERATE

| Forbidden | Why |
|---|---|
| Text paragraphs | Slides are not documents |
| Font < slide-body in Palco | Illegible on projector |
| More than 4 bullets (Palco/Live) | Cognitive overload |
| Clickable buttons | No mouse on stage |
| Hover effects | No mouse on stage |
| Fill all space | Whitespace = focus |
| More than 3 colors in one slide | Visual pollution |
| Animations > 1.5s total | Audience loses patience |
| Hardcoded px values | Breaks responsiveness |
| Code screenshots | Inaccessible, pixelates |
| Generic stock photos | Destroys credibility |
| More than 1 chart per slide | Visual competition |
| Color-only data differentiation | Inaccessible to colorblind |
| Self-explanatory slide in Palco | If it needs no narrator, it is a document |
| Narrator-dependent slide in Async | If it needs voice, info is missing |
| Slide without accessible title | Invisible to screen readers |
| `--bb-dim` below `#777777` | Fails WCAG AA |

---

## 11. FILE REGISTRY

| Category | Template files | Count |
|---|---|---|
| ESTRUTURA | templates-abertura.tsx | 5 |
| CONTEUDO | templates-conteudo.tsx | 11 |
| DADOS | templates-dados.tsx | 12 |
| VISUAL | templates-visual.tsx | 14 |
| SOCIAL | templates-social.tsx | 4 |
| BRAND | templates-brand.tsx | 4 |
| FECHAMENTO | templates-fechamento.tsx | 6 |
| **Total** | | **56** |

Registry: `slides/registry.ts` — exports `allSlideTemplates: SlideEntry[]` with `{ id, label, category, Component }`.

New templates go in the appropriate category file and get registered in `registry.ts`.

---

*SOP-SLIDES-002 v1.1.0 — LLM Execution Reference*
*Companion to SOP-SLIDES-001 (human process)*
*Source: AIOX Slide Design Manual v2.1 + codebase extraction*
*Template: sop-human-tmpl.md | SOP Factory | Synkra AIOX*
