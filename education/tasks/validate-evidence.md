# Task: Validate Evidence

**Task ID:** validate-evidence
**Version:** 1.0
**Agent:** clark-validator
**Squad:** education

## Purpose
Validate that all instructional design decisions are evidence-based using Ruth Clark's research standards. Prevents "fad-based" instructional design.

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| design_doc_path | string | Yes | Path to curriculum, module, or lesson design |
| domain | string | Yes | Course domain |
| design_level | string | Yes | "curriculum", "module", "lesson" |

## Preconditions
- [ ] Design document complete
- [ ] Instructional strategies identified
- [ ] squads/education/data/evidence-base/ contains research references

## Steps
1. Load design document
2. Identify all instructional strategies used
3. For each strategy, check evidence base:
   - Research support (peer-reviewed studies)
   - Effect size (Cohen's d > 0.4 preferred)
   - Context validity (does research context match our use case?)
   - Replication (multiple studies or single finding?)

4. Classify strategies:
   - **Strong Evidence:** Multiple studies, large effect sizes, replicated
   - **Moderate Evidence:** Some studies, medium effect sizes
   - **Weak Evidence:** Single study or anecdotal
   - **No Evidence:** Assumption or intuition-based

5. Identify high-risk strategies (weak/no evidence)
6. Recommend alternatives with stronger evidence
7. Generate validation report

## Output
- **Location:** `minds/{domain}/validation-report-{design-level}.md`
- **Format:** Evidence validation report
- **Sections:**
  - Strategies Evaluated
  - Evidence Classification per Strategy
  - High-Risk Strategies
  - Recommended Alternatives
  - Evidence Summary Table
  - Final Validation Verdict

## Veto Conditions
- >30% strategies have weak/no evidence → BLOCK design
- Core strategy contradicts research → redesign required
- High-risk strategy with no fallback → find alternative

## Completion Criteria
- [ ] All strategies evaluated for evidence
- [ ] Evidence classification complete
- [ ] High-risk strategies identified
- [ ] Alternatives recommended where needed
- [ ] Validation verdict stated
- [ ] Output saved to validation-report
