# Framework de Clones - Data Intelligence Pack
## 07 - Workflows

---

## WORKFLOW 1: IMPLEMENTAR CUSTOMER 360

### Objetivo
Criar visão unificada do cliente com todos os dados relevantes para decisão.

### Clones Envolvidos
- **Primário:** Peter Fader
- **Secundário:** Nick Mehta
- **Terciário:** Avinash Kaushik

### Passo a Passo

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: FUNDAMENTAÇÃO (Peter Fader)                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Definir critérios de "bom cliente"                            │
│   └── CLV alto? Frequência? Fit com ICP?                        │
│                                                                  │
│ □ Mapear dados disponíveis                                      │
│   └── Transações, engajamento, suporte, community               │
│                                                                  │
│ □ Definir segmentação inicial                                   │
│   └── Por valor (RFM), por produto, por cohort                  │
│                                                                  │
│ □ Estabelecer quais perguntas o 360 deve responder              │
│   └── "Este cliente vale investir?"                             │
│   └── "Qual próxima ação?"                                      │
│   └── "Que oferta faz sentido?"                                 │
│                                                                  │
│ OUTPUT: Lista de campos essenciais + lógica de segmentação      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: OPERACIONALIZAÇÃO (Nick Mehta)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Definir componentes do Health Score                           │
│   └── Product usage (30%)                                       │
│   └── Engagement (25%)                                          │
│   └── Support health (20%)                                      │
│   └── Community participation (15%)                             │
│   └── Contract/relationship (10%)                               │
│                                                                  │
│ □ Criar thresholds                                              │
│   └── Verde: 70-100                                             │
│   └── Amarelo: 40-69                                            │
│   └── Vermelho: 0-39                                            │
│                                                                  │
│ □ Mapear ações por status                                       │
│   └── Verde → Candidato a upsell/referral                       │
│   └── Amarelo → Check-in proativo                               │
│   └── Vermelho → Intervenção urgente                            │
│                                                                  │
│ OUTPUT: Health Score funcionando + playbooks por status         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: COMUNICAÇÃO (Avinash Kaushik)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Estruturar output visual                                      │
│   └── Quais campos na tela principal?                           │
│   └── Que drill-downs disponibilizar?                           │
│                                                                  │
│ □ Criar formato "So What"                                       │
│   └── Para cada cliente: situação + recomendação                │
│   └── Evitar data dump sem ação                                 │
│                                                                  │
│ □ Definir cadência de uso                                       │
│   └── Quem olha? Quando? Que decisão toma?                      │
│                                                                  │
│ OUTPUT: Interface e reports que geram ação                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## WORKFLOW 2: CRIAR SISTEMA DE CHURN ALERTS

### Objetivo
Identificar clientes em risco antes do churn e acionar intervenção.

### Clones Envolvidos
- **Primário:** Nick Mehta
- **Secundário:** Peter Fader (priorização por valor)
- **Secundário:** David Spinks (alertas de community)
- **Secundário:** Wes Kao (alertas de learning)

