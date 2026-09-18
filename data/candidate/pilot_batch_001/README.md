# Pilot Batch 001

作成日：2026-09-19
状態：CANDIDATE
対象：福岡第一高校パイロット5人

## 注意

このディレクトリは候補データであり、VERIFIED、HUMAN APPROVAL、MASTERではない。公開サイトの正式データとして使用しない。

Excel原本を変更せず、公開Sourceの本文を再確認して作成した。不明値は空欄とし、推定で補っていない。

## ファイル

| ファイル | 内容 |
| --- | --- |
| `person_candidates.csv` | 5人の最小Person候補 |
| `organization_candidates.csv` | 今回のCareerが参照する組織候補 |
| `career_candidates.csv` | 資料で組織と役割を確認できたCareer候補 |
| `source_references.csv` | 使用したSourceと今回の確認日 |
| `evidence_records.csv` | 項目ごとの出典位置と判定 |
| `issues.csv` | 未解決事項と、Career化しなかった理由 |
| `qa_decisions.csv` | 項目単位の次段階レビュー可否。VERIFIED化そのものではない |
| `qa_report.md` | Python検査結果。スクリプト実行時に更新 |

## 対象人物

- P000012 ジャン・ローレンス・ハーパージュニア
- P000013 松本 宗志
- P000011 砂川 琉勇
- P000017 泉美 優知
- P000027 ウッズジェリオ 翔

## 今回Career化しない情報

- P000011の明星大学：進学予定の専門媒体情報はあるが、実在籍・競技参加を確認できない。
- P000017の中央工学校：進路情報はあるが、入学事実と進学先での役割を確認できない。
- P000027の留学：国、学校、組織、入学、競技参加を確認できない。

これらは`issues.csv`に残し、OrganizationやCareerを推測作成しない。

## 検証

```bash
python3 scripts/validate_pilot_batch.py data/candidate/pilot_batch_001
```

検査合格は構造上の問題がないことだけを示し、史実の正しさやMaster承認を意味しない。

`READY_FOR_VERIFIED_REVIEW`はYuichiが差分と出典を確認する対象であり、VERIFIED、HUMAN APPROVAL、MASTERのいずれも意味しない。
