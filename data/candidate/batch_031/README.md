# Batch 031: B.LEAGUE期の過去所属クラブ深掘り（Master既存選手）CANDIDATE段階

作成日：2026-09-29

計画：`docs/DEEPENING_BLEAGUE_ERA_PLAN.md`（Yuichiの指示「深堀からお願いします」、2026-09-29）

## 結果

- 対象：Master 166名のうちB.LEAGUE PlayerIDのある155名（4 Wave、40名ずつ）
- 新規Career：**264件**（108名分）。いずれも既存Masterにない、B.LEAGUE期（2016-17以降）の過去の在籍
- Evidence：1,056件（Career 1件につき、所属履歴＋公式順位表の2件でクラブを確認、開始年・終了年は所属履歴）
- 検証：PASS（`validation_report.md`）
- 既存Masterの値は変更していない

## 使った資料（いずれも2026-09-29にブラウザで取得、`data/raw/research/`に原文を保存）

- `bleague_club_history_2026-09-29.txt`：155名（156ページ）の選手プロフィール「クラブ所属履歴」
- `bleague_standings_clubs_by_season_2026-09-29.csv`：公式順位表（2016-17〜2026-27、B1〜B3）に載った各クラブの略称とTeamID
- `bleague_club_abbreviations_2026-09-29.tsv`：略称 → 順位表上の正式名称

所属履歴は略称（例：SR渋谷、千葉J）しかないため、シーズンごとの公式順位表で略称とクラブ（TeamID）を対応付けた。

## 登録ルール

- 同じクラブに続けて在籍した期間を1件のCareerにする。一度離れて戻った場合は別のCareer
- start＝最初のシーズンの開始年、end＝最後のシーズンの終了年（2016-17〜2020-21なら2016〜2021）
- 同じシーズンに2クラブある場合（シーズン途中の移籍）は両方を登録し、同じ年を使う
- 改称したクラブ（B.LEAGUE公式のTeamIDが同じ）は1つのOrganizationにまとめる（Yuichiの判断、2026-09-29）。当時の名称はORG_NAME_HISTORY issueに記録
- すでに別Organizationとして登録済みだった2クラブ（東京サンレーヴス／しながわシティ、湘南ユナイテッドBC／ウォルガ湘南）は、シーズンの名称に合うOrganizationを使った
- 既存Masterにある在籍（同じOrganizationで期間が重なる、または期間未記録）は追加しない

## Organization

- 新規：香川ファイブアローズ（ORG000224）、豊田合成スコーピオンズ（ORG000225）、岐阜スゥープス（ORG000226）、ベルテックス静岡（ORG000227）、東京海上日動ビッグブルー（ORG000228）
- **名称の訂正（要承認）**：ORG000222「トライフォース岡山」→「トライフープ岡山」。batch_022で要約型Web取得ツールの英訳から登録した誤りで、公式の選手一覧・順位表（TeamID=1639）はいずれも「トライフープ岡山」。Masterに入っているため、Approval Sprint 008で訂正として承認を受ける（`org_corrections.csv`）
- 湘南ユナイテッドBC（ORG000163）は候補段階のOrganizationで、今回のCareerから参照される

## Issue（82件、いずれもHOLD）

| 種類 | 件数 | 内容 |
| --- | ---: | --- |
| MASTER_PERIOD_DIFFERENCE | 30 | 既存Master Careerの期間が未記録、または公式所属履歴から導いた期間と異なる。Masterは変更していない |
| ORG_NAME_HISTORY | 28 | 在籍当時のクラブ名が現在の登録名と異なる（例：サンロッカーズ渋谷→東京サンロッカーズ、西宮→神戸ストークス） |
| NOT_ON_CURRENT_ROSTER | 13 | 2026-27の所属履歴行がない（河村勇輝、長島エマニエルなど）。終了年は変更していない |
| SAME_SEASON_TWO_CLUBS | 10 | 同一シーズンに2クラブ |
| DUAL_PLAYER_ID | 1 | 松本礼太（P000082）はPlayerIDが2つあり、所属履歴が2ページに分かれている。両方を合わせて扱った |

## 状態

CANDIDATE段階。VERIFIED・HUMAN APPROVAL（Approval Sprint 008、2段階承認の初回）・MASTERは未実施。
