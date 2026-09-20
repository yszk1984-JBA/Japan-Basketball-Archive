# Batch 005 Wave 1 次段階レビュー資料

作成日：2026-09-21

この資料はCANDIDATEからVERIFIED候補へ進める項目を選別したQA記録です。この資料の作成だけではHUMAN APPROVAL、MASTER、公開サイトへの反映を行いません。

## 対象

- Person：4人
- Career：11件
- Organization：11件
- Source：15件
- Evidence：78件
- QA Decision：26件
- HOLD Issue：9件

## VERIFIED候補の選別範囲

- Person Decision：4件
- Career Decision：11件
- Organization Decision：11件
- 全Decisionの現在判定：`READY_FOR_VERIFIED_REVIEW`
- 詳細：[`verification_scope.csv`](verification_scope.csv)

`eligible_fields`だけをVERIFIED候補に含めます。`held_fields`とHOLD Issueは除外します。

## HOLDの内訳

- `ACTIVITY_END_DATE`：2件
- `CAREER_END_DATE`：1件
- `HEIGHT_BY_DATE`：1件
- `HEIGHT_BY_SOURCE`：1件
- `HIGH_SCHOOL_PERIOD`：1件
- `SAGA_CONTRACT_REGISTRATION`：1件
- `SCHOOL_END_DATE`：1件
- `UNIVERSITY_PERIOD`：1件

詳細は[`held_issues.csv`](held_issues.csv)にあり、追加確認先も記録しています。

## 重複・ID再利用確認

- `P000028`佐藤涼成と`P000066`河合瑠那は既存Person IDを再利用しています。
- `C000229`河合瑠那の横浜エクセレンスCareerは既存Career IDを再利用しています。
- 福岡第一高等学校、東海大学、佐賀バルーナーズ、横浜ビー・コルセアーズ、横浜エクセレンス、白鷗大学は既存Organization IDを再利用しています。
- 崎濱秀斗と崎濱秀真は名が異なるため別Person IDです。

## 選別上の境界

- プロ契約、リーグ登録、公式戦出場、活動終了を別項目として扱います。
- 轟琉維の佐賀での所属・出場は対象に含め、クラブ一次資料で未確認の契約・登録区分は除外します。
- 身長の資料間差、学校・大学の未確認期間、正確な登録抹消日は除外します。
- VERIFIED候補はHuman ApprovalまたはMasterではありません。

## 対象Decision ID

B5W1D0001、B5W1D0002、B5W1D0003、B5W1D0004、B5W1D0005、B5W1D0006、B5W1D0007、B5W1D0008、B5W1D0009、B5W1D0010、B5W1D0011、B5W1D0012、B5W1D0013、B5W1D0014、B5W1D0015、B5W1D0016、B5W1D0017、B5W1D0018、B5W1D0019、B5W1D0020、B5W1D0021、B5W1D0022、B5W1D0023、B5W1D0024、B5W1D0025、B5W1D0026
