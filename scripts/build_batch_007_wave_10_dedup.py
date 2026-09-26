#!/usr/bin/env python3
"""Batch 007 Wave 10: retire two CANDIDATE persons that duplicate MASTER persons.

Found 2026-09-26 by a global name check across master + every candidate
person file:

- 篠山竜青: CANDIDATE P000085 (batch_007/wave_01) duplicates MASTER P000176
  (batch_014/wave_03, approved in Approval Sprint 006).
- 高島紳司: CANDIDATE P000110 (batch_007/wave_09) duplicates MASTER P000165
  (batch_014/wave_01, approved in Approval Sprint 006).

Yuichi asked (2026-09-26) to consolidate them. The MASTER IDs are kept and
MASTER data is NOT changed. The CANDIDATE duplicates are retired by writing
REJECT_CANDIDATE decisions for the Person and its Careers in this later
wave; build_site_candidate_data.py takes the latest decision per entity, so
the duplicates stop appearing as candidate pages on the site. Original
batch_007 rows are left untouched (history is preserved).

Candidate-only facts not yet in MASTER (篠山: 北陸 start 2004 / 日本大学 end
2011 from Wikipedia-level sources) are NOT carried over; they are logged as
an issue for a later deepening wave through the normal approval path.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_007" / "wave_10"
REVIEWED_AT = "2026-09-26"

DUPLICATES = [
    # (candidate person, candidate careers, master person, name)
    ("P000085", ["C000296", "C000297", "C000298"], "P000176", "篠山竜青"),
    ("P000110", ["C000377", "C000378", "C000379"], "P000165", "高島紳司"),
]


def main() -> None:
    decisions, issues = [], []
    d = 128
    for cand, careers, master, name in DUPLICATES:
        reason = f"MASTER {master}（{name}）と同一人物の重複登録。Yuichiの指示（2026-09-26）によりMASTERのIDに統合し、本候補は取り下げ"
        for entity_type, entity_id in [("Person", cand)] + [("Career", c) for c in careers]:
            d += 1
            decisions.append({
                "decision_id": f"B7D{d:04d}", "entity_type": entity_type, "entity_id": entity_id,
                "decision": "REJECT_CANDIDATE", "eligible_fields": "", "held_fields": "",
                "reason": reason, "reviewed_at": REVIEWED_AT,
            })
    issues.append({
        "issue_id": "B7I0031", "category": "DUPLICATE_OF_MASTER", "scope": "P000085,P000110",
        "description": "篠山竜青（候補P000085＝MASTER P000176）と高島紳司（候補P000110＝MASTER P000165）が別IDで重複登録されていた。YuichiがMASTER側への統合を指示（2026-09-26）。MASTERは変更せず、候補側のPerson・CareerをREJECT_CANDIDATEとして取り下げた。",
    })
    issues.append({
        "issue_id": "B7I0032", "category": "CANDIDATE_ONLY_FACTS", "scope": "P000085→P000176",
        "description": "取り下げた候補P000085には、MASTER P000176にない値（北陸高等学校の開始2004年、日本大学の終了2011年。いずれもWikipedia等の出典）がある。統合時には移していない。必要なら深掘りWaveでMASTER P000176向けに改めて候補化し、通常の承認経路で扱う。",
    })
    empty = {
        "person_candidates.csv": ["person_id", "name"],
        "organization_candidates.csv": ["organization_id", "name"],
        "career_candidates.csv": ["career_id", "person_id", "organization_id", "role", "start", "end"],
        "source_references.csv": ["source_id", "title", "publisher", "url", "accessed_at"],
        "evidence_records.csv": ["record_id", "entity_type", "entity_id", "field_name", "candidate_value",
                                 "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"],
    }
    for fname, header in empty.items():
        write_csv(BASE / fname, header, [])
    write_csv(BASE / "qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision",
                                          "eligible_fields", "held_fields", "reason", "reviewed_at"], decisions)
    write_csv(BASE / "issues.csv", ["issue_id", "category", "scope", "description"], issues)
    (BASE / "README.md").write_text(
        "# Batch 007 Wave 10: 重複候補の取り下げ（MASTERへの統合）\n\n"
        "作成日：2026-09-26\n\n"
        "全Person名の横断チェックで、次の2名がCANDIDATEとMASTERに別IDで重複登録されていることが判明した。"
        "Yuichiの指示（2026-09-26「まとめたい」）により、MASTER側のIDに統合した。\n\n"
        "| 氏名 | 取り下げた候補ID | 残すMASTER ID |\n| --- | --- | --- |\n"
        "| 篠山竜青 | P000085（C000296〜C000298） | P000176 |\n"
        "| 高島紳司 | P000110（C000377〜C000379） | P000165 |\n\n"
        "- MASTERのデータは変更していない。\n"
        "- 候補側は元のwave_01・wave_09の行を残したまま、本WaveでPerson・CareerをREJECT_CANDIDATEとした（最新の判断が優先されるため、サイトの候補ページからも外れる）。\n"
        "- 候補側にだけあった値（篠山竜青の北陸高等学校開始2004年・日本大学終了2011年）は移していない（issue B7I0032）。\n",
        encoding="utf-8")
    print(f"Wrote batch_007/wave_10: {len(decisions)} decisions, {len(issues)} issues")


if __name__ == "__main__":
    main()
