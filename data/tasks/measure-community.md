# Measure Community - Avaliacao Completa de Metricas de Comunidade

## Metadata
```yaml
task_id: measure-community
version: 1.0.0
category: community-analytics
tier: TASK
difficulty: advanced
estimated_time: 4-8 hours
elicit: true
primary_agents:
  - david-spinks
secondary_agents:
  - peter-fader
  - nick-mehta
dependencies:
  - checklists/community-health-checklist.md
  - templates/community-report-tmpl.yaml
outputs:
  - Community Health Score
  - SPACES Value Assessment
  - Member Value Calculation
  - Engagement Metrics Dashboard
  - Actionable Recommendations
methodology:
  - SPACES Model (David Spinks/CMX)
  - Three-Level Strategy Framework (Spinks)
  - Community Health Indicators (Gainsight)
  - Engagement Benchmark Score (Higher Logic)
  - Member Value Framework (CMX)
```

---

## Objetivo

Conduzir uma avaliacao completa da saude e valor de uma comunidade usando o framework SPACES de David Spinks, fundador do CMX e autor de "The Business of Belonging".

Esta task permite:

- **Medir saude da comunidade** usando metricas padrao da industria
- **Calcular ROI** de iniciativas de comunidade
- **Avaliar valor por dimensao** (Support, Product, Acquisition, Content, Engagement, Success)
- **Identificar gaps** e oportunidades de melhoria
- **Benchmarkar** contra comunidades similares
- **Criar plano de acao** baseado em dados

> "Comunidade e a unica coisa que nao pode ser copiada. Produtos podem ser replicados, comunidade nao."
> - David Spinks

---

## CONTEXTO: ESPACOS vs AUDIENCIA

### Diferenca Fundamental

```
AUDIENCIA: Relacao 1-para-muitos (marca -> pessoas)
- Seguidores passivos
- Consumo unidirecional
- Valor concentrado na marca

COMUNIDADE: Relacao muitos-para-muitos (pessoas <-> pessoas)
- Membros ativos
- Interacoes bidirecionais
- Valor distribuido entre membros
```

### Por que Medir Comunidade e Diferente

| Aspecto | Audiencia (Metricas tradicionais) | Comunidade (SPACES) |
|---------|-----------------------------------|---------------------|
| Sucesso | Alcance, impressoes | Conexoes, valor gerado |
| Engajamento | Curtidas, compartilhamentos | Conversas, ajuda mutua |
| ROI | Vendas diretas | Retencao, suporte, produto |
| Crescimento | Novos seguidores | Participacao ativa |

---

## PRE-REQUISITOS

### Checklist de Preparacao

```markdown
## Antes de Iniciar

### Dados Necessarios
- [ ] Acesso a plataforma de comunidade (Discord, Slack, Circle, etc.)
- [ ] Metricas de membros (total, ativos, novos)
- [ ] Historico de atividade (posts, comentarios, reacoes)
- [ ] Dados de eventos (presenca, recorrencia)
- [ ] Metricas de suporte (tickets desviados, tempo de resposta)
- [ ] Feedback de membros (NPS, pesquisas)

### Periodo de Analise
- [ ] Definir periodo (recomendado: ultimos 90 dias)
- [ ] Ter baseline anterior para comparacao
- [ ] Acesso a dados historicos

### Stakeholders
- [ ] Objetivo de negocio claro
- [ ] Alinhamento com lideranca
- [ ] Proposta de valor da comunidade definida
```

---

## FASE 0: DIAGNOSTICO INICIAL

### Step 0.1: Elicitacao de Contexto

```yaml
elicit: true
questions:
  - question: "Qual e a plataforma principal da sua comunidade?"
    options:
      - Discord
      - Slack
      - Circle
      - Facebook Group
      - LinkedIn Group
      - Forum proprio
      - WhatsApp/Telegram
      - Outra

  - question: "Qual o tamanho atual da comunidade?"
    options:
      - Pequena (ate 500 membros)
      - Media (500-5.000 membros)
      - Grande (5.000-50.000 membros)
      - Enterprise (50.000+ membros)

  - question: "Qual o objetivo principal da comunidade?"
    options:
      - Suporte (membros ajudam membros)
      - Produto (feedback, beta testing)
      - Aquisicao (referrals, word-of-mouth)
      - Conteudo (UGC, casos de uso)
      - Engajamento (retencao, networking)
      - Sucesso do cliente (onboarding, best practices)

  - question: "A comunidade existe ha quanto tempo?"
    options:
      - Menos de 6 meses (early stage)
      - 6-12 meses (growth stage)
      - 1-3 anos (mature)
      - 3+ anos (established)
```

### Step 0.2: Matriz de Maturidade

```
┌────────────────────────────────────────────────────────────────┐
│                 MATRIZ DE MATURIDADE CMX                        │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  NIVEL 1: NASCENTE (0-6 meses)                                 │
│  - Foco: Definir proposito e primeiros membros                 │
│  - Metricas: # membros, primeiras interacoes                   │
│  - Benchmark: Qualquer engajamento e bom                       │
│                                                                  │
│  NIVEL 2: CRESCIMENTO (6-18 meses)                             │
│  - Foco: Escalar participacao e criar habitos                  │
│  - Metricas: MAU, conversas, retorno                           │
│  - Benchmark: 10-15% MAU                                        │
│                                                                  │
│  NIVEL 3: MADURA (18-36 meses)                                 │
│  - Foco: Demonstrar ROI e otimizar                             │
│  - Metricas: SPACES completo, business impact                  │
│  - Benchmark: 15-25% MAU, ROI positivo                         │
│                                                                  │
│  NIVEL 4: ESTRATEGICA (36+ meses)                              │
│  - Foco: Comunidade como vantagem competitiva                  │
│  - Metricas: Revenue attribution, CLV impact                   │
│  - Benchmark: Comunidade como canal #1 de alguma metrica       │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

---

## FASE 1: METRICAS FUNDAMENTAIS

### Step 1.1: Metricas de Participacao

```markdown
## Metricas Base de Participacao

