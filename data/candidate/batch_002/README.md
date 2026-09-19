# Batch 002

作成日：2026-09-19
状態：CANDIDATE・初期QA完了
対象：B.LEAGUE公式一覧に掲載された福岡第一高校出身者10人

## 現在の結果

- Person候補：10件
- Career候補：30件
- Source：39件
- 項目別Evidence：167件
- 次段階レビュー待ち：40件
- CANDIDATE保留：0件
- 未解決事項：19件
- 構造QA：PASS

次段階レビュー待ちは、10人のPerson基本情報、10件のプロCareer、公式資料で項目を確認できた高校Career 10件、大学・留学Career 10件である。Career全体を保留する候補は0件になったが、期間や役割など19件の未解決事項は項目単位でHOLDしている。

古野拓巳は、JUBF公式の第17回学生選抜大会プロフィールで日本経済大学3年の選手、出身校は福岡第一高と確認した。第18回大会結果では4年時の競技参加も確認した。日本経済大学Careerを追加したが、開始・終了年月は逆算せず空欄としている。

松崎裕樹の2026-27所属について、Excel原本は滋賀としていたが、B.LEAGUE公式プロフィールとレバンガ北海道公式発表は北海道としている。原本を変更せず、Batch 002では新しいCareer候補`C000212`として2026年のレバンガ北海道加入を保持した。

## ファイル

| ファイル | 内容 |
| --- | --- |
| `person_candidates.csv` | 10人のPerson候補 |
| `organization_candidates.csv` | 今回のCareerが参照する18組織 |
| `career_candidates.csv` | 高校・大学・留学・プロのCareer候補29件 |
| `source_references.csv` | B.LEAGUE、JBA、JUBF、学校・クラブ等の公式資料 |
| `evidence_records.csv` | 項目ごとの出典位置と判定 |
| `issues.csv` | 高校・大学・原本矛盾の確認状況 |
| `qa_decisions.csv` | 次段階レビュー可否 |
| `qa_report.md` | Python構造検査結果 |
| `felo_intake_review.md` | Felo調査結果の採否と次の確認先 |
| `gemini_a_intake_review.md` | Gemini調査AのURL再確認、採用・不採用理由 |
| `gemini_b_intake_review.md` | Gemini調査BのURL再確認、採用・不採用理由 |
| `furuno_followup_review.md` | 古野拓巳のJUBF公式資料による追加確認 |
| `verified_review_packet.md` | YuichiがVERIFIED候補作成前に確認する人物別レビュー資料 |

受領した外部調査の原文は、[`Felo回答`](../../raw/research/batch_002/felo_2026-09-19.txt)、[`Gemini調査A`](../../raw/research/batch_002/gemini_a_2026-09-19.txt)、[`Gemini調査B`](../../raw/research/batch_002/gemini_b_2026-09-19.txt)に変更せず保存している。

## 再生成と検証

```bash
python3 scripts/build_batch_002_seed.py
python3 scripts/validate_pilot_batch.py data/candidate/batch_002
python3 scripts/build_batch_002_review_packet.py
```

再生成スクリプトは2026-09-19に人間が確認した公式ページの値を定型CSVへ書き出す。Webサイトを自動取得するスクレイパーではない。公式ページの内容が更新された場合は、Sourceを再確認してスクリプト内の候補値と確認日を更新する。

このディレクトリはVERIFIED、HUMAN APPROVAL、MASTERではなく、公開サイトの正式データにも使用しない。
