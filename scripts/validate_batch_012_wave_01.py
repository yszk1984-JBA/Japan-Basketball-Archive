#!/usr/bin/env python3
"""Validate Batch 012 Wave 1 candidate structure.

Built on jba_lib instead of re-copying the read/write/duplicate-name
boilerplate that scripts/validate_batch_002..006_*.py each carried
separately -- this is the first validator written after the 2026-09-23
tooling refactor.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv  # noqa: E402
from jba_lib.organizations import find_duplicate_names  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_012" / "wave_01"
EXPECTED_PERSON_COUNT = 1


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
        errors.append(f"Person: expected {EXPECTED_PERSON_COUNT}, got {len(people)}")

    master_people = {row["person_id"]: row["name"] for row in read_csv(ROOT / "data" / "master" / "person.csv")}
    person_ids = {row["person_id"] for row in people}
    if person_ids & master_people.keys():
        errors.append("新規Person IDがMasterと重複")
    current_file = (BASE / "person_candidates.csv").resolve()
    for path in (ROOT / "data" / "candidate").rglob("person_candidates.csv"):
        if path.resolve() == current_file:
            continue
        for other in read_csv(path):
            for person in people:
                if other["name"] == person["name"] and other["person_id"] != person["person_id"]:
                    errors.append(f"{person['name']}: 既存候補{other['person_id']}とIDが不一致")
                if other["person_id"] == person["person_id"] and other["name"] != person["name"]:
                    errors.append(f"{person['person_id']}: 既存候補と氏名が不一致")

    all_orgs: dict[str, str] = {row["organization_id"]: row["name"] for row in read_csv(ROOT / "data" / "master" / "organization.csv")}
    for path in (ROOT / "data" / "candidate").rglob("organization_candidates.csv"):
        for row in read_csv(path):
            all_orgs.setdefault(row["organization_id"], row["name"])
    for row in orgs:
        existing_name = all_orgs.get(row["organization_id"])
        if existing_name is not None and existing_name != row["name"]:
            errors.append(f"{row['organization_id']}: 既存では{existing_name!r}だが本Waveでは{row['name']!r}")
        all_orgs[row["organization_id"]] = row["name"]
    for name, ids in find_duplicate_names(all_orgs).items():
        if any(row["organization_id"] in ids for row in orgs):
            errors.append(f"Organization名重複の可能性: {name!r} が {ids} に存在")

    for label, rows, key in [
        ("Person", people, "person_id"), ("Organization", orgs, "organization_id"),
        ("Career", careers, "career_id"), ("Source", sources, "source_id"),
        ("Evidence", evidence, "record_id"), ("Issue", issues, "issue_id"),
        ("Decision", decisions, "decision_id"),
    ]:
        if len({row[key] for row in rows}) != len(rows):
            errors.append(f"{label} IDが重複")

    org_ids = {row["organization_id"] for row in orgs}
    career_ids = {row["career_id"] for row in careers}
    source_ids = {row["source_id"] for row in sources}
    for row in careers:
        if row["person_id"] not in person_ids:
            errors.append(f"{row['career_id']}: Person参照が不足")
        if row["organization_id"] not in org_ids:
            errors.append(f"{row['career_id']}: Organization参照が不足")

    allowed_entities = {"Person": person_ids, "Career": career_ids, "Organization": org_ids}
    for row in evidence:
        if row["source_id"] not in source_ids:
            errors.append(f"{row['record_id']}: Source参照が不足")
        if row["entity_type"] not in allowed_entities or row["entity_id"] not in allowed_entities.get(row["entity_type"], set()):
            errors.append(f"{row['record_id']}: Entity参照が不足")
        if row["assessment"] not in {"SUPPORTED", "PARTIAL"}:
            errors.append(f"{row['record_id']}: assessmentが不正")
        if not row["source_locator"]:
            errors.append(f"{row['record_id']}: Source内位置が不足")

    for row in decisions:
        if row["decision"] not in {"READY_FOR_VERIFIED_REVIEW", "HOLD_CANDIDATE", "REJECT_CANDIDATE"}:
            errors.append(f"{row['decision_id']}: decisionが不正")

    ready = sum(row["decision"] == "READY_FOR_VERIFIED_REVIEW" for row in decisions)
    hold = sum(row["decision"] == "HOLD_CANDIDATE" for row in decisions)
    report = [
        "# Batch 012 Wave 1 検証レポート", "", "作成日：2026-09-24", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件", f"- Person候補：{len(people)}件",
        f"- Career候補：{len(careers)}件", f"- Source：{len(sources)}件",
        f"- Evidence：{len(evidence)}件", f"- READY判断：{ready}件",
        f"- HOLD判断：{hold}件", f"- Issue：{len(issues)}件",
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

