#!/usr/bin/env python3
"""Build the Human Approval packet for the remaining pro-priority VERIFIED people."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "verified" / "approval_sprint_002"

BATCHES = {
    "Batch 003": {
        "path": ROOT / "data" / "verified" / "batch_003",
        "commit": "0fd6dc53d71a34fc65766e6056023f912653b746",
        "person_ids": ["P000014"],
    },
    "Batch 004": {
        "path": ROOT / "data" / "verified" / "batch_004",
        "commit": "f12fb3694e14a9203b5ac4e875175904c3b9a7c6",
        "person_ids": [
            "P000014", "P000065", "P000067", "P000068", "P000069",
            "P000070", "P000071", "P000072",
        ],
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
        organizations = {row["organization_id"]: row for row in read(base / "organization_verified.csv")}
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
            related_career_ids = {row["career_id"] for row in related_careers}
            related_evidence = [
                row for row in evidence
                if row["entity_id"] == person_id or row["entity_id"] in related_career_ids
            ]
            related_issues = [row for row in issues if row["person_id"] == person_id and row["status"] == "HOLD"]
            existing_person = next(
                (row for row in person_rows if row["person_id"] == person_id), None
            )
            if existing_person:
                existing_person["verified_batch"] += f"|{batch_name}"
                existing_person["verified_commit"] += f"|{config['commit']}"
                existing_person["career_count"] = str(
                    int(existing_person["career_count"]) + len(related_careers)
                )
                existing_person["evidence_count"] = str(
                    int(existing_person["evidence_count"]) + len(related_evidence)
                )
                existing_person["hold_issue_count"] = str(
                    int(existing_person["hold_issue_count"]) + len(related_issues)
                )
            else:
                person_rows.append({
                    "person_id": person_id,
                    "name": person["name"],
                    "verified_batch": batch_name,
                    "verified_commit": config["commit"],
                    "career_count": str(len(related_careers)),
                    "evidence_count": str(len(related_evidence)),
                    "hold_issue_count": str(len(related_issues)),
                    "priority_reason": "福岡第一を起点とするプロ・ドラフト・大学Career",
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

        organization_rows.extend(
            {"verified_batch": batch_name, **organizations[organization_id]}
            for organization_id in sorted(organization_ids)
        )
        evidence_rows.extend({"verified_batch": batch_name, **row} for row in evidence)
        source_rows.extend({"verified_batch": batch_name, **row} for row in sources)
        hold_rows.extend({
            "verified_batch": batch_name,
            "issue_id": row["issue_id"],
            "person_id": row["person_id"],
            "name": people[row["person_id"]]["name"],
            "related_id": row["related_id"],
            "issue_type": row["issue_type"],
            "description": row["description"],
            "disposition": row["disposition"],
        } for row in issues if row["status"] == "HOLD")

        held_keys = {
            (row["entity_type"], row["entity_id"], field)
            for row in held for field in row["held_fields"].split("|")
        }
        for row in evidence:
            key = (row["entity_type"], row["entity_id"], row["field_name"])
            if key in held_keys:
                raise SystemExit(f"Held field leaked into approval scope: {key}")

    write("person_review.csv", ["person_id", "name", "verified_batch", "verified_commit", "career_count", "evidence_count", "hold_issue_count", "priority_reason"], person_rows)
    write("career_review.csv", ["verified_batch", "person_id", "name", "career_id", "organization_id", "role", "start", "end", "organization_name", "evidence_count", "source_ids"], career_rows)
    write("organization_review.csv", ["verified_batch", "organization_id", "name"], organization_rows)
    write("evidence_review.csv", ["verified_batch", "record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence_rows)
    write("source_review.csv", ["verified_batch", "source_id", "title", "publisher", "url", "accessed_at"], source_rows)
    write("hold_review.csv", ["verified_batch", "issue_id", "person_id", "name", "related_id", "issue_type", "description", "disposition"], hold_rows)

    errors: list[str] = []
    expected_ids = {person_id for config in BATCHES.values() for person_id in config["person_ids"]}
    if {row["person_id"] for row in person_rows} != expected_ids:
        errors.append("対象Person IDが指定範囲と一致しない")
    if expected_ids & {row["person_id"] for row in read(ROOT / "data" / "master" / "person.csv")}:
        errors.append("既存Master Personが混入")
    source_keys = {(row["verified_batch"], row["source_id"]) for row in source_rows}
    for row in evidence_rows:
        if row["assessment"] != "SUPPORTED":
            errors.append(f"{row['record_id']}: SUPPORTEDではない")
        if (row["verified_batch"], row["source_id"]) not in source_keys:
            errors.append(f"{row['record_id']}: Source参照が不足")

    validation = [
        "# Approval Sprint 002 検証レポート", "", "作成日：2026-09-21", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件", f"- Person：{len(person_rows)}件",
        f"- Career：{len(career_rows)}件", f"- Evidence：{len(evidence_rows)}件",
        f"- Source：{len(source_rows)}件", f"- HOLD Issue：{len(hold_rows)}件",
        "", "## エラー", "",
    ]
    validation.extend(f"- {error}" for error in errors)
    if not errors:
        validation.append("- なし")
    (OUTPUT / "validation_report.md").write_text("\n".join(validation) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit("Approval Sprint 002 validation failed")

    names = "、".join(row["name"] for row in person_rows)
    readme = f"""# Approval Sprint 002