### Definicoes

| Metrica | Formula | O que mede |
|---------|---------|------------|
| **Total Members** | Todos os cadastrados | Tamanho bruto |
| **Active Members** | Acessaram no periodo | Engajamento minimo |
| **MAU** | Active / Total * 100 | Taxa de atividade mensal |
| **DAU** | Daily active / Total * 100 | Atividade diaria |
| **Stickiness** | DAU / MAU * 100 | Habito de retorno |
| **Lurkers** | Acessam mas nao interagem | Consumo passivo |

### Coleta de Dados

| Metrica | Seu Valor | Benchmark CMX | Status |
|---------|-----------|---------------|--------|
| Total Members | [____] | - | - |
| MAU | [___]% | 10-20% | [___] |
| DAU | [___]% | 1-5% | [___] |
| Stickiness | [___]% | 5-20% | [___] |

### Referencia CMX (comunidades reais)

| Comunidade | Plataforma | Membros | MAU |
|------------|------------|---------|-----|
| CMX Slack | Slack | 4,200 | 14% |
| CMX Facebook | Facebook | 11,800 | 18% |
| Figma Community | Forum | 150,000+ | ~8% |
| Notion Community | Forum | 50,000+ | ~12% |
```

### Step 1.2: Metricas de Atividade

```markdown
## Metricas de Atividade

### Definicoes

| Metrica | Formula | O que mede |
|---------|---------|------------|
| **Posts/Member** | Total posts / Active members | Criacao de conteudo |
| **Comments/Post** | Total comments / Total posts | Nivel de discussao |
| **Response Rate** | Posts respondidos / Total posts | Suporte da comunidade |
| **Response Time** | Tempo medio ate 1a resposta | Velocidade de ajuda |
| **Conversation Depth** | Media de respostas por thread | Qualidade das discussoes |

### Coleta de Dados

| Metrica | Seu Valor | Benchmark | Status |
|---------|-----------|-----------|--------|
| Posts/Member/mes | [____] | 2-5 | [___] |
| Comments/Post | [____] | 3-10 | [___] |
| Response Rate | [___]% | 70-90% | [___] |
| Response Time | [____]h | <24h | [___] |
| Conversation Depth | [____] | 3-5 | [___] |
```

### Step 1.3: Metricas de Retencao de Membros

```markdown
## Metricas de Retencao

### Definicoes

| Metrica | Formula | O que mede |
|---------|---------|------------|
| **Churn Rate** | Membros inativos 90d+ / Total | Perda de engajamento |
| **Retention Week 1** | Ativos semana 2 / Novos semana 1 | Onboarding |
| **Retention Month 1** | Ativos mes 2 / Novos mes 1 | Engajamento inicial |
| **Retention Month 3** | Ativos mes 4 / Novos mes 1 | Habito formado |
| **Reactivation Rate** | Ex-inativos que voltaram / Inativos | Recuperacao |

### Cohort Analysis Template

| Cohort | Semana 1 | Semana 2 | Semana 4 | Mes 2 | Mes 3 |
|--------|----------|----------|----------|-------|-------|
| Jan 2024 | 100% | [__]% | [__]% | [__]% | [__]% |
| Fev 2024 | 100% | [__]% | [__]% | [__]% | [__]% |
| Mar 2024 | 100% | [__]% | [__]% | [__]% | [__]% |

### Benchmarks por Tipo de Comunidade

| Tipo | Ret. Semana 1 | Ret. Mes 1 | Ret. Mes 3 |
|------|---------------|------------|------------|
| SaaS Community | 40-60% | 20-40% | 10-25% |
| Creator Community | 30-50% | 15-30% | 8-18% |
| Professional Network | 35-55% | 18-35% | 12-22% |
| Customer Support | 50-70% | 25-45% | 15-30% |
```

---

## FASE 2: FRAMEWORK SPACES

### Step 2.1: Overview do SPACES Model

```
┌────────────────────────────────────────────────────────────────┐
│                      SPACES MODEL                               │
│              (CMX Community Value Framework)                    │
│                                                                  │
│   Criado por David Spinks, Carrie Melissa Jones,               │
│   Evan Hamilton, Erica McGillivray, Steven Broudy              │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  S - SUPPORT (Suporte)                                         │
│      Membros ajudam membros com duvidas                         │
│      KPI: Tickets desviados, tempo de resposta                  │
│      ROI: Reducao de custo de suporte                           │
│                                                                  │
│  P - PRODUCT (Produto)                                         │
│      Feedback, ideias, beta testing                             │
│      KPI: Features sugeridas, bugs reportados                   │
│      ROI: Melhoria de produto, reducao de P&D                   │
│                                                                  │
│  A - ACQUISITION (Aquisicao)                                   │
│      Word-of-mouth, referrals, advocacy                         │
│      KPI: Referrals, NPS, advocates ativos                      │
│      ROI: Reducao de CAC, aumento de confianca                  │
│                                                                  │
│  C - CONTENT (Conteudo)                                        │
│      UGC, casos de uso, tutoriais, templates                    │
│      KPI: Conteudos criados, views, downloads                   │
│      ROI: Escala de conteudo sem custo linear                   │
│                                                                  │
│  E - ENGAGEMENT (Engajamento)                                  │
│      Eventos, discussoes, networking                            │
│      KPI: Participacao, retorno, satisfacao                     │
│      ROI: Aumento de stickiness e retencao                      │
│                                                                  │
│  S - SUCCESS (Sucesso)                                         │
│      Best practices, mentoria peer-to-peer                      │
│      KPI: Time-to-value, outcomes alcancados                    │
│      ROI: Aceleracao de adocao, reducao de churn                │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

