# Master訂正記録：重複Organizationの統合（白鷗大学・富田高校）

作成日：2026-10-01
承認者：Yuichi（この会話内での明示的な指示、2026-10-01）

## Yuichiの指示（原文、チャットでの返信をそのまま記録）

```
白鷗大学と白鴎大学をまとめる
「富田高校」と「私立富田高校」が同じ学校とする
```

## 経緯

- **白鷗大学**：`ORG000093`「白鷗大学」（batch_005、2026-09-21）と`ORG000208`「白鴎大学」（batch_017、2026-09-25）が、字体違い（鷗／鴎）で別Organizationとして登録されていた。B.LEAGUE公式プロフィールの表記は「白鴎大学」。batch_007 wave_11（2026-09-30）では同じ大学として扱い重複を作らないようにしたが、Master上の2行は残っていた（Approval Sprint 009・010の資料で「要判断」として提示）
- **富田高校**：`ORG000266`「私立富田高等学校」（batch_032、高橋快成）と`ORG000436`「富田高等学校」（batch_033、植田碧羽）。公式プロフィールの表記だけでは同じ学校と断定できないため別Organizationのまま反映し、Yuichiの判断を待っていた

## 判断

先に登録されたIDを残す（2026-09-23のORG000017→ORG000019の統合と同じ扱い）。

| 退役 | 統合先 |
| --- | --- |
| `ORG000208` 白鴎大学 | `ORG000093` 白鷗大学 |
| `ORG000436` 富田高等学校 | `ORG000266` 私立富田高等学校 |

## 反映内容（`scripts/apply_org_merge_2026_10_01.py`）

- `data/master/career.csv`：18件のCareerの`organization_id`を付け替え（白鴎大学17件、富田高等学校1件）。役割・期間は変更なし
- `data/master/evidence.csv`：上記Careerの`organization_id`エビデンス18件の`candidate_value`を統合先IDに変更。`source_locator`（「出身校（大）：白鴎大学」など、資料の表記）はそのまま残す
- `data/master/organization.csv`：`ORG000208`・`ORG000436`の行を削除（395件→393件）

## 影響範囲外

- `data/candidate/`・`data/verified/`のスナップショットは変更しない
- Person・Source・他のOrganizationは変更しない
- 公開サイト：退役IDの組織ページ（/organizations/org000208、/organizations/org000436）は統合先へ転送する

## 今後の横展開での扱い

`scripts/build_batch_032_roster.py`のbatch_032・033の設定は、確定済みスナップショットを再現するため変更しない。次のbatch（B.NEXTなど）を追加するときは、「白鴎大学」を`ORG000093`、「富田高等学校」を`ORG000266`へ寄せる設定をそのbatchに入れる。
