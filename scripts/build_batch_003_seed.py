#!/usr/bin/env python3
"""Build Batch 003 candidate data from checked official sources.

The output remains CANDIDATE. It does not create VERIFIED or MASTER data.
"""

from __future__ import annotations

import csv
from pathlib import Path


OUTPUT_DIR = Path("data/candidate/batch_003")
CHECKED_AT = "2026-09-20"

PEOPLE = [
    ("P000028", "佐藤 涼成"),
    ("P000029", "早田 流星"),
    ("P000030", "鷹野 祐磨"),
    ("P000031", "星賀 舞也"),
    ("P000032", "岡本 汰稀"),
    ("P000033", "岩下 周介"),
    ("P000034", "カマレ ムレマ フランシス"),
    ("P000010", "當山 修梧"),
    ("P000014", "キエキエ トピー アリ"),
    ("P000016", "本松 龍斗"),
]

ORGANIZATIONS = [
    ("ORG000010", "福岡第一高等学校"),
    ("ORG000093", "白鷗大学"),
    ("ORG000020", "日本体育大学"),
    ("ORG000030", "青山学院大学"),
    ("ORG000094", "九州国際大学"),
    ("ORG000095", "東海大学九州"),
    ("ORG000096", "山梨学院大学"),
    ("ORG000018", "専修大学"),
    ("ORG000017", "日本経済大学"),
]

CAREERS = [
    ("C000046", "P000028", "ORG000010", "Player", "", ""),
    ("C000213", "P000028", "ORG000093", "Player", "", ""),
    ("C000047", "P000029", "ORG000010", "Player", "", ""),
    ("C000214", "P000029", "ORG000020", "Player", "", ""),
    ("C000048", "P000030", "ORG000010", "Player", "", ""),
    ("C000049", "P000031", "ORG000010", "Player", "", ""),
    ("C000215", "P000031", "ORG000030", "Player", "", ""),
    ("C000050", "P000032", "ORG000010", "Player", "", ""),
    ("C000216", "P000032", "ORG000094", "Player", "", ""),
    ("C000051", "P000033", "ORG000010", "Player", "", ""),
    ("C000217", "P000033", "ORG000095", "Player", "", ""),
    ("C000052", "P000034", "ORG000010", "Player", "", ""),
    ("C000218", "P000034", "ORG000096", "Player", "", ""),
    ("C000010", "P000010", "ORG000010", "Player", "", ""),
    ("C000031", "P000010", "ORG000018", "Player", "", ""),
    ("C000014", "P000014", "ORG000010", "Player", "", ""),
    ("C000030", "P000014", "ORG000017", "Player", "", ""),
    ("C000033", "P000016", "ORG000020", "Student Coach", "", ""),
]

