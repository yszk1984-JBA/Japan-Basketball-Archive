#!/usr/bin/env python3
"""Shared settings for Batch 025 (強豪校横展開 第2弾 学校2/12：帝京長岡高等学校).

Discovery: B.LEAGUE "ワタシノB.LEAGUE" tag list for TagID=35:帝京長岡高等学校,
read in the browser on 2026-09-26 (no "もっと見る"). Values were read
from each roster_detail page in the browser (profile header, Q&A
「出身校（高）/（大）」, 「クラブ所属履歴」). Builder shared with Batch 019
(scripts/batch_019_common.py).

タグ2名とも新規。帝京長岡高等学校（ORG000217）・東京ユナイテッドバスケットボールクラブ（ORG000223）を新規Organizationとして登録。ブラ ブサナ グロリダは公式プロフィールの出身校（大）が「白?大学」と文字化けして表示されるが、Yuichiの判断（2026-09-26）により白鷗大学（ORG000093）として大学Careerを登録した（evidenceはPARTIAL、issue参照）。
"""

BATCH = 25
SCHOOL_ORG = ('ORG000217', '帝京長岡高等学校')
SCHOOL_TAG = '帝京長岡高等学校'
EXTRA_ORGS = {"ORG000093": "白鷗大学",
 'ORG000020': '日本体育大学',
 'ORG000223': '東京ユナイテッドバスケットボールクラブ',
 'ORG000101': '鹿児島レブナイズ'}
