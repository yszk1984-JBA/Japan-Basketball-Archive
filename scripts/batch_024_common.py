#!/usr/bin/env python3
"""Shared settings for Batch 024 (強豪校横展開 第2弾 学校2/12：正智深谷高等学校).

Discovery: B.LEAGUE "ワタシノB.LEAGUE" tag list for TagID=35:正智深谷高等学校,
read in the browser on 2026-09-26 (no "もっと見る"). Values were read
from each roster_detail page in the browser (profile header, Q&A
「出身校（高）/（大）」, 「クラブ所属履歴」). Builder shared with Batch 019
(scripts/batch_019_common.py).

タグ2名とも新規。正智深谷高等学校を新規Organization（ORG000216）として登録。
"""

BATCH = 24
SCHOOL_ORG = ('ORG000216', '正智深谷高等学校')
SCHOOL_TAG = '正智深谷高等学校'
EXTRA_ORGS = {'ORG000016': '中央大学',
 'ORG000124': '明治大学',
 'ORG000110': '広島ドラゴンフライズ',
 'ORG000200': '福井ブローウィンズ'}
