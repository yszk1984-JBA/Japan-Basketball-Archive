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

## Wave 4（深掘りWave / Enrichment Wave, Round 2）

状態：CANDIDATE構造QA（`validate_batch_006_wave_04.py`）まで完了。HUMAN APPROVAL・VERIFIED・MASTER・公開は未実施。

### 位置づけ

過去所属チーム深掘りRound 2。全71名の棚卸し（[`docs/HISTORICAL_CAREER_DEEPENING_LOG.md`](../../../docs/HISTORICAL_CAREER_DEEPENING_LOG.md)参照）で、Master登録済みでCareer数が2件の選手を再点検し、「大学在学中で経歴が単に短いだけ」のケースと「現所属クラブ以前のプロ経歴が欠落しているケース」を選別した。対象は井手優希（P000075）・クベマ ジョセフ スティーブ（P000076）で、いずれもbatch_006/wave_01由来。

### 追加した内容

wave_01が残していたissueを解消する形で、独立した複数の公式発表・専門媒体ソースを突き合わせて以下を追加した。

- 井手優希：JR東日本秋田ペッカーズ（2019-2020）・山口ペイトリオッツ（現・山口パッツファイブ/ORG000100、2021-2022）・アースフレンズ東京Z（2022-2023）・横浜エクセレンス（2023-2024）・岩手ビッグブルズ（2024-2025、契約満了日2025-06-30まで確認）の計5件。
- クベマ：しながわシティバスケットボールクラブ（品川、専修大学在学中の2023-2024契約）1件。ヴェルテックス静岡（練習・試合帯同のみ、契約・出場実績・期間とも未確認）はCareerとして追加しなかった。
- 既存のHOLD_CANDIDATE（井手：C000268 日本体育大学／クベマ：C000271 専修大学）について、追加ソースでorganization_idのみ裏付けが取れたためREADY_FOR_VERIFIED_REVIEWへ更新（在籍期間は依然HOLD）。

なお山口パッツファイブ（ORG000100）は2023年7月1日に「山口ペイトリオッツ」から改称した同一組織であり、新規組織IDは発行していない（現行スキーマに名称履歴を保持する項目がないためissue化）。

検証結果は[`wave_04/validation_report.md`](wave_04/validation_report.md)を参照する。
