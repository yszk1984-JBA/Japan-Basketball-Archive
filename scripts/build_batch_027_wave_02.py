#!/usr/bin/env python3
"""Build Batch 027 Wave 2 (秋田県立能代科学技術高等学校, 第2弾 学校2/12) CANDIDATE data.

See scripts/batch_027_common.py for discovery, scope and ID notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch_019_common import build  # noqa: E402
from batch_027_common import BATCH, EXTRA_ORGS, SCHOOL_ORG, SCHOOL_TAG  # noqa: E402
from batch_027_common import WAVE2_EXTRA_ORGS, WAVE2_SCHOOL_ORG, WAVE2_SCHOOL_TAG  # noqa: E402

PLAYERS = [{'person_id': 'P000235',
  'name': '中嶋 正尭',
  'bleague_id': 16023,
  'birth_date': '2003-06-09',
  'university': 'ORG000214',
  'club': 'ORG000191',
  'club_start': '2026',
  'club_locator': '「2026-27 三重」（履歴はこの1行のみ）',
  'club_locator_short': '2026-27〜',
  'start_summary': 'B.LEAGUE公式のクラブ所属履歴で2026-27シーズンからの在籍を確認',
  'extra_issues': [{'type': 'ORG_NAME_HISTORY',
                    'related': 'C000756',
                    'description': '中嶋正尭のB.LEAGUE公式プロフィールの出身校（高）は「秋田県立能代科学技術高等学校」。Yuichiの判断（2026-09-26）により能代工業高校と同じ扱いとし、秋田県立能代工業高等学校（ORG000159）のCareerとして登録した。単一名称スキーマでは校名の違いを表現できない（宇都宮ブレックス・仙台大学附属明成と同種の事例）。',
                    'next_check': 'Organization名称の時系列表現（改称・統合履歴）のスキーマ整備を検討'}]}]


if __name__ == "__main__":
    build(2, PLAYERS, first_career_seq=756, batch=BATCH, school_org=WAVE2_SCHOOL_ORG,
          school_tag=WAVE2_SCHOOL_TAG, extra_orgs=WAVE2_EXTRA_ORGS)
