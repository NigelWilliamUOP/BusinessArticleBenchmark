import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_jsonl(path):
    rows = []
    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_number}: invalid JSON: {exc}") from exc
    return rows


def weighted_geometric_mean(weights, scores):
    return math.exp(sum(weight * math.log(scores[benchmark]) for benchmark, weight in weights.items()))


def leave_one_out(weights, scores):
    values = []
    for dropped in weights:
        retained_total = 1.0 - weights[dropped]
        if retained_total <= 0:
            continue
        revised = {key: value / retained_total for key, value in weights.items() if key != dropped}
        values.append({"dropped_benchmark": dropped, "score": weighted_geometric_mean(revised, scores)})
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default=str(ROOT / "synthetic" / "benchmark_registry_v0.1.jsonl"))
    parser.add_argument("--crosswalk", default=str(ROOT / "synthetic" / "task_benchmark_crosswalk_v0.1.json"))
    parser.add_argument("--taxonomy", default=str(ROOT / "data" / "taxonomy_weights_v0.1.json"))
    parser.add_argument("--output", default=str(ROOT / "synthetic" / "results" / "frontier_envelope_2026-08.json"))
    args = parser.parse_args()

    registry_rows = load_jsonl(args.registry)
    crosswalk = load_json(args.crosswalk)
    taxonomy = load_json(args.taxonomy)
    registry = {row["benchmark_id"]: row for row in registry_rows}
    if len(registry) != len(registry_rows):
        raise SystemExit("Duplicate benchmark_id")
    scores = {key: row["score"] for key, row in registry.items()}

    task_results = []
    system_values = defaultdict(list)
    for task_id, specification in crosswalk["tasks"].items():
        weights = specification["weights"]
        if abs(sum(weights.values()) - 1.0) > 1e-12:
            raise SystemExit(f"{task_id}: weights do not sum to one")
        missing = set(weights) - scores.keys()
        if missing:
            raise SystemExit(f"{task_id}: missing benchmarks {sorted(missing)}")
        score = weighted_geometric_mean(weights, scores)
        loo = leave_one_out(weights, scores)
        sensitivity = [item["score"] for item in loo]
        system = {"COMP": "computational", "SYN": "synthesis", "DATA": "secondary_data"}[task_id.split("-")[1]]
        system_values[system].append(score)
        task_results.append({
            "task_id": task_id,
            "production_system": system,
            "synthetic_score": score * 100,
            "leave_one_benchmark_out_range": [min(sensitivity) * 100, max(sensitivity) * 100],
            "weights": weights,
            "rationale": specification["rationale"],
        })

    overall = sum(item["synthetic_score"] for item in task_results) / len(task_results)
    global_loo = []
    for dropped in registry:
        revised_tasks = []
        for specification in crosswalk["tasks"].values():
            weights = specification["weights"]
            if dropped not in weights:
                revised_tasks.append(weighted_geometric_mean(weights, scores) * 100)
                continue
            retained_total = 1.0 - weights[dropped]
            revised = {key: value / retained_total for key, value in weights.items() if key != dropped}
            revised_tasks.append(weighted_geometric_mean(revised, scores) * 100)
        global_loo.append({"dropped_benchmark": dropped, "index": sum(revised_tasks) / len(revised_tasks)})

    system_indices = {
        system: sum(values) / len(values) * 100
        for system, values in sorted(system_values.items())
    }
    taxonomy_weighted_capability = sum(
        system_indices[system] * specification["share_of_core_opportunity"]
        for system, specification in taxonomy["systems"].items()
    )

    taxonomy_weighted_loo = []
    for dropped in registry:
        revised_system_values = defaultdict(list)
        for task_id, specification in crosswalk["tasks"].items():
            weights = specification["weights"]
            retained_total = 1.0 - weights.get(dropped, 0.0)
            revised = {
                key: value / retained_total
                for key, value in weights.items()
                if key != dropped
            }
            score = weighted_geometric_mean(revised, scores) * 100
            system = {"COMP": "computational", "SYN": "synthesis", "DATA": "secondary_data"}[task_id.split("-")[1]]
            revised_system_values[system].append(score)
        revised_system_indices = {
            system: sum(values) / len(values)
            for system, values in revised_system_values.items()
        }
        weighted_score = sum(
            revised_system_indices[system] * specification["share_of_core_opportunity"]
            for system, specification in taxonomy["systems"].items()
        )
        taxonomy_weighted_loo.append({
            "dropped_benchmark": dropped,
            "taxonomy_weighted_capability": weighted_score,
        })

    corpus_share = taxonomy["core_opportunity_percent"] * taxonomy_weighted_capability / 100
    corpus_share_loo = [
        taxonomy["core_opportunity_percent"] * item["taxonomy_weighted_capability"] / 100
        for item in taxonomy_weighted_loo
    ]

    output = {
        "index_version": crosswalk["version"],
        "as_of": crosswalk["as_of"],
        "index_name": crosswalk["index_name"],
        "composite_type": crosswalk["composite_type"],
        "headline": {
            "synthetic_frontier_index": overall,
            "scale": "0_to_100",
            "leave_one_benchmark_out_range": [
                min(item["index"] for item in global_loo),
                max(item["index"] for item in global_loo),
            ],
            "status": "model_implied_synthetic_signal",
        },
        "production_system_indices": system_indices,
        "task_results": task_results,
        "benchmark_registry": registry_rows,
        "global_leave_one_out": global_loo,
        "illustrative_corpus_share_proxy": {
            "taxonomy_weighted_capability_within_opportunity_envelope": taxonomy_weighted_capability,
            "share_of_recovered_corpus_percent": corpus_share,
            "leave_one_benchmark_out_range": [min(corpus_share_loo), max(corpus_share_loo)],
            "opportunity_envelope_percent": taxonomy["core_opportunity_percent"],
            "status": "illustrative_only_not_a_prevalence_estimate",
        },
        "claim_rules": crosswalk["claim_rules"],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
