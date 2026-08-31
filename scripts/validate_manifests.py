import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANCHOR_PATH = ROOT / "tasks" / "anchors_v0.1.jsonl"
COUNTERFACTUAL_PATH = ROOT / "tasks" / "counterfactuals_v0.1.jsonl"
SOURCE_PATH = ROOT / "sources" / "counterfactual_source_registry_v0.1.jsonl"

EXPECTED_PREFIX_COUNTS = {"BMA-COMP": 4, "BMA-SYN": 4, "BMA-DATA": 4}


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


def assert_unique(rows, field, label):
    values = [row[field] for row in rows]
    assert len(values) == len(set(values)), f"duplicate {field} in {label}"


def validate_counts(rows, label):
    assert len(rows) == 12, f"{label} must contain 12 tasks, found {len(rows)}"
    for prefix, expected in EXPECTED_PREFIX_COUNTS.items():
        actual = sum(row["task_id"].startswith(prefix) for row in rows)
        assert actual == expected, f"{label}: expected {expected} {prefix} tasks, found {actual}"


def main():
    anchors = load_jsonl(ANCHOR_PATH)
    variants = load_jsonl(COUNTERFACTUAL_PATH)
    sources = load_jsonl(SOURCE_PATH)

    validate_counts(anchors, "anchors")
    validate_counts(variants, "counterfactuals")
    assert_unique(anchors, "task_id", "anchors")
    assert_unique(variants, "task_id", "counterfactuals")

    anchor_ids = {row["task_id"] for row in anchors}
    paired = []
    for row in variants:
        required = {
            "benchmark_version", "variant_version", "task_id", "paired_anchor",
            "set", "workflow", "topic", "method", "brief", "permitted_inputs",
            "validator_family", "changed_dimensions", "minimum_outputs",
        }
        missing = required - row.keys()
        assert not missing, f"{row.get('task_id')}: missing {sorted(missing)}"
        assert row["benchmark_version"] == "BMA-ARB-v0.1"
        assert row["variant_version"] == "CF-v0.1"
        assert row["set"] == "counterfactual"
        assert row["task_id"].endswith("-CF1")
        assert row["paired_anchor"] in anchor_ids
        assert row["task_id"] == row["paired_anchor"] + "-CF1"
        assert len(row["changed_dimensions"]) >= 2
        assert len(row["minimum_outputs"]) >= 4
        paired.append(row["paired_anchor"])

        anchor = next(item for item in anchors if item["task_id"] == row["paired_anchor"])
        assert row["workflow"] == anchor["workflow"]
        assert row["validator_family"] == anchor["validator_family"]

    assert set(paired) == anchor_ids, "every anchor must have exactly one counterfactual"
    assert len(paired) == len(set(paired)), "an anchor is paired more than once"

    source_task_ids = {row["task_id"] for row in sources}
    variant_ids = {row["task_id"] for row in variants}
    assert variant_ids <= source_task_ids, "every variant needs at least one source-registry row"

    print(json.dumps({
        "status": "valid",
        "anchors": len(anchors),
        "counterfactuals": len(variants),
        "paired_tasks": len(paired),
        "source_registry_rows": len(sources),
    }, indent=2))


if __name__ == "__main__":
    main()
