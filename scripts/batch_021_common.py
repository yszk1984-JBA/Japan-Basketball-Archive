#!/usr/bin/env python3
"""Shared settings for Batch 021 (強豪校横展開 第2弾 学校3/12：中部大学第一高等学校).

Discovery: B.LEAGUE "ワタシノB.LEAGUE" tag list for
TagID=35:中部大学第一高等学校, read in the browser on 2026-09-26:
11 current alumni, no "もっと見る". (An earlier summary-tool fetch
reported only 6 -- the browser count is authoritative.) None of the 11
are registered yet; split 4+4+3 into Waves 1-3.

Values were read from each roster_detail page in the browser (profile
header, Q&A 「出身校（高）/（大）」, 「クラブ所属履歴」). Builder shared
with Batch 019 (scripts/batch_019_common.py).

New Organizations: 中部大学第一高等学校 (ORG000213), 名古屋学院大学
(ORG000214); highest existing ID was ORG000212 (batch_020).
"""

BATCH = 21
SCHOOL_ORG = ("ORG000213", "中部大学第一高等学校")
SCHOOL_TAG = "中部大学第一高等学校"
EXTRA_ORGS = {
    "ORG000121": "日本大学",
    "ORG000128": "大東文化大学",
    "ORG000020": "日本体育大学",
    "ORG000015": "東海大学",
    "ORG000018": "専修大学",
    "ORG000030": "青山学院大学",
    "ORG000168": "天理大学",
    "ORG000031": "拓殖大学",
    "ORG000214": "名古屋学院大学",
    "ORG000110": "広島ドラゴンフライズ",
    "ORG000109": "アルバルク東京",
    "ORG000054": "名古屋ダイヤモンドドルフィンズ",
    "ORG000150": "信州ブレイブウォリアーズ",
    "ORG000142": "大阪エヴェッサ",
    "ORG000149": "富山グラウジーズ",
    "ORG000191": "ヴィアティン三重",
    "ORG000182": "青森ワッツ",
    "ORG000143": "群馬クレインサンダーズ",
}
