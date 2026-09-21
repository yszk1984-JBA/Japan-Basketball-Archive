#!/usr/bin/env python3
"""Build and validate same-period organization relationship candidates."""

from __future__ import annotations

import csv
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "relationship_pilot_001"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    memberships = read(BASE / "roster_membership_candidates.csv")
    sources = read(BASE / "source_references.csv")
    people = {row["person_id"]: row["name"] for row in read(ROOT / "data" / "master" / "person.csv")}
    organizations = {row["organization_id"]: row["name"] for row in read(ROOT / "data" / "master" / "organization.csv")}
    source_ids = {row["source_id"] for row in sources}
    errors: list[str] = []

    if len(memberships) != 6:
        errors.append(f"Membership: expected 6, got {len(memberships)}")
    if len({row["membership_id"] for row in memberships}) != len(memberships):
        errors.append("Membership IDが重複")
    if len({row["person_id"] for row in memberships}) != len(memberships):
        errors.append("Person IDが重複")

    for row in memberships:
        if people.get(row["person_id"]) != row["name"]:
            errors.append(f"{row['membership_id']}: Master Personと不一致")
        if organizations.get(row["organization_id"]) != "福岡第一高等学校":
            errors.append(f"{row['membership_id']}: 福岡第一高校のOrganizationではない")
        if row["source_id"] not in source_ids:
            errors.append(f"{row['membership_id']}: Source参照が不足")
        if row["assessment"] != "CANDIDATE":
            errors.append(f"{row['membership_id']}: CANDIDATEではない")

    relationships: list[dict[str, str]] = []
    for index, (left, right) in enumerate(combinations(memberships, 2), start=1):
        if left["organization_id"] != right["organization_id"]:
            errors.append(f"Pair {index}: Organizationが不一致")
        if left["period_label"] != right["period_label"]:
            errors.append(f"Pair {index}: 期間ラベルが不一致")
        if left["source_id"] != right["source_id"]:
            errors.append(f"Pair {index}: Sourceが不一致")
        relationships.append({
            "relationship_candidate_id": f"TRC{index:04d}",
            "person_id_a": left["person_id"],
            "name_a": left["name"],
            "person_id_b": right["person_id"],
            "name_b": right["name"],
            "organization_id": left["organization_id"],
            "period_label": left["period_label"],
            "relationship_type": "same_organization_same_roster_period",
            "membership_id_a": left["membership_id"],
            "membership_id_b": right["membership_id"],
            "source_id": left["source_id"],
            "assessment": "CANDIDATE",
        })

    if len(relationships) != 15:
        errors.append(f"Relationship: expected 15, got {len(relationships)}")

    write(
        BASE / "relationship_candidates.csv",
        [
            "relationship_candidate_id", "person_id_a", "name_a", "person_id_b", "name_b",
            "organization_id", "period_label", "relationship_type", "membership_id_a",
            "membership_id_b", "source_id", "assessment",
        ],
        relationships,
    )

    report = [
        "# Relationship Pilot 001 検証レポート", "", "作成日：2026-09-21", "",
        "## 結果", "", f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件", f"- Roster Membership候補：{len(memberships)}件",
        f"- 同時所属関係候補：{len(relationships)}件", f"- Source：{len(sources)}件",
        "- Master・公開サイト：未変更", "", "## エラー", "",
    ]
    report.extend(f"- {error}" for error in errors)
    if not errors:
        report.append("- なし")
    (BASE / "validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
