# Public evaluator rubric

## Scoring order

1. Verify required artefacts and run provenance.
2. Re-execute the analysis in a clean environment.
3. Apply task-specific deterministic checks.
4. Sample and verify substantive claim-source pairs.
5. Apply the five mandatory gates.
6. Blind the model identity and score the six quality dimensions.

## Quality anchors

| Score | General meaning |
| ---: | --- |
| 0 | Missing, unusable or fundamentally invalid. |
| 1 | Material defects undermine most conclusions. |
| 2 | Partially adequate but important limitations remain. |
| 3 | Competent, reproducible and mostly well justified. |
| 4 | Rigorous, transparent and unusually strong within the task constraints. |

Judges must cite artefact locations for every score of 0, 1 or 4. Deterministic failures take precedence over prose quality.

## Evidence audit

- Draw a reproducible sample of substantive claims, stratified across theory, data, method and results.
- Verify existence, relevance and faithful representation of each cited source.
- Treat a citation as fabricated when the cited item cannot be verified after identifier, title and author checks.
- Treat a source as materially misrepresented when it does not support the attributed proposition or its qualifications reverse the claim.
- Record the numerator and denominator used for claim-support precision.

## Autonomy audit

Human actions after task start are limited to infrastructure recovery that neither changes the model state nor supplies substantive guidance. Source selection, code repair, method choice, interpretation and manuscript editing are substantive interventions and fail the autonomy gate.
