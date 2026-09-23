#!/usr/bin/env python3
"""Build Batch 010 Wave 4 (洛南高等学校 4/4, final wave) CANDIDATE data.

Final wave for 洛南高等学校 (school 3/11 of the powerhouse expansion
initiative). Covers the last of the 19 not-yet-registered current
B.LEAGUE alumni: 大西一輝 (ヴィアティン三重).

Discovery note: 大西一輝 is confirmed on the B.LEAGUE official
TagID=35:洛南高等学校 alumni tag list (his card shows 出身校=中京大学,
i.e. his university, per the wave_01 finding that this field displays
university rather than high school). HOWEVER, a real bug was found on
bleague.jp itself: both the 洛南 tag-list card and ヴィアティン三重's own
club_detail roster page link to PlayerID=11482 for 大西一輝, but
https://www.bleague.jp/roster_detail/?PlayerID=11482 actually resolves
to a COMPLETELY DIFFERENT player (ザック・モーア / Zack Moore, born
1997-03-26, ex-UC Santa Barbara / UBC). This PlayerID is NOT used as a
source here -- logged instead as a DISCOVERY_METHOD_GAP issue. Primary
sourcing instead comes from ヴィアティン三重's own official team site
(veertien-basketball.jp) and a specialized fan-site profile
(bibitobleague.club), which independently confirm matching biographical
details (name, birth date 2003-10-25, 京都府出身) and, critically, rule
out a namesake collision: a DIFFERENT basketball player also named
大西一輝 plays for 環太平洋大学 (per kyureki.com) and is NOT this person.

No B.LEAGUE-side start year for his ヴィアティン三重 tenure could be
confirmed from any available source -- left NULL/blank per governance
(never guess unknown information), with a DATA_QUALITY_NOTE issue
logged.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_010" / "wave_04"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000152", "name": "大西 一輝"},
]

# ORG000119 (洛南高等学校) already exists and is reused -- checked
# against master + every candidate organization_candidates.csv before
# writing this file. 中京大学・ヴィアティン三重 confirmed genuinely new
# (checked: no existing Organization anywhere in master or candidate
# files uses either name); current max existing Organization ID is
# ORG000190 (batch_010/wave_03, which deliberately reserved ORG000189
# for 中京大学 here), so 中京大学=ORG000189 and ヴィアティン三重=ORG000191.
ORGANIZATIONS = [
    {"organization_id": "ORG000119", "name": "洛南高等学校"},
    {"organization_id": "ORG000189", "name": "中京大学"},
    {"organization_id": "ORG000191", "name": "ヴィアティン三重"},
]

CAREERS = [
    {"career_id": "C000511", "person_id": "P000152", "organization_id": "ORG000119", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000512", "person_id": "P000152", "organization_id": "ORG000189", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000513", "person_id": "P000152", "organization_id": "ORG000191", "role": "Player", "start": "", "end": ""},
]

SOURCES = [
    {"source_id": "B10W4S0001", "title": "ワタシノB.LEAGUE選手一覧 | 洛南高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:洛南高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B10W4S0002", "title": "大西一輝選手 選手詳細", "publisher": "ヴィアティン三重バスケットボール", "url": "https://veertien-basketball.jp/team/players/detail/id=60078?PlayerID=11482", "accessed_at": CHECKED_AT},
    {"source_id": "B10W4S0003", "title": "大西一輝選手 選手一覧", "publisher": "ヴィアティン三重バスケットボール", "url": "https://veertien-basketball.jp/team/players/", "accessed_at": CHECKED_AT},
    {"source_id": "B10W4S0004", "title": "大西一輝(バスケ)のプロフィールと経歴！両親や兄弟・姉妹情報も！", "publisher": "ビビッとBリーグ", "url": "https://bibitobleague.club/archives/5889", "accessed_at": CHECKED_AT},
]

EVIDENCE = [
    {"record_id": "B10W4E0001", "entity_type": "Person", "entity_id": "P000152", "field_name": "name", "candidate_value": "大西 一輝", "source_id": "B10W4S0002", "source_locator": "基本情報 > 氏名", "evidence_summary": "ヴィアティン三重公式サイトで氏名を確認", "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": ""},
    {"record_id": "B10W4E0002", "entity_type": "Person", "entity_id": "P000152", "field_name": "name", "candidate_value": "大西一輝（おおにし いつき）", "source_id": "B10W4S0004", "source_locator": "基本情報", "evidence_summary": "ファンサイトで氏名・読みを確認（同姓同名の環太平洋大学の別選手との混同でないことを、生年月日の一致で確認）", "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": ""},
    {"record_id": "B10W4E0003", "entity_type": "Person", "entity_id": "P000152", "field_name": "birth_date", "candidate_value": "2003-10-25", "source_id": "B10W4S0002", "source_locator": "基本情報 > 生年月日", "evidence_summary": "ヴィアティン三重公式サイトで生年月日を確認", "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": ""},
    {"record_id": "B10W4E0004", "entity_type": "Person", "entity_id": "P000152", "field_name": "birth_date", "candidate_value": "2003年10月25日", "source_id": "B10W4S0004", "source_locator": "基本情報", "evidence_summary": "ファンサイトでも同一の生年月日を確認（クラブ公式との一致で同一人物と確認）", "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": ""},
    {"record_id": "B10W4E0005", "entity_type": "Career", "entity_id": "C000511", "field_name": "organization_id", "candidate_value": "ORG000119", "source_id": "B10W4S0001", "source_locator": "洛南高等学校タグ一覧内の選手カード", "evidence_summary": "B.LEAGUE公式の出身校タグ一覧（TagID=35:洛南高等学校）に掲載されていることで在籍を確認", "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": ""},
    {"record_id": "B10W4E0006", "entity_type": "Career", "entity_id": "C000511", "field_name": "organization_id", "candidate_value": "ORG000119", "source_id": "B10W4S0004", "source_locator": "経歴 > 高校", "evidence_summary": "ファンサイトで洛南高等学校在籍（3年時にチームの中心選手に成長）を確認", "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": ""},
    {"record_id": "B10W4E0007", "entity_type": "Career", "entity_id": "C000512", "field_name": "organization_id", "candidate_value": "ORG000189", "source_id": "B10W4S0002", "source_locator": "基本情報 > 出身大学", "evidence_summary": "ヴィアティン三重公式サイトで中京大学出身であることを確認", "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": ""},
    {"record_id": "B10W4E0008", "entity_type": "Career", "entity_id": "C000512", "field_name": "organization_id", "candidate_value": "ORG000189", "source_id": "B10W4S0004", "source_locator": "経歴 > 大学", "evidence_summary": "ファンサイトで中京大学イーグルスでのプレー歴を確認", "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": ""},
    {"record_id": "B10W4E0009", "entity_type": "Career", "entity_id": "C000513", "field_name": "organization_id", "candidate_value": "ORG000191", "source_id": "B10W4S0002", "source_locator": "基本情報 > 現所属", "evidence_summary": "ヴィアティン三重公式サイト自身のロスターに背番号11として掲載されていることで現所属を確認", "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": ""},
    {"record_id": "B10W4E0010", "entity_type": "Career", "entity_id": "C000513", "field_name": "organization_id", "candidate_value": "ORG000191", "source_id": "B10W4S0003", "source_locator": "選手一覧ロスター", "evidence_summary": "ヴィアティン三重公式選手一覧ページにも掲載されていることを重ねて確認", "assessment": "SUPPORTED", "checked_at": CHECKED_AT, "issue_note": ""},
]

ISSUES = [
    {"issue_id": "B10W4I0001", "person_id": "P000152", "related_id": "C000511", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD", "description": "洛南高等学校在籍そのものは出身校タグ一覧・ファンサイトで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。", "next_check": "本人のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B10W4I0002", "person_id": "P000152", "related_id": "C000512", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD", "description": "中京大学在籍そのものはヴィアティン三重公式サイト・ファンサイトで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。", "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスター、または中京大学バスケットボール部公式での裏付けを確認"},
    {"issue_id": "B10W4I0003", "person_id": "P000152", "related_id": "C000513", "issue_type": "DATA_QUALITY_NOTE", "status": "HOLD", "description": "大西一輝のヴィアティン三重加入年（Career開始年）が、確認できたいずれの資料（クラブ公式サイト、ファンサイト、検索結果）にも明記されておらず未確認のためNULLのまま登録した。", "next_check": "ヴィアティン三重の過去シーズンのプレスリリース（新加入選手発表）またはB.LEAGUE公式の年度別ロスター履歴での裏付けを確認"},
    {"issue_id": "B10W4I0004", "person_id": "P000152", "related_id": "P000152", "issue_type": "DISCOVERY_METHOD_GAP", "status": "HOLD", "description": "B.LEAGUE公式サイト自身に選手ID誤りのバグを発見：洛南高等学校タグ一覧のカード、およびヴィアティン三重のclub_detailロスターページの双方が、大西一輝の詳細ページとしてhttps://www.bleague.jp/roster_detail/?PlayerID=11482 をリンクしているが、実際にこのURLを開くと全く別人（ザック・モーア、1997-03-26生、元UCサンタバーバラ/UBC）のプロフィールが表示される。このPlayerIDは本Waveのソースとして使用せず、代わりにクラブ公式サイト（veertien-basketball.jp）とファンサイトを一次情報として採用した。なお、同姓同名で環太平洋大学出身の別のバスケットボール選手（球歴.comに掲載）が存在することも確認しており、生年月日の一致（2003-10-25）により本人とは別人であることを確認済み。", "next_check": "B.LEAGUE公式サイトの当該PlayerID紐付けバグが修正され、大西一輝本人の正しいroster_detailページが判明した場合は差し替え"},
]

DECISIONS = [
    {"decision_id": "B10W4D0001", "entity_type": "Person", "entity_id": "P000152", "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "name|birth_date", "held_fields": "", "reason": "クラブ公式サイトとファンサイトの2系統で氏名・生年月日が一致し、同姓同名の別選手との混同でないことも生年月日で確認済み", "reviewed_at": CHECKED_AT},
    {"decision_id": "B10W4D0002", "entity_type": "Organization", "entity_id": "ORG000189", "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "name", "held_fields": "", "reason": "新規Organization、クラブ公式サイト・ファンサイト双方で中京大学出身であることを確認、既存Organizationとの重複なしを確認済み", "reviewed_at": CHECKED_AT},
    {"decision_id": "B10W4D0003", "entity_type": "Organization", "entity_id": "ORG000191", "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "name", "held_fields": "", "reason": "新規Organization、B.LEAGUE参入クラブとして既存資料多数、既存Organizationとの重複なしを確認済み", "reviewed_at": CHECKED_AT},
    {"decision_id": "B10W4D0004", "entity_type": "Career", "entity_id": "C000511", "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "organization_id|role", "held_fields": "start|end", "reason": "出身校タグ一覧・ファンサイトで確認、在籍期間は未確認", "reviewed_at": CHECKED_AT},
    {"decision_id": "B10W4D0005", "entity_type": "Career", "entity_id": "C000512", "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "organization_id|role", "held_fields": "start|end", "reason": "クラブ公式サイト・ファンサイトで確認、在籍期間は未確認", "reviewed_at": CHECKED_AT},
    {"decision_id": "B10W4D0006", "entity_type": "Career", "entity_id": "C000513", "decision": "READY_FOR_VERIFIED_REVIEW", "eligible_fields": "organization_id|role", "held_fields": "start|end", "reason": "クラブ公式サイト自身のロスターへの掲載で現所属を確認、加入年は未確認", "reviewed_at": CHECKED_AT},
]


def main() -> int:
    BASE.mkdir(parents=True, exist_ok=True)
    write_csv(BASE / "person_candidates.csv", ["person_id", "name"], PERSONS)
    write_csv(BASE / "organization_candidates.csv", ["organization_id", "name"], ORGANIZATIONS)
    write_csv(BASE / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], CAREERS)
    write_csv(BASE / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], SOURCES)
    write_csv(
        BASE / "evidence_records.csv",
        ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"],
        EVIDENCE,
    )
    write_csv(BASE / "issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], ISSUES)
    write_csv(
        BASE / "qa_decisions.csv",
        ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"],
        DECISIONS,
    )
    print(
        f"Wrote batch_010/wave_04: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, "
        f"{len(CAREERS)} careers, {len(SOURCES)} sources, {len(EVIDENCE)} evidence, "
        f"{len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
