# Japan Basketball Archive

日本のバスケットボールの歴史と人物のキャリアを、出典とともに記録するアーカイブです。将来の公開を目指しますが、現在のリポジトリはPrivateで運用します。

## 現在の段階

Governance v1.0：運用ルールとデータ設計v0.1を整備する段階です。既存の福岡第一高校パイロットデータは今後取り込みます。データ移行・検証プログラム・サイトは未実装です。

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

上記は予定です。現在は文書のみ作成します。

## GitHubでの基本操作

変更はファイルの編集、commitは変更内容をローカルの履歴に保存、pushはcommitをGitHubに送る操作です。変更差分を確認してからcommitし、その後pushします。文書のcommitやpushは、Master Dataの承認を意味しません。公開設定の変更やサイト公開は別の判断です。
