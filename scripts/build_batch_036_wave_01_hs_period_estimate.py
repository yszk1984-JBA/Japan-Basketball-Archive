#!/usr/bin/env python3
"""Build batch_036 Wave 1: estimated high-school periods from birth dates, CANDIDATE.

Yuichi (2026-10-25): 「多くの選手の高校生の期間が期間未確認になっていることが多い／
日本の高校に進学・卒業している人に関しては、生年月日から推測して高校の期間を設定
してください」. His decisions on the follow-up questions:
- show the period on the site as an estimate (「推定」と明記して表示);
- exclude players who attended a school outside Japan (海外の学校に通った選手).

This is an explicit, owner-approved exception to the Governance rule
"do not guess". Every value is marked as an estimate (issue_note 「推定値」),
so the site can label it and a later official source can replace it.

Rule (Japanese school year): people born 2 April Y .. 1 April Y+1 are in the
same school year; they enter high school in April Y+16 and graduate in March
Y+19. Period = start Y+16, end Y+19 (the same start/end-year convention as
the club seasons). The birth date is the one already in MASTER (B.LEAGUE
official profile in almost every case).

Targets: MASTER Careers at a Japanese high school (name ends with 高等学校/高校,
no Latin letters) with no period, for persons who
- have exactly one birth date in MASTER,
- have exactly one Japanese high school, and
- have no school outside Japan.
A period that conflicts with a dated university Career of the same person
(university start earlier than the estimated graduation) is not set and is
kept as an issue.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_036/wave_01"
CHECKED = "2026-10-25"
P = "B36W1"
NOTE = "推定値：生年月日から日本の学年制で算出（Yuichiの方針 2026-10-25）。資料で確認した期間ではない"
SCHOOL = re.compile(r"(大学|大$|高校|高等学校|中学|学園|学院|カレッジ|スクール|アカデミー|College|University|School|Academy|Prep|Institute)", re.I)


def is_hs(name: str) -> bool:
    return name.endswith("高等学校") or name.endswith("高校")


def is_foreign_school(name: str) -> bool:
    return bool(SCHOOL.search(name)) and (bool(re.search(r"[A-Za-z]", name)) or bool(re.match(r"^[ァ-ヶー・]+", name)))


def hs_years(birth: str) -> tuple[int, int]:
    y, m, d = (int(x) for x in birth.split("-"))
    base = y if (m, d) >= (4, 2) else y - 1
    return base + 16, base + 19


def main() -> None:
    orgs = {r["organization_id"]: r["name"] for r in read_csv(ROOT / "data/master/organization.csv")}
    people = {r["person_id"]: r["name"] for r in read_csv(ROOT / "data/master/person.csv")}
    careers = read_csv(ROOT / "data/master/career.csv")
    m_sources = {r["source_id"]: r for r in read_csv(ROOT / "data/master/source.csv")}
    births: dict[str, list[dict[str, str]]] = defaultdict(list)
    for e in read_csv(ROOT / "data/master/evidence.csv"):
        if e["entity_type"] == "Person" and e["field_name"] == "birth_date":
            births[e["entity_id"]].append(e)
    by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
    for c in careers:
        by_person[c["person_id"]].append(c)

    corr, evidence, sources, issues, skipped = [], [], {}, [], defaultdict(list)
    for pid in sorted(by_person):
        cs = by_person[pid]
        jhs = [c for c in cs if is_hs(orgs[c["organization_id"]]) and not is_foreign_school(orgs[c["organization_id"]])]
        if not jhs or all(c["start"] or c["end"] for c in jhs):
            continue
        if any(is_foreign_school(orgs[c["organization_id"]]) for c in cs):
            skipped["海外の学校に通った選手（Yuichiの方針で対象外）"].append(pid)
            continue
        values = sorted({e["candidate_value"] for e in births.get(pid, [])})
        if len(values) != 1:
            skipped["生年月日がMasterにない、または複数ある"].append(pid)
            continue
        if len(jhs) > 1:
            skipped["日本の高校が2校以上（どちらの期間か決められない）"].append(pid)
            continue
        c = jhs[0]
        if c["start"] or c["end"]:
            continue
        birth = values[0]
        start, end = hs_years(birth)
        univ = [u for u in cs if "大学" in orgs[u["organization_id"]] and u["start"]]
        if any(int(u["start"]) < end for u in univ):
            u = min(univ, key=lambda x: x["start"])
            issues.append({"issue_id": f"{P}I{len(issues) + 1:04d}", "person_id": pid, "related_id": c["career_id"],
                           "issue_type": "ESTIMATE_CONFLICT", "status": "HOLD",
                           "description": f"{people[pid]}：生年月日（{birth}）から算出した高校期間 {start}〜{end} が、{orgs[u['organization_id']]}の開始年 {u['start']} と合わないため設定していない。",
                           "next_check": "高校・大会の公式記録で確認"})
            continue
        be = births[pid][0]
        sid = be["source_id"]
        sources[sid] = m_sources[sid]
        y, mo, d = birth.split("-")
        loc = f"生年月日：{int(y)}年{int(mo)}月{int(d)}日（Master Evidence {be['record_id']}、{m_sources[sid]['publisher']}）"
        summary = (f"生年月日から日本の学年制（4月2日〜翌年4月1日生まれが同学年）で、高校入学{start}年4月・卒業{end}年3月と算出した推定値。"
                   f"開始年＝{start}、終了年＝{end}")
        for field, value in (("start", str(start)), ("end", str(end))):
            evidence.append({"record_id": f"{P}E{len(evidence) + 1:04d}", "entity_type": "Career", "entity_id": c["career_id"],
                             "field_name": field, "candidate_value": value, "source_id": sid, "source_locator": loc,
                             "evidence_summary": summary, "assessment": "SUPPORTED", "checked_at": CHECKED, "issue_note": NOTE})
        corr.append({"career_id": c["career_id"], "person_id": pid, "organization_name": orgs[c["organization_id"]],
                     "old_start": "", "old_end": "", "new_start": str(start), "new_end": str(end),
                     "reason": f"推定（生年月日 {birth} から算出）"})
    for reason, pids in skipped.items():
        issues.append({"issue_id": f"{P}I{len(issues) + 1:04d}", "person_id": "", "related_id": "|".join(pids),
                       "issue_type": "ESTIMATE_SKIPPED", "status": "HOLD",
                       "description": f"高校期間の推定を行わなかった：{reason}（{len(pids)}名：{'、'.join(people[p] for p in pids)}）",
                       "next_check": "高校・大会の公式記録で確認"})
    write_csv(OUT / "master_corrections.csv", ["career_id", "person_id", "organization_name", "old_start", "old_end",
                                               "new_start", "new_end", "reason"], corr)
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], list(sources.values()))
    write_csv(OUT / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
    print(f"batch_036 wave_01: estimates={len(corr)} evidence={len(evidence)} sources={len(sources)} issues={len(issues)} "
          + ", ".join(f"{k}={len(v)}" for k, v in skipped.items()))


if __name__ == "__main__":
    main()
