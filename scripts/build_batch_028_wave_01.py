#!/usr/bin/env python3
"""Build Batch 028 Wave 1 (報徳学園高等学校, 第2弾 学校1/12) CANDIDATE data.

See scripts/batch_028_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_028_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000236',
  'name': '宇都宮 陸',
  'bleague_id': 51000124,
  'birth_date': '2002-12-06',
  'university': 'ORG000188',
  'club': 'ORG000180',
  'club_start': '2024',
  'club_locator': '「2026-27 FE名古屋」〜「2024-25 FE名古屋」',
  'club_locator_short': '2024-25〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの在籍を確認',
  'pro_gaps': 'A東京（2022-23）・愛媛（2021-22）',
  'extra_issues': [{'type': 'CAREER_TIMELINE_NOTE',
                    'description': '宇都宮陸のクラブ所属履歴に2023-24の行がない（2022-23 A東京→2024-25 '
                                   'FE名古屋）。大学在学中の登録（特別指定選手等）の可能性があるが、種別は推測で記録しない。',
                    'next_check': 'クラブ公式発表・リーグ公式資料で確認'}]}]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=759, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
