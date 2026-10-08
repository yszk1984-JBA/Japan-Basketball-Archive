#!/usr/bin/env python3
"""Build batch_033 Wave 6: schools of B.ONE players, CANDIDATE.

Yuichi (2026-10-08): 「B.ONE選手（約30名）の出身高校を埋める」.
Target: MASTER persons on a 2026-27 B.ONE roster with no high-school Career.
All were registered in batch_033 (per-origin rule). Their B.LEAGUE profile
shows 出身校 (高)(大) as 「-」, so universities found on the same pages are
added too.

Raw values: data/raw/research/club_profiles_school_bone_2026-10-08.txt (club
official signing / special-designation announcements and player pages, read in
the browser). Identity: the birth date on each page matches the B.LEAGUE
profile (or the page carries the same PlayerID).

- One Career per school. Periods only where the page prints them
  (堀内・丸山: 「2014-17 高知中央高等学校」 etc.); otherwise blank.
- Middle schools and youth programmes are not recorded.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_033/wave_06"
RAW = ROOT / "data/raw/research/club_profiles_school_bone_2026-10-08.txt"
CHECKED = "2026-10-08"
P = "B33W6"
FIRST_CAREER = 2742
NEW_ORGS = {
    "ORG000497": "Maranatha High School", "ORG000498": "William Jewell College", "ORG000499": "Moberly Area Community College",
    "ORG000500": "パリサデス高校", "ORG000501": "ウィッティア大学", "ORG000502": "ピッツバーグ州立大学",
    "ORG000503": "金沢市立工業高等学校", "ORG000504": "コロンビア大学", "ORG000505": "IMGアカデミー",
    "ORG000506": "Haines City HS", "ORG000507": "Northeast Mississippi Community College",
}
ALB = "https://www.albirex.com/news/detail/id="
VOL = "https://www.volters.jp/news/detail/id="
HAN = "https://hannaryz.jp/news/detail/id="
DAMA = "https://veltex.co.jp/news/detail/id=44275"
I_PROSE = ("SCHOOL_FROM_PROSE", "学校名を紹介文・コメントの記述から読み取った（出身校欄ではない）。")
# (person, url, org, text on page, locator label, start, end, issue)
T = [
    ("P000415", DAMA, "ORG000497", "Maranatha High School", "■経歴", "", "",
     ("SCHOOL_AMBIGUOUS", "「Maranatha High School」は米国に同名校が複数あり、所在地はページに書かれていない。所在地未確認のまま1つのOrganizationとして登録した。")),
    ("P000415", DAMA, "ORG000498", "William Jewell College", "■経歴", "", "", None),
    ("P000415", DAMA, "ORG000499", "Moberly Area Community College", "■経歴", "", "", None),
    ("P000418", "https://www.b-warriors.net/news/45321/", "ORG000500", "パリサデス高校", "■経歴", "", "", None),
    ("P000418", "https://www.b-warriors.net/news/45321/", "ORG000501", "ウィッティア大学", "■経歴", "", "", None),
    ("P000419", HAN + "17614", "ORG000119", "洛南高等学校", "■出身校", "", "", None),
    ("P000419", HAN + "17614", "ORG000196", "関西学院大学", "■出身校", "", "", None),
    ("P000420", HAN + "19573", "ORG000119", "洛南高校", "■出身校", "", "", None),
    ("P000420", HAN + "19573", "ORG000207", "法政大学", "■出身校", "", "", None),
    ("P000421", VOL + "14415", "ORG000093", "白鷗大学", "プロフィール（出身校）", "", "", None),
    ("P000447", HAN + "20765", "ORG000502", "ピッツバーグ州立大学", "■出身校", "", "", None),
    ("P000452", "https://trains.co.jp/news/detail/id=19033", "ORG000297", "東海大学付属諏訪高等学校", "本文", "", "",
     I_PROSE),
    ("P000452", "https://trains.co.jp/news/detail/id=19033", "ORG000203", "国士舘大学", "■出身校", "", "", None),
    ("P000461", "https://g-crane-thunders.jp/news/detail/id=14807", "ORG000016", "中央大学", "出身校", "", "", None),
    ("P000462", VOL + "16168", "ORG000369", "宮崎県立小林高校", "プロフィール（学歴）", "", "", None),
    ("P000462", ALB + "24757", "ORG000020", "日本体育大学", "■出身校", "", "", None),
    ("P000463", ALB + "24749", "ORG000031", "拓殖大学", "■出身校", "", "", None),
    ("P000464", "https://www.storks.jp/news/detail/id=14736", "ORG000503", "金沢市立工業高校", "出身校", "", "", None),
    ("P000464", ALB + "24751", "ORG000148", "近畿大学", "■出身校", "", "", None),
    ("P000465", VOL + "13030", "ORG000156", "尽誠学園高等学校(香川県)", "プロフィール（学歴）", "", "", None),
    ("P000465", ALB + "24752", "ORG000148", "近畿大学", "■出身校", "", "",
     ("SCHOOL_NOT_ON_TEAM", "近畿大学には在籍したが、2019-20の熊本ヴォルターズの発表（https://www.volters.jp/news/detail/id=13030）に「男子バスケットボール部には所属せず」とある。学校Careerの役割はPlayerで登録しているため、扱いを確認する。")),
    ("P000466", ALB + "18571", "ORG000217", "帝京長岡高等学校", "■経歴", "", "", None),
    ("P000466", ALB + "18571", "ORG000093", "白鷗大学", "■経歴", "", "", None),
    ("P000467", ALB + "24924", "ORG000475", "2014-17　高知中央高等学校", "経歴", "2014", "2017", None),
    ("P000467", ALB + "24924", "ORG000214", "2017-19　名古屋学院大学", "経歴", "2017", "2019", None),
    ("P000467", ALB + "24924", "ORG000019", "2019-21　日本経済大学", "経歴", "2019", "2021", None),
    ("P000468", HAN + "15461", "ORG000117", "モントローズ・クリスチャン高校", "■出身校", "", "",
     ("SCHOOL_NAME_VARIANT", "ページの表記は「モントローズ・クリスチャン高校」。既存の「モントロス・クリスチャン高等学校」（ORG000117、同じ米国の学校）として登録した。")),
    ("P000468", HAN + "15461", "ORG000504", "コロンビア大学", "■出身校", "", "", None),
    ("P000469", ALB + "24921", "ORG000218", "2018-21　報徳学園高等学校", "経歴", "2018", "2021", None),
    ("P000469", ALB + "24921", "ORG000121", "2021-25　日本大学", "経歴", "2021", "2025", None),
    ("P000482", "https://www.fukuiblowinds.com/news/detail/id=47877", "ORG000505", "IMGアカデミー", "出身校", "", "", None),
    ("P000483", "https://b-corsairs.com/news/team_20170125-1/", "ORG000120", "北陸高等学校", "【経歴】", "", "", None),
    ("P000483", "https://b-corsairs.com/news/team_20170125-1/", "ORG000166", "筑波大学", "【経歴】", "", "", None),
    ("P000495", "https://veltex.co.jp/news/detail/id=51569", "ORG000148", "近畿大学", "◼︎出身校", "", "", None),
    ("P000553", "https://go-seahorses.jp/team/players/detail/id=20611?PlayerID=51000320", "ORG000506", "Haines City HS", "出身校", "", "", None),
    ("P000553", VOL + "19938", "ORG000507", "2025-26 Northeast Mississippi Community College", "経歴", "2025", "2026", None),
]


def raw_rows() -> dict[str, dict[str, str]]:
    rows = {}
    for line in RAW.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        bid, name, pub, url, text = line.split("|", 4)
        rows[url] = {"bid": bid, "name": name, "publisher": pub, "text": text}
    return rows


def main() -> None:
    raw = raw_rows()
    m_people = {r["person_id"]: r["name"] for r in read_csv(ROOT / "data/master/person.csv")}
    m_orgs = {r["organization_id"]: r["name"] for r in read_csv(ROOT / "data/master/organization.csv")}
    m_careers = read_csv(ROOT / "data/master/career.csv")
    used_orgs, used_careers, cand_careers = set(m_orgs), {r["career_id"] for r in m_careers}, []
    for path in (ROOT / "data/candidate").rglob("organization_candidates.csv"):
        if OUT not in path.parents:
            used_orgs |= {r["organization_id"] for r in read_csv(path)}
    for path in (ROOT / "data/candidate").rglob("career_candidates.csv"):
        if OUT not in path.parents:
            rows = read_csv(path)
            used_careers |= {r["career_id"] for r in rows}
            cand_careers += rows
    errors = []
    if set(NEW_ORGS) & used_orgs or set(NEW_ORGS.values()) & set(m_orgs.values()):
        errors.append("new Organization ID/name already used")
    src_ids, sources, careers, evidence, decisions, issues, orgs = {}, [], [], [], [], [], {}
    for i, (pid, url, oid, text, where, start, end, issue) in enumerate(T):
        r = raw.get(url)
        if not r:
            errors.append(f"{pid}: URL not in raw")
            continue
        if r["name"].replace(" ", "") != m_people[pid].replace(" ", ""):
            errors.append(f"{pid}: name differs")
        if text not in r["text"]:
            errors.append(f"{pid}: '{text}' not in raw")
        orgs[oid] = NEW_ORGS.get(oid) or m_orgs.get(oid)
        if not orgs[oid]:
            errors.append(f"{oid} unknown")
        if any(c["person_id"] == pid and c["organization_id"] == oid for c in m_careers + cand_careers):
            errors.append(f"{pid}: Career to {oid} exists")
        if url not in src_ids:
            src_ids[url] = f"{P}S{len(src_ids) + 1:04d}"
            pub, _, title = r["publisher"].partition("（")
            sources.append({"source_id": src_ids[url], "title": f"{r['name']} {title.rstrip('）') or '選手プロフィール'}",
                            "publisher": pub, "url": url, "accessed_at": CHECKED})
        sid, cid = src_ids[url], f"C{FIRST_CAREER + i:06d}"
        careers.append({"career_id": cid, "person_id": pid, "organization_id": oid, "role": "Player", "start": start, "end": end})
        ident = "ページの生年月日がB.LEAGUE公式プロフィールと一致" if "生年月日" in r["text"] else "クラブ公式の発表"
        fields = [("organization_id", oid), ("role", "Player")] + ([("start", start), ("end", end)] if start else [])
        for f, v in fields:
            evidence.append({"record_id": f"{P}E{len(evidence) + 1:04d}", "entity_type": "Career", "entity_id": cid, "field_name": f,
                             "candidate_value": v, "source_id": sid, "source_locator": f"{where}：{text}",
                             "evidence_summary": f"クラブ公式の資料で出身校を確認（{ident}）" + ("。期間はページの年度表記のとおり" if start else ""),
                             "assessment": "SUPPORTED", "checked_at": CHECKED, "issue_note": ""})
        held = "" if start else "start|end"
        decisions.append({"decision_id": f"{P}D{len(decisions) + 1:04d}", "entity_type": "Career", "entity_id": cid,
                          "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "organization_id|role" + ("|start|end" if start else ""),
                          "held_fields": held, "reason": "クラブ公式の資料で出身校を確認" + ("" if start else "、在学期間は未確認"), "reviewed_at": CHECKED})
        if issue:
            issues.append({"issue_id": f"{P}I{len(issues) + 1:04d}", "person_id": pid, "related_id": cid, "issue_type": issue[0],
                           "status": "HOLD", "description": f"{m_people[pid]}：{issue[1]}", "next_check": "学校・大会の公式資料で確認"})
    if {c["career_id"] for c in careers} & used_careers:
        errors.append("Career ID already used")
    if errors:
        raise SystemExit("; ".join(errors))
    write_csv(OUT / "person_candidates.csv", ["person_id", "name"], [])
    write_csv(OUT / "organization_candidates.csv", ["organization_id", "name"], [{"organization_id": o, "name": n} for o, n in sorted(orgs.items())])
    write_csv(OUT / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], sources)
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
    write_csv(OUT / "qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields",
                                         "reason", "reviewed_at"], decisions)
    print(f"wave_06: persons={len({c['person_id'] for c in careers})} careers={len(careers)} orgs={len(orgs)} (new {len(NEW_ORGS)}) "
          f"evidence={len(evidence)} sources={len(sources)} issues={len(issues)}")


if __name__ == "__main__":
    main()
