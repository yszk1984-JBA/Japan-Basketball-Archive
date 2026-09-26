#!/usr/bin/env python3
"""Build Batch 019 Wave 2 (桐光学園高等学校, 第2弾 学校1/12) CANDIDATE data.

See scripts/batch_019_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402

PLAYERS = [
    {
        "person_id": "P000197", "name": "須藤 昂矢", "bleague_id": 32956, "birth_date": "1997-05-15",
        "university": "ORG000124", "club": "ORG000055", "club_start": "2020",
        "club_locator": "「2026-27 横浜BC」〜「2020-21 横浜BC」", "club_locator_short": "2020-21〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2020-21シーズンからの在籍を確認",
        "pro_gaps": "西宮（2019-20、1シーズン）",
    },
    {
        "person_id": "P000198", "name": "兪 龍海", "bleague_id": 5100000025, "birth_date": "2001-07-09",
        "university": "ORG000136", "club": "ORG000097", "club_start": "2026",
        "club_locator": "「2026-27 三遠」（直前は「2025-26 横浜BC」）", "club_locator_short": "2026-27〜、復帰",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンの三遠復帰を確認（既存の復帰時開始年方針により2026とする）",
        "pro_gaps": "横浜BC（2025-26）・三遠（2023-24〜2024-25、および2020-21）",
        "extra_issues": [{
            "type": "CAREER_TIMELINE_NOTE",
            "description": "兪龍海のクラブ所属履歴は2020-21三遠の次が2023-24三遠で、2021-22・2022-23の行がない。大学在学中の登録（特別指定選手等）の可能性があるが、公式資料で種別を確認していないため推測で記録しない。",
            "next_check": "三遠ネオフェニックス公式の2020-21および2023-24の加入発表で登録種別を確認",
        }],
    },
    {
        "person_id": "P000199", "name": "植松 義也", "bleague_id": 5100000030, "birth_date": "1998-12-18",
        "university": "ORG000124", "club": "ORG000142", "club_start": "2025",
        "club_locator": "「2026-27 大阪」「2025-26 大阪」", "club_locator_short": "2025-26〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認",
        "pro_gaps": "琉球（2022-23〜2024-25、3シーズン）・福岡（2020-21〜2021-22、2シーズン）",
    },
    {
        "person_id": "P000200", "name": "宮本 一樹", "bleague_id": 51000118, "birth_date": "1999-06-17",
        "university": "ORG000136", "club": "ORG000149", "club_start": "2025",
        "club_locator": "「2026-27 富山」「2025-26 富山」", "club_locator_short": "2025-26〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認",
        "pro_gaps": "滋賀（2023-24〜2024-25、2シーズン）・FE名古屋（2021-22〜2022-23、2シーズン）",
    },
]


if __name__ == "__main__":
    build(2, PLAYERS, first_career_seq=644)
