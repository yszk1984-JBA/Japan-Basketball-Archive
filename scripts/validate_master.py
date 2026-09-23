#!/usr/bin/env python3
"""Validate MASTER internal consistency.

Rewritten 2026-09-23 to stop hardcoding expected row counts and
per-approval field values in this file. The old version asserted
things like `("Person", (len(persons), 34))` and a dict of exact
field values for every approval_id -- meaning this script had to be
hand-edited every time a new batch reached MASTER, and it silently
drifted out of sync with reality otherwise (that rigidity is exactly
why the ORG000017/ORG000019 duplicate organization name went
undetected: this file checked reference integrity but never checked
for two IDs sharing one name).

What this file now checks (all derived from the CSVs themselves, not
from numbers typed into this script):

- ID uniqueness within each table (Person/Organization/Career/Source).
- Referential integrity (Career -> Person/Organization, Evidence ->
  Source/entity).
- Evidence rows are all SUPPORTED (HOLD items must never reach MASTER).
- Organization names are unique -- an exact duplicate name under two
  IDs is always an error here, never a silent pass.
- Approval and Publication records have their required fields filled
  in, approval_id/publication_id are unique, and every approval is
  attributed to Yuichi (AI must never appear as approver; see
  AGENTS.md).

What this file deliberately does NOT check: whether a specific
approval_id's recorded scope still matches the packet it came from
byte-for-byte. That immutability check belongs to the
apply_approval_sprint_*.py script that applied it (each one pins a
git commit and diffs the packet against it at apply time) -- doing it
again here with hardcoded values doesn't scale and isn't what "is
MASTER internally consistent right now" means.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv  # noqa: E402
from jba_lib.organizations import find_duplicate_names  # noqa: E402

BASE = Path(__file__).resolve().parents[1] / "data" / "master"


def check_unique_ids(rows: list[dict[str, str]], id_field: str, label: str, errors: list[str]) -> None:
    seen: dict[str, int] = {}
    for row in rows:
        seen[row[id_field]] = seen.get(row[id_field], 0) + 1
    for identifier, count in seen.items():
        if count > 1:
            errors.append(f"{label}: {id_field}={identifier} appears {count} times")


def main() -> int:
    errors: list[str] = []

    persons = read_csv(BASE / "person.csv")
    organizations = read_csv(BASE / "organization.csv")
    careers = read_csv(BASE / "career.csv")
    sources = read_csv(BASE / "source.csv")
    evidence = read_csv(BASE / "evidence.csv")
    approvals = read_csv(BASE / "approval_records.csv")
    publications = read_csv(BASE / "publication_records.csv")

    check_unique_ids(persons, "person_id", "Person", errors)
    check_unique_ids(organizations, "organization_id", "Organization", errors)
    check_unique_ids(careers, "career_id", "Career", errors)
    check_unique_ids(sources, "source_id", "Source", errors)
    check_unique_ids(evidence, "record_id", "Evidence", errors)
    check_unique_ids(approvals, "approval_id", "Approval", errors)
    check_unique_ids(publications, "publication_id", "Publication", errors)

    # Organization name duplicates: this is the check that would have
    # caught ORG000017/ORG000019 ("日本経済大学" x2) before it reached
    # MASTER. A duplicate name is always an error -- variants that are
    # merely *similar* are a separate, human judgment call and are not
    # flagged here (see jba_lib.organizations.find_possible_variants
    # for that, used as an advisory check in new-batch scripts instead).
    organization_names = {row["organization_id"]: row["name"] for row in organizations}
    for name, ids in find_duplicate_names(organization_names).items():
        errors.append(f"Organization name duplicated across IDs {ids}: {name!r}")

    person_ids = {row["person_id"] for row in persons}
    organization_ids = {row["organization_id"] for row in organizations}
    career_ids = {row["career_id"] for row in careers}
    source_ids = {row["source_id"] for row in sources}

    for row in careers:
        if row["person_id"] not in person_ids:
            errors.append(f"{row['career_id']}: unknown person")
        if not row["organization_id"] or row["organization_id"] not in organization_ids:
            errors.append(f"{row['career_id']}: missing or unknown organization")

    entity_ids = {
        "Person": person_ids,
        "Organization": organization_ids,
        "Career": career_ids,
    }
    for row in evidence:
        if row["assessment"] != "SUPPORTED":
            errors.append(f"{row['record_id']}: assessment is not SUPPORTED")
        if row["source_id"] not in source_ids:
            errors.append(f"{row['record_id']}: unknown source")
        if row["entity_id"] not in entity_ids.get(row["entity_type"], set()):
            errors.append(f"{row['record_id']}: unknown entity")

    approval_required_fields = ["approval_id", "approved_by", "approved_at", "approval_reference"]
    approval_ids = {row["approval_id"] for row in approvals}
    for row in approvals:
        for field in approval_required_fields:
            if not row.get(field):
                errors.append(f"{row['approval_id']}: missing {field}")
        if row.get("approved_by") and row["approved_by"] != "Yuichi":
            errors.append(
                f"{row['approval_id']}: approved_by is {row['approved_by']!r}, must be Yuichi "
                "(AI must never record itself as the approver; see AGENTS.md)"
            )

    publication_required_fields = ["publication_id", "approval_id", "published_at", "site_url", "status"]
    for row in publications:
        for field in publication_required_fields:
            if not row.get(field):
                errors.append(f"{row['publication_id']}: missing {field}")
        if row.get("approval_id") and row["approval_id"] not in approval_ids:
            errors.append(f"{row['publication_id']}: refers to unknown approval {row['approval_id']}")

    report = [
        "# MASTER検証レポート", "", "作成日：2026-09-23（validate_master.py汎用化後）", "",
        "## 結果", "",
        f"- 検証：{'PASS' if not errors else 'FAIL'}",
        f"- エラー：{len(errors)}件",
        f"- Person：{len(persons)}件",
        f"- Organization：{len(organizations)}件",
        f"- Career：{len(careers)}件",
        f"- Source：{len(sources)}件",
        f"- Evidence：{len(evidence)}件",
        f"- Approval：{len(approvals)}件",
        f"- Publication：{len(publications)}件", "", "## エラー", "",
    ]
    report.extend(f"- {error}" for error in errors)
    if not errors:
        report.append("- なし")
    (BASE / "validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

