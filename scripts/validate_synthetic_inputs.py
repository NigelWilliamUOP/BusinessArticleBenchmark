import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "synthetic" / "benchmark_registry_v0.1.jsonl"
CROSSWALK = ROOT / "synthetic" / "task_benchmark_crosswalk_v0.1.json"
ANCHORS = ROOT / "tasks" / "anchors_v0.1.jsonl"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path):
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
    return rows


def main():
    registry = load_jsonl(REGISTRY)
    crosswalk = load_json(CROSSWALK)
    anchors = load_jsonl(ANCHORS)

    required_registry = {
        "benchmark_id", "benchmark", "metric", "score", "score_scale",
        "reported_system", "published_date", "source_url", "source_type",
        "capability", "qualification",
    }
    benchmark_ids = []
    for row in registry:
        missing = required_registry - row.keys()
        assert not missing, f"registry row missing {sorted(missing)}"
        assert 0 < row["score"] <= 1
        assert row["score_scale"] == "0_to_1"
        assert row["source_url"].startswith("https://")
        benchmark_ids.append(row["benchmark_id"])
    assert len(registry) == 7
    assert len(benchmark_ids) == len(set(benchmark_ids)), "duplicate benchmark_id"

    anchor_ids = {row["task_id"] for row in anchors}
    assert len(anchor_ids) == 12
    assert set(crosswalk["tasks"]) == anchor_ids
    assert crosswalk["composite_type"] == "best-published-system frontier envelope"
    assert len(crosswalk["claim_rules"]) >= 4

    referenced = set()
    for task_id, specification in crosswalk["tasks"].items():
        weights = specification["weights"]
        assert weights, f"{task_id}: empty weights"
        assert abs(sum(weights.values()) - 1.0) < 1e-12, f"{task_id}: weights do not sum to one"
        assert all(weight > 0 for weight in weights.values()), f"{task_id}: non-positive weight"
        assert set(weights) <= set(benchmark_ids), f"{task_id}: unknown benchmark"
        assert specification["rationale"].strip()
        referenced.update(weights)
    assert referenced == set(benchmark_ids), "not every benchmark is used"

    counts = {prefix: 0 for prefix in ("COMP", "SYN", "DATA")}
    for task_id in anchor_ids:
        counts[task_id.split("-")[1]] += 1
    assert counts == {"COMP": 4, "SYN": 4, "DATA": 4}

    print(json.dumps({
        "status": "valid",
        "benchmarks": len(registry),
        "tasks": len(anchor_ids),
        "system_task_counts": counts,
    }, indent=2))


if __name__ == "__main__":
    main()
