#!/usr/bin/env python3
"""Build Batch 030 Wave 1 (近畿大学附属高等学校, 第2弾 学校1/12) CANDIDATE data.

See scripts/batch_030_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_030_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000238',
  'name': '西野 曜',
  'bleague_id': 30468,
  'birth_date': '1998-07-27',
  'university': 'ORG000018',
  'club': 'ORG000200',
  'club_start': '2024',
  'club_locator': '「2026-27 福井」〜「2024-25 福井」',
  'club_locator_short': '2024-25〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2024-25シーズンからの在籍を確認',
  'pro_gaps': '横浜BC（2023-24）・SR渋谷（2020-21〜2022-23）・秋田（2019-20）'}]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=765, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
