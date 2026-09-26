#!/usr/bin/env python3
"""Build Batch 021 Wave 2 (中部大学第一高等学校, 第2弾 学校3/12) CANDIDATE data.

See scripts/batch_021_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_021_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000213',
  'name': '坂本 聖芽',
  'bleague_id': 5100000027,
  'birth_date': '1999-09-13',
  'university': 'ORG000015',
  'club': 'ORG000142',
  'club_start': '2025',
  'club_locator': '「2026-27 大阪」「2025-26 大阪」',
  'club_locator_short': '2025-26〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認',
  'pro_gaps': '名古屋D（2020-21〜2024-25、5シーズン）'},
 {'person_id': 'P000214',
  'name': '宇都 直輝',
  'bleague_id': 8503,
  'birth_date': '1991-06-11',
  'university': 'ORG000018',
  'club': 'ORG000149',
  'club_start': '2023',
  'club_locator': '「2026-27 富山」〜「2023-24 富山」（直前は「2022-23 奈良」）',
  'club_locator_short': '2023-24〜、復帰',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2023-24シーズンの富山復帰を確認（既存の復帰時開始年方針により2023とする）',
  'pro_gaps': '奈良（2022-23）・富山（2016-17〜2021-22）',
  'extra_issues': [{'type': 'PRE_BLEAGUE_HISTORY',
                    'description': '宇都直輝のB.LEAGUE公式クラブ所属履歴は2016-17シーズン（B.LEAGUE開幕）以降のみ掲載されている。それ以前の経歴は公式資料で未確認のため記録していない。',
                    'next_check': '深掘りWaveでNBL等の当時の公式資料・クラブ公式発表を確認'}]},
 {'person_id': 'P000215',
  'name': '張本 天傑',
  'bleague_id': 8738,
  'birth_date': '1992-01-08',
  'university': 'ORG000030',
  'club': 'ORG000054',
  'club_start': '2016',
  'club_locator': '「2026-27 名古屋D」〜「2016-17 名古屋D」（履歴は名古屋Dのみ）',
  'club_locator_short': '2016-17〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2016-17シーズン（B.LEAGUE開幕）からの連続在籍を確認',
  'extra_issues': [{'type': 'PRE_BLEAGUE_HISTORY',
                    'description': '張本天傑のB.LEAGUE公式クラブ所属履歴は2016-17シーズン（B.LEAGUE開幕）以降のみ掲載されている。B.LEAGUE開幕前に同クラブ（当時の名称は別途確認が必要。既存Organizationに三菱電機ダイヤモンドドルフィンズ '
                                   'ORG000104 がある）に在籍していた可能性があるが、公式資料で未確認のため開始年は2016とし、推測で遡らせていない。',
                    'next_check': '深掘りWaveでNBL時代の公式資料・クラブ公式発表で加入年と当時名称を確認'}]},
 {'person_id': 'P000216',
  'name': '中村 瀬那',
  'bleague_id': 34792,
  'birth_date': '2002-06-03',
  'university': 'ORG000168',
  'club': 'ORG000191',
  'club_start': '2026',
  'club_locator': '「2026-27 三重」（履歴はこの1行のみ）',
  'club_locator_short': '2026-27〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認'}]


if __name__ == "__main__":
    build(2, PLAYERS, first_career_seq=692, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
