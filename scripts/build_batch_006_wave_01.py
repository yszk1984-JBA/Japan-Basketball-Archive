#!/usr/bin/env python3
"""Build Batch 006 Wave 1 candidates without touching VERIFIED or MASTER."""

from __future__ import annotations

import csv
from pathlib import Path


OUT = Path("data/candidate/batch_006/wave_01")
CHECKED = "2026-09-21"


def write(name: str, headers: list[str], rows: list[list[str]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def main() -> None:
    write("person_candidates.csv", ["person_id", "name"], [
        ["P000075", "井手 優希"],
        ["P000076", "クベマ スティーブ"],
        ["P000012", "ジャン・ローレンス・ハーパージュニア"],
        ["P000078", "長島 エマニエル"],
    ])
    write("organization_candidates.csv", ["organization_id", "name"], [
        ["ORG000010", "福岡第一高等学校"],
        ["ORG000015", "東海大学"],
        ["ORG000018", "専修大学"],
        ["ORG000020", "日本体育大学"],
        ["ORG000040", "ライジングゼファー福岡"],
        ["ORG000100", "山口パッツファイブ"],
        ["ORG000111", "東京八王子ビートレインズ"],
        ["ORG000114", "東京サンロッカーズ"],
    ])
    write("career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], [
        ["C000267", "P000075", "ORG000010", "Player", "", ""],
        ["C000268", "P000075", "ORG000020", "Player", "", ""],
        ["C000269", "P000075", "ORG000100", "Player", "2025", ""],
        ["C000270", "P000076", "ORG000010", "Player", "", ""],
        ["C000271", "P000076", "ORG000018", "Player", "", ""],
        ["C000272", "P000076", "ORG000111", "Player", "2024", ""],
        ["C000273", "P000012", "ORG000010", "Player", "", ""],
        ["C000274", "P000012", "ORG000015", "Player", "", ""],
        ["C000275", "P000012", "ORG000114", "Player", "2023", ""],
        ["C000276", "P000078", "ORG000010", "Player", "", ""],
        ["C000277", "P000078", "ORG000040", "Player", "2016", "2018"],
    ])
    write("source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], [
        ["B6W1S0001", "第23回FIBA ASIA U-18男子日本代表 メンバー表", "日本バスケットボール協会", "https://www.japanbasketball.jp/wp/wp-content/uploads/H26_U18men_member_0811.pdf", CHECKED],
        ["B6W1S0002", "井手優希 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=36865", CHECKED],
        ["B6W1S0003", "クベマスティーブ B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=41165", CHECKED],
        ["B6W1S0004", "スティーブ・クベマ・ジョセフ選手契約合意（継続）", "東京八王子ビートレインズ", "https://trains.co.jp/news/detail/id=18901", CHECKED],
        ["B6W1S0005", "第96回天皇杯 福岡第一高校チームページ", "日本バスケットボール協会", "https://zennihon2020-21.japanbasketball.jp/team/1st/men-fukuoka", CHECKED],
        ["B6W1S0006", "ジャン・ローレンス・ハーパージュニア B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=5100000034", CHECKED],
        ["B6W1S0007", "ジャン・ローレンス・ハーパージュニア選手 契約締結", "東京サンロッカーズ", "https://www.sunrockers.jp/news/detail/id=22691", CHECKED],
        ["B6W1S0008", "長島エマニエル B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=9309", CHECKED],
        ["B6W1S0009", "ウインターカップ2010 男子決勝 福岡第一", "日本バスケットボール協会", "https://japanbasketball.jp/wintercup/2010/pbp_team-php-game_id=10050.html", CHECKED],
    ])

    evidence: list[list[str]] = []

    def ev(number: int, entity_type: str, entity_id: str, field: str, value: str,
           source: str, locator: str, summary: str,
           assessment: str = "SUPPORTED", note: str = "") -> None:
        evidence.append([
            f"B6W1E{number:04d}", entity_type, entity_id, field, value,
            source, locator, summary, assessment, CHECKED, note,
        ])

    # 井手優希
    ev(1, "Person", "P000075", "name", "井手 優希", "B6W1S0001", "PDF 選手表 > No.10", "JBA公式表の氏名")
    ev(2, "Person", "P000075", "name_en", "Yuki Ide", "B6W1S0002", "基本情報 > 英語表記", "B.LEAGUE公式表記")
    ev(3, "Person", "P000075", "birth_date", "1996-05-26", "B6W1S0001", "PDF 選手表 > 生年月日", "JBA公式表の生年月日")
    ev(4, "Career", "C000267", "organization_id", "ORG000010", "B6W1S0001", "PDF 選手表 > 所属", "福岡第一高校3年として掲載")
    ev(5, "Career", "C000267", "role", "Player", "B6W1S0001", "PDF 選手表 > No.10", "U18日本代表選手として掲載")
    ev(6, "Career", "C000267", "activity_date", "2014-08-11", "B6W1S0001", "PDF 注記 > 所属基準日", "高校所属確認日")
    ev(7, "Career", "C000268", "organization_id", "ORG000020", "B6W1S0002", "基本情報 > 出身校", "日本体育大学を掲載")
    ev(8, "Career", "C000268", "role", "Player", "B6W1S0002", "選手プロフィール", "競技経歴上の出身校", "PARTIAL", "大学公式ロスターの追加確認が必要")
    ev(9, "Career", "C000269", "organization_id", "ORG000100", "B6W1S0002", "クラブ所属履歴 > 2025-26 山口", "山口所属を掲載")
    ev(10, "Career", "C000269", "role", "Player", "B6W1S0002", "2025-26 B3RS シーズン成績", "公式戦出場を確認")
    ev(11, "Career", "C000269", "competition_participation", "2025-26 B3RS 51試合", "B6W1S0002", "2025-26シーズン成績", "B3公式戦出場")

    # クベマ スティーブ
    ev(12, "Person", "P000076", "name", "クベマ スティーブ", "B6W1S0003", "基本情報 > 選手名", "B.LEAGUE公式表記")
    ev(13, "Person", "P000076", "name_en", "Steve Kubema", "B6W1S0003", "基本情報 > 英語表記", "B.LEAGUE公式表記")
    ev(14, "Person", "P000076", "birth_date", "2001-08-18", "B6W1S0003", "基本情報 > 生年月日", "B.LEAGUE公式表記")
    ev(15, "Career", "C000270", "organization_id", "ORG000010", "B6W1S0003", "QA > 出身校（高）", "福岡第一高等学校を掲載")
    ev(16, "Career", "C000270", "role", "Player", "B6W1S0003", "選手プロフィール > 出身校（高）", "高校競技経歴の表示", "PARTIAL", "大会公式ロスターでの追加確認が望ましい")
    ev(17, "Career", "C000271", "organization_id", "ORG000018", "B6W1S0003", "基本情報・QA > 出身校（大）", "専修大学を掲載")
    ev(18, "Career", "C000271", "role", "Player", "B6W1S0003", "選手プロフィール > 出身校（大）", "大学競技経歴の表示", "PARTIAL", "大学公式ロスターの追加確認が必要")
    ev(19, "Career", "C000272", "organization_id", "ORG000111", "B6W1S0003", "クラブ所属履歴 > 2024-25以降 八王子", "八王子所属を掲載")
    ev(20, "Career", "C000272", "role", "Player", "B6W1S0003", "2025-26 B3RS シーズン成績", "公式戦出場を確認")
    ev(21, "Career", "C000272", "start", "2024", "B6W1S0003", "クラブ所属履歴 > 2024-25 八王子", "所属開始年")
    ev(22, "Career", "C000272", "competition_participation", "2025-26 B3RS 41試合", "B6W1S0003", "2025-26シーズン成績", "B3公式戦出場")
    ev(23, "Career", "C000272", "contract_season", "2026-27", "B6W1S0004", "契約合意本文", "継続契約を発表")

    # ジャン・ローレンス・ハーパージュニア
    ev(24, "Person", "P000012", "name", "ジャン・ローレンス・ハーパージュニア", "B6W1S0006", "基本情報 > 選手名", "B.LEAGUE公式の現行氏名")
    ev(25, "Person", "P000012", "name_en", "John Lawrence Harper Jr.", "B6W1S0006", "基本情報 > 英語表記", "B.LEAGUE公式表記")
    ev(26, "Person", "P000012", "birth_date", "2003-02-09", "B6W1S0006", "基本情報 > 生年月日", "B.LEAGUE公式表記")
    ev(27, "Career", "C000273", "organization_id", "ORG000010", "B6W1S0005", "プレイヤー表 > No.31", "福岡第一高校ロスターに掲載")
    ev(28, "Career", "C000273", "role", "Player", "B6W1S0005", "プレイヤー表 > No.31", "大会公式選手ロスター")
    ev(29, "Career", "C000273", "activity_year", "2020", "B6W1S0005", "第96回天皇杯チームページ", "大会時点の高校所属")
    ev(30, "Career", "C000274", "organization_id", "ORG000015", "B6W1S0006", "基本情報 > 出身校", "東海大学を掲載")
    ev(31, "Career", "C000274", "role", "Player", "B6W1S0007", "契約発表本文 > 東海大学在学中", "大学在学中の特別指定経歴")
    ev(32, "Career", "C000275", "organization_id", "ORG000114", "B6W1S0007", "経歴 > 2023-24以降", "SR渋谷／東京SR所属")
    ev(33, "Career", "C000275", "role", "Player", "B6W1S0006", "2025-26 B1シーズン成績", "B1公式戦出場")
    ev(34, "Career", "C000275", "start", "2023", "B6W1S0006", "クラブ所属履歴 > 2023-24 SR渋谷", "所属開始年")
    ev(35, "Career", "C000275", "competition_participation", "2025-26 B1 57試合", "B6W1S0006", "2025-26シーズン成績", "B1公式戦出場")
    ev(36, "Career", "C000275", "award", "2025-26 最優秀新人賞", "B6W1S0006", "受賞歴", "B.LEAGUE公式受賞歴")
    ev(37, "Career", "C000275", "contract_season", "2026-27", "B6W1S0007", "契約締結本文", "継続契約を発表")

    # 長島エマニエル
    ev(38, "Person", "P000078", "name", "長島 エマニエル", "B6W1S0008", "基本情報 > 選手名", "B.LEAGUE公式表記")
    ev(39, "Person", "P000078", "name_en", "Emanieru Nagashima", "B6W1S0008", "基本情報 > 英語表記", "B.LEAGUE公式表記")
    ev(40, "Person", "P000078", "birth_date", "1992-07-01", "B6W1S0008", "基本情報 > 生年月日", "B.LEAGUE公式表記")
    ev(41, "Career", "C000276", "organization_id", "ORG000010", "B6W1S0009", "男子決勝 > 福岡第一 > No.7", "福岡第一の試合記録に掲載")
    ev(42, "Career", "C000276", "role", "Player", "B6W1S0009", "男子決勝ボックススコア", "公式戦出場を確認")
    ev(43, "Career", "C000276", "activity_year", "2010", "B6W1S0009", "ウインターカップ2010男子決勝", "高校活動年")
    ev(44, "Career", "C000277", "organization_id", "ORG000040", "B6W1S0008", "クラブ所属履歴 > 2016-17・2017-18 福岡", "福岡所属を掲載")
    ev(45, "Career", "C000277", "role", "Player", "B6W1S0008", "B.LEAGUE選手プロフィール", "B.LEAGUE選手として掲載")
    ev(46, "Career", "C000277", "start", "2016", "B6W1S0008", "クラブ所属履歴 > 2016-17 福岡", "所属開始年")
    ev(47, "Career", "C000277", "end", "2018", "B6W1S0008", "2017-18シーズン終了時", "掲載経歴の終了年")

    for number, org_id, value, source, locator in [
        (48, "ORG000010", "福岡第一高等学校", "B6W1S0005", "チーム名"),
        (49, "ORG000015", "東海大学", "B6W1S0007", "選手プロフィール > 出身校"),
        (50, "ORG000018", "専修大学", "B6W1S0003", "基本情報 > 出身校"),
        (51, "ORG000020", "日本体育大学", "B6W1S0002", "基本情報 > 出身校"),
        (52, "ORG000040", "ライジングゼファー福岡", "B6W1S0008", "クラブ所属履歴 > 福岡"),
        (53, "ORG000100", "山口パッツファイブ", "B6W1S0002", "クラブ所属履歴 > 山口"),
        (54, "ORG000111", "東京八王子ビートレインズ", "B6W1S0004", "発行元・契約本文"),
        (55, "ORG000114", "東京サンロッカーズ", "B6W1S0007", "発行元・契約本文"),
    ]:
        ev(number, "Organization", org_id, "name", value, source, locator, "公式資料内の組織表記")

    ev(56, "Career", "C000269", "start", "2025", "B6W1S0002", "クラブ所属履歴 > 2025-26 山口", "所属開始年")

    write("evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)
    write("issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], [
        ["B6W1I0001", "P000075", "C000267", "HIGH_SCHOOL_PERIOD", "HOLD", "2014年8月時点の福岡第一高校3年を確認したが入学・卒業年月は未確認", "期間を直接示す公式資料がある場合のみ更新"],
        ["B6W1I0002", "P000075", "C000268", "UNIVERSITY_PERIOD", "HOLD", "日本体育大学はB.LEAGUE出身校表示のみで競技登録期間は未確認", "大学・JUBF公式ロスターを確認"],
        ["B6W1I0003", "P000075", "C000269", "PRO_HISTORY_GAPS", "HOLD", "最小経路として現在の山口を候補化し、横浜EX・岩手等の過去Careerは未作成", "後続Waveでクラブ別Careerを追加"],
        ["B6W1I0004", "P000076", "P000076", "NAME_VARIATION", "HOLD", "B.LEAGUEはクベマ スティーブ、クラブはスティーブ・クベマ・ジョセフと表記", "正式名と登録名を別項目で保持する将来設計を検討"],
        ["B6W1I0005", "P000076", "C000270|C000271", "EDUCATION_PERIOD", "HOLD", "高校・大学の開始年と終了年は未確認", "大会・大学連盟の公式ロスターを確認"],
        ["B6W1I0006", "P000076", "C000272", "PRO_HISTORY_GAPS", "HOLD", "八王子以前の静岡・品川Careerは今回の最小経路に未収録", "後続Waveでクラブ別Careerを追加"],
        ["B6W1I0007", "P000012", "P000012", "NAME_VARIATION", "HOLD", "高校資料とB.LEAGUEで氏名の空白・中黒・順序に表記差がある", "原文表記をSourceごとに保持"],
        ["B6W1I0008", "P000012", "C000273|C000274", "EDUCATION_PERIOD", "HOLD", "高校・大学の開始年と終了年は未確認", "期間を直接示す公式資料がある場合のみ更新"],
        ["B6W1I0009", "P000012", "C000275", "PRO_HISTORY_GAPS", "HOLD", "最小経路として東京SRを候補化し、琉球・群馬の個別Careerは未作成", "後続Waveで特別指定Careerを追加"],
        ["B6W1I0010", "P000078", "P000078", "POST_HIGH_SCHOOL_GAP", "HOLD", "高校と2016-18福岡の間の大学・所属は未確認", "本人・クラブ・大学の公式経歴を確認"],
    ])
    write("qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"], [
        ["B6W1D0001", "Person", "P000075", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "JBA・B.LEAGUE公式資料で確認", CHECKED],
        ["B6W1D0002", "Career", "C000267", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|activity_date", "start|end", "JBA公式U18メンバー表で確認", CHECKED],
        ["B6W1D0003", "Career", "C000268", "HOLD_CANDIDATE", "organization_id", "role|start|end", "B.LEAGUE出身校表示のみ", CHECKED],
        ["B6W1D0004", "Career", "C000269", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|competition_participation", "end", "B.LEAGUE公式所属履歴と公式戦成績で確認", CHECKED],
        ["B6W1D0005", "Person", "P000076", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "B.LEAGUE公式資料で確認", CHECKED],
        ["B6W1D0006", "Career", "C000270", "READY_FOR_VERIFIED_REVIEW", "organization_id", "role|start|end", "B.LEAGUE公式の高校欄で確認", CHECKED],
        ["B6W1D0007", "Career", "C000271", "HOLD_CANDIDATE", "organization_id", "role|start|end", "B.LEAGUE出身校表示のみ", CHECKED],
        ["B6W1D0008", "Career", "C000272", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|competition_participation|contract_season", "end", "B.LEAGUEとクラブ公式で確認", CHECKED],
        ["B6W1D0009", "Person", "P000012", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "B.LEAGUE公式資料で確認。Pilot Batch 001の既存Person IDを継続", CHECKED],
        ["B6W1D0010", "Career", "C000273", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|activity_year", "start|end", "JBA公式大会ロスターで確認", CHECKED],
        ["B6W1D0011", "Career", "C000274", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "B.LEAGUE・クラブ公式で確認", CHECKED],
        ["B6W1D0012", "Career", "C000275", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|competition_participation|award|contract_season", "end", "B.LEAGUEとクラブ公式で確認", CHECKED],
        ["B6W1D0013", "Person", "P000078", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "B.LEAGUE公式資料で確認", CHECKED],
        ["B6W1D0014", "Career", "C000276", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|activity_year", "start|end", "JBA公式大会記録で確認", CHECKED],
        ["B6W1D0015", "Career", "C000277", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|end", "", "B.LEAGUE公式所属履歴で確認", CHECKED],
        ["B6W1D0016", "Organization", "ORG000010", "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料内表記を確認", CHECKED],
        ["B6W1D0017", "Organization", "ORG000015", "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料内表記を確認", CHECKED],
        ["B6W1D0018", "Organization", "ORG000018", "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料内表記を確認", CHECKED],
        ["B6W1D0019", "Organization", "ORG000020", "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料内表記を確認", CHECKED],
        ["B6W1D0020", "Organization", "ORG000040", "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料内表記を確認", CHECKED],
        ["B6W1D0021", "Organization", "ORG000100", "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料内表記を確認", CHECKED],
        ["B6W1D0022", "Organization", "ORG000111", "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料内表記を確認", CHECKED],
        ["B6W1D0023", "Organization", "ORG000114", "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料内表記を確認", CHECKED],
    ])


if __name__ == "__main__":
    main()
