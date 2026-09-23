#!/usr/bin/env python3
"""Build Batch 007 Wave 1 CANDIDATE data.

Scope-widening experiment approved by Yuichi (2026-09-23): B.LEAGUE
players are no longer limited to Fukuoka Daiichi alumni. This wave
tests jba_lib on 4 well-known B.LEAGUE players picked without any
Fukuoka Daiichi connection, using the minimum-viable Career chain
(high school -> university -> CURRENT club only; older club stops are
intentionally left out, see note below) to measure how much research
one wave actually takes.

Persons (none previously touched by any batch -- checked against
Master + every candidate/verified person file before writing this):
- 富樫勇樹 (Yuki Togashi, 千葉ジェッツ)
- 比江島慎 (Makoto Hiejima, 宇都宮ブレックス)
- 篠山竜青 (Ryusei Shinoyama, 川崎ブレイブサンダース)
- 齋藤拓実 (Takumi Saito, 名古屋ダイヤモンドドルフィンズ)

Deliberate scope decision: only the CURRENT club is recorded as a
Career, not each historical team stop (e.g. 比江島慎's 三河/栃木
stints before 宇都宮). Several of those historical club names are
pre-rename/pre-merger identities of clubs already in
organization.csv (the same "OrganizationAlias・継承ルール" gap flagged
and left unresolved in Batch 004's B4W3I0011 issue). Deciding that
policy is out of scope for this wave; recording only the unambiguous
current affiliation avoids repeating the ORG000017/ORG000019 mistake
under a different name.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_007" / "wave_01"
CHECKED_AT = "2026-09-23"

PERSONS = [
    {"person_id": "P000083", "name": "富樫勇樹"},
    {"person_id": "P000084", "name": "比江島慎"},
    {"person_id": "P000085", "name": "篠山竜青"},
    {"person_id": "P000086", "name": "齋藤拓実"},
]

# organization_id -> name. ORG000030/ORG000047/ORG000054 already exist
# in data/master/organization.csv (青山学院大学 / 宇都宮ブレックス /
# 名古屋ダイヤモンドドルフィンズ) and are reused, not re-minted --
# checked with jba_lib.organizations.find_organization_id_by_exact_name
# before writing this file.
ORGANIZATIONS = [
    {"organization_id": "ORG000117", "name": "モントロス・クリスチャン高等学校"},
    {"organization_id": "ORG000118", "name": "千葉ジェッツ"},
    {"organization_id": "ORG000119", "name": "洛南高等学校"},
    {"organization_id": "ORG000030", "name": "青山学院大学"},
    {"organization_id": "ORG000047", "name": "宇都宮ブレックス"},
    {"organization_id": "ORG000120", "name": "北陸高等学校"},
    {"organization_id": "ORG000121", "name": "日本大学"},
    {"organization_id": "ORG000122", "name": "川崎ブレイブサンダース"},
    {"organization_id": "ORG000123", "name": "桐光学園高校"},
    {"organization_id": "ORG000124", "name": "明治大学"},
    {"organization_id": "ORG000054", "name": "名古屋ダイヤモンドドルフィンズ"},
]

CAREERS = [
    {"career_id": "C000299", "person_id": "P000083", "organization_id": "ORG000117", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000300", "person_id": "P000083", "organization_id": "ORG000118", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000290", "person_id": "P000084", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000291", "person_id": "P000084", "organization_id": "ORG000030", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000292", "person_id": "P000084", "organization_id": "ORG000047", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000296", "person_id": "P000085", "organization_id": "ORG000120", "role": "Player", "start": "2004", "end": ""},
    {"career_id": "C000297", "person_id": "P000085", "organization_id": "ORG000121", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000298", "person_id": "P000085", "organization_id": "ORG000122", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000293", "person_id": "P000086", "organization_id": "ORG000123", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000294", "person_id": "P000086", "organization_id": "ORG000124", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000295", "person_id": "P000086", "organization_id": "ORG000054", "role": "Player", "start": "", "end": ""},
]

SOURCES = [
    {"source_id": "B7S0001", "title": "富樫勇樹 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=9055", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0002", "title": "比江島慎 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8589", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0003", "title": "篠山竜青 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8484", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0004", "title": "篠山竜青 川崎ブレイブサンダース公式選手プロフィール", "publisher": "川崎ブレイブサンダース", "url": "https://kawasaki-bravethunders.com/team/players/detail/id=8224?PlayerID=8484", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0005", "title": "齋藤拓実 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=14301", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0006", "title": "齋藤拓実 名古屋ダイヤモンドドルフィンズ公式選手プロフィール", "publisher": "名古屋ダイヤモンドドルフィンズ", "url": "https://nagoya-dolphins.jp/team/players/detail/id=14611?PlayerID=14301", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0007", "title": "【トッププレーヤーの高校時代】齋藤拓実（前編）「父と兄の影響でバスケを始めた」", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/japan/b1/20221126/403301.html", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0008", "title": "五十嵐圭や篠山竜青など名ポイントガードを多数輩出…Bリーグで活躍する北陸高校OB", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/japan/highschool/20200713/239606.html", "accessed_at": CHECKED_AT},
]

# (record_id, entity_type, entity_id, field_name, candidate_value, source_id, source_locator, evidence_summary, assessment, issue_note)
EVIDENCE = [
    ("B7E0001", "Person", "P000083", "name", "富樫勇樹", "B7S0001", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED", ""),
    ("B7E0002", "Person", "P000083", "name_en", "Yuki Togashi", "B7S0001", "基本情報 > 英語表記", "B.LEAGUE公式の英語表記", "SUPPORTED", ""),
    ("B7E0003", "Person", "P000083", "birth_date", "1993-07-30", "B7S0001", "基本情報 > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED", ""),
    ("B7E0004", "Career", "C000299", "organization_id", "ORG000117", "B7S0001", "プロフィール > 出身校（高）", "B.LEAGUE公式プロフィールの出身校欄", "SUPPORTED", "開志国際高等学校との在籍関係（先後・重複の有無）は未確認。公式ページに記載があるのはモントロス・クリスチャン高等学校のみ"),
    ("B7E0005", "Career", "C000299", "role", "Player", "B7S0001", "プロフィール > 出身校（高）", "選手として掲載", "SUPPORTED", ""),
    ("B7E0006", "Career", "C000300", "organization_id", "ORG000118", "B7S0001", "クラブ所属履歴 > 2026-27シーズン 千葉J", "B.LEAGUE公式のクラブ所属履歴", "SUPPORTED", ""),
    ("B7E0007", "Career", "C000300", "role", "Player", "B7S0001", "クラブ所属履歴 > 2026-27シーズン 千葉J", "選手として掲載", "SUPPORTED", ""),

    ("B7E0008", "Person", "P000084", "name", "比江島慎", "B7S0002", "選手プロフィール > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED", ""),
    ("B7E0009", "Person", "P000084", "name_en", "Makoto Hiejima", "B7S0002", "選手プロフィール > 英語表記", "B.LEAGUE公式の英語表記", "SUPPORTED", ""),
    ("B7E0010", "Person", "P000084", "birth_date", "1990-08-11", "B7S0002", "選手プロフィール > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED", ""),
    ("B7E0011", "Career", "C000290", "organization_id", "ORG000119", "B7S0002", "プロフィール > 出身校（高）", "B.LEAGUE公式プロフィールの出身校欄", "SUPPORTED", ""),
    ("B7E0012", "Career", "C000290", "role", "Player", "B7S0002", "プロフィール > 出身校（高）", "選手として掲載", "SUPPORTED", ""),
    ("B7E0013", "Career", "C000291", "organization_id", "ORG000030", "B7S0002", "プロフィール > 出身校（大）", "B.LEAGUE公式プロフィールの出身校欄", "SUPPORTED", ""),
    ("B7E0014", "Career", "C000291", "role", "Player", "B7S0002", "プロフィール > 出身校（大）", "選手として掲載", "SUPPORTED", ""),
    ("B7E0015", "Career", "C000292", "organization_id", "ORG000047", "B7S0002", "クラブ所属履歴 > 2026-27シーズン 宇都宮ブレックス", "B.LEAGUE公式のクラブ所属履歴", "SUPPORTED", ""),
    ("B7E0016", "Career", "C000292", "role", "Player", "B7S0002", "クラブ所属履歴 > 2026-27シーズン 宇都宮ブレックス", "選手として掲載", "SUPPORTED", ""),

    ("B7E0017", "Person", "P000085", "name", "篠山竜青", "B7S0003", "プロフィール > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED", ""),
    ("B7E0018", "Person", "P000085", "name_en", "Ryusei Shinoyama", "B7S0003", "プロフィール > 英語表記", "B.LEAGUE公式の英語表記", "SUPPORTED", ""),
    ("B7E0019", "Person", "P000085", "birth_date", "1988-07-20", "B7S0003", "プロフィール > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED", ""),
    ("B7E0020", "Career", "C000296", "organization_id", "ORG000120", "B7S0008", "本文 > 2004年に北陸に入学し", "専門媒体記事による北陸高校在籍の記述", "SUPPORTED", "専門媒体単独。学校・大会公式資料による直接確認はまだ"),
    ("B7E0021", "Career", "C000296", "role", "Player", "B7S0008", "本文 > 3年次のインターハイ優勝、ウインターカップベスト5", "専門媒体記事による在籍中の実績記述", "SUPPORTED", "専門媒体単独。学校・大会公式資料による直接確認はまだ"),
    ("B7E0022", "Career", "C000296", "start", "2004", "B7S0008", "本文 > 2004年に北陸に入学し", "入学年の明記", "SUPPORTED", "卒業年は記事著者の推定であり、本人の卒業を直接示す資料ではないため記録していない"),
    ("B7E0023", "Career", "C000297", "organization_id", "ORG000121", "B7S0004", "選手プロフィール > 出身校", "川崎ブレイブサンダース公式プロフィールの出身校欄", "SUPPORTED", ""),
    ("B7E0024", "Career", "C000297", "role", "Player", "B7S0004", "選手プロフィール > 出身校", "選手として掲載", "SUPPORTED", ""),
    ("B7E0025", "Career", "C000298", "organization_id", "ORG000122", "B7S0003", "クラブ所属履歴 > 2026-27シーズン Kawasaki", "B.LEAGUE公式のクラブ所属履歴", "SUPPORTED", ""),
    ("B7E0026", "Career", "C000298", "role", "Player", "B7S0003", "クラブ所属履歴 > 2026-27シーズン Kawasaki", "選手として掲載", "SUPPORTED", ""),

    ("B7E0027", "Person", "P000086", "name", "齋藤拓実", "B7S0005", "選手プロフィール > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED", ""),
    ("B7E0028", "Person", "P000086", "name_en", "Takumi Saito", "B7S0005", "選手プロフィール > 英語表記", "B.LEAGUE公式の英語表記", "SUPPORTED", ""),
    ("B7E0029", "Person", "P000086", "birth_date", "1995-08-11", "B7S0005", "選手プロフィール > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED", ""),
    ("B7E0030", "Career", "C000293", "organization_id", "ORG000123", "B7S0007", "記事本文 > 桐光学園高校", "専門媒体記事による桐光学園高校在籍の記述", "SUPPORTED", "専門媒体単独。学校・大会公式資料による直接確認はまだ"),
    ("B7E0031", "Career", "C000293", "role", "Player", "B7S0007", "記事本文 > 高校2年次にインターハイ・ウインターカップ出場", "専門媒体記事による在籍中の実績記述", "SUPPORTED", "専門媒体単独。学校・大会公式資料による直接確認はまだ"),
    ("B7E0032", "Career", "C000294", "organization_id", "ORG000124", "B7S0006", "選手プロフィール > 出身校", "名古屋ダイヤモンドドルフィンズ公式プロフィールの出身校欄", "SUPPORTED", ""),
    ("B7E0033", "Career", "C000294", "role", "Player", "B7S0006", "選手プロフィール > 出身校", "選手として掲載", "SUPPORTED", ""),
    ("B7E0034", "Career", "C000295", "organization_id", "ORG000054", "B7S0005", "クラブ所属履歴 > 2026-27シーズン 名古屋ダイヤモンドドルフィンズ", "B.LEAGUE公式のクラブ所属履歴", "SUPPORTED", ""),
    ("B7E0035", "Career", "C000295", "role", "Player", "B7S0005", "クラブ所属履歴 > 2026-27シーズン 名古屋ダイヤモンドドルフィンズ", "選手として掲載", "SUPPORTED", ""),
]

ISSUES = [
    ("B7I0001", "P000083", "C000299", "SCHOOL_HISTORY_UNCONFIRMED", "HOLD",
     "開志国際高等学校在籍がコーチ本人（父・富樫英樹氏）へのインタビュー記事等で言及されるが、B.LEAGUE公式プロフィールにはモントロス・クリスチャン高等学校のみが記載され、開志国際とのCareer上の関係（在籍順・重複）を直接示す一次資料は未確認",
     "開志国際高等学校または本人・B.LEAGUE等の公式資料でCareer関係を確認"),
    ("B7I0002", "P000084", "C000290", "PERIOD_UNKNOWN", "HOLD",
     "洛南高等学校Careerの入学・卒業年月は未確認",
     "学校またはインターハイ/ウインターカップ公式資料で年度を確認"),
    ("B7I0003", "P000084", "C000291", "PERIOD_UNKNOWN", "HOLD",
     "青山学院大学Careerの入学・卒業年月は未確認",
     "大学またはインカレ公式資料で年度を確認"),
    ("B7I0004", "P000085", "C000296", "GRADUATION_YEAR_UNCONFIRMED", "HOLD",
     "北陸高等学校の卒業年は専門媒体記事の推定（2007年頃）であり、本人の卒業を直接示す一次資料は未確認",
     "学校または当時の大会公式資料で卒業年度を確認"),
    ("B7I0005", "P000085", "C000296", "SOURCE_TIER", "HOLD",
     "北陸高等学校在籍を裏付ける一次資料（学校公式・大会公式ロスター等）が未確認、現状は専門媒体（バスケットボールキング）のみ",
     "学校または全国大会（インターハイ・ウインターカップ）公式資料を確認"),
    ("B7I0006", "P000085", "C000297", "PERIOD_UNKNOWN", "HOLD",
     "日本大学Careerの入学・卒業年月は未確認",
     "大学またはインカレ公式資料で年度を確認"),
    ("B7I0007", "P000086", "C000293", "SOURCE_TIER", "HOLD",
     "桐光学園高校在籍を裏付ける一次資料（学校公式・大会公式ロスター等）が未確認、現状は専門媒体（バスケットボールキング）のみ",
     "学校または全国大会（インターハイ・ウインターカップ）公式資料を確認"),
    ("B7I0008", "P000086", "C000293", "PERIOD_UNKNOWN", "HOLD",
     "桐光学園高校Careerの入学・卒業年月は未確認（記事から2015年頃の卒業と推定されるのみ）",
     "学校または当時の大会公式資料で卒業年度を確認"),
    ("B7I0009", "P000086", "C000294", "PERIOD_UNKNOWN", "HOLD",
     "明治大学Careerの入学・卒業年月は未確認",
     "大学またはインカレ公式資料で年度を確認"),
    ("B7I0010", "ALL", "ALL", "CLUB_HISTORY_SCOPE", "HOLD",
     "本Waveでは各選手の現所属クラブのみをCareerとして記録し、過去の所属クラブ（例：比江島慎の三河・栃木、齋藤拓実の滋賀・アルバルク東京）は対象外とした。栃木ブレックス→宇都宮ブレックス等、名称変更・承継の可能性がある組織をどう扱うかは、Batch 004のB4W3I0011（三菱電機/名古屋ダイヤモンドドルフィンズ）と同じ未解決論点であり、本Waveでも解消していない",
     "OrganizationAlias・組織承継ルールをYuichiと合意してから過去クラブ経歴を追加する"),
]

DECISIONS = [
    ("B7D0001", "Person", "P000083", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "B.LEAGUE公式プロフィールで確認"),
    ("B7D0002", "Career", "C000299", "HOLD_CANDIDATE", "role", "organization_id", "出身校欄の記載はあるが開志国際高等学校との関係未確認のためHOLD"),
    ("B7D0003", "Career", "C000300", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式のクラブ所属履歴で確認"),

    ("B7D0004", "Person", "P000084", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "B.LEAGUE公式プロフィールで確認"),
    ("B7D0005", "Career", "C000290", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校欄で確認、期間は未確認のためHOLD"),
    ("B7D0006", "Career", "C000291", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校欄で確認、期間は未確認のためHOLD"),
    ("B7D0007", "Career", "C000292", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式のクラブ所属履歴で確認"),

    ("B7D0008", "Person", "P000085", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "B.LEAGUE公式プロフィールで確認"),
    ("B7D0009", "Career", "C000296", "HOLD_CANDIDATE", "role|start", "end", "専門媒体単独の情報かつ卒業年未確認のためHOLD"),
    ("B7D0010", "Career", "C000297", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "クラブ公式の出身校欄で確認、期間は未確認のためHOLD"),
    ("B7D0011", "Career", "C000298", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式のクラブ所属履歴で確認"),

    ("B7D0012", "Person", "P000086", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "B.LEAGUE公式プロフィールで確認"),
    ("B7D0013", "Career", "C000293", "HOLD_CANDIDATE", "role", "organization_id|start|end", "専門媒体単独の情報のためHOLD"),
    ("B7D0014", "Career", "C000294", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "クラブ公式の出身校欄で確認、期間は未確認のためHOLD"),
    ("B7D0015", "Career", "C000295", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式のクラブ所属履歴で確認"),
]


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    write_csv(BASE / "person_candidates.csv", ["person_id", "name"], PERSONS)
    write_csv(BASE / "organization_candidates.csv", ["organization_id", "name"], ORGANIZATIONS)
    write_csv(BASE / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], CAREERS)
    write_csv(BASE / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], SOURCES)
    write_csv(
        BASE / "evidence_records.csv",
        ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"],
        [
            {
                "record_id": rid, "entity_type": etype, "entity_id": eid, "field_name": field,
                "candidate_value": value, "source_id": sid, "source_locator": locator,
                "evidence_summary": summary, "assessment": assessment, "checked_at": CHECKED_AT, "issue_note": note,
            }
            for rid, etype, eid, field, value, sid, locator, summary, assessment, note in EVIDENCE
        ],
    )
    write_csv(
        BASE / "issues.csv",
        ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"],
        [
            {"issue_id": iid, "person_id": pid, "related_id": rid, "issue_type": itype, "status": status, "description": desc, "next_check": nxt}
            for iid, pid, rid, itype, status, desc, nxt in ISSUES
        ],
    )
    write_csv(
        BASE / "qa_decisions.csv",
        ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"],
        [
            {"decision_id": did, "entity_type": etype, "entity_id": eid, "decision": decision, "eligible_fields": eligible, "held_fields": held, "reason": reason, "reviewed_at": CHECKED_AT}
            for did, etype, eid, decision, eligible, held, reason in DECISIONS
        ],
    )
    print(f"Wrote Batch 007 Wave 1 candidate files under {BASE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

