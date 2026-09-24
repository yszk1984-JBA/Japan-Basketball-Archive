#!/usr/bin/env python3
"""Build Batch 014 Wave 1 (北陸高等学校, school 7/11) CANDIDATE data.

Seventh school of the powerhouse-school expansion initiative (see
docs/BATCH_008_PROPOSAL.md). Unlike the previous three schools,
北陸高等学校 already has an existing Organization ID (ORG000120,
registered in an earlier batch) -- confirmed by checking
data/master/organization.csv before writing this file, so no new
Organization is minted for the school itself here.

Discovery: B.LEAGUE's "ワタシノB.LEAGUE" tag list for TagID=35:北陸高等学校
was accessed directly (per the pattern from batch_011-013). It shows
exactly 15 current alumni -- no "もっと見る" pagination needed. All 15
are genuinely new to the project (checked against data/master/person.csv
and every existing person_candidates.csv), including 五十嵐圭 (the
school's most notable alumnus per docs/BATCH_008_PROPOSAL.md's
selection rationale) who does NOT appear on the current tag list --
presumably because he is no longer an actively registered B.LEAGUE
player, and is therefore out of scope for this initiative (which only
targets currently active B.LEAGUE players).

15 people is above the standard 4/wave size, so this school spans 4
waves (4+4+4+3); this is Wave 1 of 4 (高島紳司, 野本建吾, 大﨑翔太,
多嶋朝飛).

Per the batch's approved scope, only the current club is registered as
Pro career (minimal path: high school -> university -> current club);
prior clubs are logged as PRO_HISTORY_GAPS issues instead of being
added as Career rows.

Notable: 野本建吾 is a case of returning to a club he had already
played for (川崎, 2016-17/2017-18) after two other clubs (秋田, 群馬) --
per the existing convention for same-club returns (see 藤澤尚之,
batch_013), the current stint's start year is the return year (2025).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_014" / "wave_01"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000165", "name": "高島 紳司"},
    {"person_id": "P000166", "name": "野本 建吾"},
    {"person_id": "P000167", "name": "大﨑 翔太"},
    {"person_id": "P000168", "name": "多嶋 朝飛"},
]

# ORG000120（北陸高等学校）は既に登録済みのため再利用（新規登録なし）。
# ORG000128(大東文化大学)・ORG000030(青山学院大学)・ORG000122(川崎ブレイブ
# サンダース)・ORG000115(立川ダイス)・ORG000016(中央大学)・ORG000183
# (さいたまブロンコス)・ORG000015(東海大学) も既存Organizationとして再利用
# -- master + 全candidateのorganization_candidates.csvと突き合わせ済み。
# 新規Organizationはこのwaveにはない。
ORGANIZATIONS = [
    {"organization_id": "ORG000120", "name": "北陸高等学校"},
    {"organization_id": "ORG000128", "name": "大東文化大学"},
    {"organization_id": "ORG000047", "name": "宇都宮ブレックス"},
    {"organization_id": "ORG000122", "name": "川崎ブレイブサンダース"},
    {"organization_id": "ORG000030", "name": "青山学院大学"},
    {"organization_id": "ORG000115", "name": "立川ダイス"},
    {"organization_id": "ORG000016", "name": "中央大学"},
    {"organization_id": "ORG000183", "name": "さいたまブロンコス"},
    {"organization_id": "ORG000015", "name": "東海大学"},
]

CAREERS = [
    # 高島紳司（現所属は宇都宮ブレックス、2022-23〜継続。旧大阪在籍はissue参照）
    {"career_id": "C000548", "person_id": "P000165", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000549", "person_id": "P000165", "organization_id": "ORG000128", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000550", "person_id": "P000165", "organization_id": "ORG000047", "role": "Player", "start": "2022", "end": ""},
    # 野本建吾（現所属は川崎ブレイブサンダースへの復帰、2025-26〜。秋田・
    # 群馬・旧川崎在籍はissue参照）
    {"career_id": "C000551", "person_id": "P000166", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000552", "person_id": "P000166", "organization_id": "ORG000030", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000553", "person_id": "P000166", "organization_id": "ORG000122", "role": "Player", "start": "2025", "end": ""},
    # 大﨑翔太（現所属は立川ダイス、2025-26〜継続。島根・愛媛・横浜EX・
    # 岩手・徳島在籍はissue参照）
    {"career_id": "C000554", "person_id": "P000167", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000555", "person_id": "P000167", "organization_id": "ORG000016", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000556", "person_id": "P000167", "organization_id": "ORG000115", "role": "Player", "start": "2025", "end": ""},
    # 多嶋朝飛（現所属はさいたまブロンコス、2025-26〜継続。北海道・茨城・
    # 大阪・仙台在籍はissue参照）
    {"career_id": "C000557", "person_id": "P000168", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000558", "person_id": "P000168", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000559", "person_id": "P000168", "organization_id": "ORG000183", "role": "Player", "start": "2025", "end": ""},
]

SOURCES = [
    {"source_id": "B14W1S0001", "title": "ワタシノB.LEAGUE選手一覧 | 北陸高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:北陸高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B14W1S0002", "title": "高島紳司 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=5100000036", "accessed_at": CHECKED_AT},
    {"source_id": "B14W1S0003", "title": "野本建吾 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8486", "accessed_at": CHECKED_AT},
    {"source_id": "B14W1S0004", "title": "大﨑翔太 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=30516", "accessed_at": CHECKED_AT},
    {"source_id": "B14W1S0005", "title": "多嶋朝飛 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8507", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B14W1E{_evidence_seq:04d}",
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


# --- 高島紳司 ---
add_evidence("Person", "P000165", "name", "高島 紳司", "B14W1S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000165", "birth_date", "2000-10-13", "B14W1S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000548", "organization_id", "ORG000120", "B14W1S0002", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000549", "organization_id", "ORG000128", "B14W1S0002", "基本情報 > 出身校（大）：大東文化大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000550", "organization_id", "ORG000047", "B14W1S0002", "クラブ経歴 > 「2022-23：宇都宮」以降継続", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="それ以前（2020-21・2021-22）の大阪在籍は今回のWaveでは対象外。詳細はissue B14W1I0003を参照")
add_evidence("Career", "C000550", "start", "2022", "B14W1S0002", "クラブ経歴 > 「2022-23：宇都宮」が初出", "B.LEAGUE公式のクラブ所属履歴で2022-23シーズンからの加入を確認", "SUPPORTED")

# --- 野本建吾 ---
add_evidence("Person", "P000166", "name", "野本 建吾", "B14W1S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000166", "birth_date", "1992-04-25", "B14W1S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000551", "organization_id", "ORG000120", "B14W1S0003", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000552", "organization_id", "ORG000030", "B14W1S0003", "基本情報 > 出身校（大）：青山学院大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000553", "organization_id", "ORG000122", "B14W1S0003", "クラブ経歴 > 「2025-26：川崎」が復帰後の初出", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの復帰を確認", "SUPPORTED",
             issue_note="旧川崎在籍（2016-17・2017-18）、秋田（2018-19〜2020-21）、群馬（2021-22〜2024-25）在籍は今回のWaveでは対象外。詳細はissue B14W1I0004を参照")
add_evidence("Career", "C000553", "start", "2025", "B14W1S0003", "クラブ経歴 > 「2025-26：川崎」が復帰後の初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの川崎復帰を確認", "SUPPORTED")

# --- 大﨑翔太 ---
add_evidence("Person", "P000167", "name", "大﨑 翔太", "B14W1S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000167", "birth_date", "1998-01-23", "B14W1S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000554", "organization_id", "ORG000120", "B14W1S0004", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000555", "organization_id", "ORG000016", "B14W1S0004", "基本情報 > 出身校（大）：中央大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000556", "organization_id", "ORG000115", "B14W1S0004", "クラブ経歴 > 「2025-26：立川」以降継続", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="島根（2019-20）、愛媛（2020-21）、横浜エクセレンス（2021-22・2022-23）、岩手（2023-24）、徳島（2024-25）在籍は今回のWaveでは対象外。詳細はissue B14W1I0005を参照")
add_evidence("Career", "C000556", "start", "2025", "B14W1S0004", "クラブ経歴 > 「2025-26：立川」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 多嶋朝飛 ---
add_evidence("Person", "P000168", "name", "多嶋 朝飛", "B14W1S0005", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000168", "birth_date", "1988-10-08", "B14W1S0005", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000557", "organization_id", "ORG000120", "B14W1S0005", "基本情報 > 出身校（高）：北陸高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000558", "organization_id", "ORG000015", "B14W1S0005", "基本情報 > 出身校（大）：東海大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000559", "organization_id", "ORG000183", "B14W1S0005", "クラブ経歴 > 「2025-26：埼玉」以降継続", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="北海道（2016-17〜2020-21）、茨城（2021-22・2022-23）、大阪（2023-24）、仙台（2024-25）在籍は今回のWaveでは対象外。詳細はissue B14W1I0006を参照")
add_evidence("Career", "C000559", "start", "2025", "B14W1S0005", "クラブ経歴 > 「2025-26：埼玉」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B14W1D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


for pid, cids in [
    ("P000165", ["C000548", "C000549", "C000550"]),
    ("P000166", ["C000551", "C000552", "C000553"]),
    ("P000167", ["C000554", "C000555", "C000556"]),
    ("P000168", ["C000557", "C000558", "C000559"]),
]:
    add_decision("Person", pid, "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
    add_decision("Career", cids[0], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[1], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[2], "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去クラブ在籍はissueに記録")

ISSUES = [
    {"issue_id": "B14W1I0001", "person_id": "P000165|P000166|P000167|P000168", "related_id": "C000548|C000551|C000554|C000557", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "4名とも北陸高等学校在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B14W1I0002", "person_id": "P000165|P000166|P000167|P000168", "related_id": "C000549|C000552|C000555|C000558", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "4名とも大学在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B14W1I0003", "person_id": "P000165", "related_id": "P000165", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "高島紳司は現所属（宇都宮ブレックス、2022-23〜）以前に大阪（2020-21・2021-22）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B14W1I0004", "person_id": "P000166", "related_id": "P000166", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "野本建吾は現所属（川崎ブレイブサンダース、2025-26〜）が2016-17・2017-18シーズンに一度在籍したクラブへの復帰であり、その間に秋田（2018-19〜2020-21）、群馬（2021-22〜2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できる。今回のWaveでは現在の川崎復帰後の在籍のみを最小経路として登録し、過去クラブおよび最初の川崎在籍は対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加（最初の川崎在籍を含む）"},
    {"issue_id": "B14W1I0005", "person_id": "P000167", "related_id": "P000167", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "大﨑翔太は現所属（立川ダイス、2025-26〜）以前に島根（2019-20）、愛媛（2020-21）、横浜エクセレンス（2021-22・2022-23）、岩手ビッグブルズ（2023-24）、徳島ガンバロウズ（2024-25）と5クラブを渡り歩くプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B14W1I0006", "person_id": "P000168", "related_id": "P000168", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "多嶋朝飛は現所属（さいたまブロンコス、2025-26〜）以前に北海道（2016-17〜2020-21）、茨城ロボッツ（2021-22・2022-23）、大阪エヴェッサ（2023-24）、仙台89ERS（2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
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
        f"Wrote batch_014/wave_01: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
