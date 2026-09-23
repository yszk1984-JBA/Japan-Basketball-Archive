#!/usr/bin/env python3
"""Build Batch 008 Wave 1 CANDIDATE data.

New initiative approved by Yuichi (2026-09-24): expand the archive beyond
福岡第一高校 by systematically covering other well-known basketball
powerhouse high schools ("強豪校"), tracing each school's alumni into
B.LEAGUE and university basketball. See docs/BATCH_008_PROPOSAL.md for the
full 11-school list and scope decisions (current B.LEAGUE players only,
one school at a time, reporting after each).

This wave covers School #1 of 11: 福岡大学附属大濠高等学校 (Fukuoka
University Ohori High School, Fukuoka) -- Winter Cup champion 5 times,
most recently back-to-back in 2024 and 2025.

Selection method: B.LEAGUE's own official "ワタシノB.LEAGUE選手一覧" page,
filtered by high-school tag (TagID=35), lists 18 current B.LEAGUE players
tagged as 大濠 alumni. Of those 18, one (金丸晃輔, P000090) is already
registered via batch_007/wave_02 and is NOT touched here. This wave
covers the first 4 of the remaining 17 (standard wave size per
docs/RESEARCH_BATCH_SIZING_V0.1.md); the other 13 are queued for
subsequent waves of this same batch.

Persons in this wave (checked against Master + every candidate/verified
person file before writing -- none previously registered):
- 杉浦佑成 (Yusei Sugiura, 仙台89ERS)
- 寒竹隼人 (Hayato Kantake, ライジングゼファー福岡)
- 青木保憲 (Yasunori Aoki, 大阪エヴェッサ)
- 土家大輝 (Daiki Tsuchiya, 信州ブレイブウォリアーズ)

Deliberate scope decision (same as batch_007/wave_01): only the minimum
Career chain -- high school -> university -> CURRENT club -- is recorded.
Several of these players (esp. 寒竹隼人, 土家大輝) have long, multi-team
B.LEAGUE histories; those are left for a future Enrichment Wave, matching
the established pattern for this project's other batches.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_008" / "wave_01"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000111", "name": "杉浦 佑成"},
    {"person_id": "P000112", "name": "寒竹 隼人"},
    {"person_id": "P000113", "name": "青木 保憲"},
    {"person_id": "P000114", "name": "土家 大輝"},
]

# ORG000127 (福岡大学附属大濠高等学校), ORG000031 (拓殖大学), ORG000132
# (仙台89ERS), ORG000040 (ライジングゼファー福岡), ORG000136 (早稲田大学)
# already exist and are reused, not re-minted -- checked against
# data/master/organization.csv and every candidate organization_candidates.csv
# before writing this file.
ORGANIZATIONS = [
    {"organization_id": "ORG000127", "name": "福岡大学附属大濠高等学校"},
    {"organization_id": "ORG000166", "name": "筑波大学"},
    {"organization_id": "ORG000132", "name": "仙台89ERS"},
    {"organization_id": "ORG000031", "name": "拓殖大学"},
    {"organization_id": "ORG000040", "name": "ライジングゼファー福岡"},
    {"organization_id": "ORG000142", "name": "大阪エヴェッサ"},
    {"organization_id": "ORG000136", "name": "早稲田大学"},
    {"organization_id": "ORG000150", "name": "信州ブレイブウォリアーズ"},
]

CAREERS = [
    # 杉浦佑成
    {"career_id": "C000390", "person_id": "P000111", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000391", "person_id": "P000111", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000392", "person_id": "P000111", "organization_id": "ORG000132", "role": "Player", "start": "2025", "end": ""},
    # 寒竹隼人
    {"career_id": "C000393", "person_id": "P000112", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000394", "person_id": "P000112", "organization_id": "ORG000031", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000395", "person_id": "P000112", "organization_id": "ORG000040", "role": "Player", "start": "2023", "end": ""},
    # 青木保憲
    {"career_id": "C000396", "person_id": "P000113", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000397", "person_id": "P000113", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000398", "person_id": "P000113", "organization_id": "ORG000142", "role": "Player", "start": "2025", "end": ""},
    # 土家大輝
    {"career_id": "C000399", "person_id": "P000114", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000400", "person_id": "P000114", "organization_id": "ORG000136", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000401", "person_id": "P000114", "organization_id": "ORG000150", "role": "Player", "start": "2025", "end": ""},
]

SOURCES = [
    {"source_id": "B8W1S0001", "title": "ワタシノB.LEAGUE選手一覧 | 福岡大学附属大濠高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:福岡大学附属大濠高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B8W1S0002", "title": "杉浦佑成 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=10820", "accessed_at": CHECKED_AT},
    {"source_id": "B8W1S0003", "title": "寒竹隼人 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8840", "accessed_at": CHECKED_AT},
    {"source_id": "B8W1S0004", "title": "青木保憲 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=15817", "accessed_at": CHECKED_AT},
    {"source_id": "B8W1S0005", "title": "土家大輝 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=5100000017", "accessed_at": CHECKED_AT},
    {"source_id": "B8W1S0006", "title": "福岡大学附属大濠高校出身のバスケットボール選手", "publisher": "バスケWeb辞典 (j-cbaske.com)", "url": "https://j-cbaske.com/baswiki/archives/5873", "accessed_at": CHECKED_AT},
    {"source_id": "B8W1S0007", "title": "青木保憲", "publisher": "Wikipedia日本語版", "url": "https://ja.wikipedia.org/wiki/青木保憲", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B8W1E{_evidence_seq:04d}",
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


# --- 杉浦佑成 (P000111) ---
add_evidence("Person", "P000111", "name", "杉浦 佑成", "B8W1S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000111", "birth_date", "1995-06-24", "B8W1S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000390", "organization_id", "ORG000127", "B8W1S0002", "学歴 > 高校：福岡大学附属大濠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000390", "organization_id", "ORG000127", "B8W1S0001", "TagID=35（福岡大学附属大濠高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000391", "organization_id", "ORG000166", "B8W1S0002", "学歴 > 大学：筑波大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000391", "organization_id", "ORG000166", "B8W1S0006", "選手一覧表 > 杉浦佑成 / 進学大学：筑波大学", "バスケWeb辞典でも筑波大学進学を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000392", "organization_id", "ORG000132", "B8W1S0002", "現在の所属：仙台89ERS（2025-26シーズン〜）", "B.LEAGUE公式プロフィールで現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000392", "start", "2025", "B8W1S0002", "クラブ所属履歴 > 「2025-26 仙台」", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 寒竹隼人 (P000112) ---
add_evidence("Person", "P000112", "name", "寒竹 隼人", "B8W1S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000112", "birth_date", "1986-08-01", "B8W1S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000393", "organization_id", "ORG000127", "B8W1S0003", "学歴 > 高校：福岡大学附属大濠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000393", "organization_id", "ORG000127", "B8W1S0001", "TagID=35（福岡大学附属大濠高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000394", "organization_id", "ORG000031", "B8W1S0003", "学歴 > 大学：拓殖大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000394", "organization_id", "ORG000031", "B8W1S0006", "選手一覧表 > 寒竹隼人 / 進学大学：拓殖大学", "バスケWeb辞典でも拓殖大学進学を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000395", "organization_id", "ORG000040", "B8W1S0003", "現在の所属：ライジングゼファー福岡", "B.LEAGUE公式プロフィールで現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000395", "start", "2023", "B8W1S0003", "クラブ所属履歴 > 「2023-24: 福岡」以降、2026-27まで継続", "B.LEAGUE公式のクラブ所属履歴で2023-24シーズンからの加入を確認", "SUPPORTED")

# --- 青木保憲 (P000113) ---
add_evidence("Person", "P000113", "name", "青木 保憲", "B8W1S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000113", "birth_date", "1995-06-23", "B8W1S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000396", "organization_id", "ORG000127", "B8W1S0001", "TagID=35（福岡大学附属大濠高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED",
             issue_note="本人のB.LEAGUE公式プロフィールページ自体には出身校欄の記載が見当たらなかった")
add_evidence("Career", "C000396", "organization_id", "ORG000127", "B8W1S0007", "本文 > 「福岡大学附属大濠高校、筑波大学ではそれぞれキャプテンを務めた」", "Wikipediaで大濠高校在学（キャプテン歴）を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000397", "organization_id", "ORG000166", "B8W1S0006", "選手一覧表 > 青木保憲 / 進学大学：筑波大学", "バスケWeb辞典で筑波大学進学を確認", "SUPPORTED")
add_evidence("Career", "C000397", "organization_id", "ORG000166", "B8W1S0007", "本文 > 「筑波大学ではそれぞれキャプテンを務めた」", "Wikipediaでも筑波大学在学（キャプテン歴）を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000398", "organization_id", "ORG000142", "B8W1S0004", "現在の所属：大阪エヴェッサ（2025-26シーズン）", "B.LEAGUE公式プロフィールで現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000398", "start", "2025", "B8W1S0004", "クラブ所属履歴 > 2025-26シーズンより大阪エヴェッサ", "B.LEAGUE公式プロフィールで2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 土家大輝 (P000114) ---
add_evidence("Person", "P000114", "name", "土家 大輝", "B8W1S0005", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000114", "birth_date", "2000-04-05", "B8W1S0005", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000399", "organization_id", "ORG000127", "B8W1S0001", "TagID=35（福岡大学附属大濠高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED",
             issue_note="本人のB.LEAGUE公式プロフィールページの「出身校」欄には大学名（早稲田大学）のみ表示され、高校は別欄に無い")
add_evidence("Career", "C000399", "organization_id", "ORG000127", "B8W1S0006", "選手一覧表 > 土家大輝（福岡大学附属大濠高校出身選手一覧に掲載）", "バスケWeb辞典の大濠高校出身選手一覧に掲載（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000400", "organization_id", "ORG000136", "B8W1S0005", "学歴 > 出身校：早稲田大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000400", "organization_id", "ORG000136", "B8W1S0006", "選手一覧表 > 土家大輝 / 進学大学：早稲田大学", "バスケWeb辞典でも早稲田大学進学を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000401", "organization_id", "ORG000150", "B8W1S0005", "現在の所属：信州（2025-26シーズン）", "B.LEAGUE公式プロフィールで現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000401", "start", "2025", "B8W1S0005", "クラブ所属履歴 > 「2025-26：信州」", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B8W1D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000111", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000390", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000391", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・バスケWeb辞典の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000392", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000112", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000393", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000394", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・バスケWeb辞典の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000395", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000113", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000396", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧・Wikipediaの独立2ソースで確認（本人プロフィールページには出身校欄の記載なし）、在籍期間は未確認")
add_decision("Career", "C000397", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "バスケWeb辞典・Wikipediaの独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000398", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000114", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000399", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧・バスケWeb辞典の独立2ソースで確認（本人プロフィールページの出身校欄は大学名のみ表示）、在籍期間は未確認")
add_decision("Career", "C000400", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・バスケWeb辞典の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000401", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

ISSUES = [
    {"issue_id": "B8W1I0001", "person_id": "P000111|P000112|P000113|P000114", "related_id": "C000390|C000393|C000396|C000399", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "4名とも福岡大学附属大濠高等学校在籍そのものは複数ソースで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "高校公式または大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B8W1I0002", "person_id": "P000111|P000112|P000113|P000114", "related_id": "C000391|C000394|C000397|C000400", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "4名とも大学在籍そのものは複数ソースで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B8W1I0003", "person_id": "P000112", "related_id": "P000112", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "寒竹隼人は現所属（ライジングゼファー福岡、2023-24〜）以前にも仙台（2020-23）、琉球（2018-20）、大阪（2017-18）、島根（2016-17）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B8W1I0004", "person_id": "P000114", "related_id": "P000114", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "土家大輝は現所属（信州、2025-26〜）以前にも大阪（2024-25）、福島（2022-24）、島根（2021-22）、FE名古屋（2020-21）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B8W1I0005", "person_id": "P000113|P000114", "related_id": "C000396|C000399", "issue_type": "PROFILE_FIELD_GAP", "status": "HOLD",
     "description": "青木保憲・土家大輝の本人B.LEAGUE公式プロフィールページには、高校名を直接示す「出身校」欄の記載が見当たらなかった（青木保憲は欄自体が空欄、土家大輝は大学名のみ表示）。出身校タグ一覧・バスケWeb辞典・Wikipedia（青木保憲のみ）で裏付けたが、選手個人ページの表示形式の違いによるものか未確認。",
     "next_check": "B.LEAGUE公式プロフィールページの表示更新があれば再確認"},
    {"issue_id": "B8W1I0006", "person_id": "P000111|P000112|P000113|P000114", "related_id": "P000111|P000112|P000113|P000114", "issue_type": "SCOPE_NOTE", "status": "RESOLVED",
     "description": "docs/BATCH_008_PROPOSAL.mdで選定した福岡大学附属大濠高等学校（学校1/11）のうち、B.LEAGUE公式出身校タグ一覧の18名から既存登録済み1名（金丸晃輔、P000090）を除いた17名の一部（4名）を本Waveで対応。残り13名は後続Waveで対応する。",
     "next_check": "batch_008/wave_02以降で残り13名を対応"},
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
        f"Wrote batch_008/wave_01: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
