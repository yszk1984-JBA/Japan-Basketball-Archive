# Approval Sprint 009 — Master Approval

- Approval ID：`APP-AS009-20260930-01`
- 承認者：Yuichi
- 承認日：2026-09-30
- 承認時の指示：下記「Yuichiの承認発言（原文）」
- 承認対象レビューcommit：`a8427f8`
- VERIFIED対象版：`6d497b2`（batch_032（B.PREMIERロスター起点の横展開、新規143名）＋batch_007再確認25名）
- 承認範囲：168名、Career 808件、SUPPORTED Evidence 2,795件、参照Organization 232件
- 承認対象外：`hold_review.csv`の428件
- 確認方式：2段階承認。Tierは判定案どおりYuichiが確定：Tier 1（簡易確認）106名、Tier 2（丁寧確認）62名（`person_review.csv`）

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

## Sprint 008の抜き取り再確認（7名）

Sprint 009の資料（`as008_sample_recheck.csv`）で依頼したSprint 008の抜き取り7名の再確認は、今回の承認時点では結果の記録なし（未実施）。次の機会に結果を記録する。

## 保留した論点

- 白鷗大学（ORG000093）と白鴎大学（ORG000208）の統合：今回は判断なし。別Organizationのまま反映する。

## 抜き取り再確認の対象（次回のApproval Sprintで丁寧確認の手順により再確認）

Tier 1で承認した106名から約10%（11名）を抽出した。

- 抽出方法：Python `random.Random(20260930).sample(sorted(Tier 1のperson_id), 11)`
- 対象：P000258 菅澤紀行、P000272 高橋快成、P000287 石川裕大、P000297 原修太、P000308 平尾充庸、P000333 松野遥弥、P000334 三谷桂司朗、P000346 荒谷裕秀、P000356 長野誠史、P000357 今村佳太、P000358 加藤嵩都
- 再確認で誤りが5%を超えた場合は、原因を記録してTier 1の条件を見直す。

承認対象外のHOLD Issueと保留フィールドはMasterへ反映しない。公開サイトへの反映は、この承認には含めない。
