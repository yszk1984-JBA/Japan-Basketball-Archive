#!/usr/bin/env python3
"""Build Batch 007 Wave 9 (新規開拓Wave / Acquisition Wave).

Continuing the cadence after Wave 8 (深掘りWave, batch_004/wave_06):
this is the 1st acquisition wave of a new 3:1 cycle.

Target selection: notable current 男子日本代表候補 (Japan national team
candidate pool, per the JBA's 2026年夏53名 announcement / the 17-man
squad reported by Goal.com on 2026-08) who are not yet in the archive:
馬場雄大, 佐々木隆成, シェーファーアヴィ幸樹, 高島紳司. This continues
the Wave 7 theme (notable/star players) rather than club-coverage.

Notes:
- 馬場雄大: bleague.jp's own club-history table skips his NBA/G League
  years (2019-2023, not a B.LEAGUE club) between アルバルク東京 and
  長崎ヴェルカ. Per the standing CLUB_HISTORY_SCOPE scope limit, only
  school + university + CURRENT club are recorded here.
- 佐々木隆成: his high school (山口県立豊浦高等学校) is confirmed by
  Wikipedia only -- neither bleague.jp nor basketballking.jp's player
  bio mention a high school. Flagged as SOURCE_TIER (single source).
- シェーファーアヴィ幸樹: no high school Career is recorded. Wikipedia
  mentions he attended "ブリュースターアカデミー" (a US prep school)
  before Georgia Tech, but a second source (jpsk.jp) only says he
  transferred to Tokyo and started basketball in his 2nd year of high
  school, without naming any school -- not enough to confidently
  register a specific 高校 Organization, so it is left unrecorded
  rather than guessed.
- 高島紳司: 北陸高等学校 (ORG000120) and 大東文化大学 (ORG000128) reuse
  existing orgs already registered for other players.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_007" / "wave_09"

PERSONS = [
    {"person_id": "P000107", "name": "馬場雄大"},
    {"person_id": "P000108", "name": "佐々木隆成"},
    {"person_id": "P000109", "name": "シェーファーアヴィ幸樹"},
    {"person_id": "P000110", "name": "高島紳司"},
]

ORGANIZATIONS = [
    {"organization_id": "ORG000165", "name": "富山第一高校"},
    {"organization_id": "ORG000166", "name": "筑波大学"},
    {"organization_id": "ORG000135", "name": "長崎ヴェルカ"},
    {"organization_id": "ORG000167", "name": "山口県立豊浦高等学校"},
    {"organization_id": "ORG000168", "name": "天理大学"},
    {"organization_id": "ORG000097", "name": "三遠ネオフェニックス"},
    {"organization_id": "ORG000169", "name": "ジョージア工科大学"},
    {"organization_id": "ORG000132", "name": "仙台89ERS"},
    {"organization_id": "ORG000120", "name": "北陸高等学校"},
    {"organization_id": "ORG000128", "name": "大東文化大学"},
    {"organization_id": "ORG000047", "name": "宇都宮ブレックス"},
]

CAREERS = [
    {"career_id": "C000369", "person_id": "P000107", "organization_id": "ORG000165", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000370", "person_id": "P000107", "organization_id": "ORG000166", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000371", "person_id": "P000107", "organization_id": "ORG000135", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000372", "person_id": "P000108", "organization_id": "ORG000167", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000373", "person_id": "P000108", "organization_id": "ORG000168", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000374", "person_id": "P000108", "organization_id": "ORG000097", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000375", "person_id": "P000109", "organization_id": "ORG000169", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000376", "person_id": "P000109", "organization_id": "ORG000132", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000377", "person_id": "P000110", "organization_id": "ORG000120", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000378", "person_id": "P000110", "organization_id": "ORG000128", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000379", "person_id": "P000110", "organization_id": "ORG000047", "role": "Player", "start": "", "end": ""},
]

SOURCES = [
    {"source_id": "B7S0057", "title": "馬場雄大 選手情報", "publisher": "B.LEAGUE公式 (bleague.jp, PlayerID=12577)", "url": "https://www.bleague.jp/roster_detail/?PlayerID=12577", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0058", "title": "佐々木隆成", "publisher": "Wikipedia日本語版", "url": "https://ja.wikipedia.org/wiki/佐々木隆成", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0059", "title": "佐々木隆成 選手情報", "publisher": "B.LEAGUE公式 (bleague.jp, PlayerID=20037)", "url": "https://www.bleague.jp/roster_detail/?PlayerID=20037", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0060", "title": "佐々木 隆成", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/player/article/134977.html", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0061", "title": "シェーファーアヴィ幸樹 選手情報", "publisher": "B.LEAGUE公式 (bleague.jp, PlayerID=19956)", "url": "https://www.bleague.jp/roster_detail/?PlayerID=19956", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0062", "title": "シェーファーアヴィ幸樹", "publisher": "Wikipedia日本語版", "url": "https://ja.wikipedia.org/wiki/シェーファーアヴィ幸樹", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0063", "title": "「2年後に五輪に出る」ための決断。シーホース三河・シェーファー アヴィ幸樹に学ぶ、夢を叶える思考術", "publisher": "jpsk.jp", "url": "https://jpsk.jp/articles/seahorses_Schafer_01.html", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0064", "title": "高島紳司 選手情報", "publisher": "B.LEAGUE公式 (bleague.jp, PlayerID=5100000036)", "url": "https://www.bleague.jp/roster_detail/?PlayerID=5100000036", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0065", "title": "高島紳司", "publisher": "Wikipedia日本語版", "url": "https://ja.wikipedia.org/wiki/高島紳司", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0066", "title": "【注目の新卒選手#3】宇都宮・高島紳司とはどんな選手？「万能な攻撃性能とブレックスでも即戦力級の守備」", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/japan/b1/20230419/426404.html", "accessed_at": "2026-09-23"},
]

EVIDENCE: list[dict] = []
_evidence_seq = 223  # last used in wave_08 was B7E0223


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B7E{_evidence_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "field_name": field_name,
        "candidate_value": candidate_value,
        "source_id": source_id,
        "source_locator": source_locator,
        "evidence_summary": evidence_summary,
        "assessment": assessment,
        "checked_at": "2026-09-23",
        "issue_note": issue_note,
    })


# ---- P000107 馬場雄大 ----
add_evidence("Person", "P000107", "name", "馬場雄大", "B7S0057", "選手名", "bleague.jp選手プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000107", "date_of_birth", "1995-11-07", "B7S0057", "生年月日 > 1995年11月7日", "bleague.jp選手プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000369", "organization_id", "ORG000165", "B7S0057", "出身校 > 富山第一高校", "bleague.jp選手プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000370", "organization_id", "ORG000166", "B7S0057", "出身校 > 筑波大学", "bleague.jp選手プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000371", "organization_id", "ORG000135", "B7S0057", "クラブ所属履歴 > 2023-24〜2026-27 長崎ヴェルカ", "bleague.jpのクラブ所属履歴で現所属クラブ（長崎ヴェルカ）を確認", "SUPPORTED")

# ---- P000108 佐々木隆成 ----
add_evidence("Person", "P000108", "name", "佐々木隆成", "B7S0059", "選手名", "bleague.jp選手プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000108", "date_of_birth", "1996-05-02", "B7S0059", "生年月日 > 1996年5月2日", "bleague.jp選手プロフィールで生年月日を確認", "SUPPORTED")
add_evidence(
    "Career", "C000372", "organization_id", "ORG000167", "B7S0058",
    "本文 > 「山口県立豊浦高等学校から天理大学へ進学」",
    "Wikipediaで出身高校を確認。bleague.jp公式プロフィール・バスケットボールキングの選手ページのいずれにも出身高校の記載がなく、現時点でWikipedia以外の裏付けが取れていない",
    "SUPPORTED",
    issue_note="出身高校（山口県立豊浦高等学校）を裏付ける一次資料（学校公式・大会公式ロスター等）または公式プロフィールでの言及が未確認。現状はWikipedia単独",
)
add_evidence("Career", "C000373", "organization_id", "ORG000168", "B7S0058", "本文 > 「天理大学へ進学」", "Wikipediaで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000373", "organization_id", "ORG000168", "B7S0060", "出身校（出身大学） > 天理大学", "バスケットボールキングの選手プロフィールでも出身大学を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000374", "organization_id", "ORG000097", "B7S0059", "クラブ所属履歴 > 2022-23〜2026-27 三遠", "bleague.jpのクラブ所属履歴で現所属クラブ（三遠ネオフェニックス）を確認", "SUPPORTED")

# ---- P000109 シェーファーアヴィ幸樹 ----
add_evidence("Person", "P000109", "name", "シェーファーアヴィ幸樹", "B7S0061", "選手名", "bleague.jp選手プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000109", "date_of_birth", "1998-01-28", "B7S0061", "生年月日 > 1998年1月28日", "bleague.jp選手プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000375", "organization_id", "ORG000169", "B7S0062", "本文 > 「NCAAディビジョン1の名門ジョージア工科大学へ入学した」", "Wikipediaで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000375", "organization_id", "ORG000169", "B7S0063", "本文 > 「NCAAディビジョン1に所属するバスケットボール名門校」ジョージア工科大学、専攻は物理学", "jpsk.jpのインタビュー記事でも出身大学を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000376", "organization_id", "ORG000132", "B7S0061", "クラブ所属履歴 > 2026-27 仙台89ERS（現所属）", "bleague.jpのクラブ所属履歴で現所属クラブ（仙台89ERS、2026-27シーズンより三河から移籍）を確認", "SUPPORTED")

# ---- P000110 高島紳司 ----
add_evidence("Person", "P000110", "name", "高島紳司", "B7S0064", "選手名", "bleague.jp選手プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000110", "date_of_birth", "2000-10-13", "B7S0064", "生年月日 > 2000年10月13日", "bleague.jp選手プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000377", "organization_id", "ORG000120", "B7S0065", "本文 > 「北陸高校から大東文化大学に進み」", "Wikipediaで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000377", "organization_id", "ORG000120", "B7S0066", "本文 > 「北陸高校（福井県）」", "バスケットボールキングの記事でも出身高校を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000378", "organization_id", "ORG000128", "B7S0065", "本文 > 「大東文化大学に進み」", "Wikipediaで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000378", "organization_id", "ORG000128", "B7S0066", "本文 > 「大東文化大学」", "バスケットボールキングの記事でも出身大学を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000379", "organization_id", "ORG000047", "B7S0064", "クラブ所属履歴 > 2022-23〜2026-27 宇都宮ブレックス", "bleague.jpのクラブ所属履歴で現所属クラブ（宇都宮ブレックス）を確認", "SUPPORTED")


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B7D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": "2026-09-23",
    })


DECISIONS: list[dict] = []
_decision_seq = 113  # last used in wave_08 was B7D0113

add_decision("Person", "P000107", "READY_FOR_VERIFIED_REVIEW", "name|date_of_birth", "", "bleague.jp選手プロフィールで氏名・生年月日を確認")
add_decision("Career", "C000369", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpで出身高校（富山第一高校）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000370", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpで出身大学（筑波大学）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000371", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpのクラブ所属履歴で現所属（長崎ヴェルカ）を確認。開始日は資料なしのため保留")

add_decision("Person", "P000108", "READY_FOR_VERIFIED_REVIEW", "name|date_of_birth", "", "bleague.jp選手プロフィールで氏名・生年月日を確認")
add_decision(
    "Career", "C000372", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end",
    "Wikipediaで出身高校（山口県立豊浦高等学校）を確認。bleague.jp・バスケットボールキングいずれにも記載がなくWikipedia単独のためissueに記録した上でREADYとする",
)
add_decision("Career", "C000373", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipedia・バスケットボールキングの独立した2ソースで出身大学（天理大学）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000374", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpのクラブ所属履歴で現所属（三遠ネオフェニックス）を確認。開始日は資料なしのため保留")

add_decision("Person", "P000109", "READY_FOR_VERIFIED_REVIEW", "name|date_of_birth", "", "bleague.jp選手プロフィールで氏名・生年月日を確認")
add_decision("Career", "C000375", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipedia・jpsk.jpの独立した2ソースで出身大学（ジョージア工科大学）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000376", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpのクラブ所属履歴で現所属（仙台89ERS）を確認。開始日は資料なしのため保留")

add_decision("Person", "P000110", "READY_FOR_VERIFIED_REVIEW", "name|date_of_birth", "", "bleague.jp選手プロフィールで氏名・生年月日を確認")
add_decision("Career", "C000377", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipedia・バスケットボールキングの独立した2ソースで出身高校（北陸高等学校）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000378", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipedia・バスケットボールキングの独立した2ソースで出身大学（大東文化大学）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000379", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpのクラブ所属履歴で現所属（宇都宮ブレックス）を確認。開始日は資料なしのため保留")

ISSUES = [
    {
        "issue_id": "B7I0028",
        "category": "CLUB_HISTORY_SCOPE",
        "scope": "P000107,P000108,P000109,P000110",
        "description": (
            "4人とも、現所属クラブ以前の過去所属クラブ（馬場雄大のNBA/G League挑戦期を含むアルバルク東京時代、"
            "佐々木隆成の熊本・大阪時代、シェーファーアヴィ幸樹のA東京・滋賀・三河時代、高島紳司の大阪時代）は"
            "対象外とした。Wave 1・3・5・6・7と同様のCLUB_HISTORY_SCOPE。"
        ),
    },
    {
        "issue_id": "B7I0029",
        "category": "SOURCE_TIER",
        "scope": "P000108",
        "description": (
            "佐々木隆成の出身高校（山口県立豊浦高等学校）は、Wikipediaのみで確認できた情報であり、"
            "bleague.jp公式プロフィール・バスケットボールキングの選手ページいずれにも出身高校の記載がない。"
            "学校公式・大会公式ロスター等の一次資料での裏付けが望ましい。"
        ),
    },
    {
        "issue_id": "B7I0030",
        "category": "HIGH_SCHOOL_UNRECORDED",
        "scope": "P000109",
        "description": (
            "シェーファーアヴィ幸樹の出身高校は今回登録していない。Wikipediaは『ブリュースターアカデミー』"
            "（米国の大学進学準備校）への進学に言及するが、jpsk.jpのインタビュー記事は「高校2年時にバスケを始めた」"
            "「東京へ転校した」とのみ述べ具体的な学校名を確認できず、両資料の関係も不明確なため、"
            "特定の高校名を確定できる状態ではないと判断し記録を見送った。"
        ),
    },
]


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    write_csv(BASE / "person_candidates.csv", PERSONS, ["person_id", "name"])
    write_csv(BASE / "organization_candidates.csv", ORGANIZATIONS, ["organization_id", "name"])
    write_csv(BASE / "career_candidates.csv", CAREERS, ["career_id", "person_id", "organization_id", "role", "start", "end"])
    write_csv(BASE / "source_references.csv", SOURCES, ["source_id", "title", "publisher", "url", "accessed_at"])
    write_csv(BASE / "evidence_records.csv", EVIDENCE, [
        "record_id", "entity_type", "entity_id", "field_name", "candidate_value",
        "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note",
    ])
    write_csv(BASE / "issues.csv", ISSUES, ["issue_id", "category", "scope", "description"])
    write_csv(BASE / "qa_decisions.csv", DECISIONS, [
        "decision_id", "entity_type", "entity_id", "decision",
        "eligible_fields", "held_fields", "reason", "reviewed_at",
    ])
    print(
        f"Wrote wave_09: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
