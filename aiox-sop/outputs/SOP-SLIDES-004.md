# SOP-SLIDES-004 — Multi-Output Slide Pipeline

| Field | Value |
|---|---|
| **SOP ID** | SOP-SLIDES-004 |
| **Version** | 1.0.0 |
| **Effective Date** | 2026-03-16 |
| **Classification** | Public |
| **Status** | DRAFT |
| **Consumer** | LLM agents, slide-chief orchestrator |
| **Companions** | SOP-SLIDES-001 (process), SOP-SLIDES-002 (AIOX TSX), SOP-SLIDES-003 (agnostic TSX) |
| **Research Base** | `docs/research/2026-03-16-slide-generator-squad/` (6 reports, 36 sources) |
| **Review Date** | 2026-09-16 |

---

## 1. PURPOSE

This SOP defines the **multi-output slide pipeline**: from briefing to delivery across multiple rendering targets. It introduces a **canonical JSON interchange schema** that decouples content generation from rendering, enabling a single content pass to produce TSX Web, PPTX, and Markdown (Slidev/Marp) outputs.

It also formalizes the **evaluation framework** combining PPTEval (3 dimensions) and GAD Score from the research literature.

**This SOP does NOT duplicate** slide type patterns, brand config, or component APIs. Those live in SOP-002 (AIOX) and SOP-003 (agnostic). This SOP references them.

---

## 2. JSON INTERCHANGE SCHEMA

The canonical JSON schema is the **single source of truth** between content generation (Step 3) and rendering (Step 4). Every renderer consumes this same JSON.

