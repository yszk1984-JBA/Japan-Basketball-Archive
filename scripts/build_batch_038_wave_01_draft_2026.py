#!/usr/bin/env python3
"""Build batch_038 Wave 1: B.LEAGUE DRAFT 2026 players, CANDIDATE.

Yuichi (2026-10-29): 「今年のＢリーグドラフトの選手のリサーチお願い致します」→ chose
「DRAFT 2026の14名を深掘り」 (the 11 draftees and the 3 youth-priority signings).
All 14 are already MASTER persons with the official 2026-27 club. This wave adds:
- the draft result as a Person fact (field `draft`), from the B.LEAGUE report;
- the university year at the time of the draft as a Career detail (field `grade`);
- the loan / development-contract status of 岩下准平, 田中流嘉州 and 堀田尚秀
  (field `contract_type`) from the club announcements;
- university periods: 田中流嘉州 from the club's career table (2022-26); for the
  others an estimate from the official year at the draft (4th year in academic
  year 2025 → April 2022 - March 2026; 2nd year → from April 2024), marked
  「推定値（学年表記から）」 in the same way as the birth-date estimates
  (Yuichi's exception, 2026-10-25);
- 山﨑一渉: his first US university (ラドフォード大学, new Organization) and the
  period of ノーザンコロラド大学 (transfer in April 2025, through 2025-26).
Raw: data/raw/research/draft_2026_2026-10-29.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_038/wave_01"
CHECKED = "2026-10-29"
P = "B38W1"
EST = "推定値（学年表記から）：ドラフト時の学年から在学期間を算出（Yuichiの方針 2026-10-25の推定の扱いに準じる）。資料で確認した期間ではない"

SOURCES = {
    "report": ("B.LEAGUE DRAFT 2026レポート…SR渋谷が山﨑一渉を1位指名（2026-01-30）", "B.LEAGUE（B.MAGAZINE）", "https://www.bleague.jp/bmagazine/detail/id=545053"),
    "shiga_draft": ("「B.LEAGUE DRAFT 2026」指名選手及び、長崎ヴェルカとの連携合意について（2026-01-29）", "滋賀レイクス（クラブ公式）", "https://shigalakes.com/news/detail/id=22061"),
    "shiga_iwashita": ("岩下准平選手 特別指定選手として加入および期限付移籍について", "滋賀レイクス（クラブ公式）", "https://shigalakes.com/news/detail/id=22082"),
    "shiga_tanaka": ("田中流嘉州選手 長崎ヴェルカへ期限付き移籍のお知らせ（2026-06-22）", "滋賀レイクス（クラブ公式）", "https://shigalakes.com/news/detail/id=24887"),
    "velca_iwashita": ("岩下准平 選手契約基本合意および期限付移籍のお知らせ（2026-06-22）", "長崎ヴェルカ（クラブ公式）", "https://www.velca.jp/news/detail/id=50765"),
    "akita_hotta": ("【Bリーグドラフト】堀田尚秀選手 2026-27シーズン契約合意のお知らせ", "秋田ノーザンハピネッツ（クラブ公式）", "https://northern-happinets.com/news/detail/id=19863"),
    "waseda": ("バスケットボール部男子 岩屋主将、堀田副将がプロの世界へ！秋田ノーザンハピネッツと契約（2026-02-19）", "早稲田大学 競技スポーツセンター（大学公式）", "https://www.waseda.jp/inst/athletic/news/2026/02/19/55864/"),
    "kyoto": ("西部秀馬選手 特別指定選手のプロ契約として加入（2026-02-06）", "京都ハンナリーズ（クラブ公式）", "https://hannaryz.jp/news/detail/id=21939"),
    "yokohama": ("新井楽人選手 2026-27シーズン 選手契約締結および特別指定選手登録のお知らせ（2026-02-10）", "横浜ビー・コルセアーズ（クラブ公式）", "https://b-corsairs.com/news/team_20260210_0/"),
    "toyama": ("泉登翔選手 特別指定選手登録のお知らせ（2026-02-12）", "富山グラウジーズ（クラブ公式）", "https://grouses.jp/news/detail/id=21735"),
    "ibaraki": ("#12 赤間賢人選手 特別指定選手として登録（2026-02-03）", "茨城ロボッツ（クラブ公式）", "https://www.ibarakirobots.win/news/20260203_04_team/"),
    "sr": ("「B.LEAGUE DRAFT 2026」1巡目1位指名でノーザンコロラド大・山﨑一渉選手の交渉権を獲得（2026-01-29）", "東京サンロッカーズ（クラブ公式）", "https://www.sunrockers.jp/news/detail/id=20029"),
}
REPORT_LOC = "B.LEAGUE DRAFT 2026指名選手一覧"
DRAFT = [  # person, value, locator
    ("P000345", "B.LEAGUE DRAFT 2026 1巡目・全体1位（サンロッカーズ渋谷）", "全体1位：サンロッカーズ渋谷→山﨑一渉（ノーザン・コロラド大学）"),
    ("P000185", "B.LEAGUE DRAFT 2026 1巡目・全体2位（茨城ロボッツ）", "全体2位：茨城ロボッツ→赤間賢人（東海大学）"),
    ("P000248", "B.LEAGUE DRAFT 2026 1巡目・全体3位（横浜ビー・コルセアーズ）", "全体3位：横浜ビー・コルセアーズ→新井楽人（日本大学）"),
    ("P000125", "B.LEAGUE DRAFT 2026 1巡目・全体4位（長崎ヴェルカ）", "全体4位：長崎ヴェルカ→岩下准平（筑波大学）"),
    ("P000138", "B.LEAGUE DRAFT 2026 1巡目・全体5位（秋田ノーザンハピネッツ）", "全体5位：秋田ノーザンハピネッツ→岩屋頼（早稲田大学）"),
    ("P000333", "B.LEAGUE DRAFT 2026 1巡目・全体6位（広島ドラゴンフライズ）", "全体6位：広島ドラゴンフライズ→松野遥弥（専修大学）"),
    ("P000163", "B.LEAGUE DRAFT 2026 2巡目・全体7位（京都ハンナリーズ）", "全体7位：京都ハンナリーズ→西部秀馬（日本体育大学）"),
    ("P000378", "B.LEAGUE DRAFT 2026 2巡目・全体8位（滋賀レイクス）", "全体8位：滋賀レイクス→田中流嘉州（大東文化大学）"),
    ("P000162", "B.LEAGUE DRAFT 2026 3巡目・全体9位（秋田ノーザンハピネッツ）", "全体9位：秋田ノーザンハピネッツ→堀田尚秀（早稲田大学）"),
    ("P000116", "B.LEAGUE DRAFT 2026 3巡目・全体10位（富山グラウジーズ）", "全体10位：富山グラウジーズ→泉登翔（日本大学）"),
    ("P000366", "B.LEAGUE DRAFT 2026 3巡目・全体11位（佐賀バルーナーズ）", "全体11位：佐賀バルーナーズ→武富楓太（東海大学九州）"),
    ("P000286", "B.LEAGUE DRAFT 2026 ユース優先交渉権によりトップチームと契約（レバンガ北海道）", "本文：「レバンガ北海道 U18の西村優真…」（ドラフトを経由せず「ユース優先交渉権」でトップチームと契約）"),
    ("P000239", "B.LEAGUE DRAFT 2026 ユース優先交渉権によりトップチームと契約（仙台89ERS）", "本文：「仙台89ERS U18の阿部真冴橙…」（ドラフトを経由せず「ユース優先交渉権」でトップチームと契約）"),
    ("P000362", "B.LEAGUE DRAFT 2026 ユース優先交渉権によりトップチームと契約（名古屋ダイヤモンドドルフィンズ）", "本文：「名古屋D U18の若野瑛太…」（ドラフトを経由せず「ユース優先交渉権」でトップチームと契約）"),
]
# career, field, value, [(source, locator)]
DETAILS = [
    ("C001070", "grade", "4年（2025年度、ドラフト時）", [("yokohama", "本文：「副キャプテンを務めた大学4年時」、出身校「…→日本大学 在学中」")]),
    ("C000432", "grade", "4年（2025年度、ドラフト時）", [("shiga_draft", "本文：「岩下准平選手（筑波大学4年）」")]),
    ("C000470", "grade", "4年（2025年度、ドラフト時）", [("waseda", "本文：「2025年度主将の岩屋頼（スポーツ科学部4年）」")]),
    ("C000540", "grade", "4年（2025年度、ドラフト時）", [("waseda", "本文：「副将の堀田尚秀（スポーツ科学部4年）」")]),
    ("C000543", "grade", "4年（2025年度、ドラフト時）", [("kyoto", "本文：「西部秀馬選手(日本体育大学/4年生)」")]),
    ("C000406", "grade", "4年（2025年度、ドラフト時）", [("toyama", "本文：「日本大学4年の泉登翔です」")]),
    ("C000609", "grade", "2年（2025年度、ドラフト時）", [("ibaraki", "本文：「昨年12月に大学2年生にしてドラフトエントリーを発表」")]),
    ("C002704", "grade", "4年（2025年度、ドラフト時）", [("shiga_draft", "本文：「田中流嘉洲選手（大東文化大学4年）を指名」")]),
    ("C000433", "contract_type", "長崎ヴェルカから期限付移籍（育成契約選手制度、2026-27シーズンから）",
     [("shiga_iwashita", "本文：「長崎ヴェルカとの選手契約を締結し、「育成契約選手制度」に基づいて2026-27シーズンは滋賀レイクスへ期限付移籍」"),
      ("velca_iwashita", "本文：「「育成契約選手制度」に基づき、岩下准平選手との契約基本合意および滋賀レイクスへの期限付移籍が決定」")]),
    ("C001699", "contract_type", "滋賀レイクスから期限付移籍（育成契約選手制度、2026-27シーズンから）",
     [("shiga_tanaka", "本文：「「育成契約選手制度」に基づき、同シーズンから長崎ヴェルカへ期限付き移籍」「契約期間は2028-29シーズンまでの3年契約」")]),
    ("C000541", "contract_type", "育成契約選手制度（2026-27シーズンから3シーズン）",
     [("akita_hotta", "本文：「契約期間は2026-27シーズンからの3シーズンで、「育成契約選手制度」を用いた契約」")]),
]
# career, person, org, (old), (new), estimate?, [(source, locator)], summary
PERIODS = [
    ("C002704", "P000378", "大東文化大学", ("", ""), ("2022", "2026"), False, [("shiga_tanaka", "経歴：「2022-26 大東文化大学」")], "クラブ公式の経歴表の在学期間"),
    ("C001070", "P000248", "日本大学", ("", ""), ("2022", "2026"), True,
     [("yokohama", "主な経歴：「2022年 ・第62回関東大学バスケットボール新人戦 準優勝」、本文：「大学4年時」")], "2025年度に4年 → 2022年4月入学・2026年3月までの在学と算出"),
    ("C000432", "P000125", "筑波大学", ("", ""), ("2022", "2026"), True, [("shiga_draft", "本文：「岩下准平選手（筑波大学4年）」")], "2025年度に4年 → 2022〜2026と算出"),
    ("C000470", "P000138", "早稲田大学", ("", ""), ("2022", "2026"), True, [("waseda", "本文：「2025年度主将の岩屋頼（スポーツ科学部4年）」")], "2025年度に4年 → 2022〜2026と算出"),
    ("C000540", "P000162", "早稲田大学", ("", ""), ("2022", "2026"), True, [("waseda", "本文：「副将の堀田尚秀（スポーツ科学部4年）」")], "2025年度に4年 → 2022〜2026と算出"),
    ("C000543", "P000163", "日本体育大学", ("", ""), ("2022", "2026"), True, [("kyoto", "本文：「西部秀馬選手(日本体育大学/4年生)」")], "2025年度に4年 → 2022〜2026と算出"),
    ("C000406", "P000116", "日本大学", ("", ""), ("2022", "2026"), True, [("toyama", "本文：「日本大学4年の泉登翔です」")], "2025年度に4年 → 2022〜2026と算出"),
    ("C000609", "P000185", "東海大学", ("", ""), ("2024", ""), True, [("ibaraki", "本文：「昨年12月に大学2年生にしてドラフトエントリーを発表」「東海大学でも1年時から」")],
     "2025年度に2年 → 2024年4月入学と算出。終了年（卒業・退部）は不明"),
    ("C002702", "P000345", "ノーザンコロラド大学", ("", ""), ("2025", "2026"), False, [("sr", "本文：「昨年4月にはノーザンコロラド大学へ転校」（2026-01-29掲載）")],
     "2025年4月に転校、2025-26シーズンまで（2026-27は東京サンロッカーズ）"),
]
NEW_ORG = ("ORG000518", "ラドフォード大学")
NEW_CAREER = ("C002829", "P000345", "sr", "本文：「全米大学体育協会（NCAA）1部のラドフォード大学へ進学」")
HOLDS = [
    ("P000333", "松野遥弥・武富楓太の大学の学年は報道（媒体）のみで、公式資料では未確認。大学の期間・学年は登録していない。"),
    ("P000185", "赤間賢人の東海大学の終了年（卒業・退部）は未確認。開始年のみ推定。"),
    ("P000345", "山﨑一渉のラドフォード大学の在学期間（進学年・転校年）は記載がなく未確認。"),
    ("P000116", "泉登翔・山﨑一渉のプロ契約の期間はクラブ公式で未確認（Careerの期間には影響しない）。"),
]


def main() -> None:
    m_people = {r["person_id"]: r["name"] for r in read_csv(ROOT / "data/master/person.csv")}
    m_orgs = {r["organization_id"]: r["name"] for r in read_csv(ROOT / "data/master/organization.csv")}
    m_careers = {r["career_id"]: r for r in read_csv(ROOT / "data/master/career.csv")}
    m_ev = read_csv(ROOT / "data/master/evidence.csv")
    errors = []
    sources, evidence, corr, issues = {}, [], [], []

    def sid(key: str) -> str:
        if key not in sources:
            t, pub, url = SOURCES[key]
            sources[key] = {"source_id": f"{P}S{len(sources) + 1:04d}", "title": t, "publisher": pub, "url": url, "accessed_at": CHECKED}
        return sources[key]["source_id"]

    def ev(etype: str, eid: str, field: str, value: str, key: str, loc: str, summary: str, note: str = "") -> None:
        evidence.append({"record_id": f"{P}E{len(evidence) + 1:04d}", "entity_type": etype, "entity_id": eid, "field_name": field,
                         "candidate_value": value, "source_id": sid(key), "source_locator": loc, "evidence_summary": summary,
                         "assessment": "SUPPORTED", "checked_at": CHECKED, "issue_note": note})

    for pid, value, loc in DRAFT:
        if pid not in m_people:
            errors.append(f"{pid}: not in MASTER")
        if any(e["entity_id"] == pid and e["field_name"] == "draft" for e in m_ev):
            errors.append(f"{pid}: draft already in MASTER")
        ev("Person", pid, "draft", value, "report", f"{REPORT_LOC if '→' in loc else '本文'} > {loc}", "B.LEAGUE公式のドラフトレポートで指名（またはユース優先交渉権による契約）を確認")
    for cid, field, value, refs in DETAILS:
        if cid not in m_careers:
            errors.append(f"{cid}: not in MASTER")
        for key, loc in refs:
            ev("Career", cid, field, value, key, loc, "クラブ・大学の公式発表で確認")
    for cid, pid, oname, old, new, est, refs, summary in PERIODS:
        m = m_careers.get(cid)
        if not m or m["person_id"] != pid or (m["start"], m["end"]) != old or m_orgs[m["organization_id"]] != oname:
            errors.append(f"{cid}: MASTER differs")
            continue
        for key, loc in refs:
            for field, o, nv in (("start", old[0], new[0]), ("end", old[1], new[1])):
                if o != nv:
                    ev("Career", cid, field, nv, key, loc, summary, EST if est else "既存MASTER Careerの期間の訂正案")
        corr.append({"career_id": cid, "person_id": pid, "organization_name": oname, "old_start": old[0], "old_end": old[1],
                     "new_start": new[0], "new_end": new[1], "reason": ("推定（学年表記から）：" if est else "") + summary})
    oid, oname = NEW_ORG
    if oid in m_orgs or oname in m_orgs.values():
        errors.append(f"{oid}: exists")
    cid, pid, key, loc = NEW_CAREER
    if cid in m_careers:
        errors.append(f"{cid}: used")
    careers = [{"career_id": cid, "person_id": pid, "organization_id": oid, "role": "Player", "start": "", "end": ""}]
    ev("Career", cid, "organization_id", oid, key, loc, "クラブ公式の発表で進学先を確認")
    ev("Career", cid, "role", "Player", key, loc, "大学の選手として")
    for i, (p, d) in enumerate(HOLDS, 1):
        issues.append({"issue_id": f"{P}I{i:04d}", "person_id": p, "related_id": p, "issue_type": "NOT_CONFIRMED", "status": "HOLD",
                       "description": d, "next_check": "公式資料で確認"})
    if errors:
        raise SystemExit("; ".join(errors))
    write_csv(OUT / "organization_candidates.csv", ["organization_id", "name"], [{"organization_id": oid, "name": oname}])
    write_csv(OUT / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], careers)
    write_csv(OUT / "master_corrections.csv", ["career_id", "person_id", "organization_name", "old_start", "old_end",
                                               "new_start", "new_end", "reason"], corr)
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], list(sources.values()))
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
    print(f"batch_038 wave_01: draft facts={len(DRAFT)} details={len(DETAILS)} periods={len(corr)} new careers=1 "
          f"evidence={len(evidence)} sources={len(sources)} issues={len(issues)}")


if __name__ == "__main__":
    main()
