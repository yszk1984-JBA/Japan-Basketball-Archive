#!/usr/bin/env python3
"""Build Batch 004 Wave 5 (深掘りWave/Enrichment Wave) candidate data.

Target: 河村勇輝 (P000064), already promoted to MASTER via Batch 004 Wave 1 /
Approval Sprint. His most recent MASTER Career record (C000223, メンフィス・
グリズリーズ Two-Way契約, 2024-10-19) is now stale. This wave adds his
subsequent NBA affiliations (シカゴ・ブルズ x2 stints, ロサンゼルス・
クリッパーズ) as new Career candidates. Existing MASTER files are NOT
modified — new facts always go through CANDIDATE -> QA -> VERIFIED ->
HUMAN APPROVAL before ever reaching data/master/*.
"""
from __future__ import annotations

from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_004" / "wave_05"
BASE.mkdir(parents=True, exist_ok=True)

ORGANIZATIONS = [
    {"organization_id": "ORG000139", "name": "シカゴ・ブルズ"},
    {"organization_id": "ORG000140", "name": "ロサンゼルス・クリッパーズ"},
]

CAREERS = [
    {"career_id": "C000327", "person_id": "P000064", "organization_id": "ORG000139", "role": "Player", "start": "2025-07", "end": "2025-10"},
    {"career_id": "C000328", "person_id": "P000064", "organization_id": "ORG000139", "role": "Player", "start": "2026-01", "end": "2026-08"},
    {"career_id": "C000329", "person_id": "P000064", "organization_id": "ORG000140", "role": "Player", "start": "2026-08", "end": ""},
]

SOURCES = [
    {"source_id": "B4W5S0001", "title": "サマーリーグでアピールに成功した河村勇輝がブルズと2Way契約締結…NBA2シーズン目へ",
     "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/world/20250720/555885.html", "accessed_at": "2026-09-23"},
    {"source_id": "B4W5S0002", "title": "河村勇輝がブルズへ“復帰”…再び2ウェイ契約締結、チームが正式発表",
     "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/world/20260107/587979.html", "accessed_at": "2026-09-23"},
    {"source_id": "B4W5S0003", "title": "【2026年8月最新】河村勇輝がクリッパーズと契約！エキシビット10契約とは？",
     "publisher": "すぽろぐ（バスケットボール総合情報サイト）", "url": "https://spolog-basketball.com/yuki-kawamura-latest-information-1/", "accessed_at": "2026-09-23"},
]

EVIDENCE = []
_e = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id, locator, summary, assessment, issue_note=""):
    global _e
    _e += 1
    EVIDENCE.append({
        "record_id": f"B4W5E{_e:04d}", "entity_type": entity_type, "entity_id": entity_id,
        "field_name": field_name, "candidate_value": candidate_value, "source_id": source_id,
        "source_locator": locator, "evidence_summary": summary, "assessment": assessment,
        "checked_at": "2026-09-23", "issue_note": issue_note,
    })


# C000327: シカゴ・ブルズ 1回目（2Way, 2025-07-20発表）
add_evidence("Career", "C000327", "organization_id", "ORG000139", "B4W5S0001", "本文 > シカゴ・ブルズは「7月20日（現地時間19日）」に河村勇輝との2Way契約締結を発表",
             "バスケットボールキングの公式発表報道", "SUPPORTED")
add_evidence("Career", "C000327", "role", "Player", "B4W5S0001", "本文 > 2Way契約締結", "同上", "SUPPORTED")
add_evidence("Career", "C000327", "contract_type", "Two-Way contract", "B4W5S0001", "本文 > ブルズと2Way契約締結", "同上", "SUPPORTED")
add_evidence("Career", "C000327", "start", "2025-07", "B4W5S0001", "本文 > 7月20日（現地時間19日）発表", "同上", "SUPPORTED")
add_evidence("Career", "C000327", "end", "2025-10", "B4W5S0003", "本文 > 開幕直前の2025年10月17日に健康上の理由で契約を解除",
             "すぽろぐ記事による契約解除日の記述", "SUPPORTED")

# C000328: シカゴ・ブルズ 2回目（再契約, 2026-01-06/07発表）
add_evidence("Career", "C000328", "organization_id", "ORG000139", "B4W5S0002", "本文 > シカゴ・ブルズは1月7日（現地時間6日）、河村勇輝と2ウェイ契約を結んだことを発表",
             "バスケットボールキングの公式発表報道", "SUPPORTED")
