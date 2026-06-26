# Task: Domain Check

## Metadata

```yaml
id: domain-check
name: Domain + Handle + INPI Pre-Check
executor: domain-scout
elicit: false
estimated_duration: "10-25 min"
```

**Responsible Executor:** Agent (@domain-scout)  
**Dependencies:** depends_on: `[load-workspace-context, naming-generation]` · enables: `[wf-naming-to-domain]` · workflow: `wf-naming-to-domain`

## Objective

Validar viabilidade digital e legal básica dos nomes candidatos, com prioridade para mercado brasileiro.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| names | list | yes | candidatos aprovados de naming |
| priority_tlds | list | no | prioridade de TLD |
| budget | number | no | budget anual em USD |
| check_social | bool | no | checar handles sociais |
| check_inpi | bool | no | checagem preliminar INPI |

Defaults:
- `priority_tlds`: `[".com.br", ".com", ".io"]`
- `budget`: `150`
- `check_social`: `true`
- `check_inpi`: `true`

---

## Output

| Artifact | Location | Description |
|---|---|---|
| `domain-legal-report.md` | `workspace/businesses/{brand_name}/L2-tactical/brand/naming/domain-legal-report.md` | Viabilidade digital + risco legal preliminar por candidato |
| `domain-decision.yaml` | `workspace/businesses/{brand_name}/L2-tactical/brand/domain-decision.yaml` | Estrutura decisoria para consolidacao do nome/dominio escolhido |

## Execution Steps

### Step 1: Domain availability
- Rodar WHOIS para cada nome + TLD prioritário.
- Marcar status: disponível, ocupado, premium, indefinido.
- **Turbo mode (opcional):** Ativar Vercel MCP `check_domain_availability_and_price` para bulk check com pricing real (até 10 domínios/call).

### Step 2: Pricing estimate
- Estimar faixa de preço por TLD via heurísticas.
- Sinalizar risco premium (palavra de dicionário, 3-4 chars, alta procura).
- **Para preço exato:** Usar Vercel MCP (retorna preço real de registro).

### Step 3: Variations
- Se `.com.br` e `.com` indisponíveis, gerar variações curtas e brand-safe.
- Evitar prefixos/sufixos que desfoquem posicionamento.

### Step 4: Social handles
- Verificar handle equivalente ao nome em Instagram, X/Twitter, LinkedIn e TikTok.

### Step 5: INPI pre-check
- Checagem preliminar manual por termo principal em classes relevantes.
- Classificar: baixo risco, médio risco, alto risco.

### Step 6: Consolidated recommendation
- Entregar ranking final por viabilidade total: legal + digital + custo.

---

## Output Template

```markdown
## Domain & Legal Viability Report

### Candidates
- {nome_1}
- {nome_2}
- {nome_3}

### Availability Matrix
| Nome | .com.br | .com | .io | Handles | INPI risco | Custo estimado/ano |
|---|---|---|---|---|---|---|
| {nome_1} | {status} | {status} | {status} | {ok/parcial/ruim} | {baixo/medio/alto} | ${valor} |
| {nome_2} | {status} | {status} | {status} | {ok/parcial/ruim} | {baixo/medio/alto} | ${valor} |
| {nome_3} | {status} | {status} | {status} | {ok/parcial/ruim} | {baixo/medio/alto} | ${valor} |

### Recommendation
1. {best_name} -> {best_domain}
2. {second_name} -> {second_domain}
3. {third_name} -> {third_domain}

### Notes
- Confirmação jurídica final deve ser feita antes de registrar marca.
```

---

## Veto Conditions

- [ ] Nenhum candidato viável em `.com.br` ou `.com`
- [ ] Todos com risco legal alto no INPI pre-check
- [ ] Custo médio fora do budget definido

---

## Handoff

```yaml
to: brand-chief
pass:
  - ranked_candidates: ["{best_name}", "{second_name}", "{third_name}"]
  - best_domain: "{best_domain}"
  - inpi_risk_summary: "{summary}"
  - social_summary: "{summary}"
```
