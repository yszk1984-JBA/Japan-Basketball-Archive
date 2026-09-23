#!/usr/bin/env python3
"""Build Batch 007 Wave 2 CANDIDATE data.

Continuation of the scope-widening experiment (Yuichi, 2026-09-23).
Same minimum-viable Career chain as Wave 1 (high school -> university
-> CURRENT club only).

Original proposal for this wave named 4 candidates; verification against
official sources during research forced two substitutions before any
CANDIDATE file was written (see data/candidate/batch_007/README.md for
the full account):
- 河村勇輝 was dropped: already Master P000064 (Batch 004, Fukuoka
  Daiichi alumnus) with every Career already recorded including his
  current club (ORG000055 横浜ビー・コルセアーズ). Adding him here would
  have created a duplicate Person.
- 太田敦也 was dropped: retired 2025-06-27 (三遠ネオフェニックス公式発表).
  No current club, so he does not fit this wave's "current club only"
  scope.
Replacements 西田優大 and 金丸晃輔 were verified current before being
added to this list.

Persons (none previously touched by any batch -- checked against
Master + every candidate/verified person file before writing this):
- 田中大貴 (Daiki Tanaka, 東京サンロッカーズ -- rebranded from
  サンロッカーズ渋谷 for the B.PREMIER 2026-27 season; Master already
  carries the post-rebrand name as ORG000114, so no alias was created)
- 岸本隆一 (Ryuichi Kishimoto, 京都ハンナリーズ -- signed 2026-27..2027-28
  after 2013-2026 at 琉球ゴールデンキングス, which is out of this wave's
  scope for the same reason as Wave 1's historical-club exclusions)
- 西田優大 (Yudai Nishida, シーホース三河)
- 金丸晃輔 (Kosuke Kanamaru, 佐賀バルーナーズ)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_007" / "wave_02"
CHECKED_AT = "2026-09-23"

PERSONS = [
    {"person_id": "P000087", "name": "田中大貴"},
    {"person_id": "P000088", "name": "岸本隆一"},
    {"person_id": "P000089", "name": "西田優大"},
    {"person_id": "P000090", "name": "金丸晃輔"},
]

# ORG000015/ORG000042/ORG000048/ORG000114 already exist in
# data/master/organization.csv (東海大学 / 京都ハンナリーズ / 佐賀バル
# ーナーズ / 東京サンロッカーズ) and are reused, not re-minted.
# ORG000124 (明治大学) was minted by Batch 007 Wave 1 for 齋藤拓実 and is
# reused here for 金丸晃輔 -- caught by validate_batch_007_wave_02.py
# flagging a name collision on first run, not found by inspection.
ORGANIZATIONS = [
    {"organization_id": "ORG000125", "name": "長崎県立長崎西高等学校"},
    {"organization_id": "ORG000126", "name": "沖縄県立北中城高等学校"},
    {"organization_id": "ORG000127", "name": "福岡大学附属大濠高等学校"},
    {"organization_id": "ORG000128", "name": "大東文化大学"},
    {"organization_id": "ORG000130", "name": "シーホース三河"},
    {"organization_id": "ORG000015", "name": "東海大学"},
    {"organization_id": "ORG000042", "name": "京都ハンナリーズ"},
    {"organization_id": "ORG000048", "name": "佐賀バルーナーズ"},
    {"organization_id": "ORG000114", "name": "東京サンロッカーズ"},
    {"organization_id": "ORG000124", "name": "明治大学"},
]

CAREERS = [
    {"career_id": "C000301", "person_id": "P000087", "organization_id": "ORG000125", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000302", "person_id": "P000087", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000303", "person_id": "P000087", "organization_id": "ORG000114", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000304", "person_id": "P000088", "organization_id": "ORG000126", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000305", "person_id": "P000088", "organization_id": "ORG000128", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000306", "person_id": "P000088", "organization_id": "ORG000042", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000307", "person_id": "P000089", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000308", "person_id": "P000089", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000309", "person_id": "P000089", "organization_id": "ORG000130", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000310", "person_id": "P000090", "organization_id": "ORG000127", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000311", "person_id": "P000090", "organization_id": "ORG000124", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000312", "person_id": "P000090", "organization_id": "ORG000048", "role": "Player", "start": "", "end": ""},
]

SOURCES = [
    {"source_id": "B7S0009", "title": "田中大貴 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=9037", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0010", "title": "田中大貴 東京サンロッカーズ公式選手プロフィール", "publisher": "東京サンロッカーズ", "url": "https://www.sunrockers.jp/team/players/detail/id=16564?PlayerID=9037", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0011", "title": "ワタシノB.LEAGUE選手一覧 | 長崎県立長崎西高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:%E9%95%B7%E5%B4%8E%E7%9C%8C%E7%AB%8B%E9%95%B7%E5%B4%8E%E8%A5%BF%E9%AB%98%E7%AD%89%E5%AD%A6%E6%A0%A1", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0012", "title": "田中大貴が語るバスケ部時代vol.2「背番号『24』は、母校長崎西の『西＝24』」", "publisher": "バスケットカウント", "url": "https://basket-count.com/article/detail/3918", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0013", "title": "岸本隆一 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8655", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0014", "title": "岸本 隆一選手 契約締結（複数年）のお知らせ", "publisher": "京都ハンナリーズ", "url": "https://hannaryz.jp/news/detail/id=24529", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0015", "title": "ワタシノB.LEAGUE選手一覧 | 沖縄県立北中城高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:%E6%B2%96%E7%B8%84%E7%9C%8C%E7%AB%8B%E5%8C%97%E4%B8%AD%E5%9F%8E%E9%AB%98%E7%AD%89%E5%AD%A6%E6%A0%A1", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0016", "title": "【B.STARS Vol.3-①】岸本隆一（琉球ゴールデンキングス）", "publisher": "月刊バスケットボールWEB", "url": "https://www.basketball-zine.com/article/detail/7981", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0017", "title": "西田優大 シーホース三河公式選手プロフィール", "publisher": "シーホース三河", "url": "https://go-seahorses.jp/team/players/detail/id=17209?PlayerID=30403", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0018", "title": "金丸晃輔 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8592", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0019", "title": "14 金丸晃輔選手 佐賀バルーナーズ公式選手プロフィール", "publisher": "佐賀バルーナーズ", "url": "https://ballooners.jp/team/member/player14", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0020", "title": "プロバスケットボール選手・金丸晃輔さんにインタビュー【第1回】", "publisher": "Meiji NOW（明治大学）", "url": "https://meijinow.jp/senior/interview/8831", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0021", "title": "【トッププレーヤーの高校時代】金丸晃輔「バスケをはじめたきっかけは、ダイエット」（前編）", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/japan/b1/20201124/298048.html", "accessed_at": CHECKED_AT},
]

# (record_id, entity_type, entity_id, field_name, candidate_value, source_id, source_locator, evidence_summary, assessment, issue_note)
EVIDENCE = [
    ("B7E0036", "Person", "P000087", "name", "田中大貴", "B7S0009", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED", ""),
    ("B7E0037", "Person", "P000087", "birth_date", "1991-09-03", "B7S0009", "基本情報 > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED", ""),
    ("B7E0038", "Career", "C000301", "organization_id", "ORG000125", "B7S0011", "検索結果 > 田中大貴", "B.LEAGUE公式「ワタシノB.LEAGUE」の出身校タグ一覧に掲載", "SUPPORTED", ""),
    ("B7E0039", "Career", "C000301", "role", "Player", "B7S0011", "検索結果 > 田中大貴", "選手として掲載", "SUPPORTED", ""),
    ("B7E0040", "Career", "C000302", "organization_id", "ORG000015", "B7S0009", "プロフィール > 出身校", "B.LEAGUE公式プロフィールの出身校欄", "SUPPORTED", ""),
    ("B7E0041", "Career", "C000302", "role", "Player", "B7S0009", "プロフィール > 出身校", "選手として掲載", "SUPPORTED", ""),
    ("B7E0042", "Career", "C000303", "organization_id", "ORG000114", "B7S0010", "所属クラブの変遷 > 東京サンロッカーズ渋谷（2023-24シーズン以降現在）", "クラブ公式の所属履歴", "SUPPORTED", "サンロッカーズ渋谷は2026-27シーズンより東京サンロッカーズへ改称（B.LEAGUE公式発表）。Master ORG000114は改称後の名称で登録済みのため、そのまま使用しAliasは作成していない"),
    ("B7E0043", "Career", "C000303", "role", "Player", "B7S0010", "所属クラブの変遷 > 東京サンロッカーズ渋谷（2023-24シーズン以降現在）", "選手として掲載", "SUPPORTED", ""),

    ("B7E0044", "Person", "P000088", "name", "岸本隆一", "B7S0013", "選手プロフィール > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED", ""),
    ("B7E0045", "Person", "P000088", "birth_date", "1990-05-17", "B7S0013", "選手プロフィール > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED", ""),
    ("B7E0046", "Career", "C000304", "organization_id", "ORG000126", "B7S0015", "検索結果：1人 > 岸本隆一", "B.LEAGUE公式「ワタシノB.LEAGUE」の出身校タグ一覧に掲載", "SUPPORTED", ""),
    ("B7E0047", "Career", "C000304", "role", "Player", "B7S0015", "検索結果：1人 > 岸本隆一", "選手として掲載", "SUPPORTED", ""),
    ("B7E0048", "Career", "C000305", "organization_id", "ORG000128", "B7S0014", "学歴 > 大東文化大学", "京都ハンナリーズ公式の契約発表記事内の経歴紹介", "SUPPORTED", ""),
    ("B7E0049", "Career", "C000305", "role", "Player", "B7S0014", "学歴 > 大東文化大学", "選手として掲載", "SUPPORTED", ""),
    ("B7E0050", "Career", "C000306", "organization_id", "ORG000042", "B7S0014", "契約期間 > 2026-27シーズンから2027-28シーズンまで、2年間の複数年契約", "クラブ公式の契約発表", "SUPPORTED", ""),
    ("B7E0051", "Career", "C000306", "role", "Player", "B7S0014", "契約期間 > 2026-27シーズンから2027-28シーズンまで、2年間の複数年契約", "選手として掲載", "SUPPORTED", ""),

    ("B7E0052", "Person", "P000089", "name", "西田優大", "B7S0017", "基本情報 > 選手名", "クラブ公式の選手名", "SUPPORTED", ""),
    ("B7E0053", "Person", "P000089", "birth_date", "1999-03-13", "B7S0017", "基本情報 > 生年月日", "クラブ公式の生年月日", "SUPPORTED", ""),
    ("B7E0054", "Career", "C000307", "organization_id", "ORG000127", "B7S0017", "経歴概要 > 高校で大濠高校に進学", "クラブ公式選手プロフィールの経歴概要", "SUPPORTED", ""),
    ("B7E0055", "Career", "C000307", "role", "Player", "B7S0017", "経歴概要 > 高校で大濠高校に進学", "選手として掲載", "SUPPORTED", ""),
    ("B7E0056", "Career", "C000308", "organization_id", "ORG000015", "B7S0017", "経歴概要 > 大学では東海大学でプレー", "クラブ公式選手プロフィールの経歴概要", "SUPPORTED", ""),
    ("B7E0057", "Career", "C000308", "role", "Player", "B7S0017", "経歴概要 > 大学では東海大学でプレー", "選手として掲載", "SUPPORTED", ""),
    ("B7E0058", "Career", "C000309", "organization_id", "ORG000130", "B7S0017", "現在の所属チーム > シーホース三河", "クラブ公式選手プロフィールの現所属欄", "SUPPORTED", ""),
    ("B7E0059", "Career", "C000309", "role", "Player", "B7S0017", "現在の所属チーム > シーホース三河", "選手として掲載", "SUPPORTED", ""),

    ("B7E0060", "Person", "P000090", "name", "金丸晃輔", "B7S0018", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED", ""),
    ("B7E0061", "Person", "P000090", "birth_date", "1989-03-08", "B7S0019", "選手情報 > 生年月日", "クラブ公式の生年月日", "SUPPORTED", ""),
    ("B7E0062", "Career", "C000310", "organization_id", "ORG000127", "B7S0021", "本文 > 高校進学時、大濠高校への進学を決定", "専門媒体記事による大濠高校在籍の記述", "SUPPORTED", "専門媒体単独。学校・大会公式資料・B.LEAGUE公式「ワタシノB.LEAGUE」タグ一覧のいずれでも直接確認はまだ"),
    ("B7E0063", "Career", "C000310", "role", "Player", "B7S0021", "本文 > 高校では1年生からメンバー入り", "専門媒体記事による在籍中の実績記述", "SUPPORTED", "専門媒体単独。学校・大会公式資料による直接確認はまだ"),
    ("B7E0064", "Career", "C000311", "organization_id", "ORG000124", "B7S0020", "記事本文 > 2011年政治経済学部卒", "明治大学公式インタビューサイトの卒業年・学部記載", "SUPPORTED", ""),
    ("B7E0065", "Career", "C000311", "role", "Player", "B7S0020", "記事冒頭 > 明大在学時にはバスケットボール部主将を務め", "明治大学公式インタビューサイトの記述", "SUPPORTED", ""),
    ("B7E0066", "Career", "C000312", "organization_id", "ORG000048", "B7S0019", "経歴 > 2024年～", "クラブ公式選手プロフィールの経歴欄", "SUPPORTED", ""),
    ("B7E0067", "Career", "C000312", "role", "Player", "B7S0019", "経歴 > 2024年～", "選手として掲載", "SUPPORTED", ""),
]

ISSUES = [
    ("B7I0011", "P000090", "C000310", "SOURCE_TIER", "HOLD",
     "福岡大学附属大濠高等学校在籍を裏付ける一次資料（学校公式・大会公式ロスター等）が未確認。B.LEAGUE公式「ワタシノB.LEAGUE」の同校タグ一覧にも金丸晃輔は掲載されておらず（2026-09-23時点、9人中に該当なし）、現状は専門媒体（バスケットボールキング）のみ。ウインターカップ公式アーカイブ（wintercup.japanbasketball.jp）で該当年度（2005-2007年頃）のロスター確認を試みたが、レガシーサイトのため今回はツール側の技術的制約でアクセスできなかった",
     "学校、当時の大会公式資料、またはウインターカップ公式アーカイブへの再アクセスで確認"),
    ("B7I0012", "ALL", "ALL", "CLUB_HISTORY_SCOPE", "HOLD",
     "Wave 1と同様、本Waveでも各選手の現所属クラブのみをCareerとして記録し、過去の所属クラブ（例：田中大貴のアルバルク東京、岸本隆一の琉球ゴールデンキングス、金丸晃輔のシーホース三河・島根スサノオマジック・三遠ネオフェニックス等）は対象外とした。田中大貴の所属先はサンロッカーズ渋谷から東京サンロッカーズへ2026-27シーズンより改称されているが、Master ORG000114には改称後の名称が既に登録されていたためAlias作成の判断は不要だった。OrganizationAlias・組織承継ルールの未解決自体はBatch 004のB4W3I0011から変わっていない",
     "OrganizationAlias・組織承継ルールをYuichiと合意してから過去クラブ経歴を追加する"),
]

DECISIONS = [
    ("B7D0016", "Person", "P000087", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認"),
    ("B7D0017", "Career", "C000301", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式「ワタシノB.LEAGUE」の出身校タグで確認、期間は未確認のためHOLD"),
    ("B7D0018", "Career", "C000302", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの出身校欄で確認、期間は未確認のためHOLD"),
    ("B7D0019", "Career", "C000303", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "クラブ公式のクラブ所属履歴で確認"),

    ("B7D0020", "Person", "P000088", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認"),
    ("B7D0021", "Career", "C000304", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式「ワタシノB.LEAGUE」の出身校タグで確認、期間は未確認のためHOLD"),
    ("B7D0022", "Career", "C000305", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "移籍先クラブ公式の契約発表記事内の経歴紹介で確認、期間は未確認のためHOLD"),
    ("B7D0023", "Career", "C000306", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "移籍先クラブ公式の契約発表で確認"),

    ("B7D0024", "Person", "P000089", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "クラブ公式選手プロフィールで確認"),
    ("B7D0025", "Career", "C000307", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "クラブ公式選手プロフィールの経歴概要で確認、期間は未確認のためHOLD"),
    ("B7D0026", "Career", "C000308", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "クラブ公式選手プロフィールの経歴概要で確認、期間は未確認のためHOLD"),
    ("B7D0027", "Career", "C000309", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "クラブ公式選手プロフィールの現所属欄で確認"),

    ("B7D0028", "Person", "P000090", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式・クラブ公式プロフィールで確認"),
    ("B7D0029", "Career", "C000310", "HOLD_CANDIDATE", "role", "organization_id|start|end", "専門媒体単独の情報のためHOLD"),
    ("B7D0030", "Career", "C000311", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "大学公式インタビューサイト（Meiji NOW）で確認、期間は未確認のためHOLD"),
    ("B7D0031", "Career", "C000312", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "クラブ公式選手プロフィールで現所属を確認"),
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
    print(f"Wrote Batch 007 Wave 2 candidate files under {BASE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
