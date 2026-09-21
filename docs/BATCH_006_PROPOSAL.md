# Batch 006 — B.LEAGUE・プロ選手優先 Wave 1

作成日：2026-09-21

状態：Wave 1の4人をCANDIDATE化し、構造QAはPASS。VERIFIED・HUMAN APPROVAL・MASTER・公開は未実施。

## 目的

MVPでは選手検索、経歴、出典表示に必要なデータ量を優先する。同時所属機能は保留し、福岡第一高校をコアにB.LEAGUE・プロ経験者を追加する。

## Wave 1対象

| 優先 | 人物 | 区分 | 主な公式入口 |
| --- | --- | --- | --- |
| 1 | ジャン・ローレンス・ハーパージュニア | B1選手 | B.LEAGUE、東京サンロッカーズ、JBA |
| 2 | クベマ スティーブ | プロ選手 | B.LEAGUE、東京八王子ビートレインズ |
| 3 | 井手 優希 | プロ選手 | B.LEAGUE、JBA |
| 4 | 長島 エマニエル | B.LEAGUE経験者 | B.LEAGUE、JBA大会記録 |

4人はいずれも作業開始時点のMaster Personに存在しない。現役3人を優先し、B.LEAGUE経験者1人を加える。

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
