# Data Intelligence Pack v1.0 - Setup

## MISSION

Criar o Data Intelligence Squad com 6 agents especializados (clones de experts reais) e tasks operacionais para análise de dados de negócio.

---

## CONTEXTO

Este pack implementa um framework de 3 camadas:

```
CAMADA 1 - FUNDAMENTAÇÃO (Tier 0)
├── Peter Fader (CLV, RFM, Customer Centricity)
└── Sean Ellis (AARRR, North Star, PMF)

CAMADA 2 - OPERACIONALIZAÇÃO (Tier 1)
├── Nick Mehta (Health Score, Churn, DEAR)
├── David Spinks (Community Metrics, SPACES)
└── Wes Kao (Learning Outcomes, CBC)

CAMADA 3 - COMUNICAÇÃO (Tier 2)
└── Avinash Kaushik (Attribution, DMMM, Storytelling)
```

**Regra de Ouro:** Nunca implemente uma métrica sem passar por pelo menos 1 fundamentador (Tier 0).

---

## FONTES PARA PESQUISA

### Framework Docs (LEIA PRIMEIRO)
```
squads/data/data/framework/
├── 01_arquitetura_geral.md
├── 02_tier0_fundacao.md
├── 03_tier0_fundamentadores.md (Fader + Ellis)
├── 04_tier1_operacionalizadores.md (Mehta + Spinks + Kao)
├── 05_tier2_comunicadores.md (Kaushik)
├── 06_matriz_decisao.md
├── 07_workflows.md
└── 08_cheatsheet.md
```

### Web Research (USAR PARA ENRIQUECER)
Para cada expert, pesquisar:
- Livros publicados
- Papers acadêmicos (se aplicável)
- Blog posts e newsletters
- Talks e podcasts
- Frameworks originais

---

## PADRÃO DE AGENT (1500+ linhas)

Seguir estrutura do squads/copy/agents/:

```yaml
# agent-name.md

ACTIVATION-NOTICE: ...
CRITICAL: ...

agent:
  name: Full Name
  id: agent-id
  title: ESPECIALIDADE - Role Description
  icon: emoji
  tier: 0|1|2
  era: Current
  whenToUse: "Descrição de quando usar este agent"

persona:
  role: Descrição do papel
  style: Estilo de comunicação
  identity: Como o agent se apresenta
  focus: Foco principal

core_principles:
  - "Princípio 1..."
  - "Princípio 2..."

commands:
  - "*help - Ver comandos"
  - "*framework-name - Aplicar framework X"
  - ...

operational_frameworks:
  total_frameworks: N

  framework_1:
    name: "Nome do Framework"
    category: "categoria"
    origin: "Fonte original"
    ...

signature_phrases:
  - phrase: "Citação direta"
    context: "Quando usa"
    source: "Onde disse"
  ...

# E mais seções conforme necessário
```

---

## PADRÃO DE TASK (800+ linhas)

```yaml
# task-name.md

## Metadata
task:
  name: Task Name
  id: task-id
  version: "1.0"
  category: categoria
  difficulty: basic|intermediate|advanced
  primary_agents:
    - agent-1
    - agent-2
  ...

## Overview
Descrição da task...

## PHASE 0: PRE-FLIGHT CHECK
...

## PHASE 1: ...
...

## Elicitation Questions
...

## Output Format
...

## Examples
...
```

---

## WORKFLOW

1. **Leia o framework doc** correspondente ao seu agent/task
2. **Faça web research** para enriquecer com conteúdo real
3. **Crie o arquivo** seguindo o padrão
4. **Verifique acceptance criteria**
5. **Marque como completo** no prd.json

---

## COMPLETION

```bash
jq --arg id "DATA-XXX" --arg notes "Completed: N frameworks, M signature phrases, X linhas" \
  '.userStories = [.userStories[] | if .id == $id then .passes = true | .notes = $notes else . end]' \
  squads/data/projects/data-v1-setup/prd.json > tmp.json && mv tmp.json squads/data/projects/data-v1-setup/prd.json
```

---

## QUALIDADE ESPERADA

- Agents: 1500+ linhas, 10+ frameworks, 30+ signature phrases
- Tasks: 800+ linhas, fases claras, elicitation questions
- Checklists: 300+ linhas, quality gates
- Templates: Estrutura YAML completa

**NÃO ACEITÁVEL:**
- Agents genéricos sem frameworks específicos do expert
- Tasks sem metodologia clara
- Conteúdo que poderia ser de qualquer pessoa (não específico do expert)

---

## GO!

Identifique sua story, leia as fontes, pesquise o expert, e crie conteúdo de alta qualidade.
