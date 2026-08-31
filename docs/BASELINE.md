# Business and Management Autonomous Research Benchmark

## Baseline specification, 30 August 2026

Version: **BMA-ARB v0.1**

## Purpose and claim

BMA-ARB measures whether a frontier-model agent can autonomously produce a technically complete business or management research paper from a research brief and permitted digital inputs.

The benchmark does not detect whether published papers were written by AI. It tests capability under controlled conditions. A pass means that the agent acquired or constructed the required inputs, executed the method, produced verifiable results, supported its claims and delivered a manuscript without substantive human intervention. It does not mean that a journal would accept the paper.

The population baseline is the repaired **10.20% core-business sensitivity estimate** from the 2026 Scopus study. This is the estimated share of the recovered Business, Management and Accounting corpus that appeared autonomously feasible after excluding technical cross-field papers.

## Why a new benchmark is required

Existing evaluations cover parts of the workflow:

- [PaperBench](https://openai.com/index/paperbench/) asks agents to replicate 20 ICML papers and uses 8,316 hierarchical rubric items. It establishes the value of paper-specific, author-informed rubrics.
- [CORE-Bench](https://arxiv.org/abs/2409.11363) tests computational reproduction from code and data. Its original best agent achieved 21% on the hardest tasks.
- [REPRO-Bench](https://arxiv.org/html/2507.18901v1) uses full social-science papers and reproduction packages. Existing agents achieved 21.4% accuracy and a purpose-built agent reached 36.6%.
- [ORAgentBench](https://arxiv.org/abs/2606.19787) tests end-to-end operations-research work in executable environments. Its best configuration passed 35.51% of all tasks and 20.59% of hard tasks.
- [DeepResearch Bench](https://arxiv.org/abs/2506.11763) separates report quality from citation retrieval and accuracy.
- [METR's time-horizon measure](https://metr.org/time-horizons/) tracks the human task duration at which agents reach a specified success probability. It is informative about long-horizon autonomy, but is currently based mainly on software tasks.

None tests the combination found in the Scopus taxonomy: theory construction, literature synthesis, corporate and official data extraction, statistical analysis, optimisation, citation validity and manuscript production.

## August 2026 model panel

The first scored run should use exact dated model identifiers, not mutable product names.

| Track | Model family at baseline | Reason for inclusion |
| --- | --- | --- |
| Frontier | OpenAI GPT-5.6 Sol, maximum reasoning | Current OpenAI flagship; the provider reports strong agentic knowledge-work and coding performance. |
| Frontier | Anthropic Claude Fable 5, maximum reasoning | Anthropic describes it as its highest available capability model. |
| Frontier | Google Gemini 3.1 Pro, high thinking | Google's February 2026 model card identifies it as its most advanced model for complex tasks, with a 1M-token context window. |
| Challenger | Grok 4.6, high reasoning | Current xAI knowledge-work and agentic model. |
| Open/low-cost challenger | DeepSeek V4 Pro, thinking | API-accessible model with tool use, a 1M-token context window and a dated model version. |

Provider benchmarks are recorded as context, not converted into BMA-ARB scores. OpenAI reports GPT-5.6 Sol scoring 53.6 on Agents' Last Exam. Google reports Gemini 3.1 Pro scoring 33.5% on APEX-Agents. xAI reports 57.5% for Grok 4.6 on APEX-Agents. These evaluations differ in tasks, harnesses and scoring.

## Benchmark structure

### Monthly sentinel

Run **12 tasks**, four from each production system identified in the taxonomy:

| Production system | Tasks | Taxonomy contribution to the 10.2% estimate |
| --- | ---: | ---: |
| Computational experiments and formal models | 4 | 4.65 percentage points before the cross-field exclusion |
| Literature, document and conceptual synthesis | 4 | 4.57 percentage points before the cross-field exclusion |
| Secondary-data and digital-text analysis | 4 | 3.78 percentage points before the cross-field exclusion |

Eight tasks are fixed anchors. Four are rolling challenges, retained for three monthly runs and then replaced. Fixed tasks measure longitudinal change. Rolling tasks test generalisation and reduce the effect of target-paper contamination.

### Quarterly benchmark

Expand to 30 tasks, ten per production system. Run three independent replicates per model. The quarterly run estimates task-level reliability and tests whether monthly changes exceed run-to-run variation.

### Annual refresh

Add tasks derived from papers published after the previous annual cut-off. Retire contaminated or technically obsolete cases, but retain their historic scores. Never rewrite an old task and present it as the same series.

## The 12 baseline tasks

The runner receives blinded briefs from `bma_benchmark_runner_manifest_v0.1.jsonl`. Titles, DOIs and expected findings are stored separately in `bma_benchmark_gold_manifest_v0.1.jsonl` and must not be mounted in the agent environment.

| Task | Workflow | Research family | Gold basis |
| --- | --- | --- | --- |
| BMA-COMP-01 | Formal model | Cooperative advertising | Computational Management Science paper |
| BMA-COMP-02 | Simulation | Maritime supply-chain disruption | International Transactions in Operational Research paper |
| BMA-COMP-03 | Machine learning | Innovation and corruption | Management Decision paper |
| BMA-COMP-04 | Forecasting | Financial volatility | Journal of Forecasting paper |
| BMA-SYN-01 | Meta-analysis | Female representation and corruption | Administration & Society paper |
| BMA-SYN-02 | Conceptual theory | Type II greenwashing | Organization & Environment paper |
| BMA-SYN-03 | Systematic review | Women's talent development | Human Resource Development Review paper |
| BMA-SYN-04 | Systematic review | Destructive leadership in education | Educational Management Administration & Leadership paper |
| BMA-DATA-01 | Corporate-report panel | Governance, CSR and cost of equity | Journal of Financial Reporting and Accounting paper |
| BMA-DATA-02 | Provincial panel | Digital economy and logistics emissions | Cleaner Logistics and Supply Chain paper |
| BMA-DATA-03 | Input-output analysis | Malaysia's trade partners | Foreign Trade Review paper |
| BMA-DATA-04 | Corporate-report content analysis | Biodiversity accountability | Accounting, Auditing & Accountability Journal paper |

The papers are reference architectures, not text-matching targets. The benchmark should use task variants where practical, such as altered date windows, held-out jurisdictions or modified model assumptions. This makes memorising the published paper insufficient.

## Agent environment

Each run receives:

- the blinded task brief and output schema;
- a browser and scholarly search, with the target title and DOI blocked;
- a terminal with Python and R, plus common statistical, optimisation and document-processing packages;
- an empty working directory and persistent run log;
- the same wall-time and spend cap for every model in a track.

Recommended monthly capability budget: **8 hours wall time and £25 equivalent API spend per task**. Record actual spend. Do not stop a cheaper model early merely because another model has used less money.

No human may select sources, repair code, interpret an error, suggest a method or edit the manuscript. Infrastructure-only recovery, such as restarting a failed container without changing state, must be logged.

## Required outputs

Every task must produce:

1. `manuscript.md`, structured as a journal article.
2. `research_log.jsonl`, containing every search, source decision, tool call and model action.
3. `sources.csv`, with identifiers, URLs, access dates and claimed uses.
4. `analysis/`, containing data, executable code, environment lock file and generated tables or figures.
5. `claim_evidence_ledger.csv`, mapping each substantive claim to a result or source.
6. `verification_report.md`, listing failed checks, sensitivity tests and unresolved limitations.

## Scoring and release rule

### Mandatory gates

A task is an autonomous-paper pass only when all five gates pass:

| Gate | Pass condition |
| --- | --- |
| Completion | All required artefacts exist and the manuscript is coherent and complete. |
| Executability | The analysis runs from a clean environment without human repair. |
| Result validity | Hidden validators confirm the main calculations, constraints or coded evidence. |
| Evidence integrity | At least 95% of checked substantive claims are supported, every cited item exists, and no citation is materially misrepresented. |
| Autonomy | No substantive human intervention occurred after the run began. |

The 95% threshold applies to sampled claim-source pairs. A single fabricated reference fails the evidence gate.

### Quality profile

Score six dimensions from 0 to 4:

- research design;
- source and data integrity;
- analytical correctness;
- robustness and verification;
- theoretical contribution;
- manuscript and reference quality.

Report the profile even when a mandatory gate fails. Do not allow fluent writing to compensate for invalid analysis.

### Headline measures

Report, for each model and exact harness:

- autonomous-paper pass rate, with the numerator and denominator;
- median quality score among all tasks, not only passes;
- workflow-specific pass rates;
- claim-support precision and fabricated-reference count;
- clean-execution rate;
- median cost, tokens, tool calls and wall time per task;
- pass yield per £100.

Do not average models into a single “frontier AI” score. The unit being evaluated is the **model, reasoning setting, harness and tool environment**.

## Baseline interpretation

The August 2026 evidence supports three statements:

1. Frontier systems have strong component capabilities, including search, coding, long-context processing and tool use.
2. Relevant end-to-end research benchmarks still show low reliability. ORAgentBench's best pass rate is 35.51%; REPRO-Agent reaches 36.6% accuracy on reproducibility assessment.
3. No published score currently establishes how often a frontier system can autonomously produce a valid business or management paper.

The **initial BMA-ARB model score is therefore deliberately unreported until the 12 tasks are executed**. Vendor benchmark scores are not a substitute. The first controlled run becomes the August 2026 capability baseline.

## Monthly operating procedure

1. Freeze exact model IDs, reasoning settings, harness commit, tools, budget and task versions.
2. Run the 12 tasks independently. Models cannot see other runs or the gold pack.
3. Execute deterministic validators before any LLM judging.
4. Use two blinded judges for rubric dimensions and adjudicate disagreements of two or more scale points.
5. Publish the task-level results, failures, cost and run provenance. Append a new month; never overwrite an earlier score.

Every third month, repeat all tasks three times. A capability-improvement claim requires either an increase in fixed-anchor pass rate sustained for two months or a quarterly difference whose bootstrap interval excludes zero. Until enough quarters exist, report raw changes without a trend claim.

## Principal validity risks

- **Target-paper contamination:** block target identifiers, use task variants, run phrase-overlap checks and retain rolling challenges.
- **Harness drift:** version the entire agent scaffold. A tool improvement is not a model improvement.
- **Judge circularity:** deterministic validators take precedence; judges cannot see model identity.
- **Task drift:** fixed-anchor and rolling-challenge scores are reported separately.
- **Publication overclaim:** the benchmark measures research-artifact completion, not peer-review acceptance or actual AI use in published work.
- **Selective reruns:** report every initiated run. Infrastructure failures are a separate outcome, not silently discarded.

## Baseline deliverables

- `tasks/anchors_v0.1.jsonl`: blinded task briefs for the execution environment.
- `evaluator/private/anchor_gold_manifest_v0.1.jsonl`: evaluator-only paper identifiers and expected architecture; excluded from the public repository.
- `evaluator/public/score_schema_v0.1.json`: mandatory result structure.
- `scripts/validate_results.py`: deterministic schema, gate and aggregation validator.
