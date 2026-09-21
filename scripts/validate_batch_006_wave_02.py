#!/usr/bin/env python3
"""Validate Batch 006 Wave 2 candidate structure and cross-batch IDs."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_006" / "wave_02"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    files = {
        "people": BASE / "person_candidates.csv",
        "orgs": BASE / "organization_candidates.csv",
        "careers": BASE / "career_candidates.csv",
        "sources": BASE / "source_references.csv",
        "evidence": BASE / "evidence_records.csv",
        "issues": BASE / "issues.csv",
        "decisions": BASE / "qa_decisions.csv",
    }
    data = {key: read(path) for key, path in files.items()}
    people, orgs, careers = data["people"], data["orgs"], data["careers"]
    sources, evidence = data["sources"], data["evidence"]
    issues, decisions = data["issues"], data["decisions"]
    person_ids = {row["person_id"] for row in people}
    org_ids = {row["organization_id"] for row in orgs}
    career_ids = {row["career_id"] for row in careers}
    source_ids = {row["source_id"] for row in sources}
    errors: list[str] = []

    if len(people) != 4:
        errors.append(f"Person: expected 4, got {len(people)}")

    checks = [
        ("Person", people, "person_id"), ("Organization", orgs, "organization_id"),
        ("Career", careers, "career_id"), ("Source", sources, "source_id"),
        ("Evidence", evidence, "record_id"), ("Issue", issues, "issue_id"),
        ("Decision", decisions, "decision_id"),
    ]
    for label, rows, key in checks:
        if len({row[key] for row in rows}) != len(rows):
            errors.append(f"{label} IDが重複")

    master_people = {row["person_id"]: row["name"] for row in read(ROOT / "data/master/person.csv")}
    master_orgs = {row["organization_id"]: row["name"] for row in read(ROOT / "data/master/organization.csv")}
    master_careers = {row["career_id"] for row in read(ROOT / "data/master/career.csv")}
    for person in people:
        if person["person_id"] in master_people:
            errors.append(f"{person['person_id']}: Master Person IDと重複")
        if person["name"] in master_people.values():
            errors.append(f"{person['name']}: Master Person氏名と重複")
    for org in orgs:
        existing = master_orgs.get(org["organization_id"])
        if existing is not None and existing != org["name"]:
            errors.append(f"{org['organization_id']}: Master Organization名と不一致")
    if career_ids & master_careers:
        errors.append("Career IDがMasterと重複")

    current_people = files["people"].resolve()
    for path in (ROOT / "data/candidate").rglob("person_candidates.csv"):
        if path.resolve() == current_people:
            continue
        for other in read(path):
            for person in people:
                if other["name"] == person["name"] and other["person_id"] != person["person_id"]:
                    errors.append(f"{person['name']}: 既存候補{other['person_id']}とIDが不一致")
                if other["person_id"] == person["person_id"] and other["name"] != person["name"]:
                    errors.append(f"{person['person_id']}: 既存候補と氏名が不一致")

    current_careers = files["careers"].resolve()
    for path in (ROOT / "data/candidate").rglob("career_candidates.csv"):
        if path.resolve() == current_careers:
            continue
        other_ids = {row["career_id"] for row in read(path)}
        if career_ids & other_ids:
            errors.append(f"Career IDが既存候補と重複: {path.relative_to(ROOT)}")

    for row in careers:
        if row["person_id"] not in person_ids:
            errors.append(f"{row['career_id']}: Person参照が不足")
        if row["organization_id"] not in org_ids:
            errors.append(f"{row['career_id']}: Organization参照が不足")
    for row in evidence:
        if row["source_id"] not in source_ids:
            errors.append(f"{row['record_id']}: Source参照が不足")
        allowed = {"Person": person_ids, "Career": career_ids, "Organization": org_ids}
        if row["entity_type"] not in allowed or row["entity_id"] not in allowed.get(row["entity_type"], set()):
            errors.append(f"{row['record_id']}: Entity参照が不足")
        if row["assessment"] not in {"SUPPORTED", "PARTIAL"}:
            errors.append(f"{row['record_id']}: assessmentが不正")
        if not row["source_locator"]:
            errors.append(f"{row['record_id']}: Source内位置が不足")
    for row in issues:
        if row["person_id"] not in person_ids:
            errors.append(f"{row['issue_id']}: Person参照が不足")
        if row["status"] != "HOLD":
            errors.append(f"{row['issue_id']}: statusが不正")
    for row in decisions:
        if row["decision"] not in {"READY_FOR_VERIFIED_REVIEW", "HOLD_CANDIDATE", "REJECT_CANDIDATE"}:
            errors.append(f"{row['decision_id']}: decisionが不正")

    ready = sum(row["decision"] == "READY_FOR_VERIFIED_REVIEW" for row in decisions)
    hold = sum(row["decision"] == "HOLD_CANDIDATE" for row in decisions)
    report = [
        "# Batch 006 Wave 2 検証レポート", "", "作成日：2026-09-22", "",
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
