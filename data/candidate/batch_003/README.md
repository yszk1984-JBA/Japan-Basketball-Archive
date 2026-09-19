# Batch 003

作成日：2026-09-19

状態：CANDIDATE作成・構造QA完了、全Decision IDからVERIFIED作成済み

対象：[Batch 003の10人](../../../docs/BATCH_003_PROPOSAL.md)

## 現在の状況

- Felo回答：受領済み
- Felo回答の直接URL：0件
- Codexが独立して回収・確認した公式URL：2件
- Gemini調査A：受領・公式URL監査済み
- Gemini調査B：受領・公式URL監査済み
- Gemini調査Aで再確認した公式Source候補：7件
- Gemini調査BはURL提示0件。Codexの再検索で5人全員の公式Source候補を確認
- Person：10人
- Career：18件
- Organization：9件
- Source：28件
- Evidence：196件
- Issue：24件（未解決23件、解決済み1件）
- Python構造QA：PASS、エラー0件
- Claudeによる独立QA：未実施
- VERIFIED：2026-09-20に全28 Decision IDのeligible_fieldsから作成済み
- HUMAN APPROVAL、MASTER、公開サイト：未変更

## ファイル

| ファイル | 内容 |
| --- | --- |
| `felo_intake_review.md` | Felo回答のURL監査、採用候補、HOLD理由 |
| `gemini_a_intake_review.md` | Gemini調査Aの公式URL監査、採用候補、HOLD理由 |
| `gemini_b_intake_review.md` | Gemini調査Bの公式URL監査、矛盾、採用候補、HOLD理由 |
| `person_candidates.csv` | 10人の最小Person候補 |
| `organization_candidates.csv` | Careerが参照する組織候補 |
| `career_candidates.csv` | 公式資料で組織と役割を確認できたCareer候補 |
| `source_references.csv` | 使用した公式Sourceと確認日 |
| `evidence_records.csv` | 項目ごとの資料内位置、候補値、判定 |
| `issues.csv` | 期間不明、資料間矛盾、役割修正などの記録 |
| `qa_decisions.csv` | 項目単位の次段階レビュー可否 |
| `qa_report.md` | Python構造QAの結果 |
| `verified_review_packet.md` | Yuichiが人物別・項目別に確認するためのレビュー資料 |

外部調査の原文は[`Felo回答`](../../raw/research/batch_003/felo_2026-09-19.txt)、[`Gemini調査A`](../../raw/research/batch_003/gemini_a_2026-09-19.txt)、[`Gemini調査B`](../../raw/research/batch_003/gemini_b_2026-09-20.txt)へ保存している。

## 主な保留・修正

- 入学・卒業年月は、学年から逆算せず全Careerで保留した。
- 鷹野祐磨の卒業後Careerは公式資料を確認できず、作成していない。
- 當山修梧はJUBFの2021年・2022年がともに2年表示のため、学年を次段階レビュー対象から外した。
- カマレ ムレマ フランシスの大学背番号はJUBF公式の#70を候補とし、外部回答の#75は不採用とした。
- 本松龍斗は日本体育大学のPlayerではなく、公式PROFILEに基づくStudent Coachとして候補化した。
- 福岡第一高校との関係しか確認できない本松龍斗について、高校Careerは作成していない。

## 検証

```bash
python3 scripts/validate_pilot_batch.py data/candidate/batch_003
```

PASSはID、参照、必須項目、判定値の形式が規則に合うことだけを示す。史実の正しさ、VERIFIED、HUMAN APPROVAL、MASTERを意味しない。

VERIFIED出力は[`data/verified/batch_003`](../../verified/batch_003/README.md)に保存した。次はVERIFIEDの差分、HOLD項目、SourceをYuichiが確認し、Masterへ進める範囲を別途明示する。VERIFIED作成許可はMaster承認として扱わない。
