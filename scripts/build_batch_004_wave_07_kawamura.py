#!/usr/bin/env python3
"""Build batch_004 Wave 7: NBA update for 河村勇輝 (P000064), CANDIDATE.

Yuichi (2026-10-03): 「河村勇輝の情報をアップデートして　特にNBA情報」.
河村 was registered in batch_004, so the update goes into that batch
(per-origin rule, docs/HISTORICAL_CAREER_DEEPENING_LOG.md).

Primary sources are NBA.com's own data (stats.nba.com career totals and
team rosters, read in the browser on 2026-10-03) and NBA G League official
news. Raw values: data/raw/research/nba_kawamura_2026-10-03.md.

- Careers use the season rule of batch_031: start = first season's start
  year, end = last season's end year, no end while on a 2026-27 roster.
- The two Bulls two-way contracts (2025-07 and 2026-01) fall in one season
  (2025-26) and are one Career; the waiver in between is an issue.
- wave_05's three Careers (media/blog sources, month-format dates) are
  withdrawn (REJECT_CANDIDATE) and replaced.
- Periods for three existing MASTER Careers (三遠, 横浜BC, グリズリーズ) are
  proposed as MASTER corrections (master_corrections.csv); MASTER is not
  changed here.
- Reasons for the 2025-10 waiver (reported as health-related) are not
  recorded (掲載しない項目).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import read_csv, write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/candidate/batch_004/wave_07"
CHECKED = "2026-10-03"
PID = "P000064"
P = "B4W7"

SOURCES = [
    ("S0001", "Yuki Kawamura 通算成績（レギュラーシーズン、シーズン別）", "NBA.com（stats.nba.com）",
     "https://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=Totals&PlayerID=1642530"),
    ("S0002", "Memphis Grizzlies ロスター 2024-25", "NBA.com（stats.nba.com）",
     "https://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2024-25&TeamID=1610612763"),
    ("S0003", "Chicago Bulls ロスター 2025-26", "NBA.com（stats.nba.com）",
     "https://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2025-26&TeamID=1610612741"),
    ("S0004", "LA Clippers ロスター 2026-27", "NBA.com（stats.nba.com）",
     "https://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2026-27&TeamID=1610612746"),
    ("S0005", "Bulls Sign Yuki Kawamura To Two-Way Contract（2025-07-19）", "NBA G League",
     "https://gleague.nba.com/news/bulls-sign-yuki-kawamura-to-two-way-contract"),
    ("S0006", "Chicago Bulls Sign Yuki Kawamura To Two-Way Contract（2026-01）", "NBA G League",
     "https://gleague.nba.com/news/chicago-bulls-sign-yuki-kawamura-to-two-way-contract"),
    ("S0007", "2025-26 Chicago Bulls Transactions", "Basketball-Reference",
     "https://www.basketball-reference.com/teams/CHI/2026_transactions.html"),
    ("S0008", "Yuki Kawamura 選手ページ", "NBA.com",
     "https://www.nba.com/player/1642530/yuki-kawamura/profile"),
    ("S0009", "河村勇輝 選手プロフィール（クラブ所属履歴）", "B.LEAGUE",
     "https://www.bleague.jp/roster_detail/?PlayerID=30460"),
]
ACCESSED = {"S0009": "2026-09-29"}

CAREERS = [
    {"career_id": "C002685", "person_id": PID, "organization_id": "ORG000139", "role": "Player", "start": "2025", "end": "2026"},
    {"career_id": "C002686", "person_id": PID, "organization_id": "ORG000140", "role": "Player", "start": "2026", "end": ""},
]
ORGS = [("ORG000139", "シカゴ・ブルズ"), ("ORG000140", "ロサンゼルス・クリッパーズ")]

# (entity, field, value, source, locator, summary)
EVIDENCE = [
    ("C002685", "organization_id", "ORG000139", "S0001", "SEASON_ID 2025-26 / TEAM_ABBREVIATION CHI / GP 18",
     "NBA公式の通算成績で2025-26シーズンのシカゴ・ブルズ在籍（18試合出場）を確認"),
    ("C002685", "organization_id", "ORG000139", "S0003", "PLAYER Yuki Kawamura / NUM 8 / HOW_ACQUIRED Signed on 07/19/25",
     "NBA公式の2025-26ロスターに掲載"),
    ("C002685", "role", "Player", "S0005", "本文：has signed guard Yuki Kawamura … to a two-way contract",
     "NBA G League公式ニュースで選手契約（two-way契約）を確認"),
    ("C002685", "start", "2025", "S0003", "HOW_ACQUIRED：Signed on 07/19/25", "2025年7月19日（現地）の契約で2025-26シーズンから在籍"),
    ("C002685", "start", "2025", "S0005", "公開日2025-07-19・本文：signed … to a two-way contract", "NBA G League公式ニュースで契約を確認"),
    ("C002685", "end", "2026", "S0001", "SEASON_ID 2025-26がCHIの最後の行", "2025-26シーズンの終了年"),
    ("C002685", "end", "2026", "S0004", "2026-27はLA Clippersのロスター（Signed on 08/08/26）", "次シーズンは別クラブに在籍"),
    ("C002686", "organization_id", "ORG000140", "S0004", "PLAYER Yuki Kawamura / NUM 8 / HOW_ACQUIRED Signed on 08/08/26",
     "NBA公式の2026-27ロスターに掲載"),
    ("C002686", "organization_id", "ORG000140", "S0008", "選手ページ見出し：LA Clippers", "NBA公式の選手ページの現所属"),
    ("C002686", "role", "Player", "S0004", "POSITION G", "選手として掲載"),
    ("C002686", "start", "2026", "S0004", "HOW_ACQUIRED：Signed on 08/08/26", "2026年8月8日（現地）の契約で2026-27シーズンから在籍"),
]
# Proposed MASTER corrections (periods only; organization unchanged).
CORRECTIONS = [
    ("C000221", "三遠ネオフェニックス", "", "", "2019", "2020", "S0009", "クラブ所属履歴 >「2019-20 三遠」（この1行のみ）",
     "B.LEAGUE公式の所属履歴は2019-20の1シーズン（batch_031 issue B31W1I0019）"),
    ("C000222", "横浜ビー・コルセアーズ", "", "", "2020", "2024", "S0009", "クラブ所属履歴 >「2020-21 横浜BC」〜「2023-24 横浜BC」",
     "B.LEAGUE公式の所属履歴は2020-21〜2023-24（batch_031 issue B31W1I0020）"),
    ("C000223", "メンフィス・グリズリーズ", "", "", "2024", "2025", "S0001", "SEASON_ID 2024-25 / TEAM_ABBREVIATION MEM / GP 22",
     "NBA公式の通算成績で2024-25シーズンのみ在籍（22試合出場）。2024-25ロスター（S0002）にも掲載"),
]
ISSUES = [
    ("C002685", "CONTRACT_HISTORY",
     "シカゴ・ブルズとは2025-26シーズン中に2回two-way契約を結んでいる（2025-07-19、2026-01-06。NBA G League公式ニュース）。間の2025-10-17に契約解除（Basketball-Referenceの記録。公式発表は未確認）。シーズン単位の登録ルールにより1件のCareer（2025〜2026）とした。解除の理由は記録しない。",
     "球団公式の発表で解除日を確認。契約単位の記録が必要になればスキーマを検討"),
    ("C002686", "STATUS_VOLATILE",
     "ロサンゼルス・クリッパーズとの契約はExhibit 10契約（報道：NBC Sports 2026-08-09、バスケットボールキング 2026-09-28）。2026-09-30からトレーニングキャンプで、レギュラーシーズン開幕までにtwo-way契約への転換や契約解除がありうる。",
     "2026-27レギュラーシーズン開幕後にNBA公式ロスターで再確認"),
    (PID, "G_LEAGUE_ASSIGNMENTS",
     "グリズリーズ・ブルズ在籍中のGリーグ（メンフィス・ハッスル、ウィンディシティ・ブルズ）への派遣は、NBAクラブとの契約の一部のため別Careerにしていない。",
     "Gリーグ在籍を記録するかはYuichiと方針を決める"),
]


def main() -> None:
    sources = [{"source_id": f"{P}{sid}", "title": t, "publisher": pub, "url": url,
                "accessed_at": ACCESSED.get(sid, CHECKED)} for sid, t, pub, url in SOURCES]
    evidence = []
    for i, (eid, field, value, sid, loc, summary) in enumerate(EVIDENCE, 1):
        evidence.append({"record_id": f"{P}E{i:04d}", "entity_type": "Career", "entity_id": eid, "field_name": field,
                         "candidate_value": value, "source_id": f"{P}{sid}", "source_locator": loc,
                         "evidence_summary": summary, "assessment": "SUPPORTED", "checked_at": CHECKED, "issue_note": ""})
    corr_rows = []
    n = len(evidence)
    for cid, org, os_, oe, ns, ne, sid, loc, why in CORRECTIONS:
        for field, value in (("start", ns), ("end", ne)):
            n += 1
            evidence.append({"record_id": f"{P}E{n:04d}", "entity_type": "Career", "entity_id": cid, "field_name": field,
                             "candidate_value": value, "source_id": f"{P}{sid}", "source_locator": loc,
                             "evidence_summary": why, "assessment": "SUPPORTED", "checked_at": CHECKED,
                             "issue_note": "既存MASTER Careerの期間の訂正案（master_corrections.csv）"})
        corr_rows.append({"career_id": cid, "person_id": PID, "organization_name": org, "old_start": os_, "old_end": oe,
                          "new_start": ns, "new_end": ne, "reason": why})
    decisions = [
        {"decision_id": f"{P}D0001", "entity_type": "Career", "entity_id": "C002685", "decision": "READY_FOR_VERIFIED_REVIEW",
         "eligible_fields": "organization_id|role|start|end", "held_fields": "",
         "reason": "NBA公式の通算成績・ロスターとNBA G League公式ニュースで確認", "reviewed_at": CHECKED},
        {"decision_id": f"{P}D0002", "entity_type": "Career", "entity_id": "C002686", "decision": "READY_FOR_VERIFIED_REVIEW",
         "eligible_fields": "organization_id|role|start", "held_fields": "end",
         "reason": "NBA公式の2026-27ロスターと選手ページで確認。在籍中のため終了年なし", "reviewed_at": CHECKED},
    ]
    for i, cid in enumerate(("C000327", "C000328", "C000329"), 3):
        decisions.append({"decision_id": f"{P}D{i:04d}", "entity_type": "Career", "entity_id": cid, "decision": "REJECT_CANDIDATE",
                          "eligible_fields": "", "held_fields": "",
                          "reason": "wave_05のCareer（報道・個人サイトが出典、年月形式の期間）を、NBA公式資料によるシーズン単位のCareer（C002685・C002686）に置き換えたため取り下げ",
                          "reviewed_at": CHECKED})
    issues = [{"issue_id": f"{P}I{i:04d}", "person_id": PID, "related_id": rel, "issue_type": t, "status": "HOLD",
               "description": d, "next_check": nc} for i, (rel, t, d, nc) in enumerate(ISSUES, 1)]

    # structural checks
    errors = []
    used = {e["source_id"] for e in evidence}
    if used - {s["source_id"] for s in sources}:
        errors.append("unknown source")
    existing = {r["career_id"] for r in read_csv(ROOT / "data/master/career.csv")}
    for path in (ROOT / "data/candidate").rglob("career_candidates.csv"):
        if OUT in path.parents:
            continue
        existing |= {r["career_id"] for r in read_csv(path)}
    if {c["career_id"] for c in CAREERS} & existing:
        errors.append("Career ID already used")
    master = {r["career_id"]: r for r in read_csv(ROOT / "data/master/career.csv")}
    for c in corr_rows:
        m = master[c["career_id"]]
        if (m["start"], m["end"]) != (c["old_start"], c["old_end"]) or m["person_id"] != PID:
            errors.append(f"{c['career_id']}: MASTER value differs from old value")
    wave5 = {r["career_id"] for r in read_csv(ROOT / "data/candidate/batch_004/wave_05/career_candidates.csv")}
    if not {"C000327", "C000328", "C000329"} <= wave5:
        errors.append("wave_05 careers missing")
    if errors:
        raise SystemExit("; ".join(errors))

    write_csv(OUT / "person_candidates.csv", ["person_id", "name"], [])
    write_csv(OUT / "organization_candidates.csv", ["organization_id", "name"], [{"organization_id": o, "name": n} for o, n in ORGS])
    write_csv(OUT / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], CAREERS)
    write_csv(OUT / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], sources)
    write_csv(OUT / "evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
                                             "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write_csv(OUT / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issues)
    write_csv(OUT / "qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields",
                                         "reason", "reviewed_at"], decisions)
    write_csv(OUT / "master_corrections.csv", ["career_id", "person_id", "organization_name", "old_start", "old_end",
                                               "new_start", "new_end", "reason"], corr_rows)
    print(f"wave_07: careers={len(CAREERS)} evidence={len(evidence)} sources={len(sources)} issues={len(issues)} "
          f"rejects=3 master_corrections={len(corr_rows)}")


if __name__ == "__main__":
    main()
