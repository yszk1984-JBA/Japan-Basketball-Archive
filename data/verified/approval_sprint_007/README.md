# Approval Sprint 007

作成日：2026-09-26

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

強豪校横展開 第2弾（学校1〜12、Batch 019〜030、18 wave）でVERIFIED候補となり、
まだMasterに含まれていない46名を対象とする。対象校は以下の通り。

- 桐光学園高等学校（第2弾 学校1/12）
- 船橋市立船橋高等学校（第2弾 学校2/12）
- 中部大学第一高等学校（第2弾 学校3/12）
- 尽誠学園高等学校（第2弾 学校4/12）
- 前橋育英高等学校（第2弾 学校5/12）
- 正智深谷高等学校（第2弾 学校6/12）
- 帝京長岡高等学校（第2弾 学校7/12）
- 桜丘高等学校（第2弾 学校8/12）
- 秋田県立能代工業高等学校（第2弾 学校9/12）
- 報徳学園高等学校（第2弾 学校10/12）
- 大阪桐蔭高等学校（第2弾 学校11/12）
- 近畿大学附属高等学校（第2弾 学校12/12）

対象者の氏名一覧は `person_review.csv` を参照（本READMEには全46名は列挙しない）。

## 対象版

- VERIFIED snapshot commit：`adf7443`

## 件数

- Person：46件
- Career：137件
- Organization参照（unique）：63件
- Evidence：274件
- Source：46件
- HOLD Issue：141件
- HOLD判断・項目：137件

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceと、対応するPerson・Career・Organizationだけが承認候補。
`hold_review.csv`と`held_fields_review.csv`は対象外で、不明値を補わない。

## 個別に判断が必要な項目

次のCareerはSUPPORTED Evidenceを持たない（Yuichiの判断に基づく登録）。承認に含めるか除外するかを明示してほしい。

- C000768：ブラ ブサナ グロリダ → 白鷗大学（SUPPORTED Evidenceなし。公式サイトの表記が文字化けしており、Yuichiの判断（2026-09-26）で白鷗大学として登録した項目。evidenceはPARTIALのためVERIFIED Evidenceには含まれない）

この資料の作成はHuman Approvalではない。Yuichiが対象版と範囲を明示して承認した後に限り、Masterへ反映できる。
