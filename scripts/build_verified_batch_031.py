#!/usr/bin/env python3
"""Promote Batch 031 (B.LEAGUE-era deepening of MASTER persons) to VERIFIED.

Same promotion logic as build_verified_batches_019_030.py (jba_lib.verify).
The only difference: every Career here belongs to a person who is ALREADY in
MASTER, so validate_verified's generic "unknown person" check (which expects
the person row inside the same wave) is replaced by a check that the person
exists in MASTER. Nothing is written to data/master/*.csv.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.verify import build_verified, validate_verified  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CREATED_AT = "2026-09-29"
SOURCE_COMMIT = "2120f79"
WAVES = ["wave_01", "wave_02", "wave_03", "wave_04"]


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def main() -> int:
    master_people = {r["person_id"] for r in read(ROOT / "data/master/person.csv")}
    total_errors = 0
    lines = ["# Batch 031 VERIFIED promotion — 生成レポート", "", f"作成日：{CREATED_AT}", "",
             "B.LEAGUE期の過去所属クラブ深掘り（Master既存選手）の各waveをVERIFIEDへpromotion。", "",
             "| Wave | Career | Org | Evidence | HOLD Issue | 検証 |", "| --- | ---: | ---: | ---: | ---: | --- |"]
    totals = {}
    for wave in WAVES:
        wave_dir = ROOT / "data/candidate/batch_031" / wave
        out = ROOT / "data/verified" / f"batch_031_{wave}"
        label = f"Batch 31 Wave {int(wave[-2:])} (B.LEAGUE期 過去所属クラブ深掘り)"
        counts = build_verified(ROOT, wave_dir, out, SOURCE_COMMIT, CREATED_AT, label)
        errors = validate_verified(ROOT, out, wave_dir, label, CREATED_AT)
        careers = {r["career_id"]: r for r in read(out / "career_verified.csv")}
        kept = []
        for e in errors:
            cid = e.split(":")[0]
            if e.endswith("unknown person") and careers.get(cid, {}).get("person_id") in master_people:
                continue
            kept.append(e)
        bad = [c for c in careers.values() if c["person_id"] not in master_people]
        kept += [f"{c['career_id']}: MasterにないPerson" for c in bad]
        report = (out / "validation_report.md").read_text(encoding="utf-8").split("## エラー")[0]
        report = report.replace(f"- エラー：{len(errors)}件", f"- エラー：{len(kept)}件").replace(
            "- 検証：FAIL" if errors else "- 検証：PASS", f"- 検証：{'PASS' if not kept else 'FAIL'}")
        report += "## エラー\n\n" + ("\n".join(f"- {e}" for e in kept) if kept else "- なし") + \
            "\n\n注：本BatchのCareerはすべてMaster登録済みの人物のもの。汎用検証の「同じwave内に人物行がない」エラーは、人物がMasterに存在することの確認に置き換えた。\n"
        (out / "validation_report.md").write_text(report, encoding="utf-8")
        total_errors += len(kept)
        for k, v in counts.items():
            totals[k] = totals.get(k, 0) + v
        lines.append(f"| {wave} | {counts['careers']} | {counts['organizations']} | {counts['evidence']} | {counts['issues']} | {'PASS' if not kept else 'FAIL'} |")
        print(wave, counts, "errors", len(kept))
    lines += ["", f"- 合計Career：{totals['careers']}件、Evidence：{totals['evidence']}件、HOLD Issue：{totals['issues']}件",
              f"- エラー合計：{total_errors}件", "", "HUMAN APPROVAL・Master・公開サイトへの反映はこの生成には含まれない。"]
    (ROOT / "data/verified/BATCH_031_VERIFIED_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
