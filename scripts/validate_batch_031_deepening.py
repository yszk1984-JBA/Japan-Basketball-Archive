#!/usr/bin/env python3
"""Validate Batch 031 (B.LEAGUE-era deepening of MASTER persons), all waves."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_031"


def main() -> int:
    errors: list[str] = []
    master_people = {r["person_id"] for r in read_csv(ROOT / "data/master/person.csv")}
    master_orgs = {r["organization_id"]: r["name"] for r in read_csv(ROOT / "data/master/organization.csv")}
    master_careers = read_csv(ROOT / "data/master/career.csv")
    corrections = {r["organization_id"]: r for r in read_csv(BASE / "org_corrections.csv")}

    other_career_ids = {r["career_id"] for r in master_careers}
    for path in (ROOT / "data" / "candidate").rglob("career_candidates.csv"):
        if BASE in path.parents:
            continue
        other_career_ids |= {r["career_id"] for r in read_csv(path)}
    other_orgs: dict[str, str] = dict(master_orgs)
    for path in (ROOT / "data" / "candidate").rglob("organization_candidates.csv"):
        if BASE in path.parents:
            continue
        for r in read_csv(path):
            other_orgs.setdefault(r["organization_id"], r["name"])

    totals = Counter()
    all_ids = Counter()
    lines = []
    for wave in sorted(BASE.glob("wave_*")):
        careers = read_csv(wave / "career_candidates.csv")
        orgs = read_csv(wave / "organization_candidates.csv")
        sources = {r["source_id"] for r in read_csv(wave / "source_references.csv")}
        evidence = read_csv(wave / "evidence_records.csv")
        issues = read_csv(wave / "issues.csv")
        decisions = read_csv(wave / "qa_decisions.csv")
        org_ids = {r["organization_id"] for r in orgs}
        for r in orgs:
            known = other_orgs.get(r["organization_id"])
            if known is not None and known != r["name"]:
                fix = corrections.get(r["organization_id"])
                if not (fix and fix["old_name"] == known and fix["new_name"] == r["name"]):
                    errors.append(f"{wave.name} {r['organization_id']}: 既存名{known!r}と不一致{r['name']!r}")
        career_ids = set()
        for c in careers:
            all_ids[c["career_id"]] += 1
            career_ids.add(c["career_id"])
            if c["career_id"] in other_career_ids:
                errors.append(f"{c['career_id']}: 既存Career IDと重複")
            if c["person_id"] not in master_people:
                errors.append(f"{c['career_id']}: MasterにないPerson {c['person_id']}")
            if c["organization_id"] not in org_ids:
                errors.append(f"{c['career_id']}: Organization参照が不足")
            if not c["start"].isdigit() or (c["end"] and (not c["end"].isdigit() or int(c["end"]) <= int(c["start"]))):
                errors.append(f"{c['career_id']}: start/endが不正 {c['start']}-{c['end']}")
            for m in master_careers:
                if m["person_id"] == c["person_id"] and m["organization_id"] == c["organization_id"] and m["start"] == c["start"]:
                    errors.append(f"{c['career_id']}: Master {m['career_id']}と同じ所属・開始年")
        covered = Counter()
        for e in evidence:
            if e["source_id"] not in sources:
                errors.append(f"{e['record_id']}: Source参照が不足")
            if e["entity_id"] not in career_ids:
                errors.append(f"{e['record_id']}: Career参照が不足")
            if not e["source_locator"]:
                errors.append(f"{e['record_id']}: Source内位置が不足")
            covered[(e["entity_id"], e["field_name"])] += 1
        for c in careers:
            if covered[(c["career_id"], "organization_id")] < 2:
                errors.append(f"{c['career_id']}: organization_idの根拠が2件（所属履歴＋順位表）そろっていない")
            if covered[(c["career_id"], "start")] < 1:
                errors.append(f"{c['career_id']}: startの根拠なし")
            if c["end"] and covered[(c["career_id"], "end")] < 1:
                errors.append(f"{c['career_id']}: endの根拠なし")
        decided = {d["entity_id"] for d in decisions}
        if decided != career_ids:
            errors.append(f"{wave.name}: 判断のないCareer {sorted(career_ids - decided)[:5]}")
        totals.update(careers=len(careers), evidence=len(evidence), issues=len(issues), sources=len(sources))
        lines.append(f"| {wave.name} | {len(careers)} | {len(evidence)} | {len(sources)} | {len(issues)} |")
    dup = [k for k, v in all_ids.items() if v > 1]
    if dup:
        errors.append(f"batch内でCareer ID重複: {dup[:5]}")

    report = [
        "# Batch 031 検証レポート", "", "作成日：2026-09-29", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}", f"- エラー：{len(errors)}件",
        f"- Career：{totals['careers']}件", f"- Evidence：{totals['evidence']}件",
        f"- Source：{totals['sources']}件", f"- Issue：{totals['issues']}件",
        "- VERIFIED・Master・公開サイト：未変更", "",
        "| Wave | Career | Evidence | Source | Issue |", "| --- | ---: | ---: | ---: | ---: |", *lines,
        "", "## エラー", "",
    ]
    report.extend(f"- {e}" for e in errors) if errors else report.append("- なし")
    (BASE / "validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
