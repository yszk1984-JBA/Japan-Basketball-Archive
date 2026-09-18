# Pilot Batch 001 QA Report

この検査は構造QAであり、史実の正しさ、VERIFIED、HUMAN APPROVAL、MASTERを意味しない。

## 結果

- 構造検査：PASS
- エラー：0件
- 未解決事項：6件

## 件数

- `person_candidates.csv`：5行
- `organization_candidates.csv`：3行
- `career_candidates.csv`：7行
- `source_references.csv`：8行
- `evidence_records.csv`：23行
- `issues.csv`：8行

## エラー

- なし

## 解釈

PASSはID、参照、必須項目、assessment値の形式が今回の規則に合うことだけを示す。
`issues.csv`のOPEN/HOLDは解決しておらず、人間確認なしに候補値を昇格させない。
