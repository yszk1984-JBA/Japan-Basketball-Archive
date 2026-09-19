#!/usr/bin/env python3
"""Build a beginner-friendly review packet for Batch 002.

The packet prepares Yuichi's review before VERIFIED data is created. It never
records approval and never writes MASTER data.
"""

from __future__ import annotations

import csv
import hashlib
from collections import defaultdict
from pathlib import Path


BATCH_DIR = Path("data/candidate/batch_002")
OUTPUT = BATCH_DIR / "verified_review_packet.md"
SNAPSHOT_FILES = [
    "person_candidates.csv",
    "organization_candidates.csv",
    "career_candidates.csv",
    "source_references.csv",
    "evidence_records.csv",
    "issues.csv",
    "qa_decisions.csv",
]

FIELD_LABELS = {
    "name": "氏名",
    "name_en": "英語表記",
    "birth_date": "生年月日",
    "organization_id": "所属組織",
    "role": "役割",
    "start": "開始年",
    "end": "終了年",
    "grade": "学年",
    "jersey_number": "背番号",
    "position": "ポジション",
    "height_cm": "身長",
    "activity_date": "活動日",
    "latest_activity_year": "最新確認年",
    "award": "受賞",
}


def read_csv(filename: str) -> list[dict[str, str]]:
    with (BATCH_DIR / filename).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def labels(value: str) -> str:
    fields = [field for field in value.split("|") if field]
    return "、".join(FIELD_LABELS.get(field, field) for field in fields) or "なし"


def markdown_link(title: str, url: str) -> str:
    return f"[{title}]({url})"


def humanize_issue(description: str) -> str:
    prefix = "確認済み項目は"
    separator = "。未確認項目は"
    if description.startswith(prefix) and separator in description:
        eligible, held = description[len(prefix):].split(separator, 1)
        return f"確認済み：{labels(eligible)}。未確認：{labels(held)}"
    return description


