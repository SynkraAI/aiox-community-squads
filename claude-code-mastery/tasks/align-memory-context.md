# Task: Align Memory and Context Model

**Task ID:** CCM-CONTEXT-003
**Version:** 1.0.0
**Command:** `*align-memory-context`
**Orchestrator:** Anvil (skill-craftsman)
**Purpose:** Alinhar a doutrina de contexto da squad com o modelo real de memória do Claude Code, incluindo `MEMORY.md`, limites de budget, exclusão de estado derivável e comportamento append-only em modo assistant.

## Contrato SINKRA

task: align-memory-context
atomic_layer: Atom
executor: skill-craftsman
Domain: Tactical
accountability_token: TK-CCM-ACC-001
Input:
- runtime_memory_sources
- context_surfaces
- target_guidance_scope
Output:
- memory-context-alignment-report
- guidance-delta
output_schema: memory-alignment-yaml
Pre-Conditions:
- Fontes do modelo de memória disponíveis
- Superfícies de contexto identificadas antes da edição
- Critério de sucesso entendido antes da execução
Post-Conditions:
- Guidance de contexto sincronizada com o runtime real
- Diferenças entre modo padrão e assistant explicitadas
- Próximo passo ou handoff emitido
Performance:
- Execução em uma sessão sem falha silenciosa
- Recomendações focadas em reduzir contexto inútil
- Resultado acionável para docs e tasks da squad
Completion Criteria:
- Memory context aligned with cc-architecture-map
- 0 stale refs in context surfaces
- Guidance final sem ambiguidade operacional crítica

---


## Overview

```
  +-------------------------+
  | 1. Ler o modelo real    |
  |    de memória           |
  +-------------------------+
              |
              v
  +-------------------------+
  | 2. Auditar superfícies  |
  |    de contexto          |
  +-------------------------+
              |
              v
  +-------------------------+
  | 3. Reescrever guidance  |
  |    estável vs dinâmica  |
  +-------------------------+
              |
              v
  +-------------------------+
  | 4. Ajustar tarefas e    |
  |    referências          |
  +-------------------------+
              |
              v
  +-------------------------+
  | 5. Validar budget e     |
  |    anti-patterns        |
  +-------------------------+
              |
              v
  +-------------------------+
  | 6. Publicar delta       |
  |    report               |
  +-------------------------+
```

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| runtime_memory_sources | list | `cc-architecture-map` + decoded outputs | Yes | Deve incluir memória/contexto do runtime real |
| context_surfaces | list | Squad docs e tasks | Yes | Deve incluir quick ref, tasks de contexto e guidance de `CLAUDE.md` |
| target_guidance_scope | enum | User | No | `docs`, `tasks`, `agents`, `all` |
| apply_changes | boolean | User | No | Default: `true` |

---

## Preconditions

- Fontes de memória do runtime estão acessíveis
- A squad possui superfícies dedicadas a contexto e `CLAUDE.md`
- O executor consegue distinguir índice, memória derivada e log operacional

---

## Execution Phases

### Phase 1: Ler o modelo real de memória

Extrair como regras canônicas:

- `MEMORY.md` como arquivo de entrada/índice
- limite de 200 linhas e 25 KB
- exclusão de estado derivável do projeto
- seleção de memórias relevantes por utilidade clara
- exclusão de `MEMORY.md` da seleção adicional
- modo assistant/KAIROS com log diário append-only

### Phase 2: Auditar superfícies de contexto da squad

Auditar pelo menos:

- `data/claude-code-quick-ref.yaml`
- `tasks/context-rot-audit.md`
- `tasks/claude-md-engineer.md`
- `tasks/optimize-context.md`
- trechos de agentes que ensinam contexto/memória

### Phase 3: Reescrever guidance estável vs dinâmica

Separar guidance em dois blocos:

- `regras estáveis`
  - tamanho do índice
  - o que entra e o que não entra em memória
  - quando dividir para rules/imports
- `comportamento dinâmico`
  - seleção de memória relevante
  - uso contextual de warnings/gotchas
  - append-only em modo assistant

### Phase 4: Ajustar tasks e referências

Atualizar tasks e referências para que:

- não incentivem `MEMORY.md` como dumping ground
- não tratem `CLAUDE.md` longo como default aceitável
- indiquem quando promover conteúdo para rules/imports
- deixem explícito o que é guidance para modo assistant

### Phase 5: Validar budget e anti-patterns

Bloquear guidance que:

- exceda os limites canônicos sem justificativa
- recomende guardar fatos deriváveis do código
- misture índice curado com log bruto
- omita a distinção entre memória estável e memória transitória

### Phase 6: Publicar delta report

Emitir relatório com:

- superfícies auditadas
- guidance corrigida
- anti-patterns removidos
- superfícies ainda pendentes

---

## Output Format

```markdown
## Memory Context Alignment Report

**Scope:** {target_guidance_scope}
**Status:** {applied|planned}

### Regras Canônicas

- {lista curta das regras estabilizadas}

### Superfícies Corrigidas

| Arquivo | Drift | Correção |
|---------|-------|----------|

### Anti-patterns Removidos

| Anti-pattern | Risco | Status |
|--------------|-------|--------|
```

---

## Veto Conditions

- Guidance recomendar `MEMORY.md` acima do limite canônico sem ressalva
- Guidance tratar memória como cópia do estado derivável do projeto
- Guidance misturar índice e log append-only como se fossem o mesmo artefato
- Superfícies de contexto permanecerem com instruções contraditórias após a edição

---

## Completion Criteria

- Há uma distinção explícita entre índice, memória relevante e log append-only
- Tasks de contexto da squad não contradizem o runtime real
- O relatório final identifica claramente o que foi sincronizado e o que ficou pendente
- Há handoff definido para `config-engineer` ou `roadmap-sentinel` se necessário

---

*Task: align-memory-context v1.0.0*
