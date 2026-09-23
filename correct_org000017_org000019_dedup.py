#!/usr/bin/env python3
"""Master correction: retire ORG000017 (duplicate of ORG000019, both
"日本経済大学"), approved by Yuichi in chat on 2026-09-23.

Background: batch_004's own QA flagged this exact duplicate as HOLD
issue B4W1I0008 ("既存バッチで日本経済大学にORG000017とORG000019が混在
する / Master前に組織IDの正規化方針を決める") but it was never resolved
before Approval Sprints 001-004 carried both IDs into MASTER.
validate_master.py did not check for duplicate Organization names, so
this passed silently (validation_report.md said "エラー：0件").

ORG000019 was registered first (Batch 002, 2026-09-19); ORG000017 was
registered later (Batch 003) without checking for an existing exact
name match. This script keeps ORG000019 as canonical and retires
ORG000017:

- career.csv: repoint every Career whose organization_id is ORG000017
  to ORG000019 (C000030, C000225, C000254).
- evidence.csv: update the corresponding organization_id evidence rows
  to record ORG000019 (not ORG000017) as the value they support, and
  repoint the two Organization/name evidence rows that were about
  ORG000017 onto ORG000019.
- organization.csv: remove the ORG000017 row.

This does not touch data/candidate or data/verified snapshots (those
remain the historical record of what each batch actually produced);
only MASTER is corrected, per docs/DATA_POLICY.md ("既存のMasterも訂正
は候補から同じ経路を通し、変更前後と理由を残す" -- the "同じ経路" here is
an explicit Human Approval from Yuichi, recorded in
data/master/corrections/2026-09-23_org000017_org000019.md, rather than
a fabricated CANDIDATE/VERIFIED cycle for a metadata correction).
"""

from __future__ import annotations

from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402
from jba_lib.organizations import load_organizations, find_duplicate_names  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "master"

RETIRED_ID = "ORG000017"
CANONICAL_ID = "ORG000019"


def main() -> None:
    organizations = load_organizations(MASTER / "organization.csv")
    if organizations.get(RETIRED_ID) != "日本経済大学" or organizations.get(CANONICAL_ID) != "日本経済大学":
        raise SystemExit(
            "Expected ORG000017 and ORG000019 to both be 日本経済大学 before "
            "correcting -- aborting, data has changed since this script was written."
        )

    # --- career.csv ---------------------------------------------------
    career_path = MASTER / "career.csv"
    careers = read_csv(career_path)
    career_headers = ["career_id", "person_id", "organization_id", "role", "start", "end"]
    changed_careers: list[str] = []
    for row in careers:
        if row["organization_id"] == RETIRED_ID:
            row["organization_id"] = CANONICAL_ID
            changed_careers.append(row["career_id"])
    write_csv(career_path, career_headers, careers)

    # --- evidence.csv ---------------------------------------------------
    evidence_path = MASTER / "evidence.csv"
    evidence = read_csv(evidence_path)
    evidence_headers = [
        "record_id", "entity_type", "entity_id", "field_name", "candidate_value",
        "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note",
    ]
    changed_evidence: list[str] = []
    for row in evidence:
        if row["entity_type"] == "Career" and row["field_name"] == "organization_id" and row["candidate_value"] == RETIRED_ID:
            row["candidate_value"] = CANONICAL_ID
            changed_evidence.append(row["record_id"])
        elif row["entity_type"] == "Organization" and row["entity_id"] == RETIRED_ID:
            row["entity_id"] = CANONICAL_ID
            changed_evidence.append(row["record_id"])
    write_csv(evidence_path, evidence_headers, evidence)

    # --- organization.csv ---------------------------------------------------
    organization_path = MASTER / "organization.csv"
    organization_rows = read_csv(organization_path)
    remaining = [row for row in organization_rows if row["organization_id"] != RETIRED_ID]
    if len(remaining) != len(organization_rows) - 1:
        raise SystemExit(f"expected to remove exactly one row for {RETIRED_ID}")
    write_csv(organization_path, ["organization_id", "name"], remaining)

    print(f"Careers repointed ({RETIRED_ID} -> {CANONICAL_ID}): {changed_careers}")
    print(f"Evidence rows updated: {changed_evidence}")
    print(f"Organization row removed: {RETIRED_ID}")

    remaining_orgs = load_organizations(organization_path)
    still_duplicated = find_duplicate_names(remaining_orgs)
    print(f"Remaining duplicate names after fix: {still_duplicated or 'none'}")


if __name__ == "__main__":
    main()
