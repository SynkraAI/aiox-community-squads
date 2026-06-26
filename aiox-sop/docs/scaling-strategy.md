# Scaling Strategy — aiox-sop Pipeline

> Referência: `axioma_report.md` (Sustentabilidade 6.8/10) | `infrastructure_connections.json`
> Criado: 2026-03-30 | Owner: Tech Lead

---

## Cenários de Carga

| Cenário | SOPs/semana | Status |
|---------|------------|--------|
| **Baseline (atual)** | 3-5 | Operação manual, pré-pipeline |
| **Target (curto prazo)** | 15 | Pipeline operacional — design target |
| **Scale-1 (médio prazo)** | 50 | Multi-squad, crescimento orgânico |
| **Scale-2 (longo prazo)** | 150+ | Enterprise / multi-cliente |

---

## N8N — Orquestrador de Workflows

### Situação atual
Single instance em `https://n8n.allfluence.ai`. Toda orquestração do pipeline depende desta instância (SPOF mapeado como N8N-001 no risk-register).

### Target (15 SOPs/semana)
Single instance é suficiente. Ação requerida:
- Configurar **N8N execution log retention** (30 dias)
- Ativar **error workflow global** — alert automático no `slack-devops` em qualquer falha de workflow
- Documentar workflows no N8N via API inventory antes de criar novos (GAP-004)

### Scale-1 (50 SOPs/semana)
- **Queue mode** no N8N: separar `main process` de `worker processes`
- Adicionar **Redis** como backend de execuções (substitui SQLite)
- 2 worker instances: `n8n-worker-1`, `n8n-worker-2` via Docker Compose no Hetzner
- Concorrência máxima: 10 execuções simultâneas

### Scale-2 (150+ SOPs/semana)
- **N8N HA**: 3+ instâncias atrás de load balancer (Traefik ou Nginx)
- Redis Cluster ou Redis Sentinel para HA do backend de execuções
- Separar filas por prioridade: `queue-high` (P1), `queue-standard` (P2), `queue-batch` (P3)
- Trigger: quando throughput sustentado > 80 SOPs/semana por 2 semanas consecutivas

---

## OpenClaw Gateway (Claude API)

### Rate Limits atuais (Anthropic Tier)
- Opus: ~50 RPM, ~40K TPM
- Sonnet: ~100 RPM, ~80K TPM
- Haiku: ~200 RPM, ~100K TPM

### Consumo por SOP processado
- T2.2 (schema mapping) → Sonnet: ~2K tokens
- T3.1 (clarity, Clone) → Opus: ~3K tokens
- T3.3 (SINKRA adherence, Clone) → Opus: ~3K tokens
- T3.4 (gap analysis) → Sonnet: ~2K tokens
- T5.1-T5.3 (doc generation) → Sonnet: ~5K tokens cada
- **Total por SOP: ~18-22K tokens**

### Capacidade por cenário
| Cenário | SOPs/semana | Tokens/semana | Modelo crítico |
|---------|------------|---------------|----------------|
| Target (15) | 15 | ~330K | Opus (Clone: 6K/SOP) |
| Scale-1 (50) | 50 | ~1.1M | Opus rate limit atingido |
| Scale-2 (150) | 150 | ~3.3M | Requer Tier upgrade + queue |

### Estratégia de escala
- **Target**: Sem mudança — volume dentro dos limites atuais
- **Scale-1**: Implementar **retry queue com backoff exponencial** no Gateway (já declarado via `retry_policy_extraction`). Distribuir Opus calls ao longo do dia via N8N scheduling
- **Scale-2**: Solicitar Anthropic Tier upgrade. Implementar **model fallback**: Opus → Sonnet se rate limit atingido (com flag de qualidade reduzida no audit trail)
- Trigger de review: quando `timeout_llm_call` (PT30M) é atingido > 3x/semana

---

## Supabase — Storage e Database

### Connection Pool
- Supabase Pro: 60 conexões diretas, 200 via PgBouncer
- Consumo atual por SOP: ~8-12 queries (T1.2, T1.3, T6.5, T6.6, audit trail)

| Cenário | SOPs/semana | Peak concurrent connections |
|---------|------------|---------------------------|
| Target (15) | 15 | ~5 (via PgBouncer) |
| Scale-1 (50) | 50 | ~15 (via PgBouncer) |
| Scale-2 (150) | 150 | ~45 — avaliar upgrade para Business |

### Storage
- Tamanho médio por SOP: 500KB-2MB (PDF/DOCX + outputs ML + docs gerados)
- Target (15/semana): ~1.5GB/mês → sem preocupação
- Scale-1 (50/semana): ~5GB/mês → monitorar
- Scale-2 (150/semana): ~15GB/mês → implementar **lifecycle policy** (arquivar para S3 após 90 dias)

### Trigger de scaling
- Alert em 80% de storage capacity (SUPABASE-001 no risk-register)
- Fallback para S3 bucket já declarado em `infrastructure_connections.yaml`

---

## Third-party SLAs (Dependências Externas)

| Serviço | SLA declarado | Impacto de downtime |
|---------|--------------|-------------------|
| Claude API (Anthropic) | 99.9% | Bloqueia T2.2, T3.1, T3.3, T3.4, T5.x — fallback: queue |
| Notion API | 99.9% | Bloqueia T6.5 (publicação) — fallback: publicar só Git+Supabase |
| ClickUp API | 99.9% | Bloqueia T_REWORK_NOTIFY — fallback: email manual |
| Google Forms/Drive | 99.9% | Bloqueia T1.1 — fallback: intake manual por email |
| N8N (self-hosted) | Sem SLA externo | SPOF — ver estratégia N8N acima |

---

## Thresholds de Review de Infraestrutura

| Métrica | Threshold | Ação |
|---------|-----------|------|
| Throughput sustentado | > 80 SOPs/semana por 2 semanas | Avaliar Scale-2 (N8N HA + Redis Cluster) |
| LLM timeout rate | > 3x/semana | Solicitar Anthropic Tier upgrade |
| Supabase storage | > 80% capacity | Ativar lifecycle policy → S3 |
| N8N failure rate | > 5%/semana | Investigar + implementar queue mode |
| Rework rate | > 20% | Revisão do quality gate QG-3.1 (grading thresholds) |

---

## Responsáveis

| Componente | Owner | Revisão |
|-----------|-------|---------|
| N8N scaling | Tech Lead | Trimestral ou ao atingir threshold |
| Gateway AI / Claude | AI Engineer | Mensal (monitorar rate limits) |
| Supabase | Tech Lead | Trimestral |
| Dependências externas | Tech Lead | Semestral (atualizar SLAs) |
