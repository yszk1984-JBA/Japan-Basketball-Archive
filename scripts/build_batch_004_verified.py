#!/usr/bin/env python3
"""Create Batch 004 VERIFIED candidates from eligible fields only.

This is an AI verification output. It never creates HUMAN APPROVAL or MASTER data.
"""

from __future__ import annotations

import csv
import subprocess
from collections import defaultdict
from pathlib import Path


CANDIDATE_DIR = Path("data/candidate/batch_004")
REVIEW_DIR = CANDIDATE_DIR / "review_packet"
OUTPUT_DIR = Path("data/verified/batch_004")
SOURCE_COMMIT = "4718d81"
CREATED_AT = "2026-09-21"
WAVES = [CANDIDATE_DIR / f"wave_{number:02d}" for number in range(1, 5)]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def unchanged_since_review() -> None:
    paths = [str(path) for wave in WAVES for path in sorted(wave.glob("*.csv"))]
    paths.extend([
        str(REVIEW_DIR / "verification_scope.csv"),
        str(REVIEW_DIR / "held_issues.csv"),
    ])
    result = subprocess.run(
        ["git", "diff", "--quiet", SOURCE_COMMIT, "--", *paths],
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("Batch 004 candidate snapshot changed after the review packet")


def unique(rows: list[dict[str, str]], key: str, value_fields: list[str]) -> list[dict[str, str]]:
    found: dict[str, dict[str, str]] = {}
    for row in rows:
        identifier = row[key]
        compact = {field: row[field] for field in [key, *value_fields]}
        if identifier in found and found[identifier] != compact:
            raise SystemExit(f"conflicting duplicate {identifier}")
        found[identifier] = compact
    return list(found.values())


def main() -> None:
    unchanged_since_review()
    decisions = read(REVIEW_DIR / "verification_scope.csv")
    issues = read(REVIEW_DIR / "held_issues.csv")
    if len(decisions) != 75 or any(row["decision"] != "READY_FOR_VERIFIED_REVIEW" for row in decisions):
        raise SystemExit("review scope is not exactly 75 ready decisions")

    eligible: dict[tuple[str, str], set[str]] = defaultdict(set)
    held: list[dict[str, str]] = []
    for row in decisions:
        target = (row["entity_type"], row["entity_id"])
        eligible[target].update(filter(None, row["eligible_fields"].split("|")))
        if row["held_fields"]:
            held.append({
                "wave": row["wave"],
                "decision_id": row["decision_id"],
                "entity_type": row["entity_type"],
                "entity_id": row["entity_id"],
                "held_fields": row["held_fields"],
                "reason": "CANDIDATEの未確認・矛盾項目として保持",
            })

    persons = unique(
        [row for wave in WAVES for row in read(wave / "person_candidates.csv")],
        "person_id", ["name"],
    )
    organizations = unique(
        [row for wave in WAVES for row in read(wave / "organization_candidates.csv")],
        "organization_id", ["name"],
    )
    careers = unique(
        [row for wave in WAVES for row in read(wave / "career_candidates.csv")],
        "career_id", ["person_id", "organization_id", "role", "start", "end"],
    )
    sources = unique(
        [row for wave in WAVES for row in read(wave / "source_references.csv")],
        "source_id", ["title", "publisher", "url", "accessed_at"],
    )
    evidence = [row for wave in WAVES for row in read(wave / "evidence_records.csv")]

    verified_evidence = [
        row for row in evidence
        if row["assessment"] == "SUPPORTED"
        and row["field_name"] in eligible[(row["entity_type"], row["entity_id"])]
    ]
    used_source_ids = {row["source_id"] for row in verified_evidence}
    verified_sources = [row for row in sources if row["source_id"] in used_source_ids]

    verified_persons = [
        row for row in persons if "name" in eligible[("Person", row["person_id"])]
    ]
    verified_organizations = [
        row for row in organizations
        if "name" in eligible[("Organization", row["organization_id"])]
    ]
    verified_careers = []
    for row in careers:
        allowed = eligible[("Career", row["career_id"])]
        verified_careers.append({
            "career_id": row["career_id"],
            "person_id": row["person_id"],
            "organization_id": row["organization_id"] if "organization_id" in allowed else "",
            "role": row["role"] if "role" in allowed else "",
            "start": row["start"] if "start" in allowed else "",
            "end": row["end"] if "end" in allowed else "",
        })

    issue_dispositions = [{
        "wave": row["wave"],
        "issue_id": row["issue_id"],
        "person_id": row["person_id"],
        "related_id": row["related_id"],
        "issue_type": row["issue_type"],
        "status": "HOLD",
        "description": row["description"],
        "disposition": "VERIFIEDへ含めず、追加の公式資料が得られるまで保留",
    } for row in issues]

    write(OUTPUT_DIR / "person_verified.csv", ["person_id", "name"], verified_persons)
    write(OUTPUT_DIR / "organization_verified.csv", ["organization_id", "name"], verified_organizations)
    write(OUTPUT_DIR / "career_verified.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], verified_careers)
    write(OUTPUT_DIR / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], verified_sources)
    write(OUTPUT_DIR / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], verified_evidence)
    write(OUTPUT_DIR / "held_fields.csv", ["wave", "decision_id", "entity_type", "entity_id", "held_fields", "reason"], held)
    write(OUTPUT_DIR / "issue_dispositions.csv", ["wave", "issue_id", "person_id", "related_id", "issue_type", "status", "description", "disposition"], issue_dispositions)

    scope = f"""# Batch 004 VERIFIED候補 作成範囲

作成日：{CREATED_AT}

ユーザーの「続けて」という作業指示を受け、Batch 004レビュー資料の全75 Decisionについて`eligible_fields`だけをVERIFIED候補へ抽出した。

- CANDIDATE・レビュー基準commit：`{SOURCE_COMMIT}`
- 対象：`data/candidate/batch_004/review_packet/verification_scope.csv`
- 除外：`held_fields`、全HOLD Issue
- HUMAN APPROVAL：含まない
- Master承認・反映：含まない
- 公開サイト反映：含まない
"""
    (OUTPUT_DIR / "verification_scope.md").write_text(scope, encoding="utf-8")

    report = f"""# Batch 004 VERIFIED生成レポート

作成日：{CREATED_AT}

## 結果

- CANDIDATEスナップショット：commit `{SOURCE_COMMIT}`から変更なし
- 対象Decision：{len(decisions)}件
- Person：{len(verified_persons)}件
- Career：{len(verified_careers)}件
- Organization：{len(verified_organizations)}件
- Source：{len(verified_sources)}件
- 採用Evidence：{len(verified_evidence)}件
- HOLD項目のあるDecision：{len(held)}件
- HOLD Issue：{len(issue_dispositions)}件
- Master：未作成
- 公開サイト：未変更

## 解釈

VERIFIEDは公式SourceとQAを通過した確認済み候補であり、HUMAN APPROVALまたはMasterを意味しない。Careerの`role`、`start`、`end`にHOLD指定がある場合、その列は空欄にしている。
"""
    (OUTPUT_DIR / "verification_report.md").write_text(report, encoding="utf-8")

    readme = f"""# Batch 004 VERIFIED

作成日：{CREATED_AT}

状態：VERIFIED候補、HUMAN APPROVAL・MASTER未実施

Batch 004の全75 Decision IDについて、`eligible_fields`に一致するSUPPORTED Evidenceだけを抽出した。`held_fields`と33件のHOLD Issueは別ファイルに保持している。

このディレクトリは確認済み候補であり、正式なMaster Dataでも公開承認済みデータでもない。

## ファイル

- `person_verified.csv`：10人
- `organization_verified.csv`：20組織
- `career_verified.csv`：38件
- `source_references.csv`：採用Evidenceが参照する公式Source
- `evidence_records.csv`：eligible_fieldsに一致したSUPPORTED Evidence
- `held_fields.csv`：VERIFIEDへ含めなかった項目
- `issue_dispositions.csv`：33件のHOLD
- `verification_scope.md`：対象範囲と除外事項
- `verification_report.md`：生成結果
"""
    (OUTPUT_DIR / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
