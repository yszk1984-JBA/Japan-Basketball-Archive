# Batch 004 Wave 2

作成日：2026-09-20
状態：CANDIDATE作成・構造QA完了

対象：河合瑠那、長岡大杜

このフォルダは公式資料から作成した候補データである。VERIFIED、HUMAN APPROVAL、MASTERではない。

## 結果

- Person：2人
- Organization：4件
- Career：5件
- Source：7件
- Evidence：40件
- Issue：8件
- QA Decision：11件
- Python構造QA：PASS、エラー0件
- VERIFIED、HUMAN APPROVAL、MASTER：未実施

## 重要な保留

- 河合瑠那の身長は、JUBF 180cm、B.LEAGUE 181cm、クラブ発表183cmで異なる。時点別の原文を保持し、単一値に統合しない。
- 長岡大杜は、`docs/BATCH_004_PROPOSAL.md`では「Excel原本内の同名候補あり」とされていたが、原本Personシートに同名人物は存在しなかった。このため新規CANDIDATE IDを付け、不一致をIssueに残した。
- B.LEAGUEプロフィールに連結表示された「リーグ登録国籍特別指定」は国籍値として採用しない。
- 発表日と実際の所属開始日・終了日は区別する。

## 検証

```bash
python3 scripts/build_batch_004_wave_02.py
python3 scripts/validate_pilot_batch.py data/candidate/batch_004/wave_02
```

構造QAのPASSは史実の正しさやMaster承認を意味しない。
