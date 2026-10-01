# BMA-ARB monthly preparation — September 2026

## Decision summary

The fixed 12-task benchmark specification is unchanged. No official frontier release later than the 31 August repository baseline was located. The five-model primary panel is retained. DeepSeek V4 Pro is now explicitly configured at maximum reasoning; this is a model-setting correction, not a task or harness change. Gemini 3.7 Flash is recorded only as an optional cost-efficiency shadow model.

No model task was executed in this environment. The raw autonomous task pass rate is therefore **not observed (0 initiated; denominator 0)**, not 0%. Clean execution, evidence failures and workflow pass rates are also unobserved. Actual run cost is £0.

## Prepared run

- Primary panel: 5 models.
- Fixed anchor suite: 12 tasks — four computational, four synthesis and four secondary-data tasks.
- Primary runs remaining: 60.
- Maximum task spend: £25; maximum total: £1,500.
- Maximum task time: 8 hours; maximum aggregate task time: 480 hours.
- Optional shadow run: 12 Gemini 3.7 Flash tasks, separate from the primary panel.

## Model changes versus harness changes

| Type | September treatment |
| --- | --- |
| Model release | No post-baseline frontier release detected. |
| Model setting | DeepSeek V4 Pro changed from unspecified “thinking” to `reasoning=max`. |
| Panel extension | Gemini 3.7 Flash may run as a 12-task shadow; it does not replace Gemini 3.1 Pro. |
| Harness | Not yet frozen. Record harness commit, system prompt hash, tool image and provider-resolved model ID before launch. |
| Benchmark | No task, rubric, gate or budget change. |

## Reporting state

| Measure | Current value |
| --- | ---: |
| Raw autonomous task pass rate | Not observed (0/0) |
| Computational workflow pass rate | Not observed |
| Synthesis workflow pass rate | Not observed |
| Secondary-data workflow pass rate | Not observed |
| Evidence failures | Not observed |
| Clean execution rate | Not observed |
| Actual cost | £0 |
| Primary runs remaining | 60 |

## Contamination risk

Risk is **high and unresolved** because the public task briefs closely track published 2026 papers and the target papers are searchable online. Blinding titles and DOIs reduces direct retrieval but does not prevent semantic discovery. Official scoring therefore requires target-title/DOI blocking, phrase-overlap checks, frozen source snapshots, research-log inspection and evaluator-only deterministic validators. Public prompts must not be treated as uncontaminated merely because the target identifiers are omitted.

## Launch blocker

External provider execution and the frozen Antigravity harness were not available here. All 60 primary model-task runs remain to be launched. Official scoring must also wait for the 12 deterministic validator fixtures; the manifests correctly mark this as not ready rather than producing provisional passes.
