# Batch 003 Gemini調査AのURL監査

受領日：2026-09-19

状態：RAW受領、公式URL再確認済み、CANDIDATE未作成

## 結論

5人について提示された主要な公式URLはすべて到達でき、該当する氏名と登録内容を確認できた。`utm_source=gemini`は追跡用文字列なのでSource URLから除く。

確認できた値は、Gemini回答を根拠にせず、下記公式ページ・PDFをSource候補として項目別Evidenceに使用する。期間は学年から逆算せず、資料の日付または大会年における活動確認として扱う。

## 公式Source候補

| 人物 | 公式Source | 直接確認できた範囲 | CANDIDATEでの扱い |
| --- | --- | --- | --- |
| 佐藤 涼成 | [JUBF 2024年度第47回李相佰盃メンバー表](https://jubf.jp/index/show-pdf/url/aHR0cHM6Ly9kMmEwdjF4N3F2eGw2Yy5jbG91ZGZyb250Lm5ldC9maWxlcy9zcG9ocF9qdWJmL25ld3MvNjYwMjliODAwOTQ1ZC5wZGY=) | `SATO, Ryosei`、PG、173cm・75kg、2003-07-09、白鷗大学2年、福岡第一高校 | Person基本情報と白鷗大学での活動確認。開始・終了時期はHOLD |
| 早田 流星 | [JBA 第101回天皇杯 日本体育大学ロスター](https://zennihon2025-26.japanbasketball.jp/team/fin/m02/) | 背番号10、185cm、2003-07-18、日本体育大学4年、福岡第一高校 | Person基本情報と日本体育大学での活動確認 |
| 早田 流星 | [JUBF 2025日本体育大学](https://jubf.jp/game/university-detail/id/5/type/intercollege/y/2025/s/men) | 4年、PF、背番号10、185cm、福岡第一高校、2試合出場 | 大学Careerの役割・登録項目・競技参加 |
| 鷹野 祐磨 | [2019年度男子U16日本代表第1次強化合宿メンバー](https://iwate.japanbasketball.jp/manage/wp-content/uploads/2019/04/42d4fca113768eb1273ef8bdba5e06eb.pdf) | `TAKANO, Yuma`、SF、185cm・73kg、2003-11-28、福岡第一高校1年、西福岡中学校 | Person基本情報と2019年4月の福岡第一高校Player活動確認 |
| 星賀 舞也 | [JUBF 2024青山学院大学](https://jubf.jp/game/university-detail/id/9/type/intercollege/y/2024/s/men) | 3年、SF、背番号25、190cm、福岡第一高校、3試合出場 | 青山学院大学Careerと競技参加 |
| 星賀 舞也 | [JUBF 2024年12月4日BOX](https://jubf.jp/game/detail/id/1194/type/intercollege/s/men) | 背番号25、先発、出場28分59秒 | 特定試合での競技参加 |
| 岡本 汰稀 | [JUBF 2025九州国際大学](https://jubf.jp/game/university-detail/id/230/type/intercollege/y/2025/s/men) | 4年、PF、背番号23、190cm、福岡第一高校、2試合出場 | 九州国際大学Careerと競技参加 |

## 修正して扱う点

- 佐藤涼成のJUBF資料は大会期間を2024年5月17日〜19日と記載し、年齢・所属の基準日は2024年3月26日としている。3月26日を資料の公開日とは断定しない。
- 佐藤涼成の体重はJUBF資料で75kg、横浜BC公式で86kgである。資料時点が異なるため、どちらかを誤りとせず、時点付きEvidenceとして分ける。
- 星賀舞也の190cmは2024年の青山学院大学登録値であり、高校時の身長として扱わない。
- 岡本汰稀の190cm、PF、背番号23は2025年の九州国際大学登録値である。高校時や別年度の値へ適用しない。
- 鷹野祐磨の福岡大学所属はBasket Plusだけの提示で、大学または大学連盟の公式ロスターを確認できていないためHOLDにする。

## 項目別HOLD

| 人物 | HOLDする主な項目 |
| --- | --- |
| 佐藤 涼成 | 福岡第一高校Careerの開始・終了時期、高校時の背番号・ポジション・身長 |
| 早田 流星 | 英語表記、福岡第一高校Careerの開始・終了時期、高校時の登録項目 |
| 鷹野 祐磨 | 福岡大学への実所属、大学での登録・競技参加、高校Careerの終了時期 |
| 星賀 舞也 | 英語表記、生年月日、福岡第一高校Careerの開始・終了時期、高校時の登録項目 |
| 岡本 汰稀 | 英語表記、生年月日、福岡第一高校Careerの開始・終了時期、高校時の登録項目 |

## 次の工程

Gemini調査Bを受領し、残る5人の公式URLを同じ方法で確認する。その後、10人分をまとめてCANDIDATE、Evidence、Issue、QAへ変換する。

この監査はVERIFIED、HUMAN APPROVAL、MASTER承認ではない。
