# 渡邊雄太（P000103）・田臥勇太（P000105）・富永啓生（P000106）NBA・Gリーグ経歴の確認記録

取得日：2026-10-08（JST）／Claudeのブラウザ（Yuichiの端末）で、nba.comのページから stats.nba.com API を取得。値は加工せず記録。

## 選手情報（commonplayerinfo）

| PlayerID | DISPLAY_FIRST_LAST | BIRTHDATE | SCHOOL | COUNTRY | DRAFT_YEAR | FROM–TO（LeagueID=00） | DLEAGUE_FLAG |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1629139 | Yuta Watanabe | 1994-10-13 | George Washington | Japan | Undrafted | 2018–2023 | Y |
| 2657 | Yuta Tabuse | 1980-10-05 | Brigham Young-Hawaii | USA | Undrafted | 2004–2004 | Y |
| 1642551 | Keisei Tominaga | 2001-02-01 | Nebraska | Japan | Undrafted | null（NBA_FLAG=N） | Y |

富永（LeagueID=20）：FROM_YEAR=2024／TO_YEAR=2024／TEAM_NAME=Mad Ants。田臥のCOUNTRYが「USA」となっているのはNBA側の登録値のまま（国籍の記録には使わない）。

## NBA（LeagueID=00）レギュラーシーズン

`playercareerstats?LeagueID=00&PerMode=Totals&PlayerID=1629139`（SeasonTotalsRegularSeason）

| SEASON_ID | TEAM_ID | TEAM | GP | GS |
| --- | --- | --- | ---: | ---: |
| 2018-19 | 1610612763 | MEM | 15 | 0 |
| 2019-20 | 1610612763 | MEM | 18 | 0 |
| 2020-21 | 1610612761 | TOR | 50 | 4 |
| 2021-22 | 1610612761 | TOR | 38 | 4 |
| 2022-23 | 1610612751 | BKN | 58 | 1 |
| 2023-24 | 1610612756 | PHX | 29 | 0 |
| 2023-24 | 1610612763 | MEM | 5 | 0 |
| 2023-24 | 0 | TOT | 34 | 0 |

プレーオフ（SeasonTotalsPostSeason）：2021-22 TOR 4試合、2022-23 BKN 1試合。

`commonteamroster`（シーズン末時点のロスター）：2018-19 MEM #12、2019-20 MEM #18、2020-21 TOR #18、2021-22 TOR #18、2022-23 BKN #18、2023-24 MEM #18 に掲載。2023-24 PHXのロスターには掲載なし（シーズン途中の移籍のため）。

田臥（2657）：`playercareerstats` は空（{}）。`playergamelog?PlayerID=2657&Season=2004-05&SeasonType=Regular Season`：4試合、Nov 03, 2004 PHX vs. ATL／Nov 06, 2004 PHX @ NJN／Dec 13, 2004 PHO vs. ORL／Dec 15, 2004 PHO vs. UTA（MATCHUPの表記どおり）。2004-05 PHXのシーズン末ロスターには掲載なし。

## NBA Gリーグ（LeagueID=20、旧NBDL）

`playercareerstats?LeagueID=20&PerMode=Totals`（SeasonTotalsRegularSeason）と `playergamelog?LeagueID=20`：

| 選手 | SEASON | 試合数 | ゲームログのチーム略称（試合数） | 期間（ゲームログ） |
| --- | --- | ---: | --- | --- |
| 田臥 | 2005-06 | 34 | ABQ（34） | Nov 18, 2005 – Mar 03, 2006 |
| 田臥 | 2006-07 | 44 | BAK（44） | Nov 26, 2006 – Apr 14, 2007 |
| 田臥 | 2007-08 | 39 | ANA（39） | Dec 09, 2007 – Apr 12, 2008 |
| 富永 | 2024-25 | 14 | IMA（14、TEAM_ID 1612709910） | Dec 28, 2024 IMA vs. SLC – Mar 29, 2025 IMA @ GRG |
| 渡邊 | 2018-19 | 33 | （チーム欄空欄） | — |
| 渡邊 | 2019-20 | 22 | （チーム欄空欄） | — |
| 渡邊 | 2021-22 | 1 | （チーム欄空欄） | — |

