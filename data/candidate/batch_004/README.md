# Batch 004

作成日：2026-09-20
状態：Wave 1-4 CANDIDATE・構造QA完了、VERIFIED候補作成済み／Wave 5（深掘りWave）CANDIDATE・構造QA完了

福岡第一高校をコアにしつつ、B.LEAGUE・NBAなどのプロCareerを持つ人物から優先して確認するバッチ。

## 進捗

| Wave | 対象 | 状態 |
| --- | --- | --- |
| 1 | 河村勇輝、児玉ジュニア | CANDIDATE作成・構造QA PASS |
| 2 | 河合瑠那、長岡大杜 | CANDIDATE作成・構造QA完了。7 Source、40 Evidence、8 HOLD、QA PASS |
| 3 | 重冨周希、重冨友希、キエキエ トピー アリ、遥天翼 | CANDIDATE作成・構造QA完了。9 Source、83 Evidence、11 HOLD、QA PASS |
| 4 | 今泉太陽、崎濱秀真 | CANDIDATE作成・構造QA完了。5 Source、31 Evidence、6 HOLD、QA PASS |
| 5（深掘りWave） | 河村勇輝（既存Master人物、NBA所属歴の追加調査） | CANDIDATE作成・構造QA完了。3 Source、14 Evidence、2 Issue、QA PASS |

Wave 1の詳細は[`wave_01/README.md`](wave_01/README.md)を参照する。Wave 1ではFelo・Geminiの回答を補助に使用したが、Codexによる再確認との重複が大きかった。Wave 2以降はCodexが公式資料を直接確認し、解決しない項目だけを外部AIへ送る。

調査人数は固定せず、[`batch_size_metrics.csv`](batch_size_metrics.csv)へ実績を記録して調整する。Wave 3の4人処理で再作業がなく、通常調査は4人を標準とする。ドラフト結果のように共通資料を確認する場合や、人物同定が難しい場合は2人単位へ縮小する。

HUMAN APPROVALとMASTER反映は行っていない。Webプロトタイプの表示データも変更していない。

次段階へ進める対象とHOLDの分離は[`review_packet/README.md`](review_packet/README.md)にまとめた。全Decisionの`eligible_fields`は[`data/verified/batch_004`](../../../verified/batch_004)へ抽出済みで、HUMAN APPROVALとMaster反映は未実施である。

## Wave 5（深掘りWave / Enrichment Wave）

Yuichiからの指示（2026-09-23）「河村勇輝（NBAの昨年の情報、今年の所属情報）… も情報が少ない」を受け、既にMASTER登録済みの河村勇輝（P000064）についてNBA所属歴を追加調査した深掘りWave。新規Person追加は行っていない。

### 経緯

MasterのCareerレコード（C000223、メンフィス・グリズリーズ Two-Way契約、2024-10-19発表分）が最新情報でなかったため、`data/master/corrections/`（構造エラー修正専用）ではなく、通常のCANDIDATE→QA→VERIFIED→HUMAN APPROVALのサイクルに則った新規Enrichment Waveとして追加調査を実施した。Master本体（`data/master/*.csv`）は一切変更していない。

### 主な成果

- シカゴ・ブルズとの1回目2Way契約（2025年7月20日発表、同年10月17日に契約解除）をバスケットボールキングの報道で確認（C000327、READY_FOR_VERIFIED_REVIEW）。
- シカゴ・ブルズとの2回目2Way契約（2026年1月7日再契約）を確認（C000328、organization_id/role/start はREADY、endは保留）。
- ロサンゼルス・クリッパーズとのエキシビット10契約（2026年8月9日発表、八村塁と同僚）を確認（C000329、organization_id/role/startはREADY、endは保留＝現在進行中の契約のため）。

### 新規Issue（未解決）

- **B4W5I0001**：メンフィス・グリズリーズを具体的にいつ離れたか（Bulls入団前の離脱時期）を示す直接資料が見つからず、C000223のend確定にはYuichiの追加判断または追加資料が必要。
- **B4W5I0002**：クリッパーズとの契約はエキシビット10契約（無保証のキャンプ契約）であり、レギュラーシーズン開幕までに状況が変わる可能性が高い。次回シーズン開幕後の再確認が必要。

### 未解決の設計上の論点（Yuichiの判断待ち）

現行の`build_site_candidate_data.py`は「既にMasterに存在するPersonはCANDIDATE公開データの生成対象から除外する」仕様（`if person_id in master_person_ids: continue`）になっている。そのため、本Waveで追加した河村勇輝のCANDIDATE事実（ブルズ・クリッパーズ在籍）は、VERIFIED→HUMAN APPROVAL→MASTER反映が完了するまで、候補データサイト上には一切表示されない。これは「未承認の事実をMaster確定データと並べて見せない」という意味では意図通りとも解釈できるが、既存Master人物に対する深掘りWaveの成果が公開サイト上で全く見えないままになる、という副作用もある。表示方法（例：Master人物ページに「未確定の追加情報あり」のバッジを出す等）を変更するかどうかはYuichiの判断が必要であり、本Waveでは現状維持（非表示のまま）としている。
