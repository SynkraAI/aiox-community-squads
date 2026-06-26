# Delete Brand Squad Component

## Task Identity

```yaml
task_id: delete-brand
task_name: "Delete Brand Squad Component"
version: "1.0.0"
squad: brand
executor: brand-chief
elicit: true
```

## Purpose

Remover componentes do squad de brand de forma segura, garantindo que referências cruzadas sejam atualizadas.

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| component_type | enum | yes | agent, workflow, task |
| component_name | string | yes | Nome do componente a remover |
| reason | string | yes | Motivo da remoção |

## Steps

1. **Impact Analysis**: Verificar quem referencia o componente
2. **Plan**: Listar todas as mudanças necessárias (config, workflows, README)
3. **Elicit**: Confirmar com usuário mostrando impacto
4. **Backup**: Copiar componente antes de remover
5. **Remove**: Deletar arquivo do componente
6. **Update References**: Atualizar config.yaml, workflows, README
7. **Validate**: Rodar `*validate-squad brand`
8. **Changelog**: Registrar remoção

## Veto Conditions

- Remover entry_agent (brand-chief) sem substituto
- Remover agente referenciado em workflow ativo sem atualizar workflow
- Remover sem backup

## Output

- Componente removido
- Referências atualizadas
- CHANGELOG.md com entry
- Validação PASS

## Completion Criteria

- [ ] Componente removido do filesystem
- [ ] Zero referências quebradas
- [ ] config.yaml atualizado
- [ ] CHANGELOG.md atualizado
- [ ] `*validate-squad brand` PASS
