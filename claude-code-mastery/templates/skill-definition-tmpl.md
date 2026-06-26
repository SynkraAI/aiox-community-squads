version: "1.1.0"
artifact_id: skill-definition
lifecycle: draft

# Definição de Skill

## Objetivo
- problema:
- resultado_esperado:
- modo:
- superfície: skill | command | plugin-skill

## Contrato de Runtime
- diretório_alvo:
- tipo_de_ativação: always-on | conditional_paths | manual_only | plugin_only
- context_mode: inline | fork
- agent:
- user_invocable:
- disable_model_invocation:
- allowed_tools:
- model:
- effort:
- shell:
- runtime_fields_obrigatórios:
  - name
  - description
- runtime_fields_opcionais:
  - when_to_use
  - arguments
  - argument-hint
  - version
  - hooks
  - paths

## Campos Opcionais (CC-native)
- license:
- allowed-tools:
- model:
- effort:
- maxTurns:

> NOTA: owner_squad e sinkra_tier são PROIBIDOS em skills (Frontmatter Purity Rule). Pertencem a tasks.

## Descoberta e Roteamento
- should_trigger:
- should_not_trigger:
- description:
- when_to_use:
- paths:
- risco_de_ambiguidade:
- orçamento_de_contexto:

## Implementação
- skill_md_outline:
- arquivos_de_apoio:
- scripts:
- references:
- assets:
- placeholders_e_substituições:
  - $ARGUMENTS
  - ${CLAUDE_SKILL_DIR}
  - ${CLAUDE_SESSION_ID}

## Validação
- prompts_de_teste:
- checagens:
- observações:
