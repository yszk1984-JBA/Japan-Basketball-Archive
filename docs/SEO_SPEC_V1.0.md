# Rosterline SEO仕様書 v1.0

最終更新: 2026-10-06 ／ 作成: Claude（YUICHIさんとの壁打ちに基づく）

## 概要と前提

本仕様書は rosterline.jp への移行を前提として設計する。旧ドメイン（japanbasketballarchive.com）を据え置いたままSEO施策を進める方針は廃止し、ドメイン移行そのものをSEO施策の最初のステップとして位置づける。

移行作業（301リダイレクト、siteUrl更新、Search Console対応）の詳細は次節「ドメイン移行対応チェックリスト」にまとめる。本節以降のページタイプ別仕様（Player/School/Roster等）は、すべてrosterline.jp配下のURLを前提に記述する。

なお本仕様書はSEO・マーケティング設計のドキュメントであり、Governance v1.0が定めるRAW→CANDIDATE→QA→VERIFIED→HUMAN APPROVAL→MASTERの選手データ承認フローとは独立している。ただしsite/app/seo.tsxの変更やリダイレクト設定など、実際のサイトコードに触れる作業は、既存のデプロイフロー（ローカルでビルド・確認→Yuichiさんがpush→Cloudflare Workersが自動デプロイ）に従う。

## ドメイン移行対応チェックリスト

実施順に五つ。準備（コード）を最初に、Googleへの正式通知（Change of Address）を最後に行う。

| 実施順 | 作業 | 内容 | 場所 |
| --- | --- | --- | --- |
| 1 | siteUrl定数更新・再デプロイ | site/app/seo.tsx の `siteUrl` を `https://rosterline.jp` に変更。canonical/OGP/sitemap/JSON-LDのurlがこの定数から派生するため、変更後に数ページで出力先URLを目視確認する | コード（jba_repo）→ Yuichiさんpush → Cloudflare自動デプロイ |
| 2 | パス単位301リダイレクトマップ設定 | japanbasketballarchive.com の各URLを、ドメイン直下一括ではなくパスをそのまま引き継いでrosterline.jpの対応ページに転送する（例: `/players/yuki-kawamura` → `rosterline.jp/players/yuki-kawamura`） | Cloudflare（旧ドメインゾーン Redirect Rules） |
| 3 | 動作確認 | 代表的な旧URL数点（トップ、選手一人、一覧ページ）が301で正しく新URLに転送されることを確認 | ブラウザで実URLを確認 |
| 4 | 新規 Search Console プロパティ登録 | rosterline.jp を新規プロパティとして登録し、sitemap.xmlを提出 | Search Console |
| 5 | Change of Address（アドレス変更）実行 | 301が本番で機能していることを前提に、japanbasketballarchive.comの既存プロパティからアドレス変更ツールでrosterline.jpへの移行を正式通知。これが欠けると両ドメインが別サイトとして扱われ評価引き継ぎが遅れる | Search Console（旧プロパティ） |

※現在のCloudflare側の進捗: rosterline.jpのネームサーバーをお名前.com側で設定済み、DNS伝播待ちの段階。Activeになったら、japan-basketball-archive Workerにカスタムドメインとしてrosterline.jpを紐付ける作業が最初に必要。

## ページタイプ別仕様：Player（選手個別ページ）

| 項目 | 内容 |
| --- | --- |
| URL | `/players/{slug}`（既存方式を維持、ドメインはrosterline.jp） |
| title | `{選手名}（現所属あるいは直近所属）｜ Rosterline` |
| meta description | 経歴概要を1〜2文、所属変遷の要点を要約。文字数目安120〜160字 |
| H1 | 選手名（必要に応じてふりがな） |
| index方針 | 経歴データが一定量あるページは原則index。dataStatusが「情報不足」等でコンテンツが極めて薄いページはnoindexを検討（ゲーティング基準はs6で定義） |
| canonical | `https://rosterline.jp/players/{slug}`（seo.tsxのsiteUrlから派生） |
| OGP画像 | 選手写真は掲載しない方針（肖像権リスク、roadmap.mdの既定方針を継承）のため、汎用ロゴ/サイト共通画像を使用 |
| JSON-LD | `Person`を使用。`ProfilePage`は誤用のため使わない（GoogleのPerson/ProfilePageガイドラインは公約・公式ブロック団体前提で、本サイトは非公式アーカイブのため対象外）。主要プロパティ: `name`, `url`, `affiliation`（`Organization`型）。`sameAs`はSNS等が確定している場合のみ記述（未確定はNULL扱い） |
| Breadcrumb | Home › 選手一覧 › 選手名（`BreadcrumbList`） |
| 内部リンク | 所属組織（School/Organization）ページ、在籍していた年度のRosterページ（s5）へのリンクを本文中に設置 |

