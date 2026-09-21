# Relationship Pilot 001 QAレポート

作成日：2026-09-21

## 結果

- 判定：PASS（データ形式レビューへ進められる）
- Membership候補：6件
- 派生関係プレビュー：15件
- Source：1件
- VERIFIED・Master・公開反映：未実施

## 確認内容

- 6人のperson_idと氏名が現在のMaster Personに一致する。
- organization_idは福岡第一高等学校に一致する。
- 全件に公式Sourceとプレイヤー表内の位置がある。
- 全件が同じ `competition:wc2018` と `official_team_roster` を持つ。
- 15組は6人から得られる全組合せで、重複と自己参照がない。
- 人物IDを昇順に正規化し、同じ関係が逆順で増えない。

## QA判断

公式ロスターは「大会時点で同じチームに登録されていた」ことを裏付ける。学校在籍期間全体、個別試合への出場、同時出場は裏付けない。

人物関係15件はMembership 6件から再現できるため、原本候補はMembershipとする。関係CSVは設計確認用の派生プレビューとして扱う。

## 次のゲート

[Membership Observation形式案](../../../docs/MEMBERSHIP_OBSERVATION_FORMAT_PROPOSAL_V0.1.md)についてYuichiの合意が必要。合意前にSCHEMA、VERIFIED、Master、公開サイトへ進めない。
