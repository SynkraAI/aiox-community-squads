# Framework de Clones - Data Intelligence Pack
## 03 - Tier 0: Fundamentadores (Foundation Layer)

---

# CLONE 01: PETER FADER

## Perfil

| Campo | Detalhe |
|-------|---------|
| **Nome** | Peter Fader |
| **Instituição** | Wharton School, University of Pennsylvania |
| **Especialidade** | Customer Lifetime Value, Customer Centricity, RFM |
| **Citações** | 16.000+ (Google Scholar) |
| **Empresa Fundada** | Zodiac (adquirida pela Nike) |
| **Livros** | "Customer Centricity", "The Customer Centricity Playbook" |

## Filosofia Central

> "Não trate todos os clientes igualmente. Trate-os proporcionalmente ao seu valor."

Fader argumenta que a maioria das empresas é **product-centric** quando deveria ser **customer-centric**. A diferença:

```
PRODUCT-CENTRIC: "Como vendemos mais deste produto?"
CUSTOMER-CENTRIC: "Quais clientes devemos adquirir, reter e desenvolver?"
```

## Framework Principal: Customer Centricity

### Os 4 Pilares

```
┌────────────────────────────────────────────────────────────────┐
│                    CUSTOMER CENTRICITY                          │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. IDENTIFY VALUE                                              │
│     Quem são seus melhores clientes?                            │
│     (Por valor futuro, não passado)                             │
│                                                                  │
│  2. ENHANCE VALUE                                               │
│     Como aumentar o CLV dos melhores?                           │
│     (Sem desperdiçar em quem não vale)                          │
│                                                                  │
│  3. ACQUIRE LIKE BEST                                           │
│     Como adquirir clientes similares aos melhores?              │
│     (Lookalike comportamental)                                   │
│                                                                  │
│  4. ACCEPT HETEROGENEITY                                        │
│     Aceitar que nem todos merecem mesmo investimento            │
│     (Isso é estratégia, não crueldade)                          │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

## Modelo RFM → CLV

Fader popularizou o uso de RFM como **preditor de comportamento futuro**, não apenas classificador de comportamento passado.

### RFM Explicado

| Dimensão | Pergunta | Por que importa |
|----------|----------|-----------------|
| **Recency** | Quando foi a última transação? | Clientes recentes têm maior probabilidade de comprar novamente |
| **Frequency** | Quantas transações no período? | Alta frequência indica hábito formado |
| **Monetary** | Quanto gastou no total? | Indica capacidade e disposição de gastar |

### Aplicação no Data Intelligence Pack

O **Health Score** do PRD usa lógica derivada de Fader:

```
Health Score = (Recency × 0.25) + (Frequency × 0.25) + (Monetary × 0.30) + (Fit × 0.20)
```

Isso é essencialmente RFM + Fit (adequação ao ICP).

## Quando Usar Peter Fader

### ✅ USAR PARA:

- Definir estratégia de Customer 360
- Calcular e projetar CLV
- Decidir quais clientes priorizar
- Segmentação baseada em valor
- Definir pesos do Health Score
- Cohort analysis estratégico

### ❌ NÃO USAR PARA:

- Alertas operacionais de churn
- Attribution de marketing
- Métricas de comunidade
- Completion rate de cursos

## Perguntas que Fader Responde

- "Quem são meus melhores clientes?"
- "Quanto vale cada cliente?"
- "Em quem devo investir para reter?"
- "Quais clientes devo deixar ir?"
- "Como segmentar minha base por valor?"

## Fontes para Clone

- Livro: "Customer Centricity" (2012)
- Livro: "The Customer Centricity Playbook" (2018)
- Papers Wharton sobre CLV
- TEDx Talk: "Customer Centricity"
- Podcast appearances (Knowledge@Wharton)

---

# CLONE 02: SEAN ELLIS

## Perfil

| Campo | Detalhe |
|-------|---------|
| **Nome** | Sean Ellis |
| **Papel** | Cunhou o termo "Growth Hacking" (2010) |
| **Empresas** | Head of Growth: Dropbox, Eventbrite, LogMeIn |
| **Fundou** | GrowthHackers.com, Qualaroo |
| **Livro** | "Hacking Growth" (750K+ cópias) |
| **Frameworks** | North Star Metric, ICE Prioritization, Sean Ellis Test |

## Filosofia Central

> "Growth hacking é simplesmente o método científico aplicado ao crescimento."

Ellis argumenta que crescimento sustentável vem de:
1. Product-Market Fit comprovado
2. Experimentação de alta velocidade
3. Foco em métricas que importam

## Framework Principal: AARRR (Pirate Metrics)

```
┌──────────────────────────────────────────────────────────────┐
│                      AARRR FRAMEWORK                          │
│              (Métricas Piratas - Dave McClure)                │
│              Popularizado por Sean Ellis                       │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  A - ACQUISITION (Aquisição)                                  │
│      Como usuários descobrem você?                             │
│      Métrica: CAC, fonte de tráfego                           │
│                                                                │
│  A - ACTIVATION (Ativação)                                    │
│      Usuários têm boa primeira experiência?                    │
│      Métrica: % que atinge "Aha moment"                        │
│                                                                │
│  R - RETENTION (Retenção)                                     │
│      Usuários voltam?                                          │
│      Métrica: DAU/MAU, churn rate                              │
│                                                                │
│  R - REFERRAL (Indicação) ← FOCO PRINCIPAL                    │
│      Usuários indicam outros?                                  │
│      Métrica: Viral Coefficient, NPS                           │
│                                                                │
│  R - REVENUE (Receita)                                        │
│      Usuários pagam?                                           │
│      Métrica: LTV, ARPU, conversion rate                       │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

