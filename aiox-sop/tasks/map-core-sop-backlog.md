# Map Core SOP Backlog by Business Category

**Task ID:** `map-core-sop-backlog`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.1.0
**Last Updated:** 2026-03-18
**Governance Protocol:** `squads/squad-creator/protocols/ai-first-governance.md`

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Map Core SOP Backlog by Business Category |
| **status** | `pending` |
| **responsible_executor** | @sop-chief (orquestração) + @analyst (research context) |
| **execution_type** | `Agent` |
| **input** | Workspace businesses profiles, operations YAMLs, industry benchmarks |
| **output** | sop-research-context.yaml + sop-backlog.yaml por business |
| **action_items** | 7 fases |
| **acceptance_criteria** | 8 critérios |

**Estimated Time:** 2-4h (com research)

## Executor Specification

| Attribute | Value |
|-----------|-------|
| **Type** | Agent |
| **Pattern** | HO-EP-002 |
| **Executor** | @sop-chief (orquestra) → @analyst (pesquisa) → @sop-creator (gera backlog) |
| **Rationale** | Requer análise de padrões cross-business, categorização de mercado e pesquisa de processos por indústria |
| **Fallback** | Hybrid (Agent gera draft, Human valida categorização) |

## Overview

Task que analisa TODOS os businesses do workspace, categoriza por tipo de mercado/indústria, e gera para CADA business um backlog priorizado de SOPs core baseado na sua categoria. Cada business recebe um **research context** e um **backlog** salvos no seu próprio diretório de operations.

**Conceito-chave (Ciclo 2 Pedro Valério):**
- **Processos Burros:** repetitivos, determinísticos, sem singularidade. Worker executa 80%+. Horas para sincronizar. Invisíveis.
- **Processos Core (Delivery):** o que a empresa vende, o que gera receita. Mix dos 4 executores. Semanas a meses para sincronizar. Visíveis. São marketing, vendas e retenção.

Esta task mapeia AMBOS para cada categoria, mas prioriza os **core** porque são eles que criam moat competitivo.

**Princípio:** "Se eu consigo replicar teu processo core em dois dias, tua empresa não tem moat."

**Onde vivem os outputs:** `workspace/businesses/{slug}/L1-strategy/` - cada business recebe seus próprios arquivos. O sop-chief lê esses arquivos via `workspace/businesses/` (já declarado nos read_paths do aiox-sop config.yaml) para saber quais SOPs básicas criar.

## Input

- **workspace_businesses** (directory)
  - Description: Diretório com todos os businesses do workspace
  - Required: Yes
  - Source: `workspace/businesses/*/L0-identity/company-dna.yaml`

- **operations_yamls** (directory)
  - Description: YAMLs operacionais de cada business (team-structure, pricing, KPIs)
  - Required: No (nem todos possuem)
  - Source: `workspace/businesses/*/L1-strategy/`

- **existing_sops** (directory)
  - Description: SOPs já criados para evitar duplicação
  - Required: No
  - Source: `workspace/businesses/*/sops/`

- **industry_benchmarks** (research)
  - Description: Processos padrão por indústria (via pesquisa web ou knowledge base)
  - Required: No (enrichment opcional)
  - Source: Web research ou `squads/aiox-sop/data/`

## Output

### Squad Knowledge Base (estático, genérico)

- **category-map.yaml** (único, no squad)
  - Description: Base de conhecimento que mapeia categorias de negócio → SOPs mínimas que todo negócio daquele tipo precisa ter. Não contém dados de businesses específicos. É o "manual de referência" do sop-chief.
  - Destination: `squads/aiox-sop/data/category-map.yaml`
  - Format: YAML com categorias, processos core típicos por indústria, processos burros universais
  - Consumed by: sop-chief (sabe quais SOPs básicas cada TIPO de negócio precisa)
  - Atualização: Rara. Só quando novas categorias de mercado são identificadas.

### Per-Business (dinâmico, específico)

- **sop-research-context.yaml** (por business)
  - Description: Research context com categoria do business, processos core e burros aplicáveis a ELE
  - Destination: `workspace/businesses/{slug}/L1-strategy/sop-research-context.yaml`
  - Format: YAML com categoria atribuída, processos core, processos burros, research gaps
  - Consumed by: sop-chief (contexto ao criar SOPs para este business)

