#!/usr/bin/env python3
"""Build a focused Human Approval packet for eight published VERIFIED candidates."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "verified" / "approval_sprint_001"

BATCHES = {
    "Batch 003": {
        "path": ROOT / "data" / "verified" / "batch_003",
        "commit": "0fd6dc53d71a34fc65766e6056023f912653b746",
        "person_ids": ["P000010", "P000029", "P000030", "P000031", "P000032", "P000033", "P000034"],
    },
    "Batch 004": {
        "path": ROOT / "data" / "verified" / "batch_004",
        "commit": "f12fb3694e14a9203b5ac4e875175904c3b9a7c6",
        "person_ids": ["P000064"],
    },
}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(name: str, headers: list[str], rows: list[dict[str, str]]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    person_rows: list[dict[str, str]] = []
    career_rows: list[dict[str, str]] = []
    organization_rows: list[dict[str, str]] = []
    evidence_rows: list[dict[str, str]] = []
    source_rows: list[dict[str, str]] = []
    hold_rows: list[dict[str, str]] = []

    for batch_name, config in BATCHES.items():
        base = config["path"]
        target_ids = set(config["person_ids"])
        people = {row["person_id"]: row for row in read(base / "person_verified.csv")}
        careers = [row for row in read(base / "career_verified.csv") if row["person_id"] in target_ids]
        career_ids = {row["career_id"] for row in careers}
        organization_ids = {row["organization_id"] for row in careers}
        organizations = {
            row["organization_id"]: row for row in read(base / "organization_verified.csv")
        }
        evidence = [
            row for row in read(base / "evidence_records.csv")
            if (row["entity_type"] == "Person" and row["entity_id"] in target_ids)
            or (row["entity_type"] == "Career" and row["entity_id"] in career_ids)
            or (row["entity_type"] == "Organization" and row["entity_id"] in organization_ids)
        ]
        source_ids = {row["source_id"] for row in evidence}
        sources = [row for row in read(base / "source_references.csv") if row["source_id"] in source_ids]
        issues = [row for row in read(base / "issue_dispositions.csv") if row["person_id"] in target_ids]
        held = [
            row for row in read(base / "held_fields.csv")
            if row["entity_id"] in target_ids or row["entity_id"] in career_ids
        ]

        for person_id in config["person_ids"]:
            person = people[person_id]
            related_careers = [row for row in careers if row["person_id"] == person_id]
            related_evidence = [
                row for row in evidence
                if row["entity_id"] == person_id
                or row["entity_id"] in {career["career_id"] for career in related_careers}
            ]
            related_issues = [row for row in issues if row["person_id"] == person_id and row["status"] == "HOLD"]
            person_rows.append({
                "person_id": person_id,
                "name": person["name"],
                "verified_batch": batch_name,
                "verified_commit": config["commit"],
                "career_count": str(len(related_careers)),
                "evidence_count": str(len(related_evidence)),
                "hold_issue_count": str(len(related_issues)),
                "public_status": "候補データ・正式承認前",
            })

        for career in careers:
            career_evidence = [row for row in evidence if row["entity_id"] == career["career_id"]]
            career_rows.append({
                "verified_batch": batch_name,
                "person_id": career["person_id"],
                "name": people[career["person_id"]]["name"],
                **career,
                "organization_name": organizations[career["organization_id"]]["name"],
                "evidence_count": str(len(career_evidence)),
                "source_ids": "|".join(dict.fromkeys(row["source_id"] for row in career_evidence)),
            })

        for organization_id in sorted(organization_ids):
            organization_rows.append({
                "verified_batch": batch_name,
                **organizations[organization_id],
            })

        for row in evidence:
            evidence_rows.append({"verified_batch": batch_name, **row})
        for row in sources:
            source_rows.append({"verified_batch": batch_name, **row})
        for row in issues:
            if row["status"] == "HOLD":
                hold_rows.append({
                    "verified_batch": batch_name,
                    "issue_id": row["issue_id"],
                    "person_id": row["person_id"],
                    "name": people[row["person_id"]]["name"],
                    "related_id": row["related_id"],
                    "issue_type": row["issue_type"],
                    "description": row["description"],
                    "disposition": row["disposition"],
                })

        # Every held-field row must have stayed out of the focused evidence scope.
        held_keys = {(row["entity_type"], row["entity_id"], field)
                     for row in held for field in row["held_fields"].split("|")}
        for row in evidence:
            key = (row["entity_type"], row["entity_id"], row["field_name"])
            if key in held_keys:
                raise SystemExit(f"Held field leaked into approval scope: {key}")

    write(
        "person_review.csv",
        ["person_id", "name", "verified_batch", "verified_commit", "career_count", "evidence_count", "hold_issue_count", "public_status"],
        person_rows,
    )
    write(
        "career_review.csv",
        ["verified_batch", "person_id", "name", "career_id", "organization_id", "role", "start", "end", "organization_name", "evidence_count", "source_ids"],
        career_rows,
    )
    write(
        "organization_review.csv",
        ["verified_batch", "organization_id", "name"],
        organization_rows,
    )
    write(
        "evidence_review.csv",
        ["verified_batch", "record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"],
        evidence_rows,
    )
    write(
        "source_review.csv",
        ["verified_batch", "source_id", "title", "publisher", "url", "accessed_at"],
        source_rows,
    )
    write(
        "hold_review.csv",
        ["verified_batch", "issue_id", "person_id", "name", "related_id", "issue_type", "description", "disposition"],
        hold_rows,
    )

    errors: list[str] = []
    expected_person_ids = {
        person_id
        for config in BATCHES.values()
        for person_id in config["person_ids"]
    }
    actual_person_ids = {row["person_id"] for row in person_rows}
    if actual_person_ids != expected_person_ids:
        errors.append("対象Person IDが指定範囲と一致しない")
    review_source_keys = {(row["verified_batch"], row["source_id"]) for row in source_rows}
    for row in evidence_rows:
        if row["assessment"] != "SUPPORTED":
            errors.append(f"{row['record_id']}: SUPPORTEDではない")
        if (row["verified_batch"], row["source_id"]) not in review_source_keys:
            errors.append(f"{row['record_id']}: Source参照が不足")
    if any(row["person_id"] not in expected_person_ids for row in career_rows):
        errors.append("対象外PersonのCareerが混入")

    validation = [
        "# Approval Sprint 001 検証レポート", "", "作成日：2026-09-21", "",
        "## 結果", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件",
        f"- Person：{len(person_rows)}件",
        f"- Career：{len(career_rows)}件",
        f"- Evidence：{len(evidence_rows)}件",
        f"- Source：{len(source_rows)}件",
        f"- HOLD Issue：{len(hold_rows)}件", "", "## エラー", "",
    ]
    validation.extend(f"- {error}" for error in errors)
    if not errors:
        validation.append("- なし")
    (OUTPUT / "validation_report.md").write_text("\n".join(validation) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit("Approval Sprint 001 validation failed")

    names = "、".join(row["name"] for row in person_rows)
    readme = f"""# Approval Sprint 001

