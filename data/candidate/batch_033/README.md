# Batch 033：ロスター起点の横展開（B.ONE 2026-27）CANDIDATE段階

作成日：2026-09-30

Yuichiの指示（2026-09-30）「B.ONEの25クラブについても進める」。手順・登録ルールはBatch 032（B.PREMIER）と同じ（`docs/ROSTER_EXPANSION_PLAN.md`、`scripts/build_batch_032_roster.py 33`）。

## 結果

- 対象：B.ONE 25クラブの2026-27公式選手一覧（国籍区分「日本」、231名）のうち、Master・候補のSourceにPlayerIDがない184名
- 新規Person：**182名**（P000382〜P000563、5 Wave）
- Career：896件（学校317件＋クラブ579件）
- 新規Organization：122件（ほぼ出身校。`new_organizations.csv`）。Batch 032で作成したOrganization（アイシン アレイオンズ、東海大学付属札幌高等学校など）は作り直さず再利用した
- 検証：PASS（`validation_report.md`）
- 18歳未満：該当なし

## 登録しなかった2名（`excluded.csv`）

| 選手 | クラブ | 理由 |
| --- | --- | --- |
| 宮田諭 | 東京U | 公式プロフィールが空欄（生年月日・出身校なし） |
| ジュフ・伴馬 | 熊本 | 同上 |

## Batch 032からの追加ルール

- 表記ゆれの寄せ先を追加（都道府県名の有無・略称のみの違い）：宇都宮工業→栃木県立宇都宮工業、東海大付属浦安→東海大学付属浦安、大阪市立桜宮高校→桜宮、小林→宮崎県立小林、松山工業→愛媛県立松山工業、静岡県沼津私立飛龍→飛龍、宮崎県私立延岡学園→延岡学園、愛知県中部大学第一→中部大学第一
- 「神戸市立科学技術高等学校」は、batch_007 wave_11で登録済みの「御影工業高等学校」（ORG000356、改称前の名称）と同じOrganizationにした
- 出身校欄の「 - 」「/」も学校の区切りとして扱う（例：北陸学院高等学校 - セントトーマスモアスクール）
- 「千葉ジェッツふなばしU18」はクラブのユースチームのため学校として登録しない
- ORG000017（日本経済大学の旧重複ID、Masterで統合済み）は照合対象から外した

## Issue（HOLD、VERIFIEDには含めない）

| 種類 | 件数 |
| --- | ---: |
| HIGH_SCHOOL_PERIOD / UNIVERSITY_PERIOD | 163 / 154 |
| ORG_NAME_HISTORY | 57 |
| PRE_BLEAGUE_HISTORY | 40 |
| SCHOOL_NOT_LISTED | 20 |
| SAME_SEASON_TWO_CLUBS | 15 |
| SCHOOL_NAME_UNREADABLE | 1（ポーグ健の大学「白?大学」） |
| NON_SCHOOL_ENTRY | 1（クーリバリ セリンムルタラの「千葉ジェッツふなばしU18」） |
| ENROLLED_STUDENT | 1（関谷間、NHK学園高等学校「在学中」） |

## 確認してほしい点（Yuichi）

- 「富田高等学校」（植田碧羽）と「私立富田高等学校」（高橋快成、Batch 032）は同じ学校の可能性があるが、公式の表記だけでは断定できないため別Organizationのまま
- ポーグ健の「白?大学」は白鴎大学の可能性があるが、読めない文字を推測で補わず未登録（Batch 025のブラ ブサナ グロリダと同じ状況）

## 状態

CANDIDATE段階。Batch 032で作成したOrganizationを参照するため、Approval Sprint 009（Batch 032）の後に承認・反映する想定。
