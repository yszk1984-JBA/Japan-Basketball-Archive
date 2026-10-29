#!/usr/bin/env python3
"""Promote batch_038 wave_01 (B.LEAGUE DRAFT 2026 players) to VERIFIED after checking that the
CANDIDATE snapshot is unchanged since review, every target still matches MASTER and every
value has SUPPORTED evidence. Additions to existing MASTER entities are carried as evidence."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/candidate/batch_038/wave_01"
OUT = ROOT / "data/verified/batch_038_wave_01"
SOURCE_COMMIT = "b799eb6"


def main() -> int:
    paths = [str(p.relative_to(ROOT)) for p in sorted(SRC.glob("*.csv"))]
    if not SOURCE_COMMIT or subprocess.run(["git", "diff", "--quiet", SOURCE_COMMIT, "--", *paths], cwd=ROOT).returncode:
        raise SystemExit("CANDIDATE changed after review (or no commit given)")
    errors = []
    people = {r["person_id"] for r in read_csv(ROOT / "data/master/person.csv")}
    master = {r["career_id"]: r for r in read_csv(ROOT / "data/master/career.csv")}
    orgs = {r["organization_id"] for r in read_csv(ROOT / "data/master/organization.csv")}
    ev = read_csv(SRC / "evidence_records.csv")
    src = {r["source_id"] for r in read_csv(SRC / "source_references.csv")}
    corr = read_csv(SRC / "master_corrections.csv")
    careers = read_csv(SRC / "career_candidates.csv")
    new_orgs = {r["organization_id"] for r in read_csv(SRC / "organization_candidates.csv")}
    new_cids = {c["career_id"] for c in careers}
    for c in corr:
        m = master.get(c["career_id"])
        if not m or (m["start"], m["end"]) != (c["old_start"], c["old_end"]):
            errors.append(f"{c['career_id']}: MASTERの値が訂正前と一致しない")
        for f in ("start", "end"):
            if c[f"old_{f}"] != c[f"new_{f}"] and not any(e["entity_id"] == c["career_id"] and e["field_name"] == f and e["candidate_value"] == c[f"new_{f}"] for e in ev):
                errors.append(f"{c['career_id']}: {f}の根拠なし")
    for c in careers:
        if c["person_id"] not in people or c["organization_id"] not in orgs | new_orgs or c["career_id"] in master:
            errors.append(f"{c['career_id']}: 不正なCareer")
    for e in ev:
        if e["assessment"] != "SUPPORTED" or e["source_id"] not in src:
            errors.append(f"{e['record_id']}: SUPPORTEDでない、または出典なし")
        if e["entity_type"] == "Person" and e["entity_id"] not in people:
            errors.append(f"{e['record_id']}: MasterにないPerson")
        if e["entity_type"] == "Career" and e["entity_id"] not in master and e["entity_id"] not in new_cids:
            errors.append(f"{e['record_id']}: 不明なCareer")
    OUT.mkdir(parents=True, exist_ok=True)
    for n in ("master_corrections.csv", "evidence_records.csv", "source_references.csv", "career_candidates.csv",
              "organization_candidates.csv", "issues.csv"):
        shutil.copy(SRC / n, OUT / n)
    (OUT / "validation_report.md").write_text(
        f"# Batch 38 Wave 1（B.LEAGUE DRAFT 2026）VERIFIED検証レポート\n\n作成日：2026-10-29\n\n- 基準commit：`{SOURCE_COMMIT}`\n"
        f"- 検証：{'PASS' if not errors else 'FAIL'}\n- 期間訂正：{len(corr)}件、Career追加：{len(careers)}件、Evidence：{len(ev)}件\n"
        "- HUMAN APPROVAL・Master：未実施\n\n## エラー\n\n" + ("\n".join(f"- {e}" for e in errors) if errors else "- なし") + "\n",
        encoding="utf-8")
    print("errors", errors)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
