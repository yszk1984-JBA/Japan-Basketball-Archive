#!/usr/bin/env python3
"""Create Batch 006 VERIFIED candidates from READY decisions only.

This output never creates HUMAN APPROVAL or MASTER data.
"""

from __future__ import annotations

import csv
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WAVE = ROOT / "data" / "candidate" / "batch_006" / "wave_01"
OUTPUT = ROOT / "data" / "verified" / "batch_006"
SOURCE_COMMIT = "a3de894"
CREATED_AT = "2026-09-21"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(name: str, headers: list[str], rows: list[dict[str, str]]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def unchanged_since_review() -> None:
    paths = [str(path.relative_to(ROOT)) for path in sorted(WAVE.glob("*.csv"))]
    result = subprocess.run(
        ["git", "diff", "--quiet", SOURCE_COMMIT, "--", *paths],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("Batch 006 candidate snapshot changed after QA")


def unique(rows: list[dict[str, str]], key: str, fields: list[str]) -> list[dict[str, str]]:
    found: dict[str, dict[str, str]] = {}
    for row in rows:
        compact = {field: row[field] for field in [key, *fields]}
        if row[key] in found and found[row[key]] != compact:
            raise SystemExit(f"conflicting duplicate {row[key]}")
        found[row[key]] = compact
    return list(found.values())


def main() -> None:
    unchanged_since_review()
    decisions = read(WAVE / "qa_decisions.csv")
    ready = [row for row in decisions if row["decision"] == "READY_FOR_VERIFIED_REVIEW"]
    holds = [row for row in decisions if row["decision"] == "HOLD_CANDIDATE"]
    issues = read(WAVE / "issues.csv")
    if len(ready) != 21 or len(holds) != 2:
        raise SystemExit("Batch 006 QA decision counts changed")
    if len(issues) != 10 or any(row["status"] != "HOLD" for row in issues):
        raise SystemExit("Batch 006 HOLD issue counts changed")

    eligible: dict[tuple[str, str], set[str]] = defaultdict(set)
    held_rows: list[dict[str, str]] = []
    for row in ready:
        target = (row["entity_type"], row["entity_id"])
        eligible[target].update(filter(None, row["eligible_fields"].split("|")))
        if row["held_fields"]:
            held_rows.append({
                "decision_id": row["decision_id"],
                "entity_type": row["entity_type"],
                "entity_id": row["entity_id"],
                "held_fields": row["held_fields"],
                "reason": "READY判断内の未確認項目としてVERIFIEDから除外",
            })
    for row in holds:
        held_fields = "|".join(dict.fromkeys(filter(None, [
            *row["eligible_fields"].split("|"), *row["held_fields"].split("|"),
        ])))
        held_rows.append({
            "decision_id": row["decision_id"],
            "entity_type": row["entity_type"],
            "entity_id": row["entity_id"],
            "held_fields": held_fields,
            "reason": "HOLD_CANDIDATE判断のためEntity全体をVERIFIEDから除外",
        })

    persons = unique(read(WAVE / "person_candidates.csv"), "person_id", ["name"])
    organizations = unique(read(WAVE / "organization_candidates.csv"), "organization_id", ["name"])
    careers = unique(
        read(WAVE / "career_candidates.csv"), "career_id",
        ["person_id", "organization_id", "role", "start", "end"],
    )
    sources = unique(
        read(WAVE / "source_references.csv"), "source_id",
        ["title", "publisher", "url", "accessed_at"],
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
    verified_careers: list[dict[str, str]] = []
    for row in careers:
        allowed = eligible[("Career", row["career_id"])]
        if "organization_id" not in allowed:
            continue
        verified_careers.append({
            "career_id": row["career_id"],
            "person_id": row["person_id"],
            "organization_id": row["organization_id"],
            "role": row["role"] if "role" in allowed else "",
            "start": row["start"] if "start" in allowed else "",
            "end": row["end"] if "end" in allowed else "",
        })

    issue_dispositions = [{
        "issue_id": row["issue_id"],
        "person_id": row["person_id"],
        "related_id": row["related_id"],
        "issue_type": row["issue_type"],
        "status": "HOLD",
        "description": row["description"],
        "disposition": "VERIFIEDへ含めず、追加の公式資料が得られるまで保留",
    } for row in issues]

    write("person_verified.csv", ["person_id", "name"], verified_persons)
    write("organization_verified.csv", ["organization_id", "name"], verified_organizations)
    write("career_verified.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], verified_careers)
    write("source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], verified_sources)
    write("evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], verified_evidence)
    write("held_fields.csv", ["decision_id", "entity_type", "entity_id", "held_fields", "reason"], held_rows)
    write("issue_dispositions.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "disposition"], issue_dispositions)

    scope = f"""# Batch 006 Wave 1 VERIFIED候補 作成範囲

作成日：{CREATED_AT}

Batch 006 Wave 1のQA判断から、READY 21件の`eligible_fields`だけをVERIFIED候補へ抽出した。

- CANDIDATE・QA基準commit：`{SOURCE_COMMIT}`
- 対象：`data/candidate/batch_006/wave_01/qa_decisions.csv`のREADY 21件
- 除外：HOLD_CANDIDATE 2件、`held_fields`、全HOLD Issue
- HUMAN APPROVAL：含まない
- Master承認・反映：含まない
- 公開サイト反映：含まない
"""
    (OUTPUT / "verification_scope.md").write_text(scope, encoding="utf-8")

    report = f"""# Batch 006 Wave 1 VERIFIED生成レポート

作成日：{CREATED_AT}

## 結果

- CANDIDATEスナップショット：commit `{SOURCE_COMMIT}`から変更なし
- READY Decision：{len(ready)}件
- HOLD Decision：{len(holds)}件
- Person：{len(verified_persons)}件
- Career：{len(verified_careers)}件
- Organization：{len(verified_organizations)}件
- Source：{len(verified_sources)}件
- 採用Evidence：{len(verified_evidence)}件
- HOLD記録：{len(held_rows)}件
- HOLD Issue：{len(issue_dispositions)}件
- HUMAN APPROVAL・Master：未実施
- 公開サイト：未変更

VERIFIEDは公式SourceとQAを通過した確認済み候補であり、Human ApprovalまたはMasterを意味しない。
"""
    (OUTPUT / "verification_report.md").write_text(report, encoding="utf-8")

    readme = f"""# Batch 006 VERIFIED

作成日：{CREATED_AT}

状態：VERIFIED候補、HUMAN APPROVAL・MASTER未実施

Batch 006 Wave 1のREADY 21判断について、`eligible_fields`に一致するSUPPORTED Evidenceだけを抽出した。HOLD判断、`held_fields`、10件のHOLD Issueは除外・分離している。

このディレクトリは確認済み候補であり、正式なMaster Dataでも公開承認済みデータでもない。

## ファイル

- `person_verified.csv`：{len(verified_persons)}人
- `organization_verified.csv`：{len(verified_organizations)}組織
- `career_verified.csv`：{len(verified_careers)}件
- `source_references.csv`：採用Evidenceが参照する公式Source
- `evidence_records.csv`：eligible_fieldsに一致したSUPPORTED Evidence
- `held_fields.csv`：VERIFIEDへ含めなかった判断・項目
- `issue_dispositions.csv`：{len(issue_dispositions)}件のHOLD
- `verification_scope.md`：対象範囲と除外事項
- `verification_report.md`：生成結果
- `validation_report.md`：構造検証結果
"""
    (OUTPUT / "README.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
