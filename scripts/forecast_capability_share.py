import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path


GATES = ("completion", "executability", "result_validity", "evidence_integrity", "autonomy")
TASK_SYSTEM = {"COMP": "computational", "SYN": "synthesis", "DATA": "secondary_data"}


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


def quantile(values, probability):
    ordered = sorted(values)
    if not ordered:
        return None
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def project_probability(probability, months, doubling_months):
    if probability <= 0:
        return 0.0
    if probability >= 1:
        return 1.0
    odds = probability / (1 - probability)
    future_odds = odds * 2 ** (months / doubling_months)
    return future_odds / (1 + future_odds)


def pass_value(row):
    return all(row.get("gates", {}).get(gate) is True for gate in GATES)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("results_jsonl")
    parser.add_argument("--weights", default="data/taxonomy_weights_v0.1.json")
    parser.add_argument("--scenarios", default="forecast/scenario_assumptions_v0.1.json")
    parser.add_argument("--output", default="forecast/capability_share_forecast.json")
    parser.add_argument("--draws", type=int, default=50000)
    parser.add_argument("--seed", type=int, default=20260831)
    args = parser.parse_args()

    rows = load_jsonl(args.results_jsonl)
    if not rows:
        raise SystemExit("No benchmark results")
    weights = load_json(args.weights)
    assumptions = load_json(args.scenarios)

    grouped = defaultdict(list)
    for row in rows:
        required = ("month", "model", "harness", "task_id", "gates")
        if any(field not in row for field in required):
            raise SystemExit(f"Incomplete result row: {row.get('run_id', 'unknown')}")
        key = (
            row["month"], row["model"]["provider"], row["model"]["model_id"],
            row["model"]["reasoning_setting"], row["harness"]["commit"],
        )
        grouped[key].append(row)

    rng = random.Random(args.seed)
    releases = []
    for key, group in sorted(grouped.items()):
        month, provider, model_id, reasoning, harness_commit = key
        counts = {name: {"passes": 0, "tasks": 0} for name in TASK_SYSTEM.values()}
        for row in group:
            parts = row["task_id"].split("-")
            if len(parts) < 3 or parts[1] not in TASK_SYSTEM:
                raise SystemExit(f"Unrecognised task_id: {row['task_id']}")
            system = TASK_SYSTEM[parts[1]]
            counts[system]["tasks"] += 1
            counts[system]["passes"] += int(pass_value(row))

        total_tasks = sum(item["tasks"] for item in counts.values())
        total_passes = sum(item["passes"] for item in counts.values())
        if any(item["tasks"] == 0 for item in counts.values()):
            raise SystemExit(f"{key}: every production system requires at least one task")

        draws_by_system = {}
        for system, count in counts.items():
            alpha = count["passes"] + 0.5
            beta = count["tasks"] - count["passes"] + 0.5
            draws_by_system[system] = [rng.betavariate(alpha, beta) for _ in range(args.draws)]

        share_draws = []
        for index in range(args.draws):
            share_draws.append(sum(
                weights["systems"][system]["share_of_population"] * draws_by_system[system][index]
                for system in counts
            ))

        system_output = {}
        for system, count in counts.items():
            values = draws_by_system[system]
            system_output[system] = {
                **count,
                "raw_pass_rate": count["passes"] / count["tasks"],
                "posterior_mean_pass_probability": sum(values) / len(values),
                "posterior_interval_90": [quantile(values, 0.05), quantile(values, 0.95)],
                "taxonomy_weight_share_of_population": weights["systems"][system]["share_of_population"],
            }

        scenario_output = {}
        for scenario, specification in assumptions["scenarios"].items():
            doubling = specification["business_task_pass_odds_doubling_months"]
            horizons = {}
            for months in assumptions["forecast_horizons_months"]:
                projected = []
                for index in range(args.draws):
                    projected.append(sum(
                        weights["systems"][system]["share_of_population"]
                        * project_probability(draws_by_system[system][index], months, doubling)
                        for system in counts
                    ))
                horizons[str(months)] = {
                    "median_share_of_corpus": quantile(projected, 0.5),
                    "posterior_interval_90_conditional_on_scenario": [
                        quantile(projected, 0.05), quantile(projected, 0.95)
                    ],
                }
            scenario_output[scenario] = {
                "odds_doubling_months": doubling,
                "rationale": specification["rationale"],
                "horizons": horizons,
            }

        releases.append({
            "month": month,
            "model": {"provider": provider, "model_id": model_id, "reasoning_setting": reasoning},
            "harness_commit": harness_commit,
            "headline": {
                "metric": "raw_autonomous_task_pass_rate",
                "passes": total_passes,
                "initiated_tasks": total_tasks,
                "pass_rate": total_passes / total_tasks,
            },
            "production_systems": system_output,
            "frozen_2026_capability_share": {
                "median_share_of_corpus": quantile(share_draws, 0.5),
                "posterior_interval_90_sampling_only": [quantile(share_draws, 0.05), quantile(share_draws, 0.95)],
                "opportunity_envelope_ceiling": weights["core_opportunity_share"],
                "status": "benchmark_calibrated_model_implied_quantity",
            },
            "conditional_forecasts": scenario_output,
        })

    output = {
        "forecast_version": assumptions["version"],
        "taxonomy_weight_version": weights["version"],
        "seed": args.seed,
        "draws": args.draws,
        "claim_warning": "Scenario forecasts are conditional model-implied quantities, not population prevalence estimates or adoption forecasts.",
        "releases": releases,
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
