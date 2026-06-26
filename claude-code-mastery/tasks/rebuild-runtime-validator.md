# Task: Rebuild Runtime Validator

**Task ID:** CCM-CONFIG-006
**Version:** 1.0.0
**Command:** `*rebuild-validator`
**Orchestrator:** Sigil (config-engineer)
**Purpose:** Reconstruir `scripts/validate-setup.js` como validador orientado a contrato de runtime, alinhado ao comportamento real do Claude Code e aos thresholds da squad.

## Contrato SINKRA

task: rebuild-runtime-validator
atomic_layer: Atom
executor: config-engineer
Domain: Tactical
accountability_token: TK-CCM-ACC-001
Input:
- validator_target
- runtime_contract_sources
- quality_gates
Output:
- validator-rebuild-report
- validator-contract-matrix
output_schema: validator-script
Pre-Conditions:
- Script atual acessível e legível
- Fontes de contrato de runtime disponíveis
- Thresholds da squad definidos
Post-Conditions:
- Cobertura do validador explicitada por domínio
- Lacunas remanescentes registradas com severidade
- Próximo passo ou handoff emitido
Performance:
- Execução em uma sessão sem falha silenciosa
- Checklists substituídos por checks rastreáveis
- Resultado acionável para implementação
Completion Criteria:
- Validator script passes all test cases
- cc-permission-rules coverage verified
- Nova matriz de validação conectada a quality gates

---


## Overview

```
  +--------------------------+
  | 1. Auditar validador     |
  |    atual                 |
  +--------------------------+
              |
              v
  +--------------------------+
  | 2. Definir matriz de     |
  |    cobertura do contrato |
  +--------------------------+
              |
              v
  +--------------------------+
  | 3. Redesenhar a          |
  |    arquitetura do script |
  +--------------------------+
              |
              v
  +--------------------------+
  | 4. Implementar checks    |
  |    orientados a runtime  |
  +--------------------------+
              |
              v
  +--------------------------+
  | 5. Emitir saída humana + |
  |    máquina               |
  +--------------------------+
              |
              v
  +--------------------------+
  | 6. Validar com QG        |
  |    e smoke fixtures      |
  +--------------------------+
```

---

## Inputs

| Field | Type | Source | Required | Validation |
|-------|------|--------|----------|------------|
| project_root | string | Working directory | Yes | Deve apontar para projeto com `.claude/` ou `CLAUDE.md` |
| validator_target | string | Default | No | Default: `squads/claude-code-mastery/scripts/validate-setup.js` |
| runtime_contract_sources | list | Squad data + decoded outputs | Yes | Deve incluir permission rules, architecture map e extração do `claude-code-main` |
| output_mode | enum | User | No | `markdown`, `json`, `both` |

---

## Preconditions

- O script legado pode ser executado ou analisado
- Há acesso a `quality-gates.yaml`
- O executor conhece a diferença entre referência histórica e contrato atual

---

## Execution Phases

### Phase 1: Auditar o validador atual

Identificar o que o script atual cobre e o que deixa de cobrir:

- modos de permissão
- deny coverage
- sandbox
- MCP
- keybindings
- memória/contexto
- features gated
- formato de saída

Classificar cada lacuna como:

- `missing_check`
- `stale_check`
- `weak_signal`
- `wrong_contract`

### Phase 2: Definir a matriz de cobertura

Construir uma matriz explícita:

| Domínio | Fonte canônica | Check esperado | Severidade |
|--------|-----------------|----------------|------------|

Domínios mínimos:

- permission modes e pipeline
- regras sensíveis deny/ask/allow
- sandbox e restrições
- MCP local/plugin/enterprise
- keybindings e atalhos reservados
- contexto/memória
- saída estruturada e thresholds

### Phase 3: Redesenhar a arquitetura do validador

O novo validador deve:

- separar coleta, avaliação e renderização
- produzir saída legível e saída estruturada
- mapear findings por severidade
- conectar score aos thresholds de `quality-gates.yaml`

Preferir uma arquitetura extensível, não um script monolítico com checks ad hoc.

### Phase 4: Implementar checks orientados a runtime

Checks obrigatórios:

- nomes de modos suportados realmente pelo runtime
- proteção deny-first mínima
- `.mcp.json` e política MCP efetiva
- enterprise exclusivity e allow/deny MCP
- schema e conflitos de keybindings
- limites de `CLAUDE.md` e `MEMORY.md`
- sinais de guidance obsoleto em config

### Phase 5: Emitir saída para humano e máquina

Saída mínima:

- resumo executivo em Markdown
- findings estruturados em JSON ou YAML
- score por dimensão
- vetoes acionados
- recomendações ordenadas

### Phase 6: Validar com quality gates

Verificar aderência a:

- `deny_rule_coverage`
- `settings_parse_success`
- `context_budget_adherence`
- `artifact_contract_coverage`

Se houver fixtures ou projetos de referência, rodar smoke validation neles.

---

## Output Format

```markdown
## Validator Rebuild Report

**Target:** {validator_target}
**Output Mode:** {output_mode}
**Status:** {planned|implemented}

### Coverage Matrix

| Domínio | Legacy | Novo | Observação |
|---------|--------|------|------------|

### Findings

| # | Severidade | Gatilho | Ação |
|---|------------|---------|------|

### Quality Gate Fit

| Gate | Threshold | Status |
|------|-----------|--------|
```

---

## Veto Conditions

- Permanecer `askAlways` ou `autoApprove` como modo atual suportado
- Script continuar emitindo apenas nota/letra sem findings estruturados
- Ausência de checks para MCP, keybindings ou memória/contexto
- Quality gates da squad não serem consumidos pelo novo desenho

---

## Completion Criteria

- Existe matriz de cobertura ligando checks a fontes canônicas
- O redesign elimina checks historicamente incorretos
- O output final inclui formato para humano e para máquina
- O relatório final aponta se a implementação está pronta ou ainda depende de execução

---

*Task: rebuild-runtime-validator v1.0.0*
