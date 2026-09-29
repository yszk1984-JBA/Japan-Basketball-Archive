# Approval Sprint 010

作成日：2026-09-30

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。2段階承認（3回目）。

## 対象

B.ONE 2026-27のロスター起点の横展開（batch_033、`docs/ROSTER_EXPANSION_PLAN.md`）。

- 新規人物 **182名**（P000382〜P000563）、Career 896件、SUPPORTED Evidence 2997件
- VERIFIED snapshot commit：`a506070`
- Organization：245件（Master既存86件、Approval Sprint 009で承認待ち36件、その他Master未登録123件（ほぼbatch_033で作成））

**順序**：Approval Sprint 009（batch_032）で作ったOrganizationを参照するため、Sprint 009の承認・反映の後に扱うことを想定している。

## Tier判定案（自動検証による案。確定はYuichi）

- Tier 1（簡易確認）案：131名
- Tier 2（丁寧確認）案：51名

Tier 2の理由（重複あり）：

- 改称した組織：48名
- 学校名の一部が読めず未登録の項目がある：1名
- 出身校欄に学校以外：1名
- 高校「在学中」の表記があり在籍状況の確認が必要：1名

判定案と理由は`person_review.csv`の`tier_proposal`・`tier_reasons`列。

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するPerson・Career・Organizationが承認候補。`hold_review.csv`の453件は対象外。

## 確認してほしい点

- 「富田高等学校」と「私立富田高等学校」（Batch 032）は同じ学校の可能性があるが別Organizationのまま
- 公式プロフィールが空欄の2名（宮田諭、ジュフ・伴馬）は登録していない

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