※選手の所属・経歴データ自体は、本仕様書とは別のGovernance v1.0（RAW→...→MASTER）を経て確定した値のみを表示対象とする。

## ページタイプ別仕様：School / Organization（学校・所属団体ページ）

※未確認事項: 学校・所属団体の個別詳細ページ（例: `/organizations/{slug}`）が現時点で実装済みかは本仕様書執筆時点で未確認。roadmap.mdでは「組織カテゴリのサブフィルタ」が今後の検討事項とされている。以下は、個別ページとして実装する場合の目標仕様。未実装の間は、選手一覧ページのカテゴリ絞り込み（`organization-category.ts`基準）がSEO上の受け皿となり、s6の方針に従う。

| 項目 | 内容 |
| --- | --- |
| URL | `/organizations/{slug}` |
| title | `{組織名} 出身選手一覧 ｜ Rosterline` |
| meta description | 当該組織に所属歴がある選手人数、代表的な選手名を要約 |
| H1 | 組織名 |
| index方針 | 所属選手が一定数以下（目安3名未満）のページは薄いコンテンツとしてnoindexを検討（最低人数の具体値はs6で別定） |
| JSON-LD | 組織種別に応じ `EducationalOrganization`（学校）または `SportsTeam`（プロクラブ等）。区分は`organization-category.ts`の分類に準拠 |
| Breadcrumb | Home › 学校・所属団体一覧 › 組織名 |
| 内部リンク | 所属選手一覧（Playerページへ）、在籍年度のRosterページ（s5）へのリンク |

※組織名の表記は、過去の歴定名称を現在の名称で上書きしないというGovernanceの原則をページ内容でもそのまま継承（改称歴がある場合は、現在名でURLを発行しつつ本文内で歴定名を表記）。

## ページタイプ別仕様：Roster（年度別名簿ページ）

roadmap.mdで12月実施予定とされている年度別ロースターページ構想に対応。「{組織名} {年度} 名簿」系のロングテール検索を狙うページ。組織×年度の組み合わせで大量にページが生成されるため、s6のページ品質ゲーティングを最も強く適用する対象。

| 項目 | 内容 |
| --- | --- |
| URL | `/organizations/{slug}/rosters/{year}`（案、要確定） |
| title | `{組織名} {年度}年度 名簿 ｜ Rosterline` |
| meta description | 当時在籍していた選手人数と代表選手名を要約 |
| H1 | `{組織名} {年度}年度 名簿` |
| index方針 | 在籍選手が一定数以上、かつSourceが紐付いている年度のみindex。データ欠損年度（空白期間）はnoindex、あるいはページ自体を生成しない |
| JSON-LD | `SportsTeam`（season情報を付与）を軸に、在籍選手を`ItemList`で列挙し各項目が対応するPlayerページを参照。詳細構造は実装時に要最終確定 |
| 内部リンク | 各選手のPlayerページ、所属組織ページ（s4）、前年度・次年度のRosterページ同士の相互リンク |

※注意点: 年度×組織の組み合わせ数が多く、機械的な大量生成になりやすいため、roadmap.mdの「有料広告・大量記事生成を避ける」方針と整合させ、Googleのscaled content abuseガイドラインにつながらないように、作成対象年度をデータが一定水準以上存在するものに限定する。

## 一覧・絞り込みページのindex/noindex方針

一覧ページ（`/players`等）とその絞り込みバリエーション（カテゴリ別・五十音別等のクエリパラメータ組み合わせ）は、ファセットナビゲーション固有の重複・薄いコンテンツ問題を避けるため、以下の方針で統一する。

