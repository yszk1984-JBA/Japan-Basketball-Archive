#!/usr/bin/env python3
"""Build Batch 029 Wave 1 (大阪桐蔭高等学校, 第2弾 学校1/12) CANDIDATE data.

See scripts/batch_029_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_029_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000237',
  'name': '金友 蓮',
  'bleague_id': 51000596,
  'birth_date': '2003-10-15',
  'university': 'ORG000193',
  'club': 'ORG000205',
  'club_start': '2026',
  'club_locator': '「2026-27 金沢」（直前は「2025-26 熊本」）',
  'club_locator_short': '2026-27〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認',
  'pro_gaps': '熊本（2025-26）'}]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=762, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
