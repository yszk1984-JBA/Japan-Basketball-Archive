#!/usr/bin/env python3
"""Build Batch 002 candidate seed from checked B.LEAGUE official profiles.

The output remains CANDIDATE. It does not create VERIFIED or MASTER data.
"""

from __future__ import annotations

import csv
from pathlib import Path


OUTPUT_DIR = Path("data/candidate/batch_002")
ACCESSED_AT = "2026-09-19"
LIST_URL = (
    "https://www.bleague.jp/mybleague_list/"
    "?TagID=35:%E7%A6%8F%E5%B2%A1%E7%AC%AC%E4%B8%80%E9%AB%98%E7%AD%89%E5%AD%A6%E6%A0%A1"
)

PLAYERS = [
    {
        "person_id": "P000063",
        "name": "古野 拓巳",
        "name_en": "Takumi Furuno",
        "birth_date": "1993-02-20",
        "profile_url": "https://www.bleague.jp/roster_detail/?PlayerID=9348",
        "source_id": "B2S0001",
        "high_school_career_id": "C000210",
        "pro_career_id": "C000211",
        "pro_org_id": "ORG000091",
        "pro_org_name": "愛媛オレンジバイキングス",
        "education_display": "日本経済大学",
    },
    {
        "person_id": "P000038",
        "name": "内尾 聡理",
        "name_en": "Sori Uchio",
        "birth_date": "2001-04-12",
        "profile_url": "https://www.bleague.jp/roster_detail/?PlayerID=51000353",
        "source_id": "B2S0002",
        "high_school_career_id": "C000057",
        "pro_career_id": "C000107",
        "pro_org_id": "ORG000048",
        "pro_org_name": "佐賀バルーナーズ",
        "education_display": "中央大学",
    },
    {
        "person_id": "P000037",
        "name": "鵤 誠司",
        "name_en": "Seiji Ikaruga",
        "birth_date": "1994-01-08",
        "profile_url": "https://www.bleague.jp/roster_detail/?PlayerID=8529",
        "source_id": "B2S0003",
        "high_school_career_id": "C000056",
        "pro_career_id": "C000103",
        "pro_org_id": "ORG000047",
        "pro_org_name": "宇都宮ブレックス",
        "education_display": "青山学院大学",
    },
    {
        "person_id": "P000041",
        "name": "狩野 祐介",
        "name_en": "Yusuke Karino",
        "birth_date": "1990-04-18",
        "profile_url": "https://www.bleague.jp/roster_detail/?PlayerID=8463",
        "source_id": "B2S0004",
        "high_school_career_id": "C000060",
        "pro_career_id": "C000129",
        "pro_org_id": "ORG000040",
        "pro_org_name": "ライジングゼファー福岡",
        "education_display": "東海大学",
    },
    {
        "person_id": "P000042",
        "name": "並里 成",
        "name_en": "Narito Namizato",
        "birth_date": "1989-08-07",
        "profile_url": "https://www.bleague.jp/roster_detail/?PlayerID=9489",
        "source_id": "B2S0005",
        "high_school_career_id": "C000061",
        "pro_career_id": "C000140",
        "pro_org_id": "ORG000055",
        "pro_org_name": "横浜ビー・コルセアーズ",
        "education_display": "福岡第一高校",
    },
    {
        "person_id": "P000039",
        "name": "渡辺 竜之佑",
        "name_en": "Ryunosuke Watanabe",
        "birth_date": "1994-08-24",
        "profile_url": "https://www.bleague.jp/roster_detail/?PlayerID=9329",
        "source_id": "B2S0006",
        "high_school_career_id": "C000058",
        "pro_career_id": "C000117",
        "pro_org_id": "ORG000042",
        "pro_org_name": "京都ハンナリーズ",
        "education_display": "専修大学",
    },
    {
        "person_id": "P000043",
        "name": "松崎 裕樹",
        "name_en": "Hiroki Matsuzaki",
        "birth_date": "2000-06-02",
        "profile_url": "https://www.bleague.jp/roster_detail/?PlayerID=51000227",
        "source_id": "B2S0007",
        "high_school_career_id": "C000062",
        "pro_career_id": "C000212",
        "pro_org_id": "ORG000092",
        "pro_org_name": "レバンガ北海道",
        "pro_start": "2026",
        "education_display": "東海大学",
    },
    {
        "person_id": "P000035",
        "name": "小川 麻斗",
        "name_en": "Asato Ogawa",
        "birth_date": "2001-08-23",
        "profile_url": "https://www.bleague.jp/roster_detail/?PlayerID=5100000033",
        "source_id": "B2S0008",
        "high_school_career_id": "C000054",
        "pro_career_id": "C000088",
        "pro_org_id": "ORG000043",
        "pro_org_name": "神戸ストークス",
        "education_display": "日本体育大学",
    },
    {
        "person_id": "P000040",
        "name": "神田 壮一郎",
        "name_en": "Soichiro Kanda",
        "birth_date": "2001-06-16",
        "profile_url": "https://www.bleague.jp/roster_detail/?PlayerID=51000380",
        "source_id": "B2S0009",
        "high_school_career_id": "C000059",
        "pro_career_id": "C000120",
        "pro_org_id": "ORG000050",
        "pro_org_name": "ウォルガ湘南",
        "education_display": "拓殖大学",
    },
    {
        "person_id": "P000036",
        "name": "井手 拓実",
        "name_en": "Takumi Ide",
        "birth_date": "1999-10-12",
        "profile_url": "https://www.bleague.jp/roster_detail/?PlayerID=51000110",
        "source_id": "B2S0010",
        "high_school_career_id": "C000055",
        "pro_career_id": "C000092",
        "pro_org_id": "ORG000046",
        "pro_org_name": "アースフレンズ東京Z",
        "education_display": "日本体育大学",
    },
]


