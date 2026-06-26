# ETL Compile

## Contrato SINKRA

Domain: `Operational`
executor: etl-transformer
atomic_layer: Molecule
Input: source_dir, file_pattern, structure map
Output: compiled markdown bundle, metrics envelope
Pre-condition: fontes extraídas disponíveis e output route resolvida
Post-condition: bundle consolidado escrito com TOC, ordem e métricas rastreáveis
Performance: garantir chars_out >= chars_in e bloquear diretório vazio


## Metadata

| Field | Value |
|---|---|
| **task_name** | Compile Multiple Sources Into Single Document |
| **status** | Active |
| **responsible_executor** | `@etl-chief` or `@etl-transformer` |
| **execution_type** | `Deterministic` |
| **input** | Directory path or file list + optional structure map |
| **output** | Single consolidated markdown with TOC |
| **action_items** | 4-phase compilation flow |
| **acceptance_criteria** | 6 measurable criteria |

## Purpose

Consolidate multiple extracted files (transcripts, markdown, text) into a single navigable document with table of contents. Useful for creating unified training materials, documentation bundles, or RAG-friendly consolidated sources.

## Inputs

### Minimal Input

```json
{
  "source_dir": "/path/to/extracted/files",
  "output_file": "compiled_output.md",
  "constraints": {
    "business_slug": "acme",
    "workspace_mode": "auto"
  }
}
```

### Full Input

```json
{
  "source_dir": "/path/to/extracted/files",
  "output_file": "compiled_output.md",
  "file_pattern": "*.txt",
  "structure": {
    "title": "Collection Title",
    "author": "Optional Author",
    "sections": [
      {
        "name": "Section One",
        "files": ["file1.txt", "file2.txt"]
      },
      {
        "name": "Section Two",
        "files": ["file3.txt", "file4.txt"]
      }
    ]
  },
  "options": {
    "include_toc": true,
    "include_separators": true,
    "separator_style": "---",
    "strip_empty_lines": true
  }
}
```

## Execution Flow

### Phase 0: Workspace preflight

- Run `bash squads/etl-ops/scripts/validate-etl-essentials.sh`
- Load `tasks/load-workspace-context.md`
- Resolve output root:
  - canonical: `workspace/businesses/{business_slug}/etl/compiled/`
  - custom: `docs/etl/{business_slug}/`
  - legacy: caller-provided path outside workspace

### Phase 1: Discovery

- Scan `source_dir` for files matching `file_pattern` (default: `*.txt`, `*.md`)
- If `structure.sections` provided, validate all referenced files exist
- If no structure, sort files alphanumerically
- VETO if source_dir does not exist or contains no matching files

### Phase 2: Structure Resolution

- If structure provided: use explicit section/file mapping
- If no structure: infer from filenames (detect prefixes like `01_`, `Part1_`, etc.)
- Build internal compilation map: `[{ section, title, filepath }]`

### Phase 3: Compilation

For each file in order:

1. Read file content
2. Clean content (trim whitespace, normalize line endings)
3. Extract or generate title (from filename or first heading)
4. Append to output buffer with:
   - Section header (if new section)
   - Item header (## level)
   - Separator (if enabled)
   - Content

### Phase 4: Finalization

1. Generate TOC from collected headers
2. Prepend header block (title, author if provided, TOC)
3. Write to `output_file`
4. Calculate and report metrics

When `workspace_mode=auto|canonical` and `business_slug` exists:
- prefer `output_file = workspace/businesses/{business_slug}/etl/compiled/{name}.md`

## Output Format

```markdown
# {title}

## By {author}

---

## Table of Contents

### {Section One}
- {Item Title 1}
- {Item Title 2}

### {Section Two}
- {Item Title 3}

---

# {Section One}

## {Item Title 1}

{content}

---

## {Item Title 2}

{content}

---
```

## Checkpoint Rules

| Phase | Checkpoint | Veto Condition |
|-------|------------|----------------|
| Discovery | Files found | No matching files in source_dir |
| Structure | Map built | Referenced file missing |
| Compilation | Content read | File read error |
| Finalization | Output written | Write permission denied |

## Metrics

Report in envelope:

```yaml
metrics:
  files_processed: 12
  sections: 4
  total_chars: 125000
  total_words: 21000
  output_size_kb: 122
```

## Acceptance Criteria

1. All files in structure (or discovered) are included in output
2. TOC contains all section and item headers
3. Output is valid markdown
4. No content loss (chars_out >= chars_in)
5. Files appear in specified or alphanumeric order
6. Compilation completes without read/write errors


Completion Criteria: output validado, persistido no destino correto e pronto para handoff
