# Approval Sprint 010 — Master Approval

- Approval ID：`APP-AS010-20260930-01`
- 承認者：Yuichi
- 承認日：2026-09-30
- 承認時の指示：下記「Yuichiの承認発言（原文）」
- 承認対象レビューcommit：`39e8233`
- VERIFIED対象版：`a506070`（batch_033（B.ONEロスター起点の横展開、新規182名））
- 承認範囲：182名、Career 896件、SUPPORTED Evidence 2,997件、参照Organization 245件
- 承認対象外：`hold_review.csv`の453件
- 確認方式：2段階承認。Tierは判定案どおりYuichiが確定：Tier 1（簡易確認）131名、Tier 2（丁寧確認）51名（`person_review.csv`）

## Yuichiの承認発言（原文、チャットでの返信をそのまま記録）

Approval Sprint 009と010をまとめて承認した1通の返信。

```
Sprint 009は 6d497b2、Sprint 010は a506070 です。
Tierの確定： 判定案どおり（009はTier 1が106名・Tier 2が62名、010はTier 1が131名・Tier 2が51名）
範囲： SUPPORTED Evidenceの範囲をMasterに反映してよいこと。HOLDは対象外であること。
```

## 承認の文脈（AIによる記録。Yuichi自身の発言ではない）

直前にYuichiが「Sprint 009と010を承認します」と返信した。AIが、承認記録には対象の版・範囲・Tierの確定をYuichi自身の言葉で残す必要があると伝え、この3点を依頼した。上の発言はその返信である。

Tier別の確認所要時間は記録していない（計測は運用改善用で、承認の条件ではない）。

## 保留した論点

- 「富田高等学校」と「私立富田高等学校」：別Organizationのまま反映する。

## 抜き取り再確認の対象（次回のApproval Sprintで丁寧確認の手順により再確認）

Tier 1で承認した131名から約10%（13名）を抽出した。

- 抽出方法：Python `random.Random(20260930).sample(sorted(Tier 1のperson_id), 13)`
- 対象：P000387 高橋昌也、P000388 鍋田隆征、P000395 山崎凜、P000397 伊集貴也、P000459 ザック・モーア、P000479 高橋育実、P000491 山崎玲緒、P000521 横川俊樹、P000525 佐藤誠人、P000533 小林巧、P000547 中谷麻登、P000549 野溝利一、P000560 佐藤星来
- 再確認で誤りが5%を超えた場合は、原因を記録してTier 1の条件を見直す。

承認対象外のHOLD Issueと保留フィールドはMasterへ反映しない。公開サイトへの反映は、この承認には含めない。
