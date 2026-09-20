# Wave 02 QA Report

この検査は構造QAであり、史実の正しさ、VERIFIED、HUMAN APPROVAL、MASTERを意味しない。

## 結果

- 構造検査：PASS
- エラー：0件
- 未解決事項：8件

## 件数

- `person_candidates.csv`：2行
- `organization_candidates.csv`：4行
- `career_candidates.csv`：5行
- `source_references.csv`：7行
- `evidence_records.csv`：40行
- `issues.csv`：8行
- `qa_decisions.csv`：11行

## 次段階レビュー判定

- READY_FOR_VERIFIED_REVIEW：11件
- HOLD_CANDIDATE：0件
- REJECT_CANDIDATE：0件

## エラー

- なし

## 解釈

PASSはID、参照、必須項目、assessment値の形式が今回の規則に合うことだけを示す。
`issues.csv`のOPEN/HOLDは解決しておらず、人間確認なしに候補値を昇格させない。
