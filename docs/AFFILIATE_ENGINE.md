# Rosterline Affiliate Engine v0.1 — 設計案

作成日：2026-11-28
状態：**基本設計を承認（2026-11-28、Yuichi）→ `feature/affiliate-engine-v0.1`で実装済み（全案件無効）**。mainへのマージ・本番公開・広告の有効化は、実装結果を確認したうえでYuichiが最終承認する。この文書のcommitは広告掲載の承認ではない。

運用（広告の追加・停止・期限）は「13. 運用手順」、テスト結果は「16. テスト結果」を参照。

関連：[MONETIZATION_DRAFT_V0.1](MONETIZATION_DRAFT_V0.1.md)（Phase 2「関連商品のアフィリエイトを必要最小限で試験」の具体化）、[ROADMAP](ROADMAP.md)

---

## 0. 結論（先に読む）

- **既存Architectureの範囲で実装できる。** 新しいフレームワーク・DB・外部APIは不要。広告データは`site/app/affiliate/`配下のJSONで持ち、ビルド時に読み込む（`columns-data.ts`と同じ「手で編集する小さな設定データ」の扱い）。
- **バスケットボールデータ（`data/`、`master-data.ts`）には一切触れない。** 広告データは`data/`に置かない。Governance（RAW→MASTER）の対象外であることを明示するため。
- **収益の期待値は小さい。** 直近の検索流入は1日数十セッション規模で、EPC 4.63〜7.59円から見ると、Archiveページへの掲載だけでは月数百円規模にとどまる可能性が高い（下記「11. 収益の見立て」）。v0.1の目的は「売上」ではなく、**案件の追加・停止をコード修正なしで回せる土台と、どのページ・枠がクリックされるかの計測**とする。
- **選手ページには v0.1 では広告を出さない。** 「選手が商品を推奨している」と誤認されるリスクが最も高く、閲覧目的（経歴を知る）と購買意図のずれも大きいため。

---

## 1. 現在のArchitectureとの整合性（A）

| 項目 | 現状（2026-11-28、`main` @ `e75559c`） | Affiliate Engineでの扱い |
| --- | --- | --- |
| フレームワーク | vinext（Next.js互換API）＋React 19、Cloudflare Workers。`main`へのpushで自動デプロイ | そのまま使う。Server Componentで描画、クリック計測のみClient Component |
| ページ生成 | 選手・組織は`generateStaticParams`でビルド時生成 | 表示可否の判定（有効期限を含む）は**ビルド時点**で確定する。期限切れの反映には再デプロイが必要（後述J-7） |
| データ | CSV（`data/master`等）→Pythonで`site/app/master-data.ts`を生成 | **使わない・変更しない**。広告データは別ディレクトリ・別ファイル |
| 小さな設定データ | `columns-data.ts`（手書きの配列） | 同じ考え方。ただし後述の検証スクリプトをPythonで書くためJSON形式にする（`tsconfig`は`resolveJsonModule: true`で対応済み） |
| GA4 | `layout.tsx`でgtag直書き（`G-9QYZ1747RN`）。`ShareButtons.tsx`が`window.gtag?.('event','share',…)`を送る | 同じパターンで`affiliate_click`イベントを送る。新しい計測タグは入れない |
| AdSense | `layout.tsx`でスクリプト読込、`ads.txt`設置済み、審査は不承認（2026-11-25） | 触らない。Affiliate EngineはAdSenseと独立 |
| 規約表示 | `privacy/page.tsx`にAdSense・GAの記載あり。アフィリエイトの記載なし | アフィリエイト（A8.net・楽天）の記載を追加 |
| SEO | `seo.tsx`でcanonical・JSON-LD・noindex判定 | 変更しない。広告リンクは`rel="sponsored noopener"`で出す |

**懸念：** 広告データをJSONにすると、型は`types.ts`で付けるがJSON自体には型が効かない。誤記はビルド前の検証スクリプト（`scripts/check_affiliate_data.py`）で止める。

---

## 2. 実装設計（B）

### 2.1 データモデル（3層）

```text
Program（案件＝Affiliate Master）  1件 ── n件  Link（正式な広告素材＝Link Manager）
                                                   ↑
Placement（表示ルール）── 「どのページ種別・どの枠に・どのLinkを・何件まで」
```

**Program**（`programs.json`）— ASPとの提携単位

