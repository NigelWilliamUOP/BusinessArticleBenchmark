# Contributing to the genealogy

## Add a curated node

Add one JSON object to `benchmark_nodes_v0.1.jsonl`. Use a paper, official benchmark page or maintained repository as the primary source. Blog summaries may help discovery but should not be the sole source for a curated record.

Required fields are enforced by `scripts/validate_genealogy.py`. `evidence_note` should state the concrete contribution. `claim_boundary` should state what the source does not establish.

## Add an edge

Add one record to `benchmark_edges_v0.1.jsonl`. Allowed relations are:

- `extends`
- `evaluates_on`
- `evaluates`
- `operationalises`
- `uses_verifier`
- `adapts`
- `complements`
- `closest_precedent`
- `planned_collaboration`
- `informs`
- `shares_task_lineage`

A relationship must be supportable from the source. Do not use `extends` where two projects merely address similar problems.

## Candidate review

The weekly bot appends arXiv discoveries to `candidates/latest.jsonl`. A candidate remains unreviewed until a person:

1. checks the primary paper or project page;
2. resolves duplicates and renamed versions;
3. enters a bounded curated node;
4. adds supported relationships;
5. removes the promoted candidate from the queue.

The bot never edits curated records.

## Portsmouth data

Only aggregate, privacy-safe statistics may be committed. Do not add output titles, author names, staff identifiers, emails, reviewer grades or provisional REF selection decisions. Journal weighting must come from an authorised public-metadata join, not inference from titles.

## Validation

```bash
python scripts/validate_genealogy.py
python scripts/render_genealogy.py --check
```
