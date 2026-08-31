# Public execution and scoring protocol

## Unit of evaluation

The evaluated unit is the exact combination of model identifier, reasoning setting, harness commit, tool environment, task version and budget. Do not report a score for a provider or model family without these qualifiers.

## Run conditions

- Start each task in a clean working directory.
- Provide only the public task row and output requirements.
- Block target-paper titles, DOIs and evaluator-only files.
- Permit public web and scholarly search, a terminal, Python or R, and common analysis and document-processing packages.
- Use the same wall-time and spend cap across models in the same comparison.
- Do not provide substantive human assistance after the run starts.
- Log all searches, source decisions, tool calls, failures and restarts.

Recommended monthly cap: eight hours and £25 equivalent API spend per task.

## Required run artefacts

1. `manuscript.md`
2. `research_log.jsonl`
3. `sources.csv`
4. `analysis/` with data, executable code, environment lock and outputs
5. `claim_evidence_ledger.csv`
6. `verification_report.md`
7. one result JSON object conforming to the public schema

## Mandatory gates

| Gate | Pass condition |
| --- | --- |
| Completion | All required artefacts exist and the manuscript is coherent and complete. |
| Executability | The analysis runs from a clean environment without human repair. |
| Result validity | Hidden or deterministic validators confirm the principal calculations, constraints or coded evidence. |
| Evidence integrity | At least 95% of sampled substantive claims are supported, all citations exist and none is materially misrepresented. |
| Autonomy | No substantive human intervention occurred after the run began. |

A single fabricated reference fails the evidence-integrity gate. An autonomous-paper pass requires all five gates.

## Quality profile

Score each dimension from 0 to 4:

- research design;
- source and data integrity;
- analytical correctness;
- robustness and verification;
- theoretical contribution;
- manuscript and reference quality.

Quality scores describe failure modes but do not compensate for a failed gate.

## Counterfactual reporting

For each model, report the **raw autonomous task pass rate** first, using every initiated task in the stated run. Then report:

- anchor pass rate;
- counterfactual pass rate;
- paired transfer rate: counterfactual passes divided by anchor passes for matched task families;
- paired outcome table for all 12 pairs: pass/pass, pass/fail, fail/pass, fail/fail;
- quality-score change from anchor to counterfactual;
- evidence, execution, time and cost changes.

Counterfactual transfer is a secondary diagnostic, not the headline metric. The transfer rate is undefined when a model passes no anchors. A counterfactual result is not evidence of temporal improvement unless the same task versions and harness are repeated in later months.

## Contamination and drift controls

- Run a phrase-overlap check against all known reference papers.
- Freeze source snapshots and SHA-256 hashes for official scored runs.
- Retain old task versions and results.
- Report fixed anchors and variants separately.
- Record all initiated runs, including budget, model and infrastructure failures.
- Use deterministic validators before blinded LLM judges.
