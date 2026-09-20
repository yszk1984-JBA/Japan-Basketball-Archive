# Batch 004

作成日：2026-09-20
状態：Wave 1 CANDIDATE・構造QA完了

福岡第一高校をコアにしつつ、B.LEAGUE・NBAなどのプロCareerを持つ人物から優先して確認するバッチ。

## 進捗

| Wave | 対象 | 状態 |
| --- | --- | --- |
| 1 | 河村勇輝、児玉ジュニア | CANDIDATE作成・構造QA PASS |
| 2 | 河合瑠那、長岡大杜 | CANDIDATE作成・構造QA完了。7 Source、40 Evidence、8 HOLD、QA PASS |
| 3 | 重冨周希、重冨友希、キエキエ トピー アリ、遥天翼 | CANDIDATE作成・構造QA完了。9 Source、83 Evidence、11 HOLD、QA PASS |
| 4 | 今泉太陽、崎濱秀真 | 2人Waveでドラフト候補を確認予定 |

Wave 1の詳細は[`wave_01/README.md`](wave_01/README.md)を参照する。Wave 1ではFelo・Geminiの回答を補助に使用したが、Codexによる再確認との重複が大きかった。Wave 2以降はCodexが公式資料を直接確認し、解決しない項目だけを外部AIへ送る。

調査人数は固定せず、[`batch_size_metrics.csv`](batch_size_metrics.csv)へ実績を記録して調整する。現在は2人Waveとの比較のため、Wave 3で4人を試す。

HUMAN APPROVALとMASTER反映は行っていない。Webプロトタイプの表示データも変更していない。