`franchisehistory?LeagueID=20`（略称とチーム名の対応）：
- 1612709893 Albuquerque Thunderbirds（2004–2009）
- 1612709900 Bakersfield Jam（2006–2015、DefunctTeams）
- 1612709899 Anaheim Arsenal（2006–2008、DefunctTeams）
- 1612709910 Fort Wayne Mad Ants（2007–2023）→ Indiana Mad Ants（2024）→ Noblesville Boom（2025）

## 記録しないこと

渡邊のGリーグ出場（two-way契約・NBAクラブからの派遣）は、河村勇輝と同じく別Careerにしない。契約解除・トレードの理由は記録しない。

## 大学の年度別ロスター（大学公式）

### ジョージ・ワシントン大学（gwsports.com、Men's Basketball Roster）

| ページ | 表記（#・Name・Class・Pos・Hometown） |
| --- | --- |
| https://gwsports.com/sports/mens-basketball/roster/2013-14 | 掲載なし |
| https://gwsports.com/sports/mens-basketball/roster/2014-15 | 12 Yuta Watanabe / Fr. / F / Kagawa, Japan |
| https://gwsports.com/sports/mens-basketball/roster/2015-16 | 12 Yuta Watanabe / So. / G / Kagawa, Japan |
| https://gwsports.com/sports/mens-basketball/roster/2016-17 | 12 Yuta Watanabe / Jr. / G / Kagawa, Japan |
| https://gwsports.com/sports/mens-basketball/roster/2017-18 | 12 Yuta Watanabe / Sr. / G / Kagawa, Japan |
| https://gwsports.com/sports/mens-basketball/roster/2018-19 | 掲載なし |

### ネブラスカ大学（huskers.com、Men's Basketball Roster）

| ページ | 表記 |
| --- | --- |
| https://huskers.com/sports/mens-basketball/roster/season/2020-21 | 掲載なし |
| https://huskers.com/sports/mens-basketball/roster/season/2021-22 | 30 Keisei Tominaga / Guard / Sophomore / Moriyama Nagoya Aichi, Japan / Sakuragaoka Gakuen / Ranger College |
| https://huskers.com/sports/mens-basketball/roster/season/2022-23 | 30 Keisei Tominaga / Guard / Junior / Moriyama Nagoya Aichi, Japan / Sakuragaoka Gakuen / Ranger College |
| https://huskers.com/sports/mens-basketball/roster/season/2023-24 | 30 Guard Keisei Tominaga / Senior / Moriyama Nagoya Aichi, Japan / Ranger College |
| https://huskers.com/sports/mens-basketball/roster/season/2024-25 | 掲載なし |

前の学校（Previous School）欄の「Ranger College」は、ネブラスカ大学の前に在籍した学校の記載。

### ネブラスカ大学公式ニュース「Huskers Sign Keisei Tominaga」（2020-11-11）

https://huskers.com/news/2020/11/11/huskers-sign-keisei-tominaga

- 「Tominaga … is currently a sophomore at Ranger (Texas) College, which will begin its season in January of 2021.」
- 「Tominaga was one of the top freshmen in junior college basketball last season, helping Ranger College … to a 28-3 record」
- 「As a high school senior, he averaged 39.8 points per game for Sakuragaoka Gakuen High School at the All-Japan Championship」

### レンジャー・カレッジ公式（ranger.prestosports.com）

ロスターページはボット確認（Cloudflare）が表示されたため取得していない（回避しない）。

### 確認できなかったもの

- 田臥：ブリガムヤング大学ハワイ校の在学期間、ABA（ロングビーチ・ジャム）、NBAクラブのトレーニングキャンプ参加
- 渡邊：尽誠学園高校の在学期間
