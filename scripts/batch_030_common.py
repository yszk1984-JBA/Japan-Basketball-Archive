#!/usr/bin/env python3
"""Shared settings for Batch 030 (強豪校横展開 第2弾 学校1/12：近畿大学附属高等学校).

Discovery: B.LEAGUE "ワタシノB.LEAGUE" tag list for TagID=35:近畿大学附属高等学校,
read in the browser on 2026-09-26 (no "もっと見る"). Values were read
from each roster_detail page in the browser (profile header, Q&A
「出身校（高）/（大）」, 「クラブ所属履歴」). Builder shared with Batch 019
(scripts/batch_019_common.py).

タグ1名。近畿大学附属高等学校を新規Organization（ORG000220）として登録。
"""

BATCH = 30
SCHOOL_ORG = ('ORG000220', '近畿大学附属高等学校')
SCHOOL_TAG = '近畿大学附属高等学校'
EXTRA_ORGS = {'ORG000018': '専修大学', 'ORG000200': '福井ブローウィンズ'}
