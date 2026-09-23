#!/usr/bin/env python3
"""Build Batch 007 Wave 6 (新規開拓Wave / Acquisition Wave) candidate data.

Cadence: Wave 5 was the 1st of 3 acquisition waves following Wave 4/4b's
enrichment. This is the 2nd.

Target selection: re-ran the 26-club B.PREMIER 2026-27 coverage check from
Wave 5, this time correcting for a club rename that the earlier check
missed -- サンロッカーズ渋谷 renamed to 東京サンロッカーズ for 2026-27, and
that name (ORG000114) was ALREADY covered via 田中大貴 (batch_007/wave_02),
so it was never actually an uncovered club; Wave 5's README overcounted the
uncovered list by one for this reason. With the corrected club-name list,
exactly 4 clubs remain with zero current-roster coverage, and this wave
covers all 4: 富山グラウジーズ、信州ブレイブウォリアーズ、滋賀レイクス、
島根スサノオマジック -- meaning after this wave, all 26 B.PREMIER 2026-27
clubs have at least one current-roster player in the archive.

Methodology matches Wave 3/5: one veteran/well-documented player per club,
B.LEAGUE公式選手プロフィール as the primary source, current-club-only Career
scope (past clubs deferred, same as issue B7I0013/B7I0022). Two of the four
players (水戸健史, 古川孝敏) genuinely have no high school listed on their
official profile (one shows an explicit "-", the other omits the field
entirely) -- left unrecorded rather than guessed, per governance.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_007" / "wave_06"

PERSONS = [
    {"person_id": "P000099", "name": "水戸健史"},
    {"person_id": "P000100", "name": "古川孝敏"},
    {"person_id": "P000101", "name": "田原隆徳"},
    {"person_id": "P000102", "name": "白濱僚祐"},
]

ORGANIZATIONS = [
    {"organization_id": "ORG000148", "name": "近畿大学"},
    {"organization_id": "ORG000149", "name": "富山グラウジーズ"},
    {"organization_id": "ORG000015", "name": "東海大学"},
    {"organization_id": "ORG000150", "name": "信州ブレイブウォリアーズ"},
    {"organization_id": "ORG000151", "name": "北海道恵庭南高等学校"},
    {"organization_id": "ORG000152", "name": "札幌大学"},
    {"organization_id": "ORG000153", "name": "滋賀レイクス"},
    {"organization_id": "ORG000154", "name": "佐賀県立佐賀北高等学校"},
    {"organization_id": "ORG000093", "name": "白鷗大学"},
    {"organization_id": "ORG000155", "name": "島根スサノオマジック"},
]

CAREERS = [
    {"career_id": "C000343", "person_id": "P000099", "organization_id": "ORG000148", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000344", "person_id": "P000099", "organization_id": "ORG000149", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000345", "person_id": "P000100", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000346", "person_id": "P000100", "organization_id": "ORG000150", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000347", "person_id": "P000101", "organization_id": "ORG000151", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000348", "person_id": "P000101", "organization_id": "ORG000152", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000349", "person_id": "P000101", "organization_id": "ORG000153", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000350", "person_id": "P000102", "organization_id": "ORG000154", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000351", "person_id": "P000102", "organization_id": "ORG000093", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000352", "person_id": "P000102", "organization_id": "ORG000155", "role": "Player", "start": "", "end": ""},
]

SOURCES = [
    {"source_id": "B7S0043", "title": "水戸健史 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8501", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0044", "title": "古川孝敏 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8500", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0045", "title": "田原隆徳 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=10297", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0046", "title": "白濱僚祐 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8734", "accessed_at": "2026-09-23"},
]

EVIDENCE: list[dict] = []
_evidence_seq = 162  # last used in wave_05 was B7E0162


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B7E{_evidence_seq:04d}",
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


# --- 水戸健史 (P000099, B7S0043) ---
add_evidence("Person", "P000099", "name", "水戸健史", "B7S0043", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED")
add_evidence("Person", "P000099", "birth_date", "1985-04-23", "B7S0043", "基本情報 > 生年月日1985年4月23日", "B.LEAGUE公式の生年月日", "SUPPORTED")
add_evidence("Career", "C000343", "organization_id", "ORG000148", "B7S0043", "プロフィール > 出身校（大）：近畿大学", "B.LEAGUE公式プロフィールの大学欄。出身校（高）欄は「-」で高校名の記載なし", "SUPPORTED", issue_note="出身高校はプロフィール上「-」で未記載のため登録せず")
add_evidence("Career", "C000343", "role", "Player", "B7S0043", "プロフィール > 出身校（大）", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000344", "organization_id", "ORG000149", "B7S0043", "クラブ所属履歴 > 2026-27 富山（2016-17シーズンより継続）", "B.LEAGUE公式のクラブ所属履歴（現所属）", "SUPPORTED")
add_evidence("Career", "C000344", "role", "Player", "B7S0043", "クラブ所属履歴 > 2026-27 富山", "選手として掲載", "SUPPORTED")

# --- 古川孝敏 (P000100, B7S0044) ---
add_evidence("Person", "P000100", "name", "古川孝敏", "B7S0044", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED")
add_evidence("Person", "P000100", "birth_date", "1987-10-20", "B7S0044", "基本情報 > 生年月日1987年10月20日", "B.LEAGUE公式の生年月日", "SUPPORTED")
add_evidence("Career", "C000345", "organization_id", "ORG000015", "B7S0044", "プロフィール > 出身校（大）：東海大学", "B.LEAGUE公式プロフィールの大学欄。出身校（高）の項目自体が存在しない", "SUPPORTED", issue_note="プロフィールに出身校（高）の項目がないため登録せず")
add_evidence("Career", "C000345", "role", "Player", "B7S0044", "プロフィール > 出身校（大）", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000346", "organization_id", "ORG000150", "B7S0044", "クラブ所属履歴 > 2026-27 信州", "B.LEAGUE公式のクラブ所属履歴（現所属、2025-26京都から移籍）", "SUPPORTED")
add_evidence("Career", "C000346", "role", "Player", "B7S0044", "クラブ所属履歴 > 2026-27 信州", "選手として掲載", "SUPPORTED")

# --- 田原隆徳 (P000101, B7S0045) ---
add_evidence("Person", "P000101", "name", "田原隆徳", "B7S0045", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED")
add_evidence("Person", "P000101", "birth_date", "1994-04-25", "B7S0045", "基本情報 > 生年月日1994年4月25日", "B.LEAGUE公式の生年月日", "SUPPORTED")
add_evidence("Career", "C000347", "organization_id", "ORG000151", "B7S0045", "プロフィール > 出身校（高）：北海道恵庭南高等学校", "B.LEAGUE公式プロフィールの出身校欄", "SUPPORTED")
add_evidence("Career", "C000347", "role", "Player", "B7S0045", "プロフィール > 出身校（高）", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000348", "organization_id", "ORG000152", "B7S0045", "プロフィール > 出身校（大）：札幌大学", "B.LEAGUE公式プロフィールの大学欄", "SUPPORTED")
add_evidence("Career", "C000348", "role", "Player", "B7S0045", "プロフィール > 出身校（大）", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000349", "organization_id", "ORG000153", "B7S0045", "クラブ所属履歴 > 2026-27 滋賀（3年連続所属）", "B.LEAGUE公式のクラブ所属履歴（現所属）", "SUPPORTED")
add_evidence("Career", "C000349", "role", "Player", "B7S0045", "クラブ所属履歴 > 2026-27 滋賀", "選手として掲載", "SUPPORTED")

# --- 白濱僚祐 (P000102, B7S0046) ---
add_evidence("Person", "P000102", "name", "白濱僚祐", "B7S0046", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED")
add_evidence("Person", "P000102", "birth_date", "1991-08-29", "B7S0046", "基本情報 > 生年月日1991年8月29日", "B.LEAGUE公式の生年月日", "SUPPORTED")
add_evidence("Career", "C000350", "organization_id", "ORG000154", "B7S0046", "プロフィール > 出身校（高）：佐賀県立佐賀北高等学校", "B.LEAGUE公式プロフィールの出身校欄", "SUPPORTED")
add_evidence("Career", "C000350", "role", "Player", "B7S0046", "プロフィール > 出身校（高）", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000351", "organization_id", "ORG000093", "B7S0046", "プロフィール > 出身校（大）：白鴎大学", "B.LEAGUE公式プロフィールの大学欄。表記は「白鴎大学」（鴎）だが、Master ORG000093の登録表記「白鷗大学」（鷗）と同一機関の異体字表記のため、既存表記のまま登録", "SUPPORTED", issue_note="「鴎」と「鷗」は異体字。既存ORG000093の表記に合わせた")
add_evidence("Career", "C000351", "role", "Player", "B7S0046", "プロフィール > 出身校（大）", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000352", "organization_id", "ORG000155", "B7S0046", "クラブ所属履歴 > 2026-27 島根（2021-22シーズンより継続）", "B.LEAGUE公式のクラブ所属履歴（現所属）", "SUPPORTED")
add_evidence("Career", "C000352", "role", "Player", "B7S0046", "クラブ所属履歴 > 2026-27 島根", "選手として掲載", "SUPPORTED")

DECISIONS: list[dict] = []
_decision_seq = 79  # last used in wave_05 was B7D0079


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B7D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": "2026-09-23",
    })


for person in PERSONS:
    add_decision("Person", person["person_id"], "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")

add_decision("Career", "C000343", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの大学欄で確認、期間は未確認のためHOLD")
add_decision("Career", "C000344", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式プロフィールの現所属欄（クラブ所属履歴）で確認")

add_decision("Career", "C000345", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの大学欄で確認、期間は未確認のためHOLD")
add_decision("Career", "C000346", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式プロフィールの現所属欄（クラブ所属履歴）で確認")

add_decision("Career", "C000347", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの出身校欄で確認、期間は未確認のためHOLD")
add_decision("Career", "C000348", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの大学欄で確認、期間は未確認のためHOLD")
add_decision("Career", "C000349", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式プロフィールの現所属欄（クラブ所属履歴）で確認")

add_decision("Career", "C000350", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの出身校欄で確認、期間は未確認のためHOLD")
add_decision("Career", "C000351", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの大学欄で確認、期間は未確認のためHOLD")
add_decision("Career", "C000352", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式プロフィールの現所属欄（クラブ所属履歴）で確認")

ISSUES = [
    {
        "issue_id": "B7I0023",
        "person_id": "ALL",
        "related_id": "ALL",
        "issue_type": "CLUB_HISTORY_SCOPE",
        "status": "HOLD",
        "description": (
            "Wave 1・3・5と同様、本Waveでも各選手の現所属クラブのみをCareerとして記録し、"
            "過去の所属クラブ（例：田原隆徳の山形・群馬・大阪・宇都宮・栃木・北海道、"
            "白濱僚祐の秋田、古川孝敏の京都・秋田・琉球・栃木、水戸健史は富山一筋で"
            "該当なし）は対象外とした。OrganizationAlias・組織承継ルールの未解決自体は"
            "Batch 004のB4W3I0011・Batch 007のB7I0013・B7I0022から変わっていない。"
        ),
        "next_check": "OrganizationAlias・組織承継ルールをYuichiと合意してから過去クラブ経歴を追加する",
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
    write_csv(BASE / "issues.csv", ISSUES, ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"])
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
