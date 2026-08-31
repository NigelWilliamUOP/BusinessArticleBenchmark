# Compute investment guide for business schools

## Decision principle

The benchmark should drive workload investment, not the announced size of a future model. Business schools normally need access to frontier inference, secure data handling, retrieval, execution and verification. They do not need to train a frontier foundation model.

Training frontier models is becoming more capital intensive, while capability-equivalent inference costs have historically fallen quickly. UK researchers may also seek access to the national AI Research Resource. The default near-term strategy is therefore **API-first, portable and measured**, with local accelerators reserved for specific open-model, privacy or high-utilisation workloads.

## Four investment layers

| Layer | Invest now | Scale when the benchmark shows |
| --- | --- | --- |
| Frontier access | Multi-provider API budget, usage controls and procurement routes | Sustained pass-rate gains justify routine research use |
| Research execution | Isolated containers, CPU/RAM, modest accelerator pool and reproducible environments | Computational-task execution or queueing becomes the binding constraint |
| Evidence infrastructure | Licensed retrieval, document parsing, corporate-report store, provenance and citation verification | Synthesis or secondary-data failures concentrate in retrieval and evidence gates |
| Assurance | Independent reruns, leakage tests, source audits and human sign-off for regulated claims | More outputs reach completion but fail validity or evidence integrity |

## Buy-versus-access gates

Consider owned GPU capacity only when all of the following are documented:

1. a stable open-weight workload that cannot be met by the required frontier APIs;
2. sustained utilisation high enough to compare with three-year fully loaded ownership cost;
3. data-sensitivity or latency requirements that cannot be met contractually in cloud services;
4. staff capacity for security, drivers, scheduling, monitoring and model serving;
5. a benchmark showing that local models remain within the school's acceptable capability gap.

Otherwise use provider APIs, institutional cloud agreements or national shared compute. Reassess quarterly because hardware performance, model efficiency and token prices change faster than university capital cycles.

## Capacity calculation

For a candidate service, estimate annual frontier-model expenditure as:

\[
B=12\,U\,J\,A\,c(1+q),
\]

where \(U\) is active researchers, \(J\) initiated research tasks per researcher per month, \(A\) is mean attempts per task, \(c\) is measured cost per attempt from BMA-ARB, and \(q\) is the contingency proportion. Report low, expected and high utilisation. Do not use list-price token arithmetic when benchmark runs provide measured task cost.

## Investment triggers

- Fund retrieval and verification first when evidence-integrity failures exceed analytical failures.
- Fund execution sandboxes or accelerators when valid plans fail because of runtime, memory or queue limits.
- Fund methods training when analyses execute but fail leakage, identification or robustness checks.
- Expand API budgets when valid pass yield per £100 improves and demand is constrained by quotas.
- Delay hardware purchase when a forthcoming platform claim is unverified or workload utilisation is uncertain.

The forecast should recommend capability and capacity bands, not a particular GPU purchase, until benchmark workload telemetry establishes demand.
