#!/usr/bin/env python3
"""Build Batch 008 Wave 3 (福岡大学附属大濠高等学校 3/4) CANDIDATE data.

Continues wave_01/wave_02's coverage of the school's 17 not-yet-registered
current B.LEAGUE alumni (out of 18 total on B.LEAGUE's TagID=35 listing;
金丸晃輔 already registered via batch_007/wave_02). This wave covers 6 more
(wave_01=4, wave_02=6, wave_03=6, wave_04=1 remaining: 島﨑輝).

Persons (checked against Master + every candidate/verified person file
before writing -- none previously registered):
- 木林優 (Yu Kibayashi, レバンガ北海道) -- his own B.LEAGUE roster page has
  no 学歴 (education) field at all; HS/Univ sourced from Wikipedia,
  corroborated for HS only by the TagID=35 official alumni tag list.
- 湧川颯斗 (Hayato Wakugawa, 三遠ネオフェニックス) -- no university; went
  straight from high school to pro (滋賀レイクス, then 三遠).
- 中田嵩基 (Shuki Nakata, 山形ワイヴァンズ)
- 平松克樹 (Katsuki Hiramatsu, ファイティングイーグルス名古屋)
- 岩下准平 (Junpei Iwashita, 滋賀レイクス) -- still 筑波大学 4年生 per news
  reports; original pro contract is with 長崎ヴェルカ, loaned to 滋賀 under
  the 育成契約選手制度 for the 2026-27 season (see issue B8W3I0007).
- 浅井修伍 (Shugo Asai, 青森ワッツ)

Same deliberate scope as wave_01/wave_02: minimum Career chain only (high
school -> university -> CURRENT club). Historical pro clubs before the
current one (木林優:長崎ヴェルカ, 湧川颯斗:滋賀レイクス, 中田嵩基:ライジング
ゼファー福岡, 浅井修伍:茨城ロボッツ) are deliberately excluded and logged
as individual PRO_HISTORY_GAPS issues, matching the batch_008/wave_01
precedent (B8W1I0003, B8W1I0004).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_008" / "wave_03"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000121", "name": "木林 優"},
    {"person_id": "P000122", "name": "湧川 颯斗"},
    {"person_id": "P000123", "name": "中田 嵩基"},
    {"person_id": "P000124", "name": "平松 克樹"},
    {"person_id": "P000125", "name": "岩下 准平"},
    {"person_id": "P000126", "name": "浅井 修伍"},
]

# ORG000127 (大濠), ORG000166 (筑波大学), ORG000092 (レバンガ北海道),
# ORG000097 (三遠ネオフェニックス), ORG000124 (明治大学), ORG000180
# (FE名古屋), ORG000153 (滋賀レイクス) already exist and are reused --
# checked against master + every candidate organization_candidates.csv
# before writing this file. 山形ワイヴァンズ・青森ワッツ confirmed genuinely
# new (not found anywhere in master or candidate data).
ORGANIZATIONS = [
    {"organization_id": "ORG000127", "name": "福岡大学附属大濠高等学校"},
    {"organization_id": "ORG000166", "name": "筑波大学"},
    {"organization_id": "ORG000092", "name": "レバンガ北海道"},
    {"organization_id": "ORG000097", "name": "三遠ネオフェニックス"},
    {"organization_id": "ORG000181", "name": "山形ワイヴァンズ"},
    {"organization_id": "ORG000124", "name": "明治大学"},
    {"organization_id": "ORG000180", "name": "ファイティングイーグルス名古屋"},
    {"organization_id": "ORG000153", "name": "滋賀レイクス"},
    {"organization_id": "ORG000182", "name": "青森ワッツ"},
]

CAREERS = [
    # 木林優
    {"career_id": "C000420", "person_id": "P000121", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000421", "person_id": "P000121", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000422", "person_id": "P000121", "organization_id": "ORG000092", "role": "Player", "start": "2025", "end": ""},
    # 湧川颯斗（大学なし）
    {"career_id": "C000423", "person_id": "P000122", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000424", "person_id": "P000122", "organization_id": "ORG000097", "role": "Player", "start": "2024", "end": ""},
    # 中田嵩基
    {"career_id": "C000425", "person_id": "P000123", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000426", "person_id": "P000123", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000427", "person_id": "P000123", "organization_id": "ORG000181", "role": "Player", "start": "2025", "end": ""},
    # 平松克樹
    {"career_id": "C000428", "person_id": "P000124", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000429", "person_id": "P000124", "organization_id": "ORG000124", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000430", "person_id": "P000124", "organization_id": "ORG000180", "role": "Player", "start": "2024", "end": ""},
    # 岩下准平
    {"career_id": "C000431", "person_id": "P000125", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000432", "person_id": "P000125", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000433", "person_id": "P000125", "organization_id": "ORG000153", "role": "Player", "start": "2025", "end": ""},
    # 浅井修伍
    {"career_id": "C000434", "person_id": "P000126", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000435", "person_id": "P000126", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000436", "person_id": "P000126", "organization_id": "ORG000182", "role": "Player", "start": "2025", "end": ""},
]

SOURCES = [
    {"source_id": "B8W3S0001", "title": "木林優 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000349", "accessed_at": CHECKED_AT},
    {"source_id": "B8W3S0002", "title": "木林優", "publisher": "Wikipedia", "url": "https://ja.wikipedia.org/wiki/%E6%9C%A8%E6%9E%97%E5%84%AA", "accessed_at": CHECKED_AT},
    {"source_id": "B8W3S0003", "title": "湧川颯斗 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000236", "accessed_at": CHECKED_AT},
    {"source_id": "B8W3S0004", "title": "中田嵩基 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000246", "accessed_at": CHECKED_AT},
    {"source_id": "B8W3S0005", "title": "平松克樹 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000443", "accessed_at": CHECKED_AT},
    {"source_id": "B8W3S0006", "title": "岩下准平 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000586", "accessed_at": CHECKED_AT},
    {"source_id": "B8W3S0007", "title": "浅井修伍 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000235", "accessed_at": CHECKED_AT},
    {"source_id": "B8W3S0008", "title": "ワタシノB.LEAGUE選手一覧 | 福岡大学附属大濠高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:福岡大学附属大濠高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B8W3S0009", "title": "滋賀レイクス、筑波大4年・岩下准平選手と契約 島根戦でプロデビュー", "publisher": "みんなの経済新聞ネットワーク（Yahoo!ニュース）", "url": "https://news.yahoo.co.jp/articles/4cc89ee36f835bab2dbbe9d0e3b41ec5302ebac3", "accessed_at": CHECKED_AT},
    {"source_id": "B8W3S0010", "title": "岩下准平選手 特別指定選手として加入および期限付移籍について", "publisher": "滋賀レイクス", "url": "https://shigalakes.com/news/detail/id=22082", "accessed_at": CHECKED_AT},
    {"source_id": "B8W3S0011", "title": "B2山形が福岡退団の中田嵩基を獲得「山形の攻撃的なスタイルでプレーできることがとても楽しみ」", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/japan/20250627/551529.html", "accessed_at": CHECKED_AT},
    {"source_id": "B8W3S0012", "title": "浅井修伍がB1茨城からB2青森に移籍「成長した姿を」新天地で飛躍誓う", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/japan/20250616/549475.html", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B8W3E{_evidence_seq:04d}",
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


# --- 木林優 ---
add_evidence("Person", "P000121", "name", "木林 優", "B8W3S0001", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000121", "birth_date", "2002-03-30", "B8W3S0001", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000420", "organization_id", "ORG000127", "B8W3S0002", "経歴 > 高校卒業後に筑波大学へ進学", "Wikipediaで出身高校を確認", "SUPPORTED",
             issue_note="本人のB.LEAGUE公式プロフィールページには学歴欄自体が存在しないため、Wikipediaを主ソースとした")
add_evidence("Career", "C000420", "organization_id", "ORG000127", "B8W3S0008", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000421", "organization_id", "ORG000166", "B8W3S0002", "経歴 > 高校卒業後に筑波大学へ進学", "Wikipediaで出身大学を確認", "SUPPORTED",
             issue_note="本人のB.LEAGUE公式プロフィールページには学歴欄自体が存在せず、B.LEAGUE公式での裏付けはとれていない")
add_evidence("Career", "C000422", "organization_id", "ORG000092", "B8W3S0001", "クラブ経歴 > 「2025-26：北海道」が初出（前年は長崎）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000422", "start", "2025", "B8W3S0001", "クラブ経歴 > 「2025-26：北海道」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 湧川颯斗 ---
add_evidence("Person", "P000122", "name", "湧川 颯斗", "B8W3S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000122", "birth_date", "2004-05-02", "B8W3S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000423", "organization_id", "ORG000127", "B8W3S0003", "学歴 > 出身校（高）：福岡大学附属大濠高校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000423", "organization_id", "ORG000127", "B8W3S0008", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000424", "organization_id", "ORG000097", "B8W3S0003", "クラブ経歴 > 「2024-25：三遠」が初出（前年は滋賀）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000424", "start", "2024", "B8W3S0003", "クラブ経歴 > 「2024-25：三遠」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入を確認", "SUPPORTED")

# --- 中田嵩基 ---
add_evidence("Person", "P000123", "name", "中田 嵩基", "B8W3S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000123", "birth_date", "2000-07-11", "B8W3S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000425", "organization_id", "ORG000127", "B8W3S0004", "学歴 > 出身校（高）：福岡大学附属大濠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000425", "organization_id", "ORG000127", "B8W3S0008", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000426", "organization_id", "ORG000166", "B8W3S0004", "学歴 > 出身校（大）：筑波大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000427", "organization_id", "ORG000181", "B8W3S0011", "本文 > 「B2山形が福岡退団の中田嵩基を獲得」", "B.LEAGUE媒体記事で山形ワイヴァンズへの加入を確認", "SUPPORTED")
add_evidence("Career", "C000427", "start", "2025", "B8W3S0011", "本文 > 2025年6月27日付記事、2025-26シーズンからの加入", "記事日付・B.LEAGUE公式のクラブ所属履歴（2025-26：山形が初出）で加入時期を確認", "SUPPORTED")

# --- 平松克樹 ---
add_evidence("Person", "P000124", "name", "平松 克樹", "B8W3S0005", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000124", "birth_date", "2002-04-25", "B8W3S0005", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000428", "organization_id", "ORG000127", "B8W3S0005", "学歴 > 出身校（高）：福岡大学附属大濠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000428", "organization_id", "ORG000127", "B8W3S0008", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000429", "organization_id", "ORG000124", "B8W3S0005", "学歴 > 出身校（大）：明治大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000430", "organization_id", "ORG000180", "B8W3S0005", "クラブ経歴 > 「2024-25：FE名古屋」が初出", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000430", "start", "2024", "B8W3S0005", "クラブ経歴 > 「2024-25：FE名古屋」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入を確認", "SUPPORTED")

# --- 岩下准平 ---
add_evidence("Person", "P000125", "name", "岩下 准平", "B8W3S0006", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000125", "birth_date", "2003-04-02", "B8W3S0006", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000431", "organization_id", "ORG000127", "B8W3S0008", "TagID=35（福岡大学附属大濠高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED",
             issue_note="本人のB.LEAGUE公式プロフィールページの出身校欄は空欄で、高校の記載がない")
add_evidence("Career", "C000432", "organization_id", "ORG000166", "B8W3S0009", "本文 > 「筑波大4年・岩下准平選手」", "報道（Yahoo!ニュース）で筑波大学在籍（4年生）を確認", "SUPPORTED",
             issue_note="本人のB.LEAGUE公式プロフィールページの出身校欄は空欄で、大学の記載がない")
add_evidence("Career", "C000433", "organization_id", "ORG000153", "B8W3S0006", "クラブ経歴 > 「2025-26：滋賀」が初出", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000433", "start", "2025", "B8W3S0006", "クラブ経歴 > 「2025-26：滋賀」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED",
             issue_note="原契約は長崎ヴェルカで、滋賀へは特別指定選手・育成契約選手制度による加入。詳細はissue B8W3I0007を参照")

# --- 浅井修伍 ---
add_evidence("Person", "P000126", "name", "浅井 修伍", "B8W3S0007", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000126", "birth_date", "2000-12-08", "B8W3S0007", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000434", "organization_id", "ORG000127", "B8W3S0007", "学歴 > 出身校（高）：福岡大学附属大濠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000434", "organization_id", "ORG000127", "B8W3S0008", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000435", "organization_id", "ORG000166", "B8W3S0007", "学歴 > 出身校（大）：筑波大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000436", "organization_id", "ORG000182", "B8W3S0012", "本文 > 「浅井修伍がB1茨城からB2青森に移籍」", "B.LEAGUE媒体記事で青森ワッツへの加入を確認", "SUPPORTED")
add_evidence("Career", "C000436", "start", "2025", "B8W3S0012", "本文 > 2025年6月16日付記事、2025-26シーズンからの加入", "記事日付・B.LEAGUE公式のクラブ所属履歴（2025-26：青森が初出）で加入時期を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B8W3D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000121", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000420", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipedia・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000421", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipediaのみで確認（本人のB.LEAGUE公式プロフィールには学歴欄なし）、在籍期間は未確認")
add_decision("Career", "C000422", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000122", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000423", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000424", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000123", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000425", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000426", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000427", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE媒体記事・公式クラブ所属履歴で確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000124", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000428", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000429", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000430", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000125", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000431", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認（本人プロフィールページの出身校欄は空欄）、在籍期間は未確認")
add_decision("Career", "C000432", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "報道（Yahoo!ニュース）で確認（本人プロフィールページの出身校欄は空欄）、在籍期間は未確認")
add_decision("Career", "C000433", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。原契約クラブ・育成契約選手制度の詳細はissueに記録")

add_decision("Person", "P000126", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000434", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000435", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000436", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE媒体記事・公式クラブ所属履歴で確認、現在進行中の契約のため終了日は未定")

ISSUES = [
    {"issue_id": "B8W3I0001", "person_id": "P000121|P000122|P000123|P000124|P000125|P000126", "related_id": "C000420|C000423|C000425|C000428|C000431|C000434", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "6名とも福岡大学附属大濠高等学校在籍そのものは複数ソースで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "高校公式または大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B8W3I0002", "person_id": "P000121|P000123|P000124|P000125|P000126", "related_id": "C000421|C000426|C000429|C000432|C000435", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "5名（湧川颯斗を除く、大学に進学していない）とも大学在籍そのものは確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B8W3I0003", "person_id": "P000121", "related_id": "P000121", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "木林優は現所属（レバンガ北海道、2025-26〜）以前に長崎ヴェルカ（2023年12月特別指定選手加入〜2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴・Wikipediaで確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B8W3I0004", "person_id": "P000122", "related_id": "P000122", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "湧川颯斗は現所属（三遠ネオフェニックス、2024-25〜）以前に滋賀レイクス（ORG000153、2022-23〜2023-24）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B8W3I0005", "person_id": "P000123", "related_id": "P000123", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "中田嵩基は現所属（山形ワイヴァンズ、2025-26〜）以前にライジングゼファー福岡（ORG000040、2022-23〜2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴・バスケットボールキング記事で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B8W3I0006", "person_id": "P000126", "related_id": "P000126", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "浅井修伍は現所属（青森ワッツ、2025-26〜）以前に茨城ロボッツ（ORG000103、2022-23〜2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴・バスケットボールキング記事で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B8W3I0007", "person_id": "P000125", "related_id": "C000433", "issue_type": "LOAN_STATUS", "status": "HOLD",
     "description": "岩下准平の滋賀レイクス在籍は、報道（滋賀レイクス公式・Yahoo!ニュース）によれば原契約は長崎ヴェルカ（ORG000135）であり、「育成契約選手制度」に基づき特別指定選手として加入した後、2026-27シーズンは期限付移籍（ローン）扱いとなっている。B.LEAGUE公式のクラブ所属履歴は滋賀を現所属として扱っているためそれに従って記録したが、ローン・原契約関係を表現するデータモデルが未整備。なお本人はニュース時点で筑波大学4年生であり、在学中の特別指定選手契約である点も西田公陽（batch_008/wave_02、issue B8W2I0003）と同様の未整備事項。",
     "next_check": "ローン移籍・在学中特別指定選手の扱い方（原契約チームとの関係表現）を今後検討"},
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
        f"Wrote batch_008/wave_03: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
