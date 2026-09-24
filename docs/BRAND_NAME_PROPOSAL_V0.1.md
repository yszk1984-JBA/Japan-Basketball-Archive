# ブランド名・表記の検討 v0.1

作成日：2026-09-24

状態：検討案。ブランド名、ドメイン取得、公開サイトの表記変更はいずれも未決定。

## 背景

[MONETIZATION_DRAFT_V0.1](MONETIZATION_DRAFT_V0.1.md)の未決定事項「『JBA』という略称が既存団体と混同されないためのブランド表記」への対応。「JBA」は公益財団法人日本バスケットボール協会の略称と重なり、商標や不正競争防止法（混同惹起）の観点でリスクがある。サイトが広まるほど変更しにくくなるため、早めに決める。

2026-09-24時点で、`site/`のサイト名は「Japan Basketball Archive」のフル表記で、ロゴは「J」の1文字であり、「JBA」という略称は使っていない。

## 方針

- A（先行実施）：ドメイン japanbasketballarchive.com は維持し、「JBA」という略称を使わないこと、非公式である旨の表記を徹底する。
- B（ブランド名確定後に判断）：新ブランド名でドメインを取得し、旧ドメインから301リダイレクトする。旧ドメインは数年間更新を続ける。

## Aの内容

### 表記ルール

- 「JBA」をサイト名、ロゴ、OGP、SNSの名前・プロフィールに使わない。
- 「公式」「協会」「認定」と読める表現を使わない。

### 免責表記案（フッターとAboutページ）

> 本サイトは、公益財団法人日本バスケットボール協会（JBA）、B.LEAGUE、その他の競技団体とは関係のない、個人が運営する非公式アーカイブです。掲載情報は公開資料に基づいており、出典を各ページに記載しています。

> This is an independent, unofficial archive and is not affiliated with the Japan Basketball Association (JBA), B.LEAGUE, or any other governing body.

公開サイトへの反映は、公開範囲・表示の判断と合わせてYuichiが決める。

## ブランド名の第一候補：Rosterline（ロスターライン）

- 意味：所属（roster）の線。採用したデザイン方向性（経歴を横軸の年表バーで表示するデータベース調）と名前が一致する。
- 表記案：「Rosterline｜日本バスケ経歴アーカイブ」。「roster」は日本では耳なじみが薄いため、日本語のサブタイトルを併記する。
- 2026-09-24の簡易Web検索では、同名のサービスは見当たらなかった。近い名前にRoster（roster.com、タレント管理）とRosterly（シフト管理アプリ）がある。

その他の候補：Courtlog（コートログ）、Hoop Ledger、Hoop Lineage、籠球録、籠球譜。

### ドメインの空き状況（2026-09-24、Yuichiがお名前.comとCloudflareで確認）

| 状態 | ドメイン |
| --- | --- |
| 取得済み（他者が保有） | rosterline.com / .app / .xyz / .ca / .co.uk |
| 空き | rosterline.jp、.org（Cloudflare：初年度$8.50、更新$11.20/年）、.net（$11.86/年）、.io、.co、.dev ほか |

- 本命の案：rosterline.jp。Cloudflare Registrarは.jpに対応していない想定のため、国内のレジストラで取得し、DNSをCloudflareに向ける。
- Cloudflareで完結させる場合の案：.org または .net。
- 初年度だけ安く、更新料が大きく上がるTLD（.online、.site、.store、.techなど）は避ける。
- 守りのために複数のドメインを買い集めることはしない。

## 確定前の確認事項

- rosterline.com と .app の使用状況。同じ分野の稼働サービスなら名前を再検討する。
- J-PlatPatでの商標検索：第35類・第41類・第42類。称呼は「ロスターライン」と「ロスター」で調べる。
- SNSのアカウント名：X、Instagram、LinkedIn。
- 有料化する場合は、新ブランド名の商標出願を検討する。
