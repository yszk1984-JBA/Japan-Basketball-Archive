#!/usr/bin/env python3
"""Build batch_034 Wave 1: post-opening roster update for 2026-27, CANDIDATE.

Yuichi (2026-10-22): 「ひさしぶりに選手のリサーチをアップデートしたい」→ chose
「開幕後の現所属の更新」. The B.PREMIER / B.ONE official rosters were re-read
on 2026-10-22 and compared with the 2026-09-29/30 rosters and MASTER
(raw: data/raw/research/bleague_roster_2026-10-22.tsv and
bleague_roster_followup_2026-10-22.md).

The update spans persons from several batches (batch_007, batch_032,
batch_033 ...), so -- as with batch_031 -- it is kept in one dedicated batch
instead of being split per origin batch.

Contents:
- master_corrections.csv: period corrections of existing MASTER Careers
  (石川裕大 宇都宮 end, 小寺 香川 end, 井手 東京Z start, 古野 愛媛 start).
- career_candidates.csv: 石川裕大's new 東京Z Career, and the Careers of two
  new persons (佐野悠星, 宮永颯太) who appeared on the rosters after opening.
- person_candidates.csv: the two new persons (both 18+; 佐藤瑠一シャンドレイ is
  16 and is not registered).
- issues.csv: HOLD items (河村 Clippers, 平尾, 小寺 mid-season departure,
  unreadable profiles, unknown schools).

Season rule (batch_031): start = first season's start year; end = last
season's end year; no end while on the 2026-27 roster.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_034/wave_01"
CHECKED = "2026-10-22"
P = "B34W1"
PROFILE = "https://www.bleague.jp/roster_detail/?PlayerID={}"

# career, person, PlayerID, name, club, (old_start, old_end), (new_start, new_end), locator, summary
CORRECTIONS = [
    ("C001269", "P000287", "51000425", "石川裕大", "宇都宮ブレックス", ("2024", ""), ("2024", "2026"),
     "クラブ所属履歴 > 「2024-25 宇都宮」「2025-26 宇都宮」、最新行「2026-27 東京Z」",
     "B.LEAGUE公式の所属履歴で宇都宮の最後のシーズンが2025-26（2026-27は東京Z）であることを確認。終了年＝2025-26の終了年"),
    ("C002515", "P000532", "9456", "小寺ハミルトンゲイリー", "香川ファイブアローズ", ("2026", ""), ("2026", "2027"),
     "クラブ所属履歴 > 「2026-27 香川」／香川の2026-27選手一覧「退団済」に掲載",
     "B.LEAGUE公式で香川の2026-27選手一覧（退団済）に掲載。在籍は2026-27のみのため、終了年＝2026-27の終了年（期間のルールどおり）"),
    ("C000092", "P000036", "51000110", "井手拓実", "アースフレンズ東京Z", ("", ""), ("2026", ""),
     "クラブ所属履歴 > 「2026-27 東京Z」（前行「2025-26 福岡」）",
     "B.LEAGUE公式の所属履歴で東京Zへの在籍開始シーズンを確認（2026-27在籍中のため終了年なし）"),
    ("C000211", "P000063", "9348", "古野拓巳", "愛媛オレンジバイキングス", ("", ""), ("2022", ""),
     "クラブ所属履歴 > 「2022-23 愛媛」〜「2026-27 愛媛」（前行「2021-22 熊本」）",
     "B.LEAGUE公式の所属履歴で愛媛への在籍開始シーズンを確認（2026-27在籍中のため終了年なし）"),
]
NEW_PERSONS = [
    # person, PlayerID, name, birth_date, birth text
    ("P000564", "51000483", "佐野 悠星", "2002-09-06", "2002年9月6日"),
    ("P000565", "51000720", "宮永 颯太", "2004-03-09", "2004年3月9日"),
]
# career, person, PlayerID, organization, start, end, locator
NEW_CAREERS = [
    ("C002778", "P000287", "51000425", "ORG000046", "2026", "", "クラブ所属履歴 > 「2026-27 東京Z」"),
    ("C002779", "P000564", "51000483", "ORG000171", "2024", "2025", "クラブ所属履歴 > 「2024-25 奈良」"),
    ("C002780", "P000564", "51000483", "ORG000222", "2026", "", "クラブ所属履歴 > 「2026-27 岡山」"),
    ("C002781", "P000565", "51000720", "ORG000223", "2026", "", "クラブ所属履歴 > 「2026-27 東京U」"),
]
HOLDS = [
    ("P000064", "C002686", "NBA_ROSTER_CHANGE",
     "河村勇輝はNBA公式（stats.nba.com commonteamroster、LAC 2026-27）のクリッパーズのロスターに掲載なし。commonplayerinfoはTEAM_NAME=Bulls、ROSTERSTATUS=Inactive、TO_YEAR=2025。クリッパーズのCareer（C002686、2026〜）は変更しない（2026-10-22 Yuichiの回答は指定なし→保留で進める）。",
     "Gリーグ（LeagueID=20）の2026-27名簿の公開後、または新しい所属の公式発表後に、C002686の扱いとあわせて確認"),
    ("P000308", "C001371", "ROSTER_STATUS_UNCLEAR",
     "平尾充庸の所属履歴は「2026-27 茨城」まで掲載されているが、茨城の2026-27選手一覧（在籍中・退団済・全選手）のいずれにも載っていない。茨城ロボッツのCareer（C001371、2017〜）は変更しない。",
     "B.LEAGUE公式・茨城ロボッツ公式の発表を確認"),
    ("P000532", "C002515", "MID_SEASON_DEPARTURE",
     "小寺ハミルトンゲイリーは香川の2026-27選手一覧で「退団済」。期間のルールにより終了年を2027としたが、シーズン途中（開幕前後）の退団で、2026-27の大半は在籍していない。",
     "次の所属が公式に出た時点で表示上の扱いを確認"),
    ("P000041", "C000129", "PROFILE_UNAVAILABLE",
     "狩野祐介のB.LEAGUE公式プロフィール（PlayerID=8463）がHTTP 500で読めず、福岡のCareer（C000129、期間なし）の開始年を確認できなかった（2026-10-22、複数回）。",
     "時間をおいて公式プロフィール、またはライジングゼファー福岡公式の選手ページで確認"),
    ("", "", "PROFILE_UNAVAILABLE",
     "開幕後に一覧へ載った岡本飛竜（PlayerID=8839、福井）とファイ パプ月瑠（PlayerID=9400、香川）は、B.LEAGUE公式プロフィールがHTTP 500で読めず、Masterとの照合（既存登録の有無）・生年月日を確認できなかった。登録していない。",
     "時間をおいて公式プロフィール、またはクラブ公式の加入発表で確認"),
    ("P000564", "P000564", "SCHOOL_NOT_LISTED",
     "佐野悠星のB.LEAGUE公式プロフィールは出身校の記載なし。学校のCareerは登録していない。",
     "岡山・奈良のクラブ公式の加入発表で確認"),
    ("P000565", "P000565", "SCHOOL_NOT_LISTED",
     "宮永颯太のB.LEAGUE公式プロフィールは出身校の記載なし。学校のCareerは登録していない。",
     "東京ユナイテッド公式の加入発表で確認"),
    ("P000564", "P000564", "PRE_BLEAGUE_HISTORY",
     "佐野悠星の公式所属履歴は2024-25 奈良、2026-27 岡山のみ（2025-26の記載なし）。記載のない期間は推測せず記録していない。",
     "クラブ公式の発表で確認"),
]


def main() -> None:
    m_people = {r["person_id"]: r["name"] for r in read_csv(ROOT / "data/master/person.csv")}
    m_orgs = {r["organization_id"]: r["name"] for r in read_csv(ROOT / "data/master/organization.csv")}
    m_careers = {r["career_id"]: r for r in read_csv(ROOT / "data/master/career.csv")}
    errors = []
    sources, evidence, decisions, corr = {}, [], [], []

    def source(bid: str, name: str) -> str:
        if bid not in sources:
            sources[bid] = {"source_id": f"{P}S{len(sources) + 1:04d}", "title": f"{name} 選手プロフィール（クラブ所属履歴）",
                            "publisher": "B.LEAGUE", "url": PROFILE.format(bid), "accessed_at": CHECKED}
        return sources[bid]["source_id"]

    def ev(etype: str, eid: str, field: str, value: str, sid: str, loc: str, summary: str, note: str = "") -> None:
        evidence.append({"record_id": f"{P}E{len(evidence) + 1:04d}", "entity_type": etype, "entity_id": eid, "field_name": field,
                         "candidate_value": value, "source_id": sid, "source_locator": loc, "evidence_summary": summary,
                         "assessment": "SUPPORTED", "checked_at": CHECKED, "issue_note": note})

    for cid, pid, bid, name, club, old, new, loc, summary in CORRECTIONS:
        m = m_careers.get(cid)
        if not m or m["person_id"] != pid or (m["start"], m["end"]) != old or m_orgs[m["organization_id"]] != club:
            errors.append(f"{cid}: MASTER row differs from the expected one")
            continue
        sid = source(bid, name)
        for field, o, n in (("start", old[0], new[0]), ("end", old[1], new[1])):
            if o != n:
                ev("Career", cid, field, n, sid, loc, summary, "既存MASTER Careerの期間の訂正案")
        if cid == "C002515":  # the departure is shown on the club's roster list, not on the profile
            sources["roster_722"] = {"source_id": f"{P}S{len(sources) + 1:04d}", "title": "香川ファイブアローズ 2026-27 選手一覧（退団済）",
                                     "publisher": "B.LEAGUE", "accessed_at": CHECKED,
                                     "url": "https://www.bleague.jp/roster/?tab=2&year=2026&club=722&c=日本&e=退団済&o=sort"}
            ev("Career", cid, "end", new[1], sources["roster_722"]["source_id"], "選手一覧（2026-27、香川、退団済）> 小寺 ハミルトンゲイリー",
               "B.LEAGUE公式の2026-27選手一覧で香川の「退団済」に掲載されていることを確認", "既存MASTER Careerの期間の訂正案")
        corr.append({"career_id": cid, "person_id": pid, "organization_name": club, "old_start": old[0], "old_end": old[1],
                     "new_start": new[0], "new_end": new[1], "reason": f"B.LEAGUE公式 {loc}"})

    persons = []
    for pid, bid, name, birth, btext in NEW_PERSONS:
        if pid in m_people:
            errors.append(f"{pid}: already in MASTER")
        if any(n.replace(" ", "") == name.replace(" ", "") for n in m_people.values()):
            errors.append(f"{name}: same name in MASTER")
        if int(birth[:4]) > 2008:
            errors.append(f"{name}: under 18")
        sid = source(bid, name.replace(" ", ""))
        persons.append({"person_id": pid, "name": name})
        ev("Person", pid, "name", name, sid, "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認")
        ev("Person", pid, "birth_date", birth, sid, f"基本情報 > 生年月日：{btext}", "B.LEAGUE公式プロフィールで生年月日を確認")
        decisions.append({"decision_id": f"{P}D{len(decisions) + 1:04d}", "entity_type": "Person", "entity_id": pid,
                          "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "name|birth_date", "held_fields": "",
                          "reason": "B.LEAGUE公式プロフィールで確認", "reviewed_at": CHECKED})

    careers, orgs = [], {}
    names = {pid: n for pid, _, n, _, _ in NEW_PERSONS} | m_people
    for cid, pid, bid, oid, start, end, loc in NEW_CAREERS:
        if cid in m_careers:
            errors.append(f"{cid}: already in MASTER")
        orgs[oid] = m_orgs[oid]
        careers.append({"career_id": cid, "person_id": pid, "organization_id": oid, "role": "Player", "start": start, "end": end})
        sid = source(bid, names[pid].replace(" ", ""))
        ev("Career", cid, "organization_id", oid, sid, loc, f"B.LEAGUE公式の所属履歴で{m_orgs[oid]}への在籍を確認（略称表記）")
        ev("Career", cid, "role", "Player", sid, "選手プロフィール", "B.LEAGUE公式の選手プロフィール")
        ev("Career", cid, "start", start, sid, loc, "所属履歴の最初のシーズンの開始年")
        fields = "organization_id|role|start"
        if end:
            ev("Career", cid, "end", end, sid, loc, "所属履歴の最後のシーズンの終了年")
            fields += "|end"
        decisions.append({"decision_id": f"{P}D{len(decisions) + 1:04d}", "entity_type": "Career", "entity_id": cid,
                          "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": fields, "held_fields": "" if end else "end",
                          "reason": "B.LEAGUE公式の所属履歴で確認" + ("" if end else "（2026-27在籍中のため終了年なし）"),
                          "reviewed_at": CHECKED})

    issues = [{"issue_id": f"{P}I{i:04d}", "person_id": p, "related_id": r, "issue_type": t, "status": "HOLD",
               "description": d, "next_check": n} for i, (p, r, t, d, n) in enumerate(HOLDS, 1)]
    if errors:
        raise SystemExit("; ".join(errors))
    write_csv(OUT / "person_candidates.csv", ["person_id", "name"], persons)
    write_csv(OUT / "organization_candidates.csv", ["organization_id", "name"],
              [{"organization_id": o, "name": n} for o, n in sorted(orgs.items())])
    write_csv(OUT / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], list(sources.values()))
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
    write_csv(OUT / "qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields",
                                         "reason", "reviewed_at"], decisions)
    write_csv(OUT / "master_corrections.csv", ["career_id", "person_id", "organization_name", "old_start", "old_end",
                                               "new_start", "new_end", "reason"], corr)
    print(f"batch_034 wave_01: persons={len(persons)} careers={len(careers)} corrections={len(corr)} "
          f"evidence={len(evidence)} issues={len(issues)} sources={len(sources)}")


if __name__ == "__main__":
    main()