- **sop-backlog.yaml** (por business)
  - Description: Backlog priorizado de SOPs que ESTE business precisa
  - Destination: `workspace/businesses/{slug}/L1-strategy/sop-backlog.yaml`
  - Format: YAML com SOPs priorizados (P0-P3), executor dominante, complexidade
  - Consumed by: sop-chief (prioriza qual SOP criar primeiro), COO (diagnóstico)

## Action Items

### Fase 1: Inventário de Businesses

Varrer `workspace/businesses/` e extrair dados de categorização de cada business.

**Substeps:**
- [ ] Ler `L0-identity/company-dna.yaml` de cada business
- [ ] Extrair: `industry`, `segment`, `business_model`, `revenue_range`, `team_size`, `stage`
- [ ] Extrair: `pain_points`, `bottlenecks`, `operational_gaps` (se disponíveis)
- [ ] Verificar existência de `L1-strategy/` e `sops/` em cada business
- [ ] Gerar inventário completo em memória

**Mapeamento de campos esperados no company-profile.yaml:**

```yaml
# Campos de categorização (paths dentro do YAML)
industry: company.industry          # Ex: "EdTech", "MedTech", "Telecom"
segment: company.segment            # Ex: "Medical Preparation", "Aesthetic Equipment"
business_model: company.business_model  # Ex: "SaaS + Education", "B2B Equipment Sales"
revenue: company.revenue_range      # Ex: "{currency}5-20M", "{currency}100M+"
team_size: company.team_size        # Ex: 130, "6-15"
stage: company.stage                # Ex: "SCALE", "GROWTH", "EARLY"
```

### Fase 2: Categorização por Mercado

Agrupar businesses por categoria de mercado usando taxonomia padronizada.

**Categorias identificadas no workspace atual:**

| ID | Categoria | Slug | Businesses | Faturamento Range |
|----|-----------|------|------------|-------------------|

> **Nota:** A tabela de categorias com businesses e faixas de faturamento é carregada dinamicamente de `data/market-categories.yaml`. Não hardcode valores monetários aqui.

**Regras de categorização:**
- Business pode aparecer em mais de uma categoria (ex: `youfront` = SaaS + Agência)
- Categoria principal = onde está o core revenue
- Categoria secundária = adjacências

**Substeps:**
- [ ] Aplicar taxonomia aos businesses inventariados
- [ ] Resolver ambiguidades (perguntar ao usuário se necessário)
- [ ] Manter mapa de categorias em memória para uso nas fases seguintes

### Fase 3: Mapeamento de Processos Burros (Universais)

Identificar processos repetitivos que são comuns a TODAS as categorias. Estes são quick wins universais.

**Processos Burros Universais (cross-category):**

| ID | Processo | Executor | Complexidade |
|----|----------|----------|-------------|
| PB-UNIV-01 | Criar pasta/projeto no sistema de gestão (ClickUp, Notion, etc.) | Worker | Baixa |
| PB-UNIV-02 | Classificar/qualificar lead inbound | Worker/Agent | Baixa-Média |
| PB-UNIV-03 | Enviar email padrão (confirmação, boas-vindas, follow-up) | Worker | Baixa |
| PB-UNIV-04 | Onboarding administrativo de novo colaborador | Hybrid | Média |
| PB-UNIV-05 | Gerar relatório periódico de métricas | Worker | Baixa |
| PB-UNIV-06 | Publicar conteúdo em redes sociais (agendamento) | Worker | Baixa |
| PB-UNIV-07 | Emitir nota fiscal / fatura | Worker | Baixa |
| PB-UNIV-08 | Backup de dados / exportação periódica | Worker | Baixa |
| PB-UNIV-09 | Triagem de suporte / atendimento nível 1 | Agent | Média |
| PB-UNIV-10 | Atualizar CRM com dados de interação | Worker | Baixa |

