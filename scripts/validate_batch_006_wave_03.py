#!/usr/bin/env python3
"""Validate Batch 006 Wave 3 (深掘りWave/Enrichment Wave) candidate structure.

Target: 長島エマニエル (P000078, already MASTER) -- pre-2016 career history
(飛龍高等学校, 白鷗大学, 横浜ビー・コルセアーズ, バンビシャス奈良).

Like batch_004's enrichment waves, this adds no new Person and its
evidence/decisions may reference Career/Organization entities defined in
an EARLIER wave of this same batch, or in MASTER. Organization references
are additionally checked against the GLOBAL union of all batches' candidate
orgs, since this wave references ORG000093 (白鷗大学), which is registered
as a CANDIDATE in batch_004/wave_02 and not yet promoted to Master.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "data" / "candidate" / "batch_006"
BASE = BATCH / "wave_03"
EXPECTED_PERSON_COUNT = 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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

    all_person_ids: set[str] = set()
    all_org_ids: dict[str, str] = {row["organization_id"]: row["name"] for row in read_csv(ROOT / "data" / "master" / "organization.csv")}
    all_career_ids: set[str] = set()
    for wave_dir in sorted(BATCH.glob("wave_*")):
        for row in read_csv(wave_dir / "person_candidates.csv"):
            all_person_ids.add(row["person_id"])
        for row in read_csv(wave_dir / "career_candidates.csv"):
            all_career_ids.add(row["career_id"])
    all_person_ids |= {row["person_id"] for row in read_csv(ROOT / "data" / "master" / "person.csv")}
    all_career_ids |= {row["career_id"] for row in read_csv(ROOT / "data" / "master" / "career.csv")}
    # Cross-batch org lookup: this wave references ORG000093 (白鷗大学), a
    # CANDIDATE registered in batch_004/wave_02, not yet promoted to Master.
    for path in (ROOT / "data" / "candidate").rglob("organization_candidates.csv"):
        for row in read_csv(path):
            all_org_ids.setdefault(row["organization_id"], row["name"])

    for row in orgs:
        existing_name = all_org_ids.get(row["organization_id"])
        if existing_name is not None and existing_name != row["name"]:
            errors.append(f"{row['organization_id']}: 既存では{existing_name!r}だが本Waveでは{row['name']!r}")
        all_org_ids[row["organization_id"]] = row["name"]

    for label, rows, key in [
        ("Organization", orgs, "organization_id"), ("Career", careers, "career_id"),
        ("Source", sources, "source_id"), ("Evidence", evidence, "record_id"),
        ("Issue", issues, "issue_id"), ("Decision", decisions, "decision_id"),
    ]:
        if len({row[key] for row in rows}) != len(rows):
            errors.append(f"{label} IDが重複")

    for row in careers:
        if row["person_id"] not in all_person_ids:
            errors.append(f"{row['career_id']}: Person参照が不足")
        if row["organization_id"] not in all_org_ids and row["organization_id"] not in {o['organization_id'] for o in orgs}:
            errors.append(f"{row['career_id']}: Organization参照が不足")
        all_career_ids.add(row["career_id"])

    source_ids = {row["source_id"] for row in sources}
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

    for row in issues:
        if row["status"] not in {"HOLD", "RESOLVED", "OPEN"}:
            errors.append(f"{row['issue_id']}: statusが不正")

    ready = sum(row["decision"] == "READY_FOR_VERIFIED_REVIEW" for row in decisions)
    hold = sum(row["decision"] == "HOLD_CANDIDATE" for row in decisions)
    report = [
        "# Batch 006 Wave 3（深掘りWave）検証レポート", "", "作成日：2026-09-23", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件",
        f"- 新規Person候補：{len(people)}件（深掘りWaveのため0件が正）",
        f"- 新規Organization候補：{len(orgs)}件", f"- 新規Career候補：{len(careers)}件",
        f"- 新規Source：{len(sources)}件", f"- 新規Evidence：{len(evidence)}件",
        f"- 新規Decision：{len(decisions)}件（READY {ready} / HOLD {hold}）",
        f"- 新規Issue：{len(issues)}件",
        "- 対象：長島エマニエル（P000078、既にMaster登録済み）の2016年以前の経歴（飛龍高等学校・白鷗大学・横浜ビー・コルセアーズ・バンビシャス奈良）",
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
