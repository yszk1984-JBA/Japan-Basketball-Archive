#!/usr/bin/env python3
"""Aggregate Batch 004 QA outputs into a human-review packet."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


BASE = Path("data/candidate/batch_004")
OUT = BASE / "review_packet"
WAVES = [BASE / f"wave_{number:02d}" for number in range(1, 5)]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    decisions: list[dict[str, str]] = []
    issues: list[dict[str, str]] = []
    person_ids: set[str] = set()
    career_ids: set[str] = set()
    organization_ids: set[str] = set()
    source_ids: set[str] = set()
    evidence_count = 0

    for wave in WAVES:
        wave_name = wave.name
        person_ids.update(row["person_id"] for row in read(wave / "person_candidates.csv"))
        career_ids.update(row["career_id"] for row in read(wave / "career_candidates.csv"))
        organization_ids.update(row["organization_id"] for row in read(wave / "organization_candidates.csv"))
        source_ids.update(row["source_id"] for row in read(wave / "source_references.csv"))
        evidence_count += len(read(wave / "evidence_records.csv"))

        for row in read(wave / "qa_decisions.csv"):
            decisions.append({"wave": wave_name, **row})
        for row in read(wave / "issues.csv"):
            issues.append({"wave": wave_name, **row})

    write_csv(
        OUT / "verification_scope.csv",
        ["wave", "decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"],
        decisions,
    )
    write_csv(
        OUT / "held_issues.csv",
        ["wave", "issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"],
        issues,
    )

    decision_types = Counter(row["entity_type"] for row in decisions)
    issue_types = Counter(row["issue_type"] for row in issues)
    issue_lines = "\n".join(
        f"- `{issue_type}`：{count}件" for issue_type, count in sorted(issue_types.items())
    )
    decision_ids = "、".join(row["decision_id"] for row in decisions)
    report = f"""# Batch 004 次段階レビュー資料

作成日：2026-09-21

この資料はCANDIDATEからVERIFIED候補作成へ進む範囲を、人間が判断するためのものです。この資料の作成だけではVERIFIED、HUMAN APPROVAL、MASTERへの昇格を行いません。

## 対象

- Person：{len(person_ids)}人
- Career：{len(career_ids)}件
- Organization：{len(organization_ids)}件
- Source：{len(source_ids)}件
- Evidence：{evidence_count}件
- QA Decision：{len(decisions)}件
- HOLD Issue：{len(issues)}件

## 次段階レビュー候補

- Person Decision：{decision_types['Person']}件
- Career Decision：{decision_types['Career']}件
- Organization Decision：{decision_types['Organization']}件
- 全Decisionの現在判定：`READY_FOR_VERIFIED_REVIEW`
- 詳細：[`verification_scope.csv`](verification_scope.csv)

`eligible_fields`だけが次段階の対象です。`held_fields`は昇格対象から除外します。

## HOLDの内訳

{issue_lines}

詳細は[`held_issues.csv`](held_issues.csv)にあり、各行に次の確認先を記録しています。HOLDを解消しなくても、対象外として分離したまま次段階レビューへ進めます。

## 重複確認

- Batch 004内の人物名は10人すべて別IDで、同名別IDはありません。
- 福岡第一高等学校、東海大学、日本経済大学、横浜エクセレンス、山口パッツファイブは複数Waveに出ますが、同じOrganization IDを再利用しています。
- `P000014`キエキエ トピー アリは既存人物IDを再利用しています。Batch 004で新規発番した人物は9人です。

## 人間判断の対象文

次のように対象・範囲・判断を明示すると、VERIFIED候補作成へ進められます。

> 対象：Batch 004、範囲：全Decision IDのeligible_fields、判断：VERIFIED候補作成へ進めてよい。held_fieldsとHOLD Issueは対象外。

対象Decision ID：{decision_ids}

## 禁止事項

- この承認をMaster承認として扱わない。
- `held_fields`やHOLD Issueを推測で補わない。
- プロ契約、リーグ登録、公式戦出場、ドラフト候補掲載を相互に読み替えない。
"""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "README.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