| フィールド | 例 | 説明 |
| --- | --- | --- |
| `id` | `AFF000001` | 安定ID。変更しない |
| `name` | スーパースポーツゼビオ | 表示名 |
| `asp` | `a8` / `rakuten` | ASP |
| `aspProgramId` | `s00000020001001` | ASP側のID（参照用、表示しない） |
| `partnershipStatus` | `pending` / `approved` / `rejected` / `ended` | **ASP管理画面で運営者が確認した提携状況** |
| `enabled` | `true` / `false` | 運営者の表示スイッチ（Enable / Disable） |
| `validFrom` / `validUntil` | `2026-12-01` / `null` | 掲載期間。`null`は期限なし |
| `termsCheckedAt` | `2026-11-28` | 報酬条件・掲載規約を最後に確認した日 |
| `reward` | `{ "rate": "6.5%", "note": "…" }` | 記録用。**サイトには表示しない** |
| `categories` | `["shoes","ball","club-gear"]` | 取扱カテゴリ（ルールの絞り込み用） |
| `restrictions` | `["no-minor-targeting?"]` | 掲載規約上の制約メモ（運営者が記入） |
| `notes` | | 自由記述 |

**Link**（`links.json`）— ASPが発行した広告素材そのもの

| フィールド | 例 | 説明 |
| --- | --- | --- |
| `id` | `LNK000001` | 安定ID |
| `programId` | `AFF000001` | 親Program |
| `kind` | `text` / `banner` / `product` / `raw` | 素材の種類 |
| `mode` | `fields` / `rawHtml` | 下記参照 |
| `href` | ASP発行URL（コピペ） | `mode: fields`のとき |
| `impressionPixel` | A8のインプレッション計測用画像URL（コピペ） | `mode: fields`のとき。ASPが発行した場合のみ |
| `rawHtml` | ASP発行コード全文（コピペ） | `mode: rawHtml`のとき。**一切改変せず出力** |
| `label` | ゼビオでバッシュを探す | テキスト。**ASPがテキストの変更を認めている素材だけ**運営者が設定 |
| `categories` | `["shoes"]` | Placementとの照合用 |
| `enabled` / `validUntil` | | Link単位のスイッチ・期限 |
| `issuedAt` | `2026-11-28` | 運営者がASPから取得した日 |

- `mode: fields`：ASPが「リンクURL＋計測画像」を分けて扱ってよい素材（自由テキスト型のテキストリンク等）。Rosterlineのデザインに合わせたボタンとして描画できる。
- `mode: rawHtml`：バナー・商品リンク等、ASP発行コードをそのまま貼る必要がある素材。HTMLを**無加工で**出力する。
- **どちらのモードを使ってよいかは素材ごとにASPの規約で決まる。** 推測で`fields`に分解しない（運営者がASPの規約・素材説明を確認して選ぶ）。

**Placement**（`placements.json`）— 表示ルール

```json
{
  "id": "PLC-column-end",
  "slot": "column-end",
  "pageTypes": ["column"],
  "pageKeys": ["high-school-trends", "how-to-research-careers"],
  "categories": ["shoes", "ball", "club-gear"],
  "maxItems": 2,
  "enabled": true,
  "heading": "部活・観戦に"
}
```

- `slot`：コンポーネントを置く位置の名前。ページ側は「枠」を置くだけで、何を出すかはルールが決める。
- `pageTypes`：`column` / `ranking` / `guide` / `archive`（選手・組織ページ。v0.1では使わない）
- `pageKeys`：特定ページに限定（パイロット用）。省略時は`pageTypes`の全ページ。
- `categories`：出してよいLinkのカテゴリ。
- 同じLinkを同じページに2回出さない。`maxItems`の上限を超えない。

### 2.2 表示判定（`select.ts`、純粋関数）

あるページの枠に表示するLinkは、次を**すべて**満たすものだけ：

1. Placementが`enabled: true`、かつ`slot`・`pageType`・（指定があれば）`pageKey`が一致
2. Programが`partnershipStatus: "approved"`かつ`enabled: true`
3. Programの`validFrom ≤ ビルド日 ≤ validUntil`（`validUntil: null`は期限なし）
4. Linkが`enabled: true`かつ期限内、`href`または`rawHtml`が空でない
5. Linkの`categories`がPlacementの`categories`と1つ以上重なる

該当が0件なら、**枠ごと（見出し・PR表記も含めて）何も描画しない**（`null`を返す）。

並び順はJSON上の記載順（固定）。v0.1ではローテーション・自動最適化はしない。

### 2.3 コンポーネント

```tsx
// ページ側（例：ColumnLayout.tsx の末尾）
<AffiliateSlot slot="column-end" pageType="column" pageKey={slug} />
```

- `AffiliateSlot`（Server Component）：`select.ts`で対象を決め、0件なら`null`。1件以上なら次の構造で描画：
  - 上部に **「PR」バッジ＋「広告（アフィリエイト）」** の表記と、「リンク先で購入・予約されると、運営者に報酬が支払われることがあります。」の一文
  - 各Link：`mode: fields`はボタン（`rel="sponsored noopener"`、`target="_blank"`）＋計測画像、`mode: rawHtml`はそのまま
