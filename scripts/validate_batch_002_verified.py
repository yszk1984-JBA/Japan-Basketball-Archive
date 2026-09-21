#!/usr/bin/env python3
"""Validate Batch 002 VERIFIED output without treating it as MASTER."""

from __future__ import annotations

import csv
from pathlib import Path


BASE = Path("data/verified/batch_002")
SCOPE = Path("data/candidate/batch_002/qa_decisions.csv")


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

    expected = {
        "Person": (len(persons), 10), "Career": (len(careers), 30),
        "Organization": (len(organizations), 19), "Source": (len(sources), 38),
        "Evidence": (len(evidence), 146), "Held": (len(held), 28),
        "Issue": (len(issues), 30), "Decision": (len(decisions), 40),
    }
    for label, (actual, count) in expected.items():
        if actual != count:
            errors.append(f"{label}: expected {count}, got {actual}")

    eligible = {
        (row["entity_type"], row["entity_id"]): set(filter(None, row["eligible_fields"].split("|")))
        for row in decisions
    }
    person_ids = {row["person_id"] for row in persons}
    organization_ids = {row["organization_id"] for row in organizations}
    career_ids = {row["career_id"] for row in careers}
    source_ids = {row["source_id"] for row in sources}
    for row in careers:
        if row["person_id"] not in person_ids:
            errors.append(f"{row['career_id']}: unknown person")
        if not row["organization_id"] or row["organization_id"] not in organization_ids:
            errors.append(f"{row['career_id']}: missing or unknown organization")
        allowed = eligible.get(("Career", row["career_id"]), set())
        for field in ["organization_id", "role", "start", "end"]:
            if row[field] and field not in allowed:
                errors.append(f"{row['career_id']}: held {field} was populated")

    entity_ids = {"Person": person_ids, "Career": career_ids}
    for row in evidence:
        if row["assessment"] != "SUPPORTED":
            errors.append(f"{row['record_id']}: non-supported evidence")
        if row["source_id"] not in source_ids:
            errors.append(f"{row['record_id']}: unknown source")
        if row["entity_id"] not in entity_ids.get(row["entity_type"], set()):
            errors.append(f"{row['record_id']}: unknown entity")
        if row["field_name"] not in eligible.get((row["entity_type"], row["entity_id"]), set()):
            errors.append(f"{row['record_id']}: field outside eligible scope")

    if sum(row["status"] == "HOLD" for row in issues) != 19:
        errors.append("HOLD Issue count is not 19")

    report = [
        "# Batch 002 VERIFIED検証レポート", "", "作成日：2026-09-21", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件", f"- Person：{len(persons)}件",
        f"- Career：{len(careers)}件", f"- Evidence：{len(evidence)}件",
        f"- HOLD Issue：{sum(row['status'] == 'HOLD' for row in issues)}件",
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