### Passo a Passo

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: DEFINIR SINAIS (Nick Mehta + Fader)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Mapear leading indicators de churn                            │
│   └── Login drop >50% (Mehta)                                   │
│   └── Support ticket crítico (Mehta)                            │
│   └── Champion deixou empresa (Mehta)                           │
│   └── Community drop (Spinks)                                   │
│   └── Course stall (Kao)                                        │
│                                                                  │
│ □ Priorizar por CLV em risco (Fader)                            │
│   └── Clientes de alto CLV = prioridade máxima                  │
│   └── Clientes de baixo CLV = prioridade menor                  │
│                                                                  │
│ □ Definir severidade                                            │
│   └── Critical: múltiplos sinais + alto CLV                     │
│   └── High: 1 sinal forte + alto CLV                            │
│   └── Medium: sinais moderados                                  │
│   └── Low: sinais fracos ou baixo CLV                           │
│                                                                  │
│ OUTPUT: Lista de tipos de alerta com severidade                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: CRIAR ALERTAS (Nick Mehta)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Alerta: INACTIVITY                                            │
│   └── Trigger: 14 dias sem login                                │
│   └── Severidade: baseada em CLV                                │
│   └── Ação: Email automático + task para CS                     │
│                                                                  │
│ □ Alerta: MEETING_RISK                                          │
│   └── Trigger: Reunião de renewal em 30 dias + health <50       │
│   └── Severidade: High                                          │
│   └── Ação: Prep call + escalation                              │
│                                                                  │
│ □ Alerta: COMMUNITY_DROP (com Spinks)                           │
│   └── Trigger: Participação caiu >60% mês-a-mês                 │
│   └── Severidade: Medium                                        │
│   └── Ação: Outreach personalizado                              │
│                                                                  │
│ □ Alerta: LEARNING_STALL (com Kao)                              │
│   └── Trigger: 7 dias sem progresso no curso                    │
│   └── Severidade: Medium                                        │
│   └── Ação: Nudge + oferta de suporte                           │
│                                                                  │
│ OUTPUT: Sistema de alertas funcionando                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: PLAYBOOKS DE AÇÃO (Nick Mehta)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Playbook: Inactivity Response                                 │
│   └── Dia 1: Email automático "Sentimos sua falta"              │
│   └── Dia 3: Task para CS ligar                                 │
│   └── Dia 7: Email do founder                                   │
│   └── Dia 14: Escalation para manager                           │
│                                                                  │
│ □ Playbook: Meeting Risk Prep                                   │
│   └── -30 dias: Review completo da conta                        │
│   └── -14 dias: Call de alignment interno                       │
│   └── -7 dias: Prep de save offers                              │
│   └── Meeting: Executar save playbook                           │
│                                                                  │
│ □ Métricas de efetividade                                       │
│   └── % alertas que viraram ação                                │
│   └── % ações que evitaram churn                                │
│   └── $ saved por alerta                                        │
│                                                                  │
│ OUTPUT: Playbooks documentados + métricas de tracking           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## WORKFLOW 3: IMPLEMENTAR ATTRIBUTION

### Objetivo
Entender quais canais/fontes trazem e convertem clientes.

### Clones Envolvidos
- **Primário:** Avinash Kaushik
- **Secundário:** Sean Ellis (referral attribution)
- **Secundário:** Peter Fader (attribution por CLV)

### Passo a Passo

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: DEFINIR OBJETIVO (Kaushik + Fader)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Que decisão será informada? (Kaushik - DMMM)                  │
│   └── "Onde investir mais em marketing?"                        │
│   └── "Qual canal desligar?"                                    │
│   └── "Quanto vale cada fonte?"                                 │
│                                                                  │
│ □ Conectar com valor do cliente (Fader)                         │
│   └── Não apenas "quantos clientes"                             │
│   └── Mas "quanto CLV cada fonte gera"                          │
│                                                                  │
│ □ Mapear fontes a rastrear                                      │
│   └── Paid (Google, Meta, etc)                                  │
│   └── Organic (SEO, Direct)                                     │
│   └── Referral (indicações) ← importante para vocês             │
│   └── Social (orgânico)                                         │
│   └── Events/Webinars                                           │
│                                                                  │
│ OUTPUT: Lista de fontes + pergunta que attribution responde     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: IMPLEMENTAR MODELOS (Kaushik)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ First-Touch Attribution                                       │
│   └── "O que trouxe o cliente inicialmente?"                    │
│   └── Campo: first_touch_source                                 │
│   └── Uso: Otimizar awareness/discovery                         │
│                                                                  │
│ □ Last-Touch Attribution                                        │
│   └── "O que converteu o cliente?"                              │
│   └── Campo: last_touch_source                                  │
│   └── Uso: Otimizar conversão                                   │
│                                                                  │
│ □ Comparação First vs Last                                      │
│   └── Se muito diferentes = jornada longa                       │
│   └── Se iguais = jornada curta                                 │
│                                                                  │
│ □ Attribution por CLV (Fader contribution)                      │
│   └── Não só "fonte trouxe 100 clientes"                        │
│   └── Mas "fonte trouxe R$500K em CLV"                          │
│                                                                  │
│ OUTPUT: v_attribution_funnel funcionando                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: REFERRAL ATTRIBUTION (Sean Ellis)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Rastrear cadeia de indicação                                  │
│   └── Quem indicou quem?                                        │
│   └── Qual o viral coefficient por cohort?                      │
│                                                                  │
│ □ Medir qualidade de referrals                                  │
│   └── CLV de indicados vs outros canais                         │
│   └── Retention de indicados vs outros                          │
│   └── Completion rate de indicados vs outros                    │
│                                                                  │
│ □ Otimizar programa de referral                                 │
│   └── Quando pedir indicação? (timing)                          │
│   └── Qual incentivo funciona?                                  │
│   └── Qual mensagem converte?                                   │
│                                                                  │
│ OUTPUT: Referral como canal otimizado e rastreado               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 4: REPORTING (Kaushik - So What)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Report mensal de Attribution                                  │
│   └── SO WHAT: "Referral traz 40% dos clientes com 2x CLV"      │
│   └── WHAT CHANGED: "Paid caiu 20% em eficiência"               │
│   └── WHY: "Saturação de audiência no Meta"                     │
│   └── NOW WHAT: "Mover 30% budget de Paid → Referral program"   │
│                                                                  │
│ OUTPUT: Report que gera decisão de alocação                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## WORKFLOW 4: COHORT ANALYSIS