### Step 2.2: Avaliacao - SUPPORT

```markdown
## S - SUPPORT (Suporte)

### Definicao
"Membros ajudam membros a resolver problemas, reduzindo a carga do suporte oficial."

### Perguntas de Diagnostico
1. Membros respondem perguntas de outros membros?
2. Quanto tempo leva para uma pergunta ser respondida pela comunidade?
3. Quantos tickets de suporte sao resolvidos pela comunidade vs. time oficial?
4. Existe um programa de membros experts/champions?

### Metricas de Support

| Metrica | Formula | Seu Valor | Benchmark |
|---------|---------|-----------|-----------|
| **Community Resolution Rate** | Perguntas resolvidas por membros / Total | [___]% | 40-60% |
| **Ticket Deflection** | Perguntas na comunidade vs tickets | [___]% | 20-40% |
| **First Response Time (Community)** | Tempo medio ate 1a resposta de membro | [___]h | <4h |
| **Expert Contribution Rate** | % respostas de power users | [___]% | 15-30% |
| **Solution Accuracy** | Respostas marcadas como solucao | [___]% | 70-85% |

### Calculo de ROI - Support

```
Valor Gerado = Tickets Desviados x Custo por Ticket

Exemplo:
- Tickets desviados/mes: 500
- Custo por ticket (suporte): R$ 25
- Valor mensal: 500 x R$25 = R$ 12.500

ROI Support = Valor Gerado - Custo de Gestao da Comunidade
```

### Score Support (0-10)

| Score | Criterio |
|-------|----------|
| 1-3 | Poucos membros respondem, maioria fica sem resposta |
| 4-6 | Comunidade responde, mas lento ou impreciso |
| 7-8 | Comunidade ativa, resolucao rapida e precisa |
| 9-10 | Comunidade e o canal preferido para suporte |

**Seu Score Support:** [___] / 10
```

### Step 2.3: Avaliacao - PRODUCT

```markdown
## P - PRODUCT (Produto)

### Definicao
"Comunidade como fonte de insights para melhoria de produto."

### Perguntas de Diagnostico
1. A comunidade sugere features que sao implementadas?
2. Existe um processo para coletar e priorizar feedback?
3. Membros participam de beta testing?
4. Bugs sao reportados pela comunidade antes de causar problemas maiores?

### Metricas de Product

| Metrica | Formula | Seu Valor | Benchmark |
|---------|---------|-----------|-----------|
| **Feature Suggestions/Month** | Total sugestoes recebidas | [___] | 10-50 |
| **Suggestions Implemented** | % implementadas em 12 meses | [___]% | 5-15% |
| **Beta Participation Rate** | % que participa de betas | [___]% | 10-25% |
| **Bug Reports from Community** | Bugs reportados por membros | [___] | - |
| **Product Ideas Quality** | Ideias que viram roadmap | [___]% | 3-8% |

### Framework de Coleta de Feedback

```
1. IDEACAO
   - Canal dedicado para sugestoes
   - Template padrao para feature requests
   - Votacao da comunidade (upvotes)

2. VALIDACAO
   - Discussao com membros interessados
   - Prototipacao com feedback
   - Beta testing com grupo seleto

3. LANCAMENTO
   - Comunicacao na comunidade primeiro
   - Early access para membros ativos
   - Coleta de feedback pos-lancamento
```

### Score Product (0-10)

| Score | Criterio |
|-------|----------|
| 1-3 | Feedback nao e coletado sistematicamente |
| 4-6 | Feedback coletado, mas pouco implementado |
| 7-8 | Processo claro, implementacao regular |
| 9-10 | Comunidade e voz principal no roadmap |

**Seu Score Product:** [___] / 10
```

### Step 2.4: Avaliacao - ACQUISITION

```markdown
## A - ACQUISITION (Aquisicao)

### Definicao
"Comunidade como canal de aquisicao organica."

### Perguntas de Diagnostico
1. Membros indicam novos membros/clientes?
2. Existe um programa de referral?
3. Membros criam conteudo que atrai novos usuarios?
4. Qual o NPS da comunidade?

### Metricas de Acquisition

| Metrica | Formula | Seu Valor | Benchmark |
|---------|---------|-----------|-----------|
| **Referral Rate** | Novos via indicacao / Total novos | [___]% | 10-30% |
| **Advocate Activation** | Membros que indicaram alguem | [___]% | 5-15% |
| **Community NPS** | Net Promoter Score | [___] | >50 |
| **Viral Coefficient** | Indicacoes/membro | [___] | >0.3 |
| **Community Attribution** | Conversoes com touchpoint comunidade | [___]% | 5-20% |

### Calculo de ROI - Acquisition

```
Valor Gerado = Clientes via Comunidade x CAC Poupado

Exemplo:
- Clientes via referral/mes: 20
- CAC normal: R$ 500
- Valor mensal: 20 x R$500 = R$ 10.000

