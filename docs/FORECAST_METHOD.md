# Forecasting the autonomous share of business and management research

## Release decision

Publish a numerical forecast only after the first valid BMA-ARB run. Before that run, the benchmark has no observed business-research completion rate, so importing scores from software or general-agent benchmarks would create false precision.

The forecast has three separate layers.

| Layer | Quantity | Status |
| --- | --- | --- |
| Benchmark | Raw autonomous task pass rate | Observed after each run |
| Population bridge | Benchmark-calibrated share of the frozen 2026 corpus | Model-implied |
| Future trajectory | Conditional share under conservative, central and accelerated capability scenarios | Scenario forecast |

## Headline benchmark measure

For model-harness combination \(m\) in month \(t\):

\[
R_{mt}=\frac{\text{tasks passing all five gates}}{\text{all initiated tasks}}.
\]

This remains the public benchmark headline. Infrastructure, budget and time failures remain in the denominator because silent exclusion would overstate deployable capability.

## Population bridge

The 2026 core-business opportunity envelope is 10.20% of the recovered Scopus corpus. It consists of three production systems:

| Production system | Share of the full recovered corpus | Share of the 10.20% envelope |
| --- | ---: | ---: |
| Computational experiments and formal models | 2.60% | 25.48% |
| Literature, document and conceptual synthesis | 4.07% | 39.93% |
| Secondary-data and digital-text analysis | 3.53% | 34.59% |
| **Total** | **10.20%** | **100.00%** |

Let \(w_k\) be a system's share of the full corpus and \(p_{kmt}\) the model's probability of an autonomous pass for that system. The frozen-corpus capability share is:

\[
C^{2026}_{mt}=\sum_k w_k p_{kmt}.
\]

The public script uses a Jeffreys beta-binomial estimate for each \(p_k\) and simulation to show uncertainty arising from the small task count. This interval does not include taxonomy-label error, corpus coverage error or model-selection uncertainty.

Do not call \(C^{2026}\) an adoption rate. It is the share of the frozen corpus whose workflow is both inside the taxonomy opportunity envelope and passed by the tested agent under benchmark conditions.

## Why the envelope must be re-audited

Monthly model runs can increase \(p_k\), but the frozen measure cannot exceed 10.20%. New capabilities may make additional research families feasible. Once a year:

1. draw a new probability sample from the current publication year;
2. apply the same autonomous-production construct and blocker rule;
3. retain a bridge sample coded under both old and new taxonomies;
4. estimate revised production-system weights;
5. publish old-weight and new-weight results side by side.

This separates model progress from changes in the kinds of papers being published.

## Conditional model forecast

The initial forecast scenarios act on pass odds rather than pass percentages:

\[
\operatorname{odds}(p_{k,t+h})=\operatorname{odds}(p_{kt})\,2^{h/d_s},
\]

where \(d_s\) is the scenario-specific odds-doubling time. Version 0.1 uses 36 months for the conservative scenario, 18 months for central and 9 months for accelerated. These values are transparent judgemental priors, not estimates from BMA-ARB.

The central prior deliberately assumes slower transfer than METR's historical seven-month frontier time-horizon doubling because METR's tasks are predominantly software based and research validity requires retrieval, evidence integrity and methodological verification. Scenario assumptions must be replaced by a fitted trend after at least six monthly observations spanning two frontier-model generations.

## Forecast outputs

Every release should show:

1. observed raw pass rate and numerator/denominator;
2. system-specific pass counts;
3. model-implied frozen-2026 capability share with a simulation interval;
4. scenario paths at 6, 12, 24 and 36 months;
5. annual opportunity-envelope estimate when available;
6. model, harness, budget, source and forecast-assumption versions;
7. a forecast scorecard comparing previous forecasts with later observations.

## Prohibited claims

- Do not infer that papers were actually written by AI.
- Do not describe the benchmark-calibrated share as a design-based population estimate.
- Do not translate external software-benchmark growth directly into business-paper prevalence.
- Do not average different models into a single frontier-AI score.
- Do not present scenario ranges as confidence or prediction intervals.
