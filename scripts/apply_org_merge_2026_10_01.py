#!/usr/bin/env python3
"""Merge duplicate Organizations in MASTER (Yuichi, 2026-10-01).

Yuichi's instruction (verbatim, recorded in
data/master/corrections/2026-10-01_org_merge_hakuoh_tomita.md):
  白鷗大学と白鴎大学をまとめる
  「富田高校」と「私立富田高校」が同じ学校とする

Same procedure as the 2026-09-23 ORG000017 -> ORG000019 merge: the earlier
registered ID is kept, Careers and the organization_id Evidence values are
re-pointed, and the retired row is removed. Source text (source_locator,
e.g. 「出身校（大）：白鴎大学」) is left exactly as the source printed it.
data/candidate and data/verified snapshots are not changed.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data/master"
MERGES = {  # retired -> kept
    "ORG000208": "ORG000093",  # 白鴎大学 -> 白鷗大学
    "ORG000436": "ORG000266",  # 富田高等学校 -> 私立富田高等学校
}
EXPECTED_NAMES = {"ORG000208": "白鴎大学", "ORG000093": "白鷗大学", "ORG000436": "富田高等学校", "ORG000266": "私立富田高等学校"}


def read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as h:
        r = csv.DictReader(h)
        return list(r.fieldnames or []), list(r)


def write(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=headers, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    oh, orgs = read(MASTER / "organization.csv")
    names = {o["organization_id"]: o["name"] for o in orgs}
    for oid, name in EXPECTED_NAMES.items():
        if names.get(oid) != name:
            raise SystemExit(f"{oid}: expected {name!r}, found {names.get(oid)!r} (already merged?)")

    ch, careers = read(MASTER / "career.csv")
    moved = []
    for c in careers:
        if c["organization_id"] in MERGES:
            moved.append((c["career_id"], c["person_id"], c["organization_id"]))
            c["organization_id"] = MERGES[c["organization_id"]]
    kept = set(MERGES.values())
    dup = [k for k, v in Counter((c["person_id"], c["organization_id"], c["start"], c["end"]) for c in careers
                                 if c["organization_id"] in kept).items() if v > 1]
    if dup:
        raise SystemExit(f"merge would create duplicate Careers: {dup}")
    write(MASTER / "career.csv", ch, careers)

    eh, evidence = read(MASTER / "evidence.csv")
    ev_changed = 0
    for e in evidence:
        if e["field_name"] == "organization_id" and e["candidate_value"] in MERGES:
            e["candidate_value"] = MERGES[e["candidate_value"]]
            ev_changed += 1
        if e["entity_type"] == "Organization" and e["entity_id"] in MERGES:
            e["entity_id"] = MERGES[e["entity_id"]]
            ev_changed += 1
    write(MASTER / "evidence.csv", eh, evidence)

    write(MASTER / "organization.csv", oh, [o for o in orgs if o["organization_id"] not in MERGES])
    for cid, pid, old in moved:
        print(f"{cid} {pid}: {old} -> {MERGES[old]}")
    print(f"careers re-pointed: {len(moved)}, evidence rows changed: {ev_changed}, organizations removed: {len(MERGES)}")


if __name__ == "__main__":
    main()
