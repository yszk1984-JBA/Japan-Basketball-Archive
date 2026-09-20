#!/usr/bin/env python3
"""Create Batch 005 Wave 1 VERIFIED candidates from eligible fields only.

This output never creates HUMAN APPROVAL or MASTER data.
"""

from __future__ import annotations

import csv
import subprocess
from collections import defaultdict
from pathlib import Path


WAVE = Path("data/candidate/batch_005/wave_01")
REVIEW = Path("data/candidate/batch_005/review_packet")
OUTPUT = Path("data/verified/batch_005")
SOURCE_COMMIT = "bddb2e1"
CREATED_AT = "2026-09-21"


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
    paths = [str(path) for path in sorted(WAVE.glob("*.csv"))]
    paths.extend([
        str(REVIEW / "verification_scope.csv"),
        str(REVIEW / "held_issues.csv"),
    ])
    result = subprocess.run(
        ["git", "diff", "--quiet", SOURCE_COMMIT, "--", *paths],
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("Batch 005 candidate snapshot changed after the review packet")


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
    decisions = read(REVIEW / "verification_scope.csv")
    issues = read(REVIEW / "held_issues.csv")
    if len(decisions) != 26 or any(row["decision"] != "READY_FOR_VERIFIED_REVIEW" for row in decisions):
        raise SystemExit("review scope is not exactly 26 ready decisions")
    if len(issues) != 9 or any(row["status"] != "HOLD" for row in issues):
        raise SystemExit("review packet is not exactly 9 HOLD issues")

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

    persons = unique(read(WAVE / "person_candidates.csv"), "person_id", ["name"])
    organizations = unique(read(WAVE / "organization_candidates.csv"), "organization_id", ["name"])
    careers = unique(
        read(WAVE / "career_candidates.csv"),
        "career_id", ["person_id", "organization_id", "role", "start", "end"],
    )
    sources = unique(
        read(WAVE / "source_references.csv"),
        "source_id", ["title", "publisher", "url", "accessed_at"],
    )
    evidence = read(WAVE / "evidence_records.csv")

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
        row for row in organizations if "name" in eligible[("Organization", row["organization_id"])]
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

    write(OUTPUT / "person_verified.csv", ["person_id", "name"], verified_persons)
    write(OUTPUT / "organization_verified.csv", ["organization_id", "name"], verified_organizations)
    write(OUTPUT / "career_verified.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], verified_careers)
    write(OUTPUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], verified_sources)
    write(OUTPUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], verified_evidence)
    write(OUTPUT / "held_fields.csv", ["wave", "decision_id", "entity_type", "entity_id", "held_fields", "reason"], held)
    write(OUTPUT / "issue_dispositions.csv", ["wave", "issue_id", "person_id", "related_id", "issue_type", "status", "description", "disposition"], issue_dispositions)

    scope = f"""# Batch 005 Wave 1 VERIFIED候補 作成範囲

作成日：{CREATED_AT}

Batch 005 Wave 1レビュー資料の全26 Decisionについて、`eligible_fields`だけをVERIFIED候補へ抽出した。

- CANDIDATE・レビュー基準commit：`{SOURCE_COMMIT}`
- 対象：`data/candidate/batch_005/review_packet/verification_scope.csv`
- 除外：`held_fields`、全HOLD Issue
- HUMAN APPROVAL：含まない
- Master承認・反映：含まない
- 公開サイト反映：含まない
"""
    (OUTPUT / "verification_scope.md").write_text(scope, encoding="utf-8")

    report = f"""# Batch 005 Wave 1 VERIFIED生成レポート

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
- Human Approval・Master：未実施
- 公開サイト：未変更

## 解釈

VERIFIEDは公式SourceとQAを通過した確認済み候補であり、Human ApprovalまたはMasterを意味しない。Careerの`role`、`start`、`end`にHOLD指定がある場合、その列は空欄にしている。
"""
    (OUTPUT / "verification_report.md").write_text(report, encoding="utf-8")

    readme = f"""# Batch 005 VERIFIED

作成日：{CREATED_AT}

状態：VERIFIED候補、HUMAN APPROVAL・MASTER未実施

Batch 005 Wave 1の全26 Decision IDについて、`eligible_fields`に一致するSUPPORTED Evidenceだけを抽出した。`held_fields`と9件のHOLD Issueは別ファイルに保持している。

このディレクトリは確認済み候補であり、正式なMaster Dataでも公開承認済みデータでもない。

## ファイル

- `person_verified.csv`：{len(verified_persons)}人
- `organization_verified.csv`：{len(verified_organizations)}組織
- `career_verified.csv`：{len(verified_careers)}件
- `source_references.csv`：採用Evidenceが参照する公式Source
- `evidence_records.csv`：eligible_fieldsに一致したSUPPORTED Evidence
- `held_fields.csv`：VERIFIEDへ含めなかった項目
- `issue_dispositions.csv`：{len(issue_dispositions)}件のHOLD
- `verification_scope.md`：対象範囲と除外事項
- `verification_report.md`：生成結果
- `validation_report.md`：構造検証結果
"""
    (OUTPUT / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
