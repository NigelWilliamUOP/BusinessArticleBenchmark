#!/usr/bin/env python3
"""Validate the curated living benchmark genealogy using only the standard library."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENEALOGY = ROOT / "genealogy"

NODE_FILE = GENEALOGY / "benchmark_nodes_v0.1.jsonl"
EDGE_FILE = GENEALOGY / "benchmark_edges_v0.1.jsonl"
COLLAB_FILE = GENEALOGY / "collaboration_targets_v0.1.jsonl"
PORTFOLIO_FILE = GENEALOGY / "portsmouth_portfolio_profile_v0.1.json"
CANDIDATE_FILE = GENEALOGY / "candidates" / "latest.jsonl"

REQUIRED_NODE_FIELDS = {
    "id",
    "name",
    "year",
    "first_release",
    "kind",
    "status",
    "domains",
    "research_stages",
    "evaluation_unit",
    "human_guidance",
    "verifier_types",
    "reports_compute",
    "reports_human_time",
    "reports_monetary_cost",
    "journal_quality_floor",
    "open_artifacts",
    "source_url",
    "latest_checked",
    "evidence_note",
    "portsmouth_relevance",
    "collaboration_priority",
    "claim_boundary",
}

ALLOWED_KINDS = {"benchmark", "system", "framework", "project", "review", "local_program", "method"}
ALLOWED_STATUS = {"active", "preprint", "published", "local_design"}
ALLOWED_GUIDANCE = {
    "autonomous",
    "human_in_loop",
    "human_on_loop",
    "mixed",
    "progressively_withdrawn",
    "protocol_specified",
    "not_applicable",
    "not_reported",
}
ALLOWED_PRIORITY = {"high", "medium", "watch", "none"}
ALLOWED_RELATIONS = {
    "extends",
    "evaluates_on",
    "evaluates",
    "operationalises",
    "uses_verifier",
    "adapts",
    "complements",
    "closest_precedent",
    "planned_collaboration",
    "informs",
    "shares_task_lineage",
}
ALLOWED_CONFIDENCE = {"high", "medium", "provisional"}
DATE_PATTERN = re.compile(r"^\d{4}(?:-\d{2})?(?:-\d{2})?$")
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")

FORBIDDEN_PORTFOLIO_KEYS = {
    "titles",
    "output_titles",
    "paper_titles",
    "authors",
    "author_names",
    "staff",
    "staff_names",
    "staff_ids",
    "emails",
    "pure_ids",
    "reviewer_grades",
    "selected_for_return",
    "provisional_selection",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        raise ValueError(f"Missing required file: {path.relative_to(ROOT)}")
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path.relative_to(ROOT)}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path.relative_to(ROOT)}:{line_number}: expected a JSON object")
        rows.append(value)
    return rows


def require_https(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.startswith("https://"):
        raise ValueError(f"{label}: expected an https URL")


def validate_string_list(value: Any, label: str) -> None:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{label}: expected a non-empty list of strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{label}: duplicate values are not allowed")


def walk_forbidden_keys(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_PORTFOLIO_KEYS:
                raise ValueError(f"{path}.{key}: row-level or personal data key is forbidden")
            walk_forbidden_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_forbidden_keys(child, f"{path}[{index}]")


def validate_nodes(nodes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    if not nodes:
        raise ValueError("The curated node registry is empty")
    by_id: dict[str, dict[str, Any]] = {}
    for index, node in enumerate(nodes, 1):
        missing = REQUIRED_NODE_FIELDS - node.keys()
        if missing:
            raise ValueError(f"node {index}: missing fields {sorted(missing)}")
        node_id = node["id"]
        if not isinstance(node_id, str) or not ID_PATTERN.fullmatch(node_id):
            raise ValueError(f"node {index}: invalid id {node_id!r}")
        if node_id in by_id:
            raise ValueError(f"duplicate node id: {node_id}")
        by_id[node_id] = node
        if not isinstance(node["name"], str) or not node["name"].strip():
            raise ValueError(f"{node_id}: name is required")
        if not isinstance(node["year"], int) or not 2020 <= node["year"] <= 2100:
            raise ValueError(f"{node_id}: invalid year")
        for field in ("first_release", "latest_checked"):
            if not isinstance(node[field], str) or not DATE_PATTERN.fullmatch(node[field]):
                raise ValueError(f"{node_id}.{field}: expected YYYY, YYYY-MM or YYYY-MM-DD")
        if node["kind"] not in ALLOWED_KINDS:
            raise ValueError(f"{node_id}: unknown kind {node['kind']!r}")
        if node["status"] not in ALLOWED_STATUS:
            raise ValueError(f"{node_id}: unknown status {node['status']!r}")
        if node["human_guidance"] not in ALLOWED_GUIDANCE:
            raise ValueError(f"{node_id}: unknown human_guidance {node['human_guidance']!r}")
        if node["collaboration_priority"] not in ALLOWED_PRIORITY:
            raise ValueError(f"{node_id}: unknown collaboration_priority")
        validate_string_list(node["domains"], f"{node_id}.domains")
        validate_string_list(node["research_stages"], f"{node_id}.research_stages")
        validate_string_list(node["verifier_types"], f"{node_id}.verifier_types")
        if not isinstance(node["evaluation_unit"], str) or not node["evaluation_unit"].strip():
            raise ValueError(f"{node_id}: evaluation_unit is required")
        for field in (
            "reports_compute",
            "reports_human_time",
            "reports_monetary_cost",
            "journal_quality_floor",
            "open_artifacts",
        ):
            if not isinstance(node[field], bool):
                raise ValueError(f"{node_id}.{field}: expected boolean")
        if not isinstance(node["portsmouth_relevance"], int) or not 1 <= node["portsmouth_relevance"] <= 5:
            raise ValueError(f"{node_id}: portsmouth_relevance must be 1..5")
        for field in ("evidence_note", "claim_boundary"):
            if not isinstance(node[field], str) or len(node[field].strip()) < 20:
                raise ValueError(f"{node_id}.{field}: provide a substantive bounded statement")
        require_https(node["source_url"], f"{node_id}.source_url")
        if "code_url" in node:
            require_https(node["code_url"], f"{node_id}.code_url")
    return by_id


def validate_edges(edges: list[dict[str, Any]], node_ids: set[str]) -> None:
    seen: set[tuple[str, str, str]] = set()
    for index, edge in enumerate(edges, 1):
        required = {"from", "to", "relation", "confidence", "source_url", "note"}
        missing = required - edge.keys()
        if missing:
            raise ValueError(f"edge {index}: missing fields {sorted(missing)}")
        if edge["from"] not in node_ids or edge["to"] not in node_ids:
            raise ValueError(f"edge {index}: endpoint not found ({edge['from']} -> {edge['to']})")
        if edge["from"] == edge["to"]:
            raise ValueError(f"edge {index}: self-edges are not allowed")
        if edge["relation"] not in ALLOWED_RELATIONS:
            raise ValueError(f"edge {index}: unknown relation {edge['relation']!r}")
        if edge["confidence"] not in ALLOWED_CONFIDENCE:
            raise ValueError(f"edge {index}: unknown confidence {edge['confidence']!r}")
        require_https(edge["source_url"], f"edge {index}.source_url")
        if not isinstance(edge["note"], str) or len(edge["note"].strip()) < 15:
            raise ValueError(f"edge {index}: note is too short")
        key = (edge["from"], edge["to"], edge["relation"])
        if key in seen:
            raise ValueError(f"duplicate edge: {key}")
        seen.add(key)


def validate_collaborations(rows: list[dict[str, Any]], node_ids: set[str]) -> None:
    priorities: set[int] = set()
    targets: set[str] = set()
    for index, row in enumerate(rows, 1):
        required = {
            "target_id",
            "organisation",
            "priority",
            "proposal",
            "mutual_value",
            "first_contact_goal",
            "source_url",
        }
        missing = required - row.keys()
        if missing:
            raise ValueError(f"collaboration {index}: missing fields {sorted(missing)}")
        if row["target_id"] not in node_ids:
            raise ValueError(f"collaboration {index}: unknown target_id {row['target_id']!r}")
        if row["target_id"] in targets:
            raise ValueError(f"duplicate collaboration target: {row['target_id']}")
        targets.add(row["target_id"])
        if not isinstance(row["priority"], int) or row["priority"] < 1:
            raise ValueError(f"collaboration {index}: priority must be a positive integer")
        if row["priority"] in priorities:
            raise ValueError(f"duplicate collaboration priority: {row['priority']}")
        priorities.add(row["priority"])
        require_https(row["source_url"], f"collaboration {index}.source_url")
        for field in ("organisation", "proposal", "mutual_value", "first_contact_goal"):
            if not isinstance(row[field], str) or len(row[field].strip()) < 10:
                raise ValueError(f"collaboration {index}.{field}: substantive text required")


def validate_portfolio(path: Path) -> dict[str, Any]:
    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid portfolio profile: {exc}") from exc
    if not isinstance(profile, dict):
        raise ValueError("portfolio profile must be an object")
    walk_forbidden_keys(profile)
    text = json.dumps(profile, ensure_ascii=False)
    if EMAIL_PATTERN.search(text):
        raise ValueError("portfolio profile contains an email address")
    required = {
        "profile_id",
        "as_of",
        "institution",
        "unit",
        "privacy",
        "candidate_output_count",
        "title_signal_counts",
        "journal_portfolio_status",
        "benchmark_weighting_policy",
    }
    missing = required - profile.keys()
    if missing:
        raise ValueError(f"portfolio profile missing fields {sorted(missing)}")
    if not isinstance(profile["candidate_output_count"], int) or profile["candidate_output_count"] <= 0:
        raise ValueError("portfolio candidate_output_count must be positive")
    if profile["journal_portfolio_status"] not in {"not_yet_enriched", "enriched"}:
        raise ValueError("unknown journal_portfolio_status")
    signal_names: set[str] = set()
    for row in profile["title_signal_counts"]:
        if not isinstance(row, dict) or not {"signal", "count", "percent_of_outputs"} <= row.keys():
            raise ValueError("invalid title_signal_counts record")
        if row["signal"] in signal_names:
            raise ValueError(f"duplicate portfolio signal: {row['signal']}")
        signal_names.add(row["signal"])
        if not isinstance(row["count"], int) or not 0 <= row["count"] <= profile["candidate_output_count"]:
            raise ValueError(f"invalid count for portfolio signal {row['signal']}")
        if not isinstance(row["percent_of_outputs"], (int, float)) or not 0 <= row["percent_of_outputs"] <= 100:
            raise ValueError(f"invalid percentage for portfolio signal {row['signal']}")
    return profile


def validate_candidates(rows: list[dict[str, Any]]) -> None:
    seen: set[str] = set()
    for index, row in enumerate(rows, 1):
        required = {
            "candidate_id",
            "title",
            "source_url",
            "published",
            "first_seen",
            "search_terms",
            "review_status",
        }
        missing = required - row.keys()
        if missing:
            raise ValueError(f"candidate {index}: missing fields {sorted(missing)}")
        if row["candidate_id"] in seen:
            raise ValueError(f"duplicate candidate_id: {row['candidate_id']}")
        seen.add(row["candidate_id"])
        require_https(row["source_url"], f"candidate {index}.source_url")
        if row["review_status"] not in {"unreviewed", "promoted", "rejected", "duplicate"}:
            raise ValueError(f"candidate {index}: unknown review_status")
        validate_string_list(row["search_terms"], f"candidate {index}.search_terms")


def main() -> int:
    try:
        nodes = load_jsonl(NODE_FILE)
        edges = load_jsonl(EDGE_FILE)
        collaborations = load_jsonl(COLLAB_FILE)
        candidates = load_jsonl(CANDIDATE_FILE)
        by_id = validate_nodes(nodes)
        validate_edges(edges, set(by_id))
        validate_collaborations(collaborations, set(by_id))
        profile = validate_portfolio(PORTFOLIO_FILE)
        validate_candidates(candidates)
    except ValueError as exc:
        print(f"genealogy validation failed: {exc}", file=sys.stderr)
        return 1

    kind_counts = Counter(node["kind"] for node in nodes)
    print(
        "genealogy validation passed: "
        f"{len(nodes)} nodes, {len(edges)} edges, {len(collaborations)} collaboration targets, "
        f"{len(candidates)} candidate records, {profile['candidate_output_count']} aggregate Portsmouth outputs"
    )
    print("node kinds:", ", ".join(f"{key}={value}" for key, value in sorted(kind_counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
