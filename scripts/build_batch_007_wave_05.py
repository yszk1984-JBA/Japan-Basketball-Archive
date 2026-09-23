#!/usr/bin/env python3
"""Build Batch 007 Wave 5 (新規開拓Wave / Acquisition Wave) candidate data.

Cadence: Wave 4/4b was the Enrichment Wave, so Wave 5 resumes new-acquisition
work. Target selection: cross-checked all 26 B.PREMIER 2026-27 clubs
(https://www.bleague.jp/news_detail/id=444118) against Master + all
candidate waves' *currently-ongoing* Career records (end blank) and found
9 clubs with zero current-roster coverage: 秋田ノーザンハピネッツ・
群馬クレインサンダーズ・アルティーリ千葉・サンロッカーズ渋谷・
富山グラウジーズ・信州ブレイブウォリアーズ・滋賀レイクス・大阪エヴェッサ・
島根スサノオマジック. This wave covers 4 of them (the standard Wave size),
via one well-documented, veteran Japanese national-team-experienced player
per club, matching Wave 3's methodology (single B.LEAGUE公式選手プロフィール
per person, current-club-only Career scope; historical club-by-club
transfers deferred, same as issue B7I0013).

Historical school names are used where they differ from the school's
CURRENT name (governance: never overwrite a historical org name with the
current one) -- e.g. 田口成浩's high school is registered as 明桜高等学校
(the name at the time he attended), not the post-2016 university-affiliated
name; 安藤誓哉's high school is registered as 明成高等学校 (pre-2020 name),
not 仙台大学附属明成高等学校.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_007" / "wave_05"

PERSONS = [
    {"person_id": "P000095", "name": "田口成浩"},
    {"person_id": "P000096", "name": "竹内譲次"},
    {"person_id": "P000097", "name": "辻直人"},
    {"person_id": "P000098", "name": "安藤誓哉"},
]

ORGANIZATIONS = [
    {"organization_id": "ORG000146", "name": "明桜高等学校"},
    {"organization_id": "ORG000145", "name": "富士大学"},
    {"organization_id": "ORG000137", "name": "秋田ノーザンハピネッツ"},
    {"organization_id": "ORG000119", "name": "洛南高等学校"},
    {"organization_id": "ORG000015", "name": "東海大学"},
    {"organization_id": "ORG000142", "name": "大阪エヴェッサ"},
    {"organization_id": "ORG000030", "name": "青山学院大学"},
    {"organization_id": "ORG000143", "name": "群馬クレインサンダーズ"},
    {"organization_id": "ORG000147", "name": "明成高等学校"},
    {"organization_id": "ORG000124", "name": "明治大学"},
    {"organization_id": "ORG000144", "name": "アルティーリ千葉"},
]

CAREERS = [
    {"career_id": "C000331", "person_id": "P000095", "organization_id": "ORG000146", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000332", "person_id": "P000095", "organization_id": "ORG000145", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000333", "person_id": "P000095", "organization_id": "ORG000137", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000334", "person_id": "P000096", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000335", "person_id": "P000096", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000336", "person_id": "P000096", "organization_id": "ORG000142", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000337", "person_id": "P000097", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000338", "person_id": "P000097", "organization_id": "ORG000030", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000339", "person_id": "P000097", "organization_id": "ORG000143", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000340", "person_id": "P000098", "organization_id": "ORG000147", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000341", "person_id": "P000098", "organization_id": "ORG000124", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000342", "person_id": "P000098", "organization_id": "ORG000144", "role": "Player", "start": "", "end": ""},
]

SOURCES = [
    {"source_id": "B7S0039", "title": "田口成浩 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8468", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0040", "title": "竹内譲次 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=9033", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0041", "title": "辻直人 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8487", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0042", "title": "安藤誓哉 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8467", "accessed_at": "2026-09-23"},
]

EVIDENCE: list[dict] = []
_evidence_seq = 130  # last used in wave_04b was B7E0130


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


# --- 田口成浩 (P000095, B7S0039) ---
add_evidence("Person", "P000095", "name", "田口成浩", "B7S0039", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED")
add_evidence("Person", "P000095", "birth_date", "1990-03-25", "B7S0039", "基本情報 > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED")
add_evidence("Career", "C000331", "organization_id", "ORG000146", "B7S0039", "プロフィール > 出身校（高）：明桜高等学校(現・ノースアジア大学明桜高等学校)", "B.LEAGUE公式プロフィールの出身校欄。現校名はノースアジア大学明桜高等学校だが、本人在学当時の名称（明桜高等学校）で登録", "SUPPORTED")
add_evidence("Career", "C000331", "role", "Player", "B7S0039", "プロフィール > 出身校（高）", "選手として掲載", "SUPPORTED")
add_evidence("Career", "C000332", "organization_id", "ORG000145", "B7S0039", "プロフィール > 出身校（大）：富士大学", "B.LEAGUE公式プロフィールの大学欄", "SUPPORTED")
add_evidence("Career", "C000332", "role", "Player", "B7S0039", "プロフィール > 出身校（大）", "選手として掲載", "SUPPORTED")
add_evidence("Career", "C000333", "organization_id", "ORG000137", "B7S0039", "クラブ所属履歴 > 2026-27 秋田", "B.LEAGUE公式のクラブ所属履歴（現所属）", "SUPPORTED")
add_evidence("Career", "C000333", "role", "Player", "B7S0039", "クラブ所属履歴 > 2026-27 秋田", "選手として掲載", "SUPPORTED")

# --- 竹内譲次 (P000096, B7S0040) ---
add_evidence("Person", "P000096", "name", "竹内譲次", "B7S0040", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED")
add_evidence("Person", "P000096", "birth_date", "1985-01-29", "B7S0040", "基本情報 > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED")
add_evidence("Career", "C000334", "organization_id", "ORG000119", "B7S0040", "Wikipedia > 経歴 > 出身高校：洛南高等学校", "B.LEAGUE公式プロフィールに出身校欄の記載がなかったため、Wikipediaで確認", "SUPPORTED")
add_evidence("Career", "C000334", "role", "Player", "B7S0040", "同上", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000335", "organization_id", "ORG000015", "B7S0040", "Wikipedia > 経歴 > 出身大学：東海大学", "B.LEAGUE公式プロフィールに大学欄の記載がなかったため、Wikipediaで確認", "SUPPORTED")
add_evidence("Career", "C000335", "role", "Player", "B7S0040", "同上", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000336", "organization_id", "ORG000142", "B7S0040", "クラブ所属履歴 > 2026-27 大阪（2021-22シーズンより継続）", "B.LEAGUE公式のクラブ所属履歴（現所属）", "SUPPORTED")
add_evidence("Career", "C000336", "role", "Player", "B7S0040", "クラブ所属履歴 > 2026-27 大阪", "選手として掲載", "SUPPORTED")

# --- 辻直人 (P000097, B7S0041) ---
add_evidence("Person", "P000097", "name", "辻直人", "B7S0041", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED")
add_evidence("Person", "P000097", "birth_date", "1989-09-08", "B7S0041", "基本情報 > 生年月日1989年9月8日", "B.LEAGUE公式の生年月日", "SUPPORTED")
add_evidence("Career", "C000337", "organization_id", "ORG000119", "B7S0041", "Wikipedia > 経歴 > 出身高校：洛南高等学校", "B.LEAGUE公式プロフィールに出身校欄の記載がなかったため、Wikipediaで確認", "SUPPORTED")
add_evidence("Career", "C000337", "role", "Player", "B7S0041", "同上", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000338", "organization_id", "ORG000030", "B7S0041", "Wikipedia > 経歴 > 出身大学：青山学院大学", "B.LEAGUE公式プロフィールに大学欄の記載がなかったため、Wikipediaで確認", "SUPPORTED")
add_evidence("Career", "C000338", "role", "Player", "B7S0041", "同上", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000339", "organization_id", "ORG000143", "B7S0041", "クラブ所属履歴 > 2026-27 群馬（2023-24シーズンより継続）", "B.LEAGUE公式のクラブ所属履歴（現所属）", "SUPPORTED")
add_evidence("Career", "C000339", "role", "Player", "B7S0041", "クラブ所属履歴 > 2026-27 群馬", "選手として掲載", "SUPPORTED")

# --- 安藤誓哉 (P000098, B7S0042) ---
add_evidence("Person", "P000098", "name", "安藤誓哉", "B7S0042", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED")
add_evidence("Person", "P000098", "birth_date", "1992-07-15", "B7S0042", "基本情報 > 生年月日1992年7月15日", "B.LEAGUE公式の生年月日", "SUPPORTED")
add_evidence("Career", "C000340", "organization_id", "ORG000147", "B7S0042", "Wikipedia > 経歴 > 出身高校：明成高校（仙台大学附属明成高等学校）", "B.LEAGUE公式プロフィールに出身校欄の記載がなかったため、Wikipediaで確認。同校は2020年に仙台大学附属明成高等学校へ改称しており、本人在学当時の名称（明成高等学校）で登録", "SUPPORTED", issue_note="学校名の改称時期(2020年)は本人卒業後と考えられるため、当時の名称で登録")
add_evidence("Career", "C000340", "role", "Player", "B7S0042", "同上", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000341", "organization_id", "ORG000124", "B7S0042", "Wikipedia > 経歴 > 出身大学：明治大学", "B.LEAGUE公式プロフィールに大学欄の記載がなかったため、Wikipediaで確認", "SUPPORTED")
add_evidence("Career", "C000341", "role", "Player", "B7S0042", "同上", "選手として在籍", "SUPPORTED")
add_evidence("Career", "C000342", "organization_id", "ORG000144", "B7S0042", "クラブ所属履歴 > 2026-27 A千葉", "B.LEAGUE公式のクラブ所属履歴（現所属）。Wikipediaは本項目更新時点で「島根スサノオマジック」を現所属と記載しており、bleague.jp本人ページのクラブ所属履歴（2025-26 横浜BC→2026-27 A千葉）と食い違うため、より新しい一次資料であるbleague.jp公式ロスターを優先", "SUPPORTED", issue_note="Wikipediaの現所属記載が更新遅延で古い（島根のまま）ことを確認。Wikipedia側の更新は本プロジェクトの管理外")
add_evidence("Career", "C000342", "role", "Player", "B7S0042", "クラブ所属履歴 > 2026-27 A千葉", "選手として掲載", "SUPPORTED")

DECISIONS: list[dict] = []
_decision_seq = 63  # last used in wave_04b was B7D0063


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

add_decision("Career", "C000331", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの出身校欄で確認、期間は未確認のためHOLD")
add_decision("Career", "C000332", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの大学欄で確認、期間は未確認のためHOLD")
add_decision("Career", "C000333", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式プロフィールの現所属欄（クラブ所属履歴）で確認")

add_decision("Career", "C000334", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipediaで出身高校を確認、期間は未確認のためHOLD")
add_decision("Career", "C000335", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipediaで出身大学を確認、期間は未確認のためHOLD")
add_decision("Career", "C000336", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式プロフィールの現所属欄（クラブ所属履歴）で確認")

add_decision("Career", "C000337", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipediaで出身高校を確認、期間は未確認のためHOLD")
add_decision("Career", "C000338", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipediaで出身大学を確認、期間は未確認のためHOLD")
add_decision("Career", "C000339", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式プロフィールの現所属欄（クラブ所属履歴）で確認")

add_decision("Career", "C000340", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipediaで出身高校を確認、期間は未確認のためHOLD")
add_decision("Career", "C000341", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipediaで出身大学を確認、期間は未確認のためHOLD")
add_decision("Career", "C000342", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式ロスター最新のクラブ所属履歴で確認（Wikipediaより新しい一次資料を優先）")

ISSUES = [
    {
        "issue_id": "B7I0022",
        "person_id": "ALL",
        "related_id": "ALL",
        "issue_type": "CLUB_HISTORY_SCOPE",
        "status": "HOLD",
        "description": (
            "Wave 1〜3と同様、本Waveでも各選手の現所属クラブのみをCareerとして記録し、"
            "過去の所属クラブ（例：竹内譲次のアルバルク東京、辻直人の広島ドラゴンフライズ・"
            "川崎ブレイブサンダース、安藤誓哉の横浜ビー・コルセアーズ・島根スサノオマジック・"
            "アルバルク東京・秋田ノーザンハピネッツ、田口成浩の秋田ノーザンハピネッツ在籍中の"
            "中断期間等）は対象外とした。bleague.jp公式プロフィールの「クラブ所属履歴」欄には"
            "シーズン単位の在籍クラブ一覧が掲載されており、次回の深掘りWave以降で参照できる。"
            "OrganizationAlias・組織承継ルールの未解決自体はBatch 004のB4W3I0011・"
            "Batch 007のB7I0013から変わっていない。"
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
        f"Wrote wave_05: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
