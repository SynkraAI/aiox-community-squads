# ETL Extract Keyframes

## Contrato SINKRA

Domain: `Operational`
executor: etl-extractor
atomic_layer: Molecule
Input: video source, extraction strategy, output route
Output: keyframes directory, index.json, metrics
Pre-condition: fonte de vídeo válida e ferramentas multimodais disponíveis
Post-condition: frames extraídos, indexados e deduplicados quando solicitado
Performance: bloquear zero frames extraídos ou index inválido


## Metadata

| Field | Value |
|---|---|
| **task_name** | Extract Keyframes from Video |
| **status** | Active |
| **responsible_executor** | `@etl-extractor` |
| **execution_type** | `Deterministic` |
| **input** | Video file path or URL + extraction strategy |
| **output** | Keyframes directory + index.json |
| **action_items** | 4-phase extraction flow |
| **acceptance_criteria** | 7 measurable criteria |

## Purpose

Extract representative keyframes from video files using scene detection, interval sampling, or visual uniqueness filtering. Produces frames optimized for:

- Multimodal RAG pipelines
- Training data generation
- Visual context for transcripts
- Content indexing and search

## Inputs

### Minimal Input

```json
{
  "source": {
    "kind": "file",
    "value": "/path/to/video.mp4"
  },
  "strategy": "scene_detection",
  "constraints": {
    "business_slug": "acme",
    "workspace_mode": "auto"
  }
}
```

### Full Input

```json
{
  "source": {
    "kind": "file",
    "value": "/path/to/video.mp4"
  },
  "strategy": "scene_detection",
  "options": {
    "threshold": 0.3,
    "max_frames": 100,
    "output_format": "jpg",
    "quality": 85,
    "filter_duplicates": true,
    "ssim_threshold": 0.85,
    "include_timestamps": true
  }
}
```

## Extraction Strategies

### 1. Scene Detection (Default)

Detects shot boundaries using histogram/luminance changes.

**Tools:** PySceneDetect (preferred) or FFmpeg

```bash
# PySceneDetect
scenedetect -i video.mp4 -o output/ save-images

# FFmpeg fallback (with timestamp-based naming)
ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)'" -vsync vfr -frame_pts true output/frame_%d.jpg
# -frame_pts true: frame name = PTS timestamp (correlates with video timeline)
# Without it: sequential names (frame_00001.jpg) lose temporal correlation
```

**Parameters:**
- `threshold`: Scene change sensitivity (0.0-1.0, default: 0.3)
- Lower = more sensitive (more frames)
- Higher = less sensitive (fewer frames)

**Best for:** Edited videos, presentations, courses with clear cuts

### 2. Interval Sampling

Extracts frames at fixed time intervals.

```bash
# 1 frame every 5 seconds (with timestamp-based naming)
ffmpeg -i video.mp4 -vf "fps=1/5" -frame_pts true output/frame_%d.jpg
```

**Parameters:**
- `interval_seconds`: Time between frames (default: 5)

**Best for:** Long videos without clear scene changes, surveillance footage

### 3. Adaptive (SSIM Uniqueness)

Combines scene detection with structural similarity filtering.

**Process:**
1. Run scene detection
2. Calculate SSIM between consecutive frames
3. Keep only frames with SSIM < threshold (sufficiently different)

**Parameters:**
- `ssim_threshold`: Similarity threshold (0.0-1.0, default: 0.85)
- Lower = more strict (fewer, more unique frames)
- Higher = more permissive (more frames)

**Best for:** Slides, presentations, content with gradual changes

## Execution Flow

### Phase 0: Workspace preflight

- Run `bash squads/etl-ops/scripts/validate-etl-essentials.sh`
- Load `tasks/load-workspace-context.md`
- Resolve output root:
  - canonical: `workspace/businesses/{business_slug}/etl/keyframes/{run_id}/`
  - custom: `docs/etl/{business_slug}/`
  - legacy: caller-provided output path

### Phase 1: Validate Source

- Verify file exists and is accessible
- Detect video format and duration
- Calculate expected frame count at target FPS
- VETO if file not found or invalid format

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=duration,r_frame_rate -of json {input}
```

### Phase 2: Extract Frames

**If strategy = scene_detection:**
```bash
# Check PySceneDetect availability
which scenedetect

# If available
scenedetect -i {input} -o {output_dir} list-scenes save-images

