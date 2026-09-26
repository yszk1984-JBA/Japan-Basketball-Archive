#!/usr/bin/env python3
"""Shared settings for Batch 029 (強豪校横展開 第2弾 学校1/12：大阪桐蔭高等学校).

Discovery: B.LEAGUE "ワタシノB.LEAGUE" tag list for TagID=35:大阪桐蔭高等学校,
read in the browser on 2026-09-26 (no "もっと見る"). Values were read
from each roster_detail page in the browser (profile header, Q&A
「出身校（高）/（大）」, 「クラブ所属履歴」). Builder shared with Batch 019
(scripts/batch_019_common.py).

タグ1名。大阪桐蔭高等学校を新規Organization（ORG000219）として登録。
"""

BATCH = 29
SCHOOL_ORG = ('ORG000219', '大阪桐蔭高等学校')
SCHOOL_TAG = '大阪桐蔭高等学校'
EXTRA_ORGS = {'ORG000193': '大阪産業大学', 'ORG000205': '金沢サムライズ'}
