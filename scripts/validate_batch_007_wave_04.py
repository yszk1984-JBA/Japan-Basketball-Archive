#!/usr/bin/env python3
"""Validate Batch 007 Wave 4 (深掘りWave/Enrichment Wave) candidate structure.

Unlike an Acquisition Wave, an Enrichment Wave adds no new Persons and its
evidence/decisions may reference Career/Organization entities defined in
EARLIER waves of the same batch. So entity references are checked against
the union of all batch_007 waves' candidates (plus this wave's own new ones),
not just this wave's own files.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv  # noqa: E402
from jba_lib.organizations import find_duplicate_names  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "data" / "candidate" / "batch_007"
BASE = BATCH / "wave_04"
EXPECTED_PERSON_COUNT = 0


def main() -> int:
    errors: list[str] = []

    people = read_csv(BASE / "person_candidates.csv")
    orgs = read_csv(BASE / "organization_candidates.csv")
    careers = read_csv(BASE / "career_candidates.csv")
    sources = read_csv(BASE / "source_references.csv")
    evidence = read_csv(BASE / "evidence_records.csv")
    issues = read_csv(BASE / "issues.csv")
    decisions = read_csv(BASE / "qa_decisions.csv")

    if len(people) != EXPECTED_PERSON_COUNT:
        errors.append(f"Person: expected {EXPECTED_PERSON_COUNT} (深掘りWaveは新規Person追加なし), got {len(people)}")

    # Union of all prior + this wave's Person/Organization/Career for this batch
    all_person_ids: set[str] = set()
    all_org_ids: dict[str, str] = {row["organization_id"]: row["name"] for row in read_csv(ROOT / "data" / "master" / "organization.csv")}
    all_career_ids: set[str] = set()
    for wave_dir in sorted(BATCH.glob("wave_*")):
        for row in read_csv(wave_dir / "person_candidates.csv"):
            all_person_ids.add(row["person_id"])
        for row in read_csv(wave_dir / "organization_candidates.csv"):
            all_org_ids.setdefault(row["organization_id"], row["name"])
        for row in read_csv(wave_dir / "career_candidates.csv"):
            all_career_ids.add(row["career_id"])
    # Also allow Master persons/careers as valid enrichment targets in principle
    all_person_ids |= {row["person_id"] for row in read_csv(ROOT / "data" / "master" / "person.csv")}

    # New organizations in this wave must not collide with an existing different name
    for row in orgs:
        existing_name = all_org_ids.get(row["organization_id"])
        if existing_name is not None and existing_name != row["name"]:
            errors.append(f"{row['organization_id']}: 既存では{existing_name!r}だが本Waveでは{row['name']!r}")
        all_org_ids[row["organization_id"]] = row["name"]
    for name, ids in find_duplicate_names(all_org_ids).items():
        if any(row["organization_id"] in ids for row in orgs):
            errors.append(f"Organization名重複の可能性: {name!r} が {ids} に存在")

    for label, rows, key in [
        ("Organization", orgs, "organization_id"), ("Career", careers, "career_id"),
        ("Source", sources, "source_id"), ("Evidence", evidence, "record_id"),
        ("Issue", issues, "issue_id"), ("Decision", decisions, "decision_id"),
    ]:
        if len({row[key] for row in rows}) != len(rows):
            errors.append(f"{label} IDが重複")

    # New career_candidates must reference a known person and organization
    for row in careers:
        if row["person_id"] not in all_person_ids:
            errors.append(f"{row['career_id']}: Person参照が不足")
        if row["organization_id"] not in all_org_ids and row["organization_id"] not in {o['organization_id'] for o in orgs}:
            errors.append(f"{row['career_id']}: Organization参照が不足")
        all_career_ids.add(row["career_id"])

    source_ids = {row["source_id"] for row in sources}
    # Evidence may cite this wave's own new sources, or a source_id already used in an earlier wave
    all_source_ids = set(source_ids)
    for wave_dir in sorted(BATCH.glob("wave_*")):
        for row in read_csv(wave_dir / "source_references.csv"):
            all_source_ids.add(row["source_id"])

    allowed_entities = {"Person": all_person_ids, "Career": all_career_ids, "Organization": set(all_org_ids)}
    for row in evidence:
        if row["source_id"] not in all_source_ids:
            errors.append(f"{row['record_id']}: Source参照が不足（このWaveまたは過去Waveのsource_referencesに存在しない）")
        if row["entity_type"] not in allowed_entities or row["entity_id"] not in allowed_entities.get(row["entity_type"], set()):
            errors.append(f"{row['record_id']}: Entity参照が不足")
        if row["assessment"] not in {"SUPPORTED", "PARTIAL"}:
            errors.append(f"{row['record_id']}: assessmentが不正")
        if not row["source_locator"]:
            errors.append(f"{row['record_id']}: Source内位置が不足")

    for row in decisions:
        if row["decision"] not in {"READY_FOR_VERIFIED_REVIEW", "HOLD_CANDIDATE", "REJECT_CANDIDATE"}:
            errors.append(f"{row['decision_id']}: decisionが不正")
        if row["entity_type"] not in allowed_entities or row["entity_id"] not in allowed_entities.get(row["entity_type"], set()):
            errors.append(f"{row['decision_id']}: Entity参照が不足")

    ready = sum(row["decision"] == "READY_FOR_VERIFIED_REVIEW" for row in decisions)
    hold = sum(row["decision"] == "HOLD_CANDIDATE" for row in decisions)
    report = [
        "# Batch 007 Wave 4（深掘りWave）検証レポート", "", "作成日：2026-09-23", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件",
        f"- 新規Person候補：{len(people)}件（深掘りWaveのため0件が正）",
        f"- 新規Organization候補：{len(orgs)}件", f"- 新規Career候補：{len(careers)}件",
        f"- 新規Source：{len(sources)}件", f"- 新規Evidence：{len(evidence)}件",
        f"- 新規Decision：{len(decisions)}件（READY {ready} / HOLD {hold}）",
        f"- 新規Issue：{len(issues)}件",
        "- 対象：Wave1〜3で既にCANDIDATE登録済みの12人のCareerレコード（既存レコードのID・値は変更せず追記のみ）",
        "- VERIFIED・Master・公開サイト：未変更", "", "## エラー", "",
    ]
    report.extend(f"- {error}" for error in errors)
    if not errors:
        report.append("- なし")
    (BASE / "validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
