# Operating and integration specification

## 1. Preserve the estimands

Report paper-level raw autonomous task pass rate first. A pass requires the
existing completion, executability, result-validity, evidence-integrity and
autonomy gates. All initiated tasks, including infrastructure failures, remain in
the denominator. Do not give independent quality status to a producing agent.

Report fixed anchors, counterfactual transfer and prospective tasks separately.
Do not change the existing synthetic frontier index or corpus-share forecast.
Component decisions remain diagnostic, not substitutes for full task execution.

For the decision pilot, report mechanical correct/initiated, family breakdowns,
failed or unusable outputs, all planned-but-not-started cases and routing choices.
A justified `insufficient`, `infeasible`, rejection or missing-data decision passes
only when the frozen case reference permits it. Blanket refusal earns no credit.
Scientific decision correctness additionally requires independently adjudicated
rationale/evidence, not merely a label and a citation identifier.

## 2. Data and adjudication states

| State | Use | Permitted claim |
|---|---|---|
| Public synthetic development, 12 examples | Prompt/interface development | Development behaviour only |
| Public synthetic calibration, 60 examples | Debugging and matched diagnostic | Mechanical fixture performance only |
| Audited fixed empirical panel, not built here | Comparable measurements across dates | Conditional on the frozen task population |
| Protected prospective panel, not imported | Transfer and temporal adaptation | New-task results, separately reported |

For each real candidate, complete AUDIT_TEMPLATE.json before model execution.
Document the construct, evidence actually available to the worker, source/version
checksums, a defensible reference answer and alternatives, plus the conditions
under which uncertainty is correct. Use deterministic validation first. Have an
independent evaluator adjudicate judgement-dependent cases; Nigel is the agreed
human authority. Model agreement can trigger review, not overwrite the answer.

Record disagreements before consensus. Do not replace original labels silently.
An adjudication change creates a new reference version, with a reason, reviewer,
time and affected results. Recompute paired comparisons under the same reference
version for all systems. Keep the old results available. Independent adjudication
has not been performed for these synthetic proposals.

## 3. Controlled and system comparisons

The fixed-lower and fixed-higher conditions hold the harness, evidence packets,
output rules, tools and resource ceilings constant. Record exact provider, model
version, reasoning setting and harness commit. Equivalent requested parameters do
not guarantee equivalent effective provider settings; capture both.

The routed condition changes the system, not just the model. Its current routing
rule is deliberately simple: send high inferential-demand or high temporal-update
cases to the higher slot, all others to the lower slot. The case profiles and
thresholds were authored before any model results. No routing performance has
been established. Development-only optimisation must produce a new frozen policy
before evaluation. Never choose a per-case winner after reading test results.

Keep the published calibration score descriptive because the cases/answers are
public. For a later private fixed panel, freeze model settings, prompts, evidence,
scorers, task order/seed, worker permissions and routing before calls begin.
Interleave conditions within the execution window to reduce provider-time drift;
record real timestamps. Declare any repeat-run panel across all matched cases in
advance. Internal self-correction may use the fixed budget. A new external restart
is a new attempt and cannot secretly replace a failed primary run.

## 4. Worker and evaluator separation

1. Verify the frozen manifest and retain its commitment outside worker access.
2. Mount only `prepared/requests/<job_id>.json` into a fresh worker environment.
3. Do not mount catalogue.py, the public calibration references, tests, source
   repositories, SRO repair materials, historical outcomes after the cutoff, or
   previous workers' outputs. Disable browsing for this bounded decision pilot.
4. Before dispatch, append a `started` event with the frozen job ID and a unique
   run ID. Reserve approved spend in the external provider runner before calling.
5. Append one `finished` event containing the untouched parsed prediction or an
   explicit terminal failure, together with actual usage and resource provenance.
   Missing replies after initiation remain interrupted failures. Preserve raw
   provider responses and tool traces externally with checksums; do not replace
   uncertain charges with zero. Never put credentials in these files.

