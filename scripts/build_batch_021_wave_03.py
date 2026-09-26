#!/usr/bin/env python3
"""Build Batch 021 Wave 3 (中部大学第一高等学校, 第2弾 学校3/12) CANDIDATE data.

See scripts/batch_021_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_021_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000217',
  'name': '吉本 大心',
  'bleague_id': 7482,
  'birth_date': '2002-04-23',
  'university': 'ORG000031',
  'club': 'ORG000191',
  'club_start': '2026',
  'club_locator': '「2026-27 三重」（履歴はこの1行のみ）',
  'club_locator_short': '2026-27〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認'},
 {'person_id': 'P000218',
  'name': 'ワン ウェイジャ',
  'bleague_id': 5100000041,
  'birth_date': '1998-09-03',
  'university': 'ORG000214',
  'club': 'ORG000182',
  'club_start': '2025',
  'club_locator': '「2026-27 青森」「2025-26 青森」',
  'club_locator_short': '2025-26〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認',
  'pro_gaps': '福島（2024-25）・秋田（2020-21〜2023-24、4シーズン）'},
 {'person_id': 'P000219',
  'name': '中村 拓人',
  'bleague_id': 5100000023,
  'birth_date': '2001-03-03',
  'university': 'ORG000128',
  'club': 'ORG000143',
  'club_start': '2025',
  'club_locator': '「2026-27 群馬」「2025-26 群馬」',
  'club_locator_short': '2025-26〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認',
  'pro_gaps': '広島（2021-22〜2024-25、4シーズン）・北海道（2020-21）'}]


if __name__ == "__main__":
    build(3, PLAYERS, first_career_seq=704, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