**Substeps:**
- [ ] Consolidar processos burros identificados nos pain_points dos businesses
- [ ] Cruzar com lista universal acima
- [ ] Validar que são genuinamente determinísticos (Worker 80%+)
- [ ] Priorizar por frequência de aparição cross-business

### Fase 4: Mapeamento de Processos Core (Por Categoria)

Para CADA categoria, identificar os processos core que são o delivery/moat da empresa.

**Processos Core esperados por categoria (seed inicial):**

#### CAT-01: EdTech / Educação Online
| ID | Processo Core | Evidência | Businesses |
|----|--------------|-----------|------------|
| PC-01-01 | Pipeline de produção de conteúdo/aulas | Gargalo #1 em 4/6 EdTechs | nexos, ecossistema, omni, aiox |
| PC-01-02 | Onboarding de aluno premium | Retenção e NPS | eu_medico, academia, aiox |
| PC-01-03 | Ciclo de lançamento de turma/cohort | Revenue event principal | aiox, academia, omni |
| PC-01-04 | Avaliação e certificação de alunos | Credibilidade do produto | eu_medico, nexos |
| PC-01-05 | Suporte pedagógico / mentoria | Diferencial competitivo | eu_medico, omni, grupo_scalco |

#### CAT-04: Agência / Serviços de Marketing
| ID | Processo Core | Evidência | Businesses |
|----|--------------|-----------|------------|
| PC-04-01 | Pipeline de propostas comerciais | Case: custo/proposta reduzido 98% via automação | grupo_fabio, youfront |
| PC-04-02 | Produção de criativos (ads, vídeos) | Gargalo de escala em 3/3 agências | nutraself, youfront, grupo_fabio |
| PC-04-03 | Relatório de performance para cliente | Retenção e upsell | youfront, grupo_fabio |
| PC-04-04 | Onboarding de novo cliente | Time-to-value | grupo_fabio, youfront |

#### CAT-06: Healthcare / MedTech
| ID | Processo Core | Evidência | Businesses |
|----|--------------|-----------|------------|
| PC-06-01 | Pipeline regulatório (ANVISA, certificações) | Compliance obrigatório | conta_magic |
| PC-06-02 | Gestão de estoque médico / equipamentos | Logística crítica | conta_magic |
| PC-06-03 | Atendimento clínico / triagem | Delivery do serviço | eu_medico |

#### CAT-05: Gaming / Entretenimento
| ID | Processo Core | Evidência | Businesses |
|----|--------------|-----------|------------|
| PC-05-01 | Pipeline de publicação de jogos | Core do modelo publisher | level8_herobase |
| PC-05-02 | Onboarding de micro-studios | Escala do modelo | level8_herobase |
| PC-05-03 | QA e testing de builds | Quality gate do delivery | level8_herobase |

#### CAT-08: Telecom / Multi-negócios
| ID | Processo Core | Evidência | Businesses |
|----|--------------|-----------|------------|
| PC-08-01 | Gestão de franquias / unidades | Escala do modelo | grupo_wv |
| PC-08-02 | Provisioning de serviço telecom | Delivery core | grupo_wv |
| PC-08-03 | Controle administrativo multi-empresa | Alto custo admin multi-empresa | grupo_wv |

#### CAT-07: Turismo / Gastronomia
| ID | Processo Core | Evidência | Businesses |
|----|--------------|-----------|------------|
| PC-07-01 | Onboarding de estabelecimento parceiro | Crescimento do marketplace | brasil_em_dobro |
| PC-07-02 | Pipeline de expansão para nova cidade | Replicação do modelo | brasil_em_dobro |

#### CAT-10: Direct Response / eCommerce
| ID | Processo Core | Evidência | Businesses |
|----|--------------|-----------|------------|
| PC-10-01 | Pipeline de criação de VSL/funnel | Revenue driver #1 | nutraself |
| PC-10-02 | Ciclo de teste de criativos | Escala de tráfego pago | nutraself |
| PC-10-03 | Supply chain de suplementos | Delivery físico | nutraself |

