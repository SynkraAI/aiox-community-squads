# SWARM.4 Permission Sync - Transition Plan

Este documento fornece as diretrizes operacionais para a integração da lógica de Permission Sync (agent-authority.md -> allowedTools) dentro do modo Swarm OS do Claude Code. 

## 1. O que é o Dry-Run Mode (estado atual)
O script `generate-tool-allowlists.js` operando via hook em `PreToolUse` analisa cada ferramenta executada pelo agent e verifica contra a authority configuration definida em `.claude/rules/agent-authority.md`. 
Atualmente, estamos operando em modo **DRY-RUN DEFAULT**. Isso significa que as violações são APENAS reportadas para log analítico, e nenhuma ferramenta é de fato bloqueada, mantendo o ambiente vivo enquanto o pipeline se adapta às políticas rígidas (BR-COORD-013).

## 2. Como ler os Logs de Violação (Dry-Run Logs)
Os logs de telemetria analítica contendo infrações são salvos centralmente em:
`.logs/permission-sync/violations.jsonl`

Exemplo de linha do log original:
```json
{"timestamp":"2026-03-27T10:00:00.000Z","agent":"dev","tool":"Bash","action":"would_block","reason":"Command blocked by agent-authority for role @dev: Bash(gh pr*)","command":"gh pr status"}
```
A propriedade `action: "would_block"` indica que o comando *teria sido bloqueado* pelo Enforcement Híbrido se ele estivesse online, mas por hora passou ileso.

## 3. Como ativar o Enforcement (Block verdadeiro)
O enforcement não é gerido por variáveis de ambiente voláteis, e sim na raiz de configuração da Core em:
`.aiox-core/core-config.yaml`

Para habilitar a trava de Kernel:
1. Abra `.aiox-core/core-config.yaml` e procure a chave da hierarquia Swarm OS.
2. Alterne de `swarm_permission_enforcement: false` para `swarm_permission_enforcement: true`.
3. Gere o allowlists: `node squads/claude-code-mastery/scripts/generate-tool-allowlists.js --generate`

Após esse processo, o campo `action` nos logs passará a registrar `"blocked"` e as execuções de tools não-autorizados retornarão uma resposta de "permissionDecisionReason" com payload `deny` forçando parada.

## 4. O que fazer se as coisas quebrarem (Rollback)
Se workflows legítimos do AIOX passarem a quebrar com a trava Native SWARM ativada, faça downgrade sumário:
1. Altere novamente `swarm_permission_enforcement: true` para `false` no seu arquivo `core-config.yaml`.
2. O sistema reverterá automaticamente e transparentemente para modo DRY-RUN.
3. Não há necessidade de reinicializar instâncias ativas do Claude Code CLI devido ao Hook ser consumido context-free a cada prompt.

## 5. Hook Dedup (Duplicação resolvido)
Uma das maiores fricções (RISK-5) ocorria no fato desta flag gerar duplicidade com hooks pré-existentes como o `enforce-git-push-authority.sh`. 
Isto está resolvido sob o **AC12**: A função de log ignora comandos atrelados ao `git push`, passando a gestão integral disso para a root hook legada sem causar lock triplo no `PreToolUse`.
