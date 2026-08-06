---
task: "Define ICP"
responsavel: "@commercial-intelligence"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - client_business_context
  - product_value_prop
Saida: |
  - icp_definition
  - decision_maker_personas
Checklist:
  - "[ ] Levantar segmento, porte, faturamento, localizacao e maturidade digital do cliente ideal"
  - "[ ] Levantar tecnologias, CRM e ERP tipicamente usados pelo ICP"
  - "[ ] Definir persona de cada decisor (cargo, dores, objetivos, criterio de decisao)"
  - "[ ] Definir sinal de fit e sinal de desqualificacao (anti-ICP)"
  - "[ ] Validar o ICP contra os clientes de maior sucesso ja existentes"
  - "[ ] Publicar o ICP e as personas para uso do SDR e do Closer"
---

# *define-icp

## Objetivo

Documentar o Perfil de Cliente Ideal e as personas de decisor a partir de dado real,
não de aspiração — o ICP orienta toda a priorização de `@sdr` e `@closer` a partir daqui.

## Procedimento

1. Levantar o contexto de negócio do cliente (`client_business_context`) e a proposta de
   valor do produto (`product_value_prop`) — sem isso, ICP vira chute.
2. Olhar para a base de clientes existentes, quando houver, e identificar o padrão nos
   que tiveram maior sucesso, menor churn ou maior ticket — esse é o ICP real, não o
   ICP aspiracional ("quem eu gostaria de vender").
3. Documentar os campos firmográficos: segmento, porte (funcionários/faturamento),
   localização, maturidade digital, tecnologias usadas, CRM, ERP.
4. Para cada persona de decisor envolvida na compra, documentar: cargo, dor principal,
   objetivo de negócio, critério de decisão típico e onde ela costuma buscar informação.
5. Definir sinais de fit positivo (o que indica bom encaixe) e sinais de anti-ICP (o que
   desqualifica de cara — ex.: porte pequeno demais para o ticket mínimo, segmento
   regulado que o produto não atende).
6. Validar o ICP rascunhado contra 3-5 casos reais de sucesso — se não bater com os
   melhores clientes atuais, revisar antes de publicar.
7. Publicar como documento vivo e versionado — ICP não se define uma vez e se esquece;
   revisitar a cada ciclo relevante ou quando `*recover-lost-opportunity` apontar
   padrão de desalinhamento.

## Modelo de campos ICP

| Campo | Valor |
|---|---|
| Segmento | |
| Porte (funcionários) | |
| Faturamento | |
| Localização | |
| Maturidade digital | |
| Tecnologias usadas | |
| CRM | |
| ERP | |
| Sinal de fit | |
| Sinal de anti-ICP | |

## Erros comuns a evitar

- ICP aspiracional em vez de ICP baseado nos clientes que realmente têm sucesso.
- ICP genérico demais para orientar priorização real de `*score-lead-fit`.
- Nunca revisitar o ICP mesmo com sinal recorrente de desalinhamento vindo do funil.

## Usage

```
@commercial-intelligence
*define-icp
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `client_business_context` | string | Yes | client business context |
| `product_value_prop` | string | Yes | product value proposition |

## Output

- **icp_definition**: ICP definition (segmento, porte, faturamento, localizacao, tecnologias, maturidade)
- **decision_maker_personas**: decision maker personas

## Origin

Confidence: 92%
