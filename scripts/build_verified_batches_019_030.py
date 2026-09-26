#!/usr/bin/env python3
"""Promote all pending CANDIDATE waves from the powerhouse-school expansion
second round (Batch 019〜030, 第2弾 学校1〜12) to VERIFIED, one wave at a time.

Copied from build_verified_batches_008_018.py with a new MANIFEST.

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
CREATED_AT = "2026-09-26"

# (batch, wave, school label, source commit -- last commit touching that
# wave's candidate CSVs, i.e. its QA-final snapshot)
MANIFEST = [
    ("019", "wave_01", "桐光学園高等学校（第2弾 学校1/12）", "6e10d07"),
    ("019", "wave_02", "桐光学園高等学校（第2弾 学校1/12）", "6e10d07"),
    ("020", "wave_01", "船橋市立船橋高等学校（第2弾 学校2/12）", "2bc7c5e"),
    ("020", "wave_02", "船橋市立船橋高等学校（第2弾 学校2/12）", "2bc7c5e"),
    ("021", "wave_01", "中部大学第一高等学校（第2弾 学校3/12）", "a5ab646"),
    ("021", "wave_02", "中部大学第一高等学校（第2弾 学校3/12）", "a5ab646"),
    ("021", "wave_03", "中部大学第一高等学校（第2弾 学校3/12）", "a5ab646"),
    ("022", "wave_01", "尽誠学園高等学校（第2弾 学校4/12）", "0e35a77"),
    ("022", "wave_02", "尽誠学園高等学校（第2弾 学校4/12）", "0e35a77"),
    ("023", "wave_01", "前橋育英高等学校（第2弾 学校5/12）", "0e35a77"),
    ("024", "wave_01", "正智深谷高等学校（第2弾 学校6/12）", "0e35a77"),
    ("025", "wave_01", "帝京長岡高等学校（第2弾 学校7/12）", "406d8e6"),
    ("026", "wave_01", "桜丘高等学校（第2弾 学校8/12）", "0e35a77"),
    ("027", "wave_01", "秋田県立能代工業高等学校（第2弾 学校9/12）", "0e35a77"),
    ("027", "wave_02", "秋田県立能代工業高等学校（第2弾 学校9/12）", "406d8e6"),
    ("028", "wave_01", "報徳学園高等学校（第2弾 学校10/12）", "0e35a77"),
    ("029", "wave_01", "大阪桐蔭高等学校（第2弾 学校11/12）", "0e35a77"),
    ("030", "wave_01", "近畿大学附属高等学校（第2弾 学校12/12）", "0e35a77"),
]


def main() -> int:
    total_errors = 0
    grand_totals: dict[str, int] = {}
    summary_lines = [
        "# Batch 019〜030 VERIFIED promotion — 一括生成レポート", "",
        f"作成日：{CREATED_AT}", "",
        "強豪校横展開 第2弾（学校1〜12）の全CANDIDATE waveをVERIFIEDへ一括promotion。",
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
    (ROOT / "data" / "verified" / "BATCH_019_030_VERIFIED_SUMMARY.md").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )
    print(f"\nTotal: {grand_totals}, total_errors={total_errors}")
    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
