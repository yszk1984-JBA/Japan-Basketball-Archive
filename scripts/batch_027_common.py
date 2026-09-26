#!/usr/bin/env python3
"""Shared settings for Batch 027 (強豪校横展開 第2弾 学校2/12：秋田県立能代工業高等学校).

Discovery: B.LEAGUE "ワタシノB.LEAGUE" tag list for TagID=35:秋田県立能代工業高等学校,
read in the browser on 2026-09-26 (no "もっと見る"). Values were read
from each roster_detail page in the browser (profile header, Q&A
「出身校（高）/（大）」, 「クラブ所属履歴」). Builder shared with Batch 019
(scripts/batch_019_common.py).

タグ「秋田県立能代工業高等学校」は1名（盛實海翔、Wave 1）。関連として「秋田県立能代科学技術高等学校」のタグも確認したところ1名（中嶋正尭）が掲載されていたため、Wave 2で別Organization（ORG000221）として登録した。両校の関係（統合・後継等）は一次資料で確認しておらず、同一組織としては扱っていない。「能代工業高等学校」「能代科学技術高等学校」の短い表記ではいずれも0件。
"""

BATCH = 27
SCHOOL_ORG = ('ORG000159', '秋田県立能代工業高等学校')
SCHOOL_TAG = '秋田県立能代工業高等学校'
EXTRA_ORGS = {'ORG000018': '専修大学', 'ORG000149': '富山グラウジーズ'}

# Wave 2: 秋田県立能代科学技術高等学校 tag (separate Organization; the
# relationship to 能代工業 is not asserted).
WAVE2_SCHOOL_ORG = ('ORG000221', '秋田県立能代科学技術高等学校')
WAVE2_SCHOOL_TAG = '秋田県立能代科学技術高等学校'
WAVE2_EXTRA_ORGS = {'ORG000214': '名古屋学院大学', 'ORG000191': 'ヴィアティン三重'}