### Objetivo
Entender comportamento e valor por grupo de clientes.

### Clones Envolvidos
- **Primário:** Peter Fader (cohort por valor)
- **Secundário:** Sean Ellis (cohort por viralidade)
- **Secundário:** Wes Kao (cohort por learning outcomes)
- **Terciário:** Avinash Kaushik (apresentação)

### Passo a Passo

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: DEFINIR COHORTS (Fader + Ellis)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Cohort por mês de aquisição                                   │
│   └── Jan/24, Feb/24, Mar/24...                                 │
│   └── Comparar retention mês-a-mês                              │
│                                                                  │
│ □ Cohort por produto                                            │
│   └── Comunidade Lendár[IA]                                     │
│   └── Gestor IA                                                 │
│   └── Formação Lendária                                         │
│   └── Mastermind                                                │
│                                                                  │
│ □ Cohort por source (Ellis)                                     │
│   └── Referral vs Paid vs Organic                               │
│   └── Comparar retention e CLV                                  │
│                                                                  │
│ □ Cohort por completion (Kao)                                   │
│   └── Completou curso vs Não completou                          │
│   └── Comparar renewal e referral                               │
│                                                                  │
│ OUTPUT: Definição de cohorts relevantes                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: CALCULAR MÉTRICAS (Fader + Kao)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Retention por cohort                                          │
│   └── Mês 1, 2, 3... retention                                  │
│   └── Identificar onde drop acontece                            │
│                                                                  │
│ □ CLV por cohort (Fader)                                        │
│   └── Qual cohort gera mais valor?                              │
│   └── Qual cohort tem melhor trajetória?                        │
│                                                                  │
│ □ Completion por cohort (Kao)                                   │
│   └── Qual cohort completa mais?                                │
│   └── Correlação completion → renewal                           │
│                                                                  │
│ □ Viralidade por cohort (Ellis)                                 │
│   └── Qual cohort indica mais?                                  │
│   └── K factor por cohort                                       │
│                                                                  │
│ OUTPUT: v_cohort_analysis com métricas                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: DIAGNÓSTICO (Todos)                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Por que cohort X é pior?                                      │
│   └── Mudança no produto? (Mehta)                               │
│   └── Mudança na aquisição? (Ellis)                             │
│   └── Mudança no curso? (Kao)                                   │
│   └── Mudança na comunidade? (Spinks)                           │
│                                                                  │
│ □ Ações corretivas                                              │
│   └── Cohort problemático = intervenção específica              │
│   └── Cohort bom = replicar condições                           │
│                                                                  │
│ OUTPUT: Diagnóstico por cohort + ações                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## WORKFLOW 5: AUMENTAR COMPLETION RATE (3% → 80%)

### Objetivo
Transformar curso com 3% completion em programa com 80%+.

### Clones Envolvidos
- **Primário:** Wes Kao
- **Secundário:** David Spinks (community elements)
- **Secundário:** Nick Mehta (student health)

