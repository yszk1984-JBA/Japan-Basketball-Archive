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

RESEARCH_ORGANIZATIONS = {
    "ORG000016": "中央大学",
    "ORG000030": "青山学院大学",
    "ORG000015": "東海大学",
    "ORG000032": "South Kent School",
    "ORG000018": "専修大学",
    "ORG000020": "日本体育大学",
    "ORG000031": "拓殖大学",
}

RESEARCH_CAREERS = [
    {
        "career_id": "C000070",
        "person_id": "P000038",
        "organization_id": "ORG000016",
        "role": "Player",
        "start": "2020",
        "end": "",
    },
    {
        "career_id": "C000069",
        "person_id": "P000037",
        "organization_id": "ORG000030",
        "role": "Player",
        "start": "",
        "end": "",
    },
    {
        "career_id": "C000073",
        "person_id": "P000041",
        "organization_id": "ORG000015",
        "role": "Player",
        "start": "",
        "end": "",
    },
    {
        "career_id": "C000074",
        "person_id": "P000042",
        "organization_id": "ORG000032",
        "role": "Player",
        "start": "2008",
        "end": "2009",
    },
    {
        "career_id": "C000071",
        "person_id": "P000039",
        "organization_id": "ORG000018",
        "role": "Player",
        "start": "",
        "end": "",
    },
    {
        "career_id": "C000075",
        "person_id": "P000043",
        "organization_id": "ORG000015",
        "role": "Player",
        "start": "2019",
        "end": "",
    },
    {
        "career_id": "C000067",
        "person_id": "P000035",
        "organization_id": "ORG000020",
        "role": "Player",
        "start": "2020",
        "end": "2022",
    },
    {
        "career_id": "C000072",
        "person_id": "P000040",
        "organization_id": "ORG000031",
        "role": "Player",
        "start": "",
        "end": "",
    },
    {
        "career_id": "C000068",
        "person_id": "P000036",
        "organization_id": "ORG000020",
        "role": "Player",
        "start": "2018",
        "end": "",
    },
]