### 2.1 Presentation Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["presentation"],
  "properties": {
    "presentation": {
      "type": "object",
      "required": ["title", "mode", "format", "aspect_ratio", "slides"],
      "properties": {
        "title": { "type": "string", "maxLength": 120 },
        "subtitle": { "type": "string", "maxLength": 200 },
        "author": { "type": "string" },
        "date": { "type": "string", "format": "date" },
        "mode": { "enum": ["palco", "live", "async"] },
        "format": { "enum": ["ted_keynote", "pitch_deck", "sales_deck", "technical", "zoom_virtual", "carousel_stories"] },
        "aspect_ratio": { "enum": ["16:9", "16:10", "9:16", "1:1"] },
        "brand": { "$ref": "#/$defs/brand_config" },
        "slides": {
          "type": "array",
          "minItems": 1,
          "items": { "$ref": "#/$defs/slide" }
        }
      }
    }
  }
}
```

### 2.2 Slide Schema

```json
{
  "$defs": {
    "slide": {
      "type": "object",
      "required": ["id", "type", "content"],
      "properties": {
        "id": { "type": "string", "pattern": "^slide-\\d{3}$" },
        "type": {
          "enum": [
            "TITLE", "SECTION_BREAK", "STATEMENT", "QUOTE",
            "CONTENT", "COMPARISON", "METRIC", "DATA_VIZ",
            "IMAGE", "BUILD", "CODE", "CLOSING"
          ]
        },
        "title": { "type": "string", "maxLength": 80 },
        "content": { "type": "object", "description": "Type-specific fields (see 2.3)" },
        "layout": {
          "enum": [
            "full_center", "left_aligned", "split_50_50",
            "split_60_40", "grid_1x2", "grid_1x3"
          ]
        },
        "decoratives": {
          "type": "array",
          "items": { "enum": ["CornerMarks", "MetaBar", "WatermarkNumber", "Watermark", "PageFooter", "SectionTag", "TechFrame"] }
        },
        "animation": {
          "type": "object",
          "properties": {
            "preset": { "enum": ["fadeUp", "fadeIn", "scaleIn", "slideRight", "slideLeft", "growWidth", "growHeight"] },
            "stagger": { "type": "object", "properties": { "base": { "type": "number", "default": 0.1 }, "increment": { "type": "number", "default": 0.08 } }, "description": "For lists/grids: delay = base + index * increment" },
            "delay": { "type": "number", "minimum": 0, "maximum": 1.5 }
          }
        },
        "speaker_notes": { "type": "string", "maxLength": 500 },
        "duration_s": { "type": "integer", "minimum": 3, "maximum": 120 }
      }
    }
  }
}
```

### 2.3 Type-Specific Content Fields

Each slide `type` has a specific `content` shape:

#### TITLE

```json
{
  "title": "string (max 5 words)",
  "subtitle": "string",
  "speaker": "string",
  "date": "string",
  "section_tag": "string"
}
```

#### SECTION_BREAK

```json
{
  "section_number": "string (e.g. '02')",
  "section_label": "string (e.g. 'Parte 02')",
  "title": "string (max 3 words)"
}
```

#### STATEMENT

```json
{
  "lines": ["string (each line, max 10 words total)"],
  "highlight_indices": [0]
}
```

`highlight_indices` marks which lines use accent color. Max 2.

#### QUOTE

```json
{
  "quote_text": "string",
  "highlight_portion": "string (optional — portion to accent)",
  "attribution_name": "string",
  "attribution_company": "string (optional)"
}
```

#### CONTENT

```json
{
  "section_tag": "string",
  "title": "string",
  "subtitle": "string (optional)",
  "items": [
    {
      "marker": "string (I, II, 01, etc.)",
      "title": "string (keyword, not sentence)",
      "description": "string (short fragment)"
    }
  ]
}
```

Max 4 items in Palco/Live. Max 6 in Async.

#### COMPARISON

```json
{
  "section_tag": "string",
  "title": "string",
  "left": {
    "label": "string (e.g. BEFORE)",
    "style": "negative",
    "items": ["string"]
  },
  "right": {
    "label": "string (e.g. AFTER)",
    "style": "positive",
    "items": ["string"]
  }
}
```

#### METRIC

```json
{
  "section_tag": "string (optional — label for SectionTag decorative)",
  "metrics": [
    {
      "value": "string (e.g. '10x', '98%', '$2.4M')",
      "label": "string (context above value)",
      "unit": "string (context below value)"
    }
  ]
}
```

Max 3 metrics per slide.

#### DATA_VIZ

```json
{
  "section_tag": "string",
  "conclusion_title": "string (title IS the conclusion, not the description)",
  "chart_type": "bar_vertical|bar_horizontal|line|donut|table",
  "data": [
    { "label": "string", "value": "number", "series": "string (optional)" }
  ],
  "source": "string (data attribution)"
}
```

**Constraints (validation, NOT included in JSON output):**
- Max elements per chart_type: bar_vertical=6, bar_horizontal=8, line=12, donut=4, table=4x6
- Forbidden chart types: scatter, heatmap, treemap, sankey
- Max 3 series per chart

#### IMAGE

```json
{
  "section_tag": "string (optional)",
  "title": "string (max 8 words, optional)",
  "image_url": "string (URL or asset path)",
  "image_alt": "string (required, accessibility)",
  "overlay": "gradient_bottom|gradient_left|none",
  "caption": "string (max 8 words, optional)"
}
```

Min 1920px wide. WebP preferred, max 500KB. No stock photos.

#### BUILD

```json
{
  "section_tag": "string",
  "title": "string",
  "orientation": "horizontal|vertical",
  "steps": [
    {
      "number": "string (01, 02, ...)",
      "title": "string",
      "description": "string",
      "time_label": "string (optional, e.g. 'Week 1-2')"
    }
  ]
}
```

2-5 steps. In progressive mode, future steps render at 15% opacity.

#### CODE

```json
{
  "section_tag": "string (optional)",
  "title": "string",
  "language": "string (e.g. 'typescript')",
  "code": "string (max 12 visible lines)",
  "highlight_lines": [1, 3]
}
```

Min font = body size. Never screenshot code.

#### CLOSING

```json
{
  "title": "string (max 5 words, e.g. 'THANK YOU.')",
  "cta_text": "string (e.g. 'QUESTIONS?')",
  "contact_lines": ["string (email, url, etc.)"]
}
```

### 2.4 Brand Config Reference

```json
{
  "$defs": {
    "brand_config": {
      "oneOf": [
        { "type": "string", "description": "Reference to external brand config file path" },
        {
          "type": "object",
          "description": "Inline brand config (SOP-003 schema)",
          "required": ["name", "color", "font"],
          "properties": {
            "name": { "type": "string" },
            "prefix": { "type": "string" },
            "url": { "type": "string" },
            "color": {
              "type": "object",
              "required": ["bg_primary", "bg_accent", "text_primary", "text_secondary", "accent"],
              "properties": {
                "bg_primary": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
                "bg_accent": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
                "surface": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
                "text_primary": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
                "text_secondary": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
                "accent": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
                "border": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
                "warning": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" }
              }
            },
            "font": {
              "type": "object",
              "required": ["sans", "mono"],
              "properties": {
                "sans": { "type": "string" },
                "sans_fallback": { "type": "string" },
                "mono": { "type": "string" },
                "mono_fallback": { "type": "string" }
              }
            }
          }
        }
      ]
    }
  }
}
```

### 2.5 Complete Example — 5-Slide Pitch Deck

```json
{
  "presentation": {
    "title": "Acme AI Platform",
    "subtitle": "Series A Pitch",
    "author": "Jane Smith",
    "date": "2026-03-16",
    "mode": "palco",
    "format": "pitch_deck",
    "aspect_ratio": "16:9",
    "brand": {
      "name": "Acme",
      "prefix": "ac",
      "url": "acme.ai",
      "color": {
        "bg_primary": "#050505",
        "bg_accent": "#3B82F6",
        "surface": "#111111",
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "accent": "#3B82F6",
        "border": "#1E293B",
        "warning": "#EF4444"
      },
      "font": {
        "sans": "Inter",
        "sans_fallback": "system-ui, sans-serif",
        "mono": "JetBrains Mono",
        "mono_fallback": "monospace"
      }
    },
    "slides": [
      {
        "id": "slide-001",
        "type": "TITLE",
        "title": "Acme AI Platform",
        "content": {
          "title": "ACME AI",
          "subtitle": "Series A Pitch",
          "speaker": "Jane Smith, CEO",
          "date": "March 2026",
          "section_tag": "[01] - Introduction"
        },
        "layout": "full_center",
        "decoratives": ["CornerMarks", "MetaBar", "WatermarkNumber"],
        "animation": { "preset": "fadeUp", "delay": 0.3 },
        "speaker_notes": "Welcome everyone. Today I'll present our vision for AI-powered automation.",
        "duration_s": 15
      },
      {
        "id": "slide-002",
        "type": "STATEMENT",
        "title": "The Problem",
        "content": {
          "lines": ["80% OF ENTERPRISE", "WORKFLOWS ARE", "STILL MANUAL"],
          "highlight_indices": [2]
        },
        "layout": "full_center",
        "decoratives": [],
        "animation": { "preset": "scaleIn", "delay": 0.2 },
        "speaker_notes": "The core problem we solve: most business processes haven't been touched by AI yet.",
        "duration_s": 8
      },
      {
        "id": "slide-003",
        "type": "METRIC",
        "title": "Traction",
        "content": {
          "metrics": [
            { "value": "$2.4M", "label": "ARR", "unit": "Annual Recurring Revenue" },
            { "value": "340%", "label": "YoY Growth", "unit": "Year over year" },
            { "value": "98%", "label": "Retention", "unit": "Net Revenue Retention" }
          ]
        },
        "layout": "grid_1x3",
        "decoratives": ["SectionTag"],
        "animation": { "preset": "scaleIn", "delay": 0.3 },
        "speaker_notes": "Our numbers speak for themselves. Triple-digit growth with near-perfect retention.",
        "duration_s": 15
      },
      {
        "id": "slide-004",
        "type": "COMPARISON",
        "title": "Before & After",
        "content": {
          "section_tag": "[04] - Impact",
          "title": "BEFORE & AFTER",
          "left": {
            "label": "WITHOUT ACME",
            "style": "negative",
            "items": ["3 weeks per workflow", "5 engineers required", "40% error rate"]
          },
          "right": {
            "label": "WITH ACME",
            "style": "positive",
            "items": ["2 hours per workflow", "1 operator required", "0.5% error rate"]
          }
        },
        "layout": "split_50_50",
        "decoratives": ["SectionTag"],
        "animation": { "preset": "slideRight", "delay": 0.3 },
        "speaker_notes": "The transformation is dramatic. We reduce both time and error rates by orders of magnitude.",
        "duration_s": 25
      },
      {
        "id": "slide-005",
        "type": "CLOSING",
        "title": "Thank You",
        "content": {
          "title": "THANK YOU.",
          "cta_text": "QUESTIONS?",
          "contact_lines": ["jane@acme.ai", "acme.ai"]
        },
        "layout": "full_center",
        "decoratives": ["CornerMarks"],
        "animation": { "preset": "fadeUp", "delay": 0.2 },
        "speaker_notes": "Thank you for your time. I'm happy to answer any questions.",
        "duration_s": 10
      }
    ]
  }
}
```

---

## 3. PIPELINE STEPS

### Step 1: FORMAT SELECTION

Select the presentation format. Format determines mode, constraints, and dominant slide types.

```
INPUT:  briefing (topic, audience, context, duration)
OUTPUT: format, mode (override), slide count range, dominant types

