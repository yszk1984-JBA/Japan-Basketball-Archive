#!/usr/bin/env python3
"""Build Batch 014 Wave 2 (北陸高等学校, school 7/11) CANDIDATE data.

Wave 2 of 4 for 北陸高等学校 (see build_batch_014_wave_01.py for the
school-level discovery notes). This wave covers 松山駿, 松本健児リオン,
二上耀, 中村ジャズ.

富山大学(ORG000197)・名古屋経済大学(ORG000198)は新規登録（現在の最大既存
Organization IDはORG000196、batch_013 wave_02のため、この2件を
ORG000197-198とした）。国士舘大学は新規登録（ORG000203、下記の表記
ゆれの注記を参照）。

表記ゆれの注記：中村ジャズのB.LEAGUE公式プロフィールでは出身大学が
「国士館大学」（舘ではなく館）と表記されているが、同じ北陸高等学校出身の
寺嶋恭之介（Wave 3で登録予定）のプロフィールでは正しく「国士舘大学」
（舘）と表記されている。実在する大学の正式名称は「国士舘大学」（舘）で
あり、中村ジャズのプロフィール側の表記はB.LEAGUE公式サイト側の誤記と
判断し、正式名称で登録した（同一の実在組織を表記ゆれで複数IDに分裂させ
ないため）。この判断根拠はevidence_records.csvのissue_noteに明記する。

Notable: 松山駿・二上耀はいずれも今回のWaveで初めて対象クラブに加入した
ケース（過去に在籍歴のない、genuinely新規のクラブ）であり、藤澤尚之
（batch_013）や野本建吾（Wave 1）のような「復帰」ではない。中村ジャズは
在籍記録が断続的（2019-20 東京EX, 2020-21〜2022-23の記載なし, 2023-24
茨城, 2025-26の記載なし, 2024-25 長崎, 2026-27 岩手）で、今回のWaveでは
現所属クラブのみを最小経路として登録し、過去の断続的な経歴全体を1件の
PRO_HISTORY_GAPS issueにまとめて記録した。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_014" / "wave_02"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000169", "name": "松山 駿"},
    {"person_id": "P000170", "name": "松本 健児リオン"},
    {"person_id": "P000171", "name": "二上 耀"},
    {"person_id": "P000172", "name": "中村 ジャズ"},
]

# ORG000120（北陸高等学校）・ORG000122（川崎ブレイブサンダース）・
# ORG000166（筑波大学）・ORG000173（岩手ビッグブルズ）は既存Organizationと
# して再利用。ORG000135（長崎ヴェルカ）も既存。富山大学・名古屋経済大学・
# 国士舘大学は新規登録（ORG000197〜000198、000203）。
ORGANIZATIONS = [
    {"organization_id": "ORG000120", "name": "北陸高等学校"},
    {"organization_id": "ORG000197", "name": "富山大学"},
    {"organization_id": "ORG000122", "name": "川崎ブレイブサンダース"},
    {"organization_id": "ORG000198", "name": "名古屋経済大学"},
    {"organization_id": "ORG000135", "name": "長崎ヴェルカ"},
    {"organization_id": "ORG000166", "name": "筑波大学"},
    {"organization_id": "ORG000097", "name": "三遠ネオフェニックス"},
    {"organization_id": "ORG000203", "name": "国士舘大学"},
    {"organization_id": "ORG000173", "name": "岩手ビッグブルズ"},
]

CAREERS = [
    # 松山駿（現所属は川崎ブレイブサンダース、2026-27〜。過去在籍歴のない
    # 新規加入。富山・FE名古屋・越谷在籍はissue参照）
    {"career_id": "C000560", "person_id": "P000169", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000561", "person_id": "P000169", "organization_id": "ORG000197", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000562", "person_id": "P000169", "organization_id": "ORG000122", "role": "Player", "start": "2026", "end": ""},
    # 松本健児リオン（現所属は長崎ヴェルカ、2021-22〜継続。西宮・奈良在籍
    # および2020-21の空白はissue参照）
    {"career_id": "C000563", "person_id": "P000170", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000564", "person_id": "P000170", "organization_id": "ORG000198", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000565", "person_id": "P000170", "organization_id": "ORG000135", "role": "Player", "start": "2021", "end": ""},
    # 二上耀（現所属は三遠ネオフェニックス、2026-27〜。過去在籍歴のない
    # 新規加入。千葉ジェッツ在籍はissue参照）
    {"career_id": "C000566", "person_id": "P000171", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000567", "person_id": "P000171", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000568", "person_id": "P000171", "organization_id": "ORG000097", "role": "Player", "start": "2026", "end": ""},
    # 中村ジャズ（現所属は岩手ビッグブルズ、2026-27〜。断続的な過去経歴は
    # issue参照）
    {"career_id": "C000569", "person_id": "P000172", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000570", "person_id": "P000172", "organization_id": "ORG000203", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000571", "person_id": "P000172", "organization_id": "ORG000173", "role": "Player", "start": "2026", "end": ""},
]

SOURCES = [
    {"source_id": "B14W2S0001", "title": "松山駿 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=20023", "accessed_at": CHECKED_AT},
    {"source_id": "B14W2S0002", "title": "松本健児リオン 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=10893", "accessed_at": CHECKED_AT},
    {"source_id": "B14W2S0003", "title": "二上耀 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000112", "accessed_at": CHECKED_AT},
    {"source_id": "B14W2S0004", "title": "中村ジャズ 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=30510", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B14W2E{_evidence_seq:04d}",
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


# --- 松山駿 ---
add_evidence("Person", "P000169", "name", "松山 駿", "B14W2S0001", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000169", "birth_date", "1996-09-27", "B14W2S0001", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000560", "organization_id", "ORG000120", "B14W2S0001", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000561", "organization_id", "ORG000197", "B14W2S0001", "基本情報 > 出身校（大）：富山大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000562", "organization_id", "ORG000122", "B14W2S0001", "クラブ経歴 > 「2026-27：川崎」が最新（新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="富山（2018-19・2019-20）、FE名古屋（2019-20一部・2020-21）、越谷（2021-22〜2025-26）在籍は今回のWaveでは対象外。詳細はissue B14W2I0003を参照")
add_evidence("Career", "C000562", "start", "2026", "B14W2S0001", "クラブ経歴 > 「2026-27：川崎」が最新", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの加入を確認", "SUPPORTED")

# --- 松本健児リオン ---
add_evidence("Person", "P000170", "name", "松本 健児リオン", "B14W2S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000170", "birth_date", "1994-05-30", "B14W2S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000563", "organization_id", "ORG000120", "B14W2S0002", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000564", "organization_id", "ORG000198", "B14W2S0002", "基本情報 > 出身校（大）：名古屋経済大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000565", "organization_id", "ORG000135", "B14W2S0002", "クラブ経歴 > 「2021-22：長崎」以降継続", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="西宮（2016-17、現・神戸ストークスの前身の可能性があるが未確認）、奈良（2017-18〜2019-20）在籍、および2020-21シーズンの記載空白は今回のWaveでは対象外。詳細はissue B14W2I0004を参照")
add_evidence("Career", "C000565", "start", "2021", "B14W2S0002", "クラブ経歴 > 「2021-22：長崎」が初出", "B.LEAGUE公式のクラブ所属履歴で2021-22シーズンからの加入を確認", "SUPPORTED")

# --- 二上耀 ---
add_evidence("Person", "P000171", "name", "二上 耀", "B14W2S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000171", "birth_date", "1999-04-13", "B14W2S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000566", "organization_id", "ORG000120", "B14W2S0003", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000567", "organization_id", "ORG000166", "B14W2S0003", "基本情報 > 出身校（大）：筑波大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000568", "organization_id", "ORG000097", "B14W2S0003", "クラブ経歴 > 「2026-27：三遠」が最新（新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="千葉ジェッツ（2021-22〜2025-26）在籍は今回のWaveでは対象外。詳細はissue B14W2I0005を参照")
add_evidence("Career", "C000568", "start", "2026", "B14W2S0003", "クラブ経歴 > 「2026-27：三遠」が最新", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの加入を確認", "SUPPORTED")

# --- 中村ジャズ ---
add_evidence("Person", "P000172", "name", "中村 ジャズ", "B14W2S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000172", "birth_date", "1997-06-18", "B14W2S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000569", "organization_id", "ORG000120", "B14W2S0004", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000570", "organization_id", "ORG000203", "B14W2S0004", "基本情報 > 出身校（大）：国士舘大学（本人プロフィールは「国士館大学」と表記されているが、同校出身の他選手のプロフィールでの正しい表記および実在大学の正式名称に基づき「国士舘大学」として登録）", "B.LEAGUE公式プロフィールで出身大学を確認（表記ゆれあり）", "PARTIAL")
add_evidence("Career", "C000571", "organization_id", "ORG000173", "B14W2S0004", "クラブ経歴 > 「2026-27：岩手」が最新（新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="東京エクセレンス（2019-20）、茨城（2023-24）、長崎（2024-25）在籍、および複数シーズンの記載空白は今回のWaveでは対象外。詳細はissue B14W2I0006を参照")
add_evidence("Career", "C000571", "start", "2026", "B14W2S0004", "クラブ経歴 > 「2026-27：岩手」が最新", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B14W2D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


for pid, cids in [
    ("P000169", ["C000560", "C000561", "C000562"]),
    ("P000170", ["C000563", "C000564", "C000565"]),
    ("P000171", ["C000566", "C000567", "C000568"]),
    ("P000172", ["C000569", "C000570", "C000571"]),
]:
    add_decision("Person", pid, "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
    add_decision("Career", cids[0], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[1], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[2], "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去クラブ在籍はissueに記録")

ISSUES = [
    {"issue_id": "B14W2I0001", "person_id": "P000169|P000170|P000171|P000172", "related_id": "C000560|C000563|C000566|C000569", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "4名とも北陸高等学校在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B14W2I0002", "person_id": "P000169|P000170|P000171|P000172", "related_id": "C000561|C000564|C000567|C000570", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "4名とも大学在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B14W2I0003", "person_id": "P000169", "related_id": "P000169", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "松山駿は現所属（川崎ブレイブサンダース、2026-27〜、新規加入）以前に富山（2018-19・2019-20）、FE名古屋（2019-20の一部・2020-21）、越谷アルファーズ（2021-22〜2025-26）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B14W2I0004", "person_id": "P000170", "related_id": "P000170", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "松本健児リオンは現所属（長崎ヴェルカ、2021-22〜）以前に西宮（2016-17、現在の神戸ストークスの前身クラブの可能性があるが名称変更の経緯は未確認）、奈良（2017-18〜2019-20）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。加えて2020-21シーズンの記載が同履歴に一切なく、空白理由は資料からは確認できず憶測で埋めていない。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加するとともに、西宮→現クラブの組織同一性、および2020-21シーズンの空白理由を追加情報源で確認"},
    {"issue_id": "B14W2I0005", "person_id": "P000171", "related_id": "P000171", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "二上耀は現所属（三遠ネオフェニックス、2026-27〜、新規加入）以前に千葉ジェッツ（2021-22〜2025-26）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B14W2I0006", "person_id": "P000172", "related_id": "P000172", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "中村ジャズは現所属（岩手ビッグブルズ、2026-27〜、新規加入）以前に東京エクセレンス（2019-20）、茨城ロボッツ（2023-24）、長崎ヴェルカ（2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、記録が断続的（複数シーズンで記載空白）であり、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブおよび空白シーズンは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加するとともに、断続的な在籍記録の背景（移籍空白・登録外等）を追加情報源で確認"},
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
        f"Wrote batch_014/wave_02: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