#### CAT-02: Desenvolvimento Pessoal / Coaching
| ID | Processo Core | Evidência | Businesses |
|----|--------------|-----------|------------|
| PC-02-01 | Pipeline de imersão presencial | Evento = revenue principal | grupo_scalco |
| PC-02-02 | Gestão de comunidade / tribo | Retenção e LTV | grupo_scalco, vida_lendaria |
| PC-02-03 | Pipeline de mentoria high-ticket | Revenue por sessão | mentoria_andre_franco |

#### CAT-03: SaaS / Tecnologia
| ID | Processo Core | Evidência | Businesses |
|----|--------------|-----------|------------|
| PC-03-01 | Onboarding de usuário SaaS | Ativação e retenção | optimus, ecossistema |
| PC-03-02 | Ciclo de release / deploy | Delivery contínuo | optimus, youfront |
| PC-03-03 | Suporte técnico / bug triage | Churn prevention | optimus, ecossistema |

#### CAT-09: Cripto / Investimentos
| ID | Processo Core | Evidência | Businesses |
|----|--------------|-----------|------------|
| PC-09-01 | Pipeline de análise de mercado / sinais | Delivery core | mentoria_andre_franco |
| PC-09-02 | Compliance regulatório financeiro | Obrigatório | mentoria_andre_franco |

**Substeps por categoria:**
- [ ] Ler todos os company-profiles da categoria
- [ ] Extrair pain_points, bottlenecks, operational_gaps
- [ ] Identificar padrões: quais processos aparecem em 2+ businesses da mesma categoria?
- [ ] Classificar cada processo: core vs burro
- [ ] Para processos core: detalhar executor_mix e time_to_sync

### Fase 5: Priorização do Backlog

Consolidar todos os processos (core + burros) em um backlog único priorizado.

**Critérios de priorização:**

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Frequência cross-business** | 30% | Quantos businesses se beneficiam |
| **Impacto em receita** | 25% | Processo core = alto impacto |
| **Complexidade de criação** | 20% | Menor complexidade = faster win |
| **Dados disponíveis** | 15% | Quanto mais dados no workspace, mais fácil criar |
| **Urgência reportada** | 10% | Pain points explícitos nos profiles |

**Níveis de prioridade:**
- **P0 (Critical):** Processo core que aparece em 3+ businesses E tem dados no workspace
- **P1 (High):** Processo core com 2+ businesses OU burro universal com 5+ businesses
- **P2 (Medium):** Processo core single-business OU burro com 2-4 businesses
- **P3 (Low):** Processo identificado por benchmark sem evidência no workspace

**Substeps:**
- [ ] Consolidar todos os processos mapeados (Fase 3 + Fase 4)
- [ ] Aplicar scoring com pesos definidos
- [ ] Rankear por score descendente

### Fase 6: Geração dos Outputs

#### 6a: Category Map (squad knowledge base)

Gerar `squads/aiox-sop/data/category-map.yaml` com a base de conhecimento genérica.

**Substeps:**
- [ ] Consolidar todas as categorias mapeadas (Fase 2)
- [ ] Para cada categoria: listar processos core típicos + processos burros universais
- [ ] Incluir SOPs mínimas que todo negócio daquele tipo precisa
- [ ] Salvar em `squads/aiox-sop/data/category-map.yaml`

#### 6b: Per-Business Outputs (workspace)

Para CADA business no workspace, gerar os dois arquivos de output.

**Substeps:**
- [ ] Para cada business: identificar sua(s) categoria(s) no category-map
- [ ] Compilar processos core da(s) categoria(s) + processos burros universais
- [ ] Gerar `workspace/businesses/{slug}/L1-strategy/sop-research-context.yaml`
- [ ] Gerar `workspace/businesses/{slug}/L1-strategy/sop-backlog.yaml`
- [ ] Incluir seção `research_gaps` com dados faltantes que precisam de pesquisa

**Estrutura do sop-research-context.yaml (per-business):**

