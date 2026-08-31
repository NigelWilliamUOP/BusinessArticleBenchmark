# Results

Official result releases should be append-only and organised by `YYYY-MM/model/harness-commit/`.

Publish:

- one result row per initiated task run;
- task-level gate and quality outcomes;
- aggregate anchor and counterfactual summaries;
- costs, wall time, tokens and tool calls;
- hashes for run artefacts and frozen source snapshots;
- infrastructure failures and rerun decisions.

Do not publish evaluator-only answer keys or hidden validator fixtures.
