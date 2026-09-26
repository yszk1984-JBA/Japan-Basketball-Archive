#!/usr/bin/env python3
"""Build Batch 022 Wave 1 (尽誠学園高等学校, 第2弾 学校4/12) CANDIDATE data.

See scripts/batch_022_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_022_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000220',
  'name': '松尾 河秋',
  'bleague_id': 51000367,
  'birth_date': '2002-10-12',
  'university': 'ORG000128',
  'club': 'ORG000205',
  'club_start': '2026',
  'club_locator': '「2026-27 金沢」（直前の行は「2023-24 愛媛」）',
  'club_locator_short': '2026-27〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認',
  'pro_gaps': '愛媛（2023-24）',
  'extra_issues': [{'type': 'CAREER_TIMELINE_NOTE',
                    'description': '松尾河秋のクラブ所属履歴は「2026-27 金沢」「2023-24 '
                                   '愛媛」の2行のみで、2024-25・2025-26の行がない。理由・登録種別は推測で記録しない。',
                    'next_check': 'クラブ公式発表・リーグ公式資料で確認'}]},
 {'person_id': 'P000221',
  'name': '髙岡 圭汰朗',
  'bleague_id': 51000129,
  'birth_date': '1999-06-14',
  'university': 'ORG000148',
  'club': 'ORG000111',
  'club_start': '2026',
  'club_locator': '「2026-27 八王子」（直前の行は「2022-23 奈良」）',
  'club_locator_short': '2026-27〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認',
  'pro_gaps': '奈良（2021-22〜2022-23）',
  'extra_issues': [{'type': 'CAREER_TIMELINE_NOTE',
                    'description': '髙岡圭汰朗のクラブ所属履歴は2022-23奈良の次が2026-27八王子で、2023-24〜2025-26の行がない。理由は推測で記録しない。',
                    'next_check': 'クラブ公式発表・リーグ公式資料で確認'}]},
 {'person_id': 'P000222',
  'name': '上田 隼輔',
  'bleague_id': 51000137,
  'birth_date': '1999-09-18',
  'university': 'ORG000188',
  'club': 'ORG000155',
  'club_start': '2025',
  'club_locator': '「2026-27 島根」「2025-26 島根」',
  'club_locator_short': '2025-26〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認',
  'pro_gaps': '富山（2021-22〜2024-25、4シーズン）'},
 {'person_id': 'P000223',
  'name': '笠井 康平',
  'bleague_id': 18167,
  'birth_date': '1993-08-12',
  'university': 'ORG000030',
  'club': 'ORG000222',
  'club_start': '2026',
  'club_locator': '「2026-27 岡山」（直前は「2025-26 福島」）',
  'club_locator_short': '2026-27〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認',
  'pro_gaps': '福島（2024-25〜2025-26）・奈良（2023-24）・宇都宮（2022-23）・群馬（2020-21〜2021-22）・名古屋D（2018-19〜2019-20）'}]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=713, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
