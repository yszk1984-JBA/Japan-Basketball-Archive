# Organization Current Names 001

作成日：2026-10-06

状態：CANDIDATE。構造QAはPASS（`scripts/validate_organization_current_names_001.py`）。VERIFIED・HUMAN APPROVAL・MASTER・公開表示は未実施。

## 位置づけ

[組織承継・改称関係機能案 v0.1](../../../docs/ORGANIZATION_SUCCESSION_PROPOSAL_V0.1.md)で保留にしていた「公開サイトでの見せ方」について、Yuichiが2026-10-06に案B（当時の名称は正として残し、現在の名称を書き添える）を選んだ。

- Organizationの`name`（資料に書かれた当時の名称）は変更しない
- 改称後の学校をOrganizationとして新しく起票しない（承継リンク案の論点4と同じ方針）
- 付随情報として「現在の名称」を記録し、公開サイトでは「明成高等学校（現：仙台大学附属明成高等学校）」のように表示する

承継リンク（`organization_succession_candidates.csv`）は「改称前と改称後の両方がOrganizationとして存在する」場合のための仕組みで、今回の7件は改称後の名称がOrganizationとして登録されていないため、別の付随ファイルとした。

## 対象

高校・大学として登録されている256組織を目視で確認し、登録名と現在の名称が異なる7校を候補にした。

| ID | 組織 | 登録名 | 現在の名称 | 時期 | 種類 | 出典 |
| --- | --- | --- | --- | --- | --- | --- |
| OCN0001 | ORG000147 | 明成高等学校 | 仙台大学附属明成高等学校 | 2020年4月 | 改称 | Wikipedia |
| OCN0002 | ORG000159 | 秋田県立能代工業高等学校 | 秋田県立能代科学技術高等学校 | 2021年4月 | 2校の統合による新設校 | 学校公式 |
| OCN0003 | ORG000293 | 京北高等学校 | 東洋大学京北高等学校 | 2015年 | 改称 | Wikipedia |
| OCN0004 | ORG000432 | 旭川大学高等学校 | 旭川志峯高等学校 | 2023年4月 | 改称 | 学校公式 |
| OCN0005 | ORG000146 | 明桜高等学校 | ノースアジア大学明桜高等学校 | 2020年4月 | 改称 | Wikipedia＋学校公式（現在名） |
| OCN0006 | ORG000456 | 村野工業高等学校 | 彩星工科高等学校 | 2023年度 | 改称 | 兵庫県公式 |
| OCN0007 | ORG000316 | 光泉高等学校 | 光泉カトリック高等学校 | 2020年 | 改称 | Wikipedia |

## 注意点

- Wikipedia（出典優先順位5、探索用）だけで裏付けている候補が4件ある（OCN0001・0003・0005・0007）。現在の名称そのものは広く確認できる情報だが、学校公式の沿革での確認は未了。
- OCN0002（能代工業）は改称ではなく、能代工業と能代西の統合で新設された学校。「現：」ではなく「統合後：」などの表示にするかは要判断。
- 検討したが候補にしなかったもの：桜宮高等学校（大阪市立→大阪府立への移管。登録名に設置者を含まないため表示変更不要）、東海大学九州（2026-10-06の判断で東海大学とは別組織のまま）。
- 登録名が資料の表記のまま略称になっている学校（例：「村野工業高等学校」。正式名称は当時「神戸村野工業高等学校」）は、今回は名称の訂正をせず、現在の名称のみを付記する。

## ファイル

- `current_name_candidates.csv`：current_name_id, organization_id, recorded_name, current_name, effective_date, effective_date_precision, change_type, source_id, source_locator, assessment, note
- `source_references.csv`：8件（source_rankはDATA_POLICYの出典優先順位）
- [`validation_report.md`](validation_report.md)：構造検証の結果
