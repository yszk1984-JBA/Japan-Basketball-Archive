#!/usr/bin/env python3
"""Shared settings for Batch 023 (強豪校横展開 第2弾 学校4/12：前橋育英高等学校).

Discovery: B.LEAGUE "ワタシノB.LEAGUE" tag list for TagID=35:前橋育英高等学校,
read in the browser on 2026-09-26 (no "もっと見る"). Values were read
from each roster_detail page in the browser (profile header, Q&A
「出身校（高）/（大）」, 「クラブ所属履歴」). Builder shared with Batch 019
(scripts/batch_019_common.py).

タグ4名全員が新規。前橋育英高等学校を新規Organization（ORG000215）として登録。久岡幸太郎・久岡賢太郎は同姓・同じ中央大学出身だが、関係を示す一次資料はなく関係性は記録していない。
"""

BATCH = 23
SCHOOL_ORG = ('ORG000215', '前橋育英高等学校')
SCHOOL_TAG = '前橋育英高等学校'
EXTRA_ORGS = {'ORG000128': '大東文化大学',
 'ORG000016': '中央大学',
 'ORG000030': '青山学院大学',
 'ORG000135': '長崎ヴェルカ',
 'ORG000103': '茨城ロボッツ',
 'ORG000173': '岩手ビッグブルズ',
 'ORG000132': '仙台89ERS'}
