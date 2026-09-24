#!/usr/bin/env python3
"""Build Batch 015 Wave 2 (藤枝明誠高等学校, school 8/11, final wave) CANDIDATE data.

Second and final wave for 藤枝明誠高等学校 (6 alumni total; see
build_batch_015_wave_01.py for Wave 1 and the school-level discovery
notes). This wave covers 角野亮伍, 赤間賢人 (2 people, below the
standard 4/wave size since this is the school's last wave).

サザンニューハンプシャー大学(ORG000206)は新規登録（現在の最大既存
Organization IDはORG000205、Wave 1のためORG000206とした）。米国
Southern New Hampshire Universityの日本語表記。

Notable: 赤間賢人のB.LEAGUE公式プロフィールの関連動画に「特別指定の
大学生プレーヤー」との言及があり、大学在学中の特別指定選手制度での
起用の可能性を示唆しているが、契約形態の詳細は資料からは確認できず、
Careerデータへの反映（特別な扱い）は行っていない（通常のPlayer roleとして
登録）。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_015" / "wave_02"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000184", "name": "角野 亮伍"},
    {"person_id": "P000185", "name": "赤間 賢人"},
]

# ORG000204（藤枝明誠高等学校）はWave 1で新規登録済みのため再利用。
# ORG000130（シーホース三河）・ORG000015（東海大学）・ORG000103
# （茨城ロボッツ）は既存Organizationとして再利用。サザンニューハンプ
# シャー大学は新規登録（ORG000206）。
ORGANIZATIONS = [
    {"organization_id": "ORG000204", "name": "藤枝明誠高等学校"},
    {"organization_id": "ORG000206", "name": "サザンニューハンプシャー大学"},
    {"organization_id": "ORG000130", "name": "シーホース三河"},
    {"organization_id": "ORG000015", "name": "東海大学"},
    {"organization_id": "ORG000103", "name": "茨城ロボッツ"},
]

CAREERS = [
    # 角野亮伍（現所属はシーホース三河、2021-22〜継続。旧大阪在籍は
    # issue参照）
    {"career_id": "C000605", "person_id": "P000184", "organization_id": "ORG000204", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000606", "person_id": "P000184", "organization_id": "ORG000206", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000607", "person_id": "P000184", "organization_id": "ORG000130", "role": "Player", "start": "2021", "end": ""},
    # 赤間賢人（B.LEAGUEデビューから一貫して茨城ロボッツ、移籍・空白なし）
    {"career_id": "C000608", "person_id": "P000185", "organization_id": "ORG000204", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000609", "person_id": "P000185", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000610", "person_id": "P000185", "organization_id": "ORG000103", "role": "Player", "start": "2025", "end": ""},
]

SOURCES = [
    {"source_id": "B15W2S0001", "title": "角野亮伍 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=32982", "accessed_at": CHECKED_AT},
    {"source_id": "B15W2S0002", "title": "赤間賢人 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000583", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B15W2E{_evidence_seq:04d}",
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


# --- 角野亮伍 ---
add_evidence("Person", "P000184", "name", "角野 亮伍", "B15W2S0001", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000184", "birth_date", "1996-06-14", "B15W2S0001", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000605", "organization_id", "ORG000204", "B15W2S0001", "基本情報 > 出身校（高）：藤枝明誠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000606", "organization_id", "ORG000206", "B15W2S0001", "基本情報 > 出身校（大）：サザンニューハンプシャー大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000607", "organization_id", "ORG000130", "B15W2S0001", "クラブ経歴 > 「2021-22：三河」以降継続", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="大阪エヴェッサ（2020-21）在籍は今回のWaveでは対象外。詳細はissue B15W2I0003を参照")
add_evidence("Career", "C000607", "start", "2021", "B15W2S0001", "クラブ経歴 > 「2021-22：三河」が初出", "B.LEAGUE公式のクラブ所属履歴で2021-22シーズンからの加入を確認", "SUPPORTED")

# --- 赤間賢人 ---
add_evidence("Person", "P000185", "name", "赤間 賢人", "B15W2S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000185", "birth_date", "2005-06-19", "B15W2S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000608", "organization_id", "ORG000204", "B15W2S0002", "基本情報 > 出身校（高）：藤枝明誠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000609", "organization_id", "ORG000015", "B15W2S0002", "基本情報 > 出身校（大）：東海大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000610", "organization_id", "ORG000103", "B15W2S0002", "クラブ経歴 > 「2025-26：茨城」が初出（唯一の在籍クラブ）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000610", "start", "2025", "B15W2S0002", "クラブ経歴 > 「2025-26：茨城」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B15W2D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


for pid, cids in [
    ("P000184", ["C000605", "C000606", "C000607"]),
    ("P000185", ["C000608", "C000609", "C000610"]),
]:
    add_decision("Person", pid, "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
    add_decision("Career", cids[0], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[1], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[2], "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

ISSUES = [
    {"issue_id": "B15W2I0001", "person_id": "P000184|P000185", "related_id": "C000605|C000608", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "2名とも藤枝明誠高等学校在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B15W2I0002", "person_id": "P000184|P000185", "related_id": "C000606|C000609", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "2名とも大学在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスター、または米国大学側の記録での裏付けを確認"},
    {"issue_id": "B15W2I0003", "person_id": "P000184", "related_id": "P000184", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "角野亮伍は現所属（シーホース三河、2021-22〜）以前に大阪エヴェッサ（2020-21）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
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
        f"Wrote batch_015/wave_02: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
