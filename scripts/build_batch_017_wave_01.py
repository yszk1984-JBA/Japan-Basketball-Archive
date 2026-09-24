#!/usr/bin/env python3
"""Build Batch 017 Wave 1 (土浦日本大学高等学校, school 10/11) CANDIDATE data.

Tenth school of the powerhouse-school expansion initiative (see
docs/BATCH_008_PROPOSAL.md). 土浦日本大学高等学校 already has an
existing Organization ID (ORG000134, first registered in
batch_007/wave_03) -- reused here, not newly minted. This is distinct
from ORG000121 (日本大学 itself), which several of this school's
alumni separately list as their university.

Discovery: B.LEAGUE's "ワタシノB.LEAGUE" tag list for
TagID=35:土浦日本大学高等学校 was accessed directly. It shows exactly
6 current alumni -- no "もっと見る" pagination needed. All 6 are
genuinely new to the project. Standard 4/wave sizing applies, so this
school spans 2 waves; this is Wave 1 of 2 (松村竜吾, 落合知也, 陳岡流羽,
中野広大).

Per the batch's approved scope, only the current club is registered as
Pro career (minimal path); prior clubs are logged as PRO_HISTORY_GAPS
issues.

Notable: 陳岡流羽（Wave 1）と陳岡燈生（Wave 2）は同姓・同じ出身地（茨城県）
だが、近親関係を示す一次資料は確認できていないため、関係については
一切記録せず、README側に観察メモとしてのみ残す。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_017" / "wave_01"
CHECKED_AT = "2026-09-25"

PERSONS = [
    {"person_id": "P000186", "name": "松村 竜吾"},
    {"person_id": "P000187", "name": "落合 知也"},
    {"person_id": "P000188", "name": "陳岡 流羽"},
    {"person_id": "P000189", "name": "中野 広大"},
]

# ORG000134(土浦日本大学高等学校)・ORG000121(日本大学)・
# ORG000111(東京八王子ビートレインズ)・ORG000174(しながわシティ
# バスケットボールクラブ)・ORG000103(茨城ロボッツ)・
# ORG000050(ウォルガ湘南) は既存Organizationとして再利用 -- master +
# 全candidateのorganization_candidates.csvと突き合わせ済み。
# 法政大学・白鴎大学は新規登録（現在の最大既存Organization IDは
# ORG000206、batch_015のため ORG000207-208 とした）。
ORGANIZATIONS = [
    {"organization_id": "ORG000134", "name": "土浦日本大学高等学校"},
    {"organization_id": "ORG000121", "name": "日本大学"},
    {"organization_id": "ORG000111", "name": "東京八王子ビートレインズ"},
    {"organization_id": "ORG000207", "name": "法政大学"},
    {"organization_id": "ORG000174", "name": "しながわシティバスケットボールクラブ"},
    {"organization_id": "ORG000208", "name": "白鴎大学"},
    {"organization_id": "ORG000103", "name": "茨城ロボッツ"},
    {"organization_id": "ORG000050", "name": "ウォルガ湘南"},
]

CAREERS = [
    # 松村竜吾（現所属は東京八王子ビートレインズ、2026-27〜。新規加入。
    # 直前の広島ドラゴンフライズ在籍はissue参照）
    {"career_id": "C000611", "person_id": "P000186", "organization_id": "ORG000134", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000612", "person_id": "P000186", "organization_id": "ORG000121", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000613", "person_id": "P000186", "organization_id": "ORG000111", "role": "Player", "start": "2026", "end": ""},
    # 落合知也（現所属はしながわシティバスケットボールクラブ、
    # 2024-25〜。過去の越谷アルファーズ・栃木ブレックス在籍はissue参照）
    {"career_id": "C000614", "person_id": "P000187", "organization_id": "ORG000134", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000615", "person_id": "P000187", "organization_id": "ORG000207", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000616", "person_id": "P000187", "organization_id": "ORG000174", "role": "Player", "start": "2024", "end": ""},
    # 陳岡流羽（B.LEAGUEデビューから一貫して茨城ロボッツ、移籍・空白なし）
    {"career_id": "C000617", "person_id": "P000188", "organization_id": "ORG000134", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000618", "person_id": "P000188", "organization_id": "ORG000208", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000619", "person_id": "P000188", "organization_id": "ORG000103", "role": "Player", "start": "2024", "end": ""},
    # 中野広大（現所属はウォルガ湘南、2022-23〜。過去の群馬クレイン
    # サンダーズ・岩手ビッグブルズ・さいたまブロンコス在籍はissue参照）
    {"career_id": "C000620", "person_id": "P000189", "organization_id": "ORG000134", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000621", "person_id": "P000189", "organization_id": "ORG000207", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000622", "person_id": "P000189", "organization_id": "ORG000050", "role": "Player", "start": "2022", "end": ""},
]

SOURCES = [
    {"source_id": "B17W1S0001", "title": "ワタシノB.LEAGUE選手一覧 | 土浦日本大学高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:土浦日本大学高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B17W1S0002", "title": "松村竜吾 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000550", "accessed_at": CHECKED_AT},
    {"source_id": "B17W1S0003", "title": "落合知也 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8648", "accessed_at": CHECKED_AT},
    {"source_id": "B17W1S0004", "title": "陳岡流羽 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000479", "accessed_at": CHECKED_AT},
    {"source_id": "B17W1S0005", "title": "中野広大 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=10892", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B17W1E{_evidence_seq:04d}",
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


# --- 松村竜吾 ---
add_evidence("Person", "P000186", "name", "松村 竜吾", "B17W1S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000186", "birth_date", "2002-09-13", "B17W1S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000611", "organization_id", "ORG000134", "B17W1S0002", "基本情報 > 出身校（高）：土浦日本大学高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000612", "organization_id", "ORG000121", "B17W1S0002", "基本情報 > 出身校（大）：日本大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000613", "organization_id", "ORG000111", "B17W1S0002", "クラブ経歴 > 「2026-27：八王子」が最新（新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="広島ドラゴンフライズ（2025-26）在籍は今回のWaveでは対象外。詳細はissue B17W1I0003を参照")
add_evidence("Career", "C000613", "start", "2026", "B17W1S0002", "クラブ経歴 > 「2026-27：八王子」が最新", "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの加入を確認", "SUPPORTED")

# --- 落合知也 ---
add_evidence("Person", "P000187", "name", "落合 知也", "B17W1S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000187", "birth_date", "1987-06-18", "B17W1S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000614", "organization_id", "ORG000134", "B17W1S0003", "基本情報 > 出身校（高）：土浦日本大学高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000615", "organization_id", "ORG000207", "B17W1S0003", "基本情報 > 出身校（大）：法政大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000616", "organization_id", "ORG000174", "B17W1S0003", "クラブ経歴 > 「2024-25：品川」が初出（現所属への新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="越谷アルファーズ（2017-18〜2022-23）・栃木ブレックス（2016-17〜2017-18、宇都宮ブレックスの当時の名称）在籍、および2023-24シーズンの空白は今回のWaveでは対象外。詳細はissue B17W1I0004を参照")
add_evidence("Career", "C000616", "start", "2024", "B17W1S0003", "クラブ経歴 > 「2024-25：品川」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入を確認", "SUPPORTED")

# --- 陳岡流羽 ---
add_evidence("Person", "P000188", "name", "陳岡 流羽", "B17W1S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000188", "birth_date", "2003-02-01", "B17W1S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000617", "organization_id", "ORG000134", "B17W1S0004", "基本情報 > 出身校（高）：土浦日本大学高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000618", "organization_id", "ORG000208", "B17W1S0004", "基本情報 > 出身校（大）：白鴎大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000619", "organization_id", "ORG000103", "B17W1S0004", "クラブ経歴 > 「2024-25：茨城」が初出（唯一の在籍クラブ）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000619", "start", "2024", "B17W1S0004", "クラブ経歴 > 「2024-25：茨城」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 中野広大 ---
add_evidence("Person", "P000189", "name", "中野 広大", "B17W1S0005", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000189", "birth_date", "1994-05-08", "B17W1S0005", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000620", "organization_id", "ORG000134", "B17W1S0005", "基本情報 > 出身校（高）：土浦日本大学高等学校", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000621", "organization_id", "ORG000207", "B17W1S0005", "基本情報 > 出身校（大）：法政大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000622", "organization_id", "ORG000050", "B17W1S0005", "クラブ経歴 > 「2022-23：湘南」が初出（現所属への新規加入）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブへの加入を確認", "SUPPORTED",
             issue_note="群馬クレインサンダーズ（2016-17〜2018-19）・岩手ビッグブルズ（2018-19〜2019-20）・さいたまブロンコス（2020-21〜2021-22）在籍は今回のWaveでは対象外。詳細はissue B17W1I0005を参照")
add_evidence("Career", "C000622", "start", "2022", "B17W1S0005", "クラブ経歴 > 「2022-23：湘南」が初出", "B.LEAGUE公式のクラブ所属履歴で2022-23シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B17W1D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


for pid, cids in [
    ("P000186", ["C000611", "C000612", "C000613"]),
    ("P000187", ["C000614", "C000615", "C000616"]),
    ("P000188", ["C000617", "C000618", "C000619"]),
    ("P000189", ["C000620", "C000621", "C000622"]),
]:
    add_decision("Person", pid, "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
    add_decision("Career", cids[0], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[1], "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
    add_decision("Career", cids[2], "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去クラブ在籍はissueに記録")

ISSUES = [
    {"issue_id": "B17W1I0001", "person_id": "P000186|P000187|P000188|P000189", "related_id": "C000611|C000614|C000617|C000620", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "4名とも土浦日本大学高等学校在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "各選手のB.LEAGUE公式プロフィールの学歴欄、または高校公式・大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B17W1I0002", "person_id": "P000186|P000187|P000188|P000189", "related_id": "C000612|C000615|C000618|C000621", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "4名とも大学在籍そのものは各選手のB.LEAGUE公式プロフィールで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B17W1I0003", "person_id": "P000186", "related_id": "P000186", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "松村竜吾は現所属（東京八王子ビートレインズ、2026-27〜、新規加入）以前に広島ドラゴンフライズ（2025-26、1シーズン）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B17W1I0004", "person_id": "P000187", "related_id": "P000187", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "落合知也は現所属（しながわシティバスケットボールクラブ、2024-25〜、新規加入）以前に越谷アルファーズ（2017-18〜2022-23、6シーズン）・栃木ブレックス（2016-17〜2017-18、2シーズン。宇都宮ブレックスの当時のクラブ名称であり、Governance方針により当時名称のまま記録している）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できる。また2022-23と2024-25の間の2023-24シーズンはクラブ所属履歴に記載がなく空白（本人の代表歴に3x3男子日本代表候補の記載があり、3x3活動に専念していた可能性があるが未確認）。今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブ・空白シーズンは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加、2023-24シーズンの活動内容を確認"},
    {"issue_id": "B17W1I0005", "person_id": "P000189", "related_id": "P000189", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "中野広大は現所属（ウォルガ湘南、2022-23〜、新規加入）以前に群馬クレインサンダーズ（2016-17〜2018-19）・岩手ビッグブルズ（2018-19〜2019-20）・さいたまブロンコス（2020-21〜2021-22）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
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
        f"Wrote batch_017/wave_01: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
