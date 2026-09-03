#!/usr/bin/env python3
"""Build a privacy-safe aggregate Portsmouth UOA17 output profile from an authorised XLSX."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from typing import Any

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"

PATTERNS = {
    "quantitative_or_effect": r"\b(effect|effects|impact|impacts|association|associated|relationship|relationships|determinant|determinants|antecedent|antecedents|mediator|mediation|moderator|moderation|experiment|experimental|survey|panel data|regression|structural equation|causal|causality|influence|predict|prediction|performance)\b",
    "policy_documentary_historical": r"\b(policy|policies|public sector|government|governance|regulat|histor|document|reporting|accountability|procurement|defen[cs]e|public administration|political|institutional|institutions|sustainability disclosure|corporate disclosure)\b",
    "digital_text_data": r"\b(machine learning|artificial intelligence|\bAI\b|digital|text mining|natural language|social media|big data|bibliometric|topic model|network analysis|content analysis|data[- ]driven|analytics|blockchain|platform)\b",
    "conceptual_or_theory": r"\b(conceptual|theor|framework|typology|taxonomy|proposition|perspective|reconceptual|conceptualisation|conceptualization)\b",
    "formal_or_computational": r"\b(optimisation|optimization|algorithm|mathematical|simulation|system dynamics|forecast|neural network|mixed[- ]integer|integer program|linear program|game theoretic|computational|data envelopment|agent[- ]based|stochastic|multi[- ]objective)\b",
    "evidence_synthesis": r"\b(systematic (?:literature )?review|meta[- ]analysis|scoping review|bibliometric review|critical interpretive synthesis|integrative review|literature review)\b",
    "qualitative_or_case": r"\b(qualitative|case stud|interview|ethnograph|focus group|narrative|interpretive|grounded theory)\b",
}


def column_index(reference: str) -> int:
    letters = re.match(r"([A-Z]+)", reference)
    if letters is None:
        raise ValueError(f"Invalid cell reference: {reference}")
    value = 0
    for char in letters.group(1):
        value = value * 26 + ord(char) - 64
    return value - 1


def read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    values: list[str] = []
    for item in root.findall(f"{{{MAIN_NS}}}si"):
        values.append("".join(node.text or "" for node in item.iter(f"{{{MAIN_NS}}}t")))
    return values


def worksheet_path(archive: zipfile.ZipFile, sheet_name: str) -> str:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    sheets = workbook.find(f"{{{MAIN_NS}}}sheets")
    if sheets is None:
        raise ValueError("Workbook contains no worksheets")
    relationship_id: str | None = None
    for sheet in sheets:
        if sheet.attrib.get("name") == sheet_name:
            relationship_id = sheet.attrib.get(f"{{{DOC_REL_NS}}}id")
            break
    if relationship_id is None:
        available = [sheet.attrib.get("name", "") for sheet in sheets]
        raise ValueError(f"Sheet {sheet_name!r} not found. Available sheets: {available}")
    relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    target: str | None = None
    for relationship in relationships.findall(f"{{{PKG_REL_NS}}}Relationship"):
        if relationship.attrib.get("Id") == relationship_id:
            target = relationship.attrib.get("Target")
            break
    if target is None:
        raise ValueError(f"Could not resolve worksheet relationship for {sheet_name}")
    if target.startswith("/"):
        return target.lstrip("/")
    if target.startswith("xl/"):
        return target
    return "xl/" + target


def read_rows(path: Path, sheet_name: str) -> list[list[str]]:
    with zipfile.ZipFile(path) as archive:
        shared = read_shared_strings(archive)
        root = ET.fromstring(archive.read(worksheet_path(archive, sheet_name)))
        output: list[list[str]] = []
        for row in root.iter(f"{{{MAIN_NS}}}row"):
            cells: dict[int, str] = {}
            for cell in row.findall(f"{{{MAIN_NS}}}c"):
                reference = cell.attrib.get("r", "")
                index = column_index(reference)
                value_type = cell.attrib.get("t")
                if value_type == "inlineStr":
                    text_node = cell.find(f".//{{{MAIN_NS}}}t")
                    value = text_node.text if text_node is not None else ""
                else:
                    value_node = cell.find(f"{{{MAIN_NS}}}v")
                    raw = value_node.text if value_node is not None and value_node.text is not None else ""
                    if value_type == "s" and raw:
                        value = shared[int(raw)]
                    elif value_type == "b":
                        value = "TRUE" if raw == "1" else "FALSE"
                    else:
                        value = raw
                cells[index] = value
            if cells:
                current = [""] * (max(cells) + 1)
                for index, value in cells.items():
                    current[index] = value
                output.append(current)
        return output


def find_title_column(rows: list[list[str]]) -> tuple[int, int]:
    for row_index, row in enumerate(rows):
        for column, value in enumerate(row):
            normalized = re.sub(r"[^a-z]+", " ", str(value).lower()).strip()
            if normalized in {"title", "paper title", "output title", "ouput title"}:
                return row_index, column
    raise ValueError("Could not find a Title or Paper title header")


def build_profile(titles: list[str], as_of: str) -> dict[str, Any]:
    total = len(titles)
    counts = {
        signal: sum(bool(re.search(pattern, title, re.IGNORECASE)) for title in titles)
        for signal, pattern in PATTERNS.items()
    }
    counts["no_explicit_design_signal"] = sum(
        not any(re.search(pattern, title, re.IGNORECASE) for pattern in PATTERNS.values())
        for title in titles
    )
    ordered_signals = [
        "quantitative_or_effect",
        "policy_documentary_historical",
        "digital_text_data",
        "conceptual_or_theory",
        "evidence_synthesis",
        "formal_or_computational",
        "qualitative_or_case",
        "no_explicit_design_signal",
    ]
    return {
        "profile_id": "portsmouth_business_school_uoa17_v0.1",
        "version": "0.1",
        "as_of": as_of,
        "institution": "University of Portsmouth",
        "unit": "Business and Management Studies (UOA17 proxy for the Portsmouth Business School research-output portfolio)",
        "source_type": "Internal aggregate output-audit snapshot; source rows are not published in this repository.",
        "privacy": "The public profile exports no output titles, authors, staff names, identifiers, email addresses, reviewer grades or provisional selection decisions.",
        "candidate_output_count": total,
        "classification_method": "Overlapping, case-insensitive title-keyword signals. These are provisional research-design cues, not article-level classifications.",
        "signals_overlap": True,
        "title_signal_counts": [
            {
                "signal": signal,
                "count": counts[signal],
                "percent_of_outputs": round(100 * counts[signal] / total, 1),
            }
            for signal in ordered_signals
        ],
        "journal_portfolio_status": "not_yet_enriched",
        "journal_portfolio_note": "The available audit snapshot does not contain journal title or ISSN. Journal-level weighting will be added only after an authorised metadata join against public publication records.",
        "benchmark_weighting_policy": {
            "current": "Use this profile only to check that pilot tasks cover the observed range of title-level research-design signals. Do not derive a journal-tier target from it.",
            "target": "Weight article trials and modular tasks to the observed three-year Portsmouth portfolio by journal, article type and method family after journal and ISSN enrichment.",
            "prohibitions": [
                "Do not infer CABS or journal tiers from paper titles.",
                "Do not publish row-level internal output-audit data.",
                "Do not treat overlapping title signals as mutually exclusive article classes.",
                "Do not optimise towards a generic journal distribution when the Portsmouth portfolio becomes available.",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Authorised internal XLSX path")
    parser.add_argument("--sheet", default="UOA17")
    parser.add_argument("--output", required=True)
    parser.add_argument("--as-of", default=date.today().isoformat())
    args = parser.parse_args()

    input_path = Path(args.input)
    if input_path.suffix.lower() != ".xlsx":
        print("Only .xlsx input is supported", file=sys.stderr)
        return 2
    try:
        rows = read_rows(input_path, args.sheet)
        header_row, title_column = find_title_column(rows)
        titles = [
            str(row[title_column]).strip()
            for row in rows[header_row + 1 :]
            if len(row) > title_column and str(row[title_column]).strip()
        ]
    except (OSError, zipfile.BadZipFile, ValueError, ET.ParseError) as exc:
        print(f"portfolio profile build failed: {exc}", file=sys.stderr)
        return 1
    if not titles:
        print("portfolio profile build failed: no output titles found", file=sys.stderr)
        return 1

    profile = build_profile(titles, args.as_of)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote aggregate profile for {len(titles)} outputs to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
