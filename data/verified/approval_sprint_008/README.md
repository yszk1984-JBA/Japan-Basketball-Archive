# Approval Sprint 008

作成日：2026-09-29

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。**2段階承認（Tier）の初回試行。**

## 対象

B.LEAGUE期の過去所属クラブ深掘り（batch_031、4 wave）でVERIFIEDとなった、Master既存108名の過去の所属Career 264件と、参照するOrganization。あわせて、Master既存Organizationの名称訂正1件（ORG000222）。

- VERIFIED snapshot commit：`f53dbd3`
- 新規Person：なし（全員Master登録済み）
- 新規Organization：6件（湘南ユナイテッドBC、香川ファイブアローズ、豊田合成スコーピオンズ、岐阜スゥープス、ベルテックス静岡、東京海上日動ビッグブルー）
- 名称訂正：ORG000222「トライフォース岡山」→「トライフープ岡山」（`organization_correction_review.csv`）

## Tier判定案（自動検証による案。確定はYuichi）

- Tier 1（簡易確認）案：74名
- Tier 2（丁寧確認）案：34名

判定案と理由は`person_review.csv`の`tier_proposal`・`tier_reasons`列。Tier 2の主な理由は、改称クラブの同一性判断、2026-27の所属履歴がないこと、PlayerIDの重複、名称訂正Organizationの参照。

### 確認の仕方

- Tier 1：出典が公式でURLが有効／所属と期間が根拠の資料位置と一致／人物同定に問題がない／掲載しない項目が含まれない、の4点
- Tier 2：上記に加え、全Evidenceを資料位置と1件ずつ照合

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するCareer・Organizationと、`organization_correction_review.csv`の名称訂正が承認候補。`hold_review.csv`の82件は対象外（既存Masterの期間の差異30件もここに含まれ、Masterは変更しない）。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
