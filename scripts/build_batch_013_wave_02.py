#!/usr/bin/env python3
"""Build Batch 013 Wave 2 (東山高等学校, school 6/11, final wave) CANDIDATE data.

Second and final wave for 東山高等学校 (8 alumni total; see
build_batch_013_wave_01.py for Wave 1 and the school-level discovery
notes). This wave covers 岡田侑大, 堀田尚秀, 西部秀馬, 川嶋勇人.

東山高等学校 (ORG000195) was already minted in Wave 1 and is reused here
without a new ID. 関西学院大学 has no existing Organization ID and is
newly minted as ORG000196 (current max existing Organization ID before
this wave was ORG000195 from Wave 1 of this same batch).

Per the batch's approved scope, only the current club is registered as
Pro career (minimal path); prior clubs are logged as PRO_HISTORY_GAPS
issues. Two players here have long, multi-club histories:

- 岡田侑大: 三河(2018-19/2019-20) -> 富山(2020-21) -> 信州(2021-22/2022-23)
  -> 京都(2023-24/2024-25) -> 島根(2025-26〜, current).
- 川嶋勇人: 京都(2016-17, rookie season) -> 三遠(2017-18〜2020-21) ->
  秋田(2021-22/2022-23) -> FE名古屋(2023-24) -> 京都(2024-25〜, current --
  a return to the same club he started at 8 seasons earlier). Per the
  existing convention for same-club returns (see 津屋一球, batch_010;
  藤澤尚之, batch_013 wave_01), the current stint's start year is the
  return year (2024), not the original 2016 one.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_013" / "wave_02"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000161", "name": "岡田 侑大"},
    {"person_id": "P000162", "name": "堀田 尚秀"},
    {"person_id": "P000163", "name": "西部 秀馬"},
    {"person_id": "P000164", "name": "川嶋 勇人"},
]

# ORG000195(東山高等学校)はWave 1で新規登録済みのため再利用。ORG000031
# (拓殖大学)・ORG000155(島根スサノオマジック)・ORG000136(早稲田大学)・
# ORG000137(秋田ノーザンハピネッツ)・ORG000020(日本体育大学)・ORG000042
# (京都ハンナリーズ)は既存Organizationとして再利用 -- master + 全candidateの
# organization_candidates.csvと突き合わせ済み。関西学院大学は新規で、
# Wave 1時点の最大既存Organization IDはORG000195のため ORG000196 とした。
ORGANIZATIONS = [
    {"organization_id": "ORG000195", "name": "東山高等学校"},
    {"organization_id": "ORG000031", "name": "拓殖大学"},
    {"organization_id": "ORG000155", "name": "島根スサノオマジック"},
    {"organization_id": "ORG000136", "name": "早稲田大学"},
    {"organization_id": "ORG000137", "name": "秋田ノーザンハピネッツ"},
    {"organization_id": "ORG000020", "name": "日本体育大学"},
    {"organization_id": "ORG000042", "name": "京都ハンナリーズ"},
    {"organization_id": "ORG000196", "name": "関西学院大学"},
]

CAREERS = [
    # 岡田侑大（現所属は島根スサノオマジック、2025-26〜。三河・富山・信州・
    # 旧京都在籍はissue参照）
    {"career_id": "C000536", "person_id": "P000161", "organization_id": "ORG000195", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000537", "person_id": "P000161", "organization_id": "ORG000031", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000538", "person_id": "P000161", "organization_id": "ORG000155", "role": "Player", "start": "2025", "end": ""},
    # 堀田尚秀（現所属は秋田ノーザンハピネッツ、2025-26〜継続）
    {"career_id": "C000539", "person_id": "P000162", "organization_id": "ORG000195", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000540", "person_id": "P000162", "organization_id": "ORG000136", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000541", "person_id": "P000162", "organization_id": "ORG000137", "role": "Player", "start": "2025", "end": ""},
    # 西部秀馬（現所属は京都ハンナリーズ、2025-26〜継続）
    {"career_id": "C000542", "person_id": "P000163", "organization_id": "ORG000195", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000543", "person_id": "P000163", "organization_id": "ORG000020", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000544", "person_id": "P000163", "organization_id": "ORG000042", "role": "Player", "start": "2025", "end": ""},
    # 川嶋勇人（現所属は京都ハンナリーズへの復帰、2024-25〜。三遠・秋田・
    # FE名古屋在籍および旧京都在籍（2016-17）はissue参照）
    {"career_id": "C000545", "person_id": "P000164", "organization_id": "ORG000195", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000546", "person_id": "P000164", "organization_id": "ORG000196", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000547", "person_id": "P000164", "organization_id": "ORG000042", "role": "Player", "start": "2024", "end": ""},
]

SOURCES = [
    {"source_id": "B13W2S0001", "title": "岡田侑大 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=18475", "accessed_at": CHECKED_AT},
    {"source_id": "B13W2S0002", "title": "堀田尚秀 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000599", "accessed_at": CHECKED_AT},
    {"source_id": "B13W2S0003", "title": "西部秀馬 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000585", "accessed_at": CHECKED_AT},
    {"source_id": "B13W2S0004", "title": "川嶋勇人 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8727", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B13W2E{_evidence_seq:04d}",
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


# --- 岡田侑大 ---
add_evidence("Person", "P000161", "name", "岡田 侑大", "B13W2S0001", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000161", "birth_date", "1998-06-10", "B13W2S0001", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000536", "organization_id", "ORG000195", "B13W2S0001", "基本情報 > 出身校（高）：東山高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000537", "organization_id", "ORG000031", "B13W2S0001", "基本情報 > 出身校（大）：拓殖大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000538", "organization_id", "ORG000155", "B13W2S0001", "クラブ経歴 > 「2025-26：島根」が最新", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED",
             issue_note="三河（2018-19・2019-20）、富山（2020-21）、信州（2021-22・2022-23）、旧京都在籍（2023-24・2024-25）は今回のWaveでは対象外。詳細はissue B13W2I0003を参照")
add_evidence("Career", "C000538", "start", "2025", "B13W2S0001", "クラブ経歴 > 「2025-26：島根」が最新", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入を確認", "SUPPORTED")

# --- 堀田尚秀 ---
add_evidence("Person", "P000162", "name", "堀田 尚秀", "B13W2S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000162", "birth_date", "2003-07-31", "B13W2S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000539", "organization_id", "ORG000195", "B13W2S0002", "基本情報 > 出身校（高）：東山高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000540", "organization_id", "ORG000136", "B13W2S0002", "基本情報 > 出身校（大）：早稲田大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000541", "organization_id", "ORG000137", "B13W2S0002", "クラブ経歴 > 「2025-26：秋田」が初出（唯一の在籍クラブ）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000541", "start", "2025", "B13W2S0002", "クラブ経歴 > 「2025-26：秋田」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 西部秀馬 ---
add_evidence("Person", "P000163", "name", "西部 秀馬", "B13W2S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000163", "birth_date", "2003-05-20", "B13W2S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000542", "organization_id", "ORG000195", "B13W2S0003", "基本情報 > 出身校（高）：東山高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000543", "organization_id", "ORG000020", "B13W2S0003", "基本情報 > 出身校（大）：日本体育大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000544", "organization_id", "ORG000042", "B13W2S0003", "クラブ経歴 > 「2025-26：京都」が初出（唯一の在籍クラブ）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000544", "start", "2025", "B13W2S0003", "クラブ経歴 > 「2025-26：京都」が初出", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 川嶋勇人 ---
add_evidence("Person", "P000164", "name", "川嶋 勇人", "B13W2S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000164", "birth_date", "1990-05-15", "B13W2S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000545", "organization_id", "ORG000195", "B13W2S0004", "基本情報 > 出身校（高）：東山高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000546", "organization_id", "ORG000196", "B13W2S0004", "基本情報 > 出身校（大）：関西学院大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000547", "organization_id", "ORG000042", "B13W2S0004", "クラブ経歴 > 「2024-25：京都」以降継続、2016-17に同クラブでのルーキーシーズンあり", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの復帰を確認", "SUPPORTED",
             issue_note="三遠（2017-18〜2020-21）、秋田（2021-22・2022-23）、FE名古屋（2023-24）在籍、および2016-17の京都での最初の在籍は今回のWaveでは対象外。詳細はissue B13W2I0004を参照")
add_evidence("Career", "C000547", "start", "2024", "B13W2S0004", "クラブ経歴 > 「2024-25：京都」が復帰後の初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの京都復帰を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B13W2D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000161", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000536", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000537", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000538", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去クラブ在籍はissueに記録")

add_decision("Person", "P000162", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000539", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000540", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000541", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000163", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000542", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000543", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000544", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000164", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000545", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000546", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000547", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去クラブ在籍・旧京都在籍はissueに記録")

ISSUES = [
    {"issue_id": "B13W2I0001", "person_id": "P000161|P000162|P000163|P000164", "related_id": "C000536|C000539|C000542|C000545", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "4名とも東山高等学校在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B13W2I0002", "person_id": "P000161|P000162|P000163|P000164", "related_id": "C000537|C000540|C000543|C000546", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "4名とも大学在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B13W2I0003", "person_id": "P000161", "related_id": "P000161", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "岡田侑大は現所属（島根スサノオマジック、2025-26〜）以前に三河（2018-19・2019-20）、富山（2020-21）、信州（2021-22・2022-23）、旧京都在籍（2023-24・2024-25）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B13W2I0004", "person_id": "P000164", "related_id": "P000164", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "川嶋勇人は現所属（京都ハンナリーズ、2024-25〜）が2016-17シーズンのルーキー時に一度在籍したクラブへの復帰であり、その間に三遠（2017-18〜2020-21）、秋田（2021-22・2022-23）、FE名古屋（2023-24）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できる。今回のWaveでは現在の京都復帰後の在籍のみを最小経路として登録し、過去クラブおよび2016-17の最初の京都在籍は対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加（2016-17の最初の京都在籍を含む）"},
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
        f"Wrote batch_013/wave_02: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
