#!/usr/bin/env python3
"""Promote batch_034 wave_01 (2026-10-29 update) to VERIFIED.

Generic promotion (jba_lib.verify). 石川裕大's new Career belongs to a person
already in MASTER, so the generic "unknown person" error is replaced by a
MASTER-membership check (same as build_verified_batch_004_wave_07.py). The
MASTER period corrections are carried as master_corrections.csv with their
SUPPORTED evidence.
"""

from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.verify import build_verified, validate_verified  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CREATED_AT = "2026-10-29"
SOURCE_COMMIT = "78525ec"
WAVE = ROOT / "data/candidate/batch_037/wave_01"
OUT = ROOT / "data/verified/batch_037_wave_01"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def main() -> int:
    label = "Batch 37 Wave 1 (2026-10-29の更新)"
    counts = build_verified(ROOT, WAVE, OUT, SOURCE_COMMIT, CREATED_AT, label)
    errors = validate_verified(ROOT, OUT, WAVE, label, CREATED_AT)
    master_people = {r["person_id"] for r in read(ROOT / "data/master/person.csv")}
    careers = {r["career_id"]: r for r in read(OUT / "career_verified.csv")}
    kept = [e for e in errors if not (e.endswith("unknown person") and careers.get(e.split(":")[0], {}).get("person_id") in master_people)]
    shutil.copy(WAVE / "master_corrections.csv", OUT / "master_corrections.csv")
    corr = read(OUT / "master_corrections.csv")
    corr_ids = {r["career_id"] for r in corr}
    corr_ev = [e for e in read(WAVE / "evidence_records.csv") if e["entity_id"] in corr_ids and e["assessment"] == "SUPPORTED"]
    with (OUT / "master_correction_evidence.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(corr_ev[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(corr_ev)
    for c in corr:
        for field in ("start", "end"):
            if c[f"old_{field}"] != c[f"new_{field}"] and not any(
                    e["entity_id"] == c["career_id"] and e["field_name"] == field and e["candidate_value"] == c[f"new_{field}"] for e in corr_ev):
                kept.append(f"{c['career_id']}: {field}の訂正案に根拠なし")
    src_all = {r["source_id"]: r for r in read(WAVE / "source_references.csv")}
    have = {r["source_id"] for r in read(OUT / "source_references.csv")}
    extra = [src_all[s] for s in dict.fromkeys(e["source_id"] for e in corr_ev) if s not in have]
    if extra:
        with (OUT / "source_references.csv").open("a", encoding="utf-8", newline="") as h:
            csv.DictWriter(h, fieldnames=list(extra[0].keys()), lineterminator="\n").writerows(extra)
    report = (OUT / "validation_report.md").read_text(encoding="utf-8").split("## エラー")[0]
    report = report.replace(f"- エラー：{len(errors)}件", f"- エラー：{len(kept)}件").replace(
        "- 検証：FAIL" if errors else "- 検証：PASS", f"- 検証：{'PASS' if not kept else 'FAIL'}")
    report += "## エラー\n\n" + ("\n".join(f"- {e}" for e in kept) if kept else "- なし") + \
        "\n\n注：既存の人物（河村・ジャンバルボ・長島・長谷川）はMaster登録済み。汎用検証の「unknown person」はMasterに人物がいることの確認に置き換えた。Masterの期間訂正案3件は`master_corrections.csv`と`master_correction_evidence.csv`。\n"
    (OUT / "validation_report.md").write_text(report, encoding="utf-8")
    print(counts, "errors", kept)
    return 1 if kept else 0


if __name__ == "__main__":
    raise SystemExit(main())
