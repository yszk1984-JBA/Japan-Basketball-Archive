#!/usr/bin/env python3
"""Validate MASTER references and recorded human approvals."""

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
        "Person": (len(persons), 30),
        "Organization": (len(organizations), 41),
        "Career": (len(careers), 91),
        "Source": (len(sources), 102),
        "Evidence": (len(evidence), 573),
        "Approval": (len(approvals), 4),
        "Publication": (len(publications), 4),
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

    approvals_by_id = {row["approval_id"]: row for row in approvals}
    required_approvals = {
        "APP-B005-20260921-01": {
            "approval_id": "APP-B005-20260921-01",
            "verified_commit": "7093141",
            "approved_by": "Yuichi",
            "approved_at": "2026-09-21",
        },
        "APP-AS001-20260921-01": {
            "approval_id": "APP-AS001-20260921-01",
            "verified_commit": "2ac462c",
            "approved_scope": "8 persons, 18 careers, 167 supported evidence",
            "excluded_scope": "19 HOLD issues",
            "approved_by": "Yuichi",
            "approved_at": "2026-09-21",
        },
        "APP-AS002-20260921-01": {
            "approval_id": "APP-AS002-20260921-01",
            "verified_commit": "4c29a0a",
            "approved_scope": "8 persons, 32 careers, 183 supported evidence",
            "excluded_scope": "27 HOLD issues",
            "approved_by": "Yuichi",
            "approved_at": "2026-09-21",
        },
        "APP-AS003-20260921-01": {
            "approval_id": "APP-AS003-20260921-01",
            "verified_commit": "a25eed93913e7bc40d43fd5cc672304a48a840cd",
            "approved_scope": "10 persons, 30 careers, 146 supported evidence",
            "excluded_scope": "19 HOLD issues",
            "approved_by": "Yuichi",
            "approved_at": "2026-09-21",
        },
    }
    for approval_id, required in required_approvals.items():
        approval = approvals_by_id.get(approval_id)
        if approval is None:
            errors.append(f"approval missing: {approval_id}")
            continue
        for field, value in required.items():
            if approval[field] != value:
                errors.append(
                    f"approval {approval_id} {field}: expected {value}, got {approval[field]}"
                )

    publications_by_id = {row["publication_id"]: row for row in publications}
    required_publications = {
        "PUB-B005-20260921-01": {
            "publication_id": "PUB-B005-20260921-01",
            "approval_id": "APP-B005-20260921-01",
            "published_at": "2026-09-21",
            "site_url": "https://japanbasketballarchive.com/",
            "status": "LIVE",
        },
        "PUB-AS001-20260921-01": {
            "publication_id": "PUB-AS001-20260921-01",
            "approval_id": "APP-AS001-20260921-01",
            "published_at": "2026-09-21",
            "site_url": "https://japanbasketballarchive.com/",
            "status": "LIVE",
        },
        "PUB-AS002-20260921-01": {
            "publication_id": "PUB-AS002-20260921-01",
            "approval_id": "APP-AS002-20260921-01",
            "published_at": "2026-09-21",
            "site_url": "https://japanbasketballarchive.com/",
            "status": "LIVE",
        },
        "PUB-AS003-20260921-01": {
            "publication_id": "PUB-AS003-20260921-01",
            "approval_id": "APP-AS003-20260921-01",
            "published_at": "2026-09-21",
            "site_url": "https://japanbasketballarchive.com/",
            "status": "LIVE",
        },
    }
    for publication_id, required in required_publications.items():
        publication = publications_by_id.get(publication_id)
        if publication is None:
            errors.append(f"publication missing: {publication_id}")
            continue
        for field, value in required.items():
            if publication[field] != value:
                errors.append(
                    f"publication {publication_id} {field}: expected {value}, got {publication[field]}"
                )

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
