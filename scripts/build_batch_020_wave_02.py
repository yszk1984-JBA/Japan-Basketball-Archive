#!/usr/bin/env python3
"""Build Batch 020 Wave 2 (船橋市立船橋高等学校, 第2弾 学校2/12) CANDIDATE data.

See scripts/batch_020_common.py for discovery, scope and ID notes.
遠藤祐亮 follows the batch_010 precedent (竹内公輔): continuous tenure
at 栃木ブレックス→宇都宮ブレックス (renamed July 2019, same club) is
registered as one ORG000047 Career starting in the actual join year.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_020_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [
    {
        "person_id": "P000205", "name": "阿部 諒", "bleague_id": 15756, "birth_date": "1995-05-04",
        "university": "ORG000031", "club": "ORG000048", "club_start": "2025",
        "club_locator": "「2026-27 佐賀」「2025-26 佐賀」", "club_locator_short": "2025-26〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認",
        "pro_gaps": "SR渋谷（2024-25、および2017-18）・仙台（2023-24）・島根（2018-19〜2022-23）",
    },
    {
        "person_id": "P000206", "name": "遠藤 祐亮", "bleague_id": 8497, "birth_date": "1989-10-19",
        "university": "ORG000128", "club": "ORG000047", "club_start": "2016",
        "club_locator": "「2026-27 宇都宮」〜「2019-20 宇都宮」「2018-19 栃木」〜「2016-17 栃木」（連続在籍）", "club_locator_short": "2016-17〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2016-17シーズン（栃木ブレックス時代）からの連続在籍を確認。batch_010の竹内公輔と同じく改称前からの加入年を開始年とした",
        "extra_issues": [
            {"type": "ORG_NAME_HISTORY", "related": "C000673",
             "description": "宇都宮ブレックス（ORG000047）は2019年7月に「栃木ブレックス」から改称した（batch_010 issue B10W1I0006で確認済み）。遠藤祐亮は改称前の2016-17から在籍しており、所属履歴も2018-19までは「栃木」表記だが、単一名称スキーマでは改称前の呼称を表現できないため、既存方針どおりORG000047の1件のCareerとして登録した。",
             "next_check": "Organization名称の時系列表現（改称履歴）のスキーマ整備を検討"},
            {"type": "PRE_BLEAGUE_HISTORY",
             "description": "遠藤祐亮のB.LEAGUE公式クラブ所属履歴は2016-17シーズン（B.LEAGUE開幕）以降のみ掲載されている。それ以前の経歴は公式資料で未確認のため記録していない。",
             "next_check": "深掘りWaveでNBL等の当時の公式資料・クラブ公式発表を確認"},
        ],
    },
    {
        "person_id": "P000207", "name": "田中 晴瑛", "bleague_id": 51000435, "birth_date": "2003-02-01",
        "university": "ORG000212", "club": "ORG000149", "club_start": "2024",
        "club_locator": "「2026-27 富山」〜「2024-25 富山」（履歴は富山のみ）", "club_locator_short": "2024-25〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの在籍を確認",
    },
    {
        "person_id": "P000208", "name": "市場 脩斗", "bleague_id": 51000446, "birth_date": "2003-02-14",
        "university": "ORG000018", "club": "ORG000092", "club_start": "2025",
        "club_locator": "「2026-27 北海道」「2025-26 北海道」", "club_locator_short": "2025-26〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認",
        "pro_gaps": "越谷（2024-25、1シーズン）",
    },
]


if __name__ == "__main__":
    build(2, PLAYERS, first_career_seq=668, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
