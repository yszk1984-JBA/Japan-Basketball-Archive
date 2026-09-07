# AI_WORKFLOW — Governance v1.0

## AI運用体制

| 担当 | 役割 | 責務 |
| --- | --- | --- |
| Yuichi | Owner | 最終判断、Human verification、Master approval |
| ChatGPT | PM/CTO | planning、architecture、database design、development、automation、sprint review |
| Gemini | Research | Web/PDF research、data extraction、source discovery、candidate data |
| Claude | Data QA | duplicate、contradiction、source、schema review |
| Python | Automated Validation | ID・参照・形式・必須項目などの機械検証 |

CodexはChatGPTの開発・自動化作業を実行する支援環境として扱う。Master承認権限は持たない。この表は運用上の役割であり、各サービスの接続や自動連携が実装済みという意味ではない。

## 作業と引継ぎ

1. ChatGPTが目的、対象、成果物、受入条件を整理する。
2. Geminiが資料を調査し、原資料参照・抽出結果・不明点を候補として提出する。
3. Claudeが重複、矛盾、出典の裏付け、スキーマ適合をレビューし、指摘と対象を記録する。
4. Pythonで自動検証する。ChatGPTが実行結果とQA指摘の解決状況を確認し、通過分をVERIFIEDとして整理する。
5. YuichiがHuman verificationを行い、対象の版と範囲を明示してMaster approvalを行う。
6. 承認された範囲だけをMASTERへ反映し、ChatGPTがsprint reviewで成果と残課題を整理する。

引継ぎには対象ファイル・版、ID、出典位置、実施内容、未解決事項、検証結果を含める。担当サービスが未利用なら「未実施」と記録し、ClaudeによるQAやPython検証を実施したと偽らない。代替担当で進める場合はYuichiと合意し、実際の担当を残す。

## 判断の境界

AIはMaster Dataを直接承認・確定しない。AI同士の一致や自動検証合格もHuman approvalの代わりにはならない。不明情報は推測せず、矛盾は出典とともに提示する。承認方法と差戻しは[DATA_POLICY](DATA_POLICY.md)に従う。
