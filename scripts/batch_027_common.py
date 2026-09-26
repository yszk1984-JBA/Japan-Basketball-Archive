#!/usr/bin/env python3
"""Shared settings for Batch 027 (強豪校横展開 第2弾 学校2/12：秋田県立能代工業高等学校).

Discovery: B.LEAGUE "ワタシノB.LEAGUE" tag list for TagID=35:秋田県立能代工業高等学校,
read in the browser on 2026-09-26 (no "もっと見る"). Values were read
from each roster_detail page in the browser (profile header, Q&A
「出身校（高）/（大）」, 「クラブ所属履歴」). Builder shared with Batch 019
(scripts/batch_019_common.py).

タグ「秋田県立能代工業高等学校」は1名（盛實海翔、Wave 1）。関連として「秋田県立能代科学技術高等学校」のタグも確認したところ1名（中嶋正尭）が掲載されていたため、Wave 2で登録した。Yuichiの判断（2026-09-26）により、能代科学技術高校は能代工業高校と同じ扱いとし、既存Organization（ORG000159）に紐づけた（一度採番したORG000221は使用しない）。「能代工業高等学校」「能代科学技術高等学校」の短い表記ではいずれも0件。
"""

BATCH = 27
SCHOOL_ORG = ('ORG000159', '秋田県立能代工業高等学校')
SCHOOL_TAG = '秋田県立能代工業高等学校'
EXTRA_ORGS = {'ORG000018': '専修大学', 'ORG000149': '富山グラウジーズ'}

# Wave 2: 秋田県立能代科学技術高等学校 tag. Per Yuichi (2026-09-26) it is
# treated as the same Organization as 能代工業 (ORG000159); the source URL
# and locator keep the tag's own spelling.
WAVE2_SCHOOL_ORG = ('ORG000159', '秋田県立能代工業高等学校')
WAVE2_SCHOOL_TAG = '秋田県立能代科学技術高等学校'
WAVE2_EXTRA_ORGS = {'ORG000214': '名古屋学院大学', 'ORG000191': 'ヴィアティン三重'}