- `AffiliateClickTracker`（Client Component）：枠のラッパーとしてクリックを拾い、GA4にイベントを送る。`rawHtml`の中身も改変せずに計測できるよう、**イベント委譲（枠のdivでclickを拾う）**で実装する。
- デザイン：既存`site-b.css`のトーン（`jbaListB-*`）に合わせ、本文と明確に区別できる枠線・背景にする。モバイルで1列、タップ領域44px以上、レイアウトシフトを起こさないよう画像はサイズ指定。

### 2.4 計測（GA4）

`ShareButtons.tsx`と同じ方式。

```ts
window.gtag?.('event', 'affiliate_click', {
  affiliate_id: 'AFF000001',
  link_id: 'LNK000001',
  asp_name: 'a8',
  page_type: 'guide',
  placement_id: 'PLC003',
  transport_type: 'beacon',
});
```

（実装では表示回数の`affiliate_impression`も送る。15.1参照）

- 成果（購入・確定）はASP側の管理画面で見る。GA4では「どのページ・枠がクリックされたか」だけを見る。
- GA4側で上記パラメータをカスタムディメンションに登録するのは運営者の作業（15.1参照）。
- 計測の失敗はリンク遷移に影響させない（`try/catch`）。

### 2.5 規約表示（Compliance）

- 枠ごとの「PR」「広告（アフィリエイト）」表記（上記）。
- `privacy/page.tsx`に「アフィリエイトプログラムについて」節を追加：A8.net・楽天アフィリエイトの利用、Cookie等による成果計測、広告主はデータ・順位に関与しないこと。
- `about/page.tsx`の「編集方針」に一文追加：広告・アフィリエイトは掲載データ・ランキングと分離し、選手・学校・クラブが商品を推奨するものではないこと。
- 広告の文言・見出しに**選手名・学校名・クラブ名を使わない**（例：「〇〇高校出身選手のバッシュ」は不可）。

---

## 3. 追加・変更するファイル（C）

**追加**

| ファイル | 内容 |
| --- | --- |
| `site/app/affiliate/types.ts` | Program / Link / Placement の型 |
| `site/app/affiliate/programs.json` | AFF000001〜004（初期は全件`partnershipStatus: "pending"`、`enabled: false`） |
| `site/app/affiliate/links.json` | 空配列（運営者がASPから取得したコードを入れるまで何も出ない） |
| `site/app/affiliate/placements.json` | パイロット用ルール（G参照） |
| `site/app/affiliate/select.ts` | 表示判定（純粋関数） |
| `site/app/affiliate/AffiliateSlot.tsx` | 共通広告枠（Server Component） |
| `site/app/affiliate/AffiliateClickTracker.tsx` | クリック計測（Client Component） |
| `scripts/check_affiliate_data.py` | JSONの検証（必須項目、ID重複、参照切れ、期限切れ・14日以内に切れる案件の警告、`href`のドメインがASPのものか） |
| `docs/AFFILIATE_ENGINE.md` | 本文書 |

**変更**

| ファイル | 変更内容 |
| --- | --- |
| `site/app/columns/ColumnLayout.tsx` | 記事末尾（「集計の前提」の後）に`<AffiliateSlot>`を1行追加 |
| `site/app/rankings/RankingPage.tsx` | 注記の後に`<AffiliateSlot>`を1行追加（表示するかはPlacementで制御） |
| `site/app/site-b.css` | 広告枠のスタイル |
| `site/app/privacy/page.tsx` | アフィリエイトの節を追加 |
| `site/app/about/page.tsx` | 編集方針に一文追加 |
| `docs/ROADMAP.md` | 収益化ワークストリームを追加 |
| `README.md` | 文書一覧に本文書を追加 |

**変更しない**：`data/`配下すべて、`site/app/master-data.ts`、`scripts/build_*`、`proxy.ts`、`layout.tsx`、選手・組織ページ、既存のURL。

（実装時の追加：Guideの新設に伴い`seo.tsx`（ヘッダー・フッターに「ガイド」）と`sitemap.ts`（`/guide`を追加、about・privacyの更新日）を変更した。実際の変更ファイルは「15. 実装したファイル」。）

---

## 4. 既存機能への影響（D）

| 対象 | 影響 |
| --- | --- |
| MASTER DATA・候補データ | なし（読み書きしない） |
| URL・サイトマップ・canonical | なし（新しいURLを作らない） |
| 検索機能（`TopSearch`、一覧の絞り込み） | なし |
| SEO | 広告リンクは`rel="sponsored"`。外部スクリプトは読み込まない（`rawHtml`がスクリプトを含む素材は v0.1 では採用しない、J-4） |
| 表示速度 | 画像バナー・計測画像の分だけ増える。パイロットページに限定し、Lighthouseで前後比較 |
| AdSense再申請 | 直接の影響はないが、広告的な要素が多いと「有用性の低いコンテンツ」と見られやすい。パイロットは1ページ1枠・最大2件に抑える |
| 案件が無い・無効のとき | 枠ごと非表示のため、現在の見た目と同じ |

