# Batch 002

作成日：2026-09-19
状態：CANDIDATE・初期QA完了
対象：B.LEAGUE公式一覧に掲載された福岡第一高校出身者10人

## 現在の結果

- Person候補：10件
- Career候補：24件
- Source：24件
- 項目別Evidence：102件
- 次段階レビュー待ち：28件
- CANDIDATE保留：6件
- 未解決事項：20件
- 構造QA：PASS

次段階レビュー待ちは、10人のPerson基本情報、10件のプロCareer、公式資料で確認できた高校Career 4件、大学・留学Career 4件である。残る高校Career 6件は、個別の公式登録資料をまだ確認していないため保留している。レビュー待ちのCareerでも、期間等の未確認項目は項目単位でHOLDしている。

松崎裕樹の2026-27所属について、Excel原本は滋賀としていたが、B.LEAGUE公式プロフィールとレバンガ北海道公式発表は北海道としている。原本を変更せず、Batch 002では新しいCareer候補`C000212`として2026年のレバンガ北海道加入を保持した。

## ファイル

| ファイル | 内容 |
| --- | --- |
| `person_candidates.csv` | 10人のPerson候補 |
| `organization_candidates.csv` | 今回のCareerが参照する11組織 |
| `career_candidates.csv` | 高校Career候補10件、プロCareer候補10件 |
| `source_references.csv` | B.LEAGUE公式一覧・選手詳細・クラブ公式発表 |
| `evidence_records.csv` | 項目ごとの出典位置と判定 |
| `issues.csv` | 高校・大学・原本矛盾の確認状況 |
| `qa_decisions.csv` | 次段階レビュー可否 |
| `qa_report.md` | Python構造検査結果 |
| `felo_intake_review.md` | Felo調査結果の採否と次の確認先 |
| `gemini_a_intake_review.md` | Gemini調査AのURL再確認、採用・不採用理由 |

受領した外部調査の原文は、[`Felo回答`](../../raw/research/batch_002/felo_2026-09-19.txt)と[`Gemini調査A`](../../raw/research/batch_002/gemini_a_2026-09-19.txt)に変更せず保存している。

## 再生成と検証

```bash
python3 scripts/build_batch_002_seed.py
python3 scripts/validate_pilot_batch.py data/candidate/batch_002
```

再生成スクリプトは2026-09-19に人間が確認した公式ページの値を定型CSVへ書き出す。Webサイトを自動取得するスクレイパーではない。公式ページの内容が更新された場合は、Sourceを再確認してスクリプト内の候補値と確認日を更新する。

このディレクトリはVERIFIED、HUMAN APPROVAL、MASTERではなく、公開サイトの正式データにも使用しない。
