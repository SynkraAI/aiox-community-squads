# Framework de Clones - Data Intelligence Pack
## 06 - Matriz de Decisão

---

## SELEÇÃO RÁPIDA POR PERGUNTA

### Perguntas Estratégicas (Tier 1)

| Pergunta | Clone | Por quê |
|----------|-------|---------|
| "Quem são nossos melhores clientes?" | **Peter Fader** | CLV e segmentação por valor |
| "Quanto vale cada cliente?" | **Peter Fader** | Cálculo e projeção de CLV |
| "Qual segmento devemos priorizar?" | **Peter Fader** | Customer Centricity |
| "Nosso programa de indicação funciona?" | **Sean Ellis** | Viral coefficient |
| "Temos Product-Market Fit?" | **Sean Ellis** | Sean Ellis Test |
| "Qual deve ser nossa North Star Metric?" | **Sean Ellis** | North Star framework |
| "Que experimento priorizar?" | **Sean Ellis** | ICE framework |

### Perguntas Operacionais (Tier 2)

| Pergunta | Clone | Por quê |
|----------|-------|---------|
| "Quem está em risco de churn?" | **Nick Mehta** | Health Score + signals |
| "Que ação tomar com cliente X?" | **Nick Mehta** | Playbooks de CS |
| "Como estruturar Health Score?" | **Nick Mehta** | DEAR framework |
| "Nossa comunidade está saudável?" | **David Spinks** | SPACES + community metrics |
| "Por que membros não participam?" | **David Spinks** | Community diagnostics |
| "Qual o ROI da comunidade?" | **David Spinks** | Community ROI framework |
| "Por que completion rate é baixo?" | **Wes Kao** | CBC design principles |
| "Como redesenhar curso para engajar?" | **Wes Kao** | Course Mechanics Canvas |
| "Que métricas de learning usar?" | **Wes Kao** | Learning outcomes |

### Perguntas de Comunicação (Tier 3)

| Pergunta | Clone | Por quê |
|----------|-------|---------|
| "Qual fonte traz mais clientes?" | **Avinash Kaushik** | Attribution models |
| "Como apresentar para o CEO?" | **Avinash Kaushik** | So What framework |
| "Que métricas reportar?" | **Avinash Kaushik** | DMMM |
| "Esse relatório gera ação?" | **Avinash Kaushik** | Report structure |

---

## SELEÇÃO POR FUNCIONALIDADE DO PRD

### v_customer_360

```
PRIMÁRIO:   Peter Fader (quem importa, segmentação por valor)
SECUNDÁRIO: Nick Mehta (Health Score components)
TERCIÁRIO:  Avinash Kaushik (como apresentar a visão 360)
```

### Health Score

```
PRIMÁRIO:   Nick Mehta (DEAR framework, componentes, pesos)
SECUNDÁRIO: Peter Fader (validar que RFM está correto)
TERCIÁRIO:  David Spinks (adicionar community health se relevante)
```

### churn_alerts

```
PRIMÁRIO:   Nick Mehta (tipos de alerta, severidade, ações)
SECUNDÁRIO: David Spinks (alertas específicos de community drop)
TERCIÁRIO:  Wes Kao (alertas de learning stall)
```

### v_attribution_funnel

```
PRIMÁRIO:   Avinash Kaushik (modelos, interpretação)
SECUNDÁRIO: Peter Fader (attribution por CLV do adquirido)
TERCIÁRIO:  Sean Ellis (attribution de referral)
```

### v_cohort_analysis

```
PRIMÁRIO:   Peter Fader (cohort por valor)
SECUNDÁRIO: Sean Ellis (cohort por viralidade)
TERCIÁRIO:  Wes Kao (cohort por learning outcomes)
```

### Community Metrics (se adicionado)

```
PRIMÁRIO:   David Spinks (SPACES, MAU/DAU, stickiness)
SECUNDÁRIO: Nick Mehta (adaptar health para community)
TERCIÁRIO:  Avinash Kaushik (ROI reporting)
```

### Learning Outcomes (se adicionado)

```
PRIMÁRIO:   Wes Kao (completion, engagement, outcomes)
SECUNDÁRIO: Nick Mehta (student health score)
TERCIÁRIO:  Avinash Kaushik (learning ROI reporting)
```

---

## SELEÇÃO POR STAKEHOLDER

### Para CEO/Founder

```
CLONE PRIMÁRIO: Avinash Kaushik
├── So What framework (ação clara)
├── DMMM (ligação com business objectives)
└── Comunicação executiva

SUPORTE: Peter Fader (CLV strategy)
```

### Para CS Team

```
CLONE PRIMÁRIO: Nick Mehta
├── Playbooks acionáveis
├── Health Score para priorização
└── Churn alerts para ação imediata

SUPORTE: David Spinks (community engagement)
```

### Para Marketing

```
CLONE PRIMÁRIO: Avinash Kaushik
├── Attribution models
├── See-Think-Do-Care
└── Campaign ROI

SUPORTE: Sean Ellis (referral optimization)
```

### Para Finance

```
CLONE PRIMÁRIO: Peter Fader
├── CLV calculations
├── Unit economics
└── Customer segmentation por valor

SUPORTE: Avinash Kaushik (reporting)
```

