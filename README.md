# Japan Basketball Archive

日本のバスケットボールの歴史と人物のキャリアを、出典とともに記録するアーカイブです。将来の公開を目指しますが、現在のリポジトリはPrivateで運用します。

## 現在の段階

Governance v1.0に基づき、福岡第一高校パイロットを小規模バッチで検証しています。Batch 003はCANDIDATE・構造QA・Yuichiによる範囲指定を経てVERIFIEDを作成しました。HUMAN APPROVALとMaster Dataは未実施です。公開画面を早期に検証するため、確認中の少数データを使うWebプロトタイプを`site/`で並行開発しています。

## 原則

- AIはMaster Dataを直接承認・確定しない。最終承認者はOwnerのYuichi。
- 不明情報を推測しない。
- 事実にはSourceを持たせる。
- RAW → CANDIDATE → QA → VERIFIED → HUMAN APPROVAL → MASTER の順に進める。
- VERIFIEDは検証済みの候補であり、人間の承認済みを意味しない。

## 文書

- [PROJECT](docs/PROJECT.md)：目的・範囲
- [SCHEMA](docs/SCHEMA.md)：Person / Career / Organization / Source のデータ設計v0.1
- [DATA_POLICY](docs/DATA_POLICY.md)：出典・検証・承認ルール
- [AI_WORKFLOW](docs/AI_WORKFLOW.md)：AIと人間の担当
- [ROADMAP](docs/ROADMAP.md)：進め方と完了条件
- [FUTURE_ARCHITECTURE](docs/FUTURE_ARCHITECTURE.md)：検索・公開API・Data Factoryの将来方針
- [MONETIZATION_DRAFT_V0.1](docs/MONETIZATION_DRAFT_V0.1.md)：Talent Pipelineを軸にした収益化の検討案
- [PILOT_EXCEL_AUDIT_V0.1](docs/PILOT_EXCEL_AUDIT_V0.1.md)：福岡第一高校Excelの初回監査結果
- [PILOT_CANDIDATE_P000027](docs/PILOT_CANDIDATE_P000027.md)：欠落している人物参照の候補整理
- [PILOT_SOURCE_URL_REVIEW](docs/PILOT_SOURCE_URL_REVIEW.md)：Source URLの確認結果
- [PILOT_EVIDENCE_FORMAT_V0.1](docs/PILOT_EVIDENCE_FORMAT_V0.1.md)：項目別出典を記録する最小形式案
- [PILOT_BATCH_001_PROPOSAL](docs/PILOT_BATCH_001_PROPOSAL.md)：最初の5人で行う小規模検証案
- [DATA_SCALING_WORKFLOW_V0.1](docs/DATA_SCALING_WORKFLOW_V0.1.md)：データ量と品質を並行して高めるバッチ運用
- [BATCH_002_BLEAGUE_PROPOSAL](docs/BATCH_002_BLEAGUE_PROPOSAL.md)：B.LEAGUE公式一覧から選んだ次の10人
- [BATCH_003_PROPOSAL](docs/BATCH_003_PROPOSAL.md)：既存バッチと重複しない次の10人
- [BATCH_003_RESEARCH_PROMPTS](docs/BATCH_003_RESEARCH_PROMPTS.md)：Felo・Gemini用の一括調査指示文
- [BATCH_004_PROPOSAL](docs/BATCH_004_PROPOSAL.md)：福岡第一からプロへ進んだ人物を優先する次の10人
- [BATCH_004_RESEARCH_PROMPTS](docs/BATCH_004_RESEARCH_PROMPTS.md)：Batch 004のFelo・Gemini用調査指示文
- [BATCH_002_RESEARCH_PROMPTS](docs/BATCH_002_RESEARCH_PROMPTS.md)：Feloによる資料発見とGeminiによる公式資料精査の指示文
- [Pilot Batch 001](data/candidate/pilot_batch_001/README.md)：5人分のCANDIDATE、項目別出典、未解決事項、構造QA
- [Batch 002](data/candidate/batch_002/README.md)：B.LEAGUE公式を入口にした10人分のCANDIDATEと初期QA
- [Batch 003 CANDIDATE](data/candidate/batch_003/README.md)：次の10人の調査、CANDIDATE、QA、レビュー資料
- [Batch 003 VERIFIED](data/verified/batch_003/README.md)：全28 Decision IDの確認済み項目とHOLD分離
- [AGENTS](AGENTS.md)：このリポジトリで作業するAIへの指示

## 将来の配置

```text
data/raw/        原資料（変更しない）
data/candidate/  抽出・整理した候補とQA記録
data/verified/   QAと自動検証を通過した承認待ちデータ
data/master/     Yuichiが明示的に承認した正式データ
scripts/         自動検証など
site/            公開サイト
```

`data/candidate/`と`scripts/`はBatch 001から、`data/verified/`はBatch 003から使用しています。`data/master/`は未作成です。`site/`にはMaster Dataと分離したWebプロトタイプを置きます。

## GitHubでの基本操作

変更はファイルの編集、commitは変更内容をローカルの履歴に保存、pushはcommitをGitHubに送る操作です。変更差分を確認してからcommitし、その後pushします。文書のcommitやpushは、Master Dataの承認を意味しません。公開設定の変更やサイト公開は別の判断です。
