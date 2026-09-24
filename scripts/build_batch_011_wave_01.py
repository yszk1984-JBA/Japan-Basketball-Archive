#!/usr/bin/env python3
"""Build Batch 011 Wave 1 (開志国際高等学校, school 4/11) CANDIDATE data.

Fourth school of the powerhouse-school expansion initiative (see
docs/BATCH_008_PROPOSAL.md). 開志国際高等学校 (Niigata) has no existing
Organization ID -- newly minted here as ORG000192.

Discovery: B.LEAGUE's "ワタシノB.LEAGUE" tag list for TagID=35:開志国際高等学校
(https://www.bleague.jp/mybleague_list/?TagID=35:開志国際高等学校) shows
exactly 3 current alumni -- no "もっと見る" pagination needed this time
(unlike 大濠/明成/洛南's longer lists). All 3 are genuinely new to the
project (checked against data/master/person.csv and every existing
person_candidates.csv). This is a single wave of 3 (below the standard
4/wave size, since that is the school's entire current B.LEAGUE alumni
count per the official tag).

Per the batch's approved scope (docs/BATCH_008_PROPOSAL.md), only the
current club is registered as Pro career (minimal path: high school ->
university (if any) -> current club); prior clubs found in each
player's クラブ所属履歴 are logged as PRO_HISTORY_GAPS issues instead of
being added as Career rows, matching the convention used throughout
batch_008-010.

Notable: 平良宗龍 has no university (出身校（大）: "-" on his B.LEAGUE
profile) -- he is a high-school-to-pro case, so his path is just
高校 -> 現所属クラブ (2 Careers, not 3).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_011" / "wave_01"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000153", "name": "介川 アンソニー翔"},
    {"person_id": "P000154", "name": "小栗 瑛哉"},
    {"person_id": "P000155", "name": "平良 宗龍"},
]

# ORG000018 (専修大学), ORG000150 (信州ブレイブウォリアーズ), ORG000155
# (島根スサノオマジック), ORG000173 (岩手ビッグブルズ) already exist and are
# reused -- checked against master + every candidate
# organization_candidates.csv before writing this file. 開志国際高等学校・
# 大阪産業大学 confirmed genuinely new; current max existing Organization ID
# is ORG000191 (batch_010/wave_04), so these are ORG000192-000193.
ORGANIZATIONS = [
    {"organization_id": "ORG000192", "name": "開志国際高等学校"},
    {"organization_id": "ORG000018", "name": "専修大学"},
    {"organization_id": "ORG000155", "name": "島根スサノオマジック"},
    {"organization_id": "ORG000193", "name": "大阪産業大学"},
    {"organization_id": "ORG000150", "name": "信州ブレイブウォリアーズ"},
    {"organization_id": "ORG000173", "name": "岩手ビッグブルズ"},
]

CAREERS = [
    # 介川アンソニー翔（現所属クラブがB.LEAGUEデビュー先、2024-25〜）
    {"career_id": "C000514", "person_id": "P000153", "organization_id": "ORG000192", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000515", "person_id": "P000153", "organization_id": "ORG000018", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000516", "person_id": "P000153", "organization_id": "ORG000155", "role": "Player", "start": "2024", "end": ""},
    # 小栗瑛哉（現所属は信州、2025-26〜。それ以前の金沢・秋田在籍はissue参照）
    {"career_id": "C000517", "person_id": "P000154", "organization_id": "ORG000192", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000518", "person_id": "P000154", "organization_id": "ORG000193", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000519", "person_id": "P000154", "organization_id": "ORG000150", "role": "Player", "start": "2025", "end": ""},
    # 平良宗龍（大学経由なし、高校→現所属クラブ。過去の琉球練習生歴はissue参照）
    {"career_id": "C000520", "person_id": "P000155", "organization_id": "ORG000192", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000521", "person_id": "P000155", "organization_id": "ORG000173", "role": "Player", "start": "2025", "end": ""},
]

SOURCES = [
    {"source_id": "B11W1S0001", "title": "ワタシノB.LEAGUE選手一覧 | 開志国際高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:開志国際高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B11W1S0002", "title": "介川アンソニー翔 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000458", "accessed_at": CHECKED_AT},
    {"source_id": "B11W1S0003", "title": "小栗瑛哉 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=42539", "accessed_at": CHECKED_AT},
    {"source_id": "B11W1S0004", "title": "平良宗龍 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=55000079", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B11W1E{_evidence_seq:04d}",
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


# --- 介川アンソニー翔 ---
add_evidence("Person", "P000153", "name", "介川 アンソニー翔", "B11W1S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000153", "birth_date", "2004-03-30", "B11W1S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000514", "organization_id", "ORG000192", "B11W1S0001", "TagID=35（開志国際高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000515", "organization_id", "ORG000018", "B11W1S0002", "基本情報 > 出身校：専修大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000516", "organization_id", "ORG000155", "B11W1S0002", "クラブ経歴 > 「2024-25：島根」が初出（唯一の在籍クラブ）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000516", "start", "2024", "B11W1S0002", "クラブ経歴 > 「2024-25：島根」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 小栗瑛哉 ---
add_evidence("Person", "P000154", "name", "小栗 瑛哉", "B11W1S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000154", "birth_date", "2001-03-01", "B11W1S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000517", "organization_id", "ORG000192", "B11W1S0001", "TagID=35（開志国際高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000518", "organization_id", "ORG000193", "B11W1S0003", "基本情報 > 出身校：大阪産業大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000519", "organization_id", "ORG000150", "B11W1S0003", "クラブ経歴 > 「2025-26：信州」が初出", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="それ以前（2022-23〜2024-25）の金沢・秋田在籍は今回のWaveでは対象外。詳細はissue B11W1I0004を参照")
add_evidence("Career", "C000519", "start", "2025", "B11W1S0003", "クラブ経歴 > 「2025-26：信州」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 平良宗龍 ---
add_evidence("Person", "P000155", "name", "平良 宗龍", "B11W1S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000155", "birth_date", "2006-05-26", "B11W1S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000520", "organization_id", "ORG000192", "B11W1S0001", "TagID=35（開志国際高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED")
add_evidence("Career", "C000521", "organization_id", "ORG000173", "B11W1S0004", "クラブ経歴 > 「2025-26：岩手」が初出（唯一の現在の在籍クラブ）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="2022-23シーズンに琉球ゴールデンキングスで練習生として1試合出場の記録があるが、今回のWaveでは現所属クラブのみを対象とした。詳細はissue B11W1I0005を参照")
add_evidence("Career", "C000521", "start", "2025", "B11W1S0004", "クラブ経歴 > 「2025-26：岩手」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B11W1D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000153", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000514", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000515", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000516", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000154", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000517", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000518", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000519", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去クラブ在籍はissueに記録")

add_decision("Person", "P000155", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000520", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認、在籍期間は未確認")
add_decision("Career", "C000521", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去の練習生歴はissueに記録")

ISSUES = [
    {"issue_id": "B11W1I0001", "person_id": "P000153|P000154|P000155", "related_id": "C000514|C000517|C000520", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "3名とも開志国際高等学校在籍そのものは出身校タグ一覧で確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B11W1I0002", "person_id": "P000153|P000154", "related_id": "C000515|C000518", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "2名とも大学在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B11W1I0003", "person_id": "P000153", "related_id": "P000153", "issue_type": "DATA_QUALITY_NOTE", "status": "HOLD",
     "description": "介川アンソニー翔はB.LEAGUE公式プロフィール記載の身長・体重・ポジション（SF/PF、197cm/93kg）を今回のWaveでは未登録（本プロジェクトの既存Personスキーマではname/birth_dateのみを対象としており、他の2校のWaveでも同様の扱い）。",
     "next_check": "身長・体重・ポジション等の追加項目をスキーマに含めるか検討（Yuichiの判断が必要）"},
    {"issue_id": "B11W1I0004", "person_id": "P000154", "related_id": "P000154", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "小栗瑛哉は現所属（信州ブレイブウォリアーズ、2025-26〜）以前に金沢（2022-23、金沢武士団とみられる）、秋田ノーザンハピネッツ（ORG000137、2022-23〜2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。金沢の正式クラブ名（金沢武士団と推定）は今回未確認のため、Organization未登録。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加（金沢の正式クラブ名を確認のうえ）"},
    {"issue_id": "B11W1I0005", "person_id": "P000155", "related_id": "P000155", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "平良宗龍は現所属（岩手ビッグブルズ、2025-26〜）以前に琉球ゴールデンキングス（ORG000106）で2022-23シーズンに練習生として1試合出場した記録がB.LEAGUE公式の個人成績で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveで練習生期間のCareerを追加するか検討（1試合のみの出場のため優先度は低）"},
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
        f"Wrote batch_011/wave_01: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
