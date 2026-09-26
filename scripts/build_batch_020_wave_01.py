#!/usr/bin/env python3
"""Build Batch 020 Wave 1 (船橋市立船橋高等学校, 第2弾 学校2/12) CANDIDATE data.

See scripts/batch_020_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_020_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [
    {
        "person_id": "P000201", "name": "平良 彰吾", "bleague_id": 30459, "birth_date": "1997-04-02",
        "university": "ORG000031", "club": "ORG000130", "club_start": "2026",
        "club_locator": "「2026-27 三河」（直前は「2025-26 琉球」）", "club_locator_short": "2026-27〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認",
        "pro_gaps": "琉球（2024-25〜2025-26）・横浜EX（2023-24〜2024-25。2024-25は琉球と両方の行がありシーズン途中の移籍とみられるが時期は未確認）・湘南（2022-23）・品川（2021-22）・福岡（2019-20〜2020-21）。いずれも所属履歴上の略称で、正式クラブ名は未確認",
    },
    {
        "person_id": "P000202", "name": "古牧 昌也", "bleague_id": 12500, "birth_date": "1993-06-19",
        "university": "ORG000121", "club": "ORG000183", "club_start": "2026",
        "club_locator": "「2026-27 埼玉」（直前は「2025-26 奈良」）", "club_locator_short": "2026-27〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認（所属履歴上の略称「埼玉」、選手一覧の現所属表記はさいたまブロンコス）",
        "pro_gaps": "奈良（2022-23〜2025-26）・横浜BC（2021-22）・群馬（2018-19〜2020-21）・東京Z（2017-18）",
    },
    {
        "person_id": "P000203", "name": "野﨑 由之", "bleague_id": 51000136, "birth_date": "2000-02-08",
        "university": "ORG000018", "club": "ORG000149", "club_start": "2021",
        "club_locator": "「2026-27 富山」〜「2021-22 富山」（履歴は富山のみ）", "club_locator_short": "2021-22〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2021-22シーズンからの在籍を確認",
    },
    {
        "person_id": "P000204", "name": "赤穂 雷太", "bleague_id": 30465, "birth_date": "1998-08-28",
        "university": "ORG000030", "club": "ORG000137", "club_start": "2023",
        "club_locator": "「2026-27 秋田」〜「2023-24 秋田」", "club_locator_short": "2023-24〜",
        "start_summary": "B.LEAGUE公式のクラブ所属履歴で2023-24シーズンからの在籍を確認",
        "pro_gaps": "横浜BC（2022-23）・千葉J（2020-21〜2021-22）・横浜（2019-20。所属履歴上は「横浜」のみで、どのクラブを指すかは未確認）",
    },
]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=656, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
