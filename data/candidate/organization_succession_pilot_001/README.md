# Organization Succession Pilot 001

作成日：2026-09-23

状態：CANDIDATE。構造QAはPASS（`scripts/validate_organization_succession_pilot_001.py`）。スキーマ採用・VERIFIED・HUMAN APPROVAL・MASTER・公開実装は未実施。

## 位置づけ

[組織承継・改称関係機能案 v0.1](../../../docs/ORGANIZATION_SUCCESSION_PROPOSAL_V0.1.md)について、Yuichiと次の3点を合意した（2026-09-23）。

1. スキーマ拡張の方針：Option A（付随リンクファイルを追加。中心4エンティティ＝Person/Organization/Career/Sourceは不変）
2. 承継とみなす範囲：名称変更のみ（東芝→DeNAのような運営権異動は対象外、別途検討）
3. 公開サイトでの見せ方：今回は保留

本Pilotは、この合意に基づき、既存CANDIDATEデータの中から見つかっている改称事例を`organization_succession_candidates.csv`として試験的に構造化したもの。

## 対象とした2件

| succession_id | 変更前 | 変更後 | 改称時期 |
| --- | --- | --- | --- |
| OSC0001 | 湘南ユナイテッドBC（ORG000163） | ウォルガ湘南（ORG000050） | 2026-27シーズンより |
| OSC0002 | 東芝ブレイブサンダース（ORG000164） | 川崎ブレイブサンダース（ORG000122） | 2016年7月1日 |

## 対象外とした1件（未解決の論点）

サンロッカーズ渋谷→東京サンロッカーズ（ORG000114）は、今回のPilotには含めていない。理由は、改称前の名称「サンロッカーズ渋谷」がOrganizationとして一度も登録されていないため。田中大貴（batch_007/wave_02）のMaster Careerは、最初から改称後の名称（東京サンロッカーズ、ORG000114）で登録されており、「サンロッカーズ渋谷」名義でのCareerを持つ人物がまだ登録されていない。

succession linkはpredecessor_organization_idの参照先が必要なため、この事例をPilotに含めるには「サンロッカーズ渋谷」をOrganizationとして新規登録する必要がある。ただし、これに対応する実際のCareerが存在しない状態でOrganizationだけを登録することが適切かどうかは、これまでの運用（実際に必要になった時点でのみOrganizationを起票する）と方向性が異なるため、Yuichiの判断を仰ぎたい。

## 生成した候補データ

- `organization_succession_candidates.csv`：succession_id, predecessor_organization_id, predecessor_name, successor_organization_id, successor_name, effective_date, effective_date_precision, reason, source_id, source_locator, assessment
- `source_references.csv`：2件（湘南クラブ公式サイトの改称発表、川崎ブレイブサンダースWikipediaの沿革節）

reasonは今回の合意範囲に合わせ、2件とも`NAME_CHANGE`のみを使用している。`effective_date_precision`は、湘南の事例が`season`（2026-27シーズンよりという season 単位の情報のため）、東芝→川崎の事例が`day`（2016年7月1日という日付が明記された一次資料があるため）と、確認できた精度をそのまま保持している。

検証結果は[`validation_report.md`](validation_report.md)を参照する。
