#!/usr/bin/env python3
"""Build Batch 007 Wave 4 (深掘りWave/Enrichment Wave) candidate data.

Wave 4 does not add new persons. It adds:
  - New evidence for previously HELD fields on existing Wave 1-3 Career records
  - Two newly-discovered intermediate Career records for 富樫勇樹 (Career history gap)
  - New qa_decisions rows (append-only; original wave decisions are left untouched)
  - New issues for unresolved conflicts / open club-history gaps for future waves
"""
from __future__ import annotations

from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "candidate" / "batch_007" / "wave_04"
BASE.mkdir(parents=True, exist_ok=True)

# ---- New organizations (only for the newly-discovered 富樫勇樹 intermediate clubs) ----
ORGANIZATIONS = [
    {"organization_id": "ORG000137", "name": "秋田ノーザンハピネッツ"},
    {"organization_id": "ORG000138", "name": "テキサス・レジェンズ"},
]

# ---- New career records (intermediate clubs discovered for 富樫勇樹, P000083) ----
CAREERS = [
    {"career_id": "C000325", "person_id": "P000083", "organization_id": "ORG000137", "role": "Player", "start": "2012", "end": "2014"},
    {"career_id": "C000326", "person_id": "P000083", "organization_id": "ORG000138", "role": "Player", "start": "2014", "end": "2015"},
]

