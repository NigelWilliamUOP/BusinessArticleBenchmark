# BMA-ARB monthly preparation, November 2026

## Release decision

The fixed BMA-ARB v0.1 12-task suite, five mandatory paper gates, £25 task budget and eight-hour task limit are unchanged. The November primary panel changes in two places: Gemini 4 Argon replaces Gemini 3.8 Flash after its documented 13 October GA API release, and DeepSeek's `deepseek-flash` alias now resolves to the 17 October V4.1-Flash-1017 update. OpenAI GPT-6 Astra, Claude Fable 5.1 and Grok 4.7 remain primary.

No provider run was initiated. Raw autonomous task pass rate is **not observed (0 initiated; denominator 0)**, not 0%. Workflow pass rates, evidence failures and clean execution are unobserved. Actual external model cost is £0.

## November primary panel

| Provider | November primary model | Setting | Change from October |
| --- | --- | --- | --- |
| OpenAI | GPT-6 Astra | max | No primary change. GPT-6.1 Terra becomes a cost shadow. |
| Anthropic | Claude Fable 5.1 | max | No primary change. Haiku 5.5 is not a maximum-capability replacement. |
| Google | Gemini 4 Argon | high | Replaces Gemini 3.8 Flash after GA API and model-card publication. |
| SpaceXAI | Grok 4.7 | xhigh | No primary text-model change. |
| DeepSeek | V4.1 Flash 1017 | max | Underlying model update under the same `deepseek-flash` alias. |

GPT-6.1 Terra and Claude Opus 5.5 are optional cost shadows. Gemini 4 Carbon is pending access because the official announcement did not yet correspond to a listed public API endpoint or model card at the freeze. GPT-6 Rosalind is excluded from the general panel because it is a trusted-access life-sciences deployment using Astra weights.

## Run accounting

| Measure | November state |
| --- | ---: |
| Primary runs planned and remaining | 60 |
| Runs per primary model | 12 |
| Computational / synthesis / secondary-data runs | 20 / 20 / 20 |
| Optional launchable shadow runs | 24 |
| Pending Carbon candidate runs | 12 |
| Maximum November primary spend | £1,500 |
| Actual spend | £0 |

September and October contain a further 120 unexecuted preparation rows. They cannot now be run and labelled as observations from those months because the harness and provider-resolved model snapshots were not frozen. They remain archive evidence of intended runs, not a recoverable temporal baseline.

## Model versus harness change

The Argon replacement and DeepSeek 1017 routing are model changes. The task briefs, gates, budget, time limit and raw-pass-rate definition did not change. No harness change was applied. The exact harness commit, system prompt, tool image and provider-resolved model identity remain null and are enforced as launch blockers in the November guide.

## Contamination and claim ceiling

Retrieval contamination risk remains high because public prompts are semantically close to identifiable papers. Title and DOI blocking does not prevent paraphrase-based discovery. Training exposure remains uncertain and must be recorded separately. Official scoring is also blocked because all 12 deterministic validator fixtures remain unbuilt.

The claim ceiling is **no benchmark result**. This release is a model-landscape and run-preparation record only. It does not estimate model capability, AI authorship, publication acceptance or the autonomous share of business and management research.

## Official sources reviewed

- OpenAI Deployment Safety Hub and API changelog, through 30 October 2026: GPT-6.1 Terra, GPT-6 Rosalind and GPT-6 channel updates.
- Anthropic system-card index and model documentation, through 7 October 2026: Claude Haiku 5.5; Fable 5.1 remains the maximum-capability primary.
- Google DeepMind model cards and Gemini API changelog, through 13 October 2026: Gemini 4 Argon GA; Gemini 4 Carbon announcement monitored separately.
- SpaceXAI release notes, through 27 October 2026: no new general text model after Grok 4.7.
- DeepSeek API change log, 17 October 2026: V4.1-Flash-1017 behind the `deepseek-flash` alias.
