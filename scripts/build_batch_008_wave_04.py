#!/usr/bin/env python3
"""Build Batch 008 Wave 4 (福岡大学附属大濠高等学校 4/4, final wave) CANDIDATE data.

Completes coverage of the school's 17 not-yet-registered current B.LEAGUE
alumni (wave_01=4, wave_02=6, wave_03=6, wave_04=1). This is the final
person from B.LEAGUE's TagID=35 alumni listing not yet in the archive.

Person (checked against Master + every candidate/verified person file
before writing -- not previously registered):
- 島﨑輝 (Hikaru Shimazaki, さいたまブロンコス) -- his B.LEAGUE club-history
  field shows only "2026-27 埼玉", i.e. this is his B.LEAGUE debut season;
  no prior pro club to exclude, so no PRO_HISTORY_GAPS issue is needed
  (unlike most other wave_01-03 persons).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_008" / "wave_04"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000127", "name": "島﨑 輝"},
]

# ORG000127 (大濠) and ORG000016 (中央大学) already exist and are reused --
# checked against master + every candidate organization_candidates.csv
# before writing this file. さいたまブロンコス confirmed genuinely new (not
# found anywhere in master or candidate data); current max existing
# Organization ID is ORG000182 (batch_008/wave_03), so this is ORG000183.
ORGANIZATIONS = [
    {"organization_id": "ORG000127", "name": "福岡大学附属大濠高等学校"},
    {"organization_id": "ORG000016", "name": "中央大学"},
    {"organization_id": "ORG000183", "name": "さいたまブロンコス"},
]

CAREERS = [
    {"career_id": "C000437", "person_id": "P000127", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000438", "person_id": "P000127", "organization_id": "ORG000016", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000439", "person_id": "P000127", "organization_id": "ORG000183", "role": "Player", "start": "2026", "end": ""},
]

SOURCES = [
    {"source_id": "B8W4S0001", "title": "島﨑輝 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=34423", "accessed_at": CHECKED_AT},
    {"source_id": "B8W4S0002", "title": "ワタシノB.LEAGUE選手一覧 | 福岡大学附属大濠高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:福岡大学附属大濠高等学校", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B8W4E{_evidence_seq:04d}",
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


add_evidence("Person", "P000127", "name", "島﨑 輝", "B8W4S0001", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000127", "birth_date", "2003-06-29", "B8W4S0001", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000437", "organization_id", "ORG000127", "B8W4S0001", "学歴 > 出身校（高）：福岡大学附属大濠高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000437", "organization_id", "ORG000127", "B8W4S0002", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000438", "organization_id", "ORG000016", "B8W4S0001", "学歴 > 出身校（大）：中央大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000439", "organization_id", "ORG000183", "B8W4S0001", "クラブ経歴 > 「2026-27：埼玉」のみ記載（B.LEAGUEデビューシーズン）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000439", "start", "2026", "B8W4S0001", "クラブ経歴 > 「2026-27：埼玉」が初出（唯一の記載）", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B8W4D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000127", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000437", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000438", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000439", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

ISSUES = [
    {"issue_id": "B8W4I0001", "person_id": "P000127", "related_id": "C000437", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "島﨑輝の福岡大学附属大濠高等学校在籍そのものは複数ソースで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "高校公式または大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B8W4I0002", "person_id": "P000127", "related_id": "C000438", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "島﨑輝の中央大学在籍そのものは確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
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
        f"Wrote batch_008/wave_04: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
