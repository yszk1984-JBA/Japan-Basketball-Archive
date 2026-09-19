#!/usr/bin/env python3
"""Create Batch 003 VERIFIED data from the explicitly reviewed snapshot.

This script refuses to run if the candidate snapshot differs from the hashes
embedded in the review packet. It never writes MASTER data.
"""

from __future__ import annotations

import csv
import hashlib
import re
from collections import defaultdict
from pathlib import Path


CANDIDATE_DIR = Path("data/candidate/batch_003")
OUTPUT_DIR = Path("data/verified/batch_003")
REVIEW_PACKET = CANDIDATE_DIR / "verified_review_packet.md"
AUTHORIZED_AT = "2026-09-20"
AUTHORIZED_BY = "Yuichi"
AUTHORIZED_SCOPE = "Batch 003の全Decision ID（B3D0001〜B3D0028）"
CANDIDATE_COMMIT = "fda72ce"
SNAPSHOT_FILES = [
    "person_candidates.csv",
    "organization_candidates.csv",
    "career_candidates.csv",
    "source_references.csv",
    "evidence_records.csv",
    "issues.csv",
    "qa_decisions.csv",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_hashes() -> dict[str, str]:
    text = REVIEW_PACKET.read_text(encoding="utf-8")
    return dict(re.findall(r"\| `([^`]+\.csv)` \| `([0-9a-f]{64})` \|", text))


def main() -> None:
    expected = expected_hashes()
    if set(expected) != set(SNAPSHOT_FILES):
        raise SystemExit("review packet does not contain the expected snapshot files")
    for filename in SNAPSHOT_FILES:
        actual = sha256(CANDIDATE_DIR / filename)
        if actual != expected[filename]:
            raise SystemExit(f"candidate snapshot changed: {filename}")

    persons = read_csv(CANDIDATE_DIR / "person_candidates.csv")
    organizations = read_csv(CANDIDATE_DIR / "organization_candidates.csv")
    careers = read_csv(CANDIDATE_DIR / "career_candidates.csv")
    sources = read_csv(CANDIDATE_DIR / "source_references.csv")
    evidence = read_csv(CANDIDATE_DIR / "evidence_records.csv")
    issues = read_csv(CANDIDATE_DIR / "issues.csv")
    decisions = read_csv(CANDIDATE_DIR / "qa_decisions.csv")

    if len(decisions) != 28 or any(
        row["decision"] != "READY_FOR_VERIFIED_REVIEW" for row in decisions
    ):
        raise SystemExit("authorized scope is not exactly 28 ready decisions")

    eligible: dict[tuple[str, str], set[str]] = {}
    for row in decisions:
        eligible[(row["entity_type"], row["entity_id"])] = set(
            filter(None, row["eligible_fields"].split("|"))
        )

    verified_evidence = [
        row
        for row in evidence
        if row["assessment"] == "SUPPORTED"
        and row["field_name"] in eligible.get(
            (row["entity_type"], row["entity_id"]), set()
        )
    ]
    verified_source_ids = {row["source_id"] for row in verified_evidence}
    verified_sources = [
        row for row in sources if row["source_id"] in verified_source_ids
    ]
    verified_org_ids = {row["organization_id"] for row in careers}
    verified_organizations = [
        row for row in organizations if row["organization_id"] in verified_org_ids
    ]

    held_fields = [
        {
            "decision_id": row["decision_id"],
            "entity_type": row["entity_type"],
            "entity_id": row["entity_id"],
            "held_fields": row["held_fields"],
            "reason": "CANDIDATEの未確認・矛盾項目として保持",
        }
        for row in decisions
        if row["held_fields"]
    ]

    resolved_by_scope = {
        "B3I0012": "JUBF公式の2023年2年を採用し、外部AI回答の4年を不採用",
        "B3I0015": "JUBF公式の背番号70を採用し、外部AI回答の75を不採用",
    }
    issue_dispositions = []
    for row in issues:
        if row["issue_id"] in resolved_by_scope:
            status = "RESOLVED_FOR_VERIFIED"
            disposition = resolved_by_scope[row["issue_id"]]
        elif row["status"] == "RESOLVED":
            status = "RESOLVED"
            disposition = row["next_check"]
        else:
            status = "HOLD"
            disposition = "VERIFIEDへ含めず、追加の公式資料が得られるまで保留"
        issue_dispositions.append(
            {
                "issue_id": row["issue_id"],
                "person_id": row["person_id"],
                "related_id": row["related_id"],
                "issue_type": row["issue_type"],
                "status": status,
                "description": row["description"],
                "disposition": disposition,
            }
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(
        OUTPUT_DIR / "person_verified.csv",
        ["person_id", "name"],
        persons,
    )
    write_csv(
        OUTPUT_DIR / "organization_verified.csv",
        ["organization_id", "name"],
        verified_organizations,
    )
    write_csv(
        OUTPUT_DIR / "career_verified.csv",
        ["career_id", "person_id", "organization_id", "role", "start", "end"],
        careers,
    )
    write_csv(
        OUTPUT_DIR / "source_references.csv",
        ["source_id", "title", "publisher", "url", "accessed_at"],
        verified_sources,
    )
    write_csv(
        OUTPUT_DIR / "evidence_records.csv",
        [
            "record_id", "entity_type", "entity_id", "field_name",
            "candidate_value", "source_id", "source_locator",
            "evidence_summary", "assessment", "checked_at", "issue_note",
        ],
        verified_evidence,
    )
    write_csv(
        OUTPUT_DIR / "held_fields.csv",
        ["decision_id", "entity_type", "entity_id", "held_fields", "reason"],
        held_fields,
    )
    write_csv(
        OUTPUT_DIR / "issue_dispositions.csv",
        [
            "issue_id", "person_id", "related_id", "issue_type", "status",
            "description", "disposition",
        ],
        issue_dispositions,
    )

    authorization = [
        "# Batch 003 VERIFIED候補 作成許可記録",
        "",
        f"記録日：{AUTHORIZED_AT}",
        f"確認者：{AUTHORIZED_BY}",
        "",
        "## ユーザーの明示的な指示",
        "",
        "> 対象：Batch 003 VERIFIED候補、範囲：全Decision ID、判断：VERIFIED候補作成へ進めてよい",
        "",
        "## 対象",
        "",
        f"- 範囲：{AUTHORIZED_SCOPE}",
        f"- CANDIDATE基準commit：`{CANDIDATE_COMMIT}`",
        "- レビュー資料：`data/candidate/batch_003/verified_review_packet.md`",
        "- Master承認：含まない",
        "- 公開サイト反映：含まない",
        "",
        "## CANDIDATEスナップショット",
        "",
        "| ファイル | SHA-256 |",
        "| --- | --- |",
    ]
    authorization.extend(
        f"| `{filename}` | `{expected[filename]}` |" for filename in SNAPSHOT_FILES
    )
    (OUTPUT_DIR / "review_authorization.md").write_text(
        "\n".join(authorization) + "\n", encoding="utf-8"
    )

    evidence_by_entity = defaultdict(int)
    for row in verified_evidence:
        evidence_by_entity[(row["entity_type"], row["entity_id"])] += 1
    report = [
        "# Batch 003 VERIFIED生成レポート",
        "",
        f"作成日：{AUTHORIZED_AT}",
        "",
        "## 結果",
        "",
        "- CANDIDATEスナップショット：一致",
        f"- 対象Decision：{len(decisions)}件",
        f"- Person：{len(persons)}件",
        f"- Career：{len(careers)}件",
        f"- Organization：{len(verified_organizations)}件",
        f"- Source：{len(verified_sources)}件",
        f"- 採用Evidence：{len(verified_evidence)}件",
        f"- HOLD項目のあるDecision：{len(held_fields)}件",
        f"- HOLD Issue：{sum(row['status'] == 'HOLD' for row in issue_dispositions)}件",
        "- Master：未作成",
        "- 公開サイト：未変更",
        "",
        "## 解釈",
        "",
        "VERIFIEDは公式Source・QA・指定範囲のレビューを通過した候補であり、Master承認済みを意味しない。",
        "開始・終了年月、當山修梧の学年、本松龍斗の大学Player役割などのHOLD項目は含めていない。",
        "",
    ]
    (OUTPUT_DIR / "verification_report.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    readme = [
        "# Batch 003 VERIFIED",
        "",
        f"作成日：{AUTHORIZED_AT}",
        "",
        "状態：VERIFIED、HUMAN APPROVAL・MASTER未実施",
        "",
        "Batch 003の全28 Decision IDについて、Yuichiの明示的な指示に基づき、eligible_fieldsだけをCANDIDATEから抽出した。held_fieldsと未解決Issueは別ファイルに保持している。",
        "",
        "このディレクトリのVERIFIEDは確認済み候補であり、正式なMaster Dataでも公開承認済みデータでもない。",
        "",
        "## ファイル",
        "",
        "- `person_verified.csv`：確認対象となった10人",
        "- `organization_verified.csv`：Careerが参照する9組織",
        "- `career_verified.csv`：確認対象となった18件のCareer",
        "- `source_references.csv`：採用Evidenceが参照する公式Source",
        "- `evidence_records.csv`：eligible_fieldsに一致したSUPPORTED Evidence",
        "- `held_fields.csv`：VERIFIEDへ含めなかった項目",
        "- `issue_dispositions.csv`：IssueのVERIFIED時点での扱い",
        "- `review_authorization.md`：対象版・範囲・指示の記録",
        "- `verification_report.md`：生成結果",
        "",
    ]
    (OUTPUT_DIR / "README.md").write_text("\n".join(readme), encoding="utf-8")


if __name__ == "__main__":
    main()
