#!/usr/bin/env python3
"""Promote all pending CANDIDATE waves from the powerhouse-school expansion
(Batch 008〜018, 学校1〜11) to VERIFIED, one wave at a time.

This is the CANDIDATE -> VERIFIED step only (Governance v1.0 lifecycle:
RAW -> CANDIDATE -> QA -> VERIFIED -> HUMAN APPROVAL -> MASTER). It never
writes to data/master/*.csv and never records a Human Approval decision;
those remain Yuichi's alone, via a separate approval-sprint step and his
own explicit reply in chat.

Each wave already has its own QA (see the per-wave validate_batch_*.py
scripts). This script only re-applies the exact promotion logic used by
the earlier hand-written build_batch_006_wave_02_verified.py (now shared
in jba_lib/verify.py) to every wave in the batch, rather than
hand-copying a near-identical script 22 times.

Naming convention for output directories: always `batch_XXX_wave_YY`,
even for a batch with only one wave (earlier sprints sometimes used a
bare `batch_XXX` name for a batch's first/only wave -- this script uses
the wave-qualified name uniformly, for less ambiguity as more waves are
processed together).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.verify import build_verified, validate_verified  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CREATED_AT = "2026-09-25"

# (batch, wave, school label, source commit -- last commit touching that
# wave's candidate CSVs, i.e. its QA-final snapshot)
MANIFEST = [
    ("008", "wave_01", "福岡大学附属大濠高等学校（学校1/11）", "1789cfd"),
    ("008", "wave_02", "福岡大学附属大濠高等学校（学校1/11）", "b8018ad"),
    ("008", "wave_03", "福岡大学附属大濠高等学校（学校1/11）", "b8018ad"),
    ("008", "wave_04", "福岡大学附属大濠高等学校（学校1/11）", "b8018ad"),
    ("009", "wave_01", "仙台大学附属明成高等学校（学校2/11）", "88af82d"),
    ("010", "wave_01", "洛南高等学校（学校3/11）", "38890c8"),
    ("010", "wave_02", "洛南高等学校（学校3/11）", "38890c8"),
    ("010", "wave_03", "洛南高等学校（学校3/11）", "38890c8"),
    ("010", "wave_04", "洛南高等学校（学校3/11）", "38890c8"),
    ("011", "wave_01", "開志国際高等学校（学校4/11）", "ec26ab7"),
    ("012", "wave_01", "延岡学園高等学校（学校5/11）", "6a78892"),
    ("013", "wave_01", "東山高等学校（学校6/11）", "0dac068"),
    ("013", "wave_02", "東山高等学校（学校6/11）", "0dac068"),
    ("014", "wave_01", "北陸高等学校（学校7/11）", "426e72f"),
    ("014", "wave_02", "北陸高等学校（学校7/11）", "426e72f"),
    ("014", "wave_03", "北陸高等学校（学校7/11）", "426e72f"),
    ("014", "wave_04", "北陸高等学校（学校7/11）", "426e72f"),
    ("015", "wave_01", "藤枝明誠高等学校（学校8/11）", "ec65cf5"),
    ("015", "wave_02", "藤枝明誠高等学校（学校8/11）", "ec65cf5"),
    ("017", "wave_01", "土浦日本大学高等学校（学校10/11）", "973a1d9"),
    ("017", "wave_02", "土浦日本大学高等学校（学校10/11）", "973a1d9"),
    ("018", "wave_01", "八王子学園八王子高等学校（学校11/11）", "3fdd985"),
]


def main() -> int:
    total_errors = 0
    grand_totals: dict[str, int] = {}
    summary_lines = [
        "# Batch 008〜018 VERIFIED promotion — 一括生成レポート", "",
        f"作成日：{CREATED_AT}", "",
        "強豪校水平展開（学校1〜11）の全CANDIDATE waveをVERIFIEDへ一括promotion。",
        "各waveの詳細は `data/verified/batch_XXX_wave_YY/` を参照。", "",
        "| Batch | Wave | 学校 | Person | Career | Org | Evidence | HOLD Issue | 検証 |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for batch, wave, label_school, commit in MANIFEST:
        wave_dir = ROOT / "data" / "candidate" / f"batch_{batch}" / wave
        output_name = f"batch_{batch}_{wave}"
        output_dir = ROOT / "data" / "verified" / output_name
        label = f"Batch {int(batch)} {wave.replace('wave_', 'Wave ').lstrip('0') or wave} ({label_school})"

        counts = build_verified(ROOT, wave_dir, output_dir, commit, CREATED_AT, label)
        errors = validate_verified(ROOT, output_dir, wave_dir, label, CREATED_AT)
        total_errors += len(errors)
        for key, value in counts.items():
            grand_totals[key] = grand_totals.get(key, 0) + value

        status = "PASS" if not errors else f"FAIL({len(errors)})"
        summary_lines.append(
            f"| {batch} | {wave} | {label_school} | {counts['persons']} | {counts['careers']} | "
            f"{counts['organizations']} | {counts['evidence']} | {counts['issues']} | {status} |"
        )
        print(f"{output_name}: {counts}, errors={len(errors)}")

    summary_lines.extend([
        "", "## 合計",
        f"- Person：{grand_totals.get('persons', 0)}件",
        f"- Career：{grand_totals.get('careers', 0)}件",
        f"- Organization：{grand_totals.get('organizations', 0)}件",
        f"- Evidence：{grand_totals.get('evidence', 0)}件",
        f"- HOLD Issue：{grand_totals.get('issues', 0)}件",
        f"- Wave数：{len(MANIFEST)}",
        f"- エラー合計：{total_errors}件",
        "", "HUMAN APPROVAL・Master・公開サイトへの反映はこの生成には含まれない。",
    ])
    (ROOT / "data" / "verified" / "BATCH_008_018_VERIFIED_SUMMARY.md").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )
    print(f"\nTotal: {grand_totals}, total_errors={total_errors}")
    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
