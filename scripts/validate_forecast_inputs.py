import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = ROOT / "data" / "taxonomy_weights_v0.1.json"
MARKET = ROOT / "data" / "market_intelligence_2026-08.jsonl"
SCENARIOS = ROOT / "forecast" / "scenario_assumptions_v0.1.json"


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
    weights = load_json(WEIGHTS)
    market = load_jsonl(MARKET)
    scenarios = load_json(SCENARIOS)

    expected_systems = {"computational", "synthesis", "secondary_data"}
    assert set(weights["systems"]) == expected_systems
    population_sum = sum(item["share_of_population"] for item in weights["systems"].values())
    envelope_sum = sum(item["share_of_core_opportunity"] for item in weights["systems"].values())
    assert abs(population_sum - weights["core_opportunity_share"]) < 1e-12
    assert abs(envelope_sum - 1.0) < 1e-12
    assert weights["status"] == "weighted_measurement_audit"

    required_market = {
        "as_of", "indicator_id", "indicator", "value", "unit", "evidence_scope",
        "source_url", "source_type", "forecast_use", "qualification",
    }
    ids = []
    for row in market:
        missing = required_market - row.keys()
        assert not missing, f"market row missing {sorted(missing)}"
        assert row["source_url"].startswith("https://")
        ids.append(row["indicator_id"])
    assert len(ids) == len(set(ids)), "duplicate market indicator_id"

    expected_scenarios = {"conservative", "central", "accelerated"}
    assert set(scenarios["scenarios"]) == expected_scenarios
    doubling = {
        name: item["business_task_pass_odds_doubling_months"]
        for name, item in scenarios["scenarios"].items()
    }
    assert doubling["conservative"] > doubling["central"] > doubling["accelerated"] > 0
    assert scenarios["forecast_horizons_months"] == sorted(set(scenarios["forecast_horizons_months"]))

    print(json.dumps({
        "status": "valid",
        "core_opportunity_share": weights["core_opportunity_share"],
        "production_systems": len(expected_systems),
        "market_indicators": len(market),
        "scenarios": doubling,
    }, indent=2))


if __name__ == "__main__":
    main()