```yaml
# workspace/businesses/{slug}/L1-strategy/sop-research-context.yaml
business:
  slug: "brasil_em_dobro"
  name: "Brasil em Dobro"
  primary_category:
    id: "CAT-07"
    name: "Turismo / Gastronomia"
    slug: "tourism-gastronomy"
  secondary_categories: []

core_processes:
  - id: "PC-07-01"
    name: "Onboarding de estabelecimento parceiro"
    description: "Ciclo completo de captação e ativação de novo parceiro no marketplace"
    why_core: "Crescimento do marketplace depende de volume de parceiros ativos"
    executor_mix:
      human: "30%"
      agent: "40%"
      worker: "20%"
      hybrid: "10%"
    complexity: "média"
    time_to_sync: "semanas"
    sop_priority: "P0"
    industry_evidence: "Onboarding de parceiros é padrão em marketplaces"
  - id: "PC-07-02"
    name: "Pipeline de expansão para nova cidade"
    # ...

dumb_processes:
  - id: "PB-UNIV-01"
    name: "Criar pasta/projeto no sistema de gestão"
    executor: "Worker"
    sop_priority: "P1"
  - id: "PB-UNIV-02"
    name: "Classificar/qualificar lead inbound"
    executor: "Worker/Agent"
    sop_priority: "P1"
  # ... (universais aplicáveis a este business)

research_gaps:
  - field: "bottlenecks"
    status: "missing"
    action: "Structured interview ou diagnóstico C-Level"
```

**Estrutura do sop-backlog.yaml (per-business):**

```yaml
# workspace/businesses/{slug}/L1-strategy/sop-backlog.yaml
business:
  slug: "brasil_em_dobro"
  name: "Brasil em Dobro"
  generated_at: "2026-03-18"
  total_sops: 12

backlog:
  - id: "SOP-PC-07-01"
    name: "Onboarding de Estabelecimento Parceiro"
    type: "core"
    priority: "P0"
    score: 88
    executor_dominante: "Agent"
    complexity: "média"
    estimated_effort: "1-2 sessões"
    status: "pending"

  - id: "SOP-PB-UNIV-02"
    name: "Classificação de Lead Inbound"
    type: "burro"
    priority: "P1"
    score: 75
    executor_dominante: "Worker"
    complexity: "baixa"
    estimated_effort: "1 sessão"
    status: "pending"
  # ...
```

### Fase 7: Relatório Executivo

Gerar relatório consolidado com visão geral cross-business.

**Substeps:**
- [ ] Compilar totais: categorias, businesses processados, processos core, processos burros
- [ ] Gerar tabela de priorização top-20 (cross-business)
- [ ] Incluir recomendações de próximos passos por categoria
- [ ] Salvar em `workspace/businesses/_reports/sop-backlog-report.md`

## Acceptance Criteria

- [ ] **AC-01:** Todos os businesses do workspace foram inventariados (100% cobertura)
- [ ] **AC-02:** Cada business está atribuído a pelo menos uma categoria
- [ ] **AC-03:** Pelo menos 8 categorias mapeadas com processos core e burros
- [ ] **AC-04:** Cada categoria tem pelo menos 3 processos core identificados
- [ ] **AC-05:** `sop-research-context.yaml` gerado para cada business com dados suficientes
- [ ] **AC-06:** `sop-backlog.yaml` gerado para cada business com pelo menos 5 SOPs priorizados
- [ ] **AC-07:** category-map.yaml em `squads/aiox-sop/data/`, per-business outputs em `workspace/businesses/{slug}/L1-strategy/`
- [ ] **AC-08:** Relatório consolidado gerado com tabela de priorização top-20

## Quality Gate

```yaml
quality_gate:
  id: "QG-SOP-BACKLOG-001"
  name: "SOP Backlog Completeness Gate"
  placement: "exit"
  type: "hybrid"
  severity: "blocking"

  criteria:
    - check: "business_coverage"
      type: "percentage"
      field: "businesses_with_backlog / total_businesses"
      value: 90
      operator: ">="
      weight: 30

    - check: "category_completeness"
      type: "count"
      field: "categories_with_core_processes"
      value: 8
      operator: ">="
      weight: 25

    - check: "backlog_per_business"
      type: "minimum"
      field: "min_sops_per_business_backlog"
      value: 5
      operator: ">="
      weight: 20

    - check: "research_contexts_generated"
      type: "percentage"
      field: "businesses_with_research_context / total_businesses"
      value: 90
      operator: ">="
      weight: 15

    - check: "output_location"
      type: "boolean"
      field: "category_map_in_squad_data_AND_per_business_in_workspace"
      value: true
      operator: "=="
      weight: 10

  thresholds:
    pass: 80
    review: 60
    fail: 59

  executor:
    type: "hybrid"
    ai_agent: "@sop-chief"
    human_review: "Validar categorização e priorização"

  pass_action:
    - "category-map.yaml publicado em squads/aiox-sop/data/"
    - "Per-business backlog publicado em workspace/businesses/*/L1-strategy/"
    - "sop-chief pode consumir category-map direto + per-business via *workspace-context {slug}"

  fail_action:
    - "Listar businesses sem backlog"
    - "Recomendar diagnóstico C-Level para businesses incompletos"
```

