#!/usr/bin/env python3
"""Build Batch 019 Wave 1 (桐光学園高等学校, 第2弾 学校1/12) CANDIDATE data.

See scripts/batch_019_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402

PLAYERS = [
    {
        "person_id": "P000193", "name": "伊藤 治輝", "bleague_id": 49518, "birth_date": "2002-09-15",
        "university": "ORG000124", "club": "ORG000180", "club_start": "2025",
        "club_locator": "「2026-27 FE名古屋」「2025-26 FE名古屋」", "club_locator_short": "2025-26〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認",
        "pro_gaps": "金沢（2024-25、1シーズン。クラブ正式名は所属履歴上の略称のみで未確認）",
    },
    {
        "person_id": "P000194", "name": "オドゲレル トルガ", "bleague_id": 51000663, "birth_date": "2003-06-03",
        "university": "ORG000030", "club": "ORG000090", "club_start": "2026",
        "club_locator": "「2026-27 横浜EX」（履歴はこの1行のみ）", "club_locator_short": "2026-27〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認",
    },
    {
        "person_id": "P000195", "name": "小針 幸也", "bleague_id": 51000252, "birth_date": "1999-05-18",
        "university": "ORG000210", "club": "ORG000106", "club_start": "2025",
        "club_locator": "「2026-27 琉球」「2025-26 琉球」", "club_locator_short": "2025-26〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認",
        "pro_gaps": "川崎（2024-25、1シーズン）・長崎（2022-23〜2023-24、2シーズン）",
    },
    {
        "person_id": "P000196", "name": "喜多川 修平", "bleague_id": 8657, "birth_date": "1985-10-01",
        "university": "ORG000018", "club": "ORG000190", "club_start": "2023",
        "club_locator": "「2026-27 越谷」〜「2023-24 越谷」", "club_locator_short": "2023-24〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2023-24シーズンからの在籍を確認",
        "pro_gaps": "宇都宮（2019-20〜2022-23）・栃木（2017-18〜2018-19、所属履歴上の当時表記。batch_010で同一クラブと確認済みの宇都宮ブレックス改称前名称。深掘り時は既存方針どおり当時名称で記録）・琉球（2016-17）",
        "extra_issues": [{
            "type": "PRE_BLEAGUE_HISTORY",
            "description": "喜多川修平のB.LEAGUE公式クラブ所属履歴は2016-17シーズン（B.LEAGUE開幕）以降のみ掲載されている。1985年生まれで大学卒業後にB.LEAGUE開幕前のリーグでプレーしていた可能性があるが、公式資料で未確認のため記録していない。",
            "next_check": "深掘りWaveでNBL・bjリーグ等の当時の公式資料・クラブ公式発表を確認",
        }],
    },
]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=632)
