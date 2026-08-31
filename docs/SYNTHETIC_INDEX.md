# Business and Management Synthetic Frontier Research Index

## Result, August 2026

The initial **BMSFRI frontier-envelope index is 38.6/100**. Its leave-one-benchmark-out sensitivity range is 34.9 to 42.0.

| Production system | Synthetic index |
| --- | ---: |
| Computational experiments and formal models | 28.9 |
| Literature, document and conceptual synthesis | 49.1 |
| Secondary-data and digital-text analysis | 37.9 |
| **Overall, 12 tasks** | **38.6** |

This is a synthetic capability signal. It is not an observed pass rate and not the performance of a single model. It combines the best published systems across seven adjacent benchmark metrics.

## Evidence components

| Benchmark component | Published frontier score | Role |
| --- | ---: | --- |
| PaperBench replication | 21.0% | End-to-end paper replication |
| CORE-Bench hard | 21.0% | Computational reproducibility |
| REPRO-Bench REPRO-Agent | 36.6% | Social-science reproducibility assessment |
| ORAgentBench all tasks | 35.51% | Executable operations research |
| DeepResearch Bench report quality | 48.88% | Research depth and report construction |
| DeepResearch Bench citation accuracy | 90.24% | Evidence attribution |
| APEX management consulting Pass@1 | 46.4% | Long-horizon professional business execution |

## Construction

Every BMA task has a published benchmark crosswalk. Task scores use a weighted geometric mean:

\[
I_j=100\exp\left(\sum_b w_{jb}\log s_b\right).
\]

The geometric mean treats capabilities as complements and limits compensation. For example, high citation accuracy cannot erase weak executable-research performance. The overall index is the unweighted mean across the 12 task scores, preserving the benchmark's raw-task emphasis.

## Task estimates

| Task | Synthetic score | Leave-one-source range |
| --- | ---: | ---: |
| BMA-COMP-01 | 30.8 | 26.6-33.8 |
| BMA-COMP-02 | 30.0 | 26.1-32.7 |
| BMA-COMP-03 | 27.5 | 24.1-31.8 |
| BMA-COMP-04 | 27.3 | 23.9-31.5 |
| BMA-SYN-01 | 47.0 | 39.9-51.4 |
| BMA-SYN-02 | 49.7 | 40.7-57.8 |
| BMA-SYN-03 | 49.9 | 40.9-54.9 |
| BMA-SYN-04 | 49.9 | 40.9-54.9 |
| BMA-DATA-01 | 38.2 | 34.7-46.6 |
| BMA-DATA-02 | 33.2 | 30.5-40.4 |
| BMA-DATA-03 | 33.4 | 30.0-39.1 |
| BMA-DATA-04 | 46.7 | 39.7-51.1 |

Weighting the three production-system indices by their shares within the frozen 10.20% taxonomy opportunity envelope gives a synthetic capability value of 40.1% within that envelope. This produces an **illustrative corpus-share proxy of 4.09%**, with a leave-one-benchmark-out range of 3.65% to 4.41%. This number is useful for scenario comparison only. The component scores are not calibrated pass probabilities, so 4.09% must not be described as an estimated prevalence, adoption rate or observed autonomous share.

## Monthly update rule

1. Add only a benchmark result released by its authors or official maintainer.
2. Preserve metric definition, harness, model, date and source.
3. Never silently replace a historic value; version the registry and regenerate the index.
4. Report stale component ages and leader changes.
5. Publish the overall index, production-system indices, task table and sensitivity range.
6. Keep results from any future direct BMA-ARB run separate as observed validation evidence.

## Claim ceiling

The index supports a scenario comparison and directional tracking claim. It does not support a population prevalence estimate. Its main limitations are construct transfer between benchmarks, different model-harness leaders, heterogeneous metric definitions, stale model coverage in older benchmarks and judgemental crosswalk weights.