IF audience = investors AND purpose = fundraise:
  format = "pitch_deck"
ELSE IF audience = customers AND purpose = sell:
  format = "sales_deck"
ELSE IF context = conference AND duration >= 15min:
  format = "ted_keynote"
ELSE IF topic = technical AND audience = developers:
  format = "technical"
ELSE IF context in [zoom, meet, teams]:
  format = "zoom_virtual"
ELSE IF channel in [instagram, linkedin, stories]:
  format = "carousel_stories"
ELSE:
  format = "pitch_deck" (safest default)
```

Format constraints (from SOP-002/003 section 4.0):

| Format | Slides | Text Density | Bullets | Self-Explanatory |
|---|---|---|---|---|
| ted_keynote | 40-90 | Minimal | Never | Never |
| pitch_deck | 10-15 | Moderate | Rare | Yes (leave-behind) |
| sales_deck | 8-25 | Moderate | Allowed | Yes (champion) |
| technical | 20-40 | Moderate+ | Allowed | Partial |
| zoom_virtual | Variable | Reduced | Cautious | Depends |
| carousel_stories | 5-10 | Minimal | Never | Always |

### Step 2: MODE + ASPECT RATIO

Mode is often determined by format (Step 1). If not locked, select by context:

```
IF context in [conference, keynote, workshop, presencial]:
  mode = "palco"
