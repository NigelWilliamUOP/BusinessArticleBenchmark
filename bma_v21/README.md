# Matched research-decision and resource amendment

Version: BMA-lifecycle-amendment-2.1.0. Built 23 September 2026.

This is an additive implementation alongside **BMA-ARB-v0.1**, not a relabelling
of the existing benchmark or a new empirical capability result. It adapts matched
inputs, task-level diagnosis and cost provenance from Hanno Hilbig's Political
Science LLM Benchmark. The existing five paper gates and raw autonomous task pass
rate remain unchanged.

## Implemented

- 60 original **public synthetic calibration** cases, ten in each of six families,
  plus 12 distinct development examples. Every case has an evidence packet,
  proposed reference answer, acceptable response labels, source requirements,
  a complexity profile and a reference-audit record. No published paper or private
  SRO reference material was used to generate them.
- Immutable-on-write data/configuration snapshots, checksums, answer-free request
  projection and 180 matched pilot request specifications across three conditions.
- Fixed lower-cost slot, fixed higher-capability slot and preregistered static
  routing. Model identities are deliberately unassigned. All conditions receive
  identical case packets and ceilings. The routed pilot assigns 40 cases to the
  lower slot and 20 to the higher slot, based on the predeclared task profile.
- Initiation-first, single-writer hash-chain ledger; every initiated failure and
  interruption remains visible. Selective external restarts and changed case
  plans are rejected. Missing human time and uncertain charges are not zero.
- Mechanical decision/numeric/citation scoring, separate independent paper-gate
  summary, operational cost accounting, and paired source-cluster uncertainty
  calculations. No component score can become a paper pass or population forecast.

## Execute locally

Python 3.10+; standard library only. From the directory containing `bma_v21/`:

```bash
python -m unittest bma_v21.test_engine -v
python -m bma_v21 demo --output bma_v21/runs/demo
python -m bma_v21 freeze --output bma_v21/runs/frozen
python -m bma_v21 prepare --frozen bma_v21/runs/frozen --output bma_v21/runs/pilot
python -m bma_v21 prepare --frozen bma_v21/runs/frozen --output bma_v21/runs/development --split development
python -m bma_v21 verify --frozen bma_v21/runs/frozen
```

Existing output directories are never overwritten. Use a new versioned path for
another run. The demo creates its own frozen dataset and request plan. It reads
public reference answers as a **test oracle**, injects four failures per condition
and tests accounting. It is not an LLM run, a routed-system comparison, a study
replication or a journal-readiness assessment.

## Metric boundaries

The primary scientific endpoint remains the original raw autonomous task pass
rate across all initiated end-to-end paper tasks, subject to all five mandatory
gates. This package's decision endpoint is explicitly
`mechanical_decision_diagnostic_only`.

Mechanical checks require an exact case ID, an accepted decision, a correct
numeric result where specified, valid evidence references and a non-empty brief
justification. They **do not establish that the justification is substantively
correct**. A deliberately irrelevant justification with otherwise correct fields
passes the mechanical layer in one regression test. This limitation is explicit;
independent rationale adjudication is required for a scientific decision pass.

The shipped answer keys are authored calibration proposals, not human gold. They
are public, and thus not a contamination-resistant test set. The development
examples are separate prompts but share methods with the calibration examples;
they are not an independent transfer sample. Six conservative family clusters
are used for this synthetic diagnostic; no confidence interval is reported as
though the 60 decisions represented 60 independent empirical studies.

## Preserved project boundaries

MISSOURI-001 remains calibration material. SRO-001 remains a prospective holdout;
its repair package, prior adjudications and private labels have not been read,
imported, changed or exposed by this implementation. CEMENT-001 needs a separately
frozen real evidence vintage before prospective longitudinal evaluation.

The existing AI-Scientist-fork three-agent branch is not modified or merged. This
package supplies requests, evaluation/accounting interfaces and the integration
contract in RUNBOOK.md; it is not a tested live integration with those agents.
The existing sentinel and anchor/counterfactual tasks remain intact.

## Live execution is deliberately blocked

There are no API calls in this package and no provider adapter. The default
external-spend authorisation is GBP0. The model slots and reasoning settings are
null. The readiness report always blocks an official run of this public starter
panel. There is no automatic private-panel importer.

A later separately reviewed runner must supply exact model/settings identifiers,
approved spend, actual provider usage, safe worker isolation and independently
audited held-out cases. Preparing requests is not running them. Supplying all
these prerequisites should result in a new versioned prospective adapter, not
weakening this starter release's readiness flag.

## Assurance limits

The hash chain is a single-writer integrity aid, not a digital signature, access
control system or filesystem sandbox. Retain the frozen manifest and ledger head
outside the worker's permissions to detect wholesale history replacement. The
allowlisted request projection prevents accidental answer fields being exported;
only a separately configured operating-system/container boundary can prevent a
worker from opening the public repository or evaluator files. No such worker was
launched during this build.

The 180-second and 1,200-output-token decision ceilings are initial operational
settings, not empirical findings. The GBP0 ceiling is a safety default. Existing
end-to-end budgets are not changed: preserve the previously agreed sentinel
3-hour/GBP10 limits where applicable; the public protocol's recommended monthly
8-hour/GBP25 ceiling remains distinct.

## Attribution

Hanno Hilbig (2026), Political Science LLM Benchmark, September panel, inspected
23 September 2026: https://www.hannohilbig.com/llm-benchmark/

Source code and methodological documentation:
https://github.com/hhilbig/polsci-open-bench

This implementation is original; no task texts, labels or code were copied from
Hilbig's repository. Author-specific numerical results are not transferred to BMA.
Code follows the parent repository's MIT licence; task briefs and documentation
follow its CC BY 4.0 licence.
