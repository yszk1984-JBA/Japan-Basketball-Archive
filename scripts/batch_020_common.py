#!/usr/bin/env python3
"""Shared settings for Batch 020 (強豪校横展開 第2弾 学校2/12：船橋市立船橋高等学校).

Discovery: B.LEAGUE "ワタシノB.LEAGUE" tag list for
TagID=35:船橋市立船橋高等学校 (8 current alumni, no "もっと見る").
The shorter spelling 「市立船橋高等学校」 returns 0 players, so the
tag name must be the full official spelling. None of the 8 are
registered yet; split 4+4 into Wave 1 and Wave 2.

Values were read on 2026-09-26 from each roster_detail page in the
browser (profile header, Q&A 「出身校（高）/（大）」, 「クラブ所属履歴」).
The builder is shared with Batch 019 (scripts/batch_019_common.py).

New Organizations: 船橋市立船橋高等学校 (ORG000211) and 駒澤大学
(ORG000212); highest existing ID was ORG000210 (batch_019). All other
universities/clubs reuse existing IDs matched against master + every
candidate organization_candidates.csv.
"""

BATCH = 20
SCHOOL_ORG = ("ORG000211", "船橋市立船橋高等学校")
SCHOOL_TAG = "船橋市立船橋高等学校"
EXTRA_ORGS = {
    "ORG000031": "拓殖大学",
    "ORG000121": "日本大学",
    "ORG000128": "大東文化大学",
    "ORG000212": "駒澤大学",
    "ORG000130": "シーホース三河",
    "ORG000183": "さいたまブロンコス",
    "ORG000137": "秋田ノーザンハピネッツ",
    "ORG000048": "佐賀バルーナーズ",
    "ORG000047": "宇都宮ブレックス",
    "ORG000092": "レバンガ北海道",
}