ELSE IF context in [youtube, twitch, screenshare, live_call]:
  mode = "live"
ELSE IF context in [post_event, course, onboarding, pdf]:
  mode = "async"

IF channel in [projector, monitor, stream]:    ratio = "16:9"
ELSE IF channel in [macbook, mac_projector]:   ratio = "16:10"
ELSE IF channel in [stories, reels, vertical]: ratio = "9:16"
ELSE IF channel in [instagram, carousel]:      ratio = "1:1"
ELSE:                                          ratio = "16:9"
```

Mode constraints:

| Mode | Max Words | Min Font | Whitespace | Animations | Speaker Notes |
|---|---|---|---|---|---|
| palco | 15 | 2.2vw | >= 50% | Yes | Required |
| live | 15 | 2.2vw | >= 45% | Yes (-30% delay) | Required |
| async | 30 | 1.6vw | >= 40% | None | Not needed |

### Step 3: CONTENT GENERATION -> JSON

The LLM generates the canonical JSON from the briefing + format + mode + brand config.

**Prompt template for LLM content generation:**

```
You are a presentation content architect. Generate a slide deck in the canonical JSON interchange format.

INPUTS:
- Topic: {{topic}}
- Audience: {{audience}}
- Format: {{format}} (see constraints below)
- Mode: {{mode}}
- Aspect Ratio: {{ratio}}
- Duration: {{duration_minutes}} minutes
- Brand Config: {{brand_config}}
- Key Messages: {{key_messages}}
- Source Material: {{source_material}}

FORMAT CONSTRAINTS:
{{format_constraints from Step 1 table}}

MODE CONSTRAINTS:
{{mode_constraints from Step 2 table}}

SLIDE TYPE TAXONOMY:
TITLE, SECTION_BREAK, STATEMENT, QUOTE, CONTENT, COMPARISON, METRIC, DATA_VIZ, IMAGE, BUILD, CODE, CLOSING

SEQUENCE RULES:
- FIRST slide = TITLE (always)
- LAST slide = CLOSING (always)
- SECTION_BREAK between thematic blocks
- Max 3 consecutive same type
- Max 120s per slide
- Insert rhythm resets (SECTION_BREAK, IMAGE, STATEMENT) in long sequences

RHYTHM PATTERNS:
- STATEMENT -> CONTENT -> CONTENT = Impact -> detail -> detail
- METRIC -> DATA_VIZ -> CONTENT = Number -> context -> explanation
- IMAGE -> STATEMENT = Visual -> emotional
- BUILD (3 steps) = Narrative progression
- COMPARISON -> STATEMENT = Contrast -> conclusion

