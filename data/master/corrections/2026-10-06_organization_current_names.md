# Master追加記録：改称した学校の「現在の名称」（付随データ）

作成日：2026-10-06
承認：`APP-OCN-20261006-01`（Yuichi、この会話内での明示的な選択、2026-10-06）

## Yuichiの判断（会話内の選択肢への回答をそのまま記録）

```
公開サイトでの見せ方：B（当時の名称は正として残し、現在の名称を書き添える）
承認範囲：7件すべて表示する (Recommended)
能代工業の表示：（統合後：秋田県立能代科学技術高等学校） (Recommended)
```

## 反映内容

- `data/master/organization_current_names.csv`（新規）：7件。CANDIDATE `data/candidate/organization_current_names_001/current_name_candidates.csv`（構造QA PASS）の内容に、表示ラベル（`display_label`：「現」または「統合後」）と承認IDを付けたもの
- `data/master/organization_current_name_sources.csv`（新規）：上記の出典8件
- `data/master/approval_records.csv`：`APP-OCN-20261006-01`を追加

## 影響範囲外

- `data/master/organization.csv`の名称（資料に書かれた当時の名称）は変更しない
- Person・Career・Source・Evidenceは変更しない
- 改称後の学校をOrganizationとして新しく起票しない

## 公開サイトでの表示

組織ページ・組織一覧・ランキングで「明成高等学校（現：仙台大学附属明成高等学校）」のように付記する。能代工業は「（統合後：秋田県立能代科学技術高等学校）」とする。

## 出典の注意

明成・京北・明桜（改称日）・光泉の4件は、出典がWikipedia（出典優先順位5）のみ。学校公式の沿革で確認できた場合は、出典を差し替える。
