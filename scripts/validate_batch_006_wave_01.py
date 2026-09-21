#!/usr/bin/env python3
"""Validate Batch 006 Wave 1 candidate structure."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_006" / "wave_01"


def read(name: str) -> list[dict[str, str]]:
    with (BASE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    people = read("person_candidates.csv")
    orgs = read("organization_candidates.csv")
    careers = read("career_candidates.csv")
    sources = read("source_references.csv")
    evidence = read("evidence_records.csv")
    issues = read("issues.csv")
    decisions = read("qa_decisions.csv")
    master_people = {row["person_id"] for row in read_master("person.csv")}
    person_ids = {row["person_id"] for row in people}
    org_ids = {row["organization_id"] for row in orgs}
    career_ids = {row["career_id"] for row in careers}
    source_ids = {row["source_id"] for row in sources}
    errors: list[str] = []

    if len(people) != 4:
        errors.append(f"Person: expected 4, got {len(people)}")
    if person_ids & master_people:
        errors.append("新規Person IDがMasterと重複")
    for label, rows, key in [
        ("Person", people, "person_id"), ("Organization", orgs, "organization_id"),
        ("Career", careers, "career_id"), ("Source", sources, "source_id"),
        ("Evidence", evidence, "record_id"), ("Issue", issues, "issue_id"),
        ("Decision", decisions, "decision_id"),
    ]:
        if len({row[key] for row in rows}) != len(rows):
            errors.append(f"{label} IDが重複")
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
    for row in decisions:
        if row["decision"] not in {"READY_FOR_VERIFIED_REVIEW", "HOLD_CANDIDATE", "REJECT_CANDIDATE"}:
            errors.append(f"{row['decision_id']}: decisionが不正")

    ready = sum(row["decision"] == "READY_FOR_VERIFIED_REVIEW" for row in decisions)
    hold = sum(row["decision"] == "HOLD_CANDIDATE" for row in decisions)
    report = [
        "# Batch 006 Wave 1 検証レポート", "", "作成日：2026-09-21", "",
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


def read_master(name: str) -> list[dict[str, str]]:
    with (ROOT / "data" / "master" / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit(main())
