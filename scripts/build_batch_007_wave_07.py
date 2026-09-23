#!/usr/bin/env python3
"""Build Batch 007 Wave 7 (新規開拓Wave / Acquisition Wave).

Per Yuichi's instruction: "Wave 7も新規開拓で、控え選手や主力選手の追加に
進めてください" -- unlike Wave 5/6 (which targeted full B.PREMIER club
roster coverage), Wave 7 targets notable/star Japanese players not yet in
the archive at all, regardless of club-coverage status.

Targets: 渡邊雄太 (NBA/千葉ジェッツ), 八村塁 (NBA/LAクリッパーズ),
田臥勇太 (宇都宮ブレックス, legendary veteran), 富永啓生 (レバンガ北海道).

Notes:
- 八村塁: Wikipedia is stale on his current team (only shows through
  Lakers); current club (LAクリッパーズ, 2026年7月移籍) sourced from
  basketballking.jp instead. High school ORG000147 明成高等学校 is reused
  from Wave 5 (安藤誓哉) -- same school, timing checks out (八村塁 attended
  ~2013-2016, before the 2020 rename to 仙台大学附属明成高等学校).
- 田臥勇太: High school registered under its HISTORICAL name
  秋田県立能代工業高等学校, per governance (must use the name held at the
  time of attendance, not the current 秋田県立能代科学技術高等学校).
- Reused existing orgs: ORG000118 千葉ジェッツ, ORG000140 ロサンゼルス・
  クリッパーズ, ORG000147 明成高等学校, ORG000047 宇都宮ブレックス,
  ORG000092 レバンガ北海道.
- Per the still-unresolved OrganizationAlias/組織承継 issue chain
  (B4W3I0011->B7I0013->B7I0022->B7I0023), only current club + school/
  university Careers are recorded here; full transfer history is deferred.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_007" / "wave_07"

PERSONS = [
    {"person_id": "P000103", "name": "渡邊雄太"},
    {"person_id": "P000104", "name": "八村塁"},
    {"person_id": "P000105", "name": "田臥勇太"},
    {"person_id": "P000106", "name": "富永啓生"},
]

ORGANIZATIONS = [
    {"organization_id": "ORG000156", "name": "尽誠学園高等学校"},
    {"organization_id": "ORG000157", "name": "ジョージ・ワシントン大学"},
    {"organization_id": "ORG000118", "name": "千葉ジェッツ"},
    {"organization_id": "ORG000147", "name": "明成高等学校"},
    {"organization_id": "ORG000158", "name": "ゴンザガ大学"},
    {"organization_id": "ORG000140", "name": "ロサンゼルス・クリッパーズ"},
    {"organization_id": "ORG000159", "name": "秋田県立能代工業高等学校"},
    {"organization_id": "ORG000160", "name": "ブリガムヤング大学ハワイ校"},
    {"organization_id": "ORG000047", "name": "宇都宮ブレックス"},
    {"organization_id": "ORG000161", "name": "桜丘高等学校"},
    {"organization_id": "ORG000162", "name": "ネブラスカ大学"},
    {"organization_id": "ORG000092", "name": "レバンガ北海道"},
]

CAREERS = [
    {"career_id": "C000353", "person_id": "P000103", "organization_id": "ORG000156", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000354", "person_id": "P000103", "organization_id": "ORG000157", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000355", "person_id": "P000103", "organization_id": "ORG000118", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000356", "person_id": "P000104", "organization_id": "ORG000147", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000357", "person_id": "P000104", "organization_id": "ORG000158", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000358", "person_id": "P000104", "organization_id": "ORG000140", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000359", "person_id": "P000105", "organization_id": "ORG000159", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000360", "person_id": "P000105", "organization_id": "ORG000160", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000361", "person_id": "P000105", "organization_id": "ORG000047", "role": "Player", "start": "", "end": ""},

    {"career_id": "C000362", "person_id": "P000106", "organization_id": "ORG000161", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000363", "person_id": "P000106", "organization_id": "ORG000162", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000364", "person_id": "P000106", "organization_id": "ORG000092", "role": "Player", "start": "", "end": ""},
]

SOURCES = [
    {"source_id": "B7S0047", "title": "渡邊雄太 選手情報", "publisher": "B.LEAGUE公式 (bleague.jp, PlayerID=51000428)", "url": "https://www.bleague.jp/player/51000428/", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0048", "title": "TOP TEAM｜千葉ジェッツふなばし", "publisher": "千葉ジェッツふなばし公式", "url": "https://chibajets.jp/team/", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0049", "title": "八村塁", "publisher": "Wikipedia日本語版", "url": "https://ja.wikipedia.org/wiki/八村塁", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0050", "title": "八村塁、新天地はクリッパーズ！ NBA3チーム目、2年契約と現地報道", "publisher": "バスケットボールキング (basketballking.jp)", "url": "https://basketballking.jp/news/world/20260707/622623.html", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0051", "title": "田臥勇太 選手情報", "publisher": "B.LEAGUE公式 (bleague.jp, PlayerID=8650)", "url": "https://www.bleague.jp/player/8650/", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0052", "title": "富永啓生 選手情報", "publisher": "B.LEAGUE公式 (bleague.jp, PlayerID=19755)", "url": "https://www.bleague.jp/player/19755/", "accessed_at": "2026-09-23"},
]

EVIDENCE: list[dict] = []
_evidence_seq = 190  # last used in wave_06 was B7E0190


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


# ---- P000103 渡邊雄太 ----
add_evidence("Person", "P000103", "name", "渡邊雄太", "B7S0047", "選手名", "bleague.jp選手プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000103", "date_of_birth", "1994-10-13", "B7S0047", "生年月日 > 1994年10月13日", "bleague.jp選手プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000353", "organization_id", "ORG000156", "B7S0047", "出身校 > 尽誠学園高等学校", "bleague.jp選手プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000354", "organization_id", "ORG000157", "B7S0047", "出身校 > ジョージ・ワシントン大学", "bleague.jp選手プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000355", "organization_id", "ORG000118", "B7S0047", "クラブ所属履歴 > 2026-27 千葉J", "bleague.jpのクラブ所属履歴で現所属クラブ（千葉ジェッツ）を確認", "SUPPORTED")
add_evidence("Career", "C000355", "organization_id", "ORG000118", "B7S0048", "TOP TEAM選手一覧 > 渡邊雄太", "千葉ジェッツ公式サイトのチームページでも現所属を確認（独立した第2ソース）", "SUPPORTED")

# ---- P000104 八村塁 ----
add_evidence("Person", "P000104", "name", "八村塁", "B7S0049", "冒頭", "Wikipediaで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000104", "date_of_birth", "1998-02-08", "B7S0049", "基本情報 > 1998年2月8日生まれ", "Wikipediaで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000356", "organization_id", "ORG000147", "B7S0049", "経歴 > 出身高校：明成高等学校（宮城県）", "Wikipediaで出身高校を確認。同校は2020年に仙台大学附属明成高等学校へ改称しており、八村塁の在籍時期（2013年頃〜2016年）は改称前のためORG000147（明成高等学校）をそのまま使用（Wave5・安藤誓哉と同一校）", "SUPPORTED")
add_evidence("Career", "C000357", "organization_id", "ORG000158", "B7S0049", "経歴 > ゴンザガ大学に進学", "Wikipediaで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000358", "organization_id", "ORG000140", "B7S0050", "本文 > 「発表日：2026年7月7日（現地時間6日）」「移籍前の所属：ロサンゼルス・レイカーズ」、ロサンゼルス・クリッパーズと2年契約", "basketballking.jpの記事（2026年7月7日付）でレイカーズからクリッパーズへの移籍・現所属を確認。Wikipediaはレイカーズ在籍までの記載で本移籍情報が反映されておらず古いため、本件は当記事を優先", "SUPPORTED", issue_note="Wikipediaの八村塁記事はクリッパーズ移籍（2026年7月）を反映しておらず、現所属の一次情報としては使用不可と判断した")

# ---- P000105 田臥勇太 ----
add_evidence("Person", "P000105", "name", "田臥勇太", "B7S0051", "選手名", "bleague.jp選手プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000105", "date_of_birth", "1980-10-05", "B7S0051", "生年月日 > 1980年10月5日", "bleague.jp選手プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000359", "organization_id", "ORG000159", "B7S0051", "出身校 > 秋田県立能代工業高等学校（現・秋田県立能代科学技術高等学校）", "bleague.jp選手プロフィールで出身高校を確認。同プロフィール自身が現校名（能代科学技術）への改称を注記しているため、在籍当時の校名である秋田県立能代工業高等学校で登録（改称後の現校名は不使用）", "SUPPORTED")
add_evidence("Career", "C000360", "organization_id", "ORG000160", "B7S0051", "出身校 > ブリガムヤング大学ハワイ校", "bleague.jp選手プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000361", "organization_id", "ORG000047", "B7S0051", "クラブ所属履歴 > 2026-27シーズン：宇都宮ブレックス（2023-24シーズン以降、継続して宇都宮ブレックス）", "bleague.jpのクラブ所属履歴で現所属クラブ（宇都宮ブレックス）を確認", "SUPPORTED")

# ---- P000106 富永啓生 ----
add_evidence("Person", "P000106", "name", "富永啓生", "B7S0052", "選手名", "bleague.jp選手プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000106", "date_of_birth", "2001-02-01", "B7S0052", "生年月日 > 2001年2月1日", "bleague.jp選手プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000362", "organization_id", "ORG000161", "B7S0052", "出身校 > 桜丘高等学校", "bleague.jp選手プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000363", "organization_id", "ORG000162", "B7S0052", "出身校 > ネブラスカ大学", "bleague.jp選手プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000364", "organization_id", "ORG000092", "B7S0052", "クラブ所属履歴 > 2026-27 北海道 / 2025-26 北海道", "bleague.jpのクラブ所属履歴で現所属クラブ（レバンガ北海道）を確認", "SUPPORTED")


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
_decision_seq = 93  # last used in wave_06 was B7D0093

add_decision("Person", "P000103", "READY_FOR_VERIFIED_REVIEW", "name|date_of_birth", "", "bleague.jp選手プロフィールで氏名・生年月日を確認")
add_decision("Career", "C000353", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpで出身高校（尽誠学園高等学校）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000354", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpで出身大学（ジョージ・ワシントン大学）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000355", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jp・千葉ジェッツ公式の独立した2ソースで現所属（千葉ジェッツ）を確認。開始日は資料なしのため保留")

add_decision("Person", "P000104", "READY_FOR_VERIFIED_REVIEW", "name|date_of_birth", "", "Wikipediaで氏名・生年月日を確認")
add_decision("Career", "C000356", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipediaで出身高校（明成高等学校、当時の校名）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000357", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "Wikipediaで出身大学（ゴンザガ大学）を確認。在籍期間は資料なしのため保留")
add_decision(
    "Career", "C000358", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end",
    "basketballking.jp（2026年7月7日付）でロサンゼルス・クリッパーズへの移籍・現所属を確認。"
    "Wikipediaは本移籍を反映しておらず古いため、日付の新しい一次情報を優先。開始日は資料なしのため保留",
)

add_decision("Person", "P000105", "READY_FOR_VERIFIED_REVIEW", "name|date_of_birth", "", "bleague.jp選手プロフィールで氏名・生年月日を確認")
add_decision(
    "Career", "C000359", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end",
    "bleague.jp選手プロフィールで出身高校を確認。改称後の現校名（秋田県立能代科学技術高等学校）ではなく、"
    "在籍当時の校名（秋田県立能代工業高等学校）で登録（歴史的組織名の保持ルールに従う）。在籍期間は資料なしのため保留",
)
add_decision("Career", "C000360", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpで出身大学（ブリガムヤング大学ハワイ校）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000361", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpのクラブ所属履歴で現所属（宇都宮ブレックス）を確認。開始日は資料なしのため保留")

add_decision("Person", "P000106", "READY_FOR_VERIFIED_REVIEW", "name|date_of_birth", "", "bleague.jp選手プロフィールで氏名・生年月日を確認")
add_decision("Career", "C000362", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpで出身高校（桜丘高等学校）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000363", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpで出身大学（ネブラスカ大学）を確認。在籍期間は資料なしのため保留")
add_decision("Career", "C000364", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "bleague.jpのクラブ所属履歴で現所属（レバンガ北海道）を確認。開始日は資料なしのため保留")

ISSUES = [
    {
        "issue_id": "B7I0024",
        "category": "CLUB_HISTORY_SCOPE",
        "scope": "P000103,P000104,P000105,P000106",
        "description": (
            "本Waveでは各選手について「出身校（高・大）」および「現所属クラブ」のCareerのみを記録し、"
            "移籍履歴の全チェーン（例：田臥勇太のNBA挑戦期を含む過去所属クラブ、渡邊雄太のNBA所属歴、"
            "八村塁のNBA移籍履歴：ウィザーズ→レイカーズ→クリッパーズ等）は記録していない。"
            "OrganizationAlias/組織承継ルールの設計がYuichiの判断待ちであるため、"
            "従来のWave（B4W3I0011→B7I0013→B7I0022→B7I0023）と同様にスコープを限定した。"
        ),
    },
    {
        "issue_id": "B7I0025",
        "category": "SOURCE_STALENESS",
        "scope": "P000104",
        "description": (
            "八村塁の現所属クラブについて、Wikipedia（B7S0049）はロサンゼルス・レイカーズ在籍までの記載で止まっており、"
            "2026年7月のロサンゼルス・クリッパーズへの移籍を反映していない。本Waveではbasketballking.jpの2026年7月7日付"
            "記事（B7S0050）を優先して現所属をクリッパーズとしたが、Wikipedia側の更新が確認でき次第、"
            "整合性の再確認が望ましい。"
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
        f"Wrote wave_07: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