# ---- New sources ----
SOURCES = [
    {"source_id": "B7S0026", "title": "富樫勇樹 - Wikipedia", "publisher": "Wikipedia", "url": "https://ja.wikipedia.org/wiki/富樫勇樹", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0027", "title": "富樫 勇樹｜指揮官の信頼も厚い男子日本代表キャプテン", "publisher": "日本バスケットボール協会(JBA)", "url": "https://okinawa-basketball.japanbasketball.jp/column/2023/08/785", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0028", "title": "齋藤拓実 - Wikipedia", "publisher": "Wikipedia", "url": "https://ja.wikipedia.org/wiki/齋藤拓実", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0029", "title": "（２）バスケットボール部 齋藤拓実", "publisher": "明大スポーツ新聞部", "url": "https://meisupo.net/news/8783/", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0030", "title": "篠山竜青 - Wikipedia", "publisher": "Wikipedia", "url": "https://ja.wikipedia.org/wiki/篠山竜青", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0031", "title": "西田優大 - Wikipedia", "publisher": "Wikipedia", "url": "https://ja.wikipedia.org/wiki/西田優大", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0032", "title": "田中大貴 (バスケットボール) - Wikipedia", "publisher": "Wikipedia", "url": "https://ja.wikipedia.org/wiki/田中大貴_(バスケットボール)", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0033", "title": "片岡大晴 - Wikipedia", "publisher": "Wikipedia", "url": "https://ja.wikipedia.org/wiki/片岡大晴", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0034", "title": "松脇圭志 - Wikipedia", "publisher": "Wikipedia", "url": "https://ja.wikipedia.org/wiki/松脇圭志", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0035", "title": "【連載】早大『令和5年度卒業記念特集』星川堅信", "publisher": "Yahoo!スポーツ（スポーツナビ）", "url": "https://sports.yahoo.co.jp/official/detail/2024022900045-spnaviow", "accessed_at": "2026-09-23"},
    {"source_id": "B7S0036", "title": "オータムリーグ出場選手インタビュー：星川堅信（早稲田大学3年）", "publisher": "J SPORTS", "url": "https://news.jsports.co.jp/basketball/article/20190310223849/", "accessed_at": "2026-09-23"},
]

# ---- Evidence records ----
EVIDENCE = []
_e = 99  # last used B7E id was B7E0099


def add_evidence(entity_type, entity_id, field_name, candidate_value, source_id, locator, summary, assessment, issue_note=""):
    global _e
    _e += 1
    EVIDENCE.append({
        "record_id": f"B7E{_e:04d}", "entity_type": entity_type, "entity_id": entity_id,
        "field_name": field_name, "candidate_value": candidate_value, "source_id": source_id,
        "source_locator": locator, "evidence_summary": summary, "assessment": assessment,
        "checked_at": "2026-09-23", "issue_note": issue_note,
    })


# 富樫勇樹 / モントロス・クリスチャン高校 (C000299) — organization_id 保留解除
add_evidence("Career", "C000299", "organization_id", "ORG000117", "B7S0026", "本文 > モントローズ・クリスチャン高校に進学",
             "Wikipediaによる独立した出身校記述。開志国際高等学校への言及なし", "SUPPORTED",
             "開志国際高等学校との関係は本ソースでも確認できず。単独情報の懸念は解消と判断")
add_evidence("Career", "C000299", "organization_id", "ORG000117", "B7S0027", "本文 > 渡米しワシントンDC郊外にあるモントロス・クリスチャン高校へ進学した",
             "JBA公式コラムによる独立した出身校記述。開志国際高等学校への言及なし", "SUPPORTED",
             "公式団体(JBA)記事のため信頼性が高い")

# 富樫勇樹 / 千葉ジェッツ (C000300) — start追加
add_evidence("Career", "C000300", "start", "2015", "B7S0026", "本文 > 9月28日にNBLの千葉ジェッツとの契約合意が発表",
             "Wikipediaにより2015年9月の千葉ジェッツ加入を確認", "SUPPORTED")

# 富樫勇樹 / 秋田ノーザンハピネッツ (C000325 新規)
add_evidence("Career", "C000325", "organization_id", "ORG000137", "B7S0026", "本文 > アーリーエントリー制度を用いて秋田ノーザンハピネッツに入団",
             "Wikipediaにより2012年12月〜2014年6月の秋田ノーザンハピネッツ在籍を確認", "SUPPORTED")
add_evidence("Career", "C000325", "start", "2012", "B7S0026", "本文 > 秋田ノーザンハピネッツ（2012年12月〜2014年6月）", "同上", "SUPPORTED")
add_evidence("Career", "C000325", "end", "2014", "B7S0026", "本文 > 秋田ノーザンハピネッツ（2012年12月〜2014年6月）", "同上", "SUPPORTED")

# 富樫勇樹 / テキサス・レジェンズ (C000326 新規)
add_evidence("Career", "C000326", "organization_id", "ORG000138", "B7S0026", "本文 > テキサス・レジェンズ（NBA傘下Dリーグ、2014年11月〜2015年2月）",
             "Wikipediaにより2014年11月〜2015年2月の在籍を確認（NBA下部組織Dリーグ）", "SUPPORTED")
add_evidence("Career", "C000326", "start", "2014", "B7S0026", "本文 > 2014年秋に契約し、11月17日に到着", "同上", "SUPPORTED")
add_evidence("Career", "C000326", "end", "2015", "B7S0026", "本文 > 2月の足首捻挫後は回復が思わしくなかった", "同上", "SUPPORTED")

# 齋藤拓実 / 桐光学園高校 (C000293)
add_evidence("Career", "C000293", "organization_id", "ORG000123", "B7S0005", "出身校欄 > 桐光学園高等学校",
             "B.LEAGUE公式選手プロフィールの出身校欄（既存ソース、高校org確認への引用漏れを補足）", "SUPPORTED")
add_evidence("Career", "C000293", "organization_id", "ORG000123", "B7S0028", "本文 > 桐光学園に進学",
             "Wikipediaによる独立した出身校記述", "SUPPORTED")
add_evidence("Career", "C000293", "end", "2014", "B7S0029", "本文 > 2014年5月時点で1年生（営１）と明記",
             "明大スポーツ新聞部記事で2014年度大学入学を直接確認。高校卒業(end)は同年3月と論理的に導出", "PARTIAL",
             "高校卒業年そのものを明記した資料ではなく、大学入学年からの論理的導出")

# 齋藤拓実 / 明治大学 (C000294)
add_evidence("Career", "C000294", "start", "2014", "B7S0029", "本文 > 2014年5月時点で1年生（営１）と明記",
             "明大スポーツ新聞部記事により2014年度入学を直接確認", "SUPPORTED")
add_evidence("Career", "C000294", "end", "", "B7S0005", "経歴概要 > 明治大学を経て2017年にアルバルク東京でプロバスケットボール人生をスタート",
             "B.LEAGUE公式プロフィールは2017年プロ入りと記載。標準4年在籍なら2018年3月卒業となり矛盾するためendは保留継続。矛盾点はissueに記録",
             "PARTIAL", "2014年度入学(直接確認)と2017年プロ入り(公式)が標準4年制と整合しない。卒業年は未確定のため保留継続")

# 篠山竜青 / 北陸高等学校 (C000296) — org二次ソース補強、end引き続き保留
add_evidence("Career", "C000296", "organization_id", "ORG000120", "B7S0030", "本文 > 出身高校：北陸高等学校",
             "Wikipediaによる独立した出身校記述（専門媒体単独という既存の懸念を解消）", "SUPPORTED")

# 篠山竜青 / 日本大学 (C000297)
add_evidence("Career", "C000297", "end", "2011", "B7S0030", "本文 > 大学卒業後の2011年より東芝ブレイブサンダースに加入",
             "Wikipediaにより卒業年を直接確認", "SUPPORTED")

# 田中大貴 / 長崎西高等学校 (C000301)
add_evidence("Career", "C000301", "start", "2007", "B7S0032", "本文 > 2007年4月、長崎西高校に進学", "Wikipediaによる入学年の直接記述", "SUPPORTED")
add_evidence("Career", "C000301", "end", "2010", "B7S0032", "本文 > 2010年4月、東海大学に進学",
             "大学入学年の直接記述から高校卒業年（同年3月）を導出", "PARTIAL")

# 田中大貴 / 東海大学 (C000302)
add_evidence("Career", "C000302", "start", "2010", "B7S0032", "本文 > 2010年4月、東海大学に進学", "Wikipediaによる入学年の直接記述", "SUPPORTED")
add_evidence("Career", "C000302", "end", "2014", "B7S0032", "本文 > 4年生時は主将としてチームを牽引",
             "4年次在籍の直接記述から標準4年制で卒業年を導出", "PARTIAL")

# 西田優大 / 東海大学 (C000308)
add_evidence("Career", "C000308", "start", "2017", "B7S0031", "本文 > 3年次が2019年12月", "3年次の時期記述から入学年を逆算", "PARTIAL")
add_evidence("Career", "C000308", "end", "2021", "B7S0031", "本文 > 4年次が2020年12月", "4年次の時期記述から標準4年制で卒業年を導出", "PARTIAL")

# 金丸晃輔 / 福岡大学附属大濠高等学校 (C000310)
add_evidence("Career", "C000310", "organization_id", "ORG000127", "B7S0018", "出身校欄 > 福岡大学附属大濠高等学校",
             "B.LEAGUE公式選手プロフィールの出身校欄（既存ソース、高校org確認への引用漏れを補足）", "SUPPORTED")

# 金丸晃輔 / 明治大学 (C000311)
add_evidence("Career", "C000311", "end", "2011", "B7S0020", "本文 > 金丸 晃輔さん〈2011年政治経済学部卒〉",
             "Meiji NOW（明治大学公式インタビューサイト）による卒業年の直接記述", "SUPPORTED")

# 松脇圭志 / 日本大学 (C000320)
add_evidence("Career", "C000320", "end", "2020", "B7S0034", "本文 > 4年次の2020年1月に富山グラウジーズへ特別指定選手として入団",
             "Wikipediaにより4年次在籍時期を直接確認し卒業年を導出", "PARTIAL")

EVIDENCE_ROWS = list(EVIDENCE)

# ---- QA decisions (append-only; new reviewed_at, do not touch original wave decision rows) ----
_d = 47
DECISIONS = []


def add_decision(entity_type, entity_id, decision, eligible, held, reason):
    global _d
    _d += 1
    DECISIONS.append({
        "decision_id": f"B7D{_d:04d}", "entity_type": entity_type, "entity_id": entity_id,
        "decision": decision, "eligible_fields": eligible, "held_fields": held,
        "reason": reason, "reviewed_at": "2026-09-23",
    })


add_decision("Career", "C000299", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "",
              "Wikipedia及びJBA公式コラムの独立した2ソースでモントロス・クリスチャン高校在籍を確認。開志国際高等学校との関係はいずれの資料にも記載なく保留解除")
add_decision("Career", "C000300", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "",
              "Wikipediaにより2015年9月の千葉ジェッツ加入(start)を確認")
add_decision("Career", "C000325", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
              "新規発見：Wikipediaにより2012年12月〜2014年6月の秋田ノーザンハピネッツ在籍を確認。CLUB_HISTORY_SCOPE(B7I0013)の一部を充足")
add_decision("Career", "C000326", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
              "新規発見：Wikipediaにより2014年11月〜2015年2月のテキサス・レジェンズ(Dリーグ)在籍を確認。CLUB_HISTORY_SCOPE(B7I0013)の一部を充足")
add_decision("Career", "C000293", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|end", "start",
              "bleague.jp公式プロフィール(既存B7S0005)とWikipediaで桐光学園高校在籍を独立確認。大学入学(2014)確定より卒業(end)を2014年3月と導出。startは生年月日推定のみで保留継続")
add_decision("Career", "C000294", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end",
              "明大スポーツ新聞部記事で2014年度入学(start)を直接確認。卒業年(end)は2017年プロ入り記載と標準4年制が整合しないため保留継続（B7I0014参照）")
add_decision("Career", "C000296", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end",
              "Wikipediaにより北陸高等学校を独立ソースで再確認（専門媒体単独の懸念を解消）。卒業年(end)は直接資料なく保留継続")
add_decision("Career", "C000297", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|end", "start",
              "Wikipediaに卒業後2011年に東芝ブレイブサンダース加入と明記されており卒業年(end)を確認。入学年(start)は生年月日推定のみで保留継続")
add_decision("Career", "C000301", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
              "Wikipediaに入学(2007年4月)・卒業に相当する大学進学(2010年4月)が明記されており両方を確認")
add_decision("Career", "C000302", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
              "Wikipediaに入学(2010年4月)が明記され、4年次主将の記述から卒業(2014年3月)を導出")
add_decision("Career", "C000308", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "",
              "Wikipediaの「3年次2019年12月・4年次2020年12月」の記述から入学(2017)・卒業(2021)を導出")
add_decision("Career", "C000310", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end",
              "bleague.jp公式選手プロフィール(既存B7S0018)により大濠高校在籍を独立確認。在籍期間は直接資料なく保留継続")
add_decision("Career", "C000311", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|end", "start",
              "Meiji NOW（明治大学公式、既存B7S0020）に卒業年(2011)の明記あり確認。入学年は生年月日推定のみで保留継続")
add_decision("Career", "C000320", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|end", "start",
              "日本大学公式スポーツニュース等を踏まえたWikipedia記述で4年次(2019年度)在籍を確認し卒業(2020年3月)を導出。入学年は生年月日推定のみで保留継続")

# ---- Issues (append-only across the batch) ----
ISSUES = [
    {"issue_id": "B7I0014", "category": "DATE_CONFLICT", "scope": "P000086",
     "description": "齋藤拓実：明治大学の入学年は2014年度（明大スポーツ新聞部記事で直接確認）だが、B.LEAGUE公式プロフィールは2017年にアルバルク東京でプロキャリア開始と記載。標準的な4年在籍なら卒業は2018年3月となり整合しない。卒業年(end)の確定にはYuichiによる追加判断または追加資料が必要。"},
    {"issue_id": "B7I0015", "category": "DATE_CONFLICT", "scope": "P000094",
     "description": "星川堅信：J SPORTSの2019年3月記事では「早稲田大学3年」と記載（2016年度入学を示唆）だが、Yahoo!スポーツの2024年2月記事は「令和5年度（2023年度）卒業記念特集」「スポ４」と記載（2020年度入学・2024年3月卒業を示唆）。入学年に食い違いがあり、Yuichiによる追加判断または追加資料が必要。"},
    {"issue_id": "B7I0016", "category": "CLUB_HISTORY_SCOPE", "scope": "P000086",
     "description": "齋藤拓実：B.LEAGUE公式選手プロフィール(既存B7S0005)の経歴概要に「2017年にアルバルク東京でプロスタート、2019年に滋賀へ移籍、2020年から名古屋ダイヤモンドドルフィンズ」との記述があり、現所属(名古屋)以前にアルバルク東京・滋賀（当時のクラブ名称の確認要）の在籍歴が欠落している。正確な移籍月と当時の正式チーム名を確認の上、次回深掘りWaveで新規Career候補として追加予定。"},
    {"issue_id": "B7I0017", "category": "CLUB_HISTORY_SCOPE", "scope": "P000093",
     "description": "松脇圭志：検索結果に「富山グラウジーズに特別指定選手として入団」「三遠ネオフェニックス選手契約(新規)」の記事タイトルが見られ、現所属(琉球ゴールデンキングス)以前に複数クラブでの在籍歴が示唆される。詳細な時期確認が次回深掘りWaveの課題。"},
    {"issue_id": "B7I0018", "category": "CLUB_HISTORY_SCOPE", "scope": "P000094",
     "description": "星川堅信：検索結果に「宇都宮ブレックス特別指定選手 活動終了」「越谷アルファーズでのプロデビュー（2024年1月）」の記述が見られ、現所属(長崎ヴェルカ)以前に複数クラブでの在籍歴が示唆される。詳細な時期確認が次回深掘りWaveの課題。"},
    {"issue_id": "B7I0019", "category": "CLUB_HISTORY_SCOPE", "scope": "P000088",
     "description": "岸本隆一：検索結果に「岸本隆一（琉球ゴールデンキングス）」と紹介する記事タイトルが見られ、現所属(京都ハンナリーズ)以前または関連して琉球ゴールデンキングスでの在籍歴が示唆される。詳細な時期確認が次回深掘りWaveの課題。"},
    {"issue_id": "B7I0020", "category": "CLUB_HISTORY_SCOPE", "scope": "P000087",
     "description": "田中大貴：検索結果に「#24 田中大貴選手 契約満了および移籍先決定のご報告｜アルバルク東京」の記事タイトルが見られ、現所属(東京サンロッカーズ)以前にアルバルク東京での在籍歴が示唆される。詳細な時期確認が次回深掘りWaveの課題。"},
]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


write_csv(BASE / "person_candidates.csv", ["person_id", "name"], [])
write_csv(BASE / "organization_candidates.csv", ["organization_id", "name"], ORGANIZATIONS)
write_csv(BASE / "career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], CAREERS)
write_csv(BASE / "source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], SOURCES)
write_csv(BASE / "evidence_records.csv",
          ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id",
           "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], EVIDENCE_ROWS)
write_csv(BASE / "issues.csv", ["issue_id", "category", "scope", "description"], ISSUES)
write_csv(BASE / "qa_decisions.csv",
          ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"],
          DECISIONS)

print(f"Wrote wave_04: {len(ORGANIZATIONS)} orgs, {len(CAREERS)} new careers, {len(SOURCES)} sources, "
      f"{len(EVIDENCE_ROWS)} evidence, {len(DECISIONS)} decisions, {len(ISSUES)} issues")