## Dependencies

### Depends On (Upstream)

- `load-workspace-context` - Load Workspace Context
  - Required output: Business profiles carregados em memória

### Required By (Downstream)

- `create-sop-human` - Create Human-Readable SOP
  - Uses output: sop-research-context.yaml do business como input para criação
- `create-sop-ml` - Create AI/ML-Readable SOP
  - Uses output: sop-backlog.yaml do business define quais SOPs criar primeiro
- `create-sop-operations-suite` - Create Operations SOP Suite
  - Uses output: sop-backlog.yaml identifica quais operations YAMLs processar

## Handoff

| Attribute | Value |
|-----------|-------|
| **Next Task** | `create-sop-human` ou `create-sop-ml` (conforme priorização do backlog) |
| **Trigger** | Backlog aprovado pelo usuário |
| **Executor** | @sop-chief (routing) → @sop-creator ou @sop-ml-architect |

### Handoff Checklist

Before handoff, verify:
- [ ] sop-backlog.yaml válido em cada business processado
- [ ] sop-research-context.yaml com categoria e processos core
- [ ] Relatório consolidado revisado
- [ ] Usuário aprovou priorização P0

### Handoff Package

Squad knowledge base (estático):
- **category-map.yaml**: `squads/aiox-sop/data/` - Mapeamento categorias → SOPs mínimas por tipo de negócio

Per-business (dinâmico):
- **sop-research-context.yaml**: `workspace/businesses/{slug}/L1-strategy/` - Categoria, processos core, processos burros, research gaps
- **sop-backlog.yaml**: `workspace/businesses/{slug}/L1-strategy/` - Backlog priorizado de SOPs a criar

Cross-business:
- **sop-backlog-report.md**: `workspace/businesses/_reports/` - Relatório executivo consolidado

## Error Handling

### Business sem company-dna.yaml

- **Trigger:** Diretório existe mas não tem company-dna.yaml
- **Detection:** FileNotFound ao tentar ler
- **Recovery:** Marcar business como "incomplete" e prosseguir. Listar no relatório como gap.
- **Prevention:** Rodar inventário de completude antes

### Categoria com business único

- **Trigger:** Categoria tem apenas 1 business
- **Detection:** Contagem de businesses por categoria == 1
- **Recovery:** Marcar processos como "single-source evidence" (confiança BAIXA). Pesquisa web para validar se são padrão da indústria.
- **Prevention:** Consolidar categorias muito granulares

### Dados insuficientes para processo core

- **Trigger:** Processo identificado mas sem evidência nos profiles
- **Detection:** Campos pain_points/bottlenecks vazios ou genéricos
- **Recovery:** Marcar como P3 e incluir em `research_gaps`
- **Prevention:** Enrichment via structured interview ou web research

## Integration

- **C-Level Squad:** Diagnóstico de operations alimenta esta task. `*diagnose-business` identifica gaps operacionais que viram SOPs. COO lê sop-backlog.yaml nos diagnósticos.
- **SOP Chief:** Lê `workspace/businesses/{slug}/L1-strategy/sop-research-context.yaml` para saber quais SOPs básicas cada business precisa. Fonte primária de análise.
- **SOP Operations Suite:** Task `create-sop-operations-suite` consome sop-backlog.yaml para gerar SOPs a partir de YAMLs de operations.
- **Imersão AIOX:** Os 17 businesses da imersão são o dataset primário. Cada CEO vê seu próprio backlog em seu workspace.

