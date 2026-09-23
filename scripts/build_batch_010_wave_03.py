#!/usr/bin/env python3
"""Build Batch 010 Wave 3 (洛南高等学校 3/4) CANDIDATE data.

Continues wave_01/wave_02's coverage of 洛南高等学校's 19 not-yet-registered
current B.LEAGUE alumni. This wave covers 6 more: 大庭岳輝, 伊藤達哉,
津屋一球, 小川敦也, 小林遥太, 伊藤良太.

Same discovery source and conventions as wave_01/wave_02 (TagID=35:
洛南高等学校 tag list; minimum Career chain only, high school ->
university -> CURRENT club; historical pro clubs excluded and logged as
PRO_HISTORY_GAPS; "名古屋D" (名古屋ダイヤモンドドルフィンズ, ORG000054) is
NOT the same club as ファイティングイーグルス名古屋, per wave_01's finding
-- relevant again here for 伊藤達哉's history).

津屋一球's current club history shows a non-contiguous return (三遠
2020-22, then SR渋谷 2022-24, then back to 三遠 2024-27): per the
same-club-return convention established elsewhere in this project (cf.
納見悠仁/石川海斗 in batch_009), the Career start is recorded as 2024
(the CURRENT continuous stint), not his original 2020 debut.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_010" / "wave_03"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000146", "name": "大庭 岳輝"},
    {"person_id": "P000147", "name": "伊藤 達哉"},
    {"person_id": "P000148", "name": "津屋 一球"},
    {"person_id": "P000149", "name": "小川 敦也"},
    {"person_id": "P000150", "name": "小林 遥太"},
    {"person_id": "P000151", "name": "伊藤 良太"},
]

# ORG000119 (洛南高等学校), ORG000015 (東海大学), ORG000110 (広島ドラゴン
# フライズ), ORG000097 (三遠ネオフェニックス), ORG000166 (筑波大学),
# ORG000047 (宇都宮ブレックス), ORG000030 (青山学院大学), ORG000040
# (ライジングゼファー福岡), ORG000185 (慶應義塾大学), ORG000050 (ウォルガ
# 湘南) already exist and are reused -- checked against master + every
# candidate organization_candidates.csv before writing this file. 京都
# 産業大学・越谷アルファーズ confirmed genuinely new; current max existing
# Organization ID is ORG000187 (batch_010/wave_02), so these are
# ORG000188 and ORG000190 (ORG000189 reserved for 中京大学 in wave_04,
# assigned in registration order across the two waves' drafting).
ORGANIZATIONS = [
    {"organization_id": "ORG000119", "name": "洛南高等学校"},
    {"organization_id": "ORG000188", "name": "京都産業大学"},
    {"organization_id": "ORG000190", "name": "越谷アルファーズ"},
    {"organization_id": "ORG000015", "name": "東海大学"},
    {"organization_id": "ORG000110", "name": "広島ドラゴンフライズ"},
    {"organization_id": "ORG000097", "name": "三遠ネオフェニックス"},
    {"organization_id": "ORG000166", "name": "筑波大学"},
    {"organization_id": "ORG000047", "name": "宇都宮ブレックス"},
    {"organization_id": "ORG000030", "name": "青山学院大学"},
    {"organization_id": "ORG000040", "name": "ライジングゼファー福岡"},
    {"organization_id": "ORG000185", "name": "慶應義塾大学"},
    {"organization_id": "ORG000050", "name": "ウォルガ湘南"},
]

CAREERS = [
    # 大庭岳輝
    {"career_id": "C000493", "person_id": "P000146", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000494", "person_id": "P000146", "organization_id": "ORG000188", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000495", "person_id": "P000146", "organization_id": "ORG000190", "role": "Player", "start": "2025", "end": ""},
    # 伊藤達哉
    {"career_id": "C000496", "person_id": "P000147", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000497", "person_id": "P000147", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000498", "person_id": "P000147", "organization_id": "ORG000110", "role": "Player", "start": "2025", "end": ""},
    # 津屋一球（現在の連続在籍はstart=2024からの2回目の三遠在籍）
    {"career_id": "C000499", "person_id": "P000148", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000500", "person_id": "P000148", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000501", "person_id": "P000148", "organization_id": "ORG000097", "role": "Player", "start": "2024", "end": ""},
    # 小川敦也（現所属クラブがB.LEAGUEデビュー先）
    {"career_id": "C000502", "person_id": "P000149", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000503", "person_id": "P000149", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000504", "person_id": "P000149", "organization_id": "ORG000047", "role": "Player", "start": "2022", "end": ""},
    # 小林遥太
    {"career_id": "C000505", "person_id": "P000150", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000506", "person_id": "P000150", "organization_id": "ORG000030", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000507", "person_id": "P000150", "organization_id": "ORG000040", "role": "Player", "start": "2026", "end": ""},
    # 伊藤良太
    {"career_id": "C000508", "person_id": "P000151", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000509", "person_id": "P000151", "organization_id": "ORG000185", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000510", "person_id": "P000151", "organization_id": "ORG000050", "role": "Player", "start": "2026", "end": ""},
]

SOURCES = [
    {"source_id": "B10W3S0001", "title": "ワタシノB.LEAGUE選手一覧 | 洛南高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:洛南高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B10W3S0002", "title": "大庭岳輝 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=30401", "accessed_at": CHECKED_AT},
    {"source_id": "B10W3S0003", "title": "伊藤達哉 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=10849", "accessed_at": CHECKED_AT},
    {"source_id": "B10W3S0004", "title": "津屋一球 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=5100000011", "accessed_at": CHECKED_AT},
    {"source_id": "B10W3S0005", "title": "小川敦也 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000228", "accessed_at": CHECKED_AT},
    {"source_id": "B10W3S0006", "title": "小林遥太 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8462", "accessed_at": CHECKED_AT},
    {"source_id": "B10W3S0007", "title": "伊藤良太 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=9234", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B10W3E{_evidence_seq:04d}",
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


# --- 大庭岳輝 ---
add_evidence("Person", "P000146", "name", "大庭 岳輝", "B10W3S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000146", "birth_date", "1997-07-29", "B10W3S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000493", "organization_id", "ORG000119", "B10W3S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000494", "organization_id", "ORG000188", "B10W3S0001", "選手カード > 出身校：京都産業大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000495", "organization_id", "ORG000190", "B10W3S0002", "クラブ経歴 > 「2025-26：越谷」が初出（前年まで横浜BC）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000495", "start", "2025", "B10W3S0002", "クラブ経歴 > 「2025-26：越谷」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 伊藤達哉 ---
add_evidence("Person", "P000147", "name", "伊藤 達哉", "B10W3S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000147", "birth_date", "1994-11-26", "B10W3S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000496", "organization_id", "ORG000119", "B10W3S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000497", "organization_id", "ORG000015", "B10W3S0001", "選手カード > 出身校：東海大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000498", "organization_id", "ORG000110", "B10W3S0003", "クラブ経歴 > 「2025-26以降：広島」（前年まで琉球）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000498", "start", "2025", "B10W3S0003", "クラブ経歴 > 「2025-26：広島」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 津屋一球 ---
add_evidence("Person", "P000148", "name", "津屋 一球", "B10W3S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000148", "birth_date", "1998-06-07", "B10W3S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000499", "organization_id", "ORG000119", "B10W3S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000500", "organization_id", "ORG000015", "B10W3S0001", "選手カード > 出身校：東海大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000501", "organization_id", "ORG000097", "B10W3S0004", "クラブ経歴 > 「2024-25：三遠」が再登場（2020-21〜2021-22も三遠、間の2022-23〜2023-24はSR渋谷）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="2020-21〜2021-22シーズンにも一度三遠に在籍しており、2022-23〜2023-24のSR渋谷在籍を挟んだ復帰である点に留意")
add_evidence("Career", "C000501", "start", "2024", "B10W3S0004", "クラブ経歴 > 「2024-25：三遠」が再登場（今回の復帰）", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの現在の在籍開始を確認", "SUPPORTED")

# --- 小川敦也 ---
add_evidence("Person", "P000149", "name", "小川 敦也", "B10W3S0005", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000149", "birth_date", "2002-06-24", "B10W3S0005", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000502", "organization_id", "ORG000119", "B10W3S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000503", "organization_id", "ORG000166", "B10W3S0001", "選手カード > 出身校：筑波大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000504", "organization_id", "ORG000047", "B10W3S0005", "クラブ経歴 > 「2022-23：宇都宮」が初出（唯一の記載）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000504", "start", "2022", "B10W3S0005", "クラブ経歴 > 「2022-23：宇都宮」が初出", "B.LEAGUE公式のクラブ所属履歴で2022-23シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 小林遥太 ---
add_evidence("Person", "P000150", "name", "小林 遥太", "B10W3S0006", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000150", "birth_date", "1991-09-12", "B10W3S0006", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000505", "organization_id", "ORG000119", "B10W3S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000506", "organization_id", "ORG000030", "B10W3S0001", "選手カード > 出身校：青山学院大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000507", "organization_id", "ORG000040", "B10W3S0006", "クラブ経歴 > 「2026-27：福岡」が初出（唯一の記載、前年まで奈良）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000507", "start", "2026", "B10W3S0006", "クラブ経歴 > 「2026-27：福岡」が初出", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの加入を確認", "SUPPORTED")

# --- 伊藤良太 ---
add_evidence("Person", "P000151", "name", "伊藤 良太", "B10W3S0007", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000151", "birth_date", "1992-07-23", "B10W3S0007", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000508", "organization_id", "ORG000119", "B10W3S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000509", "organization_id", "ORG000185", "B10W3S0001", "選手カード > 出身校：慶應義塾大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000510", "organization_id", "ORG000050", "B10W3S0007", "クラブ経歴 > 「2026-27：湘南」が初出（唯一の記載、前年は愛媛）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000510", "start", "2026", "B10W3S0007", "クラブ経歴 > 「2026-27：湘南」が初出", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B10W3D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000146", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000493", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000494", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000495", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000147", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000496", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000497", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000498", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000148", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000499", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000500", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000501", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認（2回目の三遠在籍として登録）、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000149", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000502", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000503", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000504", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000150", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000505", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000506", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000507", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000151", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000508", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000509", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000510", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

ISSUES = [
    {"issue_id": "B10W3I0001", "person_id": "P000146|P000147|P000148|P000149|P000150|P000151", "related_id": "C000493|C000496|C000499|C000502|C000505|C000508", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "6名とも洛南高等学校在籍そのものは出身校タグ一覧で確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B10W3I0002", "person_id": "P000146|P000147|P000148|P000149|P000150|P000151", "related_id": "C000494|C000497|C000500|C000503|C000506|C000509", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "6名とも大学在籍そのものは出身校タグ一覧の選手カードで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B10W3I0003", "person_id": "P000146", "related_id": "P000146", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "大庭岳輝は現所属（越谷アルファーズ、2025-26〜）以前に京都ハンナリーズ（ORG000042、2019-20〜2020-21）、横浜ビー・コルセアーズ（ORG000055、2021-22〜2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B10W3I0004", "person_id": "P000147", "related_id": "P000147", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "伊藤達哉は現所属（広島ドラゴンフライズ、2025-26〜）以前に京都ハンナリーズ（ORG000042、2017-18〜2018-19）、大阪エヴェッサ（ORG000142、2019-20〜2020-21）、名古屋ダイヤモンドドルフィンズ（ORG000054、2021-22〜2023-24、ファイティングイーグルス名古屋とは別クラブ。wave_01の発見事項を参照）、琉球ゴールデンキングス（ORG000106、2024-25）と4クラブにまたがる長いプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加（クラブ数が多く優先度を検討）"},
    {"issue_id": "B10W3I0005", "person_id": "P000150", "related_id": "P000150", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "小林遥太は現所属（ライジングゼファー福岡、2026-27〜）以前に滋賀レイクス（ORG000153、2016-17〜2017-18）、名古屋ダイヤモンドドルフィンズ（ORG000054、2018-19〜2021-22、ファイティングイーグルス名古屋とは別クラブ）、仙台89ERS（ORG000132、2022-23〜2023-24）、バンビシャス奈良（ORG000171、2024-25〜2025-26）と4クラブにまたがる長いプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加（クラブ数が多く優先度を検討）"},
    {"issue_id": "B10W3I0006", "person_id": "P000151", "related_id": "P000151", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "伊藤良太は現所属（ウォルガ湘南、2026-27〜）以前に岐阜スゥープス（2018-19、Organization ID未確認）、岩手ビッグブルズ（ORG000173、2019-20〜2021-22）、しながわシティバスケットボールクラブ（ORG000174、2023-24〜2024-25）、愛媛オレンジバイキングス（ORG000091、2025-26）と極めて多くのクラブを渡り歩く経歴がB.LEAGUE公式のクラブ所属履歴で確認できる（2016-17には「東京海上日動」という記載もあるが、これはB.LEAGUE発足前の実業団チームである可能性が高くOrganizationとしての登録要否は未検討）が、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加（岐阜スゥープスのOrganization ID確認、「東京海上日動」のB.LEAGUE登録要否の検討を含む）"},
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
        f"Wrote batch_010/wave_03: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
