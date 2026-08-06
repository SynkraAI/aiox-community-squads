---
task: "Build Prospect List"
responsavel: "@commercial-intelligence"
responsavel_type: agent
atomic_layer: task
Entrada: |
  - icp_definition
  - market_map
  - target_volume
Saida: |
  - qualified_company_list
  - decision_maker_contacts
Checklist:
  - "[ ] Buscar empresas que atendem aos criterios de ICP"
  - "[ ] Identificar o decisor e o influenciador em cada empresa"
  - "[ ] Validar dado de contato disponivel e canal de acesso"
  - "[ ] Remover empresa que bate em criterio de anti-ICP"
  - "[ ] Anexar a fonte de cada dado levantado — nunca inventar contato"
  - "[ ] Entregar a lista pronta para o SDR construir a cadencia"
---

# *build-prospect-list

## Objetivo

Gerar a lista de empresas e decisores que batem no ICP, pronta para o SDR construir a
cadência — sem contato inventado ou sem fonte.

## Procedimento

1. Buscar empresas que atendem aos critérios firmográficos do `icp_definition`
   (segmento, porte, localização) usando fontes públicas (LinkedIn/Sales Navigator,
   diretórios setoriais, dados públicos de empresas, o `market_map` já levantado).
2. Para cada empresa, identificar o decisor (persona definida no ICP) e, quando
   possível, um influenciador secundário.
3. Validar que existe canal de contato acessível e confiável (e-mail corporativo,
   perfil de LinkedIn ativo) — descartar registro sem via de acesso real.
4. Aplicar o filtro de anti-ICP definido em `*define-icp` e remover da lista quem bate
   em critério de desqualificação.
5. Anexar a fonte de cada dado da linha — é proibido preencher contato ou informação sem
   fonte rastreável, mesmo que pareça plausível.
6. Entregar a lista formatada e pronta para `@sdr` construir a cadência: empresa,
   decisor, cargo, canal de contato, fonte.

## Modelo de linha da lista

| Empresa | Decisor | Cargo | Canal | Fonte | Observação |
|---|---|---|---|---|---|

## Erros comuns a evitar

- Preencher contato ou cargo "no chute" quando a fonte não confirma o dado.
- Ignorar o filtro de anti-ICP só para bater meta de volume da lista.
- Entregar a lista sem indicar a fonte de cada linha, tornando o dado não auditável.

## Usage

```
@commercial-intelligence
*build-prospect-list
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `icp_definition` | string | Yes | ICP definition |
| `market_map` | string | Yes | market map |
| `target_volume` | number | No | target number of accounts |

## Output

- **qualified_company_list**: qualified company list
- **decision_maker_contacts**: decision maker contacts

## Origin

Confidence: 85%
