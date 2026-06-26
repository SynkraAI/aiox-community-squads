# Brand Naming Checklist

**ID:** BR_NAM_001
**Version:** 1.0.0
**Purpose:** Validar qualidade de candidatos de naming antes de apresentar ao cliente
**When:** Após fase de geração em wf-naming-to-domain
**Executor:** naming-strategist

---

## Filtros SNP (Blocking)

| # | Check | Pass | Fail |
|---|-------|------|------|
| 1 | Nome tem no max 3 silabas (ou justificativa para exceção) | [ ] | [ ] |
| 2 | Pronunciavel em português sem ambiguidade | [ ] | [ ] |
| 3 | Sem conotação negativa em PT-BR, ES, EN | [ ] | [ ] |
| 4 | Disponibilidade INPI verificada (classe relevante) | [ ] | [ ] |
| 5 | Domínio .com ou .com.br disponível ou adquirível | [ ] | [ ] |

## Score SMILE/SCRATCH (Warning)

| Criterio | Score (1-5) |
|----------|-------------|
| **S**uggestive - Evoca algo sobre a marca | __ |
| **M**emorable - Fácil de lembrar | __ |
| **I**magery - Gera imagem mental | __ |
| **L**egs - Pode se estender para sub-marcas | __ |
| **E**motional - Conecta emocionalmente | __ |

**Threshold:** >= 15/25 para avançar

## Anti-Patterns

- Nome genérico demais (ex: "Tech Solutions")
- Nome impossível de soletrar por telefone
- Nome que depende de explicação para fazer sentido
- Nome muito similar a concorrente direto

## Scoring

```yaml
blocking: 5 items (all must pass)
warning_threshold: 15/25 SMILE score
result: PASS (all blocking + SMILE >= 15) | CONDITIONAL (all blocking + SMILE < 15) | FAIL (any blocking fails)
```
