#!/usr/bin/env python3
"""Build Batch 012 Wave 1 (延岡学園高等学校, school 5/11) CANDIDATE data.

Fifth school of the powerhouse-school expansion initiative (see
docs/BATCH_008_PROPOSAL.md). 延岡学園高等学校 (Miyazaki) has no existing
Organization ID -- newly minted here as ORG000194.

Discovery: B.LEAGUE's "ワタシノB.LEAGUE" tag list for
TagID=35:延岡学園高等学校
(https://www.bleague.jp/mybleague_list/?TagID=35:延岡学園高等学校) worked
directly this time (no need to reverse-engineer via an individual
profile page, since the URL pattern discovered in batch_011 could be
constructed straight away). It shows exactly 1 current alumnus --
榎田拓真 -- no "もっと見る" pagination needed. He is genuinely new to the
project (checked against data/master/person.csv and every existing
person_candidates.csv).

Per the batch's approved scope (docs/BATCH_008_PROPOSAL.md), only the
current club is registered as Pro career (minimal path: high school ->
university (if any) -> current club); prior clubs found in his
クラブ所属履歴 are logged as a PRO_HISTORY_GAPS issue instead of being
added as Career rows, matching the convention used throughout
batch_008-011.

Notable: his B.LEAGUE公式クラブ所属履歴 lists 2022-23 長崎, 2023-24 長崎,
2024-25 越谷, then jumps to 2026-27 山口 with no 2025-26 entry at all --
an apparent gap season with no explanation on the official profile. Not
guessed at; recorded as part of the PRO_HISTORY_GAPS issue rather than
assumed to be an inactive/injury year.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_012" / "wave_01"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000156", "name": "榎田 拓真"},
]

# ORG000100 (山口パッツファイブ、Master既存) と ORG000148 (近畿大学、
# batch_007で登録済み) は既存Organizationとして再利用 -- master +
# 全candidateのorganization_candidates.csvと突き合わせ済み。延岡学園高等
# 学校は新規で、現在の最大既存Organization IDはORG000193（batch_011）の
# ため ORG000194 とした。
ORGANIZATIONS = [
    {"organization_id": "ORG000194", "name": "延岡学園高等学校"},
    {"organization_id": "ORG000148", "name": "近畿大学"},
    {"organization_id": "ORG000100", "name": "山口パッツファイブ"},
]

CAREERS = [
    # 榎田拓真（現所属は山口パッツファイブ、2026-27〜。それ以前の長崎・
    # 越谷在籍および2025-26の空白シーズンはissue参照）
    {"career_id": "C000522", "person_id": "P000156", "organization_id": "ORG000194", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000523", "person_id": "P000156", "organization_id": "ORG000148", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000524", "person_id": "P000156", "organization_id": "ORG000100", "role": "Player", "start": "2026", "end": ""},
]

SOURCES = [
    {"source_id": "B12W1S0001", "title": "ワタシノB.LEAGUE選手一覧 | 延岡学園高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:延岡学園高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B12W1S0002", "title": "榎田拓真 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000177", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B12W1E{_evidence_seq:04d}",
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


# --- 榎田拓真 ---
add_evidence("Person", "P000156", "name", "榎田 拓真", "B12W1S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000156", "birth_date", "1998-05-22", "B12W1S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000522", "organization_id", "ORG000194", "B12W1S0001", "TagID=35（延岡学園高等学校）掲載選手一覧 > 出身高校：延岡学園高等学校", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000523", "organization_id", "ORG000148", "B12W1S0002", "基本情報 > 出身校：近畿大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000524", "organization_id", "ORG000100", "B12W1S0002", "クラブ経歴 > 「2026-27：山口」が最新", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="それ以前（2022-23〜2024-25）の長崎・越谷在籍、および2025-26の空白シーズンは今回のWaveでは対象外。詳細はissue B12W1I0003を参照")
add_evidence("Career", "C000524", "start", "2026", "B12W1S0002", "クラブ経歴 > 「2026-27：山口」が最新", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B12W1D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000156", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000522", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000523", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000524", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去クラブ在籍・空白シーズンはissueに記録")

ISSUES = [
    {"issue_id": "B12W1I0001", "person_id": "P000156", "related_id": "C000522", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "延岡学園高等学校在籍そのものは出身校タグ一覧で確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "本人のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B12W1I0002", "person_id": "P000156", "related_id": "C000523", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "近畿大学在籍そのものは本人のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B12W1I0003", "person_id": "P000156", "related_id": "P000156", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "榎田拓真は現所属（山口パッツファイブ、2026-27〜）以前に長崎（2022-23〜2023-24）、越谷（2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。加えて、同履歴には2025-26シーズンの記載が一切なく（2024-25越谷の次が2026-27山口）、空白シーズンの理由（移籍空白・登録外・怪我等）は資料からは不明であり、憶測で埋めていない。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加するとともに、2025-26シーズンの空白理由を追加情報源（クラブ公式・報道等）で確認"},
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
        f"Wrote batch_012/wave_01: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