add_evidence("Career", "C000328", "role", "Player", "B4W5S0002", "本文 > 2ウェイ契約", "同上", "SUPPORTED")
add_evidence("Career", "C000328", "contract_type", "Two-Way contract", "B4W5S0002", "本文 > 再び2ウェイ契約締結", "同上", "SUPPORTED")
add_evidence("Career", "C000328", "start", "2026-01", "B4W5S0002", "本文 > 1月7日（現地時間6日）発表", "同上", "SUPPORTED")
add_evidence("Career", "C000328", "end", "2026-08", "B4W5S0003", "本文 > 2026年8月9日（現地時間）クリッパーズと契約",
             "クリッパーズ移籍発表日をブルズ在籍終了の目安として記録", "PARTIAL",
             "ブルズを正式に離れた具体的な日付そのものの記載はなく、クリッパーズ契約発表日から逆算")

# C000329: ロサンゼルス・クリッパーズ（エキシビット10契約, 2026-08-09）
add_evidence("Career", "C000329", "organization_id", "ORG000140", "B4W5S0003", "本文 > 契約日：2026年8月9日（現地時間）契約先：ロサンゼルス・クリッパーズ",
             "すぽろぐ記事による公式契約報道", "SUPPORTED")
add_evidence("Career", "C000329", "role", "Player", "B4W5S0003", "本文 > 契約先：ロサンゼルス・クリッパーズ", "同上", "SUPPORTED")
add_evidence("Career", "C000329", "contract_type", "Exhibit 10 contract", "B4W5S0003", "本文 > 契約形態：エキシビット10契約",
             "最低年俸で保証がなく、レギュラーシーズン出場も約束されない無保証契約と明記", "SUPPORTED")
add_evidence("Career", "C000329", "start", "2026-08", "B4W5S0003", "本文 > 契約日：2026年8月9日（現地時間）", "同上", "SUPPORTED")

DECISIONS = [
    {"decision_id": "B4W5D0001", "entity_type": "Career", "entity_id": "C000327", "decision": "READY_FOR_VERIFIED_REVIEW",
     "eligible_fields": "organization_id|role|contract_type|start|end", "held_fields": "",
     "reason": "バスケットボールキング・すぽろぐの公式発表報道により、シカゴ・ブルズとの1回目の2Way契約（2025年7月〜同年10月に契約解除）を確認", "reviewed_at": "2026-09-23"},
    {"decision_id": "B4W5D0002", "entity_type": "Career", "entity_id": "C000328", "decision": "READY_FOR_VERIFIED_REVIEW",
     "eligible_fields": "organization_id|role|contract_type|start", "held_fields": "end",
     "reason": "バスケットボールキングの公式発表報道によりブルズとの2回目の2Way契約（2026年1月再契約）を確認。終了時期はクリッパーズ移籍発表日からの推定に留まるため保留",
     "reviewed_at": "2026-09-23"},
    {"decision_id": "B4W5D0003", "entity_type": "Career", "entity_id": "C000329", "decision": "READY_FOR_VERIFIED_REVIEW",
     "eligible_fields": "organization_id|role|contract_type|start", "held_fields": "end",
     "reason": "すぽろぐ記事によりロサンゼルス・クリッパーズとのエキシビット10契約（2026年8月9日）を確認。現在進行中の契約のため終了日は未定（NULL）", "reviewed_at": "2026-09-23"},
]

ISSUES = [
    {"issue_id": "B4W5I0001", "category": "DATE_GAP", "scope": "P000064",
     "description": "河村勇輝：MasterのC000223（メンフィス・グリズリーズ Two-Way契約、2024-10-19発表）から本Waveで追加したC000327（シカゴ・ブルズ、2025年7月契約）までの間に、グリズリーズを具体的にいつ離れたかを示す直接資料が見つからなかった。end確定にはYuichiの追加判断または追加資料が必要。"},
    {"issue_id": "B4W5I0002", "category": "STATUS_VOLATILE", "scope": "P000064",
     "description": "河村勇輝の2026年8月時点のロサンゼルス・クリッパーズとの契約はエキシビット10契約（無保証のキャンプ契約）であり、レギュラーシーズン開幕までに2Way契約への転換や契約解除など状況が変わる可能性が高い。次回シーズン開幕後の再確認が必要。"},
]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


write_csv(BASE / "person_candidates.csv", ["person_id", "name"], [])
write_csv(BASE / "organization_candidates.csv", ["organization_id", "name"], ORGANIZATIONS)
write_csv(BASE / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], CAREERS)
write_csv(BASE / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], SOURCES)
write_csv(BASE / "evidence_records.csv",
          ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
           "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], EVIDENCE)
write_csv(BASE / "issues.csv", ["issue_id", "category", "scope", "description"], ISSUES)
write_csv(BASE / "qa_decisions.csv",
          ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"],
          DECISIONS)

print(f"Wrote batch_004/wave_05: {len(ORGANIZATIONS)} orgs, {len(CAREERS)} new careers, {len(SOURCES)} sources, "
      f"{len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues")
