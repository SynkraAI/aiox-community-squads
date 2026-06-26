# Task: font-loading-strategy

```yaml
id: font-loading-strategy
version: "1.0.0"
title: "Font Loading Strategy"
description: >
  Designs and implements an optimal font loading strategy that eliminates
  FOIT (Flash of Invisible Text) and minimizes FOUT (Flash of Unstyled Text).
  Covers font subsetting, preloading, font-display selection, variable fonts,
  fallback font matching, and CLS prevention from font swap. Produces a
  font loading architecture that balances performance with visual quality.
elicit: false
owner: perf-eng
executor: perf-eng
outputs:
  - Font inventory with file sizes
  - Font subsetting plan
  - Preload strategy
  - font-display selection per font
  - Fallback font matching (size-adjust)
  - Font loading specification document
```

---

## When This Task Runs

This task runs when:
- Custom fonts cause visible FOIT or FOUT
- Font files are large (>50KB per weight)
- CLS is caused by font swap layout shift
- Multiple font families/weights are loaded unnecessarily
- LCP is blocked by font loading
- `*font-loading` or `*font-strategy` is invoked

This task does NOT run when:
- Only system fonts are used (no custom fonts to optimize)
- The issue is text styling, not loading (delegate to `@css-eng`)
- Font design/selection decisions (delegate to `@design-sys-eng`)

---

## Execution Steps

### Step 1: Inventory Current Fonts

Audit all fonts loaded by the application.

**Inventory per font:**
| Font | Weights | Format | Size | Used On | Critical |
|------|---------|--------|------|---------|----------|
| Inter | 400, 500, 600, 700 | woff2 | 98KB total | Body text | Yes |
| JetBrains Mono | 400 | woff2 | 35KB | Code blocks | No |
| Playfair Display | 700 | woff2 | 42KB | Hero headings | Yes (above fold) |

**Detection methods:**
- Check `<link>` tags in HTML head
- Check `@font-face` declarations in CSS
- Check Google Fonts imports
- Check `next/font` usage (Next.js)
- Chrome DevTools → Network → Font filter

**Identify waste:**
- Fonts loaded but never used (orphan fonts)
- Weights loaded but never referenced in CSS
- Full Unicode range loaded when only Latin needed
- Multiple formats when only woff2 needed (modern browsers)

**Output:** Complete font inventory with waste identification.

### Step 2: Subset Fonts

Reduce font file sizes by including only needed characters.

**Subsetting strategy:**
| Subset | Characters | Use When |
|--------|-----------|----------|
| Latin | A-Z, a-z, 0-9, punctuation | English-only content |
| Latin Extended | Latin + accented chars (ã, ç, ñ) | Portuguese, Spanish, French |
| Latin + Symbols | Latin + arrows, math, currency | UI with icons |
| Custom | Specific Unicode ranges | Known character set |

**Subsetting tools:**
```bash
# Using fonttools (Python)
pyftsubset Inter-Regular.woff2 \
  --output-file=Inter-Regular-latin.woff2 \
  --flavor=woff2 \
  --unicodes="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"

# Using glyphhanger
glyphhanger --whitelist="U+0-FF" --subset=Inter-Regular.woff2
```

**Next.js auto-subsetting:**
```typescript
// next/font handles subsetting automatically
import { Inter } from 'next/font/google';
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
});
```

**Expected savings:**
| Font | Before | After (Latin subset) | Savings |
|------|--------|---------------------|---------|
| Inter Regular | 98KB | 18KB | 82% |
| Inter Bold | 100KB | 19KB | 81% |

**Output:** Subsetting plan with target Unicode ranges per font.

### Step 3: Configure Preloading

Preload critical fonts to prevent render blocking.

**Preload rules:**
- Only preload fonts used above the fold (hero, header, body)
- Maximum 2-3 preloaded fonts (more = diminishing returns)
- Use `as="font"` and `type="font/woff2"` and `crossorigin`

