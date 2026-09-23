#!/usr/bin/env python3
"""Build Batch 006 Wave 4 (深掘りWave / Enrichment Wave) -- Round 2.

Targets: 井手優希 (P000075) and クベマ・ジョセフ・スティーブ (P000076),
both originally registered in batch_006/wave_01. Selected via Round 2 of
the systematic 過去在籍チーム深掘り rollout
(docs/HISTORICAL_CAREER_DEEPENING_LOG.md).

Per the established process rule, the origin wave's issues.csv was checked
BEFORE researching. wave_01 had already flagged (all HOLD/HOLD_CANDIDATE):
- B6W1I0003 (井手優希, PRO_HISTORY_GAPS): "横浜EX・岩手等の過去Careerは未作成"
- B6W1I0006 (クベマ, PRO_HISTORY_GAPS): "八王子以前の静岡・品川Careerは今回の最小経路に未収録"
- B6W1D0003 (井手優希, Career C000268 日本体育大学): HOLD_CANDIDATE, "B.LEAGUE出身校表示のみ"
- B6W1D0007 (クベマ, Career C000271 専修大学): HOLD_CANDIDATE, "B.LEAGUE出身校表示のみ"

This wave (a) fills the pre-current-club professional history gap for both
players with newly researched, independently-sourced Careers, and (b) adds
corroborating evidence for the two HOLD_CANDIDATE university Careers,
upgrading their organization_id decision to READY_FOR_VERIFIED_REVIEW while
leaving start/end HELD (period still unconfirmed). Neither player's
existing MASTER/CANDIDATE Career rows are modified.

Full researched career chains (this wave adds only the NEW rows):

井手優希 (P000075):
  福岡第一高校(C000267,READY) -> 日本体育大学(C000268,HOLD_CANDIDATE, existed)
  -> JR東日本秋田ペッカーズ 2019-2020 [NEW, C000384]
  -> 山口ペイトリオッツ(=山口パッツファイブ/ORG000100) 2021-2022 [NEW, C000385]
  -> アースフレンズ東京Z(ORG000046) 2022-2023 [NEW, C000386]
  -> 横浜エクセレンス(ORG000090) 2023-2024 [NEW, C000387]
  -> 岩手ビッグブルズ 2024-2025(契約満了2025-06-30) [NEW, C000388]
  -> 山口パッツファイブ(ORG000100) 2025- (C000269,READY, existed, unchanged)

  Note: 山口パッツファイブ(ORG000100) is the SAME legal entity as
  "山口ペイトリオッツ", renamed 2023-07-01 (Wikipedia). No new organization_id
  is issued for the 2021-22 stint; see issue B6W4I0002 on the schema gap
  (no separate historical-name field).

クベマ・ジョセフ・スティーブ (P000076):
  福岡第一高校(C000270,READY) -> 専修大学(C000271,HOLD_CANDIDATE, existed)
  -> しながわシティバスケットボールクラブ(品川) 2023-2024, 専修大学在学中の契約 [NEW, C000389]
  -> 東京八王子ビートレインズ(C000272,READY, existed, unchanged)

  ヴェルテックス静岡(静岡)については、2022年12月にトップチーム練習・試合帯同の
  発表を確認したが、正式契約・出場実績が確認できず在籍期間も不明のため、
  Careerとしては追加しない（issue B6W4I0006に記録のみ）。

See docs/HISTORICAL_CAREER_DEEPENING_LOG.md for the Round 2 selection
method (Master persons with only 2 registered Careers, re-examined against
their current-club status to separate "still in university" cases from
genuine pre-pro-career gaps).
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_006" / "wave_04"

PERSONS: list[dict] = []  # enrichment wave: no new persons

ORGANIZATIONS = [
    {"organization_id": "ORG000172", "name": "JR東日本秋田ペッカーズ"},
    {"organization_id": "ORG000173", "name": "岩手ビッグブルズ"},
    {"organization_id": "ORG000174", "name": "しながわシティバスケットボールクラブ"},
]

CAREERS = [
    {"career_id": "C000384", "person_id": "P000075", "organization_id": "ORG000172", "role": "Player", "start": "2019", "end": "2020"},
    {"career_id": "C000385", "person_id": "P000075", "organization_id": "ORG000100", "role": "Player", "start": "2021", "end": "2022"},
    {"career_id": "C000386", "person_id": "P000075", "organization_id": "ORG000046", "role": "Player", "start": "2022", "end": "2023"},
    {"career_id": "C000387", "person_id": "P000075", "organization_id": "ORG000090", "role": "Player", "start": "2023", "end": "2024"},
    {"career_id": "C000388", "person_id": "P000075", "organization_id": "ORG000173", "role": "Player", "start": "2024", "end": "2025"},
    {"career_id": "C000389", "person_id": "P000076", "organization_id": "ORG000174", "role": "Player", "start": "2023", "end": "2024"},
]

SOURCES = [
    {"source_id": "B6W4S0001", "title": "井手 優希", "publisher": "バスケットボールデータベース (jbaske.com)", "url": "https://jbaske.com/db/archives/12030", "accessed_at": "2026-09-23"},
    {"source_id": "B6W4S0002", "title": "井手 優希選手 契約(新規)基本合意のお知らせ", "publisher": "アースフレンズ東京Z", "url": "https://eftokyo-z.jp/news/220701-01", "accessed_at": "2026-09-23"},
    {"source_id": "B6W4S0003", "title": "井手優希選手、2023-24シーズン契約合意のお知らせ", "publisher": "横浜エクセレンス", "url": "https://yokohama-ex.jp/news/detail/id=21161", "accessed_at": "2026-09-23"},
    {"source_id": "B6W4S0004", "title": "【チーム情報】井手優希選手 契約合意のお知らせ", "publisher": "岩手ビッグブルズ", "url": "https://www.bigbulls.jp/news/detail/id=19016", "accessed_at": "2026-09-23"},
    {"source_id": "B6W4S0005", "title": "【チーム情報】井手優希選手 契約満了及び自由交渉選手リスト公示のお知らせ", "publisher": "岩手ビッグブルズ", "url": "https://www.bigbulls.jp/news/detail/id=19411", "accessed_at": "2026-09-23"},
    {"source_id": "B6W4S0006", "title": "井手優希選手 移籍先決定のお知らせ", "publisher": "横浜エクセレンス", "url": "https://yokohama-ex.jp/news/detail/id=21776", "accessed_at": "2026-09-23"},
    {"source_id": "B6W4S0007", "title": "山口パッツファイブ", "publisher": "Wikipedia日本語版", "url": "https://ja.wikipedia.org/wiki/山口パッツファイブ", "accessed_at": "2026-09-23"},
    {"source_id": "B6W4S0008", "title": "クベマ・ジョセフ・スティーブ選手 契約締結（新規）のお知らせ", "publisher": "しながわシティスポーツクラブ", "url": "https://www.shinagawa-city.com/basketball/5334", "accessed_at": "2026-09-23"},
    {"source_id": "B6W4S0009", "title": "専修大のスティーブがB3しながわに加入…福岡第一で全国制覇を経験した世代最強留学生選手", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/japan/univ/20240126/471741.html", "accessed_at": "2026-09-23"},
    {"source_id": "B6W4S0010", "title": "【第99回リーグ戦 注目選手】専修大学#13 クベマ", "publisher": "関東大学バスケットボール連盟 (KCBBF)", "url": "https://www.kcbbf.jp/column/detail/id/171", "accessed_at": "2026-09-23"},
    {"source_id": "B6W4S0011", "title": "クベマ・ジョセフ・スティーブ 選手契約締結（新規）のお知らせ", "publisher": "東京八王子ビートレインズ", "url": "https://trains.co.jp/news/detail/id=15658", "accessed_at": "2026-09-23"},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B6W4E{_evidence_seq:04d}",
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


# --- C000384: JR東日本秋田ペッカーズ 2019-2020 (single source) ---
add_evidence("Career", "C000384", "organization_id", "ORG000172", "B6W4S0001", "経歴一覧 > 2019-20年：JR東日本秋田ペッカーズ（地域リーグ）", "jbaske.comのプロフィールでJR東日本秋田ペッカーズ在籍を確認", "SUPPORTED")
add_evidence("Career", "C000384", "start", "2019", "B6W4S0001", "経歴一覧 > 2019-20年：JR東日本秋田ペッカーズ", "jbaske.comの年次表記に基づく。他媒体に記載なし", "PARTIAL", issue_note="jbaske.com単独の記載")
add_evidence("Career", "C000384", "end", "2020", "B6W4S0001", "経歴一覧 > 2019-20年：JR東日本秋田ペッカーズ", "jbaske.comの年次表記に基づく。他媒体に記載なし", "PARTIAL", issue_note="jbaske.com単独の記載")

# --- C000385: 山口ペイトリオッツ(=山口パッツファイブ/ORG000100) 2021-2022 ---
add_evidence("Career", "C000385", "organization_id", "ORG000100", "B6W4S0002", "本文 > 「山口ペイトリオッツからの移籍。2021-22シーズンはこのB3リーグチームに所属」", "アースフレンズ東京Z公式の加入発表で、直前所属が山口ペイトリオッツ（現・山口パッツファイブ、ORG000100）だったことを確認", "SUPPORTED")
add_evidence("Career", "C000385", "organization_id", "ORG000100", "B6W4S0001", "経歴一覧 > 2021-22年：山口ペイトリオッツ（B3、背番号64）", "jbaske.comでも同時期の山口ペイトリオッツ在籍を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000385", "start", "2021", "B6W4S0001", "経歴一覧 > 2021-22年：山口ペイトリオッツ", "jbaske.comの年次表記。アースフレンズ東京Z公式も「2021-22シーズン所属」と記載し一致", "SUPPORTED")
add_evidence("Career", "C000385", "end", "2022", "B6W4S0002", "本文 > 「2021-22シーズンはこのB3リーグチームに所属」その後2022-23はアースフレンズ東京Zへ", "アースフレンズ東京Z公式2022年7月1日付発表により、2022年に移籍したことを確認", "SUPPORTED")
add_evidence("Career", "C000385", "organization_id", "ORG000100", "B6W4S0007", "沿革節 > 「山口ペイトリオッツ（2020年～2023年）」「2023年7月1日に山口パッツファイブへ改称」", "Wikipediaにより、ORG000100（山口パッツファイブ）が2023年7月1日以前は「山口ペイトリオッツ」という名称だった同一組織であることを確認", "SUPPORTED")

# --- C000386: アースフレンズ東京Z(ORG000046) 2022-2023 ---
add_evidence("Career", "C000386", "organization_id", "ORG000046", "B6W4S0002", "本文 > 「井手優希選手が、B.LEAGUE 2022-23シーズン アースフレンズ東京Zに加入することが決まりました」", "アースフレンズ東京Z公式の2022年7月1日付加入発表", "SUPPORTED")
add_evidence("Career", "C000386", "organization_id", "ORG000046", "B6W4S0003", "本文 > 「昨季はB2で活躍」直前所属としてアースフレンズ東京Z（2022-23シーズン）", "横浜エクセレンス公式の加入発表で、直前所属がアースフレンズ東京Zだったことを確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000386", "start", "2022", "B6W4S0002", "本文 > 2022年7月1日付、2022-23シーズンからの加入発表", "契約発表日と対象シーズンから確認", "SUPPORTED")
add_evidence("Career", "C000386", "end", "2023", "B6W4S0003", "本文 > 直前所属「2022-23 アースフレンズ東京Z」", "横浜エクセレンス公式が2022-23シーズンを直前所属期間と明記", "SUPPORTED")

# --- C000387: 横浜エクセレンス(ORG000090) 2023-2024 ---
add_evidence("Career", "C000387", "organization_id", "ORG000090", "B6W4S0003", "本文 > 「横浜エクセレンスは井手優希選手と2023-24シーズンの契約合意に至りました」", "横浜エクセレンス公式の2023年11月22日付契約発表", "SUPPORTED")
add_evidence("Career", "C000387", "organization_id", "ORG000090", "B6W4S0004", "プロフィール経歴欄 > 「2023-24 横浜エクセレンス」", "岩手ビッグブルズ公式の加入発表内プロフィールで直前所属を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000387", "start", "2023", "B6W4S0003", "本文 > 2023年11月22日付、2023-24シーズン契約", "契約発表日と対象シーズンから確認", "SUPPORTED")
add_evidence("Career", "C000387", "end", "2024", "B6W4S0004", "プロフィール経歴欄 > 「2023-24 横浜エクセレンス」に続き「2024- 岩手ビッグブルズ」", "岩手ビッグブルズ公式のプロフィール欄で2023-24シーズン終了・2024年移籍を確認", "SUPPORTED")

# --- C000388: 岩手ビッグブルズ(ORG000173) 2024-2025 (契約満了2025-06-30) ---
add_evidence("Career", "C000388", "organization_id", "ORG000173", "B6W4S0004", "本文 > 「井手優希選手との2024-25シーズンの選手契約が合意に達した」", "岩手ビッグブルズ公式の2024年10月31日付契約発表", "SUPPORTED")
add_evidence("Career", "C000388", "organization_id", "ORG000173", "B6W4S0006", "本文 > 「井手優希選手が『岩手ビッグブルズ』（岩手県）への移籍が決定」", "横浜エクセレンス公式（移籍元）が同日発表した移籍先決定のお知らせで確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000388", "start", "2024", "B6W4S0004", "本文 > 2024年10月31日付契約発表、2024-25シーズン", "契約発表日と対象シーズンから確認", "SUPPORTED")
add_evidence("Career", "C000388", "end", "2025", "B6W4S0005", "本文 > 「岩手ビッグブルズでは、井手優希選手との契約が2025年6月30日をもちまして、満了となる」", "岩手ビッグブルズ公式の2025年5月22日付契約満了発表。終了日（2025-06-30）まで確認できる", "SUPPORTED")

# --- C000389: しながわシティバスケットボールクラブ(ORG000174) 2023-2024 (クベマ, 専修大学在学中) ---
add_evidence("Career", "C000389", "organization_id", "ORG000174", "B6W4S0008", "本文 > 「B3.LEAGUE 2023-24シーズンの契約を締結」専修大学4年生（在学中）", "しながわシティスポーツクラブ公式の2024年1月26日付契約発表。大学在学中のプロ契約であることを確認", "SUPPORTED")
add_evidence("Career", "C000389", "organization_id", "ORG000174", "B6W4S0009", "本文 > 「専修大のスティーブがB3しながわに加入」", "バスケットボールキング記事（同日）でも加入を確認（独立した第2ソース）", "SUPPORTED")
add_evidence("Career", "C000389", "start", "2023", "B6W4S0008", "本文 > 「2023-24シーズンの契約」", "しながわ公式が2023-24シーズン契約と明記。正式な発表日は2024年1月26日（シーズン途中）", "SUPPORTED", issue_note="契約発表は2024年1月26日でシーズン途中加入。厳密な加入月日は不明")
add_evidence("Career", "C000389", "end", "2024", "B6W4S0011", "本文 > 直前所属「2023-24.1 しながわシティバスケットボールクラブ」", "東京八王子ビートレインズ公式（2024年8月27日、2024-25シーズン契約発表）のプロフィール欄で、直前所属が2023-24シーズンのしながわだったことを確認", "SUPPORTED")

# --- 追加corroboration: C000268（井手優希, 日本体育大学）HOLD_CANDIDATE -> organization_idはREADYへ ---
add_evidence("Career", "C000268", "organization_id", "ORG000020", "B6W4S0001", "プロフィール > 出身大学：日本体育大学", "jbaske.comでも日本体育大学出身であることを確認。wave_01時点ではB.LEAGUE公式サイトの出身校表示のみだったが、独立した第2ソースが得られた", "SUPPORTED")

# --- 追加corroboration: C000271（クベマ, 専修大学）HOLD_CANDIDATE -> organization_idはREADYへ ---
add_evidence("Career", "C000271", "organization_id", "ORG000018", "B6W4S0010", "本文 > 「専修大学#13」「4年生としてチームを盛り上げたい」", "関東大学バスケットボール連盟(KCBBF)公式コラムで専修大学在籍（4年生）を確認", "SUPPORTED")
add_evidence("Career", "C000271", "organization_id", "ORG000018", "B6W4S0009", "見出し > 「専修大のスティーブがB3しながわに加入…福岡第一で全国制覇を経験した世代最強留学生選手」", "バスケットボールキング記事でも専修大学在籍を確認（独立した第3ソース）", "SUPPORTED")
add_evidence("Career", "C000271", "organization_id", "ORG000018", "B6W4S0011", "プロフィール > 出身校：専修大学（大学4年時にキャプテン）", "東京八王子ビートレインズ公式資料でも専修大学出身・キャプテン歴を確認（独立した第4ソース）", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B6W4D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": "2026-09-23",
    })


add_decision("Career", "C000384", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end",
             "jbaske.com単独の記載でJR東日本秋田ペッカーズ在籍を確認。在籍年次は同サイト単独のためissueに記録した上でREADYとする")
add_decision("Career", "C000385", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
             "アースフレンズ東京Z公式・jbaske.comの独立2ソースで山口ペイトリオッツ（現・山口パッツファイブ/ORG000100）在籍（2021-22）を確認")
add_decision("Career", "C000386", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
             "アースフレンズ東京Z公式（加入発表）・横浜エクセレンス公式（直前所属記載）の独立2ソースでアースフレンズ東京Z在籍（2022-23）を確認")
add_decision("Career", "C000387", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
             "横浜エクセレンス公式（加入発表）・岩手ビッグブルズ公式（直前所属記載）の独立2ソースで横浜エクセレンス在籍（2023-24）を確認")
add_decision("Career", "C000388", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
             "岩手ビッグブルズ公式（加入発表・契約満了発表）・横浜エクセレンス公式（移籍先決定発表）で岩手ビッグブルズ在籍（2024-25、契約満了日2025-06-30）を確認")
add_decision("Career", "C000389", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
             "しながわシティスポーツクラブ公式・バスケットボールキング・東京八王子ビートレインズ公式の複数ソースで、専修大学在学中のしながわ在籍（2023-24）を確認")
add_decision("Career", "C000268", "READY_FOR_VERIFIED_REVIEW", "organization_id", "start|end",
             "wave_01のHOLD_CANDIDATE（B6W1D0003, B.LEAGUE出身校表示のみ）を、jbaske.comという独立した第2ソースで裏付け、organization_idのみREADYへ更新。在籍期間は依然未確認のためHOLD継続")
add_decision("Career", "C000271", "READY_FOR_VERIFIED_REVIEW", "organization_id", "start|end",
             "wave_01のHOLD_CANDIDATE（B6W1D0007, B.LEAGUE出身校表示のみ）を、関東大学バスケットボール連盟・バスケットボールキング・東京八王子ビートレインズ公式という独立した複数ソースで裏付け、organization_idのみREADYへ更新。在籍期間は依然未確認のためHOLD継続")

# issues.csv follows batch_006's own established schema (person_id, related_id,
# issue_type, status, description, next_check).
ISSUES = [
    {"issue_id": "B6W4I0001", "person_id": "P000075", "related_id": "C000384", "issue_type": "SOURCE_TIER", "status": "HOLD",
     "description": "JR東日本秋田ペッカーズ在籍（2019-2020）はjbaske.com（非公式データベース）単独の記載であり、他媒体での裏付けが取れていない。",
     "next_check": "地域リーグ公式資料またはチーム公式発表での裏付けを確認"},
    {"issue_id": "B6W4I0002", "person_id": "P000075", "related_id": "C000385", "issue_type": "ORG_NAME_HISTORY", "status": "HOLD",
     "description": "本Careerの在籍当時（2021-22シーズン）、組織ORG000100は「山口ペイトリオッツ」と称していたが、2023年7月1日に「山口パッツファイブ」へ改称（Wikipedia出典）。同一組織のため新規組織IDは発行していないが、現行スキーマは組織名を1項目のみ保持し、当時の名称を別途記録する項目がない。",
     "next_check": "組織の名称履歴（改称前・改称後）を保持するスキーマ拡張を今後検討"},
    {"issue_id": "B6W4I0003", "person_id": "P000075", "related_id": "P000075", "issue_type": "PRO_HISTORY_GAPS", "status": "RESOLVED",
     "description": "wave_01で立てたissue B6W1I0003（最小経路として現在の山口を候補化し、横浜EX・岩手等の過去Careerは未作成）を、JR東日本秋田ペッカーズ（2019-2020）・山口ペイトリオッツ/山口パッツファイブ（2021-2022）・アースフレンズ東京Z（2022-2023）・横浜エクセレンス（2023-2024）・岩手ビッグブルズ（2024-2025）の5件追加により解消。",
     "next_check": ""},
    {"issue_id": "B6W4I0004", "person_id": "P000075", "related_id": "C000268", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "wave_01のissue B6W1I0002（日本体育大学はB.LEAGUE出身校表示のみで未確認）について、jbaske.comという独立した第2ソースで日本体育大学在籍そのものは確認できた。在籍期間（入学・卒業年月）は依然いずれの資料にも記載がなく未確認のまま。",
     "next_check": "大学・JUBF公式ロスターまたは卒業年度資料を確認"},
    {"issue_id": "B6W4I0005", "person_id": "P000076", "related_id": "C000389", "issue_type": "PRO_HISTORY_GAPS", "status": "RESOLVED",
     "description": "wave_01で立てたissue B6W1I0006（八王子以前の静岡・品川Careerは今回の最小経路に未収録）のうち、品川（しながわシティバスケットボールクラブ、2023-2024、専修大学在学中の契約）分を追加し解消。",
     "next_check": ""},
    {"issue_id": "B6W4I0006", "person_id": "P000076", "related_id": "P000076", "issue_type": "INSUFFICIENT_EVIDENCE", "status": "HOLD",
     "description": "wave_01のissue B6W1I0006のうち静岡（ヴェルテックス静岡）分について、2022年12月23日付でトップチーム練習・試合帯同の発表を確認したが、正式契約や試合出場の事実は記載されておらず、在籍期間（開始・終了）も不明。Careerとしては追加せず、情報のみ記録する。",
     "next_check": "公式資料での正式契約・出場実績の有無、および期間を確認"},
    {"issue_id": "B6W4I0007", "person_id": "P000076", "related_id": "C000271", "issue_type": "EDUCATION_PERIOD", "status": "HOLD",
     "description": "wave_01のissue B6W1I0005（高校・大学の開始年と終了年は未確認）のうち専修大学在籍について、関東大学バスケットボール連盟(KCBBF)・バスケットボールキング・東京八王子ビートレインズ公式という独立した複数ソースで在籍そのものは確認できた。在籍期間（入学・卒業年）は依然未確認のまま。",
     "next_check": "専修大学公式または全日本大学バスケットボール連盟の年度別ロスターで入学年を確認"},
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
    write_csv(BASE / "issues.csv", ISSUES, [
        "issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check",
    ])
    write_csv(BASE / "qa_decisions.csv", DECISIONS, [
        "decision_id", "entity_type", "entity_id", "decision",
        "eligible_fields", "held_fields", "reason", "reviewed_at",
    ])
    print(
        f"Wrote batch_006/wave_04: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
