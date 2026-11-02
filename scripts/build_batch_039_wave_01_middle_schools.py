#!/usr/bin/env python3
"""Build batch_039 Wave 1: officially published junior-high schools of current players, CANDIDATE.

Yuichi (2026-11-02): 「今の選手の中で中学が公表されている選手がいれば、追加したい」→
「公式に公表されているものは表示する」「公式のみ」. This changes the earlier rule
(middle schools not recorded / roadmap item 3 "non-public"): junior-high schools are
recorded when an official source (B.LEAGUE, club) publishes them as the player's career.

Sources (raw: data/raw/research/middle_school_official_2026-11-02.md):
1. B.LEAGUE DRAFT 2026 prospects list (career lines with dates),
2. アルバルク東京 player_lp, 3. 大阪エヴェッサ player pages, 4. 神戸ストークス player_lp.
The prospects list also gives official high-school periods (2019年4月-2022年3月 …); where
the person's MASTER high-school Career has the same school name, the official period is
added as evidence (replacing the birth-date estimate on the site, or correcting it).
Japanese junior-high schools only (names ending with 中学校 / 中等部); foreign schools,
youth teams (U15) and clubs are skipped. Periods: only from 「YYYY年4月-YYYY年3月」 lines.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_039/wave_01"
RAW = ROOT / "data/raw/research/middle_school_official_2026-11-02.md"
CHECKED = "2026-11-02"
P = "B39W1"
FIRST_CAREER = 2830
FIRST_ORG = 519
PROSPECTS = ("【公式】候補選手一覧 | B.LEAGUE DRAFT 2026", "B.LEAGUE", "https://www.bleague.jp/draft2026/prospects/list/")
DATED = re.compile(r"(\d{4})年\s*(\d{1,2})\s*月?\s*[-ｰ～−]\s*(\d{4})年\s*(\d{1,2})月\s+(\S+)")
MS = re.compile(r"(中学校|中等部)$")


def norm(name: str) -> str:
    return name.replace(" ", "").replace("　", "").replace("･", "・")


def parse_raw() -> list[dict]:
    rows, section = [], 0
    for line in RAW.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = int(line[3])
            continue
        if "\t" not in line:
            continue
        cols = line.split("\t")
        if section == 1:
            name, birth, career = cols
            ms = [(m, s) for m in DATED.finditer(career) for s in [m.group(5)] if MS.search(s)]
            undated = [t for t in career.split() if MS.search(t)]
            hs = [m for m in DATED.finditer(career) if m.group(5).endswith(("高等学校", "高校"))]
            school = ms[0][1] if ms else (undated[0] if undated else "")
            if not school:
                continue
            m = ms[0][0] if ms else None
            period = (m.group(1), m.group(3)) if m and m.group(2) == "4" and m.group(4) == "3" else ("", "")
            loc = career[career.index(m.group(0)):career.index(m.group(0)) + len(m.group(0))] if m else school
            hs_m = hs[0] if hs and hs[0].group(2) == "4" and hs[0].group(4) == "3" else None
            rows.append({"name": name, "school": school, "period": period, "src": "prospects", "url": PROSPECTS[2],
                         "loc": f"経歴 > 「{loc}」", "hs": (hs_m.group(5), hs_m.group(1), hs_m.group(3), hs_m.group(0)) if hs_m else None})
        elif section == 2:
            name, school, _hs, url = cols
            rows.append({"name": name, "school": school, "period": ("", ""), "src": "alvark", "url": url,
                         "loc": f"プライベート > 出身校（中学校）：{school}", "hs": None})
        elif section == 3:
            pid_name, rest = cols
            bid, name = pid_name.split(" ", 1)
            school = rest.split("（")[0]
            rows.append({"name": name, "school": school, "period": ("", ""), "src": "evessa",
                         "url": f"https://www.evessa.com/lp/PlayerID_{bid}/", "loc": f"Q出身校（中）A{school}", "hs": None})
        elif section == 4:
            name, school, url = cols
            rows.append({"name": name, "school": school, "period": ("", ""), "src": "storks", "url": url,
                         "loc": f"出身校（中学校）は？ {school}", "hs": None})
    return rows


PUBLISHERS = {"prospects": "B.LEAGUE", "alvark": "アルバルク東京（クラブ公式）", "evessa": "大阪エヴェッサ（クラブ公式）", "storks": "神戸ストークス（クラブ公式）"}


def main() -> None:
    people = {r["person_id"]: r["name"] for r in read_csv(ROOT / "data/master/person.csv")}
    by_name = defaultdict(list)
    for pid, n in people.items():
        by_name[norm(n)].append(pid)
    orgs = {r["organization_id"]: r["name"] for r in read_csv(ROOT / "data/master/organization.csv")}
    org_by_name = {n: o for o, n in orgs.items()}
    careers = read_csv(ROOT / "data/master/career.csv")
    errors, skipped = [], []
    sources, evidence, decisions, new_careers, new_orgs, corr = {}, [], [], [], {}, []
    est_ids = {e["entity_id"] for e in read_csv(ROOT / "data/master/evidence.csv") if e["issue_note"].startswith("推定値")}

    def sid(key: str, title: str, pub: str, url: str) -> str:
        if key not in sources:
            sources[key] = {"source_id": f"{P}S{len(sources) + 1:04d}", "title": title, "publisher": pub, "url": url, "accessed_at": CHECKED}
        return sources[key]["source_id"]

    def ev(cid: str, field: str, value: str, s: str, loc: str, summary: str, note: str = "") -> None:
        evidence.append({"record_id": f"{P}E{len(evidence) + 1:04d}", "entity_type": "Career", "entity_id": cid, "field_name": field,
                         "candidate_value": value, "source_id": s, "source_locator": loc, "evidence_summary": summary,
                         "assessment": "SUPPORTED", "checked_at": CHECKED, "issue_note": note})

    seen = set()
    for row in parse_raw():
        pids = by_name.get(norm(row["name"]), [])
        if len(pids) != 1:
            skipped.append(f"{row['name']}：Masterで一意に特定できない")
            continue
        pid = pids[0]
        if pid in seen:
            continue
        seen.add(pid)
        school = row["school"]
        oid = org_by_name.get(school) or next((o for o, n in new_orgs.items() if n == school), None)
        if not oid:
            oid = f"ORG{FIRST_ORG + len(new_orgs):06d}"
            if oid in orgs:
                errors.append(f"{oid}: used")
            new_orgs[oid] = school
        if any(c["person_id"] == pid and c["organization_id"] == oid for c in careers):
            skipped.append(f"{row['name']}：{school}は登録済み")
            continue
        cid = f"C{FIRST_CAREER + len(new_careers):06d}"
        start, end = row["period"]
        new_careers.append({"career_id": cid, "person_id": pid, "organization_id": oid, "role": "Player", "start": start, "end": end})
        title = PROSPECTS[0] if row["src"] == "prospects" else f"{row['name']} 選手紹介"
        s = sid(row["src"] if row["src"] == "prospects" else row["url"], title, PUBLISHERS[row["src"]], row["url"])
        ev(cid, "organization_id", oid, s, row["loc"], "公式の選手紹介・経歴で出身中学校を確認")
        ev(cid, "role", "Player", s, row["loc"], "出身校（中学校）としての記載")
        if start:
            ev(cid, "start", start, s, row["loc"], "経歴の在学期間（4月入学）")
            ev(cid, "end", end, s, row["loc"], "経歴の在学期間（3月卒業）")
        decisions.append({"decision_id": f"{P}D{len(decisions) + 1:04d}", "entity_type": "Career", "entity_id": cid,
                          "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "organization_id|role" + ("|start|end" if start else ""),
                          "held_fields": "" if start else "start|end", "reason": f"{PUBLISHERS[row['src']]}の公式資料", "reviewed_at": CHECKED})
        if row["hs"]:
            hs_name, hs_start, hs_end, hs_text = row["hs"]
            hs_oid = org_by_name.get(hs_name)
            match = [c for c in careers if c["person_id"] == pid and c["organization_id"] == hs_oid] if hs_oid else []
            if len(match) != 1:
                skipped.append(f"{row['name']}：高校「{hs_name}」がMasterの高校Careerと名前で一致しないため、高校の期間は見送り")
                continue
            hc = match[0]
            loc = f"経歴 > 「{hs_text}」"
            if (hc["start"], hc["end"]) != (hs_start, hs_end):
                corr.append({"career_id": hc["career_id"], "person_id": pid, "organization_name": hs_name, "old_start": hc["start"],
                             "old_end": hc["end"], "new_start": hs_start, "new_end": hs_end, "reason": f"B.LEAGUE公式の経歴 {hs_text}"})
            for field, value in (("start", hs_start), ("end", hs_end)):
                ev(hc["career_id"], field, value, s, loc, "B.LEAGUE公式の経歴で高校の在学期間を確認（推定値ではなく公式の値）",
                   "既存MASTER Careerの期間の公式の根拠" + ("（推定値を置き換え）" if hc["career_id"] in est_ids else ""))
    issues = [{"issue_id": f"{P}I{i:04d}", "person_id": "", "related_id": "", "issue_type": "SKIPPED", "status": "HOLD",
               "description": d, "next_check": "公式資料で確認"} for i, d in enumerate(skipped, 1)]
    if errors:
        raise SystemExit("; ".join(errors))
    write_csv(OUT / "person_candidates.csv", ["person_id", "name"], [])
    write_csv(OUT / "organization_candidates.csv", ["organization_id", "name"],
              [{"organization_id": o, "name": n} for o, n in sorted((orgs | new_orgs).items()) if o in {c["organization_id"] for c in new_careers}])
    write_csv(OUT / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], new_careers)
    write_csv(OUT / "master_corrections.csv", ["career_id", "person_id", "organization_name", "old_start", "old_end", "new_start", "new_end", "reason"], corr)
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], list(sources.values()))
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
    write_csv(OUT / "qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields",
                                         "reason", "reviewed_at"], decisions)
    hs_ev = len({e["entity_id"] for e in evidence if e["field_name"] == "start" and e["entity_id"] not in {c["career_id"] for c in new_careers}})
    print(f"batch_039 wave_01: middle-school careers={len(new_careers)} (dated {sum(bool(c['start']) for c in new_careers)}) "
          f"new orgs={len(new_orgs)} hs official periods={hs_ev} (corrections {len(corr)}) evidence={len(evidence)} skipped={len(skipped)}")
    for s in skipped:
        print("  -", s)


if __name__ == "__main__":
    main()
