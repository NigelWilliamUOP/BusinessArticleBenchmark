# Living AI-research benchmark genealogy

This directory records how BMA-ARB and the planned Portsmouth Business School Research Production Frontier relate to adjacent AI-scientist systems, benchmarks, verifier programmes and evaluation frameworks.

The genealogy is not a leaderboard. It separates five questions that are often collapsed:

1. Can an agent complete a bounded research task?
2. Can it produce a complete and reproducible paper?
3. Does it revise hypotheses and choose informative tests?
4. What human guidance and verification were supplied?
5. What combination of human time and compute produces journal-ready outputs at the lowest resource cost?

## Portsmouth position

The local programme treats the **research production function** as the central object:

\[
J = f(H, C, O, V, P)
\]

where \(J\) is the number of journal-ready outputs, \(H\) is human effort, \(C\) is compute, \(O\) is orchestration, \(V\) is verification and \(P\) is the research-portfolio mix.

The quality floor is work acceptable to a journal represented in Portsmouth's observed portfolio. Released academic time counts as a resource benefit. It must be reported either as a monetary-equivalent resource release or as additional output capacity, not both in one headline benefit.

The initial infrastructure comparator is API-first. Owned GPUs remain an option in the model, not a required result.

## Curated and candidate layers

- `benchmark_nodes_v0.1.jsonl` is the reviewed node registry.
- `benchmark_edges_v0.1.jsonl` records supported relationships among nodes.
- `collaboration_targets_v0.1.jsonl` records concrete routes for joint work.
- `portsmouth_portfolio_profile_v0.1.json` contains privacy-safe aggregate evidence from the current UOA17 output universe.
- `candidates/latest.jsonl` is an automatically discovered queue. Entries are never promoted automatically.
- `generated/GENEALOGY.md` is a deterministic human-readable rendering.

The scheduled workflow queries arXiv weekly and opens a draft pull request only when it finds new candidates. Official project pages on the manual watchlist require human review because their structure and claims can change without a stable API.

## Collaboration-first rule

A new Portsmouth component should be built only where no suitable reusable component exists. The first route is to approach Project APE and CRED about:

- reusing their public-data paper-production and executable-paper infrastructure;
- extending the CRED verifier taxonomy to business and management;
- adding priced human guidance, blinded journal-readiness review and actual-portfolio weighting;
- sharing methods and results rather than constructing a parallel verifier stack.

Every proposed relationship must name a source and state a claim boundary. Similarity of terminology is not evidence of technical lineage.

## Update commands

```bash
python scripts/validate_genealogy.py
python scripts/render_genealogy.py
python scripts/render_genealogy.py --check
python scripts/update_genealogy_candidates.py
```

To rebuild the privacy-safe Portsmouth aggregate from an authorised internal workbook:

```bash
python scripts/build_portsmouth_portfolio_profile.py \
  --input "/path/to/REF audit workbook.xlsx" \
  --sheet UOA17 \
  --output genealogy/portsmouth_portfolio_profile_v0.1.json
```

The builder emits aggregates only. It does not copy titles, authors, identifiers, grades or selection fields into the repository.

## Review rule

Promotion from the candidate queue requires:

- a primary source;
- a stable identifier;
- a clear evaluation unit;
- explicit human-guidance and verifier fields;
- a bounded statement of what the work does not establish;
- at least one supported edge to the existing genealogy, where relevant.

Version the registry when field definitions change. Never silently replace historic benchmark results or claims.
