#!/usr/bin/env python3
"""Build Batch 009 Wave 1 (明成高等学校/仙台大学附属明成高等学校, school 2/11) CANDIDATE data.

Second school of the powerhouse-school expansion initiative (see
docs/BATCH_008_PROPOSAL.md; the proposal doc predates the batch_009
numbering decision but its scope/methodology applies unchanged to every
school in the 11-school list). School renamed 明成高等学校 ->
仙台大学附属明成高等学校 in 2020-04 (confirmed via Wikipedia); the SAME
Organization ID (ORG000147, already registered under the old name via
batch_007/wave_05's 安藤誓哉) is reused rather than minting a new ID, per
the established organization-rename convention (cf. 山口ペイトリオッツ/
山口パッツファイブ in batch_006/wave_04). This is a schema gap for
post-rename alumni (see issue B9W1I0007).

Discovery: B.LEAGUE's TagID=35 tag list exists under THREE distinct
name-string variants for this school (a rename artifact, unlike 大濠's
single variant):
  - "明成高等学校(現・仙台大学附属明成高等学校)" -> 安藤誓哉(already
    registered, batch_007/wave_05), 納見悠仁, 白戸大聖
  - "仙台大学附属明成高等学校(旧・明成高等学校)" -> 石川海斗
  - "仙台大学附属明成高等学校" (plain) -> 菅野ブルース, 山内ジャヘル琉人
All three were checked. A specialized wiki (j-cbaske.com/baswiki/archives/
5883) was also cross-checked as a secondary discovery source and surfaced
一名 (八村阿蓮) who is a CURRENT B.LEAGUE player (神戸ストークス, confirmed
via 神戸ストークス公式 + バスケットボールキング) but is NOT tagged under
any of the three official TagID=35 variants above -- a real gap in the
tag-list-only discovery method, logged as issue B9W1I0008 for future
waves' awareness. The wiki's other listed alumni (宮本滉希、畠山俊樹、
村田翔、伊藤尚人、宮澤燿佑、伊藤駿 and others) were individually checked
via web search and confirmed NOT currently active in B.LEAGUE (retired or
moved to non-B.LEAGUE leagues), so they are excluded per the
現役B.LEAGUE選手のみ scope.

Persons (checked against Master + every candidate/verified person file
before writing -- none previously registered; 安藤誓哉 confirmed already
registered as P000098/batch_007/wave_05 with his full high-school ->
university -> current-club chain already complete, so he needs no new
work in this wave):
- 納見悠仁 (Yuto Nohmi, 島根スサノオマジック)
- 白戸大聖 (Taisei Shirato, 山形ワイヴァンズ)
- 菅野ブルース (Bruce Kanno, 千葉ジェッツ) -- own B.LEAGUE profile has no
  出身校 field at all; high school sourced from the TagID tag list only.
  University is ステッソン大学 (Stetson University, USA) -- a genuinely
  new, foreign Organization.
- 山内ジャヘル琉人 (Jaheru Ryuto Yamauchi, 川崎ブレイブサンダース) -- own
  profile has no 出身校 fields at all (both high school and university);
  high school sourced from the TagID tag list only, university left
  unrecorded (unknown -- not asserted as "no university").
- 石川海斗 (Kaito Ishikawa, 熊本ヴォルターズ) -- own B.LEAGUE profile has
  no 出身校 fields; high school sourced from the TagID tag list, and
  university (日本大学) sourced from the j-cbaske.com wiki only.
- 八村阿蓮 (Aren Hachimura, 神戸ストークス) -- discovered via the wiki,
  not the official tag list (see above); own profile independently
  confirms both high school and university directly.

Same deliberate scope as batch_008: minimum Career chain only (high
school -> university -> CURRENT club). Historical pro clubs before the
current one are deliberately excluded and logged as individual
PRO_HISTORY_GAPS issues.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jba_lib.csv_io import write_csv  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_009" / "wave_01"
CHECKED_AT = "2026-09-24"

PERSONS = [
    {"person_id": "P000128", "name": "納見 悠仁"},
    {"person_id": "P000129", "name": "白戸 大聖"},
    {"person_id": "P000130", "name": "菅野 ブルース"},
    {"person_id": "P000131", "name": "山内 ジャヘル琉人"},
    {"person_id": "P000132", "name": "石川 海斗"},
    {"person_id": "P000133", "name": "八村 阿蓮"},
]

# ORG000147 (明成高等学校 -- reused across the 2020 rename, see module
# docstring), ORG000030 (青山学院大学), ORG000155 (島根スサノオマジック),
# ORG000015 (東海大学), ORG000181 (山形ワイヴァンズ), ORG000118
# (千葉ジェッツ), ORG000122 (川崎ブレイブサンダース), ORG000121
# (日本大学), ORG000067 (熊本ヴォルターズ), ORG000043 (神戸ストークス)
# already exist and are reused -- checked against master + every
# candidate organization_candidates.csv before writing this file.
# ステッソン大学 confirmed genuinely new (a US university, not found
# anywhere in master or candidate data); current max existing
# Organization ID is ORG000183 (batch_008/wave_04), so this is ORG000184.
ORGANIZATIONS = [
    {"organization_id": "ORG000147", "name": "明成高等学校"},
    {"organization_id": "ORG000030", "name": "青山学院大学"},
    {"organization_id": "ORG000155", "name": "島根スサノオマジック"},
    {"organization_id": "ORG000015", "name": "東海大学"},
    {"organization_id": "ORG000181", "name": "山形ワイヴァンズ"},
    {"organization_id": "ORG000184", "name": "ステッソン大学"},
    {"organization_id": "ORG000118", "name": "千葉ジェッツ"},
    {"organization_id": "ORG000122", "name": "川崎ブレイブサンダース"},
    {"organization_id": "ORG000121", "name": "日本大学"},
    {"organization_id": "ORG000067", "name": "熊本ヴォルターズ"},
    {"organization_id": "ORG000043", "name": "神戸ストークス"},
]

CAREERS = [
    # 納見悠仁
    {"career_id": "C000440", "person_id": "P000128", "organization_id": "ORG000147", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000441", "person_id": "P000128", "organization_id": "ORG000030", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000442", "person_id": "P000128", "organization_id": "ORG000155", "role": "Player", "start": "2024", "end": ""},
    # 白戸大聖
    {"career_id": "C000443", "person_id": "P000129", "organization_id": "ORG000147", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000444", "person_id": "P000129", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000445", "person_id": "P000129", "organization_id": "ORG000181", "role": "Player", "start": "2023", "end": ""},
    # 菅野ブルース
    {"career_id": "C000446", "person_id": "P000130", "organization_id": "ORG000147", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000447", "person_id": "P000130", "organization_id": "ORG000184", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000448", "person_id": "P000130", "organization_id": "ORG000118", "role": "Player", "start": "2024", "end": ""},
    # 山内ジャヘル琉人（大学不明のため未登録）
    {"career_id": "C000449", "person_id": "P000131", "organization_id": "ORG000147", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000450", "person_id": "P000131", "organization_id": "ORG000122", "role": "Player", "start": "2024", "end": ""},
    # 石川海斗
    {"career_id": "C000451", "person_id": "P000132", "organization_id": "ORG000147", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000452", "person_id": "P000132", "organization_id": "ORG000121", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000453", "person_id": "P000132", "organization_id": "ORG000067", "role": "Player", "start": "2025", "end": ""},
    # 八村阿蓮
    {"career_id": "C000454", "person_id": "P000133", "organization_id": "ORG000147", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000455", "person_id": "P000133", "organization_id": "ORG000015", "role": "Player", "start": "", "end": ""},
    {"career_id": "C000456", "person_id": "P000133", "organization_id": "ORG000043", "role": "Player", "start": "2025", "end": ""},
]

SOURCES = [
    {"source_id": "B9W1S0001", "title": "納見悠仁 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=30399", "accessed_at": CHECKED_AT},
    {"source_id": "B9W1S0002", "title": "白戸大聖 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=15832", "accessed_at": CHECKED_AT},
    {"source_id": "B9W1S0003", "title": "菅野ブルース 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000431", "accessed_at": CHECKED_AT},
    {"source_id": "B9W1S0004", "title": "山内ジャヘル琉人 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=51000441", "accessed_at": CHECKED_AT},
    {"source_id": "B9W1S0005", "title": "石川海斗 選手プロフィール", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/roster_detail/?PlayerID=8722", "accessed_at": CHECKED_AT},
    {"source_id": "B9W1S0006", "title": "八村 阿蓮", "publisher": "神戸ストークス", "url": "https://www.storks.jp/player_lp/allen_hachimura/", "accessed_at": CHECKED_AT},
    {"source_id": "B9W1S0007", "title": "ワタシノB.LEAGUE選手一覧 | 明成高等学校(現・仙台大学附属明成高等学校)", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:明成高等学校(現・仙台大学附属明成高等学校)", "accessed_at": CHECKED_AT},
    {"source_id": "B9W1S0008", "title": "ワタシノB.LEAGUE選手一覧 | 仙台大学附属明成高等学校(旧・明成高等学校)", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:仙台大学附属明成高等学校(旧・明成高等学校)", "accessed_at": CHECKED_AT},
    {"source_id": "B9W1S0009", "title": "ワタシノB.LEAGUE選手一覧 | 仙台大学附属明成高等学校", "publisher": "B.LEAGUE", "url": "https://www.bleague.jp/mybleague_list/?TagID=35:仙台大学附属明成高等学校", "accessed_at": CHECKED_AT},
    {"source_id": "B9W1S0010", "title": "明成高校出身のバスケットボール選手", "publisher": "j-cbaske.com（バスケWiki）", "url": "https://j-cbaske.com/baswiki/archives/5883", "accessed_at": CHECKED_AT},
    {"source_id": "B9W1S0011", "title": "群馬を退団した八村阿蓮、新天地は神戸に決定「港町・神戸に似合う男がやって参りました！」", "publisher": "バスケットボールキング", "url": "https://basketballking.jp/news/japan/b1/20250528/545755.html", "accessed_at": CHECKED_AT},
]

EVIDENCE: list[dict] = []
_evidence_seq = 0


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id,
                  source_locator, evidence_summary, assessment, issue_note=""):
    global _evidence_seq
    _evidence_seq += 1
    EVIDENCE.append({
        "record_id": f"B9W1E{_evidence_seq:04d}",
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


# --- 納見悠仁 ---
add_evidence("Person", "P000128", "name", "納見 悠仁", "B9W1S0001", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000128", "birth_date", "1997-04-10", "B9W1S0001", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000440", "organization_id", "ORG000147", "B9W1S0001", "学歴 > 出身校（高）：明成高等学校(現・仙台大学附属明成高等学校)", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000440", "organization_id", "ORG000147", "B9W1S0007", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000441", "organization_id", "ORG000030", "B9W1S0001", "学歴 > 出身校（大）：青山学院大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000442", "organization_id", "ORG000155", "B9W1S0001", "クラブ経歴 > 「2024-25：島根」が初出（前年は川崎、その前は新潟・島根）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000442", "start", "2024", "B9W1S0001", "クラブ経歴 > 「2024-25：島根」が初出（今回の在籍）", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの現在の在籍開始を確認", "SUPPORTED",
             issue_note="2019-20シーズンにも一度島根に在籍しており、同一クラブへの復帰である点に留意")

# --- 白戸大聖 ---
add_evidence("Person", "P000129", "name", "白戸 大聖", "B9W1S0002", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000129", "birth_date", "1995-05-25", "B9W1S0002", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000443", "organization_id", "ORG000147", "B9W1S0002", "学歴 > 出身校（高）：明成高等学校（現・仙台大学附属明成高等学校）", "B.LEAGUE公式プロフィールで出身高校を確認", "SUPPORTED")
add_evidence("Career", "C000443", "organization_id", "ORG000147", "B9W1S0007", "TagID=35掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載（独立した第2の公式確認）", "SUPPORTED")
add_evidence("Career", "C000444", "organization_id", "ORG000015", "B9W1S0002", "学歴 > 出身校（大）：東海大学", "B.LEAGUE公式プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000445", "organization_id", "ORG000181", "B9W1S0002", "クラブ経歴 > 「2023-24：山形」が初出（前年は福岡）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000445", "start", "2023", "B9W1S0002", "クラブ経歴 > 「2023-24：山形」が初出", "B.LEAGUE公式のクラブ所属履歴で2023-24シーズンからの加入を確認", "SUPPORTED")

# --- 菅野ブルース ---
add_evidence("Person", "P000130", "name", "菅野 ブルース", "B9W1S0003", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000130", "birth_date", "2003-05-06", "B9W1S0003", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000446", "organization_id", "ORG000147", "B9W1S0009", "TagID=35（仙台大学附属明成高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED",
             issue_note="本人のB.LEAGUE公式プロフィールページには出身校（高）欄の記載がない。また2020年の校名改称後の在学と見られ、組織名は旧名（明成高等学校）で登録済みのため、ORG_NAME_HISTORY（issue B9W1I0007）を参照")
add_evidence("Career", "C000447", "organization_id", "ORG000184", "B9W1S0003", "学歴 > 出身校（大）：ステッソン大学", "B.LEAGUE公式プロフィールで出身大学（米国ステッソン大学）を確認", "SUPPORTED")
add_evidence("Career", "C000448", "organization_id", "ORG000118", "B9W1S0003", "クラブ経歴 > 「2024-25：千葉」が初出（唯一の記載）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000448", "start", "2024", "B9W1S0003", "クラブ経歴 > 「2024-25：千葉」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 山内ジャヘル琉人 ---
add_evidence("Person", "P000131", "name", "山内 ジャヘル琉人", "B9W1S0004", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000131", "birth_date", "2002-12-05", "B9W1S0004", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000449", "organization_id", "ORG000147", "B9W1S0009", "TagID=35（仙台大学附属明成高等学校）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED",
             issue_note="本人のB.LEAGUE公式プロフィールページには出身校（高・大とも）欄の記載がない。大学は確認できる情報がないため今回のWaveではCareerを登録していない。また2020年の校名改称後の在学と見られ、組織名は旧名（明成高等学校）で登録済みのため、ORG_NAME_HISTORY（issue B9W1I0007）を参照")
add_evidence("Career", "C000450", "organization_id", "ORG000122", "B9W1S0004", "クラブ経歴 > 「2024-25：川崎」が初出（唯一の記載）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000450", "start", "2024", "B9W1S0004", "クラブ経歴 > 「2024-25：川崎」が初出", "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの加入（B.LEAGUEデビュー）を確認", "SUPPORTED")

# --- 石川海斗 ---
add_evidence("Person", "P000132", "name", "石川 海斗", "B9W1S0005", "基本情報 > 選手名", "B.LEAGUE公式プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000132", "birth_date", "1990-11-30", "B9W1S0005", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000451", "organization_id", "ORG000147", "B9W1S0008", "TagID=35（仙台大学附属明成高等学校(旧・明成高等学校)）掲載選手一覧", "B.LEAGUE公式の出身校タグ一覧に掲載", "SUPPORTED",
             issue_note="本人のB.LEAGUE公式プロフィールページには出身校（高）欄の記載がない")
add_evidence("Career", "C000451", "organization_id", "ORG000147", "B9W1S0010", "選手一覧表 > 石川海斗", "j-cbaske.comのバスケWikiで明成高校出身であることを確認（独立した第2の確認）", "SUPPORTED")
add_evidence("Career", "C000452", "organization_id", "ORG000121", "B9W1S0010", "選手一覧表 > 石川海斗、出身大学：日本大学", "j-cbaske.comのバスケWikiで出身大学を確認", "SUPPORTED",
             issue_note="本人のB.LEAGUE公式プロフィールページには出身校（大）欄の記載がなく、Wikiのみのソース")
add_evidence("Career", "C000453", "organization_id", "ORG000067", "B9W1S0005", "クラブ経歴 > 「2025-26：熊本」が初出（今回の在籍。前年は信州）", "B.LEAGUE公式のクラブ所属履歴で現所属クラブを確認", "SUPPORTED")
add_evidence("Career", "C000453", "start", "2025", "B9W1S0005", "クラブ経歴 > 「2025-26：熊本」が初出（今回の在籍）", "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの現在の在籍開始を確認", "SUPPORTED",
             issue_note="2019-20〜2020-21シーズンにも一度熊本に在籍しており、同一クラブへの復帰である点に留意")

# --- 八村阿蓮 ---
add_evidence("Person", "P000133", "name", "八村 阿蓮", "B9W1S0006", "基本情報 > 選手名", "神戸ストークス公式サイトの選手プロフィールで氏名を確認", "SUPPORTED")
add_evidence("Person", "P000133", "birth_date", "1999-12-20", "B9W1S0006", "基本情報 > 生年月日", "神戸ストークス公式サイトの選手プロフィールで生年月日を確認", "SUPPORTED")
add_evidence("Career", "C000454", "organization_id", "ORG000147", "B9W1S0006", "学歴 > 出身高校：明成高等学校（現・仙台大学附属明成高等学校）", "神戸ストークス公式サイトの選手プロフィールで出身高校を確認", "SUPPORTED",
             issue_note="B.LEAGUE公式のTagID=35タグ一覧（3variantsとも）には本選手が掲載されておらず、タグ一覧のみに頼る発見手法の限界を示す事例（issue B9W1I0008参照）")
add_evidence("Career", "C000455", "organization_id", "ORG000015", "B9W1S0006", "学歴 > 出身大学：東海大学", "神戸ストークス公式サイトの選手プロフィールで出身大学を確認", "SUPPORTED")
add_evidence("Career", "C000456", "organization_id", "ORG000043", "B9W1S0011", "本文 > 「群馬を退団した八村阿蓮、新天地は神戸に決定」", "バスケットボールキング記事で神戸ストークスとの契約（2025年5月）を確認", "SUPPORTED")
add_evidence("Career", "C000456", "start", "2025", "B9W1S0011", "本文 > 2025年5月28日付記事", "記事日付で2025-26シーズンからの加入を確認", "SUPPORTED")


DECISIONS: list[dict] = []
_decision_seq = 0


def add_decision(entity_type, entity_id, decision, eligible_fields, held_fields, reason):
    global _decision_seq
    _decision_seq += 1
    DECISIONS.append({
        "decision_id": f"B9W1D{_decision_seq:04d}",
        "entity_type": entity_type,
        "entity_id": entity_id,
        "decision": decision,
        "eligible_fields": eligible_fields,
        "held_fields": held_fields,
        "reason": reason,
        "reviewed_at": CHECKED_AT,
    })


add_decision("Person", "P000128", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000440", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000441", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000442", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去にも同クラブに在籍していた点はissueに記録")

add_decision("Person", "P000129", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000443", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィール・出身校タグ一覧の独立2ソースで確認、在籍期間は未確認")
add_decision("Career", "C000444", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000445", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000130", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000446", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認（本人プロフィールページの出身校（高）欄は記載なし）、在籍期間は未確認")
add_decision("Career", "C000447", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE公式プロフィールで確認、在籍期間は未確認")
add_decision("Career", "C000448", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000131", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000449", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧で確認（本人プロフィールページの出身校欄は記載なし）、在籍期間は未確認")
add_decision("Career", "C000450", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定")

add_decision("Person", "P000132", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "B.LEAGUE公式プロフィールで確認")
add_decision("Career", "C000451", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "出身校タグ一覧・バスケWikiの独立2ソースで確認（本人プロフィールページの出身校欄は記載なし）、在籍期間は未確認")
add_decision("Career", "C000452", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "バスケWikiのみで確認（本人のB.LEAGUE公式プロフィールには出身校（大）欄なし）、在籍期間は未確認")
add_decision("Career", "C000453", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "B.LEAGUE公式プロフィールで確認、現在進行中の契約のため終了日は未定。過去にも同クラブに在籍していた点はissueに記録")

add_decision("Person", "P000133", "READY_FOR_VERIFIED_REVIEW", "name|birth_date", "", "神戸ストークス公式サイトの選手プロフィールで確認")
add_decision("Career", "C000454", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "神戸ストークス公式サイトで確認、在籍期間は未確認")
add_decision("Career", "C000455", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "神戸ストークス公式サイトで確認、在籍期間は未確認")
add_decision("Career", "C000456", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "バスケットボールキング記事で確認、現在進行中の契約のため終了日は未定")

ISSUES = [
    {"issue_id": "B9W1I0001", "person_id": "P000128|P000129|P000130|P000131|P000132|P000133", "related_id": "C000440|C000443|C000446|C000449|C000451|C000454", "issue_type": "HIGH_SCHOOL_PERIOD", "status": "HOLD",
     "description": "6名とも明成高等学校（現・仙台大学附属明成高等学校）在籍そのものは複数ソースで確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "高校公式または大会公式ロスターでの裏付けを確認"},
    {"issue_id": "B9W1I0002", "person_id": "P000128|P000129|P000130|P000132|P000133", "related_id": "C000441|C000444|C000447|C000452|C000455", "issue_type": "UNIVERSITY_PERIOD", "status": "HOLD",
     "description": "5名（山内ジャヘル琉人を除く、大学情報が未確認）とも大学在籍そのものは確認できたが、入学・卒業年月はいずれの資料にも記載がなく未確認。",
     "next_check": "全日本大学バスケットボール連盟（JUBF）の年度別ロスターでの裏付けを確認"},
    {"issue_id": "B9W1I0003", "person_id": "P000128", "related_id": "P000128", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "納見悠仁は現所属（島根スサノオマジック、2024-25〜、2回目の在籍）以前に新潟アルビレックスBB（ORG000052、2020-21〜2021-22）、川崎ブレイブサンダース（ORG000122、2022-23〜2023-24）、および1回目の島根在籍（2019-20）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B9W1I0004", "person_id": "P000129", "related_id": "P000129", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "白戸大聖は現所属（山形ワイヴァンズ、2023-24〜）以前にライジングゼファー福岡（ORG000040、2020-21〜2022-23）、仙台89ERS（ORG000132、2017-18〜2019-20）でのプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加"},
    {"issue_id": "B9W1I0005", "person_id": "P000132", "related_id": "P000132", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "石川海斗は現所属（熊本ヴォルターズ、2025-26〜、2回目の在籍）以前に仙台89ERS（ORG000132、2016-17〜2017-18）、信州ブレイブウォリアーズ（ORG000150、2018-19、2023-24〜2024-25）、1回目の熊本在籍（2019-20〜2020-21）、ファイティングイーグルス名古屋（ORG000180、2021-22〜2022-23）と複数回の移籍を伴う長いプロ経歴がB.LEAGUE公式のクラブ所属履歴で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加（クラブ数が多く優先度を検討）"},
    {"issue_id": "B9W1I0006", "person_id": "P000133", "related_id": "P000133", "issue_type": "PRO_HISTORY_GAPS", "status": "HOLD",
     "description": "八村阿蓮は現所属（神戸ストークス、2025-26〜）以前にサンロッカーズ渋谷（2020-21）、群馬クレインサンダーズ（ORG000143、2021-22〜2024-25）でのプロ経歴が神戸ストークス公式・バスケットボールキング記事で確認できるが、今回のWaveでは現所属クラブのみを最小経路として登録し、過去クラブは対象外とした。サンロッカーズ渋谷のOrganization IDは今回未確認のため付記していない。",
     "next_check": "後続の深掘りWaveでクラブ別Careerを追加（サンロッカーズ渋谷のOrganization ID確認を含む）"},
    {"issue_id": "B9W1I0007", "person_id": "P000130|P000131", "related_id": "C000446|C000449", "issue_type": "ORG_NAME_HISTORY", "status": "HOLD",
     "description": "明成高等学校は2020年4月に仙台大学附属明成高等学校へ改称した（Wikipediaで確認）。菅野ブルース・山内ジャヘル琉人は生年月日から判断して改称後の在学とみられ、B.LEAGUE公式のタグ一覧でも改称後の名称タグ「仙台大学附属明成高等学校」（旧名称の注記なし）に掲載されているが、当該Organization（ORG000147）は先に登録された安藤誓哉（改称前の卒業生）の在籍時の名称「明成高等学校」で登録済みであり、単一名称のスキーマでは改称後在籍者の実際の呼称を表現できない。既存レコードの名称を無断で変更しない方針（山口ペイトリオッツ/山口パッツファイブと同種の事例）に従い、名称は変更せず本issueに記録するのみとした。",
     "next_check": "Organization名称の時系列表現（改称履歴）のスキーマ整備を検討"},
    {"issue_id": "B9W1I0008", "person_id": "P000133", "related_id": "P000133", "issue_type": "DISCOVERY_METHOD_GAP", "status": "HOLD",
     "description": "八村阿蓮は現役B.LEAGUE選手（神戸ストークス）だが、B.LEAGUE公式のTagID=35タグ一覧の3種類の名称バリアント（明成高等学校(現・仙台大学附属明成高等学校)／仙台大学附属明成高等学校(旧・明成高等学校)／仙台大学附属明成高等学校）のいずれにも掲載されていなかった。j-cbaske.comの専門Wikiとのクロスチェックで発見した。タグ一覧のみに頼る発見手法には見落としのリスクがあることが判明した。",
     "next_check": "後続の学校（3〜11校目）の調査では、B.LEAGUE公式タグ一覧に加えて専門Wiki等の補助ソースでのクロスチェックを標準手順とすることを検討"},
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
        f"Wrote batch_009/wave_01: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(CAREERS)} careers, "
        f"{len(SOURCES)} sources, {len(EVIDENCE)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues"
    )


if __name__ == "__main__":
    main()