Considerando que membros da comunidade convertem 2x melhor:
- Taxa conversao normal: 2%
- Taxa conversao comunidade: 4%
- Valor adicional de eficiencia
```

### Framework de Advocacy

```
┌─────────────────────────────────────────────────────────┐
│               PIRAMIDE DE ADVOCACY                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│     ▲ Ambassadors (1-2%)                                │
│     │  Criam conteudo, palestram, lideram               │
│    ▲│▲ Champions (5-10%)                                │
│    │││  Respondem perguntas, mentoram                   │
│   ▲│││▲ Advocates (15-25%)                              │
│   │││││  Indicam, compartilham, recomendam              │
│  ▲│││││▲ Active Members (30-40%)                        │
│  │││││││  Participam regularmente                       │
│ ▲│││││││▲ Members (100%)                                │
│ ││││││││││ Base cadastrada                              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Score Acquisition (0-10)

| Score | Criterio |
|-------|----------|
| 1-3 | Comunidade nao gera leads/clientes |
| 4-6 | Alguns referrals, mas nao sistematico |
| 7-8 | Programa de advocacy ativo, metricas claras |
| 9-10 | Comunidade e top 3 canal de aquisicao |

**Seu Score Acquisition:** [___] / 10
```

### Step 2.5: Avaliacao - CONTENT

```markdown
## C - CONTENT (Conteudo)

### Definicao
"Membros criam conteudo que beneficia toda a comunidade."

### Perguntas de Diagnostico
1. Membros criam tutoriais, templates, casos de uso?
2. Conteudo gerado pela comunidade e reutilizado (KB, docs)?
3. Existe reconhecimento para criadores de conteudo?
4. Qual a qualidade do UGC vs conteudo oficial?

### Metricas de Content

| Metrica | Formula | Seu Valor | Benchmark |
|---------|---------|-----------|-----------|
| **UGC Volume** | Conteudos criados por membros/mes | [___] | 20-100 |
| **UGC Quality Score** | Rating medio de conteudo | [___]/5 | 3.5-4.5 |
| **Content Creators** | % membros que criam conteudo | [___]% | 1-5% |
| **Content Engagement** | Views/downloads de UGC | [___] | - |
| **Content Reuse** | UGC incorporado em docs oficiais | [___] | 5-20 |

### Tipos de UGC Valioso

```
ALTO VALOR:
- Templates e frameworks reutilizaveis
- Tutoriais step-by-step
- Casos de uso detalhados
- Integracoes e extensoes
- Traducoes da comunidade

MEDIO VALOR:
- Perguntas e respostas (searchable)
- Discussoes tecnicas
- Reviews e comparacoes
- Dicas e hacks

BAIXO VALOR:
- Comentarios curtos
- Reacoes/emojis
- Perguntas repetidas
```

### Calculo de ROI - Content

```
Valor Gerado = Conteudos Criados x Custo Equivalente

Exemplo:
- Tutoriais criados/mes: 10
- Custo para criar internamente: R$ 500/tutorial
- Valor mensal: 10 x R$500 = R$ 5.000

Plus: Conteudo indexavel que atrai trafego organico
```

### Score Content (0-10)

| Score | Criterio |
|-------|----------|
| 1-3 | Pouco ou nenhum conteudo criado por membros |
| 4-6 | Algum UGC, mas qualidade inconsistente |
| 7-8 | UGC regular, qualidade boa, reutilizacao |
| 9-10 | UGC e fonte principal de conteudo educacional |

**Seu Score Content:** [___] / 10
```

### Step 2.6: Avaliacao - ENGAGEMENT

```markdown
## E - ENGAGEMENT (Engajamento)

### Definicao
"Membros participam ativamente e retornam consistentemente."

### Perguntas de Diagnostico
1. Membros participam de eventos da comunidade?
2. Qual a taxa de retorno em eventos?
3. Existem subgrupos/canais ativos?
4. Membros formam conexoes genuinas (networking)?

### Metricas de Engagement

| Metrica | Formula | Seu Valor | Benchmark |
|---------|---------|-----------|-----------|
| **Event Attendance Rate** | Presentes / Registrados | [___]% | 30-50% |
| **Repeat Attendance** | % que volta em 2+ eventos | [___]% | 40-60% |
| **Channel Activity** | Mensagens/canal/dia | [___] | 5-50 |
| **Connection Rate** | Membros que conectaram 1:1 | [___]% | 10-30% |
| **Community NPS** | "Recomendaria a comunidade?" | [___] | >50 |

### Framework de Eventos

```
TIPOS DE EVENTOS POR OBJETIVO:

CONEXAO
├── Networking sessions
├── 1:1 matching
├── Grupos de interesse
└── Mentorias

APRENDIZADO
├── Workshops
├── AMAs / Q&As
├── Study groups
└── Masterclasses

CELEBRACAO
├── Marcos da comunidade
├── Member spotlights
├── Awards
└── Aniversarios

CONTRIBUICAO
├── Hackathons
├── Challenges
├── Co-criacao
└── Feedback sessions
```

### Health Indicators - Engagement

```
SAUDAVEL:
- Eventos lotam sem marketing
- Membros organizam eventos proprios
- Discussoes surgem organicamente
- Alta taxa de retorno

ALERTA:
- Precisa muito esforco para atrair
- Eventos dependem de time interno
- Discussoes morrem rapido
- Baixa recorrencia

CRITICO:
- Eventos vazios
- Comunidade silenciosa
- Membros nao conhecem outros membros
- Zero iniciativas organicas
```

