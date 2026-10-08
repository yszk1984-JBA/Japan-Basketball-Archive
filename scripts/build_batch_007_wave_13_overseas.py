#!/usr/bin/env python3
"""Build batch_007 Wave 13: overseas careers of 八村塁・馬場雄大・比江島慎, CANDIDATE.

Yuichi (2026-10-08): 選手リサーチの続きとして「海外経歴の続き（推奨）」を選択.
All three were registered in batch_007 (wave_01, wave_07, wave_09).

Raw values: data/raw/research/overseas_hachimura_baba_hiejima_2026-10-08.md
(stats.nba.com NBA / G League, gozags.com rosters, nbl.com.au news,
utsunomiyabrex.com news), read in the browser.

- 八村塁 (P000104) is not in MASTER (left as a candidate in Sprint 009). This
  wave proposes the person again with NBA official data and replaces wave_07's
  Careers C000356-C000358 (Wikipedia / news, no periods) with Careers carrying
  official evidence and periods (wave_07 Careers -> REJECT_CANDIDATE).
- Season rule: start = first season's start year, end = last season's end year,
  no end while on a 2026-27 roster. NBL seasons (NBL21 = 2020-21) follow it.
- 馬場's G League stints were not NBA assignments (no NBA contract,
  NBA_FLAG=N), so each Texas Legends stint is its own Career.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_007/wave_13"
CHECKED = "2026-10-08"
P = "B7W13"
R, B, H = "P000104", "P000107", "P000084"
NBA = "NBA.com（stats.nba.com）"

SOURCES = [
    ("S0001", "Rui Hachimura 選手情報", NBA, "https://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID=1629060", CHECKED),
    ("S0002", "Rui Hachimura 通算成績（レギュラーシーズン・大学）", NBA,
     "https://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=Totals&PlayerID=1629060", CHECKED),
    ("S0003", "Washington Wizards ロスター 2019-20", NBA,
     "https://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2019-20&TeamID=1610612764", CHECKED),
    ("S0004", "Los Angeles Lakers ロスター 2025-26", NBA,
     "https://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2025-26&TeamID=1610612747", CHECKED),
    ("S0005", "LA Clippers ロスター 2026-27", NBA,
     "https://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2026-27&TeamID=1610612746", CHECKED),
    ("S0006", "Gonzaga Men's Basketball Roster 2016-17〜2018-19", "Gonzaga University Athletics（大学公式）",
     "https://gozags.com/sports/mens-basketball/roster/2018-19", CHECKED),
    ("S0007", "八村塁", "Wikipedia日本語版", "https://ja.wikipedia.org/wiki/八村塁", "2026-09-23"),
    ("S0008", "Yudai Baba NBA Gリーグ 選手情報・通算成績・試合記録", NBA,
     "https://stats.nba.com/stats/playergamelog?LeagueID=20&PlayerID=1629819", CHECKED),
    ("S0009", "NBA Gリーグ フランチャイズ履歴（Texas Legends）", NBA, "https://stats.nba.com/stats/franchisehistory?LeagueID=20", CHECKED),
    ("S0010", "Melbourne Sign Yudai Baba for Remainder of NBL22（2022-03-24）", "NBL（オーストラリア）公式",
     "https://www.nbl.com.au/news/melbourne-sign-yudai-baba-for-remainder-of-nbl22", CHECKED),
    ("S0011", "比江島慎選手、ブリスベン・ブレッツ移籍決定のご報告（2018-08-02）", "宇都宮ブレックス（クラブ公式）",
     "https://www.utsunomiyabrex.com/news/detail/id=8544", CHECKED),
    ("S0012", "比江島慎 選手プロフィール（クラブ所属履歴）", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=8589", "2026-09-29"),
]
ORGS = [("ORG000493", "ワシントン・ウィザーズ"), ("ORG000494", "ロサンゼルス・レイカーズ"),
        ("ORG000495", "メルボルン・ユナイテッド"), ("ORG000496", "ブリスベン・ブレッツ")]
EXISTING_ORGS = {"ORG000140": "ロサンゼルス・クリッパーズ", "ORG000138": "テキサス・レジェンズ",
                 "ORG000147": "明成高等学校"}
CANDIDATE_ORGS = {"ORG000158": "ゴンザガ大学"}  # batch_007 wave_07, not yet in MASTER
TEX, MEL = "ORG000138", "ORG000495"

CAREERS = [
    ("C002731", R, "ORG000147", "", ""),
    ("C002732", R, "ORG000158", "2016", "2019"),
    ("C002733", R, "ORG000493", "2019", "2023"),
    ("C002734", R, "ORG000494", "2022", "2026"),
    ("C002735", R, "ORG000140", "2026", ""),
    ("C002736", B, TEX, "2019", "2020"),
    ("C002737", B, MEL, "2020", "2021"),
    ("C002738", B, TEX, "2021", "2022"),
    ("C002739", B, MEL, "2021", "2022"),
    ("C002740", B, TEX, "2022", "2023"),
    ("C002741", H, "ORG000496", "2018", "2019"),
]
EVIDENCE = [
    ("Person", R, "name", "八村塁", "S0007", "冒頭", "Wikipediaで日本語の氏名を確認（公式の日本語表記は未確認）"),
    ("Person", R, "date_of_birth", "1998-02-08", "S0001", "BIRTHDATE 1998-02-08T00:00:00 / DISPLAY_FIRST_LAST Rui Hachimura / COUNTRY Japan",
     "NBA公式の選手情報で生年月日を確認（Wikipediaの1998年2月8日と一致）"),
    ("Career", "C002731", "organization_id", "ORG000147", "S0006", "2017-18・2018-19：Toyama, Japan / Meisei", "ゴンザガ大学公式ロスターの出身校欄（Meisei）"),
    ("Career", "C002731", "role", "Player", "S0007", "経歴 > 出身高校：明成高等学校（宮城県）", "高校の選手として在籍"),
    ("Career", "C002732", "organization_id", "ORG000158", "S0006", "21 Rui Hachimura（2016-17 Fr.／2017-18 So.／2018-19 Jr.）", "大学公式の年度別ロスターで在籍を確認"),
    ("Career", "C002732", "organization_id", "ORG000158", "S0002", "SeasonTotalsCollegeSeason：2016-17〜2018-19 Gonzaga", "NBA公式の大学成績"),
    ("Career", "C002732", "role", "Player", "S0002", "GP 28・37・37", "選手として出場"),
    ("Career", "C002732", "start", "2016", "S0006", "2016-17 Fr.（2015-16は掲載なし）", "2016-17シーズンの開始年"),
    ("Career", "C002732", "end", "2019", "S0006", "2018-19 Jr.（2019-20は掲載なし）", "2018-19シーズンの終了年"),
    ("Career", "C002733", "organization_id", "ORG000493", "S0002", "2019-20〜2022-23 WAS（TEAM_ID 1610612764）", "NBA公式の通算成績でワシントン・ウィザーズ在籍を確認"),
    ("Career", "C002733", "organization_id", "ORG000493", "S0003", "PLAYER Rui Hachimura / NUM 8", "NBA公式の2019-20ロスターに掲載"),
    ("Career", "C002733", "role", "Player", "S0002", "GP 48・57・42・30", "選手として出場"),
    ("Career", "C002733", "start", "2019", "S0002", "SEASON_ID 2019-20 WAS／DRAFT_YEAR 2019（S0001）", "2019-20シーズンの開始年"),
    ("Career", "C002733", "end", "2023", "S0002", "WASの最後の行 SEASON_ID 2022-23（同シーズンにLALの行あり）", "2022-23シーズンの終了年"),
    ("Career", "C002734", "organization_id", "ORG000494", "S0002", "2022-23〜2025-26 LAL（TEAM_ID 1610612747）", "NBA公式の通算成績でロサンゼルス・レイカーズ在籍を確認"),
    ("Career", "C002734", "organization_id", "ORG000494", "S0004", "PLAYER Rui Hachimura / NUM 28 / HOW_ACQUIRED Traded from WAS on 01/23/23", "NBA公式の2025-26ロスターに掲載"),
    ("Career", "C002734", "role", "Player", "S0002", "GP 33・68・59・68", "選手として出場"),
    ("Career", "C002734", "start", "2022", "S0004", "HOW_ACQUIRED：Traded from WAS on 01/23/23（2022-23シーズン途中）", "2022-23シーズンの開始年"),
    ("Career", "C002734", "end", "2026", "S0002", "LALの最後の行 SEASON_ID 2025-26", "2025-26シーズンの終了年。2026-27はクリッパーズ（S0005）"),
    ("Career", "C002735", "organization_id", "ORG000140", "S0005", "PLAYER Rui Hachimura / NUM 28 / HOW_ACQUIRED Signed on 07/06/26", "NBA公式の2026-27ロスターに掲載"),
    ("Career", "C002735", "organization_id", "ORG000140", "S0001", "TEAM_NAME Clippers / JERSEY 28", "NBA公式の選手情報の現所属"),
    ("Career", "C002735", "role", "Player", "S0005", "PLAYER Rui Hachimura", "選手として掲載"),
    ("Career", "C002735", "start", "2026", "S0005", "HOW_ACQUIRED：Signed on 07/06/26", "2026-27シーズンから在籍"),
    ("Career", "C002736", "organization_id", TEX, "S0008", "2019-20 Regular Season：41試合すべてTEX", "NBA公式のGリーグ記録でテキサス・レジェンズ在籍を確認"),
    ("Career", "C002736", "organization_id", TEX, "S0009", "1612709918 Texas Legends（2010–2025）", "略称TEXのチーム名をフランチャイズ履歴で確認"),
    ("Career", "C002736", "role", "Player", "S0008", "GP 41", "選手として出場"),
    ("Career", "C002736", "start", "2019", "S0008", "2019-20（Nov 08, 2019 – Mar 08, 2020）", "2019-20シーズンの開始年"),
    ("Career", "C002736", "end", "2020", "S0008", "2019-20", "2019-20シーズンの終了年"),
    ("Career", "C002737", "organization_id", MEL, "S0010", "本文：NBL21 Championship guard Yudai Baba／Baba played 36 games for United last season", "NBL公式でNBL21のメルボルン・ユナイテッド在籍を確認"),
    ("Career", "C002737", "role", "Player", "S0010", "36 games", "選手として出場"),
    ("Career", "C002737", "start", "2020", "S0010", "NBL21（2020-21シーズン）", "NBL21シーズンの開始年"),
    ("Career", "C002737", "end", "2021", "S0010", "NBL21（last season、2022-03-24時点）", "NBL21シーズンの終了年"),
    ("Career", "C002738", "organization_id", TEX, "S0008", "2021-22 Showcase：8試合すべてTEX", "NBA公式のGリーグ記録で在籍を確認"),
    ("Career", "C002738", "organization_id", TEX, "S0010", "本文：following a stint in the NBA G League with the Texas Legends", "NBL公式の記事でも確認"),
    ("Career", "C002738", "role", "Player", "S0008", "8試合（Nov 05 – Nov 27, 2021）", "選手として出場"),
    ("Career", "C002738", "start", "2021", "S0008", "2021-22 Showcase", "2021-22シーズンの開始年"),
    ("Career", "C002738", "end", "2022", "S0008", "2021-22", "2021-22シーズンの終了年"),
    ("Career", "C002739", "organization_id", MEL, "S0010", "見出し：Melbourne Sign Yudai Baba for Remainder of NBL22", "NBL公式でNBL22のメルボルン・ユナイテッド再加入を確認"),
    ("Career", "C002739", "role", "Player", "S0010", "signed for the remainder of the NBL22 season", "選手として契約"),
    ("Career", "C002739", "start", "2021", "S0010", "NBL22（2021-22シーズン）、2022-03-24発表", "NBL22シーズンの開始年"),
    ("Career", "C002739", "end", "2022", "S0010", "for the remainder of the NBL22 season", "NBL22シーズンの終了年"),
    ("Career", "C002740", "organization_id", TEX, "S0008", "2022-23 Showcase 16試合＋Regular Season 23試合、すべてTEX", "NBA公式のGリーグ記録で在籍を確認"),
    ("Career", "C002740", "role", "Player", "S0008", "GP 23（レギュラーシーズン）", "選手として出場"),
    ("Career", "C002740", "start", "2022", "S0008", "2022-23（Nov 04, 2022 –）", "2022-23シーズンの開始年"),
    ("Career", "C002740", "end", "2023", "S0008", "2022-23（– Mar 06, 2023）、TO_YEAR 2022", "2022-23シーズンの終了年"),
    ("Career", "C002741", "organization_id", "ORG000496", "S0011", "本文：比江島慎選手がブリスベン・ブレッツ（NBL/オーストラリア）に移籍することが決定", "クラブ公式の発表で移籍を確認"),
    ("Career", "C002741", "role", "Player", "S0011", "見出し：比江島 慎 選手、ブリスベン・ブレッツ移籍決定", "選手として移籍"),
    ("Career", "C002741", "start", "2018", "S0011", "発表日 2018.08.02（NBLの2018-19シーズン）", "2018-19シーズンの開始年"),
    ("Career", "C002741", "end", "2019", "S0012", "クラブ所属履歴 >「2018-19 栃木」", "同じ2018-19シーズンに帰国してブレックスで所属（シーズン単位で終了年2019）"),
]
REJECT = ["C000356", "C000357", "C000358"]
ISSUES = [
    (R, R, "NAME_SOURCE", "八村塁の日本語の氏名はWikipediaでのみ確認（NBA公式は英語表記「Rui Hachimura」）。JBA公式サイトはブラウザで閲覧できなかった（「ただいまサイトを閲覧できません」）。",
     "JBA公式の日本代表名簿などで日本語表記を確認"),
    (R, "C002733", "SAME_SEASON_TWO_CLUBS", "2022-23シーズンはウィザーズ（30試合）とレイカーズ（33試合）の2クラブ（2023-01-23のトレード）。シーズン単位のルールで両方に同じ年を用いた。",
     "—"),
    (B, "C002738", "SAME_SEASON_TWO_CLUBS", "2021-22シーズンはテキサス・レジェンズ（Gリーグ、Showcase 8試合）とメルボルン・ユナイテッド（NBL22、2022-03に再加入）の2クラブ。",
     "—"),
    (B, B, "GLEAGUE_SEASON_TYPES", "Gリーグの出場はNBA公式で「Showcase」（2021-22 8試合、2022-23 16試合）と「Regular Season」に分かれて記録されている。2021-22はShowcaseのみ。",
     "—"),
    (H, "C002741", "SAME_SEASON_TWO_CLUBS", "2018-19シーズンはブリスベン・ブレッツ（NBL）と栃木ブレックス（B.LEAGUE）の2クラブ（シーズン途中の帰国）。ブリスベンでの試合数・退団日はNBL公式で未確認。",
     "NBL公式の記録で出場と退団時期を確認"),
]


def main() -> None:
    sources = [{"source_id": f"{P}{sid}", "title": t, "publisher": pub, "url": url, "accessed_at": acc} for sid, t, pub, url, acc in SOURCES]
    careers = [{"career_id": c, "person_id": p, "organization_id": o, "role": "Player", "start": s, "end": e} for c, p, o, s, e in CAREERS]
    evidence = [{"record_id": f"{P}E{i:04d}", "entity_type": et, "entity_id": eid, "field_name": f, "candidate_value": v,
                 "source_id": f"{P}{sid}", "source_locator": loc, "evidence_summary": summ, "assessment": "SUPPORTED",
                 "checked_at": CHECKED, "issue_note": ""} for i, (et, eid, f, v, sid, loc, summ) in enumerate(EVIDENCE, 1)]
    m_orgs = {r["organization_id"]: r["name"] for r in read_csv(ROOT / "data/master/organization.csv")}
    m_people = {r["person_id"] for r in read_csv(ROOT / "data/master/person.csv")}
    errors = []
    for o, n in EXISTING_ORGS.items():
        if m_orgs.get(o) != n:
            errors.append(f"{o} not in MASTER as {n}")
    if R in m_people or B not in m_people or H not in m_people:
        errors.append("person MASTER status differs from expectation")
    decisions = [{"decision_id": f"{P}D0001", "entity_type": "Person", "entity_id": R, "decision": "READY_FOR_VERIFIED_REVIEW",
                  "eligible_fields": "name|date_of_birth", "held_fields": "", "reason": "NBA公式で生年月日、Wikipediaで日本語氏名を確認", "reviewed_at": CHECKED}]
    for c in careers:
        held = [f for f in ("start", "end") if not c[f]]
        decisions.append({"decision_id": f"{P}D{len(decisions) + 1:04d}", "entity_type": "Career", "entity_id": c["career_id"],
                          "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "|".join(f for f in ("organization_id", "role", "start", "end") if f not in held),
                          "held_fields": "|".join(held), "reason": "NBA公式・NBL公式・大学公式・クラブ公式の記録で確認", "reviewed_at": CHECKED})
    for cid in REJECT:
        decisions.append({"decision_id": f"{P}D{len(decisions) + 1:04d}", "entity_type": "Career", "entity_id": cid, "decision": "REJECT_CANDIDATE",
                          "eligible_fields": "", "held_fields": "",
                          "reason": "wave_07のCareer（Wikipedia・報道が出典、期間なし）を、公式資料による期間付きCareer（C002731〜C002735）に置き換えたため取り下げ",
                          "reviewed_at": CHECKED})
    issues = [{"issue_id": f"{P}I{i:04d}", "person_id": p, "related_id": rel, "issue_type": t, "status": "HOLD", "description": d, "next_check": nc}
              for i, (p, rel, t, d, nc) in enumerate(ISSUES, 1)]
    used_c = {r["career_id"] for r in read_csv(ROOT / "data/master/career.csv")}
    used_o = set(m_orgs)
    w7 = set()
    for path in (ROOT / "data/candidate").rglob("career_candidates.csv"):
        if OUT not in path.parents:
            rows = read_csv(path)
            used_c |= {r["career_id"] for r in rows}
            if path.parent.name == "wave_07" and "batch_007" in str(path):
                w7 |= {r["career_id"] for r in rows}
    for path in (ROOT / "data/candidate").rglob("organization_candidates.csv"):
        if OUT not in path.parents:
            used_o |= {r["organization_id"] for r in read_csv(path)}
    if {c["career_id"] for c in careers} & used_c:
        errors.append("Career ID already used")
    if {o for o, _ in ORGS} & used_o or {n for _, n in ORGS} & set(m_orgs.values()):
        errors.append("Organization ID/name already used")
    if not set(REJECT) <= w7:
        errors.append("wave_07 careers missing")
    if errors:
        raise SystemExit("; ".join(errors))
    orgs = [{"organization_id": o, "name": n} for o, n in ORGS + list(EXISTING_ORGS.items()) + list(CANDIDATE_ORGS.items())]
    write_csv(OUT / "person_candidates.csv", ["person_id", "name"], [{"person_id": R, "name": "八村塁"}])
    write_csv(OUT / "organization_candidates.csv", ["organization_id", "name"], sorted(orgs, key=lambda r: r["organization_id"]))
    write_csv(OUT / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], sources)
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
    write_csv(OUT / "qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields",
                                         "reason", "reviewed_at"], decisions)
    print(f"wave_13: persons=1 careers={len(careers)} new_orgs={len(ORGS)} evidence={len(evidence)} issues={len(issues)} rejects={len(REJECT)}")


if __name__ == "__main__":
    main()
