#!/usr/bin/env python3
"""Build Batch 018 Wave 1 (八王子学園八王子高等学校, school 11/11) CANDIDATE data.

Eleventh and final school of the powerhouse-school expansion initiative
(see docs/BATCH_008_PROPOSAL.md). 八王子学園八王子高等学校 has no
existing Organization ID -- newly minted here as ORG000209.

Discovery: B.LEAGUE's "ワタシノB.LEAGUE" tag list for
TagID=35:八王子学園八王子高等学校 was accessed directly. It shows
exactly 1 current alumnus (多田武史) -- no "もっと見る" pagination
needed. This is genuinely new to the project. Single player, single
wave (final wave of the initiative).

Per the batch's approved scope, only the current club is registered as
Pro career (minimal path); prior clubs are logged as PRO_HISTORY_GAPS
issues.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_018" / "wave_01"
CHECKED_AT = "2026-09-25"

PERSONS = [
    {"person_id": "P000192", "name": "多田 武史"},
]

# ORG000031(拓殖大学)・ORG000101(鹿児島レブナイズ) は既存Organization
# として再利用 -- master + 全candidateのorganization_candidates.csvと
# 突き合わせ済み。八王子学園八王子高等学校は新規登録（現在の最大既存
# Organization IDはORG000208、batch_017のため ORG000209 とした）。
ORGANIZATIONS = [
    {"organization_id": "ORG000209", "name": "八王子学園八王子高等学校"},
    {"organization_id": "ORG000031", "name": "拓殖大学"},
    {"organization_id": "ORG000101", "name": "鹿児島レブナイズ"},
]

CAREERS = [
    # 多田武史（現所属は鹿児島レブナイズ、2025-26〜。過去の秋田ノーザン
    # ハピネッツ・福島ファイヤーボンズ在籍はissue参照）
    {"career_id": "C000629", "person_id": "P000192", "organization_id": "ORG000209", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000630", "person_id": "P000192", "organization_id": "ORG000031", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000631", "person_id": "P000192", "organization_id": "ORG000101", "role": "Player", "start": "2025", "end": ""},
]

SOURCES = [
    {"source_id": "B18W1S0001", "title": "ワタシノB.LEAGUE選手一覧 | 八王子学園八王子高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:八王子学園八王子高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B18W1S0002", "title": "多田武史 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=30457", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B18W1E{_evidence_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "field_name": field_name,
        "candidate_value": candidate_value,
        "source_id": source_id,
        "source_locator": source_locator,
        "evidence_summary": evidence_summary,
        "assessment": assessment,
        "checked_at": CHECKED_AT,
        "issue_note": issue_note,
    })


# --- 多田武史 ---
add_evidence("Person", "P000192", "name", "多田 武史", "B18W1S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000192", "birth_date", "1997-11-25", "B18W1S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000629", "organization_id", "ORG000209", "B18W1S0002", "基本情報 > 出身校（高）：八王子学園八王子高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000630", "organization_id", "ORG000031", "B18W1S0002", "基本情報 > 出身校（大）：拓殖大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000631", "organization_id", "ORG000101", "B18W1S0002", "クラブ経歴 > 「2025-26：鹿児島」が最新（新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="秋田ノーザンハピネッツ（2019-20〜2022-23、4シーズン）・福島ファイヤーボンズ（2023-24〜2024-25、2シーズン）在籍は今回のWaveでは対象外。詳細はissue B18W1I0003を参照")
add_evidence("Career", "C000631", "start", "2025", "B18W1S0002", "クラブ経歴 > 「2025-26：鹿児島」が最新", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B18W1D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


for pid, cids in [
    ("P000192", ["C000629", "C000630", "C000631"]),
]:
    add_decision("Person", pid, "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
    add_decision("Career", cids[0], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[1], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[2], "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去クラブ在籍はissueに記録")

ISSUES = [
    {"issue_id": "B18W1I0001", "person_id": "P000192", "related_id": "C000629", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "多田武史の八王子学園八王子高等学校在籍そのものはB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月は資料に記載がなく未確認。",
     "next_check": "B.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B18W1I0002", "person_id": "P000192", "related_id": "C000630", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "多田武史の大学在籍そのものはB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月は資料に記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B18W1I0003", "person_id": "P000192", "related_id": "P000192", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "多田武史は現所属（鹿児島レブナイズ、2025-26〜、新規加入）以前に秋田ノーザンハピネッツ（2019-20〜2022-23、4シーズン）・福島ファイヤーボンズ（2023-24〜2024-25、2シーズン）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
]


def main() -> None:
    write_csv(BASE / "person_candidates.csv", ["person_id", "name"], PERSONS)
    write_csv(BASE / "organization_candidates.csv", ["organization_id", "name"], ORGANIZATIONS)
    write_csv(BASE / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], CAREERS)
    write_csv(BASE / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], SOURCES)
    write_csv(BASE / "evidence_records.csv", [
        "record_id", "entity_type", "entity_id", "field_name", "candidate_value",
        "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note",
    ], EVIDENCE)
    write_csv(BASE / "issues.csv", [
        "issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check",
    ], ISSUES)
    write_csv(BASE / "qa_decisions.csv", [
        "decision_id", "entity_type", "entity_id", "decision",
        "eligible_fields", "held_fields", "reason", "reviewed_at",
    ], DECISIONS)
    print(
        f"Wrote batch_018/wave_01: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
