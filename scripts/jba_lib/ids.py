"""Sequential ID allocation for Person / Organization / Career (P000010,
ORG000010, C000010 style: a letter prefix + zero-padded digits).

Source IDs are namespaced per batch/wave already (B2S0001, B4W1S0001,
...) and do not need this -- collisions there are avoided by
construction. Person/Organization/Career IDs are global and
sequential, and until now each batch script picked the "next" one by
reading one CSV and incrementing by eye. This module makes "next ID"
a single function that looks across every table the caller passes in,
so a new batch can't silently reuse or skip an ID that a different
in-flight batch also claimed.

This does not fix the ORG000017/ORG000019 case (that was two
*different*, both-valid IDs for the same name, not a collision) --
see jba_lib/organizations.py for that check. This module is about
never handing out the same ID twice.
"""

from __future__ import annotations

import re
from pathlib import Path

from .csv_io import read_csv

_ID_PATTERN = re.compile(r"^([A-Z]+)0*([0-9]+)$")


def next_sequential_id(prefix: str, digits: int, *id_iterables: list[str]) -> str:
    """Return the next unused ID for `prefix`, given one or more lists of
    existing IDs (e.g. from several CSVs that must not collide).

    Example: next_sequential_id("ORG", 6, master_org_ids, candidate_org_ids)
    -> "ORG000112" if the highest existing ORG id across both lists is
    ORG000111.
    """
    highest = 0
    for ids in id_iterables:
        for identifier in ids:
            match = _ID_PATTERN.match(identifier)
            if match and match.group(1) == prefix:
                highest = max(highest, int(match.group(2)))
    return f"{prefix}{highest + 1:0{digits}d}"


def ids_from_csv(path: Path, id_field: str) -> list[str]:
    """Convenience: pull one ID column out of a CSV file as a list."""
    return [row[id_field] for row in read_csv(path) if row.get(id_field)]