The shipped program has no network adapter or operating-system sandbox. These
are mandatory responsibilities of the later approved worker integration, not
capabilities claimed by this pack. Programmatic integration uses:

```python
from pathlib import Path
from bma_v21.engine import Ledger
ledger = Ledger(Path("run/attempts.jsonl"))
ledger.append("started", run_id, {"job_id": job_id, "execution_mode": "actual_model"})
# An approved isolated provider/harness runner executes the frozen request here.
ledger.append("finished", run_id, {
    "status": terminal_status,
    "prediction": parsed_prediction,
    "resources": resource_record,
})
```

The example is an interface contract, not a live provider implementation.
Score a completed or interrupted ledger with:

```bash
python -m bma_v21 score --frozen bma_v21/runs/frozen \
  --prepared bma_v21/runs/pilot --ledger run/attempts.jsonl \
  --output run/decision_report.json
```

## 5. Resource accounting

One resource row represents one initiated attempt. `direct_cost_gbp` covers
computation, hosting and attributable tools; keep detailed itemised charges and
original currencies/dated conversion records in the external run archive. The
basis is `provider_billed`, `estimate`, `unknown`, or `synthetic_zero` (test doubles
only). There is no assumption that open-weight inference costs nothing.

Record production, operational verification, rework and benchmark-only evaluation
minutes separately. Unknown minutes are null. A recorded zero means a measured
absence, not missing data. Operational verification is part of ordinary research
production; benchmark-only evaluation is disclosed separately.

`cost_summary` totals recorded direct cost across successes and failures. It adds
production, operational verification and rework at an explicitly supplied labour
rate, and divides by independently qualified outputs only when records are
complete. A missing cost/time entry blocks a complete unit-cost estimate. Zero
qualified outputs produce an undefined unit cost with the expenditure reported,
not a manufactured finite number. Estimated charges remain labelled estimates.

Do not pool papers, programme updates and opportunity assessments in one unit-cost
denominator. The paper-gate adapter rejects other output types. Those agents need
their own reviewed outcome contracts rather than transplanted manuscript gates.
Released researcher time requires a comparable-quality human/hybrid baseline; it
is not inferred from inference speed. No released-time estimate is made here.

## 6. Three-agent integration and holdouts

Study Producer supplies source/claim and executable-artifact records, not its own
independent grade. Programme Steward supplies original versus revised vintages
and immutable baseline predictions. Opportunity Scout supplies claim-specific
measurement/join decisions and the proposed discriminating test. Use these logs
to sample and link future real decisions to their originating study ID.

Keep per-study clusters in paired inference. Resample source studies, carrying
all their decisions and both systems' scores together. The implementation
calculates an equal-item paired difference. Its minimum ten-cluster reporting
rule is a pilot convention, not proof that ten studies ensure reliable coverage.
Report cluster count, case count and family mix. Do not pool changing monthly
panels or use public synthetic families to infer a population-wide paper share.

MISSOURI-001 remains calibration. Do not read the SRO-001 repair package,
adjudications or labels during prompt/routing development. SRO's domain/method
classification is unchanged. CEMENT-001 enters only through an independently
frozen real evidence vintage. Neither empirical package was imported here.
The AI-Scientist-fork draft PR #2 remains separate and unmerged.

## 7. Release gate and handoff

Current deliverables are source code, tests, synthetic fixtures, frozen request
plans and a draft protocol amendment. A private, independently adjudicated real
panel, named/configured models and approved live execution are outstanding.
There is no scientific capability baseline from this build. No repository merge,
paid run, recurring task, publication or registration has been activated.

For a later coding agent: run the tests unchanged; preserve this read-only
calibration release; implement provider isolation and a private-panel adapter in
a separate branch; reuse the existing research_campaigns budget/usage interfaces
where verified compatible; add mocked transport and no-leakage tests before any
live call. Do not access SRO protected evaluation content to make the build pass.
