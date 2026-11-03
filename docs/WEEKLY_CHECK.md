# B.PREMIER 週次チェックの手順

Yuichiの依頼（2026-11-03）「Bプレミアの選手の経歴が合っているかのチェックを定期的にしたい」→
選択：毎週（月曜の夜）／現所属＋新加入・退団／違いがあれば承認用の資料まで作る。

Governance v1.0（AGENTS.md）のとおり、RAW → CANDIDATE → QA → VERIFIED → HUMAN APPROVAL → MASTER を省略しない。
AIはMasterを承認しない。承認文をYuichiの代わりに書かない。週次の作業は**承認用の資料（Approval Sprint）まで**で止める。

## 1. ロスターを取る（RAW）

1. Claudeのブラウザ（Yuichiの端末）で `https://www.bleague.jp/roster/?tab=1&year=2026` を開く。
   B.LEAGUEのサイトはクラウド・端末のシェルからは接続できない（プロキシで拒否）。ブラウザだけが使える。
2. `scripts/browser/fetch_bleague_roster.js` の中身をそのまま javascript_tool で実行する（26クラブ、日本国籍・在籍中）。
3. 結果（`window.__tsv`）を `data/raw/research/bleague_roster_premier_<日付>.tsv` に保存する。先頭に `#` のヘッダー2行（前回のファイルと同じ形）。

## 2. Masterと照らし合わせる

```
python3 scripts/check_bleague_roster.py data/raw/research/bleague_roster_premier_<日付>.tsv
```

`data/raw/research/weekly_check_<日付>.md` に差分の一覧ができる（前回のスナップショットとMasterの両方と比べる）。

- 前回から一覧に新しく載った／一覧から消えた／クラブが変わった
- Masterの現所属と一覧のクラブが違う
- Masterに未登録（`weekly_check_excluded.tsv` の選手は除く）
- 登録しない選手の見直し時期（18歳になった選手など）

## 3. 差分を公式資料で確かめる

一覧は調べるきっかけで、それだけでは値にしない。差分ごとに次を開いて確かめ、`data/raw/research/weekly_check_<日付>_profiles.md` に表示どおり記録する。

- 選手プロフィール：`/roster_detail/?PlayerID=<id>`（生年月日、クラブ所属履歴、出身校）
- 退団の確認：そのクラブの `/roster/?tab=1&year=2026&club=<TeamID>&e=退団済&o=sort`
- 必要ならクラブ公式の発表

決まりごと：

- 18歳未満は登録しない（`weekly_check_excluded.tsv` に生年月日と見直す日を記す）。ケガや移籍理由は扱わない。
- シーズンの表し方：開始＝最初のシーズンの開始年、終了＝最後のシーズンの終了年。2026-27の在籍中は終了なし。
  2026-27シーズン中の退団は終了2027（平尾充庸 C001371、大友隆太郎 C001691と同じ）。
- 推測しない。確かめられないものは HOLD にして理由を書く。

## 4. CANDIDATE → VERIFIED → 承認用の資料

確かめた内容を `data/raw/research/weekly_spec_<日付>.json` に書く（例：`weekly_spec_2026-11-03.json`。キーは `scripts/weekly_pipeline.py` の説明を参照）。
空きIDは前回のSprint資料・Masterの最大値の次（Person・Career・Organization）。batch・sprintの番号も前回の次。

```
python3 scripts/weekly_pipeline.py candidate <spec>            # → commit（CANDIDATE）
python3 scripts/weekly_pipeline.py verified  <spec> <CANDIDATEのcommit>   # → commit（VERIFIED）
python3 scripts/weekly_pipeline.py packet    <spec> <VERIFIEDのcommit>    # → commit（資料）
```

差分がなかった週は、ロスターと照合結果だけをcommitし、「変化なし」と報告する。

## 5. 報告と承認

Yuichiに、差分・資料の中身・Tier案・HOLDを日本語で短く伝え、承認するなら**対象の版・範囲・Tier**を本人の言葉で書いてもらう。
承認後に限り：

1. `data/verified/approval_sprint_<NNN>/master_approval.md` に、承認のやり取りを原文のまま記録する（承認ID `APP-AS<NNN>-<日付>-01`、承認者・承認日・版）。
2. `python3 scripts/weekly_pipeline.py apply <spec> <資料のcommit> <承認ID> <VERIFIEDのcommit>`
3. `python3 scripts/build_site_master_data.py`（`site_registration.json` で自動登録される）→ commit。

## 6. Macへの反映

作業はYuichiのMacのリポジトリ（GitHub Desktop、iCloud）で行い、pushはYuichiがGitHub Desktopで行う。
gitがロックファイルを消せるよう、作業の最初に削除の許可（device_request_delete_permission、リポジトリのフォルダ）を求める。
