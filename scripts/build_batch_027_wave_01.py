#!/usr/bin/env python3
"""Build Batch 027 Wave 1 (秋田県立能代工業高等学校, 第2弾 学校2/12) CANDIDATE data.

See scripts/batch_027_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_027_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000234',
  'name': '盛實 海翔',
  'bleague_id': 19998,
  'birth_date': '1997-08-26',
  'university': 'ORG000018',
  'club': 'ORG000149',
  'club_start': '2026',
  'club_locator': '「2026-27 富山」（直前は「2025-26 北海道」）',
  'club_locator_short': '2026-27〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認',
  'pro_gaps': '北海道（2024-25〜2025-26）・SR渋谷（2018-19〜2023-24）'}]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=753, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
