#!/usr/bin/env python3
"""Build Batch 008 Wave 2 (福岡大学附属大濠高等学校 2/4) CANDIDATE data.

Continues wave_01's coverage of the school's 17 not-yet-registered current
B.LEAGUE alumni (out of 18 total on B.LEAGUE's TagID=35 listing; 金丸晃輔
already registered via batch_007/wave_02). This wave covers 6 more
(increase from wave_01's standard 4, per
docs/RESEARCH_BATCH_SIZING_V0.1.md's rule: wave_01 had >=2 official
sources/person, 0 structural QA errors, 0 misidentifications).

Persons (checked against Master + every candidate/verified person file
before writing -- none previously registered):
- 西田陽成 (Yosei Nishida, 滋賀レイクス)
- 泉登翔 (Towa Izumi, 富山グラウジーズ)
- 間山柊 (Shu Mayama, バンビシャス奈良)
- 針間大知 (Daichi Harima, ファイティングイーグルス名古屋)
- 西田公陽 (Koyo Nishida, 徳島ガンバロウズ -- currently on loan from
  シーホース三河 per news reports; the loan club is recorded as his
  Career per B.LEAGUE's own tag-list classification, see issue
  B8W2I0003)
- 渡邉伶音 (Leon Watanabe, アルティーリ千葉)

Same deliberate scope as wave_01: minimum Career chain only (high school
-> university -> CURRENT club). 渡邉伶音's university stint at 東海大学
(April-July 2025, withdrew to turn fully pro) IS recorded despite being
brief, matching the established "attended but later left" precedent
(e.g. batch_006/wave_03's 白鷗大学 case for 長島エマニエル) -- attendance
is a fact regardless of duration. His earlier special-designated-player
stint at ライジングゼファー福岡 (before university) is NOT recorded as a
Career, matching the pre-current-club-history exclusion used for other
players in this wave/batch; see issue B8W2I0004.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_008" / "wave_02"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000115", "name": "西田 陽成"},
    {"person_id": "P000116", "name": "泉 登翔"},
    {"person_id": "P000117", "name": "間山 柊"},
    {"person_id": "P000118", "name": "針間 大知"},
    {"person_id": "P000119", "name": "西田 公陽"},
    {"person_id": "P000120", "name": "渡邉 伶音"},
]

# ORG000127 (大濠), ORG000015 (東海大学), ORG000121 (日本大学), ORG000166
# (筑波大学), ORG000124 (明治大学), ORG000116 (徳島ガンバロウズ) already
# exist and are reused -- checked against master + every candidate
# organization_candidates.csv before writing this file.
ORGANIZATIONS = [
    {"organization_id": "ORG000127", "name": "福岡大学附属大濠高等学校"},
    {"organization_id": "ORG000015", "name": "東海大学"},
    {"organization_id": "ORG000153", "name": "滋賀レイクス"},
    {"organization_id": "ORG000121", "name": "日本大学"},
    {"organization_id": "ORG000149", "name": "富山グラウジーズ"},
    {"organization_id": "ORG000166", "name": "筑波大学"},
    {"organization_id": "ORG000171", "name": "バンビシャス奈良"},
    {"organization_id": "ORG000124", "name": "明治大学"},
    {"organization_id": "ORG000180", "name": "ファイティングイーグルス名古屋"},
    {"organization_id": "ORG000116", "name": "徳島ガンバロウズ"},
    {"organization_id": "ORG000144", "name": "アルティーリ千葉"},
]

CAREERS = [
    # 西田陽成
    {"career_id": "C000402", "person_id": "P000115", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000403", "person_id": "P000115", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000404", "person_id": "P000115", "organization_id": "ORG000153", "role": "Player", "start": "2024", "end": ""},
    # 泉登翔
    {"career_id": "C000405", "person_id": "P000116", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000406", "person_id": "P000116", "organization_id": "ORG000121", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000407", "person_id": "P000116", "organization_id": "ORG000149", "role": "Player", "start": "2025", "end": ""},
    # 間山柊
    {"career_id": "C000408", "person_id": "P000117", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000409", "person_id": "P000117", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000410", "person_id": "P000117", "organization_id": "ORG000171", "role": "Player", "start": "2024", "end": ""},
    # 針間大知
    {"career_id": "C000411", "person_id": "P000118", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000412", "person_id": "P000118", "organization_id": "ORG000124", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000413", "person_id": "P000118", "organization_id": "ORG000180", "role": "Player", "start": "2025", "end": ""},
    # 西田公陽
    {"career_id": "C000414", "person_id": "P000119", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000415", "person_id": "P000119", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000416", "person_id": "P000119", "organization_id": "ORG000116", "role": "Player", "start": "2026", "end": ""},
    # 渡邉伶音
    {"career_id": "C000417", "person_id": "P000120", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000418", "person_id": "P000120", "organization_id": "ORG000015", "role": "Player", "start": "2025", "end": "2025"},
    {"career_id": "C000419", "person_id": "P000120", "organization_id": "ORG000144", "role": "Player", "start": "2025", "end": ""},
]

SOURCES = [
    {"source_id": "B8W2S0001", "title": "西田陽成 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000470", "accessed_at": CHECKED_AT},
    {"source_id": "B8W2S0002", "title": "泉登翔 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000464", "accessed_at": CHECKED_AT},
    {"source_id": "B8W2S0003", "title": "間山柊 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000484", "accessed_at": CHECKED_AT},
    {"source_id": "B8W2S0004", "title": "針間大知 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000592", "accessed_at": CHECKED_AT},
    {"source_id": "B8W2S0005", "title": "西田公陽 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000362", "accessed_at": CHECKED_AT},
    {"source_id": "B8W2S0006", "title": "渡邉伶音 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000352", "accessed_at": CHECKED_AT},
    {"source_id": "B8W2S0007", "title": "ワタシノB.LEAGUE選手一覧 | 福岡大学附属大濠高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:福岡大学附属大濠高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B8W2S0008", "title": "福大大濠の渡邉伶音が特別指定選手としてA千葉入り", "publisher": "B.LEAGUE（media_news）", "url": "https://www.bleague.jp/media_news/detail/id=444402", "accessed_at": CHECKED_AT},
    {"source_id": "B8W2S0009", "title": "A千葉の渡邉伶音が特別指定選手の活動終了…4月からは東海大学へ進学", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/japan/20250331/531962.html", "accessed_at": CHECKED_AT},
    {"source_id": "B8W2S0010", "title": "東海大退学の渡邉伶音がA千葉と契約「責任と覚悟を持って決断」", "publisher": "B.LEAGUE（media_news）", "url": "https://www.bleague.jp/media_news/detail/id=533865", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B8W2E{_evidence_seq:04d}",
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


# --- 西田陽成 ---
add_evidence("Person", "P000115", "name", "西田 陽成", "B8W2S0001", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000115", "birth_date", "2002-05-26", "B8W2S0001", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000402", "organization_id", "ORG000127", "B8W2S0001", "出身校（高校）：福岡大学附属大濠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000402", "organization_id", "ORG000127", "B8W2S0007", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000403", "organization_id", "ORG000015", "B8W2S0001", "出身校（大学）：東海大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000404", "organization_id", "ORG000153", "B8W2S0001", "現在の所属クラブ：滋賀レイクス", "B.LEAGUE公式プロフィールで現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000404", "start", "2024", "B8W2S0001", "クラブ所属履歴 > 「2024-25シーズン：滋賀レイクス」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入を確認", "SUPPORTED")

# --- 泉登翔 ---
add_evidence("Person", "P000116", "name", "泉 登翔", "B8W2S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000116", "birth_date", "2003-07-04", "B8W2S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000405", "organization_id", "ORG000127", "B8W2S0007", "TagID=35（福岡大学附属大濠高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED",
             issue_note="本人のB.LEAGUE公式プロフィールページの出身校欄には大学名（日本大学）のみ表示され、高校の別欄記載はない")
add_evidence("Career", "C000406", "organization_id", "ORG000121", "B8W2S0002", "出身校：日本大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000407", "organization_id", "ORG000149", "B8W2S0002", "現在の所属：富山グラウジーズ（2026-27シーズン）", "B.LEAGUE公式プロフィールで現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000407", "start", "2025", "B8W2S0002", "クラブ所属履歴 > 「2025-26：富山グラウジーズ」が初出（前年は広島）", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 間山柊 ---
add_evidence("Person", "P000117", "name", "間山 柊", "B8W2S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000117", "birth_date", "2003-01-14", "B8W2S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000408", "organization_id", "ORG000127", "B8W2S0003", "学歴 > 高校：福岡大学附属大濠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000408", "organization_id", "ORG000127", "B8W2S0007", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000409", "organization_id", "ORG000166", "B8W2S0003", "学歴 > 大学：筑波大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000410", "organization_id", "ORG000171", "B8W2S0003", "現在：バンビシャス奈良", "B.LEAGUE公式プロフィールで現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000410", "start", "2024", "B8W2S0003", "クラブ所属履歴 > 「2024-25シーズン：奈良」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入を確認", "SUPPORTED")

# --- 針間大知 ---
add_evidence("Person", "P000118", "name", "針間 大知", "B8W2S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000118", "birth_date", "2003-05-10", "B8W2S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000411", "organization_id", "ORG000127", "B8W2S0004", "学歴 > 高校：福岡大学附属大濠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000411", "organization_id", "ORG000127", "B8W2S0007", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000412", "organization_id", "ORG000124", "B8W2S0004", "学歴 > 大学：明治大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000413", "organization_id", "ORG000180", "B8W2S0004", "クラブ所属履歴 > 「2025-26シーズン：ファイティングイーグルス名古屋」", "B.LEAGUE公式プロフィールで現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000413", "start", "2025", "B8W2S0004", "クラブ所属履歴 > 「2025-26シーズン：ファイティングイーグルス名古屋」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 西田公陽 ---
add_evidence("Person", "P000119", "name", "西田 公陽", "B8W2S0005", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000119", "birth_date", "2001-06-05", "B8W2S0005", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000414", "organization_id", "ORG000127", "B8W2S0005", "学歴 > 高校：福岡大学附属大濠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000414", "organization_id", "ORG000127", "B8W2S0007", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000415", "organization_id", "ORG000015", "B8W2S0005", "学歴 > 大学：東海大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000416", "organization_id", "ORG000116", "B8W2S0005", "現在の所属：「2026-27 徳島」ガンバロウズ", "B.LEAGUE公式プロフィールで現所属クラブを確認", "SUPPORTED",
             issue_note="報道（バスケットボールキング等）によれば原契約はシーホース三河（ORG000130）で、徳島へは期限付き移籍（ローン）中。B.LEAGUE公式の出身校タグ一覧・選手プロフィールいずれも徳島を現所属として扱っているため、それに従って記録した")
add_evidence("Career", "C000416", "start", "2026", "B8W2S0005", "クラブ所属履歴 > 「2026-27：徳島（現所属）」", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの加入を確認", "SUPPORTED")

# --- 渡邉伶音 ---
add_evidence("Person", "P000120", "name", "渡邉 伶音", "B8W2S0006", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000120", "birth_date", "2006-04-02", "B8W2S0006", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000417", "organization_id", "ORG000127", "B8W2S0008", "本文 > 「福大大濠の渡邉伶音が特別指定選手としてA千葉入り」", "B.LEAGUE媒体記事で福岡大学附属大濠高校出身であることを確認", "SUPPORTED")
add_evidence("Career", "C000417", "organization_id", "ORG000127", "B8W2S0007", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000418", "organization_id", "ORG000015", "B8W2S0009", "本文 > 「4月からは東海大学へ進学」", "B.LEAGUE媒体記事で2025年4月の東海大学進学を確認", "SUPPORTED")
add_evidence("Career", "C000418", "start", "2025", "B8W2S0009", "本文 > 「4月からは東海大学へ進学」（2025年3月31日付記事）", "進学時期（2025年4月）を確認", "SUPPORTED")
add_evidence("Career", "C000418", "end", "2025", "B8W2S0010", "本文 > 「今春に東海大学へ進学していましたが...2025年7月をもって退学」", "B.LEAGUE媒体記事で2025年7月の中退を確認", "SUPPORTED")
add_evidence("Career", "C000419", "organization_id", "ORG000144", "B8W2S0010", "本文 > アルティーリ千葉が2025-26シーズンの選手契約に合意", "B.LEAGUE媒体記事でアルティーリ千葉との正式契約（2025年7月）を確認", "SUPPORTED")
add_evidence("Career", "C000419", "start", "2025", "B8W2S0010", "本文 > 「2025-26シーズンの選手契約に合意」（2025年7月16日付記事）", "契約時期を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B8W2D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000115", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000402", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000403", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000404", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000116", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000405", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認（本人プロフィールページには出身校欄の大学名記載のみ）、在籍期間は未確認")
add_decision("Career", "C000406", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000407", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000117", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000408", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000409", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000410", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000118", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000411", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000412", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000413", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000119", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000414", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000415", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000416", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。ローン移籍の可能性はissueに記録")

add_decision("Person", "P000120", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000417", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE媒体記事・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000418", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "", "B.LEAGUE媒体記事で入学（2025年4月）・中退（2025年7月）とも確認")
add_decision("Career", "C000419", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE媒体記事で確認、現在進行中の契約のため終了日は未定")

ISSUES = [
    {"issue_id": "B8W2I0001", "person_id": "P000115|P000116|P000117|P000118|P000119|P000120", "related_id": "C000402|C000405|C000408|C000411|C000414|C000417", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "6名とも福岡大学附属大濠高等学校在籍そのものは複数ソースで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "高校公式または大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B8W2I0002", "person_id": "P000115|P000116|P000117|P000118|P000119", "related_id": "C000403|C000406|C000409|C000412|C000415", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "5名（渡邉伶音を除く）とも大学在籍そのものは確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B8W2I0003", "person_id": "P000119", "related_id": "C000416", "issue_type": "LOAN_STATUS", "status": "HOLD",
     "description": "西田公陽の徳島ガンバロウズ在籍は、報道によれば原契約チームのシーホース三河（ORG000130）からの期限付き移籍（ローン）である可能性がある。B.LEAGUE公式は徳島を現所属として扱っているためそれに従ったが、ローン・原契約関係を表現するデータモデルが未整備。",
     "next_check": "ローン移籍の扱い方（原契約チームとの関係表現）を今後検討"},
    {"issue_id": "B8W2I0004", "person_id": "P000120", "related_id": "P000120", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "渡邉伶音は東海大学進学（2025年4月）以前の2025年1月〜3月、高校在学中にライジングゼファー福岡で特別指定選手として活動していたことが報道で確認できるが、今回のWaveでは大学中退後の正式契約（アルティーリ千葉）のみを最小経路として登録し、特別指定選手期間は対象外とした。",
     "next_check": "後続の深掘りWaveで特別指定選手期間のCareerを追加するか検討"},
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
        f"Wrote batch_008/wave_02: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
