# Batch 032：ロスター起点の横展開（B.PREMIER 2026-27）CANDIDATE段階

作成日：2026-09-30

計画：`docs/ROSTER_EXPANSION_PLAN.md`（Yuichiの指示、2026-09-29）

## 結果

- 対象：B.PREMIER 26クラブの2026-27公式選手一覧（国籍区分「日本」、253名）のうち、Master未登録の148名
- 新規Person：**143名**（P000239〜P000381、4 Wave）
- Career：687件（学校240件＋クラブ447件）
- 新規Organization：128件（`new_organizations.csv`。学校127件、クラブ1件＝アイシン アレイオンズ）
- 検証：PASS（`validation_report.md`、batch_007 wave_11と合わせて検証）

あわせて、batch_007で候補登録のまま未承認だった25名を `data/candidate/batch_007/wave_11` で再確認した（同READMEを参照）。

## 登録しなかった5名（`excluded.csv`）

| 選手 | クラブ | 理由 |
| --- | --- | --- |
| 小松亮太 | 秋田 | 17歳（18歳未満は当面対象外） |
| 山本大扇 | 大阪 | 17歳 |
| プラット聖也 | 長崎 | 17歳 |
| 佐藤武 | 大阪 | 公式プロフィールが空欄（生年月日・出身校なし） |
| 八村阿蓮 | 神戸 | 同名の人物がMaster（P000133）に登録済み。MasterのSourceにこのPlayerIDがないため機械照合で拾えなかった。同一人物かの確認と過去所属の深掘りは別途 |

## 使った資料（`data/raw/research/`に原文を保存）

- `bleague_roster_premier_2026-09-29.tsv`：公式選手一覧（26クラブ、253名）
- `bleague_profiles_roster_2026-09-29.txt`：対象173名の公式プロフィールの値（2026-09-29〜30に取得）
- 公式順位表・略称ファイル（batch_031と共通）

## Issue（ほぼすべてHOLD、VERIFIEDには含めない）

| 種類 | 件数 | 内容 |
| --- | ---: | --- |
| HIGH_SCHOOL_PERIOD / UNIVERSITY_PERIOD | 126 / 114 | 学校の在籍期間が未確認 |
| ORG_NAME_HISTORY | 60 | 在籍当時のクラブ名・学校名が登録名と異なる（改称） |
| PRE_BLEAGUE_HISTORY | 47 | 所属履歴が2016-17から始まり、開幕前の在籍が未確認 |
| SCHOOL_NOT_LISTED | 21 | 公式プロフィールの出身校（高）が「-」（神戸・東京SRの選手に多い） |
| SAME_SEASON_TWO_CLUBS | 9 | 同じシーズンに2クラブ以上 |
| SCHOOL_NAME_UNREADABLE | 1 | エリエット・ドンリーの大学名が「シャミナード?学」と表示され読めない |
| NON_SCHOOL_ENTRY | 1 | 伊久江ロイ英輝の出身校欄の「Tokyo Samurai」はクラブチームとみられるため学校として登録せず |
| ENROLLED_STUDENT | 1 | 阿部真冴橙（19歳）の高校に「在学中」の表記 |

## 確認してほしい点（Yuichi）

- **白鷗大学の重複**：Masterに「白鷗大学」（ORG000093）と「白鴎大学」（ORG000208）が別Organizationとして存在する。今回は公式表記どおり「白鴎大学」（ORG000208）に紐づけた。統合するかは別途判断
- セントメリーズインターナショナルスクール（シェーファー アヴィ幸樹）と St. Mary’s International School（伊久江ロイ英輝）は同じ学校の可能性があるが、別表記のため別Organizationのまま
- 海外の学校名は公式プロフィールの表記どおり（英語・カタカナ混在）

## 状態

CANDIDATE段階。VERIFIED・HUMAN APPROVAL（Approval Sprint 009予定）・MASTERは未実施。