def main() -> None:
    persons = read_csv("person_candidates.csv")
    organizations = read_csv("organization_candidates.csv")
    careers = read_csv("career_candidates.csv")
    sources = read_csv("source_references.csv")
    evidence = read_csv("evidence_records.csv")
    issues = read_csv("issues.csv")
    decisions = read_csv("qa_decisions.csv")

    person_names = {row["person_id"]: row["name"] for row in persons}
    organization_names = {
        row["organization_id"]: row["name"] for row in organizations
    }
    source_by_id = {row["source_id"]: row for row in sources}
    career_by_id = {row["career_id"]: row for row in careers}
    careers_by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for career in careers:
        careers_by_person[career["person_id"]].append(career)

    decisions_by_target = {
        (row["entity_type"], row["entity_id"]): row for row in decisions
    }
    evidence_by_target: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in evidence:
        evidence_by_target[(row["entity_type"], row["entity_id"])].append(row)
    issues_by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in issues:
        if row["status"] in {"OPEN", "HOLD"}:
            issues_by_person[row["person_id"]].append(row)

    ready_count = sum(
        row["decision"] == "READY_FOR_VERIFIED_REVIEW" for row in decisions
    )
    held_issue_count = sum(
        row["status"] in {"OPEN", "HOLD"} for row in issues
    )

    lines = [
        "# Batch 002 VERIFIED作成前レビュー資料",
        "",
        "作成日：2026-09-19",
        "",
        "状態：CANDIDATE・構造QA完了、VERIFIED未作成",
        "",
        "## この資料の目的",
        "",
        "公式資料で確認できた項目を、Yuichiが人物別に確認するための資料である。ここでの確認は、VERIFIED候補を作る前の内容確認であり、Master承認ではない。保留項目を推測で補わない。",
        "",
        "## 現在の状況",
        "",
        f"- 対象人物：{len(persons)}人",
        f"- Career候補：{len(careers)}件",
        f"- 次段階レビュー候補：{ready_count}件",
        f"- 項目別HOLD：{held_issue_count}件",
        "- 構造QA：PASS",
        "- VERIFIED、HUMAN APPROVAL、MASTER：未実施",
        "",
        "## 確認方法",
        "",
        "1. 各人物の「確認対象項目」と公式Sourceを確認する。",
        "2. 「保留項目」は今回のVERIFIED候補へ含めない。",
        "3. 誤りや別人の疑いがあれば、対象のDecision IDと理由を差し戻す。",
        "4. 問題がなければ、末尾の回答形式でVERIFIED候補作成の範囲を指定する。",
        "",
        "## 重要な注意点",
        "",
        "- 松崎裕樹の2026-27所属は、原本Excelの滋賀ではなく、公式発表に合わせてレバンガ北海道を候補としている。原本は変更していない。",
        "- 小川麻斗の2022年終了は日本体育大学男子部での競技Career終了を指す。大学の学籍は継続と公式発表に明記されている。",
        "- 並里成はSouth Kent Schoolの期間を確認したが、その後を含む『大学Careerなし』という包括的な否定は採用していない。",
        "- 高校・大学の開始年や終了年は、公式資料に直接記載がない限り空欄またはHOLDとしている。",
        "",
        "## 人物別レビュー",
        "",
    ]

    for person in persons:
        person_id = person["person_id"]
        person_decision = decisions_by_target[("Person", person_id)]
        person_source_ids: list[str] = []
        person_eligible = set(
            filter(None, person_decision["eligible_fields"].split("|"))
        )
        for item in evidence_by_target[("Person", person_id)]:
            if (
                item["assessment"] == "SUPPORTED"
                and item["field_name"] in person_eligible
                and item["source_id"] not in person_source_ids
            ):
                person_source_ids.append(item["source_id"])
        person_sources = "、".join(
            markdown_link(source_by_id[source_id]["title"], source_by_id[source_id]["url"])
            for source_id in person_source_ids
        )
        lines.extend(
            [
                f"### {person['name']}（`{person_id}`）",
                "",
                f"Person確認：`{person_decision['decision_id']}` — {labels(person_decision['eligible_fields'])} — {person_sources}",
                "",
                "| Decision ID | 対象 | 確認対象項目 | 保留項目 | 主な公式Source |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for career in careers_by_person[person_id]:
            career_id = career["career_id"]
            decision = decisions_by_target[("Career", career_id)]
            eligible_fields = set(filter(None, decision["eligible_fields"].split("|")))
            source_ids: list[str] = []
            for item in evidence_by_target[("Career", career_id)]:
                if (
                    item["assessment"] == "SUPPORTED"
                    and item["field_name"] in eligible_fields
                    and item["source_id"] not in source_ids
                ):
                    source_ids.append(item["source_id"])
            source_links = "<br>".join(
                markdown_link(source_by_id[source_id]["title"], source_by_id[source_id]["url"])
                for source_id in source_ids[:3]
            ) or "—"
            organization = organization_names[career["organization_id"]]
            lines.append(
                "| "
                f"`{decision['decision_id']}` | `{career_id}` {organization} | "
                f"{labels(decision['eligible_fields'])} | "
                f"{labels(decision['held_fields'])} | {source_links} |"
            )
        lines.extend(["", "未解決事項：", ""])
        person_issues = issues_by_person.get(person_id, [])
        if person_issues:
            lines.extend(
                f"- `{row['issue_id']}` {humanize_issue(row['description'])}"
                for row in person_issues
            )
        else:
            lines.append("- なし")
        lines.append("")

    lines.extend(
        [
            "## レビュー対象スナップショット",
            "",
            "以下のハッシュは、このレビュー資料が対象とするCANDIDATEファイルを識別するためのもの。後で内容が変わった場合は再レビューする。",
            "",
            "| ファイル | SHA-256 |",
            "| --- | --- |",
        ]
    )
    for filename in SNAPSHOT_FILES:
        lines.append(f"| `{filename}` | `{sha256(BATCH_DIR / filename)}` |")

    lines.extend(
        [
            "",
            "## Yuichiの回答形式",
            "",
            "確認後は、次の形式で対象を指定する。無回答や単なる『OK』は、Master承認として扱わない。",
            "",
            "```text",
            "対象：Batch 002 VERIFIED候補",
            "範囲：全Decision ID / または個別のDecision ID",
            "判断：VERIFIED候補作成へ進めてよい / 差戻し",
            "差戻し理由：該当する場合のみ記載",
            "```",
            "",
            "VERIFIED候補作成後、Master反映の前に別途HUMAN APPROVALが必要となる。",
        ]
    )

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