OUTPUT: Valid JSON following the presentation schema (section 2.1).
Every slide must have: id, type, title, content (type-specific), layout, speaker_notes, duration_s.
```

**Validation after generation:**

```
ASSERT slides[0].type == "TITLE"
ASSERT slides[-1].type == "CLOSING"
ASSERT all slide.type in TAXONOMY
ASSERT sum(duration_s) approximately matches duration_minutes * 60
ASSERT no more than 3 consecutive same type
ASSERT word count per slide <= mode.max_words (for text-heavy types)
ASSERT JSON validates against schema (section 2.1 + 2.2)
```

### Step 4: RENDERING FORK

The canonical JSON is consumed by one or more renderers in parallel.

```
┌─────────────────────────────────────────────────┐
│  INPUT: Canonical JSON (from Step 3)            │
│                                                 │
│  IF target includes "tsx_web":                  │
│    → TSX Renderer (4.1)                         │
│                                                 │
│  IF target includes "pptx":                     │
│    → PPTX Renderer (4.2)                        │
│                                                 │
│  IF target includes "markdown":                 │
│    → Markdown Renderer (4.3)                    │
│                                                 │
│  Renderers run independently. Same JSON in,     │
│  different format out.                          │
└─────────────────────────────────────────────────┘
```

### Step 5: EVALUATION

Apply the evaluation framework (section 5) to each rendered output.

```
IF composite_score >= 7.0:
  verdict = "PASS"
ELSE IF composite_score >= 5.0:
  verdict = "REVISE" — return to Step 3 with feedback
ELSE:
  verdict = "FAIL" — return to Step 1 to reassess format/approach

Max revision iterations = 3
After 3 revisions with score < 7.0: HALT, escalate to human review
```

### Step 6: DELIVERY

```
OUTPUT = rendered file(s) in requested format(s)

IF format requires leave-behind (pitch_deck, sales_deck):
  Generate TWO versions:
    1. "palco" version (sparse, narrator-dependent)
    2. "async" version (self-explanatory, more text)
  Both from same canonical JSON with mode override

DELIVERY ARTIFACTS:
  - Rendered file(s) (.tsx / .pptx / .md)
  - Canonical JSON (for future re-rendering)
  - Speaker notes export (if mode != async)
  - Evaluation scorecard
```

---

## 4. RENDERER SPECIFICATIONS

### 4.1 TSX Web Renderer

**Delegates to SOP-002 (AIOX brand) or SOP-003 (any brand).**

JSON-to-TSX mapping:

| JSON Field | TSX Output |
|---|---|
| `presentation.brand` | Brand config resolution (SOP-003 section 0) |
| `slide.type` | Component selection (SOP-002/003 section 4/6) |
| `slide.layout` | Layout class/structure selection |
| `slide.decoratives[]` | `<CornerMarks>`, `<MetaBar>`, `<WatermarkNumber>`, etc. |
| `slide.animation` | `{...fadeUp(delay)}`, `{...scaleIn(delay)}`, etc. |
| `slide.content.*` | Props passed to type-specific component |
| `slide.speaker_notes` | Exported as separate data structure (not rendered) |
| `presentation.mode` | Controls animation behavior, word limits, safe zones |

**Rules:**
- IF `presentation.brand.name == "AIOX"` → use SOP-002 patterns (hardcoded AIOX tokens)
- ELSE → use SOP-003 patterns (CSS variable-based tokens from brand config)
- ALWAYS generate `SlideLayout` wrapper per slide
- ALWAYS apply `style={FONT_SANS}` or `style={FONT_MONO}` to every text element
- IF `mode == "async"` → strip all animation props
- IF `mode == "live"` → reduce animation delays by 30%

### 4.2 PPTX Renderer

**Uses Office-PowerPoint-MCP-Server (32 tools, python-pptx based).**

JSON-to-MCP mapping:

| JSON Field | MCP Tool(s) |
|---|---|
| `presentation` (root) | `create_presentation` → set dimensions from `aspect_ratio` |
| `presentation.brand.font` | `set_font` on slide master |
| `presentation.brand.color` | Theme colors via `set_theme_colors` |
| `slide` (each) | `add_slide` with layout selection |
| `slide.content.title` | `add_text_box` or `set_title` with font/size |
| `slide.content.items[]` | `add_text_box` per item, or `add_table` for structured data |
| `slide.content.metrics[]` | `add_text_box` with large font for value |
| `slide.content.chart_type` | `add_chart` (bar, line, pie, etc.) |
| `slide.content.image_url` | `add_image` with positioning |
| `slide.content.code` | `add_text_box` with mono font, syntax-highlighted |
| `slide.speaker_notes` | `set_notes` per slide |
| `slide.decoratives` | Manual positioning: corner marks as lines, watermark as low-opacity text |

**PPTX-specific constraints:**
- No CSS animations (PPTX has its own animation system — map `animation.preset` to PowerPoint entrance effects)
- Font embedding required for non-system fonts
- Image resolution: export at 96 DPI minimum for screen, 300 DPI for print
- Aspect ratio: set via `presentation.slide_width` and `presentation.slide_height` in EMU

**Animation mapping (PPTX entrance effects):**

| JSON Preset | PPTX Effect |
|---|---|
| fadeUp | Fly In (from bottom) + Fade |
| fadeIn | Fade |
| scaleIn | Grow & Turn or Zoom |
| slideRight | Fly In (from left) |
| slideLeft | Fly In (from right) |
| growWidth | Wipe (left to right) |
| growHeight | Wipe (bottom to top) |
| stagger | Apply entrance effect delays sequentially (base + index × 0.08s) |

**Aspect Ratio → PPTX Dimensions (EMU):**

| Ratio | Width (EMU) | Height (EMU) | Pixels |
|---|---|---|---|
| 16:9 | 12192000 | 6858000 | 1920×1080 |
| 16:10 | 12192000 | 7620000 | 1920×1200 |
| 9:16 | 6858000 | 12192000 | 1080×1920 |
| 1:1 | 6858000 | 6858000 | 1080×1080 |

### 4.3 Markdown Renderer

**Targets Slidev (Vue-based) or Marp (pure Markdown).**

JSON-to-Markdown mapping:

```markdown
---
# Slidev frontmatter (from presentation metadata)
theme: {{theme_from_brand}}
title: {{presentation.title}}
author: {{presentation.author}}
date: {{presentation.date}}
aspectRatio: {{presentation.aspect_ratio}}
---

