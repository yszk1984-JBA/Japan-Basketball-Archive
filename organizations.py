"""Organization identity helpers.

Root cause of the ORG000017/ORG000019 duplicate (both "日本経済大学",
discovered 2026-09-23): each batch script picked the "next"
organization_id and wrote a fresh Organization row after eyeballing
the existing CSV, with no shared check for "does this exact name
already have an ID?". Batch 004's own QA flagged the collision
(see data/candidate/batch_004/review_packet/held_issues.csv,
issue B4W1I0008) but nothing enforced the check going forward, so it
was never wired into a script.

This module does exactly one new thing: before a script mints a new
Organization row, check whether the exact name already has an ID
anywhere in the supplied organization tables, and refuse to mint a
duplicate silently. It does NOT do fuzzy/alias matching automatically
-- per docs/DATA_POLICY.md and AGENTS.md, school-name variants
(福岡第一 / 福岡第一高校 / 福岡第一高等学校 / Fukuoka Daiichi ...) must
not be auto-merged. `find_possible_variants` only *surfaces* close
matches (whitespace/full-width differences) for a human to decide;
it never merges anything by itself.
"""

from __future__ import annotations

import unicodedata
from collections import defaultdict
from pathlib import Path

from .csv_io import read_csv


def load_organizations(*paths: Path) -> dict[str, str]:
    """Load organization_id -> name from one or more CSV files.

    Pass every table that is in scope for the duplicate check: at
    minimum data/master/organization.csv, plus any in-flight
    candidate/verified organization file the new batch will also
    touch. A name that already exists in ANY of these should not get
    a second ID.
    """
    organizations: dict[str, str] = {}
    for path in paths:
        for row in read_csv(path):
            organizations[row["organization_id"]] = row["name"]
    return organizations


def find_organization_id_by_exact_name(name: str, organizations: dict[str, str]) -> str | None:
    """Return the existing organization_id for an exact name match, if any."""
    for organization_id, existing_name in organizations.items():
        if existing_name == name:
            return organization_id
    return None


def find_duplicate_names(organizations: dict[str, str]) -> dict[str, list[str]]:
    """Return {name: [id, id, ...]} for every name that has more than one ID.

    This is the check that would have caught ORG000017/ORG000019 at
    validation time instead of silently passing. Call this from
    validate_master.py and from any new batch's own validation step.
    """
    by_name: dict[str, list[str]] = defaultdict(list)
    for organization_id, name in organizations.items():
        by_name[name].append(organization_id)
    return {name: ids for name, ids in by_name.items() if len(ids) > 1}


def _normalize_for_comparison(name: str) -> str:
    # NFKC folds full-width/half-width variants and compatibility
    # characters; this is comparison-only and never written back.
    return unicodedata.normalize("NFKC", name).strip()


def find_possible_variants(organizations: dict[str, str]) -> dict[str, list[str]]:
    """Surface names that are identical after light normalization but not
    byte-for-byte identical (whitespace, full/half-width, etc).

    Returns {normalized_form: [distinct original names]} for groups
    with more than one distinct original spelling. This is a hint for
    a human to review (docs/DATA_POLICY.md: 表記揺れの発見は良いが、
    自動統合はしない) -- it is deliberately narrower than fuzzy
    name matching, which risks flagging genuinely different schools
    (e.g. 東海大学 vs 東海大学九州) as the same.
    """
    by_normalized: dict[str, set[str]] = defaultdict(set)
    for name in organizations.values():
        by_normalized[_normalize_for_comparison(name)].add(name)
    return {
        normalized: sorted(names)
        for normalized, names in by_normalized.items()
        if len(names) > 1
    }