### Score Engagement (0-10)

| Score | Criterio |
|-------|----------|
| 1-3 | Comunidade silenciosa, eventos vazios |
| 4-6 | Engajamento esporadico, picos e vales |
| 7-8 | Engajamento consistente, eventos populares |
| 9-10 | Comunidade auto-sustentavel, iniciativas organicas |

**Seu Score Engagement:** [___] / 10
```

### Step 2.7: Avaliacao - SUCCESS

```markdown
## S - SUCCESS (Sucesso)

### Definicao
"Comunidade acelera o sucesso dos membros com o produto/servico."

### Perguntas de Diagnostico
1. Membros atingem seus objetivos mais rapido na comunidade?
2. Existem best practices compartilhadas?
3. Ha mentoria peer-to-peer?
4. Qual o time-to-value para membros da comunidade vs nao-membros?

### Metricas de Success

| Metrica | Formula | Seu Valor | Benchmark |
|---------|---------|-----------|-----------|
| **Time to First Value** | Dias ate primeiro "aha moment" | [___]d | 7-30d |
| **Goal Achievement Rate** | % que atinge objetivo declarado | [___]% | 40-70% |
| **Retention Lift** | Retencao comunidade vs nao-comunidade | [___]% | +10-30% |
| **NPS Lift** | NPS comunidade vs nao-comunidade | [___] | +10-20 pts |
| **Mentor Match Rate** | Mentorias ativas / membros novos | [___]% | 10-30% |

### Framework de Sucesso - Jornada do Membro

```
┌─────────────────────────────────────────────────────────────┐
│             JORNADA DE SUCESSO NA COMUNIDADE                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  FASE 1: ONBOARDING (Dias 1-7)                              │
│  ├── Welcome automatizado                                    │
│  ├── Introducao aos recursos                                 │
│  ├── Primeira pergunta respondida                            │
│  └── KPI: Primeira interacao em <48h                         │
│                                                              │
│  FASE 2: ATIVACAO (Dias 7-30)                               │
│  ├── Participou de evento/discussao                          │
│  ├── Conectou com outro membro                               │
│  ├── Criou primeira contribuicao                             │
│  └── KPI: 3+ interacoes significativas                       │
│                                                              │
│  FASE 3: HABITO (Dias 30-90)                                │
│  ├── Retorna semanalmente                                    │
│  ├── Ajudou outro membro                                     │
│  ├── Participou de programa (mentoria, grupo)                │
│  └── KPI: Retencao mes 3 >25%                                │
│                                                              │
│  FASE 4: ADVOCACIA (Dia 90+)                                │
│  ├── Indicou novo membro                                     │
│  ├── Criou conteudo                                          │
│  ├── Liderou iniciativa                                      │
│  └── KPI: Champion identificado                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Calculo de ROI - Success

```
Valor Gerado = Retencao Incremental x LTV

Exemplo:
- Membros ativos na comunidade: 1.000
- Lift de retencao: +15%
- LTV medio: R$ 2.000
- Valor: 1.000 x 15% x R$2.000 = R$ 300.000/ano
```

### Score Success (0-10)

| Score | Criterio |
|-------|----------|
| 1-3 | Comunidade nao impacta sucesso do membro |
| 4-6 | Algum impacto, mas nao mensuravel |
| 7-8 | Impacto claro em onboarding e retencao |
| 9-10 | Comunidade e diferencial competitivo |

**Seu Score Success:** [___] / 10
```

---

## FASE 3: COMMUNITY HEALTH SCORE

### Step 3.1: Calculando o Health Score

```markdown
## Community Health Score (CHS)

### Formula Base

```
CHS = (S + P + A + C + E + S) / 6

Onde cada dimensao varia de 0 a 10.
```

### Seus Resultados

| Dimensao | Score | Peso (opcional) | Ponderado |
|----------|-------|-----------------|-----------|
| Support | [___] | 1.0 | [___] |
| Product | [___] | 1.0 | [___] |
| Acquisition | [___] | 1.0 | [___] |
| Content | [___] | 1.0 | [___] |
| Engagement | [___] | 1.0 | [___] |
| Success | [___] | 1.0 | [___] |
| **TOTAL** | | | **[___]** |

### Interpretacao do Health Score

| Score | Status | Interpretacao |
|-------|--------|---------------|
| 0-3 | Critico | Comunidade precisa de intervencao urgente |
| 4-5 | Em Risco | Gaps significativos, priorizacao necessaria |
| 6-7 | Saudavel | Funcionando bem, oportunidades de otimizacao |
| 8-9 | Forte | Comunidade madura, foco em escala |
| 10 | Excepcional | Benchmark da industria |
```

### Step 3.2: Pesos por Objetivo de Negocio

```markdown
## Ponderacao por Objetivo

Ajuste os pesos conforme o objetivo principal da comunidade:

### Se foco e REDUCAO DE CUSTO:

| Dimensao | Peso |
|----------|------|
| Support | 2.0 |
| Content | 1.5 |
| Success | 1.5 |
| Outros | 0.5 |

### Se foco e CRESCIMENTO:

| Dimensao | Peso |
|----------|------|
| Acquisition | 2.0 |
| Engagement | 1.5 |
| Content | 1.5 |
| Outros | 0.5 |

### Se foco e RETENCAO:

| Dimensao | Peso |
|----------|------|
| Success | 2.0 |
| Engagement | 2.0 |
| Support | 1.5 |
| Outros | 0.5 |

### Se foco e INOVACAO DE PRODUTO:

| Dimensao | Peso |
|----------|------|
| Product | 2.5 |
| Content | 1.5 |
| Success | 1.0 |
| Outros | 0.5 |
```

