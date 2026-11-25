# 出身中学校の候補探し（Web検索のみ、2026-11-25）

Yuichiの依頼（2026-11-25）「中学のリサーチはできる？」→「先にWeb検索で候補探しだけ進めて」。
このときMacにつながっておらず、クラウドからは japanbasketball.jp・bleague.jp・basket-count.com 等に接続できない（プロキシで拒否、web-fetch でも取得不可）。
そのため、**ここに書いたものは検索結果のタイトルとURLだけで、ページの中身は未確認**。値として使う前に、Macのブラウザで実ページを開いて確認する（RAWの手がかり）。

対象：B.PREMIERの現役選手で中学校のCareerがない142名（`bleague_roster_premier_2026-11-07.tsv` と Master の照合）。日本の中学校に通った可能性が低い外国籍・海外育ちの選手を除くと約120名。

## 1. まとめて調べられる資料（優先）

### JBA「都道府県対抗ジュニアバスケットボール大会」（ジュニアオールスター）公式サイト

都道府県選抜のチームページ。名簿に所属中学校が載っている可能性が高い（未確認）。公式（JBA）の大会記録なので、載っていれば「公式」扱いにできる見込み。2019年が最後の大会（第32回）。現役選手の多くが中学生だった2007〜2019年をカバー。

- 2019（第32回）チームページの形式：`https://juniorallstar2019.japanbasketball.jp/team/m_<都道府県>/`
  - 例：[男子 神奈川](https://juniorallstar2019.japanbasketball.jp/team/m_kanagawa/)、[男子 兵庫](https://juniorallstar2019.japanbasketball.jp/team/m_hyogo/)、[男子 広島](https://juniorallstar2019.japanbasketball.jp/team/m_hiroshima/)、[男子 鳥取](https://juniorallstar2019.japanbasketball.jp/team/m_tottori/)、[男子 岐阜](https://juniorallstar2019.japanbasketball.jp/team/m_gifu/)、[男子 愛知](https://juniorallstar2019.japanbasketball.jp/team/m_aichi/)、[男子 大阪](https://juniorallstar2019.japanbasketball.jp/team/m_osaka/)、[男子 北海道](https://juniorallstar2019.japanbasketball.jp/team/m_hokkaido/)、[男子 群馬](https://juniorallstar2019.japanbasketball.jp/team/m_gunma/)、[男子 静岡](https://juniorallstar2019.japanbasketball.jp/team/m_shizuoka/)、[男子 埼玉](https://juniorallstar2019.japanbasketball.jp/team/m_saitama/)、[男子 東京B](https://juniorallstar2019.japanbasketball.jp/team/m_tokyob/)、[男子 富山](https://juniorallstar2019.japanbasketball.jp/team/m_toyama/)
- 2017：[大会最終日のニュース](http://juniorallstar2017.japanbasketball.jp/archives/4196)（サイトは juniorallstar2017.japanbasketball.jp）
- 2008（第21回）チームページの形式：`http://juniorallstar.japanbasketball.jp/2008/team_d.html?teamno=<番号>&mw=1`（[例](http://juniorallstar.japanbasketball.jp/2008/team_d.html?teamno=109&mw=1)。web-fetch では http/https のリダイレクトが往復して読めなかった）
- 2007：[大会公式サイト](http://juniorallstar.japanbasketball.jp/2007/)
- 2015・2016：JBAのニュース（[2015](http://www.japanbasketball.jp/convention/10760)、[2016](https://www.japanbasketball.jp/convention/21762)）。年ごとのサイトの形式は要確認。

### 全国中学校バスケットボール大会（全中）

- [2012 第42回（埼玉）公式サイト](http://saitama.japanbasketball.jp/zenchu/)
- [2016 第46回（福井）出場チーム](http://fukui-zenchu2016.japanbasketball.jp/boys/teams/)
- 山口開催の[出場チーム（男子）](http://zenchu-basketball.yamaguchi-chutairen.com/c1_boy/index.html)（年度は要確認）
- 中学校名はチーム名そのものなので、名簿に選手名があれば学校が確定する。

### 都道府県協会の資料

- [岡山県 年度別優秀選手一覧](http://okayama.japanbasketball.jp/yushusenshu/nendobetsu.html)（岡山県バスケットボール協会。中学生の優秀選手を含む可能性）

## 2. 選手ごとの手がかり（記事のタイトルに中学校名や中学時代の話題があるもの）

| 選手 | 手がかり | URL |
| --- | --- | --- |
| 安藤誓哉 | 記事タイトル「母校の小岩第四中学校バスケ部へシューズを寄贈」 | https://basket-count.com/article/detail/47859 |
| 片岡大晴 | 「“ルーツは仙台にあり”第2回片岡大晴…＜前編＞」（中学時代の記述がある可能性） | https://basketballking.jp/news/japan/20180207/46312.html |
| 田中大貴 | 「田中大貴が語るバスケ部時代vol.3」（vol.1・2に中学時代の記述がある可能性） | https://basket-count.com/article/detail/3919 |
| 田中大貴 | 「田舎の公立校からBリーグMVP田中大貴が目指してきた『万能性』」 | https://number.bunshun.jp/articles/-/843473 |
| 内尾聡理 | 「ひとり親家庭で育ち、バスケ、勉強に全力を注いで日本一に」（生い立ちの記事） | https://sportiva.shueisha.co.jp/clm/otherballgame/basketball/2025/02/04/fe/ |
| 松崎裕樹 | 「【注目の新卒選手#1】横浜BC・松崎裕樹とはどんな選手？」 | https://basketballking.jp/news/japan/univ/20230412/425280.html |

検索した10名（佐藤涼成・鵤誠司・内尾聡理・松崎裕樹・児玉ジュニア・田中大貴・片岡大晴・星川堅信・安藤誓哉・田原隆徳）のうち、タイトルで学校名まで分かったのは安藤誓哉の1名。選手ごとの検索は1人1〜2回の検索で手がかりが得られる割合が低いため、1のまとめて調べられる資料を先に使う。

## 3. 次にやること（Macにつながってから）

1. ジュニアオールスターの公式サイト（2007〜2019）をブラウザで開き、チームページの名簿に中学校が載っているか確認する。載っていれば、全年度・全都道府県の男子名簿を取得し、Masterの選手（生年度が合う人）と氏名で照合する。
2. 全中の出場チーム・名簿も同じように確認する。
3. 2の選手ごとの手がかりは、実ページで中学校名を確認してから使う。
4. 公式（JBA・協会）以外の資料から記録するものは「公式未確認」と表示する（2026-11-21の判断）。
