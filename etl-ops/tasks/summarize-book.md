# ETL Summarize Book

## Contrato SINKRA

Domain: `Operational`
executor: etl-transformer
atomic_layer: Molecule
Input: markdown extraído do livro + constraints de contexto
Output: manifesto estrutural, book-context, chapter summaries e síntese final
Pre-condition: extração concluída e source preferencial em EPUB/Markdown
Post-condition: livro resumido em estágios, com contexto acumulado e artefatos rastreáveis
Performance: bloquear execução sem estrutura mínima ou sem cobertura de capítulos

## Metadata

| Field | Value |
|---|---|
| **task_name** | Summarize Book Progressively |
| **status** | Active |
| **responsible_executor** | `@etl-transformer` |
| **execution_type** | `Hybrid` |
| **input** | Markdown do livro + `constraints.document_strategy=book_progressive` |
| **output** | `manifest`, `book_context`, `chapter_summary`, `rolling_context`, `final_summary` |
| **action_items** | 6-phase staged summarization flow |
| **acceptance_criteria** | 9 measurable criteria |

## Purpose

Aplicar a heurística de livro em estágios:

1. EPUB/Markdown antes de PDF
2. Estrutura antes de resumo
3. Contexto externo curto antes dos capítulos
4. Um capítulo por vez
5. Síntese final só a partir de artefatos intermediários

## Inputs

### Minimal Input

```json
{
  "source_file": "/path/to/book.md",
  "constraints": {
    "document_strategy": "book_progressive",
    "summary_strategy": "progressive_llm"
  }
}
```

### With Context Sources

```json
{
  "source_file": "/path/to/book.md",
  "constraints": {
    "document_strategy": "book_progressive",
    "summary_strategy": "progressive_llm",
    "context_sources": [
      { "kind": "url", "value": "https://en.wikipedia.org/wiki/Example_Book" },
      { "kind": "text", "value": "Publisher blurb..." }
    ]
  }
}
```

## Execution Flow

### Phase 0: Validate source quality

- Preferir `.epub` convertido para `.md`
- Se a origem for PDF:
  - continuar apenas se a extração tiver estrutura mínima
  - emitir warning explícito: preferir EPUB quando disponível

### Phase 1: Structure pass

- Detectar heading tree
- Construir manifesto do livro
- Detectar capítulos e seções
- VETO se `chapter_count == 0`

### Phase 2: Context pack

- Coletar `context_sources`
- Resumir o contexto externo em `book_context`
- Se não houver contexto externo, gerar contexto determinístico mínimo a partir do manifesto

### Phase 3: Chapter loop

Para cada capítulo:

1. Montar pacote com `book_context`
2. Incluir `rolling_context` dos capítulos anteriores
3. Resumir apenas o capítulo atual
4. Persistir `chapter_summary_{n}.md`

### Phase 4: Rolling continuity

- Atualizar `rolling_context.md` com janela curta dos resumos anteriores
- Garantir que o próximo capítulo receba continuidade sem carregar o livro inteiro

### Phase 5: Final synthesis

- Gerar síntese final usando somente:
  - `book_context`
  - `chapter_summaries`
  - `rolling_context`
- VETO se a síntese final depender do livro bruto

## Acceptance Criteria

1. O modo exige `document_strategy=book_progressive`.
2. Manifesto estrutural do livro é gerado.
3. `book_context` existe antes do primeiro capítulo.
4. Cada capítulo é resumido individualmente.
5. Há artefato de `rolling_context`.
6. A síntese final é derivada dos artefatos intermediários.
7. PDF gera warning explícito quando EPUB não estiver disponível.
8. Todos os artefatos são persistidos e rastreáveis.
9. O fluxo pode operar em modo determinístico ou LLM progressivo.
