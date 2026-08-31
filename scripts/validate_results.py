import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from statistics import median


REQUIRED_GATES = ("completion", "executability", "result_validity", "evidence_integrity", "autonomy")
QUALITY_FIELDS = (
    "research_design",
    "source_data_integrity",
    "analytical_correctness",
    "robustness_verification",
    "theoretical_contribution",
    "manuscript_references",
)


def load_jsonl(path):
    rows = []
    for line_no, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON on line {line_no}: {exc}") from exc
    return rows


def validate(row):
    errors = []
    for field in ("benchmark_version", "month", "run_id", "task_id", "task_set", "model", "harness", "run_status", "gates", "quality", "resources"):
        if field not in row:
            errors.append(f"missing {field}")
    if errors:
        return errors
    if row["benchmark_version"] != "BMA-ARB-v0.1":
        errors.append("unexpected benchmark_version")
    if not re.fullmatch(r"BMA-(COMP|SYN|DATA)-[0-9]{2}(-CF[0-9]+)?", row["task_id"]):
        errors.append("invalid task_id")
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}", row["month"]):
        errors.append("month must be YYYY-MM")
    if row["task_set"] not in ("anchor", "counterfactual"):
        errors.append("task_set must be anchor or counterfactual")
    is_counterfactual = "-CF" in row["task_id"]
    if is_counterfactual != (row["task_set"] == "counterfactual"):
        errors.append("task_set does not match task_id")
    if is_counterfactual and not row.get("paired_anchor"):
        errors.append("counterfactual result missing paired_anchor")
    if is_counterfactual and row.get("paired_anchor") != row["task_id"].rsplit("-CF", 1)[0]:
        errors.append("paired_anchor does not match counterfactual task_id")
    for gate in REQUIRED_GATES:
        if not isinstance(row["gates"].get(gate), bool):
            errors.append(f"gate {gate} is not boolean")
    for field in QUALITY_FIELDS:
        value = row["quality"].get(field)
        if not isinstance(value, int) or not 0 <= value <= 4:
            errors.append(f"quality {field} must be integer 0..4")
    evidence = row.get("evidence_metrics")
    if row["gates"].get("evidence_integrity"):
        if not evidence:
            errors.append("evidence_integrity pass requires evidence_metrics")
        else:
            checked = evidence.get("claims_checked", 0)
            supported = evidence.get("claims_supported", 0)
            if checked <= 0 or supported / checked < 0.95:
                errors.append("evidence_integrity pass requires claim-support precision >= 0.95")
            if evidence.get("fabricated_references", 0) != 0:
                errors.append("evidence_integrity pass requires zero fabricated references")
            if evidence.get("materially_misrepresented_references", 0) != 0:
                errors.append("evidence_integrity pass requires zero materially misrepresented references")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results_jsonl")
    parser.add_argument("--output", default="bma_benchmark_summary.json")
    args = parser.parse_args()
    rows = load_jsonl(args.results_jsonl)
    if not rows:
        raise SystemExit("No result rows")

    seen = set()
    groups = defaultdict(list)
    all_errors = []
    for index, row in enumerate(rows, 1):
        errors = validate(row)
        if errors:
            all_errors.append({"row": index, "errors": errors})
            continue
        key = (row["month"], row["run_id"], row["task_id"], row["model"]["provider"], row["model"]["model_id"], row["harness"]["commit"])
        if key in seen:
            all_errors.append({"row": index, "errors": ["duplicate run key"]})
            continue
        seen.add(key)
        groups[(row["month"], row["model"]["provider"], row["model"]["model_id"], row["harness"]["commit"])].append(row)

    if all_errors:
        raise SystemExit(json.dumps({"validation_errors": all_errors}, indent=2))

    summaries = []
    for key, group in sorted(groups.items()):
        month, provider, model_id, commit = key
        passes = [all(row["gates"][gate] for gate in REQUIRED_GATES) for row in group]
        quality_values = [sum(row["quality"][field] for field in QUALITY_FIELDS) / (4 * len(QUALITY_FIELDS)) * 100 for row in group]
        cost = sum(row["resources"]["cost_gbp"] for row in group)
        workflow = {"COMP": "computational", "SYN": "synthesis", "DATA": "secondary_data"}
        workflow_counts = defaultdict(lambda: {"tasks": 0, "passes": 0})
        set_counts = defaultdict(lambda: {"tasks": 0, "passes": 0})
        for row, passed in zip(group, passes):
            label = workflow[row["task_id"].split("-")[1]]
            workflow_counts[label]["tasks"] += 1
            workflow_counts[label]["passes"] += int(passed)
            set_counts[row["task_set"]]["tasks"] += 1
            set_counts[row["task_set"]]["passes"] += int(passed)
        evidence = [row.get("evidence_metrics", {}) for row in group]
        claims_checked = sum(item.get("claims_checked", 0) for item in evidence)
        claims_supported = sum(item.get("claims_supported", 0) for item in evidence)
        task_outcomes = {
            row["task_id"]: all(row["gates"][gate] for gate in REQUIRED_GATES)
            for row in group
        }
        paired_outcomes = defaultdict(int)
        for row in group:
            if row["task_set"] != "counterfactual":
                continue
            anchor_id = row["paired_anchor"]
            if anchor_id not in task_outcomes:
                continue
            label = ("pass" if task_outcomes[anchor_id] else "fail") + "/" + ("pass" if task_outcomes[row["task_id"]] else "fail")
            paired_outcomes[label] += 1
        anchor_passes = set_counts["anchor"]["passes"]
        paired_passes = paired_outcomes.get("pass/pass", 0)
        summaries.append({
            "month": month,
            "provider": provider,
            "model_id": model_id,
            "harness_commit": commit,
            "tasks": len(group),
            "passes": sum(passes),
            "pass_rate": sum(passes) / len(group),
            "median_quality_percent": median(quality_values),
            "workflow_pass_rates": {
                label: {
                    **counts,
                    "pass_rate": counts["passes"] / counts["tasks"],
                }
                for label, counts in sorted(workflow_counts.items())
            },
            "task_set_pass_rates": {
                label: {
                    **counts,
                    "pass_rate": counts["passes"] / counts["tasks"],
                }
                for label, counts in sorted(set_counts.items())
            },
            "paired_outcomes": dict(sorted(paired_outcomes.items())),
            "counterfactual_transfer_rate": (paired_passes / anchor_passes) if anchor_passes else None,
            "claim_support_precision": (claims_supported / claims_checked) if claims_checked else None,
            "fabricated_references": sum(item.get("fabricated_references", 0) for item in evidence),
            "clean_execution_rate": sum(row["gates"]["executability"] for row in group) / len(group),
            "median_cost_gbp": median(row["resources"]["cost_gbp"] for row in group),
            "median_wall_seconds": median(row["resources"]["wall_seconds"] for row in group),
            "median_tool_calls": median(row["resources"]["tool_calls"] for row in group),
            "total_cost_gbp": cost,
            "passes_per_100_gbp": (sum(passes) / cost * 100) if cost else None,
        })

    output = {"benchmark_version": "BMA-ARB-v0.1", "groups": summaries}
    Path(args.output).write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