# Slide content follows, separated by ---
```

| JSON Field | Slidev Markdown | Marp Markdown |
|---|---|---|
| Slide separator | `---` | `---` |
| `slide.type: TITLE` | `# Title` + YAML `layout: cover` | `# Title` + `<!-- _class: lead -->` |
| `slide.type: SECTION_BREAK` | `layout: section` + `# Section` | `<!-- _class: invert -->` + `# Section` |
| `slide.type: STATEMENT` | `layout: statement` + `# Bold text` (centered, large) | `<!-- _class: lead -->` + `# Bold text` |
| `slide.type: CONTENT` | `## Title` + `- item` list | `## Title` + `- item` list |
| `slide.type: QUOTE` | `> quote` + `— attribution` | `> quote` + `— attribution` |
| `slide.type: COMPARISON` | Two-column `::left::` / `::right::` | HTML table or `<div>` grid |
| `slide.type: METRIC` | Custom Vue component or `<div>` | `# Value` (styled via CSS) |
| `slide.type: DATA_VIZ` | Mermaid/Chart.js integration | Mermaid block or image |
| `slide.type: IMAGE` | `![alt](url)` | `![alt](url)` + `<!-- _backgroundImage -->` |
| `slide.type: BUILD` | `v-clicks` directive (Slidev) | Numbered list |
| `slide.type: CODE` | ` ```lang ` fenced code block | ` ```lang ` fenced code block |
| `slide.type: CLOSING` | `layout: end` + `# Thank You` + contact info | `<!-- _class: lead -->` + `# Thank You` + contact |
| `slide.speaker_notes` | `<!-- speaker notes -->` block | `<!-- notes -->` block |

**Slidev-specific features:**
- Use `v-click` for progressive reveal (maps to BUILD steps)
- Use `<style>` blocks for brand colors
- Use Windi CSS / UnoCSS for utility classes

**Marp-specific features:**
- Use `<!-- _class: -->` directives for layout
- Use `<!-- _backgroundColor: -->` for brand colors
- Export: `marp --pdf` for PDF, `marp --pptx` for PPTX

---

## 5. EVALUATION FRAMEWORK

Composite score from 4 dimensions, adapted from PPTEval (PPTAgent V2) and GAD Score (SlideGen).

### 5.1 Content Score (weight: 0.30)

| Criterion | Score Range | Evaluation |
|---|---|---|
| Factual accuracy | 0-10 | Claims supported by source material |
| Topic relevance | 0-10 | Every slide serves the presentation goal |
| Completeness | 0-10 | Key messages covered, no gaps |
| Word economy | 0-10 | Respects mode word limits, no filler |

`content_score = mean(factual, relevance, completeness, word_economy)`

### 5.2 Design Score (weight: 0.30)