---

## 5. 実装工数（E）

| 作業 | 目安 |
| --- | --- |
| 型・JSON・表示判定 | 2.0h |
| `AffiliateSlot`・計測・CSS | 2.5h |
| 検証スクリプト | 1.5h |
| 規約表示（privacy / about） | 1.0h |
| パイロット2ページへの組込み | 0.5h |
| ローカル確認（`tsc`・`oxlint`・`vinext build`・表示確認・GA4 DebugView） | 2.0h |
| 文書更新 | 0.5h |
| **合計（Claude側）** | **約10h（実作業1〜2セッション）** |
| 運営者側（ASPでの提携申請・素材取得・GA4設定・最終確認） | 約2〜3h |

---

## 6. 運営者が準備する情報（F）

案件ごとに、ASP管理画面で確認して次を用意する（Claudeは推測で埋めない）。

1. **提携状況**：承認済み／審査中／否認（A8.netは「提携中」になっているか、楽天は対象ショップ・サービスが成果対象か）
2. **広告素材**：使う素材のコード全文（コピペ）と、その素材が「テキストの変更可」か「改変不可（そのまま貼る）」か
3. **掲載規約**：禁止事項（掲載不可のサイト・ページの種類、リスティング・SNSの扱い、未成年向けの扱い、比較・ランキング表現、価格表記など）
4. **報酬条件の確認日**と、条件変更の通知を受け取る方法
5. **掲載開始日・終了日**（期間限定キャンペーン素材の場合）
6. **GA4**：管理画面で`affiliate_impression`／`affiliate_click`のパラメータ（`affiliate_id`、`link_id`、`asp_name`、`page_type`、`placement_id`）をカスタムディメンションに登録
7. **楽天の対象商品の方針**：「バスケットボール用品・書籍・グッズ」のうち、どの商品・検索結果ページにリンクするか（個別商品は在庫切れ・終売でリンク切れになりやすい）
8. **パイロットページの承認**（G）

---

## 7. 試験導入に適したページ（G）

**v0.1 パイロット（推奨）**

| ページ | 枠 | 候補案件 | 理由 |
| --- | --- | --- | --- |
| `/columns/high-school-trends` | 記事末尾 | ゼビオ／アルペン（部活用品のカテゴリリンク） | 高校バスケに関心がある読者（部活生・保護者）が来やすい。運営者の編集記事なので選手推奨の誤認が起きにくい |
| `/rankings/high-school` | 注記の後 | 楽天市場（バスケ用品）または書籍 | 出身高校ランキングはサイトの主要入口の一つ。表の後ろに置き、表との区別を明確にする |

**v0.1では出さない**

| ページ | 理由 |
| --- | --- |
| 選手詳細・選手比較 | 選手が商品を推奨していると誤認されやすい。閲覧目的と購買意図のずれも大きい |
| 組織詳細（高校・大学・クラブ） | 学校・クラブの推奨と誤認されやすい。高校ページは未成年の関係者の閲覧も多い |
| トップ・about・privacy・contact・updates | 信頼性に関わるページ |

**本命は Rosterline Guide**：「バスケットボールのサイズの選び方」など、購買の目的を持って検索される記事。v0.1の枠（`pageType: "guide"`）は先に用意し、記事の公開と同時に有効化する。最初の1本は、事実で書ける「ボールのサイズ（号数）の選び方」が手堅い（年代別の公式球の号数は競技規則で確認できる）。

---

## 8. テスト・デプロイ計画（H）

1. **開発ブランチ**：`feature/affiliate-engine-v0.1`で実装。`main`には入れない。
2. **安全な初期値**：全Programを`enabled: false`で実装をマージしても、サイトの見た目は変わらない（枠が出ない）状態にする。
3. **ローカル検証**：
   - `python3 scripts/check_affiliate_data.py`（データ検証）
   - `pnpm exec tsc --noEmit`、`pnpm lint`、`pnpm build`
   - `select.ts`の判定を表で確認（承認済み／審査中／無効／期限切れ／素材なし／カテゴリ不一致の各ケースで、表示されるか・枠ごと消えるか）
   - パイロット2ページをモバイル幅（375px）とPCで目視、PR表記の位置、リンク先が正しいASPドメインか
   - GA4 DebugViewで`affiliate_click`が届くか
4. **2段階のマージ**（いずれもYuichiの承認後、GitHub Desktopでpush）：
   - 段階1：コードのみ（全案件`enabled: false`）→ 本番で見た目が変わらないことを確認
   - 段階2：1案件だけ`approved`・`enabled: true`にして本番でクリック・ASP側のクリック計上を確認 → 残りを順次
5. **停止手順**：該当Programの`enabled`を`false`にしてcommit・push（Cloudflareの自動デプロイで反映、数分）。
6. **4週間後の振り返り**：枠別クリック数、ASP側の発生・確定、表示速度、AdSense再申請への影響を記録し、Guideへの展開を判断。