### Step 3.3: Visualizacao Radar

```
## SPACES Radar Chart

              SUPPORT
                 10
                  │
                  8
                  │
                  6
                  │
SUCCESS ─────────4─────────── PRODUCT
                  │
                  2
                  │
                  │
    ENGAGEMENT ───┼─── ACQUISITION
                  │
               CONTENT

Marque seus scores e conecte os pontos.
Areas mais proximas do centro = gaps prioritarios.
```

---

## FASE 4: MEMBER VALUE CALCULATION

### Step 4.1: Framework de Valor por Membro

```markdown
## Member Lifetime Value (MLTV)

### Componentes de Valor

```
MLTV = Valor Direto + Valor Indireto + Valor de Network

Valor Direto:
- Compras feitas
- Upsells/expansoes
- Renovacoes

Valor Indireto:
- Suporte evitado (respostas a outros)
- Conteudo criado (UGC)
- Feedback de produto

Valor de Network:
- Referrals feitos
- Influencia na decisao de outros
- Conteudo externo criado
```

### Calculadora de Valor

| Atividade | Quantidade | Valor Unitario | Total |
|-----------|------------|----------------|-------|
| Tickets desviados (respostas) | [___] | R$ [___] | R$ [___] |
| Conteudos criados | [___] | R$ [___] | R$ [___] |
| Referrals convertidos | [___] | R$ [___] | R$ [___] |
| Features sugeridas implementadas | [___] | R$ [___] | R$ [___] |
| Eventos organizados | [___] | R$ [___] | R$ [___] |
| **TOTAL MLTV** | | | **R$ [___]** |
```

### Step 4.2: Segmentacao por Valor

```markdown
## Segmentos de Membros (CMX Framework)

### Definicao dos Segmentos

| Segmento | % Base | Comportamento | Valor |
|----------|--------|---------------|-------|
| **Ambassadors** | 1-2% | Criam, lideram, evangelizam | Muito Alto |
| **Champions** | 5-10% | Respondem, mentoram, contribuem | Alto |
| **Advocates** | 15-25% | Indicam, participam, compartilham | Medio |
| **Active** | 30-40% | Participam regularmente | Baixo |
| **Lurkers** | 30-50% | Consomem passivamente | Minimo |

### Identificacao de Segmentos

```
AMBASSADOR (Top 1-2%)
- Cria conteudo original
- Organiza eventos
- Palestra/representa a marca
- Indica 5+ membros
Score minimo necessario: [definir]

CHAMPION (Top 10%)
- Responde 10+ perguntas/mes
- Mentora outros membros
- Participa de beta
- Contribui com feedback
Score minimo necessario: [definir]

ADVOCATE (Top 25%)
- Participa de eventos
- Compartilha conteudo
- Indica novos membros
- Engaja semanalmente
Score minimo necessario: [definir]
```

### Seu Mapeamento

| Segmento | Qtd Esperada | Qtd Atual | Gap |
|----------|--------------|-----------|-----|
| Ambassadors (1-2%) | [___] | [___] | [___] |
| Champions (5-10%) | [___] | [___] | [___] |
| Advocates (15-25%) | [___] | [___] | [___] |
| Active (30-40%) | [___] | [___] | [___] |
| Lurkers (30-50%) | [___] | [___] | [___] |
```

---

## FASE 5: BENCHMARKS POR TIPO DE COMUNIDADE

### Step 5.1: Benchmarks por Industria

```markdown
## Benchmarks CMX/Higher Logic

### Comunidades SaaS B2B

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| MAU | 5% | 12% | 18% | 25% |
| DAU/MAU | 3% | 8% | 15% | 22% |
| Posts/MAU | 1.2 | 2.5 | 4.2 | 7.0 |
| Response Rate | 55% | 72% | 85% | 92% |
| NPS | 25 | 45 | 62 | 78 |

### Comunidades Creator/Educacao

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| MAU | 3% | 8% | 15% | 22% |
| Completion (cursos) | 8% | 25% | 45% | 65% |
| UGC/month | 5 | 15 | 35 | 80 |
| Event Attendance | 15% | 32% | 48% | 65% |
| Referral Rate | 3% | 8% | 15% | 25% |

### Comunidades de Suporte

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| Ticket Deflection | 8% | 22% | 38% | 52% |
| Community Resolution | 25% | 45% | 62% | 78% |
| First Response Time | 48h | 12h | 4h | 1h |
| CSAT (community) | 3.2 | 3.8 | 4.3 | 4.7 |

### Comunidades Profissionais

| Metrica | P25 | P50 | P75 | P90 |
|---------|-----|-----|-----|-----|
| MAU | 8% | 15% | 22% | 32% |
| Event Attendance | 20% | 38% | 52% | 68% |
| Connection Rate | 5% | 12% | 22% | 35% |
| Job Placements | 2% | 5% | 10% | 18% |
```

### Step 5.2: Comparacao com Benchmark

