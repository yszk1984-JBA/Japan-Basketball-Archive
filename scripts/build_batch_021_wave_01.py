#!/usr/bin/env python3
"""Build Batch 021 Wave 1 (中部大学第一高等学校, 第2弾 学校3/12) CANDIDATE data.

See scripts/batch_021_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_021_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000209',
  'name': '上澤 俊喜',
  'bleague_id': 5100000039,
  'birth_date': '1998-06-02',
  'university': 'ORG000121',
  'club': 'ORG000110',
  'club_start': '2022',
  'club_locator': '「2026-27 広島」〜「2022-23 広島」',
  'club_locator_short': '2022-23〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2022-23シーズンからの在籍を確認',
  'pro_gaps': '富山（2020-21〜2021-22、2シーズン）'},
 {'person_id': 'P000210',
  'name': '中村 浩陸',
  'bleague_id': 30349,
  'birth_date': '1997-11-29',
  'university': 'ORG000128',
  'club': 'ORG000109',
  'club_start': '2025',
  'club_locator': '「2026-27 A東京」「2025-26 A東京」',
  'club_locator_short': '2025-26〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認',
  'pro_gaps': 'FE名古屋（2022-23〜2024-25、3シーズン）・大阪（2019-20〜2021-22、3シーズン）'},
 {'person_id': 'P000211',
  'name': '小澤 飛悠',
  'bleague_id': 51000498,
  'birth_date': '2004-10-04',
  'university': 'ORG000020',
  'club': 'ORG000054',
  'club_start': '2025',
  'club_locator': '「2026-27 名古屋D」「2025-26 名古屋D」（履歴はこの2行のみ）',
  'club_locator_short': '2025-26〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認'},
 {'person_id': 'P000212',
  'name': '星野 京介',
  'bleague_id': 51000108,
  'birth_date': '1999-06-01',
  'university': 'ORG000128',
  'club': 'ORG000150',
  'club_start': '2026',
  'club_locator': '「2026-27 信州」（直前は「2025-26 北海道」）',
  'club_locator_short': '2026-27〜、復帰',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2026-27シーズンの信州復帰を確認（既存の復帰時開始年方針により2026とする）',
  'pro_gaps': '北海道（2024-25〜2025-26）・信州（2023-24）・滋賀（2021-22〜2022-23）'}]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=680, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