- 正規の一覧ページ（パラメータなし、`/players`そのもの）はindex
- クエリパラメータによる絞り込みURL（`?category=xxx`等）は原則noindex、canonicalを正規一覧ページに向ける。クロール自体は許容してよいが、indexには含めない
- 静的パスとして切り出した代表的なページ（組織個別ページ・Rosterページ等）は、それぞれの節（s4・s5）の基準に従う

ページ品質ゲーティング（目安、最終値は選手データ量を見つつ要確定）:

| ページ種別 | indexの前提条件 | 条件未満時 |
| --- | --- | --- |
| Player | 経歴が1件以上、かつSourceが1件以上 | noindex |
| Organization | 所属選手が3名以上（目安） | noindex |
| Roster（年度別） | 在籍選手が一定数以上かつSourceあり | ページを生成しない |

Googleのscaled content abuseガイドラインは、類似構造の薄いページを機械的に大量生成しindexさせる行為を問題とするため、上記ゲーティングは例外を設けず徹底する。

## 構造化データ（JSON-LD）共通ルール

実装はsite/app/seo.tsxの既存ヘルパー（`baseOpenGraph`, `breadcrumbJsonLd`, `JsonLd`, `siteUrl`）を流用し、ページごとに実装を重複させない。

- **WebSite**: `name`は"Rosterline"、`url`は`siteUrl`。検索機能（sitelinks search box）を未実装のうちは`potentialAction`を含めない
- **Organization**（運営元自体の表示）: 公式団体ではない非公式アーカイブである旨は、構造化データではなくフッター注記・Aboutページで明示する（brand-name.mdで指摘済みの未実装の免責表記を仕上げる必要がある）。構造化データ上で選手との公式関係を示すプロパティ（組織側からの逆参照等）は付与しない
- **BreadcrumbList**: 各ページでH1直下の階層を`itemListElement`として記述。Home固定。例（選手ページ）:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://rosterline.jp/"},
    {"@type": "ListItem", "position": 2, "name": "選手一覧", "item": "https://rosterline.jp/players"},
    {"@type": "ListItem", "position": 3, "name": "（選手名）"}
  ]
}
```

※全ての`url`/`item`プレースホルダーは`siteUrl`（rosterline.jp）から生成される。旧ドメインの値が混入していないことを、siteUrl変更後に数ページで目視確認する（チェックリスト手順③の「動作確認」と共通）。

## 内部リンク設計方針とKPI整合

内部リンクの基本方針: Player ⇄ Organization ⇄ Roster間を相互リンクし、クロールバジェットを主要コンテンツに集中させる。一覧・絞り込みページ（s6）はクロールは許容するがindexの終着点にはしないため、評価の中継地点としてのみ機能させる。

roadmap.mdの優先順位（P0〜P3）との対応:

| 優先度 | roadmap.mdの項目 | 本仕様書での対応 |
| --- | --- | --- |
| P0 | 最新データ公開・Search Consoleサイトマップ再確認 | s2のドメイン移行チェックリスト（1〜3）に吸収 |
| P1 | ランキング/entry pages（学校のプロ輩出ランキング、クラブのOB一覧） | s4（Organization）/s5（Roster）のページ仕様が基盤 |
| P2 | sitemap lastmod修正、自動ページ要約、更新履歴/移籍ページ | 本仕様書の対象外（別途設計が必要） |
| P3 | 被リンク、ニュースレター、選手比較機能 | 本仕様書の対象外（roadmap.mdで管理継続） |

KPIは既存roadmap.mdの指標定義を継承し、Search Console（index数・表示回数・クリック数）、GA（セッション数）、X（インプレッション・リーチ）の3種のチャネルで計測する。ドメイン移行直後は旧プロパティ/新プロパティの両方をモニタリングし、評価引き継ぎが正常に進んでいるかを確認する。

※本仕様書の定めに従ってコード・設定を変更する場合、実際の変更は別の通常のデプロイ手順（コード修正→Yuichiさんpush→Cloudflare自動デプロイ）に従い、選手データ自体の承認プロセスは引き続き別途進行する。
