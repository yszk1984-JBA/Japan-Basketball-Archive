#!/usr/bin/env python3
"""Build Batch 022 Wave 2 (尽誠学園高等学校, 第2弾 学校4/12) CANDIDATE data.

See scripts/batch_022_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_022_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000224',
  'name': '若狭 功希',
  'bleague_id': 25272,
  'birth_date': '1997-03-20',
  'university': None,
  'club': 'ORG000222',
  'club_start': '2025',
  'club_locator': '「2026-27 岡山」「2025-26 岡山」（直前は「2024-25 徳島」）',
  'club_locator_short': '2025-26〜、復帰',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2025-26シーズンの岡山復帰を確認（既存の復帰時開始年方針により2025とする）',
  'pro_gaps': '徳島（2023-24〜2024-25）・岡山（2019-20〜2022-23）',
  'extra_issues': [{'type': 'UNIVERSITY_NOT_LISTED',
                    'description': '若狭功希のB.LEAGUE公式プロフィールのQ&A欄「出身校（大）」は「-」で、大学在籍の有無は公式資料から確認できない。推測で大学Careerを登録していない。',
                    'next_check': 'クラブ公式の選手紹介・加入発表で経歴を確認'}]}]


if __name__ == "__main__":
    build(2, PLAYERS, first_career_seq=725, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
