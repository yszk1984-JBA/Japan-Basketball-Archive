"""CSV read/write/merge helpers shared across batch scripts.

Extracted from the pattern repeated (with small variations) in
apply_approval_sprint_001..004.py, build_batch_*_verified.py, and
validate_master.py. Behaviour is intentionally unchanged from those
scripts: utf-8-sig on read (tolerates a BOM from Excel-edited files),
plain utf-8 with "\n" line endings on write, and merge-by-key with a
hard failure on conflicting duplicate rows rather than silently
picking one side.
"""

from __future__ import annotations

import csv
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file into a list of dicts. Missing file -> empty list.

    Missing-file-as-empty matches how several existing scripts treat
    optional packet files (e.g. a batch with no HOLD rows may not
    ship a held_fields.csv at all); callers that need the file to
    exist should check `path.exists()` themselves first.
    """
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    """Write rows to a CSV file with a fixed header order."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def dedupe_rows(rows: list[dict[str, str]], key: str) -> list[dict[str, str]]:
    """Collapse rows sharing the same key, erroring on conflicting content.

    Two rows with the same key and identical content are fine (the
    same fact reaching a packet twice). Two rows with the same key
    but different content are a data problem, not something to
    resolve by picking one -- this must never happen silently.
    """
    unique: dict[str, dict[str, str]] = {}
    for row in rows:
        identifier = row[key]
        if identifier in unique and unique[identifier] != row:
            raise SystemExit(
                f"conflicting rows for {key}={identifier}: "
                f"{unique[identifier]} != {row}"
            )
        unique[identifier] = row
    return list(unique.values())


def merge_into_csv(
    path: Path, incoming: list[dict[str, str]], headers: list[str], key: str
) -> list[dict[str, str]]:
    """Merge incoming rows into an existing CSV file, keyed by `key`.

    Existing rows are preserved. An incoming row with a key that
    already exists but different content raises -- this is the same
    safety property `dedupe_rows` has, applied against what is
    already on disk (this is how Master corrections must go through
    the same governed path rather than overwriting silently; see
    docs/DATA_POLICY.md).
    """
    existing = read_csv(path)
    merged = {row[key]: row for row in existing}
    for row in incoming:
        identifier = row[key]
        if identifier in merged and merged[identifier] != row:
            raise SystemExit(f"MASTER conflict: {key}={identifier}")
        merged[identifier] = row
    rows = [merged[identifier] for identifier in sorted(merged)]
    write_csv(path, headers, rows)
    return rows

