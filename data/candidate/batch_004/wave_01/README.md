# Batch 004 Wave 1

作成日：2026-09-20
状態：CANDIDATE作成・構造QA完了

対象：河村勇輝、児玉ジュニア

## 結果

- Person：2人
- Organization：6件
- Career：8件
- Source：12件
- Evidence：58件
- Issue：8件
- QA Decision：16件
- Python構造QA：PASS、エラー0件
- Claudeによる独立QA：未実施
- VERIFIED、HUMAN APPROVAL、MASTER：未実施

## 主な確認事項

- 河村勇輝はJBA資料で福岡第一高校と東海大学、B.LEAGUE公式で三遠・横浜BCの所属履歴と出場、Memphis Grizzlies公式でTwo-Way契約を確認した。
- 河村勇輝の現在所属は、Clippers選手ページとNBA G Leagueページの表示時点が一致しないためHOLDにした。
- 児玉ジュニアはJUBF資料で日本経済大学の大会登録、三遠公式で大学男子部退部と新規・継続契約、B.LEAGUE公式で2025-26シーズン44試合出場を確認した。
- 児玉ジュニアの2025年10月5日の個別試合出場は、今回の直接確認で本人欄を再取得できずHOLDにした。
- 日本経済大学の既存Organization IDがBatch間で重複している。今回はより新しいBatch 003の`ORG000017`を使用し、Master前の正規化課題として記録した。

## ファイル

| ファイル | 内容 |
| --- | --- |
| `person_candidates.csv` | 2人の最小Person候補 |
| `organization_candidates.csv` | Careerが参照する組織候補 |
| `career_candidates.csv` | 公式資料で確認したCareer候補 |
| `source_references.csv` | 公式Sourceと確認日 |
| `evidence_records.csv` | 項目別の資料内位置と判定 |
| `issues.csv` | 未確認期間、表示矛盾、個別試合、ID重複 |
| `qa_decisions.csv` | 項目単位の次段階レビュー可否 |
| `qa_report.md` | Python構造QA結果 |

受領したGemini原文は[`data/raw/research/batch_004/gemini_wave_01_2026-09-20.txt`](../../../raw/research/batch_004/gemini_wave_01_2026-09-20.txt)、監査結果は[`wave_01_gemini_intake_review.md`](../wave_01_gemini_intake_review.md)に保存した。

## 検証

```bash
python3 scripts/build_batch_004_wave_01.py
python3 scripts/validate_pilot_batch.py data/candidate/batch_004/wave_01
```

PASSはCSVのID・参照・必須項目・判定値の形式が規則に合うことだけを示す。史実の正しさ、VERIFIED、HUMAN APPROVAL、MASTERを意味しない。
