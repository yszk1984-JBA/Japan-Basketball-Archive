#!/usr/bin/env python3
"""Build Batch 024 Wave 1 (正智深谷高等学校, 第2弾 学校2/12) CANDIDATE data.

See scripts/batch_024_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_024_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000229',
  'name': '渡部 琉',
  'bleague_id': 5100000035,
  'birth_date': '2000-10-03',
  'university': 'ORG000016',
  'club': 'ORG000110',
  'club_start': '2024',
  'club_locator': '「2026-27 広島」〜「2024-25 広島」（直前は「2023-24 仙台」）',
  'club_locator_short': '2024-25〜、復帰',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2024-25シーズンの広島復帰を確認（既存の復帰時開始年方針により2024とする）',
  'pro_gaps': '仙台（2022-23〜2023-24）・広島（2021-22）・秋田（2020-21）'},
 {'person_id': 'P000230',
  'name': '常田 耕平',
  'bleague_id': 5100000040,
  'birth_date': '1999-11-06',
  'university': 'ORG000124',
  'club': 'ORG000200',
  'club_start': '2026',
  'club_locator': '「2026-27 福井」（直前は「2025-26 滋賀」）',
  'club_locator_short': '2026-27〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認',
  'pro_gaps': '滋賀（2024-25〜2025-26）・青森（2022-23〜2023-24）・三遠（2020-21〜2021-22）'}]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=739, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
