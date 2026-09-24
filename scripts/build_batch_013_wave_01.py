#!/usr/bin/env python3
"""Build Batch 013 Wave 1 (東山高等学校, school 6/11) CANDIDATE data.

Sixth school of the powerhouse-school expansion initiative (see
docs/BATCH_008_PROPOSAL.md). 東山高等学校 (Kyoto) has no existing
Organization ID -- newly minted here as ORG000195.

Discovery: B.LEAGUE's "ワタシノB.LEAGUE" tag list for TagID=35:東山高等学校
was accessed directly (per the URL pattern discovered in batch_011/used
again in batch_012). It shows exactly 8 current alumni -- no "もっと
見る" pagination needed. All 8 are genuinely new to the project (checked
against data/master/person.csv and every existing
person_candidates.csv). Standard 4/wave sizing applies (see
docs/BATCH_008_PROPOSAL.md), so this school spans 2 waves; this is
Wave 1 of 2 (藤澤尚之, 瀬川琉久, 堀陽稀, 米須玲音).

Per the batch's approved scope, only the current club is registered as
Pro career (minimal path: high school -> university (if any) ->
current club); prior clubs found in each player's クラブ所属履歴 are
logged as PRO_HISTORY_GAPS issues instead of being added as Career
rows, matching the convention used throughout batch_008-012.

Notable: 瀬川琉久 has no university (出身校（大）: "-") -- a high-school-
to-pro case like 平良宗龍 in batch_011, so his path is 高校 -> 現所属クラブ
only (2 Careers). 米須玲音's クラブ所属履歴 shows 2020-21/2021-22 appearances
with 川崎ブレイブサンダース while he would still have been a high-school
student (born 2003-01, 東山高等学校卒業前とみられる時期), then a gap for
2022-23/2023-24 (university years), before returning to the same club
full-time from 2024-25 -- treated as a single current stint starting
2024, with the earlier high-school-era appearances and the gap logged
as an issue rather than assumed to be continuous employment. 藤澤尚之
is a case of returning to a club he had already played for (熊本,
2020-21/2021-22) after two other clubs (奈良, 福井) -- per the existing
convention for same-club returns (see 津屋一球, batch_010), the current
stint's start year is the return year (2026), not the original one.
His history also has an unexplained gap at 2023-24 (no entry between
2024-25 福井 and 2022-23 奈良) which is not guessed at.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_013" / "wave_01"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000157", "name": "藤澤 尚之"},
    {"person_id": "P000158", "name": "瀬川 琉久"},
    {"person_id": "P000159", "name": "堀 陽稀"},
    {"person_id": "P000160", "name": "米須 玲音"},
]

# ORG000067(熊本ヴォルターズ)・ORG000168(天理大学)・ORG000118(千葉ジェッツ)・
# ORG000136(早稲田大学)・ORG000190(越谷アルファーズ)・ORG000121(日本大学)・
# ORG000122(川崎ブレイブサンダース) は既存Organizationとして再利用 -- master
# + 全candidateのorganization_candidates.csvと突き合わせ済み。東山高等学校は
# 新規で、現在の最大既存Organization IDはORG000194（batch_012）のため
# ORG000195 とした（batch_013 wave_02でも同じIDを再利用する）。
ORGANIZATIONS = [
    {"organization_id": "ORG000195", "name": "東山高等学校"},
    {"organization_id": "ORG000168", "name": "天理大学"},
    {"organization_id": "ORG000067", "name": "熊本ヴォルターズ"},
    {"organization_id": "ORG000118", "name": "千葉ジェッツ"},
    {"organization_id": "ORG000136", "name": "早稲田大学"},
    {"organization_id": "ORG000190", "name": "越谷アルファーズ"},
    {"organization_id": "ORG000121", "name": "日本大学"},
    {"organization_id": "ORG000122", "name": "川崎ブレイブサンダース"},
]

CAREERS = [
    # 藤澤尚之（現所属は熊本ヴォルターズへの復帰、2026-27〜。福井・奈良・
    # 旧熊本在籍および2023-24の空白はissue参照）
    {"career_id": "C000525", "person_id": "P000157", "organization_id": "ORG000195", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000526", "person_id": "P000157", "organization_id": "ORG000168", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000527", "person_id": "P000157", "organization_id": "ORG000067", "role": "Player", "start": "2026", "end": ""},
    # 瀬川琉久（大学経由なし、高校→現所属クラブ。2024-25〜継続して千葉ジェッツ）
    {"career_id": "C000528", "person_id": "P000158", "organization_id": "ORG000195", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000529", "person_id": "P000158", "organization_id": "ORG000118", "role": "Player", "start": "2024", "end": ""},
    # 堀陽稀（現所属は越谷アルファーズ、2025-26〜継続）
    {"career_id": "C000530", "person_id": "P000159", "organization_id": "ORG000195", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000531", "person_id": "P000159", "organization_id": "ORG000136", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000532", "person_id": "P000159", "organization_id": "ORG000190", "role": "Player", "start": "2025", "end": ""},
    # 米須玲音（現所属は川崎ブレイブサンダース。高校在学中とみられる早期在籍・
    # 大学期間中の空白はissue参照、現在の連続在籍は2024-25〜）
    {"career_id": "C000533", "person_id": "P000160", "organization_id": "ORG000195", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000534", "person_id": "P000160", "organization_id": "ORG000121", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000535", "person_id": "P000160", "organization_id": "ORG000122", "role": "Player", "start": "2024", "end": ""},
]

SOURCES = [
    {"source_id": "B13W1S0001", "title": "ワタシノB.LEAGUE選手一覧 | 東山高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:東山高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B13W1S0002", "title": "藤澤尚之 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=5100000019", "accessed_at": CHECKED_AT},
    {"source_id": "B13W1S0003", "title": "瀬川琉久 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000467", "accessed_at": CHECKED_AT},
    {"source_id": "B13W1S0004", "title": "堀陽稀 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000588", "accessed_at": CHECKED_AT},
    {"source_id": "B13W1S0005", "title": "米須玲音 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=5100000022", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B13W1E{_evidence_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "field_name": field_name,
        "candidate_value": candidate_value,
        "source_id": source_id,
        "source_locator": source_locator,
        "evidence_summary": evidence_summary,
        "assessment": assessment,
        "checked_at": CHECKED_AT,
        "issue_note": issue_note,
    })


# --- 藤澤尚之 ---
add_evidence("Person", "P000157", "name", "藤澤 尚之", "B13W1S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000157", "birth_date", "1998-06-19", "B13W1S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000525", "organization_id", "ORG000195", "B13W1S0002", "基本情報 > 出身校（高）：東山高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000526", "organization_id", "ORG000168", "B13W1S0002", "基本情報 > 出身校（大）：天理大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000527", "organization_id", "ORG000067", "B13W1S0002", "クラブ経歴 > 「2026-27：熊本」が最新", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="福井（2024-25・2025-26）、奈良（2022-23）、旧熊本在籍（2020-21・2021-22）、および2023-24の記載空白は今回のWaveでは対象外。詳細はissue B13W1I0003を参照")
add_evidence("Career", "C000527", "start", "2026", "B13W1S0002", "クラブ経歴 > 「2026-27：熊本」が最新", "B.LEAGUE公式のクラブ所属履歴で熊本への復帰（2026-27シーズン）を確認", "SUPPORTED")

# --- 瀬川琉久 ---
add_evidence("Person", "P000158", "name", "瀬川 琉久", "B13W1S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000158", "birth_date", "2006-08-14", "B13W1S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000528", "organization_id", "ORG000195", "B13W1S0003", "基本情報 > 出身校（高）：東山高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000529", "organization_id", "ORG000118", "B13W1S0003", "クラブ経歴 > 「2024-25：千葉J」が初出（唯一の在籍クラブ）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000529", "start", "2024", "B13W1S0003", "クラブ経歴 > 「2024-25：千葉J」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 堀陽稀 ---
add_evidence("Person", "P000159", "name", "堀 陽稀", "B13W1S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000159", "birth_date", "2003-05-13", "B13W1S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000530", "organization_id", "ORG000195", "B13W1S0004", "基本情報 > 出身校（高）：東山高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000531", "organization_id", "ORG000136", "B13W1S0004", "基本情報 > 出身校（大）：早稲田大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000532", "organization_id", "ORG000190", "B13W1S0004", "クラブ経歴 > 「2025-26：越谷」が初出（唯一の在籍クラブ）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000532", "start", "2025", "B13W1S0004", "クラブ経歴 > 「2025-26：越谷」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 米須玲音 ---
add_evidence("Person", "P000160", "name", "米須 玲音", "B13W1S0005", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000160", "birth_date", "2003-01-14", "B13W1S0005", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000533", "organization_id", "ORG000195", "B13W1S0005", "基本情報 > 出身校（高）：東山高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000534", "organization_id", "ORG000121", "B13W1S0005", "基本情報 > 出身校（大）：日本大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000535", "organization_id", "ORG000122", "B13W1S0005", "クラブ経歴 > 一貫して「川崎」、現在は「2024-25」以降継続", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="2020-21・2021-22シーズンの川崎在籍（高校在学中とみられる時期）と、2022-23・2023-24シーズンの記載空白（大学在学期間とみられる）は今回のWaveでは対象外。詳細はissue B13W1I0004を参照")
add_evidence("Career", "C000535", "start", "2024", "B13W1S0005", "クラブ経歴 > 「2024-25：川崎」が現在の連続在籍の起点", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの現在の連続在籍開始を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B13W1D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000157", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000525", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000526", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000527", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去クラブ在籍・空白シーズンはissueに記録")

add_decision("Person", "P000158", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000528", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000529", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000159", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000530", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000531", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000532", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000160", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000533", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000534", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000535", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去の早期在籍・空白はissueに記録")

ISSUES = [
    {"issue_id": "B13W1I0001", "person_id": "P000157|P000158|P000159|P000160", "related_id": "C000525|C000528|C000530|C000533", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "4名とも東山高等学校在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B13W1I0002", "person_id": "P000157|P000159|P000160", "related_id": "C000526|C000531|C000534", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "3名（藤澤尚之・堀陽稀・米須玲音）とも大学在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B13W1I0003", "person_id": "P000157", "related_id": "P000157", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "藤澤尚之は現所属（熊本ヴォルターズ、2026-27〜）以前に熊本（2020-21・2021-22、今回とは別の在籍期間）、奈良（2022-23）、福井（2024-25・2025-26）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現在の熊本復帰後の在籍のみを最小経路として登録し、過去クラブは対象外とした。加えて、同履歴には2023-24シーズンの記載が一切なく（2024-25福井の次が2022-23奈良で、間が空白）、空白理由は資料からは確認できず憶測で埋めていない。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加するとともに、2023-24シーズンの空白理由を追加情報源で確認"},
    {"issue_id": "B13W1I0004", "person_id": "P000160", "related_id": "P000160", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "米須玲音（1998年ではなく2003年1月生）はB.LEAGUE公式のクラブ所属履歴上、2020-21・2021-22シーズンに川崎ブレイブサンダースへの在籍記録があるが、この時期は本人が東山高等学校在学中とみられる（高校生年代での特別な起用の可能性があるが、詳細な契約形態は資料からは確認できない）。続く2022-23・2023-24シーズンは同履歴に記載がなく、大学（日本大学）在学期間と重なる可能性があるが、これも資料からは確認できない。今回のWaveでは2024-25シーズン以降の現在の連続在籍のみを最小経路として登録し、上記の早期在籍・空白期間は対象外とした。",
     "next_check": "高校生年代での起用形態（特別指定選手等の可能性）および大学在籍期間中の空白理由を追加情報源で確認"},
]


def main() -> None:
    write_csv(BASE / "person_candidates.csv", ["person_id", "name"], PERSONS)
    write_csv(BASE / "organization_candidates.csv", ["organization_id", "name"], ORGANIZATIONS)
    write_csv(BASE / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], CAREERS)
    write_csv(BASE / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], SOURCES)
    write_csv(BASE / "evidence_records.csv", [
        "record_id", "entity_type", "entity_id", "field_name", "candidate_value",
        "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note",
    ], EVIDENCE)
    write_csv(BASE / "issues.csv", [
        "issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check",
    ], ISSUES)
    write_csv(BASE / "qa_decisions.csv", [
        "decision_id", "entity_type", "entity_id", "decision",
        "eligible_fields", "held_fields", "reason", "reviewed_at",
    ], DECISIONS)
    print(
        f"Wrote batch_013/wave_01: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
