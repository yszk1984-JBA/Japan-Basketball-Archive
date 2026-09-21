#!/usr/bin/env python3
"""Build the Human Approval packet for Batch 002 VERIFIED candidates."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "verified" / "batch_002"
OUTPUT = ROOT / "data" / "verified" / "approval_sprint_003"
VERIFIED_COMMIT = "9c43baefe106bd91ae7244978821f8e6e427c700"


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
    people = read(SOURCE / "person_verified.csv")
    careers = read(SOURCE / "career_verified.csv")
    organizations = read(SOURCE / "organization_verified.csv")
    evidence = read(SOURCE / "evidence_records.csv")
    sources = read(SOURCE / "source_references.csv")
    issues = read(SOURCE / "issue_dispositions.csv")
    held = read(SOURCE / "held_fields.csv")

    person_by_id = {row["person_id"]: row for row in people}
    organization_by_id = {row["organization_id"]: row for row in organizations}
    master_person_ids = {row["person_id"] for row in read(ROOT / "data" / "master" / "person.csv")}

    person_review: list[dict[str, str]] = []
    career_review: list[dict[str, str]] = []
    hold_review: list[dict[str, str]] = []

    for person in people:
        person_id = person["person_id"]
        related_careers = [row for row in careers if row["person_id"] == person_id]
        related_ids = {row["career_id"] for row in related_careers}
        related_evidence = [
            row for row in evidence
            if row["entity_id"] == person_id or row["entity_id"] in related_ids
        ]
        related_holds = [
            row for row in issues
            if row["person_id"] == person_id and row["status"] == "HOLD"
        ]
        person_review.append({
            "person_id": person_id,
            "name": person["name"],
            "verified_batch": "Batch 002",
            "verified_commit": VERIFIED_COMMIT,
            "career_count": str(len(related_careers)),
            "evidence_count": str(len(related_evidence)),
            "hold_issue_count": str(len(related_holds)),
            "priority_reason": "福岡第一を起点とするB.LEAGUE・プロ優先Career",
        })

    for career in careers:
        career_evidence = [row for row in evidence if row["entity_id"] == career["career_id"]]
        career_review.append({
            "verified_batch": "Batch 002",
            "person_id": career["person_id"],
            "name": person_by_id[career["person_id"]]["name"],
            **career,
            "organization_name": organization_by_id[career["organization_id"]]["name"],
            "evidence_count": str(len(career_evidence)),
            "source_ids": "|".join(dict.fromkeys(row["source_id"] for row in career_evidence)),
        })

    for row in issues:
        if row["status"] != "HOLD":
            continue
        hold_review.append({
            "verified_batch": "Batch 002",
            "issue_id": row["issue_id"],
            "person_id": row["person_id"],
            "name": person_by_id[row["person_id"]]["name"],
            "related_id": row["related_id"],
            "issue_type": row["issue_type"],
            "description": row["description"],
            "disposition": row["disposition"],
        })

    organization_review = [{"verified_batch": "Batch 002", **row} for row in organizations]
    evidence_review = [{"verified_batch": "Batch 002", **row} for row in evidence]
    source_review = [{"verified_batch": "Batch 002", **row} for row in sources]

    write("person_review.csv", ["person_id", "name", "verified_batch", "verified_commit", "career_count", "evidence_count", "hold_issue_count", "priority_reason"], person_review)
    write("career_review.csv", ["verified_batch", "person_id", "name", "career_id", "organization_id", "role", "start", "end", "organization_name", "evidence_count", "source_ids"], career_review)
    write("organization_review.csv", ["verified_batch", "organization_id", "name"], organization_review)
    write("evidence_review.csv", ["verified_batch", "record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence_review)
    write("source_review.csv", ["verified_batch", "source_id", "title", "publisher", "url", "accessed_at"], source_review)
    write("hold_review.csv", ["verified_batch", "issue_id", "person_id", "name", "related_id", "issue_type", "description", "disposition"], hold_review)

    errors: list[str] = []
    if len(people) != 10 or len(careers) != 30 or len(evidence) != 146:
        errors.append("Batch 002 VERIFIEDの基準件数と一致しない")
    if len(sources) != 38 or len(organizations) != 19 or len(hold_review) != 19:
        errors.append("Source・Organization・HOLDの基準件数と一致しない")
    if {row["person_id"] for row in people} & master_person_ids:
        errors.append("既存Master Personが混入")
    source_ids = {row["source_id"] for row in sources}
    held_keys = {
        (row["entity_type"], row["entity_id"], field)
        for row in held for field in row["held_fields"].split("|")
    }
    for row in evidence:
        if row["assessment"] != "SUPPORTED":
            errors.append(f"{row['record_id']}: SUPPORTEDではない")
        if row["source_id"] not in source_ids:
            errors.append(f"{row['record_id']}: Source参照が不足")
        if (row["entity_type"], row["entity_id"], row["field_name"]) in held_keys:
            errors.append(f"{row['record_id']}: HOLD項目が承認候補へ混入")

    validation = [
        "# Approval Sprint 003 検証レポート", "", "作成日：2026-09-21", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件", f"- Person：{len(person_review)}件",
        f"- Career：{len(career_review)}件", f"- Evidence：{len(evidence_review)}件",
        f"- Source：{len(source_review)}件", f"- HOLD Issue：{len(hold_review)}件",
        "", "## エラー", "",
    ]
    validation.extend(f"- {error}" for error in errors)
    if not errors:
        validation.append("- なし")
    (OUTPUT / "validation_report.md").write_text("\n".join(validation) + "\n", encoding="utf-8")
    if errors:
        raise SystemExit("Approval Sprint 003 validation failed")

    names = "、".join(row["name"] for row in person_review)
    readme = f"""# Approval Sprint 003

