#!/usr/bin/env python3
"""Weekly check: B.LEAGUE official roster (RAW snapshot) vs MASTER current clubs.

Yuichi (2026-11-03)「Bプレミアの選手の経歴が合っているかのチェックを定期的にしたい」→
毎週（月曜の夜）、現所属＋新加入・退団、違いがあれば承認用の資料まで作る。

This script only READS. It compares a roster snapshot taken with
scripts/browser/fetch_bleague_roster.js (data/raw/research/bleague_roster_premier_<date>.tsv)
with the previous snapshot and with MASTER, and writes a difference report
(data/raw/research/weekly_check_<date>.md). It never edits MASTER. Each finding is
a lead to research (player profile, club news) before it becomes a CANDIDATE.

Usage:
  python3 scripts/check_bleague_roster.py data/raw/research/bleague_roster_premier_2026-11-10.tsv
  (the previous snapshot is the newest older file of the same kind, or --previous PATH)
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/research"
MASTER = ROOT / "data/master"
CLUBS = RAW / "bleague_club_abbreviations_2026-09-29.tsv"
EXCLUDED = RAW / "weekly_check_excluded.tsv"
SCHOOL = re.compile(r"(中学校|中等部|高等学校|高校|大学|学園|学院|College|University|School|Academy)", re.I)
# B.LEAGUE TeamIDs that appeared after the 2026-09-29 standings file, or whose MASTER name differs.
EXTRA_TEAM_NAMES: dict[str, list[str]] = {}


def norm(name: str) -> str:
    return re.sub(r"[\s　・･]", "", name)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_roster(path: Path, tab: str = "1") -> dict[str, tuple[str, str]]:
    """PlayerID -> (TeamID, name) for one tab."""
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        cols = line.split("\t")
        if cols[0] == tab:
            out[cols[2]] = (cols[1], cols[3])
    return out


def team_names() -> tuple[dict[str, list[str]], dict[str, str]]:
    names: dict[str, list[str]] = defaultdict(list)
    abbr: dict[str, str] = {}
    for line in CLUBS.read_text(encoding="utf-8").splitlines()[1:]:
        a, tid, full, *_ = line.split("\t")
        names[tid].append(full)
        abbr.setdefault(tid, a)
    for tid, extra in EXTRA_TEAM_NAMES.items():
        names[tid].extend(extra)
    return names, abbr


def snapshot_date(path: Path) -> str:
    m = re.search(r"(\d{4}-\d{2}-\d{2})\.tsv$", path.name)
    return m.group(1) if m else ""


def previous_snapshot(current: Path) -> Path | None:
    """Newest older roster snapshot that has B.PREMIER (tab=1) rows."""
    today = snapshot_date(current)
    files = [p for p in RAW.glob("bleague_roster_*.tsv") if "" < snapshot_date(p) < today and read_roster(p)]
    return max(files, key=snapshot_date) if files else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("current", type=Path)
    parser.add_argument("--previous", type=Path)
    args = parser.parse_args()
    current_path = args.current if args.current.is_absolute() else ROOT / args.current
    date = re.search(r"(\d{4}-\d{2}-\d{2})", current_path.name).group(1)
    prev_path = args.previous or previous_snapshot(current_path)
    if prev_path and not prev_path.is_absolute():
        prev_path = ROOT / prev_path

    now = read_roster(current_path)
    before = read_roster(prev_path) if prev_path else {}
    names, abbr = team_names()

    people = read_csv(MASTER / "person.csv")
    by_name: dict[str, list[str]] = defaultdict(list)
    for p in people:
        by_name[norm(p["name"])].append(p["person_id"])
    pname = {p["person_id"]: p["name"] for p in people}
    orgs = {o["organization_id"]: o["name"] for o in read_csv(MASTER / "organization.csv")}
    current_club: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for c in read_csv(MASTER / "career.csv"):
        org = orgs[c["organization_id"]]
        if c["start"] and not c["end"] and not SCHOOL.search(org):
            current_club[c["person_id"]].append((c["career_id"], org, c["start"]))

    def team(tid: str) -> str:
        return f"{abbr.get(tid, tid)}（TeamID {tid}）"

    def master_status(name: str, tid: str) -> tuple[str, str]:
        pids = by_name.get(norm(name), [])
        if not pids:
            return "unregistered", "Master未登録"
        if len(pids) > 1:
            return "ambiguous", f"Masterで同名{len(pids)}名（{', '.join(pids)}）"
        pid = pids[0]
        clubs = current_club.get(pid, [])
        expected = {norm(n) for n in names.get(tid, [])}
        if any(norm(org) in expected for _, org, _ in clubs):
            return "ok", f"{pid}：Masterの現所属と一致"
        shown = "、".join(f"{org}（{cid}、{start}〜）" for cid, org, start in clubs) or "現所属のCareerなし"
        return "mismatch", f"{pid} {pname[pid]}：Masterの現所属は {shown}"

    joined = [pid for pid in now if before and pid not in before]
    left = [pid for pid in before if pid not in now]
    moved = [pid for pid in now if pid in before and before[pid][0] != now[pid][0]]
    excluded = {}
    for line in EXCLUDED.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            bid, ename, reason, until = (line.split("\t") + [""] * 4)[:4]
            excluded[bid] = (ename, reason, until)
    findings = defaultdict(list)
    for pid, (tid, name) in now.items():
        kind, text = master_status(name, tid)
        if kind == "unregistered" and pid in excluded:
            ename, reason, until = excluded[pid]
            due = until and until <= date
            findings["review" if due else "excluded"].append(
                f"- {name}（PlayerID {pid}、{team(tid)}）：{reason}" + (f"（見直す日 {until}）" if until else ""))
            continue
        if kind != "ok":
            findings[kind].append(f"- {name}（PlayerID {pid}、{team(tid)}）：{text}")
    unknown_teams = sorted({tid for tid, _ in now.values() if tid not in names})

    lines = [f"# B.PREMIER 週次チェック（{date}）", "",
             "取得：Claudeのブラウザ（Yuichiの端末）で B.LEAGUE公式の選手一覧（tab=1、c=日本、e=在籍中）を取得し、"
             f"`{current_path.relative_to(ROOT)}` に記録。前回：`{prev_path.relative_to(ROOT) if prev_path else 'なし'}`。",
             "この一覧は調べるきっかけ（RAW）で、Masterは変更していない。各項目は選手プロフィール（/roster_detail/?PlayerID=）・クラブの発表で確かめてからCANDIDATEにする。",
             "", f"- 今回の一覧：{len(now)}名（{len({t for t, _ in now.values()})}クラブ）／前回：{len(before)}名", ""]
    def section(title: str, rows: list[str]) -> None:
        lines.extend([f"## {title}（{len(rows)}件）", ""] + (rows or ["- なし"]) + [""])
    section("前回から一覧に新しく載った", [f"- {now[p][1]}（PlayerID {p}、{team(now[p][0])}）：{master_status(now[p][1], now[p][0])[1]}" for p in joined])
    section("前回から一覧から消えた（退団・移籍・登録抹消の可能性）", [f"- {before[p][1]}（PlayerID {p}、前回 {team(before[p][0])}）" for p in left])
    section("前回からクラブが変わった", [f"- {now[p][1]}（PlayerID {p}）：{team(before[p][0])} → {team(now[p][0])}" for p in moved])
    section("Masterの現所属と一覧のクラブが違う", findings["mismatch"])
    section("Masterに未登録", findings["unregistered"])
    section("Masterで同名が複数（人物の特定が必要）", findings["ambiguous"])
    section("登録しない選手の見直し時期（18歳になった等。プロフィールを確認して登録を検討）", findings["review"])
    section("登録しない選手（weekly_check_excluded.tsv、変化なし）", findings["excluded"])
    if unknown_teams:
        section("クラブ名の対応表にないTeamID（EXTRA_TEAM_NAMESに追記が必要）", [f"- {t}" for t in unknown_teams])
    lines += ["## 注意", "", "- 18歳未満の選手は登録しない（プロフィールの生年月日で確認）。",
              "- 期限付移籍・育成契約は契約区分（contract_type）として扱う。", ""]
    out = RAW / f"weekly_check_{date}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}: now={len(now)} before={len(before)} joined={len(joined)} left={len(left)} moved={len(moved)} "
          f"mismatch={len(findings['mismatch'])} unregistered={len(findings['unregistered'])} review={len(findings['review'])} excluded={len(findings['excluded'])} ambiguous={len(findings['ambiguous'])} unknown_teams={unknown_teams}")


if __name__ == "__main__":
    main()
