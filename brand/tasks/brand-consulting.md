---
version: "1.0"
date: "2026-02-28"
author:
  agent: "claude-code"
  squad: "brand"
---

# Brand Consulting — Consultoria & Roteamento de Especialistas

## Task Definition

| Field | Value |
|-------|-------|
| **ID** | BR_CONSULT_001 |
| **task_name** | Brand Consulting |
| **status** | pending |
| **responsible_executor** | brand-chief |
| **execution_type** | Agent |
| **complexity** | medium |
| **estimated_time** | 15-30min (triagem) + tempo do especialista |

## Descricao

Task de entrada do Brand Squad. O brand-chief atua como triagem: entende a necessidade do usuario, classifica o tipo de demanda e roteia para o especialista mais adequado. Combina consultoria interativa (modo consulting) com auditoria sistematica (modo audit).

## Pre-requisitos

- Nenhum (task de entrada)
- Contexto do negocio coletado durante a conversa

## Input

```yaml
brand_consulting_input:
  user_request: "" # Descricao livre da necessidade
  business_context:
    name: ""
    industry: ""
    stage: "" # startup, growth, established, rebrand
    existing_brand: false
  mode: "" # consulting | audit | auto-detect
```

## Output

```yaml
brand_consulting_output:
  classification:
    demand_type: "" # site, landing, posicionamento, equity, messaging, identidade, brand-book, storytelling, estrategia
    confidence: 0.0
    route_id: ""
  routing:
    primary_agent: ""
    secondary_agents: []
    task_to_execute: ""
  diagnosis_summary: "" # Se modo audit
```

## Routing Matrix

Tabela de roteamento baseada no tipo de demanda detectada:

| ID | Demanda | Agente Primario | Agente Suporte | Task |
|----|---------|-----------------|----------------|------|
| RT_001 | Site/Homepage | storybrand-narrator | wheeler-brand-design | wireframe-brandscript |
| RT_002 | Landing Page | storybrand-narrator | wheeler-brand-design | landing-page-brandscript |
| RT_004 | Posicionamento | neumeier-differentiation | aaker-brand-identity | brand-positioning |
| RT_005 | Brand Equity | aaker-brand-identity | neumeier-differentiation | brand-equity-audit |
| RT_006 | Mensagem/Copy | storybrand-narrator | — | brand-messaging |
| RT_007 | Identidade Visual | wheeler-brand-design | storybrand-narrator | brand-identity |
| RT_010 | Brand Book | wheeler-brand-design | storybrand-narrator | brand-book |
| RT_012 | Storytelling | storybrand-narrator | — | brand-storytelling |
| RT_013 | Estrategia de Conteudo | brand-strategist | storybrand-narrator | content-strategy |

## Action Items

### 1. Coleta de Contexto

Entender a necessidade do usuario:
- Qual o objetivo principal? (criar marca, melhorar, auditar)
- Ja tem marca existente? (nome, logo, cores, messaging)
- Qual o estagio do negocio? (startup, growth, established)
- Qual o publico-alvo?
- Quais os concorrentes principais?

### 2. Classificacao da Demanda

Analisar a solicitacao e classificar:
- Mapear para um dos tipos da routing matrix
- Avaliar confianca da classificacao
- Se ambiguo, apresentar opcoes ao usuario

### 3. Roteamento

Direcionar para o especialista correto:
- Selecionar agente primario e suporte
- Passar contexto coletado via handoff
- Definir task a ser executada

### 4. Modo Audit (se aplicavel)

Se o usuario quer uma auditoria:
- Coletar todos os assets existentes
- Aplicar scoring por dimensao (posicionamento, messaging, visual, consistencia)
- Gerar diagnostico com gaps e recomendacoes
- Priorizar acoes por impacto

### 5. Modo Consulting (se aplicavel)

Se o usuario quer consultoria interativa:
- Entender o problema especifico
- Fazer perguntas de elicitation
- Propor abordagem
- Rotear para especialista quando o problema estiver claro

## Specialist Profiles

### storybrand-narrator (Donald Miller)
- **Especialidade:** BrandScript, messaging, storytelling, sites/landing pages
- **Quando usar:** Comunicacao, clareza de mensagem, narrativa da marca
- **Framework:** StoryBrand SB7

### wheeler-brand-design (Alina Wheeler)
- **Especialidade:** Identidade visual, brand book, design system
- **Quando usar:** Logo, cores, tipografia, guidelines visuais
- **Framework:** Designing Brand Identity (5 fases)

### neumeier-differentiation (Marty Neumeier)
- **Especialidade:** Diferenciacao, posicionamento, brand gap
- **Quando usar:** Estrategia de marca, Onlyness Statement, Zag
- **Framework:** Brand Gap, Zag, The Brand Flip

### aaker-brand-identity (David Aaker)
- **Especialidade:** Brand equity, arquitetura de marca, extensoes
- **Quando usar:** Portfolio de marcas, equity audit, brand valuation
- **Framework:** Aaker Model, Brand Identity Prism

### brand-strategist (Ana Couto)
- **Especialidade:** Estrategia de marca para mercado BR, proposito
- **Quando usar:** Marca com foco no mercado brasileiro, estrategia de conteudo
- **Framework:** Branding estrategico, proposito de marca

## Acceptance Criteria

```yaml
acceptance_criteria:
  - "Contexto do negocio coletado (nome, industria, estagio)"
  - "Demanda classificada com confianca >= 0.7"
  - "Agente primario selecionado da routing matrix"
  - "Handoff context preparado para o especialista"
  - "Usuario informado sobre qual especialista e por que"
  - "Se audit: scoring por dimensao gerado"
  - "Se consulting: problema claro antes de rotear"
```

## Veto Conditions

```yaml
veto_conditions:
  - "Rotear sem entender a demanda = PROIBIDO"
  - "Rotear para agente errado = RECLASSIFICAR"
  - "Pular coleta de contexto = PROIBIDO"
  - "Audit sem scoring numerico = INCOMPLETO"
  - "Consulting sem elicitation = SUPERFICIAL"
```

## Handoff

| Direcao | Agent | Condicao |
|---------|-------|----------|
| **To** | storybrand-narrator | Demanda de messaging, site, storytelling |
| **To** | wheeler-brand-design | Demanda de identidade visual, brand book |
| **To** | neumeier-differentiation | Demanda de posicionamento, diferenciacao |
| **To** | aaker-brand-identity | Demanda de brand equity, portfolio |
| **To** | brand-strategist | Demanda de estrategia BR, conteudo |

## Error Handling

| Erro | Acao |
|------|------|
| Demanda nao classificavel | Apresentar opcoes ao usuario para escolha |
| Multiplas demandas simultaneas | Priorizar por impacto; sugerir sequencia |
| Contexto insuficiente | Fazer perguntas adicionais de elicitation |
| Especialista nao disponivel | Sugerir alternativa mais proxima |
| Usuario quer tudo de uma vez | Recomendar workflow completo (wf-brand-complete) |

---
*Task: BR_CONSULT_001 | Agent: brand-chief → specialist | Version: 1.0*
