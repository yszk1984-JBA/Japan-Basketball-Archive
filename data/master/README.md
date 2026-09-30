# MASTER DATA

このディレクトリには、Yuichiが対象版と範囲を明示的に承認したデータだけを格納する。

## 現在の内容

最新の件数と反映済み承認の一覧は[`master_build_report.md`](master_build_report.md)を参照（2026-09-30時点：Person 516件、Organization 395件、Career 2,459件、Evidence 8,317件、Approval 12件）。

- 反映済み承認：Batch 005 Wave 1、Approval Sprint 001〜010（各Sprintの`data/verified/approval_sprint_NNN/master_approval.md`に承認記録）
- 訂正記録：[`corrections/`](corrections/)（ORG000017/ORG000019の統合、ORG000222の名称訂正）
- HOLD項目・HOLD Issue：含まない

## ファイル

- `person.csv`
- `organization.csv`
- `career.csv`
- `source.csv`
- `evidence.csv`
- `approval_records.csv`
- `publication_records.csv`
- `master_build_report.md`
- `validation_report.md`
- `corrections/`：Master反映後に行った訂正の記録（対象・理由・変更前後）

Masterへの追加・訂正は、CANDIDATEから同じGovernance工程を通し、承認済み範囲だけを反映する。データ入力ミス等の訂正は`corrections/`に記録し、Yuichiの承認を明示する。

