# Approval Sprint 008 — Master Approval

- Approval ID：`APP-AS008-20260929-01`
- 承認者：Yuichi
- 承認日：2026-09-29
- 承認時の指示：下記「Yuichiの承認発言（原文）」
- 承認対象レビューcommit：`2164a97`
- VERIFIED対象版：Batch 031 VERIFIED snapshot `f53dbd3`（4 wave、B.LEAGUE期の過去所属クラブ深掘り）
- 承認範囲：Master既存108名の過去所属Career 264件、SUPPORTED Evidence 1,056件、参照Organization（新規6件を含む）、ORG000222の名称訂正（「トライフォース岡山」→「トライフープ岡山」）
- 承認対象外：`hold_review.csv`の82件（既存Masterの期間の差異30件を含む。Masterの既存値は変更しない）
- 確認方式：2段階承認（初回試行）。Tierは判定案どおりYuichiが確定：Tier 1（簡易確認）74名、Tier 2（丁寧確認）34名（`person_review.csv`）

## Yuichiの承認発言（原文、チャットでの返信をそのまま記録）

> Approval Sprint 008を、版 f53dbd3、Tierは案どおり（Tier 1 74名／Tier 2 34名）で、SUPPORTED Evidenceの範囲とORG000222の名称訂正をMasterに反映してよい。HOLDは対象外。

## 承認の文脈（AIによる記録。Yuichi自身の発言ではない）

上記の発言は、チャットでAIがApproval Sprint 008のレビュー資料（対象108名・Career 264件、Tier判定案とその理由、新規Organization、ORG000222の名称訂正、承認対象外82件）を提示し、Yuichi自身の言葉での承認を依頼した直後の返信として記録する。

Tier別の確認所要時間は記録していない（計測は運用改善用で、承認の条件ではない）。

## 抜き取り再確認の対象（次回のApproval Sprintで丁寧確認の手順により再確認）

2段階承認の運用（`docs/APPROVAL_TIERING_PROPOSAL_V0.1.md`、2026-09-29採用）に従い、Tier 1で承認した74名から約10%（7名）を抽出した。

- 抽出方法：Python `random.Random(20260929).sample(sorted(Tier 1のperson_id), 7)`
- 対象：P000129 白戸大聖、P000155 平良宗龍、P000166 野本建吾、P000192 多田武史、P000208 市場脩斗、P000214 宇都直輝、P000225 熊谷航
- 再確認で誤りが5%を超えた場合は、原因を記録してTier 1の条件を見直す。

承認対象外のHOLD Issueと保留フィールドはMasterへ反映しない。公開サイトへの反映は、この承認には含めない。
