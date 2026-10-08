# Approval Sprint 017

作成日：2026-10-08

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

B.ONE在籍のMaster登録選手のうち、高校のCareerがなかった選手20名に、クラブ公式の資料で確認した出身校（高校・大学）のCareerを追加する（batch_033 wave_06、Yuichiの指示 2026-10-08）。VERIFIED snapshot commit：`db58da1`。

| 選手 | 学校 | 期間 | Tier案 |
| --- | --- | --- | --- |
| ダマ ムッサ | Maranatha High School（新規） | （期間なし） | Tier 2 |
| ダマ ムッサ | William Jewell College（新規） | （期間なし） | Tier 2 |
| ダマ ムッサ | Moberly Area Community College（新規） | （期間なし） | Tier 2 |
| 栗原 ルイス | パリサデス高校（新規） | （期間なし） | Tier 1 |
| 栗原 ルイス | ウィッティア大学（新規） | （期間なし） | Tier 1 |
| 小西 聖也 | 洛南高等学校 | （期間なし） | Tier 1 |
| 小西 聖也 | 関西学院大学 | （期間なし） | Tier 1 |
| 鈴木 悠介 | 洛南高等学校 | （期間なし） | Tier 1 |
| 鈴木 悠介 | 法政大学 | （期間なし） | Tier 1 |
| 長島 蓮 | 白鷗大学 | （期間なし） | Tier 1 |
| エドワード・モリス | ピッツバーグ州立大学（新規） | （期間なし） | Tier 1 |
| 宮本 龍世 | 東海大学付属諏訪高等学校 | （期間なし） | Tier 2 |
| 宮本 龍世 | 国士舘大学 | （期間なし） | Tier 2 |
| 五十嵐 圭 | 中央大学 | （期間なし） | Tier 1 |
| 大森 尊之 | 宮崎県立小林高等学校 | （期間なし） | Tier 1 |
| 大森 尊之 | 日本体育大学 | （期間なし） | Tier 1 |
| 長谷川 智伸 | 拓殖大学 | （期間なし） | Tier 1 |
| 濵高 康明 | 金沢市立工業高等学校（新規） | （期間なし） | Tier 1 |
| 濵高 康明 | 近畿大学 | （期間なし） | Tier 1 |
| 濱田 貴流馬 | 尽誠学園高等学校 | （期間なし） | Tier 2 |
| 濱田 貴流馬 | 近畿大学 | （期間なし） | Tier 2 |
| 星野 曹樹 | 帝京長岡高等学校 | （期間なし） | Tier 1 |
| 星野 曹樹 | 白鷗大学 | （期間なし） | Tier 1 |
| 堀内 星夜 | 高知中央高等学校 | 2014〜2017 | Tier 1 |
| 堀内 星夜 | 名古屋学院大学 | 2017〜2019 | Tier 1 |
| 堀内 星夜 | 日本経済大学 | 2019〜2021 | Tier 1 |
| 松井 啓十郎 | モントロス・クリスチャン高等学校 | （期間なし） | Tier 2 |
| 松井 啓十郎 | コロンビア大学（新規） | （期間なし） | Tier 2 |
| 丸山 賢人 | 報徳学園高等学校 | 2018〜2021 | Tier 1 |
| 丸山 賢人 | 日本大学 | 2021〜2025 | Tier 1 |
| 内藤 英真 | IMGアカデミー（新規） | （期間なし） | Tier 1 |
| 満田 丈太郎 | 北陸高等学校 | （期間なし） | Tier 1 |
| 満田 丈太郎 | 筑波大学 | （期間なし） | Tier 1 |
| ジャンバルボ 海斗 | 近畿大学 | （期間なし） | Tier 1 |
| ニモ 正義 | Haines City HS（新規） | （期間なし） | Tier 1 |
| ニモ 正義 | Northeast Mississippi Community College（新規） | 2025〜2026 | Tier 1 |

新規Organization：Maranatha High School、William Jewell College、Moberly Area Community College、パリサデス高校、ウィッティア大学、ピッツバーグ州立大学、金沢市立工業高等学校、コロンビア大学、IMGアカデミー、Haines City HS、Northeast Mississippi Community College。

Masterの既存値は変更しない。Approval Sprint 013〜016とは独立。

## Tier判定案

- Tier 1（16名）：クラブ公式の発表・選手ページの出身校欄・経歴欄の表記どおり
- Tier 2（4名）：ダマ ムッサ（Maranatha High Schoolの同名校）、宮本龍世（紹介文の記述）、濱田貴流馬（近畿大学のバスケ部には所属せず）、松井啓十郎（モントローズ／モントロス・クリスチャンの表記ゆれ）

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するCareerとOrganization。`hold_review.csv`の4件は対象外。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
