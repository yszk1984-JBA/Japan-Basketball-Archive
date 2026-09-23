#!/usr/bin/env python3
"""Build Batch 004 Wave 6 (深掘りWave / Enrichment Wave).

Per Yuichi's instruction "はい、深掘りで" (Wave 8 of the overall cadence,
enrichment following 3 acquisition waves: batch_007 wave_05/06/07).

Target: 重冨周希 (P000068, already MASTER) -- resolves issue
B4W3I0003 (CLUB_HISTORY_GAP): "B.LEAGUEプロフィールに2024-25・2025-26湘南
の履歴が表示されず、2026-27のみ確認".

Finding: Master ORG000050 is registered as "ウォルガ湘南" -- but this is
the club's NEW name, adopted only from the 2026-27 season (announced
2026-05-23). The club's name during the 2024-25 and 2025-26 seasons
(when 重冨周希 actually joined and played) was "湘南ユナイテッドBC". Per
the historical-organization-naming rule, the Career covering those two
seasons must reference the OLD name, not overwrite/reuse ORG000050 under
the current name. So this wave registers 湘南ユナイテッドBC as a new,
separate Organization candidate and adds one new Career for it
(2024-2026), leaving the existing Master Career C000235 (ORG000050
ウォルガ湘南, i.e. 2026-27-and-on) untouched.

This is the same underlying pattern as サンロッカーズ渋谷->東京サンロッ
カーズ (batch_007/wave_02) and is logged as another instance of the
still-unresolved OrganizationAlias/組織承継 issue chain
(B4W3I0011 -> B7I0013 -> B7I0022 -> B7I0023 -> B7I0024).
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_004" / "wave_06"

PERSONS: list[dict] = []  # enrichment wave: no new persons

ORGANIZATIONS = [
    {"organization_id": "ORG000163", "name": "湘南ユナイテッドBC"},
]

CAREERS = [
    {"career_id": "C000365", "person_id": "P000068", "organization_id": "ORG000163", "role": "Player", "start": "2024", "end": "2026"},
]

SOURCES = [
    {
        "source_id": "B4W6S0001",
        "title": "福岡第一出身の重冨周希がB2福岡からB3湘南へ移籍「さらに活躍する姿を…」双子“直接対決”の可能性も",
        "publisher": "バスケットボールキング",
        "url": "https://basketballking.jp/news/japan/b2/20240701/494746.html",
        "accessed_at": "2026-09-23",
    },
    {
        "source_id": "B4W6S0002",
        "title": "重冨周希 選手 契約（継続）合意",
        "publisher": "B3リーグ 湘南ユナイテッドBC公式サイト",
        "url": "https://shonan-united.com/news/20250603-01/",
        "accessed_at": "2026-09-23",
    },
    {
        "source_id": "B4W6S0003",
        "title": "2026-27シーズンよりクラブ名称変更のお知らせ",
        "publisher": "B3リーグ 湘南ユナイテッドBC公式サイト",
        "url": "https://shonan-united.com/news/20260523-01/",
        "accessed_at": "2026-09-23",
    },
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B4W6E{_evidence_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "field_name": field_name,
        "candidate_value": candidate_value,
        "source_id": source_id,
        "source_locator": source_locator,
        "evidence_summary": evidence_summary,
        "assessment": assessment,
        "checked_at": "2026-09-23",
        "issue_note": issue_note,
    })


add_evidence(
    "Career", "C000365", "organization_id", "ORG000163", "B4W6S0001",
    "本文 > 「B3リーグの湘南ユナイテッドBCは7月1日、B2リーグのライジングゼファー福岡から自由交渉選手リストに公示されていた重冨周希と、2024－25シーズンの新規選手契約に合意したと発表した」",
    "バスケットボールキングの移籍報道（2024年7月1日付）で、湘南ユナイテッドBC（当時の正式クラブ名）との2024-25シーズン新規契約を確認",
    "SUPPORTED",
)
add_evidence(
    "Career", "C000365", "start", "2024", "B4W6S0001",
    "同上（2024年7月1日付、2024-25シーズン新規契約発表）",
    "移籍発表の時期から開始年（2024）を確認",
    "SUPPORTED",
)
add_evidence(
    "Career", "C000365", "organization_id", "ORG000163", "B4W6S0002",
    "所属履歴 > 「2024- 湘南ユナイテッドBC」／本文 > 「重冨周希 選手との2025-26シーズンの契約（継続）が合意に至りましたのでお知らせいたします」",
    "湘南ユナイテッドBC公式サイトの契約継続発表（2025年6月3日付、独立した第2ソース）で、2024年からの継続所属および2025-26シーズンの契約継続を確認",
    "SUPPORTED",
)
add_evidence(
    "Career", "C000365", "end", "2026", "B4W6S0003",
    "本文 > 「湘南ユナイテッドBCは、2026-27シーズンよりクラブ名称を「ウォルガ湘南」へ変更いたします」（2026年5月23日付発表）",
    "クラブ公式の名称変更発表により、「湘南ユナイテッドBC」という組織名が2026-27シーズンより「ウォルガ湘南」に置き換わることを確認。重冨周希個人の退団を示す資料ではなく、組織名自体の変更時期からの導出のためPARTIAL評価",
    "PARTIAL",
    issue_note="endは重冨周希個人の移籍等ではなく、組織の名称変更時期（2026-27シーズンより）から導出した値。同選手はウォルガ湘南への改称後も引き続き在籍している可能性が高く、既存Master Career C000235（ORG000050 ウォルガ湘南）が改称後の所属を表す",
)


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B4W6D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": "2026-09-23",
    })


DECISIONS: list[dict] = []
_decision_seq = 0

add_decision(
    "Career", "C000365", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end",
    "バスケットボールキング（2024-07-01移籍報道）と湘南ユナイテッドBC公式サイト（2025-06-03契約継続発表）の独立した2ソースにより、"
    "重冨周希が2024年から湘南ユナイテッドBC（当時の正式名称）に所属していたことを確認。issue B4W3I0003（2024-25・2025-26シーズンの"
    "履歴がB.LEAGUE公式プロフィールに表示されない問題）を解消。endはクラブの名称変更時期（2026-27シーズンより）からの導出でPARTIAL評価のため保留",
)

ISSUES = [
    {
        "issue_id": "B4W6I0001",
        "category": "CLUB_SUCCESSION",
        "scope": "P000068",
        "description": (
            "湘南ユナイテッドBC（本Waveで新規登録、ORG000163）と、Master登録済みのORG000050（ウォルガ湘南）は、"
            "2026-27シーズンのクラブ名称変更（2026年5月23日発表）前後における同一組織である。"
            "サンロッカーズ渋谷->東京サンロッカーズ（batch_007/wave_02、issue B7I0013等）と同種の事例。"
            "OrganizationAlias/組織承継の仕組みが未整備のため、本Waveでは2つの独立したOrganizationとして登録し、"
            "重冨周希のCareerを名称ごとに分割した（C000365：湘南ユナイテッドBC 2024-2026、Master C000235：ウォルガ湘南 2026-）。"
            "Yuichiが組織承継ルールを決定した際に、両者の関係整理が必要。"
        ),
    },
]


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    write_csv(BASE / "person_candidates.csv", PERSONS, ["person_id", "name"])
    write_csv(BASE / "organization_candidates.csv", ORGANIZATIONS, ["organization_id", "name"])
    write_csv(BASE / "career_candidates.csv", CAREERS, ["career_id", "person_id", "organization_id", "role", "start", "end"])
    write_csv(BASE / "source_references.csv", SOURCES, ["source_id", "title", "publisher", "url", "accessed_at"])
    write_csv(BASE / "evidence_records.csv", EVIDENCE, [
        "record_id", "entity_type", "entity_id", "field_name", "candidate_value",
        "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note",
    ])
    write_csv(BASE / "issues.csv", ISSUES, ["issue_id", "category", "scope", "description"])
    write_csv(BASE / "qa_decisions.csv", DECISIONS, [
        "decision_id", "entity_type", "entity_id", "decision",
        "eligible_fields", "held_fields", "reason", "reviewed_at",
    ])
    print(
        f"Wrote wave_06: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