SOURCES = [
    ("B3S0001", "ウインターカップ2021 福岡第一対帝京長岡 ボックススコア", "日本バスケットボール協会", "https://wintercup2021.japanbasketball.jp/boxscore/?period=18&schedulekey=7425"),
    ("B3S0002", "第96回天皇杯 福岡第一高校ロスター", "日本バスケットボール協会", "https://zennihon2020-21.japanbasketball.jp/team/1st/men-fukuoka"),
    ("B3S0003", "2019年度男子U16日本代表 第1次強化合宿メンバー", "日本バスケットボール協会", "https://iwate.japanbasketball.jp/manage/wp-content/uploads/2019/04/42d4fca113768eb1273ef8bdba5e06eb.pdf"),
    ("B3S0004", "2024年度第47回李相佰盃 日本代表メンバー", "全日本大学バスケットボール連盟", "https://jubf.jp/index/show-pdf/url/aHR0cHM6Ly9kMmEwdjF4N3F2eGw2Yy5jbG91ZGZyb250Lm5ldC9maWxlcy9zcG9ocF9qdWJmL25ld3MvNjYwMjliODAwOTQ1ZC5wZGY="),
    ("B3S0005", "佐藤涼成選手 特別指定選手登録のお知らせ", "横浜ビー・コルセアーズ", "https://b-corsairs.com/news/team_20241221_1/"),
    ("B3S0006", "第101回天皇杯 日本体育大学ロスター", "日本バスケットボール協会", "https://zennihon2025-26.japanbasketball.jp/team/fin/m02/"),
    ("B3S0007", "第77回インカレ 日本体育大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/5/type/intercollege/y/2025/s/men"),
    ("B3S0008", "第76回インカレ 青山学院大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/9/type/intercollege/y/2024/s/men"),
    ("B3S0009", "第76回インカレ 青山学院大学対天理大学", "全日本大学バスケットボール連盟", "https://jubf.jp/game/detail/id/1194/type/intercollege/s/men"),
    ("B3S0010", "第77回インカレ 九州国際大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/230/type/intercollege/y/2025/s/men"),
    ("B3S0011", "第74回インカレ 東海大学九州ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/12/type/intercollege/y/2022/s/men"),
    ("B3S0012", "第75回インカレ 東海大学九州ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/12/type/intercollege/y/2023/s/men"),
    ("B3S0013", "第76回インカレ 東海大学九州ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/12/type/intercollege/y/2024/s/men"),
    ("B3S0014", "第77回インカレ 東海大学九州ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/12/type/intercollege/y/2025/s/men"),
    ("B3S0015", "第76回インカレ 山梨学院大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/204/type/intercollege/y/2024/s/men"),
    ("B3S0016", "第77回インカレ 山梨学院大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/204/type/intercollege/y/2025/s/men"),
    ("B3S0017", "第77回インカレ 山梨学院大学対名古屋学院大学", "全日本大学バスケットボール連盟", "https://jubf.jp/game/detail/id/1365/type/intercollege/s/men"),
    ("B3S0018", "第73回インカレ 専修大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/25/type/intercollege/y/2021/s/men"),
    ("B3S0019", "第74回インカレ 専修大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/25/type/intercollege/y/2022/s/men"),
    ("B3S0020", "第75回インカレ 専修大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/25/type/intercollege/y/2023/s/men"),
    ("B3S0021", "第76回インカレ 専修大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/25/type/intercollege/y/2024/s/men"),
    ("B3S0022", "キエキエ・トピー・アリ 選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=36413"),
    ("B3S0023", "第74回インカレ 日本経済大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/180/type/intercollege/y/2022/s/men"),
    ("B3S0024", "第75回インカレ 日本経済大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/180/type/intercollege/y/2023/s/men"),
    ("B3S0025", "第76回インカレ 日本経済大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/180/type/intercollege/y/2024/s/men"),
    ("B3S0026", "第76回インカレ 日本経済大学対中央大学", "全日本大学バスケットボール連盟", "https://jubf.jp/game/detail/id/1214/type/intercollege/s/men"),
    ("B3S0027", "2023年度新人戦 日本体育大学プロフィール", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/5/type/rookie/y/2023/s/men"),
    ("B3S0028", "第76回インカレ 日本体育大学プロフィール", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/5/type/intercollege/y/2024/s/men"),
]

# entity_type, entity_id, field, value, source_id, locator, summary, assessment, note
EVIDENCE = [
    ("Person", "P000028", "name", "佐藤 涼成", "B3S0004", "PDF 選手一覧 > SATO, Ryosei", "白鷗大学2年の選手として掲載", "SUPPORTED", ""),
    ("Person", "P000028", "name_en", "Ryosei Sato", "B3S0004", "PDF 選手一覧 > SATO, Ryosei", "公式資料の英語表記", "SUPPORTED", ""),
    ("Person", "P000028", "birth_date", "2003-07-09", "B3S0004", "PDF 選手一覧 > 生年月日", "生年月日を掲載", "SUPPORTED", ""),
    ("Person", "P000029", "name", "早田 流星", "B3S0006", "日本体育大学 > No.10", "大会公式ロスターの氏名", "SUPPORTED", ""),
    ("Person", "P000029", "birth_date", "2003-07-18", "B3S0006", "日本体育大学 > No.10 > 生年月日", "生年月日を掲載", "SUPPORTED", ""),
    ("Person", "P000030", "name", "鷹野 祐磨", "B3S0003", "PDF 1ページ > TAKANO, Yuma", "福岡第一高校1年の選手として掲載", "SUPPORTED", ""),
    ("Person", "P000030", "name_en", "Yuma Takano", "B3S0003", "PDF 1ページ > TAKANO, Yuma", "公式資料の英語表記", "SUPPORTED", ""),
    ("Person", "P000030", "birth_date", "2003-11-28", "B3S0003", "PDF 1ページ > 生年月日", "生年月日を掲載", "SUPPORTED", ""),
    ("Person", "P000031", "name", "星賀 舞也", "B3S0008", "青山学院大学 ROSTER > No.25", "大会公式ロスターの氏名", "SUPPORTED", ""),
    ("Person", "P000032", "name", "岡本 汰稀", "B3S0010", "九州国際大学 ROSTER > No.23", "大会公式ロスターの氏名", "SUPPORTED", ""),
    ("Person", "P000033", "name", "岩下 周介", "B3S0011", "東海大学九州 ROSTER > No.17", "大会公式ロスターの氏名", "SUPPORTED", ""),
    ("Person", "P000034", "name", "カマレ ムレマ フランシス", "B3S0016", "山梨学院大学 ROSTER > No.70", "大会公式ロスターの氏名", "SUPPORTED", ""),
    ("Person", "P000010", "name", "當山 修梧", "B3S0018", "専修大学 ROSTER > No.3", "大会公式ロスターの氏名", "SUPPORTED", ""),
    ("Person", "P000014", "name", "キエキエ トピー アリ", "B3S0022", "選手プロフィール > 選手名", "B.LEAGUE公式プロフィールの氏名", "SUPPORTED", ""),
    ("Person", "P000014", "name_en", "Topy Ali Kiekie", "B3S0022", "選手プロフィール > 英語表記", "B.LEAGUE公式プロフィールの英語表記", "SUPPORTED", ""),
    ("Person", "P000014", "birth_date", "2003-03-23", "B3S0022", "選手プロフィール > 生年月日", "生年月日を掲載", "SUPPORTED", ""),
    ("Person", "P000016", "name", "本松 龍斗", "B3S0027", "日本体育大学 PROFILE > 学生コーチ", "大会公式プロフィールの氏名", "SUPPORTED", ""),
]


def add_career_evidence(career_id, field, value, source, locator, summary, assessment="SUPPORTED", note=""):
    EVIDENCE.append(("Career", career_id, field, value, source, locator, summary, assessment, note))


# 2021年度福岡第一：大会登録と、出場時間がある選手の競技参加を分ける。
for career_id, number, name, participation in [
    ("C000046", "88", "佐藤 涼成", "35:46"),
    ("C000047", "10", "早田 流星", "12:53"),
    ("C000048", "14", "鷹野 祐磨", "DNP"),
    ("C000049", "24", "星賀 舞也", "27:07"),
    ("C000050", "30", "岡本 汰稀", "DNP"),
    ("C000051", "68", "岩下 周介", "DNP"),
    ("C000052", "70", "カマレ ムレマ フランシス", "07:19"),
]:
    locator = f"福岡第一高等学校 BOX SCORE > No.{number} {name}"
    add_career_evidence(career_id, "organization_id", "ORG000010", "B3S0001", locator, "福岡第一高等学校の登録選手として掲載")
    add_career_evidence(career_id, "role", "Player", "B3S0001", locator, "選手欄に掲載")
    add_career_evidence(career_id, "jersey_number", number, "B3S0001", locator, "大会登録背番号")
    add_career_evidence(career_id, "activity_date", "2021-12-28", "B3S0001", "試合情報 > 試合期日", "大会登録を確認した試合日", note="Career開始日・終了日を意味しない")
    if participation != "DNP":
        add_career_evidence(career_id, "competition_participation", participation, "B3S0001", locator, f"出場時間{participation}を記録")
    else:
        add_career_evidence(career_id, "competition_participation", "DNP", "B3S0001", locator, "登録はあるが当該試合はDNP", "PARTIAL", "出場確認として扱わない")

# 高校時の追加公式値。
for career_id, number, height, name in [
    ("C000046", "88", "172", "佐藤 涼成"),
    ("C000047", "10", "184", "早田 流星"),
    ("C000049", "24", "190", "星賀 舞也"),
    ("C000010", "1", "180", "當山 修梧"),
    ("C000014", "65", "200", "キエキエトピー アリ"),
]:
    locator = f"福岡第一高校 > プレイヤー > No.{number} {name}"
    add_career_evidence(career_id, "organization_id", "ORG000010", "B3S0002", locator, "福岡第一高校の公式ロスターに掲載")
    add_career_evidence(career_id, "role", "Player", "B3S0002", locator, "選手として掲載")
    add_career_evidence(career_id, "jersey_number", number, "B3S0002", locator, "2020年大会の登録背番号")
    add_career_evidence(career_id, "height_cm", height, "B3S0002", locator, "2020年大会の登録身長")
    add_career_evidence(career_id, "activity_date", "2020-11-28", "B3S0002", locator, "第96回天皇杯1次ラウンド登録", note="Career開始日・終了日を意味しない")

for field, value, summary in [
    ("organization_id", "ORG000010", "福岡第一高校1年として掲載"),
    ("role", "Player", "U16日本代表候補選手として掲載"),
    ("grade", "1年", "2019年4月時点の学年"),
    ("position", "SF", "登録ポジション"),
    ("height_cm", "185", "登録身長"),
]:
    add_career_evidence("C000048", field, value, "B3S0003", "PDF 1ページ > TAKANO, Yuma", summary, note="入学・卒業年月は直接示さない" if field == "grade" else "")

# 大学Career。学年は年度別Evidenceとして保持し、在籍期間へ変換しない。
university_records = [
    ("C000213", "ORG000093", "B3S0004", "白鷗大学2年 > SATO, Ryosei", "2年", "PG", "173", "", "2024"),
    ("C000214", "ORG000020", "B3S0007", "日本体育大学 ROSTER > No.10", "4年", "PF", "185", "10", "2025"),
    ("C000215", "ORG000030", "B3S0008", "青山学院大学 ROSTER > No.25", "3年", "SF", "190", "25", "2024"),
    ("C000216", "ORG000094", "B3S0010", "九州国際大学 ROSTER > No.23", "4年", "PF", "190", "23", "2025"),
    ("C000217", "ORG000095", "B3S0011", "東海大学九州 ROSTER > No.17", "1年", "PG", "177", "17", "2022"),
    ("C000217", "ORG000095", "B3S0012", "東海大学九州 ROSTER > No.17", "2年", "PG", "177", "17", "2023"),
    ("C000217", "ORG000095", "B3S0013", "東海大学九州 ROSTER > No.17", "3年", "SG", "177", "17", "2024"),
    ("C000217", "ORG000095", "B3S0014", "東海大学九州 ROSTER > No.17", "4年", "SG", "177", "17", "2025"),
    ("C000218", "ORG000096", "B3S0015", "山梨学院大学 ROSTER > No.70", "3年", "C", "206", "70", "2024"),
    ("C000218", "ORG000096", "B3S0016", "山梨学院大学 ROSTER > No.70", "4年", "C", "206", "70", "2025"),
    ("C000031", "ORG000018", "B3S0018", "専修大学 ROSTER > No.3", "2年", "PG", "180", "3", "2021"),
    ("C000031", "ORG000018", "B3S0019", "専修大学 ROSTER > No.3", "2年", "PG", "180", "3", "2022"),
    ("C000031", "ORG000018", "B3S0020", "専修大学 ROSTER > No.3", "3年", "PG", "180", "3", "2023"),
    ("C000031", "ORG000018", "B3S0021", "専修大学 ROSTER > No.3", "4年", "PG", "180", "3", "2024"),
    ("C000030", "ORG000017", "B3S0023", "日本経済大学 ROSTER > No.3", "2年", "C", "203", "3", "2022"),
    ("C000030", "ORG000017", "B3S0024", "日本経済大学 ROSTER > No.33", "3年", "C", "203", "33", "2023"),
    ("C000030", "ORG000017", "B3S0025", "日本経済大学 ROSTER > No.33", "4年", "C", "203", "33", "2024"),
]
seen_base = set()
for career_id, org_id, source, locator, grade, position, height, jersey, year in university_records:
    if career_id not in seen_base:
        add_career_evidence(career_id, "organization_id", org_id, source, locator, "大学公式大会ロスターに掲載")
        add_career_evidence(career_id, "role", "Player", source, locator, "登録選手として掲載")
        seen_base.add(career_id)
    for field, value, label in [
        ("grade", grade, f"{year}年大会の学年"),
        ("position", position, f"{year}年大会の登録ポジション"),
        ("height_cm", height, f"{year}年大会の登録身長"),
        ("activity_year", year, f"{year}年大会の登録"),
    ]:
        assessment = "CONFLICT" if career_id == "C000031" and field == "grade" and year in {"2021", "2022"} else "SUPPORTED"
        note = "JUBF公式で2021年と2022年がともに2年と表示" if assessment == "CONFLICT" else ("在籍開始・終了年月は直接示さない" if field == "activity_year" else "")
        add_career_evidence(career_id, field, value, source, locator, label, assessment, note)
    if jersey:
        add_career_evidence(career_id, "jersey_number", jersey, source, locator, f"{year}年大会の登録背番号")

# 大会成績・BOXで実競技参加を確認できたもの。
for career_id, source, locator, value, summary in [
    ("C000214", "B3S0007", "日本体育大学 > 大会成績 > 早田流星", "2試合", "2025年大会で2試合出場"),
    ("C000215", "B3S0009", "青山学院大学 BOX SCORE > No.25", "28:59", "2024年12月4日の試合で28分59秒出場"),
    ("C000216", "B3S0010", "九州国際大学 > 大会成績 > 岡本汰稀", "2試合", "2025年大会で2試合出場"),
    ("C000217", "B3S0014", "東海大学九州 > 大会成績 > 岩下周介", "2試合・58:49", "2025年大会で2試合58分49秒出場"),
    ("C000218", "B3S0017", "山梨学院大学 BOX SCORE > No.70", "15:26", "2025年12月の試合で15分26秒出場"),
    ("C000031", "B3S0021", "専修大学 > 大会成績 > 當山修梧", "3試合・29:11", "2024年大会で3試合29分11秒出場"),
    ("C000030", "B3S0026", "日本経済大学 BOX SCORE > No.33", "34:00・21得点", "2024年12月の試合で34分00秒出場し21得点"),
]:
    add_career_evidence(career_id, "competition_participation", value, source, locator, summary)

# クラブ公式経歴も白鷗大学との関係を裏付けるが、在籍期間は示さない。
add_career_evidence(
    "C000213", "organization_id", "ORG000093", "B3S0005",
    "選手プロフィール > 出身校・在籍校 > 白鷗大学",
    "横浜ビー・コルセアーズ公式が白鷗大学在学中と記載",
    note="大学Careerの開始・終了年月は直接示さない",
)

# 本松龍斗は大学で選手ではなく、公式PROFILEの学生コーチとして候補化。
for source, year in [("B3S0027", "2023"), ("B3S0028", "2024")]:
    locator = "日本体育大学 PROFILE > 学生コーチ > 本松龍斗"
    add_career_evidence("C000033", "organization_id", "ORG000020", source, locator, "日本体育大学の学生コーチとして掲載")
    add_career_evidence("C000033", "role", "Student Coach", source, locator, f"{year}年大会の役割")
    add_career_evidence("C000033", "activity_year", year, source, locator, f"{year}年大会プロフィールに掲載", note="学籍開始・終了年月は直接示さない")

ISSUES = [
    ("P000028", "C000046", "PERIOD_UNKNOWN", "HOLD", "高校Careerの開始・終了年月は未確認", "高校公式の入学・卒業または複数年度ロスターを確認"),
    ("P000028", "C000213", "PERIOD_UNKNOWN", "HOLD", "白鷗大学で2024年2年を確認したが開始・終了年月は未確認", "大学または競技団体の年度別資料を追加確認"),
    ("P000029", "C000047", "PERIOD_UNKNOWN", "HOLD", "高校Careerの開始・終了年月は未確認", "高校公式資料を確認"),
    ("P000029", "C000214", "PERIOD_UNKNOWN", "HOLD", "日本体育大学で2025年4年を確認したが開始・終了年月は未確認", "大学公式資料を確認"),
    ("P000030", "C000048", "PERIOD_UNKNOWN", "HOLD", "高校1年時と2021年大会登録を確認したが終了年月は未確認", "高校公式資料を確認"),
    ("P000030", "P000030", "POST_HIGH_SCHOOL_UNKNOWN", "HOLD", "卒業後の実所属と競技参加を示す公式資料を確認できない", "候補先を推測せず公式ロスターを待つ"),
    ("P000031", "C000049", "PERIOD_UNKNOWN", "HOLD", "高校Careerの開始・終了年月は未確認", "高校公式資料を確認"),
    ("P000031", "C000215", "PERIOD_UNKNOWN", "HOLD", "青山学院大学で2024年3年を確認したが開始・終了年月は未確認", "大学公式資料を確認"),
    ("P000032", "C000050", "PERIOD_UNKNOWN", "HOLD", "高校Careerの開始・終了年月は未確認", "高校公式資料を確認"),
    ("P000032", "C000216", "PERIOD_UNKNOWN", "HOLD", "九州国際大学で2025年4年を確認したが開始・終了年月は未確認", "大学公式資料を確認"),
    ("P000033", "C000051", "PERIOD_UNKNOWN", "HOLD", "高校Careerの開始・終了年月は未確認", "高校公式資料を確認"),
    ("P000033", "C000217", "SOURCE_CONFLICT", "HOLD", "外部調査の2023年4年という記載はJUBF公式の2023年2年と不一致", "JUBF公式値を候補とし外部回答値は採用しない"),
    ("P000033", "C000217", "PERIOD_UNKNOWN", "HOLD", "2022年1年から2025年4年の大会登録を確認したが入学・卒業年月は未確認", "期間は公式な年月資料が見つかるまで空欄"),
    ("P000034", "C000052", "PERIOD_UNKNOWN", "HOLD", "高校Careerの開始・終了年月は未確認", "高校公式資料を確認"),
    ("P000034", "C000218", "JERSEY_CONFLICT", "HOLD", "外部調査の大学背番号75はJUBF公式の70と不一致。2025年の75は別選手", "年度別公式ロスターの70を候補とする"),
    ("P000034", "C000218", "PERIOD_UNKNOWN", "HOLD", "山梨学院大学で2024年3年・2025年4年を確認したが開始・終了年月は未確認", "大学公式資料を確認"),
    ("P000010", "C000010", "PERIOD_UNKNOWN", "HOLD", "高校Careerの開始・終了年月は未確認", "高校公式資料を確認"),
    ("P000010", "C000031", "GRADE_CONFLICT", "HOLD", "JUBF公式で2021年と2022年がともに2年と表示される", "学年から在籍期間を逆算せず資料表示を年度別に保持"),
    ("P000010", "C000031", "PERIOD_UNKNOWN", "HOLD", "専修大学の開始・終了年月は未確認", "大学公式資料を確認"),
    ("P000014", "C000014", "PERIOD_UNKNOWN", "HOLD", "高校Careerの開始・終了年月は未確認", "高校公式資料を確認"),
    ("P000014", "C000030", "PERIOD_UNKNOWN", "HOLD", "2022年2年から2024年4年の大会登録を確認したが入学・卒業年月は未確認", "期間は公式な年月資料が見つかるまで空欄"),
    ("P000016", "P000016", "HIGH_SCHOOL_ROLE_UNKNOWN", "HOLD", "福岡第一高校出身は大学資料から確認できるが高校バスケットボール部での役割は未確認", "高校公式ロスターまたは部資料を確認"),
    ("P000016", "C000033", "ROLE_CORRECTION", "RESOLVED", "Excelの大学Player候補を採用せずJUBF公式のStudent Coachに修正", "2023年・2024年の公式PROFILEで確認済み"),
    ("P000016", "C000033", "PERIOD_UNKNOWN", "HOLD", "日本体育大学で2023年・2024年に学生コーチを確認したが学籍期間は未確認", "大学公式資料を確認"),
]


def write_csv(filename, headers, rows):
    with (OUTPUT_DIR / filename).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv("person_candidates.csv", ["person_id", "name"], PEOPLE)
    write_csv("organization_candidates.csv", ["organization_id", "name"], ORGANIZATIONS)
    write_csv("career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], CAREERS)
    write_csv("source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], [(*row, CHECKED_AT) for row in SOURCES])
    evidence_rows = []
    for index, row in enumerate(EVIDENCE, 1):
        evidence_rows.append((f"B3E{index:04d}", *row[:6], row[6], row[7], CHECKED_AT, row[8]))
    write_csv(
        "evidence_records.csv",
        ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"],
        evidence_rows,
    )
    issue_rows = [(f"B3I{index:04d}", *row) for index, row in enumerate(ISSUES, 1)]
    write_csv("issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], issue_rows)

    supported = {}
    for entity_type, entity_id, field, _value, _source, _locator, _summary, assessment, _note in EVIDENCE:
        if assessment == "SUPPORTED":
            supported.setdefault((entity_type, entity_id), [])
            if field not in supported[(entity_type, entity_id)]:
                supported[(entity_type, entity_id)].append(field)
    decisions = []
    targets = [("Person", person_id) for person_id, _ in PEOPLE] + [("Career", row[0]) for row in CAREERS]
    for index, (entity_type, entity_id) in enumerate(targets, 1):
        fields = supported.get((entity_type, entity_id), [])
        decision = "READY_FOR_VERIFIED_REVIEW" if fields else "HOLD_CANDIDATE"
        held = "start|end" if entity_type == "Career" else ""
        if entity_type == "Career" and entity_id == "C000031":
            held = "start|end|grade"
        if entity_type == "Career" and entity_id == "C000033":
            held = "start|end|Player role"
        reason = "公式資料で項目単位の裏付けを確認" if fields else "公式資料による裏付け不足"
        decisions.append((f"B3D{index:04d}", entity_type, entity_id, decision, "|".join(fields), held, reason, CHECKED_AT))
    write_csv("qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"], decisions)


if __name__ == "__main__":
    main()
