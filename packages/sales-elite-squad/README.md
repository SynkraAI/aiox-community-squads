# sales-elite-squad

Squad comercial completa: inteligencia de mercado, prospeccao (SDR), fechamento (Closer),
gestao de pipeline e customer success — reunindo, em cinco agentes especializados, as
competencias de SDR, Closer, Gestor Comercial, leitura de perfil comportamental (RH/DISC)
e PNL etica aplicada a comunicacao persuasiva.

Um unico "vendedor de IA" tende a virar generico. Esta squad divide o trabalho como uma
operacao comercial real, com cada agente focado numa etapa do ciclo e compartilhando
contexto — ICP, score de lead, perfil comportamental, achados de descoberta — de agente
para agente.

## Escopo

A squad **nao** duplica discovery de produto, arquitetura ou desenvolvimento — isso segue
com o core do projeto (`@analyst`, `@pm`, `@architect`, `@dev`, etc., conforme a squad
principal do seu setup). Esta squad cobre especificamente o ciclo comercial: da pesquisa
de mercado ate a expansao e retencao do cliente.

Justificativa e mapa completo de responsabilidade: `docs/squads/sales-elite-squad-brief.md`.

## Agentes

| Agente | Persona | Papel | Comandos |
|---|---|---|---|
| `@commercial-intelligence` | Orion | Inteligencia Comercial e Growth | 6 |
| `@sdr` | Aris | SDR — Prospeccao e Qualificacao | 6 |
| `@closer` | Kai | Closer — Descoberta, Negociacao e Fechamento | 6 |
| `@sales-manager` | Sol | Gestao Comercial e Pipeline | 6 |
| `@customer-success` | Iara | Customer Success e Expansao | 6 |

## Ponto de acoplamento no ciclo

```text
@commercial-intelligence *define-icp → *build-prospect-list → *score-lead-fit
    → @sdr *build-outreach-cadence → *write-cold-outreach → *qualify-lead-bant → *book-meeting
        → @closer *plan-discovery-meeting → *run-needs-discovery → *build-value-and-roi-case
            → *negotiate-and-close
                → @customer-success *plan-onboarding → *monitor-customer-health → *plan-renewal
    → @sales-manager *analyze-pipeline-health / *build-sales-forecast / *run-pipeline-review-gate
      (roda em paralelo, olhando o funil inteiro)
```

`@sales-manager` audita o pipeline transversalmente; `@customer-success` retoma o cliente
apos o fechamento e pode devolver oportunidade de expansao ao `@closer`.

## Tasks

#### `@commercial-intelligence`

- `*define-icp` — Definir e documentar o Perfil de Cliente Ideal (ICP) e as personas de decisor
- `*map-market-and-competitors` — Mapear mercado, concorrentes diretos/indiretos e posicionamento
- `*build-prospect-list` — Gerar lista qualificada de empresas e decisores a partir do ICP
- `*identify-buying-triggers` — Identificar gatilhos de compra (eventos, contratacoes, expansao, tecnologia)
- `*score-lead-fit` — Pontuar fit e temperatura de cada lead da lista (0-100)
- `*analyze-pricing-and-positioning` — Analisar preco, valor percebido e posicionamento competitivo

#### `@sdr`

- `*build-outreach-cadence` — Criar cadencia multicanal (e-mail, WhatsApp, LinkedIn, telefone)
- `*write-cold-outreach` — Escrever mensagens de prospeccao para um lead especifico
- `*profile-behavioral-style` — Analisar perfil comportamental (DISC) e estilo de comunicacao do decisor
- `*qualify-lead-bant` — Qualificar o lead com BANT/GPCT e atribuir nota de probabilidade de compra
- `*handle-prospecting-objections` — Mapear objecoes de prospeccao e como responder
- `*book-meeting` — Conduzir a conversa ate o agendamento e fazer o handoff para o Closer

#### `@closer`

- `*plan-discovery-meeting` — Preparar plano de reuniao com perguntas SPIN/Challenger
- `*run-needs-discovery` — Conduzir descoberta de dor, orcamento, autoridade, urgencia
- `*build-value-and-roi-case` — Construir caso de valor e ROI personalizado
- `*handle-sales-objections` — Mapear objecoes de fechamento e roteiro de resposta consultiva
- `*negotiate-and-close` — Conduzir a negociacao final e o plano de fechamento
- `*recover-lost-opportunity` — Criar plano de recuperacao para oportunidade perdida ou estagnada

#### `@sales-manager`

- `*analyze-pipeline-health` — Analisar saude do pipeline por estagio e detectar gargalos
- `*calculate-commercial-metrics` — Calcular CAC, LTV, ticket medio, conversao e ciclo de venda
- `*build-sales-forecast` — Construir forecast de vendas com cenarios e nivel de confianca
- `*audit-funnel-conversion` — Auditar a conversao entre etapas do funil e propor correcoes
- `*coach-sales-rep` — Analisar uma conversa e devolver plano de coaching individual
- `*run-pipeline-review-gate` — Emitir verdict de saude do pipeline — FAIL bloqueia forecast em risco CRITICAL/HIGH

#### `@customer-success`

- `*plan-onboarding` — Planejar onboarding com marcos de valor e responsaveis
- `*monitor-customer-health` — Definir e monitorar o health score do cliente
- `*identify-expansion-opportunity` — Identificar oportunidades de upsell e cross-sell
- `*plan-renewal` — Preparar estrategia de renovacao e prevencao de churn
- `*request-referral` — Estruturar pedido de indicacao no momento certo
- `*run-churn-risk-gate` — Emitir verdict de risco de churn — FAIL aciona plano de resgate imediato

## Metodo compartilhado

Todos os agentes seguem `templates/opportunity-diagnostic.md` ao analisar uma conta ou
oportunidade especifica: a sequencia mental de 10 passos, os campos de ICP, a leitura de
perfil comportamental (DISC), a escala de qualificacao 0-100, a estrutura de resposta
padrao (Diagnostico → Perfil → Dores → Oportunidades → Estrategia → Script → Perguntas →
Objecoes → Proxima Melhor Acao → Probabilidade de Fechamento → Recomendacoes) e as regras
de PNL etica.

**PNL etica**: usada apenas para clareza, empatia e rapport. Nunca para manipular, criar
urgencia falsa ou pressionar contra o interesse do interlocutor. Fato, hipotese e
recomendacao sao sempre rotulados separadamente — nenhum agente inventa dado sobre lead,
empresa ou mercado.

## Instalacao

Squad local do projeto:

```
./squads/sales-elite-squad/
```

## Configuracao

Estende a configuracao do aiox-core (`config.extends: extend`). Os arquivos locais em
`config/` sao placeholders — se o projeto passar a ter `docs/framework/`, reaponte o
bloco `config:` do `squad.yaml` para la.

## Estado

As 30 tasks tem frontmatter completo (Entrada, Saida, Checklist) e corpo preenchido com
procedimento passo a passo, modelo/formato de saida e erros comuns a evitar — o
checklist de cada uma e o contrato executavel; o corpo e o metodo concreto por tras dele.

O que ainda falta e a integracao real com as ferramentas do seu stack: CRM, provedor de
e-mail outbound, WhatsApp Business API, LinkedIn Sales Navigator, discador, e a fonte de
dado real por tras de pipeline_data, product_usage_data, revenue_data etc. — os
procedimentos descrevem o metodo, nao a integracao tecnica.

## Validacao

```
@squad-creator *validate-squad sales-elite-squad
@squad-creator *analyze-squad sales-elite-squad
```

## Licenca

MIT
