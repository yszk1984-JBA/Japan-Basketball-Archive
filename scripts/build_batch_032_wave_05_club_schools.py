#!/usr/bin/env python3
"""Build batch_032 Wave 5: 出身校 from club-official profiles, CANDIDATE.

Yuichi (2026-10-04): 「出身校が不明な32名 … についても続けて下さい」.
Target: MASTER persons on a 2026-27 B.PREMIER roster with no school Career
(their B.LEAGUE profile shows 出身校「-」). All of them were registered in
batch_032, so the additions go into that batch (per-origin rule).

Raw values: data/raw/research/club_profiles_school_2026-10-04.txt (club
official player pages, read in the browser on 2026-10-04). The club page
carries the same PlayerID as the B.LEAGUE profile, which fixes identity.

- One school Career per school, period blank (same rule as batch_032).
- 東京サンロッカーズ pages give the school only in prose (「…大学出身」);
  these and the abbreviated 「神奈川大」 are Tier 2 in the approval packet.
- 深水虎太郎's 出身校 is 「千葉ジェッツU18」 (a youth club, not a school):
  not registered as a school, kept as an issue.
- The pages name a university (one US high school) only, so the existing
  SCHOOL_NOT_LISTED issues for the high school stay open.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_032/wave_05"
RAW = ROOT / "data/raw/research/club_profiles_school_2026-10-04.txt"
CHECKED = "2026-10-04"
P = "B32W5"
FIRST_CAREER = 2687
NEW_ORGS = {  # name on the page -> new Organization
    "大阪商業大学": "ORG000479",
    "サンタマルガリータ・カトリック高校": "ORG000480",
    "スカイラインカレッジ": "ORG000481",
    "ワシントン州立大学": "ORG000482",
    "ノーザンコロラド大学": "ORG000483",
}
ALIASES = {"神奈川大": "神奈川大学"}
# B.LEAGUE PlayerID -> (MASTER person, school as printed, prose?)
TARGETS = [
    ("5100000031", "P000321", "大阪学院大学"),
    ("5100000066", "P000322", "セントジョセフ大学"),
    ("18148", "P000323", "東海大学"),
    ("8538", "P000324", "大阪商業大学"),
    ("51000547", "P000325", "神奈川大"),
    ("20031", "P000326", "関西学院大学"),
    ("30437", "P000327", "筑波大学"),
    ("51000563", "P000333", "専修大学"),
    ("33040", "P000337", "サンタマルガリータ・カトリック高校"),
    ("51000311", "P000338", "九州共立大学"),
    ("42616", "P000339", "スカイラインカレッジ"),
    ("15853", "P000341", "白鷗大学"),
    ("8447", "P000342", "東海大学"),
    ("12598", "P000343", "ワシントン州立大学"),
    ("49493", "P000344", "関西学院大学"),
    ("11309", "P000345", "ノーザンコロラド大学"),
    ("10872", "P000376", "筑波大学"),
    ("51000590", "P000378", "大東文化大学"),
]
NON_SCHOOL = [("51000564", "P000298")]  # 深水虎太郎: 千葉ジェッツU18


def raw_rows() -> dict[str, dict[str, str]]:
    rows = {}
    for line in RAW.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        pid, name, club, url, text = line.split("|", 4)
        rows[pid] = {"name": name, "club": club, "url": url, "text": text}
    return rows


def main() -> None:
    raw = raw_rows()
    m_people = {r["person_id"]: r["name"] for r in read_csv(ROOT / "data/master/person.csv")}
    m_orgs = {r["organization_id"]: r["name"] for r in read_csv(ROOT / "data/master/organization.csv")}
    name2org = {n: o for o, n in m_orgs.items()}
    all_orgs = dict(m_orgs)
    for path in (ROOT / "data/candidate").rglob("organization_candidates.csv"):
        if OUT not in path.parents:
            for r in read_csv(path):
                all_orgs.setdefault(r["organization_id"], r["name"])
    m_careers = read_csv(ROOT / "data/master/career.csv")
    errors = []

    sources, careers, evidence, decisions, issues, orgs = [], [], [], [], [], {}
    for i, (bid, pid, school) in enumerate(TARGETS, 1):
        r = raw[bid]
        if r["name"].replace(" ", "") != m_people[pid].replace(" ", ""):
            errors.append(f"{pid}: name differs ({r['name']} / {m_people[pid]})")
        prose = "=" not in r["text"].split("（")[0]
        if school not in r["text"]:
            errors.append(f"{pid}: school not in raw text")
        oname = ALIASES.get(school, school)
        oid = NEW_ORGS.get(school) or name2org.get(oname)
        if not oid:
            errors.append(f"{pid}: no Organization for {oname}")
            continue
        if oid in NEW_ORGS.values():
            if oid in all_orgs:
                errors.append(f"{oid}: already used")
            orgs[oid] = oname
        else:
            orgs[oid] = m_orgs[oid]
        if any(c["person_id"] == pid and c["organization_id"] == oid for c in m_careers):
            errors.append(f"{pid}: Career to {oid} already in MASTER")
        sid, cid = f"{P}S{i:04d}", f"C{FIRST_CAREER + i - 1:06d}"
        sources.append({"source_id": sid, "title": f"{r['name']} 選手プロフィール", "publisher": f"{r['club']}（クラブ公式サイト）",
                        "url": r["url"], "accessed_at": CHECKED})
        careers.append({"career_id": cid, "person_id": pid, "organization_id": oid, "role": "Player", "start": "", "end": ""})
        where = "選手紹介文" if prose else "プロフィール > " + r["text"].split("=")[0]
        quote = next(x for x in r["text"].split("。") if school in x) if prose else school
        if "PlayerID=" in r["url"]:
            summary = f"クラブ公式の選手ページ（PlayerID={bid}、B.LEAGUE公式と同じ）で出身校を確認"
        else:
            summary = "クラブ公式の選手紹介ページ（2026-27在籍選手、氏名がB.LEAGUE公式と一致）で出身校を確認"
        if prose:
            summary += "（紹介文中の「…出身」「…を経て」の記述）"
        if school in ALIASES:
            summary += f"。略記「{school}」を既存の「{oname}」（{oid}）として登録"
        evidence.append({"record_id": f"{P}E{len(evidence) + 1:04d}", "entity_type": "Career", "entity_id": cid,
                         "field_name": "organization_id", "candidate_value": oid, "source_id": sid,
                         "source_locator": f"{where}：{quote}", "evidence_summary": summary, "assessment": "SUPPORTED",
                         "checked_at": CHECKED, "issue_note": ""})
        decisions.append({"decision_id": f"{P}D{len(decisions) + 1:04d}", "entity_type": "Career", "entity_id": cid,
                          "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "organization_id|role", "held_fields": "start|end",
                          "reason": "クラブ公式の選手ページで出身校を確認、在学期間は未確認", "reviewed_at": CHECKED})
        if prose or school in ALIASES:
            issues.append({"issue_id": f"{P}I{len(issues) + 1:04d}", "person_id": pid, "related_id": cid,
                           "issue_type": "SCHOOL_FROM_PROSE" if prose else "SCHOOL_NAME_ABBREVIATED", "status": "HOLD",
                           "description": (f"{m_people[pid]}の出身校は、クラブ公式の選手紹介文の記述（「{quote}」）から読み取った。出身校欄としての記載ではない。"
                                           if prose else f"{m_people[pid]}のクラブ公式プロフィールの出身校は「{school}」と略記。既存の「{oname}」として登録した。"),
                           "next_check": "B.LEAGUE公式プロフィールの出身校欄の更新、大学の公式記録で確認"})
    for bid, pid in NON_SCHOOL:
        r = raw[bid]
        issues.append({"issue_id": f"{P}I{len(issues) + 1:04d}", "person_id": pid, "related_id": pid,
                       "issue_type": "NON_SCHOOL_ENTRY", "status": "HOLD",
                       "description": f"{m_people[pid]}のクラブ公式プロフィールの出身校欄は「千葉ジェッツU18」（ユースチーム）。学校ではないため学校のCareerは登録していない（{r['url']}）。",
                       "next_check": "ユースチームの在籍をCareerとして記録するかYuichiと方針を決める"})
    if len({c["career_id"] for c in careers}) != len(careers):
        errors.append("duplicate career id")
    used = {r["career_id"] for r in m_careers}
    for path in (ROOT / "data/candidate").rglob("career_candidates.csv"):
        if OUT not in path.parents:
            used |= {r["career_id"] for r in read_csv(path)}
    if {c["career_id"] for c in careers} & used:
        errors.append("Career ID already used")
    if errors:
        raise SystemExit("; ".join(errors))

    write_csv(OUT / "person_candidates.csv", ["person_id", "name"], [])
    write_csv(OUT / "organization_candidates.csv", ["organization_id", "name"],
              [{"organization_id": o, "name": n} for o, n in sorted(orgs.items())])
    write_csv(OUT / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], sources)
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
    write_csv(OUT / "qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields",
                                         "reason", "reviewed_at"], decisions)
    print(f"wave_05: careers={len(careers)} orgs={len(orgs)} (new {sum(o in NEW_ORGS.values() for o in orgs)}) "
          f"evidence={len(evidence)} issues={len(issues)}")


if __name__ == "__main__":
    main()