RESEARCH_SOURCES = [
    {
        "source_id": "B2S0012",
        "title": "第95回天皇杯 福岡第一高等学校ロスター",
        "publisher": "日本バスケットボール協会",
        "url": "https://zennihon2019-20.japanbasketball.jp/team/fukuoka-men/",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0013",
        "title": "ウインターカップ2019 現地レポート21",
        "publisher": "日本バスケットボール協会",
        "url": "https://wintercup2019.japanbasketball.jp/report/1119/",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0014",
        "title": "第72回インカレ 中央大学ロスター",
        "publisher": "全日本大学バスケットボール連盟",
        "url": "https://jubf.jp/game/university-detail/id/122/type/intercollege/y/2020/s/men",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0015",
        "title": "第75回インカレ 中央大学ロスター",
        "publisher": "全日本大学バスケットボール連盟",
        "url": "https://jubf.jp/game/university-detail/id/122/type/intercollege/y/2023/s/men",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0016",
        "title": "平成22年度男子U-18日本代表 第4次強化合宿",
        "publisher": "日本バスケットボール協会",
        "url": "https://japanbasketball.jp/event/news_detail-php-news_id%3D1029.html",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0017",
        "title": "第19回日・韓・中ジュニア交流競技会 日本代表メンバー",
        "publisher": "日本バスケットボール協会",
        "url": "https://japanbasketball.jp/event/news_detail-php-news_id%3D4735.html",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0018",
        "title": "第6回東アジア競技大会 男子日本代表選手発表",
        "publisher": "日本バスケットボール協会",
        "url": "https://japanbasketball.jp/japan/4853",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0019",
        "title": "福岡第一高等学校 学校案内2022",
        "publisher": "福岡第一高等学校",
        "url": "https://f.f-parama.ed.jp/wp-content/uploads/2022/01/panf2022.pdf",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0020",
        "title": "2011年度 松前重義賞 受領者一覧",
        "publisher": "東海大学",
        "url": "https://www.u-tokai.ac.jp/uploads/2021/03/2011univ.pdf",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0021",
        "title": "第1回奨学生の近況報告 並里成",
        "publisher": "スラムダンク奨学金事務局",
        "url": "https://slamdunk-sc.shueisha.co.jp/report/report01.html",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0022",
        "title": "並里レポート vol.3",
        "publisher": "スラムダンク奨学金事務局",
        "url": "https://slamdunk-sc.shueisha.co.jp/sp/common/data/namisato_vol3.pdf",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0023",
        "title": "オールジャパン2011 東海大学ボックススコア",
        "publisher": "日本バスケットボール協会",
        "url": "https://japanbasketball.jp/alljapan/2011/pbp_team-php-game_id%3D10222%26q%3D95.html",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0024",
        "title": "第22回FIBA ASIA U-18男子日本代表チーム",
        "publisher": "日本バスケットボール協会",
        "url": "https://japanbasketball.jp/event/fac_u18_men/2012/japan/",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0025",
        "title": "第67回インカレ 専修大学ロスター",
        "publisher": "全日本大学バスケットボール連盟",
        "url": "https://jubf.jp/game/university-detail/id/25/type/intercollege/y/2015/s/men",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0026",
        "title": "第68回インカレ 専修大学ロスター",
        "publisher": "全日本大学バスケットボール連盟",
        "url": "https://jubf.jp/game/university-detail/id/25/type/intercollege/y/2016/s/men",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0027",
        "title": "平成28年度男子U-18日本代表候補メンバー表",
        "publisher": "日本バスケットボール協会",
        "url": "https://www.japanbasketball.jp/wp-content/uploads/H28_U18men_member_camp_161122.pdf",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0028",
        "title": "平成30年度男子U18日本代表 第3次強化合宿",
        "publisher": "日本バスケットボール協会",
        "url": "https://japanbasketball.jp/japan/44945",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0029",
        "title": "第71回インカレ 東海大学ロスター",
        "publisher": "全日本大学バスケットボール連盟",
        "url": "https://jubf.jp/game/university-detail/id/44/type/intercollege/y/2019/s/men",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0030",
        "title": "第74回インカレ 東海大学ロスター",
        "publisher": "全日本大学バスケットボール連盟",
        "url": "https://jubf.jp/game/university-detail/id/44/type/intercollege/y/2022/s/men",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0031",
        "title": "第72回インカレ 日本体育大学ロスター",
        "publisher": "全日本大学バスケットボール連盟",
        "url": "https://jubf.jp/game/university-detail/id/5/type/intercollege/y/2020/s/men",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0032",
        "title": "2022-23シーズン 小川麻斗選手 新加入のお知らせ",
        "publisher": "千葉ジェッツ",
        "url": "https://chibajets.jp/news/detail/id=21415",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0033",
        "title": "第73回インカレ 拓殖大学ロスター",
        "publisher": "全日本大学バスケットボール連盟",
        "url": "https://jubf.jp/game/university-detail/id/35/type/intercollege/y/2021/s/men",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0034",
        "title": "第74回インカレ 拓殖大学ロスター",
        "publisher": "全日本大学バスケットボール連盟",
        "url": "https://jubf.jp/game/university-detail/id/35/type/intercollege/y/2022/s/men",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0035",
        "title": "第70回インカレ 日本体育大学ロスター",
        "publisher": "全日本大学バスケットボール連盟",
        "url": "https://jubf.jp/game/university-detail/id/5/type/intercollege/y/2018/s/men",
        "accessed_at": ACCESSED_AT,
    },
    {
        "source_id": "B2S0036",
        "title": "第73回インカレ 日本体育大学ロスター",
        "publisher": "全日本大学バスケットボール連盟",
        "url": "https://jubf.jp/game/university-detail/id/5/type/intercollege/y/2021/s/men",
        "accessed_at": ACCESSED_AT,
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
    organizations.update(RESEARCH_ORGANIZATIONS)
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
    careers.extend(RESEARCH_CAREERS)
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
    sources.extend(RESEARCH_SOURCES)
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

    def find_issue(related_id: str) -> dict[str, str]:
        return next(row for row in issues if row["related_id"] == related_id)

    def find_decision(entity_id: str) -> dict[str, str]:
        return next(row for row in decisions if row["entity_id"] == entity_id)

    # 内尾聡理：高校ロスターと中央大学インカレ登録を直接確認。
    for field_name, value, summary in [
        ("organization_id", "ORG000010", "福岡第一高等学校のプレーヤー一覧に掲載"),
        ("role", "Player", "福岡第一高等学校の選手として公式ロスターに掲載"),
        ("jersey_number", "54", "公式ロスターの背番号"),
        ("height_cm", "183", "公式ロスターの登録身長"),
    ]:
        add_evidence(
            "Career", "C000057", field_name, value, "B2S0012",
            "福岡第一高等学校 > プレーヤー > No.54 内尾聡理",
            summary, "SUPPORTED",
        )
    add_evidence(
        "Career", "C000057", "activity_date", "2019-12-28", "B2S0013",
        "本文第2段落 > #54内尾聡理",
        "ウインターカップ準決勝での活動を大会公式レポートが記載",
        "SUPPORTED", "Career終了日を意味しない",
    )
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000016", "B2S0014", "中央大学 ROSTER > No.2", "中央大学ロスターに掲載"),
        ("role", "Player", "B2S0014", "中央大学 ROSTER > No.2", "登録選手として掲載"),
        ("start", "2020", "B2S0014", "中央大学 ROSTER > 1年", "2020年大会で1年生として登録"),
        ("jersey_number", "2", "B2S0014", "中央大学 ROSTER > No.2", "大学時の背番号"),
        ("position", "SF", "B2S0014", "中央大学 ROSTER > Pos.", "大学時の登録ポジション"),
        ("height_cm", "183", "B2S0014", "中央大学 ROSTER > 身長", "大学時の登録身長"),
        ("latest_activity_year", "2023", "B2S0015", "中央大学 ROSTER > 4年 No.2", "2023年大会で4年生として登録"),
    ]:
        add_evidence(
            "Career", "C000070", field_name, value, source_id, locator,
            summary, "SUPPORTED", "卒業・終了年月は別途確認" if field_name == "latest_activity_year" else "",
        )

    # 鵤誠司：高校2・3年時と青山学院大学2年時をJBA公式発表で確認。
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000010", "B2S0016", "参加選手 > 鵤誠司", "福岡第一高校2年として掲載"),
        ("role", "Player", "B2S0016", "男子U-18日本代表強化合宿 > 選手", "選手として掲載"),
        ("grade", "2年", "B2S0016", "参加選手 > 所属・学年", "2011年2月時点の学年"),
        ("grade", "3年", "B2S0017", "日本代表選手 > #9 鵤誠司", "2011年8月時点の学年"),
    ]:
        add_evidence(
            "Career", "C000056", field_name, value, source_id, locator,
            summary, "SUPPORTED", "入学・卒業年月は直接示さない" if field_name == "grade" else "",
        )
    for field_name, value, summary in [
        ("organization_id", "ORG000030", "青山学院大学2年として掲載"),
        ("role", "Player", "男子日本代表選手として大学所属を掲載"),
        ("grade", "2年", "2013年度時点の学年"),
    ]:
        add_evidence(
            "Career", "C000069", field_name, value, "B2S0018",
            "男子日本代表選手 > #15 鵤誠司",
            summary, "SUPPORTED", "大学在籍開始・終了年月は直接示さない" if field_name == "grade" else "",
        )

    # 狩野祐介：高校卒業関係と東海大学男子部所属を公式資料で確認。
    add_evidence(
        "Career", "C000060", "organization_id", "ORG000010", "B2S0019",
        "プロバスケットボール選手欄 > 狩野祐介",
        "福岡第一高等学校普通科卒として掲載", "SUPPORTED",
        "高校バスケットボール部での役割・期間は示さない",
    )
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000015", "B2S0020", "バスケットボール部（男子）> 狩野祐介", "東海大学公式資料に掲載"),
        ("role", "Player", "B2S0020", "バスケットボール部（男子）> 狩野祐介", "男子バスケットボール部員として掲載"),
        ("grade", "3年", "B2S0020", "体育学部3年", "2011年度の学年"),
        ("award", "第87回関東大学リーグ戦MIP賞", "B2S0020", "受領者一覧 > 狩野祐介", "大学公式の受賞記録"),
        ("jersey_number", "33", "B2S0023", "東海大学ボックススコア > No.33", "公式戦の背番号"),
    ]:
        add_evidence(
            "Career", "C000073", field_name, value, source_id, locator,
            summary, "SUPPORTED", "大学在籍開始・終了年月は直接示さない" if field_name == "grade" else "",
        )

    # 並里成：福岡第一からSouth Kent Schoolを経て2009年にプロ入りした経路を確認。
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000010", "B2S0019", "プロバスケットボール選手欄 > 並里成", "福岡第一高等学校普通科卒として掲載"),
        ("role", "Player", "B2S0022", "本文 > 福岡第一高校在籍時と日本での先発経験", "福岡第一高校在籍時の競技経験を記載"),
    ]:
        add_evidence(
            "Career", "C000061", field_name, value, source_id, locator,
            summary, "SUPPORTED" if field_name == "organization_id" else "PARTIAL",
            "高校在籍開始・終了年月と高校チームでの役割を直接示さない",
        )
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000032", "B2S0021", "略歴 > サウスケントスクール", "留学先を公式奨学金ページに掲載"),
        ("role", "Player", "B2S0022", "本文 > South KentでのPG・出場記録", "同校チームでの競技参加を記載"),
        ("start", "2008", "B2S0021", "略歴 > 2008年3月入学", "入学年月を掲載"),
        ("end", "2009", "B2S0021", "略歴 > 2009年5月卒業", "卒業年月を掲載"),
    ]:
        add_evidence(
            "Career", "C000074", field_name, value, source_id, locator,
            summary, "SUPPORTED",
        )

    # 渡辺竜之佑：高校3年時と専修大学3・4年時を公式ロスターで確認。
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000010", "B2S0024", "日本代表チーム > No.10 渡辺竜之佑", "福岡第一高校3年として掲載"),
        ("role", "Player", "B2S0024", "平成24年度男子U-18日本代表チーム > 選手", "選手として掲載"),
        ("grade", "1年", "B2S0016", "参加メンバー > 渡辺竜之佑", "2011年2月時点の学年"),
        ("grade", "3年", "B2S0024", "所属 > 福岡第一高校3年", "2012年8月時点の学年"),
        ("position", "SF", "B2S0024", "P > SF", "高校3年時の登録ポジション"),
        ("height_cm", "185", "B2S0024", "身長 > 185cm", "高校3年時の登録身長"),
    ]:
        add_evidence(
            "Career", "C000058", field_name, value, source_id, locator,
            summary, "SUPPORTED", "高校の開始・終了年月は直接示さない",
        )
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000018", "B2S0025", "専修大学 ROSTER > No.6", "専修大学ロスターに掲載"),
        ("role", "Player", "B2S0025", "専修大学 ROSTER > No.6", "登録選手として掲載"),
        ("grade", "3年", "B2S0025", "学年 > 3年", "2015年大会時の学年"),
        ("grade", "4年", "B2S0026", "学年 > 4年", "2016年大会時の学年"),
        ("jersey_number", "6", "B2S0026", "No. > 6", "大学4年時の背番号"),
        ("position", "G", "B2S0026", "Pos. > G", "大学4年時の登録ポジション"),
        ("height_cm", "187", "B2S0026", "身長 > 187cm", "大学4年時の登録身長"),
    ]:
        add_evidence(
            "Career", "C000071", field_name, value, source_id, locator,
            summary, "SUPPORTED", "大学の開始・終了年月は直接示さない" if field_name == "grade" else "",
        )

    # 松崎裕樹：高校1・3年時と東海大学1・4年時を公式資料で確認。
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000010", "B2S0027", "選手 > 松崎裕樹", "福岡第一高校1年として掲載"),
        ("role", "Player", "B2S0027", "男子U-18日本代表候補選手", "選手として掲載"),
        ("grade", "1年", "B2S0027", "所属 > 福岡第一高校1年", "2016年11月時点の学年"),
        ("grade", "3年", "B2S0028", "選手 > 松崎裕樹", "2018年6月時点の学年"),
        ("position", "SF", "B2S0028", "選手 > SF", "高校3年時の登録ポジション"),
        ("height_cm", "192", "B2S0028", "ダウンロード資料 > 身長", "高校3年時の登録身長"),
    ]:
        add_evidence(
            "Career", "C000062", field_name, value, source_id, locator,
            summary, "SUPPORTED", "高校の開始・終了年月は直接示さない" if field_name == "grade" else "",
        )
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000015", "B2S0029", "東海大学 ROSTER > No.24", "東海大学ロスターに掲載"),
        ("role", "Player", "B2S0029", "東海大学 ROSTER > No.24", "登録選手として掲載"),
        ("start", "2019", "B2S0029", "学年 > 1年", "2019年大会で1年生として登録"),
        ("grade", "4年", "B2S0030", "学年 > 4年", "2022年大会時の学年"),
        ("jersey_number", "24", "B2S0030", "No. > 24", "大学4年時の背番号"),
        ("position", "F", "B2S0030", "Pos. > F", "大学4年時の登録ポジション"),
        ("height_cm", "192", "B2S0030", "身長 > 192cm", "大学4年時の登録身長"),
    ]:
        add_evidence(
            "Career", "C000075", field_name, value, source_id, locator,
            summary, "SUPPORTED", "大学の終了年月は直接示さない" if field_name == "grade" else "",
        )

    # 小川麻斗：高校公式ロスター、日体大登録、2022年12月の部活動退部を確認。
    for field_name, value, summary in [
        ("organization_id", "ORG000010", "福岡第一高等学校のプレーヤー一覧に掲載"),
        ("role", "Player", "福岡第一高等学校の選手として公式ロスターに掲載"),
        ("jersey_number", "46", "高校時の公式ロスター背番号"),
        ("height_cm", "175", "高校時の公式ロスター登録身長"),
    ]:
        add_evidence(
            "Career", "C000054", field_name, value, "B2S0012",
            "福岡第一高等学校 > プレーヤー > No.46 小川麻斗",
            summary, "SUPPORTED",
        )
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000020", "B2S0031", "日本体育大学 ROSTER > No.23", "日本体育大学ロスターに掲載"),
        ("role", "Player", "B2S0031", "日本体育大学 ROSTER > No.23", "登録選手として掲載"),
        ("start", "2020", "B2S0031", "学年 > 1年", "2020年大会で1年生として登録"),
        ("jersey_number", "23", "B2S0031", "No. > 23", "大学1年時の背番号"),
        ("position", "PG", "B2S0031", "Pos. > PG", "大学1年時の登録ポジション"),
        ("height_cm", "175", "B2S0031", "身長 > 175cm", "大学1年時の登録身長"),
        ("end", "2022", "B2S0032", "本文 > 2022年12月23日に男子部を退部", "大学男子バスケットボール部からの退部を公式発表"),
    ]:
        add_evidence(
            "Career", "C000067", field_name, value, source_id, locator,
            summary, "SUPPORTED", "学籍は継続と明記。Career終了は男子部での競技活動を指す" if field_name == "end" else "",
        )

    # 神田壮一郎：高校公式ロスターと拓殖大学2・3年時を確認。
    for field_name, value, summary in [
        ("organization_id", "ORG000010", "福岡第一高等学校のプレーヤー一覧に掲載"),
        ("role", "Player", "福岡第一高等学校の選手として公式ロスターに掲載"),
        ("jersey_number", "13", "高校時の公式ロスター背番号"),
        ("height_cm", "190", "高校時の公式ロスター登録身長"),
    ]:
        add_evidence(
            "Career", "C000059", field_name, value, "B2S0012",
            "福岡第一高等学校 > プレーヤー > No.13 神田壮一郎",
            summary, "SUPPORTED",
        )
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000031", "B2S0033", "拓殖大学 ROSTER > No.0", "拓殖大学ロスターに掲載"),
        ("role", "Player", "B2S0033", "拓殖大学 ROSTER > No.0", "登録選手として掲載"),
        ("grade", "2年", "B2S0033", "学年 > 2年", "2021年大会時の学年"),
        ("grade", "3年", "B2S0034", "学年 > 3年", "2022年大会時の学年"),
        ("jersey_number", "0", "B2S0034", "No. > 0", "大学3年時の背番号"),
        ("position", "PF", "B2S0034", "Pos. > PF", "大学3年時の登録ポジション"),
        ("height_cm", "190", "B2S0034", "身長 > 190cm", "大学3年時の登録身長"),
    ]:
        add_evidence(
            "Career", "C000072", field_name, value, source_id, locator,
            summary, "SUPPORTED", "大学の開始・終了年月は直接示さない" if field_name == "grade" else "",
        )

    # 井手拓実：日体大1・4年時の公式ロスターと福岡第一出身を確認。
    add_evidence(
        "Career", "C000055", "organization_id", "ORG000010", "B2S0035",
        "日本体育大学 ROSTER > No.30 井手拓実 > 出身校",
        "JUBF公式ロスターに出身校を福岡第一高と掲載", "SUPPORTED",
        "高校バスケットボール部の役割と期間は直接示さない",
    )
    for field_name, value, source_id, locator, summary in [
        ("organization_id", "ORG000020", "B2S0035", "日本体育大学 ROSTER > No.30", "日本体育大学ロスターに掲載"),
        ("role", "Player", "B2S0035", "日本体育大学 ROSTER > No.30", "登録選手として掲載"),
        ("start", "2018", "B2S0035", "学年 > 1年", "2018年大会で1年生として登録"),
        ("grade", "4年", "B2S0036", "学年 > 4年", "2021年大会時の学年"),
        ("jersey_number", "28", "B2S0036", "No. > 28", "大学4年時の背番号"),
        ("position", "PG", "B2S0036", "Pos. > PG", "大学4年時の登録ポジション"),
        ("height_cm", "175", "B2S0036", "身長 > 175cm", "大学4年時の登録身長"),
    ]:
        add_evidence(
            "Career", "C000068", field_name, value, source_id, locator,
            summary, "SUPPORTED", "大学の終了年月は直接示さない" if field_name == "grade" else "",
        )

    high_school_updates = {
        "C000057": ("organization_id|role|jersey_number|height_cm|activity_date", "start|end", "高校公式ロスターと大会公式レポートで確認"),
        "C000056": ("organization_id|role|grade", "start|end", "JBA公式U-18資料で高校2・3年時を確認"),
        "C000060": ("organization_id", "role|start|end", "学校公式パンフレットで卒業関係を確認"),
        "C000061": ("organization_id", "role|start|end", "学校公式パンフレットで卒業関係を確認"),
        "C000058": ("organization_id|role|grade|position|height_cm", "start|end", "JBA公式U-18資料で高校3年時を確認"),
        "C000062": ("organization_id|role|grade|position|height_cm", "start|end", "JBA公式U-18資料で高校1・3年時を確認"),
        "C000054": ("organization_id|role|jersey_number|height_cm", "start|end", "JBA公式大会ロスターで確認"),
        "C000059": ("organization_id|role|jersey_number|height_cm", "start|end", "JBA公式大会ロスターで確認"),
        "C000055": ("organization_id", "role|start|end", "JUBF公式ロスターの出身校欄で確認"),
    }
    for career_id, (eligible, held, reason) in high_school_updates.items():
        decision = find_decision(career_id)
        decision["decision"] = "READY_FOR_VERIFIED_REVIEW"
        decision["eligible_fields"] = eligible
        decision["held_fields"] = held
        decision["reason"] = reason
        issue = find_issue(career_id)
        issue["status"] = "HOLD"
        issue["description"] = f"確認済み項目は{eligible}。未確認項目は{held}"
        issue["next_check"] = "高校の入学・卒業または大会登録期間を示す公式資料を確認"

    university_decisions = [
        ("C000070", "organization_id|role|start|jersey_number|position|height_cm|latest_activity_year", "end", "JUBF公式2020・2023年ロスターで確認"),
        ("C000069", "organization_id|role|grade", "start|end", "JBA公式の2013年度日本代表資料で確認"),
        ("C000073", "organization_id|role|grade|award|jersey_number", "start|end", "東海大学公式受賞記録とJBA公式戦記録で確認"),
        ("C000074", "organization_id|role|start|end", "", "スラムダンク奨学金公式の略歴と競技記録で確認"),
        ("C000071", "organization_id|role|grade|jersey_number|position|height_cm", "start|end", "JUBF公式2015・2016年ロスターで確認"),
        ("C000075", "organization_id|role|start|grade|jersey_number|position|height_cm", "end", "JUBF公式2019・2022年ロスターで確認"),
        ("C000067", "organization_id|role|start|end|jersey_number|position|height_cm", "", "JUBF公式ロスターと千葉ジェッツ公式退部発表で確認"),
        ("C000072", "organization_id|role|grade|jersey_number|position|height_cm", "start|end", "JUBF公式2021・2022年ロスターで確認"),
        ("C000068", "organization_id|role|start|grade|jersey_number|position|height_cm", "end", "JUBF公式2018・2021年ロスターで確認"),
    ]
    for career_id, eligible, held, reason in university_decisions:
        decisions.append(
            {
                "decision_id": f"B2D{decision_number:04d}",
                "entity_type": "Career",
                "entity_id": career_id,
                "decision": "READY_FOR_VERIFIED_REVIEW",
                "eligible_fields": eligible,
                "held_fields": held,
                "reason": reason,
                "reviewed_at": ACCESSED_AT,
            }
        )
        decision_number += 1

    for person_id in ["P000038", "P000037", "P000041", "P000042", "P000039", "P000043", "P000035", "P000040", "P000036"]:
        display_issue = next(
            row for row in issues
            if row["person_id"] == person_id
            and row["issue_type"] == "EDUCATION_DISPLAY_ONLY"
        )
        display_issue["status"] = "RESOLVED"
        display_issue["next_check"] = "個別Careerと公式資料へ置換済み"

    for person_id, career_id, description in [
        ("P000038", "C000070", "中央大学は2020年1年・2023年4年を確認したが終了年月は未確認"),
        ("P000037", "C000069", "青山学院大学2年時の所属を確認したが開始・終了年月は未確認"),
        ("P000041", "C000073", "東海大学3年時の所属を確認したが開始・終了年月は未確認"),
        ("P000042", "C000074", "2009年7月のプロ入りは確認したが、その後を含む大学Career不存在の包括的証明ではない"),
        ("P000039", "C000071", "専修大学3・4年時の所属を確認したが開始・終了年月は未確認"),
        ("P000043", "C000075", "東海大学1・4年時の所属を確認したが終了年月は未確認"),
        ("P000040", "C000072", "拓殖大学2・3年時の所属を確認したが開始・終了年月は未確認"),
        ("P000036", "C000068", "日本体育大学1・4年時の所属を確認したが終了年月は未確認"),
    ]:
        issues.append(
            {
                "issue_id": f"B2I{issue_number:04d}",
                "person_id": person_id,
                "related_id": career_id,
                "issue_type": "CAREER_PERIOD_OR_ABSENCE",
                "status": "HOLD",
                "description": description,
                "next_check": "期間を直接示す公式資料がある場合のみ更新",
            }
        )
        issue_number += 1

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
