#!/usr/bin/env python3
"""Apply Yuichi's explicit Approval Sprint 002 decision to MASTER."""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "data" / "verified" / "approval_sprint_002"
MASTER = ROOT / "data" / "master"
PACKET_COMMIT = "4c29a0a"
APPROVAL_ID = "APP-AS002-20260921-01"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def merge(path: Path, incoming: list[dict[str, str]], headers: list[str], key: str) -> list[dict[str, str]]:
    existing = read(path)
    merged = {row[key]: row for row in existing}
    for row in incoming:
        identifier = row[key]
        if identifier in merged and merged[identifier] != row:
            raise SystemExit(f"MASTER conflict: {key}={identifier}")
        merged[identifier] = row
    rows = [merged[identifier] for identifier in sorted(merged)]
    write(path, headers, rows)
    return rows


def deduplicate(rows: list[dict[str, str]], key: str) -> list[dict[str, str]]:
    unique: dict[str, dict[str, str]] = {}
    for row in rows:
        identifier = row[key]
        if identifier in unique and unique[identifier] != row:
            raise SystemExit(f"Approval packet conflict: {key}={identifier}")
        unique[identifier] = row
    return list(unique.values())


def verify_approval() -> None:
    tracked = [
        "README.md", "approval_request.md", "review_summary.md", "person_review.csv",
        "career_review.csv", "organization_review.csv", "evidence_review.csv",
        "source_review.csv", "hold_review.csv", "validation_report.md",
    ]
    result = subprocess.run(
        ["git", "diff", "--quiet", PACKET_COMMIT, "--", *[str((PACKET / name).relative_to(ROOT)) for name in tracked]],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("Approval Sprint 002 differs from the approved review packet")
    approval = (PACKET / "master_approval.md").read_text(encoding="utf-8")
    required = [APPROVAL_ID, PACKET_COMMIT, "Approval Sprint 002を承認します", "承認者：Yuichi"]
    if any(value not in approval for value in required):
        raise SystemExit("Approval Sprint 002 approval record is incomplete")


def main() -> None:
    verify_approval()
    people = deduplicate([
        {"person_id": row["person_id"], "name": row["name"]}
        for row in read(PACKET / "person_review.csv")
    ], "person_id")
    careers = deduplicate([
        {field: row[field] for field in ["career_id", "person_id", "organization_id", "role", "start", "end"]}
        for row in read(PACKET / "career_review.csv")
    ], "career_id")
    organizations = deduplicate([
        {"organization_id": row["organization_id"], "name": row["name"]}
        for row in read(PACKET / "organization_review.csv")
    ], "organization_id")
    sources = deduplicate([
        {field: row[field] for field in ["source_id", "title", "publisher", "url", "accessed_at"]}
        for row in read(PACKET / "source_review.csv")
    ], "source_id")
    evidence = deduplicate([
        {field: row[field] for field in [
            "record_id", "entity_type", "entity_id", "field_name", "candidate_value",
            "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note",
        ]}
        for row in read(PACKET / "evidence_review.csv")
    ], "record_id")

    master_people = merge(MASTER / "person.csv", people, ["person_id", "name"], "person_id")
    master_organizations = merge(MASTER / "organization.csv", organizations, ["organization_id", "name"], "organization_id")
    master_careers = merge(MASTER / "career.csv", careers, ["career_id", "person_id", "organization_id", "role", "start", "end"], "career_id")
    master_sources = merge(MASTER / "source.csv", sources, ["source_id", "title", "publisher", "url", "accessed_at"], "source_id")
    master_evidence = merge(
        MASTER / "evidence.csv", evidence,
        ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"],
        "record_id",
    )
    master_approvals = merge(
        MASTER / "approval_records.csv",
        [{
            "approval_id": APPROVAL_ID,
            "batch": "Approval Sprint 002",
            "verified_commit": PACKET_COMMIT,
            "approved_scope": "8 persons, 32 careers, 183 supported evidence",
            "excluded_scope": "27 HOLD issues",
            "approved_by": "Yuichi",
            "approved_at": "2026-09-21",
            "approval_reference": "data/verified/approval_sprint_002/master_approval.md",
        }],
        ["approval_id", "batch", "verified_commit", "approved_scope", "excluded_scope", "approved_by", "approved_at", "approval_reference"],
        "approval_id",
    )

    report = f"""# MASTER反映レポート

作成日：2026-09-21

## 反映済み承認

- `APP-B005-20260921-01`：Batch 005 Wave 1
- `APP-AS001-20260921-01`：Approval Sprint 001
- `{APPROVAL_ID}`：Approval Sprint 002

## MASTER件数

- Person：{len(master_people)}件
- Organization：{len(master_organizations)}件
- Career：{len(master_careers)}件
- Source：{len(master_sources)}件
- Evidence：{len(master_evidence)}件
- Approval：{len(master_approvals)}件

Approval Sprint 002の27件のHOLD IssueはMasterに含めていない。公開サイト反映は別工程で行う。
"""
    (MASTER / "master_build_report.md").write_text(report, encoding="utf-8")
    print(
        f"MASTER updated: {len(master_people)} persons, {len(master_careers)} careers, "
        f"{len(master_evidence)} evidence, {len(master_approvals)} approvals"
    )


if __name__ == "__main__":
    main()
