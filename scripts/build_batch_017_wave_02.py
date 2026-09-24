#!/usr/bin/env python3
"""Build Batch 017 Wave 2 (土浦日本大学高等学校, school 10/11) CANDIDATE data.

Second and final wave of school 10 (see build_batch_017_wave_01.py for
discovery notes). Wave 2 covers the remaining 2 alumni: 陳岡燈生,
平岩玄.

Notable: 陳岡燈生（本Wave）と陳岡流羽（Wave 1）は同姓・同じ出身地
（茨城県）だが、近親関係を示す一次資料は確認できていないため、関係に
ついては一切記録せず、README側に観察メモとしてのみ残す（Governanceの
「AIは未知の情報を推測しない」原則に基づく）。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_017" / "wave_02"
CHECKED_AT = "2026-09-25"

PERSONS = [
    {"person_id": "P000190", "name": "陳岡 燈生"},
    {"person_id": "P000191", "name": "平岩 玄"},
]

# ORG000134(土浦日本大学高等学校)・ORG000121(日本大学)・
# ORG000015(東海大学)・ORG000181(山形ワイヴァンズ)・
# ORG000109(アルバルク東京) は既存Organizationとして再利用 -- master +
# 全candidateのorganization_candidates.csvと突き合わせ済み。本Waveでの
# 新規Organizationはなし。
ORGANIZATIONS = [
    {"organization_id": "ORG000134", "name": "土浦日本大学高等学校"},
    {"organization_id": "ORG000121", "name": "日本大学"},
    {"organization_id": "ORG000181", "name": "山形ワイヴァンズ"},
    {"organization_id": "ORG000015", "name": "東海大学"},
    {"organization_id": "ORG000109", "name": "アルバルク東京"},
]

CAREERS = [
    # 陳岡燈生（現所属は山形ワイヴァンズ、2025-26〜。過去の越谷アルファーズ・
    # 静岡在籍はissue参照）
    {"career_id": "C000623", "person_id": "P000190", "organization_id": "ORG000134", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000624", "person_id": "P000190", "organization_id": "ORG000121", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000625", "person_id": "P000190", "organization_id": "ORG000181", "role": "Player", "start": "2025", "end": ""},
    # 平岩玄（現所属はアルバルク東京、2018-19〜。過去の琉球ゴールデン
    # キングス在籍はissue参照）
    {"career_id": "C000626", "person_id": "P000191", "organization_id": "ORG000134", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000627", "person_id": "P000191", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000628", "person_id": "P000191", "organization_id": "ORG000109", "role": "Player", "start": "2018", "end": ""},
]

SOURCES = [
    {"source_id": "B17W2S0001", "title": "陳岡燈生 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000373", "accessed_at": CHECKED_AT},
    {"source_id": "B17W2S0002", "title": "平岩玄 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=15838", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B17W2E{_evidence_seq:04d}",
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


# --- 陳岡燈生 ---
add_evidence("Person", "P000190", "name", "陳岡 燈生", "B17W2S0001", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000190", "birth_date", "2001-08-28", "B17W2S0001", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000623", "organization_id", "ORG000134", "B17W2S0001", "基本情報 > 出身校（高）：土浦日本大学高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000624", "organization_id", "ORG000121", "B17W2S0001", "基本情報 > 出身校（大）：日本大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000625", "organization_id", "ORG000181", "B17W2S0001", "クラブ経歴 > 「2025-26：山形」が初出（現所属への新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="越谷アルファーズ（2023-24）・「静岡」（2024-25、B.LEAGUE公式の略称表記のみで正式クラブ名未確認。B3所属の「ベルテックス静岡」の可能性があるが本Waveでは確定情報として扱わない）在籍は今回のWaveでは対象外。詳細はissue B17W2I0003を参照")
add_evidence("Career", "C000625", "start", "2025", "B17W2S0001", "クラブ経歴 > 「2025-26：山形」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 平岩玄 ---
add_evidence("Person", "P000191", "name", "平岩 玄", "B17W2S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000191", "birth_date", "1997-12-05", "B17W2S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000626", "organization_id", "ORG000134", "B17W2S0002", "基本情報 > 出身校（高）：土浦日本大学高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000627", "organization_id", "ORG000015", "B17W2S0002", "基本情報 > 出身校（大）：東海大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000628", "organization_id", "ORG000109", "B17W2S0002", "クラブ経歴 > 「2018-19：A東京」が初出（現所属への新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="琉球ゴールデンキングス（2017-18、1シーズン）在籍は今回のWaveでは対象外。詳細はissue B17W2I0004を参照")
add_evidence("Career", "C000628", "start", "2018", "B17W2S0002", "クラブ経歴 > 「2018-19：A東京」が初出", "B.LEAGUE公式のクラブ所属履歴で2018-19シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B17W2D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


for pid, cids in [
    ("P000190", ["C000623", "C000624", "C000625"]),
    ("P000191", ["C000626", "C000627", "C000628"]),
]:
    add_decision("Person", pid, "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
    add_decision("Career", cids[0], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[1], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[2], "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去クラブ在籍はissueに記録")

ISSUES = [
    {"issue_id": "B17W2I0001", "person_id": "P000190|P000191", "related_id": "C000623|C000626", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "2名とも土浦日本大学高等学校在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B17W2I0002", "person_id": "P000190|P000191", "related_id": "C000624|C000627", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "2名とも大学在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B17W2I0003", "person_id": "P000190", "related_id": "P000190", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "陳岡燈生は現所属（山形ワイヴァンズ、2025-26〜、新規加入）以前に越谷アルファーズ（2023-24、1シーズン）・「静岡」（2024-25、1シーズン。B.LEAGUE公式のクラブ所属履歴では略称表記のみで正式クラブ名は本Waveでは未確認）でのプロ経歴が確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "「静岡」の正式クラブ名を確認のうえ、後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B17W2I0004", "person_id": "P000191", "related_id": "P000191", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "平岩玄は現所属（アルバルク東京、2018-19〜、新規加入）以前に琉球ゴールデンキングス（2017-18、1シーズン）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
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
        f"Wrote batch_017/wave_02: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