### Para Product/Education

```
CLONE PRIMÁRIO: Wes Kao
├── Learning outcomes
├── Engagement metrics
└── Course design

SUPORTE: David Spinks (community elements)
```

### Para Community Manager

```
CLONE PRIMÁRIO: David Spinks
├── SPACES model
├── Community health metrics
└── Engagement programs

SUPORTE: Wes Kao (learning in community)
```

---

## MATRIZ DE DECISÃO VISUAL

```
                    ┌─────────────────────────────────────────────────────┐
                    │                    PERGUNTA                          │
                    └─────────────────────────────────────────────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
            ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
            │  ESTRATÉGICA  │      │  OPERACIONAL  │      │  COMUNICAÇÃO  │
            │               │      │               │      │               │
            │ "Quem importa"│      │"Como medir"   │      │"Como mostrar" │
            │ "Como crescer"│      │"Quando alertar│      │"Que ação"     │
            └───────┬───────┘      └───────┬───────┘      └───────┬───────┘
                    │                      │                      │
         ┌──────────┴──────────┐          │                      │
         │                     │          │                      │
         ▼                     ▼          │                      ▼
   ┌──────────┐          ┌──────────┐    │               ┌──────────┐
   │  FADER   │          │  ELLIS   │    │               │ KAUSHIK  │
   │          │          │          │    │               │          │
   │ • CLV    │          │ • Viral  │    │               │ • Attrib │
   │ • RFM    │          │ • North* │    │               │ • Reports│
   │ • Segment│          │ • PMF    │    │               │ • DMMM   │
   └──────────┘          └──────────┘    │               └──────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
        ┌──────────┐              ┌──────────┐              ┌──────────┐
        │  MEHTA   │              │  SPINKS  │              │   KAO    │
        │          │              │          │              │          │
        │ • Health │              │ • SPACES │              │ • CBC    │
        │ • Churn  │              │ • MAU    │              │ • Complet│
        │ • DEAR   │              │ • Commun │              │ • Learn  │
        └──────────┘              └──────────┘              └──────────┘
             │                         │                         │
             │    DOMÍNIO:             │    DOMÍNIO:             │    DOMÍNIO:
             │    SaaS/Produto         │    Comunidade           │    Educação
             │                         │                         │
             └─────────────────────────┴─────────────────────────┘
```

---

## ORDEM RECOMENDADA DE CONSULTA

Para implementação completa do Data Intelligence Pack:

```
FASE 1: FUNDAMENTAÇÃO
│
├── 1. Peter Fader
│   └── Quem são os clientes que importam?
│   └── Como segmentar por valor?
│   └── Quais métricas de CLV/RFM?
│
└── 2. Sean Ellis
    └── Qual é nossa North Star Metric?
    └── Como está nosso viral coefficient?
    └── Temos PMF confirmado?

FASE 2: OPERACIONALIZAÇÃO
│
├── 3. Nick Mehta
│   └── Quais componentes do Health Score?
│   └── Que alertas de churn criar?
│   └── Quais playbooks de ação?
│
├── 4. David Spinks
│   └── Como medir saúde da comunidade?
│   └── Quais métricas de engajamento?
│   └── SPACES se aplica como?
│
└── 5. Wes Kao
    └── Como aumentar completion rate?
    └── Quais métricas de learning?
    └── Que elementos de cohort adicionar?

FASE 3: COMUNICAÇÃO
│
└── 6. Avinash Kaushik
    └── Como estruturar reports?
    └── Qual modelo de attribution?
    └── Como apresentar para liderança?
```

---

## COMBINAÇÕES RECOMENDADAS POR PROJETO

### Projeto: Implementar Customer 360

```
Fader (primário) + Mehta + Kaushik
```

### Projeto: Criar Sistema de Churn Alerts

```
Mehta (primário) + Fader + Spinks/Kao
```

### Projeto: Otimizar Attribution

```
Kaushik (primário) + Fader + Ellis
```

### Projeto: Redesign de Curso (3% → 80% completion)

```
Kao (primário) + Spinks + Mehta
```

### Projeto: Lançar Programa de Referral

```
Ellis (primário) + Fader + Kaushik
```

### Projeto: Melhorar Engajamento de Comunidade

```
Spinks (primário) + Mehta + Kao
```

### Projeto: Dashboard Executivo

```
Kaushik (primário) + Fader + Mehta
```

---

## ANTI-PATTERNS DE SELEÇÃO

### ❌ Erros Comuns

| Erro | Por que está errado | Correção |
|------|---------------------|----------|
| Usar Mehta para estratégia de aquisição | Health Score é retenção, não aquisição | Use Ellis para aquisição |
| Usar Kao para métricas de SaaS genérico | Kao é específico para educação | Use Mehta para SaaS |
| Usar Spinks para curso individual | Spinks é community, não individual | Use Kao para cursos |
| Usar Kaushik para cálculos de CLV | Kaushik é comunicação, não cálculo | Use Fader para CLV |
| Usar Ellis para health score | Ellis é growth, não retention ops | Use Mehta para health |
| Usar Fader para alertas operacionais | Fader é estratégico, não operacional | Use Mehta para alertas |

---

*Framework de Clones - Data Intelligence Pack v2.0*
*Matriz de Decisão*
