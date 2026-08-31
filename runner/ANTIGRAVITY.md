# Execute BMA-ARB v0.1 in Antigravity

## Objective

Run either the 12-task anchor set, the 12-task counterfactual set, or the paired 24-task Business and Management Autonomous Research Benchmark without exposing evaluator-only material to research agents. Produce one auditable result row per model-task-run.

## Inputs

- `tasks/anchors_v0.1.jsonl`: public anchor briefs.
- `tasks/counterfactuals_v0.1.jsonl`: public paired transfer briefs.
- `evaluator/public/score_schema_v0.1.json`: public result schema.
- `evaluator/private/`: evaluator-only. Never mount, quote or expose it to runner agents.
- `scripts/validate_results.py`: run after score rows are assembled.

## Run isolation

1. Create one clean workspace per task and model.
2. Start a fresh agent with no conversation history.
3. Give it only its single blinded task record, the common operating rules and an empty workspace.
4. Enable browser/search, terminal, Python and R. Block exact target-title and DOI searches using the evaluator-only manifest outside the runner workspace.
5. Set an eight-hour wall-time limit and a £25-equivalent API-spend ceiling.
6. Record the exact provider model ID, reasoning setting, Antigravity version, harness commit, system prompt hash, tool versions and start time.
7. Do not permit communication between task agents.
8. Randomise task order independently by model, but retain the seed.
9. For a paired run, do not expose the pair identifier or the other member's artefacts to the research agent.

## Common runner instruction

> Complete the assigned research task autonomously. Acquire only permitted digital inputs. Make all methodological and source-selection decisions yourself. Produce manuscript.md, research_log.jsonl, sources.csv, analysis/, claim_evidence_ledger.csv and verification_report.md. Your analysis must execute from a clean environment. Record failed attempts and unresolved limitations. Do not ask for human methodological advice or editing. Stop when the time or spend limit is reached and preserve all partial artefacts.

## Evaluation order

1. Check required files and run provenance.
2. Rebuild the analysis in a clean container.
3. Apply task-specific hidden validators to datasets, constraints, calculations, results and coded evidence.
4. Verify every reference exists.
5. Sample substantive claims and check them against cited sources or generated results.
6. Run two blinded rubric judges. Hide model identity and provider.
7. Adjudicate only disagreements of two or more points on a 0-4 dimension, or disagreements on a mandatory gate.
8. Write a result object conforming to `bma_benchmark_score_schema_v0.1.json`.

Deterministic validation overrides an LLM judge. Fluent prose cannot repair a failed calculation, fabricated reference or unsupported claim.

## Baseline model panel

Run the accessible models from this panel and record omissions explicitly:

- GPT-5.6 Sol, maximum reasoning;
- Claude Fable 5, maximum reasoning;
- Gemini 3.1 Pro, high thinking;
- Grok 4.6, high reasoning;
- DeepSeek V4 Pro, thinking.

Do not substitute a model silently. If a dated snapshot is available, use it. If only a mutable alias is available, record the alias and retrieval timestamp.

## Output structure

```text
bma_arb_runs/
  2026-08/
    run_manifest.json
    raw/
      MODEL_ID/
        TASK_ID/
          RUN_ID/
    scores/
      results.jsonl
      bma_benchmark_summary.json
    validation/
      schema_validation.log
      deterministic_gate_results.jsonl
      judge_disagreements.jsonl
      adjudications.jsonl
```

Run:

```bash
python scripts/validate_results.py \
  bma_arb_runs/2026-08/scores/results.jsonl \
  --output bma_arb_runs/2026-08/scores/bma_benchmark_summary.json
```

## Release checks

- Exactly 12 result rows per model for an anchor-only or counterfactual-only run, or 24 for a paired run.
- No initiated run omitted.
- Anchor and counterfactual results reported separately, with the paired transfer table when both sets are run.
- Every infrastructure failure retained and distinguished from agent failure.
- Gold manifest absent from all runner logs and mounted paths.
- All costs, tokens, tool calls and wall times reported.
- No claim that the benchmark measures journal acceptance or actual AI authorship.
