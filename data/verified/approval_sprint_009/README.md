# Approval Sprint 009

作成日：2026-09-30

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。2段階承認（2回目）。

## 対象

B.PREMIER 2026-27のロスター起点の横展開（`docs/ROSTER_EXPANSION_PLAN.md`）。

- 新規人物 143名（batch_032、P000239〜P000381）
- 以前から候補登録のまま未承認だった25名（batch_007、最新の公式情報で再確認済み）
- 合計 **168名**、Career 808件、SUPPORTED Evidence 2795件
- VERIFIED snapshot commit：`6d497b2`
- Organization：232件（うちMaster未登録148件。多くは出身校）

## Tier判定案（自動検証による案。確定はYuichi）

- Tier 1（簡易確認）案：106名
- Tier 2（丁寧確認）案：62名

Tier 2の理由（重複あり）：

- 改称した組織：55名
- 公式資料ではない出典だけで裏付けている項目がある：5名
- 資料間で年の食い違いがある：2名
- 高校「在学中」の表記があり在籍状況の確認が必要：1名
- 学校名の一部が読めず未登録の項目がある：1名
- 出身校欄に学校以外：1名

判定案と理由は`person_review.csv`の`tier_proposal`・`tier_reasons`列。

## 前回（Sprint 008）の抜き取り再確認

Sprint 008でTier 1として承認した74名から抽出した7名（seed 20260929）を、今回Tier 2の手順で再確認する（`as008_sample_recheck.csv`）。対象はMaster登録済みのデータで、この資料では値を変更しない。誤りが見つかった場合は既存Masterの訂正と同じ経路で扱い、誤りの割合が5%を超えたらTier 1の条件を見直す。

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するPerson・Career・Organizationが承認候補。`hold_review.csv`の428件（学校の在籍期間未確認、改称の記録、開幕前の在籍未確認など）は対象外。

## 確認してほしい点

- 白鷗大学（ORG000093）と白鴎大学（ORG000208）がMasterで別Organizationになっている。今回の新規人物は公式表記どおり「白鴎大学」（ORG000208）に紐づけた。統合するかは別途判断
- 八村阿蓮（神戸）はMasterの同名人物（P000133）と同一人物とみられるため、今回は登録していない（`data/candidate/batch_032/excluded.csv`）
- 18歳未満の3名は登録していない

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