```markdown
## Sua Posicao vs Benchmark

| Metrica | Seu Valor | Benchmark (P50) | Diferenca | Quartil |
|---------|-----------|-----------------|-----------|---------|
| MAU | [___]% | [___]% | [___]% | [___] |
| DAU/MAU | [___]% | [___]% | [___]% | [___] |
| Response Rate | [___]% | [___]% | [___]% | [___] |
| NPS | [___] | [___] | [___] | [___] |
| [Metrica X] | [___] | [___] | [___] | [___] |

### Interpretacao

ACIMA DO BENCHMARK (P50+):
- [lista metricas]
- Insight: [o que esta funcionando]

ABAIXO DO BENCHMARK (<P50):
- [lista metricas]
- Insight: [gaps identificados]

PRIORIDADES:
1. [metrica mais critica]
2. [metrica secundaria]
```

---

## FASE 6: DIAGNOSTICO E RECOMENDACOES

### Step 6.1: Analise de Gaps

```markdown
## Gap Analysis

### Template por Dimensao

| Dimensao | Score Atual | Score Alvo | Gap | Prioridade |
|----------|-------------|------------|-----|------------|
| Support | [___] | [___] | [___] | [___] |
| Product | [___] | [___] | [___] | [___] |
| Acquisition | [___] | [___] | [___] | [___] |
| Content | [___] | [___] | [___] | [___] |
| Engagement | [___] | [___] | [___] | [___] |
| Success | [___] | [___] | [___] | [___] |

### Criterios de Priorizacao

```
PRIORIDADE = Impacto x Facilidade

Alto Impacto + Facil = Quick Win (fazer primeiro)
Alto Impacto + Dificil = Strategic (planejar)
Baixo Impacto + Facil = Fill-in (se sobrar tempo)
Baixo Impacto + Dificil = Evitar
```
```

### Step 6.2: Playbooks por Gap

```markdown
## Playbooks de Intervencao

### Se SUPPORT esta baixo:

```
ACOES IMEDIATAS (0-30 dias):
1. Criar canal dedicado para perguntas
2. Recrutar 5 power users como experts
3. Implementar badge system para respostas
4. Configurar notificacoes para perguntas sem resposta

ACOES MEDIAS (30-90 dias):
1. Programa formal de Champions
2. Integracao com base de conhecimento
3. SLA de resposta da comunidade
4. Dashboard de metricas de suporte
```

### Se PRODUCT esta baixo:

```
ACOES IMEDIATAS:
1. Criar canal #ideias ou #feedback
2. Fazer AMA com PM
3. Compartilhar roadmap publico
4. Convidar para beta testing

ACOES MEDIAS:
1. Processo de votacao de features
2. Advisory board de membros
3. Programa de beta testers
4. Loop de feedback fechado
```

### Se ACQUISITION esta baixo:

```
ACOES IMEDIATAS:
1. Criar programa de referral simples
2. Pedir depoimentos de membros ativos
3. Incentivar compartilhamento (rewards)
4. Criar conteudo shareable

ACOES MEDIAS:
1. Programa de advocacy formal
2. Member-get-member campaigns
3. Conteudo de membros amplificado
4. Tracking de attribution
```

### Se CONTENT esta baixo:

```
ACOES IMEDIATAS:
1. Challenge de criacao de conteudo
2. Templates para facilitar contribuicao
3. Spotlight em contribuidores
4. Gamificacao (badges, leaderboard)

ACOES MEDIAS:
1. Programa de contribuidores
2. Co-criacao com comunidade
3. Repositorio de conteudo curado
4. Compensacao para top creators
```

### Se ENGAGEMENT esta baixo:

```
ACOES IMEDIATAS:
1. Calendario de eventos regular
2. Canais por interesse/tema
3. Welcome post para novos membros
4. Daily/weekly engagement ritual

ACOES MEDIAS:
1. Programa de grupos pequenos
2. Mentorias 1:1
3. Eventos presenciais
4. Challenges e competicoes
```

### Se SUCCESS esta baixo:

```
ACOES IMEDIATAS:
1. Onboarding guide para comunidade
2. Quick wins documentados
3. Office hours com experts
4. Success stories destacadas

ACOES MEDIAS:
1. Programa de mentoria
2. Trilhas de aprendizado
3. Certificacoes da comunidade
4. Dashboard de progresso pessoal
```
```

---

## FASE 7: ROI CONSOLIDADO

### Step 7.1: Calculadora de ROI

```markdown
## ROI Total da Comunidade

### Custos

| Item | Mensal | Anual |
|------|--------|-------|
| Plataforma | R$ [___] | R$ [___] |
| Community Manager | R$ [___] | R$ [___] |
| Eventos | R$ [___] | R$ [___] |
| Ferramentas | R$ [___] | R$ [___] |
| Incentivos/rewards | R$ [___] | R$ [___] |
| **TOTAL CUSTOS** | **R$ [___]** | **R$ [___]** |

### Valor Gerado

| Dimensao | Calculo | Valor Mensal | Valor Anual |
|----------|---------|--------------|-------------|
| Support | [___] tickets x R$[___] | R$ [___] | R$ [___] |
| Product | [___] features x R$[___] | R$ [___] | R$ [___] |
| Acquisition | [___] referrals x R$[___] | R$ [___] | R$ [___] |
| Content | [___] conteudos x R$[___] | R$ [___] | R$ [___] |
| Engagement | [___]% retencao x R$[___] | R$ [___] | R$ [___] |
| Success | [___] usuarios x R$[___] | R$ [___] | R$ [___] |
| **TOTAL VALOR** | | **R$ [___]** | **R$ [___]** |

### ROI Final

```
ROI = (Valor Gerado - Custo) / Custo x 100

