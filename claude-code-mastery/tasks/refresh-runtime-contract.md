# Task: Refresh Runtime Contract

**Task ID:** CCM-ROADMAP-002
**Version:** 1.0.0
**Command:** `*refresh-runtime-contract`
**Orchestrator:** Vigil (roadmap-sentinel)
**Purpose:** Atualizar o contrato canônico de runtime da squad `claude-code-mastery` reconciliando dados, docs e trechos de agentes com o comportamento real observado no código-fonte do Claude Code.

## Contrato SINKRA

task: refresh-runtime-contract
atomic_layer: Atom
executor: roadmap-sentinel
Domain: Strategic
accountability_token: TK-CCM-ACC-001
Input:
- source_analysis_root
- squad_runtime_surfaces
- escopo de atualização
Output:
- runtime-contract-delta-report
- plano de sincronização aplicado
output_schema: contract-update-yaml
Pre-Conditions:
- Fontes canônicas do runtime disponíveis e legíveis
- Superfícies da squad identificadas antes da edição
- Critério de sucesso entendido antes da execução
Post-Conditions:
- Terminologia de runtime sincronizada nas superfícies-alvo
- Divergências remanescentes registradas com impacto explícito
- Próximo passo ou handoff emitido
Performance:
- Execução em uma sessão sem falha silenciosa
- Mudanças agrupadas por domínio de runtime
- Resultado acionável para o próximo executor
Completion Criteria:
- Contract synced with latest cc-architecture-map
- 0 drift between canonical and operational surfaces
- Contradições críticas removidas das superfícies-alvo

---


## Overview

```
  +-------------------------+
  | 1. Carregar SOT         |
  |    do runtime           |
  +-------------------------+
              |
              v
  +-------------------------+
  | 2. Mapear divergências  |
  |    por domínio          |
  +-------------------------+
              |
              v
  +-------------------------+
  | 3. Priorizar superfícies|
  |    e terminologia       |
  +-------------------------+
              |
              v
  +-------------------------+
  | 4. Aplicar sincronização|
  |    coordenada           |
  +-------------------------+
              |
              v
  +-------------------------+
  | 5. Validar coerência    |
  |    cruzada              |
  +-------------------------+
              |
              v
  +-------------------------+
  | 6. Publicar delta       |
  |    report + próximos    |
  |    executores           |
  +-------------------------+
```

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| source_analysis_root | string | `outputs/decoded/claude-code-main/` | Yes | Deve conter Phase 3 e Phase 5 do pipeline de extração |
| squad_root | string | Working directory | Yes | Deve conter `squads/claude-code-mastery/` |
| target_surfaces | list | User ou padrão | No | Lista de arquivos a sincronizar; default: quick-ref, permission-rules, architecture-map, agentes-core |
| apply_changes | boolean | User | No | Se `false`, gerar apenas delta report; default: `true` |

---

## Preconditions

- Os artefatos canônicos existem em `outputs/decoded/claude-code-main/`
- Os arquivos-alvo da squad podem ser lidos e modificados
- Existe um domínio canônico explícito para cada mudança proposta

---

## Execution Phases

### Phase 1: Carregar o SOT do runtime

Ler como fontes primárias:

- `phase-3-modeling/decision-model.yaml`
- `phase-5-validation/final-rule-catalog.md`
- `phase-5-validation/validation-summary.yaml`

Se necessário, confirmar em arquivos de código do `claude-code-main` os domínios:

- permission modes e pipeline
- MCP policy
- memória e contexto
- keybindings
- background/Monitor
- remote sessions

### Phase 2: Construir matriz de divergência

Mapear diferenças entre runtime real e superfícies da squad:

- `data/claude-code-quick-ref.yaml`
- `data/cc-permission-rules.yaml`
- `data/cc-architecture-map.yaml`
- trechos relevantes de `agents/*.md`
- tasks que ensinam comportamento operacional

Classificar cada divergência como:

- `terminology_drift`
- `behavior_drift`
- `feature_gate_missing`
- `unsafe_recommendation`
- `stale_reference`

### Phase 3: Priorizar superfícies e ordem de correção

Usar a seguinte ordem:

1. superfícies que ensinam comportamento incorreto
2. superfícies que impactam setup ou auditoria
3. superfícies de apoio e referência rápida
4. superfícies históricas ou contextuais

### Phase 4: Aplicar sincronização coordenada

Atualizar as superfícies-alvo preservando uma única terminologia ativa para:

- permission modes
- precedência de decisão
- MCP e política enterprise
- regras de memória/contexto
- features gated
- limites operacionais de runtime

Quando uma funcionalidade for gated, documentar como:

- `disponível apenas sob feature flag`
- `condicional por ambiente`
- `interno/limitado`

Nunca promover capacidade condicional como se fosse universal.

### Phase 5: Validar coerência cruzada

Verificar:

- os mesmos modos aparecem com o mesmo nome em quick ref, data e agentes
- aliases históricos não aparecem como modo atual recomendado
- features gated estão rotuladas corretamente
- quick commands e guias não contradizem a referência canônica

### Phase 6: Publicar o delta report

Gerar relatório contendo:

- divergências corrigidas
- arquivos tocados
- divergências adiadas
- impacto operacional
- próximos executores recomendados

---

## Output Format

```markdown
## Runtime Contract Delta Report

**Scope:** {target_surfaces}
**Canonical Source:** {source_analysis_root}
**Status:** {applied|planned}

### Divergências Corrigidas

| Domínio | Superfície | Antes | Depois | Impacto |
|---------|------------|-------|--------|---------|

### Divergências Abertas

| Domínio | Motivo | Risco | Próximo Executor |
|---------|--------|-------|------------------|

### Decisões de Terminologia

- {lista de termos canônicos definidos}
```

---

## Veto Conditions

- Ausência do artefato canônico de Phase 3 ou Phase 5
- Permanecerem nomes de modos obsoletos como recomendação principal
- Documentação passar a tratar feature gated como capability universal
- Haver contradição explícita entre quick ref, data e agentes após a sincronização

---

## Completion Criteria

- Pelo menos uma superfície de referência e uma superfície operacional foram sincronizadas
- Existe um delta report auditável com antes/depois
- Terminologia canônica foi unificada nas superfícies alteradas
- Foi emitido handoff para `config-engineer` ou `skill-craftsman` quando aplicável

---

*Task: refresh-runtime-contract v1.0.0*