```html
<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/Inter-Regular-latin.woff2"
  as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/Inter-Bold-latin.woff2"
  as="font" type="font/woff2" crossorigin>
```

**Next.js approach (automatic):**
```typescript
import { Inter, JetBrains_Mono } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], display: 'swap' });
const jetbrains = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
});
```

**Self-hosted vs CDN:**
| Approach | Pros | Cons |
|----------|------|------|
| Self-hosted | No external dependency, full control | Must manage files |
| Google Fonts CDN | Easy setup, shared cache | Extra DNS lookup, privacy |
| next/font | Auto-optimized, self-hosted, zero CLS | Next.js only |

**Output:** Preload strategy with font priority ranking.

### Step 4: Configure font-display

Choose the correct `font-display` value per font.

**font-display values:**
| Value | Behavior | Use When |
|-------|----------|----------|
| `swap` | Show fallback immediately, swap when loaded | Body text (most common) |
| `optional` | Show fallback, may never swap if slow | Non-critical decorative text |
| `fallback` | Brief invisible (100ms), then fallback, brief swap window | Balance visual quality + perf |
| `block` | Invisible up to 3s, then fallback | Icon fonts (never show fallback glyphs) |
| `auto` | Browser decides | Avoid (unpredictable) |

**Recommended per font type:**
| Font Type | font-display | Rationale |
|-----------|-------------|-----------|
| Body text (Inter) | `swap` | Content must be readable immediately |
| Heading (Playfair) | `optional` | Acceptable to show system font if slow |
| Code (JetBrains Mono) | `swap` | Code readability is important |
| Icon font | `block` | Fallback glyphs are wrong icons |

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Regular-latin.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

**Output:** font-display selection for each font.

### Step 5: Match Fallback Fonts (CLS Prevention)

Use CSS `size-adjust` to match fallback font metrics to custom font.

**The problem:** When custom font loads and swaps with system font, text reflowed because metrics differ → CLS.

**The fix:**
```css
/* Create adjusted fallback that matches Inter metrics */
@font-face {
  font-family: 'Inter Fallback';
  src: local('Arial');
  ascent-override: 90.49%;
  descent-override: 22.56%;
  line-gap-override: 0%;
  size-adjust: 107.64%;
}

body {
  font-family: 'Inter', 'Inter Fallback', system-ui, sans-serif;
}
```

**Next.js automatic matching:**
```typescript
// next/font automatically generates adjusted fallback
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  adjustFontFallback: true, // Automatic fallback matching
});
```

**Tools for calculating overrides:**
- [Fontaine](https://github.com/unjs/fontaine) — auto-generates overrides
- [Font Style Matcher](https://meowni.ca/font-style-matcher/) — visual comparison
- `next/font` — built-in automatic calculation

**Output:** Fallback font configurations with size-adjust values.

### Step 6: Document Font Loading Strategy

Compile the complete specification.

**Documentation includes:**
- Font inventory (from Step 1)
- Subsetting plan (from Step 2)
- Preload configuration (from Step 3)
- font-display settings (from Step 4)
- Fallback matching (from Step 5)
- Performance metrics: before/after (LCP, CLS)
- Variable font usage guide (if applicable)

**Output:** Complete font loading specification document.

---

## Quality Criteria

- Total font payload must be under 100KB (all weights combined)
- No FOIT longer than 100ms on 3G connection
- CLS from font swap must be 0 (fallback font matched)
- Only above-fold fonts are preloaded
- No unused font weights loaded

---

*Squad Apex — Font Loading Strategy Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-font-loading-strategy
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "Total font payload under 100KB"
    - "No FOIT longer than 100ms on 3G"
    - "CLS from font swap is 0"
    - "Only above-fold fonts preloaded"
    - "No unused weights loaded"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@css-eng` or `@apex-lead` |
| Artifact | Font loading strategy with subsetting, preload, font-display, and fallback matching |
| Next action | Implement font CSS via `@css-eng` or validate CWV metrics via `performance-audit` |
