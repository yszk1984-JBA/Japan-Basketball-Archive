#!/usr/bin/env python3
"""Build batch_035 Wave 1: pre-B.LEAGUE (and early overseas) careers of Japan
national-team players, CANDIDATE.

Yuichi (2026-10-24): 「比江島慎の経歴が最新になってない気がします／有名選手は
当然ながら、是非最新になっているのかリサーチして欲しい」. He chose
- target: 日本代表経験者 (the 26 MASTER persons on the 2006/2019/2023 World Cup
  and 2020/2024 Olympic rosters), and
- sources for careers before B.LEAGUE (2016-17): 「公式系＋Wikipedia等（Tier 2）」.

The B.LEAGUE-era careers of all 26 already match the official B.LEAGUE club
history; what is missing is the NBL/JBL/bj era (and a few overseas clubs
before 2013). The values come from the infobox of each Japanese Wikipedia
article, read through the Wikipedia API in the browser on 2026-10-24
(raw: data/raw/research/wikipedia_national_team_infobox_2026-10-24.md, with
the oldid of every revision used). All of it is Tier 2 (non-official).

Rules
- A club that continued into B.LEAGUE is the same Organization (current
  registered name), as the Wikipedia link target shows (e.g. 「アイシン
  シーホース三河」→ シーホース三河). The pre-B part is a separate Career that
  ends in 2016; the official B.LEAGUE-era Career is not touched.
- Period = the infobox years (start year of the first season, end year of
  the last season). A single year (「2010」「2015」) does not tell the season,
  so the period is held.
- The 26 persons come from several batches, so -- as with batch_031 and
  batch_034 -- this is one dedicated batch.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_035/wave_01"
CHECKED = "2026-10-24"
P = "B35W1"
WIKI = "https://ja.wikipedia.org/w/index.php?title={}&oldid={}"
FIRST_CAREER = 2782
FIRST_ORG = 508

# person -> (Wikipedia title (URL-encoded), oldid)
PAGES = {
    "P000461": ("五十嵐圭", "%E4%BA%94%E5%8D%81%E5%B5%90%E5%9C%AD", "107648597"),
    "P000135": ("竹内公輔", "%E7%AB%B9%E5%86%85%E5%85%AC%E8%BC%94", "107658290"),
    "P000096": ("竹内譲次", "%E7%AB%B9%E5%86%85%E8%AD%B2%E6%AC%A1", "108407442"),
    "P000098": ("安藤誓哉", "%E5%AE%89%E8%97%A4%E8%AA%93%E5%93%89", "111412195"),
    "P000084": ("比江島慎", "%E6%AF%94%E6%B1%9F%E5%B3%B6%E6%85%8E", "110593762"),
    "P000176": ("篠山竜青", "%E7%AF%A0%E5%B1%B1%E7%AB%9C%E9%9D%92", "111338405"),
    "P000083": ("富樫勇樹", "%E5%AF%8C%E6%A8%AB%E5%8B%87%E6%A8%B9", "111268455"),
    "P000090": ("金丸晃輔", "%E9%87%91%E4%B8%B8%E6%99%83%E8%BC%94", "109754371"),
    "P000289": ("ギャビン・エドワーズ", "%E3%82%AE%E3%83%A3%E3%83%93%E3%83%B3%E3%83%BB%E3%82%A8%E3%83%89%E3%83%AF%E3%83%BC%E3%82%BA", "110740675"),
    "P000215": ("張本天傑", "%E5%BC%B5%E6%9C%AC%E5%A4%A9%E5%82%91", "107515068"),
    "P000297": ("原修太", "%E5%8E%9F%E4%BF%AE%E5%A4%AA", "111152930"),
}
# new Organizations: key -> name (Japanese Wikipedia article title; label as shown when only an English link)
NEW_ORGS = {
    "panasonic": "パナソニックトライアンズ",
    "halifax": "ハリファックス・レインメン",
    "meralco": "メラルコ・ボルツ",
    "anyang": "安養正官庄レッドブースターズ",
    "khimik": "Khimik OPZ",
    "grandrapids": "グランドラピッズ・ゴールド",
    "peristeri": "ペリステリBC",
    "kl": "ウェストポーツKLドラゴンズ",
}
# person, org (MASTER id or NEW_ORGS key), start, end, infobox line as read, note
CAREERS = [
    ("P000461", "ORG000114", "2003", "2009", "|所属年1=2003-2009 / |所属1=[[サンロッカーズ渋谷|日立]]", "リンク先＝サンロッカーズ渋谷（現・東京サンロッカーズ）"),
    ("P000461", "ORG000109", "2009", "2010", "|所属年2=2009-2010 / |所属2=[[アルバルク東京|トヨタ]]", ""),
    ("P000461", "ORG000054", "2010", "2016", "|所属年3=2010-2016 / |所属3=[[名古屋ダイヤモンドドルフィンズ|三菱電機名古屋]]", ""),
    ("P000135", "ORG000130", "2007", "2011", "| 所属年1 = 2007-2011 | 所属1 = [[シーホース三河|アイシンシーホース]]", ""),
    ("P000135", "ORG000109", "2011", "2014", "| 所属年2 = 2011-2014 | 所属2 = [[アルバルク東京|トヨタ自動車アルバルク]]", ""),
    ("P000135", "ORG000110", "2014", "2016", "| 所属年3 = 2014-2016 | 所属3 = [[広島ドラゴンフライズ]]", "B.LEAGUE期（宇都宮 2016〜）の前"),
    ("P000096", "ORG000114", "2007", "2016", "|所属年1= 2007-2016 / |所属1=[[サンロッカーズ渋谷|日立サンロッカーズ東京]]", ""),
    ("P000098", "halifax", "2014", "2015", "|所属1=[[ハリファックス・レインメン]] / |所属年1=2014-2015", "海外（カナダNBL）"),
    ("P000098", "meralco", "", "", "|所属2=[[メラルコ・ボルツ]] / |所属年2=2015", "海外（フィリピンPBA）。年は「2015」のみでシーズンが分からないため期間は保留"),
    ("P000098", "ORG000047", "2015", "2016", "|所属3=[[宇都宮ブレックス|リンク栃木ブレックス]] / |所属年3=2015-2016", ""),
    ("P000084", "ORG000130", "2013", "2016", "|所属年1 = 2013-2018 / |所属1 = [[シーホース三河|アイシン シーホース三河<br/>シーホース三河]]", "2016〜2018はB.LEAGUE公式どおり既存Career（C001752）。開幕前の部分のみ"),
    ("P000176", "ORG000122", "2011", "2016", "|所属1=[[川崎ブレイブサンダース|東芝ブレイブサンダース<br/>…<br/>川崎ブレイブサンダース]] / |所属年1=2011-", "2016〜は既存Career（B.LEAGUE公式）。開幕前の部分のみ"),
    ("P000083", "ORG000118", "2015", "2016", "| 所属3 = [[千葉ジェッツふなばし]] / | 所属年3 = 2015-", "2016〜は既存Career（B.LEAGUE公式）。開幕前の部分のみ"),
    ("P000090", "panasonic", "2011", "2013", "|所属1=[[パナソニックトライアンズ]]|所属年1=2011-2013", "チームは2013年に休部"),
    ("P000090", "ORG000130", "2013", "2016", "|所属2=[[シーホース三河|アイシン シーホース三河<br/>シーホース三河]]|所属年2=2013-2021", "2016〜2021は既存Career（B.LEAGUE公式）。開幕前の部分のみ"),
    ("P000289", "anyang", "", "", "|所属年1=2010 / |所属1=[[安養正官庄レッドブースターズ|安養KGC人参公社]]", "海外（韓国KBL）。年は「2010」のみ、期間は保留"),
    ("P000289", "khimik", "", "", "|所属年2=2010 / |所属2=[[:en:BC Khimik|Khimik OPZ]]", "海外（ウクライナ）。年は「2010」のみ、期間は保留"),
    ("P000289", "grandrapids", "2010", "2011", "|所属年3=2010-2011 / |所属3=[[グランドラピッズ・ゴールド|スプリングフィールド・アーマー]]", "海外（NBA Dリーグ）。在籍当時はスプリングフィールド・アーマー、リンク先は移転後の現チーム"),
    ("P000289", "peristeri", "2011", "2012", "|所属年4=2011-2012 / |所属4=[[:en:Peristeri B.C.|ペリステリBC]]", "海外（ギリシャ）"),
    ("P000289", "kl", "2012", "2013", "|所属年5=2012-2013 / |所属5=[[:en:Kuala Lumpur Dragons|ウェストポーツKLドラゴンズ]]", "海外（ASEANバスケットボールリーグ）"),
    ("P000289", "ORG000130", "2013", "2016", "|所属年6=2013-2017 / |所属6=[[シーホース三河|アイシン シーホース三河<br />シーホース三河]]", "2016〜2017は既存Career（B.LEAGUE公式）。開幕前の部分のみ"),
    ("P000215", "ORG000109", "2014", "2016", "|所属1=[[アルバルク東京|トヨタ自動車アルバルク東京]] / |所属年1=2014-2016", ""),
    ("P000297", "ORG000118", "2015", "2016", "|所属1=[[千葉ジェッツふなばし]] / |所属年1=2015-", "2016〜は既存Career（B.LEAGUE公式）。開幕前の部分のみ"),
]
SCHOOLS = [  # person, org, infobox line
    ("P000461", "ORG000120", "|高校=[[北陸中学校・高等学校|北陸高校]]"),
]
# Differences between Wikipedia and the official MASTER values (MASTER kept; recorded only)
DIFFS = [
    ("P000083", "富樫勇樹の秋田ノーザンハピネッツの開始年：Masterは2012（既存の出典）、Wikipediaは2013-2014。Masterを変更していない。"),
    ("P000329", "井上宗一郎の東京サンロッカーズ：MasterはB.LEAGUE公式の所属履歴で2021〜2023、Wikipediaは2022-2023。公式を優先しMasterを変更していない。"),
    ("P000302", "テーブス海の宇都宮ブレックス：MasterはB.LEAGUE公式の所属履歴で2019〜2022、Wikipediaは2020-2022。公式を優先しMasterを変更していない。"),
    ("P000064", "河村勇輝：Wikipediaには「2026 →ウィンディシティ・ブルズ」とあるが、NBA公式（Gリーグの2026-27名簿）は未公開。Batch 034のHOLD（B34W1I0001）のまま、登録していない。"),
]


def main() -> None:
    m_people = {r["person_id"]: r["name"] for r in read_csv(ROOT / "data/master/person.csv")}
    m_orgs = {r["organization_id"]: r["name"] for r in read_csv(ROOT / "data/master/organization.csv")}
    m_careers = read_csv(ROOT / "data/master/career.csv")
    all_orgs = dict(m_orgs)
    for path in (ROOT / "data/candidate").rglob("organization_candidates.csv"):
        if OUT not in path.parents:
            for r in read_csv(path):
                all_orgs.setdefault(r["organization_id"], r["name"])
    used_careers = {r["career_id"] for r in m_careers}
    for path in (ROOT / "data/candidate").rglob("career_candidates.csv"):
        if OUT not in path.parents:
            used_careers |= {r["career_id"] for r in read_csv(path)}
    errors = []
    names = set(all_orgs.values())
    new_ids = {}
    for i, (key, name) in enumerate(NEW_ORGS.items()):
        oid = f"ORG{FIRST_ORG + i:06d}"
        if oid in all_orgs:
            errors.append(f"{oid}: already used")
        if name in names:
            errors.append(f"{name}: an Organization with this name exists")
        new_ids[key] = oid

    sources, evidence, decisions, issues, careers, orgs = {}, [], [], [], [], {}

    def source(pid: str) -> str:
        if pid not in sources:
            title, enc, oldid = PAGES[pid]
            sources[pid] = {"source_id": f"{P}S{len(sources) + 1:04d}", "title": f"{title}（Wikipedia日本語版、版 {oldid}）",
                            "publisher": "Wikipedia日本語版（公式以外）", "url": WIKI.format(enc, oldid), "accessed_at": CHECKED}
        return sources[pid]["source_id"]

    def ev(cid: str, field: str, value: str, sid: str, loc: str, summary: str) -> None:
        evidence.append({"record_id": f"{P}E{len(evidence) + 1:04d}", "entity_type": "Career", "entity_id": cid, "field_name": field,
                         "candidate_value": value, "source_id": sid, "source_locator": f"基本情報欄 > {loc}", "evidence_summary": summary,
                         "assessment": "SUPPORTED", "checked_at": CHECKED, "issue_note": "公式以外の出典（Wikipedia）。Tier 2"})

    rows = [(pid, org, s, e, loc, note) for pid, org, s, e, loc, note in CAREERS] + \
           [(pid, org, "", "", loc, "school") for pid, org, loc in SCHOOLS]
    for n, (pid, org, start, end, loc, note) in enumerate(rows):
        if pid not in m_people:
            errors.append(f"{pid}: not in MASTER")
            continue
        oid = new_ids.get(org, org)
        oname = NEW_ORGS.get(org) or m_orgs.get(oid)
        if not oname:
            errors.append(f"{org}: unknown organization")
            continue
        orgs[oid] = oname
        cid = f"C{FIRST_CAREER + n:06d}"
        if cid in used_careers:
            errors.append(f"{cid}: already used")
        for c in m_careers:  # overlap check with the same organization
            if c["person_id"] == pid and c["organization_id"] == oid and start and c["start"] and c["start"] < (end or "9999") and (c["end"] or "9999") > start:
                errors.append(f"{pid} {oname}: overlaps MASTER {c['career_id']}")
            if note == "school" and c["person_id"] == pid and c["organization_id"] == oid:
                errors.append(f"{pid}: school already in MASTER")
        careers.append({"career_id": cid, "person_id": pid, "organization_id": oid, "role": "Player", "start": start, "end": end})
        sid = source(pid)
        school = note == "school"
        ev(cid, "organization_id", oid, sid, loc, f"Wikipedia日本語版の基本情報欄で{'出身高校' if school else '所属'}を確認" +
           ("（リンク先の記事＝現在のクラブ）" if "[[" in loc and "|" in loc.split("[[", 1)[1] and not school else ""))
        ev(cid, "role", "Player", sid, loc, "選手としての所属")
        fields, held = "organization_id|role", "start|end"
        if start:
            ev(cid, "start", start, sid, loc, "基本情報欄の所属年の開始年")
            ev(cid, "end", end, sid, loc, "基本情報欄の所属年の終了年（B.LEAGUE開幕前の部分は2016で区切る）" if end == "2016" else "基本情報欄の所属年の終了年")
            fields, held = "organization_id|role|start|end", ""
        decisions.append({"decision_id": f"{P}D{len(decisions) + 1:04d}", "entity_type": "Career", "entity_id": cid,
                          "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": fields, "held_fields": held,
                          "reason": "Wikipedia日本語版の基本情報欄（公式以外、Tier 2）" + ("" if start else "。期間はシーズンが分からないため保留"),
                          "reviewed_at": CHECKED})
        if note and not school:
            issues.append({"issue_id": f"{P}I{len(issues) + 1:04d}", "person_id": pid, "related_id": cid,
                           "issue_type": "PRE_BLEAGUE_NON_OFFICIAL" if start else "PERIOD_UNCLEAR", "status": "HOLD",
                           "description": f"{m_people[pid]}・{oname}：{note}。出典はWikipediaのみ（公式以外）。",
                           "next_check": "クラブ公式の契約発表・当時のリーグ公式記録で確認"})
    for pid, text in DIFFS:
        issues.append({"issue_id": f"{P}I{len(issues) + 1:04d}", "person_id": pid, "related_id": pid, "issue_type": "SOURCE_DIFFERENCE",
                       "status": "HOLD", "description": text, "next_check": "公式資料で確認"})
    if errors:
        raise SystemExit("; ".join(errors))
    write_csv(OUT / "person_candidates.csv", ["person_id", "name"], [])
    write_csv(OUT / "organization_candidates.csv", ["organization_id", "name"],
              [{"organization_id": o, "name": n} for o, n in sorted(orgs.items())])
    write_csv(OUT / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], list(sources.values()))
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
    write_csv(OUT / "qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields",
                                         "reason", "reviewed_at"], decisions)
    print(f"batch_035 wave_01: careers={len(careers)} orgs={len(orgs)} (new {len(NEW_ORGS)}) persons={len({c['person_id'] for c in careers})} "
          f"evidence={len(evidence)} issues={len(issues)}")


if __name__ == "__main__":
    main()
