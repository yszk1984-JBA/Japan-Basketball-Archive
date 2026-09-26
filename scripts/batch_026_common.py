#!/usr/bin/env python3
"""Shared settings for Batch 026 (強豪校横展開 第2弾 学校1/12：桜丘高等学校).

Discovery: B.LEAGUE "ワタシノB.LEAGUE" tag list for TagID=35:桜丘高等学校,
read in the browser on 2026-09-26 (no "もっと見る"). Values were read
from each roster_detail page in the browser (profile header, Q&A
「出身校（高）/（大）」, 「クラブ所属履歴」). Builder shared with Batch 019
(scripts/batch_019_common.py).

タグ2名のうち富永啓生は既存登録（P000106）のため除外し、モッチ ラミン1名を対象とした。
"""

BATCH = 26
SCHOOL_ORG = ('ORG000161', '桜丘高等学校')
SCHOOL_TAG = '桜丘高等学校'
EXTRA_ORGS = {'ORG000128': '大東文化大学', 'ORG000067': '熊本ヴォルターズ'}