| Criterion | Score Range | Evaluation |
|---|---|---|
| Visual consistency | 0-10 | Brand colors, fonts, spacing uniform |
| Whitespace | 0-10 | Meets mode minimum (50%/45%/40%) |
| Typography hierarchy | 0-10 | Clear title > subtitle > body > caption |
| Legibility | 0-10 | Contrast >= WCAG AA, font >= minimum |
| Decoration restraint | 0-10 | Max 2 CornerMarks/section, no clutter |

`design_score = mean(consistency, whitespace, hierarchy, legibility, restraint)`

### 5.3 Coherence Score (weight: 0.20)

| Criterion | Score Range | Evaluation |
|---|---|---|
| Narrative flow | 0-10 | Logical progression slide-to-slide |
| Sequence compliance | 0-10 | TITLE first, CLOSING last, breaks between sections |
| Rhythm variety | 0-10 | No more than 3 consecutive same type |
| Duration balance | 0-10 | No single slide > 120s, total matches target |

`coherence_score = mean(flow, sequence, rhythm, duration)`

### 5.4 GAD Score — Geometric Aesthetic Density (weight: 0.20)

Measures spatial quality of slide layouts. Adapted from SlideGen's Geometry-Aware Density metric.

**Note:** The original GAD Score in SlideGen is algorithmically computed from element bounding boxes and spatial coordinates. This adaptation converts it to LLM-judged criteria since rendered slides may not expose geometric metadata. For TSX renderer, a future enhancement could compute GAD programmatically from DOM element positions.

| Criterion | Score Range | Evaluation |
|---|---|---|
| Element distribution | 0-10 | Elements use available space, not clustered in one area |
| Alignment consistency | 0-10 | Elements follow a grid, not arbitrarily placed |
| Density balance | 0-10 | Neither too sparse (empty) nor too dense (cluttered) |
| Margin compliance | 0-10 | Content within safe margins per mode |

`gad_score = mean(distribution, alignment, density, margins)`

### 5.5 Composite Score

```
composite = (content_score * 0.30)
          + (design_score  * 0.30)
          + (coherence_score * 0.20)
          + (gad_score * 0.20)
```

| Composite | Verdict | Action |
|---|---|---|
| >= 7.0 | PASS | Proceed to delivery |
| 5.0 - 6.9 | REVISE | Return to Step 3 with dimensional feedback |
| < 5.0 | FAIL | Return to Step 1, reassess approach |

### 5.6 Rendered Output Capture

The evaluator needs access to the rendered output, not just the JSON. Capture method per renderer:

| Renderer | Capture Method |
|---|---|
| TSX Web | Screenshot each slide via Playwright/Puppeteer (1920×1080 viewport) |
| PPTX | Convert each slide to PNG via `python-pptx` thumbnail or LibreOffice export |
| Markdown | Render via `slidev export --format png` or `marp --images png` |

For LLM-based evaluation, provide screenshots alongside the JSON. For programmatic evaluation (future), parse DOM/PPTX element positions directly.

### 5.7 Evaluation Prompt Template

```
Evaluate this slide deck against 4 dimensions. Score each criterion 0-10.

PRESENTATION JSON: {{canonical_json}}
RENDERED OUTPUT: {{slide_screenshots_or_descriptions}}
SOURCE MATERIAL: {{original_briefing}}

DIMENSIONS:
1. CONTENT (factual accuracy, relevance, completeness, word economy)
2. DESIGN (consistency, whitespace, hierarchy, legibility, restraint)
3. COHERENCE (narrative flow, sequence compliance, rhythm, duration)
4. GAD (element distribution, alignment, density balance, margin compliance)

For each dimension, provide:
- Individual criterion scores (0-10)
- Dimension average
- Specific feedback for scores < 7

OUTPUT FORMAT:
{
  "content": { "factual": N, "relevance": N, "completeness": N, "word_economy": N, "average": N, "feedback": "..." },
  "design": { "consistency": N, "whitespace": N, "hierarchy": N, "legibility": N, "restraint": N, "average": N, "feedback": "..." },
  "coherence": { "flow": N, "sequence": N, "rhythm": N, "duration": N, "average": N, "feedback": "..." },
  "gad": { "distribution": N, "alignment": N, "density": N, "margins": N, "average": N, "feedback": "..." },
  "composite": N,
  "verdict": "PASS|REVISE|FAIL"
}
```

---

## 6. VALIDATION CHECKLIST

### Per Renderer

#### TSX Web

