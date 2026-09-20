#!/usr/bin/env python3
"""Build Batch 004 Wave 2 candidate files.

This creates CANDIDATE and QA inputs only. It never writes VERIFIED or MASTER.
"""

from __future__ import annotations

import csv
from pathlib import Path


OUT = Path("data/candidate/batch_004/wave_02")
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
        [["P000066", "河合 瑠那"], ["P000067", "長岡 大杜"]],
    )

    write(
        "organization_candidates.csv",
        ["organization_id", "name"],
        [
            ["ORG000010", "福岡第一高等学校"],
            ["ORG000090", "横浜エクセレンス"],
            ["ORG000099", "大阪学院大学"],
            ["ORG000100", "山口パッツファイブ"],
        ],
    )

    write(
        "career_candidates.csv",
        ["career_id", "person_id", "organization_id", "role", "start", "end"],
        [
            ["C000227", "P000066", "ORG000010", "Player", "", ""],
            ["C000228", "P000066", "ORG000099", "Player", "", ""],
            ["C000229", "P000066", "ORG000090", "Player", "2026", "2026"],
            ["C000230", "P000067", "ORG000010", "Player", "", ""],
            ["C000231", "P000067", "ORG000100", "Player", "2026", ""],
        ],
    )

    write(
        "source_references.csv",
        ["source_id", "title", "publisher", "url", "accessed_at"],
        [
            ["B4W2S0001", "河合瑠那 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=51000607", CHECKED],
            ["B4W2S0002", "河合瑠那選手 特別指定選手登録のお知らせ", "横浜エクセレンス", "https://yokohama-ex.jp/team/pages/id=22814", CHECKED],
            ["B4W2S0003", "河合瑠那選手 特別指定選手活動終了のお知らせ", "横浜エクセレンス", "https://yokohama-ex.jp/news/detail/id=25440", CHECKED],
            ["B4W2S0004", "大阪学院大学 2023インカレ登録", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/49/type/intercollege/y/2023/s/men", CHECKED],
            ["B4W2S0005", "大阪学院大学 2024インカレ登録", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/49/type/intercollege/y/2024/s/men", CHECKED],
            ["B4W2S0006", "長岡大杜 B.LEAGUE公式選手プロフィール", "B.LEAGUE", "https://www.bleague.jp/roster_detail/?PlayerID=52467", CHECKED],
            ["B4W2S0007", "2025-26シーズン 新規リーグエントリー選手のお知らせ", "B3リーグ", "https://www.b3league.jp/archives/45352", CHECKED],
        ],
    )

    evidence = [
        ["B4W2E0001", "Person", "P000066", "name", "河合 瑠那", "B4W2S0001", "基本情報 > 選手名", "B.LEAGUE公式プロフィールの氏名", "SUPPORTED", CHECKED, ""],
        ["B4W2E0002", "Person", "P000066", "name_en", "Runa Kawai", "B4W2S0001", "基本情報 > 英語表記", "B.LEAGUE公式プロフィールの英語表記", "SUPPORTED", CHECKED, ""],
        ["B4W2E0003", "Person", "P000066", "birth_date", "2003-06-03", "B4W2S0001", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールの生年月日", "SUPPORTED", CHECKED, ""],
        ["B4W2E0004", "Person", "P000066", "height_cm", "181", "B4W2S0001", "基本情報 > 身長", "B.LEAGUE公式プロフィールは181cm", "CONFLICT", CHECKED, "JUBFは180cm、クラブ発表は183cm"],
        ["B4W2E0005", "Person", "P000066", "height_cm", "183", "B4W2S0002", "選手プロフィール > 身長", "クラブ登録発表は183cm", "CONFLICT", CHECKED, "B.LEAGUEは181cm、JUBFは180cm"],
        ["B4W2E0006", "Career", "C000227", "organization_id", "ORG000010", "B4W2S0002", "選手プロフィール > 出身校", "福岡第一高等学校を掲載", "SUPPORTED", CHECKED, "開始・終了年月は不明"],
        ["B4W2E0007", "Career", "C000227", "role", "Player", "B4W2S0002", "特別指定選手プロフィール", "選手の経歴として福岡第一高等学校を掲載", "SUPPORTED", CHECKED, ""],
        ["B4W2E0008", "Career", "C000228", "organization_id", "ORG000099", "B4W2S0004", "ROSTER > No.2 河合瑠那", "大阪学院大学の大会登録", "SUPPORTED", CHECKED, "開始・終了年月は不明"],
        ["B4W2E0009", "Career", "C000228", "role", "Player", "B4W2S0004", "ROSTER > No.2", "登録選手として掲載", "SUPPORTED", CHECKED, ""],
        ["B4W2E0010", "Career", "C000228", "grade", "2年", "B4W2S0004", "ROSTER > No.2 > 学年", "2023年大会の学年", "SUPPORTED", CHECKED, ""],
        ["B4W2E0011", "Career", "C000228", "position", "PG", "B4W2S0004", "ROSTER > No.2 > ポジション", "2023年大会のポジション", "SUPPORTED", CHECKED, ""],
        ["B4W2E0012", "Career", "C000228", "height_cm", "180", "B4W2S0004", "ROSTER > No.2 > 身長", "2023年大会の登録身長", "SUPPORTED", CHECKED, "他資料と時点別の差がある"],
        ["B4W2E0013", "Career", "C000228", "competition_participation", "2023インカレ 1試合10分00秒", "B4W2S0004", "個人成績 > 河合瑠那", "1試合10分出場", "SUPPORTED", CHECKED, ""],
        ["B4W2E0014", "Career", "C000228", "grade", "3年", "B4W2S0005", "ROSTER > No.2 > 学年", "2024年大会の学年", "SUPPORTED", CHECKED, ""],
        ["B4W2E0015", "Career", "C000228", "competition_participation", "2024インカレ 2試合44分50秒", "B4W2S0005", "個人成績 > 河合瑠那", "2試合44分50秒出場", "SUPPORTED", CHECKED, ""],
        ["B4W2E0016", "Career", "C000229", "organization_id", "ORG000090", "B4W2S0002", "発表本文と選手プロフィール", "横浜エクセレンスが特別指定選手登録を発表", "SUPPORTED", CHECKED, ""],
        ["B4W2E0017", "Career", "C000229", "role", "Player", "B4W2S0002", "特別指定選手登録発表", "選手登録の対象として掲載", "SUPPORTED", CHECKED, ""],
        ["B4W2E0018", "Career", "C000229", "registration_type", "特別指定選手", "B4W2S0002", "発表見出し・本文", "特別指定選手として登録", "SUPPORTED", CHECKED, ""],
        ["B4W2E0019", "Career", "C000229", "bench_eligible_from", "2026-03-18", "B4W2S0002", "発表本文", "3月18日からベンチ登録可能", "SUPPORTED", CHECKED, "実際の初出場日とは限らない"],
        ["B4W2E0020", "Career", "C000229", "activity_end_announcement", "2026-05-21", "B4W2S0003", "公開日と本文", "2025-26シーズン限りで活動終了と発表", "SUPPORTED", CHECKED, "実際の終了日は本文で日付特定できない"],
        ["B4W2E0021", "Career", "C000229", "competition_participation", "2025-26 B2 1試合3分33秒・2得点", "B4W2S0001", "2025-26 B2 シーズン成績", "B2公式戦出場を掲載", "SUPPORTED", CHECKED, ""],
        ["B4W2E0022", "Person", "P000067", "name", "長岡 大杜", "B4W2S0006", "基本情報 > 選手名", "B.LEAGUE公式プロフィールの氏名", "SUPPORTED", CHECKED, ""],
        ["B4W2E0023", "Person", "P000067", "name_en", "Daito Nagaoka", "B4W2S0006", "基本情報 > 英語表記", "B.LEAGUE公式プロフィールの英語表記", "SUPPORTED", CHECKED, ""],
        ["B4W2E0024", "Person", "P000067", "birth_date", "2007-10-17", "B4W2S0006", "基本情報 > 生年月日", "B.LEAGUE公式プロフィールの生年月日", "SUPPORTED", CHECKED, ""],
        ["B4W2E0025", "Person", "P000067", "height_cm", "178", "B4W2S0006", "基本情報 > 身長", "B.LEAGUE公式プロフィールの身長", "SUPPORTED", CHECKED, ""],
        ["B4W2E0026", "Person", "P000067", "weight_kg", "77", "B4W2S0006", "基本情報 > 体重", "B.LEAGUE公式プロフィールの体重", "SUPPORTED", CHECKED, ""],
        ["B4W2E0027", "Person", "P000067", "birthplace_prefecture", "山口県", "B4W2S0006", "基本情報 > 出身地", "B.LEAGUE公式プロフィールの出身地", "SUPPORTED", CHECKED, "国籍欄としては扱わない"],
        ["B4W2E0028", "Career", "C000230", "organization_id", "ORG000010", "B4W2S0006", "基本情報 > 出身校", "福岡第一高等学校在学中と掲載", "SUPPORTED", CHECKED, "入学・卒業年月は不明"],
        ["B4W2E0029", "Career", "C000230", "role", "Player", "B4W2S0007", "新規リーグエントリー選手欄", "福岡第一高等学校在学中の選手として掲載", "SUPPORTED", CHECKED, ""],
        ["B4W2E0030", "Career", "C000230", "academic_status", "在学中", "B4W2S0007", "選手プロフィール > 出身校", "発表時点で福岡第一高等学校在学中", "SUPPORTED", CHECKED, "基準日は2026-01-30"],
        ["B4W2E0031", "Career", "C000231", "organization_id", "ORG000100", "B4W2S0007", "新規リーグエントリー選手欄", "山口パッツファイブの新規リーグエントリー", "SUPPORTED", CHECKED, ""],
        ["B4W2E0032", "Career", "C000231", "role", "Player", "B4W2S0007", "新規リーグエントリー選手欄", "登録選手として掲載", "SUPPORTED", CHECKED, ""],
        ["B4W2E0033", "Career", "C000231", "league_entry_announcement", "2026-01-30", "B4W2S0007", "公開日", "新規リーグエントリー発表日", "SUPPORTED", CHECKED, "実際の契約開始日とは限らない"],
        ["B4W2E0034", "Career", "C000231", "jersey_number", "17", "B4W2S0007", "選手プロフィール > 背番号", "山口での背番号", "SUPPORTED", CHECKED, ""],
        ["B4W2E0035", "Career", "C000231", "position", "SG", "B4W2S0007", "選手プロフィール > ポジション", "山口での登録ポジション", "SUPPORTED", CHECKED, ""],
        ["B4W2E0036", "Career", "C000231", "competition_participation", "2025-26 B3 1試合1分12秒", "B4W2S0006", "2025-26 B3 シーズン成績", "B3公式戦出場を掲載", "SUPPORTED", CHECKED, ""],
        ["B4W2E0037", "Organization", "ORG000010", "name", "福岡第一高等学校", "B4W2S0007", "選手プロフィール > 出身校", "B3公式の学校名", "SUPPORTED", CHECKED, ""],
        ["B4W2E0038", "Organization", "ORG000090", "name", "横浜エクセレンス", "B4W2S0002", "発行元・本文", "クラブ公式の組織名", "SUPPORTED", CHECKED, "Excel原本の既存IDを使用"],
        ["B4W2E0039", "Organization", "ORG000099", "name", "大阪学院大学", "B4W2S0004", "大学名・ROSTER", "JUBF公式の組織名", "SUPPORTED", CHECKED, ""],
        ["B4W2E0040", "Organization", "ORG000100", "name", "山口パッツファイブ", "B4W2S0007", "選手所属欄", "B3公式のクラブ名", "SUPPORTED", CHECKED, ""],
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
            ["B4W2I0001", "P000066", "C000227", "PERIOD_UNKNOWN", "HOLD", "福岡第一高校Careerの開始・終了年月は未確認", "年度別公式ロスターを確認"],
            ["B4W2I0002", "P000066", "C000228", "PERIOD_UNKNOWN", "HOLD", "大阪学院大学Careerの開始・終了年月は未確認", "大学または競技団体の年度別公式資料を確認"],
            ["B4W2I0003", "P000066", "P000066", "HEIGHT_VARIATION", "HOLD", "資料時点により180cm・181cm・183cmの登録値がある", "値を上書き統合せずSource別・時点別で保持"],
            ["B4W2I0004", "P000066", "C000229", "ACTIVITY_END_DATE", "HOLD", "活動終了の発表日は確認したが実際の終了日は日付特定できない", "クラブまたはリーグの登録抹消日を確認"],
            ["B4W2I0005", "P000067", "P000067", "EXCEL_MEMO_MISMATCH", "HOLD", "提案文書はExcel原本内の同名候補ありとするが、原本Personシートに長岡大杜は存在しない", "提案文書の根拠となった別版または別ファイルを確認"],
            ["B4W2I0006", "P000067", "C000230", "PERIOD_UNKNOWN", "HOLD", "福岡第一高校在学は確認したが入学・卒業年月は未確認", "学校または大会の年度別公式資料を確認"],
            ["B4W2I0007", "P000067", "C000231", "CAREER_START_DATE", "HOLD", "リーグエントリー発表日は契約・所属開始日とは限らない", "クラブ公式契約発表またはリーグ登録日を確認"],
            ["B4W2I0008", "P000067", "P000067", "NATIONALITY_FIELD_LAYOUT", "HOLD", "B.LEAGUE表示の「リーグ登録国籍特別指定」は画面項目の結合とみられ国籍値に採用できない", "国籍を明記した公式プロフィールが見つかった場合のみ追加"],
        ],
    )

    write(
        "qa_decisions.csv",
        ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"],
        [
            ["B4W2D0001", "Person", "P000066", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date", "height_cm", "B.LEAGUE公式で基本項目を確認。身長は資料差のため保留", CHECKED],
            ["B4W2D0002", "Person", "P000067", "READY_FOR_VERIFIED_REVIEW", "name|name_en|birth_date|height_cm|weight_kg|birthplace_prefecture", "nationality", "B.LEAGUE公式で基本項目を確認。国籍は採用しない", CHECKED],
            ["B4W2D0003", "Organization", "ORG000010", "READY_FOR_VERIFIED_REVIEW", "name", "", "B3公式で組織名を確認", CHECKED],
            ["B4W2D0004", "Organization", "ORG000090", "READY_FOR_VERIFIED_REVIEW", "name", "", "クラブ公式で組織名を確認", CHECKED],
            ["B4W2D0005", "Organization", "ORG000099", "READY_FOR_VERIFIED_REVIEW", "name", "", "JUBF公式で組織名を確認", CHECKED],
            ["B4W2D0006", "Organization", "ORG000100", "READY_FOR_VERIFIED_REVIEW", "name", "", "B3公式で組織名を確認", CHECKED],
            ["B4W2D0007", "Career", "C000227", "READY_FOR_VERIFIED_REVIEW", "organization_id|role", "start|end", "クラブ公式プロフィールで福岡第一高校の経歴を確認", CHECKED],
            ["B4W2D0008", "Career", "C000228", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|grade|position|height_cm|competition_participation", "start|end", "JUBF公式で大学登録と出場を確認", CHECKED],
            ["B4W2D0009", "Career", "C000229", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|registration_type|bench_eligible_from|activity_end_announcement|competition_participation", "exact_end_date", "クラブ公式とB.LEAGUE公式で登録・活動終了発表・出場を確認", CHECKED],
            ["B4W2D0010", "Career", "C000230", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|academic_status", "start|end", "B3公式で福岡第一高校在学中を確認", CHECKED],
            ["B4W2D0011", "Career", "C000231", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|league_entry_announcement|jersey_number|position|competition_participation", "exact_start|end", "B3・B.LEAGUE公式で登録と出場を確認", CHECKED],
        ],
    )


if __name__ == "__main__":
    main()
