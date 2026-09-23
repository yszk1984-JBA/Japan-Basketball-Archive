# Batch 006

作成日：2026-09-22

状態：Wave 1の4人は2026年9月22日にHuman Approval・Master反映完了、公開未実施。Wave 2の4人はCANDIDATE・構造QA・VERIFIED候補化まで完了し、HUMAN APPROVAL・MASTER・公開は未実施。

MVPの選手数拡充を優先し、福岡第一高校を経由したB.LEAGUE・プロ選手を追加する。

Wave 1対象：井手 優希、クベマ スティーブ、ジャン・ローレンス・ハーパージュニア、長島 エマニエル。

Wave 2対象：秋山 皓太、大城 侑朔、土居 光、松本 礼太。

Wave 2では学校・大会・リーグの公式資料を優先し、専門媒体の記事は人物・期間候補を補助する上位参考資料として使用する。専門媒体だけで確認した値はHOLDに分離する。

詳細は[`docs/BATCH_006_PROPOSAL.md`](../../../docs/BATCH_006_PROPOSAL.md)を参照する。

検証結果は[`wave_01/validation_report.md`](wave_01/validation_report.md)を参照する。

Wave 2の検証結果は[`wave_02/validation_report.md`](wave_02/validation_report.md)を参照する。

## Wave 3（深掘りWave / Enrichment Wave）

状態：CANDIDATE構造QA（`validate_batch_006_wave_03.py`）まで完了。HUMAN APPROVAL・VERIFIED・MASTER・公開は未実施。

### 位置づけ

Yuichiの指示「深掘り（過去所属チーム）の本格展開」を受けた、既存選手の過去所属チーム深掘り初弾。wave_01対象の長島エマニエル（P000078、既にMaster登録済み）について、wave_01自身が残していたissue B6W1I0010（「高校と2016-18福岡の間の大学・所属は未確認」）を解消する。

### 追加した内容

jbaske.com（非公式バスケットボールデータベース）とWikipediaの独立した2ソースを突き合わせ、以下を確認した。

- 飛龍高等学校（静岡県） — 福岡第一高校へ転校する前の在学校
- 白鷗大学（中退） — Wikipedia単独ソースのため要裏付け（issue B6W3I0001）
- 横浜ビー・コルセアーズ（練習生、2012-2013年） — 在籍年次はjbaske.com単独（issue B6W3I0002）
- バンビシャス奈良（2013-2015年） — 在籍年次はjbaske.com単独（issue B6W3I0002）

既存のライジングゼファー福岡（2016-2018年、C000277）は変更していない。jbaske.com・bleague.jpいずれも彼の最終所属をライジングゼファー福岡（2017-18シーズン）としており、「現在の所属が古い」ケースではなく「2016年より前の経歴が欠落していた」ケースであることを確認した。

### 過去所属チーム深掘りの横断調査で判明したこと

今回のWaveは、全71名の登録済み選手を対象とした横断棚卸し（[`docs/HISTORICAL_CAREER_DEEPENING_LOG.md`](../../../docs/HISTORICAL_CAREER_DEEPENING_LOG.md)参照）の一環として選定した。調査の過程で、河合瑠那（P000066）・長岡大杜（P000067、いずれもbatch_004/wave_02由来）は、実は追加調査が不要であることが判明した。両者の出身高校・大学のCareerは、batch_004/wave_02の時点で既に公式資料（全日本大学バスケットボール連盟のインカレロスター等）でSUPPORTED・READY_FOR_VERIFIED_REVIEWまで到達しており、単にHUMAN APPROVAL・VERIFIED昇格が済んでいないだけだった。この2人分の重複調査・重複ID発行は行っていない。

検証結果は[`wave_03/validation_report.md`](wave_03/validation_report.md)を参照する。
