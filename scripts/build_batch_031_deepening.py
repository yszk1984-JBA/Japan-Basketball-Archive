#!/usr/bin/env python3
"""Build Batch 031: B.LEAGUE-era past-club deepening for existing MASTER persons.

Plan: docs/DEEPENING_BLEAGUE_ERA_PLAN.md (Yuichi, 2026-09-29: 深掘りから).
Targets: docs/DEEPENING_BLEAGUE_ERA_TARGETS.csv (155 MASTER persons with a
B.LEAGUE PlayerID in their MASTER sources).

Inputs (all read in the browser on 2026-09-29 and stored verbatim under
data/raw/research/):
- bleague_club_history_2026-09-29.txt: each player's 「クラブ所属履歴」.
- bleague_standings_clubs_by_season_2026-09-29.csv: (season, division tab,
  abbreviation, TeamID) from the official standings pages.
- bleague_club_abbreviations_2026-09-29.tsv: abbreviation -> full club name
  as printed on the standings pages, with the seasons each spelling was used.

Rules (see the plan):
- One Career per continuous stay at one club; a return is a new Career.
- start = first season's start year, end = last season's end year; a stay
  that includes 2026-27 (current season) gets no end.
- Clubs renamed under the same B.LEAGUE TeamID are ONE Organization
  (Yuichi, 2026-09-29, same as the 栃木→宇都宮ブレックス precedent); the
  season-time name is recorded as an ORG_NAME_HISTORY issue. Two clubs that
  were ALREADY registered as separate Organizations (東京サンレーヴス /
  しながわシティ, 湘南ユナイテッドBC / ウォルガ湘南) keep using the
  Organization whose name matches the season.
- A stay that already exists in MASTER (same Organization, overlapping or
  undated period) is NOT re-added. If MASTER's dates differ from the
  B.LEAGUE-derived ones, that is logged as an issue only -- MASTER values are
  never changed here.

All targets are MASTER persons, so this is one dedicated batch rather than
one deepening wave per original batch (the per-origin rule in
docs/HISTORICAL_CAREER_DEEPENING_LOG.md exists because the site's candidate
build groups by batch; MASTER persons are skipped by that build anyway).
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "research"
OUT = ROOT / "data" / "candidate" / "batch_031"
CHECKED_AT = "2026-09-29"
CURRENT_SEASON = 2026
WAVE_SIZE = 40
FIRST_CAREER = 769
DIVISION = {("1", False): "B1", ("2", False): "B2", ("3", False): "B3"}

# TeamID -> Organization. Most are resolved by exact name match against
# existing Organizations; these are the explicit cases.
NEW_ORGS = {
    "722": ("ORG000224", "香川ファイブアローズ"),
    "752": ("ORG000225", "豊田合成スコーピオンズ"),
    "1363": ("ORG000226", "岐阜スゥープス"),
    "1637": ("ORG000227", "ベルテックス静岡"),
    "746": ("ORG000228", "東京海上日動ビッグブルー"),
}
# ORG000222 was registered (batch_022) as 「トライフォース岡山」 from a
# summary-tool translation; the official name on every source is
# 「トライフープ岡山」 (TeamID 1639). Corrected here, see org_corrections.csv.
ORG_CORRECTIONS = {"ORG000222": ("トライフォース岡山", "トライフープ岡山")}
SPLIT_TEAMS = {
    # TeamID: [(last_season_start_inclusive, org_id), ...]
    "748": [(2019, "ORG000102"), (9999, "ORG000174")],
    "2728": [(2025, "ORG000163"), (9999, "ORG000050")],
}


def read(path: Path, **kw) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as h:
        lines = [line for line in h if not line.startswith("#")]
    return list(csv.DictReader(lines, **kw))


def season_label(y: int) -> str:
    return f"{y}-{str(y + 1)[2:]}"


def load_inputs():
    standings = read(RAW / "bleague_standings_clubs_by_season_2026-09-29.csv")
    by_season_abbr = {(int(r["season_start_year"]), r["abbr"]): r for r in standings}
    abbr_names = read(RAW / "bleague_club_abbreviations_2026-09-29.tsv", delimiter="\t")
    history = {}
    for line in (RAW / "bleague_club_history_2026-09-29.txt").read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        pid, name, birth, rows = line.split("|")
        parsed = []
        for item in filter(None, rows.split(";")):
            season, abbr = item.split(" ", 1)
            parsed.append((int(season[:4]), abbr))
        history[pid] = {"name": name, "birth": birth, "rows": parsed}
    return standings, by_season_abbr, abbr_names, history


def main() -> None:
    standings, by_season_abbr, abbr_names, history = load_inputs()

    orgs: dict[str, str] = {r["organization_id"]: r["name"] for r in read(ROOT / "data/master/organization.csv")}
    for path in (ROOT / "data" / "candidate").rglob("organization_candidates.csv"):
        for r in read(path):
            orgs.setdefault(r["organization_id"], r["name"])
    for oid, (_, new) in ORG_CORRECTIONS.items():
        orgs[oid] = new
    for oid, name in NEW_ORGS.values():
        orgs[oid] = name
    name_to_org = defaultdict(set)
    for oid, name in orgs.items():
        name_to_org[name.replace(" ", "")].add(oid)

    team_names = defaultdict(set)
    for r in abbr_names:
        team_names[r["team_id"]].add(r["full_name_on_standings"])

    def full_name(season: int, abbr: str, tid: str) -> str:
        for r in abbr_names:
            lo, hi = map(int, r["seasons"].split("-"))
            if r["abbr"] == abbr and r["team_id"] == tid and lo <= season <= hi:
                return r["full_name_on_standings"]
        return ""

    def resolve(season: int, abbr: str):
        row = by_season_abbr.get((season, abbr))
        if row:
            tid, tab, std_season = row["team_id"], row["tab"], season
        else:
            # The player page sometimes uses today's abbreviation for an old
            # season (e.g. 横浜BC for 2020-21 when the standings said 横浜).
            cands = {r["team_id"] for r in standings if r["abbr"] == abbr}
            if len(cands) != 1:
                return None
            tid = cands.pop()
            match = [r for r in standings if r["team_id"] == tid and int(r["season_start_year"]) == season]
            if not match:
                return None
            tab, std_season = match[0]["tab"], season
        std_abbr = [r["abbr"] for r in standings if r["team_id"] == tid and int(r["season_start_year"]) == season][0]
        if tid in SPLIT_TEAMS:
            org = next(o for last, o in SPLIT_TEAMS[tid] if season <= last)
        elif tid in NEW_ORGS:
            org = NEW_ORGS[tid][0]
        else:
            found = set()
            for n in team_names[tid]:
                found |= name_to_org.get(n.replace(" ", ""), set())
            if tid == "1639":
                found = {"ORG000222"}
            if len(found) != 1:
                return None
            org = found.pop()
        return {"tid": tid, "tab": tab, "std_season": std_season, "std_abbr": std_abbr,
                "season_name": full_name(season, std_abbr, tid), "org": org}

    targets = list(csv.DictReader((ROOT / "docs/DEEPENING_BLEAGUE_ERA_TARGETS.csv").open(encoding="utf-8")))
    master_people = {r["person_id"]: r["name"] for r in read(ROOT / "data/master/person.csv")}
    master_careers = read(ROOT / "data/master/career.csv")

    career_seq = FIRST_CAREER
    waves = [targets[i:i + WAVE_SIZE] for i in range(0, len(targets), WAVE_SIZE)]
    summary = []
    for wave_no, chunk in enumerate(waves, 1):
        prefix = f"B31W{wave_no}"
        base = OUT / f"wave_{wave_no:02d}"
        careers, sources, evidence, decisions, issues, org_rows = [], [], [], [], [], {}
        source_ids: dict[tuple, str] = {}
        seq = defaultdict(int)

        def next_id(kind: str) -> str:
            seq[kind] += 1
            return f"{prefix}{kind}{seq[kind]:04d}"

        def source_for(key: tuple, title: str, url: str) -> str:
            if key not in source_ids:
                sid = next_id("S")
                source_ids[key] = sid
                sources.append({"source_id": sid, "title": title, "publisher": "B.LEAGUE", "url": url, "accessed_at": CHECKED_AT})
            return source_ids[key]

        def ev(entity_id, field, value, sid, locator, summary_text, note=""):
            evidence.append({
                "record_id": next_id("E"), "entity_type": "Career", "entity_id": entity_id,
                "field_name": field, "candidate_value": value, "source_id": sid,
                "source_locator": locator, "evidence_summary": summary_text,
                "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": note,
            })

        def issue(pid, related, itype, text, next_check):
            issues.append({"issue_id": next_id("I"), "person_id": pid, "related_id": related,
                           "issue_type": itype, "status": "HOLD", "description": text, "next_check": next_check})

        wave_new = 0
        for t in chunk:
            pid = t["person_id"]
            name = master_people[pid]
            plain = name.replace(" ", "")
            bids = t["bleague_player_ids"].split("|")
            if len(bids) > 1:
                issue(pid, pid, "DUAL_PLAYER_ID",
                      f"{plain}はMasterのSourceにB.LEAGUE PlayerIDが{len(bids)}つ（{'・'.join(bids)}）あり、公式サイト上もそれぞれ別ページに所属履歴が分かれて表示される（生年月日は同一）。本Waveでは両ページの履歴を合わせて扱った。公式サイト側の紐付けの問題か、登録上の理由かは未確認。",
                      "B.LEAGUE公式の表示・クラブ公式発表で同一人物の登録状況を確認")
            prof_sids = {}
            rows = []
            for b in bids:
                prof_sids[b] = source_for(("profile", b), f"{plain} 選手プロフィール（クラブ所属履歴）",
                                          f"https://www.bleague.jp/roster_detail/?PlayerID={b}")
                rows += [(y, ab, b) for y, ab in history[b]["rows"]]
            rows = sorted(set(rows))
            if not rows:
                continue
            last_year = max(y for y, _, _ in rows)
            if last_year < CURRENT_SEASON:
                issue(pid, pid, "NOT_ON_CURRENT_ROSTER",
                      f"{plain}のB.LEAGUE公式クラブ所属履歴の最新行は{season_label(last_year)}で、2026-27シーズンの行がない（2026-09-29時点）。移籍・退団・海外挑戦等の理由は記録しない。既存Master Careerの終了年は変更していない。",
                      "クラブ公式発表で現況を確認し、必要なら訂正経路で終了年を扱う")
            per_season = defaultdict(list)
            resolved = []
            for y, ab, b in rows:
                r = resolve(y, ab)
                per_season[y].append(ab)
                if r is None:
                    issue(pid, pid, "CLUB_UNRESOLVED",
                          f"{plain}の所属履歴「{season_label(y)} {ab}」の略称を公式順位表のクラブに対応付けられなかった。Careerは登録していない。",
                          "B.LEAGUE公式のクラブページで確認")
                    continue
                resolved.append((y, ab, b, r))
            for y, abs_ in per_season.items():
                if len(abs_) > 1:
                    issue(pid, pid, "SAME_SEASON_TWO_CLUBS",
                          f"{plain}の所属履歴には{season_label(y)}に「{'」「'.join(abs_)}」の{len(abs_)}行がある（シーズン途中の移籍とみられる）。両方のCareerに同じ年を用いた。移籍時期・理由は記録しない。",
                          "クラブ公式の加入・退団発表で時期を確認")
            by_org = defaultdict(list)
            for y, ab, b, r in resolved:
                by_org[r["org"]].append((y, ab, b, r))
            stints = []
            for org, items in by_org.items():
                items.sort()
                cur = [items[0]]
                for it in items[1:]:
                    if it[0] == cur[-1][0] + 1:
                        cur.append(it)
                    else:
                        stints.append((org, cur))
                        cur = [it]
                stints.append((org, cur))
            stints.sort(key=lambda s: s[1][0][0])

            mine = [c for c in master_careers if c["person_id"] == pid]
            for org, items in stints:
                s = items[0][0]
                last = items[-1][0]
                e = "" if last >= CURRENT_SEASON else str(last + 1)
                matched = None
                for c in mine:
                    if c["organization_id"] != org:
                        continue
                    cs = int(c["start"]) if c["start"] else None
                    ce = int(c["end"]) if c["end"] else None
                    # Inclusive with one year of slack: older MASTER rows
                    # sometimes use calendar years (e.g. start=end=2025 for
                    # a 2024-25 stay). A genuine return to the same club is
                    # always separated by at least one other season, so the
                    # slack cannot merge two separate stays.
                    lo = cs if cs is not None else -1
                    hi = ce if ce is not None else 9999
                    if lo <= last + 1 and hi >= s:
                        matched = c
                        break
                if matched:
                    if (matched["start"] and matched["start"] != str(s)) or (matched["end"] and e and matched["end"] != e) or (not matched["start"]):
                        issue(pid, matched["career_id"], "MASTER_PERIOD_DIFFERENCE",
                              f"{plain}の既存Master Career {matched['career_id']}（{orgs[org]}、start={matched['start'] or '空'}・end={matched['end'] or '空'}）は、B.LEAGUE公式所属履歴から導いた期間（{season_label(s)}〜{season_label(last)}、start={s}・end={e or '空'}）と異なる、または期間が未記録。Masterの値は変更していない。",
                              "差異の理由（特別指定・契約時期等）を確認し、必要なら訂正経路で扱う")
                    continue
                cid = f"C{career_seq:06d}"
                career_seq += 1
                wave_new += 1
                careers.append({"career_id": cid, "person_id": pid, "organization_id": org, "role": "Player", "start": str(s), "end": e})
                org_rows[org] = orgs[org]
                rows_txt = f"「{season_label(items[0][0])} {items[0][1]}」" + (f"〜「{season_label(items[-1][0])} {items[-1][1]}」" if len(items) > 1 else "")
                sid = prof_sids[items[0][2]]
                ev(cid, "organization_id", org, sid, f"クラブ所属履歴 > {rows_txt}", "B.LEAGUE公式の所属履歴で在籍を確認（略称表記）")
                r0 = items[0][3]
                div = {"1": "B1", "2": "B2", "3": "B3"}[r0["tab"]] if r0["std_season"] < 2026 else f"tab={r0['tab']}"
                std_sid = source_for(("standings", r0["std_season"], r0["tab"]),
                                     f"B.LEAGUE 順位表 {season_label(r0['std_season'])}（{div}）",
                                     f"https://www.bleague.jp/standings/?year={r0['std_season']}&tab={r0['tab']}")
                ev(cid, "organization_id", org, std_sid,
                   f"順位表 > クラブ「{r0['season_name']}」（略称「{r0['std_abbr']}」、club_detail TeamID={r0['tid']}）",
                   "公式順位表で略称とクラブ名・TeamIDの対応を確認")
                ev(cid, "start", str(s), sid, f"クラブ所属履歴 > 「{season_label(s)} {items[0][1]}」", f"所属履歴の最初のシーズン{season_label(s)}の開始年")
                if e:
                    ev(cid, "end", e, sid, f"クラブ所属履歴 > 「{season_label(last)} {items[-1][1]}」", f"所属履歴の最後のシーズン{season_label(last)}の終了年")
                decisions.append({"decision_id": next_id("D"), "entity_type": "Career", "entity_id": cid,
                                  "decision": "READY_FOR_VERIFIED_REVIEW",
                                  "eligible_fields": "organization_id|role|start" + ("|end" if e else ""),
                                  "held_fields": "" if e else "end",
                                  "reason": "B.LEAGUE公式の所属履歴と公式順位表で確認" + ("" if e else "。2026-27在籍中のため終了年なし"),
                                  "reviewed_at": CHECKED_AT})
                names_used = sorted({it[3]["season_name"] for it in items if it[3]["season_name"]})
                if any(n.replace(" ", "") != orgs[org].replace(" ", "") for n in names_used):
                    issue(pid, cid, "ORG_NAME_HISTORY",
                          f"{cid}の在籍期間中の公式順位表上のクラブ名は「{'」「'.join(names_used)}」で、登録Organization名「{orgs[org]}」と異なる。B.LEAGUE公式のTeamID（{r0['tid']}）が同一のため、Yuichiの判断（2026-09-29、栃木→宇都宮ブレックスと同じ扱い）により同一Organizationとして登録した。",
                          "Organization名称の時系列表現（改称履歴）のスキーマ整備を検討")
        write_csv(base / "person_candidates.csv", ["person_id", "name"], [])
        write_csv(base / "organization_candidates.csv", ["organization_id", "name"],
                  [{"organization_id": k, "name": v} for k, v in sorted(org_rows.items())])
        write_csv(base / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
        write_csv(base / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], sources)
        write_csv(base / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value",
                                                  "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
        write_csv(base / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
        write_csv(base / "qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision",
                                              "eligible_fields", "held_fields", "reason", "reviewed_at"], decisions)
        summary.append((wave_no, len(chunk), len(careers), len(evidence), len(issues), len(org_rows)))
        print(f"batch_031/wave_{wave_no:02d}: persons={len(chunk)} careers={len(careers)} evidence={len(evidence)} issues={len(issues)} orgs={len(org_rows)} sources={len(sources)}")

    write_csv(OUT / "org_corrections.csv", ["organization_id", "old_name", "new_name", "reason"],
              [{"organization_id": k, "old_name": o, "new_name": n,
                "reason": "batch_022で要約型Web取得ツールの英訳から登録した誤り。B.LEAGUE公式の選手一覧・順位表（TeamID=1639）の表記はいずれも「トライフープ岡山」"}
               for k, (o, n) in ORG_CORRECTIONS.items()])
    print(f"next free Career ID: C{career_seq:06d}")


if __name__ == "__main__":
    main()
