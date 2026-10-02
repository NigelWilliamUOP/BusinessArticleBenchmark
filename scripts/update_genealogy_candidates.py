#!/usr/bin/env python3
"""Discover recent AI-scientist benchmark papers through arXiv without auto-promoting them."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENEALOGY = ROOT / "genealogy"
CONFIG_FILE = GENEALOGY / "candidate_search_config_v0.1.json"
NODE_FILE = GENEALOGY / "benchmark_nodes_v0.1.jsonl"
CANDIDATE_FILE = GENEALOGY / "candidates" / "latest.jsonl"

ATOM = {"atom": "http://www.w3.org/2005/Atom"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def arxiv_query(term: str, max_results: int) -> list[dict[str, Any]]:
    cleaned = term.replace('"', '').strip()
    query = f'all:"{cleaned}"'
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    request = urllib.request.Request(
        f"https://export.arxiv.org/api/query?{params}",
        headers={"User-Agent": "BMA-ARB-living-genealogy/0.1 (https://github.com/NigelWilliamUOP/BusinessArticleBenchmark)"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        payload = response.read()
    root = ET.fromstring(payload)
    records: list[dict[str, Any]] = []
    for entry in root.findall("atom:entry", ATOM):
        source_url = (entry.findtext("atom:id", default="", namespaces=ATOM) or "").replace("http://", "https://")
        title = " ".join((entry.findtext("atom:title", default="", namespaces=ATOM) or "").split())
        summary = " ".join((entry.findtext("atom:summary", default="", namespaces=ATOM) or "").split())
        published = entry.findtext("atom:published", default="", namespaces=ATOM) or ""
        updated = entry.findtext("atom:updated", default="", namespaces=ATOM) or ""
        authors = [
            " ".join((author.findtext("atom:name", default="", namespaces=ATOM) or "").split())
            for author in entry.findall("atom:author", ATOM)
        ]
        categories = [category.attrib.get("term", "") for category in entry.findall("atom:category", ATOM)]
        if source_url and title:
            records.append(
                {
                    "title": title,
                    "source_url": source_url,
                    "published": published[:10],
                    "updated": updated[:10],
                    "authors": [author for author in authors if author],
                    "categories": [category for category in categories if category],
                    "summary": summary[:1000],
                }
            )
    return records


def main() -> int:
    config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    curated = load_jsonl(NODE_FILE)
    existing = load_jsonl(CANDIDATE_FILE)

    curated_urls = {row["source_url"].rstrip("/") for row in curated}
    curated_titles = {normalize_title(row["name"]) for row in curated}
    existing_by_url = {row["source_url"].rstrip("/"): row for row in existing}
    existing_titles = {normalize_title(row["title"]) for row in existing}

    cutoff = date.today() - timedelta(days=int(config["lookback_days"]))
    discovered: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for index, term in enumerate(config["queries"]):
        try:
            results = arxiv_query(term, int(config["max_results_per_query"]))
        except Exception as exc:  # network failure should be visible but not corrupt the queue
            errors.append(f"{term}: {exc}")
            continue
        for row in results:
            try:
                published_date = datetime.strptime(row["published"], "%Y-%m-%d").date()
            except ValueError:
                continue
            if published_date < cutoff:
                continue
            key = row["source_url"].rstrip("/")
            if key in curated_urls or normalize_title(row["title"]) in curated_titles:
                continue
            record = discovered.setdefault(key, row)
            record.setdefault("search_terms", [])
            if term not in record["search_terms"]:
                record["search_terms"].append(term)
        if index < len(config["queries"]) - 1:
            time.sleep(3)

    today = datetime.now(timezone.utc).date().isoformat()
    additions: list[dict[str, Any]] = []
    for key, row in sorted(discovered.items(), key=lambda item: (item[1]["published"], item[1]["title"])):
        if key in existing_by_url or normalize_title(row["title"]) in existing_titles:
            continue
        row["candidate_id"] = "arxiv_" + hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]
        row["first_seen"] = today
        row["review_status"] = "unreviewed"
        additions.append(row)

    if errors:
        print("warning: one or more arXiv queries failed", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
    if not additions:
        print("no new genealogy candidates")
        return 0

    merged = existing + additions
    merged.sort(key=lambda row: (row["published"], row["title"], row["candidate_id"]))
    CANDIDATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATE_FILE.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in merged),
        encoding="utf-8",
    )
    print(f"added {len(additions)} new genealogy candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