---

## 9. 将来の拡張（I）

| 段階 | 内容 | 前提 |
| --- | --- | --- |
| v0.2 | Rosterline Guide記事に枠を展開。案件追加（U-NEXT、DAZN、バスケットLIVE、J SPORTS等） | Guide記事の公開、各ASPでの提携 |
| v0.3 | 組織ページ（クラブのみ）に「観戦・遠征」枠（楽天トラベル） | ホームアリーナ所在地をどう持つか（Masterデータとは別の補助データ）の合意 |
| v0.4 | 枠別・案件別の月次レポート（GA4＋ASPのCSVを手動で取り込み集計） | 計測データが数か月分たまること |
| 将来 | スポンサー枠（Sponsor）、Insightsの有料レポートへの導線 | MONETIZATION_DRAFTのPhase 3以降 |

管理画面・商品API・自動最適化は、案件数が10件を超えるなど手作業の負担が実際に問題になってから検討する。

---

## 10. 規約・技術上の懸念（J）

1. **ステルスマーケティング規制（景品表示法、2023年10月施行）**：広告であることが一般の閲覧者に分かる表示が必要。枠ごとの「PR／広告」表記を必須とし、記事本文の中に紛れ込ませない。最終的な表記方法の妥当性は運営者が消費者庁の運用基準で確認する（本文書は法的判断ではない）。
2. **選手・学校・クラブの推奨との誤認**：選手ページ・組織ページに出さない、広告文言に固有名詞を使わない、で防ぐ。パブリシティ権の問題を避ける意味もある。
3. **ASPコードの改変禁止**：`rawHtml`は無加工で出力する。`fields`への分解は、ASPが認めている素材に限る（運営者が確認）。
4. **外部スクリプトを含む素材**：楽天のウィジェット等、`<script>`を含む素材は表示速度・レイアウトのずれ・Cookieの面で負担が大きいため v0.1 では使わない。
5. **未成年への訴求**：Guide記事「中学生／高校生のバッシュの選び方」は読者に未成年が多い。各ASP・広告主の掲載規約に未成年向けの制限がないか確認が必要（未確認）。サイトの方針（18歳未満の個人情報を掲載しない）とは別問題だが、記事では特定の未成年選手に触れない。
6. **`rel="sponsored"`**：Googleの方針どおり広告リンクに付与。付け忘れは検証スクリプトでは検出できないため、コンポーネント側で必ず付ける実装にする（ページごとに手書きしない）。
7. **有効期限の反映タイミング**：ページはビルド時に生成されるため、`validUntil`を過ぎても次のデプロイまで表示が残る。コラムを毎日追加しているためデプロイ頻度は高いが、期限の決まった素材は`validUntil`を1日前倒しで設定する。検証スクリプトで14日以内に切れる案件を警告する。
8. **AdSense再申請との関係**：アフィリエイト自体は禁止されていないが、広告比率が高く独自性の低いページは不承認の理由になりやすい。Guide記事は「アフィリエイトのための記事」ではなく、出典を示した実用記事として書く。
9. **確定率・報酬条件の変動**：入力データの報酬率・EPC・確定率は2026-11-28時点の値。変わる前提で`termsCheckedAt`を持ち、四半期ごとに再確認する。
10. **プライバシーポリシー**：A8.net・楽天の計測（Cookie等）について追記が必要。

---

## 11. 収益の見立て（参考、仮定を含む）

| 仮定 | 値 |
| --- | --- |
| パイロット2ページの月間閲覧 | 300〜1,000PV（未計測。GA4で要確認） |
| 広告枠のクリック率 | 0.5〜2% |
| 1クリックあたりの報酬（EPC） | 4.63〜7.59円（A8.net表示値、2026-11-28） |
| 月間の見込み | 約7〜150円 |

- 月数万円の水準には、**購買の目的で検索される記事（Guide）への流入**が月数万PV規模で必要になる。v0.1は「土台と計測」と割り切り、収益の判断はGuide公開後に行う。
- 閲覧者の目的（Jobs to Be Done）で見ると、Archiveの閲覧者の目的は「選手の経歴を知る」で、「用品を買う」ではない。Archiveにアフィリエイトを増やしても収益は伸びにくく、閲覧体験と信頼性のコストの方が大きくなる。収益の柱は引き続きInsights（独自データの分析・レポート）とData（B2B）と考える（MONETIZATION_DRAFT）。

---

## 12. 承認記録

2026-11-28、Yuichiが基本設計を承認（Program／Link／Placementの3JSON、`site/app/affiliate/`、data・master-data不変更、未提携・無効・期限切れ・素材未登録は非表示、初期は全案件無効、広告なしなら枠ごと非表示、GA4 `affiliate_click`、Privacy・About追記、選手・組織ページはv0.1で見送り）。パイロットは`/columns/high-school-trends`、`/rankings/high-school`に、**Rosterline Guide第1弾（`/guide/basketball-ball-size`）を追加**し、Archive系とGuideのクリック率を比較できるようにする。mainへのマージ・本番公開・広告有効化は実装結果の確認後に最終承認。

