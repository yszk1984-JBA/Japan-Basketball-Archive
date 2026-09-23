# MASTER DATA

このディレクトリには、Yuichiが対象版と範囲を明示的に承認したデータだけを格納する。

## 現在の内容

- Batch 005 Wave 1：4人・11 Career
- Approval Sprint 001：8人・18 Career
- Approval Sprint 002：8人・32 Career
- Approval Sprint 003：10人・30 Career
- Approval Sprint 004：4人・9 Career
- Approval ID：`APP-B005-20260921-01`、`APP-AS001-20260921-01`、`APP-AS002-20260921-01`、`APP-AS003-20260921-01`、`APP-AS004-20260922-01`
- Person：34件
- Organization：42件（2026-09-23、Organization ID重複[ORG000017/ORG000019]をORG000019へ統合。詳細は[`corrections/2026-09-23_org000017_org000019.md`](corrections/2026-09-23_org000017_org000019.md)）
- Career：100件
- Evidence：573件
- HOLD項目・HOLD Issue：含まない
- 公開サイト反映：Approval Sprint 003までの4件を2026-09-21に反映済み。Approval Sprint 004は未反映

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

