#!/usr/bin/env python3
"""Build Batch 026 Wave 1 (桜丘高等学校, 第2弾 学校1/12) CANDIDATE data.

See scripts/batch_026_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_026_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000233',
  'name': 'モッチ ラミン',
  'bleague_id': 30405,
  'birth_date': '1997-09-11',
  'university': 'ORG000128',
  'club': 'ORG000067',
  'club_start': '2025',
  'club_locator': '「2026-27 熊本」「2025-26 熊本」',
  'club_locator_short': '2025-26〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認',
  'pro_gaps': '佐賀・三河（いずれも2024-25。シーズン途中の移籍とみられるが時期は未確認）・埼玉（2019-20）',
  'extra_issues': [{'type': 'CAREER_TIMELINE_NOTE',
                    'description': 'モッチラミンのクラブ所属履歴は2019-20埼玉の次が2024-25で、2020-21〜2023-24の行がない。理由は推測で記録しない。',
                    'next_check': 'クラブ公式発表・リーグ公式資料で確認'}]}]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=750, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