---

## 13. 運用手順（広告の追加・停止）

すべて`site/app/affiliate/`のJSONを編集してcommit・pushするだけで反映される（mainへのpushでCloudflareが自動デプロイ）。ページのコードは触らない。

### 13.1 案件を有効にする（例：ゼビオ）

1. A8.netで提携が「提携中」になっていることを確認する。
2. 使う広告素材のコードをA8.netからコピーする。**書き換えない。**
3. `links.json`に1件追加する（IDは連番）。

   ASPのコードをそのまま貼る場合（バナー・商品リンク）：

   ```json
   {
     "id": "LNK000001",
     "programId": "AFF000001",
     "kind": "banner",
     "mode": "rawHtml",
     "rawHtml": "（A8.netのコードを全文そのまま。\" はJSONのエスケープ）",
     "categories": ["ball", "shoes", "club-gear"],
     "enabled": true,
     "validUntil": null,
     "issuedAt": "2026-12-01"
   }
   ```

   リンクURLと計測用画像を分けて使ってよい素材（文言を変えてよいテキスト素材）の場合は`"mode": "fields"`にし、`href`・`impressionPixel`・`label`を入れる。どちらが許されるかは素材ごとのASPの規約で確認する。
4. `programs.json`の該当案件を`"partnershipStatus": "approved"`、`"enabled": true`にし、`termsCheckedAt`を確認日にする。広告主・ASPから指定の表記があれば`requiredDisclosure`に入れる（広告枠に表示される）。
5. 確認する：
   ```
   python3 scripts/check_affiliate_data.py
   cd site && node --test scripts/affiliate.test.mjs && pnpm build
   ```
   `check_affiliate_data.py`が`ERROR`を出したら、その素材は表示されない（許可していないタグ・属性・ドメインを含む等）。
6. commit・push（GitHub Desktop）。

### 13.2 案件を止める（通常）

`programs.json`の該当案件を`"enabled": false`にしてcommit・push。素材単位なら`links.json`の`enabled`を`false`にする。

### 13.3 緊急停止（すぐに全広告を止める）

1. `placements.json`の全ルールを`"enabled": false`にしてcommit・push（GitHubのWeb画面でファイルを直接編集してもよい）。
2. Cloudflareのダッシュボード（Workers & Pages → 対象のWorker → Deployments）でビルドが完了したことを確認する。数分かかる。
3. それでも急ぐ場合は、Cloudflareのダッシュボードで直前のデプロイにロールバックする（広告を有効にする前の版に戻る）。

### 13.4 表示ルールを変える

`placements.json`で、出すページ（`pageKeys`）・カテゴリー・件数（`maxItems`は1〜3）を変える。新しいページに枠を置くときだけ、ページに`<AffiliateSlot>`（記事なら上部に`<AffiliateNotice>`も）を1行追加する。

### 13.5 ショップ名の表示と、リンクの飛び先の制限

- 広告枠のボタンにショップ名を出すのは、`programs.json`の`displayName`を設定した案件だけ。広告主の規約で社名・商標の記載が制限されていることがあるため、規約を確認して表示してよいと分かった場合だけ設定する（初期値はすべて`null`＝表示しない）。
- `allowedDestinations`を設定した案件は、A8.netの自由テキスト・商品リンクの飛び先（`a8ejpredirect`）がその範囲外なら表示しない（検証スクリプトもERRORにする）。

### 13.6 案件ごとの掲載条件（確認済みのもの）

**AFF000001 スーパースポーツゼビオ**（A8.net、2026-11-28確認、提携中・提携日2026-11-28・終了日未定）

| 条件 | Rosterlineでの対応 |
| --- | --- |
| 商品リンク・自由テキストの飛び先は`https://www.supersports.com/ja-jp/xebio/`内 | `allowedDestinations`に設定。範囲外の素材は表示しない |
| 生成されたリンクは変更しない（計測用パラメーター付き） | コードをそのまま登録する |
| 社名（ゼビオ株式会社／株式会社ヴィクトリア）・コピーライト・商標の記載・転載不可 | `displayName: null`（ボタンにショップ名を出さない）。リンクテキストにも店名・社名を入れない |
| 画像加工不可 | バナーはASPのコードのまま使う |
| サイト名・ページタイトル・コンテンツがゼビオと誤解されるような構成は禁止 | 記事タイトル・見出しに店名を使わない |
| 広告とわかる表示をファーストビュー等わかりやすい位置に | 記事上部のPR表記＋広告枠の「PR｜広告（アフィリエイト）」 |
| 成果条件：WEB注文後30日の入金確認。否認：抽選・予約・先行販売商品、Nike Mind 001等 | 記録のみ |
| 「ゼビオ」等のリスティング広告は禁止 | 当サイトはリスティング広告を出さない |

