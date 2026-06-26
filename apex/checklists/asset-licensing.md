# Checklist: Asset Licensing

```yaml
id: asset-licensing
version: "1.0.0"
description: "License verification checklist for curated visual assets"
owner: web-intel
usage: "Run before presenting curated assets to user for selection"
```

---

## License Categories

| Category | Commercial Use | Attribution | Examples |
|----------|---------------|-------------|----------|
| **Free (no restrictions)** | Yes | No | CC0, Public Domain, Unsplash License |
| **Free (attribution)** | Yes | Required | CC-BY, MIT, Apache |
| **Free (share-alike)** | Yes | Required + SA | CC-BY-SA |
| **Non-commercial** | No | Required | CC-NC, CC-BY-NC |
| **Proprietary** | Varies | Varies | Stock photo licenses, custom |
| **Unknown** | Verify | Verify | No license found |

---

## Verification Checks

### License Detection
- [ ] **Every asset has license status** — no assets without license classification
- [ ] **License source documented** — where the license info was found (page, metadata, API)
- [ ] **Unknown licenses flagged** — clearly marked as "verify before use"
- [ ] **Non-commercial licenses highlighted** — prevent accidental commercial use

### Usage Rights
- [ ] **Commercial use verified** — if project is commercial, only use commercial-OK licenses
- [ ] **Attribution requirements noted** — list what attribution is needed and where
- [ ] **Modification rights checked** — can the asset be cropped, edited, combined?
- [ ] **Distribution rights checked** — can the asset be included in deployed app?

### Stock Photo Specifics
- [ ] **Unsplash License** — free for commercial, no attribution required (but appreciated)
- [ ] **Pexels License** — free for commercial, no attribution required
- [ ] **Pixabay License** — free for commercial, no attribution required
- [ ] **Other stock** — verify specific license terms

### Icon/Illustration Specifics
- [ ] **MIT/Apache** — include license file in project
- [ ] **CC-BY** — add attribution in credits or about page
- [ ] **Custom licenses** — read full terms before use

### 3D Asset Specifics
- [ ] **CC0 models** — free for any use (Poly Haven, some Sketchfab)
- [ ] **CC-BY models** — attribution required in app/credits
- [ ] **Purchased models** — verify redistribution rights
- [ ] **Texture licenses** — separate from model license

### Presentation Requirements
- [ ] **License column in asset catalog** — always visible
- [ ] **Warning for restricted licenses** — visual indicator for CC-NC or unknown
- [ ] **Attribution template generated** — if any assets need attribution
- [ ] **No auto-selection of restricted assets** — user must explicitly choose
