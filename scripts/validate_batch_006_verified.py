#!/usr/bin/env python3
"""Validate Batch 006 VERIFIED candidates without treating them as MASTER."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "verified" / "batch_006"
SCOPE = ROOT / "data" / "candidate" / "batch_006" / "wave_01" / "qa_decisions.csv"


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
    ready = [row for row in decisions if row["decision"] == "READY_FOR_VERIFIED_REVIEW"]

    expected = {
        "persons": (len(persons), 4),
        "organizations": (len(organizations), 8),
        "careers": (len(careers), 9),
        "sources": (len(sources), 9),
        "evidence": (len(evidence), 51),
        "held": (len(held), 10),
        "issues": (len(issues), 10),
        "ready decisions": (len(ready), 21),
    }
    for label, (actual, wanted) in expected.items():
        if actual != wanted:
            errors.append(f"{label}: expected {wanted}, got {actual}")

    eligible: dict[tuple[str, str], set[str]] = {}
    for row in ready:
        target = (row["entity_type"], row["entity_id"])
        eligible.setdefault(target, set()).update(filter(None, row["eligible_fields"].split("|")))

    person_ids = {row["person_id"] for row in persons}
    organization_ids = {row["organization_id"] for row in organizations}
    source_ids = {row["source_id"] for row in sources}
    career_ids = {row["career_id"] for row in careers}
    master_person_ids = {row["person_id"] for row in read(ROOT / "data" / "master" / "person.csv")}
    if person_ids & master_person_ids:
        errors.append("Masterに存在するPersonが新規VERIFIEDへ混入")

    for row in careers:
        if row["person_id"] not in person_ids:
            errors.append(f"{row['career_id']}: unknown person")
        if row["organization_id"] not in organization_ids:
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
        if row["entity_type"] == "Career" and row["entity_id"] not in career_ids:
            errors.append(f"{row['record_id']}: evidence refers to excluded career")

    if any(row["status"] != "HOLD" for row in issues):
        errors.append("issue disposition contains a non-HOLD status")
    if any(not row["held_fields"] for row in held):
        errors.append("held_fields contains a blank field list")

    report = [
        "# Batch 006 VERIFIED検証レポート", "", "作成日：2026-09-21", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件", f"- Person：{len(persons)}件",
        f"- Career：{len(careers)}件", f"- Organization：{len(organizations)}件",
        f"- Source：{len(sources)}件", f"- Evidence：{len(evidence)}件",
        f"- HOLD記録：{len(held)}件", f"- HOLD Issue：{len(issues)}件",
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
