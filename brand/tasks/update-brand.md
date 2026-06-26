# Update Brand Squad

## Task Identity

```yaml
task_id: update-brand
task_name: "Update Brand Squad"
version: "1.0.0"
squad: brand
executor: brand-chief
elicit: true
```

## Purpose

Atualizar o squad de brand com novos agentes, workflows, tasks ou correções sem perder estado existente.

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| update_type | enum | yes | agent, workflow, task, config, all |
| target | string | conditional | Nome do componente a atualizar |
| reason | string | yes | Motivo da atualização |

## Steps

1. **Backup**: Copiar estado atual do componente alvo
2. **Diagnose**: Ler componente existente, identificar o que muda
3. **Plan**: Propor mudanças com diff
4. **Elicit**: Confirmar com usuário
5. **Execute**: Aplicar mudanças
6. **Validate**: Rodar `*validate-squad brand` para confirmar integridade
7. **Changelog**: Atualizar CHANGELOG.md com a mudança

## Veto Conditions

- Alterar metodologia de agente sem aprovação explícita
- Remover agente sem justificativa documentada
- Modificar workspace_contract sem validar downstream

## Output

- Componente atualizado
- CHANGELOG.md com entry
- Validação PASS

## Completion Criteria

- [ ] Componente atualizado sem regressão
- [ ] CHANGELOG.md atualizado
- [ ] `*validate-squad brand` PASS
