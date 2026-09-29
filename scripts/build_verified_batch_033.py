#!/usr/bin/env python3
"""Promote Batch 033 (B.ONE roster-based expansion) to VERIFIED.

Generic promotion (jba_lib.verify), one output directory per wave. Nothing
is written to data/master/*.csv.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.verify import build_verified, validate_verified  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CREATED_AT = "2026-09-30"
SOURCE_COMMIT = "c74d473"
WAVES = ["wave_01", "wave_02", "wave_03", "wave_04", "wave_05"]


def main() -> int:
    lines = ["# Batch 033 VERIFIED promotion — 生成レポート", "", f"作成日：{CREATED_AT}", "",
             f"CANDIDATE・QA基準commit：`{SOURCE_COMMIT}`（B.ONEロスター起点の横展開）", "",
             "| Wave | Person | Career | Org | Evidence | HOLD Issue | 検証 |",
             "| --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    total = 0
    for wave in WAVES:
        wave_dir = ROOT / "data/candidate/batch_033" / wave
        out = ROOT / "data/verified" / f"batch_033_{wave}"
        label = f"Batch 33 Wave {int(wave[-2:])} (B.ONEロスター起点の横展開)"
        c = build_verified(ROOT, wave_dir, out, SOURCE_COMMIT, CREATED_AT, label)
        errors = validate_verified(ROOT, out, wave_dir, label, CREATED_AT)
        total += len(errors)
        lines.append(f"| {wave} | {c['persons']} | {c['careers']} | {c['organizations']} | {c['evidence']} | {c['issues']} | {'PASS' if not errors else 'FAIL'} |")
        print(wave, c, errors[:3])
    lines += ["", f"- エラー合計：{total}件", "", "HUMAN APPROVAL・Master・公開サイトへの反映はこの生成には含まれない。"]
    (ROOT / "data/verified/BATCH_033_VERIFIED_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
