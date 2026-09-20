#!/usr/bin/env python3
"""Build Batch 004 Wave 1 candidate files.

This creates CANDIDATE and QA inputs only. It never writes VERIFIED or MASTER.
"""

from __future__ import annotations

import csv
from pathlib import Path


OUT = Path("data/candidate/batch_004/wave_01")
CHECKED = "2026-09-20"


def write(name: str, headers: list[str], rows: list[list[str]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def main() -> None:
    write(
        "person_candidates.csv",
        ["person_id", "name"],
        [
            ["P000064", "河村 勇輝"],
            ["P000065", "児玉 ジュニア"],
        ],
    )

    write(
        "organization_candidates.csv",
        ["organization_id", "name"],
        [
            ["ORG000010", "福岡第一高等学校"],
            ["ORG000015", "東海大学"],
            ["ORG000055", "横浜ビー・コルセアーズ"],
            ["ORG000017", "日本経済大学"],
            ["ORG000097", "三遠ネオフェニックス"],
            ["ORG000098", "メンフィス・グリズリーズ"],
        ],
    )

    write(
        "career_candidates.csv",
        ["career_id", "person_id", "organization_id", "role", "start", "end"],
        [
            ["C000219", "P000064", "ORG000010", "Player", "", ""],
            ["C000220", "P000064", "ORG000015", "Player", "", ""],
            ["C000221", "P000064", "ORG000097", "Player", "", ""],
            ["C000222", "P000064", "ORG000055", "Player", "", ""],
            ["C000223", "P000064", "ORG000098", "Player", "2024", ""],
            ["C000224", "P000065", "ORG000010", "Player", "", ""],
            ["C000225", "P000065", "ORG000017", "Player", "", ""],
            ["C000226", "P000065", "ORG000097", "Player", "2025", ""],
        ],
    )

    write(
        "source_references.csv",
        ["source_id", "title", "publisher", "url", "accessed_at"],
        [
            ["B4W1S0001", "平成29年度 バスケットボール男子U16日本代表チーム メンバー表", "日本バスケットボール協会", "https://www.japanbasketball.jp/wp-content/uploads/U16men-member_20180330.pdf", CHECKED],
            ["B4W1S0002", "2020年度男子日本代表Bチーム メンバー", "日本バスケットボール協会", "https://www.japanbasketball.jp/wp-content/uploads/National-B-Team_Men_member_20200806.pdf", CHECKED],
            ["B4W1S0003", "河村勇輝 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=30460", CHECKED],
            ["B4W1S0004", "Grizzlies promote Yuki Kawamura to two-way contract", "Memphis Grizzlies", "https://www.nba.com/grizzlies/news/grizzlies-promote-yuki-kawamura-to-two-way-contract", CHECKED],
            ["B4W1S0005", "LA Clippers Yuki Kawamura player page", "LA Clippers / NBA", "https://www.nba.com/clippers/player/1642530/yuki-kawamura", CHECKED],
            ["B4W1S0006", "NBA G League Yuki Kawamura player page", "NBA G League", "https://gleague.nba.com/player/1642530", CHECKED],
            ["B4W1S0007", "日本経済大学 2024新人戦ロスター", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/180/type/rookie/y/2024/s/men", CHECKED],
            ["B4W1S0008", "WUBS 2025 日本学生選抜メンバー", "全日本大学バスケットボール連盟", "https://jubf.jp/index/show-pdf/url/aHR0cHM6Ly9kMmEwdjF4N3F2eGw2Yy5jbG91ZGZyb250Lm5ldC9maWxlcy9zcG9ocF9qdWJmL25ld3MvNjg5MmMzMGU0Y2U3ZS5wZGY%3D", CHECKED],
            ["B4W1S0009", "児玉 ジュニア選手 契約締結（新規）のお知らせ", "三遠ネオフェニックス", "https://www.neophoenix.jp/news/detail/id=21966", CHECKED],
            ["B4W1S0010", "児玉ジュニア B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=51000552", CHECKED],
            ["B4W1S0011", "児玉 ジュニア選手 契約締結（継続）のお知らせ", "三遠ネオフェニックス", "https://www.neophoenix.jp/news/detail/id=24999", CHECKED],
            ["B4W1S0012", "B.LEAGUE 大阪対三遠 2025年10月5日", "B.LEAGUE", "https://www.bleague.jp/game_detail/?ScheduleKey=504749&TAB=B", CHECKED],
        ],
    )

    evidence = [
        ["B4W1E0001", "Person", "P000064", "name", "河村 勇輝", "B4W1S0001", "PDF 1ページ > 河村勇輝欄", "JBA公式メンバー表の氏名", "SUPPORTED", CHECKED, ""],
        ["B4W1E0002", "Person", "P000064", "name_en", "Yuki Kawamura", "B4W1S0001", "PDF 1ページ > KAWAMURA Yuki", "JBA公式メンバー表の英語表記", "SUPPORTED", CHECKED, ""],
        ["B4W1E0003", "Person", "P000064", "birth_date", "2001-05-02", "B4W1S0001", "PDF 1ページ > 生年月日", "生年月日を掲載", "SUPPORTED", CHECKED, ""],
        ["B4W1E0004", "Career", "C000219", "organization_id", "ORG000010", "B4W1S0001", "PDF 1ページ > 所属欄", "福岡第一高等学校1年として掲載", "SUPPORTED", CHECKED, "開始・終了年月は不明"],
        ["B4W1E0005", "Career", "C000219", "role", "Player", "B4W1S0001", "PDF 1ページ > 選手一覧", "男子U16日本代表選手として掲載", "SUPPORTED", CHECKED, ""],
        ["B4W1E0006", "Career", "C000219", "grade", "1年", "B4W1S0001", "PDF 1ページ > 学年欄", "2018年3月時点の学年", "SUPPORTED", CHECKED, ""],
        ["B4W1E0007", "Career", "C000219", "activity_date", "2018-03-30", "B4W1S0001", "PDF 1ページ > 発表日と選手欄", "同校所属を確認した日付", "SUPPORTED", CHECKED, ""],
        ["B4W1E0008", "Career", "C000220", "organization_id", "ORG000015", "B4W1S0002", "PDF 選手一覧 > 河村勇輝欄", "東海大学1年として掲載", "SUPPORTED", CHECKED, "開始・終了年月は不明"],
        ["B4W1E0009", "Career", "C000220", "role", "Player", "B4W1S0002", "PDF 選手一覧", "男子日本代表Bチーム選手として掲載", "SUPPORTED", CHECKED, ""],
        ["B4W1E0010", "Career", "C000220", "grade", "1年", "B4W1S0002", "PDF 選手一覧 > 学年欄", "2020年8月時点の学年", "SUPPORTED", CHECKED, ""],
        ["B4W1E0011", "Career", "C000220", "activity_date", "2020-08-06", "B4W1S0002", "PDF 発表日と選手欄", "東海大学所属を確認した日付", "SUPPORTED", CHECKED, ""],
        ["B4W1E0012", "Career", "C000221", "organization_id", "ORG000097", "B4W1S0003", "クラブ所属履歴 > 2019-20 三遠", "B.LEAGUE公式の所属履歴", "SUPPORTED", CHECKED, ""],
        ["B4W1E0013", "Career", "C000221", "role", "Player", "B4W1S0003", "選手プロフィール > クラブ所属履歴", "B.LEAGUE選手として掲載", "SUPPORTED", CHECKED, ""],
        ["B4W1E0014", "Career", "C000221", "season", "2019-20", "B4W1S0003", "クラブ所属履歴", "三遠所属シーズン", "SUPPORTED", CHECKED, "暦年の開始・終了日は不明"],
        ["B4W1E0015", "Career", "C000222", "organization_id", "ORG000055", "B4W1S0003", "クラブ所属履歴 > 横浜BC", "2020-21から2023-24の所属履歴", "SUPPORTED", CHECKED, ""],
        ["B4W1E0016", "Career", "C000222", "role", "Player", "B4W1S0003", "選手プロフィール > クラブ所属履歴", "B.LEAGUE選手として掲載", "SUPPORTED", CHECKED, ""],
        ["B4W1E0017", "Career", "C000222", "seasons", "2020-21|2021-22|2022-23|2023-24", "B4W1S0003", "クラブ所属履歴", "横浜BC所属シーズン", "SUPPORTED", CHECKED, "暦年の開始・終了日は不明"],
        ["B4W1E0018", "Career", "C000222", "competition_participation", "2023-24 B1 56試合", "B4W1S0003", "2023-24 B1 シーズン成績", "56試合・56先発を掲載", "SUPPORTED", CHECKED, ""],
        ["B4W1E0019", "Career", "C000223", "organization_id", "ORG000098", "B4W1S0004", "公式発表本文", "Memphis GrizzliesがTwo-Way契約への昇格を発表", "SUPPORTED", CHECKED, "終了時期は不明"],
        ["B4W1E0020", "Career", "C000223", "role", "Player", "B4W1S0004", "公式発表本文 > guard Yuki Kawamura", "選手契約の対象として掲載", "SUPPORTED", CHECKED, ""],
        ["B4W1E0021", "Career", "C000223", "contract_type", "Two-Way contract", "B4W1S0004", "公式発表本文", "Two-Way契約への昇格", "SUPPORTED", CHECKED, ""],
        ["B4W1E0022", "Career", "C000223", "contract_announcement_date", "2024-10-19", "B4W1S0004", "公式発表の公開日時", "契約発表日", "SUPPORTED", CHECKED, ""],
        ["B4W1E0023", "Person", "P000064", "current_affiliation", "LA Clippers", "B4W1S0005", "選手ページ見出し", "Clippers選手ページに掲載", "CONFLICT", CHECKED, "Clippers現行ロスターとNBA G Leagueページの所属表示を含め更新時点が一致しない"],
        ["B4W1E0024", "Person", "P000064", "current_affiliation", "Windy City Bulls", "B4W1S0006", "選手ページ見出し", "NBA G Leagueページの所属表示", "CONFLICT", CHECKED, "Clippers選手ページとの更新時点が一致しない"],
        ["B4W1E0025", "Person", "P000065", "name", "児玉 ジュニア", "B4W1S0008", "PDF 日本学生選抜 > 児玉ジュニア欄", "JUBF公式資料の氏名", "SUPPORTED", CHECKED, ""],
        ["B4W1E0026", "Person", "P000065", "name_en", "Junior Kodama", "B4W1S0008", "PDF 日本学生選抜 > KODAMA Junior", "JUBF公式資料の英語表記", "SUPPORTED", CHECKED, ""],
        ["B4W1E0027", "Person", "P000065", "birth_date", "2006-03-15", "B4W1S0008", "PDF 日本学生選抜 > 生年月日", "生年月日を掲載", "SUPPORTED", CHECKED, ""],
        ["B4W1E0028", "Career", "C000224", "organization_id", "ORG000010", "B4W1S0009", "選手プロフィール > 出身校・受賞歴", "福岡第一高等学校とWC2023優勝を掲載", "SUPPORTED", CHECKED, "開始・終了年月は不明"],
        ["B4W1E0029", "Career", "C000224", "role", "Player", "B4W1S0009", "選手プロフィール > WC2023優勝", "選手プロフィールの高校大会受賞歴", "SUPPORTED", CHECKED, ""],
        ["B4W1E0030", "Career", "C000224", "activity_year", "2023", "B4W1S0009", "選手プロフィール > 受賞歴", "SoftBankウインターカップ2023優勝", "SUPPORTED", CHECKED, ""],
        ["B4W1E0031", "Career", "C000225", "organization_id", "ORG000017", "B4W1S0007", "日本経済大学 ROSTER > No.3", "日本経済大学の公式大会ロスター", "SUPPORTED", CHECKED, "開始・終了年月は不明"],
        ["B4W1E0032", "Career", "C000225", "role", "Player", "B4W1S0007", "日本経済大学 ROSTER > No.3", "登録選手として掲載", "SUPPORTED", CHECKED, ""],
        ["B4W1E0033", "Career", "C000225", "grade", "1年", "B4W1S0007", "日本経済大学 ROSTER > No.3", "2024年大会の学年", "SUPPORTED", CHECKED, ""],
        ["B4W1E0034", "Career", "C000225", "position", "SG", "B4W1S0007", "日本経済大学 ROSTER > No.3", "2024年大会のポジション", "SUPPORTED", CHECKED, ""],
        ["B4W1E0035", "Career", "C000225", "height_cm", "180", "B4W1S0007", "日本経済大学 ROSTER > No.3", "2024年大会の登録身長", "SUPPORTED", CHECKED, ""],
        ["B4W1E0036", "Career", "C000225", "activity_year", "2024", "B4W1S0007", "日本経済大学 ROSTER > No.3", "2024年大会登録", "SUPPORTED", CHECKED, ""],
        ["B4W1E0037", "Career", "C000225", "jersey_number", "3", "B4W1S0007", "日本経済大学 ROSTER > No.3", "2024年大会の背番号", "SUPPORTED", CHECKED, ""],
        ["B4W1E0038", "Career", "C000225", "grade", "2年", "B4W1S0008", "PDF 日本学生選抜 > 児玉ジュニア欄", "2025年の学年", "SUPPORTED", CHECKED, ""],
        ["B4W1E0039", "Career", "C000225", "activity_year", "2025", "B4W1S0008", "PDF 日本学生選抜 > 児玉ジュニア欄", "2025年の代表登録", "SUPPORTED", CHECKED, ""],
        ["B4W1E0040", "Career", "C000225", "basketball_club_status", "退部を発表", "B4W1S0009", "ニュース本文", "日本経済大学男子バスケットボール部を退部し三遠での活動に専念", "SUPPORTED", CHECKED, "学籍は在学中と別欄に記載"],
        ["B4W1E0041", "Career", "C000225", "status_announcement_date", "2025-09-19", "B4W1S0009", "ニュース公開日", "退部と契約を発表した日", "SUPPORTED", CHECKED, "実際の退部日とは限らない"],
        ["B4W1E0042", "Career", "C000226", "organization_id", "ORG000097", "B4W1S0009", "ニュース本文と経歴欄", "三遠との2025-26契約と2025-の経歴", "SUPPORTED", CHECKED, ""],
        ["B4W1E0043", "Career", "C000226", "role", "Player", "B4W1S0009", "契約締結発表", "三遠の選手契約", "SUPPORTED", CHECKED, ""],
        ["B4W1E0044", "Career", "C000226", "contract_season", "2025-26", "B4W1S0009", "ニュース本文", "2025-26シーズン選手契約", "SUPPORTED", CHECKED, ""],
        ["B4W1E0045", "Career", "C000226", "contract_announcement_date", "2025-09-19", "B4W1S0009", "ニュース公開日", "新規契約発表日", "SUPPORTED", CHECKED, ""],
        ["B4W1E0046", "Career", "C000226", "jersey_number", "33", "B4W1S0009", "選手プロフィール欄", "三遠での背番号", "SUPPORTED", CHECKED, ""],
        ["B4W1E0047", "Career", "C000226", "position", "PG/SG", "B4W1S0009", "選手プロフィール欄", "三遠での登録ポジション", "SUPPORTED", CHECKED, ""],
        ["B4W1E0048", "Career", "C000226", "competition_participation", "2025-26 B1 44試合", "B4W1S0010", "2025-26 B1 シーズン成績", "44試合・7先発を掲載", "SUPPORTED", CHECKED, "個別初出場日は未確認"],
        ["B4W1E0049", "Career", "C000226", "contract_season", "2026-27", "B4W1S0011", "ニュース本文", "2026-27シーズン継続契約", "SUPPORTED", CHECKED, ""],
        ["B4W1E0050", "Career", "C000226", "contract_announcement_date", "2026-05-28", "B4W1S0011", "ニュース公開日", "継続契約発表日", "SUPPORTED", CHECKED, ""],
        ["B4W1E0051", "Career", "C000226", "contract_term", "2028-29シーズンまで", "B4W1S0011", "ニュース本文", "2028-29シーズンまでの3年契約", "SUPPORTED", CHECKED, ""],
        ["B4W1E0052", "Career", "C000226", "specific_game_appearance", "2025-10-05 大阪対三遠", "B4W1S0012", "試合ページ", "試合は確認できるが本人の個別欄を再取得できない", "UNVERIFIED", CHECKED, "初出場日または個別出場の根拠にしない"],
        ["B4W1E0053", "Organization", "ORG000010", "name", "福岡第一高等学校", "B4W1S0001", "PDF 1ページ > 所属欄", "JBA公式資料の組織名", "SUPPORTED", CHECKED, ""],
        ["B4W1E0054", "Organization", "ORG000015", "name", "東海大学", "B4W1S0002", "PDF 選手一覧 > 所属欄", "JBA公式資料の組織名", "SUPPORTED", CHECKED, ""],
        ["B4W1E0055", "Organization", "ORG000055", "name", "横浜ビー・コルセアーズ", "B4W1S0003", "クラブ所属履歴 > 横浜BC", "B.LEAGUE公式のクラブ表記を正式名へ対応", "SUPPORTED", CHECKED, "公式ページ内の履歴表示は略称・横浜BC"],
        ["B4W1E0056", "Organization", "ORG000017", "name", "日本経済大学", "B4W1S0007", "日本経済大学 ROSTER", "JUBF公式資料の組織名", "SUPPORTED", CHECKED, "既存バッチの組織ID重複は別Issue"],
        ["B4W1E0057", "Organization", "ORG000097", "name", "三遠ネオフェニックス", "B4W1S0009", "ニュース本文", "クラブ公式の組織名", "SUPPORTED", CHECKED, ""],
        ["B4W1E0058", "Organization", "ORG000098", "name", "メンフィス・グリズリーズ", "B4W1S0004", "公式発表の発行元と本文", "NBAクラブの日本語表記候補", "SUPPORTED", CHECKED, "原資料の英語名はMemphis Grizzlies"],
    ]
    write(
        "evidence_records.csv",
        ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"],
        evidence,
    )

    write(
        "issues.csv",
        ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"],
        [
            ["B4W1I0001", "P000064", "C000219", "PERIOD_UNKNOWN", "HOLD", "福岡第一高校Careerの開始・終了年月は未確認", "学校または大会の複数年度公式資料を確認"],
            ["B4W1I0002", "P000064", "C000220", "PERIOD_UNKNOWN", "HOLD", "東海大学Careerの開始・終了年月は未確認", "大学または競技団体の年度別公式資料を確認"],
            ["B4W1I0003", "P000064", "P000064", "CURRENT_AFFILIATION_CONFLICT", "HOLD", "Clippers選手ページとNBA G Leagueページの所属表示に更新時点の違いがある", "契約発表・現行ロスター・公式取引記録を同一基準日で確認"],
            ["B4W1I0004", "P000064", "C000223", "NBA_CAREER_PERIOD", "HOLD", "MemphisとのTwo-Way契約発表後の終了時期と公式戦実績はこの資料だけでは確定しない", "NBA公式選手ログと取引記録を確認"],
            ["B4W1I0005", "P000065", "C000224", "PERIOD_UNKNOWN", "HOLD", "福岡第一高校Careerの開始・終了年月は未確認", "高校の年度別大会公式ロスターを確認"],
            ["B4W1I0006", "P000065", "C000225", "ACADEMIC_AND_CLUB_STATUS", "HOLD", "日本経済大学の学籍継続と男子部退部は別状態。入学日・退部日・学籍終了日は未確認", "大学公式の学籍・退部日を直接示す資料がある場合のみ更新"],
            ["B4W1I0007", "P000065", "C000226", "SPECIFIC_GAME_UNVERIFIED", "HOLD", "2025年10月5日の試合ページで本人の個別欄を再取得できない", "B.LEAGUE公式の個人ゲームログまたは取得可能なボックススコアを確認"],
            ["B4W1I0008", "P000065", "ORG000017", "ORGANIZATION_ID_DUPLICATE", "HOLD", "既存バッチで日本経済大学にORG000017とORG000019が混在する", "Master前に組織IDの正規化方針を決める"],
        ],
    )

    write(
        "qa_decisions.csv",
        ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"],
        [
            ["B4W1D0001", "Person", "P000064", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "current_affiliation", "公式資料で人物基本項目を確認。現在所属は表示矛盾のため保留", CHECKED],
            ["B4W1D0002", "Person", "P000065", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "", "JUBF公式資料で人物基本項目を確認", CHECKED],
            ["B4W1D0003", "Organization", "ORG000010", "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料の組織表記を確認", CHECKED],
            ["B4W1D0004", "Organization", "ORG000015", "READY_FOR_VERIFIED_REVIEW", "name", "", "公式資料の組織表記を確認", CHECKED],
            ["B4W1D0005", "Organization", "ORG000055", "READY_FOR_VERIFIED_REVIEW", "name", "", "B.LEAGUE公式プロフィールで組織表記を確認", CHECKED],
            ["B4W1D0006", "Organization", "ORG000017", "READY_FOR_VERIFIED_REVIEW", "name", "organization_id normalization", "JUBF公式資料で組織名を確認。既存ID重複は別途保留", CHECKED],
            ["B4W1D0007", "Organization", "ORG000097", "READY_FOR_VERIFIED_REVIEW", "name", "", "クラブ公式とB.LEAGUE公式で組織名を確認", CHECKED],
            ["B4W1D0008", "Organization", "ORG000098", "READY_FOR_VERIFIED_REVIEW", "name", "", "NBAクラブ公式発表で組織名を確認", CHECKED],
            ["B4W1D0009", "Career", "C000219", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|grade|activity_date", "start|end", "JBA公式資料で福岡第一高校所属を確認", CHECKED],
            ["B4W1D0010", "Career", "C000220", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|grade|activity_date", "start|end", "JBA公式資料で東海大学所属を確認", CHECKED],
            ["B4W1D0011", "Career", "C000221", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|season", "start|end", "B.LEAGUE公式プロフィールで所属シーズンを確認", CHECKED],
            ["B4W1D0012", "Career", "C000222", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|seasons|competition_participation", "start|end", "B.LEAGUE公式プロフィールで所属履歴と出場を確認", CHECKED],
            ["B4W1D0013", "Career", "C000223", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|contract_type|contract_announcement_date", "end|official_game_appearance", "Memphis公式発表でTwo-Way契約を確認", CHECKED],
            ["B4W1D0014", "Career", "C000224", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|activity_year", "start|end", "クラブ公式プロフィールで福岡第一とWC2023優勝を確認", CHECKED],
            ["B4W1D0015", "Career", "C000225", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|grade|position|height_cm|activity_year|jersey_number|basketball_club_status|status_announcement_date", "start|end|academic_end", "JUBFとクラブ公式で大学登録と男子部退部発表を確認", CHECKED],
            ["B4W1D0016", "Career", "C000226", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|contract_season|contract_announcement_date|jersey_number|position|competition_participation|contract_term", "end|specific_game_appearance", "クラブ公式とB.LEAGUE公式で契約とシーズン出場を確認", CHECKED],
        ],
    )


if __name__ == "__main__":
    main()
