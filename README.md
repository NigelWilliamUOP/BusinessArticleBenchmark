# Business and Management Autonomous Research Benchmark

**BMA-ARB** measures whether a frontier-model agent can autonomously produce a technically complete, verifiable business or management research paper from a research brief and permitted public digital inputs.

It is a capability benchmark, not an AI-writing detector and not a prediction of journal acceptance. A pass requires a complete manuscript, cleanly executable analysis, valid results, reliable evidence and no substantive human intervention.

## What is in this release

- 12 baseline anchor tasks derived from the 2026 Scopus taxonomy.
- 12 matched counterfactual variants that preserve the capability tested while changing the empirical setting, construct, period or model assumptions.
- Public scoring rules, result schema and deterministic validation scripts.
- A runner hand-off for Antigravity or another auditable agent harness.
- A source registry for reconstructing public-data tasks.

Evaluator-only answer keys, hidden validators and paper identifiers are intentionally excluded from the public repository.

## Benchmark design

| Production system | Anchor tasks | Counterfactual variants |
| --- | ---: | ---: |
| Computational experiments and formal models | 4 | 4 |
| Literature, document and conceptual synthesis | 4 | 4 |
| Secondary-data and digital-text analysis | 4 | 4 |

The headline measure is the **raw autonomous task pass rate**: tasks passing all five mandatory gates divided by all initiated tasks. The paired design supplies two secondary diagnostics:

1. **Anchor performance** measures longitudinal change on stable tasks.
2. **Counterfactual transfer** measures whether capability survives substantive changes that make memorising the reference paper insufficient.

Report the raw pass rate first. Report anchor, counterfactual and paired-transfer results separately underneath it; do not substitute a transfer-adjusted composite score.

## Quick start

```bash
python scripts/validate_manifests.py
python scripts/validate_results.py results/example_results.jsonl
```

Run the public prompts in `tasks/anchors_v0.1.jsonl` and `tasks/counterfactuals_v0.1.jsonl`. Each run must emit the artefacts listed in `docs/PROTOCOL.md` and a result record conforming to `evaluator/public/score_schema_v0.1.json`.

## Synthetic frontier index

Until direct BMA-ARB runs are practical, the **Business and Management Synthetic Frontier Research Index (BMSFRI)** provides a transparent proxy constructed from seven published adjacent benchmarks. The August 2026 best-published-system frontier envelope is **38.6/100** on the benchmark's raw 12-task basis.

This is neither an observed task pass rate nor a score achieved by one model. Every component, crosswalk weight, imputation and claim limit is public and machine-readable.

```bash
python scripts/validate_synthetic_inputs.py
python scripts/build_synthetic_index.py
```

See `docs/SYNTHETIC_INDEX.md` and `synthetic/results/frontier_envelope_2026-08.json`.

## Living benchmark genealogy

`genealogy/` maintains a reviewed graph of AI-scientist systems, benchmarks, verifier programmes and evaluation frameworks. It records what each work evaluates, the human guidance supplied, whether compute or human time is reported, its relationship to BMA-ARB and the claim boundary.

The genealogy also defines the planned **Portsmouth Business School Research Production Frontier**. This extension will estimate journal-ready outputs as a function of human effort, compute, orchestration, verification and Portsmouth's observed output portfolio. It is collaboration-first: Project APE and CRED are priority partners rather than systems to duplicate.

The public Portsmouth profile contains aggregates only. The current audit snapshot supports provisional title-level coverage signals but lacks journal title and ISSN, so journal weighting remains pending an authorised public-metadata join.

```bash
python scripts/validate_genealogy.py
python scripts/render_genealogy.py --check
```

A weekly workflow searches arXiv for new candidates and opens a draft pull request only when the discovery queue changes. Candidates are never promoted automatically.

See `genealogy/README.md` and `genealogy/generated/GENEALOGY.md`.

## Counterfactual rule

Every variant changes at least two design dimensions while retaining the same principal capability and validator family as its anchor. Variants are not assumed to have a single correct published conclusion. They are scored on process integrity, executable analysis and whether claims follow from acquired evidence.

## Capability-share forecast

`scripts/forecast_capability_share.py` converts system-specific benchmark passes into a benchmark-calibrated share of the frozen 2026 corpus using the audited taxonomy weights. It then produces transparent conservative, central and accelerated scenario paths.

The raw task pass rate remains the benchmark headline. The population bridge and forecast are separate model-implied quantities. No numerical forecast should be released until a valid BMA-ARB baseline has been run.

```bash
python scripts/forecast_capability_share.py results/results.jsonl
```

See `docs/FORECAST_METHOD.md` and `docs/COMPUTE_INVESTMENT_GUIDE.md`.

## Versioning

- Task wording, permitted inputs and validators are immutable within a task version.
- New variants receive new identifiers; old tasks are never silently rewritten.
- Exact model, harness, tool environment, budget and source snapshot must be recorded for every run.
- Fixed anchors and counterfactual variants must be reported separately.
- Genealogy candidates remain separate from curated records until a primary-source review is complete.

## Status

This release is **design-complete but not directly scored**. A synthetic frontier index is available as a provisional tracking baseline. Before the first official direct comparison, freeze the source files, compute checksums and complete evaluator-only validation fixtures.

## Citation

See `CITATION.cff`.

## Licence

Code is released under the MIT License. Task briefs, documentation and rubrics are released under CC BY 4.0; see `LICENSE-DATA`.
