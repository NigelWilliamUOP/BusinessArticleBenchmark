# BMA-ARB monthly preparation, October 2026

## Release decision

The fixed BMA-ARB v0.1 12-task suite is unchanged. The five-provider model panel changes completely because each provider released, replaced or rerouted a relevant model during September. No benchmark task, gate, budget or scoring rule changed.

No provider run was initiated in this environment. Raw autonomous task pass rate is **not observed (0 initiated; denominator 0)**, not 0%. Workflow pass rates, evidence failures and clean execution are also unobserved. Actual external model cost is £0.

## October primary panel

| Provider | October primary model | Setting | September change |
| --- | --- | --- | --- |
| OpenAI | GPT-6 Astra | max | Replaces GPT-5.6 Sol. |
| Anthropic | Claude Fable 5.1 | max | Replaces Fable 5. |
| Google | Gemini 3.8 Flash GA | high | Replaces Gemini 3.1 Pro preview; Argon held pending API documentation. |
| SpaceXAI | Grok 4.7 | xhigh | Replaces Grok 4.6 high. |
| DeepSeek | V4.1 Flash | max | V4 Pro retired; legacy requests rerouted from 14 September. |

GPT-6.1 Sol and Claude Opus 5.5 are optional cost-efficiency shadows. Gemini 4 Argon is a pending-access candidate only because an official reproducible API endpoint and model card were not found at the freeze date.

## Run accounting

| Measure | October state |
| --- | ---: |
| Primary runs planned | 60 |
| Primary runs initiated | 0 |
| Primary runs remaining | 60 |
| Computational tasks | 4 per model, 20 runs |
| Synthesis tasks | 4 per model, 20 runs |
| Secondary-data tasks | 4 per model, 20 runs |
| Optional launchable shadow runs | 24 |
| Pending Argon runs | 12 |
| Maximum primary spend | £1,500 |
| Actual spend | £0 |

## Model versus harness change

The October panel is a model change. The fixed tasks, five mandatory gates, raw-pass-rate headline and £25/eight-hour per-task limits are unchanged. The exact execution harness is still unfrozen, so its commit, system prompt, tool image and provider-resolved model ID must be recorded before launch. September had no initiated runs, so October cannot yet support a temporal capability comparison; it would establish the first observed direct-run baseline.

The Hilbig-inspired v2.1 amendment remains an unmerged synthetic calibration branch. Its 60 synthetic cases and resource diagnostics cannot be combined with the autonomous-paper pass-rate denominator.

## Contamination and claim ceiling

Retrieval contamination risk remains high. The prompts are public and semantically close to identifiable papers, so title and DOI blocking does not prevent discovery through paraphrased search. Training exposure is uncertain and must be reported separately from retrieval exposure. Official scoring also remains blocked because the 12 deterministic validator fixtures are not built.

The current claim ceiling is therefore **no benchmark result**. The pack supports a planned run, not an estimate of model capability, journal acceptance or AI authorship.

## Official sources reviewed

- OpenAI, GPT-6 Astra release and system card, 3 September 2026: https://openai.com/index/safety-overview-gpt-6-astra/ and https://deploymentsafety.openai.com/gpt-6-astra
- OpenAI, GPT-6.1 Sol addendum, 29 September 2026: https://deploymentsafety.openai.com/gpt-6-1-sol
- Anthropic, Fable 5.1, 1 September 2026, and Opus 5.5, 22 September 2026: https://platform.claude.com/docs/en/models/fable-5-1/overview and https://platform.claude.com/docs/en/models/opus-5-5/overview
- Google, Gemini 3.8 Flash model card and API documentation, 2 September 2026: https://deepmind.google/models/model-cards/gemini-3-8-flash/ and https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
- SpaceXAI, Grok 4.7, 21 September 2026: https://x.ai/news/grok-4-7 and https://docs.x.ai/developers/models/grok-4.7
- DeepSeek, V4.1 Flash, 10 September 2026: https://api-docs.deepseek.com/news/news260910/
