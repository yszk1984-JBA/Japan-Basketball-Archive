# MASTER反映レポート

作成日：2026-09-22

## 反映済み承認

- `APP-B005-20260921-01`：Batch 005 Wave 1
- `APP-AS001-20260921-01`：Approval Sprint 001
- `APP-AS002-20260921-01`：Approval Sprint 002
- `APP-AS003-20260921-01`：Approval Sprint 003
- `APP-AS004-20260922-01`：Approval Sprint 004

## MASTER件数

- Person：34件
- Organization：42件
- Career：100件
- Source：111件
- Evidence：624件
- Approval：6件

Approval Sprint 004の10件のHOLD Issueと10件の保留フィールドはMasterに含めていない。公開サイト反映は別工程で行う。

## 2026-09-23：Master訂正（Organization ID重複解消）

Organization「日本経済大学」がORG000017・ORG000019の2つのIDで重複登録されていたため、Yuichiの承認（`APP-CORR-ORG-20260923-01`）を得てORG000019に統合した。ORG000017参照の3件のCareer（C000030, C000225, C000254）とそれに対応するEvidence 5件を修正し、`organization.csv`からORG000017を削除した（43件→42件）。経緯・判断の詳細は[`corrections/2026-09-23_org000017_org000019.md`](corrections/2026-09-23_org000017_org000019.md)を参照。`scripts/validate_master.py`にOrganization名重複検出を追加し、本訂正後にPASSを確認した。