未確認：店名を含まないリンクテキストでの運用で問題がないか（例：「バスケットボールを通販で探す」）。店名入りのテキストにしたい場合は、A8.netの「広告主お問い合わせ」で確認してから`displayName`・テキストを変える。

### 13.7 ASPの許可ドメインを増やす

広告素材の画像やリンクが`a8.net`／`rakuten.co.jp`／`r10s.jp`以外のドメインを使っている場合、その素材は表示されない。素材が正式なものであることを確認したうえで、`select.ts`の`ASP_ALLOWED_HOSTS`と`check_affiliate_data.py`の`ASP_ALLOWED_HOSTS`を同じ内容に変更する。

---

## 14. 有効期限の管理

ページはビルド時に作られるため、期限切れの広告が次のデプロイまで残るリスクがある。v0.1では次の4段で防ぐ。

| 段 | 仕組み | いつ効くか |
| --- | --- | --- |
| 1. ビルド時の除外 | `select.ts`がビルド時点（日本時間）の日付で期限切れ・開始前を除外 | デプロイのたび |
| 2. 閲覧時の非表示 | 広告ごとに`data-aff-until`（最終表示日）を埋め込み、閲覧者のブラウザで日付を過ぎた広告を隠す。全件切れたら枠・PR表記も隠す | 期限の翌日0時（日本時間、閲覧者の端末時刻）から |
| 3. 毎日の検証 | GitHub Actions（`.github/workflows/affiliate-check.yml`）が毎日0:05（日本時間）に`check_affiliate_data.py`を実行。表示中の案件の期限切れ・不正な素材があれば失敗し、GitHubの通知メールが届く。14日以内に切れる案件は警告 | 毎日 |
| 4. 毎日の再ビルド（任意） | 期限を設定した表示中の案件があるときだけ、同じワークフローがCloudflareのDeploy Hookを呼んでサイトを作り直す | Secretsを登録した場合のみ |

- 段2は、JavaScriptが無効な環境では効かない。また、期限切れの広告のHTMLが一瞬表示され、計測用画像が読み込まれる可能性がある。保証の本体は段1＋段4（毎日の再ビルド）で、段2は再ビルドまでの間を埋める安全策。
- 段4を使うには、運営者が(1) CloudflareでDeploy Hookを作成（Workers & Pages → 対象のWorker → Settings → Builds → Deploy Hooks、ブランチは`main`）、(2) GitHubのリポジトリ設定（Settings → Secrets and variables → Actions）に`CLOUDFLARE_DEPLOY_HOOK_URL`として登録する。現在のデプロイがCloudflare Workers Buildsで行われていることは未確認（READMEの「GitHubへのpushでCloudflareが自動デプロイ」から推定）。
- スケジュール実行はmainブランチのワークフローだけが動く。mainへのマージ後から有効になる。
- **失敗時の対応**：通知メールが届いたら、Actionsのログで`ERROR`の行を確認し、該当案件を`enabled: false`にしてpushする（13.2）。段4が動いていれば、期限切れの広告はその日の再ビルドで既に消えている。

---

## 15. 実装したファイル

| ファイル | 内容 |
| --- | --- |
| `site/app/affiliate/types.ts` | 型 |
| `site/app/affiliate/programs.json` / `links.json` / `placements.json` | 広告データ（初期：全案件`pending`・`enabled: false`、素材0件） |
| `site/app/affiliate/data.ts` | JSONの読み込み |
| `site/app/affiliate/select.ts` | 表示判定・rawHtmlの検査・期限判定（純粋関数） |
| `site/app/affiliate/AffiliateSlot.tsx` | 広告枠と記事上部のPR表記（Server Component） |
| `site/app/affiliate/AffiliateClient.tsx` | 計測（click／impression）と期限切れの非表示（Client Component） |
| `site/app/guide/guide-data.ts` / `GuideLayout.tsx` / `page.tsx` | Rosterline Guide（`/guide`）。コラムとは別セクション |
| `site/app/guide/basketball-ball-size/page.tsx` | Guide第1弾 |
| `site/scripts/affiliate.test.mjs` | 表示判定のテスト（13件） |
| `scripts/check_affiliate_data.py` | データ検証 |
| `.github/workflows/affiliate-check.yml` | 毎日の検証・任意の再ビルド |
| 変更：`columns/ColumnLayout.tsx`、`rankings/RankingPage.tsx` | PR表記と広告枠を1行ずつ（表示はPlacementで制御） |
| 変更：`seo.tsx`、`sitemap.ts` | ヘッダー・フッターに「ガイド」、サイトマップに`/guide` |
| 変更：`privacy/page.tsx`、`about/page.tsx` | アフィリエイト、運営と収益化の方針 |
| 変更：`site-b.css` | 広告枠・PR表記・Guideの表、モバイルのナビ間隔 |

