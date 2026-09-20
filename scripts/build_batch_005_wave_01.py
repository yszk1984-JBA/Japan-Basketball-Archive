#!/usr/bin/env python3
"""Build Batch 005 Wave 1 candidates without touching VERIFIED or MASTER."""

from __future__ import annotations

import csv
from pathlib import Path


OUT = Path("data/candidate/batch_005/wave_01")
CHECKED = "2026-09-21"


def write(name: str, headers: list[str], rows: list[list[str]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def main() -> None:
    write("person_candidates.csv", ["person_id", "name"], [
        ["P000073", "崎濱 秀斗"],
        ["P000074", "轟 琉維"],
        ["P000028", "佐藤 涼成"],
        ["P000066", "河合 瑠那"],
    ])
    write("organization_candidates.csv", ["organization_id", "name"], [
        ["ORG000010", "福岡第一高等学校"],
        ["ORG000015", "東海大学"],
        ["ORG000048", "佐賀バルーナーズ"],
        ["ORG000055", "横浜ビー・コルセアーズ"],
        ["ORG000090", "横浜エクセレンス"],
        ["ORG000093", "白鷗大学"],
        ["ORG000106", "琉球ゴールデンキングス"],
        ["ORG000107", "琉球ゴールデンキングスU18"],
        ["ORG000108", "セントトーマス モア スクール"],
        ["ORG000109", "アルバルク東京"],
        ["ORG000110", "広島ドラゴンフライズ"],
    ])
    write("career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], [
        ["C000257", "P000073", "ORG000010", "Player", "2021", "2024"],
        ["C000258", "P000073", "ORG000107", "Player", "2024", "2024"],
        ["C000259", "P000073", "ORG000108", "Player", "2024", ""],
        ["C000260", "P000073", "ORG000106", "Player", "2024", "2026"],
        ["C000261", "P000074", "ORG000010", "Player", "", ""],
        ["C000262", "P000074", "ORG000015", "Player", "", ""],
        ["C000263", "P000074", "ORG000109", "Player", "2025", "2025"],
        ["C000264", "P000074", "ORG000048", "Player", "2025", "2026"],
        ["C000265", "P000028", "ORG000055", "Player", "2025", "2025"],
        ["C000266", "P000028", "ORG000110", "Player", "2025", ""],
        ["C000229", "P000066", "ORG000090", "Player", "2026", "2026"],
    ])
    write("source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], [
        ["B5W1S0001", "#17 崎濱秀斗選手加入（特別指定選手）のお知らせ", "琉球ゴールデンキングス", "https://goldenkings.jp/retired_numbers_26/detail_26/id=21221", CHECKED],
        ["B5W1S0002", "崎濱秀斗 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=51000486", CHECKED],
        ["B5W1S0003", "#17 崎濱秀斗選手 特別指定選手の活動終了のご報告", "琉球ゴールデンキングス", "https://goldenkings.jp/clubkings/pages/id=25788", CHECKED],
        ["B5W1S0004", "轟 琉維選手 2024-25シーズン 特別指定選手 加入のお知らせ", "アルバルク東京", "https://www.alvark-tokyo.jp/news/detail/team/id=19876", CHECKED],
        ["B5W1S0005", "#8 轟 琉維選手 リーグ登録完了のお知らせ", "アルバルク東京", "https://www.alvark-tokyo.jp/news/detail/event/team/media/id=19920", CHECKED],
        ["B5W1S0006", "2/8（土）仙台89ERS戦 ゲームレポート", "アルバルク東京", "https://www.alvark-tokyo.jp/news/detail/game/id=250208", CHECKED],
        ["B5W1S0007", "轟 琉維選手 2024-25シーズン 特別指定選手 活動終了のご報告", "アルバルク東京", "https://www.alvark-tokyo.jp/news/detail/team/id=20126", CHECKED],
        ["B5W1S0008", "轟琉維 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=51000457", CHECKED],
        ["B5W1S0009", "佐藤涼成選手 2024-25シーズン 特別指定選手登録のお知らせ", "横浜ビー・コルセアーズ", "https://b-corsairs.com/news/team_20241221_1/", CHECKED],
        ["B5W1S0010", "佐藤涼成 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=51000447", CHECKED],
        ["B5W1S0011", "#88 佐藤 涼成選手 契約合意（新規）のお知らせ", "広島ドラゴンフライズ", "https://hiroshimadragonflies.com/news/detail/id=21158", CHECKED],
        ["B5W1S0012", "2026-27シーズン 契約合意（継続）選手のお知らせ", "広島ドラゴンフライズ", "https://hiroshimadragonflies.com/news/detail/id=24483", CHECKED],
        ["B5W1S0013", "河合瑠那選手 特別指定選手登録のお知らせ", "横浜エクセレンス", "https://yokohama-ex.jp/team/pages/id=22814", CHECKED],
        ["B5W1S0014", "河合瑠那 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=51000607", CHECKED],
        ["B5W1S0015", "河合瑠那 選手 特別指定選手活動終了のお知らせ", "横浜エクセレンス", "https://yokohama-ex.jp/news/detail/id=25440", CHECKED],
    ])

    evidence: list[list[str]] = []

    def ev(number: int, entity_type: str, entity_id: str, field: str, value: str,
           source: str, locator: str, summary: str,
           assessment: str = "SUPPORTED", note: str = "") -> None:
        evidence.append([
            f"B5W1E{number:04d}", entity_type, entity_id, field, value,
            source, locator, summary, assessment, CHECKED, note,
        ])

    # 崎濱秀斗：学校歴、プロ契約、リーグ出場、活動終了を分離する。
    ev(1, "Person", "P000073", "name", "崎濱 秀斗", "B5W1S0002", "基本情報 > 選手名", "B.LEAGUE公式の氏名")
    ev(2, "Person", "P000073", "name_en", "Shuto Sakihama", "B5W1S0002", "基本情報 > 英語表記", "B.LEAGUE公式の英語表記")
    ev(3, "Person", "P000073", "birth_date", "2005-05-08", "B5W1S0001", "選手プロフィール > 生年月日", "クラブ公式プロフィール")
    ev(4, "Person", "P000073", "height_cm", "178", "B5W1S0001", "選手プロフィール > 身長", "加入発表時の登録身長")
    ev(5, "Person", "P000073", "weight_kg", "84", "B5W1S0001", "選手プロフィール > 体重", "加入発表時の登録体重")
    ev(6, "Person", "P000073", "position", "PG", "B5W1S0001", "選手プロフィール > ポジション", "加入発表時の登録ポジション")
    ev(7, "Career", "C000257", "organization_id", "ORG000010", "B5W1S0001", "選手プロフィール > 経歴 > 2021-24", "福岡第一高校を掲載")
    ev(8, "Career", "C000257", "start", "2021", "B5W1S0001", "選手プロフィール > 経歴", "高校経歴の開始年")
    ev(9, "Career", "C000257", "end", "2024", "B5W1S0001", "選手プロフィール > 経歴", "高校経歴の終了年")
    ev(10, "Career", "C000257", "role", "Player", "B5W1S0001", "本文 > 福岡第一高校時代", "チームの中心選手として活動したとの記載")
    ev(11, "Career", "C000258", "organization_id", "ORG000107", "B5W1S0001", "選手プロフィール > 経歴 > 2024", "琉球ゴールデンキングスU18を掲載")
    ev(12, "Career", "C000258", "role", "Player", "B5W1S0001", "本文 > キングスU18での活動経験", "選手としての活動経験")
    ev(13, "Career", "C000258", "start", "2024", "B5W1S0001", "選手プロフィール > 経歴", "U18活動年")
    ev(14, "Career", "C000258", "end", "2024", "B5W1S0001", "選手プロフィール > 経歴", "U18活動年")
    ev(15, "Career", "C000259", "organization_id", "ORG000108", "B5W1S0002", "基本情報 > 出身校", "セントトーマス モア スクールを掲載")
    ev(16, "Career", "C000259", "role", "Player", "B5W1S0001", "本文 > 学業とバスケットボール", "同校で競技活動を行う記載")
    ev(17, "Career", "C000259", "start", "2024", "B5W1S0001", "選手プロフィール > 経歴 > 2024-", "開始年を掲載")
    ev(18, "Career", "C000260", "organization_id", "ORG000106", "B5W1S0001", "加入発表本文", "琉球ゴールデンキングスへの加入")
    ev(19, "Career", "C000260", "role", "Player", "B5W1S0001", "加入発表本文", "特別指定選手のプロ契約")
    ev(20, "Career", "C000260", "registration_type", "特別指定選手（プロ契約）", "B5W1S0001", "加入発表本文", "契約区分を明記")
    ev(21, "Career", "C000260", "start", "2024", "B5W1S0003", "主な経歴 > 2024-26", "クラブ経歴の開始年")
    ev(22, "Career", "C000260", "end", "2026", "B5W1S0003", "主な経歴 > 2024-26", "クラブ経歴の終了年")
    ev(23, "Career", "C000260", "competition_participation", "2024-25 B1 13試合・CS 4試合、2025-26 B1 40試合", "B5W1S0002", "シーズン成績", "B.LEAGUE公式戦出場")
    ev(24, "Career", "C000260", "activity_status", "活動終了・退団", "B5W1S0003", "発表本文", "特別指定選手としての活動終了と退団")

    # 轟琉維：アルバルク東京の契約・登録・出場・終了と、佐賀での出場を分離する。
    ev(25, "Person", "P000074", "name", "轟 琉維", "B5W1S0008", "基本情報 > 選手名", "B.LEAGUE公式の氏名")
    ev(26, "Person", "P000074", "name_en", "Rui Todoroki", "B5W1S0008", "基本情報 > 英語表記", "B.LEAGUE公式の英語表記")
    ev(27, "Person", "P000074", "birth_date", "2004-05-01", "B5W1S0004", "選手プロフィール > 生年月日", "クラブ公式プロフィール")
    ev(28, "Person", "P000074", "height_cm", "169", "B5W1S0008", "基本情報 > 身長", "B.LEAGUE公式の登録身長")
    ev(29, "Person", "P000074", "weight_kg", "71", "B5W1S0008", "基本情報 > 体重", "B.LEAGUE公式の登録体重")
    ev(30, "Person", "P000074", "position", "PG", "B5W1S0004", "選手プロフィール > ポジション", "クラブ公式の登録ポジション")
    ev(31, "Career", "C000261", "organization_id", "ORG000010", "B5W1S0004", "選手プロフィール > 出身校", "福岡第一高校を掲載")
    ev(32, "Career", "C000261", "role", "Player", "B5W1S0004", "選手加入プロフィール", "競技者経歴として掲載", "PARTIAL", "高校在籍期間は未確認")
    ev(33, "Career", "C000262", "organization_id", "ORG000015", "B5W1S0005", "選手プロフィール > 出身校", "東海大学在学中・2年と掲載")
    ev(34, "Career", "C000262", "role", "Player", "B5W1S0004", "本文 > 東海大学2年", "東海大学所属選手として掲載")
    ev(35, "Career", "C000262", "grade", "2年", "B5W1S0005", "選手プロフィール > 出身校", "2025年1月時点で2年")
    ev(36, "Career", "C000263", "organization_id", "ORG000109", "B5W1S0004", "加入発表本文", "アルバルク東京への加入")
    ev(37, "Career", "C000263", "role", "Player", "B5W1S0004", "加入発表本文", "特別指定選手として加入")
    ev(38, "Career", "C000263", "registration_type", "特別指定選手", "B5W1S0004", "発表見出し・本文", "登録区分を明記")
    ev(39, "Career", "C000263", "league_registration", "2025-01-11登録完了", "B5W1S0005", "発表本文", "リーグ登録手続き完了")
    ev(40, "Career", "C000263", "competition_participation", "2025-02-08 Bリーグ初出場・初得点", "B5W1S0006", "ゲームレポート冒頭", "B1公式戦デビュー")
    ev(41, "Career", "C000263", "activity_end", "2025-03-05", "B5W1S0007", "発表本文", "活動終了日を明記")
    ev(42, "Career", "C000264", "organization_id", "ORG000048", "B5W1S0008", "クラブ所属履歴 > 2025-26", "佐賀所属を掲載")
    ev(43, "Career", "C000264", "role", "Player", "B5W1S0008", "シーズン成績 > 2025-26 B1", "佐賀での公式戦出場")
    ev(44, "Career", "C000264", "registration_type", "特別指定選手", "B5W1S0008", "クラブ所属履歴・公式戦成績", "B.LEAGUE選手ページで所属・出場を確認", "PARTIAL", "登録区分はクラブ一次発表の追加確認が必要")
    ev(45, "Career", "C000264", "competition_participation", "2025-26 B1 13試合", "B5W1S0008", "シーズン成績・試合成績", "佐賀でのB1公式戦出場")

    # 佐藤涼成：横浜BC特別指定と広島のプロ契約を別Careerにする。
    ev(46, "Person", "P000028", "name", "佐藤 涼成", "B5W1S0010", "基本情報 > 選手名", "B.LEAGUE公式の氏名")
    ev(47, "Person", "P000028", "name_en", "Ryosei Sato", "B5W1S0010", "基本情報 > 英語表記", "B.LEAGUE公式の英語表記")
    ev(48, "Person", "P000028", "birth_date", "2003-07-09", "B5W1S0011", "選手プロフィール > 生年月日", "クラブ公式プロフィール")
    ev(49, "Career", "C000265", "organization_id", "ORG000055", "B5W1S0009", "登録発表本文", "横浜ビー・コルセアーズで登録")
    ev(50, "Career", "C000265", "role", "Player", "B5W1S0009", "登録発表本文", "特別指定選手として登録")
    ev(51, "Career", "C000265", "registration_type", "特別指定選手", "B5W1S0009", "発表見出し・本文", "登録区分を明記")
    ev(52, "Career", "C000265", "activity_period", "2025-01-01〜2025-03-05", "B5W1S0009", "登録発表 > 活動期間", "開始日と終了日を明記")
    ev(53, "Career", "C000265", "competition_participation", "2024-25 B1 7試合", "B5W1S0010", "シーズン成績", "横浜BCでのB1公式戦出場")
    ev(54, "Career", "C000266", "organization_id", "ORG000110", "B5W1S0011", "契約発表本文", "広島ドラゴンフライズとの契約")
    ev(55, "Career", "C000266", "role", "Player", "B5W1S0011", "契約発表本文", "特別指定選手のプロ契約")
    ev(56, "Career", "C000266", "contract_type", "特別指定選手（プロ契約）", "B5W1S0011", "契約発表本文", "契約区分を明記")
    ev(57, "Career", "C000266", "start", "2025", "B5W1S0011", "経歴 > 2025年-", "クラブ経歴の開始年")
    ev(58, "Career", "C000266", "competition_participation", "2025-26 B1 25試合", "B5W1S0010", "シーズン成績", "広島でのB1公式戦出場")
    ev(59, "Career", "C000266", "contract_continuation", "2026-27以降の複数年契約", "B5W1S0012", "佐藤涼成 > GMコメント", "来季以降の複数年契約合意")

    # 河合瑠那：既存Career IDを再利用し、プロ活動の状態を補強する。
    ev(60, "Person", "P000066", "name", "河合 瑠那", "B5W1S0014", "基本情報 > 選手名", "B.LEAGUE公式の氏名")
    ev(61, "Person", "P000066", "name_en", "Runa Kawai", "B5W1S0014", "基本情報 > 英語表記", "B.LEAGUE公式の英語表記")
    ev(62, "Career", "C000229", "organization_id", "ORG000090", "B5W1S0013", "登録発表本文", "横浜エクセレンスで特別指定選手登録")
    ev(63, "Career", "C000229", "role", "Player", "B5W1S0014", "シーズン成績 > 2025-26 B2", "B2公式戦出場")
    ev(64, "Career", "C000229", "registration_type", "特別指定選手", "B5W1S0013", "発表見出し・本文", "登録区分を明記")
    ev(65, "Career", "C000229", "competition_participation", "2025-26 B2 1試合3分33秒・2得点", "B5W1S0014", "シーズン成績", "B2公式戦出場")
    ev(66, "Career", "C000229", "activity_end_announcement", "2026-05-21", "B5W1S0015", "公開日・発表本文", "2025-26シーズンをもって活動終了")
    ev(67, "Career", "C000229", "free_agent_list_announcement", "2026-05-21", "B5W1S0015", "発表本文", "同日に自由交渉選手リストへ公示予定と発表")

    # 組織名の根拠。
    org_evidence = [
        (68, "ORG000010", "福岡第一高等学校", "B5W1S0011", "選手プロフィール > 出身校"),
        (69, "ORG000015", "東海大学", "B5W1S0005", "選手プロフィール > 出身校"),
        (70, "ORG000048", "佐賀バルーナーズ", "B5W1S0008", "クラブ所属履歴 > 佐賀"),
        (71, "ORG000055", "横浜ビー・コルセアーズ", "B5W1S0009", "発行元・登録発表本文"),
        (72, "ORG000090", "横浜エクセレンス", "B5W1S0015", "発行元・活動終了本文"),
        (73, "ORG000093", "白鷗大学", "B5W1S0011", "選手プロフィール > 出身校"),
        (74, "ORG000106", "琉球ゴールデンキングス", "B5W1S0001", "発行元・加入発表本文"),
        (75, "ORG000107", "琉球ゴールデンキングスU18", "B5W1S0001", "本文・選手プロフィール > 経歴"),
        (76, "ORG000108", "セントトーマス モア スクール", "B5W1S0002", "基本情報 > 出身校"),
        (77, "ORG000109", "アルバルク東京", "B5W1S0004", "発行元・加入発表本文"),
        (78, "ORG000110", "広島ドラゴンフライズ", "B5W1S0011", "発行元・契約発表本文"),
    ]
    for number, org_id, value, source, locator in org_evidence:
        ev(number, "Organization", org_id, "name", value, source, locator, "公式資料内の組織表記")

    ev(79, "Career", "C000263", "start", "2025", "B5W1S0004", "公開日・加入発表本文", "2025年の加入を確認")
    ev(80, "Career", "C000263", "end", "2025", "B5W1S0007", "活動終了本文 > 2025年3月5日", "2025年の活動終了を確認")
    ev(81, "Career", "C000264", "start", "2025", "B5W1S0008", "クラブ所属履歴 > 2025-26 佐賀", "2025-26シーズン所属の開始年")
    ev(82, "Career", "C000264", "end", "2026", "B5W1S0008", "クラブ所属履歴 > 2025-26 佐賀", "2025-26シーズン所属の終了年")
    ev(83, "Career", "C000265", "start", "2025", "B5W1S0009", "活動期間 > 2025年1月1日", "活動開始年")
    ev(84, "Career", "C000265", "end", "2025", "B5W1S0009", "活動期間 > 2025年3月5日", "活動終了年")
    ev(85, "Career", "C000229", "start", "2026", "B5W1S0013", "特別指定選手登録発表", "2026年の登録開始を確認")
    ev(86, "Career", "C000229", "end", "2026", "B5W1S0015", "2025-26シーズンをもって活動終了", "活動終了年")

    write("evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)

    write("issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], [
        ["B5W1I0001", "P000073", "C000259", "SCHOOL_END_DATE", "HOLD", "セントトーマス モア スクールの開始年は確認したが終了年は未確認", "学校・本人・次進路の公式発表を確認"],
        ["B5W1I0002", "P000073", "C000260", "ACTIVITY_END_DATE", "HOLD", "活動終了と2024-26表記は確認したが終了日の日付はページ本文で確認できない", "クラブの公示日または登録抹消日を確認"],
        ["B5W1I0003", "P000074", "C000261", "HIGH_SCHOOL_PERIOD", "HOLD", "福岡第一高校出身は確認したが在籍開始年・終了年は未確認", "高校大会ロスターまたは公式経歴を確認"],
        ["B5W1I0004", "P000074", "C000262", "UNIVERSITY_PERIOD", "HOLD", "2025年1月時点の東海大学2年は確認したがCareer開始・終了年は未確認", "JUBFまたは大学公式の年度別ロスターを確認"],
        ["B5W1I0005", "P000074", "C000264", "SAGA_CONTRACT_REGISTRATION", "HOLD", "B.LEAGUE公式プロフィールで佐賀所属と出場は確認したが、クラブ一次資料の契約・登録区分は未確認", "佐賀バルーナーズ公式の加入・活動終了発表を確認"],
        ["B5W1I0006", "P000028", "P000028", "HEIGHT_BY_DATE", "HOLD", "横浜BC発表は173cm、広島・B.LEAGUEは175cmで時点差がある", "身長は資料時点付きで保持し単一値確定を避ける"],
        ["B5W1I0007", "P000028", "C000266", "CAREER_END_DATE", "HOLD", "2026-27以降の複数年契約は確認したがCareer終了日は将来事象で未確定", "契約終了・移籍の公式発表を継続確認"],
        ["B5W1I0008", "P000066", "C000229", "ACTIVITY_END_DATE", "HOLD", "活動終了発表日とシーズン終了は確認したが実際の登録抹消日は未確認", "リーグ公示またはクラブの登録抹消日を確認"],
        ["B5W1I0009", "P000066", "P000066", "HEIGHT_BY_SOURCE", "HOLD", "B.LEAGUEは181cm、横浜EXは183cmで資料間差がある", "身長は資料時点付きで保持し単一値確定を避ける"],
    ])

    write("qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"], [
        ["B5W1D0001", "Person", "P000073", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date|height_cm|weight_kg|position", "", "クラブ公式とB.LEAGUE公式で確認", CHECKED],
        ["B5W1D0002", "Career", "C000257", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "", "クラブ公式経歴で確認", CHECKED],
        ["B5W1D0003", "Career", "C000258", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "", "クラブ公式経歴で確認", CHECKED],
        ["B5W1D0004", "Career", "C000259", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start", "end", "クラブ公式とB.LEAGUE公式で確認", CHECKED],
        ["B5W1D0005", "Career", "C000260", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|registration_type|start|end|competition_participation|activity_status", "exact_end_date", "契約・出場・活動終了を別資料で確認", CHECKED],
        ["B5W1D0006", "Person", "P000074", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date|height_cm|weight_kg|position", "", "クラブ公式とB.LEAGUE公式で確認", CHECKED],
        ["B5W1D0007", "Career", "C000261", "READY_FOR_VERIFIED_REVIEW", "organization_id", "role|start|end", "クラブ公式の出身校経歴で確認。高校での役割と期間は保留", CHECKED],
        ["B5W1D0008", "Career", "C000262", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|grade", "start|end", "クラブ公式で大学所属と学年を確認", CHECKED],
        ["B5W1D0009", "Career", "C000263", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end|registration_type|league_registration|competition_participation|activity_end", "", "クラブ公式で加入・登録・出場・終了を確認", CHECKED],
        ["B5W1D0010", "Career", "C000264", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end|competition_participation", "registration_type|exact_start_date|exact_end_date", "B.LEAGUE公式で所属と出場を確認", CHECKED],
        ["B5W1D0011", "Person", "P000028", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "single_current_height", "クラブ公式とB.LEAGUE公式で確認", CHECKED],
        ["B5W1D0012", "Career", "C000265", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end|registration_type|activity_period|competition_participation", "", "クラブ公式とB.LEAGUE公式で確認", CHECKED],
        ["B5W1D0013", "Career", "C000266", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|contract_type|start|competition_participation|contract_continuation", "end", "広島公式とB.LEAGUE公式で確認", CHECKED],
        ["B5W1D0014", "Person", "P000066", "READY_FOR_VERIFIED_REVIEW", "name|name_en", "single_current_height", "B.LEAGUE公式で確認", CHECKED],
        ["B5W1D0015", "Career", "C000229", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end|registration_type|competition_participation|activity_end_announcement|free_agent_list_announcement", "exact_end_date", "クラブ公式とB.LEAGUE公式で確認", CHECKED],
    ] + [
        [f"B5W1D{number:04d}", "Organization", org_id, "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料内表記を確認", CHECKED]
        for number, org_id in enumerate([
            "ORG000010", "ORG000015", "ORG000048", "ORG000055", "ORG000090", "ORG000093",
            "ORG000106", "ORG000107", "ORG000108", "ORG000109", "ORG000110",
        ], start=16)
    ])


if __name__ == "__main__":
    main()
