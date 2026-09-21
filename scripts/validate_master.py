#!/usr/bin/env python3
"""Validate MASTER references and the recorded Batch 005 approval."""

from __future__ import annotations

import csv
from pathlib import Path


BASE = Path("data/master")


def read(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    errors: list[str] = []
    persons = read("person.csv")
    organizations = read("organization.csv")
    careers = read("career.csv")
    sources = read("source.csv")
    evidence = read("evidence.csv")
    approvals = read("approval_records.csv")
    publications = read("publication_records.csv")

    expected = {
        "Person": (len(persons), 4),
        "Organization": (len(organizations), 11),
        "Career": (len(careers), 11),
        "Source": (len(sources), 15),
        "Evidence": (len(evidence), 84),
        "Approval": (len(approvals), 1),
        "Publication": (len(publications), 1),
    }
    for label, (actual, count) in expected.items():
        if actual != count:
            errors.append(f"{label}: expected {count}, got {actual}")

    person_ids = {row["person_id"] for row in persons}
    organization_ids = {row["organization_id"] for row in organizations}
    career_ids = {row["career_id"] for row in careers}
    source_ids = {row["source_id"] for row in sources}
    for row in careers:
        if row["person_id"] not in person_ids:
            errors.append(f"{row['career_id']}: unknown person")
        if not row["organization_id"] or row["organization_id"] not in organization_ids:
            errors.append(f"{row['career_id']}: missing or unknown organization")

    entity_ids = {
        "Person": person_ids,
        "Organization": organization_ids,
        "Career": career_ids,
    }
    for row in evidence:
        if row["assessment"] != "SUPPORTED":
            errors.append(f"{row['record_id']}: assessment is not SUPPORTED")
        if row["source_id"] not in source_ids:
            errors.append(f"{row['record_id']}: unknown source")
        if row["entity_id"] not in entity_ids.get(row["entity_type"], set()):
            errors.append(f"{row['record_id']}: unknown entity")

    if len(approvals) == 1:
        approval = approvals[0]
        required = {
            "approval_id": "APP-B005-20260921-01",
            "verified_commit": "7093141",
            "approved_by": "Yuichi",
            "approved_at": "2026-09-21",
        }
        for field, value in required.items():
            if approval[field] != value:
                errors.append(f"approval {field}: expected {value}, got {approval[field]}")

    if len(publications) == 1:
        publication = publications[0]
        required = {
            "publication_id": "PUB-B005-20260921-01",
            "approval_id": "APP-B005-20260921-01",
            "published_at": "2026-09-21",
            "site_url": "https://japanbasketballarchive.com/",
            "status": "LIVE",
        }
        for field, value in required.items():
            if publication[field] != value:
                errors.append(f"publication {field}: expected {value}, got {publication[field]}")

    report = [
        "# MASTER検証レポート", "", "作成日：2026-09-21", "",
        "## 結果", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件",
        f"- Person：{len(persons)}件",
        f"- Organization：{len(organizations)}件",
        f"- Career：{len(careers)}件",
        f"- Source：{len(sources)}件",
        f"- Evidence：{len(evidence)}件",
        f"- Approval：{len(approvals)}件",
        f"- Publication：{len(publications)}件", "", "## エラー", "",
    ]
    report.extend(f"- {error}" for error in errors)
    if not errors:
        report.append("- なし")
    (BASE / "validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