作成日：2026-09-21

状態：HUMAN APPROVAL待ち。MASTER未反映。

## 対象

既にVERIFIEDで、まだMasterに含まれていないプロ・B.LEAGUE優先8名を対象とする。

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

`evidence_review.csv`のSUPPORTED Evidenceと、対応するPerson・Career・Organizationだけが承認候補。`hold_review.csv`は対象外で、不明値は補わない。

この資料の作成はHuman Approvalではない。Yuichiが対象版と範囲を明示して承認した後に限り、Masterへ反映できる。
"""
    (OUTPUT / "README.md").write_text(readme, encoding="utf-8")

    review_lines = [
        "# Approval Sprint 002 レビュー要約", "", "作成日：2026-09-21", "",
        "## 対象者", "",
        "| 人物 | Career | 根拠 | HOLD | 確認済み組織 |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for person in person_rows:
        related = [row for row in career_rows if row["person_id"] == person["person_id"]]
        organizations = " → ".join(dict.fromkeys(row["organization_name"] for row in related))
        review_lines.append(
            f"| {person['name']} | {person['career_count']} | {person['evidence_count']} | "
            f"{person['hold_issue_count']} | {organizations} |"
        )
    review_lines.extend([
        "", "## 判断方法", "",
        f"- 承認候補：8人・{len(career_rows)} Career・{len(evidence_rows)}件のSUPPORTED Evidence",
        f"- 承認対象外：{len(hold_rows)}件のHOLD Issue",
        "- HOLDは不明な期間、未確認値、契約・登録・出場の区別などであり、承認してもMasterへ入らない",
        "- ドラフト候補はプロ契約済みとは扱わない",
        "", "## 詳細ファイル", "",
        "- `person_review.csv`：対象人物と件数",
        "- `career_review.csv`：承認候補の所属・活動歴",
        "- `evidence_review.csv`：項目別の根拠",
        "- `source_review.csv`：出典URL",
        "- `hold_review.csv`：承認対象外の不明点",
    ])
    (OUTPUT / "review_summary.md").write_text("\n".join(review_lines) + "\n", encoding="utf-8")

    approval_request = f"""# Human Approval確認文

この確認文は、Yuichiが資料を確認した後に使用する。事前入力やAIによる代筆は行わない。

> 対象：Approval Sprint 002の8名（{names}）。対象版：Batch 003 `{BATCHES['Batch 003']['commit']}`、Batch 004 `{BATCHES['Batch 004']['commit']}`。範囲：`evidence_review.csv`のSUPPORTED Evidenceに対応するPerson・Career・Organization。判断：対象範囲をMasterへ反映してよい。`hold_review.csv`の全件は承認対象外。
"""
    (OUTPUT / "approval_request.md").write_text(approval_request, encoding="utf-8")

    print(
        f"Approval Sprint 002: {len(person_rows)} persons, {len(career_rows)} careers, "
        f"{len(evidence_rows)} evidence, {len(hold_rows)} HOLD issues"
    )


if __name__ == "__main__":
    main()
