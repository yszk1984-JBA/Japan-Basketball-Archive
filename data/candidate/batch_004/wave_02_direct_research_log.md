# Batch 004 Wave 2 Codex直接調査ログ

確認日：2026-09-20

対象：河合瑠那、長岡大杜

状態：公式Sourceの直接確認を開始。CANDIDATE作成前。

Felo・Geminiを経由せず、Codexが公式ページを直接開いて確認した。下記はSource候補であり、CANDIDATE、VERIFIED、MASTERではない。

## 河合瑠那

| 確認対象 | 公式Source | 直接確認できた内容 | 状態 |
| --- | --- | --- | --- |
| 人物基本情報・リーグ出場 | [B.LEAGUE公式プロフィール](https://www.bleague.jp/roster_detail/?PlayerID=51000607) | 河合瑠那、Runa Kawai、2003年6月3日、2025-26横浜EX、B2で1試合3分33秒・2得点 | Source候補 |
| 特別指定登録 | [横浜エクセレンス 特別指定選手登録](https://yokohama-ex.jp/team/pages/id=22814) | #2、PG/SG、福岡第一高等学校、2026年3月から特別指定選手。3月18日からベンチ登録可能 | Source候補 |
| 特別指定活動終了 | [横浜エクセレンス 活動終了](https://yokohama-ex.jp/news/detail/id=25440) | 2026年5月21日発表。2025-26シーズン限りで活動終了、自由交渉選手リスト公示予定 | Source候補 |
| 大阪学院大学の登録 | [JUBF 2023インカレ 大阪学院大学](https://jubf.jp/game/university-detail/id/49/type/intercollege/y/2023/s/men) | #2、2年、PG、180cm、福岡第一高、1試合10分出場 | Source候補 |
| 大阪学院大学の継続登録 | [JUBF 2024インカレ 大阪学院大学](https://jubf.jp/game/university-detail/id/49/type/intercollege/y/2024/s/men) | #2、3年、PG、180cm、福岡第一高、2試合44分50秒出場 | Source候補 |

大学ロスターとクラブ資料で身長が180cmと183cm、プロ登録ページで181cmと異なる。測定・登録時点の違いとしてSourceごとに保持し、単一値へ統合しない。

## 長岡大杜

| 確認対象 | 公式Source | 直接確認できた内容 | 状態 |
| --- | --- | --- | --- |
| 人物基本情報・福岡第一・B3出場 | [B.LEAGUE公式プロフィール](https://www.bleague.jp/roster_detail/?PlayerID=52467) | 長岡大杜、Daito Nagaoka、2007年10月17日、178cm・77kg、福岡第一高等学校在学中、2025-26山口、B3で1試合1分12秒出場 | Source候補 |
| リーグ登録 | [B3リーグ 新規リーグエントリー](https://www.b3league.jp/archives/45352) | 2026年1月30日発表。#17、SG、福岡第一高等学校在学中、山口パッツファイブの新規リーグエントリー | Source候補 |

B.LEAGUE公式プロフィールの「リーグ登録国籍」欄に「特別指定」と表示される。国籍値としては不自然なため、特別指定区分の表示として扱い、国籍情報には使用しない。

## 次の処理

1. 河合瑠那のPerson、福岡第一、大阪学院大学、横浜EXのCareer候補を作る。
2. 長岡大杜はExcel原本内の同名候補とIDを直接照合し、原本を変更せず人物同定を記録する。
3. 長岡大杜の福岡第一と山口のCareer候補を作る。
4. 契約、特別指定登録、公式戦出場、活動終了を別Evidenceにする。
5. Python構造QAを実行する。

現時点では外部AIによる例外調査は不要。