作成日：2026-09-21

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

Batch 002でVERIFIED候補となり、まだMasterに含まれていない10名を対象とする。

{names}

## 対象版

- Batch 002 VERIFIED：`{VERIFIED_COMMIT}`

## 件数

- Person：{len(person_review)}件
- Career：{len(career_review)}件
- Organization参照：{len(organization_review)}件
- Evidence：{len(evidence_review)}件
- Source：{len(source_review)}件
- HOLD Issue：{len(hold_review)}件

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceと、対応するPerson・Career・Organizationだけが承認候補。`hold_review.csv`は対象外で、不明値は補わない。

この資料の作成はHuman Approvalではない。Yuichiが対象版と範囲を明示して承認した後に限り、Masterへ反映できる。
"""
    (OUTPUT / "README.md").write_text(readme, encoding="utf-8")

    summary = [
        "# Approval Sprint 003 レビュー要約", "", "作成日：2026-09-21", "",
        "## 対象者", "", "| 人物 | Career | 根拠 | HOLD | 確認済み組織 |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for person in person_review:
        related = [row for row in career_review if row["person_id"] == person["person_id"]]
        org_names = " → ".join(dict.fromkeys(row["organization_name"] for row in related))
        summary.append(
            f"| {person['name']} | {person['career_count']} | {person['evidence_count']} | "
            f"{person['hold_issue_count']} | {org_names} |"
        )
    summary.extend([
        "", "## 判断方法", "",
        f"- 承認候補：10人・{len(career_review)} Career・{len(evidence_review)}件のSUPPORTED Evidence",
        f"- 承認対象外：{len(hold_review)}件のHOLD Issue",
        "- HOLDは未確認の期間・役割等であり、承認してもMasterへ入らない",
        "- 契約、リーグ登録、公式戦出場は資料が裏付ける範囲だけを採用する",
        "", "## 詳細ファイル", "",
        "- `person_review.csv`：対象人物と件数",
        "- `career_review.csv`：承認候補の所属・活動歴",
        "- `evidence_review.csv`：項目別の根拠",
        "- `source_review.csv`：出典URL",
        "- `hold_review.csv`：承認対象外の不明点",
    ])
    (OUTPUT / "review_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    request = f"""# Human Approval確認文

この確認文は、Yuichiが資料を確認した後に使用する。事前入力やAIによる代筆は行わない。

> 対象：Approval Sprint 003の10名（{names}）。対象版：Batch 002 VERIFIED `{VERIFIED_COMMIT}`。範囲：`evidence_review.csv`のSUPPORTED Evidenceに対応するPerson・Career・Organization。判断：対象範囲をMasterへ反映してよい。`hold_review.csv`の全19件は承認対象外。
"""
    (OUTPUT / "approval_request.md").write_text(request, encoding="utf-8")

    print(
        f"Approval Sprint 003: {len(person_review)} persons, {len(career_review)} careers, "
        f"{len(evidence_review)} evidence, {len(hold_review)} HOLD issues"
    )


if __name__ == "__main__":
    main()
