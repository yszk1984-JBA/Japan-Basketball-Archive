#!/usr/bin/env python3
"""Build batch_037 Wave 1: research update of 2026-10-29, CANDIDATE.

Yuichi (2026-10-27/29): 「今日のリサーチをお願いします」「もう一度お願い致します」.
Follow-ups of the post-opening update (batch_034 HOLDs) and of the school gaps:
- 平尾充庸 retired on 2026-09-27 (茨城ロボッツ official) → end of his 茨城 Career.
- 河村勇輝: not on the Clippers 2026-27 roster; NBA official G League list
  (2026-27) shows him with the San Diego Clippers → end of the Clippers Career,
  new San Diego Clippers Career.
- 狩野祐介: start of his 福岡 Career (profile was unreadable on 2026-10-22).
- New persons 岡本飛竜 and ファイパプ月瑠 (unreadable on 2026-10-22).
- Schools: ジャンバルボ海斗 (B.LEAGUE official article), 長島蓮 and 長谷川智伸
  (Wikipedia, Tier 2), and 長谷川's pre-B.LEAGUE club (Wikipedia, Tier 2).
Raw: data/raw/research/update_2026-10-29.md. Rules as before (season years;
pre-B part of a continuing club ends in 2016; non-official sources = Tier 2).
The persons come from several batches, so this is one dedicated batch.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_037/wave_01"
CHECKED = "2026-10-29"
P = "B37W1"
BL = "https://www.bleague.jp/roster_detail/?PlayerID={}"
FIRST_CAREER = 2806

SOURCES = {
    "okamoto": ("岡本飛竜 選手プロフィール（クラブ所属履歴）", "B.LEAGUE", BL.format("8839"), True),
    "fall": ("ファイパプ月瑠 選手プロフィール（クラブ所属履歴）", "B.LEAGUE", BL.format("9400"), True),
    "kano": ("狩野祐介 選手プロフィール（クラブ所属履歴）", "B.LEAGUE", BL.format("8463"), True),
    "hirao": ("平尾充庸 選手プロフィール（クラブ所属履歴）", "B.LEAGUE", BL.format("8561"), True),
    "hirao_retire": ("#25 平尾 充庸選手 9/27(日) 三遠戦「LAST GAME」のお知らせ（2026-09-13）", "茨城ロボッツ（クラブ公式）",
                     "https://www.ibarakirobots.win/news/20260913_01_team/", True),
    "hirao_role": ("平尾 充庸氏 プレーヤーズメンター 兼 クラブリレーションリーダー 就任のご報告（2026-09-30）", "茨城ロボッツ（クラブ公式）",
                   "https://www.ibarakirobots.win/news/20260930_03_team/", True),
    "gleague": ("NBA G League 選手一覧 2026-27（commonallplayers、LeagueID=20）", "NBA（stats.nba.com）",
                "https://stats.nba.com/stats/commonallplayers?LeagueID=20&Season=2026-27&IsOnlyCurrentSeason=1", True),
    "fall_news": ("香川ファイブアローズが帰化選手のファイパプ月瑠を獲得…2季ぶりにBリーグの舞台へ（2026-10-09）", "B.LEAGUE（MEDIA NEWS）",
                  "https://www.bleague.jp/media_news/detail/id=665814", True),
    "giambalvo": ("ジャンバルボ 海斗（近畿大学）／インカレで好パフォーマンス！（B.MAGAZINE）", "B.LEAGUE",
                  "https://www.bleague.jp/bmagazine/detail/id=544903", True),
    "okamoto_bbk": ("岡本飛竜、新天地が決定…福井ブローウィンズと契約合意（2026-10-02）", "バスケットボールキング（公式以外）",
                    "https://basketballking.jp/news/japan/20261002/635704.html", False),
    "okamoto_wiki": ("岡本飛竜（Wikipedia日本語版、版 111544473）", "Wikipedia日本語版（公式以外）",
                     "https://ja.wikipedia.org/w/index.php?title=%E5%B2%A1%E6%9C%AC%E9%A3%9B%E7%AB%9C&oldid=111544473", False),
    "nagashima_wiki": ("長島蓮（Wikipedia日本語版、版 111541694）", "Wikipedia日本語版（公式以外）",
                       "https://ja.wikipedia.org/w/index.php?title=%E9%95%B7%E5%B3%B6%E8%93%AE&oldid=111541694", False),
    "hasegawa_wiki": ("長谷川智伸（Wikipedia日本語版、版 108143921）", "Wikipedia日本語版（公式以外）",
                      "https://ja.wikipedia.org/w/index.php?title=%E9%95%B7%E8%B0%B7%E5%B7%9D%E6%99%BA%E4%BC%B8&oldid=108143921", False),
}
NEW_ORGS = {"ORG000516": "サンディエゴ・クリッパーズ", "ORG000517": "西海学園高等学校"}
NEW_PERSONS = [  # person, name, birth, source, locator
    ("P000566", "岡本 飛竜", "1993-04-20", "okamoto", "基本情報 > 生年月日：1993年4月20日"),
    ("P000567", "ファイ パプ月瑠", "1987-06-22", "fall", "基本情報 > 生年月日：1987年6月22日"),
]
# career, person, org, start, end, [(source, locator)], summary
P_OK, P_FALL = "P000566", "P000567"
NEW_CAREERS = [
    (P_OK, "ORG000194", "", "", [("okamoto_bbk", "本文：「延岡学園高校、拓殖大学を経て、島根スサノオマジックでプロキャリアを始めた」"),
                                 ("okamoto_wiki", "基本情報欄 > |高校=[[延岡学園高等学校・尚学館中学校|延岡学園高等学校]]")], "出身高校"),
    (P_OK, "ORG000031", "", "", [("okamoto_bbk", "本文：「延岡学園高校、拓殖大学を経て…」"),
                                 ("okamoto_wiki", "基本情報欄 > |大学=[[拓殖大学オレンジクラッシャーズ|拓殖大学]]")], "出身大学"),
    (P_OK, "ORG000155", "2015", "2016", [("okamoto_wiki", "基本情報欄 > |所属1=[[島根スサノオマジック]] |所属年1=2015-2018")],
     "B.LEAGUE開幕前（bjリーグ）の部分。2016〜2018はB.LEAGUE公式の所属履歴による別のCareer"),
    (P_OK, "ORG000155", "2016", "2018", [("okamoto", "クラブ所属履歴 > 「2016-17 島根」〜「2017-18 島根」")], ""),
    (P_OK, "ORG000110", "2018", "2021", [("okamoto", "クラブ所属履歴 > 「2018-19 広島」〜「2020-21 広島」")], ""),
    (P_OK, "ORG000052", "2021", "2022", [("okamoto", "クラブ所属履歴 > 「2021-22 新潟」")], ""),
    (P_OK, "ORG000109", "2022", "2025", [("okamoto", "クラブ所属履歴 > 「2022-23 A東京」〜「2024-25 A東京」")], ""),
    (P_OK, "ORG000155", "2025", "2026", [("okamoto", "クラブ所属履歴 > 「2025-26 島根」")], ""),
    (P_OK, "ORG000200", "2026", "", [("okamoto", "クラブ所属履歴 > 「2026-27 福井」")], "2026-27在籍中のため終了年なし"),
    (P_FALL, "ORG000194", "", "", [("fall_news", "本文：「延岡学園高校、関東学院大学を経て、当時bjリーグ所属の横浜ビー・コルセアーズでキャリアを始めた」")], "出身高校"),
    (P_FALL, "ORG000236", "", "", [("fall_news", "本文：「延岡学園高校、関東学院大学を経て…」")], "出身大学"),
    (P_FALL, "ORG000055", "2016", "2017", [("fall", "クラブ所属履歴 > 「2016-17 横浜」")], "略称「横浜」＝横浜ビー・コルセアーズ（記事の「横浜ビー・コルセアーズでキャリアを始めた」とも一致）"),
    (P_FALL, "ORG000040", "2017", "2018", [("fall", "クラブ所属履歴 > 「2017-18 福岡」")], ""),
    (P_FALL, "ORG000142", "2018", "2019", [("fall", "クラブ所属履歴 > 「2018-19 大阪」")], ""),
    (P_FALL, "ORG000092", "2019", "2021", [("fall", "クラブ所属履歴 > 「2019-20 北海道」〜「2020-21 北海道」")], ""),
    (P_FALL, "ORG000048", "2021", "2023", [("fall", "クラブ所属履歴 > 「2021-22 佐賀」〜「2022-23 佐賀」")], ""),
    (P_FALL, "ORG000052", "2023", "2025", [("fall", "クラブ所属履歴 > 「2023-24 新潟」〜「2024-25 新潟」")], ""),
    (P_FALL, "ORG000224", "2026", "", [("fall", "クラブ所属履歴 > 「2026-27 香川」")], "2026-27在籍中のため終了年なし"),
    ("P000064", "ORG000516", "2026", "", [("gleague", "Yuki Kawamura（PERSON_ID=1642530）：TEAM_CITY=San Diego、TEAM_NAME=Clippers、ROSTERSTATUS=1")],
     "NBA公式のGリーグ2026-27選手一覧に掲載。2026-27在籍中のため終了年なし"),
    ("P000495", "ORG000517", "", "", [("giambalvo", "本文：「西海学園高校卒」「高校は地元・長崎県の西海学園高校に進み」")], "出身高校"),
    ("P000421", "ORG000170", "", "", [("nagashima_wiki", "基本情報欄 > | 高校 = [[飛龍高等学校]]")], "出身高校"),
    ("P000463", "ORG000127", "", "", [("hasegawa_wiki", "基本情報欄 > |高校=[[福岡大学附属大濠高等学校]]")], "出身高校"),
    ("P000463", "ORG000054", "2013", "2016", [("hasegawa_wiki", "基本情報欄 > |所属1=[[名古屋ダイヤモンドドルフィンズ|三菱電機ダイヤモンドドルフィンズ名古屋]] |所属年1=2013-2016")],
     "B.LEAGUE開幕前（NBL）。リンク先＝名古屋ダイヤモンドドルフィンズ"),
]
# career, person, org name, old, new, [(source, locator)], summary
CORRECTIONS = [
    ("C001371", "P000308", "茨城ロボッツ", ("2017", ""), ("2017", "2027"),
     [("hirao", "クラブ所属履歴 > 「2017-18 茨城」〜「2026-27 茨城」"),
      ("hirao_retire", "本文：「9月27日(日)の三遠ネオフェニックス戦を最後に現役を引退する」"),
      ("hirao_role", "本文：「9月27日の三遠ネオフェニックス戦をもって…現役を引退しました」")],
     "2026-27シーズンのホーム開幕戦（2026-09-27）で現役を引退。終了年＝最後のシーズン2026-27の終了年"),
    ("C002686", "P000064", "ロサンゼルス・クリッパーズ", ("2026", ""), ("2026", "2027"),
     [("gleague", "Yuki Kawamura：Gリーグ2026-27はSan Diego Clippers（TEAM_ABBREVIATION=SDC）")],
     "クリッパーズの2026-27ロスター（2026-10-22確認）に掲載なし、Gリーグ傘下チームに所属。終了年＝2026-27の終了年（期間のルールどおり）"),
    ("C000129", "P000041", "ライジングゼファー福岡", ("", ""), ("2025", ""),
     [("kano", "クラブ所属履歴 > 「2025-26 福岡」〜「2026-27 福岡」（前行「2024-25 佐賀」）")],
     "B.LEAGUE公式の所属履歴で福岡への在籍開始シーズンを確認（2026-27在籍中のため終了年なし）"),
]
HOLDS = [
    ("P000064", "C002686", "SEASON_RULE", "河村勇輝のクリッパーズはキャンプ契約のみで2026-27の公式戦ロスターに入っていないが、期間のルール（終了＝最後のシーズンの終了年）により2026〜2027とした。契約解除日（報道では2026-10-12）は公式資料で未確認のため記録していない。", "NBA公式の取引記録で確認"),
    ("P000308", "C001371", "SEASON_RULE", "平尾充庸は2026-27シーズン開幕直後（2026-09-27）に引退したが、期間のルールにより終了年を2027とした。", "表示上の扱いを確認"),
    ("P000567", "P000567", "PRE_BLEAGUE_HISTORY", "ファイパプ月瑠のB.LEAGUE開幕前（bjリーグ横浜BC等、2011〜2016）の所属は今回は未確認。記事には「当時bjリーグ所属の横浜ビー・コルセアーズでキャリアを始めた」とある。2025-26は所属履歴に記載なし。", "クラブ公式・当時の記録で確認"),
    ("P000566", "P000566", "SOURCE_DIFFERENCE", "岡本飛竜の出身校はB.LEAGUE公式プロフィールに記載がなく、報道（バスケットボールキング）とWikipediaのみ。", "クラブ公式の発表で確認"),
    ("", "", "NOT_FOUND", "出身高校を確認できなかった：ジョシュ・ホーキンソン（大学公式ページが404）、ウィリアムス ニカ（校名の綴りが資料で揺れる）、狩野富成（前所属クラブのGMコメント中の記述のみ）、橋本拓哉（公式の表記が専門学校）、深水虎太郎・河田チリジ・エドワード・モリス・クーリバリ（見つからず）。", "公式資料で確認"),
]


def main() -> None:
    m_people = {r["person_id"]: r["name"] for r in read_csv(ROOT / "data/master/person.csv")}
    m_orgs = {r["organization_id"]: r["name"] for r in read_csv(ROOT / "data/master/organization.csv")}
    m_careers = {r["career_id"]: r for r in read_csv(ROOT / "data/master/career.csv")}
    errors = []
    for oid, name in NEW_ORGS.items():
        if oid in m_orgs or name in m_orgs.values():
            errors.append(f"{oid} {name}: exists")
    for pid, name, *_ in NEW_PERSONS:
        if pid in m_people or any(v.replace(" ", "") == name.replace(" ", "") for v in m_people.values()):
            errors.append(f"{pid} {name}: exists")
    orgs = dict(m_orgs) | NEW_ORGS
    sources, evidence, decisions, careers, corr, issues = {}, [], [], [], [], []

    def sid(key: str) -> str:
        if key not in sources:
            title, pub, url, _ = SOURCES[key]
            sources[key] = {"source_id": f"{P}S{len(sources) + 1:04d}", "title": title, "publisher": pub, "url": url, "accessed_at": CHECKED}
        return sources[key]["source_id"]

    def ev(etype: str, eid: str, field: str, value: str, key: str, loc: str, summary: str, note: str = "") -> None:
        if not SOURCES[key][3]:
            note = (note + "。" if note else "") + "公式以外の出典。Tier 2"
        evidence.append({"record_id": f"{P}E{len(evidence) + 1:04d}", "entity_type": etype, "entity_id": eid, "field_name": field,
                         "candidate_value": value, "source_id": sid(key), "source_locator": loc, "evidence_summary": summary,
                         "assessment": "SUPPORTED", "checked_at": CHECKED, "issue_note": note})

    persons = []
    for pid, name, birth, key, loc in NEW_PERSONS:
        persons.append({"person_id": pid, "name": name})
        ev("Person", pid, "name", name, key, "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認")
        ev("Person", pid, "birth_date", birth, key, loc, "B.LEAGUE公式プロフィールで生年月日を確認")
        decisions.append({"decision_id": f"{P}D{len(decisions) + 1:04d}", "entity_type": "Person", "entity_id": pid,
                          "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "name|birth_date", "held_fields": "",
                          "reason": "B.LEAGUE公式プロフィールで確認", "reviewed_at": CHECKED})
    names = m_people | {p["person_id"]: p["name"] for p in persons}
    for n, (pid, oid, start, end, refs, note) in enumerate(NEW_CAREERS):
        cid = f"C{FIRST_CAREER + n:06d}"
        if cid in m_careers:
            errors.append(f"{cid}: used")
        if pid not in names or oid not in orgs:
            errors.append(f"{cid}: unknown person/org")
            continue
        for c in m_careers.values():
            if c["person_id"] == pid and c["organization_id"] == oid and (not start or (c["start"] and c["start"] < (end or "9999") and (c["end"] or "9999") > start)):
                errors.append(f"{cid}: overlaps/duplicates MASTER {c['career_id']}")
        careers.append({"career_id": cid, "person_id": pid, "organization_id": oid, "role": "Player", "start": start, "end": end})
        for key, loc in refs:
            what = "出身校" if not start else "所属"
            ev("Career", cid, "organization_id", oid, key, loc, f"{orgs[oid]}への{what}を確認" + (f"（{note}）" if note else ""))
            ev("Career", cid, "role", "Player", key, loc, "選手としての所属")
            if start:
                ev("Career", cid, "start", start, key, loc, "最初のシーズンの開始年")
                if end:
                    ev("Career", cid, "end", end, key, loc, "最後のシーズンの終了年")
        fields = "organization_id|role" + ("|start" if start else "") + ("|end" if end else "")
        held = "" if (start and end) else ("end" if start else "start|end")
        decisions.append({"decision_id": f"{P}D{len(decisions) + 1:04d}", "entity_type": "Career", "entity_id": cid,
                          "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": fields, "held_fields": held,
                          "reason": "；".join(SOURCES[k][1] for k, _ in refs), "reviewed_at": CHECKED})
    for cid, pid, oname, old, new, refs, summary in CORRECTIONS:
        m = m_careers.get(cid)
        if not m or m["person_id"] != pid or (m["start"], m["end"]) != old or m_orgs[m["organization_id"]] != oname:
            errors.append(f"{cid}: MASTER differs")
            continue
        for key, loc in refs:
            for field, o, nv in (("start", old[0], new[0]), ("end", old[1], new[1])):
                if o != nv:
                    ev("Career", cid, field, nv, key, loc, summary, "既存MASTER Careerの期間の訂正案")
        corr.append({"career_id": cid, "person_id": pid, "organization_name": oname, "old_start": old[0], "old_end": old[1],
                     "new_start": new[0], "new_end": new[1], "reason": summary})
    for i, (pid, rel, t, d, nx) in enumerate(HOLDS, 1):
        issues.append({"issue_id": f"{P}I{i:04d}", "person_id": pid, "related_id": rel, "issue_type": t, "status": "HOLD",
                       "description": d, "next_check": nx})
    if errors:
        raise SystemExit("; ".join(errors))
    used = {c["organization_id"] for c in careers}
    write_csv(OUT / "person_candidates.csv", ["person_id", "name"], persons)
    write_csv(OUT / "organization_candidates.csv", ["organization_id", "name"], [{"organization_id": o, "name": orgs[o]} for o in sorted(used)])
    write_csv(OUT / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], list(sources.values()))
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
    write_csv(OUT / "qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields",
                                         "reason", "reviewed_at"], decisions)
    write_csv(OUT / "master_corrections.csv", ["career_id", "person_id", "organization_name", "old_start", "old_end",
                                               "new_start", "new_end", "reason"], corr)
    print(f"batch_037 wave_01: persons={len(persons)} careers={len(careers)} corrections={len(corr)} evidence={len(evidence)} "
          f"sources={len(sources)} issues={len(issues)}")


if __name__ == "__main__":
    main()
