#!/usr/bin/env python3
"""Build Batch 014 Wave 4 (北陸高等学校, school 7/11, final wave) CANDIDATE data.

Fourth and final wave for 北陸高等学校 (15 alumni total; see
build_batch_014_wave_01.py for Waves 1 and the school-level discovery
notes). This wave covers 髙木慎哉, 下地秀一郎, 小川翔矢 (3 people, below
the standard 4/wave size since this is the school's last wave).

しながわシティバスケットボールクラブは既存Organization（ORG000174、
batch_006 wave_04で登録済み。当初「新規」と誤認しORG000201として仮登録
していたが、最終検証で重複が判明し既存IDに修正した）。福島ファイヤー
ボンズは新規登録（現在の最大既存Organization IDはORG000200、Wave 3の
ため、ORG000202とした）。

Notable: 下地秀一郎は北陸高等学校からしながわシティバスケットボール
クラブへ加入して以来（2025-26〜）移籍・空白なしの新人選手で、
PRO_HISTORY_GAPS issueは不要。小川翔矢は現所属（福島ファイヤーボンズ）
加入以前に「金沢」でのプロ経歴が1シーズンあるが、batch_011の小栗瑛哉の
ケースと同様、正式なクラブ名（金沢武士団とみられるが未確認）が今回は
未確認のためOrganization未登録とし、issueに記録した。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_014" / "wave_04"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000177", "name": "髙木 慎哉"},
    {"person_id": "P000178", "name": "下地 秀一郎"},
    {"person_id": "P000179", "name": "小川 翔矢"},
]

# ORG000120（北陸高等学校）・ORG000128（大東文化大学）・ORG000050（ウォルガ
# 湘南）・ORG000121（日本大学）・ORG000016（中央大学）・ORG000174（しながわ
# シティバスケットボールクラブ、既存）は既存Organizationとして再利用。
# 福島ファイヤーボンズは新規登録（ORG000202）。
ORGANIZATIONS = [
    {"organization_id": "ORG000120", "name": "北陸高等学校"},
    {"organization_id": "ORG000128", "name": "大東文化大学"},
    {"organization_id": "ORG000050", "name": "ウォルガ湘南"},
    {"organization_id": "ORG000121", "name": "日本大学"},
    {"organization_id": "ORG000174", "name": "しながわシティバスケットボールクラブ"},
    {"organization_id": "ORG000016", "name": "中央大学"},
    {"organization_id": "ORG000202", "name": "福島ファイヤーボンズ"},
]

CAREERS = [
    # 髙木慎哉（現所属はウォルガ湘南、2022-23〜継続。東京Z在籍はissue参照）
    {"career_id": "C000584", "person_id": "P000177", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000585", "person_id": "P000177", "organization_id": "ORG000128", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000586", "person_id": "P000177", "organization_id": "ORG000050", "role": "Player", "start": "2022", "end": ""},
    # 下地秀一郎（B.LEAGUEデビューから一貫してしながわシティバスケット
    # ボールクラブ、移籍・空白なし）
    {"career_id": "C000587", "person_id": "P000178", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000588", "person_id": "P000178", "organization_id": "ORG000121", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000589", "person_id": "P000178", "organization_id": "ORG000174", "role": "Player", "start": "2025", "end": ""},
    # 小川翔矢（現所属は福島ファイヤーボンズ、2025-26〜。金沢在籍はissue
    # 参照、正式クラブ名未確認のためOrganization未登録）
    {"career_id": "C000590", "person_id": "P000179", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000591", "person_id": "P000179", "organization_id": "ORG000016", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000592", "person_id": "P000179", "organization_id": "ORG000202", "role": "Player", "start": "2025", "end": ""},
]

SOURCES = [
    {"source_id": "B14W4S0001", "title": "髙木慎哉 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=30441", "accessed_at": CHECKED_AT},
    {"source_id": "B14W4S0002", "title": "下地秀一郎 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=52466", "accessed_at": CHECKED_AT},
    {"source_id": "B14W4S0003", "title": "小川翔矢 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=49607", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B14W4E{_evidence_seq:04d}",
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


# --- 髙木慎哉 ---
add_evidence("Person", "P000177", "name", "髙木 慎哉", "B14W4S0001", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000177", "birth_date", "1997-09-10", "B14W4S0001", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000584", "organization_id", "ORG000120", "B14W4S0001", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000585", "organization_id", "ORG000128", "B14W4S0001", "基本情報 > 出身校（大）：大東文化大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000586", "organization_id", "ORG000050", "B14W4S0001", "クラブ経歴 > 「2022-23：湘南」以降継続", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="アースフレンズ東京Z（2019-20〜2021-22）在籍は今回のWaveでは対象外。詳細はissue B14W4I0003を参照")
add_evidence("Career", "C000586", "start", "2022", "B14W4S0001", "クラブ経歴 > 「2022-23：湘南」が初出", "B.LEAGUE公式のクラブ所属履歴で2022-23シーズンからの加入を確認", "SUPPORTED")

# --- 下地秀一郎 ---
add_evidence("Person", "P000178", "name", "下地 秀一郎", "B14W4S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000178", "birth_date", "2003-04-07", "B14W4S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000587", "organization_id", "ORG000120", "B14W4S0002", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000588", "organization_id", "ORG000121", "B14W4S0002", "基本情報 > 出身校（大）：日本大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000589", "organization_id", "ORG000174", "B14W4S0002", "クラブ経歴 > 「2025-26：品川」が初出（唯一の在籍クラブ）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000589", "start", "2025", "B14W4S0002", "クラブ経歴 > 「2025-26：品川」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 小川翔矢 ---
add_evidence("Person", "P000179", "name", "小川 翔矢", "B14W4S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000179", "birth_date", "2002-10-13", "B14W4S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000590", "organization_id", "ORG000120", "B14W4S0003", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000591", "organization_id", "ORG000016", "B14W4S0003", "基本情報 > 出身校（大）：中央大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000592", "organization_id", "ORG000202", "B14W4S0003", "クラブ経歴 > 「2025-26：福島」が初出", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="2024-25シーズンの金沢在籍（正式クラブ名未確認、金沢武士団とみられる）は今回のWaveでは対象外。詳細はissue B14W4I0004を参照")
add_evidence("Career", "C000592", "start", "2025", "B14W4S0003", "クラブ経歴 > 「2025-26：福島」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B14W4D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


for pid, cids in [
    ("P000177", ["C000584", "C000585", "C000586"]),
    ("P000178", ["C000587", "C000588", "C000589"]),
    ("P000179", ["C000590", "C000591", "C000592"]),
]:
    add_decision("Person", pid, "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
    add_decision("Career", cids[0], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[1], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[2], "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

ISSUES = [
    {"issue_id": "B14W4I0001", "person_id": "P000177|P000178|P000179", "related_id": "C000584|C000587|C000590", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "3名とも北陸高等学校在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B14W4I0002", "person_id": "P000177|P000178|P000179", "related_id": "C000585|C000588|C000591", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "3名とも大学在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B14W4I0003", "person_id": "P000177", "related_id": "P000177", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "髙木慎哉は現所属（ウォルガ湘南、2022-23〜）以前にアースフレンズ東京Z（2019-20〜2021-22）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B14W4I0004", "person_id": "P000179", "related_id": "P000179", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "小川翔矢は現所属（福島ファイヤーボンズ、2025-26〜）以前に2024-25シーズンに「金沢」（金沢武士団とみられるが、正式クラブ名は今回未確認）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、金沢在籍はOrganization未登録のまま対象外とした（batch_011の小栗瑛哉と同様のケース）。",
     "next_check": "金沢の正式クラブ名を確認のうえ、後続の深掘りWaveでクラブ別Careerを追加"},
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
        f"Wrote batch_014/wave_04: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
