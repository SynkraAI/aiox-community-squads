# Extract Podcast Interview

## Contrato SINKRA

Domain: `Operational`
executor: etl-chief
atomic_layer: Molecule
Input: youtube source, podcast constraints, language
Output: diarized transcript JSON+MD, confidence report
Pre-condition: source profile compatível com podcast e transcript acessível
Post-condition: diarização entregue com speakers, confidence e envelope válido
Performance: manter fase heurística <100ms e degradar com transparência sem API key


## Metadata

| Field | Value |
|---|---|
| **task_name** | Extract and Diarize Podcast Interview |
| **status** | Active |
| **responsible_executor** | `@etl-chief` |
| **execution_type** | `Hybrid` |
| **input** | YouTube video URL or channel URL with `constraints.podcast=true` |
| **output** | Diarized transcript (JSON + MD) with speaker attribution |
| **action_items** | 3-phase pipeline: extract → diarize (deterministic) → review (LLM) |
| **acceptance_criteria** | 8 measurable criteria |

## Purpose

Specialized pipeline for podcast/interview extraction with automatic speaker identification. Optimized for cost (Phase 1 free, Phase 2 < $0.10) and speed (Phase 1 ~30ms, Phase 2 ~30s).

## Modes

### Single Video
```json
{
  "source": { "kind": "youtube_video", "value": "https://youtu.be/VIDEO_ID" },
  "desired_output": "diarized",
  "mode": "single",
  "constraints": {
    "podcast": true,
    "language": "pt",
    "speakers": "Host=Name,Guest=Name"
  }
}
```

### Batch Channel (all episodes)
```json
{
  "source": { "kind": "youtube_channel", "value": "@ChannelHandle" },
  "desired_output": "diarized",
  "mode": "batch",
  "constraints": {
    "podcast": true,
    "language": "pt",
    "max_items": 20
  }
}
```

## Execution Flow

### Phase 1: Extract Transcript (free, ~500ms)
```bash
node services/etl/bin/youtube-transcript.js {videoId} --lang {language} -o {output_dir}
```
- Checkpoint: segments > 0, chars > min_extract_chars
- VETO: no captions, video private, rate limit (retry with backoff)

### Phase 2: Deterministic Diarization (free, ~30ms)
```bash
node services/etl/bin/youtube-diarize.js {transcript.json} -o {output_dir} -f both
```
- Splits on `>>` markers → speaker blocks
- Auto-detects: podcast name, host name, guest name
- Scores blocks with heuristics (host signals, guest signals, length, questions)
- Continuation detection (prevents false speaker splits)
- Checkpoint: blocks > 0, speakers detected
- Output: `{videoId}-diarized.json` + `{videoId}-diarized.md`

### Phase 3: LLM Review (optional, ~$0.05, ~30s)
```bash
node services/etl/bin/youtube-diarize.js {transcript.json} --llm-review -o {output_dir} -f both
```
- Reviews blocks with confidence < 0.70
- Batches 20 blocks per LLM call with context windows
- Model: Gemini 2.5 Flash (cheapest)
- Requires: `OPENROUTER_API_KEY`
- Checkpoint: accuracy improvement measured
- SKIP if API key not set (graceful degradation)

### Phase 4: Auto-Heal (development mode only)
```bash
node services/etl/bin/youtube-diarize-autoheal.js --corpus ./training-data/ --target-accuracy 0.90
```
- Runs on corpus of transcripts with reference ground truths
- Analyzes systematic error patterns
- Patches diarizer thresholds/rules automatically
- Repeats until 90%+ accuracy on 20+ consecutive transcripts
- Requires: reference diarizations (from full LLM pass)

## Batch Channel Workflow

For extracting all episodes from a podcast channel:

1. List channel videos: `youtube-pipeline.js @handle --limit N --skip-cleanup --skip-metadata`
2. For each video with duration > 20min (likely interview):
   a. Extract transcript (Phase 1)
   b. Diarize deterministically (Phase 2)
   c. LLM review if key available (Phase 3)
3. Generate index with all episodes, speakers, topics

## Training Data

To build the auto-heal corpus:
```
services/etl/training-data/
  {videoId}/
    transcript.json          # from youtube-transcript.js
    reference-diarized.json  # from full LLM pass (high accuracy)
```

First transcript creates ground truth via full LLM agent pass. Subsequent transcripts use deterministic + LLM review. Auto-heal improves the deterministic pass over time, reducing LLM review cost per transcript.

## Output Routing

| Mode | Output Path |
|------|-------------|
| Single (with slug) | `workspace/businesses/{slug}/etl/runs/{run_id}/` |
| Single (no slug) | `outputs/etl/{run_id}/` |
| Batch channel | `outputs/youtube/{channel-slug}/diarized/` |

## Acceptance Criteria

1. Transcript extracted with correct language
2. Speaker change markers (`>>`) detected and processed
3. At least 2 speakers identified (HOST + GUEST)
4. Podcast name auto-detected when present in intro
5. Diarized JSON follows output-contract.yaml envelope format
6. Diarized MD is human-readable with `[SpeakerName] [HH:MM:SS]` format
7. Phase 2 heuristic runs in < 100ms
8. Phase 3 LLM review (when enabled) improves confidence on low-confidence blocks


Completion Criteria: output validado, persistido no destino correto e pronto para handoff