### 15.1 GA4計測

| イベント | 送るタイミング | パラメータ |
| --- | --- | --- |
| `affiliate_impression` | 各広告が画面に50%以上入ったとき（ページ表示ごとに1回） | `affiliate_id`、`link_id`、`asp_name`、`page_type`、`placement_id` |
| `affiliate_click` | 広告内のリンクのクリック・中クリック（`transport_type: beacon`） | 同上 |

- 送るのは広告の識別子だけ。個人情報・入力内容は送らない。ページのURLはGA4が通常どおり`page_location`として記録する。
- クリックは成約・売上ではない。成果（発生・確定）はASPの管理画面で見る。
- **比較の見方（運営者のGA4設定）**：管理 → カスタム定義で、上の5つをイベントスコープのカスタムディメンションに登録する。探索（自由形式）で、行＝`page_type`（または`affiliate_id`）、値＝イベント数、フィルタ＝イベント名が`affiliate_impression`／`affiliate_click`の2つを作れば、Archive／Ranking／Column／Guide別の表示回数・クリック数を比べられる。クリック率＝クリック数÷表示回数（探索の表をエクスポートして計算）。
- クリックは枠でまとめて受け取り（イベント委譲）、`preventDefault`しないため、リンクの遷移とASP側の計測を妨げない。

### 15.2 セキュリティ

- `rawHtml`は運営者がJSONに登録したものだけ。表示前に許可リストで検査し、通らない素材は表示しない（コードは書き換えない）。
  - 許可するタグ：`a`、`img`、`br`、`span`、`div`、`p`、`table`、`tbody`、`tr`、`td`、`strong`、`b`
  - 許可する属性：`href`、`src`、`alt`、`title`、`width`、`height`、`border`、`style`、`target`、`rel`、`class`
  - `href`・`src`はhttpsで、案件のASPの許可ドメインのみ。`script`・`iframe`・`style`要素、`on…`イベント属性、`javascript:`、styleの`url()`等は拒否
- 外部スクリプトは読み込まない（楽天のウィジェット等、`<script>`を含む素材はv0.1では使えない）。
- CSP（Content-Security-Policy）は現在サイトに設定されていない。将来CSPを入れる場合は、`img-src`にASPの画像ドメイン（`*.a8.net`、`*.rakuten.co.jp`、`*.r10s.jp`）を加える必要がある。
- `fields`の広告リンクには`rel="sponsored noopener"`を付ける。`rawHtml`はASPのコードのまま（A8.netの`rel="nofollow"`等）。

---

## 16. テスト結果（2026-11-28、`feature/affiliate-engine-v0.1`）

| 確認 | 結果 |
| --- | --- |
| 表示判定のテスト（`node --test scripts/affiliate.test.mjs`） | 13件すべて成功（2026-11-28追加：広告主指定の飛び先の範囲外は非表示）（初期データで広告が出ない／承認済み・有効・期限内・正式素材ありだけ表示／未提携・否認・終了・無効・期限切れ・開始前・素材なし・不正URL・カテゴリー不一致は非表示／maxItems・重複／A8・楽天の標準形のrawHtmlを通し、script・iframe・onclick・javascript:・許可外ドメインを拒否） |
| データ検証（`check_affiliate_data.py`） | 初期データでOK。表示中案件の期限切れ・`<script>`入り素材でERROR、14日以内の期限でWARNINGを確認 |
| 型チェック（`tsc --noEmit`） | エラーなし |
| Lint（`oxlint`） | 追加・変更したファイルにエラーなし（`components/ui`等の既存の19件はmainと同数） |
| ビルド（`vinext build`） | 成功（`/guide`、`/guide/basketball-ball-size`を含む） |
| 初期データでの表示 | 3つのパイロットページ・選手ページとも、広告枠・PR表記なし。全ページ200、サイトマップに`/guide`2件、コラム一覧にGuideは出ない |
| テスト用の素材を一時的に有効にした表示（確認後に元に戻した） | 3ページで記事上部のPR表記と広告枠が表示。`onclick`入りの素材は除外。モバイル幅（375px）で表示崩れなし |
| GA4イベント（ブラウザでの確認。GA4本番には送らず、ページ内の送信内容を記録） | `affiliate_impression`が広告ごとに1回、`affiliate_click`がクリック時に送られ、パラメータ5項目が正しいことを確認。クリックで新しいタブが開く（遷移を止めていない） |
| 期限切れの閲覧時非表示 | ブラウザの日付を期限の翌日にすると、該当の広告だけが隠れ、計測も送られないことを確認 |

未確認：本番環境（Cloudflare）での動作、実際のASP素材での表示とASP側のクリック計上、GA4管理画面での受信、Deploy Hookの動作。
