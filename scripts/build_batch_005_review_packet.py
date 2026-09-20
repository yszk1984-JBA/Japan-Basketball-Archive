#!/usr/bin/env python3
"""Create the Batch 005 Wave 1 human-review packet."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


WAVE = Path("data/candidate/batch_005/wave_01")
OUT = Path("data/candidate/batch_005/review_packet")


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
    decisions = [{"wave": "wave_01", **row} for row in read(WAVE / "qa_decisions.csv")]
    issues = [{"wave": "wave_01", **row} for row in read(WAVE / "issues.csv")]
    persons = read(WAVE / "person_candidates.csv")
    careers = read(WAVE / "career_candidates.csv")
    organizations = read(WAVE / "organization_candidates.csv")
    sources = read(WAVE / "source_references.csv")
    evidence = read(WAVE / "evidence_records.csv")

    if len(decisions) != 26 or any(row["decision"] != "READY_FOR_VERIFIED_REVIEW" for row in decisions):
        raise SystemExit("Batch 005 review scope is not exactly 26 ready decisions")
    if len(issues) != 9 or any(row["status"] != "HOLD" for row in issues):
        raise SystemExit("Batch 005 review packet must contain exactly 9 HOLD issues")

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
    report = f"""# Batch 005 Wave 1 次段階レビュー資料

作成日：2026-09-21

この資料はCANDIDATEからVERIFIED候補へ進める項目を選別したQA記録です。この資料の作成だけではHUMAN APPROVAL、MASTER、公開サイトへの反映を行いません。

## 対象

- Person：{len(persons)}人
- Career：{len(careers)}件
- Organization：{len(organizations)}件
- Source：{len(sources)}件
- Evidence：{len(evidence)}件
- QA Decision：{len(decisions)}件
- HOLD Issue：{len(issues)}件

## VERIFIED候補の選別範囲

- Person Decision：{decision_types['Person']}件
- Career Decision：{decision_types['Career']}件
- Organization Decision：{decision_types['Organization']}件
- 全Decisionの現在判定：`READY_FOR_VERIFIED_REVIEW`
- 詳細：[`verification_scope.csv`](verification_scope.csv)

`eligible_fields`だけをVERIFIED候補に含めます。`held_fields`とHOLD Issueは除外します。

## HOLDの内訳

{issue_lines}

詳細は[`held_issues.csv`](held_issues.csv)にあり、追加確認先も記録しています。

## 重複・ID再利用確認

- `P000028`佐藤涼成と`P000066`河合瑠那は既存Person IDを再利用しています。
- `C000229`河合瑠那の横浜エクセレンスCareerは既存Career IDを再利用しています。
- 福岡第一高等学校、東海大学、佐賀バルーナーズ、横浜ビー・コルセアーズ、横浜エクセレンス、白鷗大学は既存Organization IDを再利用しています。
- 崎濱秀斗と崎濱秀真は名が異なるため別Person IDです。

## 選別上の境界

- プロ契約、リーグ登録、公式戦出場、活動終了を別項目として扱います。
- 轟琉維の佐賀での所属・出場は対象に含め、クラブ一次資料で未確認の契約・登録区分は除外します。
- 身長の資料間差、学校・大学の未確認期間、正確な登録抹消日は除外します。
- VERIFIED候補はHuman ApprovalまたはMasterではありません。

## 対象Decision ID

{decision_ids}
"""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "README.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
