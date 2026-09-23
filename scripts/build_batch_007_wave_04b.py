#!/usr/bin/env python3
"""Build Batch 007 Wave 4b (深掘りWave追補 / Enrichment Wave addendum).

Follow-up to Wave 4, discovered after Wave 4 was already committed
(commit 2593b45). Per the "深掘りWaveのデータ構造" rule, existing wave
files are never modified -- this goes into its own new wave folder,
adding a brand-new Career (junior high school) for P000083 and new
evidence/qa_decisions extending Wave 1's existing C000299 (high school)
Career record, which had organization_id HELD pending the
開志国際高等学校 ambiguity.

Target: 富樫勇樹 (P000083, still CANDIDATE, not yet Master).
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_007" / "wave_04b"

ORGANIZATIONS = [
    {"organization_id": "ORG000141", "name": "新発田市立本丸中学校"},
]

CAREERS = [
    {"career_id": "C000330", "person_id": "P000083", "organization_id": "ORG000141", "role": "Player", "start": "", "end": ""},
]

SOURCES = [
    {
        "source_id": "B7S0037",
        "title": "中学日本一を実現した親子鷹 小4から「別格」だった富樫勇樹",
        "publisher": "Yahoo!スポーツ（スポーツナビ）",
        "url": "https://sports.yahoo.co.jp/column/detail/202009170002-spnavi",
        "accessed_at": "2026-09-23",
    },
    {
        "source_id": "B7S0038",
        "title": "開志国際の富樫英樹コーチが語るバスケ愛と選手育成（前編）「勇樹は他の子とは全然違っていました」",
        "publisher": "BASKET COUNT",
        "url": "https://basket-count.com/article/detail/45530",
        "accessed_at": "2026-09-23",
    },
]

EVIDENCE: list[dict] = []
_evidence_seq = 124  # last used in wave_04 was B7E0124


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


# --- C000330 新発田市立本丸中学校（新規Career） ---
add_evidence(
    "Career", "C000330", "organization_id", "ORG000141", "B7S0026",
    "経歴 > 新発田市立本丸中学校でミニバスから育ち、中学3年時に全国大会で優勝",
    "Wikipediaにより出身中学校（新発田市立本丸中学校）を確認",
    "SUPPORTED",
)
add_evidence(
    "Career", "C000330", "organization_id", "ORG000141", "B7S0037",
    "本文 > 「本丸中学校（新潟県新発田市立）」に在籍、中3時に全中初優勝",
    "Yahoo!スポーツナビの記事でも同じ中学校名を確認（独立した第2ソース）",
    "SUPPORTED",
)
add_evidence(
    "Career", "C000330", "role", "Player", "B7S0026",
    "経歴 > バスケットボール部に所属",
    "同上",
    "SUPPORTED",
)

# --- C000299（既存Career、高校＝モントロス・クリスチャン高校）: 開志国際高等学校との関係を追加調査 ---
add_evidence(
    "Career", "C000299", "organization_id", "ORG000117", "B7S0026",
    "経歴 > 中学卒業後にアメリカへ留学し、モントロス・クリスチャン高等学校（メリーランド州）に進学",
    "Wikipediaの経歴節に開志国際高等学校への言及は一切なく、渡米してモントロス・クリスチャン高校に進学したとのみ記載",
    "SUPPORTED",
    issue_note="開志国際高等学校という校名はWikipedia本文中に登場しない",
)
add_evidence(
    "Career", "C000299", "organization_id", "ORG000117", "B7S0037",
    "本文 > 「中学卒業と同時にアメリカへ渡りました」",
    "Yahoo!スポーツナビでも中学卒業後は直接渡米したとの記述で、開志国際高等学校への言及なし（独立した第2ソース）",
    "SUPPORTED",
    issue_note="開志国際高等学校という校名はこの記事にも登場しない",
)
add_evidence(
    "Career", "C000299", "organization_id", "ORG000117", "B7S0038",
    "本文 > 富樫英樹コーチが「51歳の年に開志国際ができるということで高校に移った」、開志国際は2018年にインターハイ初優勝（就任5年後）",
    "父・富樫英樹氏へのインタビュー記事より、開志国際高等学校バスケットボール部の創設・強化は富樫英樹氏が同校に着任して以降であり、時系列上、富樫勇樹が中学卒業後（渡米前）に開志国際に在籍し得た可能性は低いことが示唆される。ただし「開志国際は勇樹とは無関係」と明言した一次資料ではなく、創部時期からの論理的推定に留まるためPARTIAL評価",
    "PARTIAL",
    issue_note="開志国際高等学校の部活動開始時期と富樫勇樹の渡米時期の前後関係からの推定であり、直接『無関係』と明言した資料ではない",
)

DECISIONS = [
    {
        "decision_id": "B7D0062",
        "entity_type": "Career",
        "entity_id": "C000330",
        "decision": "READY_FOR_VERIFIED_REVIEW",
        "eligible_fields": "organization_id|role",
        "held_fields": "start|end",
        "reason": "Wikipedia・Yahoo!スポーツナビの独立した2ソースにより出身中学校（新発田市立本丸中学校）を確認。在籍期間（start/end）を明示する資料が見つからないため保留",
        "reviewed_at": "2026-09-23",
    },
    {
        "decision_id": "B7D0063",
        "entity_type": "Career",
        "entity_id": "C000299",
        "decision": "READY_FOR_VERIFIED_REVIEW",
        "eligible_fields": "organization_id|role",
        "held_fields": "start|end",
        "reason": (
            "Wave1でHOLDだったorganization_id（開志国際高等学校との関係未確認）について追加調査。"
            "Wikipedia・Yahoo!スポーツナビいずれにも開志国際高等学校への言及がなく、"
            "父・富樫英樹コーチへのインタビュー記事から開志国際バスケ部の強化開始時期が富樫勇樹の渡米後と推定されることも踏まえ、"
            "モントロス・クリスチャン高等学校（ORG000117）を出身高校としてREADYに更新。"
            "ただし開志国際との無関係を直接明言した資料はないため、完全な断定ではない旨をissueに残す"
        ),
        "reviewed_at": "2026-09-23",
    },
]

ISSUES = [
    {
        "issue_id": "B7I0021",
        "category": "INFERENCE_CONFIDENCE",
        "scope": "P000083",
        "description": (
            "富樫勇樹とORG000117（モントロス・クリスチャン高等学校）の関係はWikipedia・Yahoo!スポーツナビの"
            "2独立ソースでSUPPORTEDだが、開志国際高等学校との無関係については「開志国際高等学校の部活動強化開始が"
            "本人渡米後と推定される」という時系列からの論理的推定（PARTIAL）に留まり、開志国際側からの直接の否定・"
            "確認は取れていない。Yuichiの追加判断、または開志国際高等学校の公式沿革等での裏取りが望ましい。"
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
    write_csv(BASE / "person_candidates.csv", [], ["person_id", "name"])
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
        f"Wrote wave_04b: {len(ORGANIZATIONS)} orgs, {len(CAREERS)} new careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
