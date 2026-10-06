# Approval Sprint 014

作成日：2026-10-06

状態：HUMAN APPROVAL待ち。MASTER未反映・公開未実施。

## 対象

B.PREMIER在籍のMaster登録選手のうち、高校のCareerがなかった15名に、出身高校のCareerを1件ずつ追加する（batch_032 wave_06、Yuichiの指示 2026-10-06「1から」）。VERIFIED snapshot commit：`28291b5`。

| 選手 | 出身高校 | Tier案 |
| --- | --- | --- |
| 金田 龍弥 | 大阪学院大学高等学校 | Tier 2 |
| 木村 圭吾 | 八王子学園八王子高等学校 | Tier 1 |
| 寺園 脩斗 | 延岡学園高等学校 | Tier 1 |
| 道原 紀晃 | 御影工業高等学校 | Tier 2 |
| 中島 三千哉 | 育英高等学校 | Tier 1 |
| 中野 司 | 報徳学園高等学校 | Tier 1 |
| 山口 颯斗 | 正智深谷高等学校 | Tier 1 |
| 松野 遥弥 | 桜丘高等学校 | Tier 1 |
| 大庭 圭太郎 | 如水館高等学校 | Tier 1 |
| 野﨑 零也 | 佐賀東高等学校 | Tier 1 |
| ベンドラメ 礼生 | 延岡学園高等学校 | Tier 2 |
| 山際 爽吾 | 福岡大学附属大濠高等学校 | Tier 1 |
| 山﨑 一渉 | 明成高等学校 | Tier 2 |
| 大友 隆太郎 | 茨城県立水戸第一高等学校（新規） | Tier 1 |
| 田中 流嘉州 | 中部大学第一高等学校 | Tier 1 |

新規Organization：茨城県立水戸第一高等学校。

在学期間はどれも未確認のため空欄。Masterの既存値は変更しない。Approval Sprint 013（出身大学など18件）とは独立しており、どちらを先に承認してもよい。

## Tier判定案

- Tier 1（11名）：クラブ公式・JBA公式のページの表記どおりで、既存のOrganization名と一致
- Tier 2（4名）：金田龍弥（「大阪学院高校」の略記）、道原紀晃（神戸市立科学技術→御影工業高等学校に寄せた）、山﨑一渉（仙台大学附属明成→明成高等学校に寄せた）、ベンドラメ礼生（専門メディアの記事のみ）

## 判断範囲

`evidence_review.csv`のSUPPORTED Evidenceに対応するCareerとOrganization。`hold_review.csv`の4件は対象外。

この資料の作成はHuman Approvalではない。Yuichiが対象版・範囲・Tierを明示して承認した後に限り、Masterへ反映できる。
