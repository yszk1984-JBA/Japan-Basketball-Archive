#!/usr/bin/env python3
"""Validate Batch 004 VERIFIED candidates without treating them as MASTER."""

from __future__ import annotations

import csv
from pathlib import Path


BASE = Path("data/verified/batch_004")
SCOPE = Path("data/candidate/batch_004/review_packet/verification_scope.csv")


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    errors: list[str] = []
    persons = read(BASE / "person_verified.csv")
    organizations = read(BASE / "organization_verified.csv")
    careers = read(BASE / "career_verified.csv")
    sources = read(BASE / "source_references.csv")
    evidence = read(BASE / "evidence_records.csv")
    held = read(BASE / "held_fields.csv")
    issues = read(BASE / "issue_dispositions.csv")
    decisions = read(SCOPE)

    expected_counts = {
        "persons": (len(persons), 10),
        "organizations": (len(organizations), 20),
        "careers": (len(careers), 38),
        "issues": (len(issues), 33),
        "decisions": (len(decisions), 75),
    }
    for label, (actual, expected) in expected_counts.items():
        if actual != expected:
            errors.append(f"{label}: expected {expected}, got {actual}")

    eligible: dict[tuple[str, str], set[str]] = {}
    for row in decisions:
        target = (row["entity_type"], row["entity_id"])
        eligible.setdefault(target, set()).update(filter(None, row["eligible_fields"].split("|")))

    person_ids = {row["person_id"] for row in persons}
    organization_ids = {row["organization_id"] for row in organizations}
    career_ids = {row["career_id"] for row in careers}
    source_ids = {row["source_id"] for row in sources}
    for row in careers:
        if row["person_id"] not in person_ids:
            errors.append(f"{row['career_id']}: unknown person")
        if row["organization_id"] and row["organization_id"] not in organization_ids:
            errors.append(f"{row['career_id']}: unknown organization")
        allowed = eligible.get(("Career", row["career_id"]), set())
        for field in ["organization_id", "role", "start", "end"]:
            if row[field] and field not in allowed:
                errors.append(f"{row['career_id']}: held {field} was populated")

    for row in evidence:
        if row["assessment"] != "SUPPORTED":
            errors.append(f"{row['record_id']}: non-supported evidence")
        if row["source_id"] not in source_ids:
            errors.append(f"{row['record_id']}: unknown source")
        if row["field_name"] not in eligible.get((row["entity_type"], row["entity_id"]), set()):
            errors.append(f"{row['record_id']}: field outside eligible scope")

    if any(row["status"] != "HOLD" for row in issues):
        errors.append("issue disposition contains a non-HOLD status")
    if any(not row["held_fields"] for row in held):
        errors.append("held_fields contains a blank held field")

    report = [
        "# Batch 004 VERIFIED検証レポート", "", "作成日：2026-09-21", "",
        "## 結果", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件",
        f"- Person：{len(persons)}件",
        f"- Career：{len(careers)}件",
        f"- Organization：{len(organizations)}件",
        f"- Source：{len(sources)}件",
        f"- Evidence：{len(evidence)}件",
        f"- HOLD fields：{len(held)}件",
        f"- HOLD Issue：{len(issues)}件",
        "- HUMAN APPROVAL・Master：未実施", "", "## エラー", "",
    ]
    report.extend(f"- {error}" for error in errors)
    if not errors:
        report.append("- なし")
    (BASE / "validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
