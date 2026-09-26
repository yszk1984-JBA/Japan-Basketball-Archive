#!/usr/bin/env python3
"""Build Batch 025 Wave 1 (帝京長岡高等学校, 第2弾 学校2/12) CANDIDATE data.

See scripts/batch_025_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_025_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000231',
  'name': 'ブラ ブサナ グロリダ',
  'bleague_id': 39532,
  'birth_date': '1999-03-27',
  'university': None,
  'club': 'ORG000223',
  'club_start': '2022',
  'club_locator': '「2026-27 東京U」〜「2022-23 東京U」',
  'club_locator_short': '2022-23〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2022-23シーズンからの在籍を確認',
  'pro_gaps': '埼玉（2021-22）',
  'extra_issues': [{'type': 'UNIVERSITY_NAME_GARBLED',
                    'description': 'ブラブサナグロリダのB.LEAGUE公式プロフィールのQ&A欄「出身校（大）」は「白?大学」（2文字目が半角の「?」＝U+003F）と表示され、公式サイト側の文字化けとみられる。白鷗大学（ORG000093）の可能性が高いが、資料上の表記からは確定できないため大学Careerを登録していない。',
                    'next_check': 'クラブ公式の選手紹介・白鷗大学の公式ロスター等で出身大学を確認'}]},
 {'person_id': 'P000232',
  'name': '遠藤 善',
  'bleague_id': 5100000044,
  'birth_date': '1998-11-05',
  'university': 'ORG000020',
  'club': 'ORG000101',
  'club_start': '2025',
  'club_locator': '「2026-27 鹿児島」「2025-26 鹿児島」',
  'club_locator_short': '2025-26〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2025-26シーズンからの在籍を確認',
  'pro_gaps': '茨城（2024-25）・新潟（2021-22〜2023-24）・大阪（2020-21）'}]


if __name__ == "__main__":
    build(1, PLAYERS, first_career_seq=745, batch=BATCH, school_org=SCHOOL_ORG,
          school_tag=SCHOOL_TAG, extra_orgs=EXTRA_ORGS)
