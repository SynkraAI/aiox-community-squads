# Data Knowledge Base

## Propósito

Este diretório concentra a **base de conhecimento de referência** do squad `data`.
Aqui ficam apenas artefatos estáveis usados para orientar agentes, tasks, workflows
e decisões de modelagem analítica.

Regra prática:

- `data/` = conhecimento canônico, frameworks, matrizes, referência
- `templates/` = contratos de saída
- `tasks/` = execução
- `workflows/` = orquestração
- `docs/` = não permitido dentro deste squad

## Conteúdo Atual

```text
data/
├── README.md
└── framework/
    ├── 01_arquitetura_geral.md
    ├── 02_tier0_fundacao.md
    ├── 03_tier0_fundamentadores.md
    ├── 04_tier1_operacionalizadores.md
    ├── 05_tier2_comunicadores.md
    ├── 06_matriz_decisao.md
    ├── 07_workflows.md
    └── 08_cheatsheet.md
```

## Como Usar

Ordem recomendada de leitura:

1. `framework/01_arquitetura_geral.md`
   Define a estrutura do pack, os 3 tiers e a regra de ouro.
2. `framework/02_tier0_fundacao.md`
   Explica princípios inegociáveis e anti-padrões.
3. `framework/03_tier0_fundamentadores.md`
   Referência para Peter Fader e Sean Ellis.
4. `framework/04_tier1_operacionalizadores.md`
   Referência para Nick Mehta, David Spinks e Wes Kao.
5. `framework/05_tier2_comunicadores.md`
   Referência para Avinash Kaushik.
6. `framework/06_matriz_decisao.md`
   Atalho para escolher o clone certo por pergunta, stakeholder ou funcionalidade.
7. `framework/07_workflows.md`
   Versão de referência dos fluxos macro do pack.
8. `framework/08_cheatsheet.md`
   Resumo rápido para ativação e consulta operacional.

## Critérios de Permanência em `data/`

Um arquivo só deve existir neste diretório se cumprir pelo menos um destes critérios:

- define framework, heurística, taxonomia ou matriz de decisão reutilizável
- serve como referência estável para múltiplos agents/tasks/workflows
- representa conhecimento do domínio `data` que não depende de execução de uma task específica

Um arquivo **não** deve existir em `data/` se for:

- relatório de execução
- output temporário
- handoff de sessão
- diagnóstico pontual
- documentação operacional duplicada do que já vive em `README`, `tasks/` ou `workflows/`

## Política de Manutenção

- Não recriar `docs/` dentro de `squads/data/`.
- Se surgir material de referência novo, preferir adicionar em `data/`.
- Se surgir output de execução, preferir `workspace/businesses/{slug}/analytics/` ou `docs/data/{slug}/`.
- Ao renomear arquivos de framework, atualizar também:
  - `squads/data/config.yaml`
  - `squads/data/README.md`
  - `squads/data/projects/data-v1-setup/prd.json`
  - `squads/data/projects/data-v1-setup/prompt.md`

## Observações

- O conteúdo em `framework/` foi migrado de `docs/framework/` para manter o squad limpo e consistente com a política pedida para este diretório.
- Este README é o índice canônico do knowledge base do squad `data`.
