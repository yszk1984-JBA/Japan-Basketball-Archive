#!/usr/bin/env python3
"""Build Batch 007 Wave 8 (深掘りWave / Enrichment Wave).

Test case for "過去在籍チームの深掘り" per Yuichi's question after Wave 8
(batch_004/wave_06): can past-club history be added via enrichment waves?

Target: 辻直人 (P000097, still CANDIDATE from batch_007/wave_05). Wave 5
recorded only his current club (群馬クレインサンダーズ) plus school/
university, deliberately deferring past-club history (issue B7I0022,
CLUB_HISTORY_SCOPE). This wave fills in his full pro career:
東芝ブレイブサンダース (2012-2016, pre-B.League/NBL era) -> 川崎ブレイブ
サンダース (2016-2021, B.League era) -> 広島ドラゴンフライズ
(2021-2023) -> 群馬クレインサンダーズ (2023-, already recorded in
wave_05 as C000339; this wave adds its start year via new
evidence/decision, without touching wave_05's own files).

Governance note: 辻直人 joined the Toshiba-owned team in 2012 when it was
named 東芝ブレイブサンダース. That same organization later renamed
(2013: 東芝ブレイブサンダース神奈川; 2016-07-01: league designation
becomes 川崎ブレイブサンダース; 2018: ownership moves from Toshiba to
DeNA). Per the historical-organization-naming rule, a new Organization
(東芝ブレイブサンダース, ORG000164) is registered for the pre-2016 era,
distinct from the already-registered ORG000122 (川崎ブレイブサンダース,
used for the B.League era 2016-2021, matching bleague.jp's own season
labels). The 2013 "神奈川" sub-rename is NOT separately modeled here
(flagged as a granularity simplification in the issue below) -- this is
the third concrete instance of the same organization-rename pattern
already seen with サンロッカーズ渋谷->東京サンロッカーズ and
湘南ユナイテッドBC->ウォルガ湘南.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_007" / "wave_08"

PERSONS: list[dict] = []  # enrichment wave: no new persons

ORGANIZATIONS = [
    {"organization_id": "ORG000164", "name": "東芝ブレイブサンダース"},
]

CAREERS = [
    {"career_id": "C000366", "person_id": "P000097", "organization_id": "ORG000164", "role": "Player", "start": "2012", "end": "2016"},
    {"career_id": "C000367", "person_id": "P000097", "organization_id": "ORG000122", "role": "Player", "start": "2016", "end": "2021"},
    {"career_id": "C000368", "person_id": "P000097", "organization_id": "ORG000110", "role": "Player", "start": "2021", "end": "2023"},
]

SOURCES = [
    {"source_id": "B7S0053", "title": "辻直人", "publisher": "Wikipedia日本語版", "url": "https://ja.wikipedia.org/wiki/辻直人", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0054", "title": "辻直人 選手情報", "publisher": "B.LEAGUE公式 (bleague.jp, PlayerID=8487)", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8487", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0055", "title": "辻直人 選手ページ（SEASON別CLUB一覧）", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/player/article/8196.html", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0056", "title": "川崎ブレイブサンダース", "publisher": "Wikipedia日本語版", "url": "https://ja.wikipedia.org/wiki/川崎ブレイブサンダース", "accessed_at": "2026-09-23"},
]

EVIDENCE: list[dict] = []
_evidence_seq = 211  # last used in wave_07 was B7E0211


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


# --- C000366 東芝ブレイブサンダース（2012-2016） ---
add_evidence("Career", "C000366", "organization_id", "ORG000164", "B7S0053", "経歴 > 「2012年4月、東芝ブレイブサンダースに入団」", "Wikipediaで東芝ブレイブサンダース入団を確認", "SUPPORTED")
add_evidence("Career", "C000366", "start", "2012", "B7S0053", "同上", "入団年（2012年）を確認", "SUPPORTED")
add_evidence(
    "Career", "C000366", "end", "2016", "B7S0056",
    "沿革 > 「2016年7月1日、正式クラブ名を『東芝川崎ブレイブサンダース』、リーグでのチーム呼称を『川崎ブレイブサンダース』に変更した」",
    "川崎ブレイブサンダースのWikipedia沿革により、2016年7月1日付でリーグ上の呼称が「川崎ブレイブサンダース」に変わったことを確認。辻直人本人が別組織に移籍したのではなく、在籍中の組織自体の名称変更であるため、end=2016は組織名変更時期からの導出（PARTIAL）",
    "PARTIAL",
    issue_note="2013年に一時「東芝ブレイブサンダース神奈川」への改称もあったが、本Waveでは細分化せず「東芝ブレイブサンダース」としてまとめている（粒度の簡略化）",
)

# --- C000367 川崎ブレイブサンダース（2016-2021、B.LEAGUE時代） ---
add_evidence("Career", "C000367", "organization_id", "ORG000122", "B7S0054", "クラブ所属履歴 > 2016-17〜2020-21：川崎ブレイブサンダース", "bleague.jp公式のクラブ所属履歴で2016-17〜2020-21シーズンの川崎ブレイブサンダース在籍を確認", "SUPPORTED")
add_evidence("Career", "C000367", "organization_id", "ORG000122", "B7S0055", "SEASON別CLUB一覧 > 2016-2017〜2020-2021：川崎", "バスケットボールキングの選手成績ページでも同シーズン区間の川崎在籍を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000367", "start", "2016", "B7S0054", "同上（bleague.jp所属履歴の初出シーズン2016-17）", "B.LEAGUE開幕（2016-17シーズン）時点で川崎ブレイブサンダース名義だったことを確認", "SUPPORTED")
add_evidence("Career", "C000367", "end", "2021", "B7S0053", "経歴 > 「2021年5月31日、川崎を退団」し、「同年6月2日に広島ドラゴンフライズへの移籍が発表」", "Wikipediaで川崎退団の正確な日付を確認", "SUPPORTED")

# --- C000368 広島ドラゴンフライズ（2021-2023） ---
add_evidence("Career", "C000368", "organization_id", "ORG000110", "B7S0053", "経歴 > 「同年6月2日に広島ドラゴンフライズへの移籍が発表」", "Wikipediaで広島ドラゴンフライズへの移籍を確認", "SUPPORTED")
add_evidence("Career", "C000368", "organization_id", "ORG000110", "B7S0054", "クラブ所属履歴 > 2021-22〜2022-23：広島ドラゴンフライズ", "bleague.jp公式のクラブ所属履歴でも同シーズン区間の広島在籍を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000368", "start", "2021", "B7S0053", "同上", "移籍発表日（2021年6月2日）から開始年を確認", "SUPPORTED")
add_evidence("Career", "C000368", "end", "2023", "B7S0053", "経歴 > 「2023年5月24日に広島ドラゴンフライズを退団することが発表され、同年6月8日に群馬クレインサンダーズへの加入が決定」", "Wikipediaで広島退団の正確な日付を確認", "SUPPORTED")

# --- C000339（既存Career、群馬クレインサンダーズ、wave_05由来）: startを補足 ---
add_evidence("Career", "C000339", "start", "2023", "B7S0053", "経歴 > 「同年6月8日に群馬クレインサンダーズへの加入が決定」", "Wikipediaで群馬クレインサンダーズ加入決定日（2023年6月8日）を確認。Wave5では未確認だったstartを補足", "SUPPORTED")


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
_decision_seq = 109  # last used in wave_07 was B7D0109

add_decision(
    "Career", "C000366", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
    "Wikipediaで2012年の東芝ブレイブサンダース入団を確認。endは組織自体の名称変更時期（2016年7月1日、川崎ブレイブサンダースへ改称）からの導出のためPARTIAL評価だが、"
    "辻直人本人の移籍を伴わない期間区切りであり、組織名変更という客観的事実に基づくためREADYとする。2013年の「神奈川」を含む一時改称は簡略化して未反映（issue参照）",
)
add_decision(
    "Career", "C000367", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
    "bleague.jp公式・バスケットボールキングの独立した2ソースで2016-17〜2020-21シーズンの川崎ブレイブサンダース在籍を確認。"
    "start(2016)はB.LEAGUE開幕時点の所属、end(2021)はWikipediaの退団日（2021年5月31日）で確認",
)
add_decision(
    "Career", "C000368", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
    "Wikipedia・bleague.jp公式の独立した2ソースで2021-22〜2022-23シーズンの広島ドラゴンフライズ在籍を確認。"
    "start(2021)・end(2023)ともWikipediaの移籍発表日・退団発表日で確認",
)
add_decision(
    "Career", "C000339", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end",
    "Wave5では確認できなかったstartを、Wikipediaの群馬クレインサンダーズ加入決定日（2023年6月8日）により補足。"
    "endは現所属のため未確定（保留継続）",
)

ISSUES = [
    {
        "issue_id": "B7I0026",
        "category": "ORG_SUCCESSION",
        "scope": "P000097",
        "description": (
            "東芝ブレイブサンダース（本Waveで新規登録、ORG000164）と、既存のORG000122（川崎ブレイブサンダース）は、"
            "2016年7月1日のリーグ呼称変更前後における同一組織である。サンロッカーズ渋谷->東京サンロッカーズ"
            "（batch_007/wave_02、B7I0013）、湘南ユナイテッドBC->ウォルガ湘南（batch_004/wave_06、B4W6I0001）に続く"
            "3件目の同種事例。さらに、東芝ブレイブサンダースは2013年に一時「東芝ブレイブサンダース神奈川」への改称も"
            "経ており、本Waveではこの中間名称を独立Organizationとして分離せず簡略化している（粒度の簡略化）。"
            "OrganizationAlias/組織承継ルールの設計時に、両論点（組織承継・改称の粒度）をあわせて整理する必要がある。"
        ),
    },
    {
        "issue_id": "B7I0027",
        "category": "CLUB_HISTORY_SCOPE_RESOLVED",
        "scope": "P000097",
        "description": (
            "batch_007/wave_05のissue B7I0022（現所属クラブ以前の過去所属クラブは対象外）について、辻直人分を本Waveで解消した。"
            "東芝ブレイブサンダース(2012-2016)->川崎ブレイブサンダース(2016-2021)->広島ドラゴンフライズ(2021-2023)->"
            "群馬クレインサンダーズ(2023-、既存C000339のstartを補足)という全プロキャリアを記録済み。"
            "他の選手（渡邊雄太・八村塁のNBA移籍歴等）についてはB7I0024として引き続き未対応。"
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
        f"Wrote wave_08: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} new careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
