#!/usr/bin/env python3
"""Corrections 001: fill missing periods of current-club MASTER Careers of
B.PREMIER players (CANDIDATE).

Yuichi (2026-10-04): 「現在のBリーグプレミア所属選手のリサーチの深堀りをしたい」,
choosing 「期間未記録のクラブ在籍（12名14件）」. Of the 14 undated non-school
rows, 8 were schools whose names the quick filter missed; the 6 real club
Careers are corrected here. They are the batch_031 MASTER_PERIOD_DIFFERENCE
issues for B.PREMIER players with an empty period. Two other issues of that
kind (佐藤涼成 C000265, 渡邉伶音 C000419) have a period already set from a
different convention (special-designation activity dates / pro-contract
year) and are left to Yuichi's decision, not changed here.

Rule (batch_031): start = first season's start year of the continuous stay
that includes 2026-27; no end while on the 2026-27 roster. Club history was
re-read from each B.LEAGUE profile on 2026-10-04 (unchanged since
2026-09-29; raw: data/raw/research/bleague_club_history_2026-10-04_premier_periods.txt).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/corrections_001"
CHECKED = "2026-10-04"
# career, person, PlayerID, name, club, new_start, history rows (first..last of the stay), batch_031 issue
ROWS = [
    ("C000088", "P000035", "5100000033", "小川麻斗", "神戸ストークス", "2026", "「2026-27 神戸」", "B31W1I0006"),
    ("C000103", "P000037", "8529", "鵤誠司", "宇都宮ブレックス", "2017", "「2017-18 栃木」〜「2026-27 宇都宮」（栃木＝宇都宮ブレックスの改称前、TeamID 703）", "B31W1I0008"),
    ("C000107", "P000038", "51000353", "内尾聡理", "佐賀バルーナーズ", "2025", "「2025-26 佐賀」〜「2026-27 佐賀」", "B31W1I0009"),
    ("C000117", "P000039", "9329", "渡辺竜之佑", "京都ハンナリーズ", "2025", "「2025-26 京都」〜「2026-27 京都」", "B31W1I0011"),
    ("C000140", "P000042", "9489", "並里成", "横浜ビー・コルセアーズ", "2026", "「2026-27 横浜BC」", "B31W1I0016"),
    ("C000226", "P000065", "51000552", "児玉ジュニア", "三遠ネオフェニックス", "2025", "「2025-26 三遠」〜「2026-27 三遠」", "B31W1I0021"),
]


def main() -> None:
    master = {r["career_id"]: r for r in read_csv(ROOT / "data/master/career.csv")}
    sources, evidence, corr = [], [], []
    for i, (cid, pid, bid, name, club, start, rows, issue) in enumerate(ROWS, 1):
        m = master[cid]
        if m["person_id"] != pid or m["start"] or m["end"]:
            raise SystemExit(f"{cid}: MASTER row is not the expected undated row")
        sid = f"COR1S{i:04d}"
        sources.append({"source_id": sid, "title": f"{name} 選手プロフィール（クラブ所属履歴）", "publisher": "B.LEAGUE",
                        "url": f"https://www.bleague.jp/roster_detail/?PlayerID={bid}", "accessed_at": CHECKED})
        evidence.append({"record_id": f"COR1E{i:04d}", "entity_type": "Career", "entity_id": cid, "field_name": "start",
                         "candidate_value": start, "source_id": sid, "source_locator": f"クラブ所属履歴 > {rows}",
                         "evidence_summary": f"B.LEAGUE公式の所属履歴で{club}への在籍開始シーズンを確認（2026-27在籍中のため終了年なし）",
                         "assessment": "SUPPORTED", "checked_at": CHECKED,
                         "issue_note": f"既存MASTER Careerの期間の訂正案（batch_031 {issue}）"})
        corr.append({"career_id": cid, "person_id": pid, "organization_name": club, "old_start": "", "old_end": "",
                     "new_start": start, "new_end": "", "reason": f"B.LEAGUE公式の所属履歴 {rows}（batch_031 {issue}）"})
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], sources)
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "master_corrections.csv", ["career_id", "person_id", "organization_name", "old_start", "old_end",
                                               "new_start", "new_end", "reason"], corr)
    print(f"corrections_001: {len(corr)} corrections, {len(evidence)} evidence")


if __name__ == "__main__":
    main()
