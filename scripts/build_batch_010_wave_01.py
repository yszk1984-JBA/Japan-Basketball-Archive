#!/usr/bin/env python3
"""Build Batch 010 Wave 1 (洛南高等学校, school 3/11) CANDIDATE data.

Third school of the powerhouse-school expansion initiative (see
docs/BATCH_008_PROPOSAL.md). 洛南高等学校 (Kyoto) already has an
Organization ID (ORG000119) registered via batch_007 (辻直人, 竹内譲次,
比江島慎, batch_007/wave_01/wave_05) and batch_007/wave_03 (星川堅信) --
reused here, no new ID minted.

Discovery: B.LEAGUE's TagID=35:洛南高等学校 tag list shows 23 current
alumni. The tag list's own player cards (unlike 大濠/明成's list, which
had to be cross-referenced against each player's own roster_detail page)
directly show each player's UNIVERSITY in their "出身校" field -- the
high school itself is already implied by the tag filter, and confirmed
as the primary evidence for each person's high-school Career here,
matching the sole-source pattern used elsewhere in this project when an
individual profile page lacks the field. Getting the full 23-name list
required loading the page in a browser and clicking "もっと見る" twice,
since the static HTML (what WebFetch sees) only renders 18 of the 23
entries -- a "more" button calling a JS function.

Of the 23 tagged alumni, 4 are already registered with complete
high-school -> university -> current-club chains matching their current
B.LEAGUE status, so need no new work: 星川堅信 (P000094,
batch_007/wave_03), 竹内譲次 (P000096), 辻直人 (P000097, both
batch_007/wave_05), 比江島慎 (P000084, batch_007/wave_01). That leaves 19
new persons, split across 4 waves (wave_01-03: 6 each, wave_04: 1) per
the standard wave-sizing increase rule.

Notable finding: 竹内公輔's club history shows "栃木" (2016-17〜2018-19)
immediately followed by "宇都宮" (2019-20〜present) with no gap -- this is
NOT two different clubs. 栃木ブレックス renamed to 宇都宮ブレックス in
2019-07 (confirmed via news search: Nikkei, basketballking). Per the
established organization-rename convention (same as 明成/仙台大学附属明成
in batch_009), the SAME Organization ID (ORG000047, already registered
via 比江島慎) is reused and his Career start is recorded as 2016 (his
actual join date, under the club's old name), not 2019 -- to avoid
fabricating a false employment gap. This is a schema gap for the
pre-rename name, logged as issue B10W1I0006 (ORG_NAME_HISTORY).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_010" / "wave_01"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000134", "name": "星川 開聖"},
    {"person_id": "P000135", "name": "竹内 公輔"},
    {"person_id": "P000136", "name": "荒川 颯"},
    {"person_id": "P000137", "name": "笹山 貴哉"},
    {"person_id": "P000138", "name": "岩屋 頼"},
    {"person_id": "P000139", "name": "森井 健太"},
]

# ORG000119 (洛南高等学校), ORG000166 (筑波大学), ORG000047 (宇都宮ブレックス
# -- reused across its 2019 rename from 栃木ブレックス, see module
# docstring), ORG000031 (拓殖大学), ORG000180 (ファイティングイーグルス名古屋),
# ORG000136 (早稲田大学), ORG000137 (秋田ノーザンハピネッツ), ORG000055
# (横浜ビー・コルセアーズ) already exist and are reused -- checked against
# master + every candidate organization_candidates.csv before writing this
# file. 慶應義塾大学 confirmed genuinely new; current max existing
# Organization ID is ORG000184 (batch_009/wave_01), so this is ORG000185.
ORGANIZATIONS = [
    {"organization_id": "ORG000119", "name": "洛南高等学校"},
    {"organization_id": "ORG000166", "name": "筑波大学"},
    {"organization_id": "ORG000047", "name": "宇都宮ブレックス"},
    {"organization_id": "ORG000185", "name": "慶應義塾大学"},
    {"organization_id": "ORG000031", "name": "拓殖大学"},
    {"organization_id": "ORG000180", "name": "ファイティングイーグルス名古屋"},
    {"organization_id": "ORG000136", "name": "早稲田大学"},
    {"organization_id": "ORG000137", "name": "秋田ノーザンハピネッツ"},
    {"organization_id": "ORG000055", "name": "横浜ビー・コルセアーズ"},
]

CAREERS = [
    # 星川開聖（現所属クラブがB.LEAGUEデビュー先）
    {"career_id": "C000457", "person_id": "P000134", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000458", "person_id": "P000134", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000459", "person_id": "P000134", "organization_id": "ORG000047", "role": "Player", "start": "2024", "end": ""},
    # 竹内公輔（栃木ブレックス時代からの継続在籍、start=2016）
    {"career_id": "C000460", "person_id": "P000135", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000461", "person_id": "P000135", "organization_id": "ORG000185", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000462", "person_id": "P000135", "organization_id": "ORG000047", "role": "Player", "start": "2016", "end": ""},
    # 荒川颯
    {"career_id": "C000463", "person_id": "P000136", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000464", "person_id": "P000136", "organization_id": "ORG000031", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000465", "person_id": "P000136", "organization_id": "ORG000047", "role": "Player", "start": "2026", "end": ""},
    # 笹山貴哉
    {"career_id": "C000466", "person_id": "P000137", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000467", "person_id": "P000137", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000468", "person_id": "P000137", "organization_id": "ORG000180", "role": "Player", "start": "2021", "end": ""},
    # 岩屋頼（現所属クラブがB.LEAGUEデビュー先）
    {"career_id": "C000469", "person_id": "P000138", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000470", "person_id": "P000138", "organization_id": "ORG000136", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000471", "person_id": "P000138", "organization_id": "ORG000137", "role": "Player", "start": "2025", "end": ""},
    # 森井健太
    {"career_id": "C000472", "person_id": "P000139", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000473", "person_id": "P000139", "organization_id": "ORG000136", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000474", "person_id": "P000139", "organization_id": "ORG000055", "role": "Player", "start": "2020", "end": ""},
]

SOURCES = [
    {"source_id": "B10W1S0001", "title": "ワタシノB.LEAGUE選手一覧 | 洛南高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:洛南高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B10W1S0002", "title": "星川開聖 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000461", "accessed_at": CHECKED_AT},
    {"source_id": "B10W1S0003", "title": "竹内公輔 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8726", "accessed_at": CHECKED_AT},
    {"source_id": "B10W1S0004", "title": "荒川颯 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=30458", "accessed_at": CHECKED_AT},
    {"source_id": "B10W1S0005", "title": "笹山貴哉 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8517", "accessed_at": CHECKED_AT},
    {"source_id": "B10W1S0006", "title": "岩屋頼 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000600", "accessed_at": CHECKED_AT},
    {"source_id": "B10W1S0007", "title": "森井健太 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=10851", "accessed_at": CHECKED_AT},
    {"source_id": "B10W1S0008", "title": "宇都宮ブレックスが琉球を退団した荒川颯を獲得「自分自身の価値を証明するためにも、ブレックスというチームに新たな風を吹かせる」", "publisher": "バスケットカウント", "url": "https://basket-count.com/article/detail/265731", "accessed_at": CHECKED_AT},
    {"source_id": "B10W1S0009", "title": "栃木ブレックスがチーム名称変更、「宇都宮ブレックス」に", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/japan/20190708/174056.html", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B10W1E{_evidence_seq:04d}",
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


# --- 星川開聖 ---
add_evidence("Person", "P000134", "name", "星川 開聖", "B10W1S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000134", "birth_date", "2004-11-19", "B10W1S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000457", "organization_id", "ORG000119", "B10W1S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000458", "organization_id", "ORG000166", "B10W1S0001", "選手カード > 出身校：筑波大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000459", "organization_id", "ORG000047", "B10W1S0002", "クラブ経歴 > 「2024-25：宇都宮」が初出（唯一の記載）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000459", "start", "2024", "B10W1S0002", "クラブ経歴 > 「2024-25：宇都宮」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 竹内公輔 ---
add_evidence("Person", "P000135", "name", "竹内 公輔", "B10W1S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000135", "birth_date", "1985-01-29", "B10W1S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000460", "organization_id", "ORG000119", "B10W1S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000461", "organization_id", "ORG000185", "B10W1S0001", "選手カード > 出身校：慶應義塾大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000462", "organization_id", "ORG000047", "B10W1S0003", "クラブ経歴 > 「2016-17〜2018-19：栃木」「2019-20以降：宇都宮」", "B.LEAGUE公式のクラブ所属履歴を確認", "SUPPORTED",
             issue_note="栃木ブレックスは2019年7月に宇都宮ブレックスへ改称（バスケットボールキングで確認）した同一クラブのため、Organizationは既存の宇都宮ブレックス（ORG000047）を再利用し、改称前からの継続在籍として扱った。詳細はissue B10W1I0006を参照")
add_evidence("Career", "C000462", "start", "2016", "B10W1S0003", "クラブ経歴 > 「2016-17：栃木」が初出", "B.LEAGUE公式のクラブ所属履歴で2016-17シーズンからの加入（改称前の栃木ブレックス在籍時から）を確認", "SUPPORTED")

# --- 荒川颯 ---
add_evidence("Person", "P000136", "name", "荒川 颯", "B10W1S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000136", "birth_date", "1997-07-25", "B10W1S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000463", "organization_id", "ORG000119", "B10W1S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000464", "organization_id", "ORG000031", "B10W1S0001", "選手カード > 出身校：拓殖大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000465", "organization_id", "ORG000047", "B10W1S0008", "本文 > 「宇都宮ブレックスが琉球を退団した荒川颯を獲得」", "バスケットカウント記事で宇都宮ブレックスとの契約（2026-27シーズン）を確認", "SUPPORTED")
add_evidence("Career", "C000465", "start", "2026", "B10W1S0004", "クラブ経歴 > 「2026-27：宇都宮」が初出", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの加入を確認", "SUPPORTED")

# --- 笹山貴哉 ---
add_evidence("Person", "P000137", "name", "笹山 貴哉", "B10W1S0005", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000137", "birth_date", "1993-02-15", "B10W1S0005", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000466", "organization_id", "ORG000119", "B10W1S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000467", "organization_id", "ORG000166", "B10W1S0001", "選手カード > 出身校：筑波大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000468", "organization_id", "ORG000180", "B10W1S0005", "クラブ経歴 > 「2021-22以降：FE名古屋」", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000468", "start", "2021", "B10W1S0005", "クラブ経歴 > 「2021-22：FE名古屋」が初出（前年は名古屋D、別クラブ）", "B.LEAGUE公式のクラブ所属履歴で2021-22シーズンからの加入を確認", "SUPPORTED",
             issue_note="前年までの「名古屋D」（名古屋ダイヤモンドドルフィンズ、ORG000054）はFE名古屋とは別法人の別クラブであり、改称等の同一性はない（詳細はissue B10W1I0007を参照）")

# --- 岩屋頼 ---
add_evidence("Person", "P000138", "name", "岩屋 頼", "B10W1S0006", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000138", "birth_date", "2003-04-20", "B10W1S0006", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000469", "organization_id", "ORG000119", "B10W1S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000470", "organization_id", "ORG000136", "B10W1S0001", "選手カード > 出身校：早稲田大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000471", "organization_id", "ORG000137", "B10W1S0006", "クラブ経歴 > 「2025-26：秋田」が初出（唯一の記載）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000471", "start", "2025", "B10W1S0006", "クラブ経歴 > 「2025-26：秋田」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 森井健太 ---
add_evidence("Person", "P000139", "name", "森井 健太", "B10W1S0007", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000139", "birth_date", "1995-09-22", "B10W1S0007", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000472", "organization_id", "ORG000119", "B10W1S0001", "TagID=35（洛南高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000473", "organization_id", "ORG000136", "B10W1S0001", "選手カード > 出身校：早稲田大学", "B.LEAGUE公式の出身校タグ一覧の選手カードで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000474", "organization_id", "ORG000055", "B10W1S0007", "クラブ経歴 > 「2020-21：横浜BC」が初出（前年は新潟）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000474", "start", "2020", "B10W1S0007", "クラブ経歴 > 「2020-21：横浜BC」が初出", "B.LEAGUE公式のクラブ所属履歴で2020-21シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B10W1D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000134", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000457", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000458", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000459", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000135", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000460", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000461", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000462", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認（栃木ブレックス改称前からの継続在籍として登録）、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000136", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000463", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000464", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000465", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "バスケットカウント記事・B.LEAGUE公式クラブ所属履歴で確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000137", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000466", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000467", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000468", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。前所属「名古屋D」との非同一性はissueに記録")

add_decision("Person", "P000138", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000469", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000470", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000471", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000139", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000472", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000473", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧の選手カードで確認、在籍期間は未確認")
add_decision("Career", "C000474", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

ISSUES = [
    {"issue_id": "B10W1I0001", "person_id": "P000134|P000135|P000136|P000137|P000138|P000139", "related_id": "C000457|C000460|C000463|C000466|C000469|C000472", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "6名とも洛南高等学校在籍そのものは出身校タグ一覧で確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。個々のB.LEAGUE公式プロフィールページに高校名を明記した学歴欄があるかは今回未確認（出身校タグ一覧の掲載のみを根拠とした）。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B10W1I0002", "person_id": "P000134|P000135|P000136|P000137|P000138|P000139", "related_id": "C000458|C000461|C000464|C000467|C000470|C000473", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "6名とも大学在籍そのものは出身校タグ一覧の選手カードで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B10W1I0003", "person_id": "P000135", "related_id": "P000135", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "竹内公輔は宇都宮ブレックス（栃木ブレックス時代を含む、2016-17〜）の一貫した在籍として登録したが、それ以前の経歴は今回確認していない。",
     "next_check": "デビュー時期・それ以前の経歴を確認"},
    {"issue_id": "B10W1I0004", "person_id": "P000136", "related_id": "P000136", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "荒川颯は現所属（宇都宮ブレックス、2026-27〜）以前にライジングゼファー福岡（ORG000040、2019-20）、ファイティングイーグルス名古屋（ORG000180、2020-21）、横浜エクセレンス（ORG000090、2021-22）、レバンガ北海道（ORG000092、2022-23）、琉球ゴールデンキングス（ORG000106、2023-24〜2025-26）と5クラブにまたがる長いプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加（クラブ数が多く優先度を検討）"},
    {"issue_id": "B10W1I0005", "person_id": "P000139", "related_id": "P000139", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "森井健太は現所属（横浜ビー・コルセアーズ、2020-21〜）以前に新潟アルビレックスBB（ORG000052、2016-17〜2019-20）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B10W1I0006", "person_id": "P000135", "related_id": "C000462", "issue_type": "ORG_NAME_HISTORY", "status": "HOLD",
     "description": "宇都宮ブレックス（ORG000047）は2019年7月に「栃木ブレックス」から改称した（バスケットボールキング記事で確認）。竹内公輔は改称前の2016-17シーズンから在籍しているが、単一名称のスキーマでは改称前の呼称「栃木ブレックス」を表現できず、既存レコードの名称を無断で変更しない方針のためORG000047の登録名は変更していない（明成高等学校/仙台大学附属明成高等学校と同種の事例）。",
     "next_check": "Organization名称の時系列表現（改称履歴）のスキーマ整備を検討"},
    {"issue_id": "B10W1I0007", "person_id": "P000137", "related_id": "C000468", "issue_type": "DATA_QUALITY_NOTE", "status": "HOLD",
     "description": "笹山貴哉のクラブ所属履歴に2016-17〜2020-21シーズン「名古屋D」と表示されるが、これは現所属のファイティングイーグルス名古屋（ORG000180、法人：豊通ファイティングイーグルス株式会社）とは無関係の別クラブ「名古屋ダイヤモンドドルフィンズ」（ORG000054）の略称であることを確認した（FE名古屋公式の呼称変更のお知らせで、FE名古屋は2020年に呼称のみ変更し法人・クラブ名は変更なしと確認）。誤って同一クラブとして継続在籍を記録しないよう、今回は2021-22シーズン以降のFE名古屋在籍のみを登録した。",
     "next_check": "後続の深掘りWaveで名古屋ダイヤモンドドルフィンズ在籍期間（2016-17〜2020-21）のCareerを追加するか検討"},
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
        f"Wrote batch_010/wave_01: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
