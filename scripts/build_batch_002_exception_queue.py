#!/usr/bin/env python3
"""Build the deferred exception queue for Batch 002.

The queue separates unresolved fields from the confirmed candidate fields so
the same unsuccessful search is not repeated. It does not create VERIFIED or
MASTER data.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


BATCH_DIR = Path("data/candidate/batch_002")
OUTPUT_CSV = BATCH_DIR / "exception_queue.csv"
OUTPUT_MD = BATCH_DIR / "exception_queue_summary.md"

FIELD_LABELS = {
    "role": "役割",
    "start": "開始時期",
    "end": "終了時期",
}


def read_csv(filename: str) -> list[dict[str, str]]:
    with (BATCH_DIR / filename).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def split_high_school_description(description: str) -> tuple[str, str]:
    prefix = "確認済み項目は"
    separator = "。未確認項目は"
    if description.startswith(prefix) and separator in description:
        confirmed, held = description[len(prefix):].split(separator, 1)
        return confirmed, held
    return description, ""


def humanize_scope(value: str) -> str:
    return "、".join(
        FIELD_LABELS.get(field, field) for field in value.split("|") if field
    )


def classify(issue: dict[str, str]) -> tuple[str, str, str, str]:
    description = issue["description"]
    if issue["issue_type"] == "HIGH_SCHOOL_EVIDENCE":
        confirmed, held = split_high_school_description(description)
        category = (
            "HIGH_SCHOOL_PERIOD_AND_ROLE"
            if "role" in held
            else "HIGH_SCHOOL_PERIOD"
        )
        resume_condition = (
            "学校・JBA・大会主催者の新しい公式資料が見つかり、"
            "在籍期間または役割が本文で直接確認できる場合"
        )
        return category, confirmed, held, resume_condition

    if "不存在" in description:
        return (
            "CAREER_ABSENCE",
            "2009年7月のプロ入り",
            "大学Career不存在の包括的確認",
            "本人・所属先等の公式経歴が、大学を経ずにプロ入りしたことを直接示す場合",
        )

    held = "start|end" if "開始・終了年月" in description else "end"
    return (
        "CAREER_PERIOD",
        description.split("が", 1)[0] if "が" in description else description,
        held,
        "大学・競技団体・所属先の新しい公式資料が見つかり、入学・卒業・退部等の時期が本文で直接確認できる場合",
    )


def main() -> None:
    persons = read_csv("person_candidates.csv")
    organizations = read_csv("organization_candidates.csv")
    careers = read_csv("career_candidates.csv")
    issues = read_csv("issues.csv")

    person_names = {row["person_id"]: row["name"] for row in persons}
    organization_names = {
        row["organization_id"]: row["name"] for row in organizations
    }
    career_by_id = {row["career_id"]: row for row in careers}

    queue_rows: list[dict[str, str]] = []
    for sequence, issue in enumerate(
        (row for row in issues if row["status"] in {"OPEN", "HOLD"}), start=1
    ):
        career = career_by_id.get(issue["related_id"], {})
        category, confirmed, held, resume_condition = classify(issue)
        queue_rows.append(
            {
                "queue_id": f"B2Q{sequence:04d}",
                "issue_id": issue["issue_id"],
                "person_id": issue["person_id"],
                "person_name": person_names[issue["person_id"]],
                "career_id": issue["related_id"],
                "organization": organization_names.get(
                    career.get("organization_id", ""), ""
                ),
                "category": category,
                "queue_state": "DEFERRED_UNTIL_NEW_SOURCE",
                "confirmed_scope": confirmed,
                "held_scope": held,
                "next_action": issue["next_check"],
                "resume_condition": resume_condition,
            }
        )

    fieldnames = [
        "queue_id",
        "issue_id",
        "person_id",
        "person_name",
        "career_id",
        "organization",
        "category",
        "queue_state",
        "confirmed_scope",
        "held_scope",
        "next_action",
        "resume_condition",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(queue_rows)

    counts = Counter(row["category"] for row in queue_rows)
    lines = [
        "# Batch 002 例外キュー",
        "",
        "作成日：2026-09-19",
        "",
        "状態：CANDIDATEの項目別HOLDを次回確認まで保留",
        "",
        "## 目的",
        "",
        "未確認項目を確認済み項目から分離し、同じ検索を繰り返さずに次の人数拡大へ進むための作業表である。新しい公式資料が見つかった場合だけ、該当行の調査を再開する。これはVERIFIED、HUMAN APPROVAL、MASTERではない。",
        "",
        "## 件数",
        "",
        f"- 合計：{len(queue_rows)}件",
        f"- 高校の期間・役割：{counts['HIGH_SCHOOL_PERIOD'] + counts['HIGH_SCHOOL_PERIOD_AND_ROLE']}件",
        f"- 大学等の期間：{counts['CAREER_PERIOD']}件",
        f"- Career不存在の確認：{counts['CAREER_ABSENCE']}件",
        "",
        "## 運用ルール",
        "",
        "1. 現在の公式資料で確認できた項目は、そのままCANDIDATEに残す。",
        "2. このキューの項目は推測で補わない。",
        "3. 同じ検索語と同じ資料だけで再調査しない。",
        "4. `resume_condition`を満たす新しい公式資料が得られた時だけ再開する。",
        "5. 例外キューが残っていても、確認済み項目の次段階レビューと次バッチの調査は進められる。",
        "",
        "## 人物別の保留内容",
        "",
        "| Queue | 人物 | 組織 | 保留内容 | 再開条件 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in queue_rows:
        lines.append(
            f"| `{row['queue_id']}` | {row['person_name']} | "
            f"{row['organization']} | {humanize_scope(row['held_scope'])} | "
            f"{row['resume_condition']} |"
        )
    lines.extend(
        [
            "",
            "詳細な確認済み範囲、次の確認先、元のIssue IDは`exception_queue.csv`に記録している。",
            "",
        ]
    )
    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUTPUT_CSV} ({len(queue_rows)} rows)")
    print(f"Wrote {OUTPUT_MD}")


if __name__ == "__main__":
    main()