作成日：2026-09-21

状態：HUMAN APPROVAL待ち。MASTER未反映。

## 対象

公開サイトで候補表示中、かつ既にVERIFIEDとなっている8名を対象とする。

{names}

## 対象版

- Batch 003：`{BATCHES['Batch 003']['commit']}`
- Batch 004：`{BATCHES['Batch 004']['commit']}`

## 件数

- Person：{len(person_rows)}件
- Career：{len(career_rows)}件
- Organization参照：{len(organization_rows)}件
- Evidence：{len(evidence_rows)}件
- Source：{len(source_rows)}件
- HOLD Issue：{len(hold_rows)}件

## 判断範囲

`evidence_review.csv`に含まれるSUPPORTED Evidenceと、それに対応するPerson・Career・Organizationだけを承認候補とする。`hold_review.csv`の全項目は対象外とし、不明値を補わない。

この資料の作成はHuman Approvalではない。Yuichiが対象版と範囲を明示して承認した後に限り、MASTERへ反映できる。
"""
    (OUTPUT / "README.md").write_text(readme, encoding="utf-8")

    approval_request = f"""# Human Approval確認文

この確認文は、Yuichiが資料を確認した後に使用する。事前入力やAIによる代筆は行わない。

> 対象：Approval Sprint 001の8名（{names}）。対象版：Batch 003 `{BATCHES['Batch 003']['commit']}`、Batch 004 `{BATCHES['Batch 004']['commit']}`。範囲：`evidence_review.csv`のSUPPORTED Evidenceに対応するPerson・Career・Organization。判断：対象範囲をMasterへ反映してよい。`hold_review.csv`の19件は承認対象外。
"""
    (OUTPUT / "approval_request.md").write_text(approval_request, encoding="utf-8")

    print(
        f"Approval Sprint 001: {len(person_rows)} persons, {len(career_rows)} careers, "
        f"{len(evidence_rows)} evidence, {len(hold_rows)} HOLD issues"
    )


if __name__ == "__main__":
    main()
