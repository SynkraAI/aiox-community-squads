# Framework de Clones - Data Intelligence Pack
## Arquitetura Geral v2.0

---

## PROPÓSITO

Este framework define **6 "clones"** (mentes especializadas) para guiar a implementação do Data Intelligence Squad. Cada clone representa o melhor pensamento mundial em sua área específica.

**Problema que resolve:** Implementar métricas sem saber qual decisão cada uma informa. Dashboards cheios de números sem clareza estratégica.

**Solução:** Consultar o clone certo antes de implementar qualquer métrica ou funcionalidade.

---

## ESTRUTURA DE 3 TIERS

```
┌─────────────────────────────────────────────────────────────┐
│                    TIER 0 - FUNDAMENTAÇÃO                    │
│              "Quem importa e como crescer"                   │
│                                                              │
│   ┌──────────────────┐    ┌──────────────────┐              │
│   │   PETER FADER    │    │   SEAN ELLIS     │              │
│   │   CLV + RFM      │    │  Viral/Referral  │              │
│   │   Wharton        │    │  GrowthHackers   │              │
│   └──────────────────┘    └──────────────────┘              │
│                                                              │
│   Usar ANTES de implementar qualquer métrica                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  TIER 1 - OPERACIONALIZAÇÃO                  │
│              "Como monitorar, medir e alertar"               │
│                                                              │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│   │ NICK MEHTA  │  │DAVID SPINKS │  │   WES KAO   │        │
│   │ Health/Churn│  │  Community  │  │  Learning   │        │
│   │  Gainsight  │  │    CMX      │  │   Maven     │        │
│   └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                              │
│   Usar PARA implementar e monitorar                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   TIER 2 - COMUNICAÇÃO                       │
│              "Como traduzir em ação e apresentar"            │
│                                                              │
│                 ┌──────────────────────┐                     │
│                 │  AVINASH KAUSHIK     │                     │
│                 │ Attribution/Story    │                     │
│                 │    ex-Google         │                     │
│                 └──────────────────────┘                     │
│                                                              │
│   Usar PARA comunicar insights e gerar ação                  │
└─────────────────────────────────────────────────────────────┘
```

---

## REGRA DE OURO

> **Nunca implemente uma métrica sem passar por pelo menos 1 fundamentador.**

Erro comum: Criar dashboard de "Health Score" sem definir primeiro quem são os clientes que importam (Fader) ou como o crescimento deve acontecer (Ellis).

---

## COMO USAR ESTE FRAMEWORK

### Passo 1: Identifique a Funcionalidade
Qual parte do Data Intelligence Pack você está implementando?
- Customer 360
- Health Score
- Churn Alerts
- Attribution
- Cohort Analysis
- Community Metrics
- Learning Outcomes

### Passo 2: Consulte a Matriz de Decisão
Veja o arquivo `06_matriz_decisao.md` para saber qual clone consultar.

### Passo 3: Siga o Workflow
Use os workflows em `07_workflows.md` para implementação estruturada.

### Passo 4: Valide com Cheatsheet
Confira `08_cheatsheet.md` para validação rápida.

---

## CONTEXTO DE APLICAÇÃO

Este framework foi otimizado para:

| Contexto | Característica |
|----------|----------------|
| **Modelo de Negócio** | SaaS, Comunidade, Educação Online |
| **Estágio** | Startup / Scale-up |
| **Aquisição Principal** | Indicações e Referral |
| **Desafio Principal** | Completion rate baixo (3% → meta 96%) |
| **Região** | Brasil (adaptável global) |

---

## ARQUIVOS DO FRAMEWORK

| # | Arquivo | Conteúdo |
|---|---------|----------|
| 01 | arquitetura_geral | Visão geral e estrutura (este arquivo) |
| 02 | tier0_fundacao | Princípios base e anti-patterns |
| 03 | tier0_fundamentadores | **Tier 0:** Peter Fader + Sean Ellis (Foundation) |
| 04 | tier1_operacionalizadores | **Tier 1:** Nick Mehta + David Spinks + Wes Kao (Operations) |
| 05 | tier2_comunicadores | **Tier 2:** Avinash Kaushik (Communication) |
| 06 | matriz_decisao | Quando usar qual clone |
| 07 | workflows | Fluxos completos por funcionalidade |
| 08 | cheatsheet | Resumo rápido de uma página |

---

## VERSIONAMENTO

- **v1.0** - Framework original com 6 clones (Fader, Davenport, Mehta, Novo, Murphy, Kaushik)
- **v2.0** - Framework revisado para contexto startup/educação/comunidade
  - Substituiu Tom Davenport → Sean Ellis (referral focus)
  - Substituiu Jim Novo → David Spinks (community metrics)
  - Substituiu Lincoln Murphy → Wes Kao (learning outcomes)

---

*Framework de Clones - Data Intelligence Pack v2.0*
*Criado para Academia Lendár[IA]*
