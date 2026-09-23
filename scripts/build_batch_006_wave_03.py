#!/usr/bin/env python3
"""Build Batch 006 Wave 3 (深掘りWave / Enrichment Wave).

Target: 長島エマニエル (P000078, Master; originally registered in
batch_006/wave_01). Resolves issue B6W1I0010 (POST_HIGH_SCHOOL_GAP:
"高校と2016-18福岡の間の大学・所属は未確認"), raised when wave_01 could only
confirm 福岡第一高校 (C000276) and ライジングゼファー福岡 2016-2018
(C000277) -- his B.LEAGUE-era stint.

jbaske.com (unofficial DB) and Wikipedia (independent, 2 sources) both
additionally describe: 飛龍高等学校 (転校前の高校, before he transferred to
福岡第一高校), 白鷗大学 (中退, Wikipedia only), 横浜ビー・コルセアーズ
(練習生, 2012-2013) and バンビシャス奈良 (2013-2015) -- all BEFORE his
ライジングゼファー福岡 stint, filling the gap wave_01 flagged.

The existing C000277 (ライジングゼファー福岡, 2016-2018) is NOT touched:
both jbaske.com and bleague.jp's own historical roster page describe this
as his LAST known affiliation (jbaske.com explicitly says he retired after
the 2017-18 season), so this is a "pre-2016 history was missing" case, not
a "post-2018 history is stale" case.

This is part of the systematic 過去在籍チーム深掘り rollout Yuichi asked to
begin in full (following the single test case on 辻直人, batch_007/wave_08).
See docs/HISTORICAL_CAREER_DEEPENING_LOG.md for the census method used to
select targets across the whole archive, and for two other candidates
(河合瑠那 P000066, 長岡大杜 P000067) that turned out to need NO new research
at all -- their historical Careers are already fully sourced and sitting
READY_FOR_VERIFIED_REVIEW in batch_004/wave_02, simply awaiting Human
Approval/VERIFIED promotion to Master, which this session does not do.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_006" / "wave_03"

PERSONS: list[dict] = []  # enrichment wave: no new persons

ORGANIZATIONS = [
    {"organization_id": "ORG000170", "name": "飛龍高等学校"},
    {"organization_id": "ORG000171", "name": "バンビシャス奈良"},
]

CAREERS = [
    {"career_id": "C000380", "person_id": "P000078", "organization_id": "ORG000170", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000381", "person_id": "P000078", "organization_id": "ORG000093", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000382", "person_id": "P000078", "organization_id": "ORG000055", "role": "Player", "start": "2012", "end": "2013"},
    {"career_id": "C000383", "person_id": "P000078", "organization_id": "ORG000171", "role": "Player", "start": "2013", "end": "2015"},
]

SOURCES = [
    {"source_id": "B6W3S0001", "title": "長島 エマニエル", "publisher": "バスケットボールデータベース (jbaske.com)", "url": "https://jbaske.com/db/archives/10940", "accessed_at": "2026-09-23"},
    {"source_id": "B6W3S0002", "title": "長島エマニエル", "publisher": "Wikipedia日本語版", "url": "https://ja.wikipedia.org/wiki/長島エマニエル", "accessed_at": "2026-09-23"},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B6W3E{_evidence_seq:04d}",
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


add_evidence("Career", "C000380", "organization_id", "ORG000170", "B6W3S0001", "経歴 > 高校：飛龍高校→福岡第一高校", "jbaske.comのデータベースで、福岡第一高校へ転校する前に飛龍高校（静岡県）に在学していたことを確認", "SUPPORTED")
add_evidence("Career", "C000380", "organization_id", "ORG000170", "B6W3S0002", "経歴節 > 「飛龍高校に進学。2年時に福岡第一高校に転校」", "Wikipediaでも飛龍高校在学（福岡第一高校への転校前）を確認（独立した第2ソース）", "SUPPORTED")

add_evidence(
    "Career", "C000381", "organization_id", "ORG000093", "B6W3S0002",
    "経歴節 > 「福岡第一高校卒業後、白鷗大学に進学するも中退」",
    "Wikipediaで白鷗大学への進学（中退）を確認。jbaske.com・bleague.jp・バスケットボールキングいずれにも大学進学の記載がなく、現時点でWikipedia以外の裏付けが取れていない",
    "PARTIAL",
    issue_note="白鷗大学在学（中退）はWikipedia単独の記載。在籍期間・中退時期も不明",
)

add_evidence("Career", "C000382", "organization_id", "ORG000055", "B6W3S0001", "クラブ経歴 > 「2012-2013年：横浜ビー・コルセアーズ練習生」", "jbaske.comのデータベースで横浜ビー・コルセアーズへの練習生入団を確認", "SUPPORTED")
add_evidence("Career", "C000382", "organization_id", "ORG000055", "B6W3S0002", "経歴節 > 「横浜ビー・コルセアーズに練習生として入団」", "Wikipediaでも横浜ビー・コルセアーズ練習生としての在籍を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000382", "start", "2012", "B6W3S0001", "クラブ経歴 > 「2012-2013年：横浜ビー・コルセアーズ練習生」", "jbaske.comの年次表記に基づく。他媒体に具体的な年次の記載はない", "PARTIAL", issue_note="在籍年次はjbaske.com単独の記載")
add_evidence("Career", "C000382", "end", "2013", "B6W3S0001", "クラブ経歴 > 「2012-2013年：横浜ビー・コルセアーズ練習生」", "jbaske.comの年次表記に基づく。他媒体に具体的な年次の記載はない", "PARTIAL", issue_note="在籍年次はjbaske.com単独の記載")

add_evidence("Career", "C000383", "organization_id", "ORG000171", "B6W3S0001", "クラブ経歴 > 「2013-2015年：バンビシャス奈良」", "jbaske.comのデータベースでバンビシャス奈良への移籍を確認", "SUPPORTED")
add_evidence("Career", "C000383", "organization_id", "ORG000171", "B6W3S0002", "経歴節 > 「その後バンビシャス奈良に移籍」", "Wikipediaでもバンビシャス奈良在籍を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000383", "start", "2013", "B6W3S0001", "クラブ経歴 > 「2013-2015年：バンビシャス奈良」", "jbaske.comの年次表記に基づく。他媒体に具体的な年次の記載はない", "PARTIAL", issue_note="在籍年次はjbaske.com単独の記載")
add_evidence("Career", "C000383", "end", "2015", "B6W3S0001", "クラブ経歴 > 「2013-2015年：バンビシャス奈良」", "jbaske.comの年次表記に基づく。他媒体に具体的な年次の記載はない", "PARTIAL", issue_note="在籍年次はjbaske.com単独の記載")


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B6W3D{_decision_seq:04d}",
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

add_decision("Career", "C000380", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end",
             "jbaske.com・Wikipediaの独立した2ソースで、福岡第一高校転校前の飛龍高等学校在学を確認。具体的な在学年次はいずれの資料にも記載がないため保留")
add_decision("Career", "C000381", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end",
             "Wikipedia単独で白鷗大学進学（中退）を確認。他媒体での裏付けが取れていないためissueに記録した上でREADYとする")
add_decision("Career", "C000382", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
             "組織参照（横浜ビー・コルセアーズ）はjbaske.com・Wikipediaの独立2ソースで確認。在籍年次（2012-2013）はjbaske.com単独のためissueに記録した上でREADYとする")
add_decision("Career", "C000383", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
             "組織参照（バンビシャス奈良）はjbaske.com・Wikipediaの独立2ソースで確認。在籍年次（2013-2015）はjbaske.com単独のためissueに記録した上でREADYとする")

# issues.csv follows batch_006's own established schema (person_id, related_id,
# issue_type, status, description, next_check) -- different from batch_007's
# newer (category, scope, description) schema.
ISSUES = [
    {"issue_id": "B6W3I0001", "person_id": "P000078", "related_id": "C000381", "issue_type": "SOURCE_TIER", "status": "HOLD",
     "description": "白鷗大学在学（中退）はWikipedia単独の記載であり、jbaske.com・bleague.jp・バスケットボールキングいずれにも記載がない。",
     "next_check": "他媒体（大学公式・大会公式ロスター等）での裏付けを確認"},
    {"issue_id": "B6W3I0002", "person_id": "P000078", "related_id": "C000382,C000383", "issue_type": "SOURCE_TIER", "status": "HOLD",
     "description": "横浜ビー・コルセアーズ練習生（2012-2013年）・バンビシャス奈良（2013-2015年）の在籍年次は、組織名自体はjbaske.com・Wikipediaの2ソースで確認できるが、具体的な年次はjbaske.com（非公式データベース）単独の記載。",
     "next_check": "公式資料での年次の裏付けを確認"},
    {"issue_id": "B6W3I0003", "person_id": "P000078", "related_id": "P000078", "issue_type": "POST_HIGH_SCHOOL_GAP", "status": "RESOLVED",
     "description": "wave_01で立てたissue B6W1I0010（高校と2016-18福岡の間の大学・所属が未確認）を、飛龍高等学校（転校前）・白鷗大学（中退）・横浜ビー・コルセアーズ練習生・バンビシャス奈良の4件追加により解消。",
     "next_check": ""},
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
    write_csv(BASE / "issues.csv", ISSUES, [
        "issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check",
    ])
    write_csv(BASE / "qa_decisions.csv", DECISIONS, [
        "decision_id", "entity_type", "entity_id", "decision",
        "eligible_fields", "held_fields", "reason", "reviewed_at",
    ])
    print(
        f"Wrote batch_006/wave_03: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
