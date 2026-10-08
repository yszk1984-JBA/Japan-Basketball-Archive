#!/usr/bin/env python3
"""Promote batch_007 wave_13 (八村・馬場・比江島 overseas careers) to VERIFIED.

Generic promotion (jba_lib.verify). 馬場・比江島 are in MASTER (八村 is this wave's person), so the
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
CREATED_AT = "2026-10-08"
SOURCE_COMMIT = "0956d97"
WAVE = ROOT / "data/candidate/batch_007/wave_13"
OUT = ROOT / "data/verified/batch_007_wave_13"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def main() -> int:
    label = "Batch 7 Wave 13 (八村塁・馬場雄大・比江島慎 海外経歴)"
    counts = build_verified(ROOT, WAVE, OUT, SOURCE_COMMIT, CREATED_AT, label)
    errors = validate_verified(ROOT, OUT, WAVE, label, CREATED_AT)
    master_people = {r["person_id"] for r in read(ROOT / "data/master/person.csv")}
    careers = {r["career_id"]: r for r in read(OUT / "career_verified.csv")}
    kept = [e for e in errors if not (e.endswith("unknown person") and careers.get(e.split(":")[0], {}).get("person_id") in master_people)]
    report = (OUT / "validation_report.md").read_text(encoding="utf-8").split("## エラー")[0]
    report = report.replace(f"- エラー：{len(errors)}件", f"- エラー：{len(kept)}件").replace(
        "- 検証：FAIL" if errors else "- 検証：PASS", f"- 検証：{'PASS' if not kept else 'FAIL'}")
    report += "## エラー\n\n" + ("\n".join(f"- {e}" for e in kept) if kept else "- なし") + \
        "\n\n注：八村塁（P000104）は本Waveの人物候補。馬場・比江島はMaster登録済み。汎用検証の「unknown person」はMasterに人物がいることの確認に置き換えた。\n"
    (OUT / "validation_report.md").write_text(report, encoding="utf-8")
    print(counts, "errors", kept)
    return 1 if kept else 0


if __name__ == "__main__":
    raise SystemExit(main())
