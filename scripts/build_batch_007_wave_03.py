#!/usr/bin/env python3
"""Build Batch 007 Wave 3 CANDIDATE data.

Selection policy update (Yuichi, 2026-09-23; recorded in
docs/DATA_SCALING_WORKFLOW_V0.1.md): going forward, prioritize players
on 2026-27 B.LEAGUE PREMIER (26-club) rosters; always include any
Fukuoka Daiichi High School alumnus found among them; also include
alumni of other high schools broadly (not just Fukuoka Daiichi).

Before naming any candidate, checked (2026-09-23) whether a new
(not-yet-in-project) Fukuoka Daiichi alumnus exists on a B.PREMIER-26
roster: the official B.LEAGUE "Watashino B.LEAGUE" alma-mater tag page
(https://www.bleague.jp/mybleague_list/?TagID=35:福岡第一高等学校) lists
14 current B.LEAGUE players from the school, and all 14 (including all
7 on B.PREMIER-26 rosters) were already confirmed present in Master.
There is currently no Fukuoka Daiichi backlog, so this wave selects
broadly from other high schools instead, from B.PREMIER-26 clubs with
no current-club coverage in Master or in any existing CANDIDATE wave
(checked against Master data/master/career.csv and Batch 007 Wave 1 /
Wave 2 career_candidates.csv before selecting):
- 安藤周人 (Shuto Ando, アルバルク東京)
- 片岡大晴 (Daiharu/Masaharu Kataoka, 仙台89ERS)
- 松脇圭志 (Keishi Matsuwaki, 琉球ゴールデンキングス)
- 星川堅信 (Kenshin Hoshikawa, 長崎ヴェルカ)

Same minimum-viable Career chain as Wave 1/2 (high school -> university
-> CURRENT club only; historical clubs remain out of scope pending the
OrganizationAlias/succession-rule decision -- see B7I0013 below, same
open item as Wave 1's B7I0010 / Wave 2's B7I0012).

Each of these 4 people is covered by a single official B.LEAGUE
roster_detail page giving name, birth date, high school, university and
current club all together, so this wave uses one source per person
(4 sources total) rather than Wave 2's multi-source-per-person pattern.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_007" / "wave_03"
CHECKED_AT = "2026-09-23"

PERSONS = [
    {"person_id": "P000091", "name": "安藤周人"},
    {"person_id": "P000092", "name": "片岡大晴"},
    {"person_id": "P000093", "name": "松脇圭志"},
    {"person_id": "P000094", "name": "星川堅信"},
]

# ORG000030 (青山学院大学), ORG000093 (白鷗大学), ORG000109 (アルバルク東京),
# ORG000106 (琉球ゴールデンキングス), ORG000119 (洛南高等学校) already exist
# in data/master/organization.csv or Batch 007 Wave 1 and are reused, not
# re-minted. ORG000121 (日本大学) was minted by Wave 1 for 篠山竜青 and is
# reused here for 松脇圭志.
ORGANIZATIONS = [
    {"organization_id": "ORG000131", "name": "三重県立四日市工業高等学校"},
    {"organization_id": "ORG000030", "name": "青山学院大学"},
    {"organization_id": "ORG000109", "name": "アルバルク東京"},
    {"organization_id": "ORG000133", "name": "仙台市立仙台高等学校"},
    {"organization_id": "ORG000093", "name": "白鷗大学"},
    {"organization_id": "ORG000132", "name": "仙台89ERS"},
    {"organization_id": "ORG000134", "name": "土浦日本大学高等学校"},
    {"organization_id": "ORG000121", "name": "日本大学"},
    {"organization_id": "ORG000106", "name": "琉球ゴールデンキングス"},
    {"organization_id": "ORG000119", "name": "洛南高等学校"},
    {"organization_id": "ORG000136", "name": "早稲田大学"},
    {"organization_id": "ORG000135", "name": "長崎ヴェルカ"},
]

CAREERS = [
    {"career_id": "C000313", "person_id": "P000091", "organization_id": "ORG000131", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000314", "person_id": "P000091", "organization_id": "ORG000030", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000315", "person_id": "P000091", "organization_id": "ORG000109", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000316", "person_id": "P000092", "organization_id": "ORG000133", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000317", "person_id": "P000092", "organization_id": "ORG000093", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000318", "person_id": "P000092", "organization_id": "ORG000132", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000319", "person_id": "P000093", "organization_id": "ORG000134", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000320", "person_id": "P000093", "organization_id": "ORG000121", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000321", "person_id": "P000093", "organization_id": "ORG000106", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000322", "person_id": "P000094", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000323", "person_id": "P000094", "organization_id": "ORG000136", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000324", "person_id": "P000094", "organization_id": "ORG000135", "role": "Player", "start": "", "end": ""},
]

SOURCES = [
    {"source_id": "B7S0022", "title": "安藤周人 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=10815", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0023", "title": "片岡大晴 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8481", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0024", "title": "松脇圭志 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=30434", "accessed_at": CHECKED_AT},
    {"source_id": "B7S0025", "title": "星川堅信 B.LEAGUE公式選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=5100000021", "accessed_at": CHECKED_AT},
]

# (record_id, entity_type, entity_id, field_name, candidate_value, source_id, source_locator, evidence_summary, assessment, issue_note)
EVIDENCE = [
    ("B7E0068", "Person", "P000091", "name", "安藤周人", "B7S0022", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED", ""),
    ("B7E0069", "Person", "P000091", "birth_date", "1994-06-13", "B7S0022", "基本情報 > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED", ""),
    ("B7E0070", "Career", "C000313", "organization_id", "ORG000131", "B7S0022", "プロフィール > 出身校", "B.LEAGUE公式プロフィールの出身校欄", "SUPPORTED", ""),
    ("B7E0071", "Career", "C000313", "role", "Player", "B7S0022", "プロフィール > 出身校", "選手として掲載", "SUPPORTED", ""),
    ("B7E0072", "Career", "C000314", "organization_id", "ORG000030", "B7S0022", "プロフィール > 大学", "B.LEAGUE公式プロフィールの大学欄", "SUPPORTED", ""),
    ("B7E0073", "Career", "C000314", "role", "Player", "B7S0022", "プロフィール > 大学", "選手として掲載", "SUPPORTED", ""),
    ("B7E0074", "Career", "C000315", "organization_id", "ORG000109", "B7S0022", "所属クラブの変遷 > アルバルク東京（現所属）", "B.LEAGUE公式の所属履歴", "SUPPORTED", ""),
    ("B7E0075", "Career", "C000315", "role", "Player", "B7S0022", "所属クラブの変遷 > アルバルク東京（現所属）", "選手として掲載", "SUPPORTED", ""),

    ("B7E0076", "Person", "P000092", "name", "片岡大晴", "B7S0023", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED", ""),
    ("B7E0077", "Person", "P000092", "birth_date", "1985-12-24", "B7S0023", "基本情報 > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED", ""),
    ("B7E0078", "Career", "C000316", "organization_id", "ORG000133", "B7S0023", "プロフィール > 出身校", "B.LEAGUE公式プロフィールの出身校欄", "SUPPORTED", ""),
    ("B7E0079", "Career", "C000316", "role", "Player", "B7S0023", "プロフィール > 出身校", "選手として掲載", "SUPPORTED", ""),
    ("B7E0080", "Career", "C000317", "organization_id", "ORG000093", "B7S0023", "プロフィール > 大学", "B.LEAGUE公式プロフィールの大学欄", "SUPPORTED", ""),
    ("B7E0081", "Career", "C000317", "role", "Player", "B7S0023", "プロフィール > 大学", "選手として掲載", "SUPPORTED", ""),
    ("B7E0082", "Career", "C000318", "organization_id", "ORG000132", "B7S0023", "所属クラブの変遷 > 仙台89ERS（現所属、2026-27シーズン契約）", "B.LEAGUE公式の所属履歴", "SUPPORTED", ""),
    ("B7E0083", "Career", "C000318", "role", "Player", "B7S0023", "所属クラブの変遷 > 仙台89ERS（現所属、2026-27シーズン契約）", "選手として掲載", "SUPPORTED", ""),

    ("B7E0084", "Person", "P000093", "name", "松脇圭志", "B7S0024", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED", ""),
    ("B7E0085", "Person", "P000093", "birth_date", "1997-05-15", "B7S0024", "基本情報 > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED", ""),
    ("B7E0086", "Career", "C000319", "organization_id", "ORG000134", "B7S0024", "プロフィール > 出身校", "B.LEAGUE公式プロフィールの出身校欄", "SUPPORTED", ""),
    ("B7E0087", "Career", "C000319", "role", "Player", "B7S0024", "プロフィール > 出身校", "選手として掲載", "SUPPORTED", ""),
    ("B7E0088", "Career", "C000320", "organization_id", "ORG000121", "B7S0024", "プロフィール > 大学", "B.LEAGUE公式プロフィールの大学欄", "SUPPORTED", ""),
    ("B7E0089", "Career", "C000320", "role", "Player", "B7S0024", "プロフィール > 大学", "選手として掲載", "SUPPORTED", ""),
    ("B7E0090", "Career", "C000321", "organization_id", "ORG000106", "B7S0024", "所属クラブの変遷 > 琉球ゴールデンキングス（現所属）", "B.LEAGUE公式の所属履歴", "SUPPORTED", ""),
    ("B7E0091", "Career", "C000321", "role", "Player", "B7S0024", "所属クラブの変遷 > 琉球ゴールデンキングス（現所属）", "選手として掲載", "SUPPORTED", ""),

    ("B7E0092", "Person", "P000094", "name", "星川堅信", "B7S0025", "基本情報 > 選手名", "B.LEAGUE公式の選手名", "SUPPORTED", ""),
    ("B7E0093", "Person", "P000094", "birth_date", "2001-11-01", "B7S0025", "基本情報 > 生年月日", "B.LEAGUE公式の生年月日", "SUPPORTED", ""),
    ("B7E0094", "Career", "C000322", "organization_id", "ORG000119", "B7S0025", "プロフィール > 出身校", "B.LEAGUE公式プロフィールの出身校欄", "SUPPORTED", ""),
    ("B7E0095", "Career", "C000322", "role", "Player", "B7S0025", "プロフィール > 出身校", "選手として掲載", "SUPPORTED", ""),
    ("B7E0096", "Career", "C000323", "organization_id", "ORG000136", "B7S0025", "プロフィール > 大学", "B.LEAGUE公式プロフィールの大学欄", "SUPPORTED", ""),
    ("B7E0097", "Career", "C000323", "role", "Player", "B7S0025", "プロフィール > 大学", "選手として掲載", "SUPPORTED", ""),
    ("B7E0098", "Career", "C000324", "organization_id", "ORG000135", "B7S0025", "所属クラブの変遷 > 長崎ヴェルカ（現所属）", "B.LEAGUE公式の所属履歴", "SUPPORTED", ""),
    ("B7E0099", "Career", "C000324", "role", "Player", "B7S0025", "所属クラブの変遷 > 長崎ヴェルカ（現所属）", "選手として掲載", "SUPPORTED", ""),
]

ISSUES = [
    ("B7I0013", "ALL", "ALL", "CLUB_HISTORY_SCOPE", "HOLD",
     "Wave 1・Wave 2と同様、本Waveでも各選手の現所属クラブのみをCareerとして記録し、過去の所属クラブ（例：松脇圭志の三遠ネオフェニックス・富山グラウジーズ、片岡大晴の京都ハンナリーズ・埼玉ブロンコス等）は対象外とした。OrganizationAlias・組織承継ルールの未解決自体はBatch 004のB4W3I0011から変わっていない",
     "OrganizationAlias・組織承継ルールをYuichiと合意してから過去クラブ経歴を追加する"),
]

DECISIONS = [
    ("B7D0032", "Person", "P000091", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認"),
    ("B7D0033", "Career", "C000313", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの出身校欄で確認、期間は未確認のためHOLD"),
    ("B7D0034", "Career", "C000314", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの大学欄で確認、期間は未確認のためHOLD"),
    ("B7D0035", "Career", "C000315", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式プロフィールの現所属欄で確認"),

    ("B7D0036", "Person", "P000092", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認"),
    ("B7D0037", "Career", "C000316", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの出身校欄で確認、期間は未確認のためHOLD"),
    ("B7D0038", "Career", "C000317", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの大学欄で確認、期間は未確認のためHOLD"),
    ("B7D0039", "Career", "C000318", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式プロフィールの現所属欄で確認"),

    ("B7D0040", "Person", "P000093", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認"),
    ("B7D0041", "Career", "C000319", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの出身校欄で確認、期間は未確認のためHOLD"),
    ("B7D0042", "Career", "C000320", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの大学欄で確認、期間は未確認のためHOLD"),
    ("B7D0043", "Career", "C000321", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式プロフィールの現所属欄で確認"),

    ("B7D0044", "Person", "P000094", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認"),
    ("B7D0045", "Career", "C000322", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの出身校欄で確認、期間は未確認のためHOLD"),
    ("B7D0046", "Career", "C000323", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールの大学欄で確認、期間は未確認のためHOLD"),
    ("B7D0047", "Career", "C000324", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "", "B.LEAGUE公式プロフィールの現所属欄で確認"),
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
    print(f"Wrote Batch 007 Wave 3 candidate files under {BASE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