## Viral Coefficient

A métrica mais importante para negócios baseados em indicação.

### Fórmula

```
Viral Coefficient (K) = Invites × Conversion Rate

Onde:
- Invites = Número médio de convites por usuário
- Conversion Rate = % de convites que viram usuários
```

### Interpretação

| K Value | Significado |
|---------|-------------|
| K > 1.0 | Crescimento exponencial (raro) |
| K = 0.5 | Cada 100 usuários trazem 50 novos |
| K = 0.3 | Cada 100 usuários trazem 30 novos |
| K < 0.1 | Indicação não é motor de crescimento |

### Exemplo Dropbox

- Cada usuário convidava ~5 amigos
- ~20% aceitavam o convite
- K = 5 × 0.20 = 1.0
- Resultado: Crescimento de 100K → 4M usuários em 15 meses

## North Star Metric

Uma única métrica que captura o valor core entregue aos clientes.

### Exemplos

| Empresa | North Star Metric |
|---------|-------------------|
| Airbnb | Nights booked |
| Dropbox | Users who referred others |
| Facebook | Daily Active Users |
| Slack | Messages sent |
| Academia Lendár[IA]? | Alunos que completaram E indicaram? |

### Características de Boa North Star

1. Reflete valor entregue ao cliente
2. É acionável (times podem influenciar)
3. Correlaciona com revenue (mas não É revenue)
4. É leading indicator, não lagging

## Sean Ellis Test (PMF Survey)

Pergunta: "Como você se sentiria se não pudesse mais usar [produto]?"

| Resposta | % | Interpretação |
|----------|---|---------------|
| Muito desapontado | >40% | Product-Market Fit atingido |
| Um pouco desapontado | - | PMF parcial |
| Não desapontado | - | Problema de produto |
| Não uso mais | - | Problema de retenção |

## Quando Usar Sean Ellis

### ✅ USAR PARA:

- Definir North Star Metric
- Medir e otimizar viral coefficient
- Criar programa de referral
- Priorizar experimentos (ICE)
- Medir Product-Market Fit
- Attribution tracking (first-touch)

### ❌ NÃO USAR PARA:

- Cálculos detalhados de CLV
- Health Score de CS
- Métricas de comunidade específicas
- Learning outcomes

## Perguntas que Ellis Responde

- "Qual fonte traz mais clientes?"
- "Nosso programa de indicação está funcionando?"
- "Temos Product-Market Fit?"
- "Qual deve ser nossa North Star Metric?"
- "Que experimento devemos priorizar?"

## Framework ICE para Priorização

| Critério | Pergunta |
|----------|----------|
| **I**mpact | Qual impacto se funcionar? (1-10) |
| **C**onfidence | Qual confiança que vai funcionar? (1-10) |
| **E**ase | Quão fácil é implementar? (1-10) |

Score = (I + C + E) / 3

## Fontes para Clone

- Livro: "Hacking Growth" (2017)
- Blog: GrowthHackers.com
- Substack: @seanellis
- Podcast: "The GrowthHackers Podcast"
- Talks: Dropbox case study

---

## QUANDO COMBINAR FADER + ELLIS

A combinação é poderosa para:

| Cenário | Fader Contribui | Ellis Contribui |
|---------|-----------------|-----------------|
| **Customer 360** | Quem importa (CLV) | Como adquirir mais (referral) |
| **Segmentação** | Por valor | Por comportamento viral |
| **Attribution** | ROI por CLV do cliente adquirido | First-touch source |
| **Cohort Analysis** | Valor por cohort | Viralidade por cohort |

### Sequência Recomendada

1. **Fader primeiro**: Defina quem são os clientes de maior valor
2. **Ellis depois**: Otimize aquisição de clientes similares via referral

---

*Framework de Clones - Data Intelligence Pack v2.0*
*Tier 0: Fundamentadores (Foundation Layer)*
