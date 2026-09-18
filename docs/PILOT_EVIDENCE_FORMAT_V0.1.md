# 項目別出典記録 最小形式案 v0.1

作成日：2026-09-19  
状態：Draft  
目的：福岡第一高校パイロットのCANDIDATEとQAで、値と出典箇所を追跡できるようにする。

## 位置づけ

この形式はPerson / Career / Organization / Sourceに続く新しい中心エンティティではない。Governance v1.0で求める出典対応、QA結果、不明点を記録する付随記録案である。

Excel原本のEvidenceシートを参考にするが、既存の`Confirmed`等をそのまま採用しない。この文書だけではデータ取込、Schema拡張、VERIFIED化、Master反映を許可しない。

## 最小項目

| 項目 | 必須 | 内容 | 例 |
| --- | --- | --- | --- |
| record_id | 必須 | 付随記録の一意なID | PE000001 |
| entity_type | 必須 | Person / Career / Organization | Person |
| entity_id | 必須 | 対象ID | P000027 |
| field_name | 必須 | 裏付け対象の項目名 | full_name_ja |
| candidate_value | 任意 | 資料から読み取った候補値。不明なら空欄 | ウッズジェリオ 翔 |
| source_id | 必須 | Sourceの参照ID | SRC000012 |
| source_locator | 必須 | ページ、表、見出し、Excelシート・行等 | 九州／男子 → 福岡第一 |
| evidence_summary | 必須 | 該当箇所の短い要約 | 福岡第一欄に氏名を掲載 |
| assessment | 必須 | SUPPORTED / PARTIAL / CONFLICT / UNVERIFIED | PARTIAL |
| checked_at | 必須 | 実際に確認した日 | 2026-09-18 |
| issue_note | 任意 | 表記揺れ、矛盾、未確認事項 | 公式氏名は未確認 |

## assessmentの意味

| 値 | 使用条件 |
| --- | --- |
| SUPPORTED | 指定した資料箇所が、その項目の候補値を直接裏付ける |
| PARTIAL | 値の一部、時点、関係の一部だけを裏付ける |
| CONFLICT | 別資料または既存候補と矛盾する |
| UNVERIFIED | URLや資料候補はあるが、本文の該当箇所を確認できていない |

`SUPPORTED`はGovernance上のVERIFIEDまたはMASTERを意味しない。資料と候補値の対応だけを表す。

## 記録単位

1行で1項目だけを扱う。同じ資料が氏名、身長、所属を示していても、field_nameを分けて3行にする。これにより、資料が裏付けていない値まで行全体の事実として扱うことを防ぐ。

不明値は`candidate_value`を空欄にし、`issue_note`へ不明理由を書く。推定値で埋めない。

## 例

| record_id | entity_type | entity_id | field_name | candidate_value | source_id | source_locator | evidence_summary | assessment | checked_at | issue_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PE000001 | Person | P000027 | full_name_ja | ウッズジェリオ 翔 | SRC000012 | 九州／男子 → 福岡第一 | 福岡第一欄に氏名を掲載 | PARTIAL | 2026-09-18 | 公式表記は未確認 |
| PE000002 | Career | C000045 | organization_id |  | SRC000012 | 九州／男子 → 福岡第一 | 進路は「留学」とのみ記載 | UNVERIFIED | 2026-09-18 | 留学先組織を特定できない |
| PE000003 | Career | C000017 | role | Manager | SRC000012 | 九州／男子 → 福岡第一 | 氏名の後に「マネ」と記載 | SUPPORTED | 2026-09-18 | 福岡第一での役割に限定 |

## 既存Evidenceからの対応

| 既存列 | 対応 |
| --- | --- |
| evidence_id | record_id候補 |
| entity_type | そのまま利用候補 |
| entity_id | そのまま利用候補。ただし参照先の存在確認が必要 |
| field_name | そのまま利用候補 |
| source_id | そのまま利用候補 |
| evidence_statement | evidence_summary候補 |
| verification_status | 自動移行しない。assessmentを資料箇所から再判定 |
| verified_date | checked_atへ自動移行しない。実際の再確認日を記録 |
| notes | issue_note候補 |

既存Evidenceには`candidate_value`と`source_locator`がないため、取込前に原資料を再確認して補う。

## QA条件

- entity_idが対象表に存在する。
- source_idがSourceに存在する。
- source_locatorから人間が同じ箇所を再確認できる。
- candidate_valueが資料の表記・精度を超えていない。
- 1行に複数の独立した事実をまとめていない。
- 不明・矛盾をSUPPORTEDにしていない。
- assessmentをVERIFIEDまたはMaster承認として扱っていない。

## 保存形式

最初の5人では、レビューしやすい表形式で試す。CSV、JSON、データベース等の正式な保存形式は、実測後に決める。
