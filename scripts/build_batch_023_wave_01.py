#!/usr/bin/env python3
"""Build Batch 023 Wave 1 (前橋育英高等学校, 第2弾 学校4/12) CANDIDATE data.

See scripts/batch_023_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_023_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000225',
  'name': '熊谷 航',
  'bleague_id': 19957,
  'birth_date': '1996-05-07',
  'university': 'ORG000128',
  'club': 'ORG000135',
  'club_start': '2025',
  'club_locator': '「2026-27 長崎」「2025-26 長崎」',
  'club_locator_short': '2025-26〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認',
  'pro_gaps': '秋田（2023-24〜2024-25）・信州（2021-22〜2022-23）・三河（2018-19〜2020-21）'},
 {'person_id': 'P000226',
  'name': '久岡 幸太郎',
  'bleague_id': 18478,
  'birth_date': '1997-01-04',
  'university': 'ORG000016',
  'club': 'ORG000103',
  'club_start': '2023',
  'club_locator': '「2026-27 茨城」〜「2023-24 茨城」',
  'club_locator_short': '2023-24〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2023-24シーズンからの在籍を確認（2023-24は広島の行もあり、シーズン途中の移籍とみられるが時期は未確認）',
  'pro_gaps': '広島（2023-24）・香川（2022-23）・東京Z（2018-19〜2021-22）'},
 {'person_id': 'P000227',
  'name': '久岡 賢太郎',
  'bleague_id': 34704,
  'birth_date': '2003-07-02',
  'university': 'ORG000016',
  'club': 'ORG000173',
  'club_start': '2026',
  'club_locator': '「2026-27 岩手」（履歴はこの1行のみ）',
  'club_locator_short': '2026-27〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認'},
 {'person_id': 'P000228',
  'name': '船生 誠也',
  'bleague_id': 8737,
  'birth_date': '1993-12-15',
  'university': 'ORG000030',
  'club': 'ORG000132',
  'club_start': '2025',
  'club_locator': '「2026-27 仙台」「2025-26 仙台」',
  'club_locator_short': '2025-26〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認',
  'pro_gaps': 'SR渋谷（2024-25）・広島（2021-22〜2023-24）・琉球（2020-21）・富山（2018-19〜2019-20）・名古屋D（2016-17〜2017-18）',
  'extra_issues': [{'type': 'PRE_BLEAGUE_HISTORY',
                    'description': '船生誠也のB.LEAGUE公式クラブ所属履歴は2016-17シーズン（B.LEAGUE開幕）以降のみ掲載されている。それ以前の経歴は公式資料で未確認のため記録していない。',
                    'next_check': '深掘りWaveでNBL等の当時の公式資料・クラブ公式発表を確認'}]}]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=727, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
