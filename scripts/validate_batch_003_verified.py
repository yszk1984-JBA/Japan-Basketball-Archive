#!/usr/bin/env python3
"""Structural validation for Batch 003 VERIFIED output."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path("data/verified/batch_003")


def rows(filename: str) -> list[dict[str, str]]:
    with (ROOT / filename).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    errors = []
    persons = rows("person_verified.csv")
    organizations = rows("organization_verified.csv")
    careers = rows("career_verified.csv")
    sources = rows("source_references.csv")
    evidence = rows("evidence_records.csv")
    held = rows("held_fields.csv")
    issues = rows("issue_dispositions.csv")

    person_ids = {row["person_id"] for row in persons}
    organization_ids = {row["organization_id"] for row in organizations}
    career_ids = {row["career_id"] for row in careers}
    source_ids = {row["source_id"] for row in sources}

    if len(persons) != 10:
        errors.append(f"Person count is {len(persons)}, expected 10")
    if len(careers) != 18:
        errors.append(f"Career count is {len(careers)}, expected 18")
    if len(organizations) != 9:
        errors.append(f"Organization count is {len(organizations)}, expected 9")
    if len(held) != 18:
        errors.append(f"Held decision count is {len(held)}, expected 18")

    for row in careers:
        if row["person_id"] not in person_ids:
            errors.append(f"Missing Person: {row['person_id']}")
        if row["organization_id"] not in organization_ids:
            errors.append(f"Missing Organization: {row['organization_id']}")
        if row["start"] or row["end"]:
            errors.append(f"Held period leaked into {row['career_id']}")

    valid_entity_ids = {"Person": person_ids, "Career": career_ids}
    for row in evidence:
        if row["assessment"] != "SUPPORTED":
            errors.append(f"Non-supported Evidence: {row['record_id']}")
        if row["source_id"] not in source_ids:
            errors.append(f"Missing Source: {row['source_id']}")
        if row["entity_id"] not in valid_entity_ids.get(row["entity_type"], set()):
            errors.append(f"Missing entity: {row['entity_type']} {row['entity_id']}")
        if row["entity_id"] == "C000031" and row["field_name"] == "grade":
            errors.append("Held grade leaked into C000031")

    if any(row["status"] == "HOLD" and not row["disposition"] for row in issues):
        errors.append("HOLD issue without disposition")

    report = [
        "# Batch 003 VERIFIED構造検査",
        "",
        "この検査はVERIFIED出力の構造とHOLD除外を確認する。Master承認を意味しない。",
        "",
        "## 結果",
        "",
        f"- 構造検査：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件",
        f"- Person：{len(persons)}件",
        f"- Career：{len(careers)}件",
        f"- Evidence：{len(evidence)}件",
        f"- HOLD Issue：{sum(row['status'] == 'HOLD' for row in issues)}件",
        "- Master：未作成",
        "",
        "## エラー",
        "",
    ]
    report.extend(f"- {error}" for error in errors) if errors else report.append("- なし")
    (ROOT / "validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report[:8]))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