ROI = (R$ [___] - R$ [___]) / R$ [___] x 100 = [___]%
```

### Interpretacao

| ROI | Status |
|-----|--------|
| <0% | Prejuizo - revisar estrategia |
| 0-100% | Ponto de equilibrio - otimizar |
| 100-300% | Saudavel - escalar |
| >300% | Excelente - investir mais |
```

---

## FASE 8: PLANO DE ACAO

### Step 8.1: Template de Plano

```markdown
## Plano de Melhoria - 90 Dias

### DIAS 1-30: FUNDACAO

| Acao | Responsavel | Prazo | Metrica de Sucesso |
|------|-------------|-------|-------------------|
| [Acao 1] | [Nome] | [Data] | [KPI] |
| [Acao 2] | [Nome] | [Data] | [KPI] |
| [Acao 3] | [Nome] | [Data] | [KPI] |

### DIAS 31-60: EXECUCAO

| Acao | Responsavel | Prazo | Metrica de Sucesso |
|------|-------------|-------|-------------------|
| [Acao 1] | [Nome] | [Data] | [KPI] |
| [Acao 2] | [Nome] | [Data] | [KPI] |

### DIAS 61-90: OTIMIZACAO

| Acao | Responsavel | Prazo | Metrica de Sucesso |
|------|-------------|-------|-------------------|
| [Acao 1] | [Nome] | [Data] | [KPI] |
| [Acao 2] | [Nome] | [Data] | [KPI] |

### METRICAS DE ACOMPANHAMENTO

| Metrica | Baseline | Meta 30d | Meta 60d | Meta 90d |
|---------|----------|----------|----------|----------|
| MAU | [___]% | [___]% | [___]% | [___]% |
| Health Score | [___] | [___] | [___] | [___] |
| [KPI Principal] | [___] | [___] | [___] | [___] |
```

---

## OUTPUT FINAL

### Deliverables

Ao completar esta task, voce tera:

1. **SPACES Assessment Completo** - Score em cada dimensao
2. **Community Health Score** - Numero consolidado
3. **Member Value Analysis** - Segmentacao e MLTV
4. **Benchmark Comparison** - Posicao vs industria
5. **Gap Analysis** - Prioridades identificadas
6. **ROI Calculation** - Valor da comunidade
7. **90-Day Action Plan** - Roadmap de melhorias

### Template de Relatorio Executivo

```markdown
# Community Health Report
## [Nome da Comunidade] - [Data]

### Executive Summary
- Community Health Score: [X/10]
- ROI Estimado: [X]%
- Principal Forca: [dimensao]
- Principal Gap: [dimensao]

### SPACES Scores
| S | P | A | C | E | S |
|---|---|---|---|---|---|
| X | X | X | X | X | X |

### Key Metrics
- Total Members: [X]
- MAU: [X]%
- NPS: [X]

### Top 3 Recomendacoes
1. [Recomendacao 1]
2. [Recomendacao 2]
3. [Recomendacao 3]

### Proximos Passos
1. [Acao com prazo]
2. [Acao com prazo]
```

---

## REFERENCIAS

### David Spinks
- Livro: "The Business of Belonging" (2021)
- Newsletter: davidspinks.substack.com
- Podcast: "Masters of Community"
- SPACES Model original: cmxhub.com/blog/the-spaces-model

### CMX
- CMX Academy: community.cmxhub.com
- CMX Summit: eventos anuais
- CMX Research Reports

### Outras Fontes
- Higher Logic: Community Benchmarking Report
- Gainsight: Community Health Indicators
- Lenny's Newsletter: "A founder's guide to community"

---

## CHECKLIST FINAL

```markdown
## Validacao da Task

### Completude
- [ ] Todas as metricas de participacao coletadas
- [ ] Score SPACES calculado (6 dimensoes)
- [ ] Health Score consolidado
- [ ] Member Value segmentado
- [ ] Benchmarks comparados
- [ ] Gaps identificados e priorizados
- [ ] ROI calculado
- [ ] Plano de 90 dias criado

### Qualidade
- [ ] Dados baseados em evidencias (nao estimativas)
- [ ] Calculos verificados
- [ ] Recomendacoes acionaveis
- [ ] Prazos realistas
- [ ] Responsaveis definidos

### Entrega
- [ ] Relatorio executivo pronto
- [ ] Apresentacao para stakeholders
- [ ] Dashboard de acompanhamento configurado
```

---

## ANTI-PATTERNS

### Erros Comuns a Evitar

1. **Medir apenas tamanho**
   - ERRADO: "Temos 10.000 membros!"
   - CERTO: "Temos 10.000 membros, 12% MAU, gerando R$50k/mes em valor"

2. **Ignorar lurkers**
   - ERRADO: "Lurkers nao contam"
   - CERTO: "Lurkers sao 40% da base e consomem conteudo valioso"

3. **Otimizar metrica errada**
   - ERRADO: Focar em total de membros
   - CERTO: Focar em membros ativos e valor gerado

4. **Copiar metricas de outra comunidade**
   - ERRADO: "A comunidade X tem 20% MAU, precisamos tambem"
   - CERTO: "Nossa comunidade e diferente, nosso benchmark e..."

5. **Nao conectar com objetivos de negocio**
   - ERRADO: "Engajamento subiu 15%"
   - CERTO: "Engajamento subiu 15%, gerando 20% mais referrals"

---

**Total de Linhas: 850+**
**Metodologias Integradas: 5** (SPACES, Three-Level Strategy, Community Health, Member Value, Engagement Benchmark)
**Frameworks Incluidos: 8+**
**Calculadoras: 5** (ROI, Health Score, Member Value, Gap Analysis, Benchmark Comparison)