# If not available, fallback to FFmpeg
ffmpeg -i {input} -vf "select='gt(scene,{threshold})'" -vsync vfr {output_dir}/frame_%05d.jpg
```

**If strategy = interval:**
```bash
ffmpeg -i {input} -vf "fps=1/{interval_seconds}" {output_dir}/frame_%05d.jpg
```

**Checkpoint:** At least 1 frame extracted

### Phase 3: Filter Duplicates (Optional)

If `filter_duplicates == true`:

```python
from skimage.metrics import structural_similarity as ssim
import cv2

def filter_by_ssim(frames_dir, threshold=0.85):
    frames = sorted(Path(frames_dir).glob("*.jpg"))
    unique = [frames[0]]
    prev = cv2.imread(str(frames[0]), cv2.IMREAD_GRAYSCALE)

    for frame in frames[1:]:
        curr = cv2.imread(str(frame), cv2.IMREAD_GRAYSCALE)
        score, _ = ssim(prev, curr, full=True)

        if score < threshold:
            unique.append(frame)
            prev = curr
        else:
            frame.unlink()  # Remove duplicate

    return unique
```

**Checkpoint:** Frames reduced, duplicates removed

### Phase 4: Generate Index

Create `index.json` with metadata for each keyframe:

```json
{
  "source_file": "video.mp4",
  "duration_sec": 1800,
  "strategy": "scene_detection",
  "threshold": 0.3,
  "total_source_frames": 54000,
  "keyframes_extracted": 42,
  "reduction_ratio": 0.9992,
  "keyframes": [
    {
      "id": 1,
      "filename": "frame_00001.jpg",
      "frame_num": 150,
      "timestamp_sec": 5.0,
      "scene_score": 0.78
    },
    {
      "id": 2,
      "filename": "frame_00002.jpg",
      "frame_num": 890,
      "timestamp_sec": 29.67,
      "scene_score": 0.65
    }
  ]
}
```

## Output Structure

```
{output_dir}/
├── keyframes/
│   ├── frame_00001.jpg
│   ├── frame_00002.jpg
│   └── ...
├── index.json
└── scenes.csv (if PySceneDetect used)
```

Canonical output suggestion:

```
workspace/businesses/{business_slug}/etl/keyframes/{run_id}/
├── keyframes/
├── index.json
└── scenes.csv
```

## Checkpoint Rules

| Phase | Checkpoint | Veto Condition |
|-------|------------|----------------|
| Validate | File readable | File not found, invalid format |
| Extract | Frames > 0 | Zero frames extracted |
| Filter | Unique frames > 0 | All frames filtered as duplicates |
| Index | index.json valid | Write error |

## Metrics

Report in envelope:

```yaml
metrics:
  duration_sec: 1800
  fps: 30
  total_frames: 54000
  keyframes_extracted: 42
  duplicates_filtered: 8
  final_keyframes: 34
  reduction_ratio: 0.9994
  avg_scene_score: 0.52
  extraction_time_sec: 12.5
```

## CLI Quick Reference

```bash
# Scene detection with PySceneDetect
scenedetect -i video.mp4 list-scenes -o output/
scenedetect -i video.mp4 save-images -o output/
scenedetect -i video.mp4 split-video -o output/

# Scene detection with FFmpeg (timestamp naming)
ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr -frame_pts true output/frame_%d.jpg

# Get all scene scores (for analysis)
ffmpeg -i video.mp4 -vf "select='gte(scene,0)',metadata=print:file=scores.txt" -an -f null -

# Interval sampling (timestamp naming)
ffmpeg -i video.mp4 -vf "fps=1/5" -frame_pts true output/frame_%d.jpg

# High quality extraction (timestamp naming)
ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)'" -qscale:v 2 -frame_pts true output/frame_%d.jpg

# THRESHOLD GUIDE:
# - 0.3: Edited videos, slides, clear cuts (default)
# - 0.1-0.15: Talking-head (subtle changes)
# - 0.4-0.5: High-motion content
```

## Acceptance Criteria

1. Source video is validated before extraction
2. At least 1 keyframe extracted (or explicit veto with reason)
3. Strategy matches requested (scene_detection, interval, adaptive)
4. Duplicate filtering applied when requested
5. index.json contains all keyframe metadata with timestamps
6. Frame files are valid images (readable by OpenCV/PIL)
7. Metrics include reduction_ratio calculation


Completion Criteria: output validado, persistido no destino correto e pronto para handoff
