# AI_WORKFLOW — Governance v1.0

## AI運用体制

| 担当 | 役割 | 責務 |
| --- | --- | --- |
| Yuichi | Owner | 最終判断、Human verification、Master approval |
| ChatGPT | PM/CTO | planning、architecture、database design、development、automation、sprint review |
| Felo | Research Discovery | Web/PDFの広域検索、公式資料候補と表記揺れの発見 |
| Gemini | Research Verification | 公式資料の精査、該当箇所の抽出、矛盾・不明点の報告 |
| Claude | Data QA | duplicate、contradiction、source、schema review |
| Python | Automated Validation | ID・参照・形式・必須項目などの機械検証 |

CodexはChatGPTの開発・自動化作業を実行する支援環境として扱う。Master承認権限は持たない。この表は運用上の役割であり、各サービスの接続や自動連携が実装済みという意味ではない。

## 作業と引継ぎ

1. ChatGPTが目的、対象、成果物、受入条件を整理する。
2. Feloが広く資料を探し、公式資料候補、直接URL、表記揺れ、不明点を提出する。
3. Geminiが公式資料を精査し、項目、原文、資料内位置、矛盾、不明点を提出する。
4. ChatGPT / Codexが実在URLと該当箇所を再確認し、RAWからCANDIDATEへ整理する。調査AIの回答文自体はSourceにしない。
5. Claudeが重複、矛盾、出典の裏付け、スキーマ適合をレビューし、指摘と対象を記録する。未利用の場合はChatGPT / Codexが代替したことを記録する。
6. Pythonで自動検証する。ChatGPTが実行結果とQA指摘の解決状況を確認し、通過分をVERIFIEDレビュー候補として整理する。
7. YuichiがHuman verificationを行い、対象の版と範囲を明示してMaster approvalを行う。
8. 承認された範囲だけをMASTERへ反映し、ChatGPTがsprint reviewで成果と残課題を整理する。

引継ぎには対象ファイル・版、ID、出典位置、実施内容、未解決事項、検証結果を含める。担当サービスが未利用なら「未実施」と記録し、ClaudeによるQAやPython検証を実施したと偽らない。代替担当で進める場合はYuichiと合意し、実際の担当を残す。

## 判断の境界

AIはMaster Dataを直接承認・確定しない。AI同士の一致や自動検証合格もHuman approvalの代わりにはならない。不明情報は推測せず、矛盾は出典とともに提示する。承認方法と差戻しは[DATA_POLICY](DATA_POLICY.md)に従う。
