#!/usr/bin/env python3
"""Promote batch_032 wave_06 (出身高校) to VERIFIED.

Generic promotion (jba_lib.verify). The persons are already in MASTER, so the
generic "unknown person" error is replaced by a MASTER-membership check
(same as build_verified_batch_004_wave_07.py).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.verify import build_verified, validate_verified  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CREATED_AT = "2026-10-06"
SOURCE_COMMIT = "9aed4ed"
WAVE = ROOT / "data/candidate/batch_032/wave_06"
OUT = ROOT / "data/verified/batch_032_wave_06"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def main() -> int:
    label = "Batch 32 Wave 6 (出身高校)"
    counts = build_verified(ROOT, WAVE, OUT, SOURCE_COMMIT, CREATED_AT, label)
    errors = validate_verified(ROOT, OUT, WAVE, label, CREATED_AT)
    master_people = {r["person_id"] for r in read(ROOT / "data/master/person.csv")}
    careers = {r["career_id"]: r for r in read(OUT / "career_verified.csv")}
    kept = [e for e in errors if not (e.endswith("unknown person") and careers.get(e.split(":")[0], {}).get("person_id") in master_people)]
    report = (OUT / "validation_report.md").read_text(encoding="utf-8").split("## エラー")[0]
    report = report.replace(f"- エラー：{len(errors)}件", f"- エラー：{len(kept)}件").replace(
        "- 検証：FAIL" if errors else "- 検証：PASS", f"- 検証：{'PASS' if not kept else 'FAIL'}")
    report += "## エラー\n\n" + ("\n".join(f"- {e}" for e in kept) if kept else "- なし") + \
        "\n\n注：対象の人物はすべてMaster登録済み。汎用検証の「unknown person」はMasterに人物がいることの確認に置き換えた。\n"
    (OUT / "validation_report.md").write_text(report, encoding="utf-8")
    print(counts, "errors", kept)
    return 1 if kept else 0


if __name__ == "__main__":
    raise SystemExit(main())