- [ ] Every text element has `style={FONT_SANS}` or `style={FONT_MONO}`
- [ ] `SlideLayout` wraps every slide
- [ ] Contrast ratios pass WCAG AA (4.5:1 body, 3:1 large text)
- [ ] Animations stripped in async mode
- [ ] `prefers-reduced-motion` media query present
- [ ] No hardcoded px outside 1920x1080 canvas
- [ ] `npm run lint && npm run typecheck` = 0 errors

#### PPTX

- [ ] Slide dimensions match aspect_ratio (EMU values correct)
- [ ] Fonts embedded or system-available
- [ ] Speaker notes populated for palco/live modes
- [ ] Image resolution >= 96 DPI
- [ ] No overlapping elements
- [ ] Text not clipped by shape boundaries
- [ ] File opens correctly in PowerPoint, Keynote, and Google Slides

#### Markdown (Slidev/Marp)

- [ ] Slide separators (`---`) correct
- [ ] Frontmatter valid YAML
- [ ] Code fences use correct language identifiers
- [ ] Images referenced with valid paths/URLs
- [ ] Speaker notes in comment blocks
- [ ] Renders correctly with `slidev` or `marp` CLI
- [ ] Export to PDF produces correct page count

### Cross-Renderer

- [ ] All 12 slide types have a mapping in each target renderer
- [ ] Slide count matches between JSON and rendered output
- [ ] Speaker notes preserved across all formats
- [ ] Brand colors applied consistently in all renderers

---

## 7. ANTI-PATTERNS

### Pipeline Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|---|---|---|
| Skip JSON schema, render directly from briefing | No interchange format = no multi-output, no evaluation | Always generate canonical JSON first (Step 3) |
| Modify JSON per renderer | Schema drift, inconsistent content | One JSON, multiple renderers. Renderers adapt layout, not content |
| Evaluate before rendering | Can't assess design/GAD without rendered output | Evaluate after rendering (Step 5) |
| Use same word density for all modes | Palco slides unreadable, async slides empty | Respect mode constraints (Step 2 table) |
| Generate PPTX by screenshot of TSX | Lossy, low resolution, no editable text | Each renderer reads JSON independently |
| Hardcode brand in JSON schema | Schema becomes single-brand | Brand config is a reference or inline object, never embedded in schema definition |

### Content Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|---|---|---|
| Title describes the chart ("Revenue by Month") | Title should BE the insight | Title IS the conclusion ("Revenue Grew 40%") |
| Same type 4+ times in a row | Kills rhythm, audience zones out | Max 3 consecutive, insert rhythm resets |
| More than 15 words on palco/live slide | Illegible from distance, splits attention | Respect mode.max_words constraint |
| Paragraph of text on any slide | Slides are not documents | Keywords and fragments only |
| Missing speaker notes in palco/live | Narrator has no script | speaker_notes required for palco/live modes |
| Self-explanatory slide in palco mode | Steals attention from narrator | Slide supports narrator, not replaces |

### Rendering Anti-Patterns

| Anti-Pattern | Renderer | Why It Fails |
|---|---|---|
| CSS animations in PPTX | PPTX | PPTX uses its own animation system |
| `v-click` in Marp | Markdown | Marp has no progressive reveal; only Slidev supports `v-click` |
| Stock photos | All | Destroys credibility |
| Code as screenshot | All | Inaccessible, pixelates on resize |
| Color-only data differentiation | All | Inaccessible to colorblind users |

---

## 8. COMPANION REFERENCES

| SOP | Use For | Key Sections |
|---|---|---|
| SOP-SLIDES-001 | Human-readable process, decision criteria | Full workflow for designers/authors |
| SOP-SLIDES-002 | AIOX-specific TSX code patterns | Section 2 (API), 3 (tokens), 6 (12 types) |
| SOP-SLIDES-003 | Brand-agnostic TSX code patterns | Section 0 (brand config), 2 (shared module), 4 (12 types) |

| Research | Use For | Key Data |
|---|---|---|
| `02-research-report.md` | Ecosystem overview, tool landscape | Sections 1 (libraries), 3.3 (architecture pattern) |
| `03-recommendations.md` | Stack selection, MCP tools | Section 1.1 (MCP server), 2.3 (JSON schema) |
| `04-pptagent-v2-domain-analysis.md` | PPTEval dimensions, business rules | Section 2 (taxonomy), 5 (evaluation) |
| `05-competitive-analysis.md` | GAD Score, cross-project comparison | Section 5 (evaluation), 10 (diagnosis) |
