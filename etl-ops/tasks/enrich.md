# ETL Enrich

## Contrato SINKRA

Domain: `Operational`
executor: etl-transformer
atomic_layer: Molecule
Input: raw transcript file, metadata hints, output route
Output: enriched transcript markdown, schema validation report
Pre-condition: arquivo-fonte legível e contrato de saída disponível
Post-condition: transcrição enriquecida validada contra schema e fidelity rules
Performance: bloquear word count delta > 10% ou schema inválido


## Metadata

| Field | Value |
|---|---|
| **task_name** | Enrich Raw Transcript Into Structured Markdown |
| **status** | Active |
| **responsible_executor** | `@etl-transformer` |
| **execution_type** | `Hybrid` (deterministic + optional LLM) |
| **input** | Raw transcript file + metadata hints |
| **output** | Enriched markdown per `enriched-transcript.schema.json` |
| **action_items** | 5-phase enrichment flow |
| **acceptance_criteria** | 8 measurable criteria |

## Purpose

Transform raw transcription output (unstructured text from speech-to-text) into structured, indexed markdown with YAML frontmatter. Produces content optimized for:

- Training data ingestion
- RAG knowledge bases
- Human readability
- Semantic search indexing

## Transformation Principles

**From acquisition_training learnings (10G videos → 200KB markdown):**

1. **Destilar, não transcrever** - Remover repetições, hesitações, fillers ("um", "tipo", "sabe")
2. **Estruturar por conceito** - Reorganizar por tema, não por ordem cronológica do vídeo
3. **Tabelas > parágrafos** - Sempre que houver comparações, listas, ou dados estruturados
4. **Preservar quotes-chave** - Frases memoráveis como citações blockquote
5. **Zero opinião** - Apenas conteúdo original, sem interpretações ou adições

**Regra 90/10:** 90%+ da informação está no texto. Frames são complementares (fórmulas, diagramas, números específicos).

## Inputs

### Minimal Input

```json
{
  "source_file": "/path/to/raw_transcript.txt",
  "output_file": "/path/to/enriched_output.md",
  "constraints": {
    "business_slug": "acme",
    "workspace_mode": "auto"
  }
}
```

### Full Input

```json
{
  "source_file": "/path/to/raw_transcript.txt",
  "output_file": "/path/to/enriched_output.md",
  "metadata": {
    "source": "https://example.com/video.mp4",
    "collection": "Series Name",
    "sequence": 3,
    "speaker": "Speaker Name",
    "language": "en"
  },
  "options": {
    "extract_concepts": true,
    "generate_summary": true,
    "format_structure": true,
    "use_llm": false
  }
}
```

## Execution Flow

### Phase 0: Workspace preflight

- Run `bash squads/etl-ops/scripts/validate-etl-essentials.sh`
- Load `tasks/load-workspace-context.md`
- Resolve output root:
  - canonical: `workspace/businesses/{business_slug}/etl/enriched/`
  - custom: `docs/etl/{business_slug}/`
  - legacy: caller-provided output path

### Phase 1: Load & Validate

- Read source file
- Detect encoding (UTF-8 assumed, fallback to latin-1)
- Calculate baseline metrics (chars, words, lines)
- VETO if file empty or unreadable

### Phase 2: Metadata Extraction

**Deterministic (no LLM):**
- Title: from filename or first non-empty line
- Sequence: from filename prefix pattern (`01_`, `Part1_`, etc.)
- Language: from filename suffix or assume from input

**With LLM (if `use_llm: true`):**
- Topic: one-line summary
- Key concepts: extracted terms (max 15)

### Phase 3: Content Structuring

**Deterministic transformations:**
1. Normalize whitespace (collapse multiple blank lines)
2. Detect natural breaks (speaker changes, topic shifts via keywords)
3. Insert markdown headers at break points
4. Convert lists (detect "first", "second", numbered patterns)
5. Detect and format quotes (direct speech patterns)
6. Detect and format emphasis (repeated words, ALL CAPS)

**Structure heuristics:**
- Lines starting with "So," "Now," "Okay," "Alright" often indicate new sections
- Questions followed by explanations suggest Q&A format
- Numbered items or "number one", "number two" indicate lists

### Phase 4: Frontmatter Assembly

Build YAML frontmatter per `enriched-transcript.schema.json`:

```yaml
---
source: "{metadata.source}"
collection: "{metadata.collection}"
sequence: {metadata.sequence}
title: "{extracted_title}"
topic: "{extracted_topic}"
key_concepts: [{extracted_concepts}]
language: "{metadata.language}"
speaker: "{metadata.speaker}"
---
```

### Phase 5: Output & Validation

1. Combine frontmatter + structured body
2. Validate against `enriched-transcript.schema.json`
3. Write to output_file
4. Calculate fidelity metrics

When `workspace_mode=auto|canonical` and `business_slug` exists:
- prefer `output_file = workspace/businesses/{business_slug}/etl/enriched/{name}.md`

## Fidelity Rules

Enrichment must preserve content integrity:

| Metric | Threshold | Action on Fail |
|--------|-----------|----------------|
| Word count delta | < 5% | WARN |
| Word count delta | > 10% | VETO |
| Semantic preservation | N/A (manual) | Include diff sample in envelope |

**Allowed additions:**
- Markdown formatting characters (`#`, `-`, `*`, `>`)
- Frontmatter block
- Section headers (generated from content patterns)

**Forbidden:**
- Adding content not in source
- Removing substantive content
- Paraphrasing (unless explicitly requested)

## Checkpoint Rules

| Phase | Checkpoint | Veto Condition |
|-------|------------|----------------|
| Load | File read | Empty or unreadable |
| Metadata | Title extracted | No title derivable |
| Structure | Headers inserted | Zero structure detected (acceptable, continue) |
| Frontmatter | Valid YAML | Schema validation fail |
| Output | File written | Write error |

## Output Example

```markdown
---
source: "https://cdn.example.com/training/module_03.mp4"
collection: "Training Series"
sequence: 3
title: "Advanced Techniques"
topic: "Deep dive into optimization strategies and common pitfalls"
key_concepts: ["optimization", "caching", "performance", "bottlenecks"]
language: "en"
speaker: "Instructor"
---

# Advanced Techniques

Overview of optimization strategies covered in this module.

## Key Optimization Principles

The first thing to understand is that premature optimization is problematic...

### Caching Strategies

> "Cache everything that doesn't change frequently."

Three main approaches:

- In-memory caching
- Distributed caching
- Edge caching

## Common Pitfalls

Things to avoid when optimizing...
```

## Acceptance Criteria

1. Output contains valid YAML frontmatter
2. Frontmatter validates against `enriched-transcript.schema.json`
3. Body is valid markdown
4. Word count delta < 10% from source
5. Title is non-empty and meaningful
6. At least one markdown structure element added (header, list, or quote)
7. No content fabrication (all text traceable to source)
8. Output file written successfully


Completion Criteria: output validado, persistido no destino correto e pronto para handoff
