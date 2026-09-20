# AI_WORKFLOW — Governance v1.0

## AI運用体制

| 担当 | 役割 | 責務 |
| --- | --- | --- |
| Yuichi | Owner | 最終判断、Human verification、Master approval |
| ChatGPT / Codex | PM/CTO・標準調査 | planning、公式資料の直接確認、CANDIDATE作成、development、automation、sprint review |
| Felo | 例外調査 | 通常調査で公式資料が見つからない人物のWeb/PDF探索、表記揺れの発見 |
| Gemini | 例外資料精査 | 読みにくいPDF、海外資料、表記揺れ、長文資料の補助的な精査 |
| Claude | バッチQA | 10〜20人単位のduplicate、contradiction、source、schema review |
| Python | Automated Validation | ID・参照・形式・必須項目などの機械検証 |

CodexはChatGPTの開発・自動化作業を実行する支援環境として扱う。Master承認権限は持たない。この表は運用上の役割であり、各サービスの接続や自動連携が実装済みという意味ではない。

## 作業と引継ぎ

1. ChatGPTが目的、対象、成果物、受入条件を整理する。
2. ChatGPT / CodexがB.LEAGUE、クラブ、JBA、大学連盟等の公式資料を直接検索・確認する。
3. 確認できた値、直接URL、資料内位置、確認日を項目別EvidenceとしてRAWからCANDIDATEへ整理する。
4. 通常調査で解決しない人物だけを例外キューへ移し、Feloで追加探索、Geminiで難しい資料の精査を行う。両者の回答文自体はSourceにしない。
5. 10〜20人分が揃った段階でClaudeが重複、矛盾、出典の裏付け、スキーマ適合をレビューする。未利用の場合はChatGPT / Codexが代替したことを記録する。
6. PythonでID・参照・形式等を自動検証する。ChatGPTが実行結果とQA指摘の解決状況を確認し、通過分をVERIFIEDレビュー候補として整理する。
7. YuichiがHuman verificationを行い、対象の版と範囲を明示してMaster approvalを行う。
8. 承認された範囲だけをMASTERへ反映し、ChatGPTがsprint reviewで成果と残課題を整理する。

通常の選手調査ではFelo・Geminiを必須工程にしない。外部AIへの貼り付けと再確認が重複するため、公式プロフィール等を直接取得できる場合はCodexからCANDIDATEへ進める。

引継ぎには対象ファイル・版、ID、出典位置、実施内容、未解決事項、検証結果を含める。担当サービスが未利用なら「未実施」と記録し、ClaudeによるQAやPython検証を実施したと偽らない。代替担当で進める場合はYuichiと合意し、実際の担当を残す。

## 判断の境界

AIはMaster Dataを直接承認・確定しない。AI同士の一致や自動検証合格もHuman approvalの代わりにはならない。不明情報は推測せず、矛盾は出典とともに提示する。承認方法と差戻しは[DATA_POLICY](DATA_POLICY.md)に従う。
