# Batch 004

作成日：2026-09-20
状態：Wave 1-4 CANDIDATE・構造QA・次段階レビュー資料作成完了

福岡第一高校をコアにしつつ、B.LEAGUE・NBAなどのプロCareerを持つ人物から優先して確認するバッチ。

## 進捗

| Wave | 対象 | 状態 |
| --- | --- | --- |
| 1 | 河村勇輝、児玉ジュニア | CANDIDATE作成・構造QA PASS |
| 2 | 河合瑠那、長岡大杜 | CANDIDATE作成・構造QA完了。7 Source、40 Evidence、8 HOLD、QA PASS |
| 3 | 重冨周希、重冨友希、キエキエ トピー アリ、遥天翼 | CANDIDATE作成・構造QA完了。9 Source、83 Evidence、11 HOLD、QA PASS |
| 4 | 今泉太陽、崎濱秀真 | CANDIDATE作成・構造QA完了。5 Source、31 Evidence、6 HOLD、QA PASS |

Wave 1の詳細は[`wave_01/README.md`](wave_01/README.md)を参照する。Wave 1ではFelo・Geminiの回答を補助に使用したが、Codexによる再確認との重複が大きかった。Wave 2以降はCodexが公式資料を直接確認し、解決しない項目だけを外部AIへ送る。

調査人数は固定せず、[`batch_size_metrics.csv`](batch_size_metrics.csv)へ実績を記録して調整する。Wave 3の4人処理で再作業がなく、通常調査は4人を標準とする。ドラフト結果のように共通資料を確認する場合や、人物同定が難しい場合は2人単位へ縮小する。

HUMAN APPROVALとMASTER反映は行っていない。Webプロトタイプの表示データも変更していない。

次段階へ進める対象とHOLDの分離は[`review_packet/README.md`](review_packet/README.md)にまとめた。VERIFIED候補作成は、Yuichiが対象・範囲を明示して判断した後に行う。
