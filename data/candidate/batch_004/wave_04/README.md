# Batch 004 Wave 4

作成日：2026-09-21
状態：CANDIDATE作成・構造QA完了

対象：今泉太陽、崎濱秀真

このフォルダはB.LEAGUEと全日本大学バスケットボール連盟の公式資料から作成した候補データである。VERIFIED、HUMAN APPROVAL、MASTERではない。

## 結果

- Person：2人
- Organization：3件
- Career：4件
- Source：5件
- Evidence：31件
- Issue：6件
- QA Decision：9件
- Python構造QA：PASS、エラー0件
- VERIFIED、HUMAN APPROVAL、MASTER：未実施

## 調査上の要点

- 両名はB.LEAGUE DRAFT 2026の候補者として掲載されている。
- 候補者掲載と、プロ契約・リーグ登録・公式戦出場は別の事実として分離した。
- 今泉太陽は日本経済大学、崎濱秀真は新潟経営大学のJUBF公式大会ロスターと出場記録を確認した。
- B.LEAGUE公式指名結果に両名の氏名は確認できないが、不在だけを根拠に別の状態を断定しない。
- 高校期間はB.LEAGUE候補者経歴で確認した。高校バスケットボール部でのPlayer役割は直接ロスター未確認のため保留した。

## 検証

```bash
python3 scripts/build_batch_004_wave_04.py
python3 scripts/validate_pilot_batch.py data/candidate/batch_004/wave_04
```
