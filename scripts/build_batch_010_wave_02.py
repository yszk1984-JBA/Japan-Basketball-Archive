#!/usr/bin/env python3
"""Build Batch 010 Wave 2 (洛南高等学校 2/4) CANDIDATE data.

Continues wave_01's coverage of 洛南高等学校's 19 not-yet-registered
current B.LEAGUE alumni. This wave covers 6 more: 淺野ケニー, 飯尾文哉,
谷口大智, 寺嶋良, 谷口光貴, 大橋大空.

Same discovery source and conventions as wave_01 (TagID=35:洛南高等学校
tag list; minimum Career chain only, high school -> university ->
CURRENT club; historical pro clubs excluded and logged as PRO_HISTORY_GAPS).

大橋大空's B.LEAGUE profile club-history data has an apparent gap (no
2024-25 entry between his 2023-24 島根 stint and 2025-26 横浜エクセレンス
stint) -- recorded start=2025 based on available data, with the gap
itself flagged rather than guessed at.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_010" / "wave_02"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000140", "name": "淺野 ケニー"},
    {"person_id": "P000141", "name": "飯尾 文哉"},
    {"person_id": "P000142", "name": "谷口 大智"},
    {"person_id": "P000143", "name": "寺嶋 良"},
    {"person_id": "P000144", "name": "谷口 光貴"},
    {"person_id": "P000145", "name": "大橋 大空"},
]

# ORG000119 (洛南高等学校), ORG000018 (専修大学), ORG000121 (日本大学),
# ORG000155 (島根スサノオマジック), ORG000015 (東海大学), ORG000110
# (広島ドラゴンフライズ), ORG000016 (中央大学), ORG000040 (ライジングゼファー
# 福岡), ORG000143 (群馬クレインサンダーズ), ORG000090 (横浜エクセレンス)
# already exist and are reused -- checked against master + every candidate
# organization_candidates.csv before writing this file. サウスイースタン・
# オクラホマ州立大学・ブルーフィールド州立大学 confirmed genuinely new
# (US universities); current max existing Organization ID is ORG000185
# (batch_010/wave_01), so these are ORG000186 and ORG000187.
ORGANIZATIONS = [
    {"organization_id": "ORG000119", "name": "洛南高等学校"},
    {"organization_id": "ORG000018", "name": "専修大学"},
    {"organization_id": "ORG000143", "name": "群馬クレインサンダーズ"},
    {"organization_id": "ORG000121", "name": "日本大学"},
    {"organization_id": "ORG000155", "name": "島根スサノオマジック"},
    {"organization_id": "ORG000186", "name": "サウスイースタン・オクラホマ州立大学"},
    {"organization_id": "ORG000015", "name": "東海大学"},
    {"organization_id": "ORG000110", "name": "広島ドラゴンフライズ"},
    {"organization_id": "ORG000016", "name": "中央大学"},
    {"organization_id": "ORG000040", "name": "ライジングゼファー福岡"},
    {"organization_id": "ORG000187", "name": "ブルーフィールド州立大学"},
    {"organization_id": "ORG000090", "name": "横浜エクセレンス"},
]

CAREERS = [
    # 淺野ケニー
    {"career_id": "C000475", "person_id": "P000140", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000476", "person_id": "P000140", "organization_id": "ORG000018", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000477", "person_id": "P000140", "organization_id": "ORG000143", "role": "Player", "start": "2024", "end": ""},
    # 飯尾文哉
    {"career_id": "C000478", "person_id": "P000141", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000479", "person_id": "P000141", "organization_id": "ORG000121", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000480", "person_id": "P000141", "organization_id": "ORG000155", "role": "Player", "start": "2025", "end": ""},
    # 谷口大智
    {"career_id": "C000481", "person_id": "P000142", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000482", "person_id": "P000142", "organization_id": "ORG000186", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000483", "person_id": "P000142", "organization_id": "ORG000143", "role": "Player", "start": "2025", "end": ""},
    # 寺嶋良
    {"career_id": "C000484", "person_id": "P000143", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000485", "person_id": "P000143", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000486", "person_id": "P000143", "organization_id": "ORG000110", "role": "Player", "start": "2021", "end": ""},
    # 谷口光貴
    {"career_id": "C000487", "person_id": "P000144", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000488", "person_id": "P000144", "organization_id": "ORG000016", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000489", "person_id": "P000144", "organization_id": "ORG000040", "role": "Player", "start": "2026", "end": ""},
    # 大橋大空
    {"career_id": "C000490", "person_id": "P000145", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000491", "person_id": "P000145", "organization_id": "ORG000187", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000492", "person_id": "P000145", "organization_id": "ORG000090", "role": "Player", "start": "2025", "end": ""},
]

SOURCES = [
    {"source_id": "B10W2S0001", "title": "ワタシノB.LEAGUE選手一覧 | 洛南高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:洛南高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B10W2S0002", "title": "淺野ケニー 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000232", "accessed_at": CHECKED_AT},
    {"source_id": "B10W2S0003", "title": "飯尾文哉 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000113", "accessed_at": CHECKED_AT},
    {"source_id": "B10W2S0004", "title": "谷口大智 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8470", "accessed_at": CHECKED_AT},
    {"source_id": "B10W2S0005", "title": "寺嶋良 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=30400", "accessed_at": CHECKED_AT},
    {"source_id": "B10W2S0006", "title": "谷口光貴 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8488", "accessed_at": CHECKED_AT},
    {"source_id": "B10W2S0007", "title": "大橋大空 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000274", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B10W2E{_evidence_seq:04d}",
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


# --- 淺野ケニー ---
add_evidence("Person", "P000140", "name", "淺野 ケニー", "B10W2S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000140", "birth_date", "2002-08-16", "B10W2S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000475", "organization_id", "ORG000119", "B10W2S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000476", "organization_id", "ORG000018", "B10W2S0001", "選手カード > 出身校：専修大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000477", "organization_id", "ORG000143", "B10W2S0002", "クラブ経歴 > 「2024-25：群馬」が初出（前年は三遠、その前は京都）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000477", "start", "2024", "B10W2S0002", "クラブ経歴 > 「2024-25：群馬」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入を確認", "SUPPORTED")

# --- 飯尾文哉 ---
add_evidence("Person", "P000141", "name", "飯尾 文哉", "B10W2S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000141", "birth_date", "2000-06-10", "B10W2S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000478", "organization_id", "ORG000119", "B10W2S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000479", "organization_id", "ORG000121", "B10W2S0001", "選手カード > 出身校：日本大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000480", "organization_id", "ORG000155", "B10W2S0003", "クラブ経歴 > 「2025-26：島根」が初出（前年まで大阪）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000480", "start", "2025", "B10W2S0003", "クラブ経歴 > 「2025-26：島根」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 谷口大智 ---
add_evidence("Person", "P000142", "name", "谷口 大智", "B10W2S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000142", "birth_date", "1990-04-15", "B10W2S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000481", "organization_id", "ORG000119", "B10W2S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000482", "organization_id", "ORG000186", "B10W2S0001", "選手カード > 出身校：サウスイースタン・オクラホマ州立大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学（米国）を確認", "SUPPORTED")
add_evidence("Career", "C000483", "organization_id", "ORG000143", "B10W2S0004", "クラブ経歴 > 「2025-26：群馬」が初出（前年まで島根）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000483", "start", "2025", "B10W2S0004", "クラブ経歴 > 「2025-26：群馬」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 寺嶋良 ---
add_evidence("Person", "P000143", "name", "寺嶋 良", "B10W2S0005", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000143", "birth_date", "1997-10-23", "B10W2S0005", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000484", "organization_id", "ORG000119", "B10W2S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000485", "organization_id", "ORG000015", "B10W2S0001", "選手カード > 出身校：東海大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000486", "organization_id", "ORG000110", "B10W2S0005", "クラブ経歴 > 「2021-22以降：広島」（前年まで京都）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000486", "start", "2021", "B10W2S0005", "クラブ経歴 > 「2021-22：広島」が初出", "B.LEAGUE公式のクラブ所属履歴で2021-22シーズンからの加入を確認", "SUPPORTED")

# --- 谷口光貴 ---
add_evidence("Person", "P000144", "name", "谷口 光貴", "B10W2S0006", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000144", "birth_date", "1992-12-18", "B10W2S0006", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000487", "organization_id", "ORG000119", "B10W2S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000488", "organization_id", "ORG000016", "B10W2S0001", "選手カード > 出身校：中央大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000489", "organization_id", "ORG000040", "B10W2S0006", "クラブ経歴 > 「2026-27：福岡」が初出（今回の復帰。前年は横浜BC、その前も福岡）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="2023-24〜2024-25シーズンにも一度福岡に在籍しており、2025-26シーズンの横浜BC在籍を挟んだ復帰である点に留意")
add_evidence("Career", "C000489", "start", "2026", "B10W2S0006", "クラブ経歴 > 「2026-27：福岡」が初出（今回の復帰）", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの現在の在籍開始を確認", "SUPPORTED")

# --- 大橋大空 ---
add_evidence("Person", "P000145", "name", "大橋 大空", "B10W2S0007", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000145", "birth_date", "1999-04-05", "B10W2S0007", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000490", "organization_id", "ORG000119", "B10W2S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000491", "organization_id", "ORG000187", "B10W2S0001", "選手カード > 出身校：ブルーフィールド州立大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学（米国）を確認", "SUPPORTED")
add_evidence("Career", "C000492", "organization_id", "ORG000090", "B10W2S0007", "クラブ経歴 > 「2025-26：横浜エクセレンス」（前は2023-24島根）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="B.LEAGUE公式のクラブ所属履歴には2024-25シーズンの記載がなく、2023-24（島根）と2025-26（横浜エクセレンス）の間にデータの欠落がある可能性がある。start=2025は取得できたデータに基づく推定であり、2024-25シーズンの所属は未確認")

DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B10W2D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000140", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000475", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000476", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000477", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000141", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000478", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000479", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000480", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000142", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000481", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000482", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000483", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000143", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000484", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000485", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000486", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000144", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000487", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000488", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000489", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去にも同クラブに在籍していた点はissueに記録")

add_decision("Person", "P000145", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000490", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000491", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000492", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。2024-25シーズンのデータ欠落はissueに記録")

ISSUES = [
    {"issue_id": "B10W2I0001", "person_id": "P000140|P000141|P000142|P000143|P000144|P000145", "related_id": "C000475|C000478|C000481|C000484|C000487|C000490", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "6名とも洛南高等学校在籍そのものは出身校タグ一覧で確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B10W2I0002", "person_id": "P000140|P000141|P000142|P000143|P000144|P000145", "related_id": "C000476|C000479|C000482|C000485|C000488|C000491", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "6名とも大学在籍そのものは出身校タグ一覧の選手カードで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B10W2I0003", "person_id": "P000140", "related_id": "P000140", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "淺野ケニーは現所属（群馬クレインサンダーズ、2024-25〜）以前に京都ハンナリーズ（ORG000042、2022-23）、三遠ネオフェニックス（ORG000097、2023-24）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B10W2I0004", "person_id": "P000141", "related_id": "P000141", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "飯尾文哉は現所属（島根スサノオマジック、2025-26〜）以前に大阪エヴェッサ（ORG000142、2021-22〜2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B10W2I0005", "person_id": "P000142", "related_id": "P000142", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "谷口大智は現所属（群馬クレインサンダーズ、2025-26〜）以前に秋田ノーザンハピネッツ（ORG000137、2016-17〜2018-19）、広島ドラゴンフライズ（ORG000110、2019-20〜2020-21）、茨城ロボッツ（ORG000103、2021-22）、島根スサノオマジック（ORG000155、2022-23〜2024-25）と4クラブにまたがる長いプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加（クラブ数が多く優先度を検討）"},
    {"issue_id": "B10W2I0006", "person_id": "P000143", "related_id": "P000143", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "寺嶋良は現所属（広島ドラゴンフライズ、2021-22〜）以前に京都ハンナリーズ（ORG000042、2019-20〜2020-21）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B10W2I0007", "person_id": "P000144", "related_id": "P000144", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "谷口光貴は現所属（ライジングゼファー福岡、2026-27〜、2回目の復帰）以前に川崎ブレイブサンダース（ORG000122、2016-17〜2018-19）、滋賀レイクス（ORG000153、2019-20〜2020-21）、香川ファイブアローズ（2020-21〜2021-22、Organization ID未確認）、熊本ヴォルターズ（ORG000067、2022-23）、1回目の福岡在籍（2023-24〜2024-25）、横浜ビー・コルセアーズ（ORG000055、2025-26）と、極めて多くのクラブを渡り歩く複雑な経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加（クラブ数が特に多く優先度を検討。香川ファイブアローズのOrganization ID確認を含む）"},
    {"issue_id": "B10W2I0008", "person_id": "P000145", "related_id": "C000492", "issue_type": "DATA_QUALITY_NOTE", "status": "HOLD",
     "description": "大橋大空のB.LEAGUE公式クラブ所属履歴には2024-25シーズンの記載が見当たらず、2023-24（島根スサノオマジック、ORG000155）と2025-26（横浜エクセレンス）の間にデータの欠落がある可能性がある。start=2025として登録したが、2024-25シーズンの実際の所属（あるいは同シーズンの空白の理由）は未確認。",
     "next_check": "2024-25シーズンの所属を別ソースで確認"},
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
        f"Wrote batch_010/wave_02: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