## Examples

### Exemplo 1: Execução completa

```bash
# Ativar sop-chief
@sop-chief

# Executar mapeamento
*map-core-sop-backlog

# Output esperado:
# 35 businesses inventariados
# 10 categorias mapeadas
# 47 processos core identificados
# 10 processos burros universais
# 1 category-map.yaml em squads/aiox-sop/data/ (knowledge base do squad)
# 35 sop-research-context.yaml em workspace/businesses/*/L1-strategy/
# 35 sop-backlog.yaml em workspace/businesses/*/L1-strategy/
# Relatório consolidado em workspace/businesses/_reports/sop-backlog-report.md
```

### Exemplo 2: Output per-business (Brasil em Dobro)

```yaml
# workspace/businesses/brasil_em_dobro/L1-strategy/sop-research-context.yaml
business:
  slug: "brasil_em_dobro"
  name: "Brasil em Dobro"
  primary_category:
    id: "CAT-07"
    name: "Turismo / Gastronomia"
    slug: "tourism-gastronomy"

core_processes:
  - id: "PC-07-01"
    name: "Onboarding de estabelecimento parceiro"
    why_core: "Crescimento do marketplace depende de volume de parceiros"
    executor_mix:
      human: "30%"
      agent: "40%"
      worker: "20%"
      hybrid: "10%"
    complexity: "média"
    sop_priority: "P0"
```

### Exemplo 3: Backlog per-business (Eu Médico Residente)

```yaml
# workspace/businesses/eu_medico_residente/L1-strategy/sop-backlog.yaml
business:
  slug: "eu_medico_residente"
  name: "Eu Médico Residente"
  generated_at: "2026-03-18"
  total_sops: 8

backlog:
  - id: "SOP-PC-01-02"
    name: "Onboarding de Aluno Premium"
    type: "core"
    priority: "P0"
    score: 92

  - id: "SOP-PC-06-03"
    name: "Atendimento Clínico / Triagem"
    type: "core"
    priority: "P0"
    score: 88

  - id: "SOP-PB-UNIV-09"
    name: "Triagem de Suporte Nível 1"
    type: "burro"
    priority: "P1"
    score: 72
```

## Notes

- **Separação squad vs workspace:** `category-map.yaml` é knowledge base estática do squad em `squads/aiox-sop/data/` (genérico por indústria, raramente muda). Outputs per-business vivem em `workspace/businesses/{slug}/L1-strategy/` (específicos, dinâmicos). O sop-chief consome ambos via seus read_paths declarados no config.yaml.
- **Enrichment opcional:** Se web research estiver disponível (Firecrawl, EXA), usar para validar processos core contra benchmarks da indústria. Sem research, usar apenas dados do workspace.
- **Evolução incremental:** O backlog é vivo. Conforme businesses preenchem mais dados, re-executar para atualizar.
- **Conexão com Ciclo 2:** Esta task operacionaliza o conceito de "processos burros vs core" apresentado no Ciclo 2 da Imersão AIOX (Pedro Valério). Os CEOs veem seu próprio backlog no workspace.

## Validation Checklist (HO-TP-001)

### Mandatory Fields Check

- [x] `task_name` follows "Verb + Object" format
- [x] `status` is one of: pending | in_progress | completed
- [x] `responsible_executor` is clearly specified
- [x] `execution_type` is one of: Human | Agent | Hybrid | Worker
- [x] `input` array has at least 1 item
- [x] `output` array has at least 1 item
- [x] `action_items` has clear, actionable steps
- [x] `acceptance_criteria` has measurable criteria

### Quality Check

- [x] Task is atomic (single responsibility)
- [x] Inputs are well-defined with types
- [x] Outputs match acceptance criteria
- [x] Action items are sequential and clear
- [x] Executor type matches task nature
- [x] Handoff is specified (if not terminal)

---

_Task Version: 1.1.0_
_Pattern: HO-TP-001 (Task Anatomy Standard)_
_Last Updated: 2026-03-18_
_Compliant: Yes_
