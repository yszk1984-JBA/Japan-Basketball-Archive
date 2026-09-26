#!/usr/bin/env python3
"""Shared settings for Batch 022 (強豪校横展開 第2弾 学校4/12：尽誠学園高等学校).

Discovery: B.LEAGUE "ワタシノB.LEAGUE" tag list for TagID=35:尽誠学園高等学校,
read in the browser on 2026-09-26 (no "もっと見る"). Values were read
from each roster_detail page in the browser (profile header, Q&A
「出身校（高）/（大）」, 「クラブ所属履歴」). Builder shared with Batch 019
(scripts/batch_019_common.py).

タグ6名のうち渡邊雄太は既存登録（P000103）のため除外し、5名を対象とした。若狭功希はプロフィールの出身校（大）が「-」のため大学Careerを登録していない。トライフォース岡山を新規Organization（ORG000222）として登録。
"""

BATCH = 22
SCHOOL_ORG = ('ORG000156', '尽誠学園高等学校')
SCHOOL_TAG = '尽誠学園高等学校'
EXTRA_ORGS = {'ORG000128': '大東文化大学',
 'ORG000148': '近畿大学',
 'ORG000188': '京都産業大学',
 'ORG000030': '青山学院大学',
 'ORG000205': '金沢サムライズ',
 'ORG000111': '東京八王子ビートレインズ',
 'ORG000155': '島根スサノオマジック',
 'ORG000222': 'トライフォース岡山'}
