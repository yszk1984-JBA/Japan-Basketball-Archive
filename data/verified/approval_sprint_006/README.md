# Approval Sprint 006

作成日：2026-09-25

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

強豪校水平展開シリーズ（学校1〜11、Batch 008〜018、22 wave）でVERIFIED候補となり、
まだMasterに含まれていない82名を対象とする。対象校は以下の通り。

- 福岡大学附属大濠高等学校（学校1/11）
- 仙台大学附属明成高等学校（学校2/11）
- 洛南高等学校（学校3/11）
- 開志国際高等学校（学校4/11）
- 延岡学園高等学校（学校5/11）
- 東山高等学校（学校6/11）
- 北陸高等学校（学校7/11）
- 藤枝明誠高等学校（学校8/11）
- 土浦日本大学高等学校（学校10/11）
- 八王子学園八王子高等学校（学校11/11）

対象者の氏名一覧は `person_review.csv` を参照（本READMEには全82名は列挙しない）。

## 対象版

- VERIFIED snapshot commit：`8dd71b9`

## 件数

- Person：82件
- Career：242件
- Organization参照（unique）：81件
- Evidence：514件
- Source：109件
- HOLD Issue：108件
- HOLD判断・項目：241件

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceと、対応するPerson・Career・Organizationだけが承認候補。
`hold_review.csv`と`held_fields_review.csv`は対象外で、不明値を補わない。

この資料の作成はHuman Approvalではない。Yuichiが対象版と範囲を明示して承認した後に限り、Masterへ反映できる。
