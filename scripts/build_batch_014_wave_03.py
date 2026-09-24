#!/usr/bin/env python3
"""Build Batch 014 Wave 3 (北陸高等学校, school 7/11) CANDIDATE data.

Wave 3 of 4 for 北陸高等学校 (see build_batch_014_wave_01.py for the
school-level discovery notes). This wave covers 寺嶋恭之介, 岡田泰希,
藤永佳昭, 篠山竜青.

明星大学(ORG000199)・福井ブローウィンズ(ORG000200)は新規登録（現在の
最大既存Organization IDはORG000198、Wave 2のため、この2件を
ORG000199-200とした）。国士舘大学(ORG000203)はWave 2で新規登録済みの
ため再利用（寺嶋恭之介のプロフィールでは正しい表記「国士舘大学」（舘）
で記載されている）。

Notable: 篠山竜青は2016-17シーズンのB.LEAGUE初年度から2026-27シーズン
まで一貫して川崎ブレイブサンダース一筋（11シーズン、クラブ移籍・空白
シーズンなし）というこの校のWave中最もシンプルな経歴で、PRO_HISTORY_
GAPS issueは不要（現所属クラブのCareer開始年をそのままデビュー年の
2016年とした）。藤永佳昭は逆に北陸高等学校出身選手の中でも特に長く
複雑な経歴（名古屋D→千葉→千葉J→A東京→秋田→富山→福井と7クラブ）を
持つ。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_014" / "wave_03"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000173", "name": "寺嶋 恭之介"},
    {"person_id": "P000174", "name": "岡田 泰希"},
    {"person_id": "P000175", "name": "藤永 佳昭"},
    {"person_id": "P000176", "name": "篠山 竜青"},
]

# ORG000120（北陸高等学校）・ORG000203（国士舘大学、Wave 2で新規登録済み）・
# ORG000182（青森ワッツ）・ORG000153（滋賀レイクス）・ORG000015（東海大学）・
# ORG000121（日本大学）・ORG000122（川崎ブレイブサンダース）は既存として
# 再利用。明星大学・福井ブローウィンズは新規登録（ORG000199-200）。
ORGANIZATIONS = [
    {"organization_id": "ORG000120", "name": "北陸高等学校"},
    {"organization_id": "ORG000203", "name": "国士舘大学"},
    {"organization_id": "ORG000182", "name": "青森ワッツ"},
    {"organization_id": "ORG000199", "name": "明星大学"},
    {"organization_id": "ORG000153", "name": "滋賀レイクス"},
    {"organization_id": "ORG000015", "name": "東海大学"},
    {"organization_id": "ORG000200", "name": "福井ブローウィンズ"},
    {"organization_id": "ORG000121", "name": "日本大学"},
    {"organization_id": "ORG000122", "name": "川崎ブレイブサンダース"},
]

CAREERS = [
    # 寺嶋恭之介（現所属は青森ワッツ、2020-21〜継続、途中2021-22の記載
    # 空白あり。issue参照）
    {"career_id": "C000572", "person_id": "P000173", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000573", "person_id": "P000173", "organization_id": "ORG000203", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000574", "person_id": "P000173", "organization_id": "ORG000182", "role": "Player", "start": "2020", "end": ""},
    # 岡田泰希（現所属は滋賀レイクス、2024-25〜継続。愛媛・仙台在籍は
    # issue参照）
    {"career_id": "C000575", "person_id": "P000174", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000576", "person_id": "P000174", "organization_id": "ORG000199", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000577", "person_id": "P000174", "organization_id": "ORG000153", "role": "Player", "start": "2024", "end": ""},
    # 藤永佳昭（現所属は福井ブローウィンズ、2026-27〜。過去在籍歴のない
    # 新規加入。名古屋D・千葉・千葉J・A東京・秋田・富山在籍はissue参照）
    {"career_id": "C000578", "person_id": "P000175", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000579", "person_id": "P000175", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000580", "person_id": "P000175", "organization_id": "ORG000200", "role": "Player", "start": "2026", "end": ""},
    # 篠山竜青（B.LEAGUE初年度2016-17から一貫して川崎ブレイブサンダース、
    # 移籍・空白なし）
    {"career_id": "C000581", "person_id": "P000176", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000582", "person_id": "P000176", "organization_id": "ORG000121", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000583", "person_id": "P000176", "organization_id": "ORG000122", "role": "Player", "start": "2016", "end": ""},
]

SOURCES = [
    {"source_id": "B14W3S0001", "title": "寺嶋恭之介 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=32985", "accessed_at": CHECKED_AT},
    {"source_id": "B14W3S0002", "title": "岡田泰希 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=22401", "accessed_at": CHECKED_AT},
    {"source_id": "B14W3S0003", "title": "藤永佳昭 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8736", "accessed_at": CHECKED_AT},
    {"source_id": "B14W3S0004", "title": "篠山竜青 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8484", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B14W3E{_evidence_seq:04d}",
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


# --- 寺嶋恭之介 ---
add_evidence("Person", "P000173", "name", "寺嶋 恭之介", "B14W3S0001", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000173", "birth_date", "1991-10-17", "B14W3S0001", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000572", "organization_id", "ORG000120", "B14W3S0001", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000573", "organization_id", "ORG000203", "B14W3S0001", "基本情報 > 出身校（大）：国士舘大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000574", "organization_id", "ORG000182", "B14W3S0001", "クラブ経歴 > 「2020-21：青森」以降一貫して青森", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="2021-22シーズンの記載が同履歴に一切なく、空白理由は資料からは確認できず憶測で埋めていない。詳細はissue B14W3I0003を参照")
add_evidence("Career", "C000574", "start", "2020", "B14W3S0001", "クラブ経歴 > 「2020-21：青森」が初出", "B.LEAGUE公式のクラブ所属履歴で2020-21シーズンからの加入を確認", "SUPPORTED")

# --- 岡田泰希 ---
add_evidence("Person", "P000174", "name", "岡田 泰希", "B14W3S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000174", "birth_date", "1999-07-28", "B14W3S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000575", "organization_id", "ORG000120", "B14W3S0002", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000576", "organization_id", "ORG000199", "B14W3S0002", "基本情報 > 出身校（大）：明星大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000577", "organization_id", "ORG000153", "B14W3S0002", "クラブ経歴 > 「2024-25：滋賀」以降継続", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="愛媛（2018-19〜2020-21）、仙台89ERS（2021-22〜2023-24）在籍は今回のWaveでは対象外。詳細はissue B14W3I0004を参照")
add_evidence("Career", "C000577", "start", "2024", "B14W3S0002", "クラブ経歴 > 「2024-25：滋賀」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入を確認", "SUPPORTED")

# --- 藤永佳昭 ---
add_evidence("Person", "P000175", "name", "藤永 佳昭", "B14W3S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000175", "birth_date", "1992-04-10", "B14W3S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000578", "organization_id", "ORG000120", "B14W3S0003", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000579", "organization_id", "ORG000015", "B14W3S0003", "基本情報 > 出身校（大）：東海大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000580", "organization_id", "ORG000200", "B14W3S0003", "クラブ経歴 > 「2026-27：福井」が最新（新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="名古屋ダイヤモンドドルフィンズ（2016-17・2017-18）、千葉（2018-19・2019-20）、千葉ジェッツ（2020-21・2021-22）、アルバルク東京（2022-23）、秋田（2023-24）、富山（2024-25・2025-26）在籍は今回のWaveでは対象外。詳細はissue B14W3I0005を参照")
add_evidence("Career", "C000580", "start", "2026", "B14W3S0003", "クラブ経歴 > 「2026-27：福井」が最新", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの加入を確認", "SUPPORTED")

# --- 篠山竜青 ---
add_evidence("Person", "P000176", "name", "篠山 竜青", "B14W3S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000176", "birth_date", "1988-07-20", "B14W3S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000581", "organization_id", "ORG000120", "B14W3S0004", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000582", "organization_id", "ORG000121", "B14W3S0004", "基本情報 > 出身校（大）：日本大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000583", "organization_id", "ORG000122", "B14W3S0004", "クラブ経歴 > 2016-17シーズン（B.LEAGUE初年度）から2026-27シーズンまで一貫して川崎", "B.LEAGUE公式のクラブ所属履歴でB.LEAGUE初年度から現在まで移籍なしの一貫した在籍を確認", "SUPPORTED")
add_evidence("Career", "C000583", "start", "2016", "B14W3S0004", "クラブ経歴 > 「2016-17：川崎」が初出（B.LEAGUE初年度）", "B.LEAGUE公式のクラブ所属履歴で2016-17シーズン（B.LEAGUEデビュー）からの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B14W3D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


for pid, cids in [
    ("P000173", ["C000572", "C000573", "C000574"]),
    ("P000174", ["C000575", "C000576", "C000577"]),
    ("P000175", ["C000578", "C000579", "C000580"]),
    ("P000176", ["C000581", "C000582", "C000583"]),
]:
    add_decision("Person", pid, "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
    add_decision("Career", cids[0], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[1], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[2], "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

ISSUES = [
    {"issue_id": "B14W3I0001", "person_id": "P000173|P000174|P000175|P000176", "related_id": "C000572|C000575|C000578|C000581", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "4名とも北陸高等学校在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B14W3I0002", "person_id": "P000173|P000174|P000175|P000176", "related_id": "C000573|C000576|C000579|C000582", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "4名とも大学在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B14W3I0003", "person_id": "P000173", "related_id": "P000173", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "寺嶋恭之介はB.LEAGUE公式のクラブ所属履歴上、2020-21シーズンから一貫して青森ワッツに在籍しているが、2021-22シーズンのみ記載が一切ない。移籍・登録外・怪我等いずれの理由かは資料からは確認できず、憶測で埋めていない。",
     "next_check": "2021-22シーズンの空白理由を追加情報源（クラブ公式・報道等）で確認"},
    {"issue_id": "B14W3I0004", "person_id": "P000174", "related_id": "P000174", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "岡田泰希は現所属（滋賀レイクス、2024-25〜）以前に愛媛オレンジバイキングス（2018-19〜2020-21）、仙台89ERS（2021-22〜2023-24）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B14W3I0005", "person_id": "P000175", "related_id": "P000175", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "藤永佳昭は現所属（福井ブローウィンズ、2026-27〜、新規加入）以前に名古屋ダイヤモンドドルフィンズ（2016-17・2017-18）、千葉（2018-19・2019-20）、千葉ジェッツ（2020-21・2021-22）、アルバルク東京（2022-23）、秋田ノーザンハピネッツ（2023-24）、富山グラウジーズ（2024-25・2025-26）と6クラブを渡り歩くプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
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
        f"Wrote batch_014/wave_03: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
