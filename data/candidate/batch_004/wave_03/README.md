# Batch 004 Wave 3

作成日：2026-09-20
状態：CANDIDATE作成・構造QA完了

対象：重冨周希、重冨友希、キエキエ トピー アリ、遥天翼

このフォルダは公式資料から作成した候補データである。VERIFIED、HUMAN APPROVAL、MASTERではない。

## 結果

- Person：4人
- Organization：14件
- Career：21件
- Source：9件
- Evidence：83件
- Issue：11件
- QA Decision：39件
- Python構造QA：PASS、エラー0件
- 再作業：0件
- VERIFIED、HUMAN APPROVAL、MASTER：未実施

## 調査上の要点

- 重冨兄弟は専修大学公式PDFで、2017年度入部、福岡第一高出身、別人としての氏名と学部を同時確認した。
- キエキエ トピー アリはBatch 003の既存`P000014`を使い、鹿児島と横浜EXのプロCareerだけを追加候補化した。
- 遥天翼は選手Careerと、茨城U15ヘッドコーチ、熊本アシスタントコーチを役割別Careerとして分けた。
- 学校名だけを示す資料は、学校バスケットボール部でのPlayer役割の完全な裏付けにはしない。

## 検証

```bash
python3 scripts/build_batch_004_wave_03.py
python3 scripts/validate_pilot_batch.py data/candidate/batch_004/wave_03
```
