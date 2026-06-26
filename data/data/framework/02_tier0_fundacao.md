# Framework de Clones - Data Intelligence Pack
## 02 - Tier 0: Fundação

---

## PRINCÍPIOS INEGOCIÁVEIS

Antes de usar qualquer clone, internalize estes princípios:

### Princípio 1: Métrica sem Decisão é Ruído

```
ERRADO: "Vamos medir tudo e ver o que aparece"
CERTO:  "Qual decisão esta métrica vai informar?"
```

Toda métrica no Data Intelligence Pack deve responder:
- **Quem** vai olhar para isso?
- **Quando** vai olhar?
- **Que ação** vai tomar baseado no número?

Se não conseguir responder, não implemente.

---

### Princípio 2: Sequência Importa

```
ERRADO: Implementar Health Score → depois definir quem importa
CERTO:  Definir quem importa (CLV) → depois criar Health Score
```

A ordem correta é sempre:

1. **Fundamentação** (Camada 1) - Quem são os clientes que importam?
2. **Operacionalização** (Camada 2) - Como monitorar esses clientes?
3. **Comunicação** (Camada 3) - Como apresentar para gerar ação?

---

### Princípio 3: Clone Certo para Pergunta Certa

Cada clone tem um domínio específico. Usar o clone errado gera resposta errada.

| Clone | Domínio | NÃO usar para |
|-------|---------|---------------|
| Peter Fader | Valor do cliente, segmentação | Alertas operacionais |
| Sean Ellis | Crescimento viral, referral | Análise financeira |
| Nick Mehta | Saúde do cliente, churn | Estratégia de aquisição |
| David Spinks | Comunidade, engajamento | Cálculos de CLV |
| Wes Kao | Educação, completion rate | Métricas de produto SaaS |
| Avinash Kaushik | Attribution, storytelling | Sistemas de alerta |

---

### Princípio 4: Heterogeneidade é Feature, não Bug

Nem todo cliente merece o mesmo tratamento. Isso não é cruel, é estratégico.

```
ERRADO: "Tratamos todos os clientes igualmente"
CERTO:  "Tratamos clientes proporcionalmente ao valor que geram/podem gerar"
```

Peter Fader chama isso de **Customer Centricity** - focar recursos nos clientes de maior valor atual e potencial.

---

### Princípio 5: Comunidade ≠ Audiência

```
AUDIÊNCIA: Consumidores passivos de conteúdo
COMUNIDADE: Membros que interagem entre si
```

David Spinks ensina que comunidade só existe quando há:
- Conexão membro-a-membro (não só marca-a-membro)
- Identidade compartilhada
- Senso de pertencimento

Se seus "membros" só consomem e não interagem, você tem audiência.

---

### Princípio 6: Completion ≠ Learning

```
ERRADO: "95% completaram o curso = sucesso"
CERTO:  "X% aplicaram e tiveram resultado = sucesso"
```

Wes Kao ensina que completion rate é proxy, não outcome. O que importa é:
- Transformação real do aluno
- Aplicação prática do conteúdo
- Resultado mensurável pós-curso

---

## ANTI-PATTERNS COMUNS

### Anti-Pattern 1: Dashboard Frankenstein

**Sintoma:** Dashboard com 47 métricas de 12 fontes diferentes.

**Causa:** Cada departamento pediu "suas" métricas.

**Solução:** Voltar para Fundamentação (Fader) e definir North Star Metric (Ellis).

---

### Anti-Pattern 2: Health Score Copiado

**Sintoma:** Health Score com pesos idênticos ao template do software.

**Causa:** Não definiu quais comportamentos predizem sucesso no SEU contexto.

**Solução:** Consultar Nick Mehta (DEAR framework) + calibrar com dados reais.

---

### Anti-Pattern 3: Comunidade Fantasma

**Sintoma:** 10.000 membros, 50 ativos.

**Causa:** Focou em aquisição sem definir proposta de valor para participação.

**Solução:** Consultar David Spinks (SPACES model) para definir por que alguém participaria.

---

### Anti-Pattern 4: Curso Cemitério

**Sintoma:** 3% completion rate, conteúdo excelente.

**Causa:** Modelo self-paced sem accountability ou comunidade.

**Solução:** Consultar Wes Kao para redesign cohort-based ou adicionar elementos de engajamento.

---

### Anti-Pattern 5: Attribution Theater

**Sintoma:** Relatórios bonitos de attribution que ninguém usa para decisão.

**Causa:** Modelo não conectado com ações reais de marketing.

**Solução:** Consultar Avinash Kaushik (DMMM) para alinhar métricas com decisões.

---

### Anti-Pattern 6: Referral Forçado

**Sintoma:** Programa de indicação que ninguém usa.

**Causa:** Incentivo errado ou timing errado no lifecycle do cliente.

**Solução:** Consultar Sean Ellis (viral coefficient) + mapear momento ideal para ask.

---

## CHECKLIST PRÉ-IMPLEMENTAÇÃO

Antes de implementar qualquer funcionalidade do Data Intelligence Pack:

```
□ Defini qual decisão esta métrica vai informar
□ Identifiquei quem vai olhar e quando
□ Consultei pelo menos 1 clone da Camada 1 (Fundamentação)
□ Sei qual ação será tomada baseada no resultado
□ Tenho baseline para comparação
□ Defini frequência de revisão
```

Se algum item está em branco, volte para a Fundamentação.

---

## GLOSSÁRIO BASE

| Termo | Definição | Clone Referência |
|-------|-----------|------------------|
| **CLV** | Customer Lifetime Value - valor total esperado de um cliente | Peter Fader |
| **RFM** | Recency, Frequency, Monetary - modelo de segmentação comportamental | Peter Fader |
| **Viral Coefficient** | Quantos novos usuários cada usuário traz | Sean Ellis |
| **North Star Metric** | Métrica única que captura valor core entregue | Sean Ellis |
| **Health Score** | Índice composto de saúde do cliente | Nick Mehta |
| **DEAR** | Deployment, Engagement, Adoption, ROI | Nick Mehta |
| **MAU/DAU** | Monthly/Daily Active Users | David Spinks |
| **SPACES** | Support, Product, Acquisition, Content, Engagement, Success | David Spinks |
| **CBC** | Cohort-Based Course | Wes Kao |
| **Completion Rate** | % de alunos que terminam o curso | Wes Kao |
| **DMMM** | Digital Marketing & Measurement Model | Avinash Kaushik |
| **Attribution** | Atribuição de conversão a touchpoints | Avinash Kaushik |

---

*Framework de Clones - Data Intelligence Pack v2.0*
*Tier 0: Fundação*
