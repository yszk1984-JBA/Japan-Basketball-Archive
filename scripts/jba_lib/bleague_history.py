"""Resolve B.LEAGUE 「クラブ所属履歴」 rows to Organizations.

Extracted from scripts/build_batch_031_deepening.py so later batches
(roster-based expansion, batch_032 onwards) apply exactly the same rules:

- The player page lists only club abbreviations per season. The official
  standings pages (/standings/?year=Y&tab=N) give abbreviation -> TeamID
  for each season, and the abbreviations file gives the full club name.
- Clubs renamed under the same TeamID are ONE Organization (Yuichi,
  2026-09-29). Two clubs that were already registered separately keep
  using the Organization whose name matches the season (SPLIT_TEAMS).
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "research"
STANDINGS_FILE = RAW / "bleague_standings_clubs_by_season_2026-09-29.csv"
ABBR_FILE = RAW / "bleague_club_abbreviations_2026-09-29.tsv"

SPLIT_TEAMS = {
    # TeamID: [(last_season_start_inclusive, org_id), ...]
    "748": [(2019, "ORG000102"), (9999, "ORG000174")],
    "2728": [(2025, "ORG000163"), (9999, "ORG000050")],
}
FIXED_TEAMS = {
    "722": "ORG000224", "752": "ORG000225", "1363": "ORG000226",
    "1637": "ORG000227", "746": "ORG000228", "1639": "ORG000222",
}


def read(path: Path, **kw) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as h:
        lines = [line for line in h if not line.startswith("#")]
    return list(csv.DictReader(lines, **kw))


def season_label(y: int) -> str:
    return f"{y}-{str(y + 1)[2:]}"


def all_organizations(exclude: tuple[str, ...] = ()) -> dict[str, str]:
    orgs = {r["organization_id"]: r["name"] for r in read(ROOT / "data/master/organization.csv")}
    for path in sorted((ROOT / "data" / "candidate").rglob("organization_candidates.csv")):
        if any(part in path.parts for part in exclude):
            continue
        for r in read(path):
            orgs.setdefault(r["organization_id"], r["name"])
    return orgs


class Resolver:
    def __init__(self, orgs: dict[str, str], extra_teams: dict[str, str] | None = None):
        self.orgs = orgs
        self.standings = read(STANDINGS_FILE)
        self.by_season_abbr = {(int(r["season_start_year"]), r["abbr"]): r for r in self.standings}
        self.abbr_names = read(ABBR_FILE, delimiter="\t")
        self.team_names = defaultdict(set)
        for r in self.abbr_names:
            self.team_names[r["team_id"]].add(r["full_name_on_standings"])
        self.name_to_org = defaultdict(set)
        for oid, name in orgs.items():
            self.name_to_org[name.replace(" ", "")].add(oid)
        self.fixed = {**FIXED_TEAMS, **(extra_teams or {})}

    def full_name(self, season: int, abbr: str, tid: str) -> str:
        for r in self.abbr_names:
            lo, hi = map(int, r["seasons"].split("-"))
            if r["abbr"] == abbr and r["team_id"] == tid and lo <= season <= hi:
                return r["full_name_on_standings"]
        return ""

    def team_id(self, season: int, abbr: str):
        row = self.by_season_abbr.get((season, abbr))
        if row:
            return row["team_id"], row["tab"]
        # The player page sometimes uses today's abbreviation for an old
        # season (e.g. 横浜BC for 2020-21 when the standings said 横浜).
        cands = {r["team_id"] for r in self.standings if r["abbr"] == abbr}
        if len(cands) != 1:
            return None
        tid = cands.pop()
        match = [r for r in self.standings if r["team_id"] == tid and int(r["season_start_year"]) == season]
        if not match:
            return None
        return tid, match[0]["tab"]

    def resolve(self, season: int, abbr: str):
        found_tid = self.team_id(season, abbr)
        if not found_tid:
            return None
        tid, tab = found_tid
        std_abbr = [r["abbr"] for r in self.standings if r["team_id"] == tid and int(r["season_start_year"]) == season][0]
        if tid in SPLIT_TEAMS:
            org = next(o for last, o in SPLIT_TEAMS[tid] if season <= last)
        elif tid in self.fixed:
            org = self.fixed[tid]
        else:
            found = set()
            for n in self.team_names[tid]:
                found |= self.name_to_org.get(n.replace(" ", ""), set())
            if len(found) != 1:
                return {"tid": tid, "tab": tab, "std_season": season, "std_abbr": std_abbr,
                        "season_name": self.full_name(season, std_abbr, tid), "org": None}
            org = found.pop()
        return {"tid": tid, "tab": tab, "std_season": season, "std_abbr": std_abbr,
                "season_name": self.full_name(season, std_abbr, tid), "org": org}


def parse_history(text: str) -> list[tuple[int, str]]:
    rows = []
    for item in filter(None, text.split(";")):
        season, abbr = item.split(" ", 1)
        rows.append((int(season[:4]), abbr))
    return rows


def stints(resolved: list[tuple]) -> list[tuple[str, list[tuple]]]:
    """Group (year, abbr, r) rows into continuous stays per Organization."""
    by_org = defaultdict(list)
    for item in resolved:
        by_org[item[2]["org"]].append(item)
    out = []
    for org, items in by_org.items():
        items.sort(key=lambda x: x[0])
        cur = [items[0]]
        for it in items[1:]:
            if it[0] == cur[-1][0] + 1:
                cur.append(it)
            elif it[0] == cur[-1][0]:
                continue
            else:
                out.append((org, cur))
                cur = [it]
        out.append((org, cur))
    out.sort(key=lambda s: (s[1][0][0], s[1][-1][0]))
    return out