### Passo a Passo

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: DIAGNÓSTICO (Wes Kao)                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Identificar onde drop acontece                                │
│   └── Quantos nunca começam?                                    │
│   └── Quantos param no módulo 1?                                │
│   └── Quantos param no meio?                                    │
│   └── Quantos param quase no fim?                               │
│                                                                  │
│ □ Identificar causa do drop                                     │
│   └── Falta de urgência (sem deadline)                          │
│   └── Falta de accountability (sozinho)                         │
│   └── Falta de engajamento (vídeo passivo)                      │
│   └── Falta de commitment (preço baixo)                         │
│   └── Conteúdo muito longo/complexo                             │
│                                                                  │
│ □ Survey com quem dropou                                        │
│   └── "Por que você parou?"                                     │
│   └── "O que faria você continuar?"                             │
│                                                                  │
│ OUTPUT: Diagnóstico claro do problema                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: REDESIGN (Wes Kao)                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Adicionar elementos de CBC                                    │
│   └── Fixed start/end dates                                     │
│   └── Cohort (turmas simultâneas)                               │
│   └── Live sessions (ao menos 1/semana)                         │
│   └── Peer accountability                                       │
│                                                                  │
│ □ Redesign de sessões (State Change Method)                     │
│   └── Alternar modalidades a cada 5-10 min                      │
│   └── Lecture → Poll → Breakout → Share → Q&A                   │
│                                                                  │
│ □ Adicionar deliverables                                        │
│   └── Projeto prático obrigatório                               │
│   └── Peer feedback                                             │
│   └── Showcase final                                            │
│                                                                  │
│ □ Revisar pricing                                               │
│   └── Preço mais alto = mais commitment                         │
│   └── Considerar R$500-2000 vs atual                            │
│                                                                  │
│ OUTPUT: Novo design de curso                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: COMMUNITY ELEMENTS (David Spinks)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Criar comunidade do cohort                                    │
│   └── Slack/Discord do cohort                                   │
│   └── Rituais de conexão                                        │
│   └── Pair programming / study buddies                          │
│                                                                  │
│ □ Alumni community                                              │
│   └── Graduados ajudam novos                                    │
│   └── Networking contínuo                                       │
│   └── Eventos exclusivos                                        │
│                                                                  │
│ OUTPUT: Elementos de community integrados                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 4: STUDENT HEALTH (Nick Mehta adaptado)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Criar "Student Health Score"                                  │
│   └── Attendance (30%)                                          │
│   └── Assignment completion (30%)                               │
│   └── Community participation (20%)                             │
│   └── Progress pace (20%)                                       │
│                                                                  │
│ □ Alertas de stall                                              │
│   └── 3 dias sem atividade → Nudge automático                   │
│   └── Faltou live → Outreach pessoal                            │
│   └── Assignment atrasado → Oferta de ajuda                     │
│                                                                  │
│ OUTPUT: Sistema de early warning para students                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 5: MÉTRICAS E ITERAÇÃO (Kao + Kaushik)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ □ Métricas de processo                                          │
│   └── Completion rate (meta: 80%)                               │
│   └── Attendance rate (meta: 85%)                               │
│   └── NPS (meta: 70+)                                           │
│                                                                  │
│ □ Métricas de outcome                                           │
│   └── % que atingiu objetivo declarado                          │
│   └── % que indicou após completar                              │
│   └── % que comprou próximo produto                             │
│                                                                  │
│ □ Iteração                                                      │
│   └── Rodar cohort piloto                                       │
│   └── Coletar feedback intenso                                  │
│   └── Ajustar antes de escalar                                  │
│                                                                  │
│ OUTPUT: Curso validado pronto para escala                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## WORKFLOW 6: OTIMIZAR COMUNIDADE

### Objetivo
Aumentar engajamento e ROI da comunidade.

### Clones Envolvidos
- **Primário:** David Spinks
- **Secundário:** Nick Mehta (adaptar health para community)
- **Secundário:** Wes Kao (learning in community)

### Passo a Passo

```
FASE 1: DIAGNÓSTICO (Spinks)
├── □ Medir métricas atuais (MAU, DAU, stickiness)
├── □ Identificar SPACES gaps (qual valor está faltando?)
├── □ Entrevistar membros ativos vs inativos
└── OUTPUT: Diagnóstico de saúde da comunidade

FASE 2: ESTRATÉGIA (Spinks)
├── □ Definir proposta de valor clara
├── □ Identificar "primeiro valor" (o que traz de volta?)
├── □ Criar programming calendar
└── OUTPUT: Estratégia de community

FASE 3: MÉTRICAS (Spinks + Mehta)
├── □ Community Health Score
├── □ Alertas de drop de engajamento
├── □ ROI tracking
└── OUTPUT: Sistema de medição

FASE 4: LEARNING ELEMENTS (Kao)
├── □ Integrar cursos na community
├── □ Learning paths coletivos
├── □ Peer teaching
└── OUTPUT: Community-led learning
```

---

*Framework de Clones - Data Intelligence Pack v2.0*
*Workflows*
