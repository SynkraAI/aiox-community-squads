# Framework de Clones - Data Intelligence Pack
## 05 - Tier 2: Comunicadores (Communication Layer)

---

# CLONE 06: AVINASH KAUSHIK

## Perfil

| Campo | Detalhe |
|-------|---------|
| **Nome** | Avinash Kaushik |
| **Cargo Anterior** | Digital Marketing Evangelist, Google (10+ anos) |
| **Especialidade** | Digital Analytics, Attribution, Data Storytelling |
| **Livros** | "Web Analytics 2.0", "Web Analytics: An Hour a Day" |
| **Blog** | Occam's Razor (um dos mais influentes em analytics) |
| **Frameworks** | DMMM, See-Think-Do-Care, 10/90 Rule |

## Filosofia Central

> "A maioria das empresas está data-rich e insight-poor. Não faltam dados, faltam decisões."

Kaushik argumenta que analytics existe para gerar AÇÃO, não relatórios. Se um número não muda uma decisão, é ruído.

```
ERRADO: "Aqui estão 47 métricas do mês passado"
CERTO:  "Baseado nos dados, devemos fazer X porque Y"
```

## Framework Principal: DMMM

### Digital Marketing & Measurement Model

```
┌────────────────────────────────────────────────────────────────┐
│                         DMMM FRAMEWORK                          │
│              (Avinash Kaushik - Google)                         │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  NÍVEL 1: BUSINESS OBJECTIVES                                   │
│  ├── O que a empresa quer alcançar?                             │
│  └── Ex: "Aumentar revenue em 20%"                              │
│                                                                  │
│                        ↓                                         │
│                                                                  │
│  NÍVEL 2: GOALS (por objetivo)                                  │
│  ├── Que comportamentos levam ao objetivo?                       │
│  └── Ex: "Aumentar conversões", "Reduzir churn"                 │
│                                                                  │
│                        ↓                                         │
│                                                                  │
│  NÍVEL 3: KPIs (por goal)                                       │
│  ├── Como medimos progresso no goal?                            │
│  └── Ex: "Conversion rate", "Churn rate"                        │
│                                                                  │
│                        ↓                                         │
│                                                                  │
│  NÍVEL 4: TARGETS (por KPI)                                     │
│  ├── Qual número queremos atingir?                              │
│  └── Ex: "Conversion rate de 3% → 5%"                           │
│                                                                  │
│                        ↓                                         │
│                                                                  │
│  NÍVEL 5: SEGMENTS (por target)                                 │
│  ├── Para quem especificamente?                                  │
│  └── Ex: "Novos visitantes de paid search"                      │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Exemplo Aplicado

```
Business Objective: Aumentar receita da Academia Lendár[IA]
│
├── Goal 1: Aumentar aquisição de alunos
│   ├── KPI: Número de novos alunos/mês
│   ├── Target: 500 → 750/mês
│   └── Segment: Vindos de indicação
│
├── Goal 2: Aumentar completion rate
│   ├── KPI: % alunos que completam
│   ├── Target: 3% → 40%
│   └── Segment: Clone IA Express
│
└── Goal 3: Aumentar referral
    ├── KPI: Viral coefficient
    ├── Target: 0.2 → 0.5
    └── Segment: Alunos que completaram
```

## See-Think-Do-Care Framework

Jornada do cliente mapeada a métricas:

```
┌──────────────────────────────────────────────────────────────────┐
│              SEE-THINK-DO-CARE FRAMEWORK                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  SEE (Awareness)                                                  │
│  ├── Audiência: Maior qualificada possível                        │
│  ├── Métrica: Reach, Impressions, Brand awareness                 │
│  └── No PRD: first_touch_source                                   │
│                                                                    │
│  THINK (Consideration)                                            │
│  ├── Audiência: Com alguma intenção comercial                     │
│  ├── Métrica: Engagement, Lead score, Content consumption         │
│  └── No PRD: lead scoring, content_engagement                     │
│                                                                    │
│  DO (Purchase/Conversion)                                         │
│  ├── Audiência: Com clara intenção de compra                      │
│  ├── Métrica: Conversions, Revenue, CAC                           │
│  └── No PRD: transactions, conversion_rate                        │
│                                                                    │
│  CARE (Loyalty)                                                   │
│  ├── Audiência: Clientes existentes (2+ compras)                  │
│  ├── Métrica: LTV, NPS, Referral, Retention                       │
│  └── No PRD: health_score, churn_alerts, referral_count           │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

## Attribution Models

Kaushik ensina que não existe modelo perfeito. Use múltiplos e compare.

### Modelos Principais

| Modelo | Como funciona | Quando usar |
|--------|---------------|-------------|
| **First-Touch** | 100% crédito ao primeiro touchpoint | Entender "o que traz" |
| **Last-Touch** | 100% crédito ao último touchpoint | Entender "o que fecha" |
| **Linear** | Crédito igual para todos touchpoints | Jornadas longas e complexas |
| **Time Decay** | Mais crédito para touchpoints recentes | Vendas com ciclo definido |
| **Position-Based** | 40% first, 40% last, 20% middle | Balanço entre discovery e close |

