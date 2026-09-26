# BATCH_019_PROPOSAL — 強豪校横展開 第2弾

作成日：2026-09-26

## 背景・目的

Batch 008〜018（強豪校11校）の一次調査がApproval Sprint 006でMasterへ反映されたことを受け、Yuichiの指示（2026-09-26）「選手のリサーチを継続」に対し、次の調査軸として「強豪校の第2弾」を選択（AskUserQuestionでの回答）。手順はBatch 008と同じく、B.LEAGUE公式の出身校タグ（`TagID=35:<学校名>`）を起点に、現役B.LEAGUE選手の最小経路Careerを登録する。

## 対象校の選定

B.LEAGUE公式タグで現役選手数を確認し（2026-09-26）、既存登録者を除いた新規人数で候補を提示。Yuichiが「主要5校＋小規模7校」を選択した。

| 順 | 学校名（タグ表記） | 都道府県 | タグ掲載 | 備考 |
| ---: | --- | --- | ---: | --- |
| 1 | 桐光学園高等学校 | 神奈川 | 9 | 齋藤拓実は既存登録 |
| 2 | 船橋市立船橋高等学校 | 千葉 | 8 | 「市立船橋高等学校」表記では0件 |
| 3 | 中部大学第一高等学校 | 愛知 | 11 | 選定時は要約ツールで6と記録。ブラウザ確認で11 |
| 4 | 尽誠学園高等学校 | 香川 | 6 | 渡邊雄太は既存登録 |
| 5 | 前橋育英高等学校 | 群馬 | 4 | |
| 6 | 正智深谷高等学校 | 埼玉 | 2 | |
| 7 | 帝京長岡高等学校 | 新潟 | 2 | |
| 8 | 桜丘高等学校 | 愛知 | 2 | 富永啓生は既存登録 |
| 9 | 秋田県立能代工業高等学校 | 秋田 | 1 | 「能代工業高等学校」表記では0件 |
| 10 | 報徳学園高等学校 | 兵庫 | 1 | |
| 11 | 大阪桐蔭高等学校 | 大阪 | 1 | |
| 12 | 近畿大学附属高等学校 | 大阪 | 1 | |

参考：福島東稜・京北・美濃加茂は、試した表記ではタグ掲載0件だった（表記ゆれの可能性があり、未確定）。

## スコープ

Batch 008と同じ（現役B.LEAGUE選手のみ、高校→大学→現所属クラブの最小経路、1校ずつ進めて都度報告、4人/Wave）。

## 進捗

| 学校 | 状態 |
| --- | --- |
| 1. 桐光学園高等学校 | Wave 1〜2完了（CANDIDATE段階、batch_019）。タグ9名のうち既存登録1名（齋藤拓実）を除く8名。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |
| 2. 船橋市立船橋高等学校 | Wave 1〜2完了（CANDIDATE段階、batch_020）。タグ8名全員が新規。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |
| 3. 中部大学第一高等学校 | Wave 1〜3完了（CANDIDATE段階、batch_021）。タグ11名全員が新規。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |
| 4. 尽誠学園高等学校 | 完了（CANDIDATE段階、batch_022、5名）。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |
| 5. 前橋育英高等学校 | 完了（CANDIDATE段階、batch_023、4名）。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |
| 6. 正智深谷高等学校 | 完了（CANDIDATE段階、batch_024、2名）。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |
| 7. 帝京長岡高等学校 | 完了（CANDIDATE段階、batch_025、2名）。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |
| 8. 桜丘高等学校 | 完了（CANDIDATE段階、batch_026、1名）。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |
| 9. 秋田県立能代工業高等学校 | 完了（CANDIDATE段階、batch_027、2名）。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |
| 10. 報徳学園高等学校 | 完了（CANDIDATE段階、batch_028、1名）。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |
| 11. 大阪桐蔭高等学校 | 完了（CANDIDATE段階、batch_029、1名）。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |
| 12. 近畿大学附属高等学校 | 完了（CANDIDATE段階、batch_030、1名）。HUMAN APPROVAL・VERIFIED・MASTERは未実施、Yuichiの指示待ち。 |

## 調査手順の注意

選手プロフィール上部の「出身校」には大学名のみが表示されることが多く、高校名はQ&A欄「出身校（高）」にある。要約型のWeb取得ツールは高校名や最新の所属履歴を取りこぼすことがあるため、値はブラウザで実ページから直接読み取る（詳細は`data/candidate/batch_019/README.md`）。

## 第2弾12校の一次調査完了（2026-09-26）

学校1〜12すべての一次調査が完了した（batch_019〜030、新規46名）。学校4〜12はYuichiの指示（「まとめてやって」）により一括で実施した。選定時の人数は要約型Web取得ツールによる暫定値で、実際の人数はブラウザ確認の結果（各batchのREADME）が正しい。能代工業については、関連する「秋田県立能代科学技術高等学校」タグの1名もbatch_027 Wave 2で登録し、Yuichiの判断（2026-09-26）により能代工業（ORG000159）と同じOrganizationとして扱った。

## Yuichiの判断の反映（2026-09-26）

- 能代科学技術高校は能代工業高校と同じ扱い（batch_027 Wave 2の中嶋正尭をORG000159に紐づけ）。
- ブラ ブサナ グロリダの出身大学（公式表示「白?大学」）は白鷗大学として登録（batch_025、C000768）。
- 若狭功希（出身大学「-」）は大学Careerなしのまま。所属履歴の空白年は推測せず記録のまま。
- 既存の重複登録（篠山竜青・高島紳司）はMASTER側のIDに統合し、候補側を取り下げた（batch_007 wave_10）。
