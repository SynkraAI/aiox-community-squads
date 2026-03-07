# Source Credibility Checklist

```yaml
checklist:
  id: dr-source-credibility
  version: 1.0.0
  created: 2026-03-06
  purpose: "Validate source quality for all evidence cited in pipeline"
  mode: recommended
  used_by: [cochrane, higgins, gilad, forsgren]
  when: "During Tier 1 execution, applied to each source before citing"
```

---

## Source Identity

```yaml
identity_checks:
  - id: SRC-001
    check: "Source URL is accessible and not dead link"
    type: blocking
    validation: "URL returns HTTP 200 or content is cached"

  - id: SRC-002
    check: "Author/publisher identifiable"
    type: blocking
    validation: "author_name OR publisher_name is non-empty"

  - id: SRC-003
    check: "Publication date known"
    type: blocking
    validation: "publication_date is set (year minimum)"

  - id: SRC-004
    check: "Source age within relevance window"
    type: recommended
    validation: "publication_date within last 5 years (or justified if older)"
```

---

## Authority Assessment

```yaml
authority_checks:
  - id: AUTH-001
    check: "Publisher reputation scored"
    type: blocking
    scoring:
      0.8-1.0: "Peer-reviewed journal, established research institution"
      0.6-0.8: "Industry report from recognized firm (Gartner, McKinsey, DORA)"
      0.5-0.7: "Established news outlet, official documentation"
      0.3-0.5: "Professional blog, conference presentation"
      0.0-0.3: "Anonymous, unverifiable, or self-published without credentials"

  - id: AUTH-002
    check: "Author credentials relevant to claim domain"
    type: recommended
    validation: "author has demonstrable expertise in the topic area"

  - id: AUTH-003
    check: "Source is primary (not just citing another source)"
    type: recommended
    validation: "source_type in [primary, secondary, grey_literature] is labeled"
```

---

## Evidence Quality

```yaml
evidence_quality_checks:
  - id: EVQ-001
    check: "Study design identified"
    type: blocking
    validation: "design in [systematic_review, rct, cohort, case_control, cross_sectional, case_study, expert_opinion, benchmark, survey]"

  - id: EVQ-002
    check: "Sample size assessed"
    type: blocking
    validation: "sample_size is stated or estimated (N=X)"
    thresholds:
      strong: "N >= 100 or 10+ studies in meta-analysis"
      moderate: "N 30-99 or 5-9 studies"
      weak: "N < 30 or < 5 studies"
      anecdotal: "N < 5 or single case study"

  - id: EVQ-003
    check: "Evidence level assigned (Sackett Level I-V)"
    type: blocking
    validation: "evidence_level in [I, II, III, IV, V]"

  - id: EVQ-004
    check: "Methodology described (not just conclusions)"
    type: recommended
    validation: "source includes how data was collected, not just what was found"
```

---

## Bias & Conflict Screen

```yaml
bias_screen_checks:
  - id: BCS-001
    check: "Funding source identified (or absence noted)"
    type: blocking
    validation: "funding_source is set OR 'not disclosed' is noted"

  - id: BCS-002
    check: "Potential conflicts of interest flagged"
    type: blocking
    validation: "conflict_check performed (vendor-funded? author has financial interest?)"

  - id: BCS-003
    check: "Vendor-produced content labeled as such"
    type: blocking
    validation: "if source is produced by vendor of evaluated product: vendor_content = true"

  - id: BCS-004
    check: "Cherry-picking check (does source present balanced view?)"
    type: recommended
    validation: "source acknowledges limitations or counterarguments"
```

---

## Cross-Verification

```yaml
verification_checks:
  - id: VER-001
    check: "Claim corroborated by >= 1 independent source"
    type: recommended
    validation: "at least 2 independent sources support the same claim"

  - id: VER-002
    check: "Contradicting evidence acknowledged if found"
    type: blocking
    validation: "if contradicting sources exist: documented, not hidden"

  - id: VER-003
    check: "Source triangulation attempted (multiple source types)"
    type: recommended
    validation: "evidence from >= 2 different source types (e.g., academic + industry)"
```

---

## Credibility Score Card

```yaml
scoring:
  per_source:
    formula: "average of: authority (0-1) + evidence_quality (0-1) + bias_free (0-1)"
    thresholds:
      high: ">= 0.7 — Cite with confidence"
      medium: "0.4-0.7 — Cite with caveats"
      low: "0.2-0.4 — Cite as weak evidence only"
      reject: "< 0.2 — Do not cite"

  per_pipeline_run:
    minimum_high_sources: 2
    minimum_total_sources: 5
    maximum_low_sources_ratio: 0.30
```

---

## Scoring

| Score | Result | Action |
|-------|--------|--------|
| 100% Blocking (10/10) per source | CITE | Include in report |
| >= 80% Blocking (8+/10) | CITE WITH CAVEAT | Include with noted limitations |
| < 80% Blocking | EXCLUDE or FOOTNOTE | Do not use as primary evidence |

**Total Checks:** 10 blocking + 7 recommended = 17 per source

---

**Version:** 1.0.0
**Standard:** Deep Research Source Credibility
