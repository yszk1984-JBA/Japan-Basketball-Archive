#!/usr/bin/env python3
"""Create Batch 002 VERIFIED candidates from Yuichi's reviewed scope."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "data" / "candidate" / "batch_002"
OUTPUT = ROOT / "data" / "verified" / "batch_002"
REVIEW_PACKET = CANDIDATE / "verified_review_packet.md"
CANDIDATE_COMMIT = "ff8fcff9a43e1c24e6a12b751190a95c0b6be340"
AUTHORIZED_AT = "2026-09-21"
SNAPSHOT_FILES = [
    "person_candidates.csv", "organization_candidates.csv", "career_candidates.csv",
    "source_references.csv", "evidence_records.csv", "issues.csv", "qa_decisions.csv",
]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    expected = dict(re.findall(r"\| `([^`]+\.csv)` \| `([0-9a-f]{64})` \|", REVIEW_PACKET.read_text(encoding="utf-8")))
    if set(expected) != set(SNAPSHOT_FILES):
        raise SystemExit("Review packet snapshot is incomplete")
    for filename in SNAPSHOT_FILES:
        if sha256(CANDIDATE / filename) != expected[filename]:
            raise SystemExit(f"Candidate snapshot changed: {filename}")

    persons = read(CANDIDATE / "person_candidates.csv")
    organizations = read(CANDIDATE / "organization_candidates.csv")
    career_candidates = read(CANDIDATE / "career_candidates.csv")
    sources = read(CANDIDATE / "source_references.csv")
    evidence = read(CANDIDATE / "evidence_records.csv")
    issues = read(CANDIDATE / "issues.csv")
    decisions = read(CANDIDATE / "qa_decisions.csv")

    if len(decisions) != 40 or any(row["decision"] != "READY_FOR_VERIFIED_REVIEW" for row in decisions):
        raise SystemExit("Authorized scope is not exactly 40 ready decisions")

    eligible: dict[tuple[str, str], set[str]] = {}
    for row in decisions:
        eligible[(row["entity_type"], row["entity_id"])] = set(filter(None, row["eligible_fields"].split("|")))

    careers = []
    for row in career_candidates:
        allowed = eligible.get(("Career", row["career_id"]), set())
        careers.append({
            "career_id": row["career_id"],
            "person_id": row["person_id"],
            "organization_id": row["organization_id"] if "organization_id" in allowed else "",
            "role": row["role"] if "role" in allowed else "",
            "start": row["start"] if "start" in allowed else "",
            "end": row["end"] if "end" in allowed else "",
        })

    verified_evidence = [
        row for row in evidence
        if row["assessment"] == "SUPPORTED"
        and row["field_name"] in eligible.get((row["entity_type"], row["entity_id"]), set())
    ]
    source_ids = {row["source_id"] for row in verified_evidence}
    verified_sources = [row for row in sources if row["source_id"] in source_ids]
    organization_ids = {row["organization_id"] for row in careers if row["organization_id"]}
    verified_organizations = [row for row in organizations if row["organization_id"] in organization_ids]
    held_fields = [
        {
            "decision_id": row["decision_id"], "entity_type": row["entity_type"],
            "entity_id": row["entity_id"], "held_fields": row["held_fields"],
            "reason": "CANDIDATEの未確認項目として保持",
        }
        for row in decisions if row["held_fields"]
    ]
    issue_dispositions = [
        {
            "issue_id": row["issue_id"], "person_id": row["person_id"],
            "related_id": row["related_id"], "issue_type": row["issue_type"],
            "status": row["status"], "description": row["description"],
            "disposition": row["next_check"] if row["status"] == "RESOLVED" else "VERIFIEDへ含めず、新しい公式資料が得られるまで保留",
        }
        for row in issues
    ]

    OUTPUT.mkdir(parents=True, exist_ok=True)
    write(OUTPUT / "person_verified.csv", ["person_id", "name"], persons)
    write(OUTPUT / "organization_verified.csv", ["organization_id", "name"], verified_organizations)
    write(OUTPUT / "career_verified.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    write(OUTPUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], verified_sources)
    write(OUTPUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], verified_evidence)
    write(OUTPUT / "held_fields.csv", ["decision_id", "entity_type", "entity_id", "held_fields", "reason"], held_fields)
    write(OUTPUT / "issue_dispositions.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "disposition"], issue_dispositions)

    authorization = [
        "# Batch 002 VERIFIED候補 作成許可記録", "", f"記録日：{AUTHORIZED_AT}",
        "確認者：Yuichi", "", "## ユーザーの明示的な指示", "",
        "> 対象：Batch 002 VERIFIED候補、範囲：全Decision ID、判断：VERIFIED候補作成へ進めてよい",
        "", "## 対象", "", "- 範囲：全40 Decision ID（B2D0001〜B2D0040）",
        f"- CANDIDATE基準commit：`{CANDIDATE_COMMIT}`",
        "- レビュー資料：`data/candidate/batch_002/verified_review_packet.md`",
        "- Master承認：含まない", "- 公開サイト反映：含まない", "",
        "## CANDIDATEスナップショット", "", "| ファイル | SHA-256 |", "| --- | --- |",
    ]
    authorization.extend(f"| `{filename}` | `{expected[filename]}` |" for filename in SNAPSHOT_FILES)
    (OUTPUT / "review_authorization.md").write_text("\n".join(authorization) + "\n", encoding="utf-8")

    report = f"""# Batch 002 VERIFIED生成レポート

作成日：{AUTHORIZED_AT}

## 結果

- CANDIDATEスナップショット：一致
- 対象Decision：{len(decisions)}件
- Person：{len(persons)}件
- Career：{len(careers)}件
- Organization：{len(verified_organizations)}件
- Source：{len(verified_sources)}件
- 採用Evidence：{len(verified_evidence)}件
- HOLD項目のあるDecision：{len(held_fields)}件
- HOLD Issue：{sum(row['status'] == 'HOLD' for row in issue_dispositions)}件
- Master・公開サイト：未変更

VERIFIEDは確認済み候補であり、Human Approval済みのMasterではない。
"""
    (OUTPUT / "verification_report.md").write_text(report, encoding="utf-8")
    readme = f"""# Batch 002 VERIFIED

作成日：{AUTHORIZED_AT}

状態：VERIFIED候補、HUMAN APPROVAL・MASTER未実施

全40 Decision IDについて、Yuichiの明示的指示に基づきeligible fieldsだけを抽出した。28件のheld fieldsと19件のHOLD Issueは別ファイルに保持し、VERIFIED Evidenceへ含めていない。

## 件数

- Person：{len(persons)}件
- Career：{len(careers)}件
- Organization：{len(verified_organizations)}件
- Source：{len(verified_sources)}件
- Evidence：{len(verified_evidence)}件
"""
    (OUTPUT / "README.md").write_text(readme, encoding="utf-8")
    print(f"Batch 002 VERIFIED: {len(persons)} persons, {len(careers)} careers, {len(verified_evidence)} evidence")


if __name__ == "__main__":
    main()
