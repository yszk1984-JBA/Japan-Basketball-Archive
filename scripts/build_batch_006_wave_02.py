#!/usr/bin/env python3
"""Build Batch 006 Wave 2 candidates without touching VERIFIED or MASTER."""

from __future__ import annotations

import csv
from pathlib import Path


OUT = Path("data/candidate/batch_006/wave_02")
CHECKED = "2026-09-22"


def write(name: str, headers: list[str], rows: list[list[str]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def main() -> None:
    write("person_candidates.csv", ["person_id", "name"], [
        ["P000079", "秋山 皓太"],
        ["P000080", "大城 侑朔"],
        ["P000081", "土居 光"],
        ["P000082", "松本 礼太"],
    ])
    write("organization_candidates.csv", ["organization_id", "name"], [
        ["ORG000010", "福岡第一高等学校"],
        ["ORG000015", "東海大学"],
        ["ORG000020", "日本体育大学"],
        ["ORG000046", "アースフレンズ東京Z"],
        ["ORG000111", "東京八王子ビートレインズ"],
        ["ORG000115", "立川ダイス"],
        ["ORG000116", "徳島ガンバロウズ"],
    ])
    write("career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], [
        ["C000278", "P000079", "ORG000010", "Player", "", ""],
        ["C000279", "P000079", "ORG000015", "Player", "", ""],
        ["C000280", "P000079", "ORG000115", "Player", "", ""],
        ["C000281", "P000080", "ORG000010", "Player", "", ""],
        ["C000282", "P000080", "ORG000020", "Player", "", ""],
        ["C000283", "P000080", "ORG000111", "Player", "2017", "2026"],
        ["C000284", "P000081", "ORG000010", "Player", "", ""],
        ["C000285", "P000081", "ORG000020", "Player", "", ""],
        ["C000286", "P000081", "ORG000046", "Player", "2025", "2026"],
        ["C000287", "P000082", "ORG000010", "Player", "", ""],
        ["C000288", "P000082", "ORG000015", "Player", "", ""],
        ["C000289", "P000082", "ORG000116", "Player", "2025", "2026"],
    ])
    write("source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], [
        ["B6W2S0001", "福岡第一高等学校 学校案内2022", "福岡第一高等学校", "https://f.f-parama.ed.jp/wp-content/uploads/2022/01/panf2022.pdf", CHECKED],
        ["B6W2S0002", "平成26年度男子U-18日本代表チーム候補選手メンバー表", "日本バスケットボール協会", "https://www.japanbasketball.jp/wp/wp-content/uploads/jba2014020-2.pdf", CHECKED],
        ["B6W2S0003", "秋山皓太 選手情報", "B3リーグ", "https://www.b3league.jp/player/?key=86&player=22402&team=2727", CHECKED],
        ["B6W2S0004", "平成23年度男子U-16日本代表候補選手 参加メンバー表", "日本バスケットボール協会", "https://www.japanbasketball.jp/wp-content/uploads/2ecfbc3e55987cf0d0eee45695bc35cf.pdf", CHECKED],
        ["B6W2S0005", "大城侑朔 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=10854", CHECKED],
        ["B6W2S0006", "第71回全日本大学バスケットボール選手権 日本体育大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/5/type/intercollege/y/2019/s/men", CHECKED],
        ["B6W2S0007", "土居光 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=36863", CHECKED],
        ["B6W2S0008", "松本礼太 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=51000138", CHECKED],
        ["B6W2S0009", "松本礼太 B3所属選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=49711", CHECKED],
        ["B6W2S0010", "徳島ガンバロウズ 2025-26チーム成績", "B3リーグ", "https://www.b3league.jp/club/tokushima/", CHECKED],
        ["B6W2S0011", "福岡第一OBの現在地 2021-22シーズン", "バスケットボールキング", "https://basketballking.jp/news/japan/highschool/20220328/365408.html", CHECKED],
        ["B6W2S0012", "第70回全日本大学バスケットボール選手権 東海大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/44/type/intercollege/y/2018/s/men", CHECKED],
        ["B6W2S0013", "第67回全日本大学バスケットボール選手権 日本体育大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/5/type/intercollege/y/2015/s/men", CHECKED],
        ["B6W2S0014", "第73回全日本大学バスケットボール選手権 東海大学ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/44/type/intercollege/y/2021/s/men", CHECKED],
    ])

    evidence: list[list[str]] = []

    def ev(number: int, entity_type: str, entity_id: str, field: str, value: str,
           source: str, locator: str, summary: str,
           assessment: str = "SUPPORTED", note: str = "") -> None:
        evidence.append([
            f"B6W2E{number:04d}", entity_type, entity_id, field, value,
            source, locator, summary, assessment, CHECKED, note,
        ])

    # 秋山皓太
    ev(1, "Person", "P000079", "name", "秋山 皓太", "B6W2S0002", "PDF 選手表 > No.28", "JBA公式氏名")
    ev(2, "Person", "P000079", "name_en", "Kota Akiyama", "B6W2S0003", "選手情報 > 英語表記", "B3公式表記")
    ev(3, "Person", "P000079", "birth_date", "1996-12-29", "B6W2S0002", "PDF 選手表 > No.28 > 生年月日", "JBA公式生年月日")
    ev(4, "Career", "C000278", "organization_id", "ORG000010", "B6W2S0002", "PDF 選手表 > No.28 > 所属", "福岡第一高校3年として掲載")
    ev(5, "Career", "C000278", "role", "Player", "B6W2S0002", "PDF 選手表 > No.28", "U18日本代表候補選手として掲載")
    ev(6, "Career", "C000278", "activity_date", "2014-06-04", "B6W2S0002", "PDF 注記 > 所属・年齢基準日", "高校所属確認日")
    ev(7, "Career", "C000279", "organization_id", "ORG000015", "B6W2S0003", "選手情報 > 出身校", "東海大学を掲載")
    ev(8, "Career", "C000279", "role", "Player", "B6W2S0003", "選手情報 > 出身校", "大学競技経歴としての表示", "PARTIAL", "大学公式ロスターの追加確認が必要")
    ev(9, "Career", "C000280", "organization_id", "ORG000115", "B6W2S0003", "選手情報 > 立川ダイス", "立川ダイス所属")
    ev(10, "Career", "C000280", "role", "Player", "B6W2S0003", "PLAYER STATS > 50試合", "公式戦出場を確認")
    ev(11, "Career", "C000280", "competition_participation", "B3公式戦50試合", "B6W2S0003", "PLAYER STATS", "B3公式戦成績")

    # 大城侑朔
    ev(12, "Person", "P000080", "name", "大城 侑朔", "B6W2S0005", "基本情報 > 選手名", "B.LEAGUE公式氏名")
    ev(13, "Person", "P000080", "name_en", "Yusaku Oshiro", "B6W2S0005", "基本情報 > 英語表記", "B.LEAGUE公式表記")
    ev(14, "Person", "P000080", "birth_date", "1995-03-01", "B6W2S0004", "PDF 選手表 > 大城侑朔 > 生年月日", "JBA公式生年月日")
    ev(15, "Career", "C000281", "organization_id", "ORG000010", "B6W2S0004", "PDF 選手表 > 大城侑朔 > 所属", "福岡第一高校2年として掲載")
    ev(16, "Career", "C000281", "role", "Player", "B6W2S0004", "PDF 選手表 > 大城侑朔", "U16日本代表候補選手として掲載")
    ev(17, "Career", "C000281", "activity_date", "2011-04-13", "B6W2S0004", "PDF 注記 > 所属・年齢基準日", "高校所属確認日")
    ev(18, "Career", "C000282", "organization_id", "ORG000020", "B6W2S0005", "基本情報 > 出身校", "日本体育大学を掲載")
    ev(19, "Career", "C000282", "role", "Player", "B6W2S0005", "基本情報 > 出身校", "大学競技経歴としての表示", "PARTIAL", "大学公式ロスターの追加確認が必要")
    ev(20, "Career", "C000283", "organization_id", "ORG000111", "B6W2S0005", "クラブ所属履歴 > 2017-18〜2025-26 八王子", "八王子所属を掲載")
    ev(21, "Career", "C000283", "role", "Player", "B6W2S0005", "2024-25 B3RS シーズン成績", "公式戦出場を確認")
    ev(22, "Career", "C000283", "start", "2017", "B6W2S0005", "クラブ所属履歴 > 2017-18 八王子", "所属開始年")
    ev(23, "Career", "C000283", "end", "2026", "B6W2S0005", "クラブ所属履歴 > 2025-26 八王子", "掲載経歴の終了年")
    ev(24, "Career", "C000283", "competition_participation", "2024-25 B3RS 49試合", "B6W2S0005", "シーズン成績 > 2024-25", "B3公式戦出場")

    # 土居光
    ev(25, "Person", "P000081", "name", "土居 光", "B6W2S0007", "基本情報 > 選手名", "B.LEAGUE公式氏名")
    ev(26, "Person", "P000081", "name_en", "Hikaru Doi", "B6W2S0007", "基本情報 > 英語表記", "B.LEAGUE公式表記")
    ev(27, "Person", "P000081", "birth_date", "1998-10-02", "B6W2S0007", "基本情報 > 生年月日", "B.LEAGUE公式生年月日")
    ev(28, "Career", "C000284", "organization_id", "ORG000010", "B6W2S0006", "日本体育大学ROSTER > No.24 > 出身校", "福岡第一高を掲載")
    ev(29, "Career", "C000284", "role", "Player", "B6W2S0011", "土居光の紹介 > 福岡第一", "福岡第一での選手経歴", "PARTIAL", "専門媒体による補助確認")
    ev(30, "Career", "C000285", "organization_id", "ORG000020", "B6W2S0006", "日本体育大学ROSTER > No.24", "日本体育大学所属")
    ev(31, "Career", "C000285", "role", "Player", "B6W2S0006", "ROSTER > No.24 > SF", "大学公式大会ロスター")
    ev(32, "Career", "C000285", "activity_year", "2019", "B6W2S0006", "第71回インカレROSTER > 3年", "2019年の競技登録")
    ev(33, "Career", "C000286", "organization_id", "ORG000046", "B6W2S0007", "クラブ所属履歴 > 2025-26 東京Z", "東京Z所属")
    ev(34, "Career", "C000286", "role", "Player", "B6W2S0007", "2025-26 B3RS シーズン成績", "公式戦出場を確認")
    ev(35, "Career", "C000286", "start", "2025", "B6W2S0007", "クラブ所属履歴 > 2025-26 東京Z", "所属開始年")
    ev(36, "Career", "C000286", "end", "2026", "B6W2S0007", "2025-26シーズン終了時", "掲載経歴の終了年")
    ev(37, "Career", "C000286", "competition_participation", "2025-26 B3RS 23試合", "B6W2S0007", "シーズン成績 > 2025-26", "B3公式戦出場")

    # 松本礼太
    ev(38, "Person", "P000082", "name", "松本 礼太", "B6W2S0008", "基本情報 > 選手名", "B.LEAGUE公式氏名")
    ev(39, "Person", "P000082", "name_en", "Reita Matsumoto", "B6W2S0008", "基本情報 > 英語表記", "B.LEAGUE公式表記")
    ev(40, "Person", "P000082", "birth_date", "1999-09-18", "B6W2S0008", "基本情報 > 生年月日", "B.LEAGUE公式生年月日")
    ev(41, "Career", "C000287", "organization_id", "ORG000010", "B6W2S0001", "学校案内 > Bリーグ所属卒業生 > 松本礼太", "福岡第一高校卒業生として掲載")
    ev(42, "Career", "C000287", "role", "Player", "B6W2S0011", "松本礼太の紹介 > 福岡第一", "福岡第一での選手経歴", "PARTIAL", "専門媒体による補助確認")
    ev(45, "Career", "C000288", "organization_id", "ORG000015", "B6W2S0008", "基本情報 > 出身校", "東海大学を掲載")
    ev(46, "Career", "C000288", "role", "Player", "B6W2S0008", "基本情報 > 出身校", "大学競技経歴としての表示", "PARTIAL", "大学公式ロスターの追加確認が必要")
    ev(47, "Career", "C000289", "organization_id", "ORG000116", "B6W2S0009", "クラブ所属履歴 > 2025-26 徳島", "徳島所属")
    ev(48, "Career", "C000289", "role", "Player", "B6W2S0010", "徳島ガンバロウズ > No.12", "公式戦出場を確認")
    ev(49, "Career", "C000289", "start", "2025", "B6W2S0009", "クラブ所属履歴 > 2025-26 徳島", "所属開始年")
    ev(50, "Career", "C000289", "end", "2026", "B6W2S0009", "2025-26シーズン終了時", "掲載経歴の終了年")
    ev(51, "Career", "C000289", "competition_participation", "2025-26 B3公式戦30試合", "B6W2S0010", "チーム成績 > No.12 松本礼太", "B3公式戦出場")

    for number, org_id, value, source, locator in [
        (52, "ORG000010", "福岡第一高等学校", "B6W2S0001", "学校案内表紙・発行元"),
        (53, "ORG000015", "東海大学", "B6W2S0008", "基本情報 > 出身校"),
        (54, "ORG000020", "日本体育大学", "B6W2S0006", "出場校 > 日本体育大学"),
        (55, "ORG000046", "アースフレンズ東京Z", "B6W2S0007", "クラブ所属履歴 > 東京Z"),
        (56, "ORG000111", "東京八王子ビートレインズ", "B6W2S0005", "クラブ所属履歴 > 八王子"),
        (57, "ORG000115", "立川ダイス", "B6W2S0003", "選手情報 > 所属クラブ"),
        (58, "ORG000116", "徳島ガンバロウズ", "B6W2S0010", "チーム名"),
    ]:
        ev(number, "Organization", org_id, "name", value, source, locator, "公式資料内の組織表記")

    ev(59, "Career", "C000279", "role", "Player", "B6W2S0012", "東海大学ROSTER > No.37 秋山皓太", "大学公式大会ロスター")
    ev(60, "Career", "C000279", "activity_year", "2018", "B6W2S0012", "ROSTER > 4年・大会年2018", "2018年の競技登録")
    ev(61, "Career", "C000282", "role", "Player", "B6W2S0013", "日本体育大学ROSTER > No.14 大城侑朔", "大学公式大会ロスター")
    ev(62, "Career", "C000282", "activity_year", "2015", "B6W2S0013", "ROSTER > 3年・大会年2015", "2015年の競技登録")
    ev(63, "Career", "C000288", "role", "Player", "B6W2S0014", "東海大学ROSTER > No.31 松本礼太", "大学公式大会ロスター")
    ev(64, "Career", "C000288", "activity_year", "2021", "B6W2S0014", "ROSTER > 4年・大会年2021", "2021年の競技登録")

    write("evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write("issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], [
        ["B6W2I0001", "P000079", "C000278", "HIGH_SCHOOL_PERIOD", "HOLD", "2014年6月時点の福岡第一高校3年を確認したが入学・卒業年月は未確認", "公式大会名簿または学校資料で期間を確認"],
        ["B6W2I0002", "P000079", "C000279", "UNIVERSITY_PERIOD", "HOLD", "2018年の東海大学4年・公式戦登録を確認したが入学・卒業年月は未確認", "年度別JUBFロスターまたは大学公式資料で期間を確認"],
        ["B6W2I0003", "P000079", "C000280", "PRO_PERIOD", "HOLD", "立川でのB3公式戦出場は確認したがCareer開始年・終了年は未確認", "年度別公式成績と移籍・退団発表を確認"],
        ["B6W2I0004", "P000080", "C000281", "HIGH_SCHOOL_PERIOD", "HOLD", "2011年4月時点の福岡第一高校2年を確認したが入学・卒業年月は未確認", "公式大会名簿または学校資料で期間を確認"],
        ["B6W2I0005", "P000080", "C000282", "UNIVERSITY_PERIOD", "HOLD", "2015年の日本体育大学3年・公式戦登録を確認したが入学・卒業年月は未確認", "年度別JUBFロスターまたは大学公式資料で期間を確認"],
        ["B6W2I0006", "P000081", "C000284", "HIGH_SCHOOL_PERIOD", "HOLD", "JUBFの出身校欄で福岡第一を確認したが高校の在籍期間は未確認", "高校公式大会名簿を確認"],
        ["B6W2I0007", "P000081", "C000285", "UNIVERSITY_PERIOD", "HOLD", "2019年の日本体育大学3年を確認したが入学・卒業年月は未確認", "年度別JUBFロスターを追加確認"],
        ["B6W2I0008", "P000082", "C000287", "HIGH_SCHOOL_PERIOD", "HOLD", "学校公式で卒業生関係を確認したが高校在籍期間は未確認", "大会公式ロスターで期間を裏付け"],
        ["B6W2I0009", "P000082", "C000288", "UNIVERSITY_PERIOD", "HOLD", "2021年の東海大学4年・公式戦登録を確認したが入学・卒業年月は未確認", "年度別JUBFロスターまたは大学公式資料で期間を確認"],
        ["B6W2I0010", "P000082", "C000289", "CURRENT_STATUS", "HOLD", "2025-26徳島での出場は確認したが2026-27の契約・所属は未確認", "クラブ公式の次季契約情報を確認"],
    ])
    write("qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"], [
        ["B6W2D0001", "Person", "P000079", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "JBA・B3公式資料で確認", CHECKED],
        ["B6W2D0002", "Career", "C000278", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|activity_date", "start|end", "JBA公式メンバー表で確認", CHECKED],
        ["B6W2D0003", "Career", "C000279", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|activity_year", "start|end", "JUBF公式ロスターで確認", CHECKED],
        ["B6W2D0004", "Career", "C000280", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|competition_participation", "start|end", "B3公式プロフィールと成績で確認。期間は別確認が必要", CHECKED],
        ["B6W2D0005", "Person", "P000080", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "JBA・B.LEAGUE公式資料で確認", CHECKED],
        ["B6W2D0006", "Career", "C000281", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|activity_date", "start|end", "JBA公式メンバー表で確認", CHECKED],
        ["B6W2D0007", "Career", "C000282", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|activity_year", "start|end", "JUBF公式ロスターで確認", CHECKED],
        ["B6W2D0008", "Career", "C000283", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end|competition_participation", "", "B.LEAGUE公式所属履歴と成績で確認", CHECKED],
        ["B6W2D0009", "Person", "P000081", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "B.LEAGUE公式資料で確認", CHECKED],
        ["B6W2D0010", "Career", "C000284", "READY_FOR_VERIFIED_REVIEW", "organization_id", "role|start|end", "JUBF公式の出身校欄で確認。役割は専門媒体による補助", CHECKED],
        ["B6W2D0011", "Career", "C000285", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|activity_year", "start|end", "JUBF公式ロスターで確認", CHECKED],
        ["B6W2D0012", "Career", "C000286", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end|competition_participation", "", "B.LEAGUE公式所属履歴と成績で確認", CHECKED],
        ["B6W2D0013", "Person", "P000082", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "B.LEAGUE公式資料で確認", CHECKED],
        ["B6W2D0014", "Career", "C000287", "READY_FOR_VERIFIED_REVIEW", "organization_id", "role|start|end", "学校公式で卒業生関係を確認。期間と役割は専門媒体のみ", CHECKED],
        ["B6W2D0015", "Career", "C000288", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|activity_year", "start|end", "JUBF公式ロスターで確認", CHECKED],
        ["B6W2D0016", "Career", "C000289", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end|competition_participation", "current_status", "B.LEAGUE・B3公式で所属と出場を確認", CHECKED],
    ] + [
        [f"B6W2D{number:04d}", "Organization", org_id, "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料内表記を確認", CHECKED]
        for number, org_id in enumerate([
            "ORG000010", "ORG000015", "ORG000020", "ORG000046", "ORG000111", "ORG000115", "ORG000116",
        ], start=17)
    ])


if __name__ == "__main__":
    main()