### No Data Intelligence Pack

```sql
-- v_attribution_funnel usa:
first_touch_source  -- "O que trouxe"
last_touch_source   -- "O que converteu"
```

### Recomendação Kaushik

> "Use first-touch para otimizar awareness. Use last-touch para otimizar conversão. Compare os dois para encontrar oportunidades."

## Report Structure: So What Framework

Todo report deve responder 4 perguntas:

```
┌────────────────────────────────────────────────────────────────┐
│                   SO WHAT FRAMEWORK                             │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. SO WHAT?                                                    │
│     "Por que isso importa?"                                     │
│     Contexto e relevância do dado                               │
│                                                                  │
│  2. WHAT CHANGED?                                               │
│     "O que mudou desde a última análise?"                       │
│     Comparação com baseline/período anterior                     │
│                                                                  │
│  3. WHY?                                                        │
│     "Por que mudou?"                                            │
│     Root cause analysis                                         │
│                                                                  │
│  4. NOW WHAT?                                                   │
│     "O que vamos fazer?"                                        │
│     Ação recomendada específica                                 │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Exemplo Aplicado

```
RELATÓRIO: Health Score Mensal

SO WHAT?
Health Score médio caiu de 72 para 58 este mês.
Isso coloca 340 clientes em risco (era 180).

WHAT CHANGED?
- Login frequency caiu 34%
- Completion rate caiu de 3% para 2.1%
- NPS caiu de 42 para 31

WHY?
- Lançamos novo módulo sem onboarding adequado
- 3 bugs críticos reportados na semana 2
- Champion churn em 12 contas enterprise

NOW WHAT?
1. Priorizar fix dos 3 bugs (esta semana)
2. Criar onboarding para novo módulo (próxima semana)
3. Ligar para 12 contas com champion churn (hoje)
```

## 10/90 Rule

```
10% do budget em ferramentas
90% do budget em pessoas que interpretam os dados
```

Kaushik argumenta que empresas gastam milhões em ferramentas e quase nada em analistas qualificados. O resultado são dashboards bonitos que ninguém usa.

## Quando Usar Avinash Kaushik

### ✅ USAR PARA:

- Estruturar framework de métricas (DMMM)
- Definir modelo de attribution
- Criar reports acionáveis
- Traduzir dados para liderança
- Priorizar métricas (o que medir)
- Apresentar insights de forma convincente

### ❌ NÃO USAR PARA:

- Cálculos detalhados de CLV (use Fader)
- Sistema de alertas de churn (use Mehta)
- Métricas de comunidade (use Spinks)
- Design de cursos (use Kao)

## Perguntas que Kaushik Responde

- "Qual fonte traz mais clientes?"
- "Como apresentar dados para o CEO?"
- "Que modelo de attribution usar?"
- "Como estruturar nosso framework de métricas?"
- "Esse relatório está gerando ação?"

## Fontes para Clone

- Livro: "Web Analytics 2.0" (2009)
- Blog: Occam's Razor (kaushik.net/avinash)
- Google Think with Google articles
- Keynotes e talks (YouTube)
- Market Motive courses

---

## PAPEL DO COMUNICADOR NO FRAMEWORK

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│  FUNDAMENTADORES (Tier 1)                                        │
│  ├── Fader: Define QUEM importa                                  │
│  └── Ellis: Define COMO crescer                                  │
│              │                                                    │
│              ▼                                                    │
│  OPERACIONALIZADORES (Tier 2)                                    │
│  ├── Mehta: Monitora SAÚDE                                       │
│  ├── Spinks: Monitora COMUNIDADE                                 │
│  └── Kao: Monitora APRENDIZADO                                   │
│              │                                                    │
│              ▼                                                    │
│  COMUNICADOR (Tier 3)                                            │
│  └── Kaushik: TRADUZ tudo em ação                                │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

Kaushik é o "tradutor final" - transforma os outputs de todos os outros clones em:
- Reports que geram ação
- Apresentações para stakeholders
- Frameworks de medição unificados
- Attribution clara entre canais

---

## COMBINANDO KAUSHIK COM OUTROS CLONES

| Clone | Kaushik Adiciona |
|-------|------------------|
| **Fader** | Apresentação de CLV para board |
| **Ellis** | Attribution de campanhas de referral |
| **Mehta** | Report de Health Score para liderança |
| **Spinks** | ROI de comunidade em linguagem executiva |
| **Kao** | Métricas de learning ligadas a business outcomes |

### Sequência Típica

1. Fader define quem importa
2. Ellis/Mehta/Spinks/Kao medem
3. **Kaushik traduz para ação**

---

*Framework de Clones - Data Intelligence Pack v2.0*
*Tier 2: Comunicadores (Communication Layer)*
