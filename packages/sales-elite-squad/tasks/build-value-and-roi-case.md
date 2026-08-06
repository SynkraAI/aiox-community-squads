---
task: "Build Value and ROI Case"
responsavel: "@closer"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - discovery_findings
  - product_value_prop
  - pricing_model
Saida: |
  - roi_case
  - value_proposition_deck
Checklist:
  - "[ ] Traduzir a dor levantada em custo atual mensuravel para o cliente"
  - "[ ] Calcular ganho esperado com premissa explicita e defensavel"
  - "[ ] Comparar custo de nao agir contra o investimento proposto"
  - "[ ] Adaptar a linguagem do caso ao perfil comportamental do decisor"
  - "[ ] Evitar numero de efeito sem base de calculo"
  - "[ ] Revisar o caso com o criterio de decisao levantado na descoberta"
---

# *build-value-and-roi-case

## Objetivo

Traduzir a dor confirmada na descoberta em um caso de valor e ROI calculável e
defensável — nunca um número de efeito sem base.

## Procedimento

1. Pegar cada dor confirmada em `discovery_findings` e traduzir em custo atual: tempo
   perdido, receita não capturada, risco assumido ou custo direto — sempre na métrica que
   o próprio cliente usa (o "Metrics" do MEDDICC).
2. Calcular o ganho esperado com premissas explícitas e nomeadas (ex.: "assumindo 10% de
   melhora em X, com base em [dado ou caso análogo]") — nunca apresentar número sem
   mostrar a conta por trás dele.
3. Montar a comparação: custo de não agir (manter o status quo por 6-12 meses) versus o
   investimento proposto, na unidade que o cliente entende (R$, horas, %).
4. Adaptar a apresentação ao perfil comportamental do decisor:
   - **Analítico** → planilha e detalhamento do cálculo.
   - **Dominante** → resumo de 1 página com o número final e o payback.
   - **Influente** → narrativa com caso de outro cliente parecido.
   - **Estável** → comparação passo a passo, com garantias e mitigação de risco.
5. Revisar o caso contra o `decision_criteria` levantado na descoberta — se o critério
   do cliente é "redução de risco" e o caso só fala de ganho de receita, ele não vai
   convencer, por mais correto que o número esteja.
6. Nunca prometer resultado que não pode ser sustentado — diferenciar projeção
   (hipótese, com premissa explícita) de garantia contratual (fato, assumido por escrito).

## Fórmula de referência

```
ROI = (Ganho estimado - Investimento) / Investimento
Payback (meses) = Investimento / Ganho mensal estimado
```

## Erros comuns a evitar

- Apresentar ganho percentual sem dizer sobre qual base ele é calculado.
- Usar um caso de sucesso de cliente com contexto muito diferente do atual sem ressalva.
- Ignorar o critério de decisão levantado e insistir no ângulo que o Closer prefere.

## Usage

```
@closer
*build-value-and-roi-case
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `discovery_findings` | string | Yes | discovery findings |
| `product_value_prop` | string | Yes | product value proposition |
| `pricing_model` | string | Yes | pricing model |

## Output

- **roi_case**: caso de ROI calculavel e defensavel
- **value_proposition_deck**: value proposition deck

## Origin

Confidence: 82%
