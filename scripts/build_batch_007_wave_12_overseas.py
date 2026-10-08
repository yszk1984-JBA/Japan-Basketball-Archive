#!/usr/bin/env python3
"""Build batch_007 Wave 12: overseas careers of 渡邊雄太・田臥勇太・富永啓生, CANDIDATE.

Yuichi (2026-10-08): 「渡邊雄太選手のデータが少なくないか？」→「3人まとめて進めましょう」.
All three were registered in batch_007 (wave_07), whose issue B7I0024 left the
transfer chain (NBA etc.) out of scope. This wave adds it (per-origin rule).

Raw values: data/raw/research/nba_gleague_watanabe_tabuse_tominaga_2026-10-08.md
(stats.nba.com for NBA and G League (LeagueID=20, formerly NBDL), the
universities' official rosters and signing news), read in the browser.

- Season rule as for 河村 (batch_004 wave_07): start = first season's start
  year, end = last season's end year.
- 渡邊's G League games (two-way assignments) are not separate Careers.
- Periods of two existing MASTER school Careers (渡邊 GWU, 富永 Nebraska) are
  proposed as MASTER corrections; MASTER is not changed here.
- Domestic careers before B.LEAGUE (田臥's リンク栃木ブレックス 2008-16) wait
  for Yuichi's source-policy decision and are not added.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_007/wave_12"
CHECKED = "2026-10-08"
P = "B7W12"
W, T, K = "P000103", "P000105", "P000106"
NBA = "NBA.com（stats.nba.com）"

SOURCES = [
    ("S0001", "Yuta Watanabe 通算成績（レギュラーシーズン、シーズン別）", NBA,
     "https://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=Totals&PlayerID=1629139"),
    ("S0002", "Yuta Watanabe 選手情報", NBA, "https://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID=1629139"),
    ("S0003", "Memphis Grizzlies ロスター 2018-19", NBA,
     "https://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2018-19&TeamID=1610612763"),
    ("S0004", "Toronto Raptors ロスター 2021-22", NBA,
     "https://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2021-22&TeamID=1610612761"),
    ("S0005", "Brooklyn Nets ロスター 2022-23", NBA,
     "https://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2022-23&TeamID=1610612751"),
    ("S0006", "Memphis Grizzlies ロスター 2023-24", NBA,
     "https://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2023-24&TeamID=1610612763"),
    ("S0007", "Yuta Tabuse 試合記録 2004-05（レギュラーシーズン）", NBA,
     "https://stats.nba.com/stats/playergamelog?PlayerID=2657&Season=2004-05&SeasonType=Regular%20Season"),
    ("S0008", "Yuta Tabuse 選手情報", NBA, "https://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID=2657"),
    ("S0009", "Yuta Tabuse NBA Gリーグ（旧NBDL）通算成績・試合記録 2005-06〜2007-08", NBA,
     "https://stats.nba.com/stats/playercareerstats?LeagueID=20&PerMode=Totals&PlayerID=2657"),
    ("S0010", "NBA Gリーグ フランチャイズ履歴（チーム名・TeamID）", NBA,
     "https://stats.nba.com/stats/franchisehistory?LeagueID=20"),
    ("S0011", "Keisei Tominaga NBA Gリーグ 選手情報・通算成績・試合記録 2024-25", NBA,
     "https://stats.nba.com/stats/commonplayerinfo?LeagueID=20&PlayerID=1642551"),
    ("S0012", "George Washington Men's Basketball Roster 2014-15〜2017-18", "George Washington University Athletics（大学公式）",
     "https://gwsports.com/sports/mens-basketball/roster/2017-18"),
    ("S0013", "Nebraska Men's Basketball Roster 2021-22〜2023-24", "University of Nebraska Athletics（大学公式）",
     "https://huskers.com/sports/mens-basketball/roster/season/2023-24"),
    ("S0014", "Huskers Sign Keisei Tominaga（2020-11-11）", "University of Nebraska Athletics（大学公式）",
     "https://huskers.com/news/2020/11/11/huskers-sign-keisei-tominaga"),
]
ORGS = [("ORG000485", "トロント・ラプターズ"), ("ORG000486", "ブルックリン・ネッツ"), ("ORG000487", "フェニックス・サンズ"),
        ("ORG000488", "アルバカーキ・サンダーバーズ"), ("ORG000489", "ベーカーズフィールド・ジャム"),
        ("ORG000490", "アナハイム・アーセナル"), ("ORG000491", "レンジャー・カレッジ"), ("ORG000492", "インディアナ・マッドアンツ")]
MEM = "ORG000098"

# career_id, person, org, start, end
CAREERS = [
    ("C002720", W, MEM, "2018", "2020"),
    ("C002721", W, "ORG000485", "2020", "2022"),
    ("C002722", W, "ORG000486", "2022", "2023"),
    ("C002723", W, "ORG000487", "2023", "2024"),
    ("C002724", W, MEM, "2023", "2024"),
    ("C002725", T, "ORG000487", "2004", "2005"),
    ("C002726", T, "ORG000488", "2005", "2006"),
    ("C002727", T, "ORG000489", "2006", "2007"),
    ("C002728", T, "ORG000490", "2007", "2008"),
    ("C002729", K, "ORG000491", "2019", "2021"),
    ("C002730", K, "ORG000492", "2024", "2025"),
]
CS = "SEASON_ID / TEAM_ABBREVIATION / GP"
# (career, field, value, source, locator, summary)
EVIDENCE = [
    ("C002720", "organization_id", MEM, "S0001", "2018-19 MEM 15 / 2019-20 MEM 18（TEAM_ID 1610612763）", "NBA公式の通算成績でメンフィス・グリズリーズ在籍を確認"),
    ("C002720", "organization_id", MEM, "S0003", "PLAYER Yuta Watanabe / NUM 12", "NBA公式の2018-19ロスターに掲載"),
    ("C002720", "role", "Player", "S0001", "GP 15・18", "選手として出場"),
    ("C002720", "start", "2018", "S0001", "最初の行 SEASON_ID 2018-19", "2018-19シーズンの開始年"),
    ("C002720", "end", "2020", "S0001", "MEMの連続した最後の行 SEASON_ID 2019-20（次は2020-21 TOR）", "2019-20シーズンの終了年"),
    ("C002721", "organization_id", "ORG000485", "S0001", "2020-21 TOR 50 / 2021-22 TOR 38（TEAM_ID 1610612761）", "NBA公式の通算成績でトロント・ラプターズ在籍を確認"),
    ("C002721", "organization_id", "ORG000485", "S0004", "PLAYER Yuta Watanabe / NUM 18", "NBA公式の2021-22ロスターに掲載"),
    ("C002721", "role", "Player", "S0001", "GP 50・38", "選手として出場"),
    ("C002721", "start", "2020", "S0001", "SEASON_ID 2020-21 TOR", "2020-21シーズンの開始年"),
    ("C002721", "end", "2022", "S0001", "TORの最後の行 SEASON_ID 2021-22", "2021-22シーズンの終了年"),
    ("C002722", "organization_id", "ORG000486", "S0001", "2022-23 BKN 58（TEAM_ID 1610612751）", "NBA公式の通算成績でブルックリン・ネッツ在籍を確認"),
    ("C002722", "organization_id", "ORG000486", "S0005", "PLAYER Yuta Watanabe / NUM 18", "NBA公式の2022-23ロスターに掲載"),
    ("C002722", "role", "Player", "S0001", "GP 58", "選手として出場"),
    ("C002722", "start", "2022", "S0001", "SEASON_ID 2022-23 BKN", "2022-23シーズンの開始年"),
    ("C002722", "end", "2023", "S0001", "SEASON_ID 2022-23 BKN（1シーズン）", "2022-23シーズンの終了年"),
    ("C002723", "organization_id", "ORG000487", "S0001", "2023-24 PHX 29（TEAM_ID 1610612756）", "NBA公式の通算成績でフェニックス・サンズ在籍を確認"),
    ("C002723", "role", "Player", "S0001", "GP 29", "選手として出場"),
    ("C002723", "start", "2023", "S0001", "SEASON_ID 2023-24 PHX", "2023-24シーズンの開始年"),
    ("C002723", "end", "2024", "S0001", "SEASON_ID 2023-24 PHX（同シーズンにMEMの行あり）", "2023-24シーズンの終了年"),
    ("C002724", "organization_id", MEM, "S0001", "2023-24 MEM 5（TEAM_ID 1610612763）", "NBA公式の通算成績で2023-24シーズン途中からのグリズリーズ在籍を確認"),
    ("C002724", "organization_id", MEM, "S0006", "PLAYER Yuta Watanabe / NUM 18", "NBA公式の2023-24ロスター（シーズン末）に掲載"),
    ("C002724", "role", "Player", "S0001", "GP 5", "選手として出場"),
    ("C002724", "start", "2023", "S0001", "SEASON_ID 2023-24 MEM", "2023-24シーズンの開始年"),
    ("C002724", "end", "2024", "S0001", "NBAの最後の行 SEASON_ID 2023-24（TO_YEAR 2023、S0002）", "2023-24シーズンの終了年。以後NBAの記録なし"),
    ("C002725", "organization_id", "ORG000487", "S0007", "MATCHUP：Nov 03, 2004 PHX vs. ATL ほか4試合", "NBA公式の試合記録でフェニックス・サンズでの出場を確認"),
    ("C002725", "role", "Player", "S0007", "4試合（Nov 03, 2004 – Dec 15, 2004）", "選手として出場"),
    ("C002725", "start", "2004", "S0008", "FROM_YEAR 2004 / TO_YEAR 2004", "NBA公式で2004-05シーズンのみ"),
    ("C002725", "end", "2005", "S0007", "Season 2004-05", "2004-05シーズンの終了年"),
    ("C002726", "organization_id", "ORG000488", "S0009", "2005-06 GP 34／試合記録のチーム略称 ABQ（34試合）", "NBA公式のGリーグ（旧NBDL）記録で在籍を確認"),
    ("C002726", "organization_id", "ORG000488", "S0010", "1612709893 Albuquerque Thunderbirds（2004–2009）", "略称ABQのチーム名をフランチャイズ履歴で確認"),
    ("C002726", "role", "Player", "S0009", "GP 34", "選手として出場"),
    ("C002726", "start", "2005", "S0009", "SEASON 2005-06（Nov 18, 2005 – Mar 03, 2006）", "2005-06シーズンの開始年"),
    ("C002726", "end", "2006", "S0009", "SEASON 2005-06", "2005-06シーズンの終了年"),
    ("C002727", "organization_id", "ORG000489", "S0009", "2006-07 GP 44／試合記録のチーム略称 BAK（44試合）", "NBA公式のGリーグ（旧NBDL）記録で在籍を確認"),
    ("C002727", "organization_id", "ORG000489", "S0010", "1612709900 Bakersfield Jam（2006–2015、DefunctTeams）", "略称BAKのチーム名をフランチャイズ履歴で確認"),
    ("C002727", "role", "Player", "S0009", "GP 44", "選手として出場"),
    ("C002727", "start", "2006", "S0009", "SEASON 2006-07（Nov 26, 2006 – Apr 14, 2007）", "2006-07シーズンの開始年"),
    ("C002727", "end", "2007", "S0009", "SEASON 2006-07", "2006-07シーズンの終了年"),
    ("C002728", "organization_id", "ORG000490", "S0009", "2007-08 GP 39／試合記録のチーム略称 ANA（39試合）", "NBA公式のGリーグ（旧NBDL）記録で在籍を確認"),
    ("C002728", "organization_id", "ORG000490", "S0010", "1612709899 Anaheim Arsenal（2006–2008、DefunctTeams）", "略称ANAのチーム名をフランチャイズ履歴で確認"),
    ("C002728", "role", "Player", "S0009", "GP 39", "選手として出場"),
    ("C002728", "start", "2007", "S0009", "SEASON 2007-08（Dec 09, 2007 – Apr 12, 2008）", "2007-08シーズンの開始年"),
    ("C002728", "end", "2008", "S0009", "SEASON 2007-08", "2007-08シーズンの終了年"),
    ("C002729", "organization_id", "ORG000491", "S0014", "本文：currently a sophomore at Ranger (Texas) College", "ネブラスカ大学公式の加入発表でレンジャー・カレッジ在籍を確認"),
    ("C002729", "organization_id", "ORG000491", "S0013", "Previous School：Ranger College", "ネブラスカ大学公式ロスターの前所属"),
    ("C002729", "role", "Player", "S0014", "本文：one of the top freshmen in junior college basketball last season, helping Ranger College", "選手としてプレー"),
    ("C002729", "start", "2019", "S0014", "本文（2020-11-11）：freshmen … last season（2019-20）", "1年目は2019-20シーズン"),
    ("C002729", "end", "2021", "S0014", "本文：currently a sophomore … will begin its season in January of 2021", "2年目は2020-21シーズン。2021-22はネブラスカ大学のロスター（S0013）"),
    ("C002730", "organization_id", "ORG000492", "S0011", "TEAM_NAME Mad Ants／2024-25 TEAM_ID 1612709910 IMA GP 14", "NBA公式のGリーグ記録でマッドアンツ在籍を確認"),
    ("C002730", "organization_id", "ORG000492", "S0010", "1612709910 Indiana Mad Ants（2024）", "2024-25シーズンのチーム名をフランチャイズ履歴で確認"),
    ("C002730", "role", "Player", "S0011", "GP 14（Dec 28, 2024 – Mar 29, 2025）", "選手として出場"),
    ("C002730", "start", "2024", "S0011", "FROM_YEAR 2024 / SEASON 2024-25", "2024-25シーズンの開始年"),
    ("C002730", "end", "2025", "S0011", "TO_YEAR 2024 / SEASON 2024-25", "2024-25シーズンの終了年"),
]
# MASTER period corrections: career, person, org name, new start, new end, source, locator, reason
CORRECTIONS = [
    ("C000354", W, "ジョージ・ワシントン大学", "2014", "2018", "S0012",
     "2014-15 Fr. / 2015-16 So. / 2016-17 Jr. / 2017-18 Sr.（2013-14・2018-19は掲載なし）",
     "大学公式の年度別ロスターで2014-15〜2017-18の4シーズン在籍"),
    ("C000363", K, "ネブラスカ大学", "2021", "2024", "S0013",
     "2021-22 Sophomore / 2022-23 Junior / 2023-24 Senior（2020-21・2024-25は掲載なし）",
     "大学公式の年度別ロスターで2021-22〜2023-24の3シーズン在籍"),
]
ISSUES = [
    (W, "C002723", "SAME_SEASON_TWO_CLUBS",
     "2023-24シーズンはフェニックス・サンズ（29試合）とメンフィス・グリズリーズ（5試合）の2クラブに在籍（シーズン途中の移籍）。シーズン単位のルールで両方に同じ年を用いた。移籍の時期・理由は記録しない。",
     "移籍時期を記録する必要が出たら、NBA公式の取引記録で確認"),
    (W, W, "G_LEAGUE_ASSIGNMENTS",
     "グリズリーズ・ラプターズ在籍中のGリーグ出場（2018-19 33試合、2019-20 22試合、2021-22 1試合。NBA公式のGリーグ記録ではチーム欄が空欄）は、NBAクラブとの契約の一部のため別Careerにしていない（河村勇輝と同じ扱い）。",
     "Gリーグ在籍を記録するかはYuichiと方針を決める"),
    (T, T, "OVERSEAS_UNVERIFIED",
     "NBA入り前のABA（ロングビーチ・ジャム、2003-04とされる）とNBAクラブのトレーニングキャンプ参加は、公式の記録を確認できていないため登録していない。",
     "当時のリーグ・クラブの公式資料が見つかれば確認"),
    (T, T, "PRE_BLEAGUE_HISTORY",
     "帰国後のリンク栃木ブレックス（2008〜2016、現・宇都宮ブレックス）の在籍は、B.LEAGUE開幕前の国内所属の出典方針（Yuichiの判断待ち）が決まるまで登録しない。",
     "出典方針の決定後、クラブ公式の資料で確認"),
    (K, "C002730", "ORG_NAME_HISTORY",
     "このチーム（Gリーグ TeamID 1612709910）はFort Wayne Mad Ants（2007–2023）→Indiana Mad Ants（2024）→Noblesville Boom（2025）と改称。在籍した2024-25の名称「インディアナ・マッドアンツ」で登録した。改称クラブは現在の名称で1つのOrganizationにする既存ルールとの違いはYuichiの判断待ち。",
     "Organization名を現在の名称にするか、在籍当時の名称にするかを決める"),
]


def main() -> None:
    sources = [{"source_id": f"{P}{sid}", "title": t, "publisher": pub, "url": url, "accessed_at": CHECKED} for sid, t, pub, url in SOURCES]
    careers = [{"career_id": c, "person_id": p, "organization_id": o, "role": "Player", "start": s, "end": e} for c, p, o, s, e in CAREERS]
    evidence = [{"record_id": f"{P}E{i:04d}", "entity_type": "Career", "entity_id": eid, "field_name": f, "candidate_value": v,
                 "source_id": f"{P}{sid}", "source_locator": loc, "evidence_summary": summ, "assessment": "SUPPORTED",
                 "checked_at": CHECKED, "issue_note": ""} for i, (eid, f, v, sid, loc, summ) in enumerate(EVIDENCE, 1)]
    master = {r["career_id"]: r for r in read_csv(ROOT / "data/master/career.csv")}
    m_orgs = {r["organization_id"]: r["name"] for r in read_csv(ROOT / "data/master/organization.csv")}
    corr_rows, errors = [], []
    for cid, pid, oname, ns, ne, sid, loc, why in CORRECTIONS:
        m = master[cid]
        if m["person_id"] != pid or m_orgs[m["organization_id"]] != oname:
            errors.append(f"{cid}: MASTER differs")
        for field, value in (("start", ns), ("end", ne)):
            evidence.append({"record_id": f"{P}E{len(evidence) + 1:04d}", "entity_type": "Career", "entity_id": cid, "field_name": field,
                             "candidate_value": value, "source_id": f"{P}{sid}", "source_locator": loc, "evidence_summary": why,
                             "assessment": "SUPPORTED", "checked_at": CHECKED, "issue_note": "既存MASTER Careerの期間の訂正案（master_corrections.csv）"})
        corr_rows.append({"career_id": cid, "person_id": pid, "organization_name": oname, "old_start": m["start"], "old_end": m["end"],
                          "new_start": ns, "new_end": ne, "reason": why})
    decisions = [{"decision_id": f"{P}D{i:04d}", "entity_type": "Career", "entity_id": c["career_id"], "decision": "READY_FOR_VERIFIED_REVIEW",
                  "eligible_fields": "organization_id|role|start|end", "held_fields": "",
                  "reason": "NBA公式（NBA・Gリーグ）または大学公式の記録で確認", "reviewed_at": CHECKED} for i, c in enumerate(careers, 1)]
    issues = [{"issue_id": f"{P}I{i:04d}", "person_id": p, "related_id": rel, "issue_type": t, "status": "HOLD",
               "description": d, "next_check": nc} for i, (p, rel, t, d, nc) in enumerate(ISSUES, 1)]

    used_c, used_o = set(master), set(m_orgs)
    for path in (ROOT / "data/candidate").rglob("career_candidates.csv"):
        if OUT not in path.parents:
            used_c |= {r["career_id"] for r in read_csv(path)}
    for path in (ROOT / "data/candidate").rglob("organization_candidates.csv"):
        if OUT not in path.parents:
            used_o |= {r["organization_id"] for r in read_csv(path)}
    if {c["career_id"] for c in careers} & used_c:
        errors.append("Career ID already used")
    if {o for o, _ in ORGS} & used_o or {n for _, n in ORGS} & set(m_orgs.values()):
        errors.append("Organization ID/name already used")
    if {e["source_id"] for e in evidence} - {s["source_id"] for s in sources}:
        errors.append("unknown source")
    for c in careers:
        fields = {e["field_name"] for e in evidence if e["entity_id"] == c["career_id"]}
        if fields != {"organization_id", "role", "start", "end"}:
            errors.append(f"{c['career_id']}: evidence fields {sorted(fields)}")
    if errors:
        raise SystemExit("; ".join(errors))

    orgs = [{"organization_id": o, "name": n} for o, n in ORGS] + [{"organization_id": MEM, "name": m_orgs[MEM]}]
    write_csv(OUT / "person_candidates.csv", ["person_id", "name"], [])
    write_csv(OUT / "organization_candidates.csv", ["organization_id", "name"], sorted(orgs, key=lambda r: r["organization_id"]))
    write_csv(OUT / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], sources)
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
    write_csv(OUT / "qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields",
                                         "reason", "reviewed_at"], decisions)
    write_csv(OUT / "master_corrections.csv", ["career_id", "person_id", "organization_name", "old_start", "old_end",
                                               "new_start", "new_end", "reason"], corr_rows)
    print(f"wave_12: careers={len(careers)} new_orgs={len(ORGS)} evidence={len(evidence)} issues={len(issues)} corrections={len(corr_rows)}")


if __name__ == "__main__":
    main()
