# Batch 004 Wave 1 — Gemini精査パケット

作成日：2026-09-20

対象：河村勇輝、児玉ジュニア

次の文章をGeminiへ渡す。回答をSourceとして扱わず、CodexがURLと資料内位置を再確認する。

```text
河村勇輝と児玉ジュニアについて、次の公式URLだけを精査してください。検索結果の抜粋ではなく、各URLを実際に開き、資料内位置と記載内容を確認してください。

河村勇輝：
1. JBA 男子U16日本代表メンバー
https://www.japanbasketball.jp/wp-content/uploads/U16men-member_20180330.pdf
2. JBA 2020年度男子日本代表Bチーム メンバー
https://www.japanbasketball.jp/wp-content/uploads/National-B-Team_Men_member_20200806.pdf
3. B.LEAGUE公式選手プロフィール
https://www.bleague.jp/roster_detail/?PlayerID=30460
4. LA Clippers / NBA.com 選手ページ
https://www.nba.com/clippers/player/1642530/yuki-kawamura
5. NBA G League公式選手ページ
https://gleague.nba.com/player/1642530

児玉ジュニア：
1. JUBF 日本経済大学 2024新人戦ロスター
https://jubf.jp/game/university-detail/id/180/type/rookie/y/2024/s/men
2. JUBF World University Basketball Series 2025 日本学生選抜
https://jubf.jp/index/show-pdf/url/aHR0cHM6Ly9kMmEwdjF4N3F2eGw2Yy5jbG91ZGZyb250Lm5ldC9maWxlcy9zcG9ocF9qdWJmL25ld3MvNjg5MmMzMGU0Y2U3ZS5wZGY%3D
3. 三遠ネオフェニックス 2025-26契約締結（新規）
https://www.neophoenix.jp/news/detail/id=21966
4. 三遠ネオフェニックス 2026-27契約締結（継続）
https://www.neophoenix.jp/news/detail/id=24999
5. B.LEAGUE公式選手プロフィール
https://www.bleague.jp/roster_detail/?PlayerID=51000552
6. B.LEAGUE 大阪対三遠 2025年10月5日
https://www.bleague.jp/game_detail/?ScheduleKey=504749&TAB=B

人物ごとに次を確認してください。
1. 公式氏名、英語表記、生年月日
2. 福岡第一高校との関係
3. 高校後の大学または組織
4. 契約発表と契約種別
5. リーグ登録
6. 公式戦出場
7. 現在または最後に確認できる所属と基準日
8. 資料間の矛盾、更新時点の違い

出力列：
人物｜対象項目｜確認値｜発行元｜資料名｜公開日・大会日｜直接URL｜ページ番号・資料内位置｜具体的記載｜判定

判定：
- READY_FOR_CANDIDATE_PREPARATION：公式資料の該当箇所で値を直接確認でき、矛盾がない
- HOLD_CANDIDATE：URL、資料内位置、期間、人物同定、資料間整合のいずれかが不足
- REJECT_CANDIDATE：別人、誤記、無関係資料

注意：
- NBA.comの選手更新欄がRotoWire提供の場合、クラブ自身の契約発表と区別する。
- NBA選手ページと現行ロスターの表示が一致しない場合、現在所属をREADYにしない。
- 契約発表、リーグ登録、公式戦出場を別項目にする。
- 児玉ジュニアの大学学籍継続と男子バスケットボール部退部を分ける。
- 学年から入学・卒業年月を逆算しない。
- URLを開けない場合は、その値をREADYにしない。
```
