# ETL Env Bootstrap

## Contrato SINKRA

Domain: `Operational`
executor: etl-chief
atomic_layer: Atom
Input: mode flag, runtime environment state
Output: JSON readiness report, profile status table
Pre-condition: shell local acessível e scripts do squad presentes
Post-condition: ambiente auditado e perfis READY/DEGRADED/UNAVAILABLE emitidos
Performance: reavaliar perfis após instalação e falhar loud em perfil indisponível


## Metadata

| Field | Value |
|---|---|
| **task_name** | ETL Environment Bootstrap |
| **status** | Active |
| **responsible_executor** | `@etl-chief` |
| **execution_type** | `Worker (EXEC-W-001)` |
| **input** | Mode flag (--check, --core, --full, --install-media, --install-ebook) |
| **output** | JSON readiness report + profile status table |
| **action_items** | 3-phase bootstrap flow |
| **acceptance_criteria** | 6 measurable criteria |

## Purpose

Diagnose and prepare the local environment for ETL-Ops execution. Validates all runtime dependencies (Node.js, Python, system tools, env vars) and optionally installs missing components so that routing profiles from `data/routing-profiles.yaml` can function correctly.

## Script

```
squads/etl-ops/scripts/etl-env-bootstrap.sh
```

## Modes

| Mode | Behavior |
|------|----------|
| `--check` | Diagnose only, no installs (default) |
| `--core` | Install core: npm deps + scrapling + curl + jq |
| `--full` | Install everything (core + media + ebook + web) |
| `--install-media` | Add media tools (ffmpeg, yt-dlp, whisper, scenedetect) |
| `--install-ebook` | Add ebook tools (pandoc, calibre) |

## Execution Flow

### Phase 1: Detect

- Detect OS and package manager (brew / apt-get / dnf)
- Check core tools: node, npm, python3, curl, jq
- Check npm dependencies in `services/etl/` (accept legacy `infrastructure/services/etl/` only in brownfield clones where that mirror still exists)
- Check Python dependencies (scrapling importable)
- Check media tools: ffmpeg, ffprobe, yt-dlp, whisper, scenedetect
- Check ebook tools: pandoc, ebook-convert (calibre)
- Check web extended tools: firecrawl-cli
- Check env vars: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, FIRECRAWL_API_KEY, OPENROUTER_API_KEY, WHISPER_MODEL_PATH

### Phase 2: Install (optional)

Only when mode is not `--check`:

- `--core`: Install curl, jq, npm deps, scrapling
- `--full`: All of core + media + ebook + web extended
- `--install-media`: ffmpeg, yt-dlp, whisper, scenedetect
- `--install-ebook`: pandoc, calibre

**Note:** Node.js is advisory-only (never auto-installed due to protected paths like `~/.nvm`).

### Phase 3: Report

- Re-run all checks after install for accurate state
- Assess each routing profile as READY / DEGRADED / UNAVAILABLE
- Emit JSON report to stdout
- Print human-readable summary table to stderr

## Profile Readiness Mapping

Each routing profile maps to required tools:

| Profile | Required | Fallback → DEGRADED |
|---------|----------|---------------------|
| youtube_* | node, npm-deps | — (no fallback) |
| web_page | node, npm-deps | scrapling |
| web_page_protected | scrapling | — |
| web_page_js_heavy | curl, jq, CF env vars | scrapling |
| site_crawl | curl, jq, CF env vars | FIRECRAWL_API_KEY |
| search_and_scrape | FIRECRAWL_API_KEY | — |
| ebook_epub | node, npm-deps, pandoc | without pandoc → DEGRADED |
| pdf_document | node, npm-deps | — |
| audio_transcription | ffmpeg, whisper | — |
| video_transcription | ffmpeg, whisper | — |
| video_multimodal | ffmpeg, whisper, scenedetect | without scenedetect → DEGRADED |
| direct_video_url | ffmpeg, whisper | — |
| generic_document | node, npm-deps | — |

## Output

### stdout (JSON)

```json
{
  "mode": "check",
  "os": "darwin",
  "timestamp": "2026-03-25T12:00:00Z",
  "tools": [
    { "name": "node", "status": "installed", "version": "v22.0.0", "category": "core" }
  ],
  "env_vars": [
    { "name": "CLOUDFLARE_API_TOKEN", "status": "set" }
  ],
  "profiles": [
    { "name": "youtube_video", "status": "READY", "note": "" }
  ],
  "summary": {
    "profiles_ready": 10,
    "profiles_degraded": 3,
    "profiles_unavailable": 3,
    "profiles_total": 16
  }
}
```

### stderr (human-readable)

Colored diagnostic messages + summary table with counts per status.

## Acceptance Criteria

1. Script runs without errors on macOS and Linux (`bash 3.2+`)
2. `--check` mode produces valid JSON on stdout without installing anything
3. `--core` mode installs npm dependencies and scrapling when missing
4. Profile readiness correctly reflects tool availability (READY / DEGRADED / UNAVAILABLE)
5. Exit code 0 when all profiles are at least DEGRADED; exit code 1 when any profile is UNAVAILABLE
6. Re-checks after install reflect the updated state


Completion Criteria: output validado, persistido no destino correto e pronto para handoff
