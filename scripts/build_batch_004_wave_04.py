#!/usr/bin/env python3
"""Build Batch 004 Wave 4 candidate files without touching VERIFIED or MASTER."""

from __future__ import annotations

import csv
from pathlib import Path


OUT = Path("data/candidate/batch_004/wave_04")
CHECKED = "2026-09-21"


def write(name: str, headers: list[str], rows: list[list[str]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def main() -> None:
    write("person_candidates.csv", ["person_id", "name"], [
        ["P000071", "今泉 太陽"],
        ["P000072", "崎濱 秀真"],
    ])
    write("organization_candidates.csv", ["organization_id", "name"], [
        ["ORG000010", "福岡第一高等学校"],
        ["ORG000017", "日本経済大学"],
        ["ORG000105", "新潟経営大学"],
    ])
    write("career_candidates.csv", ["career_id", "person_id", "organization_id", "role", "start", "end"], [
        ["C000253", "P000071", "ORG000010", "Player", "2019", "2022"],
        ["C000254", "P000071", "ORG000017", "Player", "2022", ""],
        ["C000255", "P000072", "ORG000010", "Player", "2019", "2022"],
        ["C000256", "P000072", "ORG000105", "Player", "2022", ""],
    ])
    write("source_references.csv", ["source_id", "title", "publisher", "url", "accessed_at"], [
        ["B4W4S0001", "B.LEAGUE DRAFT 2026 候補選手一覧", "B.LEAGUE", "https://www.bleague.jp/draft2026/prospects/list/", CHECKED],
        ["B4W4S0002", "第77回全日本大学バスケットボール選手権大会 日本経済大学", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/180/type/intercollege/y/2025/s/men", CHECKED],
        ["B4W4S0003", "第74回全日本大学バスケットボール選手権大会 新潟経営大学", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/4/type/intercollege/y/2022/s/men", CHECKED],
        ["B4W4S0004", "第76回全日本大学バスケットボール選手権大会 新潟経営大学", "全日本大学バスケットボール連盟", "https://jubf.jp/game/university-detail/id/4/type/intercollege/y/2024/s/men", CHECKED],
        ["B4W4S0005", "B.LEAGUE DRAFT 2026 指名結果", "B.LEAGUE", "https://www.bleague.jp/draft2026/result/", CHECKED],
    ])

    evidence: list[list[str]] = []

    def ev(number: int, entity_type: str, entity_id: str, field: str, value: str,
           source: str, locator: str, summary: str,
           assessment: str = "SUPPORTED", note: str = "") -> None:
        evidence.append([
            f"B4W4E{number:04d}", entity_type, entity_id, field, value,
            source, locator, summary, assessment, CHECKED, note,
        ])

    ev(1, "Person", "P000071", "name", "今泉 太陽", "B4W4S0001", "候補選手一覧 > 今泉 太陽 > プロフィール", "B.LEAGUE公式の氏名")
    ev(2, "Person", "P000071", "birth_date", "2003-08-12", "B4W4S0001", "候補選手一覧 > 今泉 太陽 > 生年月日", "生年月日を掲載")
    ev(3, "Person", "P000071", "position", "SG", "B4W4S0001", "候補選手一覧 > 今泉 太陽 > ポジション", "登録ポジション")
    ev(4, "Person", "P000071", "height_cm", "181", "B4W4S0001", "候補選手一覧 > 今泉 太陽 > 身長", "ドラフト候補プロフィールの身長")
    ev(5, "Person", "P000071", "weight_kg", "74", "B4W4S0001", "候補選手一覧 > 今泉 太陽 > 体重", "ドラフト候補プロフィールの体重")
    ev(6, "Person", "P000071", "draft_candidate_listing", "B.LEAGUE DRAFT 2026", "B4W4S0001", "候補選手一覧 > 今泉 太陽", "候補選手一覧への掲載")
    ev(7, "Career", "C000253", "organization_id", "ORG000010", "B4W4S0001", "今泉 太陽 > 経歴 > 2019年4月-2022年3月", "福岡第一高等学校の期間を掲載")
    ev(8, "Career", "C000253", "role", "Player", "B4W4S0001", "候補選手プロフィール > 経歴", "競技者プロフィール上の学校経歴", "PARTIAL", "高校大会ロスターによる役割の直接確認ではない")
    ev(9, "Career", "C000253", "start", "2019", "B4W4S0001", "今泉 太陽 > 経歴", "開始年月を2019年4月と掲載")
    ev(10, "Career", "C000253", "end", "2022", "B4W4S0001", "今泉 太陽 > 経歴", "終了年月を2022年3月と掲載")
    ev(11, "Career", "C000254", "organization_id", "ORG000017", "B4W4S0002", "ROSTER > No.8 今泉 太陽", "日本経済大学の大会ロスター")
    ev(12, "Career", "C000254", "role", "Player", "B4W4S0002", "ROSTER・STATS > No.8", "2025年大会で7試合出場")
    ev(13, "Career", "C000254", "start", "2022", "B4W4S0001", "今泉 太陽 > 経歴 > 2022年4月-現在", "大学開始年月を掲載")
    ev(14, "Career", "C000254", "competition_participation", "2025インカレ 7試合", "B4W4S0002", "STATS > No.8 今泉 太陽", "7試合・205分22秒の出場記録")
    ev(15, "Person", "P000072", "name", "崎濱 秀真", "B4W4S0001", "候補選手一覧 > 崎濱 秀真 > プロフィール", "B.LEAGUE公式の氏名")
    ev(16, "Person", "P000072", "birth_date", "2003-08-21", "B4W4S0001", "候補選手一覧 > 崎濱 秀真 > 生年月日", "生年月日を掲載")
    ev(17, "Person", "P000072", "position", "PG/SG", "B4W4S0001", "候補選手一覧 > 崎濱 秀真 > ポジション", "登録ポジション")
    ev(18, "Person", "P000072", "height_cm", "181", "B4W4S0001", "候補選手一覧 > 崎濱 秀真 > 身長", "ドラフト候補プロフィールの身長")
    ev(19, "Person", "P000072", "weight_kg", "83", "B4W4S0001", "候補選手一覧 > 崎濱 秀真 > 体重", "ドラフト候補プロフィールの体重")
    ev(20, "Person", "P000072", "draft_candidate_listing", "B.LEAGUE DRAFT 2026", "B4W4S0001", "候補選手一覧 > 崎濱 秀真", "候補選手一覧への掲載")
    ev(21, "Career", "C000255", "organization_id", "ORG000010", "B4W4S0001", "崎濱 秀真 > 経歴 > 2019年4月-2022年3月", "福岡第一高等学校の期間を掲載")
    ev(22, "Career", "C000255", "role", "Player", "B4W4S0001", "候補選手プロフィール > 経歴", "競技者プロフィール上の学校経歴", "PARTIAL", "高校大会ロスターによる役割の直接確認ではない")
    ev(23, "Career", "C000255", "start", "2019", "B4W4S0001", "崎濱 秀真 > 経歴", "開始年月を2019年4月と掲載")
    ev(24, "Career", "C000255", "end", "2022", "B4W4S0001", "崎濱 秀真 > 経歴", "終了年月を2022年3月と掲載")
    ev(25, "Career", "C000256", "organization_id", "ORG000105", "B4W4S0003", "ROSTER > No.23 崎濱 秀真", "新潟経営大学の2022年大会ロスター")
    ev(26, "Career", "C000256", "role", "Player", "B4W4S0004", "ROSTER・STATS > No.23", "2024年大会で2試合出場")
    ev(27, "Career", "C000256", "start", "2022", "B4W4S0001", "崎濱 秀真 > 経歴 > 2022年4月-現在", "大学開始年月を掲載")
    ev(28, "Career", "C000256", "competition_participation", "2024インカレ 2試合", "B4W4S0004", "STATS > No.23 崎濱 秀真", "2試合・30分27秒の出場記録")
    ev(29, "Organization", "ORG000010", "name", "福岡第一高等学校", "B4W4S0001", "両選手の経歴欄", "公式資料内の組織表記")
    ev(30, "Organization", "ORG000017", "name", "日本経済大学", "B4W4S0002", "大学名・ROSTER", "JUBF公式資料の組織名")
    ev(31, "Organization", "ORG000105", "name", "新潟経営大学", "B4W4S0004", "大学名・ROSTER", "JUBF公式資料の組織名")
    write("evidence_records.csv", ["record_id", "entity_type", "entity_id", "field_name", "candidate_value", "source_id", "source_locator", "evidence_summary", "assessment", "checked_at", "issue_note"], evidence)

    write("issues.csv", ["issue_id", "person_id", "related_id", "issue_type", "status", "description", "next_check"], [
        ["B4W4I0001", "P000071", "C000253", "HIGH_SCHOOL_ROLE", "HOLD", "B.LEAGUE候補者経歴は学校期間を示すが、高校大会ロスターでのPlayer役割は未確認", "高校大会公式ロスターを確認"],
        ["B4W4I0002", "P000071", "P000071", "DRAFT_OUTCOME", "HOLD", "候補選手一覧掲載は契約・登録・出場を意味しない。公式指名結果に氏名は確認できない", "クラブ契約発表・リーグ登録を継続確認"],
        ["B4W4I0003", "P000071", "C000254", "CURRENT_UNIVERSITY_END", "HOLD", "候補者ページの『現在』は基準日依存で、大学Career終了日は未確認", "大学または次所属の公式発表を確認"],
        ["B4W4I0004", "P000072", "C000255", "HIGH_SCHOOL_ROLE", "HOLD", "B.LEAGUE候補者経歴は学校期間を示すが、高校大会ロスターでのPlayer役割は未確認", "高校大会公式ロスターを確認"],
        ["B4W4I0005", "P000072", "P000072", "DRAFT_OUTCOME", "HOLD", "候補選手一覧掲載は契約・登録・出場を意味しない。公式指名結果に氏名は確認できない", "クラブ契約発表・リーグ登録を継続確認"],
        ["B4W4I0006", "P000072", "C000256", "CURRENT_UNIVERSITY_END", "HOLD", "候補者ページの『現在』は基準日依存で、大学Career終了日は未確認", "大学または次所属の公式発表を確認"],
    ])

    write("qa_decisions.csv", ["decision_id", "entity_type", "entity_id", "decision", "eligible_fields", "held_fields", "reason", "reviewed_at"], [
        ["B4W4D0001", "Person", "P000071", "READY_FOR_VERIFIED_REVIEW", "name|birth_date|position|height_cm|weight_kg|draft_candidate_listing", "professional_contract|league_registration|professional_appearance", "B.LEAGUE候補選手一覧で確認", CHECKED],
        ["B4W4D0002", "Person", "P000072", "READY_FOR_VERIFIED_REVIEW", "name|birth_date|position|height_cm|weight_kg|draft_candidate_listing", "professional_contract|league_registration|professional_appearance", "B.LEAGUE候補選手一覧で確認", CHECKED],
        ["B4W4D0003", "Career", "C000253", "READY_FOR_VERIFIED_REVIEW", "organization_id|start|end", "role", "B.LEAGUE候補者経歴で期間を確認", CHECKED],
        ["B4W4D0004", "Career", "C000254", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|competition_participation", "end", "B.LEAGUEとJUBF公式で確認", CHECKED],
        ["B4W4D0005", "Career", "C000255", "READY_FOR_VERIFIED_REVIEW", "organization_id|start|end", "role", "B.LEAGUE候補者経歴で期間を確認", CHECKED],
        ["B4W4D0006", "Career", "C000256", "READY_FOR_VERIFIED_REVIEW", "organization_id|role|start|competition_participation", "end", "B.LEAGUEとJUBF公式で確認", CHECKED],
        ["B4W4D0007", "Organization", "ORG000010", "READY_FOR_VERIFIED_REVIEW", "name", "", "B.LEAGUE公式資料内表記を確認", CHECKED],
        ["B4W4D0008", "Organization", "ORG000017", "READY_FOR_VERIFIED_REVIEW", "name", "organization_id normalization", "JUBF公式資料内表記を確認", CHECKED],
        ["B4W4D0009", "Organization", "ORG000105", "READY_FOR_VERIFIED_REVIEW", "name", "", "JUBF公式資料内表記を確認", CHECKED],
    ])


if __name__ == "__main__":
    main()
