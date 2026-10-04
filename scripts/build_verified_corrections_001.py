#!/usr/bin/env python3
"""Promote corrections_001 to VERIFIED: copy the SUPPORTED evidence, their
sources and the correction list after checking the CANDIDATE snapshot is
unchanged since review and every correction still matches MASTER."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/candidate/corrections_001"
OUT = ROOT / "data/verified/corrections_001"
SOURCE_COMMIT = "a79f491"


def main() -> int:
    paths = [str(p.relative_to(ROOT)) for p in sorted(SRC.glob("*.csv"))]
    if subprocess.run(["git", "diff", "--quiet", SOURCE_COMMIT, "--", *paths], cwd=ROOT).returncode:
        raise SystemExit("CANDIDATE changed after review")
    errors = []
    master = {r["career_id"]: r for r in read_csv(ROOT / "data/master/career.csv")}
    corr = read_csv(SRC / "master_corrections.csv")
    ev = read_csv(SRC / "evidence_records.csv")
    src = {r["source_id"] for r in read_csv(SRC / "source_references.csv")}
    for c in corr:
        m = master.get(c["career_id"])
        if not m or (m["start"], m["end"]) != (c["old_start"], c["old_end"]):
            errors.append(f"{c['career_id']}: MASTERの値が訂正前と一致しない")
        if not any(e["entity_id"] == c["career_id"] and e["field_name"] == "start" and e["candidate_value"] == c["new_start"]
                   and e["assessment"] == "SUPPORTED" for e in ev):
            errors.append(f"{c['career_id']}: startの根拠なし")
    if any(e["source_id"] not in src for e in ev):
        errors.append("Source参照が不足")
    OUT.mkdir(parents=True, exist_ok=True)
    for n in ("master_corrections.csv", "evidence_records.csv", "source_references.csv"):
        shutil.copy(SRC / n, OUT / n)
    (OUT / "validation_report.md").write_text(
        f"# Corrections 001 VERIFIED検証レポート\n\n作成日：2026-10-04\n\n- 基準commit：`{SOURCE_COMMIT}`\n- 検証：{'PASS' if not errors else 'FAIL'}\n"
        f"- 訂正案：{len(corr)}件、Evidence：{len(ev)}件\n- HUMAN APPROVAL・Master：未実施\n\n## エラー\n\n" +
        ("\n".join(f"- {e}" for e in errors) if errors else "- なし") + "\n", encoding="utf-8")
    print("errors", errors)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
