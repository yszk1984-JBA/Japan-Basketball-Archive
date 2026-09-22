# Batch 006 — B.LEAGUE・プロ選手優先

更新日：2026-09-22

状態：Wave 1は2026年9月22日にHuman Approval・Master反映完了、公開未実施。Wave 2の4人はCANDIDATEと構造QAまで進め、VERIFIED・HUMAN APPROVAL・MASTER・公開は未実施。

## 目的

MVPでは選手検索、経歴、出典表示に必要なデータ量を優先する。同時所属機能は保留し、福岡第一高校をコアにB.LEAGUE・プロ経験者を追加する。

## Wave 1対象

| 優先 | 人物 | 区分 | 主な公式入口 |
| --- | --- | --- | --- |
| 1 | ジャン・ローレンス・ハーパージュニア | B1選手 | B.LEAGUE、東京サンロッカーズ、JBA |
| 2 | クベマ スティーブ | プロ選手 | B.LEAGUE、東京八王子ビートレインズ |
| 3 | 井手 優希 | プロ選手 | B.LEAGUE、JBA |
| 4 | 長島 エマニエル | B.LEAGUE経験者 | B.LEAGUE、JBA大会記録 |

4人はいずれも作業開始時点のMaster Personに存在しない。ジャン・ローレンス・ハーパージュニアはPilot Batch 001の既存候補ID `P000012`を継続使用する。現役3人を優先し、B.LEAGUE経験者1人を加える。

## 最小取込範囲

1. 公式氏名、英語表記、生年月日
2. 福岡第一高校での所属を示す公式資料
3. 大学または次の所属（確認できる人物のみ）
4. 現在または過去のプロ所属
5. B.LEAGUE公式戦出場またはクラブ公式契約
6. 未確認の期間・表記揺れをHOLDとして分離

プロ所属歴を一度に完全収録することは完了条件にしない。まず高校・大学等・プロの経路をSource付きでつなぎ、過去クラブの追加は後続Waveで補う。

## 完了条件

- 4人全員がPerson候補を持つ。
- 各人物の福岡第一高校CareerとプロCareerがSourceに結び付く。
- 各値がEvidenceまたはIssueに結び付く。
- 構造QAがPASSする。
- VERIFIED、Master、公開サイトを自動更新しない。

## Wave 1 QA結果

- Person候補：4件
- Career候補：11件
- Source：9件
- Evidence：56件
- VERIFIEDレビュー可能判断：21件（Person 4、Career 9、Organization 8）
- HOLD判断：2件
- 構造QA：PASS（エラー0件）

詳細は[`validation_report.md`](../data/candidate/batch_006/wave_01/validation_report.md)を参照する。

## Wave 2対象

| 優先 | 人物 | 区分 | 主な公式入口 |
| --- | --- | --- | --- |
| 1 | 秋山 皓太 | B.LEAGUE・B3経験者 | JBA、B3リーグ、福岡第一高校 |
| 2 | 大城 侑朔 | B.LEAGUE・B3経験者 | JBA、B.LEAGUE、福岡第一高校 |
| 3 | 土居 光 | B3選手 | JUBF、B.LEAGUE、福岡第一高校 |
| 4 | 松本 礼太 | B.LEAGUE・B3選手 | B.LEAGUE、B3リーグ、福岡第一高校 |

4人はいずれもMasterおよび既存候補に未登録である。現行B.LEAGUEの福岡第一出身一覧に残る未登録者だけでは対象が尽きたため、学校公式の卒業生一覧からプロ公式記録へ接続できる人物を選んだ。

月刊バスケットボール、ウインターカップ、U18日清食品トップリーグの名鑑・ロスターは上位参考資料として優先探索する。今回の4人ではJBA代表候補名簿、学校公式資料、JUBF、B.LEAGUE、B3リーグを直接確認できた。専門媒体のみで確認した期間は採用せずHOLDに残す。

## Wave 2完了条件

- 4人全員がPerson候補を持つ。
- 各人物の福岡第一高校CareerとプロCareerがSourceに結び付く。
- 公式資料と上位参考資料の区分がEvidenceで追跡できる。
- 期間、大学競技登録、現所属の未確認事項がHOLDに分離される。
- 構造QAがPASSする。
- VERIFIED、Master、公開サイトを自動更新しない。

## Wave 2 QA結果

- Person候補：4件
- Career候補：12件
- Source：14件
- Evidence：62件
- VERIFIEDレビュー可能判断：23件（Person 4、Career 12、Organization 7）
- HOLD Issue：10件（未確認期間・現所属の将来状態等）
- 構造QA：PASS（エラー0件）

詳細は[`validation_report.md`](../data/candidate/batch_006/wave_02/validation_report.md)を参照する。
