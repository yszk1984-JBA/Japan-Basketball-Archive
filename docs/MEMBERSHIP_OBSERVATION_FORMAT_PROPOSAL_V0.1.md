# Membership Observation形式案 v0.1

作成日：2026-09-21

状態：レビュー用の提案。データ設計v0.1、Master、公開サイトへの採用は未承認。

## 結論案

同じ時期に同じ学校・クラブへ所属した人物を示すため、人物同士の組合せを原本として保存せず、公式ロスター等で確認した「人物の所属記録」を保存する。人物関係は所属記録から自動生成する。

```text
Membership Observation 6件
          ↓ 同じ organization_id + period_key で集約
同時所属の関係 15件を生成
```

6人から15組、15人から105組、100人から4,950組が生じるため、関係ペアを原本にすると修正と再承認が増える。所属記録を原本にすれば、人物の追加・訂正時も関係を再計算できる。

## 最小項目

| 項目 | 内容 |
| --- | --- |
| membership_id | 所属記録のID |
| person_id | 人物ID |
| organization_id | 学校・クラブ等の組織ID |
| period_key | 同じ時点を機械的に集約するキー |
| period_label | 画面に表示する日本語 |
| context_type | 公式ロスター、年度在籍、シーズン登録等の区分 |
| role | Player、Staff等 |
| source_id | 根拠資料 |
| source_locator | 資料内の選手欄等 |
| assessment | Governance上の現在段階 |

背番号は大会ごとに変わるため、人物の固定属性ではなくMembership Observationの補助項目として保持する。

## period_keyの例

| 種類 | 例 | 意味 |
| --- | --- | --- |
| 大会ロスター | `competition:wc2018` | ウインターカップ2018の登録時点 |
| 学校年度 | `academic_year:2018` | 2018年度の所属 |
| プロシーズン | `season:2025-26` | 2025-26シーズンの登録 |

異なる精度の期間を推測で結合しない。大会ロスター1件だけでは、年度全体の在籍や個別試合への出場を意味しない。

## 関係の生成条件

1. person_idが異なる。
2. organization_idが同じ。
3. period_keyが同じ。
4. 部門やチーム区分がある場合は同じ区分である。
5. 使用するMembershipが公開可能な承認段階に達している。

関係キーは `organization_id|period_key|小さいperson_id|大きいperson_id` とし、人物の順序による重複を防ぐ。

## Relationship Pilot 001の結果

ウインターカップ2018福岡第一高校公式ロスターから、既存Master人物6人のMembership候補6件を作成した。同一の `ORG000010` と `competition:wc2018` から15件の関係プレビューを再現できた。

この結果は形式の動作確認であり、6件のMembershipをVERIFIEDまたはMasterとして確定するものではない。

## 採用後に必要な作業

Yuichiの合意後に限り、データ設計の次版候補として次を行う。

1. SCHEMAへMembership Observationを追加する。
2. Governance工程と検証ルールを定義する。
3. Relationship Pilot 001をQAからVERIFIED候補へ進める。
4. Human Approval後にMasterへ反映する。
5. 承認済みMembershipだけを使って公開サイトで関係を生成する。

現時点では上記を実施しない。
