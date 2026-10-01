# Preparation-only merge disposition, 1 October 2026

## Scope of acceptance

PRs #1 and #4 archive September and October preparation, respectively. The repository owner requested their merger after being informed of PR #1's three unresolved review findings. This note records the assistant's limited merge assessment; it is not an independent human review or evidence that those findings have been fixed.

The monthly records remain append-only. Existing tasks, gates, scoring, budgets, historical model panels and preparation records are unchanged. Merging these PRs does not authorise provider execution or official scoring.

## Binding launch hold

Do not execute either monthly launch plan from these preparation snapshots. Instructions to run tasks in the shared or monthly Antigravity documents are conditional on a separately reviewed launch-readiness change satisfying all blockers below. This is an operator instruction, not an implemented technical interlock; no fail-closed runner has been demonstrated.

| PR #1 finding | Disposition for preparation merge | Required before execution |
| --- | --- | --- |
| Semantic retrieval can reveal target papers | Accepted as a documented, unresolved execution blocker; opaque IDs do not establish uncontaminated blinding. | Implement and validate evaluator-side semantic/phrase-overlap retrieval controls, document residual retrieval and training-exposure risk, and obtain a reviewed contamination decision. Preserve the fixed task suite; any task redesign requires a separately versioned benchmark. |
| Harness provenance is incomplete | Null preparation fields are retained honestly; they are not launch-ready defaults. | Freeze and validate the harness commit, system-prompt hash, tool-image/version and provider model resolution for every launch. A preflight must refuse incomplete provenance before any task starts; resolve model metadata without starting benchmark tasks. |
| Shared DeepSeek instruction says only thinking | Historical shared instructions are not authoritative for September's corrected setting. | A September-specific execution configuration must use and validate reasoning=max against every DS_V4PRO_MAX row. Confirm the originally intended model is still accessible; do not silently substitute a rerouted alias or retrospectively claim an October execution occurred in September. |

The 12 deterministic evaluator fixtures also remain unbuilt. Official scoring stays blocked until those fixtures and their validation evidence are complete. Keep evaluator-only materials inaccessible to research agents.

The review findings remain unresolved operationally. Do not describe this disposition, green CI, or the merge itself as a fix or a launch approval.

## Measurement state

No external model task has been initiated. Recorded actual external spend is GBP 0. Raw autonomous task pass rate, workflow pass rates, evidence failures and clean execution remain unobserved; the initiated-run denominator is zero, not a measured 0% success rate. Preserve null rates and official_scoring_eligible=false.

September provides no observed baseline for a temporal comparison. The Hilbig v2.1 synthetic calibration branch and existing synthetic/forecast outputs remain separate from direct-run benchmark results.
