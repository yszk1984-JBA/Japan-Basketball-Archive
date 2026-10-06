#!/usr/bin/env python3
"""Build batch_032 Wave 6: 出身高校 for B.PREMIER players, CANDIDATE.

Yuichi (2026-10-06): 「1から」 -- start the research plan with item 1,
filling the high school of 2026-27 B.PREMIER players who have no high-school
Career in MASTER.

Raw values: data/raw/research/club_profiles_highschool_2026-10-06.txt. Each
value was read in the browser from the page itself (club official player
pages and signing announcements, JBA's U19 roster, one media article).
Identity: the birth date and birthplace on each page match the B.LEAGUE
profile (or the page carries the same PlayerID).

- One Career per school, period blank (same rule as batch_032).
- The target for each person is fixed below together with the exact text on
  the page; the script checks that the text is in the raw file.
- Not included here (see README): 佐藤涼成 (batch_003 already holds
  unapproved school Careers C000046・C000213), 水戸健史 (registered in
  batch_007; media source only), and the persons for whom no school was found.
- Middle schools printed on some pages are not recorded (roadmap item 3).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_032/wave_06"
RAW = ROOT / "data/raw/research/club_profiles_highschool_2026-10-06.txt"
CHECKED = "2026-10-06"
P = "B32W6"
FIRST_CAREER = 2705
NEW_ORGS = {"ORG000484": "茨城県立水戸第一高等学校"}
OFFICIAL, MEDIA = "official", "media"

# (person, URL in raw file, organization, text on the page, locator label, kind, issue (type, note) or None)
TARGETS = [
    ("P000321", "https://www.storks.jp/player_lp/ryuya_kaneda/?PlayerID=5100000031", "ORG000264", "大阪学院高校",
     "選手特設ページ Q&A > 出身校（高校）は？", OFFICIAL,
     ("SCHOOL_NAME_ABBREVIATED", "「大阪学院高校」と略記。大阪学院大学高等学校（既存ORG000264）として登録した。")),
    ("P000322", "https://www.storks.jp/player_lp/keigo_kimura/?PlayerID=5100000066", "ORG000209", "八王子学園八王子高等学校",
     "選手特設ページ Q&A > 出身校（高校）は？", OFFICIAL, None),
    ("P000323", "https://www.storks.jp/player_lp/shuto_terazono/", "ORG000194", "延岡学園高等学校",
     "選手特設ページ Q&A > 出身校（高校）は？", OFFICIAL, None),
    ("P000324", "https://www.storks.jp/player_lp/noriaki_dohara/", "ORG000356", "神戸市立科学技術高等学校",
     "選手特設ページ Q&A > 出身校（高校）は？", OFFICIAL,
     ("ORG_NAME_HISTORY", "ページの表記は「神戸市立科学技術高等学校」。batch_032の登録ルール（御影工業高校が統合されて神戸市立科学技術高校になったため1つのOrganizationとする）により、既存の御影工業高等学校（ORG000356）として登録した。在学時の校名は科学技術高校。")),
    ("P000325", "https://www.storks.jp/player_lp/michiya_nakajima/", "ORG000477", "育英高等学校",
     "選手特設ページ Q&A > 出身校（高校）は？", OFFICIAL, None),
    ("P000326", "https://www.levanga.com/news/detail/id=12673", "ORG000218", "報徳学園高等学校",
     "特別指定選手契約合意のお知らせ > 【出身校】", OFFICIAL, None),
    ("P000327", "https://www.levanga.com/news/detail/id=14322", "ORG000216", "正智深谷高校",
     "特別指定選手契約合意のお知らせ > プロフィール（学歴）", OFFICIAL, None),
    ("P000333", "https://hiroshimadragonflies.com/news/detail/id=24484", "ORG000161", "桜丘高等学校",
     "契約合意（新規）のお知らせ > ●出身校", OFFICIAL, None),
    ("P000338", "https://www.ibarakirobots.win/news/20230902_01_team/", "ORG000401", "如水館高等学校",
     "特別指定選手登録のご報告 > ■出身校", OFFICIAL, None),
    ("P000341", "https://kawasaki-bravethunders.com/news/detail/id=19962", "ORG000341", "佐賀東高校",
     "加入のお知らせ > 略歴", OFFICIAL, None),
    ("P000342", "https://bbspirits.com/bleague/b19031901/", "ORG000194", "延岡学園高校",
     "記事本文（2019-03-19）", MEDIA,
     ("SCHOOL_NONOFFICIAL_SOURCE", "出身高校は専門メディア（バスケットボールスピリッツ）の記事本文の記述のみで確認。クラブ・リーグの公式資料では未確認。")),
    ("P000344", "https://www.bigbulls.jp/news/detail/id=19120", "ORG000127", "福岡大学附属大濠高校",
     "特別指定 新加入のお知らせ > ■経歴", OFFICIAL, None),
    ("P000345", "https://u18.japanbasketball.jp/2021u19men/", "ORG000147", "仙台大学附属明成高等学校3年",
     "2021年度 男子U19日本代表 選手一覧 > 所属", OFFICIAL,
     ("ORG_NAME_HISTORY", "JBAの表記は「仙台大学附属明成高等学校」（2021年度、3年）。既存の明成高等学校（ORG000147）は同じ学校の改称前の名称のため、1つのOrganizationとして登録した。")),
    ("P000376", "https://www.ibarakirobots.win/news/19088/", "ORG000484", "茨城県立水戸第一高等学校",
     "特別指定選手契約合意のご報告 > ■出身校［所属チーム］", OFFICIAL, None),
    ("P000378", "https://www.velca.jp/news/detail/id=48040", "ORG000213", "中部大学第一高校",
     "特別指定選手として新加入のお知らせ > 出身校", OFFICIAL, None),
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
    used_orgs = set(m_orgs)
    used_careers = {r["career_id"] for r in read_csv(ROOT / "data/master/career.csv")}
    cand_careers = []
    for path in (ROOT / "data/candidate").rglob("organization_candidates.csv"):
        if OUT not in path.parents:
            used_orgs |= {r["organization_id"] for r in read_csv(path)}
    for path in (ROOT / "data/candidate").rglob("career_candidates.csv"):
        if OUT not in path.parents:
            rows = read_csv(path)
            used_careers |= {r["career_id"] for r in rows}
            cand_careers += rows
    m_careers = read_csv(ROOT / "data/master/career.csv")
    errors = []

    sources, careers, evidence, decisions, issues, orgs = [], [], [], [], [], {}
    for i, (pid, url, oid, text, where, kind, issue) in enumerate(TARGETS, 1):
        r = raw.get(url)
        if not r:
            errors.append(f"{pid}: URL not in raw file")
            continue
        if r["name"].replace(" ", "") != m_people[pid].replace(" ", ""):
            errors.append(f"{pid}: name differs ({r['name']} / {m_people[pid]})")
        if text not in r["text"]:
            errors.append(f"{pid}: '{text}' not in raw text")
        if oid in NEW_ORGS:
            if oid in used_orgs or NEW_ORGS[oid] in m_orgs.values():
                errors.append(f"{oid}: already used")
            orgs[oid] = NEW_ORGS[oid]
        elif oid in m_orgs:
            orgs[oid] = m_orgs[oid]
        else:
            errors.append(f"{pid}: unknown Organization {oid}")
            continue
        if any(c["person_id"] == pid and c["organization_id"] == oid for c in m_careers + cand_careers):
            errors.append(f"{pid}: Career to {oid} already exists")
        sid, cid = f"{P}S{i:04d}", f"C{FIRST_CAREER + i - 1:06d}"
        title = r["publisher"].split("（", 1)[1].rstrip("）") if "（" in r["publisher"] else "選手プロフィール"
        publisher = r["publisher"].split("（", 1)[0]
        sources.append({"source_id": sid, "title": f"{r['name']} {title}", "publisher": publisher, "url": url, "accessed_at": CHECKED})
        careers.append({"career_id": cid, "person_id": pid, "organization_id": oid, "role": "Player", "start": "", "end": ""})
        if "生年月日" in r["text"] or "/7/10" in r["text"]:
            ident = "ページの生年月日がB.LEAGUE公式プロフィールと一致"
        elif "player_lp" in url:
            ident = "現所属クラブ公式の選手特設ページ"
        else:
            ident = "記事の出身地（福岡県）がB.LEAGUE公式プロフィール、進学先（東海大）がクラブ公式の紹介文と一致"
        summary = (f"クラブ・競技団体の公式ページで出身高校を確認（{ident}）"
                   if kind == OFFICIAL else f"専門メディアの記事本文で出身高校を確認（公式資料では未確認、{ident}）")
        evidence.append({"record_id": f"{P}E{len(evidence) + 1:04d}", "entity_type": "Career", "entity_id": cid,
                         "field_name": "organization_id", "candidate_value": oid, "source_id": sid,
                         "source_locator": f"{where}：{text}", "evidence_summary": summary, "assessment": "SUPPORTED",
                         "checked_at": CHECKED, "issue_note": ""})
        decisions.append({"decision_id": f"{P}D{len(decisions) + 1:04d}", "entity_type": "Career", "entity_id": cid,
                          "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "organization_id|role", "held_fields": "start|end",
                          "reason": "出典で出身高校を確認、在学期間は未確認", "reviewed_at": CHECKED})
        if issue:
            issues.append({"issue_id": f"{P}I{len(issues) + 1:04d}", "person_id": pid, "related_id": cid, "issue_type": issue[0],
                           "status": "HOLD", "description": f"{m_people[pid]}：{issue[1]}",
                           "next_check": "大会公式の選手名簿（インターハイ・ウインターカップ）やJBA公式資料で確認"})
    if {c["career_id"] for c in careers} & used_careers:
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
    print(f"wave_06: careers={len(careers)} orgs={len(orgs)} (new {len(NEW_ORGS)}) evidence={len(evidence)} issues={len(issues)}")


if __name__ == "__main__":
    main()
