# Batch 005 Wave 1

作成日：2026-09-21
状態：CANDIDATE作成・構造QA完了

対象：崎濱秀斗、轟琉維、佐藤涼成、河合瑠那

このフォルダは、B.LEAGUE、琉球ゴールデンキングス、アルバルク東京、横浜ビー・コルセアーズ、広島ドラゴンフライズ、横浜エクセレンスの公式資料から作成した候補データである。VERIFIED、HUMAN APPROVAL、MASTERではない。

## 結果

- Person：4人（新規2人、既存2人）
- Organization：11件（新規5件、既存6件）
- Career：11件（新規10件、既存ID再利用1件）
- Source：15件
- Evidence：78件
- Issue：9件
- QA Decision：26件
- Python構造QA：PASS、エラー0件
- VERIFIED、HUMAN APPROVAL、MASTER：未実施

## 調査上の要点

- 崎濱秀斗は、福岡第一高校、琉球U18、セントトーマス モア スクール、琉球トップチームの経路を確認した。
- 琉球との特別指定選手プロ契約、B1公式戦出場、活動終了・退団を別の事実として記録した。
- 轟琉維は、アルバルク東京での加入、リーグ登録、B1初出場、活動終了をクラブ公式で確認した。
- 轟琉維の佐賀所属とB1出場はB.LEAGUE公式で確認した。佐賀のクラブ一次資料による契約・登録区分はHOLDとした。
- 佐藤涼成は、横浜BCの特別指定選手登録と出場、広島のプロ契約、2026-27以降の契約継続を分離して記録した。
- 河合瑠那は既存Career ID `C000229`を再利用し、横浜EXでの登録、B2出場、活動終了発表、自由交渉選手リスト公示予定を記録した。
- 身長差、未確認の在籍期間、正確な登録抹消日は推測せずHOLDに残した。

## 検証

```bash
python3 scripts/build_batch_005_wave_01.py
python3 scripts/validate_pilot_batch.py data/candidate/batch_005/wave_01
```