def write_csv(filename: str, headers: list[str], rows: list[dict[str, str]]) -> None:
    with (OUTPUT_DIR / filename).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    write_csv(
        "person_candidates.csv",
        ["person_id", "name"],
        [{"person_id": p["person_id"], "name": p["name"]} for p in PLAYERS],
    )

    organizations = {"ORG000010": "福岡第一高等学校"}
    organizations.update({p["pro_org_id"]: p["pro_org_name"] for p in PLAYERS})
    write_csv(
        "organization_candidates.csv",
        ["organization_id", "name"],
        [
            {"organization_id": organization_id, "name": name}
            for organization_id, name in organizations.items()
        ],
    )

    careers: list[dict[str, str]] = []
    for player in PLAYERS:
        careers.extend(
            [
                {
                    "career_id": player["high_school_career_id"],
                    "person_id": player["person_id"],
                    "organization_id": "ORG000010",
                    "role": "Player",
                    "start": "",
                    "end": "",
                },
                {
                    "career_id": player["pro_career_id"],
                    "person_id": player["person_id"],
                    "organization_id": player["pro_org_id"],
                    "role": "Player",
                    "start": player.get("pro_start", ""),
                    "end": "",
                },
            ]
        )
    write_csv(
        "career_candidates.csv",
        ["career_id", "person_id", "organization_id", "role", "start", "end"],
        careers,
    )

    sources = [
        {
            "source_id": "B2S0000",
            "title": "ワタシノB.LEAGUE選手一覧｜福岡第一高等学校",
            "publisher": "B.LEAGUE",
            "url": LIST_URL,
            "accessed_at": ACCESSED_AT,
        }
    ]
    sources.extend(
        {
            "source_id": p["source_id"],
            "title": f"{p['name']} 選手プロフィール",
            "publisher": "B.LEAGUE",
            "url": p["profile_url"],
            "accessed_at": ACCESSED_AT,
        }
        for p in PLAYERS
    )
    sources.append(
        {
            "source_id": "B2S0011",
            "title": "#24 松崎裕樹選手 新規入団のお知らせ",
            "publisher": "レバンガ北海道",
            "url": "https://www.levanga.com/news/detail/id=22266",
            "accessed_at": ACCESSED_AT,
        }
    )
    write_csv(
        "source_references.csv",
        ["source_id", "title", "publisher", "url", "accessed_at"],
        sources,
    )

    evidence: list[dict[str, str]] = []
    issues: list[dict[str, str]] = []
    decisions: list[dict[str, str]] = []
    evidence_number = 1
    issue_number = 1
    decision_number = 1

    def add_evidence(
        entity_type: str,
        entity_id: str,
        field_name: str,
        candidate_value: str,
        source_id: str,
        source_locator: str,
        evidence_summary: str,
        assessment: str,
        issue_note: str = "",
    ) -> None:
        nonlocal evidence_number
        evidence.append(
            {
                "record_id": f"B2E{evidence_number:04d}",
                "entity_type": entity_type,
                "entity_id": entity_id,
                "field_name": field_name,
                "candidate_value": candidate_value,
                "source_id": source_id,
                "source_locator": source_locator,
                "evidence_summary": evidence_summary,
                "assessment": assessment,
                "checked_at": ACCESSED_AT,
                "issue_note": issue_note,
            }
        )
        evidence_number += 1

    for player in PLAYERS:
        add_evidence(
            "Person", player["person_id"], "name", player["name"],
            player["source_id"], "基本情報 > 選手名",
            "B.LEAGUE公式プロフィールの選手名", "SUPPORTED",
        )
        add_evidence(
            "Person", player["person_id"], "name_en", player["name_en"],
            player["source_id"], "基本情報 > 英語表記",
            "B.LEAGUE公式プロフィールの英語表記", "SUPPORTED",
        )
        add_evidence(
            "Person", player["person_id"], "birth_date", player["birth_date"],
            player["source_id"], "基本情報 > 生年月日",
            "B.LEAGUE公式プロフィールの生年月日", "SUPPORTED",
        )
        add_evidence(
            "Career", player["pro_career_id"], "organization_id",
            player["pro_org_id"], player["source_id"],
            "クラブ所属履歴 > 最新掲載",
            f"{player['pro_org_name']}を最新の所属履歴として掲載", "SUPPORTED",
            "開始・終了時期は今回の最小取込対象外",
        )
        add_evidence(
            "Career", player["pro_career_id"], "role", "Player",
            player["source_id"], "選手プロフィール",
            "B.LEAGUE選手プロフィールとして掲載", "SUPPORTED",
        )
        if player.get("pro_start"):
            add_evidence(
                "Career", player["pro_career_id"], "start",
                player["pro_start"], "B2S0011",
                "本文冒頭 > 2026-27シーズンの選手契約",
                "レバンガ北海道が2026-27シーズンの新規入団を発表",
                "SUPPORTED",
            )
        add_evidence(
            "Career", player["high_school_career_id"], "organization_id",
            "ORG000010", "B2S0000", "出身高校フィルターと選手カード",
            "福岡第一高等学校の絞り込み結果に掲載", "PARTIAL",
            "選手詳細または高校・大会公式資料で再確認する",
        )
        add_evidence(
            "Career", player["high_school_career_id"], "role", "Player",
            "B2S0000", "福岡第一高等学校の選手一覧",
            "B.LEAGUE選手として公式一覧に掲載", "PARTIAL",
            "高校時の選手登録を別資料で再確認する",
        )

        issues.append(
            {
                "issue_id": f"B2I{issue_number:04d}",
                "person_id": player["person_id"],
                "related_id": player["high_school_career_id"],
                "issue_type": "HIGH_SCHOOL_EVIDENCE",
                "status": "HOLD",
                "description": "公式フィルターで福岡第一との関係は確認できるが高校時の登録期間と役割は未確認",
                "next_check": "高校・JBA・大会公式ロスターを確認",
            }
        )
        issue_number += 1
        issues.append(
            {
                "issue_id": f"B2I{issue_number:04d}",
                "person_id": player["person_id"],
                "related_id": player["person_id"],
                "issue_type": "EDUCATION_DISPLAY_ONLY",
                "status": "HOLD",
                "description": f"B.LEAGUEの出身校表示は{player['education_display']}だが競技Careerと期間は未確認",
                "next_check": "大学・競技団体の公式ロスターを確認",
            }
        )
        issue_number += 1

        decisions.extend(
            [
                {
                    "decision_id": f"B2D{decision_number:04d}",
                    "entity_type": "Person",
                    "entity_id": player["person_id"],
                    "decision": "READY_FOR_VERIFIED_REVIEW",
                    "eligible_fields": "name|name_en|birth_date",
                    "held_fields": "",
                    "reason": "B.LEAGUE公式選手プロフィールで直接確認",
                    "reviewed_at": ACCESSED_AT,
                },
                {
                    "decision_id": f"B2D{decision_number + 1:04d}",
                    "entity_type": "Career",
                    "entity_id": player["pro_career_id"],
                    "decision": "READY_FOR_VERIFIED_REVIEW",
                    "eligible_fields": (
                        "organization_id|role|start"
                        if player.get("pro_start")
                        else "organization_id|role"
                    ),
                    "held_fields": (
                        "end" if player.get("pro_start") else "start|end"
                    ),
                    "reason": "B.LEAGUE公式のクラブ所属履歴で確認",
                    "reviewed_at": ACCESSED_AT,
                },
                {
                    "decision_id": f"B2D{decision_number + 2:04d}",
                    "entity_type": "Career",
                    "entity_id": player["high_school_career_id"],
                    "decision": "HOLD_CANDIDATE",
                    "eligible_fields": "",
                    "held_fields": "organization_id|role|start|end",
                    "reason": "高校時の登録を示す個別公式資料が未確認",
                    "reviewed_at": ACCESSED_AT,
                },
            ]
        )
        decision_number += 3

    issues.append(
        {
            "issue_id": f"B2I{issue_number:04d}",
            "person_id": "P000043",
            "related_id": "C000145|C000212",
            "issue_type": "CURRENT_CLUB_CONFLICT",
            "status": "RESOLVED",
            "description": "Excel原本C000145の2026-27滋賀所属はB.LEAGUEとレバンガ北海道の公式発表に一致しないため不採用",
            "next_check": "候補側はC000212として2026年レバンガ北海道加入を保持",
        }
    )

    write_csv(
        "evidence_records.csv",
        [
            "record_id", "entity_type", "entity_id", "field_name",
            "candidate_value", "source_id", "source_locator",
            "evidence_summary", "assessment", "checked_at", "issue_note",
        ],
        evidence,
    )
    write_csv(
        "issues.csv",
        [
            "issue_id", "person_id", "related_id", "issue_type", "status",
            "description", "next_check",
        ],
        issues,
    )
    write_csv(
        "qa_decisions.csv",
        [
            "decision_id", "entity_type", "entity_id", "decision",
            "eligible_fields", "held_fields", "reason", "reviewed_at",
        ],
        decisions,
    )


if __name__ == "__main__":
    main()
