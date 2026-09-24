#!/usr/bin/env python3
"""Build Batch 015 Wave 1 (藤枝明誠高等学校, school 8/11) CANDIDATE data.

Eighth school of the powerhouse-school expansion initiative (see
docs/BATCH_008_PROPOSAL.md). 藤枝明誠高等学校 (Shizuoka) has no existing
Organization ID -- newly minted here as ORG000204.

Discovery: B.LEAGUE's "ワタシノB.LEAGUE" tag list for
TagID=35:藤枝明誠高等学校 was accessed directly. It shows exactly 6
current alumni -- no "もっと見る" pagination needed. All 6 are genuinely
new to the project. Standard 4/wave sizing applies, so this school
spans 2 waves; this is Wave 1 of 2 (石橋永遠, 菊地広人, 藤井祐眞,
富田一成).

Per the batch's approved scope, only the current club is registered as
Pro career (minimal path); prior clubs are logged as PRO_HISTORY_GAPS
issues.

Notable: 富田一成's current club is 金沢サムライズ (newly registered here
as ORG000205). This may be the same real-world club that earlier
batches (batch_011's 小栗瑛哉, batch_014's 小川翔矢) referred to only as
an unconfirmed "金沢" (speculatively "金沢武士団") in PRO_HISTORY_GAPS
issue text -- but since those issues did not register any Organization
for it, and the exact relationship between "金沢武士団" and "金沢
サムライズ" (rename, merger, or two distinct clubs) is not confirmed
here, no retroactive change is made to those earlier issues. This is
noted for a future enrichment wave to investigate.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_015" / "wave_01"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000180", "name": "石橋 永遠"},
    {"person_id": "P000181", "name": "菊地 広人"},
    {"person_id": "P000182", "name": "藤井 祐眞"},
    {"person_id": "P000183", "name": "富田 一成"},
]

# ORG000031(拓殖大学)・ORG000111(東京八王子ビートレインズ)・
# ORG000128(大東文化大学)・ORG000092(レバンガ北海道)・
# ORG000143(群馬クレインサンダーズ)・ORG000124(明治大学) は既存
# Organizationとして再利用 -- master + 全candidateのorganization_
# candidates.csvと突き合わせ済み。藤枝明誠高等学校・金沢サムライズは
# 新規登録（現在の最大既存Organization IDはORG000203、batch_014のため
# ORG000204-205とした）。
ORGANIZATIONS = [
    {"organization_id": "ORG000204", "name": "藤枝明誠高等学校"},
    {"organization_id": "ORG000031", "name": "拓殖大学"},
    {"organization_id": "ORG000111", "name": "東京八王子ビートレインズ"},
    {"organization_id": "ORG000128", "name": "大東文化大学"},
    {"organization_id": "ORG000092", "name": "レバンガ北海道"},
    {"organization_id": "ORG000143", "name": "群馬クレインサンダーズ"},
    {"organization_id": "ORG000124", "name": "明治大学"},
    {"organization_id": "ORG000205", "name": "金沢サムライズ"},
]

CAREERS = [
    # 石橋永遠（B.LEAGUEデビューから一貫して東京八王子ビートレインズ、
    # 移籍・空白なし）
    {"career_id": "C000593", "person_id": "P000180", "organization_id": "ORG000204", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000594", "person_id": "P000180", "organization_id": "ORG000031", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000595", "person_id": "P000180", "organization_id": "ORG000111", "role": "Player", "start": "2025", "end": ""},
    # 菊地広人（B.LEAGUEデビューから一貫してレバンガ北海道、移籍・
    # 空白なし）
    {"career_id": "C000596", "person_id": "P000181", "organization_id": "ORG000204", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000597", "person_id": "P000181", "organization_id": "ORG000128", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000598", "person_id": "P000181", "organization_id": "ORG000092", "role": "Player", "start": "2023", "end": ""},
    # 藤井祐眞（現所属は群馬クレインサンダーズ、2024-25〜。過去在籍歴の
    # ない新規加入。旧川崎在籍（8シーズン）はissue参照）
    {"career_id": "C000599", "person_id": "P000182", "organization_id": "ORG000204", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000600", "person_id": "P000182", "organization_id": "ORG000031", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000601", "person_id": "P000182", "organization_id": "ORG000143", "role": "Player", "start": "2024", "end": ""},
    # 富田一成（現所属は金沢サムライズ、2025-26〜。過去在籍歴のない
    # 新規加入。山口パッツファイブ在籍はissue参照）
    {"career_id": "C000602", "person_id": "P000183", "organization_id": "ORG000204", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000603", "person_id": "P000183", "organization_id": "ORG000124", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000604", "person_id": "P000183", "organization_id": "ORG000205", "role": "Player", "start": "2025", "end": ""},
]

SOURCES = [
    {"source_id": "B15W1S0001", "title": "ワタシノB.LEAGUE選手一覧 | 藤枝明誠高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:藤枝明誠高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B15W1S0002", "title": "石橋永遠 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=52462", "accessed_at": CHECKED_AT},
    {"source_id": "B15W1S0003", "title": "菊地広人 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000350", "accessed_at": CHECKED_AT},
    {"source_id": "B15W1S0004", "title": "藤井祐眞 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8482", "accessed_at": CHECKED_AT},
    {"source_id": "B15W1S0005", "title": "富田一成 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=36969", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B15W1E{_evidence_seq:04d}",
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


# --- 石橋永遠 ---
add_evidence("Person", "P000180", "name", "石橋 永遠", "B15W1S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000180", "birth_date", "2002-07-28", "B15W1S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000593", "organization_id", "ORG000204", "B15W1S0002", "基本情報 > 出身校（高）：藤枝明誠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000594", "organization_id", "ORG000031", "B15W1S0002", "基本情報 > 出身校（大）：拓殖大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000595", "organization_id", "ORG000111", "B15W1S0002", "クラブ経歴 > 「2025-26：八王子」が初出（唯一の在籍クラブ）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000595", "start", "2025", "B15W1S0002", "クラブ経歴 > 「2025-26：八王子」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 菊地広人 ---
add_evidence("Person", "P000181", "name", "菊地 広人", "B15W1S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000181", "birth_date", "2001-10-05", "B15W1S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000596", "organization_id", "ORG000204", "B15W1S0003", "基本情報 > 出身校（高）：藤枝明誠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000597", "organization_id", "ORG000128", "B15W1S0003", "基本情報 > 出身校（大）：大東文化大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000598", "organization_id", "ORG000092", "B15W1S0003", "クラブ経歴 > 「2023-24：北海道」が初出（唯一の在籍クラブ）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000598", "start", "2023", "B15W1S0003", "クラブ経歴 > 「2023-24：北海道」が初出", "B.LEAGUE公式のクラブ所属履歴で2023-24シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 藤井祐眞 ---
add_evidence("Person", "P000182", "name", "藤井 祐眞", "B15W1S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000182", "birth_date", "1991-12-23", "B15W1S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000599", "organization_id", "ORG000204", "B15W1S0004", "基本情報 > 出身校（高）：藤枝明誠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000600", "organization_id", "ORG000031", "B15W1S0004", "基本情報 > 出身校（大）：拓殖大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000601", "organization_id", "ORG000143", "B15W1S0004", "クラブ経歴 > 「2024-25：群馬」が最新（新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="川崎ブレイブサンダース（2016-17〜2023-24、8シーズン）在籍は今回のWaveでは対象外。詳細はissue B15W1I0003を参照")
add_evidence("Career", "C000601", "start", "2024", "B15W1S0004", "クラブ経歴 > 「2024-25：群馬」が最新", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入を確認", "SUPPORTED")

# --- 富田一成 ---
add_evidence("Person", "P000183", "name", "富田 一成", "B15W1S0005", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000183", "birth_date", "1998-12-28", "B15W1S0005", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000602", "organization_id", "ORG000204", "B15W1S0005", "基本情報 > 出身校（高）：藤枝明誠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000603", "organization_id", "ORG000124", "B15W1S0005", "基本情報 > 出身校（大）：明治大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000604", "organization_id", "ORG000205", "B15W1S0005", "クラブ経歴 > 「2025-26：金沢」が最新（新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="山口パッツファイブ（2021-22〜2024-25）在籍は今回のWaveでは対象外。詳細はissue B15W1I0004を参照")
add_evidence("Career", "C000604", "start", "2025", "B15W1S0005", "クラブ経歴 > 「2025-26：金沢」が最新", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B15W1D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


for pid, cids in [
    ("P000180", ["C000593", "C000594", "C000595"]),
    ("P000181", ["C000596", "C000597", "C000598"]),
    ("P000182", ["C000599", "C000600", "C000601"]),
    ("P000183", ["C000602", "C000603", "C000604"]),
]:
    add_decision("Person", pid, "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
    add_decision("Career", cids[0], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[1], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[2], "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去クラブ在籍はissueに記録")

ISSUES = [
    {"issue_id": "B15W1I0001", "person_id": "P000180|P000181|P000182|P000183", "related_id": "C000593|C000596|C000599|C000602", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "4名とも藤枝明誠高等学校在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B15W1I0002", "person_id": "P000180|P000181|P000182|P000183", "related_id": "C000594|C000597|C000600|C000603", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "4名とも大学在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B15W1I0003", "person_id": "P000182", "related_id": "P000182", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "藤井祐眞は現所属（群馬クレインサンダーズ、2024-25〜、新規加入）以前に川崎ブレイブサンダース（2016-17〜2023-24、8シーズン）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B15W1I0004", "person_id": "P000183", "related_id": "P000183", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "富田一成は現所属（金沢サムライズ、2025-26〜、新規加入）以前に山口パッツファイブ（2021-22〜2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
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
        f"Wrote batch_015/wave_01: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
